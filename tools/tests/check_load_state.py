"""Offline verification for load_state dump selection (Phase 0.1).

Stdlib-only:  python3 tools/tests/check_load_state.py   (exits non-zero on failure)
Proves the auto-find picks the NEWEST dump ("the char you just played"), not the
alphabetically-first one, and that --character restricts to one character.
"""
import os
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # tools/
from wowkb.plan import load_state  # noqa: E402

_total = 0
_fails = []


def check(cond, msg):
    global _total
    _total += 1
    print(("PASS" if cond else "FAIL"), msg)
    if not cond:
        _fails.append(msg)


def _dump(root, account, realm, char, mtime):
    """Write a minimal PlannerState.lua under the real WTF layout, set its mtime."""
    d = pathlib.Path(root) / "WTF" / "Account" / account / realm / char / "SavedVariables"
    d.mkdir(parents=True, exist_ok=True)
    f = d / "PlannerState.lua"
    f.write_text(
        'PlannerStateDB = {\n'
        f'["character"] = "{char}",\n'
        '["realm"] = "Kil\'jaeden",\n'
        '["schema"] = 4,\n'
        '}\n')
    os.utime(f, (mtime, mtime))
    return f


with tempfile.TemporaryDirectory() as tmp:
    wow = pathlib.Path(tmp) / "_retail_"
    # Automatia sorts first alphabetically but is the OLDER dump; Encomplete is newer.
    _dump(wow, "112233", "Kiljaeden", "Automatia", mtime=1000)
    _dump(wow, "112233", "Kiljaeden", "Encomplete", mtime=9000)

    st = load_state(None, str(wow))
    check(st is not None and st.get("character") == "Encomplete",
          f"auto-find picks the NEWEST dump (Encomplete), got {st and st.get('character')!r}")

    st_a = load_state(None, str(wow), character="Automatia")
    check(st_a is not None and st_a.get("character") == "Automatia",
          f"--character Automatia restricts the glob, got {st_a and st_a.get('character')!r}")

    st_e = load_state(None, str(wow), character="Encomplete")
    check(st_e is not None and st_e.get("character") == "Encomplete",
          "--character Encomplete restricts the glob")

    st_none = load_state(None, str(wow), character="Nonexistent")
    check(st_none is None, "--character with no matching dump -> None")

print(f"\n{_total} checks, {len(_fails)} failures")
sys.exit(1 if _fails else 0)
