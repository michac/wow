"""Offline verification for `wowkb.capart`'s reading rule (render-shelf.md Part 0.5).

Stdlib-only:  python3 tools/tests/check_capart_reading.py   (exits non-zero on failure)

Part 0.5 is an ORDERED procedure with a fallback, not two independent claims:

    pass 1 — scan for a positive cue; if one is present, press it.
    pass 2 — OTHERWISE scan left to right and press the first entry not ruled out.

The case this file exists to pin is the one the old two-independent-gates arrangement made
unrepresentable: a row where pass 1 legitimately OVERRIDES elimination. That override is the whole
reason a positive cue exists, so a gate that forbids it forbids the exception it was carved for.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # tools/
from wowkb import capart  # noqa: E402

_total = 0
_fails = []


def check(cond, msg):
    global _total
    _total += 1
    print(("PASS" if cond else "FAIL"), msg)
    if not cond:
        _fails.append(msg)


# A minimal shelf: the four verdicts these rows use, and one positive cue beside one negative.
TOKENS = {
    "verdicts": {
        "cd": {"swipe": True, "cues": []},
        "weave": {"swipe": False, "cues": []},
        "hold-readable": {"swipe": False, "cues": ["blocked"]},
        "press": {"swipe": False, "cues": []},
        "below": {"swipe": False, "cues": []},
    },
    "cues": {
        "blocked": {"polarity": "negative", "slot": 1},
        "capped": {"polarity": "positive", "slot": 3},
    },
}


def row(*entries):
    out = []
    for e in entries:
        name, verdict = e[0], e[1]
        entry = {"name": name, "verdict": verdict}
        if len(e) > 2:
            entry["cues"] = list(e[2])
        out.append(entry)
    return out


def scenario(sid, entries):
    return {"id": sid, "row": entries}


# --- 1 · the passes AGREE: elimination reaches the press and it wears the positive cue ---------
agree = scenario("ST-agree", row(
    ("Metamorphosis", "cd"),
    ("Immolation Aura", "press", ["capped"]),
    ("Chaos Strike", "below"),
))
check(capart.reading_gate([agree], TOKENS) == [],
      "passes agree: swiped left, positive cue on the press -> clean")

# --- 2 · pass 1 OVERRIDES: a clean button sits LEFT of the positive cue ------------------------
# Havoc's rung 10 exactly: a banked Immolation Aura charge outranks Eye Beam, and no row position
# can say so. Elimination alone would land on Eye Beam; pass 1 is what makes the doc correct.
override = scenario("ST-override", row(
    ("Metamorphosis", "cd"),
    ("Eye Beam", "below"),
    ("Immolation Aura", "press", ["capped"]),
))
check(capart.reading_gate([override], TOKENS) == [],
      "pass 1 overrides elimination: clean button left of the positive cue -> allowed")
check(capart.elimination_gate([override], TOKENS) != [],
      "...and pass 2 alone WOULD have rejected it, which is why the chain matters")

# --- 3 · pass 1 still bites when the positive cue points at the wrong button -------------------
misplaced = scenario("ST-misplaced", row(
    ("Immolation Aura", "below", ["capped"]),
    ("Chaos Strike", "press"),
))
check(capart.reading_gate([misplaced], TOKENS) != [],
      "positive cue not on the press -> still a failure")

# --- 4 · a row with no positive cue is judged by elimination, unchanged ------------------------
plain_ok = scenario("ST-plain-ok", row(
    ("Metamorphosis", "hold-readable", ["blocked"]),
    ("Eye Beam", "press"),
    ("Chaos Strike", "below"),
))
check(capart.reading_gate([plain_ok], TOKENS) == [],
      "no positive cue: badged button skipped, scan lands on the press")

plain_bad = scenario("ST-plain-bad", row(
    ("Eye Beam", "below"),
    ("Chaos Strike", "press"),
))
check(capart.reading_gate([plain_bad], TOKENS) != [],
      "no positive cue: a clean button left of the press -> failure")

# --- 5 · `weave` is still stepped over by elimination ------------------------------------------
weave = scenario("ST-weave", row(
    ("Vengeful Retreat", "weave"),
    ("Eye Beam", "press"),
))
check(capart.reading_gate([weave], TOKENS) == [],
      "an off-GCD weave never competes for the GCD press")

# --- 6 · a malformed row is caught by the chain itself, not dropped between the passes ---------
# Both passes abstain without exactly one press, so the chain has to assert it.
for sid, entries in (
    ("ST-two-presses", row(("Eye Beam", "press"), ("Chaos Strike", "press"))),
    ("ST-no-press", row(("Eye Beam", "below"), ("Chaos Strike", "below"))),
    # …including when a positive cue is present, which is the half that used to fall through.
    ("ST-two-presses-positive", row(("Eye Beam", "press", ["capped"]),
                                    ("Chaos Strike", "press"))),
):
    check(capart.reading_gate([scenario(sid, entries)], TOKENS) != [],
          f"{sid}: a row without exactly one press is reported")

print()
print(f"{_total - len(_fails)}/{_total} passed")
if _fails:
    for f in _fails:
        print("  FAILED:", f)
    sys.exit(1)
