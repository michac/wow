"""Deploy the ClientLab scratch addon, and cross-check it against questions.json.

ClientLab is the lab addon (projects/addon-lab/): a long-lived scratch addon that
answers knowledge/addon-dev/ questions by running one line of Lua in the client.
It is deliberately NOT a product — no GitHub repo, no releases, no ghaddons, not in
the wowkb.addon registry. So its deploy is a plain DIRECTORY COPY into the WoW
install, and adding a test costs a copy, not a release cut.

    uv run python -m wowkb.lab deploy            # copy + registry cross-check
    uv run python -m wowkb.lab deploy --check     # cross-check only, don't copy
    uv run python -m wowkb.lab deploy --wow-path <dir>

THE REGISTRY CROSS-CHECK (cdmp.py:360-369's "no check function for this id" rule,
applied both directions): every `status: "built"` question in questions.json must
have a matching ns.Test{} in ClientLab/T_*.lua, and every ns.Test{} id must be a
built question. An unmatched id is a LOUD ERROR, never a silent skip — a test that
runs but has no registry row would emit a value nobody is expecting, and a built
row with no test is a silent hole in coverage.

W2 adds `show` / `report` (read a run off SavedVariables and render result beside
questions.json's `expect`). W1 builds only `deploy`.

Reuses charstate.DEFAULT_WOW rather than repeating the /mnt/c/... path here, where
it would rot out of step with every other tool.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

from .charstate import DEFAULT_WOW

REPO = Path(__file__).resolve().parents[2]
LAB = REPO / "projects" / "addon-lab"
SRC = LAB / "ClientLab"
QUESTIONS = LAB / "questions.json"

# ns.Test{ id = "X" ... }  and  ns.Test{ id="X" ... }
_ID_ASSIGN = re.compile(r'\bid\s*=\s*"([^"]+)"')
# T_Security's row("X", line, ...) helper
_ROW_CALL = re.compile(r'\brow\(\s*"([^"]+)"')


def lua_test_ids(src: Path = SRC) -> list[str]:
    """Every test id declared in ClientLab/T_*.lua, in file+source order.

    Two syntaxes: `ns.Test{ id = "..." }` (most files) and the `row("...", ...)`
    helper T_Security uses for the 14-row §4.2 table. Both are matched so the
    cross-check sees the whole registered set, not just the verbose form.
    """
    ids: list[str] = []
    for f in sorted(src.glob("T_*.lua")):
        text = f.read_text(encoding="utf-8")
        # Walk lines so an `id =` inside a row() call isn't double-counted: a row()
        # line has no `id =`, and a ns.Test{ has no row(. They are disjoint.
        for line in text.splitlines():
            m = _ID_ASSIGN.search(line)
            if m:
                ids.append(m.group(1))
                continue
            m = _ROW_CALL.search(line)
            if m:
                ids.append(m.group(1))
    return ids


def built_question_ids(path: Path = QUESTIONS) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [q["id"] for q in data["questions"] if q.get("status") == "built"]


def cross_check() -> tuple[bool, list[str]]:
    """Assert the Lua test set and the built-question set match, both directions.

    Returns (ok, messages). ok is False on ANY mismatch: a duplicate id, a built
    question with no test, or a test with no built question.
    """
    msgs: list[str] = []
    ok = True

    lua_ids = lua_test_ids()
    built = built_question_ids()

    dupes = sorted({i for i in lua_ids if lua_ids.count(i) > 1})
    if dupes:
        ok = False
        msgs.append(f"duplicate test id(s) in ClientLab/T_*.lua: {', '.join(dupes)}")

    lua_set, built_set = set(lua_ids), set(built)

    missing_tests = sorted(built_set - lua_set)
    if missing_tests:
        ok = False
        msgs.append("built questions with NO ns.Test{} in the Lua "
                    f"({len(missing_tests)}): {', '.join(missing_tests)}")

    orphan_tests = sorted(lua_set - built_set)
    if orphan_tests:
        ok = False
        msgs.append("ns.Test{} ids with NO built question in questions.json "
                    f"({len(orphan_tests)}): {', '.join(orphan_tests)}")

    if ok:
        msgs.append(f"registry cross-check OK — {len(lua_set)} tests match "
                    f"{len(built_set)} built questions, both directions.")
    return ok, msgs


def deploy(wow_path: str) -> tuple[bool, str]:
    """Mirror ClientLab/ into <wow>/Interface/AddOns/ClientLab/ (deletions too)."""
    dest_root = Path(wow_path) / "Interface" / "AddOns"
    if not dest_root.exists():
        return False, (f"AddOns directory not found: {dest_root}\n"
                       "Is --wow-path pointing at a real _retail_ install?")
    dest = dest_root / "ClientLab"
    # A clean copy mirrors deletions without a per-file diff: remove the addon's
    # own folder (and nothing else) then copy the source tree in whole.
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(SRC, dest)
    n = sum(1 for _ in dest.glob("*.lua"))
    return True, f"deployed {n} Lua files -> {dest}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Deploy the ClientLab scratch addon + cross-check the registry.")
    ap.add_argument("command", choices=["deploy"])
    ap.add_argument("--wow-path", default=DEFAULT_WOW,
                    help=f"WoW _retail_ path (default: {DEFAULT_WOW})")
    ap.add_argument("--check", action="store_true",
                    help="run the registry cross-check only; do not copy files")
    args = ap.parse_args(argv)

    ok, msgs = cross_check()
    for m in msgs:
        print(("  " if ok else "ERROR: ") + m, file=(sys.stdout if ok else sys.stderr))
    if not ok:
        print("registry cross-check FAILED — not deploying.", file=sys.stderr)
        return 1

    if args.check:
        return 0

    dok, dmsg = deploy(args.wow_path)
    print(("  " if dok else "ERROR: ") + dmsg, file=(sys.stdout if dok else sys.stderr))
    if dok:
        print("  in-game: /reload, then /clab run (OOC) -> /clab guide -> "
              "pull a dummy -> /clab run (combat) -> /reload.")
    return 0 if dok else 1


if __name__ == "__main__":
    raise SystemExit(main())
