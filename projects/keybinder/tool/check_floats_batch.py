#!/usr/bin/env python3
"""Pre-apply sanity check for a floats-rollout batch proposal.

Reads the workflow's `result.specs` JSON (a list of per-spec proposals) and
flags anything apply_floats.py would faithfully write but shouldn't:

  * dup: an ability appearing in BOTH fixedCore and any floats band
    (would be pinned AND floated — contradictory).
  * over-capacity fixedCore: more fixed abilities in a band than it has slots
    (Rotational 8, Cooldown 4, Overflow 6). Float overflow is fine — the addon
    spills — but a fixedCore that exceeds the band is a real error.
  * fixedCore bucket that isn't a floating-band bucket.

Exit non-zero if any hard error is found. Usage:
    python3 tool/check_floats_batch.py batchN.json
"""
import json
import re
import sys
from pathlib import Path

BAND_KEY = re.compile(r"^(Rotational|Cooldown|Overflow) \d+$")
CAP = {"Rotational": 8, "Cooldown": 4, "Overflow": 6}


def main() -> int:
    if len(sys.argv) != 2:
        sys.exit("usage: check_floats_batch.py batchN.json")
    specs = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    if isinstance(specs, dict):
        specs = specs.get("specs", specs)

    errors = 0
    for prop in specs:
        key = f"{prop.get('class')}/{prop.get('spec')}"
        verdict = prop.get("verdict", "?")
        conf = prop.get("confidence", "?")
        fixed = prop.get("fixedCore", []) or []
        floats = prop.get("floats", {}) or {}
        gaps = prop.get("inventoryGaps", []) or []

        fixed_names = {i["ability"] for i in fixed}
        float_names = {n for band in floats.values() for n in (band or [])}

        # dup: fixed AND floated
        dups = fixed_names & float_names
        # per-band fixedCore capacity
        band_counts = {}
        bad_bucket = []
        for i in fixed:
            b = i["bucket"]
            m = BAND_KEY.match(b)
            if not m:
                bad_bucket.append(b)
                continue
            band = m.group(1)
            band_counts[band] = band_counts.get(band, 0) + 1
        over = {b: c for b, c in band_counts.items() if c > CAP[b]}

        flag = "OK "
        if verdict == "reject":
            flag = "REJ"
        elif dups or over or bad_bucket:
            flag = "ERR"
            errors += 1
        fc = {b: band_counts.get(b, 0) for b in CAP}
        flc = {b: len(floats.get(b, []) or []) for b in CAP}
        print(f"[{flag}] {key}  v={verdict} c={conf}  "
              f"fixed(R{fc['Rotational']}/C{fc['Cooldown']}/O{fc['Overflow']}) "
              f"float(R{flc['Rotational']}/C{flc['Cooldown']}/O{flc['Overflow']})"
              + (f"  gaps={gaps}" if gaps else ""))
        if dups:
            print(f"       DUP fixed&float: {sorted(dups)}")
        if over:
            print(f"       OVER-CAP fixedCore: {over}")
        if bad_bucket:
            print(f"       NON-BAND fixedCore bucket: {bad_bucket}")

    print(f"\n{errors} spec(s) with hard errors.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
