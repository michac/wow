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
# Currency → pending-consumer valuation (needs-first Phase 1)                  #
# --------------------------------------------------------------------------- #
# A currency is only worth farming if the character still has something to SPEND
# it on. "Crests over drops for a geared main" — but a crest source drops to ~0
# once every slot is track-capped and there's nothing left to upgrade. This layer
# values an activity's *declared currency yields* against the char's live state
# (equipped ilvls + track caps), returning 0 when no consumer is pending.
#
FIELD_ACCOLADE_ILVL = 259                    # Hero box Maren sells for Field Accolades
# (HERO_CEILING / MYTH_CREST_R retired — the crest model now uses CREST_CEILING +
#  per-slot track headroom + CREST_FLOOR below, not a flat weakest-slot approximation.)


def _weakest_slot_ilvl(char_state: dict) -> float | None:
    """The char's lowest equipped-slot ilvl (the upgrade target), or None."""
    slots = [v for v in (char_state.get("ilvl_by_slot") or {}).values()
             if isinstance(v, (int, float))]
    return min(slots) if slots else None


def _r_from_headroom(delta: float) -> float:
    """R from ilvl headroom over the weakest slot — same shape as plan.slot_target_R
    (~+1 R per 6 ilvl, foot-in-door at 1), so the currency override reads on the
    same scale as the gear override it competes with in score()."""
    return min(5.0, 1.0 + delta / 6.0)


# Top ilvl each crest track upgrades TO — the crest-headroom ceiling (KB: Champion
# 263, Hero 276, Myth 285). The gear-drop path (best_slot_delta) values off real
# per-slot ilvls, so the old ilvl-band guesser (track_of_ilvl) was removed as dead.
CREST_CEILING = {"Champion": 263, "Hero": 276, "Myth": 285}

# Future-material floor: a crest above current need still banks toward later
# upgrades/crafts (80 Hero → a 259–272 craft, 80 Myth → 272–285; professions.md), so
# it's never worth 0 — but it scores below the 1.0 foot-in-door of a real need, and
# is rarity-scaled (Myth = rarest / highest ceiling) so a bank of Myth crests shows
# up in value counts without ever pulling focus onto Myth-crest content. TUNABLE.
CREST_FLOOR = {"Champion": 0.25, "Hero": 0.5, "Myth": 0.75}


def _crest_upgrade_R(char_state: dict, track: str) -> float:
    """Best CURRENT equipped-upgrade headroom for a `track` crest, from the real
    per-slot track/step (schema>=8): across equipped slots ON that track below cap,
    the largest ilvl gap to the crest ceiling → _r_from_headroom. Falls back to the
    weakest-slot-ilvl approximation when the dump has no track data (pre-schema-8).
    0.0 when there's no on-track sub-cap slot (no current upgrade consumer)."""
    ceiling = CREST_CEILING.get(track)
    if ceiling is None:
        return 0.0
    tbs = char_state.get("track_by_slot") or {}
    ilvl_by_slot = char_state.get("ilvl_by_slot") or {}
    if tbs:
        best = 0.0
        for slot, t in tbs.items():
            if not isinstance(t, dict) or t.get("track") != track:
                continue
            lvl, cap = t.get("level"), t.get("cap")
            if lvl is None or cap is None or lvl >= cap:
                continue                      # capped slot — nothing to crest
            il = ilvl_by_slot.get(slot)
            if isinstance(il, (int, float)) and ceiling - il > 0:
                best = max(best, _r_from_headroom(ceiling - il))
        return best
    # pre-schema-8 fallback: weakest slot ilvl vs the ceiling (old approximation).
    weakest = _weakest_slot_ilvl(char_state)
    if weakest is None or weakest >= ceiling:
        return 0.0
    return _r_from_headroom(ceiling - weakest)


def _crest_consumer(track: str):
    """Build a consumer that values a `track` crest as the max of (a) its current
    equipped-upgrade headroom and (b) a tier-scaled future-material floor — so a
    needed crest scores highest (headroom, up to 5.0) while an above-need crest still
    carries its bankable floor (never 0, always < a real need). The precise
    craft-reagent term is deferred until Spark counts are dumped; the floor is its
    stand-in meanwhile. Returns None only when there's no character state at all."""
    floor = CREST_FLOOR.get(track, 0.0)

    def consume(char_state: dict) -> tuple[float, str] | None:
        if not (char_state.get("ilvl_by_slot")):
            return None
        up = _crest_upgrade_R(char_state, track)
        if up > 0:
            return max(up, floor), f"{track} crests — upgrade on-track gear (headroom)"
        if floor > 0:
            return floor, f"{track} crests — future material (no current {track} upgrade)"
        return 0.0, f"{track} crests — no consumer (geared past {track})"

    return consume


def _consume_field_accolade(char_state: dict) -> tuple[float, str] | None:
    """Field Accolades buy a Hero-track slot piece (~259) from Maren Silverwing.
    Value it as a slot_target vs the weakest slot → ~0 once weakest ≥ 259 (the box
    is a sidegrade). Own-character only; the warbound-cache-for-alts value of a big
    Accolade stockpile is deferred to Phase 4.
    """
    weakest = _weakest_slot_ilvl(char_state)
    if weakest is None:
        return None
    if weakest >= FIELD_ACCOLADE_ILVL:
        return (0.0,
                f"weakest slot ≥ {FIELD_ACCOLADE_ILVL} — Accolade Hero box is a sidegrade")
    delta = FIELD_ACCOLADE_ILVL - weakest
    return (_r_from_headroom(delta),
            f"Accolade Hero box (~{FIELD_ACCOLADE_ILVL}) upgrades weakest slot ({round(weakest)})")


def _consume_none_yet(char_state: dict) -> tuple[float, str] | None:
    """Sparks / spark dust: R=0 this phase — no craft is queued until the crafting
    model (Phase 2) supplies the pending consumer that makes a Spark worth > 0."""
    return 0.0, "no craft queued (Phase 1) — Spark value lands with the craft model (Phase 2)"


# canonical yields.currencies key -> consumer test (char_state -> (R, note) | None)
CURRENCY_CONSUMERS = {
    "champion_crest": _crest_consumer("Champion"),  # now valued (was missing → 0 for cappers)
    "hero_crest": _crest_consumer("Hero"),
    "myth_crest": _crest_consumer("Myth"),
    "field_accolade": _consume_field_accolade,
    "spark": _consume_none_yet,
    "radiant_spark_dust": _consume_none_yet,
}

# canonical key -> a representative currency name, so classify_currency can tag the
# goal (gearing/crafting/…) off the same rules the descriptor path uses.
CANONICAL_CURRENCY_NAME = {
    "hero_crest": "Hero Dawncrest",
    "myth_crest": "Myth Dawncrest",
    "champion_crest": "Champion Dawncrest",
    "veteran_crest": "Veteran Dawncrest",
    "field_accolade": "Field Accolade",
    "spark": "Spark of Radiance",
    "radiant_spark_dust": "Radiant Spark Dust",
    "voidcore": "Nebulous Voidcore",
    "coffer_key_shard": "Coffer Key Shards",
}


# --------------------------------------------------------------------------- #
# Per-slot gear-drop valuation (needs-first Phase 2a)                          #
# --------------------------------------------------------------------------- #
# A gear DROP is only an upgrade if its **landing** ilvl beats the ilvl of a slot
# it can actually fill. The activity declares a `yields.slots` vector — each entry
# a {track, ilvl (LANDING, not the crested ceiling), chance, targeted, slots}. This
# values that vector against the char's live per-slot ilvls, folding in two distinct
# probability effects (needs-first Phase 3): (a) `chance` = drop probability, a
# straight EV multiplier; (b) slot randomness — a `[all]`/multi-slot roll lands on a
# RANDOM slot, so it's valued at the EXPECTED upgrade across its fillable slots, not
# the best one, UNLESS `targeted: true` (a vendor pick where YOU choose the slot).
# A Hero drop lands at 259 (1/6, dawncrests.md), so for a char whose fillable slots
# are all ≥259 it's a sidegrade → delta 0.


def best_slot_delta(yield_slots, ilvl_by_slot: dict) -> tuple[float, str | None, float | None]:
    """Best EFFECTIVE ilvl delta a gear-drop yield vector lands on THIS char.

    Each vector: {ilvl (LANDING, not the crested ceiling), chance (drop
    probability, default 1.0), targeted (slot determinism, default False),
    slots (list of canonical slot names, or ["all"])}. `ilvl_by_slot` is the
    char's live `{slot: ilvl}` map (from the dump).

    Two probability effects, kept separate (needs-first Phase 3):
      (a) `chance` — the chance the activity yields a piece at all → a straight
          EV multiplier (a world-boss drop is < 1; a bonus roll / vendor buy is 1).
      (b) slot randomness — a `slots:[all]` (or multi-slot) roll lands on a RANDOM
          slot, so it's valued at the EXPECTED upgrade across its fillable slots
          (mean of positive per-slot deltas, zeros included), NOT the best one.
          `targeted: true` (a vendor pick like Maren, where YOU choose the slot),
          or a single fillable slot, keeps the exact best-slot value.

    effective_delta = chance * value. Returns the best (effective_delta,
    representative_slot, current_ilvl) across all vectors, or `(0.0, None, None)`
    when nothing is an upgrade. Slot names match case-insensitively (the dump uses
    lowercase `waist`/`finger2`/`mainhand`/…).
    """
    equipped = {str(s).lower(): float(v) for s, v in (ilvl_by_slot or {}).items()
                if isinstance(v, (int, float))}
    best: tuple[float, str | None, float | None] = (0.0, None, None)
    if not equipped:
        return best
    for vec in yield_slots or []:
        if not isinstance(vec, dict):
            continue
        ilvl = vec.get("ilvl")
        if not isinstance(ilvl, (int, float)):
            continue
        chance = vec.get("chance")
        chance = float(chance) if isinstance(chance, (int, float)) else 1.0
        targeted = bool(vec.get("targeted"))
        raw = vec.get("slots") or []
        if isinstance(raw, str):
            raw = [raw]
        if any(str(s).lower() == "all" for s in raw):
            fillable = list(equipped)
        else:
            fillable = [str(s).lower() for s in raw if str(s).lower() in equipped]
        if not fillable:
            continue
        upgrades = [(float(ilvl) - equipped[s], s) for s in fillable
                    if float(ilvl) - equipped[s] > 0]
        if not upgrades:
            continue
        raw_delta, arg_slot = max(upgrades, key=lambda x: x[0])
        # (b) you pick the slot (targeted / single slot) → best slot; else the
        # game picks → expected upgrade over the fillable set (non-upgrades = 0).
        value = (raw_delta if (targeted or len(fillable) == 1)
                 else sum(d for d, _ in upgrades) / len(fillable))
        eff = chance * value          # (a) drop-probability EV
        if eff > best[0]:
            best = (eff, arg_slot, equipped[arg_slot])
    return best


def currency_yield_R(yields_currencies: dict | None,
                     char_state: dict | None) -> tuple[float, str] | None:
    """Best-consumer R across an activity's declared currency yields.

    - None  → the activity declares no currency yield, OR there's no character
      state to value against (caller keeps reward_base).
    - 0.0   → a currency source with NO pending consumer (every yield is capped-out).
    - (R, note) → the strongest pending consumer among the yields.

    `yields_currencies` is `{canonical_key: amount}` (amounts unused this phase —
    the consumer is headroom/gate-based, not quantity-scaled; they're carried for
    the marginal-value math in later phases). Unknown keys contribute nothing.
    """
    if not yields_currencies:
        return None
    if not char_state or not (char_state.get("ilvl_by_slot")):
        return None
    best: tuple[float, str] | None = None
    for key in yields_currencies:
        consumer = CURRENCY_CONSUMERS.get(key)
        if consumer is None:
            continue
        res = consumer(char_state)
        if res is None:
            continue
        if best is None or res[0] > best[0]:
            best = res
    return best


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
