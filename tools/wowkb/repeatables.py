"""Repeatable-quest scraper, reward valuation & catalog (re-runnable — safe on
patch days).

Harvests the *current* Midnight repeatable quests (daily / weekly / world-boss /
event), values each one's rewards toward player goals via rewards.value_quest (the
planner's R, not a parallel scorer), and emits:

  * knowledge/planning/repeatables.json  — planner candidate-shaped entries + the
    raw reward descriptor, zone, cadence, questID (+confidence), goals, and
    by_goal / by_currency reverse indexes.  (Kept SEPARATE from the hand-curated
    candidates.json — never clobbers it.)
  * knowledge/endgame/daily-weekly-quests.md — the human table, grouped by cadence.

    uv run python -m wowkb.repeatables
    uv run python -m wowkb.repeatables --no-cache     # force-refetch Wowhead pages
    uv run python -m wowkb.repeatables --limit 40     # cap enrichment (debug)

Discovery = a wide Wowhead listview net (min-level 90, reward-rich) + a curated KB
seed of sub-90 repeatables the popularity cap drops + a Blizzard per-zone
cross-check. The Wowhead quest page's recurring icon / "Type: Weekly|Daily" is the
authority on whether a quest is actually repeatable and on its cadence. See
knowledge/_meta/quests.md for the data-source doctrine.

Follow-up (documented, not wired this pass): feed char_state from wowkb.character
(per-slot ilvl, renown, currencies) into rewards.value_quest for character-relative
R, realizing the planner's v2b slot-targeting (scoring-model.md).
"""

from __future__ import annotations

import argparse
import json
import re
import time
from datetime import date
from pathlib import Path

import requests

from . import blizzard, rewards
from ._common import ROOT, save_raw
from .character import currency_names
from .quest import _infobox

REPO = ROOT
OUT_JSON = REPO / "knowledge" / "planning" / "repeatables.json"
OUT_DOC = REPO / "knowledge" / "endgame" / "daily-weekly-quests.md"
CACHE = ROOT / "raw" / "wowhead"

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"}
LISTVIEW = "https://www.wowhead.com/quests/min-level:90/max-level:90"

# Midnight (12.0) zone area ids -> name (from /data/wow/quest/area/index; 15000+/16000+).
MIDNIGHT_ZONES = {
    15355: "Harandar", 15947: "Zul'Aman", 15968: "Eversong Woods",
    15969: "Silvermoon City", 16173: "Sunstrider Isle", 16182: "Isle of Quel'Danas",
    16215: "Isle of Quel'Danas", 16648: "The Voidstorm",
}

# Curated zone overrides for AREA-LESS Midnight zones — quests whose Blizzard
# `/data/wow/quest/{id}` returns `area: None` AND whose zone is absent from
# `/data/wow/quest/area/index` (so neither the category map nor MIDNIGHT_ZONES
# can attribute them). Val & Naigtal are the 12.0.7 "Revelations" rotating
# world-boss worlds (portal from The Voidstorm; world-events.md) — intentionally
# NOT added to MIDNIGHT_ZONES because they have no Blizzard area id at all.
# Applied as the LAST zone fallback in build_entry(). Source: world-events.md.
QUEST_ZONE_OVERRIDES = {
    96713: "Val / Naigtal (rotating)",   # Showdown on Val    (Imperator Pertinax)
    96717: "Val / Naigtal (rotating)",   # Showdown on Naigtal (Nexus-Captain Leth'ir)
}

# Curated seed: repeatable quest IDs the level-90 listview / 1000-row popularity cap
# misses (sub-90 quest level, or low popularity). Sourced from the KB
# (weekly-checklist.md, leveling-notes.md). Guarantees the important repeatables land
# in the catalog regardless of Wowhead's default sort.
KNOWN_REPEATABLES = {
    # Shul'ka Li'tya "WANTED" board, Harandar — daily elite kills (leveling-notes.md)
    91970, 91980, 91982, 91998, 92010, 92012, 92013,
    # Void Assault weeklies — Eversong / Zul'Aman rotation (weekly-checklist.md)
    94385, 94386,
    # Nightmare Prey weekly (weekly-checklist.md)
    94446,
    # Weekly world bosses — Lu'ashal / Thorm'belan / Predaxas / Cragpine rotation
    # (weekly-checklist.md). Creature-lockout content that also carries a quest.
    92560, 92034, 92636, 92123,
    # 12.0.7 Val/Naigtal rotating world-boss weeklies — "Showdown on Val" (96713)
    # / "Showdown on Naigtal" (96717), level-90 variants (world-events.md). Seeded
    # belt-and-suspenders with the name signals below; area-less (see
    # QUEST_ZONE_OVERRIDES) so the listview/zone cross-check can't surface them.
    96713, 96717,
}

# "Name signals" — string-match heuristics that classify a quest from its NAME
# when structured signals (Wowhead Type / recurring icon) are absent. WORLD_BOSSES
# holds boss-NPC names; the Showdown weeklies carry neither a Type nor a recurring
# icon, so only a name match (here + REPEATABLE_NAME_RE + classify_cadence) fires.
WORLD_BOSSES = ("lu'ashal", "thorm'belan", "predaxas", "cragpine",
                "pertinax", "leth'ir")
EVENT_KEYWORDS = ("timewalking", "timeways", "darkmoon", "midsummer", "soiree",
                  "saltheril", "trading post", "traveler's log")
# Names that mark a KNOWN repeatable system even when Wowhead's Type is generic.
REPEATABLE_NAME_RE = re.compile(
    r"^wanted:|void assault|void strike|void incursion|ritual site|nightmare|"
    r"world boss|weekly|renown|bounty|\bweek \d+ of\b|delver|preferential|"
    r"showdown on val|showdown on naigtal|showdown",
    re.I)

# Coarse ilvl -> upgrade-track bands (great-vault.md). track_confidence stays "low":
# the Blizzard item API does not expose the track, so this is a best-effort guess.
TRACK_BANDS = [(278, "Myth"), (265, "Hero"), (246, "Champion"), (220, "Veteran"), (1, "Adventurer")]

# Defaults for fields the scrape can't know — flagged _needs_human so nobody mistakes
# them for measured values.
CADENCE_URGENCY = {"weekly": 2, "world-boss": 2, "daily": 1.5, "event": 1.5, "unknown": 1.5}
ENJOYMENT_HINTS = [
    ("ritual site", "ritual"), ("nightmare", "prey"), ("prey", "prey"),
    ("delve", "delve"), ("housing", "housing"), ("void", "chore"),
]


# --------------------------------------------------------------------------- #
# Wowhead listview harvest                                                     #
# --------------------------------------------------------------------------- #
def _listview_data(html: str) -> list[dict]:
    """Extract the quest `data:[…]` array — the one whose entries carry id+level."""
    best: list[dict] = []
    for m in re.finditer(r"data:\[", html):
        start = html.index("[", m.start())
        depth = 0
        for j in range(start, len(html)):
            if html[j] == "[":
                depth += 1
            elif html[j] == "]":
                depth -= 1
                if depth == 0:
                    break
        try:
            arr = json.loads(html[start:j + 1])
        except json.JSONDecodeError:
            continue
        if arr and isinstance(arr[0], dict) and "id" in arr[0] and "level" in arr[0]:
            if len(arr) > len(best):
                best = arr
    return best


def harvest() -> dict[int, dict]:
    resp = requests.get(LISTVIEW, headers=UA, timeout=60)
    resp.raise_for_status()
    save_raw("wowhead", "listview-quests.html", resp.text)
    entries = _listview_data(resp.text)
    # Midnight only (firstseenpatch 1200xx) — drop older content surfaced by the filter.
    return {e["id"]: e for e in entries
            if str(e.get("firstseenpatch", "")).startswith("1200")}


# --------------------------------------------------------------------------- #
# Wowhead quest page (cadence + repeatable authority)                          #
# --------------------------------------------------------------------------- #
def fetch_page(qid: int, use_cache: bool = True) -> str | None:
    cache = CACHE / f"quest-{qid}.html"
    if use_cache and cache.exists():
        return cache.read_text(encoding="utf-8", errors="replace")
    try:
        resp = requests.get(f"https://www.wowhead.com/quest={qid}",
                            headers=UA, allow_redirects=True, timeout=30)
        resp.raise_for_status()
    except Exception:  # noqa: BLE001 — a missing page shouldn't abort the crawl
        return None
    time.sleep(0.2)  # be polite to Wowhead
    save_raw("wowhead", f"quest-{qid}.html", resp.text)
    return resp.text


def page_facts(html: str) -> dict:
    facts = dict(_infobox(html))  # type / requires_level / side
    facts["recurring"] = "quest-recurring" in html  # recurring turn-in icon
    facts["currencies"] = list(dict.fromkeys(
        re.findall(r'/currency=\d+/[^"]*">([^<]+)</a>', html)))
    facts["item_ids"] = [int(x) for x in dict.fromkeys(
        re.findall(r'/item=(\d+)/', html))]
    return facts


# --------------------------------------------------------------------------- #
# Gear reward resolution (ilvl + best-effort track)                            #
# --------------------------------------------------------------------------- #
_item_memo: dict[int, dict] = {}


def resolve_item(iid: int) -> dict:
    if iid in _item_memo:
        return _item_memo[iid]
    out = {"id": iid, "name": None, "ilvl": None, "track": None,
           "track_confidence": "none", "is_gear": False,
           "is_cache": False, "cache_goals": [], "cache_R": 0}
    try:
        it = blizzard.get(f"/data/wow/item/{iid}", "static")
    except Exception:  # noqa: BLE001
        _item_memo[iid] = out
        return out
    out["name"] = it.get("name")
    cls = (it.get("item_class") or {}).get("name")
    ilvl = (it.get("level") if isinstance(it.get("level"), int) else None) or \
        ((it.get("preview_item") or {}).get("level") or {}).get("value")
    out["is_gear"] = it.get("is_equippable", False) and cls in ("Armor", "Weapon")
    if out["is_gear"] and ilvl:
        out["ilvl"] = ilvl
        for floor, track in TRACK_BANDS:  # coarse ilvl-band guess only
            if ilvl >= floor:
                out["track"] = track
                out["track_confidence"] = "low"
                break
    else:
        # Container / cache reward (e.g. Riftstalker's Cache 275690): a non-gear
        # item whose name reads as a cache/coffer OR whose description enumerates
        # contents CACHE_RULES recognizes. The description's contents string makes
        # its value derivable (rewards.classify_cache) rather than opaque.
        desc = it.get("description") or ""
        name_low = (out["name"] or "").lower()
        if ("cache" in name_low or "coffer" in name_low
                or any(sub in desc.lower() for sub, *_ in rewards.CACHE_RULES)):
            goals, R = rewards.classify_cache(desc, out["name"] or "")
            if goals or R:
                out["is_cache"] = True
                out["cache_goals"] = goals
                out["cache_R"] = R
    _item_memo[iid] = out
    return out


# --------------------------------------------------------------------------- #
# Zone cross-check                                                             #
# --------------------------------------------------------------------------- #
def zone_map() -> tuple[dict[int, str], dict[str, set[int]]]:
    """id -> zone name, and zone -> set(quest ids), from Blizzard per-zone lists."""
    id2zone: dict[int, str] = {}
    zone2ids: dict[str, set[int]] = {}
    for aid, name in MIDNIGHT_ZONES.items():
        try:
            data = blizzard.get(f"/data/wow/quest/area/{aid}", "static")
        except Exception:  # noqa: BLE001
            continue
        ids = {q["id"] for q in data.get("quests", []) if "id" in q}
        zone2ids.setdefault(name, set()).update(ids)
        for qid in ids:
            id2zone.setdefault(qid, name)
    return id2zone, zone2ids


# --------------------------------------------------------------------------- #
# Classification                                                               #
# --------------------------------------------------------------------------- #
def is_repeatable(name: str, entry: dict | None, facts: dict, seed: bool) -> tuple[bool, str]:
    if seed:
        return True, "high"                    # curated KB seed
    if facts.get("recurring"):
        return True, "high"                    # recurring turn-in icon
    if facts.get("type") in ("Weekly", "Daily"):
        return True, "high"
    if entry and entry.get("icon") == "quest-start-daily":
        return True, "high"
    if REPEATABLE_NAME_RE.search(name or ""):
        return True, "medium"                  # known repeatable system by name
    return False, "n/a"


def classify_cadence(name: str, entry: dict | None, facts: dict) -> tuple[str, str]:
    low = (name or "").lower()
    if any(b in low for b in WORLD_BOSSES) or "world boss" in low:
        return "world-boss", "high"
    if "showdown" in low:                      # Val/Naigtal Showdown weeklies
        return "world-boss", "medium"          # name-only signal (no Type/icon)
    if any(k in low for k in EVENT_KEYWORDS):
        return "event", "medium"
    t = facts.get("type")
    if t == "Weekly":
        return "weekly", "high"
    if t == "Daily":
        return "daily", "high"
    if entry and entry.get("icon") == "quest-start-daily":
        return "daily", "high"
    if re.search(r"\bweek \d+ of\b|ritual site studies|void assault|weekly", low):
        return "weekly", "medium"
    if low.startswith("wanted:"):
        return "daily", "medium"
    return "unknown", "low"


def make_gate(cadence: str, qid: int, name: str) -> dict:
    if cadence == "weekly":
        return {"type": "weekly_quest", "quest": str(qid)}
    if cadence == "world-boss":
        return {"type": "lockout", "name_contains": "world"}
    if cadence == "event":
        low = (name or "").lower()
        match = next((k for k in EVENT_KEYWORDS if k in low), name)
        return {"type": "event_active", "match": match}
    return {"type": "always"}                  # daily / unknown: standing, never gated done


def enjoyment_key(name: str) -> str:
    low = (name or "").lower()
    for sub, key in ENJOYMENT_HINTS:
        if sub in low:
            return key
    return "chore"


# --------------------------------------------------------------------------- #
# Entry assembly                                                               #
# --------------------------------------------------------------------------- #
def build_entry(qid: int, entry: dict | None, curnames: dict,
                id2zone: dict, use_cache: bool, seed: bool) -> dict | None:
    html = fetch_page(qid, use_cache)
    facts = page_facts(html) if html else {}

    # Base fields: prefer the listview entry; fall back to the Blizzard quest API
    # for seeds the listview didn't carry.
    name = (entry or {}).get("name")
    level = (entry or {}).get("level")
    xp = (entry or {}).get("xp") or 0
    money = (entry or {}).get("money") or 0
    # A listview entry's `category` is often the zone's area id (free attribution);
    # fall back to the Blizzard per-zone membership map, then to the quest API's area.
    zone = MIDNIGHT_ZONES.get((entry or {}).get("category")) or id2zone.get(qid)
    if entry is None or zone is None:
        try:
            q = blizzard.get(f"/data/wow/quest/{qid}", "static")
        except Exception:  # noqa: BLE001
            q = None
        if q:
            name = name or q.get("title")
            level = level or (q.get("requirements") or {}).get("min_character_level")
            xp = xp or (q.get("rewards") or {}).get("experience") or 0
            money = money or ((q.get("rewards") or {}).get("money") or {}).get("value") or 0
            zone = zone or (q.get("area") or {}).get("name")
    # Last resort: a curated override for area-less zones (Val/Naigtal) the
    # Blizzard area index can't attribute (see QUEST_ZONE_OVERRIDES).
    if zone is None:
        zone = QUEST_ZONE_OVERRIDES.get(qid)
    if not name:
        return None

    rep, rep_conf = is_repeatable(name, entry, facts, seed)
    if not rep:
        return None

    # Descriptor: from the listview entry (has amounts) or scraped page names.
    if entry is not None:
        desc = rewards.descriptor_from_listview(entry, curnames)
        # A listview row can be barren of rewards even when the quest page lists
        # them (e.g. Showdown on Val 96713 — empty itemrewards in the listview, but
        # the page shows a Riftstalker's Cache). Backfill from the scraped page so
        # cache/currency rewards aren't lost to a thin listview row.
        if not desc["currencies"] and not desc["items"] and facts:
            for n in facts.get("currencies", []):
                desc["currencies"].append({"id": None, "name": n, "amount": None})
            for iid in facts.get("item_ids", [])[:6]:
                desc["items"].append({"id": iid, "name": None, "ilvl": None, "track": None})
    else:
        desc = rewards.descriptor_from_names(facts.get("currencies", []),
                                             xp=xp, money=money)
        for iid in facts.get("item_ids", [])[:6]:
            desc["items"].append({"id": iid, "name": None, "ilvl": None, "track": None})

    # Resolve reward items: keep gear (-> ilvl + track), lift containers into
    # desc["caches"] (cache-derived goals/R), drop the rest so they don't inflate.
    gear = []
    for it in desc["items"]:
        if it.get("id") is None:
            gear.append(it)
            continue
        r = resolve_item(it["id"])
        if r["is_gear"]:
            gear.append({"id": r["id"], "name": r["name"], "ilvl": r["ilvl"],
                         "track": r["track"], "track_confidence": r["track_confidence"]})
        elif r["is_cache"]:
            desc.setdefault("caches", []).append(
                {"id": r["id"], "name": r["name"],
                 "goals": r["cache_goals"], "R": r["cache_R"]})
    desc["items"] = gear

    cadence, cad_conf = classify_cadence(name, entry, facts)
    val = rewards.value_quest(desc)               # baseline R (char_state deferred)
    goals = val["goals"]

    why_bits = [cadence]
    if goals:
        why_bits.append("goals: " + ", ".join(g for g in goals if g in rewards.POWER_GOALS) or "")
    why = f"{cadence} repeatable"
    if val["note"]:
        why += f" — {val['note']}"

    return {
        # --- planner candidate schema (candidates.json-compatible) ---
        "id": f"rep-{qid}",
        "name": name,
        "reward_base": val["R"],
        "urgency": CADENCE_URGENCY.get(cadence, 1.5),
        "time_blocks": 1,                         # _needs_human
        "enjoyment_key": enjoyment_key(name),     # _needs_human
        "gate": make_gate(cadence, qid, name),
        "why": why,
        # --- extras (repeatables.json only) ---
        "descriptor": desc,
        "goals": goals,
        "zone": zone or "unknown",
        "cadence": cadence,
        "cadence_confidence": cad_conf,
        "questID": qid,
        "questID_confidence": rep_conf,
        "quest_level": level,
        "value_confidence": val["confidence"],
        "_needs_human": True,                     # time_blocks + enjoyment_key are guesses
    }


# --------------------------------------------------------------------------- #
# Reverse indexes                                                             #
# --------------------------------------------------------------------------- #
def reverse_indexes(entries: list[dict]) -> tuple[dict, dict]:
    by_goal: dict[str, list] = {}
    by_currency: dict[str, list] = {}
    for e in entries:
        tag = {"questID": e["questID"], "name": e["name"], "cadence": e["cadence"]}
        for g in e["goals"]:
            by_goal.setdefault(g, []).append(tag)
        for c in e["descriptor"]["currencies"]:
            by_currency.setdefault(c["name"], []).append(tag)
    return ({k: by_goal[k] for k in sorted(by_goal)},
            {k: by_currency[k] for k in sorted(by_currency)})


# --------------------------------------------------------------------------- #
# Output writers                                                              #
# --------------------------------------------------------------------------- #
def write_json(entries: list[dict], by_goal: dict, by_currency: dict,
               coverage: dict, wire: list[dict]) -> None:
    payload = {
        "_note": ("Generated by `uv run python -m wowkb.repeatables` — do NOT hand-edit; "
                  "re-run to refresh. Candidate-shaped entries (see "
                  "knowledge/planning/scoring-model.md) PLUS raw descriptor/zone/cadence/"
                  "questID/goals. reward_base is a character-AGNOSTIC baseline R "
                  "(rewards.value_quest, char_state deferred). time_blocks + enjoyment_key "
                  "are placeholders (_needs_human). Kept separate from the hand-curated "
                  "candidates.json — the planner reads that one; merging is the deferred "
                  "--include-repeatables follow-up."),
        "generated": date.today().isoformat(),
        "count": len(entries),
        "candidates": sorted(entries, key=lambda e: (e["cadence"], -e["reward_base"], e["name"])),
        "by_goal": by_goal,
        "by_currency": by_currency,
        "zone_coverage": coverage,
        "questIDs_to_wire": wire,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _reward_summary(desc: dict) -> str:
    seen: dict[str, int | None] = {}  # dedup same-name currencies (dup IDs share a name)
    for c in desc["currencies"]:
        if c["name"] not in seen or (c.get("amount") or 0) > (seen[c["name"]] or 0):
            seen[c["name"]] = c.get("amount")
    bits = [n + (f" ×{a}" if a else "") for n, a in seen.items()]
    for it in desc["items"]:
        if it.get("track") or it.get("ilvl"):
            bits.append(f"{it.get('name') or 'gear'} "
                        f"({it.get('track') or '?'} {it.get('ilvl') or '?'})")
    for cache in desc.get("caches", []):
        goals = ", ".join(cache.get("goals") or [])
        bits.append(f"{cache.get('name') or 'cache'}"
                    + (f" [{goals}]" if goals else ""))
    if desc.get("xp"):
        bits.append(f"{desc['xp']} XP")
    if desc.get("money"):
        bits.append(f"{desc['money'] // 10000}g")
    return "; ".join(bits) or "—"


def write_doc(entries: list[dict], wire: list[dict], coverage: dict) -> None:
    today = date.today().isoformat()
    order = ["weekly", "daily", "world-boss", "event", "unknown"]
    by_cad: dict[str, list] = {c: [] for c in order}
    for e in entries:
        by_cad.setdefault(e["cadence"], []).append(e)

    L: list[str] = []
    L += ["---",
          "title: Midnight Daily/Weekly Repeatable Quests (Season 1)",
          "patch: 12.0.7",
          f"fetched: {today}",
          "sources:",
          "  - https://www.wowhead.com/quests/min-level:90/max-level:90   # listview harvest",
          "  - https://us.api.blizzard.com/data/wow/quest/area/15355       # Blizzard zone cross-check",
          "  - knowledge/_meta/quests.md   # quest-data doctrine",
          "confidence: medium   # auto-generated; cadence/track marked per-row, verify gated ones in-game",
          "---",
          "",
          "# Midnight Repeatable Quests — auto-generated catalog",
          "",
          "> **Generated file — do not hand-edit.** Regenerate with "
          "`cd tools && uv run python -m wowkb.repeatables`. Machine-readable twin: "
          "`knowledge/planning/repeatables.json` (planner candidate-shaped + reverse "
          "indexes). This is a *repeatable scrape*, safe to re-run on patch days.",
          "",
          "Reward **value** is the planner's baseline **R** (0–5) + goal tags "
          "(`gearing/vault/crafting/renown/cosmetic/gold/xp`), from "
          "`rewards.value_quest` — see `knowledge/planning/scoring-model.md`. R here is "
          "**character-agnostic**; a piece worthless to a geared character still shows "
          "its baseline. Character-relative scoring is the deferred follow-up below.",
          "",
          f"Catalog: **{len(entries)}** repeatable quests.",
          ""]

    for cad in order:
        rows = sorted(by_cad.get(cad, []), key=lambda e: (-e["reward_base"], e["name"]))
        if not rows:
            continue
        L += [f"## {cad.title()} ({len(rows)})", "",
              "| id | name | zone | rewards | value (R + goals) | questID | notes |",
              "|---|---|---|---|---|---|---|"]
        for e in rows:
            rw = _reward_summary(e["descriptor"]).replace("|", "\\|")
            goals = ",".join(e["goals"]) or "—"
            notes = []
            if e["cadence_confidence"] in ("low", "medium"):
                notes.append(f"cadence:{e['cadence_confidence']}")
            if e["questID_confidence"] != "high":
                notes.append(f"questID:{e['questID_confidence']}")
            if e["value_confidence"] != "high":
                notes.append(f"value:{e['value_confidence']}")
            notes.append("time/E _needs_human")
            L.append(f"| {e['id']} | {e['name']} | {e['zone']} | {rw} | "
                     f"R={e['reward_base']} {goals} | {e['questID']} | {'; '.join(notes)} |")
        L.append("")

    L += ["## Caveats",
          "",
          "- **Campaign gating.** Several repeatables unlock only after a story chain — "
          "notably the Shul'ka Li'tya **WANTED** board (Harandar): level 88 *and* "
          "Trials-of-the-Shul'ka campaign progress *and* a random daily roll. An empty "
          "board is expected, not a bug. See `knowledge/systems/leveling-notes.md`.",
          "- **`_needs_human` fields.** `time_blocks` and `enjoyment_key` are placeholder "
          "defaults, not measured — tune before trusting the planner score.",
          "- **Gear track** is a coarse ilvl-band guess (`track_confidence: low`); the "
          "Blizzard item API does not expose the upgrade track. Never asserted as fact.",
          "- **Cadence** is best-effort (Wowhead `Type` + recurring icon + name); rows "
          "flag low/medium confidence.",
          "- **Turn-in ≠ activity loot.** R values the *quest reward* only. World-boss "
          "and Void-Assault quests hand out just XP on turn-in (hence R=0) — the real "
          "loot is the boss/activity drop + weekly lockout, which this model doesn't "
          "see. Treat those rows' R as a floor.",
          "- **Container/cache rewards are R-floored.** When a quest rewards a *cache* "
          "(e.g. the Val/Naigtal Showdowns' Riftstalker's Cache), R + goals are derived "
          "from the item's description (which lists the contents), but the gear roll "
          "*inside* the cache is opaque to the API — so the shown R is a floor a real "
          "open can only beat.",
          ""]

    if wire:
        L += ["## questIDs to wire (verify in-game first)",
              "",
              "Candidate IDs for the planner's `weekly_quest` gate / PlannerState "
              "`ns.WEEKLY_QUESTS`. **Not auto-wired** — a wrong ID false-reports \"done\" "
              "(`weekly-checklist.md`). Confirm each in-game before adding.",
              ""]
        for w in wire:
            L.append(f"- `{w['questID']}` — {w['name']} "
                     f"({w['cadence']}, id-confidence {w['questID_confidence']})")
        L.append("")

    if coverage:
        L += ["## Zone cross-check coverage", "",
              "Blizzard `/data/wow/quest/area/{id}` per Midnight zone vs this catalog "
              "(quests in-zone but not catalogued are one-off/story quests or misses to "
              "spot-check):", ""]
        for zone, c in sorted(coverage.items()):
            L.append(f"- **{zone}**: {c['catalogued']} catalogued of {c['zone_total']} zone quests")
        L.append("")

    L += ["## How this was generated / how to refresh",
          "",
          "```bash",
          "cd tools && uv run python -m wowkb.repeatables      # rewrites this file + repeatables.json",
          "```",
          "",
          "Pipeline: Wowhead listview harvest (`min-level:90/max-level:90`, Midnight-patch "
          "only) + curated KB seed (sub-90 repeatables the 1000-row cap drops) + Blizzard "
          "per-zone cross-check. Each candidate's Wowhead page confirms repeatability "
          "(recurring icon / `Type: Weekly|Daily`) and cadence; gear rewards resolve ilvl "
          "via the Blizzard item API. Rewards are valued by `rewards.value_quest`.",
          "",
          "## Deferred follow-up — character-relative value",
          "",
          "This catalog uses a **character-agnostic** baseline R. The reward valuation "
          "(`rewards.value_quest`) already accepts a `char_state` argument for "
          "**character-relative** scoring (gear scored by ilvl-delta to your weakest "
          "slot; currency by whether it advances an uncapped track) — implemented and "
          "unit-tested, but **not yet wired**. To finish it: feed `char_state` from "
          "`wowkb.character` (per-slot ilvl, renown, currencies) into `value_quest`, and "
          "add a `plan.py --include-repeatables` flag that merges `repeatables.json` and "
          "rescores with `char_state`. That realizes the planner's designed-but-"
          "unimplemented **v2b slot-targeting** (`scoring-model.md`).",
          ""]
    OUT_DOC.write_text("\n".join(L), encoding="utf-8")


# --------------------------------------------------------------------------- #
def run(use_cache: bool = True, limit: int | None = None) -> dict:
    curnames = currency_names()
    print("· harvesting Wowhead listview…")
    entries = harvest()
    print(f"  {len(entries)} Midnight level-90 quests")
    print("· building zone map (Blizzard per-zone)…")
    id2zone, zone2ids = zone_map()

    # Pare-before-fetch: keep entries with a recognized POWER-goal currency reward and a
    # non-campaign icon (candidate repeatables), plus every curated seed.
    def has_power_currency(e: dict) -> bool:
        for key in ("currencyrewards", "currencychoicerewards"):
            for pair in e.get(key) or []:
                goal, _, _ = rewards.classify_currency(curnames.get(pair[0], ""))
                if goal in rewards.POWER_GOALS:
                    return True
        return False

    pool = {qid for qid, e in entries.items()
            if e.get("icon") != "quest-start-campaign" and has_power_currency(e)}
    pool |= KNOWN_REPEATABLES
    qids = sorted(pool)
    if limit:
        qids = qids[:limit]
    print(f"· enriching {len(qids)} candidates (cached pages reused)…")

    catalog: list[dict] = []
    for n, qid in enumerate(qids, 1):
        e = build_entry(qid, entries.get(qid), curnames, id2zone, use_cache,
                        seed=qid in KNOWN_REPEATABLES)
        if e:
            catalog.append(e)
        if n % 25 == 0:
            print(f"  {n}/{len(qids)}…")

    by_goal, by_currency = reverse_indexes(catalog)
    cat_ids = {e["questID"] for e in catalog}
    coverage = {zone: {"zone_total": len(ids), "catalogued": len(ids & cat_ids)}
                for zone, ids in zone2ids.items()}
    # Wire list = quests whose done-state a questID could gate: weekly_quest-gated
    # rows, plus world-boss weeklies that carry a real questID (e.g. the Val/Naigtal
    # Showdowns 96713/96717 — candidates for ns.WEEKLY_QUESTS once verified in-game).
    wire = [{"questID": e["questID"], "name": e["name"], "cadence": e["cadence"],
             "questID_confidence": e["questID_confidence"]}
            for e in catalog
            if e["gate"]["type"] == "weekly_quest" or e["cadence"] == "world-boss"]

    write_json(catalog, by_goal, by_currency, coverage, wire)
    write_doc(catalog, wire, coverage)
    print(f"· wrote {OUT_JSON.relative_to(REPO)} ({len(catalog)} entries) + "
          f"{OUT_DOC.relative_to(REPO)}")
    return {"count": len(catalog)}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="wowkb.repeatables", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--no-cache", action="store_true", help="force-refetch Wowhead pages")
    p.add_argument("--limit", type=int, help="cap candidates enriched (debug)")
    args = p.parse_args(argv)
    run(use_cache=not args.no_cache, limit=args.limit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
