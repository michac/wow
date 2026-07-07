"""Offline verification for per-slot reward vectors (needs-first Phase 2a).

Stdlib-only:  python3 tools/tests/check_slot_vector.py   (exits non-zero on failure)
Proves the `yields.slots` path of slot_target_R values a gear DROP against the
slots it can actually fill at its LANDING ilvl (Hero 1/6 = 259), so a Hero drop
is R=0 for a geared main (Encomplete's fillable slots are all ≥259) but a big
upgrade for a fresh 90 — while ritual-sites (a currency source) stays high. Also
proves the slot RESTRICTION (an explicit slot list, not just [all]) and that the
scalar `reward_ilvl_max` fallback path is unchanged for un-migrated activities.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from wowkb import rewards as rw  # noqa: E402
from wowkb.plan import load_state, score, slot_target_R  # noqa: E402

FIX = pathlib.Path(__file__).parent / "fixtures"
CAND = ROOT / "knowledge" / "planning" / "candidates.json"
_total = 0
_fails = []


def check(cond, msg):
    global _total
    _total += 1
    print(("PASS" if cond else "FAIL"), msg)
    if not cond:
        _fails.append(msg)


fresh = load_state(str(FIX / "equipment-fresh.lua"), None)
enc = load_state(str(FIX / "equipment-encomplete.lua"), None)

# A migrated Hero-drop activity: LANDS at 259 (1/6), can fill any equipped slot.
hero_drop = {"reward_base": 3, "enjoyment_key": "world",
             "yields": {"slots": [{"track": "hero", "ilvl": 259, "chance": 1.0,
                                    "slots": ["all"]}]}}

# Headline: a Hero-259 [all] drop is a sidegrade for a geared main (every fillable
# slot ≥ 259) but a big upgrade for a fresh 90.
enc_R = slot_target_R(hero_drop, enc)
fresh_R = slot_target_R(hero_drop, fresh)
check(enc_R == (0.0, enc_R[1]) and enc_R[0] == 0.0,
      f"geared main: Hero-259 drop lands ≤ every fillable slot -> R=0 ({enc_R})")
check("no slot upgrade" in enc_R[1], f"geared-main note explains the sidegrade ({enc_R[1]!r})")
check(fresh_R is not None and fresh_R[0] >= 4.0,
      f"fresh 90: same Hero-259 drop is a big upgrade -> high R ({fresh_R})")

# --- slot RESTRICTION: same landing ilvl, different fillable slot ------------
# ilvl 272 into WAIST (Encomplete 259) is an upgrade; the SAME 272 into BACK
# (285) is not — proves the value is per-slot, not just ilvl-vs-weakest.
waist_272 = {"yields": {"slots": [{"ilvl": 272, "slots": ["waist"]}]}}
back_272 = {"yields": {"slots": [{"ilvl": 272, "slots": ["back"]}]}}
wR, bR = slot_target_R(waist_272, enc), slot_target_R(back_272, enc)
check(wR[0] > 0.0, f"272 into waist (259) is an upgrade -> R>0 ({wR})")
check(bR == (0.0, bR[1]) and bR[0] == 0.0,
      f"same 272 into back (285) is a sidegrade -> R=0 (slot restriction works) ({bR})")

# best_slot_delta directly: only the fillable slot counts.
ilvls = {s["slot"]: s["ilvl"] for s in enc["equipment"]}
d_all = rw.best_slot_delta([{"ilvl": 259, "slots": ["all"]}], ilvls)
check(d_all == (0.0, None, None), f"best_slot_delta 259/[all] vs geared -> no upgrade ({d_all})")
d_waist = rw.best_slot_delta([{"ilvl": 272, "slots": ["waist"]}], ilvls)
check(d_waist[0] == 13.0 and d_waist[1] == "waist",
      f"best_slot_delta targets waist: +13 over 259 ({d_waist})")

# --- fallback: reward_ilvl_max path unchanged for un-migrated activities -----
# No yields.slots -> the scalar ceiling vs weakest-slot path (raid keeps this).
scalar = {"reward_ilvl_max": 285}
sc = slot_target_R(scalar, enc)               # weakest slot 259, delta 26 -> R capped 5
check(sc is not None and abs(sc[0] - min(5.0, 1.0 + 26 / 6.0)) < 1e-9
      and "weakest slot" in sc[1],
      f"scalar reward_ilvl_max path unchanged (+26 over weakest 259) ({sc})")
check(slot_target_R({"reward_base": 3}, enc) is None,
      "no yields.slots and no reward_ilvl_max -> None (keep reward_base)")
# yields.slots present but a pre-schema-4 dump (no equipment) -> None.
check(slot_target_R(hero_drop, {"character": "X"}) is None,
      "yields.slots but no equipment block -> None (keep reward_base)")

# --- end-to-end on the real candidate catalog + Encomplete's real spread ----
cands = {c["id"]: c for c in json.loads(CAND.read_text())["candidates"]}
DROP_IDS = ("world-boss", "delve-bountiful", "prey-weekly", "voidcores",
            "val-naigtal", "showdown-weekly", "turbulent-timeways")
for cid in DROP_IDS:
    r = slot_target_R(cands[cid], enc)
    check(r is not None and r[0] == 0.0,
          f"{cid}: slot term falls to R=0 for geared Encomplete ({r})")
# faction gear (Champion 246) is a sidegrade too.
check(slot_target_R(cands["faction-weeklies"], enc)[0] == 0.0,
      "faction-weeklies: Champion 246 landing -> R=0 for a Hero-geared main")
# ...but the same drops are real upgrades for a fresh 90 (character-relative).
check(all(slot_target_R(cands[cid], fresh)[0] > 0.0 for cid in DROP_IDS),
      "same drops score > 0 for a fresh 90 (value is character-relative)")

# ritual-sites (a Myth/Hero crest source, no yields.slots) stays high via the
# currency term while every gear-drop slot term is 0 — the Phase-2a flip.
rs = cands["ritual-sites"]
rs_score, _, _ = score(rs, "efficiency", enc)
drop_scores = [score(cands[cid], "efficiency", enc)[0] for cid in DROP_IDS
               if "currencies" not in (cands[cid].get("yields") or {})]
check(all(rs_score > s for s in drop_scores),
      f"ritual-sites outscores every pure gear-drop for Encomplete "
      f"(ritual {rs_score:.1f} vs {[round(s, 1) for s in drop_scores]})")

print(f"\n{_total} checks, {len(_fails)} failures")
sys.exit(1 if _fails else 0)
