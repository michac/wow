"""Reward descriptor + valuation — the two-layer reward model.

Layer (a) the **descriptor**: a normalized, character-agnostic snapshot of what a
quest hands out (currencies + amounts, gear items with track/ilvl, rep, xp, money).
Scraped once, stored — the "link to reward".

Layer (b) **value_quest(descriptor, char_state=None)**: the "map to find rewards" —
turns a descriptor into a planner-shaped value: a **baseline R** (0-5, per
knowledge/planning/scoring-model.md) + **goal tags** + a note. Called with
`char_state=None` today (character-agnostic baseline). The `char_state` branch is
implemented and unit-tested but **not yet wired** to live data — when it is,
`char_state` comes from `wowkb.character` (per-slot ilvl, renown, currencies) and
gear rewards score by ilvl-delta-to-your-weakest-slot, realizing the planner's
designed-but-unimplemented v2b slot-targeting (scoring-model.md).

Stdlib only — importable offline (no network), so plan.py-style unit checks work.

Seeded from knowledge/endgame/{weekly-checklist,great-vault,dawncrests}.md and the
currency IDs observed in Wowhead listviews (resolved via wago CurrencyTypes).
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Goal taxonomy                                                               #
# --------------------------------------------------------------------------- #
# The tags a reward can advance. "Power goals" raise R; "soft goals" are tracked
# so a goal-chaser can still find the quest, but contribute R=0 on their own —
# efficiency-first deliberately blinds R to cosmetic/gold/xp (scoring-model.md;
# their value re-enters through the planner's Urgency term, not here).
POWER_GOALS = ("gearing", "vault", "crafting", "renown")
SOFT_GOALS = ("cosmetic", "gold", "xp")
GOALS = POWER_GOALS + SOFT_GOALS

# --------------------------------------------------------------------------- #
# Currency classification                                                     #
# --------------------------------------------------------------------------- #
# Ordered (substring, goal, weight 0-1, note) rules, matched case-insensitively
# against the currency *name* (so it works from a scraped name alone, no ID map).
# First match wins — list most-specific first. weight is a coarse "how much does
# one of these move a goal" knob feeding _r_from_weight() below.
CURRENCY_RULES: list[tuple[str, str, float, str]] = [
    # Upgrade crests (Dawncrests) — the gearing spine. Higher tier = more R.
    ("myth dawncrest",       "gearing",  1.00, "top-tier upgrade crest"),
    ("hero dawncrest",       "gearing",  0.90, "hero-track upgrade crest"),
    ("champion dawncrest",   "gearing",  0.60, "mid upgrade crest"),
    ("veteran dawncrest",    "gearing",  0.50, "early upgrade crest"),
    ("adventurer dawncrest", "gearing",  0.30, "low upgrade crest"),
    ("dawncrest",            "gearing",  0.60, "upgrade crest (tier unknown)"),
    # Gear-adjacent high-value currencies.
    ("coffer key",           "vault",    0.90, "delve bountiful key -> gear/vault"),
    ("voidcore",             "gearing",  0.90, "bonus roll -> gear"),
    ("voidlight marl",       "gearing",  0.40, "catch-all 12.0.5 currency"),
    # Crafting.
    ("spark",                "crafting", 0.90, "crafting spark"),
    ("radiance",             "crafting", 0.90, "crafting"),
    # Reputation / renown tokens (delivered as currency in Midnight).
    ("renown -",             "renown",   0.60, "renown token"),
    ("the hara'ti",          "renown",   0.60, "faction rep"),
    ("the singularity",      "renown",   0.60, "faction rep"),
    ("silvermoon court",     "renown",   0.60, "faction rep"),
    ("amani tribe",          "renown",   0.60, "faction rep"),
    ("slayer's rise",        "renown",   0.60, "faction rep"),
    # PvP gear currencies — real power, but niche; fold into gearing (low weight).
    ("conquest",             "gearing",  0.50, "pvp gear currency"),
    ("honor",                "gearing",  0.30, "pvp gear currency"),
    ("bloody token",         "gearing",  0.30, "pvp gear currency"),
    ("slayer's duellum",     "gearing",  0.40, "slayer/pvp currency"),
    # Cosmetic / progression-flavor — soft goal, R=0 baseline.
    ("field accolade",       "cosmetic", 0.55, "ritual-site cosmetics (housing/mounts/xmog)"),
    ("ritual site knowledge","cosmetic", 0.40, "ritual-site progression"),
    ("community coupon",     "cosmetic", 0.20, "trading post cosmetic"),
    ("prize ticket",         "cosmetic", 0.20, "darkmoon cosmetic"),
    ("darkmoon",             "cosmetic", 0.20, "darkmoon cosmetic"),
]


def classify_currency(name: str) -> tuple[str | None, float, str]:
    """(goal, weight, note) for a currency name, or (None, 0, '') if unrecognized."""
    low = (name or "").lower()
    for sub, goal, weight, note in CURRENCY_RULES:
        if sub in low:
            return goal, weight, note
    return None, 0.0, ""


# --------------------------------------------------------------------------- #
# Container / cache rewards                                                    #
# --------------------------------------------------------------------------- #
# Some quests reward a CONTAINER item (a cache / coffer) instead of inline
# currency — e.g. the Val/Naigtal world-boss weeklies hand out a Riftstalker's
# Cache (item 275690). The Blizzard item API's `description` literally enumerates
# the contents ("Cache containing Field Accolades, Relic Coffer Key shards,
# materials for upgrading gear, gold, and more"), so a cache's value is
# *derivable* rather than opaque. Same (substring, goal, weight, note) shape as
# CURRENCY_RULES — matched case-insensitively against the cache's description.
CACHE_RULES: list[tuple[str, str, float, str]] = [
    ("coffer key",     "vault",    0.90, "Relic Coffer Key shards -> vault/gearing"),
    ("upgrading gear", "gearing",  0.60, "gear-upgrade materials"),
    ("material",       "crafting", 0.60, "crafting materials"),
    ("field accolade", "cosmetic", 0.55, "ritual-site cosmetics"),
    ("gold",           "gold",     0.20, "gold"),
]

# Curated fallback for caches whose description does NOT enumerate contents.
# name-substring -> (goals, R-floor). R is a FLOOR — the gear roll inside the
# cache is unknown to the API, so a real open can only beat this.
KNOWN_CACHES: dict[str, tuple[list[str], int]] = {
    "riftstalker's cache": (["cosmetic", "crafting", "gold", "vault"], 3),
}


def classify_cache(description: str, name: str = "") -> tuple[list[str], int]:
    """(goals, R-floor) for a container item, derived from its description text.

    Scans the description for CACHE_RULES substrings, unions their goals, and
    floors R from the strongest power-goal weight (soft-goal-only -> R=0, per the
    scoring model). R is a FLOOR: the actual gear roll inside is unknown to the
    API. Falls back to KNOWN_CACHES keyed on the item name when the description
    names no recognizable contents. Returns ([], 0) for a non-cache / unknown.
    """
    low = (description or "").lower()
    goals: set[str] = set()
    r_candidates: list[int] = [0]
    for sub, goal, weight, _note in CACHE_RULES:
        if sub in low:
            goals.add(goal)
            if goal in POWER_GOALS:
                r_candidates.append(_r_from_weight(weight))
    if not goals:
        nm = (name or "").lower()
        for key, (g, r) in KNOWN_CACHES.items():
            if key in nm:
                return sorted(g), r
        return [], 0
    R = min(5, max(r_candidates))
    if not (goals & set(POWER_GOALS)):
        R = 0  # cosmetic/gold-only cache: R=0 baseline (scoring-model.md)
    return sorted(goals), R


# --------------------------------------------------------------------------- #
# Gear upgrade tracks                                                          #
# --------------------------------------------------------------------------- #
TRACK_ORDER = ["Adventurer", "Veteran", "Champion", "Hero", "Myth"]
# Flat, character-agnostic value of a gear reward by its upgrade track (0-5).
# Coarse on purpose — the exact worth is character-relative (char_state branch).
TRACK_R = {"Adventurer": 1, "Veteran": 2, "Champion": 2, "Hero": 3, "Myth": 4}


def _r_from_weight(w: float) -> int:
    """Map a 0-1 power-goal weight to a coarse baseline R (0-4)."""
    if w >= 0.95:
        return 4
    if w >= 0.70:
        return 3
    if w >= 0.45:
        return 2
    if w > 0:
        return 1
    return 0


# --------------------------------------------------------------------------- #
# Descriptor construction                                                      #
# --------------------------------------------------------------------------- #
def empty_descriptor() -> dict:
    return {"currencies": [], "items": [], "caches": [], "rep": [], "xp": 0, "money": 0}


def descriptor_from_listview(entry: dict, currency_names: dict) -> dict:
    """Normalize a Wowhead quest-listview entry into a reward descriptor.

    `entry` is one element of the listview `data:[…]` array; `currency_names` maps
    currency ID -> name (from wago CurrencyTypes). Gear items are captured id-only
    here — ilvl/track are resolved later by the scraper (Blizzard item API) and
    written back onto the descriptor's items.
    """
    d = empty_descriptor()
    seen = set()
    for key in ("currencyrewards", "currencychoicerewards"):
        for pair in entry.get(key) or []:
            try:
                cid, amt = int(pair[0]), int(pair[1])
            except (TypeError, ValueError, IndexError):
                continue
            if cid in seen:
                continue
            seen.add(cid)
            d["currencies"].append(
                {"id": cid, "name": currency_names.get(cid, f"#{cid}"), "amount": amt}
            )
    for pair in entry.get("reprewards") or []:
        try:
            fid, amt = int(pair[0]), int(pair[1])
        except (TypeError, ValueError, IndexError):
            continue
        d["rep"].append({"id": fid, "name": f"#{fid}", "amount": amt})
    item_ids = set()
    for key in ("itemrewards", "itemchoices"):
        for pair in entry.get(key) or []:
            iid = pair[0] if isinstance(pair, (list, tuple)) else pair
            try:
                iid = int(iid)
            except (TypeError, ValueError):
                continue
            if iid in item_ids:
                continue
            item_ids.add(iid)
            d["items"].append({"id": iid, "name": None, "ilvl": None, "track": None})
    d["xp"] = int(entry.get("xp") or 0)
    d["money"] = int(entry.get("money") or 0)
    return d


def descriptor_from_names(currency_names: list[str], item_names: list[str] | None = None,
                          xp: int = 0, money: int = 0) -> dict:
    """Coarse descriptor from scraped reward *names* only (used by wowkb.quest).

    No amounts/ilvl/track — enough for value_quest's baseline goal tagging.
    """
    d = empty_descriptor()
    for n in currency_names:
        d["currencies"].append({"id": None, "name": n, "amount": None})
    for n in item_names or []:
        d["items"].append({"id": None, "name": n, "ilvl": None, "track": None})
    d["xp"], d["money"] = int(xp or 0), int(money or 0)
    return d


# --------------------------------------------------------------------------- #
# Valuation — the "map to find rewards"                                        #
# --------------------------------------------------------------------------- #
def _gear_baseline_R(item: dict) -> tuple[int, str]:
    """Character-agnostic R for a gear item, from its track (else a flat guess)."""
    track = item.get("track")
    if track in TRACK_R:
        return TRACK_R[track], f"{track}-track gear"
    if item.get("ilvl"):
        return 2, "gear (track unknown)"
    return 0, ""


def _value_baseline(descriptor: dict) -> dict:
    goals: set[str] = set()
    notes: list[str] = []
    r_candidates: list[int] = [0]
    confidence = "high"
    unknown_currency = False

    for c in descriptor.get("currencies", []):
        goal, weight, note = classify_currency(c["name"])
        if goal is None:
            unknown_currency = True
            goals.add("gearing")  # unknown reward currency: assume it advances *something*
            notes.append(f"unrecognized currency {c['name']!r}")
            r_candidates.append(1)
            continue
        goals.add(goal)
        if note:
            notes.append(note)
        if goal in POWER_GOALS:
            r_candidates.append(_r_from_weight(weight))

    gear_unranked = False
    for it in descriptor.get("items", []):
        name = (it.get("name") or "").lower()
        if "spark of radiance" in name or "sparks of radiance" in name:
            goals.add("crafting")
            notes.append("Sparks of Radiance -> crafting")
            r_candidates.append(3)
            continue
        r, note = _gear_baseline_R(it)
        if r:
            goals.add("gearing")
            r_candidates.append(r)
            if note:
                notes.append(note)
            if it.get("track") not in TRACK_R:
                gear_unranked = True

    # Container/cache rewards: goals + a FLOORED R derived from the item
    # description (resolve_item runs classify_cache and attaches these). R stays
    # a floor — the gear roll inside the cache is unknown to the API.
    for cache in descriptor.get("caches", []):
        cgoals = cache.get("goals") or []
        for g in cgoals:
            goals.add(g)
        if cache.get("R"):
            r_candidates.append(int(cache["R"]))
        if cgoals:
            notes.append(f"{cache.get('name') or 'cache'} contents "
                         f"({', '.join(cgoals)}) — R floored, gear roll unknown")

    for rep in descriptor.get("rep", []):
        goals.add("renown")
        r_candidates.append(2)
    if descriptor.get("xp"):
        goals.add("xp")
    if descriptor.get("money"):
        goals.add("gold")

    R = min(5, max(r_candidates))
    if not (goals & set(POWER_GOALS)):
        R = 0  # cosmetic-/gold-/xp-only: R=0 on purpose (scoring-model.md)
    if unknown_currency:
        confidence = "low"
    elif gear_unranked:
        confidence = "medium"
    note = "; ".join(dict.fromkeys(notes)) or ("cosmetic/soft rewards only" if R == 0 else "")
    return {"R": R, "goals": sorted(goals), "note": note, "confidence": confidence}


def _value_char_relative(descriptor: dict, char_state: dict) -> dict:
    """Character-relative R (v2b slot-targeting). Implemented + tested, NOT yet wired.

    char_state schema (sourced from wowkb.character when wired):
        {ilvl_by_slot:{slot:ilvl}, track_caps:{track:bool},
         renown:{faction:level}, currencies:{name:amount}}
    Gear rewards score by (reward_ilvl - your weakest relevant slot ilvl): a big
    upgrade to a fresh 90 is high R; the same piece is R=0 for a geared char (below
    slot) or if the piece's track is already capped. Currency scores by whether it
    still advances an uncapped track.
    """
    goals: set[str] = set()
    notes: list[str] = []
    r_candidates: list[int] = [0]
    slot_ilvls = {k: v for k, v in (char_state.get("ilvl_by_slot") or {}).items()
                  if isinstance(v, (int, float))}
    ref = min(slot_ilvls.values()) if slot_ilvls else None   # weakest slot = the target
    track_caps = char_state.get("track_caps") or {}

    for it in descriptor.get("items", []):
        track = it.get("track")
        ilvl = it.get("ilvl")
        if track and track_caps.get(track):
            notes.append(f"{track} track capped -> 0")
            continue
        if ilvl is None:
            continue
        base = ref if ref is not None else ilvl
        delta = ilvl - base
        if delta <= 0:
            notes.append(f"ilvl {ilvl} not above your weakest slot ({base}) -> 0")
            continue
        goals.add("gearing")
        r_candidates.append(min(5, 1 + delta // 5))  # ~every 5 ilvl of upgrade = +1 R
        notes.append(f"+{delta} ilvl over weakest slot")

    for c in descriptor.get("currencies", []):
        goal, weight, note = classify_currency(c["name"])
        if goal is None or goal in SOFT_GOALS:
            if goal:
                goals.add(goal)
            continue
        goals.add(goal)
        # A currency only helps if it advances something not yet capped. We can't
        # map every currency to a track precisely, so honor an explicit track cap
        # keyed by the currency name, else fall back to the baseline weight.
        if track_caps.get(c["name"]):
            notes.append(f"{c['name']} track capped -> 0")
            continue
        if goal in POWER_GOALS:
            r_candidates.append(_r_from_weight(weight))

    R = min(5, max(r_candidates))
    if not (goals & set(POWER_GOALS)):
        R = 0
    return {"R": R, "goals": sorted(goals),
            "note": "; ".join(dict.fromkeys(notes)) or "no character-relevant upgrade",
            "confidence": "medium"}


def value_quest(descriptor: dict, char_state: dict | None = None) -> dict:
    """Value a reward descriptor -> {"R":0-5, "goals":[...], "note":str, "confidence":str}.

    char_state=None -> character-agnostic baseline R (what the catalog/doc use now).
    char_state given -> character-relative R (v2b; built + tested, not yet wired).
    """
    if not descriptor:
        return {"R": 0, "goals": [], "note": "no rewards", "confidence": "low"}
    if char_state is None:
        return _value_baseline(descriptor)
    return _value_char_relative(descriptor, char_state)
