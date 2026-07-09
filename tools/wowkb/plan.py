"""Session planner — rank "what should I do this session?" (efficiency-first).

Implements knowledge/planning/scoring-model.md:  score = (R * U * E) / T, with
gating that subtracts what you've already done this reset. Reset-state that the
Blizzard profile API can't see comes from the PlannerState addon's SavedVariables
dump (michac/wow-planner-state); pass it with --state, or let the tool find it
under the WoW install.

    uv run python -m wowkb.plan --minutes 60
    uv run python -m wowkb.plan --minutes 90 --state /path/to/PlannerState.lua
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from wowkb import rewards
# The Lua dump parser + loaders now live in charstate (the shared 3-source door).
# Re-imported here so `from wowkb.plan import load_state` keeps working for callers
# and the offline test suite. `load()` unions the /ps dump with API + Syndicator.
from wowkb.charstate import (  # noqa: F401
    DEFAULT_REALM, DEFAULT_WOW, load, load_state, parse_savedvar,
)

REPO = Path(__file__).resolve().parents[2]
CANDIDATES = REPO / "knowledge" / "planning" / "candidates.json"
REPEATABLES = REPO / "knowledge" / "planning" / "repeatables.json"
DISCOVERED = REPO / "knowledge" / "planning" / "discovered-weeklies.json"

# Repeatable questIDs the hand-curated candidates.json already covers (via slug
# gates) — skip them when --include-repeatables merges the scraper catalog, so
# prey/void don't show up twice. Mirrors HAND_WIRED in gen_addon_quests.py.
CURATED_QUEST_IDS = {94446, 94385, 94386}

# Enjoyment multipliers (E), capped at 1.5 per the model. Mirror of the table in
# scoring-model.md — that doc is canonical; keep these in sync when you tune.
E_TABLE = {
    "delve": 1.4, "ritual": 1.2, "prey": 1.1, "world": 1.1, "mplus": 1.0,
    "housing": 1.0, "chore": 1.0, "crafting": 0.9, "raid": 0.7, "pvp": 0.4,
}
E_CAP = 1.5
BLOCK_MIN = 15  # minutes per time block
LEVEL_CAP = 90  # Midnight cap (knowledge/_meta/game-version.md) — campaign_incomplete proxy


# --------------------------------------------------------------------------- #
# Gating — is a candidate already done this reset?                             #
# Returns "done" | "todo" | "unknown".                                        #
# --------------------------------------------------------------------------- #
def gate_status(cand: dict, state: dict | None) -> str:
    g = cand.get("gate", {})
    t = g.get("type")
    if t == "always":
        return "todo"                       # standing content is never "done"
    if t == "manual":
        return "unknown"                    # planner can't see it
    if state is None:
        return "unknown"                    # no dump → can't gate the rest

    if t == "vault_has_rewards":
        vault = state.get("vault") or {}
        return "done" if not vault.get("hasRewards", False) else "todo"
    if t == "mplus_weekly_lt":
        runs = state.get("mythicPlus") or []
        done = sum(1 for r in runs if isinstance(r, dict) and r.get("thisWeek"))
        return "todo" if done < g.get("n", 8) else "done"
    if t == "weekly_quest":
        want = str(g.get("quest"))
        matches = [q for q in (state.get("weeklyQuests") or [])
                   if isinstance(q, dict)
                   and (q.get("label") == g.get("quest") or str(q.get("id")) == want)]
        if not matches:
            return "unknown"                # quest ID(s) not configured in the addon
        # A slug may map to several quests (e.g. a rotating weekly present under two
        # zone IDs); it's done if ANY of them is flagged complete.
        return "done" if any(q.get("complete") for q in matches) else "todo"
    if t == "lockout":
        needle = (g.get("name_contains") or "").lower()
        for lk in state.get("lockouts") or []:
            if isinstance(lk, dict) and needle in (lk.get("name") or "").lower():
                return "done"
        return "todo"
    if t == "raid_weekly":
        # Weekly raid kill. GetSavedInstanceInfo lockouts (state.lockouts, each with
        # name/isRaid/defeated) list the raids you're saved to this reset. Match the
        # raid by name; "done" once it's a raid lockout with >=1 boss defeated. A
        # single-boss raid (Sporefall) is "done" on the first difficulty cleared —
        # higher-difficulty re-kills for vault/ilvl are valued separately by the raid
        # vault breakpoint, so gating on any kill doesn't lose that signal.
        needle = (g.get("name_contains") or g.get("raid") or "").lower()
        if not needle:
            return "unknown"                # gate carries no matchable raid name
        for lk in state.get("lockouts") or []:
            if (isinstance(lk, dict) and lk.get("isRaid")
                    and needle in (lk.get("name") or "").lower()
                    and (lk.get("defeated") or 0) >= 1):
                return "done"
        return "todo"
    if t == "campaign_incomplete":
        # The Midnight main-story campaign is one-time and unlocks the endgame loop
        # (WQs, renown, Adventure Mode). The dump carries no campaign-complete flag,
        # so use level as a proxy: a max-level char has cleared the leveling spine and
        # this row should hide; a sub-cap roster member still needs it. Level absent →
        # unknown. (A precise campaign flag is a future PlannerState field.)
        lvl = state.get("level")
        if not isinstance(lvl, (int, float)):
            return "unknown"
        return "done" if lvl >= LEVEL_CAP else "todo"
    if t == "world_boss_weekly":
        # World bosses aren't returned by GetSavedInstanceInfo (the old 'lockout'
        # gate never fired). PlannerState schema>=3 emits a worldBosses[] block from
        # GetSavedWorldBossInfo — which lists only bosses ALREADY KILLED this reset,
        # exactly the weekly lockout signal. Mirror event_active's missing-key rule.
        wb = state.get("worldBosses")
        if wb is None:
            return "unknown"                # dump predates worldBosses (schema < 3)
        return "done" if wb else "todo"
    if t == "vault_track":
        # Delves/world activities aren't quest-flagged — their weekly motive is
        # Great Vault progress. Done once the named column is capped (its top
        # threshold met); the dump carries per-column progress+thresholds.
        # NOTE: the 'world' column counts world activities broadly (delves + world
        # bosses + …), so this is a delve *proxy*, not a pure delve counter.
        prog, thr = _vault_track(g.get("track"), state)
        if prog is None or not thr:
            return "unknown"
        return "done" if prog >= thr[-1] else "todo"
    if t == "event_active":
        # Fun radar: surface a candidate only while its calendar event is live.
        cal = state.get("calendar")
        if cal is None:
            return "unknown"                # dump predates the calendar block (schema < 2)
        needle = (g.get("match") or "").lower()
        live = any(isinstance(e, dict) and e.get("active")
                   and needle in (e.get("title") or "").lower()
                   for e in cal)
        return "todo" if live else "done"   # not live now → drop it from the plan
    return "unknown"


# --------------------------------------------------------------------------- #
# Scoring                                                                      #
# --------------------------------------------------------------------------- #
DEFAULT_VAULT_THRESHOLDS = [1, 4, 8]


def _slot_thresholds(state: dict, track: str) -> list[int] | None:
    """Sorted unlock thresholds for a vault column, straight from the dump."""
    vault = state.get("vault") or {}
    thr = sorted(int(s["threshold"]) for s in (vault.get("slots") or [])
                 if isinstance(s, dict) and s.get("type") == track
                 and s.get("threshold") is not None)
    return thr or None


def _vault_track(track: str, state: dict | None) -> tuple[int | None, list[int] | None]:
    """(progress, thresholds) for a breakpoint track, both from live dump state.

    'mplus' counts this-week M+ runs (the gate's signal) and borrows the dungeon
    column's thresholds (Midnight reports M+ under the dungeon vault type). Any
    other track reads vault.slots[type].progress + its own thresholds — so we no
    longer assume [1,4,8]; delve/world/raid columns each carry their real cutoffs
    (observed live: world 2/4/6, dungeon 2/4/8, raid 1/4/8).
    """
    if not state:
        return None, None
    if track == "mplus":
        runs = state.get("mythicPlus") or []
        prog = sum(1 for r in runs if isinstance(r, dict) and r.get("thisWeek"))
        return prog, _slot_thresholds(state, "dungeon")
    vault = state.get("vault") or {}
    slots = [s for s in (vault.get("slots") or [])
             if isinstance(s, dict) and s.get("type") == track]
    if not slots:
        return None, None
    prog = max(int(s.get("progress") or 0) for s in slots)
    return prog, _slot_thresholds(state, track)


def breakpoint_R(cand: dict, state: dict | None) -> tuple[float, str] | None:
    """Breakpoint-proximity override for R (scoring-model.md 'breakpoint proximity').

    Returns (R, why-note) when a candidate carries a vault breakpoint AND live
    progress is known: R=4 for the run that *crosses* the next threshold, R=0
    once the track is capped, else the flat reward_base (progress is mid-track,
    no breakpoint nearby). Returns None when there's no breakpoint or no state to
    read — the caller then keeps reward_base and scores exactly as before.
    """
    bp = cand.get("breakpoint")
    if not bp or bp.get("type") != "vault":
        return None
    n, dump_thr = _vault_track(bp.get("track"), state)
    if n is None:
        return None
    thr = dump_thr or sorted(bp.get("thresholds") or DEFAULT_VAULT_THRESHOLDS)
    if n >= thr[-1]:
        return 0.0, "vault track capped"
    if (n + 1) in thr:
        return 4.0, f"next run unlocks vault slot {thr.index(n + 1) + 1}"
    return float(cand.get("reward_base", 0)), ""


def quest_progress_note(cand: dict, state: dict | None) -> str:
    """'1/3'-style partial progress for a weekly_quest candidate, else ''.

    Reads have/need off the matched dumped quest (schema>=5). Only shows while the
    quest is in-log and unfinished — a turned-in weekly is already gated 'done'.
    """
    g = cand.get("gate", {})
    if g.get("type") != "weekly_quest" or not state:
        return ""
    want = str(g.get("quest"))
    for q in state.get("weeklyQuests") or []:
        if not isinstance(q, dict):
            continue
        if q.get("label") == g.get("quest") or str(q.get("id")) == want:
            have, need = q.get("have"), q.get("need")
            if isinstance(have, (int, float)) and isinstance(need, (int, float)) and need:
                return f"{int(have)}/{int(need)}"
    return ""


def weakest_slots(state: dict | None, k: int = 3) -> list[tuple[str, float]]:
    """The k lowest-ilvl equipped slots from the dump (planner v2b context).

    schema>=4 dumps per-slot ilvls; older dumps omit `equipment` → empty list.
    """
    eq = (state or {}).get("equipment") or []
    rows = [(s.get("slot"), s.get("ilvl")) for s in eq
            if isinstance(s, dict) and isinstance(s.get("ilvl"), (int, float))]
    rows.sort(key=lambda r: r[1])
    return rows[:k]


def currency_context(state: dict | None) -> str:
    """A one-line crest/currency balance summary (needs-first Phase 1 context).

    Surfaces the gearing currencies from the dump and flags the *bottleneck* — the
    smaller of the Hero/Myth crest balances — so "Myth is the binding constraint"
    is visible next to the plan. schema≥4 dumps `currencies`; older dumps → ''.
    """
    curs = {c.get("name"): c.get("quantity") for c in (state or {}).get("currencies") or []
            if isinstance(c, dict) and c.get("name")}
    if not curs:
        return ""
    hero = curs.get("Hero Dawncrest")
    myth = curs.get("Myth Dawncrest")
    # bottleneck = the scarcer crest tier (Myth for Encomplete: 20 vs 176 Hero).
    bottleneck = None
    if isinstance(hero, (int, float)) and isinstance(myth, (int, float)):
        bottleneck = "Myth Dawncrest" if myth <= hero else "Hero Dawncrest"
    order = [("Hero Dawncrest", "Hero"), ("Myth Dawncrest", "Myth"),
             ("Field Accolade", "Field Accolade"), ("Nebulous Voidcore", "Voidcore"),
             ("Coffer Key Shards", "Coffer shards")]
    parts = []
    for name, label in order:
        v = curs.get(name)
        if isinstance(v, (int, float)):
            tag = " (bottleneck)" if name == bottleneck else ""
            parts.append(f"{label} {int(v):,}{tag}")
    return " · ".join(parts)


def _slot_ilvls(state: dict | None) -> list[float]:
    """Every equipped slot's ilvl from the dump (schema>=4), else []."""
    eq = (state or {}).get("equipment") or []
    return [float(s["ilvl"]) for s in eq
            if isinstance(s, dict) and isinstance(s.get("ilvl"), (int, float))]


def slot_target_R(cand: dict, state: dict | None) -> tuple[float, str] | None:
    """Ilvl-relative reward: is this activity's gear an upgrade to THIS char?

    Two paths, preferring the per-slot vector (needs-first Phase 2a):

    - **`yields.slots`** (a list of `{track, ilvl, chance, slots}` vectors where
      `ilvl` is the drop's *landing* ilvl — Hero 1/6 = 259, not the crested 276
      ceiling): value it per-slot via `rewards.best_slot_delta` — the best positive
      delta across every slot the drop can fill (`[all]` = any equipped slot). No
      positive delta anywhere → R=0 (the drop lands ≤ your slots; a sidegrade).
      This kills the old "one weak slot inflates every Hero-ceiling activity" bug.
    - **`reward_ilvl_max`** (scalar ceiling, un-migrated activities — raid keeps its
      per-difficulty ceiling): unchanged — the top ilvl its gear can reach compared
      to the char's *weakest* equipped slot.

    Returns None when the activity has neither field, or the dump carries no
    per-slot ilvls (schema<4) — the caller then keeps reward_base, as before.
    """
    yield_slots = (cand.get("yields") or {}).get("slots")
    if yield_slots:
        ilvl_by_slot = _char_state(state)["ilvl_by_slot"]
        if not ilvl_by_slot:
            return None                      # pre-schema-4 dump — keep reward_base
        delta, slot, cur = rewards.best_slot_delta(yield_slots, ilvl_by_slot)
        if delta <= 0:
            return 0.0, "no slot upgrade — drop lands ≤ your slots"
        # ~+1 R per 6 ilvl of headroom, foot-in-door at 1 (same scale as below).
        R = min(5.0, 1.0 + delta / 6.0)
        return R, f"+{round(delta)} ilvl over {slot} ({round(cur)})"

    ceiling = cand.get("reward_ilvl_max")
    if not isinstance(ceiling, (int, float)):
        return None
    slots = _slot_ilvls(state)
    if not slots:
        return None
    weakest = min(slots)
    delta = ceiling - weakest
    if delta <= 0:
        return 0.0, f"reward ≤ your weakest slot ({round(weakest)})"
    # ~+1 R per 6 ilvl of headroom over the weakest slot, foot-in-door at 1.
    R = min(5.0, 1.0 + delta / 6.0)
    return R, f"+{round(delta)} ilvl over weakest slot ({round(weakest)})"


def _char_state(state: dict | None) -> dict:
    """Shape the dump into rewards.py's char_state schema (needs-first Phase 1).

    schema≥4 dumps per-slot `equipment` (itemID/ilvl/slot) and `currencies`
    (name/quantity). We map both into {ilvl_by_slot, currencies, track_caps}. The
    dump carries no upgrade track/level, so track_caps stays empty and the crest
    consumers approximate headroom from ilvl vs the Hero ceiling (rewards.py).
    """
    eq = (state or {}).get("equipment") or []
    ilvl_by_slot = {s["slot"]: float(s["ilvl"]) for s in eq
                    if isinstance(s, dict) and s.get("slot")
                    and isinstance(s.get("ilvl"), (int, float))}
    curs = {c["name"]: c.get("quantity") for c in (state or {}).get("currencies") or []
            if isinstance(c, dict) and c.get("name")}
    return {"ilvl_by_slot": ilvl_by_slot, "currencies": curs, "track_caps": {}}


def currency_R(cand: dict, state: dict | None) -> tuple[float, str] | None:
    """Currency-yield override for R: value this activity's declared crest/accolade
    yields by whether THIS char still has a consumer for them (needs-first Phase 1).

    Returns None when the candidate declares no `yields.currencies` or the dump
    carries no equipment (caller keeps reward_base); else delegates to
    rewards.currency_yield_R — 0 when the currency has no pending consumer (a
    Hero-capped main), high when a crest still fills a sub-cap slot.
    """
    yields = (cand.get("yields") or {}).get("currencies")
    if not yields:
        return None
    return rewards.currency_yield_R(yields, _char_state(state))


def score(cand: dict, mood: str, state: dict | None = None) -> tuple[float, str, str]:
    R = float(cand.get("reward_base", 0))
    U = float(cand.get("urgency", 1))
    floor = 2 if mood == "fun" else 1          # collectible R-floor
    cap = 3.0 if mood == "fun" else E_CAP
    if R == 0 and U >= 1.5:                    # rare cosmetic gets a foot in the door
        R = floor
    note = ""
    # R overrides: take the strongest of "crosses a vault threshold" (breakpoint
    # proximity), "upgrades my weakest slot" (ilvl-relative), and "the currency it
    # yields still has a consumer" (needs-first Phase 1). When none has data (no
    # breakpoint/ceiling/currency-yield, or a pre-schema-4 dump) fall back to
    # reward_base exactly as before. See scoring-model.md.
    overrides = [ov for ov in (breakpoint_R(cand, state),
                               slot_target_R(cand, state),
                               currency_R(cand, state)) if ov is not None]
    if overrides:
        R, note = max(overrides, key=lambda ov: ov[0])
    # Enjoyment: honor an explicit numeric `enjoyment`, else the (venue-keyed) table.
    if isinstance(cand.get("enjoyment"), (int, float)):
        E = min(float(cand["enjoyment"]), cap)
    else:
        E = min(E_TABLE.get(cand.get("enjoyment_key", "chore"), 1.0), cap)
    T = float(cand.get("time_blocks", 1)) or 0.1
    s = (R * U * E) / T
    # dominant-term reason
    terms = {"power": R, "urgency": U, "enjoyment": E}
    lead = max(terms, key=terms.get)
    return s, lead, note


def load_candidates(include_repeatables: bool) -> list[dict]:
    """Curated candidates.json, optionally merged with the scraper catalog.

    candidates.json is the hand-tuned default. --include-repeatables folds in
    repeatables.json (auto-generated by wowkb.repeatables) for fuller coverage —
    minus the questIDs candidates.json already curates (CURATED_QUEST_IDS), so
    prey/void don't double up. Repeatable T/E are scraper placeholders
    (time_blocks=1, enjoyment=chore) — flagged in the output, tune in the JSON.
    """
    cands = list(json.loads(CANDIDATES.read_text())["candidates"])
    if not include_repeatables or not REPEATABLES.exists():
        return cands
    for c in json.loads(REPEATABLES.read_text()).get("candidates", []):
        if c.get("questID") in CURATED_QUEST_IDS:
            continue
        c = dict(c)
        c["_repeatable"] = True
        cands.append(c)
    return cands


def plan(minutes: int, state: dict | None, mood: str,
         include_repeatables: bool = False) -> dict:
    candidates = load_candidates(include_repeatables)
    budget = minutes / BLOCK_MIN
    rows = []
    for c in candidates:
        st = gate_status(c, state)
        if st == "done":
            continue
        s, lead, note = score(c, mood, state)
        prog = quest_progress_note(c, state)
        note = " · ".join(x for x in (f"at {prog}" if prog else "", note) if x)
        rows.append({"c": c, "score": s, "lead": lead, "state": st, "note": note})
    rows.sort(key=lambda r: r["score"], reverse=True)

    picks, spent = [], 0.0
    for r in rows:
        t = float(r["c"].get("time_blocks", 1))
        if spent + t <= budget + 1e-9:
            picks.append(r); spent += t
    return {"picks": picks, "all": rows, "budget": budget, "spent": spent}


# --------------------------------------------------------------------------- #
def _fmt_age(mtime: float) -> str:
    """Human 'how old is this dump' from an mtime, e.g. '2h ago', '3d ago'."""
    import time
    secs = max(0, time.time() - mtime)
    if secs < 90:
        return "just now"
    for unit, n in (("d", 86400), ("h", 3600), ("m", 60)):
        if secs >= n:
            return f"{int(secs // n)}{unit} ago"
    return "just now"


def _fmt(r: dict) -> str:
    c = r["c"]
    mins = round(float(c.get("time_blocks", 1)) * BLOCK_MIN)
    flag = " (?)" if r["state"] == "unknown" else ""
    src = " ~" if c.get("_repeatable") else ""   # ~ = scraper catalog (placeholder T/E)
    note = f" · {r['note']}" if r.get("note") else ""
    return (f"  {r['score']:6.1f}{src:1}  [{mins:>3}m] {c['name']:<42} "
            f"— {c['why']}{note}{flag}")


# --------------------------------------------------------------------------- #
# Gearing view — the per-slot cache/crest chart (routing target for            #
# "how do I gear up X"). Track is inferred from ilvl bands, since the profile   #
# API doesn't expose the numeric upgrade track (charstate notes this).         #
# --------------------------------------------------------------------------- #
# Enum.QuestFrequency weekly-ish cadences: 2 = Weekly, 3 = ResetByScheduler
# (Midnight Special Assignments / pillar weeklies live-observed at 3). 1 = Daily,
# 0 = Default → not weekly. Both 2 and 3 reset weekly, so both are watchlist-worthy.
WEEKLY_FREQ = {2, 3}

TIER_SLOTS = {"head", "shoulder", "chest", "hands", "legs"}
# Decimus "Knocking Off the Top" gives ONE free Myth 272 among these three slots.
QUEST_SLOTS = {"back": "cloak", "waist": "belt", "wrist": "bracers"}
CHAMPION_CACHE_ACC = 100        # slot-specific warbound Champion cache (Field Accolades)
HERO_CACHE_ACC = 750           # slot-specific warbound Hero cache
SLOT_ORDER = ["head", "neck", "shoulder", "chest", "waist", "legs", "feet", "wrist",
              "hands", "finger1", "finger2", "trinket1", "trinket2", "back",
              "mainhand", "offhand"]


def _band(ilvl: float | None) -> str:
    """Midnight S1 ilvl → upgrade-track band (great-vault.md / dawncrests.md).
    Bands overlap in reality; these floors are the pragmatic classifier the KB uses.
    """
    if not isinstance(ilvl, (int, float)):
        return "?"
    if ilvl >= 277:
        return "myth"
    if ilvl >= 259:
        return "hero"
    if ilvl >= 246:
        return "champion"
    if ilvl >= 233:
        return "veteran"
    return "adventurer"


def _slot_reco(slot: str, band: str) -> str:
    tier = slot in TIER_SLOTS
    if band in ("adventurer", "veteran"):                      # sub-Champion
        if tier:
            return f"Champion cache ({CHAMPION_CACHE_ACC} acc) — stopgap + catalyst fodder"
        return (f"Champion cache ({CHAMPION_CACHE_ACC}) now → Hero cache "
                f"({HERO_CACHE_ACC}) as accolades allow")
    if band == "champion":
        return f"Hero cache ({HERO_CACHE_ACC}) or Hero drop, then crest up"
    if band == "hero":
        return "crest up (Hero → 276)"
    if band == "myth":
        return "—"
    return "(unknown ilvl)"


def _norm_slot(s: str | None) -> str:
    """Canonicalize a slot name across sources — dumps use 'finger1', fixtures
    'FINGER_1', the API 'Finger 1' — all collapse to 'finger1'."""
    return (s or "").lower().replace("_", "").replace(" ", "")


def gear_rows(state: dict | None) -> list[dict]:
    """Per-slot gearing rows from the unified state's equipment (ilvl + band + reco)."""
    eq = {_norm_slot(s.get("slot")): s for s in (state or {}).get("equipment") or []
          if isinstance(s, dict) and s.get("slot")}
    rows = []
    for slot in SLOT_ORDER:
        s = eq.get(slot)
        if not s:
            continue
        ilvl = s.get("ilvl")
        band = _band(ilvl)
        rows.append({
            "slot": slot, "ilvl": ilvl, "band": band, "tier": slot in TIER_SLOTS,
            "name": s.get("name"), "reco": _slot_reco(slot, band),
        })
    return rows


def render_gear(state: dict | None) -> str:
    """The gearing chart: per-slot targets + the accolade-allocation heuristic.
    This is the home for "how do I gear up X" — run it instead of re-deriving from
    the KB by hand.
    """
    rows = gear_rows(state)
    if not rows:
        return ("No equipment in the state (need a schema>=4 /ps dump or the profile "
                "API). Run /ps + /reload on the character, or drop --no-enrich.")
    L = []
    name = (state or {}).get("character") or "character"
    il = (state or {}).get("equippedIlvl")
    head = f" (equipped ilvl {round(il)})" if isinstance(il, (int, float)) and il else ""
    L.append(f"Gearing plan · {name}{head}")
    L.append("")

    sub = [r for r in rows if r["band"] in ("adventurer", "veteran")]
    champ = [r for r in rows if r["band"] == "champion"]
    higher = [r for r in rows if r["band"] in ("hero", "myth")]

    def _line(r):
        tier = " ·tier" if r["tier"] else ""
        quest = f" ·quest-slot({QUEST_SLOTS[r['slot']]})" if r["slot"] in QUEST_SLOTS else ""
        nm = f" {r['name']}" if r.get("name") else ""
        return f"  {r['slot']:<9} {str(r['ilvl']):>4}{tier}{quest} — {r['reco']}{nm}"

    if sub:
        L.append(f"BAND 1 — sub-Champion, fix first ({len(sub)} slots):")
        for r in sorted(sub, key=lambda r: r["ilvl"] or 0):
            L.append(_line(r))
        L.append("")
    if champ:
        L.append("BAND 2 — Champion (Hero caches / crest up):")
        for r in sorted(champ, key=lambda r: r["ilvl"] or 0):
            L.append(_line(r))
        L.append("")
    if higher:
        L.append("BAND 3 — Hero+ (crest up / recraft to 285):")
        for r in sorted(higher, key=lambda r: r["ilvl"] or 0):
            L.append(_line(r))
        L.append("")

    # Accolade-allocation heuristic (mirrors the by-hand rule).
    n = len(sub)
    quest_sub = [r for r in sub if r["slot"] in QUEST_SLOTS]
    floor_slots = max(0, n - (1 if quest_sub else 0))   # one weak quest-slot is free
    floor = floor_slots * CHAMPION_CACHE_ACC
    curs = {c.get("name"): c.get("quantity")
            for c in (state or {}).get("currencies") or [] if isinstance(c, dict)}
    acc = curs.get("Field Accolade") or curs.get("Field Accolades")
    L.append("Accolade heuristic:")
    L.append(f"- {n} sub-Champion slot(s). Champion-cap floor ≈ {floor} accolades"
             + (f" (one of {{{', '.join(QUEST_SLOTS[r['slot']] for r in quest_sub)}}} "
                "comes free from Decimus 'Knocking Off the Top' — take the weakest)"
                if quest_sub else "") + ".")
    L.append(f"- Each +{HERO_CACHE_ACC - CHAMPION_CACHE_ACC} accolades over the floor "
             "upgrades one planned Champion slot to Hero. Spend Hero on NON-tier slots first.")
    L.append("- If a Hero conversion is close but short, farm the gap (Val/Naigtal Heroic "
             "≈ 1,700 acc / couple hrs; 60/rare) — don't settle for Champion.")
    if isinstance(acc, (int, float)):
        L.append(f"- This character holds {int(acc):,} Field Accolades.")
    L.append("- Caches are warbound (buy on any char, mail over); upgrade CRESTS are not — "
             "each character earns its own. Tier slots → 4pc via catalyst / vault tier drops.")
    return "\n".join(L)


def _state_banner(state: dict | None) -> str:
    """One-line 'where did this state come from' header, incl. which sources loaded."""
    if not state:
        return "no PlannerState dump, no API — gates marked (?)"
    parts = []
    path = state.get("_path")
    if path:
        # Dump mtime → a stale dump (played a different char since) is obvious.
        try:
            age = _fmt_age(os.path.getmtime(path))
        except OSError:
            age = "?"
        parts.append(f"{Path(path).name} (char {state.get('character', '?')}, dumped {age})")
    else:
        parts.append("no /ps dump")
    srcs = state.get("_sources") or {}
    live = [n for n, ok in (("API", srcs.get("blizzard_api")),
                            ("Syndicator", srcs.get("syndicator"))) if ok]
    if live:
        parts.append("+ " + " + ".join(live))
    return "state: " + " ".join(parts)


def discover_weeklies(state: dict | None, write: bool = True) -> list[dict]:
    """Weekly quests the /ps active-log dump reveals that the addon watchlist
    doesn't track yet — the auto-list half of the "no manual ID hunting" design.

    The watchlist (state.weeklyQuests) only reports quests it already knows; the
    schema>=6 active-quest-log block (state.activeQuests) sees everything currently
    accepted. Any weekly-frequency quest in the log but NOT in the watchlist is
    persisted to knowledge/planning/discovered-weeklies.json (dedup by questID) so
    it survives across runs, and returned so the caller can print a promote-me TODO.
    No addon edit / release happens here (that needs verification + a GitHub
    release); this only maintains the data list.
    """
    active = (state or {}).get("activeQuests") or []
    if not active:
        return []                               # pre-schema-6 dump: no active-log block
    known = {q.get("id") for q in (state.get("weeklyQuests") or [])
             if isinstance(q, dict)}
    master: dict = {}
    if DISCOVERED.exists():
        try:
            for e in json.loads(DISCOVERED.read_text()).get("discovered", []):
                master[e.get("questID")] = e
        except Exception:  # noqa: BLE001 — a corrupt list shouldn't break the plan
            master = {}
    fresh = []
    for q in active:
        if not isinstance(q, dict) or q.get("frequency") not in WEEKLY_FREQ:
            continue
        qid = q.get("id")
        if qid is None or qid in known or qid in master:
            continue
        entry = {
            "questID": qid, "title": q.get("title"),
            "frequency": q.get("frequency"), "campaign": q.get("campaign"),
            "seen_on": state.get("character"),
            "note": "auto-discovered by wowkb.plan — verify vs the live build, then "
                    "add to KNOWN_REPEATABLES in tools/wowkb/repeatables.py, regen "
                    "(wowkb.repeatables + wowkb.gen_addon_quests), and cut an addon release",
        }
        master[qid] = entry
        fresh.append(entry)
    if fresh and write:
        DISCOVERED.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "_note": "Auto-maintained by wowkb.plan from the PlannerState /ps "
                     "active-quest-log dump (schema>=6). Weekly-frequency quests not "
                     "in the addon watchlist land here. Verify each against the live "
                     "build, promote into KNOWN_REPEATABLES (tools/wowkb/repeatables.py), "
                     "regen repeatables.json + PlannerState_Quests.lua, then cut an "
                     "addon release. Safe to edit/prune by hand.",
            "discovered": sorted(master.values(), key=lambda e: e.get("questID") or 0),
        }
        DISCOVERED.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    return fresh


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="wowkb.plan", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--minutes", type=int, default=60, help="session time budget")
    p.add_argument("--mood", choices=["efficiency", "fun"], default="efficiency")
    p.add_argument("--state", help="path to PlannerState.lua (else auto-find)")
    p.add_argument("--character", help="restrict auto-find to this character's dump "
                                       "(else newest dump across the roster wins)")
    p.add_argument("--realm", default=DEFAULT_REALM, help=f"realm slug (default: {DEFAULT_REALM})")
    p.add_argument("--wow-path", default=DEFAULT_WOW)
    p.add_argument("--no-enrich", action="store_true",
                   help="skip the Blizzard API + Syndicator enrichment (offline / faster; "
                        "gates + weakest-slot still work from the /ps dump alone)")
    p.add_argument("--no-discover", action="store_true",
                   help="don't persist newly-seen weeklies to discovered-weeklies.json")
    p.add_argument("--gear", action="store_true",
                   help="print the per-slot gearing chart (cache/crest targets + the "
                        "accolade heuristic) instead of the session activity plan")
    p.add_argument("--include-repeatables", action="store_true",
                   help="also rank the scraper catalog (repeatables.json); "
                        "rows marked ~ have placeholder time/enjoyment")
    args = p.parse_args(argv)

    state = load(character=args.character, realm=args.realm, wow_path=args.wow_path,
                 state_path=args.state, enrich=not args.no_enrich)

    if args.gear:
        print(f"\n{_state_banner(state)}\n")
        print(render_gear(state))
        return 0

    result = plan(args.minutes, state, args.mood, args.include_repeatables)
    fresh = discover_weeklies(state, write=not args.no_discover)

    print(f"\nSession plan · {args.minutes} min · mood={args.mood} · {_state_banner(state)}\n")
    weak = weakest_slots(state)
    if weak:
        il = state.get("equippedIlvl")
        head = f"equipped ilvl {round(il)}" if isinstance(il, (int, float)) and il else "gear"
        slots = ", ".join(f"{s} {round(v)}" for s, v in weak)
        print(f"weakest slots ({head}): {slots}")
    cur = currency_context(state)
    if cur:
        print(f"crests: {cur}")
    if weak or cur:
        print()
    print(f"DO THIS ({round(result['spent']*BLOCK_MIN)} of {args.minutes} min):")
    for r in result["picks"]:
        print(_fmt(r))
    rest = [r for r in result["all"] if r not in result["picks"]]
    if rest:
        print("\nbacklog (didn't fit / lower value):")
        for r in rest:
            print(_fmt(r))
    if fresh:
        print("\n(+) new weeklies seen in the /ps quest log (not yet tracked by the addon):")
        for e in fresh:
            camp = " [campaign]" if e.get("campaign") else ""
            print(f"    {e['questID']}  {e.get('title') or '?'}{camp}")
        print(f"    → logged to knowledge/planning/{DISCOVERED.name}; verify, add to "
              "KNOWN_REPEATABLES,\n      regen (wowkb.repeatables + gen_addon_quests), then cut an addon release.")
    if not (state or {}).get("_path"):
        print("\n(!) No PlannerState dump found. Install michac/wow-planner-state, /ps + /reload,")
        print("    then re-run so delve/prey/vault gates resolve instead of showing (?).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
