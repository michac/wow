"""Offline verification for slot-aware / ilvl-relative reward (Phase 1.1).

Stdlib-only:  python3 tools/tests/check_slot_target.py   (exits non-zero on failure)
Proves slot_target_R zeroes a Hero-ceiling activity for a Hero-capped char and
boosts it for a fresh char, and that score() composes it as max(breakpoint, slot).
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # tools/
from wowkb.plan import load_state, score, slot_target_R  # noqa: E402

FIX = pathlib.Path(__file__).parent / "fixtures"
_total = 0
_fails = []


def check(cond, msg):
    global _total
    _total += 1
    print(("PASS" if cond else "FAIL"), msg)
    if not cond:
        _fails.append(msg)


fresh = load_state(str(FIX / "equipment-fresh.lua"), None)
geared = load_state(str(FIX / "equipment-geared.lua"), None)

# a Hero-ceiling gear activity (world vault / voidcore / prey map)
hero = {"reward_base": 3, "reward_ilvl_max": 279, "enjoyment_key": "world"}

check(slot_target_R(hero, fresh) is not None and slot_target_R(hero, fresh)[0] >= 4.0,
      f"fresh char: Hero ceiling is a big upgrade -> high R ({slot_target_R(hero, fresh)})")
check(slot_target_R(hero, geared) == (0.0, slot_target_R(hero, geared)[1]) and
      slot_target_R(hero, geared)[0] == 0.0,
      f"geared char: Hero ceiling ≤ every slot -> R=0 ({slot_target_R(hero, geared)})")

# no ceiling on the candidate -> None (falls back to reward_base)
check(slot_target_R({"reward_base": 3}, fresh) is None,
      "no reward_ilvl_max -> None (fall back to reward_base)")
# pre-schema-4 dump (no equipment) -> None
check(slot_target_R(hero, {"character": "X"}) is None,
      "no equipment block -> None")

# end-to-end score(): the SAME activity scores higher for the fresh char
s_fresh, _, note_f = score(hero, "efficiency", fresh)
s_geared, _, _ = score(hero, "efficiency", geared)
check(s_fresh > s_geared, f"fresh outscores geared on same activity ({s_fresh:.1f} > {s_geared:.1f})")
check("weakest slot" in note_f, f"fresh score carries a slot-target note ({note_f!r})")

# compose: breakpoint (mid-track base) and slot-target -> max wins. A geared char
# with a capped-gear activity that still fills a vault column keeps the vault value.
both = {"reward_base": 3, "reward_ilvl_max": 279,
        "breakpoint": {"type": "vault", "track": "world", "thresholds": [1, 4, 8]}}
# world vault progress 2/... (crossing to 3 is NOT a threshold) -> breakpoint base 3;
# slot-target for geared = 0; max -> 3 (vault value survives being gear-capped).
vault_state = dict(geared)
vault_state["vault"] = {"slots": [{"type": "world", "progress": 2, "threshold": 1},
                                  {"type": "world", "progress": 2, "threshold": 4},
                                  {"type": "world", "progress": 2, "threshold": 8}]}
s_both, _, _ = score(both, "efficiency", vault_state)
s_gearonly, _, _ = score(hero, "efficiency", vault_state)
check(s_both > s_gearonly,
      f"max(breakpoint,slot): vault-filling activity beats gear-only when both capped "
      f"({s_both:.1f} > {s_gearonly:.1f})")

print(f"\n{_total} checks, {len(_fails)} failures")
sys.exit(1 if _fails else 0)
