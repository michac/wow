"""Offline verification for the weekly_quest gate (Step 1 wiring).

Stdlib-only:  python3 tools/tests/check_gates.py   (exits non-zero on failure)
Exercises the "done if ANY mapped quest is complete" rule that supports rotating
weeklies (one slug, several zone IDs) — e.g. void_assault = 94385/94386.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # tools/
from wowkb.plan import gate_status, load_state  # noqa: E402

FIX = pathlib.Path(__file__).parent / "fixtures"
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


# --- world_boss_weekly gate (schema-3 worldBosses[] block) --------------------
def wb_cand():
    return {"gate": {"type": "world_boss_weekly"}}


# a boss present in the dump = killed this reset = weekly lockout done
check(gate_status(wb_cand(), {"worldBosses": [{"name": "Imperator Pertinax", "id": 1}]})
      == "done", "world_boss_weekly, a boss saved -> done")
# empty block = nothing killed yet this reset
check(gate_status(wb_cand(), {"worldBosses": []}) == "todo",
      "world_boss_weekly, none saved -> todo")
# a schema-2 dump has no worldBosses key at all -> unknown (mirror event_active)
check(gate_status(wb_cand(), {"vault": {}}) == "unknown",
      "world_boss_weekly, pre-schema-3 dump (no key) -> unknown")
# end-to-end: the Lua fixture parses (plan.py _LuaParser) + gates done
wb_state = load_state(str(FIX / "worldbosses-live.lua"), None)
check(isinstance(wb_state, dict) and wb_state.get("schema") == 3,
      "worldbosses-live.lua parses as a schema-3 dump")
check(gate_status(wb_cand(), wb_state) == "done",
      "world_boss_weekly, fixture (Imperator Pertinax saved) -> done")

print(f"\n{_total} checks, {len(_fails)} failures")
sys.exit(1 if _fails else 0)
