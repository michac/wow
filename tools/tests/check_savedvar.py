"""Offline round-trip test for the SavedVariables string un-escaper (Part 3).

Stdlib-only:  python3 tools/tests/check_savedvar.py   (exits non-zero on failure)

`charstate._string` is the shared Lua-string un-escaper every SavedVariables read
round-trips through (CDMProbe, PlannerState, BucketBinds, character data). The old
naive version kept the char after `\\` verbatim, so `\\n`->"n" and `\\t`->"t"; it
only survived because the hud2 DSL avoided newlines/quotes. This proves the correct
version handles named escapes, `\\ddd` DECIMAL byte escapes, and RAW multibyte utf-8
(the two spellings of `×` WoW actually emits).
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # tools/
from wowkb.charstate import parse_savedvar  # noqa: E402

_total = 0
_fails = []


def check(cond, msg):
    global _total
    _total += 1
    print(("PASS" if cond else "FAIL"), msg)
    if not cond:
        _fails.append(msg)


# A blob exercising every escape path. `\195\151` is the two-byte decimal escape for
# `×` (U+00D7 = c3 97); the `key_raw` value carries the SAME char as raw utf-8 bytes.
BLOB = (
    'TestDB = {\n'
    '["nl"] = "line1\\nline2",\n'
    '["tab"] = "a\\tb",\n'
    '["quote"] = "say \\"hi\\"",\n'
    '["backslash"] = "c:\\\\path",\n'
    '["dec_x"] = "a\\195\\151b",\n'
    '["raw_x"] = "a\u00d7b",\n'
    '["cr"] = "x\\ry",\n'
    '}\n'
)

db = parse_savedvar(BLOB, "TestDB")
check(isinstance(db, dict), f"parses to a dict, got {type(db).__name__}")
db = db or {}

check(db.get("nl") == "line1\nline2", f'\\n -> real newline, got {db.get("nl")!r}')
check(db.get("tab") == "a\tb", f'\\t -> real tab, got {db.get("tab")!r}')
check(db.get("quote") == 'say "hi"', f'\\" -> quote, got {db.get("quote")!r}')
check(db.get("backslash") == "c:\\path", f'\\\\ -> one backslash, got {db.get("backslash")!r}')
check(db.get("dec_x") == "a\u00d7b", f'\\195\\151 -> ×, got {db.get("dec_x")!r}')
check(db.get("raw_x") == "a\u00d7b", f'raw utf-8 × round-trips, got {db.get("raw_x")!r}')
check(db.get("cr") == "x\ry", f'\\r -> carriage return, got {db.get("cr")!r}')

print(f"\n{_total} checks, {len(_fails)} failures")
sys.exit(1 if _fails else 0)
