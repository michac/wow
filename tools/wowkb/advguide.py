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
DB2_TABLES = ("Spell", "SpellName", "SpellEffect", "SpellMisc", "SpellDuration")

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
    return spell, names, eff, dur_idx, misc


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


def make_resolver(spell, names, eff, dur_idx, misc):
    """Return resolve(spell_id) → the spell's description with $-tokens filled in."""

    def resolve(sid, depth: int = 0) -> str:
        row = spell.get(str(sid))
        if not row:
            return f"<spell {sid}>"
        t = row["Description_lang"] or ""
        if not t:
            return ""
        # difficulty conditionals: $?DIFFn[true][false] / $?DIFFn[true] → keep "true"
        for _ in range(4):
            t2 = re.sub(r"\$\?DIFF\d+\[(.*?)\]\[(.*?)\]", lambda m: m.group(1) or m.group(2), t)
            t2 = re.sub(r"\$\?DIFF\d+\[(.*?)\]", lambda m: m.group(1), t2)
            if t2 == t:
                break
            t = t2
        t = re.sub(r"\$\?DIFF\d+", "", t)  # strip any bracketless leftovers
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

        def durval(m):  # $d / $dNNN
            di = misc.get(m.group(1) or str(sid))
            return _secs(dur_idx.get(di)) + " sec" if di else m.group(0)
        t = re.sub(r"\$(\d+)?d\b", durval, t)

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
        "children": [ability_node(c, resolve) for c in (sec.get("sections") or [])],
    }
    if not node["children"]:
        node.pop("children")
    return node


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
