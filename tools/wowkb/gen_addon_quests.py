"""Generate the PlannerState addon's quest-ID table from the scraper catalog.

Closes the loop that used to be hand-wired: instead of typing weekly quest IDs
into the addon's `ns.WEEKLY_QUESTS` one at a time (the "2 of 7 wired" problem),
this reads the questIDs the repeatables scraper already discovered
(knowledge/planning/repeatables.json), keeps only the HIGH-confidence ones —
per the addon doctrine "a wrong ID false-reports done, which is worse than a
gap" — and writes them to PlannerState_Quests.lua as `ns.GENERATED_QUESTS`,
which the addon merges under (never over) the hand-verified slug map.

    uv run python -m wowkb.gen_addon_quests            # write the addon file
    uv run python -m wowkb.gen_addon_quests --check     # exit 1 if out of date
    uv run python -m wowkb.gen_addon_quests --print     # stdout, don't write

Re-run after `wowkb.repeatables` refreshes the catalog, then cut an addon
release (see planner-state/CLAUDE.md) so ghaddons ships it.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
REPEATABLES = REPO / "knowledge" / "planning" / "repeatables.json"
OUT_LUA = REPO / "planner-state" / "PlannerState" / "PlannerState_Quests.lua"

# Already carried by the addon's hand-verified ns.WEEKLY_QUESTS (slug-labelled).
# Skip them here so the generated numeric labels never shadow a curated slug.
HAND_WIRED = {94446, 94385, 94386}


def _lua_str(s: str) -> str:
    """Quote a Lua string literal (double-quoted; escape \\ and ")."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def build_entries(data: dict) -> list[tuple[int, str, str]]:
    """(questID, name, cadence) for high-confidence, non-hand-wired quests."""
    out = []
    seen = set()
    for q in data.get("questIDs_to_wire", []):
        qid = q.get("questID")
        if (q.get("questID_confidence") != "high" or qid in HAND_WIRED
                or qid in seen or not isinstance(qid, int)):
            continue
        seen.add(qid)
        out.append((qid, q.get("name", "?"), q.get("cadence", "?")))
    out.sort(key=lambda e: e[0])
    return out


def render(data: dict) -> str:
    entries = build_entries(data)
    generated = data.get("generated", "?")
    lines = [
        "-- AUTO-GENERATED — do NOT hand-edit.",
        "-- Source: knowledge/planning/repeatables.json (generated %s)" % generated,
        "-- Writer: `uv run python -m wowkb.gen_addon_quests` (high-confidence questIDs only).",
        "-- The addon MERGES this under ns.WEEKLY_QUESTS; hand-verified slugs win on",
        "-- id collision. Labels here are quest names (plan.py gates these on numeric id).",
        "local _, ns = ...",
        "ns.GENERATED_QUESTS = {",
    ]
    for qid, name, cadence in entries:
        lines.append("  [%d] = %s,  -- %s" % (qid, _lua_str(name), cadence))
    lines.append("}")
    lines.append("")  # trailing newline
    return "\n".join(lines)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="wowkb.gen_addon_quests", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--check", action="store_true",
                   help="exit 1 if the on-disk file differs (CI/pre-release guard)")
    p.add_argument("--print", dest="to_stdout", action="store_true",
                   help="write to stdout instead of the addon file")
    args = p.parse_args(argv)

    data = json.loads(REPEATABLES.read_text())
    content = render(data)
    n = content.count("] = ")

    if args.to_stdout:
        sys.stdout.write(content)
        return 0
    if args.check:
        current = OUT_LUA.read_text() if OUT_LUA.exists() else ""
        if current != content:
            print(f"OUT OF DATE: {OUT_LUA} — re-run `python -m wowkb.gen_addon_quests`")
            return 1
        print(f"up to date ({n} generated questIDs)")
        return 0

    OUT_LUA.parent.mkdir(parents=True, exist_ok=True)
    OUT_LUA.write_text(content)
    print(f"wrote {OUT_LUA.relative_to(REPO)} — {n} high-confidence questIDs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
