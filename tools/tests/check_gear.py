"""Offline verification for wowkb.plan gearing view (gear_rows / render_gear).

Stdlib-only:  python3 tools/tests/check_gear.py   (exits non-zero on failure)
Exercises ilvl→band classification, slot normalization across naming conventions
(FRESH fixture uses UPPERCASE 'FINGER_1'), tier-slot recognition, and the
Champion-cap floor math (one quest-slot comes free).
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # tools/
from wowkb.plan import SLOT_ORDER, _band, gear_rows, load_state, render_gear  # noqa: E402

FIX = pathlib.Path(__file__).parent / "fixtures"
_total = 0
_fails = []


def check(cond, msg):
    global _total
    _total += 1
    if not cond:
        _fails.append(msg)


# Band boundaries (great-vault.md / dawncrests.md floors).
check(_band(145) == "adventurer", "145 → adventurer")
check(_band(240) == "veteran", "240 → veteran")
check(_band(246) == "champion", "246 → champion")
check(_band(259) == "hero", "259 → hero")
check(_band(285) == "myth", "285 → myth")
check(_band(None) == "?", "None → ?")

# The fresh fixture: all slots 200–220 (sub-Champion), UPPERCASE slot names.
state = load_state(str(FIX / "equipment-fresh.lua"), None)
rows = gear_rows(state)
check(len(rows) == 12, f"all 12 equipped slots surfaced despite UPPERCASE names (got {len(rows)})")
check({r["slot"] for r in rows} <= set(SLOT_ORDER),
      "normalized slot names map onto SLOT_ORDER")
check(all(r["band"] in ("adventurer", "veteran") for r in rows),
      "every fresh-fixture slot classifies sub-Champion")
head = next(r for r in rows if r["slot"] == "head")
check(head["tier"] is True, "head flagged as a tier slot")
check("Champion cache" in head["reco"] and "catalyst" in head["reco"],
      "tier sub-Champion slot → Champion-cache stopgap + catalyst note")

out = render_gear(state)
check("BAND 1 — sub-Champion" in out, "renders the sub-Champion band")
# 12 sub-Champion slots, back(cloak) is a quest-slot → floor = 11 × 100 = 1100.
check("floor ≈ 1100" in out, f"Champion-cap floor accounts for the free quest-slot\n{out}")
check("comes free" in out, "notes the free Decimus quest-slot")

# No equipment → a helpful message, not a crash.
check("No equipment" in render_gear({"character": "X"}), "empty state → guidance, no crash")

if _fails:
    print(f"FAIL ({len(_fails)}/{_total})")
    for m in _fails:
        print(f"  - {m}")
    sys.exit(1)
print(f"OK ({_total} checks)")
