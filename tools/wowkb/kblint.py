"""The addon-dev KB gates — README §7's current-state rule, mechanically.

A topic file states what is true now. It never states what it used to say. These are the
three checks that keep it that way:

  1. no retrospective prose ("an earlier draft said…") outside a Changelog
  2. every date sits in front matter, a citation, a [client] tag, or the Changelog
  3. no section corrected by a later part of the SAME file

    uv run python -m wowkb.kblint            # report, exit 1 on any hit
    uv run python -m wowkb.kblint --counts   # per-file table only
    uv run python -m wowkb.kblint --gate 2   # one gate

Why a tool and not three greps: a grep cannot tell a front-matter continuation line from
prose, cannot skip a fenced code block (so README §7's own gate definitions match
themselves), and cannot tell `security.md §4.6` — a cross-file pointer — from `§4.6`, a
self-correction. Each of those produced a false positive that cost an agent real work.
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
KB = REPO / "knowledge" / "addon-dev"

# Queues are exempt from everything: a queue entry IS a dated event (README §1.2).
# sources.md is a registry whose rows are "what was on disk, when".
QUEUES = {"observations.md", "mined-pending-verification.md", "12.1.0-ptr-heads-up.md"}
REGISTRY = {"sources.md"}

# README §7 *defines* the rules, so its prose necessarily contains the patterns it bans.
DOCTRINE = {"README.md"}
DOCTRINE_SECTION = re.compile(r"^## 7\. How a claim is written")

RETRO = re.compile(
    r"an earlier (draft|version|pass|run|note)"
    r"|previously (said|read|cited|written|showed|gave|asserted)"
    r"|\[corrected"
    r"|used to (be|read|say|assert|show)"
    r"|GRADE CORRECTION"
    r"|\*\*Correction"
    r"|Adversarial verification pass", re.I)

DATE = re.compile(r"20[0-9]{2}-[0-9]{2}-[0-9]{2}")

# A date is legal inside a bracketed citation stamp or a [client] tag. The bracket may
# open on an earlier line (citations wrap), so we also accept a line that is plainly a
# continuation of one.
DATE_OK = re.compile(
    r"\[(T[0-9][^]]*|client|gh[^]]*)\s"          # [T2 wiki: …  [client …  [gh: …
    r"|revid [0-9]+,\s*20"
    r"|lastedit \*{0,2}20|rev [0-9]+, lastedit"   # wiki citation, the revid twin
    r"|filed 20|closed 20|created 20"             # a bug's era is evidence about the bug
    r"|pushed_at 20|created_at 20"
    r"|@ '?[0-9a-f]{6,}'?,\s*20"                 # commit-pin: @ '3fdc10f6', 2026-07-21
    r"|`[0-9a-f]{6,}`,\s*20"                     # commit-pin: `38d4bf1e`, 2026-07-20
    r"|`[0-9a-f]{6,}`\s*\(20"                    # commit-pin: `e89d5055c761` (2026-07-16)
    r"|@ ?`?[0-9a-f]{6,}`?"                      # any `path @ <sha>` pin on the same line
    r"|\$(Id|Revision):"                         # SVN keyword expansion, verbatim
    r"|quoted at|\"\s*,\s*20[0-9]{2}-")          # blue-post attribution inside a quote

# Gate 3: a ⚠/❌ pointing at a § in THIS file is a defect ticket. One qualified by a
# filename is an ordinary cross-reference.
SELFREF = re.compile(r"(⚠⚠?|❌)(?P<mid>.{0,120}?)§[0-9]")
FILENAME_NEAR = re.compile(r"[A-Za-z0-9_.-]+\.md`?[\s,]*$|README`?[\s,]*$")


def strip(path: Path) -> list[tuple[int, str]]:
    """(lineno, text) for lines that carry a CLAIM.

    Drops front matter (including wrapped continuation lines), fenced code blocks, the
    Changelog section, and — in the doctrine file — the section that defines these rules.
    """
    out: list[tuple[int, str]] = []
    in_fm = False
    in_fence = False
    done = False
    doctrine = path.name in DOCTRINE

    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if i == 1 and line.strip() == "---":
            in_fm = True
            continue
        if in_fm:
            if line.strip() == "---":
                in_fm = False
            continue
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or done:
            continue
        if line.startswith("## Changelog"):
            done = True
            continue
        if doctrine and DOCTRINE_SECTION.match(line):
            done = True          # §7 is last in README; everything after defines the rules
            continue
        out.append((i, line))
    return out


def check(path: Path) -> dict[int, list[tuple[int, str]]]:
    name = path.name
    hits: dict[int, list[tuple[int, str]]] = {1: [], 2: [], 3: []}
    if name in QUEUES:
        return hits
    lines = strip(path)

    for n, text in lines:
        if RETRO.search(text):
            hits[1].append((n, text.strip()))
        if name not in REGISTRY and DATE.search(text) and not DATE_OK.search(text):
            hits[2].append((n, text.strip()))
        m = SELFREF.search(text)
        if m and not FILENAME_NEAR.search(m.group("mid")):
            hits[3].append((n, text.strip()))
    return hits


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="python -m wowkb.kblint",
        description="Check knowledge/addon-dev against README §7's current-state rule.")
    ap.add_argument("--counts", action="store_true", help="per-file table only")
    ap.add_argument("--gate", type=int, choices=(1, 2, 3), help="report one gate only")
    args = ap.parse_args(argv)

    gates = [args.gate] if args.gate else [1, 2, 3]
    names = {1: "retrospective prose", 2: "date in prose", 3: "self-correcting section"}
    total = {g: 0 for g in gates}
    rows = []

    for path in sorted(KB.glob("*.md")):
        hits = check(path)
        counts = {g: len(hits[g]) for g in gates}
        for g in gates:
            total[g] += counts[g]
        rows.append((path.name, counts, hits))

    w = max(len(r[0]) for r in rows)
    print(f"{'file':<{w}}  " + "  ".join(f"G{g}" for g in gates))
    for name, counts, _ in rows:
        if any(counts.values()) or not args.counts:
            marks = "  ".join(f"{counts[g] or '.':>2}" for g in gates)
            print(f"{name:<{w}}  {marks}")
    print(f"{'TOTAL':<{w}}  " + "  ".join(f"{total[g]:>2}" for g in gates))

    if not args.counts:
        for name, counts, hits in rows:
            for g in gates:
                for n, text in hits[g]:
                    print(f"\n{name}:{n}  [gate {g}: {names[g]}]\n    {text[:160]}")

    return 1 if any(total.values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())
