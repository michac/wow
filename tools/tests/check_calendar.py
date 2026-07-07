"""Offline verification for the event_active gate (fun radar / calendar consumer).

Stdlib-only:  python3 tools/tests/check_calendar.py   (exits non-zero on failure)
Covers the gate logic and the end-to-end plan(): a candidate whose calendar event
is live surfaces (todo); one that isn't live drops; and a pre-calendar (schema<2)
dump leaves it unknown -> shows '(?)'.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # tools/
from wowkb.plan import gate_status, load_state, plan  # noqa: E402

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


def ev(match):
    return {"gate": {"type": "event_active", "match": match}}


def cal(*events):
    return {"calendar": list(events)}


# --- unit: gate_status ---------------------------------------------------------
check(gate_status(ev("Timewalking"), cal(
    {"title": "Timewalking Dungeon Event", "active": True})) == "todo",
    "live match -> todo")
check(gate_status(ev("Timewalking"), cal(
    {"title": "Timewalking Dungeon Event", "active": False})) == "done",
    "match present but not live -> done (dropped)")
check(gate_status(ev("Timewalking"), cal(
    {"title": "Darkmoon Faire", "active": True})) == "done",
    "no matching title -> done (dropped)")
check(gate_status(ev("timeways"), cal(
    {"title": "Turbulent Timeways", "active": True})) == "todo",
    "case-insensitive substring -> todo")
check(gate_status(ev("Timewalking"), {"vault": {}}) == "unknown",
    "schema<2 dump (no calendar block) -> unknown")
check(gate_status(ev("Timewalking"), None) == "unknown",
    "no dump -> unknown")

# --- end-to-end: plan() surfaces a live event ----------------------------------
live = plan(120, load_state(str(FIX / "calendar-live.lua"), None), "efficiency")
tw = row(live, "turbulent-timeways")
check(tw is not None, "turbulent-timeways present when its event is live")
check(tw and tw["state"] == "todo",
      f"turbulent-timeways gated todo when live (got {tw and tw['state']!r})")

# a pre-calendar (schema-1) dump has no calendar block -> unknown, shows (?)
noc = plan(120, load_state(str(FIX / "weeklies-live.lua"), None), "efficiency")
twn = row(noc, "turbulent-timeways")
check(twn is not None and twn["state"] == "unknown",
      "turbulent-timeways -> unknown on a pre-calendar (schema-1) dump")

print(f"\n{_total} checks, {len(_fails)} failures")
sys.exit(1 if _fails else 0)
