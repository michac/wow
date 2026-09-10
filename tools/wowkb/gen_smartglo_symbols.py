"""Generate Smart Glo's spell-name symbol table from the KB's ability inventory.

A rule reads `on summon_demonic_tyrant`, not `on 265187`. The addon needs the same
mapping the Python tool has, because rules are now authored in-game as well as on disk
(the config box takes plain text, not only an `SG1:` blob) — so the table is generated
once, here, into the addon source.

    uv run python -m wowkb.gen_smartglo_symbols            # write the addon file
    uv run python -m wowkb.gen_smartglo_symbols --check    # exit 1 if out of date
    uv run python -m wowkb.gen_smartglo_symbols --print    # stdout, don't write

**The slug is the KB's spell name, mechanically lowercased.** It is not a curated alias
list and must never become one: `all-abilities.tsv`'s `aliases` column is empty on all but
three rows repo-wide, so short names like `tyrant` would have to be hand-maintained, and a
hand-maintained name table drifts silently against a patch. Slugified full names happen to
match simc's own action names, which is what lets a rule read as a near-transcription of
the APL line it came from.

**Scoping.** Names collide across specs (101 slugs repo-wide name more than one spell) and
never within one (zero collisions in all 40 specs), so a spec is the scope that makes a
bare name unambiguous. `Symbols.specAlias` carries the bare spec words that name exactly
one spec — `demonology` does, `frost` does not.

⚠ The CLIENT is Tier 1 for `id -> name`, not this table. `/sg symbols` compares every row
against `C_Spell.GetSpellName` in the live client, which is how a patch rename or a KB
drift is caught with no flight.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ABILITIES = REPO / "knowledge" / "classes" / "_abilities" / "all-abilities.tsv"
TALENTS = sorted((REPO / "knowledge" / "classes").glob("*/*/talents.json"))
OUT_LUA = REPO / "projects" / "smart-glo" / "addon" / "SmartGlo" / "Symbols.lua"

IDS_PER_LINE = 8


def slug(name: str) -> str:
    """A spell name as a rule writes it: lowercase, apostrophes dropped, runs joined by _."""
    s = name.lower().replace("'", "").replace("’", "")
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def _lua_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def build(rows: list[dict]) -> dict:
    """names: id -> slug · also: id -> the second slug the KB gives it · specs · aliases."""
    names: dict[int, str] = {}
    also: dict[int, str] = {}
    specs: dict[str, list[int]] = defaultdict(list)
    seen: dict[str, set[int]] = defaultdict(set)

    for row in rows:
        spell_id = int(row["spell_id"])
        name = slug(row["name"])
        key = f"{slug(row['class'])}.{slug(row['spec'])}"

        first = names.setdefault(spell_id, name)
        # Two ids in the whole inventory carry two different names (a talent and the
        # ability it grants share an id). Record the second rather than picking a winner:
        # the in-game check accepts either, because either is what the client may return.
        if first != name and also.get(spell_id) != name:
            also[spell_id] = name

        if spell_id not in seen[key]:
            seen[key].add(spell_id)
            specs[key].append(spell_id)

    # A bare spec word is usable only when it names exactly one spec — `demonology` does,
    # `frost` names two. An ambiguous one is simply absent, so the parser refuses it.
    by_word: dict[str, list[str]] = defaultdict(list)
    for key in specs:
        by_word[key.split(".", 1)[1]].append(key)
    alias = {word: keys[0] for word, keys in by_word.items() if len(keys) == 1}

    return {
        "talents": talents(),
        "names": dict(sorted(names.items())),
        "also": dict(sorted(also.items())),
        "specs": {k: sorted(v) for k, v in sorted(specs.items())},
        "alias": dict(sorted(alias.items())),
    }


def talents() -> dict:
    """spell_id -> the (node, entry) pairs that grant it, flattened.

    `talent()` reads the TRAIT CONFIG rather than the spell book: `IsSpellKnown` answers about
    a spell, not about a node, and it stands in for the talent rather than being it — a spell
    known from another source diverges from the talent silently, and a silent `false` under a
    `not` reads as a confident true.

    56 spells name a different node in different specs, so the value is a FLAT LIST of pairs
    rather than one pair. The addon does not know which spec's mapping applies — it does not
    need to: a node outside the player's own tree refuses, so trying each candidate and taking
    the first that answers lets the client arbitrate instead of the table guessing.
    """
    out: dict[int, list[int]] = {}
    seen: dict[int, set] = defaultdict(set)
    for path in TALENTS:
        tree = json.loads(path.read_text(encoding="utf-8")).get("trees", {})
        for group in ("class", "spec", "hero"):
            branch = tree.get(group) or []
            # `hero` is keyed by hero-tree name; `class` and `spec` are bare lists. Iterating
            # the dict would walk its KEYS, which is how every hero talent went missing.
            groups = branch.values() if isinstance(branch, dict) else [branch]
            for node in [n for sub in groups for n in sub]:
                if not isinstance(node, dict):
                    continue
                node_id = node.get("node_id")
                if not isinstance(node_id, int):
                    continue
                for entry in node.get("entries", []):
                    spell_id = entry.get("spell_id")
                    if not isinstance(spell_id, int):
                        continue
                    # A blank entry id (18 of 3,858 rows) means the mapping cannot name WHICH
                    # half of a choice node this is. 0 records that, and the addon reads it as
                    # "ranks are enough" rather than pretending to an entry check it cannot do.
                    try:
                        entry_id = int(entry.get("entry_id") or 0)
                    except (TypeError, ValueError):
                        entry_id = 0
                    pair = (node_id, entry_id)
                    if pair in seen[spell_id]:
                        continue
                    seen[spell_id].add(pair)
                    out.setdefault(spell_id, []).extend(pair)
    return dict(sorted(out.items()))


_LOADED: dict | None = None


def load() -> dict:
    """The same table the addon ships, for the Python side of the rule tool. Cached."""
    global _LOADED
    if _LOADED is None:
        with ABILITIES.open(encoding="utf-8", newline="") as fh:
            _LOADED = build(list(csv.DictReader(fh, delimiter="\t")))
    return _LOADED


def render(table: dict) -> str:
    names, also, specs, alias = table["names"], table["also"], table["specs"], table["alias"]
    nodes = table["talents"]
    out = [
        "-- AUTO-GENERATED — do NOT hand-edit.",
        "-- Source: knowledge/classes/_abilities/all-abilities.tsv",
        "-- Writer: `uv run python -m wowkb.gen_smartglo_symbols`",
        "--",
        "-- The name a rule writes for a spell, and the ids each spec's inventory carries.",
        "-- Names collide ACROSS specs and never within one, so a spec is the scope that makes",
        "-- a bare name unambiguous; `Names.lua` does the resolving and `/sg symbols` checks",
        "-- every row here against the live client, which is Tier 1 for id -> name.",
        "",
        "local _, ns = ...",
        "",
        "local Symbols = {}",
        "ns.Symbols = Symbols",
        "",
        "--- The stamp `/sg symbols` reports. Deliberately a COUNT and not a date: a date would",
        "--- churn `--check` on a regeneration that changed nothing.",
        "Symbols.source = \"knowledge/classes/_abilities/all-abilities.tsv\"",
        "Symbols.count = %d" % len(names),
        "Symbols.specCount = %d" % len(specs),
        "Symbols.talentCount = %d" % len(nodes),
        "",
        "--- id -> the slug the KB names it by.",
        "Symbols.names = {",
    ]
    out += ["  [%d] = %s," % (i, _lua_str(n)) for i, n in names.items()]
    out += [
        "}",
        "",
        "--- The ids the inventory names twice. `/sg symbols` accepts either name for these.",
        "Symbols.alsoNamed = {",
    ]
    out += ["  [%d] = %s," % (i, _lua_str(n)) for i, n in also.items()]
    out += [
        "}",
        "",
        '--- "<class>.<spec>" -> the ids in that spec\'s inventory; names come back via `names`.',
        "Symbols.specs = {",
    ]
    for key, ids in specs.items():
        out.append("  [%s] = {" % _lua_str(key))
        for start in range(0, len(ids), IDS_PER_LINE):
            out.append("    " + " ".join("%d," % i for i in ids[start:start + IDS_PER_LINE]))
        out.append("  },")
    out += [
        "}",
        "",
        "--- Bare spec words that name exactly one spec. An ambiguous word is absent on purpose.",
        "Symbols.specAlias = {",
    ]
    out += ["  [%s] = %s," % (_lua_str(w), _lua_str(k)) for w, k in alias.items()]
    out += [
        "}",
        "",
        "--- A talent spell -> the {node, entry} pairs that grant it, FLATTENED into one list.",
        "--- `talent()` reads the trait config, so it needs a node; a spell that names a",
        "--- different node in another spec carries both, and the client arbitrates by refusing",
        "--- the node that is not in the player's own tree. Entry 0 = the source did not record",
        "--- which half of a choice node this is, so ranks alone decide.",
        "Symbols.talentNodes = {",
    ]
    for spell_id, flat in nodes.items():
        out.append("  [%d] = { %s }," % (spell_id, " ".join("%d," % v for v in flat)))
    out += ["}", ""]
    return "\n".join(out)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="wowkb.gen_smartglo_symbols", description=__doc__,
                               formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--check", action="store_true",
                   help="exit 1 if the on-disk file differs (pre-release guard)")
    p.add_argument("--print", dest="to_stdout", action="store_true",
                   help="write to stdout instead of the addon file")
    args = p.parse_args(argv)

    with ABILITIES.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    table = build(rows)
    content = render(table)
    n, s = len(table["names"]), len(table["specs"])

    if args.to_stdout:
        sys.stdout.write(content)
        return 0
    if args.check:
        current = OUT_LUA.read_text(encoding="utf-8") if OUT_LUA.exists() else ""
        if current != content:
            print(f"OUT OF DATE: {OUT_LUA} — re-run `python -m wowkb.gen_smartglo_symbols`")
            return 1
        print(f"up to date ({n} spells across {s} specs)")
        return 0

    OUT_LUA.parent.mkdir(parents=True, exist_ok=True)
    OUT_LUA.write_text(content, encoding="utf-8")
    print(f"wrote {OUT_LUA.relative_to(REPO)} — {n} spells across {s} specs, "
          f"{len(table['alias'])} unambiguous spec words, {len(table['also'])} double-named ids, "
          f"{len(table['talents'])} talent spells mapped to trait nodes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
