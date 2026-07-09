"""Offline verification for wowkb.plan.discover_weeklies (active-quest-log dump).

Stdlib-only:  python3 tools/tests/check_discover.py   (exits non-zero on failure)
Exercises the "weekly in the /ps active-log but not in the watchlist -> discover;
watch-listed / daily / one-time -> skip" rule, plus dedup persistence (a second
run over the same state finds nothing new). Writes to a scratch file, never the
real knowledge/planning/discovered-weeklies.json.
"""
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # tools/
import wowkb.plan as P  # noqa: E402
from wowkb.plan import load_state  # noqa: E402

FIX = pathlib.Path(__file__).parent / "fixtures"
_total = 0
_fails = []


def check(cond, msg):
    global _total
    _total += 1
    if not cond:
        _fails.append(msg)


# Redirect the master-list path to a throwaway file so the test is hermetic.
tmp = pathlib.Path(tempfile.mkdtemp()) / "discovered-weeklies.json"
P.DISCOVERED = tmp

state = load_state(str(FIX / "activequests.lua"), None)
check(state is not None, "fixture parsed")
check(any(q.get("id") == 99001 for q in state.get("activeQuests", [])),
      "activeQuests[] survived the Lua parse")

fresh = P.discover_weeklies(state)
ids = {e["questID"] for e in fresh}
# 99001 (freq 2, Weekly) and 99004 (freq 3, ResetByScheduler) both count as weekly.
check(ids == {99001, 99004}, f"unknown weeklies at freq 2 AND 3 discovered (got {ids})")
k = next(e for e in fresh if e["questID"] == 99001)
check(k["title"] == "Knocking Off the Top" and k.get("campaign") == 1,
      "carried the title + campaign flag")
check(k.get("important") is True, "carried the Blizzard 'important' (purple-!) flag")
check(next(e for e in fresh if e["questID"] == 99004).get("important") is False,
      "non-important weekly flagged important=False")

# 96713 is weekly but watch-listed; 99002 daily; 99003 one-time -> none of these.
check(96713 not in ids, "watch-listed weekly is not re-discovered")
check(99002 not in ids and 99003 not in ids, "daily / one-time quests are ignored")

# Idempotent: a second pass over the same state persists nothing new.
check(P.discover_weeklies(state) == [], "second run finds nothing new (deduped)")
check(tmp.exists(), "master list written to disk")

if _fails:
    print(f"FAIL ({len(_fails)}/{_total})")
    for m in _fails:
        print(f"  - {m}")
    sys.exit(1)
print(f"OK ({_total} checks)")
