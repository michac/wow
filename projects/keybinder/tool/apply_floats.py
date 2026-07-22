#!/usr/bin/env python3
"""Apply a floats-rollout proposal to the canonical seed JSON.

Consumes the JSON returned by the `spec-keybind-review` workflow in `mode:"floats"`
(the Author→…→Verify pipeline that proposes, per spec, a fixed core + per-band
float lists + eviction re-homes) and writes those changes into
`data/bellular-keybinds.seed.json` deterministically — so 33 specs are patched by
one auditable script, never by hand.

Per spec it:
  1. drops every existing `Rotational N` / `Cooldown N` / `Overflow N` key from
     `abilities` (the floating bands are being rebuilt),
  2. writes each `fixedCore` {bucket: ability} into `abilities`,
  3. writes each `outsideBandChanges` {bucket: ability} into `abilities`
     (eviction re-homes + non-band gap-fills — so nothing is silently unbound),
  4. sets the `floats` block (empty bands dropped; the generator ignores them too).

Everything OUTSIDE the three floating bands is left untouched unless an
`outsideBandChanges` entry names it. After applying, run
`python3 tool/gen_data_lua.py` to regenerate Data.lua.

Usage:
    python3 tool/apply_floats.py proposals.json            # apply all specs in the file
    python3 tool/apply_floats.py proposals.json --dry-run  # show the diff, write nothing
    python3 tool/apply_floats.py proposals.json --spec "Mage/Frost" --spec "Warrior/Fury"
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
SEED = PROJECT / "data" / "bellular-keybinds.seed.json"

BAND_KEY = re.compile(r"^(Rotational|Cooldown|Overflow) \d+$")
FLOAT_BANDS = ("Rotational", "Cooldown", "Overflow")

# Collapse a multi-line array of ONLY string literals back onto one line, so the
# floats lists read like the hand-authored Demonology block instead of exploding
# to one name per line. Conservative: only fires when every element is a string.
_SCALAR_ARRAY = re.compile(
    r'\[\n\s*("(?:[^"\\]|\\.)*"(?:,\n\s*"(?:[^"\\]|\\.)*")*)\n\s*\]')


def _inline_scalar_arrays(text: str) -> str:
    def collapse(m):
        items = re.split(r",\n\s*", m.group(1))
        return "[" + ", ".join(items) + "]"
    return _SCALAR_ARRAY.sub(collapse, text)


def _load_proposals(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    specs = data.get("specs") if isinstance(data, dict) else data
    if not isinstance(specs, list):
        sys.exit(f"{path}: expected a list of spec proposals (or {{specs:[...]}}).")
    return specs


def _valid_buckets(seed: dict) -> set[str]:
    return {b["category"] for b in seed["buckets"]}


def apply_one(spec_entry: dict, prop: dict, valid: set[str]) -> list[str]:
    """Mutate one seed spec's abilities+floats from a proposal. Returns a diff log."""
    ab = spec_entry["abilities"]
    log = []

    # 1) drop the old floating-band assignments
    for k in [k for k in ab if BAND_KEY.match(k)]:
        log.append(f"  - drop  {k}: {ab.pop(k)!r}")

    # 2+3) fixed core + eviction re-homes / gap-fills
    for item in prop.get("fixedCore", []):
        bucket, ability = item["bucket"], item["ability"]
        if not BAND_KEY.match(bucket):
            log.append(f"  ! SKIP fixedCore {bucket!r} — not a floating-band bucket")
            continue
        log.append(f"  + fixed {bucket}: {ability!r}")
        ab[bucket] = ability
    for item in prop.get("outsideBandChanges", []):
        bucket, ability = item["bucket"], item["ability"]
        if bucket not in valid:
            log.append(f"  ! SKIP outsideBandChange {bucket!r} — not a known bucket")
            continue
        if BAND_KEY.match(bucket):
            log.append(f"  ! SKIP outsideBandChange {bucket!r} — use fixedCore for band buckets")
            continue
        log.append(f"  ~ home  {bucket}: {ability!r}")
        ab[bucket] = ability

    # 4) floats block (drop empty bands)
    floats = {b: prop["floats"][b] for b in FLOAT_BANDS
              if prop.get("floats", {}).get(b)}
    if floats:
        spec_entry["floats"] = floats
        for b, names in floats.items():
            log.append(f"  = float {b}: {names}")
    elif "floats" in spec_entry:
        del spec_entry["floats"]
    return log


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("proposals", help="workflow floats-mode output JSON")
    ap.add_argument("--dry-run", action="store_true", help="print the diff, write nothing")
    ap.add_argument("--spec", action="append", default=[],
                    help="limit to these Class/Spec keys (repeatable)")
    args = ap.parse_args()

    seed = json.loads(SEED.read_text(encoding="utf-8"))
    by_key = {f"{s['class']}/{s['spec']}": s for s in seed["specs"]}
    valid = _valid_buckets(seed)
    props = _load_proposals(Path(args.proposals))

    only = set(args.spec)
    applied = 0
    for prop in props:
        key = f"{prop['class']}/{prop['spec']}"
        if only and key not in only:
            continue
        if prop.get("verdict") == "reject":
            print(f"\n{key}: verdict=reject — SKIPPED (fix upstream, re-run).")
            continue
        spec_entry = by_key.get(key)
        if not spec_entry:
            print(f"\n{key}: no such spec in the seed — SKIPPED.")
            continue
        print(f"\n{key}  (verdict={prop.get('verdict', '?')}, "
              f"confidence={prop.get('confidence', '?')}):")
        for line in apply_one(spec_entry, prop, valid):
            print(line)
        applied += 1

    if args.dry_run:
        print(f"\n[dry-run] {applied} spec(s) would change; seed NOT written.")
        return 0

    out = _inline_scalar_arrays(json.dumps(seed, indent=2, ensure_ascii=False)) + "\n"
    SEED.write_text(out, encoding="utf-8")
    print(f"\nwrote {SEED.relative_to(PROJECT)} — {applied} spec(s) patched.")
    print("next: python3 tool/gen_data_lua.py  &&  uv run python tool/check_seed_spells.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
