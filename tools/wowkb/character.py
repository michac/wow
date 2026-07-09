"""One-shot character snapshot: pull every Blizzard profile endpoint plus
on-disk currencies (via the Syndicator addon) into a single digest.

The Blizzard profile API does NOT expose currencies; the Syndicator addon
logs them to SavedVariables on disk, which is readable from WSL. This tool
stitches both sources together and resolves currency IDs to names via the
wago.tools CurrencyTypes DB2 (Midnight currencies 404 on the Game Data API).

Emits DATA ONLY — no editorial narrative/deltas. Raw endpoint JSON is also
written to raw/blizzard/<name>-<endpoint>.json for provenance.

Usage:
    uv run python -m wowkb.character encomplete
    uv run python -m wowkb.character hallick --realm kiljaeden
    uv run python -m wowkb.character encomplete --json
    uv run python -m wowkb.character encomplete --no-currencies
    uv run python -m wowkb.character encomplete --wow-path "/mnt/c/.../_retail_"
"""

import argparse
import csv as _csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import wago
from ._common import RAW, save_raw
from .blizzard import get

DEFAULT_WOW = "/mnt/c/Program Files (x86)/World of Warcraft/_retail_"
DEFAULT_REALM = "kiljaeden"

# suffix appended to /profile/wow/character/<realm>/<name>
PROFILE_EPS = {
    "summary": "",
    "equipment": "/equipment",
    "specializations": "/specializations",
    "professions": "/professions",
    "reputations": "/reputations",
    "encounters-raids": "/encounters/raids",
    "keystone": "/mythic-keystone-profile",
}


# --------------------------------------------------------------------------- #
# Blizzard profile API                                                        #
# --------------------------------------------------------------------------- #
def fetch_profile(realm: str, name: str) -> dict:
    base = f"/profile/wow/character/{realm}/{name.lower()}"
    data = {}
    for key, suffix in PROFILE_EPS.items():
        try:
            d = get(base + suffix, "profile")
        except Exception as e:  # noqa: BLE001 — record and continue
            d = {"_error": str(e)}
        data[key] = d
        save_raw("blizzard", f"{name.lower()}-{key}.json", json.dumps(d, indent=2))

    # current-season keystone detail (best runs live here, not in the index)
    seasons = (data.get("keystone") or {}).get("seasons") or []
    if seasons:
        sid = seasons[-1].get("id")
        try:
            sd = get(base + f"/mythic-keystone-profile/season/{sid}", "profile")
        except Exception as e:  # noqa: BLE001
            sd = {"_error": str(e)}
        data["keystone-season"] = sd
        save_raw("blizzard", f"{name.lower()}-keystone-season.json", json.dumps(sd, indent=2))
    return data


def _iso(ms) -> str | None:
    if not ms:
        return None
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _clean(s: str | None) -> str:
    """Strip WoW UI escape sequences (|A:texture|a, |cColor, |r) from a string."""
    s = re.sub(r"\|A:[^|]*\|a", "", s or "")
    s = re.sub(r"\|c[a-zA-Z0-9]+", "", s)
    s = s.replace("|r", "").replace("|n", " ")
    return re.sub(r"\s+", " ", s).strip()


def normalize(prof: dict) -> dict:
    s = prof.get("summary", {})
    spec = prof.get("specializations", {})
    out = {
        "identity": {
            "name": s.get("name"),
            "realm": (s.get("realm") or {}).get("name"),
            "level": s.get("level"),
            "race": (s.get("race") or {}).get("name"),
            "class": (s.get("character_class") or {}).get("name"),
            "active_spec": (s.get("active_spec") or {}).get("name"),
            "hero_tree": (spec.get("active_hero_talent_tree") or {}).get("name"),
            "faction": (s.get("faction") or {}).get("name"),
            "guild": (s.get("guild") or {}).get("name"),
            "title": _clean(((s.get("active_title") or {}).get("display_string") or "").replace("{name}", s.get("name", ""))),
            "achievement_points": s.get("achievement_points"),
            "last_login": _iso(s.get("last_login_timestamp")),
            "equipped_ilvl": s.get("equipped_item_level"),
            "average_ilvl": s.get("average_item_level"),
        },
        "gear": _gear(prof.get("equipment", {})),
        "loadouts": _loadouts(spec),
        "mplus": _mplus(prof.get("keystone", {}), prof.get("keystone-season", {})),
        "raids": _raids(prof.get("encounters-raids", {})),
        "renown": _renown(prof.get("reputations", {})),
        "companions": _companions(prof.get("reputations", {})),
        "professions": _professions(prof.get("professions", {})),
    }
    return out


def _gear(eq: dict) -> list[dict]:
    items = []
    for it in eq.get("equipped_items", []):
        ench = [
            _clean(e.get("display_string"))
            for e in it.get("enchantments", [])
            if (e.get("enchantment_slot") or {}).get("type") == "PERMANENT"
        ]
        gems = [(sk.get("item") or {}).get("name") for sk in it.get("sockets", []) if sk.get("item")]
        items.append({
            "slot": (it.get("slot") or {}).get("name"),
            "ilvl": (it.get("level") or {}).get("value"),
            "id": (it.get("item") or {}).get("id"),
            "name": it.get("name"),
            "tier": bool(it.get("set")),
            "enchants": ench,
            "gems": [g for g in gems if g],
        })
    return items


def _loadouts(spec: dict) -> list[dict]:
    out = []
    for sp in spec.get("specializations", []):
        for lo in sp.get("loadouts", []):
            if lo.get("is_active"):
                out.append({
                    "spec": (sp.get("specialization") or {}).get("name"),
                    "hero_tree": (lo.get("selected_hero_talent_tree") or {}).get("name"),
                    "code": lo.get("talent_loadout_code"),
                })
    return out


def _mplus(ks: dict, season: dict) -> dict:
    runs = []
    for r in (season or {}).get("best_runs", []) or []:
        runs.append({
            "level": r.get("keystone_level"),
            "dungeon": (r.get("dungeon") or {}).get("name"),
            "timed": r.get("is_completed_within_time"),
            "minutes": round(r.get("duration", 0) / 60000, 1),
        })
    runs.sort(key=lambda x: (-(x["level"] or 0), x["dungeon"] or ""))
    return {
        "rating": round((ks.get("current_mythic_rating") or {}).get("rating", 0), 1) or None,
        "season_id": (season or {}).get("season", {}).get("id"),
        "best_runs": runs,
    }


def _raids(enc: dict) -> list[str]:
    out = []
    for exp in enc.get("expansions", []):
        for inst in exp.get("instances", []):
            for m in inst.get("modes", []):
                p = m.get("progress", {})
                if p.get("completed_count", 0) > 0:
                    out.append(
                        f"{(inst.get('instance') or {}).get('name')} "
                        f"[{(m.get('difficulty') or {}).get('name')}] "
                        f"{p['completed_count']}/{p.get('total_count')}"
                    )
    return out


def _renown(rep: dict) -> list[dict]:
    out = []
    for r in rep.get("reputations", []):
        st = r.get("standing", {})
        if st.get("renown_level") is not None:
            out.append({
                "faction": (r.get("faction") or {}).get("name"),
                "renown": st.get("renown_level"),
                "progress": f"{st.get('value', 0)}/{st.get('max', 0)}",
            })
    out.sort(key=lambda x: -(x["renown"] or 0))
    return out


def _companions(rep: dict) -> list[dict]:
    """Delve companions (Brann, Valeera) surface as reps with a 'Level N' standing."""
    out = []
    for r in rep.get("reputations", []):
        name = (r.get("standing") or {}).get("name") or ""
        m = re.match(r"Level (\d+)", name)
        if m:
            out.append({"name": (r.get("faction") or {}).get("name"), "level": int(m.group(1))})
    return out


def _professions(prof: dict) -> list[dict]:
    out = []
    for group in ("primaries", "secondaries"):
        for p in prof.get(group, []):
            for t in p.get("tiers", []):
                out.append({
                    "profession": (p.get("profession") or {}).get("name"),
                    "tier": (t.get("tier") or {}).get("name"),
                    "skill": t.get("skill_points"),
                    "max": t.get("max_skill_points"),
                    "secondary": group == "secondaries",
                })
    return out


# --------------------------------------------------------------------------- #
# Currencies (Syndicator SavedVariables + wago CurrencyTypes)                  #
# --------------------------------------------------------------------------- #
def _syndicator_file(wow_path: str) -> Path | None:
    root = Path(wow_path)
    hits = sorted(root.glob("WTF/Account/*/SavedVariables/Syndicator.lua"))
    return hits[0] if hits else None


def _char_block(text: str, name: str, realm: str | None) -> str | None:
    def norm(r):
        return re.sub(r"[^a-z]", "", (r or "").lower())

    for m in re.finditer(r'\["([^"\]]+)-([^"\]]+)"\]\s*=\s*\{', text):
        if m.group(1).lower() != name.lower():
            continue
        if realm and norm(m.group(2)) != norm(realm):
            continue
        start = m.end() - 1
        depth = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    return text[start:i + 1]
    return None


def _brace_table(block: str, pos: int) -> str:
    """Return the {...} substring starting at the '{' found at/after pos."""
    start = block.index("{", pos)
    depth = 0
    for i in range(start, len(block)):
        if block[i] == "{":
            depth += 1
        elif block[i] == "}":
            depth -= 1
            if depth == 0:
                return block[start:i + 1]
    return block[start:]


def parse_currencies(block: str) -> tuple[dict, int, list]:
    # flat id->amount map: the ["currencies"] table whose entries are [id] = amount
    flat = {}
    for m in re.finditer(r'\["currencies"\]\s*=\s*\{', block):
        table = _brace_table(block, m.start())
        pairs = re.findall(r"\[(\d+)\]\s*=\s*(\d+)", table)
        for cid, amt in pairs:
            flat[int(cid)] = int(amt)
    mm = re.search(r'\["money"\]\s*=\s*(\d+)', block)
    money = int(mm.group(1)) if mm else 0

    # header grouping (Midnight / Season 1 / ...) — ordered id lists
    groups = []
    hm = re.search(r'\["currencyByHeader"\]\s*=\s*\{', block)
    if hm:
        inner = _brace_table(block, hm.start())
        for g in re.finditer(
            r'\["header"\]\s*=\s*"([^"]+)",\s*\["currencies"\]\s*=\s*\{([^}]*)\}', inner, re.S
        ):
            ids = [int(x) for x in re.findall(r"\d+", g.group(2))]
            if ids:
                groups.append((g.group(1), ids))
    return flat, money, groups


def currency_names() -> dict:
    path = RAW / "wago" / "CurrencyTypes.csv"
    if not path.exists():
        wago.download("CurrencyTypes", None)
    names = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in _csv.DictReader(f):
            try:
                names[int(row["ID"])] = row["Name_lang"]
            except (KeyError, ValueError):
                pass
    return names


def collect_currencies(name: str, realm: str, wow_path: str) -> dict | None:
    sv = _syndicator_file(wow_path)
    if not sv:
        return {"_error": f"Syndicator.lua not found under {wow_path}/WTF/Account/*/SavedVariables/"}
    text = sv.read_text(encoding="utf-8", errors="replace")
    block = _char_block(text, name, realm)
    if not block:
        return {"_error": f"{name}-{realm} not found in {sv} (log in on the character and /reload)"}
    flat, money, groups = parse_currencies(block)
    names = currency_names()
    grouped = []
    seen = set()
    for header, ids in groups:
        rows = [
            {"id": cid, "name": names.get(cid, f"#{cid}"), "amount": flat.get(cid, 0)}
            for cid in ids
            if flat.get(cid, 0) > 0
        ]
        seen.update(ids)
        if rows:
            grouped.append({"header": header, "currencies": rows})
    other = [
        {"id": cid, "name": names.get(cid, f"#{cid}"), "amount": amt}
        for cid, amt in flat.items()
        if amt > 0 and cid not in seen
    ]
    if other:
        grouped.append({"header": "Other", "currencies": sorted(other, key=lambda r: r["name"])})
    return {"source": str(sv), "gold": round(money / 10000), "groups": grouped}


# --------------------------------------------------------------------------- #
# Markdown rendering                                                          #
# --------------------------------------------------------------------------- #
def _reset_section(state: dict | None) -> list[str]:
    """Render the PlannerState `/ps` reset-state (the third source) — what this
    character has/hasn't done THIS reset, which the profile API can't see. Empty
    when there's no dump, so the snapshot degrades to the old API+Syndicator shape.
    """
    if not state or not state.get("_path"):
        return []
    L = ["## This reset (PlannerState)"]
    wq = [q for q in state.get("weeklyQuests") or []
          if isinstance(q, dict) and not q.get("complete")]
    if wq:
        def _lbl(q):
            base = q.get("label") or q.get("id")
            if isinstance(q.get("have"), (int, float)) and q.get("need"):
                return f"{base} ({int(q['have'])}/{int(q['need'])})"
            return str(base)
        L.append("- Weeklies not done: " + ", ".join(_lbl(q) for q in wq))
    aq = [q for q in state.get("activeQuests") or []
          if isinstance(q, dict) and q.get("frequency") in (2, 3) and not q.get("isComplete")]
    if aq:
        L.append("- Weeklies in progress (quest log): "
                 + ", ".join(q.get("title") or str(q.get("id")) for q in aq))
    imp = [q for q in state.get("activeQuests") or []
           if isinstance(q, dict) and q.get("important") and not q.get("isComplete")]
    if imp:
        L.append("- ★ Important (purple-!): "
                 + ", ".join(q.get("title") or str(q.get("id")) for q in imp))
    slots = (state.get("vault") or {}).get("slots") or []
    if slots:
        by: dict = {}
        for s in slots:
            if isinstance(s, dict):
                by.setdefault(s.get("type"), []).append(s)
        parts = []
        for typ, ss in by.items():
            filled = sum(1 for s in ss
                         if (s.get("progress") or 0) >= (s.get("threshold") or 1e9))
            parts.append(f"{typ} {filled}/{len(ss)}")
        L.append("- Great Vault columns filled: " + ", ".join(parts))
    wb = state.get("worldBosses")
    if wb is not None:
        L.append(f"- World bosses killed this reset: {len(wb)}")
    cal = [e for e in state.get("calendar") or []
           if isinstance(e, dict) and e.get("active") and e.get("title")]
    if cal:
        L.append("- Active events: " + ", ".join(e["title"] for e in cal))
    L.append("")
    return L


def render_md(data: dict, cur: dict | None, state: dict | None = None) -> str:
    i = data["identity"]
    L = []
    L.append(f"# {i['name']} – {i['realm']}  (data snapshot)")
    L.append("")
    L.append(f"- **{i['race']} {i['class']}** — {i['active_spec']} "
             f"(hero tree: {i['hero_tree'] or '—'})")
    L.append(f"- Level {i['level']} · {i['faction']} · guild **{i['guild'] or '—'}** · "
             f"title {i['title'] or '—'}")
    L.append(f"- Equipped ilvl **{i['equipped_ilvl']}** (API avg {i['average_ilvl']}) · "
             f"{i['achievement_points']} ach pts · last login {i['last_login']}")
    other_loadouts = [lo["spec"] for lo in data["loadouts"] if lo["spec"] != i["active_spec"]]
    if other_loadouts:
        L.append(f"- Saved loadouts also present: {', '.join(other_loadouts)}")
    L.append("")

    L.append("## Gear")
    L.append("| Slot | ilvl | id | Item | Ench/Gem |")
    L.append("|---|---|---|---|---|")
    for g in data["gear"]:
        extra = "; ".join(g["enchants"] + [f"gem: {x}" for x in g["gems"]])
        tier = " *(tier)*" if g["tier"] else ""
        L.append(f"| {g['slot']} | {g['ilvl']} | {g['id']} | {g['name']}{tier} | {extra} |")
    L.append("")

    mp = data["mplus"]
    L.append("## Mythic+")
    if mp["rating"]:
        L.append(f"- Season {mp['season_id']} rating **{mp['rating']}** · {len(mp['best_runs'])} runs on record")
        for r in mp["best_runs"]:
            L.append(f"  - +{r['level']} {r['dungeon']} ({r['minutes']} min, "
                     f"{'timed' if r['timed'] else 'over time'})")
    else:
        L.append("- No rated runs this season.")
    L.append("")

    L.append("## Raids")
    L.append("\n".join(f"- {r}" for r in data["raids"]) or "- none recorded")
    L.append("")

    L.append("## Renown")
    for r in data["renown"]:
        L.append(f"- {r['faction']}: **{r['renown']}** ({r['progress']})")
    if data["companions"]:
        L.append("")
        L.append("Delve companions: " + " · ".join(f"{c['name']} lvl {c['level']}" for c in data["companions"]))
    L.append("")

    L.append("## Professions")
    for p in data["professions"]:
        sec = " (secondary)" if p["secondary"] else ""
        L.append(f"- {p['profession']} / {p['tier']}: {p['skill']}/{p['max']}{sec}")
    L.append("")

    L.extend(_reset_section(state))

    L.append("## Currencies")
    if not cur:
        L.append("- (skipped)")
    elif cur.get("_error"):
        L.append(f"- ⚠ {cur['_error']}")
    else:
        L.append(f"- Gold: **{cur['gold']:,}g** · source: `{cur['source']}`")
        for grp in cur["groups"]:
            L.append(f"- **{grp['header']}**: " +
                     " · ".join(f"{c['name']} {c['amount']:,}" for c in grp["currencies"]))
        L.append("- ⚠ Sparks of Radiance (an item) and Catalyst charges are NOT in "
                 "Syndicator's currency table — check those in-game.")
    L.append("")
    return "\n".join(L)


def main() -> None:
    p = argparse.ArgumentParser(prog="wowkb.character", description=__doc__)
    p.add_argument("name", help="character name, e.g. encomplete")
    p.add_argument("--realm", default=DEFAULT_REALM, help=f"realm slug (default: {DEFAULT_REALM})")
    p.add_argument("--json", action="store_true", help="emit normalized JSON instead of markdown")
    p.add_argument("--no-currencies", action="store_true", help="skip the Syndicator currency read")
    p.add_argument("--wow-path", default=DEFAULT_WOW, help="path to the _retail_ folder")
    args = p.parse_args()

    # One door for all three sources: the profile API + Syndicator (enrichment)
    # folded onto the PlannerState /ps dump (reset-state spine), via charstate.load.
    from wowkb import charstate  # deferred: charstate.load() reaches back into this module
    state = charstate.load(args.name, args.realm, wow_path=args.wow_path,
                           enrich=True, syndicator=not args.no_currencies)
    if not state or not state.get("profile"):
        err = (state or {}).get("_errors", {}).get("blizzard_api", "profile fetch failed")
        sys.exit(f"error: could not fetch {args.name}-{args.realm}: {err}")
    data = state["profile"]
    cur = state.get("syndicator")

    if args.json:
        reset = {k: v for k, v in state.items()
                 if k not in ("profile", "syndicator") and not k.startswith("_")}
        print(json.dumps({"data": data, "currencies": cur, "reset_state": reset},
                         indent=2, default=str))
    else:
        print(render_md(data, cur, state))


if __name__ == "__main__":
    main()
