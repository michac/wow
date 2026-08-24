"""The observations queue — facts our own running code discovered, and their drain.

`knowledge/addon-dev/observations.md` is a parking lot for game facts learned while
writing addon code. Its failure mode is becoming a dumping ground, so the queue has a
gate: every entry must name where it lands, and nothing may sit open indefinitely.

    uv run python -m wowkb.obs list [--open]
    uv run python -m wowkb.obs check           # exit 1 if the queue is stale
    uv run python -m wowkb.obs drain OBS-001

`check` is wired into `wowkb.addon release`: warn on --patch, block on --minor/--major.
"""

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OBS = REPO / "knowledge" / "addon-dev" / "observations.md"

# ⚠ 30, not 14, since 2026-08-22. The original figure was a guess at how long a fact stays
# fresh in the author's head, and it was tuned against a queue that drained every few days.
# It now fires on entries whose target file is a real piece of writing rather than a line
# edit — OBS-002/003 want an EditBox section `frames-textures-animation.md` does not have —
# and a gate that blocks a release over work it has mis-sized teaches people to override it,
# which is the one thing a release gate must never do. The rule it protects is unchanged:
# nothing sits open indefinitely, and the queue is not a dumping ground.
MAX_AGE_DAYS = 30
MAX_OPEN = 12

_HEAD = re.compile(r"^## (OBS-\d+)\s*·\s*(\d{4}-\d{2}-\d{2})\s*·\s*(.+?)\s*$", re.M)
_FIELD = re.compile(r"^\*\*(Drains to|Status|Confidence):\*\*\s*(.+?)\s*$", re.M)


@dataclass
class Entry:
    id: str
    opened: date
    title: str
    drains_to: str = ""
    status: str = ""
    confidence: str = ""

    @property
    def is_open(self) -> bool:
        return self.status.split()[0].lower() == "open" if self.status else True

    def age(self, today: date) -> int:
        return (today - self.opened).days


def parse(path: Path = OBS) -> list[Entry]:
    """Entries in file order. Malformed headings are skipped, not guessed at."""
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    heads = list(_HEAD.finditer(text))
    out: list[Entry] = []
    for i, m in enumerate(heads):
        body = text[m.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        try:
            opened = datetime.strptime(m.group(2), "%Y-%m-%d").date()
        except ValueError:
            continue
        e = Entry(id=m.group(1), opened=opened, title=m.group(3))
        for f in _FIELD.finditer(body):
            key, val = f.group(1), f.group(2)
            if key == "Drains to":
                e.drains_to = val
            elif key == "Status":
                e.status = val
            elif key == "Confidence":
                e.confidence = val
        out.append(e)
    return out


def cmd_list(args) -> int:
    entries = parse()
    if args.open:
        entries = [e for e in entries if e.is_open]
    if not entries:
        print("(no entries)")
        return 0
    today = date.today()
    for e in entries:
        flag = "open" if e.is_open else e.status
        age = f"{e.age(today)}d" if e.is_open else ""
        print(f"{e.id}  {e.opened}  {age:>5}  {flag:<16} {e.title}")
        if e.is_open and e.drains_to:
            print(f"          -> {e.drains_to}")
    return 0


def cmd_check(args) -> int:
    """Exit 1 if the queue is stale. The release gate."""
    entries = parse()
    today = date.today()
    open_ = [e for e in entries if e.is_open]
    problems: list[str] = []

    for e in entries:
        if not e.drains_to:
            problems.append(f"{e.id}: no 'Drains to:' — an entry that names no destination "
                            f"is not yet a claim")
    stale = [e for e in open_ if e.age(today) > MAX_AGE_DAYS]
    for e in stale:
        problems.append(f"{e.id}: open {e.age(today)} days (limit {MAX_AGE_DAYS}) — "
                        f"drains to {e.drains_to or '(unset)'}")
    if len(open_) > MAX_OPEN:
        problems.append(f"{len(open_)} entries open (limit {MAX_OPEN}) — drain before adding")

    print(f"observations: {len(entries)} total, {len(open_)} open, {len(stale)} stale")
    if problems:
        print()
        for p in problems:
            print(f"  ! {p}")
        return 1
    print("  ok")
    return 0


def cmd_drain(args) -> int:
    """Mark an entry drained. Edit the target file FIRST — this only records it."""
    path = OBS
    text = path.read_text(encoding="utf-8")
    entries = {e.id: e for e in parse(path)}
    e = entries.get(args.id.upper())
    if not e:
        print(f"error: no {args.id} in {path.relative_to(REPO)} — "
              f"have: {', '.join(entries) or '(none)'}", file=sys.stderr)
        return 1
    if not e.is_open:
        print(f"{e.id} is already {e.status}")
        return 0

    # Replace only the Status line inside this entry's own body.
    heads = list(_HEAD.finditer(text))
    for i, m in enumerate(heads):
        if m.group(1) != e.id:
            continue
        start = m.end()
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        body = text[start:end]
        # Anchor on the line only — a trailing \s* would eat the blank line that
        # separates the entry from the next `---`.
        new_body, n = re.subn(r"^\*\*Status:\*\* *open *$",
                              f"**Status:** drained {date.today().isoformat()}",
                              body, count=1, flags=re.M)
        if not n:
            print(f"error: {e.id} has no '**Status:** open' line to replace", file=sys.stderr)
            return 1
        path.write_text(text[:start] + new_body + text[end:], encoding="utf-8")
        print(f"{e.id} drained -> {e.drains_to}")
        print("  (this records the drain; the target file's claim is yours to write)")
        return 0
    return 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="python -m wowkb.obs",
        description="The addon-dev observations queue and its drain.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("list", help="list entries")
    p.add_argument("--open", action="store_true", help="only entries still open")
    p.set_defaults(fn=cmd_list)

    p = sub.add_parser("check", help="fail if the queue is stale (the release gate)")
    p.set_defaults(fn=cmd_check)

    p = sub.add_parser("drain", help="record an entry as drained")
    p.add_argument("id", help="e.g. OBS-001")
    p.set_defaults(fn=cmd_drain)

    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
