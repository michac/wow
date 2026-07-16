"""Read BucketBinds `/bb diagnostics` reports off the WoW SavedVariables file.

The BucketBinds addon can't write arbitrary files — like every addon it persists
only via SavedVariables, a serialized Lua table flushed to disk on /reload or
logout. `/bb diagnostics` populates `BucketBindsDB.diagnostics[<char>][<spec>]`
with a read-only classification of every seed bucket for the active spec plus a
live placement read-back and the list of castable abilities no seed bucket
covers. Reports ACCUMULATE across specs and characters (BucketBindsDB is
account-level), so the workflow is: run diagnostics in each spec, /reload per
character to flush, then run this reader.

This mirrors the on-disk read pattern wowkb.character already uses for Syndicator:
glob the newest BucketBinds.lua under WTF/Account/*/SavedVariables/, parse the
Lua table with charstate.parse_savedvar, and render the {char: {spec: report}}
tree.

Usage:
    uv run python -m wowkb.diagnostics
    uv run python -m wowkb.diagnostics --character Encomplete
    uv run python -m wowkb.diagnostics --character Encomplete --spec Affliction
    uv run python -m wowkb.diagnostics --json
    uv run python -m wowkb.diagnostics --wow-path "/mnt/c/.../_retail_"
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from .charstate import DEFAULT_WOW, parse_savedvar


def _find_savedvar(wow_path: str) -> str | None:
    """Newest BucketBinds.lua under any account's SavedVariables (mtime desc)."""
    pattern = f"{wow_path}/WTF/Account/*/SavedVariables/BucketBinds.lua"
    hits = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
    return hits[0] if hits else None


def _fmt_time(epoch) -> str:
    if not isinstance(epoch, (int, float)) or epoch <= 0:
        return "?"
    try:
        return (datetime.fromtimestamp(int(epoch), tz=timezone.utc)
                .astimezone().strftime("%Y-%m-%d %H:%M"))
    except (ValueError, OSError, OverflowError):
        return "?"


def _aslist(v) -> list:
    """The Lua parser yields a Python list for a non-empty positional table but an
    empty dict for `{}`, and an int-keyed dict for a sparse array — normalize all
    three to a list."""
    if isinstance(v, list):
        return v
    if isinstance(v, dict):
        return [v[k] for k in sorted(v)] if v else []
    return []


def _render_one(char: str, spec: str, report: dict) -> None:
    meta = report.get("meta") or {}
    summary = report.get("summary") or {}
    buckets = _aslist(report.get("buckets"))
    unmapped = _aslist(report.get("unmapped"))
    issues = _aslist(report.get("placementIssues"))

    spec_id = meta.get("specID", "?")
    print(f"\n── {char} / {spec} — {spec_id}, reviewed {_fmt_time(meta.get('time'))} ──")
    ver = meta.get("addonVersion")
    print(f"   addon v{ver}  ·  client {meta.get('build', '?')} ({meta.get('interface', '?')})")

    if not meta.get("seedKey"):
        print(f"   (no seed for {meta.get('classDisplay', '?')}/{spec} — counts below are castable-only)")

    print("   counts: "
          f"castable={summary.get('castableTotal', 0)} "
          f"known={summary.get('resolvedKnown', 0)} "
          f"untalented={summary.get('resolvedUnknown', 0)} "
          f"unresolved={summary.get('unresolved', 0)} "
          f"placeholder={summary.get('placeholders', 0)} "
          f"| onBar={summary.get('onBar', 0)} "
          f"placementIssues={summary.get('placementIssues', 0)} "
          f"unmapped={summary.get('unmapped', 0)}")

    # Unresolved seed names — the actionable seed bugs.
    bugs = [b for b in buckets if b.get("class") == "unresolved"]
    if bugs:
        print(f"   ! unresolved seed names (BUGS — seed drift/typo, {len(bugs)}):")
        for b in bugs:
            print(f"       {b.get('category')}: {b.get('name')!r}")

    # Placement mismatches — the "not popping up" headline.
    if issues:
        print(f"   ✗ placement mismatches ({len(issues)}):")
        for it in issues:
            detail = ""
            if it.get("issue") != "empty":
                actual = it.get("actualName") or it.get("actualType") or "?"
                detail = f" — has {actual} ({it.get('actualID')})"
            print(f"       slot {it.get('absSlot')} {it.get('category')}: "
                  f"want {it.get('intendedName')} ({it.get('intendedID')}) → "
                  f"{it.get('issue')}{detail}")

    # Untalented / not-learned — expected skips.
    skips = [b for b in buckets if b.get("class") == "resolved-unknown"]
    if skips:
        print(f"   · untalented / not learned (expected skips, {len(skips)}):")
        for b in skips:
            print(f"       {b.get('category')}: {b.get('name')} ({b.get('spellID')})")

    # Unmapped castable — the gaps.
    if unmapped:
        print(f"   gaps — castable abilities no seed bucket covers ({len(unmapped)}):")
        names = ", ".join(f"{u.get('name')} ({u.get('id')})" for u in unmapped)
        print(f"       {names}")


def _render(tree: dict, char_filter: str | None, spec_filter: str | None) -> None:
    stalest, stalest_label = None, None
    rendered = 0
    for char in sorted(tree):
        if char_filter and char_filter.lower() not in char.lower():
            continue
        byspec = tree[char]
        if not isinstance(byspec, dict):
            continue
        for spec in sorted(byspec):
            if spec_filter and spec_filter.lower() not in spec.lower():
                continue
            report = byspec[spec]
            if not isinstance(report, dict):
                continue
            _render_one(char, spec, report)
            rendered += 1
            t = (report.get("meta") or {}).get("time")
            if isinstance(t, (int, float)) and t > 0 and (stalest is None or t < stalest):
                stalest, stalest_label = t, f"{char} / {spec}"

    if rendered == 0:
        print("\nNo matching reports.")
        return
    # Freshness hint only makes sense across the unfiltered set.
    if stalest is not None and not char_filter and not spec_filter and rendered > 1:
        print(f"\nstalest report: {stalest_label} — {_fmt_time(stalest)} "
              "(re-run /bb diagnostics in that spec to refresh it)")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Render accumulated BucketBinds /bb diagnostics reports.")
    ap.add_argument("--character", help="filter to reports whose char key contains this")
    ap.add_argument("--spec", help="filter to reports whose spec name contains this")
    ap.add_argument("--wow-path", default=DEFAULT_WOW,
                    help=f"WoW _retail_ path (default: {DEFAULT_WOW})")
    ap.add_argument("--json", action="store_true",
                    help="dump the whole {char: {spec: report}} tree as JSON")
    args = ap.parse_args(argv)

    pth = _find_savedvar(args.wow_path)
    if not pth:
        print(f"No BucketBinds.lua under {args.wow_path}/WTF/Account/*/SavedVariables/.",
              file=sys.stderr)
        print("Run /bb diagnostics in-game and /reload first.", file=sys.stderr)
        return 1

    text = Path(pth).read_text(encoding="utf-8", errors="replace")
    db = parse_savedvar(text, "BucketBindsDB")
    if not isinstance(db, dict):
        print(f"Couldn't parse BucketBindsDB from {pth}.", file=sys.stderr)
        return 1
    tree = db.get("diagnostics")
    if not isinstance(tree, dict) or not tree:
        print(f"No diagnostics recorded in {pth}.", file=sys.stderr)
        print("Run /bb diagnostics in-game (per spec), then /reload.", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(tree, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    print(f"BucketBinds diagnostics — {pth}")
    _render(tree, args.character, args.spec)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
