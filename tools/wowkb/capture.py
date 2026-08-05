"""The one reader for addon captures.

Every addon in this workspace writes captures to a single SavedVariables key with one
shape (`<AddonDB>.captures.<stream>`), and this module is the only thing that reads it.
The contract lives in `.claude/skills/wow-developer/references/capture-and-dump-standard.md`.

That the reader is shared is the enforcement: an addon that writes the wrong shape fails
here, loudly, the first time anyone reads a capture. There is no lint and no CI gate
because none is needed.

    uv run python -m wowkb.capture cdmp decision
    uv run python -m wowkb.capture cdmp --list
    uv run python -m wowkb.capture bb dump --out raw/bb-dump.log

Graders stay per-addon (`wowkb.cdmp flight` and friends). They consume `load()` and never
glob a path themselves.

⚠ SavedVariables only flush on `/reload` or logout.
"""

import argparse
import glob
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

from .charstate import DEFAULT_WOW, parse_savedvar

REPO = Path(__file__).resolve().parents[2]

# short name -> the addon folder name, from which both the SavedVariables file
# (<name>.lua) and the global (<name>DB) follow. Kept as a literal here so reading a
# capture never imports the release machinery.
#
# This registry is about WHO WRITES CAPTURES, not who gets released — the two sets
# overlap but are not the same. `wowkb.addon`'s REGISTRY is the three product addons
# (release targets); ClientLab is deliberately NOT one (projects/addon-lab/CLAUDE.md:
# no repo, no releases, deploy is a directory copy) and still writes captures, so it
# belongs here and nowhere near a release gate.
ADDONS = {
    "bb": "BucketBinds",
    "cdmp": "CDMProbe",
    "clab": "ClientLab",
    "ps": "PlannerState",
}


def _aslist(v) -> list:
    """The Lua parser yields a list for a non-empty positional table, an empty dict for
    `{}`, and an int-keyed dict for a sparse array — normalize all three to a list.

    A table carrying BOTH positional entries and named keys yields mixed key types, and
    a bare `sorted()` over those raises TypeError. That is a malformed capture, which is
    exactly the case this reader exists to catch loudly rather than crash on: take the
    positional entries in index order and drop the named ones, so a caller gets the rows
    that are readable instead of a stack trace.
    """
    if isinstance(v, list):
        return v
    if isinstance(v, dict):
        idx = sorted(k for k in v if isinstance(k, int))
        return [v[k] for k in idx]
    return []


def _asdict(v) -> dict:
    return v if isinstance(v, dict) else {}


def _scalar(v) -> str:
    """One value, spelled the way the CLIENT spells it — `true`, not Python's `True`.

    A capture is a record of what the game said. Letting `repr` through would put
    Python syntax (`'nil'`, `False`, `None`) into a log about Lua, and that text gets
    quoted into KB prose.
    """
    if v is None:
        return "nil"
    if isinstance(v, bool):
        return "true" if v else "false"
    return str(v)


def render_value(v) -> str:
    """A stored value as a deterministic, diffable one-liner.

    Rows may carry a nested value — `wowkb.lab`'s test results are the first real user
    of the row path and read individual sub-fields. Rendering happens HERE, at read
    time, not in the addon: the `.log` is a DERIVED artifact regenerable from the same
    SavedVariables, so a better renderer can be applied retroactively. That is exactly
    what a pre-rendered `line` cannot do (§2 rule 4), and it is why a structured value
    costs nothing in grep-ability — `flatten` still emits one line per row.

    Keys are sorted so two runs of the same test render byte-identically and a diff
    means the CLIENT changed, not the renderer. Recurses one level, which is as deep as
    any current writer persists.
    """
    if isinstance(v, dict):
        parts = []
        for k in sorted(v, key=str):
            inner = v[k]
            if isinstance(inner, dict):
                sub = ", ".join(f"{k2}={_scalar(inner[k2])}" for k2 in sorted(inner, key=str))
                parts.append(f"{k}={{{sub}}}")
            else:
                parts.append(f"{k}={_scalar(inner)}")
        return "{" + ", ".join(parts) + "}"
    if isinstance(v, list):
        return "[" + ", ".join(render_value(x) for x in v) + "]"
    return _scalar(v)


def find_savedvar(name: str, wow_path: str = DEFAULT_WOW) -> str | None:
    """Newest <name>.lua under any account's SavedVariables, by mtime.

    Checks BOTH layouts, because they are not interchangeable and an addon may switch:
      account-wide   WTF/Account/<acct>/SavedVariables/<name>.lua
      per-character  WTF/Account/<acct>/<realm>/<char>/SavedVariables/<name>.lua
    PlannerState uses `## SavedVariablesPerCharacter`, so searching only the first
    layout finds nothing and reports an empty capture rather than a missing one.
    """
    patterns = (
        f"{wow_path}/WTF/Account/*/SavedVariables/{name}.lua",
        f"{wow_path}/WTF/Account/*/*/*/SavedVariables/{name}.lua",
    )
    hits: list[str] = []
    for p in patterns:
        hits.extend(glob.glob(p))
    hits.sort(key=os.path.getmtime, reverse=True)
    return hits[0] if hits else None


@dataclass
class Session:
    """One addon load's worth of one stream."""
    started: str = "?"
    version: str = "?"
    meta: dict = field(default_factory=dict)
    lines: list = field(default_factory=list)
    rows: list = field(default_factory=list)

    @property
    def header(self) -> str:
        bits = [f"# session {self.started} v{self.version}"]
        for k in sorted(self.meta):
            bits.append(f"{k}:{self.meta[k]}")
        return " ".join(bits)


@dataclass
class Capture:
    """Every stream from one addon's SavedVariables."""
    addon: str
    path: str
    _streams: dict

    def streams(self) -> list[str]:
        return sorted(self._streams)

    def sessions(self, stream: str) -> list[Session]:
        """Sessions for a stream, oldest first — the order the addon wrote them."""
        out: list[Session] = []
        for raw in _aslist(self._streams.get(stream)):
            s = _asdict(raw)
            out.append(Session(
                started=s.get("started", "?"),
                version=s.get("version", "?"),
                meta=_asdict(s.get("meta")),
                lines=_aslist(s.get("lines")),
                rows=[_asdict(r) for r in _aslist(s.get("rows"))],
            ))
        return out

    def flatten(self, stream: str, out: Path) -> int:
        """Write a greppable .log: sessions newest-last, one entry per line.

        Real line numbers fall out for `grep -n`. Returns the number of entry lines
        written (headers excluded).
        """
        sessions = self.sessions(stream)
        lines: list[str] = []
        total = 0
        for s in sessions:
            lines.append(s.header)
            for ln in s.lines:
                lines.append(str(ln))
                total += 1
            # A row-bearing stream still flattens, so `--out` is never empty for one:
            # rows are rendered as sorted k=v so the text stays diffable between runs.
            # render_value, not str(), so a nested value stays greppable Lua rather
            # than becoming a Python dict repr.
            for r in s.rows:
                lines.append("  " + " ".join(f"{k}={render_value(r[k])}"
                                             for k in sorted(r)))
                total += 1
        out = Path(out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
        return total


def load(addon: str, wow_path: str = DEFAULT_WOW) -> Capture | None:
    """Parse the newest SavedVariables for `addon` and return its captures.

    Returns None when the file is absent or unparseable — the caller decides whether
    that is fatal. An addon that exists but has never captured anything returns a
    Capture with no streams, which is a different and non-fatal condition.
    """
    name = ADDONS.get(addon)
    if not name:
        return None
    pth = find_savedvar(name, wow_path)
    if not pth:
        return None
    text = Path(pth).read_text(encoding="utf-8", errors="replace")
    db = parse_savedvar(text, f"{name}DB")
    if not isinstance(db, dict):
        return None
    return Capture(addon=addon, path=pth, _streams=_asdict(db.get("captures")))


# ----------------------------------------------------------------------------- CLI


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="python -m wowkb.capture",
        description="Read an addon capture stream off SavedVariables.")
    ap.add_argument("addon", choices=sorted(ADDONS), help="addon short name")
    ap.add_argument("stream", nargs="?", help="stream to flatten (omit with --list)")
    ap.add_argument("--list", action="store_true",
                    help="list streams and their session counts, then exit")
    ap.add_argument("--out", type=Path,
                    help="output .log path (default: raw/<addon>-<stream>.log)")
    ap.add_argument("--wow-path", default=DEFAULT_WOW,
                    help=f"WoW _retail_ path (default: {DEFAULT_WOW})")
    args = ap.parse_args(argv)

    cap = load(args.addon, args.wow_path)
    if cap is None:
        name = ADDONS[args.addon]
        print(f"error: no readable {name}.lua under {args.wow_path}/WTF/Account/",
              file=sys.stderr)
        print("  the addon must have been loaded and the client /reload'ed or logged out",
              file=sys.stderr)
        return 1

    if args.list or not args.stream:
        print(f"# {ADDONS[args.addon]}  {cap.path}")
        streams = cap.streams()
        if not streams:
            print("  (no captures — nothing has written to <DB>.captures yet)")
            return 0
        for name in streams:
            sessions = cap.sessions(name)
            entries = sum(len(s.lines) + len(s.rows) for s in sessions)
            newest = sessions[-1].started if sessions else "?"
            print(f"  {name:<12} {len(sessions):>2} sessions  {entries:>6} entries"
                  f"  newest {newest}")
        return 0

    if args.stream not in cap.streams():
        print(f"error: no stream '{args.stream}' in {ADDONS[args.addon]} — "
              f"have: {', '.join(cap.streams()) or '(none)'}", file=sys.stderr)
        return 1

    out = args.out or (REPO / "raw" / f"{args.addon}-{args.stream}.log")
    n = cap.flatten(args.stream, out)
    sessions = cap.sessions(args.stream)
    try:
        shown = out.relative_to(REPO)
    except ValueError:
        shown = out
    print(f"wrote {n} entries across {len(sessions)} sessions -> {shown}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
