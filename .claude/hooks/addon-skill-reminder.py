#!/usr/bin/env python3
"""PreToolUse reminder: this file is WoW addon code, so route through the KB first.

Why this exists as a HOOK rather than a rule in a document. A task rarely *starts* as
addon work — it starts as "add a spec", becomes a KB edit, becomes a probe, and is
suddenly `CreateFrame` code. By then the moment to ask "does a skill cover this?" has
passed, and no amount of trigger wording catches a transition that happens mid-flow.
The harness runs this regardless of what anyone noticed.

Silent unless the path is addon code. Never blocks.
"""
import json
import re
import sys

# The addon checkouts (each gitignored, each its own repo) plus the scratch lab.
# `/addon/` covers combat-assist, keybinder and cooldown-hud without naming them, so a
# new addon under the same convention is covered on the day it appears.
ADDON_PATH = re.compile(
    r"(/ClientLab/|/addon/|/planner-state/|/PlannerState/).*\.(lua|xml|toc)$"
)

REMINDER = (
    "This file is WoW addon code (Lua/XML/.toc running in the client).\n"
    "Load the `wow-developer` skill before continuing if it is not already loaded.\n"
    "\n"
    "Routing, in order:\n"
    "1. START AT THE KB — `knowledge/addon-dev/`. Grep it for the API, event or widget "
    "you are about to touch. A section may already answer this; §3.5 of "
    "security-taint-and-restricted-data.md was five days old and unread when a probe "
    "was built against the API it replaces.\n"
    "2. GO TO SOURCE for what the KB does not cover — a gap, OR a claim you cannot "
    "apply unambiguously to the case in front of you. Ambiguity counts: reading source "
    "to disambiguate a KB claim is correct, guessing which reading applies is not.\n"
    "3. WRITE BACK what the source taught you, so the next reader starts one step "
    "further on.\n"
    "\n"
    "House rules apply, including rule 8 — a discarded error is a fabricated result."
)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0                      # malformed input is not this hook's business
    path = (payload.get("tool_input") or {}).get("file_path") or ""
    if not ADDON_PATH.search(path):
        return 0
    json.dump({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": REMINDER,
        },
        "suppressOutput": True,
    }, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
