"""Offline verification for breakpoint-proximity scoring (Step 2).

Stdlib-only, no uv needed:  python3 tools/tests/check_breakpoint.py
Exits non-zero if any check fails.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # tools/
from wowkb.plan import breakpoint_R, load_state, plan  # noqa: E402

FIX = pathlib.Path(__file__).parent / "fixtures"
_total = 0
_fails = []


def check(cond, msg):
    global _total
    _total += 1
    print(("PASS" if cond else "FAIL"), msg)
    if not cond:
        _fails.append(msg)


def row(res, cid):
    return next((r for r in res["all"] if r["c"]["id"] == cid), None)


# --- end-to-end across fixtures ------------------------------------------------
below = plan(120, load_state(str(FIX / "vault-below.lua"), None), "efficiency")
cross = plan(120, load_state(str(FIX / "vault-crossing.lua"), None), "efficiency")
capped = plan(120, load_state(str(FIX / "vault-capped.lua"), None), "efficiency")

b, c = row(below, "mplus"), row(cross, "mplus")
check(b is not None and c is not None, "mplus-vault present in below + crossing")
check(c["score"] > b["score"], f"crossing outranks below ({c['score']:.1f} > {b['score']:.1f})")
check("unlocks vault slot 2" in c["note"], f"crossing note names slot 2: {c['note']!r}")
check(b["note"] == "", f"below carries no breakpoint note: {b['note']!r}")
check(row(capped, "mplus") is None, "capped drops mplus-vault (gated done)")

# --- backward-compat: a no-breakpoint candidate is unaffected by state ---------
rit_state = row(below, "ritual-sites")["score"]
rit_none = row(plan(120, None, "efficiency"), "ritual-sites")["score"]
check(abs(rit_state - rit_none) < 1e-9, "ritual-sites (no breakpoint) identical with/without state")

# --- unit: breakpoint_R across the range ---------------------------------------
cand = {"reward_base": 3, "breakpoint": {"type": "vault", "track": "mplus", "thresholds": [1, 4, 8]}}
mk = lambda n: {"mythicPlus": [{"thisWeek": True} for _ in range(n)]}  # noqa: E731
check(breakpoint_R(cand, None) is None, "breakpoint_R -> None when stateless")
check(breakpoint_R(cand, mk(2))[0] == 3.0, "n=2 -> base R (mid-track)")
check(breakpoint_R(cand, mk(3))[0] == 4.0, "n=3 -> R=4 (crossing)")
check(breakpoint_R(cand, mk(8))[0] == 0.0, "n=8 -> R=0 (capped)")

print(f"\n{_total} checks, {len(_fails)} failures")
sys.exit(1 if _fails else 0)
