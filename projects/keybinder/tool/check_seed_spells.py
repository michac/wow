#!/usr/bin/env python3
"""Advisory seed spell-name validator (build-time typo / rename catcher).

Cross-references every distinct ability *name* in the seed against a wago
`SpellName` DB2 dump, and reports names that don't match any 12.0.x spell —
catching seed typos and Midnight renames before they ship as silent "unresolved"
gaps in the in-game dump.

The addon resolves names → spell IDs at runtime from the player's own spellbook
(no IDs are baked into `Data.lua`), so this check is purely advisory: it exits 0
even when it finds misses. Treat a miss as "verify this name in-game / add an
alias", not a hard failure — some names are talent-gated or intentionally
placeholder.

Get the reference dump first (from the wowkb `tools/` project):

    cd tools && uv run python -m wowkb.wago SpellName
    # → raw/wago/SpellName.csv  (columns: ID, Name_lang)

Usage:
    uv run python tool/check_seed_spells.py [path/to/SpellName.csv]

stdlib-only.
"""
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent                       # projects/keybinder
WORKSPACE = PROJECT.parents[1]              # wwt-keyboard repo root
SEED = PROJECT / "data" / "bellular-keybinds.seed.json"

# Placeholder ability values the seed uses for non-spell buckets (mirrors
# PLACEHOLDER in Dump.lua). These are macro/summon targets, not spells — never
# flag them.
PLACEHOLDER = {
    "Mount", "Free", "Racial Ability",
    "Healthstone/Potion Macro", "Drinking/Mana Potion Macro",
    "Damage Potion", "Another Combat Item If Needed", "Trinket Macro",
}


def find_dump(argv_path):
    """Locate the SpellName CSV: explicit arg, else newest match in raw/wago/."""
    if argv_path:
        p = Path(argv_path)
        return p if p.exists() else None
    wago = WORKSPACE / "raw" / "wago"
    cands = sorted(wago.glob("SpellName*.csv")) if wago.is_dir() else []
    return cands[-1] if cands else None


def load_spell_names(csv_path):
    """Set of lowercased spell names from the DB2 dump (any *Name* column)."""
    names = set()
    with csv_path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        name_cols = [c for c in (reader.fieldnames or []) if "name" in c.lower()]
        if not name_cols:
            sys.exit(f"no name column in {csv_path} (headers: {reader.fieldnames})")
        for row in reader:
            for col in name_cols:
                val = (row.get(col) or "").strip()
                if val:
                    names.add(val.lower())
    return names


def seed_ability_names():
    """Distinct real ability names in the seed, split on '/' for dual entries.

    Placeholder labels are excluded; "Thunder Clap/Rend"-style dual buckets are
    split so each half is checked ("Avatar/Bladestorm" → Avatar, Bladestorm).
    Returns {name: [seedKeys...]} for reporting where a miss lives.
    """
    data = json.loads(SEED.read_text(encoding="utf-8"))
    out = {}
    for spec in data["specs"]:
        key = f"{spec['class']}/{spec['spec']}"
        for ability in spec["abilities"].values():
            if ability in PLACEHOLDER:
                continue
            for part in ability.split("/"):
                part = part.strip()
                if part and part not in PLACEHOLDER:
                    out.setdefault(part, [])
                    if key not in out[part]:
                        out[part].append(key)
    return out


def main():
    csv_path = find_dump(sys.argv[1] if len(sys.argv) > 1 else None)
    if not csv_path:
        print("SpellName dump not found. Fetch it first:")
        print("    cd tools && uv run python -m wowkb.wago SpellName")
        print("then re-run (or pass the CSV path as an argument). Skipping.")
        return  # advisory: not a failure

    known = load_spell_names(csv_path)
    names = seed_ability_names()
    misses = sorted(n for n in names if n.lower() not in known)

    print(f"seed: {len(names)} distinct ability names")
    print(f"ref : {len(known)} spell names from {csv_path.name}")
    if not misses:
        print("OK — every seed ability name matches a 12.0.x spell.")
        return
    print(f"\n{len(misses)} name(s) with no exact SpellName match "
          "(verify in-game / add an alias / fix the seed):")
    for n in misses:
        specs = names[n]
        shown = ", ".join(specs[:4]) + (" …" if len(specs) > 4 else "")
        print(f"  - {n}   [{shown}]")


if __name__ == "__main__":
    main()
