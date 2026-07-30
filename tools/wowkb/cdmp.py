"""Extract the CDMProbe pipeline DECISION LOG off the WoW SavedVariables file.

The probe (`/cdmp probe` + probe-baseline.json assertions) was retired 2026-07-29:
the secret-values / readability rules it discovered are settled game-wide invariants,
and a spec's tracked set comes from wago DB2 (`wowkb.spec_inventory`), so per-spec
re-measurement bought nothing. What remains is the always-on decision log — the
greppable pipeline trace this module flattens.

WHAT WE READ:

    CDMProbeDB.decisionlog   <- a ring of the last 3 sessions, each a list of one-line
                                `S{…} G{…} B{…}` pipeline traces appended on every
                                DECISION CHANGE (addon DecisionLog.lua).

⚠ SavedVariables only flush on /reload or logout. A capture that looks stale almost
always means the /reload was skipped.

    CDMProbeDB.alerttape     <- ⚠ TEMPORARY. The CDM alert-channel discovery tape
                                (addon AlertTape.lua): per session an `elig` eligibility
                                baseline, an `events` tape of every TriggerAlertEvent, and
                                a `fields` three-way readability probe of the pandemic
                                fields. Delete this half of the module with AlertTape.lua
                                once the rules land in knowledge/addon-dev/
                                api-events-and-discovery.md §2.8.

⚠ SavedVariables only flush on /reload or logout. A capture that looks stale almost
always means the /reload was skipped.

Usage:
    uv run python -m wowkb.cdmp decisionlog                 # → raw/cdmp-decision.log
    uv run python -m wowkb.cdmp decisionlog --out my.log
    uv run python -m wowkb.cdmp decisionlog --wow-path <dir>
    uv run python -m wowkb.cdmp alerttape                   # → raw/cdmp-alerttape.log
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
    """(decisionlog, path) from the newest CDMProbe.lua, or None."""
    pth = _find_savedvar(wow_path)
    if not pth:
        return None
    text = Path(pth).read_text(encoding="utf-8", errors="replace")
    db = parse_savedvar(text, "CDMProbeDB")
    if not isinstance(db, dict):
        return None
    return (db.get("decisionlog"), pth)


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

# --------------------------------------------------------------------------- #
# alerttape — the TEMPORARY CDM alert-channel discovery instrument               #
# --------------------------------------------------------------------------- #
# ⚠ Delete this section with the addon's AlertTape.lua once the alert-channel rules are
# settled in knowledge/addon-dev/api-events-and-discovery.md §2.8. It is a one-question
# instrument, not a permanent recorder.

def load_alerttape(wow_path: str) -> tuple[object, str] | None:
    """(alerttape, path) from the newest CDMProbe.lua, or None."""
    pth = _find_savedvar(wow_path)
    if not pth:
        return None
    db = parse_savedvar(Path(pth).read_text(encoding="utf-8", errors="replace"), "CDMProbeDB")
    if not isinstance(db, dict):
        return None
    return (db.get("alerttape"), pth)


def _rows(store) -> list[dict]:
    """The addon keys both channels by a dedup string, so SavedVariables yields a dict of
    row-dicts (not a positional array). Normalize either shape to a list of dicts."""
    if isinstance(store, dict):
        return [v for v in store.values() if isinstance(v, dict)]
    if isinstance(store, list):
        return [v for v in store if isinstance(v, dict)]
    return []


def cmd_alerttape(alerttape, path: str, out: Path) -> int:
    """Flatten the alert tape, newest session last.

    Two channels per session, and they answer different questions:
      EV  — did this alert type fire at all, in or out of combat, and how often
      FLD — the three-way READABILITY class of the pandemic fields (num/bool/SECRET/nil/
            threw). `SECRET` and `nil` mean very different things and are never merged.

    Read the EV rows for Available/OnCooldown FIRST: those are the control group. If they
    are present and PandemicTime is not, the instrument is live and the absence is a real
    finding; if nothing is present, the capture proves nothing (tape off, HUD off, or no
    /reload).
    """
    sessions = _aslist(alerttape)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    ev_total = fld_total = elg_total = 0
    for session in sessions:
        s = _asdict(session)
        lines.append(f"# session {s.get('started', '?')} v{s.get('version', '?')}")

        # ELG — the eligibility baseline, captured automatically when the session opened.
        # Read this FIRST: without it, "PandemicTime never appeared" is unreadable, because
        # you cannot tell "it fired and we missed it" from "this spell was never eligible".
        if s.get("eligError"):
            lines.append(f"ELG <unavailable: {s['eligError']}>")
        elgs = _rows(s.get("elig"))
        elgs.sort(key=lambda r: (str(r.get("viewer")), r.get("cid") or 0))
        for r in elgs:
            lines.append(
                f"ELG cid={r.get('cid')} spell={r.get('spellID')} [{r.get('viewer')}] "
                f"{r.get('name')} :: {r.get('types')}")
            elg_total += 1

        evs = _rows(s.get("events"))
        evs.sort(key=lambda r: (str(r.get("event")), str(r.get("combat")), r.get("cid") or 0))
        for r in evs:
            lines.append(
                f"EV  cid={r.get('cid')} event={r.get('event')} {r.get('combat')} "
                f"n={r.get('n')} first={r.get('first')} last={r.get('last')}")
            ev_total += 1

        flds = _rows(s.get("fields"))
        flds.sort(key=lambda r: (r.get("cid") or 0, str(r.get("combat"))))
        for r in flds:
            lines.append(
                f"FLD cid={r.get('cid')} {r.get('combat')} on={r.get('event')} "
                f"n={r.get('n')} class[{r.get('class')}] sample[{r.get('sample')}]")
            fld_total += 1

    out.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    print(f"{path}")
    print(f"{len(sessions)} session(s) · {elg_total} eligibility row(s) · "
          f"{ev_total} event row(s) · {fld_total} field row(s) → {out}")
    if ev_total == 0:
        print("\n⚠ No event rows. The capture proves NOTHING about the alert channel — "
              "check: /cdmp alerts on, /cdmp hud on, then a pull, then /reload.",
              file=sys.stderr)
    return 0


# --------------------------------------------------------------------------- #

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Extract CDMProbe recorders off SavedVariables.")
    ap.add_argument("command", choices=["decisionlog", "alerttape"],
                    help="decisionlog: flatten the pipeline decision log · alerttape: "
                         "flatten the temporary CDM alert-channel discovery tape")
    ap.add_argument("--wow-path", default=DEFAULT_WOW,
                    help=f"WoW _retail_ path (default: {DEFAULT_WOW})")
    ap.add_argument("--out", default=None,
                    help="flat .log destination (default: <repo>/raw/cdmp-<command>.log, gitignored)")
    args = ap.parse_args(argv)

    if args.command == "alerttape":
        loaded = load_alerttape(args.wow_path)
        if loaded is None:
            print(f"No readable CDMProbe.lua under "
                  f"{args.wow_path}/WTF/Account/*/SavedVariables/.", file=sys.stderr)
            return 1
        alerttape, path = loaded
        out = args.out or str(REPO_ROOT / "raw" / "cdmp-alerttape.log")
        return cmd_alerttape(alerttape, path, Path(out))

    loaded = load_decisionlog(args.wow_path)
    if loaded is None:
        print(f"No readable CDMProbe.lua under "
              f"{args.wow_path}/WTF/Account/*/SavedVariables/.", file=sys.stderr)
        print("Enable the HUD (/cdmp hud), play, and /reload first.", file=sys.stderr)
        return 1
    decisionlog, path = loaded
    out = args.out or str(REPO_ROOT / "raw" / "cdmp-decision.log")
    return cmd_decisionlog(decisionlog, path, Path(out))


if __name__ == "__main__":
    raise SystemExit(main())
