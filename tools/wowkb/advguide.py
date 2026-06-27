"""Build the Adventure Guide data for the M+ Memory Trainer's Guide mode.

Recreates the in-game Adventure Guide as structured JSON — sourced *only* from
Blizzard data (no Method/Icy Veins). Two joins:

    journal-encounter/{enc}   (Game Data API) → boss lore, per-role tips, the
                                                 nested ability tree, loot, and
                                                 the parent instance ref
    journal-instance/{id}     (Game Data API) → dungeon lore + location
    Spell* DB2 (wago.tools)                   → resolve each ability's name and
                                                 description (the AG ability text
                                                 is the linked spell's tooltip)

The spell tooltip text uses Blizzard's template syntax; a small parser resolves
it from sibling DB2 tables (see `resolve()`):
    $sN  effect value · $tN/$t tick period   (SpellEffect)
    $d   duration                            (SpellMisc → SpellDuration)
    $@spellnameN  cross-ref name             (SpellName)
    $@spelldescN  cross-ref description      (recurse into Spell)
    $?DIFFn[..][..]  difficulty branch       (first branch taken)

Why this exists: the web `/data/wow/spell/{id}` endpoint only exposes
player-facing spells — boss-ability spells 404 — so the descriptions must come
from the DB2 `Spell.Description_lang`, which wago.tools mirrors. See
`projects/mplus_memory/journal-text-investigation.md` for the full rationale.

Like `bossart.py`, the boss roster is read from the committed
`knowledge/endgame/mythic-plus/<dungeon>.md` headings (`### <Boss> <!-- enc:NNN
-->`), NOT the gitignored `raw/` cache — so a clean checkout can regenerate. The
DB2 tables are auto-downloaded into `raw/wago/` if missing.

Output (default): projects/mplus_memory/app/src/adventure-guide.json

Usage:
    uv run python -m wowkb.advguide               # all 8 dungeons
    uv run python -m wowkb.advguide --only skyreach pit-of-saron
    uv run python -m wowkb.advguide --refresh-db2 # re-pull the DB2 tables first
    uv run python -m wowkb.advguide --out path.json
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from ._common import RAW, ROOT
from .blizzard import get
from .wago import download as wago_download

MPLUS_DIR = ROOT / "knowledge" / "endgame" / "mythic-plus"
DEFAULT_OUT = ROOT / "projects" / "mplus_memory" / "app" / "src" / "adventure-guide.json"
WAGO_DIR = RAW / "wago"
DB2_TABLES = ("Spell", "SpellName", "SpellEffect", "SpellMisc", "SpellDuration", "SpellRadius")

# `### <name> <!-- enc:NNN -->` — shared with bossart.py.
HEADING_RE = re.compile(r"^###\s+(.+?)\s*<!--\s*enc:(\d+)\s*-->", re.MULTILINE)
ROLE_TITLES = ("Damage Dealers", "Healers", "Tanks")

csv.field_size_limit(10_000_000)


def slugify(name: str) -> str:
    """Mirror build-content.mjs / bossart.py slugify()."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def clean_boss_name(heading: str) -> str:
    return re.sub(r"\s*\((?:[a-z][\w-]*\s+)?\d+\)\s*$", "", heading, flags=re.I).strip()


def parse_bosses(md_path: Path):
    """Yield enc_id for each boss heading, in file order."""
    for m in HEADING_RE.finditer(md_path.read_text(encoding="utf-8")):
        yield int(m.group(2))


# ---------------------------------------------------------------- DB2 loading

def ensure_db2(refresh: bool) -> None:
    """Download the Spell* tables into raw/wago/ if missing (or if --refresh-db2)."""
    for table in DB2_TABLES:
        path = WAGO_DIR / f"{table}.csv"
        if refresh or not path.exists():
            print(f"  · db2: fetching {table} …")
            wago_download(table, None)


def load_db2():
    spell = {r["ID"]: r for r in csv.DictReader(open(WAGO_DIR / "Spell.csv", encoding="utf-8"))}
    names = {r["ID"]: r["Name_lang"] for r in csv.DictReader(open(WAGO_DIR / "SpellName.csv", encoding="utf-8"))}
    eff: dict[str, dict[str, dict]] = {}
    for r in csv.DictReader(open(WAGO_DIR / "SpellEffect.csv", encoding="utf-8")):
        eff.setdefault(r["SpellID"], {})[r["EffectIndex"]] = r
    dur_idx = {r["ID"]: r["Duration"] for r in csv.DictReader(open(WAGO_DIR / "SpellDuration.csv", encoding="utf-8"))}
    misc: dict[str, str] = {}
    for r in csv.DictReader(open(WAGO_DIR / "SpellMisc.csv", encoding="utf-8")):
        sid = r["SpellID"]
        if sid not in misc or r.get("DifficultyID") == "0":  # prefer the base difficulty row
            misc[sid] = r["DurationIndex"]
    rad_idx = {r["ID"]: r["Radius"] for r in csv.DictReader(open(WAGO_DIR / "SpellRadius.csv", encoding="utf-8"))}
    return spell, names, eff, dur_idx, misc, rad_idx


# ---------------------------------------------------------------- tooltip parser

def _secs(ms: str) -> str:
    try:
        v = float(ms) / 1000.0
        return str(int(v)) if v == int(v) else f"{v:g}"
    except (TypeError, ValueError):
        return "?"


def _num(v: str) -> str:
    try:
        return str(int(round(float(v))))
    except (TypeError, ValueError):
        return v


# DifficultyIDs the trainer emulates: Mythic Keystone (8) and Mythic (23). Journal
# text is gated by `$?diffN|…[A][B]` conditionals — diff1|diff2 = Normal/Heroic,
# diff8|diff23 = Mythic-tier — and a Mythic+ guide takes the Mythic branch.
MPLUS_DIFFICULTIES = {"8", "23"}


def _diff_true(cond: str) -> bool:
    """Whether a `$?` condition holds under the Mythic+ lens. A condition is an
    OR-list of `diffN` tokens (sometimes with a leading `|`); no diff token in it
    (a malformed/empty condition) defaults to true so its text is kept."""
    diffs = re.findall(r"diff(\d+)", cond, re.I)
    return (not diffs) or any(d in MPLUS_DIFFICULTIES for d in diffs)


def make_resolver(spell, names, eff, dur_idx, misc, rad_idx):
    """Return resolve(spell_id) → the spell's description with $-tokens filled in."""

    def spell_radius(ref: str) -> str | None:
        """The first non-zero radius (yards) across spell `ref`'s effects, or None.

        The digit in an `$...Ax` token is unreliable (it names a radius slot or
        effect index inconsistently — for some spells the value sits on effect 0
        regardless of the digit, in the _1 slot rather than _0), so scan all
        effects and both slots and take the first real radius. Area-trigger
        spells (Effect 179, aura fields) carry no SpellRadius row at all → None.
        """
        for _, e in sorted((eff.get(ref) or {}).items()):
            for slot in ("EffectRadiusIndex_0", "EffectRadiusIndex_1"):
                rv = rad_idx.get(e.get(slot))
                if rv and rv not in ("0", "0.0"):
                    return _num(rv)
        return None

    def resolve(sid, depth: int = 0) -> str:
        row = spell.get(str(sid))
        if not row:
            return f"<spell {sid}>"
        t = row["Description_lang"] or ""
        if not t:
            return ""
        # Difficulty conditionals: $?<cond>[mythic][else] or single-bracket
        # $?<cond>[mythic]. Take the branch true under the Mythic+ lens. Looped to
        # resolve chained/sequential conditionals; the two-bracket form tolerates a
        # stray space between brackets (some entries are authored that way).
        def _branch(m, two):
            return (m.group(2) if _diff_true(m.group(1)) else (m.group(3) if two else ""))
        for _ in range(6):
            # re.S: branch bodies can contain newlines ("…Piles.\n\nThe stomp…").
            t2 = re.sub(r"\$\?([A-Za-z0-9|&!]*)\[(.*?)\]\s*\[(.*?)\]", lambda m: _branch(m, True), t, flags=re.S)
            t2 = re.sub(r"\$\?([A-Za-z0-9|&!]*)\[(.*?)\]", lambda m: _branch(m, False), t2, flags=re.S)
            if t2 == t:
                break
            t = t2
        t = re.sub(r"\$\?[A-Za-z0-9|&!]*", "", t)  # strip any bracketless leftovers
        if depth < 4:
            t = re.sub(r"\$@spelldesc(\d+)", lambda m: resolve(m.group(1), depth + 1), t)
        t = re.sub(r"\$@spellname(\d+)", lambda m: names.get(m.group(1), "?"), t)

        def effval(m):  # $sN / $tN, optionally prefixed with an explicit spell id
            ref, kind, n = m.group(1) or str(sid), m.group(2), m.group(3)
            e = eff.get(ref, {}).get(str(int(n) - 1))
            if not e:
                return m.group(0)
            if kind == "s":
                return _num(e.get("EffectBasePointsF") or e.get("EffectBasePoints"))
            return _secs(e.get("EffectAuraPeriod"))  # kind == "t"
        t = re.sub(r"\$(\d+)?([st])(\d)", effval, t)

        def bare_t(m):  # bare $t → first periodic effect's tick
            for i in ("0", "1", "2"):
                e = eff.get(str(sid), {}).get(i)
                if e and e.get("EffectAuraPeriod", "0") not in ("0", "", "0.0"):
                    return _secs(e["EffectAuraPeriod"])
            return m.group(0)
        t = re.sub(r"\$t\b", bare_t, t)

        def durval(m):  # $d / $dNNN / $D / $idD  (the template casing varies)
            di = misc.get(m.group(1) or str(sid))
            return _secs(dur_idx.get(di)) + " sec" if di else m.group(0)
        t = re.sub(r"\$(\d+)?[dD]\b", durval, t)

        def radval(m):  # $Ax / $idAx → the referenced spell's radius in yards
            r = spell_radius(m.group(1) or str(sid))
            return r if r is not None else m.group(0)
        t = re.sub(r"\$(\d+)?[Aa]\d", radval, t)

        # Drop absolute damage/heal magnitudes. For NPC abilities these are scaled
        # server-side at runtime (keystone level × creature stats); the static DB2
        # base point (e.g. "12 Nature damage") is a placeholder, never the number a
        # player actually takes. Durations, tick periods, and radii are fixed, so
        # those numbers survive. A magnitude is a number (with a leading digit, so a
        # bare comma can't be swallowed), or a `$…`/`${…}`/`$<…>` value token that
        # didn't resolve, sitting just before "damage"/"healing". Percentages
        # ("75% increased damage") survive — the "%" breaks the value-then-keyword
        # adjacency this matches on.
        mag = r"(?:\d[\d,]*(?:\.\d+)?|\$\{[^}]*\}|\$<[^>]*>|\$\d*[A-Za-z]+\d*)"
        t = re.sub(rf"\b{mag}\s+((?:[A-Z][a-z]+\s+)?(?:damage|healing))\b", r"\1", t)
        # Some entries write the amount with no "damage" noun ("inflicting 25 to
        # players"); the bare value is just as meaningless, so name it generically.
        t = re.sub(r"\b(inflicts?|inflicting)\s+\d[\d,]*(?:\.\d+)?\s+(to\b)", r"\1 damage \2", t)
        t = re.sub(r"\bby\s+\$<[^>]*>%?\s*", "", t)  # "...by $<reduction>% for 3 sec" → drop the value

        # A handful of radius/period/duration tokens reference data these tables
        # don't carry (area-trigger radii, odd `${expr}` periods). Drop the whole
        # carrier clause so the prose stays grammatical rather than leaking a token.
        t = re.sub(r"\s*\b(?:within|of)\s+\$\S+\s+(?:yards?|yds?)\b", "", t)
        t = re.sub(r"\s*\bevery\s+\$\S+\s+sec\b", "", t)
        t = re.sub(r"\s*\bfor\s+\$\S+", "", t)
        t = re.sub(r"\$\{[^}]*\}|\$<[^>]*>|\$[0-9A-Za-z@]+", "", t)  # safety net: any stray token

        t = re.sub(r"\s+([.,;])", r"\1", t)  # tidy space before punctuation
        return re.sub(r"\s+", " ", t).strip()

    return resolve


def _bullets(s: str):
    return [b.strip() for b in (s or "").replace("$bullet;", "•").split("•") if b.strip()]


def ability_node(sec, resolve):
    """Convert a journal ability section into a node, preserving the child tree."""
    sp = sec.get("spell")
    node = {
        "name": sp["name"] if sp else sec.get("title"),
        "spellId": sp["id"] if sp else None,
        "text": resolve(sp["id"]) if sp else (sec.get("body_text") or ""),
        "children": dedupe_abilities([ability_node(c, resolve) for c in (sec.get("sections") or [])]),
    }
    if not node["children"]:
        node.pop("children")
    return node


def dedupe_abilities(nodes: list[dict]) -> list[dict]:
    """Collapse sibling ability nodes that share a name (case-insensitive).

    The Blizzard journal routinely lists an ability twice under one boss: either
    the *identical* spell repeated, or an old + a Midnight-retuned spell id sharing
    a display name (e.g. Crawth's "Deafening Screech" → 377004 and 454341). The
    in-game Adventure Guide de-dupes these; the raw API does not.

    Keep the entry with the **highest spell id** — the most recently issued spell,
    which is the current-patch version — and drop its twins. (First-occurrence
    order is unreliable: the journal lists the new id first for Crawth but last
    for every other collision.) Operates per sibling list, so genuinely distinct
    same-named abilities under *different* parents are never merged. The kept
    node keeps its own subtree; callers dedupe children before passing them in.
    """
    out: list[dict] = []
    by_name: dict[str, dict] = {}
    for n in nodes:
        key = (n.get("name") or "").strip().lower()
        kept = by_name.get(key)
        if kept is None:
            by_name[key] = n
            out.append(n)
        elif (n.get("spellId") or 0) > (kept.get("spellId") or 0):
            out[out.index(kept)] = n  # newer id wins; hold the original position
            by_name[key] = n
    return out


# ---------------------------------------------------------------- build

def build_boss(enc: int, dungeon_slug: str, resolve) -> dict:
    e = get(f"/data/wow/journal-encounter/{enc}", "static")
    boss = {
        "name": e["name"],
        "slug": slugify(e["name"]),
        "artKey": f"{dungeon_slug}__{slugify(e['name'])}",
        "encounterId": enc,
        "lore": e.get("description"),
        "roleTips": {},
        "abilities": [],
        "loot": [{"id": it["item"]["id"], "name": it["item"]["name"]} for it in e.get("items", [])],
    }
    for sec in e.get("sections", []):
        if sec.get("title") == "Overview":
            for sub in sec.get("sections") or []:
                if sub.get("title") in ROLE_TITLES and sub.get("body_text"):
                    boss["roleTips"][sub["title"]] = _bullets(sub["body_text"])
            continue
        boss["abilities"].append(ability_node(sec, resolve))
    boss["abilities"] = dedupe_abilities(boss["abilities"])
    return boss, e.get("instance") or {}


def build(only: set[str] | None, resolve) -> list[dict]:
    files = sorted(f for f in MPLUS_DIR.glob("*.md") if f.stem != "season-1-overview")
    if only:
        files = [f for f in files if f.stem in only]

    dungeons = []
    for md in files:
        dungeon_slug = md.stem  # the KB filename is the canonical dungeon slug
        bosses, instance_ref = [], {}
        for enc in parse_bosses(md):
            try:
                boss, inst = build_boss(enc, dungeon_slug, resolve)
            except Exception as e:  # noqa: BLE001 — report and continue the batch
                print(f"  ✗ {dungeon_slug} enc {enc}: {e}", file=sys.stderr)
                continue
            bosses.append(boss)
            instance_ref = instance_ref or inst
        # Skip non-dungeon docs in this dir (affixes/keystones/loot/rating-and-rewards):
        # they carry no `<!-- enc:NNN -->` boss headings, so they yield no roster and
        # must not ship as empty "dungeons" in the guide.
        if not bosses:
            continue
        # dungeon lore/location come from the parent instance (any boss carries the ref)
        inst_data = get(f"/data/wow/journal-instance/{instance_ref['id']}", "static") if instance_ref.get("id") else {}
        dungeons.append({
            "slug": dungeon_slug,
            "name": inst_data.get("name") or instance_ref.get("name") or dungeon_slug,
            "lore": inst_data.get("description"),
            "location": (inst_data.get("location") or {}).get("name"),
            "bosses": bosses,
        })
        print(f"  ✓ {dungeon_slug}: {len(bosses)} bosses")
    return dungeons


def main() -> None:
    p = argparse.ArgumentParser(prog="wowkb.advguide", description=__doc__)
    p.add_argument("--only", nargs="*", help="dungeon slugs (KB filenames) to build (default: all)")
    p.add_argument("--out", type=Path, default=DEFAULT_OUT, help="output JSON path")
    p.add_argument("--refresh-db2", action="store_true", help="re-download the Spell* DB2 tables first")
    args = p.parse_args()

    ensure_db2(args.refresh_db2)
    resolve = make_resolver(*load_db2())
    dungeons = build(set(args.only) if args.only else None, resolve)

    out = {"patch": "12.0.5", "source": "Blizzard journal API + wago.tools DB2", "dungeons": dungeons}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    nb = sum(len(d["bosses"]) for d in dungeons)
    print(f"\n  advguide: {len(dungeons)} dungeons · {nb} bosses → {args.out}")


if __name__ == "__main__":
    main()
