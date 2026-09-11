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
WAGO = REPO / "raw" / "wago"

# `Enum.CooldownViewerCategory`: the CDM sorts every row into a spell-ish or an aura-ish
# category, which is Blizzard's own ability/aura split and the only one that matters here —
# `aura()` reads through a CDM row, so an aura outside these categories can never answer.
AURA_CATEGORIES = {"2", "3", "6", "8"}  # TrackedBuff · TrackedBar · SpecAgnosticTracked · EquipSlotTracked
SPELL_CATEGORIES = {"0", "1", "5", "7"}  # Essential · Utility · SpecAgnosticEssential · EquipSlotEssential
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


def add_override_targets(table: dict) -> dict:
    """Name the spell a button TRANSFORMS into, inside the spec whose button it is.

    An override id is a real subject — a glow whose subject is Ruination attaches only while
    Ruination is what the row shows, which is how a transform window gets a rule of its own —
    but it has no acquisition row, so no inventory names it.

    `cooldown-manager.md` §2.9: an override effect carries aura **332** or **333**, names the
    BASE in `EffectMiscValue_0`, and carries the REPLACEMENT in `EffectBasePointsF`. So a base
    already in a spec's inventory says which spec the replacement belongs to. Holy Bulwark
    432459 → Sacred Weapon 432472 via `432478`, and the armament pair becomes nameable.

    ⚠ The MASK form is not walked. §2.9 says selection can also come from
    `EffectSpellClassMask` matched within the owning spell's `SpellClassSet`, and rows carry
    one form, both or neither — so this names the misc-form transforms and silently skips the
    rest rather than guessing at a match.
    """
    names, specs = table["names"], table["specs"]
    spell_names = {r["ID"]: r["Name_lang"] for r in _csv("SpellName")}
    owner_specs: dict[int, list[str]] = defaultdict(list)
    for key, ids in specs.items():
        for i in ids:
            owner_specs[i].append(key)

    added = 0
    for r in _csv("SpellEffect"):
        if r.get("EffectAura") not in ("332", "333"):
            continue
        base_raw, repl_raw = r.get("EffectMiscValue_0"), r.get("EffectBasePointsF", "")
        try:
            base, repl = int(base_raw), int(float(repl_raw))
        except (TypeError, ValueError):
            continue
        if repl <= 0 or base == repl or str(repl) not in spell_names:
            continue
        for key in owner_specs.get(base, ()):
            if repl in specs[key]:
                continue
            name = slug(spell_names[str(repl)])
            if repl in names and names[repl] != name:
                table["also"].setdefault(repl, name)
            else:
                names[repl] = name
            specs[key].append(repl)
            table.setdefault("_overrideTargets", defaultdict(set))[key].add(repl)
            added += 1

    for key in specs:
        specs[key] = sorted(set(specs[key]))
    table["overrideTargets"] = added
    return table


def resolve_collisions(table: dict) -> dict:
    """One slug, one id, inside a spec — and the winner is the id a rule can BIND to.

    Two ids sharing a name inside one spec is the norm, not the exception: every spec has
    some, because an override target is named after the spell it replaces. The resolver builds
    slug -> id by walking the spec's id list, so without this the last id written silently
    wins — a coin flip decided by sort order, and wrong wherever a base has two replacements
    (Vengeance's three Sigils of Flame, one per sigil talent).

    Rank by what a glow's subject has to be. A CooldownSetSpell row is a subject outright. An
    override target is a subject while its carrier is up, which is exactly the transform
    window a rule wants (Hammer of Wrath over Judgment). Anything else is in the acquisition
    inventory and has no row, so it can never attach and must never hold the name.

    Losers keep their global name — `Rules.Label` still renders them — and leave the spec's id
    list, which is the only thing the resolver walks.
    """
    names, specs = table["names"], table["specs"]
    cdm_rows = table.get("_cdmRows", {})
    over_targets = table.get("_overrideTargets", {})
    dropped = 0
    for key, ids in specs.items():
        rows, targets = cdm_rows.get(key, set()), over_targets.get(key, set())

        def rank(i: int) -> tuple[int, int]:
            if i in rows:
                return (0, i)
            if i in targets:
                return (1, i)
            return (2, i)

        by_slug: dict[str, list[int]] = defaultdict(list)
        for i in ids:
            if i in names:
                by_slug[names[i]].append(i)
        losers = set()
        for slug_, group in by_slug.items():
            if len(group) < 2:
                continue
            group.sort(key=rank)
            losers.update(group[1:])
        if losers:
            specs[key] = [i for i in ids if i not in losers]
            dropped += len(losers)
    table["collisionsResolved"] = dropped
    return table


def prefer_cdm_subjects(table: dict) -> dict:
    """Let the CDM's own spell rows win a name inside their spec.

    A glow's subject must be a row the Cooldown Manager laid out, so where the acquisition
    inventory and the CDM disagree about which id a name means, the CDM is right BY
    CONSTRUCTION — its id is the one a glow can attach to.

    They disagree in two shapes and both are the inventory's loss. It carries the BASE spell
    where a spec has its own (Vengeance's Metamorphosis, Outlaw's Sinister Strike), and it
    carries a component where the button is elsewhere: Consecration resolved to 81297, whose
    only effect row is `Effect=2` school damage, while the cast that creates the ground is
    26573.

    A superseded id keeps its global name — `Rules.Label` still renders it — but leaves the
    spec's id list, because the resolver builds slug -> id by walking that list and two ids
    sharing a slug there would let load order decide.
    """
    names, specs = table["names"], table["specs"]
    spell_names = {r["ID"]: r["Name_lang"] for r in _csv("SpellName")}
    spec_of = {r: k for r, k in table["_specOfSet"].items()}
    per_spec_slug: dict[str, dict[str, int]] = defaultdict(dict)
    for key, ids in specs.items():
        for i in ids:
            if i in names:
                per_spec_slug[key][names[i]] = i

    changed, added = 0, 0
    for r in _csv("CooldownSetSpell"):
        key = spec_of.get(r["CooldownSetID"])
        if key is None or r["Category"] not in SPELL_CATEGORIES:
            continue
        raw = spell_names.get(r["SpellID"])
        if not raw:
            continue
        name, cdm_id = slug(raw), int(r["SpellID"])
        # Recorded BEFORE the agreement check: a row the inventory already had right is still
        # a row, and the collision pass ranks by exactly that.
        table.setdefault("_cdmRows", defaultdict(set))[key].add(cdm_id)
        held = per_spec_slug[key].get(name)
        if held == cdm_id:
            continue
        if held is not None:
            specs[key] = [i for i in specs[key] if i != held]
            changed += 1
        else:
            added += 1
        # NEVER overwrite a name the inventory gave: 432459 is `holy_armaments` there and
        # "Holy Bulwark" in SpellName, and clobbering it lost the name a rule was written
        # against. A second name for one id is what `alsoNamed` is for, and the resolver
        # indexes both.
        if cdm_id in names and names[cdm_id] != name:
            table["also"].setdefault(cdm_id, name)
        else:
            names[cdm_id] = name
        if cdm_id not in specs[key]:
            specs[key].append(cdm_id)
        per_spec_slug[key][name] = cdm_id

    for key in specs:
        specs[key] = sorted(set(specs[key]))
    table["cdmPreferred"] = {"changed": changed, "added": added}
    return table


def _csv(stem: str) -> list[dict]:
    """The newest build of a cached DB2, or the unversioned file when that is all there is."""
    versioned = sorted(WAGO.glob(f"{stem}-*.csv"))
    path = versioned[-1] if versioned else WAGO / f"{stem}.csv"
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def auras(rows: list[dict]) -> dict:
    """The aura namespace: slug -> the CDM ROW it names, per spec.

    An `aura()` term needs a different table from `ready()` — the ability inventory lists what
    a spec can LEARN, and an aura is applied rather than learned. Where a name exists in both
    worlds the ability table answers, silently and wrongly: `aura(consecration)` used to
    resolve to the periodic damage tick inside the field.

    **The ROW is the unit, not the spell id.** A tracked row carries its own spell plus any
    `CooldownSetLinkedSpell` ids, every one of which identifies that row to the latch — so
    Shining Light's 321136 and 327510 are one name for one thing, not a collision. Union the
    names, key by the row.

    The canonical id prefers one that is UNIQUE to the aura row: Shield of the Righteous sits
    in an Essential category as 53600 and in a tracked category as 53600 + 132403, and picking
    53600 there would name a row that is not the aura's.

    A slug naming two different ROWS is genuinely ambiguous (32 of 1800 repo-wide) and is left
    OUT, so the parser refuses it and names the candidates instead of guessing.
    """
    spec_of = {r["spec_id"]: f"{slug(r['class'])}.{slug(r['spec'])}" for r in rows}
    names = {r["ID"]: r["Name_lang"] for r in _csv("SpellName")}
    sets = {r["ID"]: spec_of.get(r["ChrSpecialization"]) for r in _csv("CooldownSet")}
    linked: dict[str, list[str]] = defaultdict(list)
    for r in _csv("CooldownSetLinkedSpell"):
        linked[r["CooldownSetSpellID"]].append(r["SpellID"])

    set_rows = _csv("CooldownSetSpell")
    # Ids that also appear in a SPELL category of the same set, so a canonical pick can avoid
    # naming the ability row when the aura row shares its spell.
    ability_ids: dict[str, set[str]] = defaultdict(set)
    for r in set_rows:
        if r["Category"] not in AURA_CATEGORIES:
            ability_ids[r["CooldownSetID"]].add(r["SpellID"])

    per: dict[str, dict[str, set[int]]] = defaultdict(lambda: defaultdict(set))
    for r in set_rows:
        key = sets.get(r["CooldownSetID"])
        if key is None or r["Category"] not in AURA_CATEGORIES:
            continue
        ids = [r["SpellID"]] + linked.get(r["ID"], [])
        # The canonical id is per SLUG, not per row: a row's ids can carry different names —
        # Consecration's tracked row is spell 137028 "Protection Paladin" with 188370
        # "Consecration" linked — and a suffix built from an id that does not match the name
        # it is suffixing tells the reader nothing. Prefer an id the slug actually names.
        for name_slug in {slug(n) for n in (names.get(i) for i in ids) if n}:
            matching = [i for i in ids if names.get(i) and slug(names[i]) == name_slug]
            unique = [i for i in matching if i not in ability_ids[r["CooldownSetID"]]]
            pool = unique or matching
            canonical = int(r["SpellID"]) if r["SpellID"] in pool else int(sorted(pool)[0])
            per[key][name_slug].add(canonical)

    out_names: dict[int, str] = {}
    out_specs: dict[str, list[int]] = {}
    ambiguous: dict[str, dict[str, list[int]]] = {}
    for key, by_slug in sorted(per.items()):
        ids: set[int] = set()
        for name, rows_named in sorted(by_slug.items()):
            # A slug on two rows becomes two names, each suffixed with the id it resolves to.
            # The bare slug stays OUT, so writing it refuses and names both — but neither row
            # is left unnameable, and `<name>_<id>` tells a reader which spell it is where a
            # bare id told them nothing. The suffix is stable because ids are.
            if len(rows_named) > 1:
                ambiguous.setdefault(key, {})[name] = sorted(rows_named)
                for one in rows_named:
                    out_names[one] = f"{name}_{one}"
                    ids.add(one)
                continue
            (only,) = tuple(rows_named)
            out_names[only] = name
            ids.add(only)
        out_specs[key] = sorted(ids)
    # The client knows a spec by its numeric id, so a login-time check of this table against
    # the live category sets needs the mapping to get from one to the other.
    spec_ids = {int(sid): key for sid, key in sorted(spec_of.items()) if sid.isdigit()}
    return {
        "_specOfSet": sets,
        "auraNames": dict(sorted(out_names.items())),
        "auraSpecs": out_specs,
        "auraAmbiguous": ambiguous,
        "specIDs": spec_ids,
        "auraCategories": sorted(int(c) for c in AURA_CATEGORIES),
    }


_LOADED: dict | None = None


def load() -> dict:
    """The same table the addon ships, for the Python side of the rule tool. Cached."""
    global _LOADED
    if _LOADED is None:
        with ABILITIES.open(encoding="utf-8", newline="") as fh:
            rows = list(csv.DictReader(fh, delimiter="\t"))
        _LOADED = build(rows)
        _LOADED.update(auras(rows))
        prefer_cdm_subjects(_LOADED)
        add_override_targets(_LOADED)
        resolve_collisions(_LOADED)
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
        "Symbols.auraCount = %d" % len(table["auraNames"]),
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
        "--- id -> the slug an `aura()` term names it by. A DIFFERENT namespace from `names`:",
        "--- the ability inventory lists what a spec can learn and an aura is applied, not",
        "--- learned, so a name that exists in both worlds must not resolve to the ability.",
        "--- Generated from the CDM's own tracked categories, which is exactly the set of auras",
        "--- an `aura()` term can ever read -- one outside them has no row to latch.",
        "Symbols.auraNames = {",
    ]
    out += ["  [%d] = %s," % (i, _lua_str(n)) for i, n in table["auraNames"].items()]
    out += [
        "}",
        "",
        '--- "<class>.<spec>" -> the aura ids that spec can track.',
        "Symbols.auraSpecs = {",
    ]
    for key, ids in table["auraSpecs"].items():
        out.append("  [%s] = {" % _lua_str(key))
        for start in range(0, len(ids), IDS_PER_LINE):
            out.append("    " + " ".join("%d," % i for i in ids[start:start + IDS_PER_LINE]))
        out.append("  },")
    out += [
        "}",
        "",
        "--- Slugs naming two different tracked ROWS. Left out of `auraNames` on purpose, and",
        "--- carried here so the refusal can say which ids were meant instead of guessing.",
        "Symbols.auraAmbiguous = {",
    ]
    for key, by_slug in sorted(table["auraAmbiguous"].items()):
        out.append("  [%s] = {" % _lua_str(key))
        for name, ids in sorted(by_slug.items()):
            out.append("    [%s] = { %s }," % (_lua_str(name), " ".join("%d," % i for i in ids)))
        out.append("  },")
    out += [
        "}",
        "",
        "--- Spec id -> the key the tables above use. The client names a spec by number, so",
        "--- checking the aura table against the live category sets needs this to join them.",
        "Symbols.specIDs = {",
    ]
    out += ["  [%d] = %s," % (i, _lua_str(k)) for i, k in table["specIDs"].items()]
    out += [
        "}",
        "",
        "--- The `Enum.CooldownViewerCategory` values the aura table was built from, so the",
        "--- in-client check reads the same categories the generator did.",
        "Symbols.auraCategories = { %s }" % " ".join("%d," % c for c in table["auraCategories"]),
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
    table.update(auras(rows))
    prefer_cdm_subjects(table)
    add_override_targets(table)
    resolve_collisions(table)
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
