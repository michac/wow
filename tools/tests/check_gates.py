"""Offline verification for the weekly_quest gate (Step 1 wiring).

Stdlib-only:  python3 tools/tests/check_gates.py   (exits non-zero on failure)
Exercises the "done if ANY mapped quest is complete" rule that supports rotating
weeklies (one slug, several zone IDs) — e.g. void_assault = 94385/94386.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # tools/
from wowkb.plan import gate_status  # noqa: E402

_total = 0
_fails = []


def check(cond, msg):
    global _total
    _total += 1
    print(("PASS" if cond else "FAIL"), msg)
    if not cond:
        _fails.append(msg)


def cand(quest):
    return {"gate": {"type": "weekly_quest", "quest": quest}}


def wq(*entries):
    return {"weeklyQuests": list(entries)}


# rotating void assault: active zone done, inactive zone not -> DONE
check(gate_status(cand("void_assault"), wq(
    {"id": 94385, "label": "void_assault", "complete": True},
    {"id": 94386, "label": "void_assault", "complete": False},
)) == "done", "rotating void_assault, one of pair complete -> done")

# neither zone done -> TODO
check(gate_status(cand("void_assault"), wq(
    {"id": 94385, "label": "void_assault", "complete": False},
    {"id": 94386, "label": "void_assault", "complete": False},
)) == "todo", "void_assault, both incomplete -> todo")

# prey single quest
check(gate_status(cand("prey_weekly"), wq(
    {"id": 94446, "label": "prey_weekly", "complete": True})) == "done",
    "prey_weekly complete -> done")
check(gate_status(cand("prey_weekly"), wq(
    {"id": 94446, "label": "prey_weekly", "complete": False})) == "todo",
    "prey_weekly incomplete -> todo")

# a slug with no mapped quest in the dump stays unknown (correct: still shows '(?)')
check(gate_status(cand("housing_weekly"), wq(
    {"id": 94446, "label": "prey_weekly", "complete": True})) == "unknown",
    "unconfigured slug -> unknown")

# match by numeric id even if the addon label differs from the slug
check(gate_status(cand("94446"), wq(
    {"id": 94446, "label": "anything", "complete": True})) == "done",
    "numeric-id match -> done")

print(f"\n{_total} checks, {len(_fails)} failures")
sys.exit(1 if _fails else 0)
