"""Generate the per-spec ability inventory as a Tier-1 KB artifact.

This is the *writer* for `knowledge/classes/<class>/<spec>/ability-inventory.tsv`
+ `.md` and the aggregate `knowledge/classes/_abilities/`. It extends — it does
not replace — `wowkb.spec_inventory`, which stays the actives-only union the
BucketBinds floats work and `wowkb.cdmp` read.

    uv run python -m wowkb.gen_abilities --fetched 2026-08-06
    uv run python -m wowkb.gen_abilities --fetched 2026-08-06 --check
    uv run python -m wowkb.gen_abilities --fetched 2026-08-06 --residual

⚠ `abilities.md` in each spec directory is HAND-WRITTEN PROSE. This module never
writes it. The generated file is `ability-inventory.md`.

────────────────────────────────────────────────────────────────────────────────
BUILD PINNING
────────────────────────────────────────────────────────────────────────────────
Every DB2 read goes through `spec_inventory._rows`, which resolves
`raw/wago/<Table>-12.0.7.67808.csv` EXACTLY and hard-fails on a miss. There is no
"newest wins" fallback: `raw/wago/` holds tables at 67808, at 68256 and
unversioned, so a fallback silently mixes builds (measured: the unversioned
`CooldownSetSpell.csv` carries a `Field_12_1_0_68209_009` column, i.e. build
>= 68209, and joining it against `SpellName` at another build manufactures
`<1310372>`-style rows for spells that do not exist at the join build).

────────────────────────────────────────────────────────────────────────────────
THE SIX LEGS
────────────────────────────────────────────────────────────────────────────────
1. `Trait*` NATIVE TALENTS (replaces `all-talents.tsv` for this artifact).
   Tree set = `SkillLineXTraitTree.TraitTreeID` ∩ `{TraitNode.TraitTreeID where
   Type == 3}` → exactly the 13 class trees, derived not hardcoded.
   * Button spell = `TraitDefinition.VisibleSpellID or SpellID`. Without the
     VisibleSpellID rule the join loses 28 rows the Blizzard API has (Fortifying
     Brew, Thistle Tea, Healing Stream Totem, Hand of Gul'dan, Wither …).
   * Names are an ALIAS SET — `SpellName[SpellID]` ∪ `SpellName[VisibleSpellID]`
     ∪ `TraitDefinition.OverrideName_lang` — because the API emits the override
     (`Holy Bulwark` vs `Holy Armaments`, `Demonsurge` vs `Voidsurge`).
   * Spec scoping: `CondType == 1` ONLY, unioned over node conds AND
     `TraitNodeGroup` conds (the group leg is MANDATORY — node-level conds scope
     only 5 % of class-tree nodes). Empty union ⇒ every spec of the tree.
     ⚠ `CondType == 2` is GRANTED (free ranks), NOT scoping. Using it as a filter
     deletes 65 correct rows (Rake → "Feral only", Moonkin Form → "Balance only",
     Hammer of Wrath → "Retribution only"). Do not.
   * Tree kind (class/spec/hero) comes from COST, not from spec-set width:
     `TraitNodeXTraitCost` / `TraitNodeGroupXTraitCost` → `TraitCost.
     TraitCurrencyID` → `TraitTreeXTraitCurrency._Index` (1 = class, 2 = spec,
     >= 3 = hero). No cost row and no subtree ⇒ class (the 3 Mage barrier grants).
     Deriving it from "the node's spec set equals the whole tree" misfiles 147
     nodes — Midnight class trees contain genuinely spec-restricted class nodes.
   * Hero trees: `TraitNode.TraitSubTreeID != 0` marks the node; WHICH SPECS the
     subtree is offered to comes from the `Type == 3` selector node (its one
     `CondType-1` spec, its two entry `TraitSubTreeID`s), never from the hero
     nodes themselves. This recovers Augmentation Evoker's Chronowarden +
     Scalecommander, which the Blizzard static API drops entirely.
2. `SkillLineAbility` CLASS KIT on the 13 declared class-kit lines
   (`spec_inventory._class_skill_lines`, the SkillRaceClassInfo allowlist), plus
   each class's SECONDARY exclusive lines (DK 960 Runeforging, DH 2152
   Warglaives) which the old "largest exclusive line wins" rule discarded.
   `AcquireMethod == 3` rows are KEPT here (they are not Legion-only: 104 live
   non-passive class-kit rows carry it, including Hammer of Wrath, Lay on Hands,
   Avenging Wrath, Heroic Leap, Stormstrike, Void Torrent).
3. `SpecializationSpells` SPEC BASELINE — the fourth leg no previous tool had.
   Recovers Multi-Shot, Arcane Blast, Fireball, Shadowstrike, Shuriken Storm,
   Black Powder, Incinerate, Devastate and Devourer's Consume.
4. `PvpTalent` — keyed by `SpecID`, origin `pvp-talent`.
5. PET SKILL LINES — two allowlists, never a ClassMask scan. Reachability is
   liveness: a SkillLine is a pet line iff some `CreatureFamily` row names it in
   `SkillLine_0`/`SkillLine_1`. Hunter by declaration (`SkillLine_1 == 270`),
   everything else by `SpellClassOptions.SpellClassSet` majority through the
   class map learned on the 13 kit lines, with `SpellClassSet 57` (demon) ⇒
   Warlock as the required fallback (line 189 Felhunter — the Spell Lock line —
   resolves ONLY that way). Line 758 "Pet - Event - Remote Control" stays
   UNRESOLVED; it is an event vehicle and guessing would be a fabricated value.
   ⚠ KEY ON THE LINE, NOT THE FAMILY. `CreatureFamily 56 "Zombie"` points at line
   236 "Pet - Scorpid": the family is not a Hunter pet, the line is.
   Only `pet-shared` (SkillLine 270) enters the per-spec inventory. The 61 Hunter
   family lines and the 9 Warlock demon lines are `pet-family` and land in
   `_abilities/pet-family-annex.tsv` — which demon or which tamed family is out
   is a player choice, not a spec property, and admitting them would grow
   Hunter's inventory ~40 % with ~65 flavour passives.
6. `CooldownSetSpell` — annotation (Essential/Utility + OrderIndex) and the
   `cdm-only` residue, exactly as `spec_inventory` uses it.

────────────────────────────────────────────────────────────────────────────────
ORIGIN + PRECEDENCE
────────────────────────────────────────────────────────────────────────────────
A spec's rows are deduped by normalised name. When two legs claim the same name
the FIRST of this order wins, and the losing leg is recorded in `also_from`:

    talent-active > talent-choice > class-baseline > pvp-talent > pet
                  > talent-passive > cdm-only

Rationale: an active source outranks a passive one; `cdm-only` is residue and
ranks last so anything with a real declaration beats it.

    class-baseline  SkillLineAbility class kit (leg 2) or SpecializationSpells
                    (leg 3). The `source` column separates them.
    talent-active   Trait node, castable, node Type 0/1.
    talent-choice   Trait node, castable, node Type 2 (CHOICE — exact, 398/398).
    talent-passive  Trait node, NOT castable. NEW in this artifact.
    pvp-talent      PvpTalent row for the spec.
    pet             pet-shared skill line (Hunter 270 only, by design).
    cdm-only        present only in CooldownSetSpell.

CASTABLE is `NOT (SpellMisc.Attributes_0 & 0x40)` on the effective button spell
(DifficultyID 0), OR the name is bound in the BucketBinds seed. `TraitNode.Type`
canNOT supply this — Type is node SHAPE, not castability: Type 0 splits 393
ACTIVE / 2023 PASSIVE, and all 40 Type-1 capstones grant a passive-flagged spell
while the API labels them ACTIVE.
⚠ The seed half of the rescue is LOAD-BEARING for four abilities with no DB2
route to their button at all — Void Metamorphosis (471306), Collapsing Star
(1221167), Mana Tea (115869), Hammer of Wrath (1241288). Do not "clean it up".
⚠ Do NOT add "is in CooldownSetSpell" to the rescue: measured, it re-imports 584
passive talent auras and flips their suggestedMode fixed→float across all 40
specs — a silent mass re-banding of BucketBinds.

────────────────────────────────────────────────────────────────────────────────
WHAT THIS CANNOT ANSWER (state it, do not guess)
────────────────────────────────────────────────────────────────────────────────
* NO SPEC GRANULARITY EXISTS ON THE PET PATH. Not in SkillLine, SkillLineAbility,
  SkillRaceClassInfo or CreatureFamily. Every pet claim is class-level.
* Proc-replacement / override buttons that Blizzard hands the client at runtime
  (C_SpellBook override mechanics) are in NO spec-keyed DB2 table at 67808 —
  Devour, Pierce the Veil, Hammer of Light, Templar Slash, Void Volley, Engulf,
  Heroic Strike, Empty the Cellar, Zenith Stomp. `--residual` lists them; closing
  them needs an in-game spellbook enumeration, not another DB2 join.
* Presence on a pet line is not proof the pet is obtainable in 12.0.7.

────────────────────────────────────────────────────────────────────────────────
--check
────────────────────────────────────────────────────────────────────────────────
Renders every output in memory and byte-compares against disk; exit 1 on any
drift. There is NO CI in this repo — `.github/workflows/` holds one unrelated
Pages job — so `--check` is a MANUAL / pre-commit gate, not an enforced one.
`--fetched` is REQUIRED (talents.py defaults it to "" and that is a bug), and
this module emits `reviewed:` equal to `fetched:` itself, so a later hand-stamp
sweep cannot make `--check` fail permanently the way it did for talents.md.

stdlib-only apart from the shared ROOT helper.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from ._common import ROOT
from .spec_inventory import (
    CATEGORY,
    PINNED_BUILD,
    SEED,
    SPELL_ATTR0_PASSIVE,
    _baseline_kit,
    _class_skill_lines,
    _cooldowns,
    _norm,
    _passive_ids,
    _rows,
)

CLASSES = ROOT / "knowledge" / "classes"
ABIL_DIR = CLASSES / "_abilities"
PATCH = "12.0.7"

BANNER = "AUTO-GENERATED by wowkb.gen_abilities — do NOT hand-edit."

# Precedence: first wins on a name collision within a spec (see docstring).
ORIGIN_ORDER = [
    "talent-active", "talent-choice", "class-baseline", "pvp-talent",
    "pet", "talent-passive", "cdm-only",
]
ORIGIN_RANK = {o: i for i, o in enumerate(ORIGIN_ORDER)}

TSV_COLUMNS = [
    "class", "spec", "spec_id", "name", "spell_id", "origin", "source",
    "castable", "cooldown", "band", "tree", "hero_tree", "node_id", "entry_id",
    "max_ranks", "blizz_category", "seed_bucket", "also_from", "aliases",
]
ANNEX_COLUMNS = [
    "skill_line", "line_name", "class", "class_id", "family", "family_id",
    "pet_talent_type", "exotic", "name", "spell_id", "castable", "cooldown",
]

# CreatureFamily.PetTalentType (Hunter specialisation of a tamed family).
PET_TALENT_TYPE = {"0": "Ferocity", "1": "Tenacity", "2": "Cunning"}
HUNTER_PET_LINE = "270"          # "Pet - Generic Hunter" — the declaration line
DEMON_CLASS_SET = "57"           # SpellClassOptions.SpellClassSet for demon kit
EXOTIC_MARKER = "93273"          # "Hunter Pet Exotic Marker (DND)"
UNRESOLVED = "UNRESOLVED"


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def _slug(name: str) -> str:
    """'Beast Mastery' -> 'beast-mastery' (matches knowledge/classes/ layout)."""
    return name.lower().replace("'", "").replace(" ", "-")


# ── leg 1: the native Trait* talent join ─────────────────────────────────────
class TraitLeg:
    """The 13 class trees, spec-scoped, from Trait* DB2 alone.

    Attributes after construction:
        by_spec   spec_id -> [record]
        hero_map  subtree_id -> {spec_id}
        stats     counters for the report
    """

    def __init__(self, names: dict[str, str], passive: set[str],
                 cds: dict[str, float], seed_norms: set[str]):
        self.names = names
        self.passive = passive
        self.cds = cds
        self.seed_norms = seed_norms

        # ── tree set: declared (SkillLineXTraitTree) ∩ has-a-selector-node ────
        sl_to_tree = {r["SkillLineID"]: r["TraitTreeID"] for r in _rows("SkillLineXTraitTree")}
        node_rows = list(_rows("TraitNode"))
        selector_trees = {r["TraitTreeID"] for r in node_rows if r["Type"] == "3"}
        self.trees = set(sl_to_tree.values()) & selector_trees
        if len(self.trees) != 13:
            sys.exit(f"error: expected 13 class trees, derived {len(self.trees)} — "
                     f"the SkillLineXTraitTree ∩ Type-3 rule broke at {PINNED_BUILD}")

        # ── nodes ────────────────────────────────────────────────────────────
        self.node_tree, self.node_type, self.node_subtree = {}, {}, {}
        for r in node_rows:
            if r["TraitTreeID"] not in self.trees:
                continue
            self.node_tree[r["ID"]] = r["TraitTreeID"]
            self.node_type[r["ID"]] = r["Type"]
            self.node_subtree[r["ID"]] = r["TraitSubTreeID"]

        # ── definitions + entries ────────────────────────────────────────────
        defs = {r["ID"]: r for r in _rows("TraitDefinition")}
        entries = {r["ID"]: r for r in _rows("TraitNodeEntry")}
        self.node_entries: dict[str, list[tuple[int, str]]] = defaultdict(list)
        for r in _rows("TraitNodeXTraitNodeEntry"):
            nid = r["TraitNodeID"]
            if nid in self.node_tree:
                self.node_entries[nid].append((int(r["_Index"]), r["TraitNodeEntryID"]))
        for v in self.node_entries.values():
            v.sort()
        self.defs, self.entries = defs, entries

        # ── spec sets ────────────────────────────────────────────────────────
        specset: dict[str, set[str]] = defaultdict(set)
        for r in _rows("SpecSetMember"):
            specset[r["SpecSet"]].add(r["ChrSpecializationID"])
        self.specset = specset

        conds = {r["ID"]: r for r in _rows("TraitCond")}
        # Tree roster = every CondType-1 spec set declared anywhere in the tree.
        self.tree_specs: dict[str, set[str]] = defaultdict(set)
        for c in conds.values():
            if c["CondType"] == "1" and c["SpecSetID"] != "0" and c["TraitTreeID"] in self.trees:
                self.tree_specs[c["TraitTreeID"]] |= specset.get(c["SpecSetID"], set())

        # node -> CondType-1 spec set (node-level conds).
        self.node_cond_specs: dict[str, set[str]] = defaultdict(set)
        for r in _rows("TraitNodeXTraitCond"):
            c = conds.get(r["TraitCondID"])
            if c and c["CondType"] == "1" and c["SpecSetID"] != "0":
                self.node_cond_specs[r["TraitNodeID"]] |= specset.get(c["SpecSetID"], set())
        # group -> CondType-1 spec set, then group -> nodes. MANDATORY: node-level
        # conds alone scope 146 of 2896 class-tree nodes (5 %).
        group_specs: dict[str, set[str]] = defaultdict(set)
        for r in _rows("TraitNodeGroupXTraitCond"):
            c = conds.get(r["TraitCondID"])
            if c and c["CondType"] == "1" and c["SpecSetID"] != "0":
                group_specs[r["TraitNodeGroupID"]] |= specset.get(c["SpecSetID"], set())
        self.node_groups: dict[str, list[str]] = defaultdict(list)
        for r in _rows("TraitNodeGroupXTraitNode"):
            self.node_groups[r["TraitNodeID"]].append(r["TraitNodeGroupID"])
        self.group_specs = group_specs

        # ── tree kind from COST currency index (1 class, 2 spec, >=3 hero) ────
        cost_currency = {r["ID"]: r["TraitCurrencyID"] for r in _rows("TraitCost")}
        cur_index: dict[tuple[str, str], int] = {}
        for r in _rows("TraitTreeXTraitCurrency"):
            cur_index[(r["TraitTreeID"], r["TraitCurrencyID"])] = int(r["_Index"])
        self.cur_index = cur_index
        self.node_costs: dict[str, set[str]] = defaultdict(set)
        for r in _rows("TraitNodeXTraitCost"):
            c = cost_currency.get(r["TraitCostID"])
            if c:
                self.node_costs[r["TraitNodeID"]].add(c)
        group_costs: dict[str, set[str]] = defaultdict(set)
        for r in _rows("TraitNodeGroupXTraitCost"):
            c = cost_currency.get(r["TraitCostID"])
            if c:
                group_costs[r["TraitNodeGroupID"]].add(c)
        for nid, groups in self.node_groups.items():
            for g in groups:
                self.node_costs[nid] |= group_costs.get(g, set())

        # ── hero subtrees ────────────────────────────────────────────────────
        self.subtree_name = {r["ID"]: r["Name_lang"] for r in _rows("TraitSubTree")}
        self.hero_map = self._hero_specs()

        self.by_spec, self.stats = self._build()

    # -- helpers ------------------------------------------------------------
    def _button(self, entry_id: str) -> tuple[str, str, set[str]]:
        """(button_spell_id, display_name, alias_set) for a TraitNodeEntry."""
        e = self.entries.get(entry_id)
        if not e:
            return "", "", set()
        d = self.defs.get(e["TraitDefinitionID"])
        if not d:
            return "", "", set()
        spell = d["SpellID"]
        visible = d["VisibleSpellID"]
        button = visible if visible not in ("", "0") else spell
        override = (d["OverrideName_lang"] or "").strip()
        aliases = {self.names.get(spell, ""), self.names.get(visible, ""), override}
        aliases.discard("")
        display = override or self.names.get(button) or self.names.get(spell) or ""
        return button, display, aliases

    def _hero_specs(self) -> dict[str, set[str]]:
        """subtree_id -> {spec_id}, from the Type-3 selector nodes only.

        Hero nodes carry no spec cond, so the selector is the ONLY declaration of
        which specs may take a hero tree. This is what recovers Augmentation
        Evoker's two trees (the Blizzard static API gives it zero).
        """
        out: dict[str, set[str]] = defaultdict(set)
        for nid, ntype in self.node_type.items():
            if ntype != "3":
                continue
            specs = self._node_specs_raw(nid)
            for _, eid in self.node_entries.get(nid, []):
                sub = (self.entries.get(eid) or {}).get("TraitSubTreeID", "0")
                if sub not in ("", "0"):
                    out[sub] |= specs
        return out

    def _node_specs_raw(self, nid: str) -> set[str]:
        specs = set(self.node_cond_specs.get(nid, set()))
        for g in self.node_groups.get(nid, []):
            specs |= self.group_specs.get(g, set())
        return specs

    def _node_specs(self, nid: str) -> set[str]:
        tree = self.node_tree[nid]
        roster = self.tree_specs.get(tree, set())
        sub = self.node_subtree.get(nid, "0")
        if sub not in ("", "0"):
            # Hero node: scoped by its subtree's selector, not by its own conds.
            return self.hero_map.get(sub, set()) & roster
        specs = self._node_specs_raw(nid)
        return (specs & roster) if specs else set(roster)

    def _tree_kind(self, nid: str) -> str:
        if self.node_subtree.get(nid, "0") not in ("", "0"):
            return "hero"
        tree = self.node_tree[nid]
        idxs = sorted(self.cur_index.get((tree, c), 99) for c in self.node_costs.get(nid, ()))
        if not idxs:
            return "class"   # no cost row + no subtree (the 3 Mage barrier grants)
        i = idxs[0]
        return "class" if i == 1 else ("spec" if i == 2 else "hero")

    def _castable(self, button: str, aliases: set[str]) -> bool:
        if button and button not in self.passive:
            return True
        return any(_norm(a) in self.seed_norms for a in aliases)

    # -- build --------------------------------------------------------------
    def _build(self):
        by_spec: dict[str, list[dict]] = defaultdict(list)
        stats = Counter()
        for nid, ntype in self.node_type.items():
            if ntype == "3":
                continue  # SubTreeSelection — the hero picker, grants no spell
            specs = self._node_specs(nid)
            if not specs:
                continue
            kind = self._tree_kind(nid)
            sub = self.node_subtree.get(nid, "0")
            hero = self.subtree_name.get(sub, "") if sub not in ("", "0") else ""
            for _, eid in self.node_entries.get(nid, []):
                button, display, aliases = self._button(eid)
                if not button or button == "0" or not display:
                    continue
                castable = self._castable(button, aliases)
                if ntype == "2":
                    origin = "talent-choice" if castable else "talent-passive"
                else:
                    origin = "talent-active" if castable else "talent-passive"
                stats[origin] += 1
                rec = {
                    "name": display,
                    "spell_id": int(button),
                    "origin": origin,
                    "source": "TraitNodeEntry",
                    "castable": castable,
                    "cooldown": round(self.cds.get(button, 0.0), 1),
                    "tree": kind,
                    "hero_tree": hero,
                    "node_id": int(nid),
                    "entry_id": int(eid),
                    "max_ranks": int((self.entries.get(eid) or {}).get("MaxRanks") or 0),
                    "aliases": sorted(a for a in aliases if _norm(a) != _norm(display)),
                }
                for sid in specs:
                    by_spec[sid].append(rec)
        return by_spec, stats


# ── leg 5: the pet skill lines ───────────────────────────────────────────────
class PetLeg:
    """Line -> class, by reachability from CreatureFamily. See the module docstring.

    Attributes:
        line_class   skill_line -> classID | "UNRESOLVED"
        line_tier    skill_line -> "pet-shared" | "pet-family"
        rows         [annex record]
        shared       classID -> [record]  (pet-shared only; enters the inventory)
    """

    def __init__(self, names: dict[str, str], passive: set[str], cds: dict[str, float],
                 kit_lines: dict[str, dict[str, str]]):
        sl = {r["ID"]: r for r in _rows("SkillLine")}
        families = list(_rows("CreatureFamily"))
        sla = list(_rows("SkillLineAbility"))

        # 1. reachability = liveness.
        line_families: dict[str, list[dict]] = defaultdict(list)
        for f in families:
            for col in ("SkillLine_0", "SkillLine_1"):
                ln = f[col]
                if ln not in ("", "0"):
                    line_families[ln].append(f)
        self.lines = set(line_families)

        # 2. Hunter, by declaration: CreatureFamily.SkillLine_1 == 270.
        hunter_lines = {HUNTER_PET_LINE}
        for f in families:
            if f["SkillLine_1"] == HUNTER_PET_LINE:
                for col in ("SkillLine_0", "SkillLine_1"):
                    if f[col] not in ("", "0"):
                        hunter_lines.add(f[col])

        # SpellClassSet -> classID, LEARNED from the 13 declared kit lines.
        classopt = {r["SpellID"]: r["SpellClassSet"] for r in _rows("SpellClassOptions")}
        line_of_class = {ln: cid for cid, lns in kit_lines.items()
                         for ln, kind in lns.items() if kind == "kit"}
        set_votes: dict[str, Counter] = defaultdict(Counter)
        line_spells: dict[str, list[str]] = defaultdict(list)
        for r in sla:
            line_spells[r["SkillLine"]].append(r["Spell"])
            cid = line_of_class.get(r["SkillLine"])
            cs = classopt.get(r["Spell"])
            if cid and cs and cs != "0":
                set_votes[cs][cid] += 1
        self.class_set = {cs: v.most_common(1)[0][0] for cs, v in set_votes.items()}

        # 3/4/5. resolve every reachable line.
        self.line_class: dict[str, str] = {}
        for ln in sorted(self.lines, key=int):
            if ln in hunter_lines:
                self.line_class[ln] = "3"
                continue
            sets = Counter(classopt.get(s) for s in line_spells.get(ln, [])
                           if classopt.get(s) not in (None, "0"))
            classes = {self.class_set[cs] for cs in sets if cs in self.class_set}
            if len(classes) == 1:
                self.line_class[ln] = classes.pop()
            elif DEMON_CLASS_SET in sets:
                self.line_class[ln] = "9"        # the required demon fallback
            else:
                self.line_class[ln] = UNRESOLVED
        self.line_tier = {ln: ("pet-shared" if ln == HUNTER_PET_LINE else "pet-family")
                          for ln in self.lines}

        # INVARIANT. The SpellClassSet-57 ⇒ Warlock fallback is an INDUCTIVE claim
        # over one build: at 12.0.7.67808 every SkillLineAbility row referencing a
        # 57 spell sits on a Warlock demon line, and line 189 (Felhunter — the
        # Spell Lock line) resolves ONLY that way. A future build could attach 57
        # to a non-Warlock pet, and the fallback would then silently mislabel it.
        # Assert, don't degrade.
        for ln in sorted(self.lines, key=int):
            if any(classopt.get(s) == DEMON_CLASS_SET for s in line_spells.get(ln, [])):
                if self.line_class[ln] != "9":
                    sys.exit(
                        f"error: SpellClassSet {DEMON_CLASS_SET} (demon) appears on pet "
                        f"SkillLine {ln}, which resolved to class {self.line_class[ln]!r}, "
                        f"not Warlock. The 57⇒Warlock fallback no longer holds at "
                        f"{PINNED_BUILD} — re-derive it before trusting the pet leg.")

        # annex rows + the shared inventory rows.
        self.rows: list[dict] = []
        self.shared: dict[str, list[dict]] = defaultdict(list)
        for ln in sorted(self.lines, key=int):
            cid = self.line_class[ln]
            exotic = EXOTIC_MARKER in line_spells.get(ln, [])
            fams = [f for f in line_families[ln]
                    if not re.match(r"^\s*<<.*>>\s*$", f["Name_lang"] or "")]
            fam_names = ", ".join(sorted(f["Name_lang"] for f in fams))
            fam_ids = ",".join(sorted((f["ID"] for f in fams), key=int))
            ptt = sorted({PET_TALENT_TYPE.get(f["PetTalentType"], "") for f in fams} - {""})
            seen = set()
            for spell in line_spells.get(ln, []):
                nm = names.get(spell)
                if not nm or spell in seen:
                    continue
                seen.add(spell)
                rec = {
                    "skill_line": int(ln),
                    "line_name": (sl.get(ln) or {}).get("DisplayName_lang", ""),
                    "class": cid,
                    "class_id": cid,
                    "family": fam_names,
                    "family_id": fam_ids,
                    "pet_talent_type": "/".join(ptt),
                    "exotic": exotic,
                    "name": nm,
                    "spell_id": int(spell),
                    "castable": spell not in passive,
                    "cooldown": round(cds.get(spell, 0.0), 1),
                }
                self.rows.append(rec)
                if ln == HUNTER_PET_LINE and rec["castable"]:
                    self.shared[cid].append({
                        "name": nm, "spell_id": int(spell), "origin": "pet",
                        "source": f"SkillLineAbility:{ln}", "castable": True,
                        "cooldown": rec["cooldown"],
                    })


# ── the union ────────────────────────────────────────────────────────────────
def _empty(rec: dict) -> dict:
    rec.setdefault("tree", "")
    rec.setdefault("hero_tree", "")
    rec.setdefault("node_id", "")
    rec.setdefault("entry_id", "")
    rec.setdefault("max_ranks", "")
    rec.setdefault("aliases", [])
    rec.setdefault("castable", True)
    return rec


def build(seed_path: Path = SEED) -> dict:
    names = {r["ID"]: r["Name_lang"] for r in _rows("SpellName")}
    passive = _passive_ids()
    cds = _cooldowns()
    classes = {r["ID"]: r["Name_lang"] for r in _rows("ChrClasses")}
    specs = {r["ID"]: {"spec": r["Name_lang"], "classID": r["ClassID"],
                       "class": classes.get(r["ClassID"], "?")}
             for r in _rows("ChrSpecialization")}

    seed = json.loads(seed_path.read_text(encoding="utf-8"))
    seed_by_spec: dict[str, dict[str, str]] = {}
    seed_norms: set[str] = set()
    for s in seed["specs"]:
        m = {_norm(v): k for k, v in s["abilities"].items() if v}
        seed_by_spec[f"{s['class']}/{s['spec']}"] = m
        seed_norms |= set(m)

    kit_lines = _class_skill_lines()
    trait = TraitLeg(names, passive, cds, seed_norms)
    pet = PetLeg(names, passive, cds, kit_lines)

    # leg 2 — class kit incl. the secondary exclusive lines and AcquireMethod 3.
    # `_baseline_kit` speaks spec_inventory's key names; translate once.
    baseline: dict[str, list[dict]] = {
        cid: [{"name": r["name"], "spell_id": r["spellID"], "origin": "class-baseline",
               "source": r["source"], "castable": True, "cooldown": r["cooldown"]}
              for r in recs]
        for cid, recs in _baseline_kit(cds, names, include_secondary=True,
                                       keep_artifact_rows=True).items()
    }

    # leg 3 — SpecializationSpells (spec baseline).
    spec_baseline: dict[str, list[dict]] = defaultdict(list)
    for r in _rows("SpecializationSpells"):
        sid = r["SpellID"]
        nm = names.get(sid)
        if not nm or sid in passive:
            continue
        spec_baseline[r["SpecID"]].append({
            "name": nm, "spell_id": int(sid), "origin": "class-baseline",
            "source": "SpecializationSpells", "castable": True,
            "cooldown": round(cds.get(sid, 0.0), 1),
        })

    # leg 4 — PvP talents.
    pvp: dict[str, list[dict]] = defaultdict(list)
    for r in _rows("PvpTalent"):
        sid = r["SpellID"]
        nm = names.get(sid)
        if not nm:
            continue
        pvp[r["SpecID"]].append({
            "name": nm, "spell_id": int(sid), "origin": "pvp-talent",
            "source": "PvpTalent", "castable": sid not in passive,
            "cooldown": round(cds.get(sid, 0.0), 1),
        })

    # leg 6 — Cooldown Manager: annotation + residue.
    set_to_spec = {r["ID"]: r["ChrSpecialization"] for r in _rows("CooldownSet")}
    cdm: dict[str, dict[str, dict]] = defaultdict(dict)
    for r in _rows("CooldownSetSpell"):
        spec_id = set_to_spec.get(r["CooldownSetID"])
        if not spec_id or spec_id == "0":
            continue
        sid = r["SpellID"]
        nm = names.get(sid)
        if not nm:
            continue  # a spellID absent from SpellName at this build — never emit
        rec = cdm[spec_id].setdefault(_norm(nm), {
            "spellID": sid, "name": nm, "categories": set(), "order": 9999,
        })
        rec["categories"].add(CATEGORY.get(r.get("Category", ""), "Other"))
        rec["order"] = min(rec["order"], int(r.get("OrderIndex") or 0))

    out: dict[str, dict] = {}
    for spec_id, meta in specs.items():
        if spec_id not in trait.by_spec:
            continue  # pet/initial pseudo-specs have no talent tree
        key = f"{meta['class']}/{meta['spec']}"
        buckets = seed_by_spec.get(key, {})
        merged: dict[str, dict] = {}

        def place(rec: dict) -> None:
            nk = _norm(rec["name"])
            if not nk:
                return
            cur = merged.get(nk)
            if cur is None:
                merged[nk] = dict(rec)
                merged[nk]["also_from"] = []
                return
            if ORIGIN_RANK[rec["origin"]] < ORIGIN_RANK[cur["origin"]]:
                also = cur["also_from"] + [f"{cur['origin']}:{cur['source']}"]
                merged[nk] = dict(rec)
                merged[nk]["also_from"] = also
            else:
                tag = f"{rec['origin']}:{rec['source']}"
                if tag not in cur["also_from"]:
                    cur["also_from"].append(tag)

        for rec in sorted(trait.by_spec[spec_id], key=lambda r: ORIGIN_RANK[r["origin"]]):
            place(rec)
        for rec in baseline.get(meta["classID"], []):
            place(rec)
        for rec in spec_baseline.get(spec_id, []):
            place(rec)
        for rec in pvp.get(spec_id, []):
            place(rec)
        for rec in pet.shared.get(meta["classID"], []):
            place(rec)
        for nk, c in cdm.get(spec_id, {}).items():
            place({"name": c["name"], "spell_id": int(c["spellID"]),
                   "origin": "cdm-only", "source": "CooldownSetSpell",
                   "castable": c["spellID"] not in passive,
                   "cooldown": round(cds.get(c["spellID"], 0.0), 1)})

        rows = []
        for nk, rec in merged.items():
            _empty(rec)
            ann = cdm.get(spec_id, {}).get(nk)
            rec["blizz_category"] = "/".join(sorted(ann["categories"])) if ann else ""
            rec["order"] = ann["order"] if ann else 9999
            rec["seed_bucket"] = buckets.get(nk, "")
            rec["band"] = "Cooldown" if rec["cooldown"] >= 45 else "Rotational"
            rec["class"] = meta["class"]
            rec["spec"] = meta["spec"]
            rec["spec_id"] = int(spec_id)
            rows.append(rec)
        rows.sort(key=lambda r: (ORIGIN_RANK[r["origin"]], -r["cooldown"], r["name"]))
        out[key] = {"specID": int(spec_id), "class": meta["class"],
                    "spec": meta["spec"], "abilities": rows}

    return {"specs": dict(sorted(out.items())), "pet_annex": pet.rows,
            "pet_lines": pet.line_class, "trait_stats": trait.stats,
            "hero_map": {trait.subtree_name.get(k, k): sorted(v, key=int)
                         for k, v in trait.hero_map.items()}}


# ── rendering ────────────────────────────────────────────────────────────────
def _tsv(rows: list[dict], columns: list[str]) -> str:
    def cell(r, c):
        v = r.get(c, "")
        if isinstance(v, bool):
            return "true" if v else "false"
        if isinstance(v, list):
            return ";".join(str(x) for x in v)
        if isinstance(v, float):
            return f"{v:g}"
        return str(v)
    lines = ["\t".join(columns)]
    lines += ["\t".join(cell(r, c) for c in columns) for r in rows]
    return "\n".join(lines) + "\n"


def _front_matter(title: str, fetched: str, extra_sources: list[str] = ()) -> str:
    src = [f"https://wago.tools/db2 (Tier 1, DB2 pinned @ {PINNED_BUILD})",
           "projects/keybinder/data/bellular-keybinds.seed.json (castable rescue)"]
    src += list(extra_sources)
    return (
        "---\n"
        f"title: {title}\n"
        f"patch: {PATCH}\n"
        f"build: {PINNED_BUILD}\n"
        f"fetched: {fetched}\n"
        f"reviewed: {fetched}\n"
        "sources:\n" + "".join(f"  - {s}\n" for s in src) +
        "confidence: high\n"
        f"generated: {BANNER}\n"
        "---\n\n"
    )


def _spec_md(entry: dict, fetched: str) -> str:
    counts = Counter(a["origin"] for a in entry["abilities"])
    head = _front_matter(
        f"{entry['class']} {entry['spec']} — ability inventory ({PATCH})", fetched)
    body = [
        f"# {entry['class']} {entry['spec']} — ability inventory ({PATCH})\n",
        f"\n> **{BANNER}** Writer: `uv run python -m wowkb.gen_abilities "
        f"--fetched <YYYY-MM-DD>`. Data twin: `ability-inventory.tsv`. Schema + the "
        f"join model: `../../_abilities/README.md`.\n",
        f"\n> ⚠ `abilities.md` in this directory is hand-written prose and is a "
        f"different document; this file never replaces it.\n",
        f"\nspecID **{entry['specID']}** · **{len(entry['abilities'])}** rows · " +
        " · ".join(f"{o} {counts[o]}" for o in ORIGIN_ORDER if counts[o]) + "\n",
        "\n| # | Ability | ID | CD | Origin | Source | Tree | Hero | Blizz cat | Seed bucket |\n",
        "|---|---|---:|---:|---|---|---|---|---|---|\n",
    ]
    for i, a in enumerate(entry["abilities"], 1):
        cd = f"{a['cooldown']:g}s" if a["cooldown"] else "—"
        body.append(
            f"| {i} | {a['name']} | `{a['spell_id']}` | {cd} | {a['origin']} | "
            f"{a['source']} | {a['tree'] or '—'} | {a['hero_tree'] or '—'} | "
            f"{a['blizz_category'] or '—'} | {a['seed_bucket'] or '—'} |\n")
    return head + "".join(body)


_README_TEMPLATE = """# Ability inventory — schema & regeneration

A per-spec, Tier-1 inventory of every ability a spec can have: talents (active,
choice AND passive), the class kit, spec baseline, PvP talents, the shared pet
line and the Cooldown-Manager residue. Regenerated by `tools/wowkb/gen_abilities.py`.

⚠ **`<class>/<spec>/abilities.md` is hand-written prose** and is NOT generated.
The generated per-spec files are `ability-inventory.tsv` + `ability-inventory.md`.

## Files

| File | One row per | Use |
|------|-------------|-----|
| `all-abilities.tsv` | (spec, ability) | grep/awk across all 40 specs |
| `pet-family-annex.tsv` | (pet skill line, spell) | "which pet/demon gives me X" |
| `../<class>/<spec>/ability-inventory.tsv` | ability | per-spec data |
| `../<class>/<spec>/ability-inventory.md` | ability | reading, citing |

## Build pinning

Every DB2 read is pinned to **{build}** and hard-fails if the pinned CSV is
missing. `raw/wago/` holds tables at several builds; a "newest wins" fallback
silently mixes them (the unversioned `CooldownSetSpell.csv` is build >= 68209).

## Columns (`all-abilities.tsv`, tab-separated)

| Column | Meaning |
|--------|---------|
| `class`, `spec`, `spec_id` | ChrSpecialization identity |
| `name` | display name (`TraitDefinition.OverrideName_lang` wins when set) |
| `spell_id` | the **button** spell — `TraitDefinition.VisibleSpellID or SpellID` |
| `origin` | see the table below |
| `source` | the DB2 table (and skill line) the winning row came from |
| `castable` | `NOT (SpellMisc.Attributes_0 & 0x40)` on the button spell, OR the name is bound in the BucketBinds seed |
| `cooldown` | seconds, `SpellCooldowns` at DifficultyID 0 |
| `band` | `Cooldown` if `cooldown >= 45` else `Rotational` (layout-v2 contract) |
| `tree` | `class` \\| `spec` \\| `hero` — derived from the node's **cost currency**, not from spec-set width |
| `hero_tree` | `TraitSubTree.Name_lang`, else empty |
| `node_id`, `entry_id`, `max_ranks` | Trait* placement, empty for non-talent rows |
| `blizz_category` | Cooldown Manager Essential/Utility/Buff/Other |
| `seed_bucket` | the BucketBinds seed bucket binding this name today |
| `also_from` | other legs that also claim this name, `origin:source` |
| `aliases` | other names for the same entry (`Holy Bulwark` ⇄ `Holy Armaments`) |

### `origin`, in precedence order

`talent-active` > `talent-choice` > `class-baseline` > `pvp-talent` > `pet` >
`talent-passive` > `cdm-only`. On a name collision the highest wins and the
loser is recorded in `also_from`.

| origin | source |
|--------|--------|
| `talent-active` | Trait node, castable, node `Type` 0/1 |
| `talent-choice` | Trait node, castable, node `Type` 2 (CHOICE — exact 398/398) |
| `talent-passive` | Trait node, not castable |
| `class-baseline` | `SkillLineAbility` on the class kit line, or `SpecializationSpells` |
| `pvp-talent` | `PvpTalent` for this spec |
| `pet` | the shared Hunter pet line (SkillLine 270) only |
| `cdm-only` | present only in `CooldownSetSpell` |

## What this source cannot answer

- **No spec granularity exists on the pet path** — not in `SkillLine`,
  `SkillLineAbility`, `SkillRaceClassInfo` or `CreatureFamily`. Every pet claim
  here is **class-level**. A pet ability written into a per-spec file is a spec
  attribution the data does not support.
- **Runtime override / proc-replacement buttons are in no spec-keyed DB2 table**
  at {build}: Devour, Pierce the Veil, Hammer of Light, Templar Slash, Void
  Volley, Engulf, Heroic Strike, Empty the Cellar, Zenith Stomp. Closing them
  needs an in-game spellbook enumeration (ClientLab), not another DB2 join.
- **Presence on a pet line is not proof the pet is obtainable in 12.0.7.**
- `SkillLine 758` "Pet - Event - Remote Control" is emitted **UNRESOLVED** in the
  annex. It is an event vehicle; guessing a class would be a fabricated value.

## Notable corrections baked in

- **Augmentation Evoker gets Chronowarden + Scalecommander.** `trees.tsv` (from
  the Blizzard static API) gives Augmentation **zero** hero trees; the native
  `Type == 3` selector node 99825 is unambiguous. 34 of the 35 talents the
  native join recovers are this.
- **The Shadowlands Covenant lines stay dead.** `SkillLine` 2730/2731/2732/2733
  carry 13 distinct ClassMasks each; a naive ClassMask scan resurrects Shifting
  Power for Mage, Soul Rot for Warlock, Convoke for Druid… all at once. This
  tool reaches skill lines through two closed allowlists and never scans masks.
- **Runeforging (SkillLine 960) and Warglaives (2152) are back.** The old
  "largest exclusive line wins" rule silently dropped them.

## Regenerate

```bash
cd tools
uv run python -m wowkb.gen_abilities --fetched <YYYY-MM-DD>
uv run python -m wowkb.gen_abilities --fetched <YYYY-MM-DD> --check   # drift gate
uv run python -m wowkb.gen_abilities --fetched <YYYY-MM-DD> --residual
```

`--check` re-renders in memory and byte-compares. **There is no CI in this repo**
(`.github/workflows/` holds one unrelated Pages job), so `--check` is a manual /
pre-commit gate — nothing enforces it automatically.
"""


def render_all(data: dict, fetched: str) -> dict[Path, str]:
    """Every output file as {path: content}. Rendering is pure — `--check` byte-
    compares this against disk and `main` writes it."""
    files: dict[Path, str] = {}
    all_rows = []
    for key, entry in data["specs"].items():
        cls, spec = _slug(entry["class"]), _slug(entry["spec"])
        d = CLASSES / cls / spec
        files[d / "ability-inventory.tsv"] = _tsv(entry["abilities"], TSV_COLUMNS)
        files[d / "ability-inventory.md"] = _spec_md(entry, fetched)
        all_rows.extend(entry["abilities"])
    files[ABIL_DIR / "all-abilities.tsv"] = _tsv(all_rows, TSV_COLUMNS)
    files[ABIL_DIR / "pet-family-annex.tsv"] = _tsv(data["pet_annex"], ANNEX_COLUMNS)
    files[ABIL_DIR / "README.md"] = (
        _front_matter(f"Ability inventory — schema & regeneration ({PATCH})", fetched)
        + _README_TEMPLATE.format(build=PINNED_BUILD)
    )
    return files


# ── residual scan ────────────────────────────────────────────────────────────
_JUNK = re.compile(r"[—–]|\betc\.|^Pet\b|^replaces\b", re.I)


def _inventory_names(path: Path) -> set[str]:
    """Ability names from the hand-written abilities.md `## Inventory` table.

    First column only, inside the `## Inventory` section only. Parentheticals and
    bold/code markers are stripped; `A / B` splits. This is a documented
    heuristic over prose, not a Tier-1 read — treat the result as a worklist.
    """
    out: set[str] = set()
    in_section = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            in_section = line.lstrip("#").strip().lower().startswith("inventory")
            continue
        if not in_section or not line.startswith("|"):
            continue
        cell = re.sub(r"\*\*|`", "", line.split("|")[1]).strip()
        if not cell or set(cell) <= set("-: ") or cell.lower() in ("ability", "name", "talent"):
            continue
        if _JUNK.search(cell):
            continue
        for part in re.split(r"\s*/\s*", cell):
            part = re.sub(r"\s*\(.*?\)", "", part).strip()
            # A parenthetical straddling the `/` split leaves an unbalanced
            # fragment ("Crusade (passive", "replaces AW)") — not an ability name.
            if "(" in part or ")" in part or _JUNK.search(part):
                continue
            if part:
                out.add(part)
    return out


def residual(data: dict) -> list[dict]:
    """Names in the hand-written abilities.md inventories the union still can't see."""
    by_slug = {(_slug(v["class"]), _slug(v["spec"])): v for v in data["specs"].values()}
    miss = []
    for path in sorted(CLASSES.glob("*/*/abilities.md")):
        cls, spec = path.parts[-3], path.parts[-2]
        entry = by_slug.get((cls, spec))
        if not entry:
            continue
        have = {_norm(a["name"]) for a in entry["abilities"]}
        for a in entry["abilities"]:
            have |= {_norm(x) for x in a["aliases"]}
        for name in sorted(_inventory_names(path)):
            if _norm(name) and _norm(name) not in have:
                miss.append({"spec": f"{cls}/{spec}", "name": name})
    return miss


# ── cli ──────────────────────────────────────────────────────────────────────
def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="wowkb.gen_abilities", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--fetched", required=True, metavar="YYYY-MM-DD",
                   help="REQUIRED. Stamped as both `fetched:` and `reviewed:`.")
    p.add_argument("--check", action="store_true",
                   help="exit 1 if any generated file is out of date (manual gate; no CI)")
    p.add_argument("--residual", action="store_true",
                   help="list abilities.md inventory names the union still cannot see")
    p.add_argument("--json", metavar="PATH", help="dump the computed union as JSON")
    args = p.parse_args(argv)

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.fetched):
        sys.exit(f"error: --fetched must be an ISO date, got {args.fetched!r}")

    data = build()
    files = render_all(data, args.fetched)

    if args.json:
        Path(args.json).write_text(json.dumps(
            {"specs": data["specs"], "pet_lines": data["pet_lines"],
             "hero_map": data["hero_map"]}, indent=2, default=str), encoding="utf-8")

    if args.residual:
        miss = residual(data)
        print(f"{len(miss)} abilities.md inventory name(s) absent from the union:")
        for m in miss:
            print(f"  {m['spec']:<28} {m['name']}")
        return 0

    if args.check:
        stale = [path for path, content in files.items()
                 if (not path.exists()) or path.read_text(encoding="utf-8") != content]
        if stale:
            print(f"OUT OF DATE: {len(stale)} file(s) — re-run "
                  f"`python -m wowkb.gen_abilities --fetched {args.fetched}`")
            for path in stale[:20]:
                print(f"  {path.relative_to(ROOT)}")
            return 1
        print(f"up to date ({len(files)} files)")
        return 0

    for path, content in files.items():
        _atomic_write(path, content)
    rows = sum(len(v["abilities"]) for v in data["specs"].values())
    counts = Counter(a["origin"] for v in data["specs"].values() for a in v["abilities"])
    print(f"wrote {len(files)} files · {len(data['specs'])} specs · {rows} ability rows")
    print("  " + "  ".join(f"{o} {counts[o]}" for o in ORIGIN_ORDER if counts[o]))
    print(f"  pet annex: {len(data['pet_annex'])} rows over "
          f"{len(data['pet_lines'])} reachable pet lines "
          f"({sum(1 for v in data['pet_lines'].values() if v == UNRESOLVED)} unresolved)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
