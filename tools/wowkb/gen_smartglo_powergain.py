"""Generate the Tier-1 power-gain table: how much of a secondary resource a cast returns.

Two artifacts, and the split is what makes the check gate work in a fresh clone:

    uv run python -m wowkb.gen_smartglo_powergain --refresh   # DB2 -> the KB tsv (+ the Lua)
    uv run python -m wowkb.gen_smartglo_powergain             # the KB tsv -> the Lua
    uv run python -m wowkb.gen_smartglo_powergain --check     # exit 1 if the Lua is stale
    uv run python -m wowkb.gen_smartglo_powergain --print     # stdout, don't write

`--refresh` needs `raw/wago/`, which is gitignored; everything else reads the committed tsv.

**Where the number comes from.** `SpellEffect.db2` rows with `Effect = 30` (ENERGIZE) or `31`
(ENERGIZE_PCT) carry the power type in `EffectMiscValue_0` and the amount in
`EffectBasePointsF`, in RAW units — 10 raw per Soul Shard, which `SpellPower.db2` confirms
independently (Hand of Gul'dan `ManaCost 30, PowerType 7` for a three-shard spell). The addon
never ships that scale: `UnitPowerDisplayMod` reads it from the client.

⚠ **The energize lives on a DIFFERENT spell id than the cast**, and nothing in DB2 links the
two — 686 Shadow Bolt does not name 194192 Shadow Bolt through `EffectTriggerSpell`, and no
walk reaches it. They share only a NAME, so the join here is name equality against the KB's
ability inventory, narrowed to classes that own the power in question. That is the weakest hop
in the chain and it is why the `varies` column exists.

⚠ **`varies` is the whole reason this table can be trusted for some resources and not others.**
When one name carries several distinct energize amounts the gain is talent- or proc-dependent
and no single number is correct: Wake of Ashes is 1, 3 or 5 Holy Power, Ambush 1, 2 or 3 Combo
Points. Those rows are emitted with an EMPTY `fragments` and `varies = 1` so a consumer refuses
rather than guessing. Soul Shards carry exactly one — Shadowburn's kill refund, which is
Destruction and instant — and none of the hard casts that generate them, which is the measured
basis for Smart Glo allowing a projected threshold on shards and on nothing else.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
WAGO = REPO / "raw" / "wago"
ABILITIES = REPO / "knowledge" / "classes" / "_abilities" / "all-abilities.tsv"
OUT_TSV = REPO / "knowledge" / "classes" / "_abilities" / "power-gain.tsv"
OUT_LUA = REPO / "projects" / "smart-glo" / "addon" / "SmartGlo" / "PowerGain.lua"

COLUMNS = ["power_type", "power", "spell_id", "name", "class", "fragments", "varies",
           "energize_ids"]

# The seven secondaries a rule may name, and the classes that own each. A name match is
# accepted only inside its own power's classes, so a paladin spell cannot inherit a warlock
# energize just because the two share a word.
POWERS = {
    4: ("combo_points", {"rogue", "druid"}),
    5: ("runes", {"death_knight"}),
    7: ("soul_shards", {"warlock"}),
    9: ("holy_power", {"paladin"}),
    12: ("chi", {"monk"}),
    16: ("arcane_charges", {"mage"}),
    19: ("essence", {"evoker"}),
}

ENERGIZE_EFFECTS = {"30", "31"}


def slug(name: str) -> str:
    s = name.lower().replace("'", "").replace("’", "")
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def _wago(table: str) -> list[dict]:
    path = WAGO / f"{table}.csv"
    if not path.exists():
        raise SystemExit(f"missing {path.relative_to(REPO)} — "
                         f"run `uv run python -m wowkb.wago {table}` first")
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def energizes() -> dict[tuple[int, str], dict]:
    """(power_type, name slug) -> {amounts: set[int], ids: set[int]} from SpellEffect."""
    names = {r["ID"]: r["Name_lang"] for r in _wago("SpellName")}
    out: dict[tuple[int, str], dict] = defaultdict(lambda: {"amounts": set(), "ids": set()})
    for row in _wago("SpellEffect"):
        if row["Effect"] not in ENERGIZE_EFFECTS:
            continue
        try:
            power = int(row["EffectMiscValue_0"])
            amount = float(row["EffectBasePointsF"])
        except (TypeError, ValueError):
            continue
        # A zero row is a scripted energize whose amount lives in spell script, not in DB2.
        # It says "this spell touches the power" and nothing about how much, so it is not a
        # number and must not become one.
        if power not in POWERS or amount <= 0:
            continue
        name = slug(names.get(row["SpellID"], ""))
        if not name:
            continue
        entry = out[(power, name)]
        entry["amounts"].add(int(amount))
        entry["ids"].add(int(row["SpellID"]))
    return out


def refresh() -> list[dict]:
    """Join the energize rows onto the KB's ability inventory by name, within the power's classes."""
    table = energizes()
    with ABILITIES.open(encoding="utf-8", newline="") as fh:
        inventory = list(csv.DictReader(fh, delimiter="\t"))

    rows: dict[tuple[int, int], dict] = {}
    for row in inventory:
        cls = slug(row["class"])
        name = slug(row["name"])
        spell_id = int(row["spell_id"])
        for power, (token, classes) in POWERS.items():
            if cls not in classes:
                continue
            entry = table.get((power, name))
            if entry is None:
                continue
            amounts = sorted(entry["amounts"])
            rows[(power, spell_id)] = {
                "power_type": power,
                "power": token,
                "spell_id": spell_id,
                "name": name,
                "class": cls,
                "fragments": "" if len(amounts) > 1 else amounts[0],
                "varies": 1 if len(amounts) > 1 else 0,
                "energize_ids": " ".join(str(i) for i in sorted(entry["ids"])),
            }
    return [rows[k] for k in sorted(rows)]


def read_tsv() -> list[dict]:
    if not OUT_TSV.exists():
        raise SystemExit(f"missing {OUT_TSV.relative_to(REPO)} — re-run with --refresh")
    with OUT_TSV.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def write_tsv(rows: list[dict]) -> None:
    lines = ["\t".join(COLUMNS)]
    lines += ["\t".join(str(r[c]) for c in COLUMNS) for r in rows]
    OUT_TSV.write_text("\n".join(lines) + "\n", encoding="utf-8")


def render(rows: list[dict]) -> str:
    by_power: dict[int, list[dict]] = defaultdict(list)
    for row in rows:
        by_power[int(row["power_type"])].append(row)

    out = [
        "-- AUTO-GENERATED — do NOT hand-edit.",
        "-- Source: knowledge/classes/_abilities/power-gain.tsv",
        "-- Writer: `uv run python -m wowkb.gen_smartglo_powergain`",
        "--",
        "-- How much of a secondary resource a cast returns, in RAW units — 10 raw per Soul",
        "-- Shard. The scale is not shipped: `UnitPowerDisplayMod` reads it from the client.",
        "--",
        "-- A spell in `varies` returns an amount that depends on a talent or a proc, so no",
        "-- single number is right and `Cast.lua` refuses to project one rather than pick.",
        "",
        "local _, ns = ...",
        "",
        "local PowerGain = {}",
        "ns.PowerGain = PowerGain",
        "",
        "--- A COUNT, not a date: a date would churn `--check` on a regeneration that changed",
        "--- nothing.",
        "PowerGain.count = %d" % len(rows),
        "",
        "--- [powerType] = { [castSpellID] = raw units returned }.",
        "PowerGain.raw = {",
    ]
    for power in sorted(by_power):
        token = POWERS[power][0]
        out.append("  [%d] = { -- %s" % (power, token))
        for row in by_power[power]:
            if row["varies"] in ("1", 1):
                continue
            out.append("    [%s] = %s, -- %s" % (row["spell_id"], row["fragments"], row["name"]))
        out.append("  },")
    out += [
        "}",
        "",
        "--- [powerType] = { [castSpellID] = true } for the spells whose gain is not a number.",
        "PowerGain.varies = {",
    ]
    for power in sorted(by_power):
        varying = [r for r in by_power[power] if r["varies"] in ("1", 1)]
        if not varying:
            continue
        out.append("  [%d] = { -- %s" % (power, POWERS[power][0]))
        for row in varying:
            out.append("    [%s] = true, -- %s" % (row["spell_id"], row["name"]))
        out.append("  },")
    out += ["}", ""]
    return "\n".join(out)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="wowkb.gen_smartglo_powergain", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--refresh", action="store_true",
                   help="re-derive the KB tsv from raw/wago DB2 (needs the fetch cache)")
    p.add_argument("--check", action="store_true",
                   help="exit 1 if the addon file differs from the KB tsv")
    p.add_argument("--print", dest="to_stdout", action="store_true",
                   help="write the addon file to stdout instead of to disk")
    args = p.parse_args(argv)

    if args.refresh:
        rows = refresh()
        write_tsv(rows)
        print(f"wrote {OUT_TSV.relative_to(REPO)} — {len(rows)} rows")
    rows = read_tsv()
    content = render(rows)
    varying = sum(1 for r in rows if r["varies"] in ("1", 1))

    if args.to_stdout:
        sys.stdout.write(content)
        return 0
    if args.check:
        current = OUT_LUA.read_text(encoding="utf-8") if OUT_LUA.exists() else ""
        if current != content:
            print(f"OUT OF DATE: {OUT_LUA} — "
                  f"re-run `python -m wowkb.gen_smartglo_powergain`")
            return 1
        print(f"up to date ({len(rows)} rows, {varying} varying)")
        return 0

    OUT_LUA.write_text(content, encoding="utf-8")
    print(f"wrote {OUT_LUA.relative_to(REPO)} — {len(rows)} rows, {varying} varying")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
