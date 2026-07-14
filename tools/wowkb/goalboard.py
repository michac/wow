"""Goal board — the deterministic, read-only "board" the gearing agent reasons over.

This is the **facts** half of the goal-centric gearing model
(`knowledge/planning/goal-model.md`): the exact, tedious per-slot state and the
enumerated upgrade *candidates* (with mechanical facts + affordability from the
real mat pool), plus warband-level gate states and cross-character facts. It does
**NOT** rank, pare, cluster, or sequence — that judgment is the agent's job, done
over this board using goal-model.md as its rubric. See the "board vs. agent" split
in that doc.

Everything here is derived from the unified character state
(`wowkb.charstate.load`, which unions the /ps dump + Blizzard API + Syndicator).
The board renders offline from the /ps dump alone; Syndicator-only fields
(sparks/voidshards via `item_counts`) degrade silently and are flagged absent.

Consumed by `wowkb.plan --board [--json]`. Reuses plan.py's slot helpers
(SLOT_ORDER / TIER_SLOTS / _norm_slot) and rewards.CREST_CEILING so the board and
the scorer never disagree on a fact.
"""

from __future__ import annotations

import glob
import json
import os
import re
import subprocess
from pathlib import Path

from wowkb import charstate, rewards
from wowkb.plan import (
    CHAMPION_CACHE_ACC, HERO_CACHE_ACC, SLOT_ORDER, TIER_SLOTS, _norm_slot,
)

REPO = Path(__file__).resolve().parents[2]
CHAR_DIR = REPO / "knowledge" / "characters"
CANDIDATES = REPO / "knowledge" / "planning" / "candidates.json"

# --------------------------------------------------------------------------- #
# Item / currency IDs (all datamined + verified 2026-07-10).                   #
# --------------------------------------------------------------------------- #
SPARK_ITEM = 232875          # Spark of Radiance (Syndicator item_counts)
VOIDSHARD_ITEM = 268650      # Ascendant Voidshard (Syndicator item_counts)
CRACKED_KEYSTONE_ITEM = 253245  # one-time M+ unlock quest item (dawncrests.md)
CATALYST_CURRENCY = "Dawnlight Manaflux"   # currency 3378 — catalyst charges

# The mat balances a warband pool cares about — {display: source}. Currencies
# (crests/accolades/marl/manaflux) live in the /ps dump; sparks/voidshards come
# from Syndicator item_counts (absent offline).
POOL_CURRENCIES = [
    "Adventurer Dawncrest", "Veteran Dawncrest", "Champion Dawncrest",
    "Hero Dawncrest", "Myth Dawncrest", "Field Accolade", "Voidlight Marl",
    CATALYST_CURRENCY,
]

# The "…of the Dawn" threshold: 263 in every slot earns *Champion of the Dawn*
# → the 50% warband Champion-crest discount (dawncrests.md). "sub-263 slot count"
# = how many steps from that gate a character is → who's cheapest to gate.
DAWN_CHAMPION_ILVL = 263

# --------------------------------------------------------------------------- #
# Deterministic source facts — the catalog the candidate enumerator reads.     #
# Numbers + flags from dawncrests.md / professions.md / catalyst.md /          #
# activities/val-naigtal.md / factions/{harati,silvermoon-court,amani-tribe}.  #
# --------------------------------------------------------------------------- #
# Champion ilvl ladder (dawncrests.md): 246(1/6) 250 253 256 259(5/6) 263(6/6).
CHAMPION_LADDER = [246, 250, 253, 256, 259, 263]

# ~20 Champion crests/rank (koroboost; 246→263 = 5 steps ≈ 100). The KB has NO
# exact per-step table for Hero/Myth, so this is a COARSE estimate used only for
# the "affordable now?" flags — the board leans on STEP COUNT for effort, never
# claims exact crest totals (goal-model.md).
CREST_PER_STEP_EST = 20

CRAFT = {
    # non-tier slots only (tier slots excluded — catalyst.md). 80 crests + 2 sparks
    # (4 for a 2H weapon) + gold. Yields depend on the crest tier used.
    "Hero": {"crest": "Hero Dawncrest", "crest_qty": 80, "yields_ilvl": 272},
    "Myth": {"crest": "Myth Dawncrest", "crest_qty": 80, "yields_ilvl": 285},
    "sparks": 2, "sparks_2h": 4,
}

CATALYST = {"charge_currency": CATALYST_CURRENCY, "cap": 8}

MAREN = {"track": "Hero", "yields_ilvl": 259, "cost_currency": "Field Accolade",
         # 750 = the TARGETED cache (you pick the slot). A cheaper 500-accolade cache
         # exists but is RNG/random-slot — the board models the deterministic targeted
         # path. Prices confirmed in-game 2026-07-10.
         "cost": HERO_CACHE_ACC, "rng_cost": 500, "targeted": True}

# Renown one-time slot pieces (rank-gated, not currency). Only a handful of slots.
RENOWN_PIECES = {
    "waist": {"faction": "Hara'ti", "rank": 8, "track": "Champion", "ilvl": 246},
    "head":  {"faction": "Silvermoon Court", "rank": 9, "track": "Champion", "ilvl": 246},
    "neck":  {"faction": "Amani Tribe", "rank": 9, "track": "Champion", "ilvl": 246,
              "quest": "An Abundance of Wealth"},
}


# --------------------------------------------------------------------------- #
# State accessors                                                              #
# --------------------------------------------------------------------------- #
def _currencies(state: dict | None) -> dict:
    """{name: quantity} from the /ps dump currency mirror (present offline)."""
    return {c["name"]: c.get("quantity")
            for c in (state or {}).get("currencies") or []
            if isinstance(c, dict) and c.get("name")}


def _item_count(state: dict | None, item_id: int) -> int | None:
    """Syndicator item count (sparks/voidshards). None when Syndicator didn't load
    (offline / --no-enrich) — the caller flags it absent rather than reading 0."""
    ic = (state or {}).get("item_counts")
    if not isinstance(ic, dict):
        return None
    return int(ic.get(item_id) or 0)


def _sources(state: dict | None) -> dict:
    return (state or {}).get("_sources") or {}


# --------------------------------------------------------------------------- #
# Per-slot candidate enumeration                                              #
# --------------------------------------------------------------------------- #
def _crest_up_candidate(track: dict | None, ilvl, curs: dict) -> dict | None:
    """crest-up an existing tracked piece toward its track ceiling. Coarse: step
    count + an estimated 'affordable now?'. Returns None for a capped/untracked slot."""
    if not isinstance(track, dict):
        return None
    tname, lvl, cap = track.get("track"), track.get("level"), track.get("cap")
    if tname is None or lvl is None or cap is None or lvl >= cap:
        return None
    ceiling = rewards.CREST_CEILING.get(tname)
    steps = cap - lvl
    crest_name = f"{tname} Dawncrest"
    have = curs.get(crest_name) or 0
    return {
        "source": "crest-up", "track": tname, "from_ilvl": ilvl, "to_ilvl": ceiling,
        "step": f"{lvl}/{cap}", "steps_remaining": steps,
        "crest": crest_name, "crests_on_hand": int(have),
        "affordable_next_step_est": have >= CREST_PER_STEP_EST,
        "affordable_full_cap_est": have >= CREST_PER_STEP_EST * steps,
        "note": f"~{CREST_PER_STEP_EST} crests/step est — KB lacks an exact per-step table; "
                f"trust the step count, not the crest math",
    }


def _craft_candidate(ilvl, curs: dict, sparks: int | None, is_2h: bool) -> dict | None:
    """spark craft (non-tier slots only). Two crest tiers → Hero 272 / Myth 285.
    Affordability from the live crest + spark pool (have / soon / no)."""
    need_sparks = CRAFT["sparks_2h"] if is_2h else CRAFT["sparks"]
    options = []
    for tier in ("Hero", "Myth"):
        spec = CRAFT[tier]
        if isinstance(ilvl, (int, float)) and spec["yields_ilvl"] <= ilvl:
            continue                          # not an upgrade for this slot
        have_crest = curs.get(spec["crest"]) or 0
        crest_ok = have_crest >= spec["crest_qty"]
        spark_known = sparks is not None
        spark_ok = spark_known and sparks >= need_sparks
        if not spark_known:
            afford = "unknown (Syndicator offline — spark count absent)"
        elif crest_ok and spark_ok:
            afford = "have"
        elif spark_ok and have_crest >= spec["crest_qty"] * 0.6:
            afford = "soon"                    # sparks ready, crests within ~60%
        else:
            afford = "no"
        options.append({
            "yields_ilvl": spec["yields_ilvl"], "crest": spec["crest"],
            "crest_needed": spec["crest_qty"], "crests_on_hand": int(have_crest),
            "affordability": afford,
        })
    if not options:
        return None
    return {
        "source": "craft", "sparks_needed": need_sparks,
        "sparks_on_hand": sparks, "is_2h": is_2h, "options": options,
        "note": "non-tier slots only (tier slots can't be crafted — catalyst.md); "
                "recraft to a higher tier later re-uses the sparks",
    }


def _catalyst_candidate(curs: dict) -> dict:
    """tier-slot path: convert a non-tier drop into this tier slot. Charge = Dawnlight
    Manaflux (currency 3378), cap 8."""
    charges = curs.get(CATALYST["charge_currency"])
    charges = int(charges) if isinstance(charges, (int, float)) else None
    return {
        "source": "catalyst", "charge_currency": CATALYST["charge_currency"],
        "charges_available": charges, "cap": CATALYST["cap"],
        "note": "converts a non-tier drop → this tier slot (keeps ilvl/track); "
                "the only way to fill a tier slot's set bonus",
    }


def _maren_candidate(ilvl, curs: dict) -> dict | None:
    """Maren Silverwing sells a targeted Hero 259 into a slot YOU pick, for Field
    Accolades. Only an upgrade below 259."""
    if isinstance(ilvl, (int, float)) and ilvl >= MAREN["yields_ilvl"]:
        return None
    acc = curs.get(MAREN["cost_currency"])
    have = int(acc) if isinstance(acc, (int, float)) else None
    cost = MAREN["cost"]
    afford = None if have is None else (have >= cost)
    shortfall = None if have is None else max(0, cost - have)
    return {
        "source": "maren", "track": MAREN["track"], "to_ilvl": MAREN["yields_ilvl"],
        "targeted": True, "cost_currency": MAREN["cost_currency"], "cost": cost,
        "accolades_on_hand": have, "affordable": afford, "accolades_short": shortfall,
        "note": f"targeted (you pick the slot); {cost} accolades/piece"
                + ("" if not shortfall else f" — short {shortfall} on this char"),
    }


def _renown_candidate(slot: str, ilvl) -> dict | None:
    """A known one-time renown slot piece (rank-gated). Flags whether it's an upgrade."""
    piece = RENOWN_PIECES.get(slot)
    if not piece:
        return None
    upgrade = not (isinstance(ilvl, (int, float)) and ilvl >= piece["ilvl"])
    return {
        "source": "renown", "faction": piece["faction"], "rank": piece["rank"],
        "track": piece["track"], "to_ilvl": piece["ilvl"], "is_upgrade": upgrade,
        "quest": piece.get("quest"),
        "note": f"one-time from {piece['faction']} renown {piece['rank']}"
                + ("" if upgrade else " — NOT an upgrade (slot already ≥ its ilvl)"),
    }


def slot_board(row: dict, state: dict) -> dict:
    """The board for one equipped slot: current state + enumerated candidates."""
    slot = row["slot"]
    ilvl = row.get("ilvl")
    tier = slot in TIER_SLOTS
    track = row.get("track") if isinstance(row.get("track"), dict) else None
    curs = _currencies(state)
    sparks = _item_count(state, SPARK_ITEM)
    # 2H (4 sparks) is only possible on the main hand, and only when NO off-hand is
    # equipped (an equipped off-hand ⇒ dual-wield / 1H+shield ⇒ 2 sparks). Coarse but
    # right for the common cases; flagged on the candidate.
    has_offhand = any(_norm_slot(e.get("slot")) == "offhand"
                      for e in (state.get("equipment") or []) if isinstance(e, dict))
    is_2h = slot == "mainhand" and not has_offhand

    cands = []
    cu = _crest_up_candidate(track, ilvl, curs)
    if cu:
        cands.append(cu)
    if not tier:
        cr = _craft_candidate(ilvl, curs, sparks, is_2h)
        if cr:
            cands.append(cr)
    else:
        cands.append(_catalyst_candidate(curs))
    mn = _maren_candidate(ilvl, curs)
    if mn:
        cands.append(mn)
    rn = _renown_candidate(slot, ilvl)
    if rn:
        cands.append(rn)

    return {
        "slot": slot, "ilvl": ilvl, "tier": tier, "name": row.get("name"),
        "track": ({"track": track["track"], "level": track.get("level"),
                   "cap": track.get("cap")} if track else None),
        "crafted_or_untracked": track is None,
        "candidates": cands,
    }


# --------------------------------------------------------------------------- #
# Warband roll-up: cross-character facts + gate states                         #
# --------------------------------------------------------------------------- #
def discover_characters() -> list[tuple[str, str]]:
    """(name, realm) for every synced character — from the profile URLs in
    knowledge/characters/ front matter, same source /sync-characters uses."""
    try:
        out = subprocess.run(
            ["grep", "-rhoE", r"character/[a-z0-9-]+/[a-z0-9-]+", str(CHAR_DIR)],
            capture_output=True, text=True, check=False).stdout
    except OSError:
        return []
    pairs = set()
    for line in out.splitlines():
        m = re.match(r"character/([a-z0-9-]+)/([a-z0-9-]+)", line.strip())
        if m:
            pairs.add((m.group(2), m.group(1)))   # (name, realm)
    return sorted(pairs)


def _mat_pool(state: dict | None) -> dict:
    """The mat balances a warband pool sums: crests/accolades/marl/manaflux (dump)
    + sparks/voidshards (Syndicator, None when offline)."""
    curs = _currencies(state)
    pool = {name: int(curs.get(name) or 0) for name in POOL_CURRENCIES}
    pool["Spark of Radiance"] = _item_count(state, SPARK_ITEM)
    pool["Ascendant Voidshard"] = _item_count(state, VOIDSHARD_ITEM)
    return pool


def _sub_263_count(state: dict | None) -> int:
    """How many equipped slots are below 263 (the Champion-of-the-Dawn threshold) —
    i.e. steps from earning the 50% warband Champion discount."""
    eq = (state or {}).get("equipment") or []
    return sum(1 for e in eq if isinstance(e, dict)
               and isinstance(e.get("ilvl"), (int, float))
               and e["ilvl"] < DAWN_CHAMPION_ILVL)


def _mplus_unlocked(state: dict | None) -> dict:
    """M+ gate state: unlocked once there are M+ runs; the Cracked Keystone still in
    bags means the one-time unlock quest is pending."""
    runs = (state or {}).get("mythicPlus") or []
    keystone = _item_count(state, CRACKED_KEYSTONE_ITEM)
    return {
        "unlocked": bool(runs),
        "runs_recorded": len(runs),
        "cracked_keystone_in_bags": (keystone is not None and keystone > 0),
        "note": "unlock: run any Mythic +2 (Cracked Keystone quest 92600 credits on "
                "completion — get the +2 from a Mythic 0 first). dawncrests.md",
    }


def warband_board(main_state: dict, main_name: str, realm: str, wow_path: str,
                  enrich: bool) -> dict:
    """Cross-character facts + warband gate states. The main character's state is
    reused; every OTHER synced character is loaded fresh (same enrich setting)."""
    chars = discover_characters()
    per_char = []
    pool: dict = {}

    def _fold(name: str, st: dict | None) -> None:
        mats = _mat_pool(st)
        per_char.append({
            "name": name,
            "equippedIlvl": (st or {}).get("equippedIlvl"),
            "sub_263_slots": _sub_263_count(st),
            "champion_of_the_dawn": ((st or {}).get("dawn_achievements") or {}).get("champion"),
            "mats": mats,
            "loaded": st is not None,
        })
        for k, v in mats.items():
            if isinstance(v, (int, float)):
                pool[k] = pool.get(k, 0) + v      # None (offline sparks) skipped

    _fold(main_name, main_state)
    for name, rlm in chars:
        if name.lower() == (main_name or "").lower():
            continue
        try:
            st = charstate.load(name, rlm, wow_path, enrich=enrich)
        except Exception:  # noqa: BLE001 — one bad alt shouldn't sink the board
            st = None
        _fold(name, st)

    # cheapest character to earn Champion of the Dawn = fewest sub-263 slots that
    # hasn't already earned it.
    unearned = [c for c in per_char if not c["champion_of_the_dawn"] and c["loaded"]]
    cheapest = min(unearned, key=lambda c: c["sub_263_slots"], default=None)

    return {
        "gates": {
            "champion_discount_live": (main_state.get("dawn_achievements") or {}).get("champion", False),
            "mplus": _mplus_unlocked(main_state),
        },
        "characters": per_char,
        "cheapest_to_gate_champion": cheapest["name"] if cheapest else None,
        "pooled_mats": pool,
        "step_library": {
            "path": "knowledge/planning/candidates.json",
            "note": "the 'what activity yields what' reference (yields.currencies / "
                    "yields.slots) the agent maps goals→steps onto (goal-model.md)",
        },
    }


# --------------------------------------------------------------------------- #
# Board assembly                                                               #
# --------------------------------------------------------------------------- #
def build_board(state: dict, realm: str, wow_path: str, enrich: bool) -> dict:
    """The full board: per-slot candidates + the warband roll-up."""
    eq = {_norm_slot(e.get("slot")): e for e in state.get("equipment") or []
          if isinstance(e, dict) and e.get("slot")}
    slots = [slot_board(eq[s], state) for s in SLOT_ORDER if s in eq]
    name = state.get("character") or "character"
    return {
        "character": name,
        "equippedIlvl": state.get("equippedIlvl"),
        "sources": _sources(state),
        "slots": slots,
        "warband": warband_board(state, name, realm, wow_path, enrich),
        "_doc": "Deterministic goal BOARD (facts). Rank/pare/sequence per "
                "knowledge/planning/goal-model.md — that judgment is the agent's, "
                "not this tool's.",
    }


# --------------------------------------------------------------------------- #
# Rendering                                                                    #
# --------------------------------------------------------------------------- #
def _afford_tag(cand: dict) -> str:
    s = cand["source"]
    if s == "crest-up":
        n = "✓" if cand["affordable_next_step_est"] else "·"
        f = "✓" if cand["affordable_full_cap_est"] else "·"
        return f"{cand['steps_remaining']} step(s) → {cand['to_ilvl']} " \
               f"[{cand['crests_on_hand']} {cand['crest'].split()[0]} crests; " \
               f"next-step {n} full-cap {f} (est)]"
    if s == "craft":
        opts = ", ".join(f"{o['yields_ilvl']} via {o['crest'].split()[0]}"
                         f"({o['crests_on_hand']}/{o['crest_needed']}):{o['affordability']}"
                         for o in cand["options"])
        sp = cand["sparks_on_hand"]
        spk = f"{sp} sparks" if sp is not None else "sparks?(offline)"
        return f"{opts}; {cand['sparks_needed']} sparks needed ({spk})"
    if s == "catalyst":
        ch = cand["charges_available"]
        return f"charges {ch if ch is not None else '?'} / {cand['cap']}"
    if s == "maren":
        acc = cand["accolades_on_hand"]
        cost = cand["cost"]
        if acc is None:
            aff = "?"
        elif cand["affordable"]:
            aff = "✓ affordable"
        else:
            aff = f"short {cand['accolades_short']}"
        return f"Hero {cand['to_ilvl']} targeted [{acc if acc is not None else '?'}/{cost} accolades — {aff}]"
    if s == "renown":
        up = "" if cand["is_upgrade"] else " (not an upgrade)"
        return f"{cand['faction']} r{cand['rank']} → {cand['to_ilvl']}{up}"
    return ""


def render(board: dict) -> str:
    L = []
    il = board.get("equippedIlvl")
    head = f" (equipped ilvl {round(il)})" if isinstance(il, (int, float)) and il else ""
    L.append(f"Goal board · {board['character']}{head}")
    srcs = board.get("sources") or {}
    live = [n for n, k in (("dump", "planner_state"), ("API", "blizzard_api"),
                           ("Syndicator", "syndicator")) if srcs.get(k)]
    L.append(f"sources: {', '.join(live) or 'none'}"
             + ("" if srcs.get("syndicator") else "  (⚠ no Syndicator — spark/voidshard counts absent)"))
    L.append("")
    L.append("PER-SLOT CANDIDATES (facts only — rank/pare per goal-model.md):")
    for s in board["slots"]:
        tier = " ·tier" if s["tier"] else ""
        crafted = " ·crafted/untracked" if s["crafted_or_untracked"] else ""
        tr = ""
        if s["track"]:
            tr = f" {s['track']['track']} {s['track']['level']}/{s['track']['cap']}"
        L.append(f"  {s['slot']:<9} {str(s['ilvl']):>4}{tr}{tier}{crafted}")
        for c in s["candidates"]:
            L.append(f"      - {c['source']:<9} {_afford_tag(c)}")
    L.append("")

    wb = board["warband"]
    g = wb["gates"]
    L.append("WARBAND:")
    disc = g["champion_discount_live"]
    L.append(f"  Champion discount (50% warband): {'LIVE' if disc else 'NOT live'} "
             f"— earned when one char hits 263 in every slot")
    mp = g["mplus"]
    L.append(f"  Mythic+: {'unlocked' if mp['unlocked'] else 'LOCKED'}"
             + (f" · Cracked Keystone in bags (unlock pending)" if mp["cracked_keystone_in_bags"] else ""))
    L.append("")
    L.append(f"  Cross-character (cheapest to earn Champion of the Dawn: "
             f"{wb['cheapest_to_gate_champion'] or '—'}):")
    for c in wb["characters"]:
        cod = c["champion_of_the_dawn"]
        cod_s = "✓CotD" if cod else ("—" if cod is False else "?")
        eil = c["equippedIlvl"]
        eil_s = f"{round(eil)}" if isinstance(eil, (int, float)) and eil else "?"
        L.append(f"    {c['name']:<12} ilvl {eil_s:>4} · sub-263 slots {c['sub_263_slots']:>2} · {cod_s}")
    L.append("")
    L.append("  Pooled mats (warband):")
    pool = wb["pooled_mats"]
    for name in POOL_CURRENCIES + ["Spark of Radiance", "Ascendant Voidshard"]:
        if name in pool:
            L.append(f"    {name:<22} {pool[name]:,}")
    L.append("")
    L.append(f"  Step library: {wb['step_library']['path']} "
             "(map goals→steps here; see goal-model.md)")
    return "\n".join(L)


def render_json(board: dict) -> str:
    return json.dumps(board, indent=2, ensure_ascii=False, default=str)
