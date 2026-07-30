"""Extract the CDMProbe pipeline DECISION LOG off the WoW SavedVariables file.

The probe (`/cdmp probe` + probe-baseline.json assertions) was retired 2026-07-29:
the secret-values / readability rules it discovered are settled game-wide invariants,
and a spec's tracked set comes from wago DB2 (`wowkb.spec_inventory`), so per-spec
re-measurement bought nothing. What remains is the always-on decision log — the
greppable pipeline trace this module flattens.

WHAT WE READ:

    CDMProbeDB.decisionlog   <- a ring of the last 3 sessions, each a list of one-line
                                `S{…} G{…} B{…}` pipeline traces appended on every
                                DECISION CHANGE (addon DecisionLog.lua). A pre-rename
                                capture stored it under `hud2log`, still read as a fallback.

⚠ SavedVariables only flush on /reload or logout. A capture that looks stale almost
always means the /reload was skipped.

Usage:
    uv run python -m wowkb.cdmp decisionlog                 # → raw/cdmp-decision.log
    uv run python -m wowkb.cdmp decisionlog --out my.log
    uv run python -m wowkb.cdmp decisionlog --wow-path <dir>
    # `hud2log` is a back-compat alias of `decisionlog`.
"""

from __future__ import annotations

import argparse
import glob
import os
import sys
from pathlib import Path

from .charstate import DEFAULT_WOW, parse_savedvar

REPO_ROOT = Path(__file__).resolve().parents[2]


# --------------------------------------------------------------------------- #
# Loading (mirrors diagnostics.py one-for-one)                                 #
# --------------------------------------------------------------------------- #

def _find_savedvar(wow_path: str) -> str | None:
    """Newest CDMProbe.lua under any account's SavedVariables (mtime desc)."""
    pattern = f"{wow_path}/WTF/Account/*/SavedVariables/CDMProbe.lua"
    hits = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
    return hits[0] if hits else None


def _aslist(v) -> list:
    """The Lua parser yields a Python list for a non-empty positional table but an
    empty dict for `{}`, and an int-keyed dict for a sparse array — normalize all
    three to a list."""
    if isinstance(v, list):
        return v
    if isinstance(v, dict):
        return [v[k] for k in sorted(v)] if v else []
    return []


def _asdict(v) -> dict:
    return v if isinstance(v, dict) else {}


def load_decisionlog(wow_path: str) -> tuple[object, str] | None:
    """(decisionlog, path) from the newest CDMProbe.lua, or None.

    A pre-rename capture stored the log under `hud2log`, so we fall back to that key
    when the new one is absent (an un-migrated on-disk capture still extracts).
    """
    pth = _find_savedvar(wow_path)
    if not pth:
        return None
    text = Path(pth).read_text(encoding="utf-8", errors="replace")
    db = parse_savedvar(text, "CDMProbeDB")
    if not isinstance(db, dict):
        return None
    decisionlog = db.get("decisionlog")
    if decisionlog is None:
        decisionlog = db.get("hud2log")   # back-compat: pre-Phase-4 capture
    return (decisionlog, pth)


# --------------------------------------------------------------------------- #

def cmd_decisionlog(decisionlog, path: str, out: Path) -> int:
    """Flatten the pipeline decision log to a grep-friendly .log file.

    Each session is written newest-last, headed by a `# session … tracked:…` line and
    then one entry per line. Real line numbers fall out for `grep -n`. The parser already
    un-escapes the entries (each is a single quote-free line by format), so there is
    nothing to un-escape here.
    """
    sessions = _aslist(decisionlog)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    total = 0
    for session in sessions:
        s = _asdict(session)
        entries = _aslist(s.get("entries"))
        lines.append(
            f"# session {s.get('started', '?')} v{s.get('version', '?')} "
            f"tracked:{s.get('tracked', '?')}")
        for e in entries:
            lines.append(str(e))
            total += 1
    out.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    print(f"{path}")
    print(f"{len(sessions)} session(s) · {total} line(s) → {out}")
    return 0


# --------------------------------------------------------------------------- #

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Extract the CDMProbe pipeline decision log.")
    ap.add_argument("command", choices=["decisionlog", "hud2log"],
                    help="flatten CDMProbeDB.decisionlog to a .log (hud2log is a back-compat alias)")
    ap.add_argument("--wow-path", default=DEFAULT_WOW,
                    help=f"WoW _retail_ path (default: {DEFAULT_WOW})")
    ap.add_argument("--out", default=str(REPO_ROOT / "raw" / "cdmp-decision.log"),
                    help="flat .log destination (default: <repo>/raw/cdmp-decision.log, gitignored)")
    args = ap.parse_args(argv)

    loaded = load_decisionlog(args.wow_path)
    if loaded is None:
        print(f"No readable CDMProbe.lua under "
              f"{args.wow_path}/WTF/Account/*/SavedVariables/.", file=sys.stderr)
        print("Enable the HUD (/cdmp hud), play, and /reload first.", file=sys.stderr)
        return 1
    decisionlog, path = loaded
    return cmd_decisionlog(decisionlog, path, Path(args.out))


if __name__ == "__main__":
    raise SystemExit(main())
