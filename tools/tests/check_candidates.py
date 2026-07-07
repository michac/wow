"""Smoke test for the generated candidates.json (Phase 1.2).

Stdlib-only:  python3 tools/tests/check_candidates.py   (exits non-zero on failure)
Asserts every activities/*.md file yields a candidate with the required scoring
keys, that the generated file is in sync with the catalog, and that plan.py can
score the whole set without error. Does NOT import PyYAML — it reads the committed
JSON (stdlib) and lists the md ids by hand so the test stays dependency-free.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from wowkb.plan import plan, score  # noqa: E402

ACT = ROOT / "knowledge" / "planning" / "activities"
CAND = ROOT / "knowledge" / "planning" / "candidates.json"
SKIP = {"README.md", "_facets.md"}
_total = 0
_fails = []


def check(cond, msg):
    global _total
    _total += 1
    print(("PASS" if cond else "FAIL"), msg)
    if not cond:
        _fails.append(msg)


def md_id(path):
    """Pull `id: <slug>` out of the front-matter block without a YAML dep."""
    for line in path.read_text(encoding="utf-8").splitlines()[:30]:
        m = re.match(r"id:\s*(\S+)", line)
        if m:
            return m.group(1)
    return None


cands = json.loads(CAND.read_text())["candidates"]
by_id = {c["id"]: c for c in cands}

md_ids = {md_id(p) for p in sorted(ACT.glob("*.md")) if p.name not in SKIP}
md_ids.discard(None)

# every activity file is represented
missing = md_ids - set(by_id)
check(not missing, f"every activity/*.md yields a candidate (missing: {sorted(missing)})")

# the previously-missing activities are now present (analysis §7)
for want in ("omnium-folio", "profession-weekly", "darkmoon-faire",
             "val-naigtal", "showdown-weekly"):
    check(want in by_id, f"{want} present in candidates.json")

# required scoring keys on every candidate + a scorable enjoyment source
REQUIRED = ("id", "name", "why", "reward_base", "urgency", "time_blocks", "gate")
for c in cands:
    miss = [k for k in REQUIRED if k not in c]
    check(not miss, f"{c.get('id','?')} has required keys (missing {miss})")
    check("enjoyment" in c or "enjoyment_key" in c,
          f"{c.get('id','?')} carries an enjoyment source")

# the whole set scores without raising, stateless
try:
    for c in cands:
        score(c, "efficiency", None)
    ok = True
except Exception as e:  # noqa: BLE001
    ok = False
    print("  scoring raised:", e)
check(ok, "every candidate scores without error (stateless)")

# plan() runs end-to-end over the generated file
res = plan(120, None, "efficiency")
check(len(res["all"]) == len(cands), "plan() ranks the full generated catalog")

print(f"\n{_total} checks, {len(_fails)} failures")
sys.exit(1 if _fails else 0)
