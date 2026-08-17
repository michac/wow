"""Pass identity for KB maintenance runs — who last touched a file, not just when.

`reviewed:` in a knowledge file records the DATE a pass verified it, and
`grep -rL 'reviewed: <date>'` after a sweep is the audit that catches files left
behind. That works until two passes run on the same day, at which point the second
pass's stamps are indistinguishable from the first's and a file covered by neither
scope can look covered.

So a pass gets an ID — `<YYYY-MM-DD>.<n>`, allocated here, never reused — recorded in
`_meta/feed-watermark.md` between machine-readable markers. GENERATED artifacts stamp
the full ID in their front matter, which makes one specific failure detectable:

    the global update ran pass 2026-08-17.2, but simc-apl.md still says 2026-08-11.1
    ⇒ that pass did not regenerate the APLs, whatever its log claims.

That is the `spec_inventory.PINNED_BUILD` defect the 12.1 sweep found by hand — a
"regeneration" that silently re-emits the old patch — turned into a gate.

Hand-written files are NOT migrated: they keep `reviewed:` as a plain date, because
the front-matter convention needs it parseable and `reviewed: >= fetched:` depends on
it. The residual limit is recorded in `allocate()`.

Usage:
    uv run python -m wowkb.kbpass current                      # the active pass ID
    uv run python -m wowkb.kbpass allocate --kind full --scope "12.1 sweep"
    uv run python -m wowkb.kbpass check                        # generated artifacts vs the active pass
"""

import argparse
import datetime
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
WATERMARK = REPO / "knowledge" / "_meta" / "feed-watermark.md"

BEGIN = "<!-- pass:begin -->"
END = "<!-- pass:end -->"

# The generated artifacts a pass is expected to refresh. A pass that claims to have
# run but leaves one of these on an older ID did not do what its log says.
GENERATED = (
    "knowledge/classes/*/*/simc-apl.md",
)

ROW = re.compile(r"^\|\s*`(\d{4}-\d{2}-\d{2}\.\d+)`\s*\|([^|]*)\|([^|]*)\|(.*)\|\s*$")


def _table() -> list[tuple[str, str, str, str]]:
    """(id, date, kind, scope) rows from the watermark's machine-readable block."""
    try:
        text = WATERMARK.read_text(encoding="utf-8")
    except OSError:
        return []
    block = re.search(re.escape(BEGIN) + r"(.*?)" + re.escape(END), text, re.S)
    if not block:
        return []
    rows = []
    for line in block.group(1).splitlines():
        m = ROW.match(line.strip())
        if m:
            rows.append(tuple(g.strip() for g in m.groups()))
    return rows


def current() -> str | None:
    """The most recently allocated pass ID, or None if the block is absent/empty."""
    rows = _table()
    return rows[-1][0] if rows else None


def allocate(kind: str, scope: str, today: str | None = None) -> tuple[str, list[str]]:
    """Mint the next pass ID and append it to the watermark. Returns (id, warnings).

    Same-day passes get `.1`, `.2`, … so the ID never collides. The warning names the
    one case that still loses information: two same-day passes over OVERLAPPING scopes,
    where hand-written files stamped `reviewed:` by the first are indistinguishable
    from ones the second covered.
    """
    day = today or datetime.date.today().isoformat()
    rows = _table()
    same_day = [r for r in rows if r[1] == day]
    pass_id = f"{day}.{len(same_day) + 1}"

    warnings = []
    for r in same_day:
        warnings.append(
            f"pass {r[0]} already ran today over scope {r[3]!r} — if that overlaps "
            f"{scope!r}, `grep -rL 'reviewed: {day}'` cannot tell the two apart for "
            f"hand-written files. Generated artifacts are unaffected (they carry the ID)."
        )

    text = WATERMARK.read_text(encoding="utf-8")
    row = f"| `{pass_id}` | {day} | {kind} | {scope} |"
    text = text.replace(END, row + "\n" + END, 1)
    WATERMARK.write_text(text, encoding="utf-8")
    return pass_id, warnings


def stamped(path: pathlib.Path) -> str | None:
    """The `pass:` ID in a generated file's front matter, if it carries one."""
    try:
        head = path.read_text(encoding="utf-8")[:2000]
    except OSError:
        return None
    m = re.search(r"^pass:\s*(\S+)\s*$", head, re.M)
    return m.group(1) if m else None


def check() -> int:
    """Generated artifacts whose pass ID is behind the active one. Exit 1 if any."""
    active = current()
    if not active:
        print(f"error: no pass table in {WATERMARK.relative_to(REPO)}", file=sys.stderr)
        return 1

    behind, unstamped, total = [], [], 0
    for pattern in GENERATED:
        for path in sorted(REPO.glob(pattern)):
            total += 1
            got = stamped(path)
            rel = path.relative_to(REPO)
            if got is None:
                unstamped.append(str(rel))
            elif got != active:
                behind.append(f"{rel} — pass {got}, active is {active}")

    print(f"active pass {active}; checked {total} generated artifact(s)")
    for u in unstamped:
        print(f"  ⚠ {u} — no pass stamp")
    for b in behind:
        print(f"  ❌ {b}")
    if behind:
        print("\nA generated artifact behind the active pass means that pass did not "
              "regenerate it, whatever its log says.", file=sys.stderr)
    return 1 if behind else 0


def main() -> None:
    p = argparse.ArgumentParser(prog="wowkb.kbpass", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("current", help="print the active pass ID")
    sub.add_parser("check", help="generated artifacts vs the active pass; exit 1 if behind")
    a = sub.add_parser("allocate", help="mint the next pass ID and record it")
    a.add_argument("--kind", required=True, help="feed | full | tooling | …")
    a.add_argument("--scope", required=True, help="what this pass covers, one line")
    args = p.parse_args()

    if args.cmd == "current":
        cur = current()
        if not cur:
            sys.exit(f"error: no pass table in {WATERMARK.relative_to(REPO)}")
        print(cur)
    elif args.cmd == "check":
        sys.exit(check())
    else:
        pass_id, warnings = allocate(args.kind, args.scope)
        for w in warnings:
            print(f"⚠ {w}", file=sys.stderr)
        print(pass_id)


if __name__ == "__main__":
    main()
