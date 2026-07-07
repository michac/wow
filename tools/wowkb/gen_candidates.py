"""Generate the planner's candidates.json from the activities/*.md catalog.

Closes the loop that used to be hand-kept: instead of editing candidates.json by
hand (the 14-item file that drifted from the 25-file `activities/` catalog), this
reads each activity file's YAML front matter and derives the planner's scoring
inputs via the priors in `activities/_facets.md`:

  reward_base  <- goal (+ reward.type):  gearing/rating high, story/leveling mid,
                  professions conditional, collectibles 0 (runtime U-floor lifts it)
  urgency      <- time + cadence  (the _facets U table)
  enjoyment    <- venue           (an explicit md `enjoyment:` number passes through)
  gate / breakpoint / reward_ilvl_max  pass through verbatim

Slot-target and breakpoint boosts stay at RUNTIME (plan.py), not baked here — the
baseline is character-agnostic on purpose. An activity may override any prior by
setting `reward_base:`, `urgency:`, or `enjoyment:` explicitly in its front matter.

    uv run python -m wowkb.gen_candidates            # write candidates.json
    uv run python -m wowkb.gen_candidates --check     # exit 1 if out of date
    uv run python -m wowkb.gen_candidates --print     # stdout, don't write

Re-run after editing any activities/*.md, then commit the regenerated JSON.
`--include-repeatables` in plan.py is unaffected (it still merges repeatables.json).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
ACTIVITIES = REPO / "knowledge" / "planning" / "activities"
OUT_JSON = REPO / "knowledge" / "planning" / "candidates.json"

# activities/ files that are docs, not activities (no `id` front matter).
SKIP = {"README.md", "_facets.md"}

# venue -> plan.py E_TABLE key (see activities/_facets.md "(venue, group)" table).
# An explicit md `enjoyment:` number wins over this (passed straight through).
VENUE_E_KEY = {
    "delve": "delve", "world": "world", "dungeon": "mplus", "raid": "raid",
    "pvp": "pvp", "profession": "crafting", "housing": "housing",
    "meta": "chore", "quest": "chore",
}


def load_front_matter(path: Path) -> dict | None:
    """Parse the YAML front matter of a `--- ... ---` markdown file, else None."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    fm = yaml.safe_load(parts[1])
    return fm if isinstance(fm, dict) else None


def _as_set(v) -> set[str]:
    if isinstance(v, str):
        return {v}
    if isinstance(v, (list, tuple)):
        return set(v)
    return set()


def reward_base(fm: dict) -> int:
    """Character-agnostic baseline R from goal (+ reward.type). Priors: _facets.md."""
    if isinstance(fm.get("reward_base"), (int, float)):
        return int(fm["reward_base"])        # explicit override wins
    goals = _as_set(fm.get("goal"))
    rtypes = _as_set((fm.get("reward") or {}).get("type"))
    if goals & {"gearing", "rating"}:
        return 3                             # real power / score toward a breakpoint
    if "professions" in goals and "power" in rtypes:
        return 2                             # profession work that also yields gear
    if goals & {"story", "leveling"}:
        return 2                             # one-time power/XP
    if "professions" in goals:
        return 2                             # means-to-an-end, still real
    return 0                                 # collectibles-only (U-floor may lift to 1)


def urgency(fm: dict):
    """U from time + cadence (the _facets.md U table). Explicit `urgency:` wins."""
    if isinstance(fm.get("urgency"), (int, float)):
        return fm["urgency"]
    time = fm.get("time")
    cadence = fm.get("cadence")
    if time == "time-boxed":
        return 3 if cadence == "one-time" else 1.5   # annual/one-time vs recurring event
    if cadence in ("weekly", "monthly"):
        return 2                             # expires this reset
    return 1                                 # standing / repeatable / always available


def enjoyment_fields(fm: dict) -> dict:
    """Either {'enjoyment': <n>} (explicit override) or {'enjoyment_key': <venue key>}."""
    if isinstance(fm.get("enjoyment"), (int, float)):
        return {"enjoyment": fm["enjoyment"]}
    venue = fm.get("venue")
    if isinstance(venue, (list, tuple)):
        venue = venue[0] if venue else None
    return {"enjoyment_key": VENUE_E_KEY.get(venue, "chore")}


def build_candidate(fm: dict) -> dict:
    """A candidates.json entry from one activity's front matter (stable key order)."""
    c: dict = {"id": fm["id"], "name": fm.get("name", fm["id"])}
    c["why"] = (fm.get("reward") or {}).get("detail", "")
    c["reward_base"] = reward_base(fm)
    c["urgency"] = urgency(fm)
    c["time_blocks"] = fm.get("time_blocks", 1)
    c.update(enjoyment_fields(fm))
    c["gate"] = fm.get("gate", {"type": "manual"})
    if fm.get("breakpoint"):
        c["breakpoint"] = fm["breakpoint"]
    if isinstance(fm.get("reward_ilvl_max"), (int, float)):
        c["reward_ilvl_max"] = fm["reward_ilvl_max"]
    return c


def build_candidates() -> list[dict]:
    cands = []
    for path in sorted(ACTIVITIES.glob("*.md")):
        if path.name in SKIP:
            continue
        fm = load_front_matter(path)
        if not fm or "id" not in fm:
            continue
        if fm.get("status") == "invalidated":
            continue
        cands.append(build_candidate(fm))
    cands.sort(key=lambda c: c["id"])
    return cands


_NOTE = (
    "AUTO-GENERATED from knowledge/planning/activities/*.md — do NOT hand-edit. "
    "Writer: `uv run python -m wowkb.gen_candidates`. Scoring inputs are derived "
    "from each activity's front matter via the priors in activities/_facets.md: "
    "reward_base from goal+reward.type, urgency from time+cadence, enjoyment_key "
    "from venue (an explicit `enjoyment:` number passes through). Slot-target "
    "(reward_ilvl_max) and breakpoint boosts are applied at RUNTIME by plan.py, "
    "not baked here. Edit the .md files then re-run this; keep --include-repeatables."
)


def render(cands: list[dict]) -> str:
    lines = ["{", f'  "_note": {json.dumps(_NOTE, ensure_ascii=False)},',
             '  "candidates": [']
    for i, c in enumerate(cands):
        comma = "," if i < len(cands) - 1 else ""
        lines.append("    " + json.dumps(c, ensure_ascii=False) + comma)
    lines += ["  ]", "}", ""]
    return "\n".join(lines)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="wowkb.gen_candidates", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--check", action="store_true",
                   help="exit 1 if candidates.json is out of date (CI guard)")
    p.add_argument("--print", dest="to_stdout", action="store_true",
                   help="write to stdout instead of the file")
    args = p.parse_args(argv)

    content = render(build_candidates())
    n = content.count('"id":')

    if args.to_stdout:
        sys.stdout.write(content)
        return 0
    if args.check:
        current = OUT_JSON.read_text() if OUT_JSON.exists() else ""
        if current != content:
            print(f"OUT OF DATE: {OUT_JSON} — re-run `python -m wowkb.gen_candidates`")
            return 1
        print(f"up to date ({n} candidates)")
        return 0

    OUT_JSON.write_text(content)
    print(f"wrote {OUT_JSON.relative_to(REPO)} — {n} candidates from activities/*.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
