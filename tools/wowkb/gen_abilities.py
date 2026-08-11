r"""Generate the per-spec ability inventory as a Tier-1 KB artifact.

This is the *writer* for `knowledge/classes/<class>/<spec>/ability-inventory.tsv`
+ `.md` and the aggregate `knowledge/classes/_abilities/`. It extends — it does
not replace — `wowkb.spec_inventory`, which stays the actives-only union the
BucketBinds floats work and `wowkb.cdmp` read.

    uv run python -m wowkb.gen_abilities --fetched 2026-08-06
    uv run python -m wowkb.gen_abilities --fetched 2026-08-06 --check
    uv run python -m wowkb.gen_abilities --fetched 2026-08-06 --residual
    uv run python -m wowkb.gen_abilities --fetched 2026-08-06 --probe          # network
    uv run python -m wowkb.gen_abilities --fetched 2026-08-06 --descriptions   # network

⚠ `abilities.md` in each spec directory is HAND-WRITTEN PROSE. This module never
writes it. The generated file is `ability-inventory.md`.

────────────────────────────────────────────────────────────────────────────────
THE FOUR SECTIONS
────────────────────────────────────────────────────────────────────────────────
The KB models a spec's abilities in four bands of decreasing confidence:

  1. base spell list per class/spec   — mined  ┐ `ability-inventory.{tsv,md}`
  2. base talent list                 — mined  ┘ (+ `_talents/all-talents.tsv`)
  3. validated but not directly joined         — `section-3-corroborated.{tsv,md}`
  4. un-mined / uncorroborated                 — `section-4-catalogue.{tsv,md}`

Sections 1 + 2 are a JOIN: a row is there because a Tier-1 table says the spec
acquires it. Section 3 is REACHED, not joined — the ability is corroborated by
game data one hop away (an override aura, a live spell endpoint) but no
acquisition row names it. Section 4 is a CATALOGUE of everything still unplaced.

⚠ **SECTION 4 IS NOT A BACKLOG.** Nothing in it is scheduled, aged or chased. An
entry is researched when someone ASKS about it, or when real work needs that
specific ability — the same use-not-age trigger as
`projects/addon-lab/docs/lab-process.md`. A row carries its provenance and
nothing else, on purpose: an explanation would be an unmeasured claim.

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

Legs 1-6 build sections 1 + 2. Two further legs build sections 3 + 4; neither
may write into `ability-inventory.tsv`, because neither produces an acquisition
row and BucketBinds reads that file as the spec's real kit.

A. THE OVERRIDE WALK (`EffectWalk`) — `SpellEffect` outward from the spec's own
   talent spells. Two edges, and only two:
     * `EffectTriggerSpell` — always a genuine spell reference.
     * `EffectMiscValue_0` — a spell reference ONLY when `EffectAura == 332`
       (`OVERRIDE_ACTIONBAR_SPELLS`). ⚠ Under any other aura the same column is a
       skill line, a mechanic or an item id; reading it unconditionally yields
       "Dry Pork Ribs" and "Teleport: Goldshire" as Paladin abilities.
   ANCHORS INCLUDE RANK SIBLINGS — spells sharing the inventory button's
   normalised name AND its `SpellClassOptions.SpellClassSet`. Without that the
   walk misses the two clearest hits in the set: the aura-332 row for Kill Shot
   53351 sits on Black Arrow **466932**, not on the inventory button 466930, and
   Templar Strike 407480's sits on Templar Strikes **406648**, not 406646. The
   class-set half of the test is load-bearing: name alone drags in "Shockwave"
   25425 (a creature spell) and "Frenzy" 27897 (an Arcane Explosion).
   `override` → section 3. `trigger` → section 4.
   ⚠ THE SPLIT IS NOT CLEAN AND MUST NOT BE PRESENTED AS IF IT WERE. Hammer of
   Light arrives via `trigger` (Light's Guidance 427445 uses `EffectTriggerSpell`)
   and is a real pressed button. There is no mechanical rule separating a button
   from an internal effect — which is why section 4 exists rather than a filter.
   Override rows carry `spec_scope`: `spec-exclusive` when the anchor→target pair
   fires for exactly one spec of the class, `class-shared` when it fires for
   several. A `class-shared` row proves the ABILITY is reachable from that class's
   talent; it does NOT prove this spec is the one that presses it (Font of Magic
   375783 lists Spiritbloom for all three Evoker specs; only Preservation has it).
B. THE RESIDUAL PROBE (`--probe`) — for a name `--residual` still cannot place,
   take its candidate IDs from `SpellName` at the pin and GET
   `/data/wow/spell/{id}`. A **200** gives the live ID + tooltip → section 3.
   ⚠ A 404 IS NOT EVIDENCE OF ABSENCE. Hammer of Light 427441 and 427453 both 404
   and are demonstrably live; the endpoint covers independently-castable
   spellbook entries only. A 200 is strong positive evidence, a 404 says nothing,
   so a 404 leaves the name in section 4 unchanged rather than marking it dead.
   The probe is NETWORK and its results are cached to
   `_abilities/residual-probe.json` — a committed KB artifact. Ordinary runs and
   `--check` read the cache and never call out, so generation stays offline and
   deterministic.

────────────────────────────────────────────────────────────────────────────────
THE DESCRIPTION LEG — two sources, one spine, one rendering
────────────────────────────────────────────────────────────────────────────────
Every inventory row carries `description` + `description_source`. The two sources
are COMPLEMENTARY, not redundant, and both are Tier 1. Measured @ 12.0.7.67808
over the 7,065 inventory rows:

                          | DB2 `Spell.Description_lang` | API `/data/wow/spell/{id}`
    row coverage          | 7,039 = 99.6 %, pets 6/6     | 6,928 = 98.1 %, pets 0/6
    readable as-is        | NO — mostly templates        | YES, resolved English
    offline, build-pinned | YES                          | NO — network + a cache

**DB2 is the spine; the API is the rendering.** The API wins where it has text
because its numbers are real; DB2 covers what the API cannot reach — the whole
pet leg (6/6 rows, API 0/6), most of the `cdm-only` residue (API 43/109), and
every 404. Neither alone gets to 99.6 % with readable prose, so the row records
WHICH one served it and a reader checks that before quoting a number.

    api                          resolved English. Durations/magnitudes are real.
    db2-plain                    DB2 text with no `$` placeholder — readable as-is.
    db2-template                 DB2 text with UNRESOLVED `$…` slots. `$s3`, `$d`,
                                 `$?s53376&c2[…][]` are template syntax, NOT text.
    …+redirect                   a `$@spelldesc<id>` splice was followed (DB2).
    …+redirect-api               a splice resolved from the API cache instead.
    …+redirect-unresolved        a splice could not be resolved and is LEFT IN the
                                 text verbatim. 3 spells @ 67808: Blade Flurry
                                 22482 → 319606, Ravager 156287 → 152277, Chakrams
                                 259398 → 259381 — the target has no DB2 text AND
                                 404s on the API. Not evidence of absence; it is a
                                 pointer this build cannot follow.
    none                         neither source has text (26 rows @ 67808). NOT
                                 "junk" — see below; `AuraDescription_lang` is
                                 empty for all 12 of those spellIDs too, so the
                                 third DB2 column would not rescue them either.

⚠ A `none` DESCRIPTION IS A SIGNAL, NOT A DEFECT. Measured @ 67808, the 26 rows
are 12 distinct spellIDs in two kinds:

  * 6 rows / 2 names — STUB TWINS. The name IS a real ability, but THIS spellID
    is a hollow shell sitting in specs that do not have it, while the real button
    is a different spellID with a real cooldown and full API text:
      Force of Nature 37846 (cd 0, `SkillLineAbility:798`, in Feral + Guardian +
        Restoration) vs the real 205636 (cd 60, Balance talent-active).
      Incarnation: Tree of Life 81098 (cd 0, `NameSubtext_lang` "Passive", in
        Balance + Feral + Guardian) vs the real 33891 (cd 180, Restoration
        talent-choice).
  * 20 rows / 10 names — hidden, non-button spells with no twin: 4 spec identity
    auras (`Frost Death Knight` 137006, `Unholy Death Knight` 137007,
    `Protection Paladin` 137028, `Enhancement Shaman` 137041 — all `cdm-only`,
    all passive-flagged), 1 internal driver (`Pyroblast Clearcasting Driver`
    44448), 6 rows of UI plumbing (`Hotbar Slot 01/02` 294184 / 294189), and 9
    rows of internal class-line entries (`Energy Usage` 119650,
    `Zen Pilgrimage/Death Gate/Moonglade Storage Aura I` 126893,
    `Shapeshift Form` 228545). These ARE fairly called junk. The first group is
    not.

⚠ AND IT UNDER-DETECTS — do not sell it as "the stub detector". 101 names in the
inventory carry more than one spellID; 11 of those have the stub SHAPE (a cd-0
`class-baseline` member beside a cd>0 member) and only 2 of the 11 are `none`.
The other 9 (Ardent Defender, Bestial Wrath, Bladestorm, Chi Burst, Fists of
Fury, Ravager, Track Beasts, Track Humanoids, Tranquility) carry full API text on
both spellIDs and this signal says nothing about them. `none` finds a subset for
free; it is not a survey. `none_rows()` computes the split, `main` prints it.

⚠ NOTHING IS FIXED FROM THIS. Dropping a stub row changes the union BucketBinds
consumes and that is the user's call. It is reported and recorded, not actioned.

⚠ `$@spelldesc<id>` means "render spell <id>'s description here" and is spliced
in before storing — Hammer of Light 427441 is LITERALLY `$@spelldesc427453` and
would otherwise store as that string. Cycle-guarded and capped at
`DESC_REDIRECT_DEPTH`; every bound hit is counted and PRINTED, never silent.

⚠ The API results are CACHED to `_abilities/spell-descriptions.json`, a committed
KB artifact, exactly like `residual-probe.json`. Ordinary generation and `--check`
read the cache and never call out — offline and deterministic. Only
`--descriptions` (network, ~3,950 GETs) refreshes it. Its fetch set is the
inventory's distinct spellIDs PLUS any DB2-dangling `$@spelldesc` target.

⚠ A 404 from the endpoint is NOT evidence of absence (59/3,952 @ 67808). It drops
the row to its DB2 template and nothing more is ever concluded from it.

WHERE THE TEXT IS RENDERED, and why it is not everywhere:
  * `<class>/<spec>/ability-inventory.tsv` — full `description` column. Per-spec
    files are small; this is the data twin a spec's reader actually joins against.
  * `<class>/<spec>/ability-inventory.md` — a `## Descriptions` section BELOW the
    table, same numbering. The table is already 10 columns; an eleventh holding
    200 characters of tooltip makes every row unreadable.
  * `_abilities/spell-descriptions.tsv` — one row per DISTINCT spellID (3,949),
    the join table.
  * `_abilities/pet-family-annex.tsv` — full `description` column, same contract.
    The API serves 0 of its 169 distinct spellIDs (measured on a 25-spell random
    sample; consistent with the inventory pet leg's 0/6), so this is entirely the
    DB2 spine — which is the whole reason the spine exists. `--descriptions` does
    NOT fetch annex-only spellIDs: 169 GETs for a measured-zero return.
  * `_abilities/all-abilities.tsv` — `description_source` ONLY, no text. Measured:
    the text is 990 KB spread over 7,065 rows but 561 KB over 3,949 distinct
    spellIDs, i.e. 43 % of it is the same tooltip repeated for a spell several
    specs share. A description is a property of the SPELL, not of the (spec,
    ability) pair, so duplicating it into the cross-spec grep file would double
    that file's size to hold nothing new. Join on `spell_id` instead. The
    `description_source` column stays because coverage IS per row and a
    cross-spec coverage question must be answerable without the join.

⚠ TSV SAFETY. Descriptions carry `\r\n` (and could carry a tab); either written
raw silently corrupts the file — `csv.DictReader` reads the damage as data, not
as an error. `_scrub` escapes `\` → `\\`, CRLF/CR/LF → `\n`, TAB → `\t` on every
cell of every emitted TSV. No existing column contained any of those characters
at 67808, so the escape is a no-op for them.

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
PATCH = "12.1.0"

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
# The per-spec twin carries the full text; the aggregate carries only the
# provenance tag and joins to `_abilities/spell-descriptions.tsv` on `spell_id`.
# See "THE DESCRIPTION LEG" in the docstring for the measured size argument.
SPEC_TSV_COLUMNS = TSV_COLUMNS + ["description_source", "description"]
ALL_TSV_COLUMNS = TSV_COLUMNS + ["description_source"]
DESC_COLUMNS = ["spell_id", "name", "description_source", "description"]
ANNEX_COLUMNS = [
    "skill_line", "line_name", "class", "class_id", "family", "family_id",
    "pet_talent_type", "exotic", "name", "spell_id", "castable", "cooldown",
    "description_source", "description",
]
SECTION3_COLUMNS = [
    "class", "spec", "name", "spell_id", "reached_by", "spec_scope",
    "anchor", "anchor_spell_id", "provenance",
]
SECTION4_COLUMNS = [
    "class", "spec", "name", "spell_id", "reached_by", "provenance",
]

# SpellEffect.EffectAura — the ONLY aura under which EffectMiscValue_0 is a spell.
AURA_OVERRIDE_ACTIONBAR_SPELLS = "332"
# Cap on `/data/wow/spell/{id}` calls per residual name. Truncation is LOGGED,
# never silent: "Devour" alone has 140 SpellName candidates at the pin.
PROBE_CANDIDATE_CAP = 40

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


# ── leg A: the override / trigger walk ───────────────────────────────────────
class EffectWalk:
    """`SpellEffect` one hop out from each spec's own talent spells.

    See "THE FOUR SECTIONS" and leg A in the module docstring. Emits two lists:

        overrides  [{spec_key, name, spell_id, anchor, anchor_spell_id, spec_scope}]
        triggers   [{spec_key, name, spell_id, anchor, anchor_spell_id}]

    A target already present in the spec's inventory (by name or alias) is not a
    hit — the walk only reports what sections 1 + 2 could not reach.
    """

    def __init__(self, specs: dict[str, dict], names: dict[str, str]):
        self.names = names
        classset = {r["SpellID"]: r["SpellClassSet"] for r in _rows("SpellClassOptions")
                    if r["SpellClassSet"] not in ("", "0")}
        # (normalised name, class set) -> every spellID sharing both = rank siblings.
        siblings: dict[tuple[str, str], set[str]] = defaultdict(set)
        for sid, nm in names.items():
            cs = classset.get(sid)
            if cs:
                siblings[(_norm(nm), cs)].add(sid)

        trig: dict[str, set[str]] = defaultdict(set)
        ovr: dict[str, set[str]] = defaultdict(set)
        for r in _rows("SpellEffect"):
            if r.get("DifficultyID") != "0":
                continue
            sid = r["SpellID"]
            t = r.get("EffectTriggerSpell") or "0"
            if t not in ("", "0"):
                trig[sid].add(t)
            if r.get("EffectAura") == AURA_OVERRIDE_ACTIONBAR_SPELLS:
                m = r.get("EffectMiscValue_0") or "0"
                if m not in ("", "0"):
                    ovr[sid].add(m)

        raw_ovr, raw_trig = [], []
        # (class, anchor name, target) -> every spec of the class whose inventory
        # carries that anchor. Counted BEFORE the already-have filter: a hero
        # talent shared by two specs fires for both even when one of them already
        # owns the target and so contributes no hit. Filtering first would label
        # Coup de Grace → Dispatch `spec-exclusive` for Subtlety purely because
        # Outlaw, the spec that actually presses Dispatch, was filtered out.
        fires: dict[tuple[str, str, int], set[str]] = defaultdict(set)
        for key, entry in specs.items():
            have = set()
            for a in entry["abilities"]:
                have.add(_norm(a["name"]))
                have |= {_norm(x) for x in a["aliases"]}
            # anchor spellID -> the inventory ability it belongs to
            anchors: dict[str, dict] = {}
            for a in entry["abilities"]:
                if not a["origin"].startswith("talent"):
                    continue
                sid = str(a["spell_id"])
                anchors[sid] = a
                cs = classset.get(sid)
                if cs:
                    for sib in siblings.get((_norm(a["name"]), cs), ()):
                        anchors.setdefault(sib, a)
            for src, a in sorted(anchors.items(), key=lambda kv: int(kv[0])):
                for tgt in sorted(ovr.get(src, ()), key=int):
                    if names.get(tgt):
                        fires[(entry["class"], _norm(a["name"]), int(tgt))].add(entry["spec"])
                for bucket, out in ((ovr, raw_ovr), (trig, raw_trig)):
                    for tgt in sorted(bucket.get(src, ()), key=int):
                        nm = names.get(tgt)
                        if not nm or _norm(nm) in have:
                            continue
                        out.append({
                            "class": entry["class"], "spec": entry["spec"],
                            "spec_key": key, "name": nm, "spell_id": int(tgt),
                            "anchor": a["name"], "anchor_spell_id": int(src),
                        })

        for h in raw_ovr:
            n = len(fires[(h["class"], _norm(h["anchor"]), h["spell_id"])])
            h["spec_scope"] = "spec-exclusive" if n == 1 else "class-shared"

        self.overrides = self._dedupe(raw_ovr)
        self.triggers = self._dedupe(raw_trig)

    @staticmethod
    def _dedupe(rows: list[dict]) -> list[dict]:
        """One row per (spec, target name); the lowest anchor spellID wins."""
        best: dict[tuple[str, str], dict] = {}
        for r in sorted(rows, key=lambda r: r["anchor_spell_id"]):
            best.setdefault((r["spec_key"], _norm(r["name"])), r)
        return sorted(best.values(), key=lambda r: (r["spec_key"], r["name"]))


# ── leg B: the residual probe ────────────────────────────────────────────────
PROBE_CACHE = ABIL_DIR / "residual-probe.json"


def _load_probe() -> dict:
    """The committed `/data/wow/spell/{id}` results. Absent ⇒ no leg-B rows.

    Never fetched implicitly: generation and `--check` must stay offline and
    deterministic, so only `--probe` writes this file.
    """
    if not PROBE_CACHE.exists():
        return {"probed": "", "hits": {}, "misses": {}, "truncated": {}}
    return json.loads(PROBE_CACHE.read_text(encoding="utf-8"))


def probe(data: dict, fetched: str) -> dict:
    """GET `/data/wow/spell/{id}` for every candidate of every residual name.

    A 200 promotes the name to section 3. A 404 changes nothing — the endpoint
    covers independently-castable spellbook entries only, and Hammer of Light
    427441/427453 both 404 while being demonstrably live.
    """
    from .blizzard import get  # network + credentials; keep the import local

    names = {r["ID"]: r["Name_lang"] for r in _rows("SpellName")}
    by_norm: dict[str, list[str]] = defaultdict(list)
    for sid, nm in names.items():
        by_norm[_norm(nm)].append(sid)

    wanted = sorted({m["name"] for m in residual(data)})
    hits: dict[str, list[dict]] = {}
    misses: dict[str, int] = {}
    truncated: dict[str, int] = {}
    for name in wanted:
        cands = sorted(by_norm.get(_norm(name), []), key=int)
        if len(cands) > PROBE_CANDIDATE_CAP:
            truncated[name] = len(cands) - PROBE_CANDIDATE_CAP
            cands = cands[:PROBE_CANDIDATE_CAP]
        found, miss = [], 0
        for sid in cands:
            try:
                doc = get(f"/data/wow/spell/{sid}")
            except Exception:
                miss += 1
                continue
            found.append({"spell_id": int(sid), "live_name": doc.get("name", ""),
                          "description": (doc.get("description") or "").strip()})
        if found:
            hits[name] = found
        misses[name] = miss
        print(f"  {name:<24} {len(found)}/{len(cands)} live"
              + (f"  (+{truncated[name]} candidates not probed)" if name in truncated else ""))

    out = {"probed": fetched, "build": PINNED_BUILD, "candidate_cap": PROBE_CANDIDATE_CAP,
           "hits": hits, "misses": misses, "truncated": truncated}
    _atomic_write(PROBE_CACHE, json.dumps(out, indent=2, sort_keys=True) + "\n")
    return out


# ── the description leg ──────────────────────────────────────────────────────
DESC_CACHE = ABIL_DIR / "spell-descriptions.json"

# `$@spelldesc<id>` splices another spell's description in. Both forms occur:
# a WHOLE-text redirect (Hammer of Light 427441 is literally `$@spelldesc427453`)
# and an embedded one inside longer prose. Substitution handles both.
SPELLDESC_RE = re.compile(r"\$@spelldesc(\d+)")
# Depth cap on that substitution. Bounded and LOGGED — a silent cap would read
# as "fully resolved". Measured at 12.0.7.67808: max observed depth is 1.
DESC_REDIRECT_DEPTH = 4


def _spell_descriptions() -> dict[str, str]:
    """`Spell.Description_lang` at the pin — the raw, UNRESOLVED template text."""
    return {r["ID"]: (r["Description_lang"] or "")
            for r in _rows("Spell") if (r["Description_lang"] or "").strip()}


def _expand_redirects(text: str, raw: dict[str, str], stats: Counter,
                      api: dict | None = None, depth: int = 0,
                      seen: frozenset = frozenset()) -> tuple[str, str]:
    r"""Splice `$@spelldesc<id>` targets in. Returns (text, provenance_suffix).

    A redirect resolves against DB2 first, then against the API cache — the
    directive means "render spell <id>'s description here", so either source
    satisfies it. Measured at 12.0.7.67808: three inventory spells (Blade Flurry
    22482 → 319606, Ravager 156287 → 152277, Chakrams 259398 → 259381) redirect
    to a spell with NO `Description_lang`, and only the API leg reaches them.

    Suffix, worst-case wins so the weakest link is the one you see:

        ""                       nothing was spliced
        "+redirect"              every splice came from DB2
        "+redirect-api"          at least one splice came from the API cache
        "+redirect-unresolved"   at least one `$@spelldesc` could not be resolved

    Cycle-guarded (`seen`) and depth-capped (`DESC_REDIRECT_DEPTH`); every bound
    hit is counted into `stats` and printed by the caller, never swallowed.
    """
    if "$@spelldesc" not in text:
        return text, ""
    if depth >= DESC_REDIRECT_DEPTH:
        stats["redirect_depth_capped"] += 1
        return text, "+redirect-unresolved"
    rank = {"": 0, "+redirect": 1, "+redirect-api": 2, "+redirect-unresolved": 3}
    worst = ""

    def note(tag: str) -> None:
        nonlocal worst
        if rank[tag] > rank[worst]:
            worst = tag

    def sub(m: re.Match) -> str:
        tid = m.group(1)
        if tid in seen:
            stats["redirect_cycle"] += 1
            note("+redirect-unresolved")
            return m.group(0)
        inner = (raw.get(tid) or "").strip()
        if inner:
            out, tag = _expand_redirects(inner, raw, stats, api, depth + 1, seen | {tid})
            note(tag or "+redirect")
            return out
        live = ((api or {}).get(tid) or {}).get("description", "").strip()
        if live:
            stats["redirect_via_api"] += 1
            note("+redirect-api")
            return live
        stats["redirect_unresolved"] += 1
        note("+redirect-unresolved")
        return m.group(0)

    return SPELLDESC_RE.sub(sub, text), worst


def _redirect_targets(ids, raw: dict[str, str]) -> set[str]:
    """Every `$@spelldesc` target reachable from `ids` that DB2 cannot render.

    These are the extra spellIDs `--descriptions` must fetch: without them the
    three affected rows keep a literal `$@spelldesc319606` as their "description".
    """
    out: set[str] = set()
    stack = [(str(i), 0) for i in ids]
    seen: set[str] = set()
    while stack:
        sid, depth = stack.pop()
        if sid in seen or depth >= DESC_REDIRECT_DEPTH:
            continue
        seen.add(sid)
        for tid in SPELLDESC_RE.findall(raw.get(sid) or ""):
            if (raw.get(tid) or "").strip():
                stack.append((tid, depth + 1))
            else:
                out.add(tid)
    return out


def _load_desc_cache() -> dict:
    """The committed `/data/wow/spell/{id}` description cache.

    Absent ⇒ every row falls back to the DB2 template. Never fetched implicitly:
    generation and `--check` stay offline and deterministic, exactly like
    `residual-probe.json`. Only `--descriptions` writes this file.
    """
    if not DESC_CACHE.exists():
        return {"fetched": "", "build": "", "descriptions": {}, "misses": {}}
    return json.loads(DESC_CACHE.read_text(encoding="utf-8"))


def _describe(spell_id: int, raw: dict[str, str], api: dict, stats: Counter) -> tuple[str, str]:
    """(description, description_source) for one spell.

    Precedence: the API's RESOLVED English wins; the DB2 template is the spine
    that covers what the API cannot reach (pets, cdm-only residue, 404s).

        api                    resolved English, `GET /data/wow/spell/{id}` → 200
        db2-plain              DB2 text carrying NO `$` placeholder — readable as-is
        db2-template           DB2 text with unresolved `$…` placeholders
        …+redirect[-api|
           -unresolved]        a `$@spelldesc<id>` splice was followed — see
                               `_expand_redirects` for which source served it
        none                   neither source has text at this build
    """
    sid = str(spell_id)
    hit = api.get(sid) or {}
    text = (hit.get("description") or "").strip()
    if text:
        stats["api"] += 1
        return text, "api"
    text, suffix = _expand_redirects((raw.get(sid) or "").strip(), raw, stats, api)
    if not text:
        stats["none"] += 1
        return "", "none"
    src = ("db2-template" if "$" in text else "db2-plain") + suffix
    stats[src] += 1
    return text, src


def none_rows(data: dict) -> tuple[list[dict], list[dict]]:
    """Split the `description_source == none` rows into (stub_twins, no_twin).

    A `none` row whose NAME is also carried by a DIFFERENT spellID that DOES have
    text is a STUB TWIN: the sibling is the real button, this spellID is a hollow
    shell. Measured @ 12.0.7.67808 — Force of Nature 37846 (cd 0, class kit, in
    Feral/Guardian/Restoration) beside the real 205636 (cd 60, Balance talent),
    and Incarnation: Tree of Life 81098 (cd 0, `NameSubtext_lang` "Passive", in
    Balance/Feral/Guardian) beside the real 33891 (cd 180, Restoration talent).

    ⚠ THIS DETECTS A SUBSET, NOT ALL STUBS — see `_NONE_NOTE`. Reported, never
    acted on: dropping these rows would change the union BucketBinds consumes.
    """
    rows = [a for v in data["specs"].values() for a in v["abilities"]]
    with_text: dict[str, set[int]] = defaultdict(set)
    for a in rows:
        if a["description_source"] != "none":
            with_text[_norm(a["name"])].add(a["spell_id"])
    stub, alone = [], []
    for a in rows:
        if a["description_source"] != "none":
            continue
        twins = with_text.get(_norm(a["name"]), set()) - {a["spell_id"]}
        (stub if twins else alone).append(dict(a, twin_spell_ids=sorted(twins)))
    return stub, alone


def fetch_descriptions(data: dict, fetched: str) -> dict:
    """NETWORK: GET `/data/wow/spell/{id}` for every distinct inventory spellID.

    ⚠ A 404 IS NOT EVIDENCE OF ABSENCE — the endpoint covers independently-
    castable spellbook entries only, and Hammer of Light 427441/427453 both 404
    while being demonstrably live. A miss simply leaves the row on its DB2
    template; nothing is ever recorded as "does not exist".
    """
    from concurrent.futures import ThreadPoolExecutor

    from .blizzard import get  # network + credentials; keep the import local

    inv = {str(a["spell_id"]) for v in data["specs"].values() for a in v["abilities"]}
    extra = _redirect_targets(inv, _spell_descriptions()) - inv
    ids = sorted({int(i) for i in inv | extra})
    print(f"  {len(inv)} distinct inventory spellIDs across {len(data['specs'])} specs"
          + (f" + {len(extra)} DB2-dangling `$@spelldesc` target(s) "
             f"({', '.join(sorted(extra, key=int))})" if extra else ""))

    def one(sid: int):
        try:
            doc = get(f"/data/wow/spell/{sid}")
        except Exception as exc:
            code = getattr(getattr(exc, "response", None), "status_code", None)
            return sid, None, str(code or type(exc).__name__)
        return sid, doc, None

    descriptions: dict[str, dict] = {}
    misses: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=8) as pool:
        for n, (sid, doc, err) in enumerate(pool.map(one, ids), 1):
            if err:
                misses[str(sid)] = err
            else:
                descriptions[str(sid)] = {
                    "name": doc.get("name", "") or "",
                    "description": (doc.get("description") or "").strip(),
                }
            if n % 500 == 0:
                print(f"    {n}/{len(ids)} …")

    out = {"fetched": fetched, "build": PINNED_BUILD, "requested": len(ids),
           "descriptions": descriptions, "misses": misses}
    _atomic_write(DESC_CACHE, json.dumps(out, indent=2, sort_keys=True) + "\n")
    return out


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

    specs_out = dict(sorted(out.items()))
    walk = EffectWalk(specs_out, names)

    # ── the description leg (offline: DB2 spine + the committed API cache) ────
    raw_desc = _spell_descriptions()
    api_desc = _load_desc_cache().get("descriptions", {})
    desc_stats: Counter = Counter()
    desc_by_spell: dict[int, tuple[str, str]] = {}
    for entry in specs_out.values():
        for a in entry["abilities"]:
            sid = a["spell_id"]
            if sid not in desc_by_spell:
                desc_by_spell[sid] = _describe(sid, raw_desc, api_desc, desc_stats)
            a["description"], a["description_source"] = desc_by_spell[sid]
    # The pet annex runs on the SAME contract. The API cannot serve it — measured
    # 0/25 on a random sample of its 169 distinct spellIDs, consistent with the
    # inventory's pet leg being 0/6 — so this is the DB2 spine doing exactly the
    # job it is there for. `--descriptions` deliberately does NOT fetch these:
    # 169 GETs for a measured-zero return. They still go through `_describe`, so
    # an annex spell that IS in the cache (the shared line overlaps the
    # inventory) gets the resolved text and is tagged `api` like anything else.
    annex_stats: Counter = Counter()
    for rec in pet.rows:
        sid = rec["spell_id"]
        if sid in desc_by_spell:
            rec["description"], rec["description_source"] = desc_by_spell[sid]
            annex_stats[rec["description_source"]] += 1
        else:
            rec["description"], rec["description_source"] = _describe(
                sid, raw_desc, api_desc, annex_stats)

    desc_rows = [{"spell_id": sid, "name": names.get(str(sid), ""),
                  "description_source": src, "description": txt}
                 for sid, (txt, src) in sorted(desc_by_spell.items())]

    return {"specs": specs_out, "pet_annex": pet.rows,
            "pet_lines": pet.line_class, "trait_stats": trait.stats,
            "overrides": walk.overrides, "triggers": walk.triggers,
            "descriptions": desc_rows, "desc_stats": desc_stats,
            "annex_desc_stats": annex_stats,
            "hero_map": {trait.subtree_name.get(k, k): sorted(v, key=int)
                         for k, v in trait.hero_map.items()}}


# ── rendering ────────────────────────────────────────────────────────────────
def _scrub(s: str) -> str:
    r"""Make a value safe to drop between two tabs.

    Spell descriptions carry `\r\n` (and could carry a tab); either one written
    raw silently corrupts the file — the row grows a field or splits in two, and
    `csv.DictReader` reports it as data rather than as an error. Escaped, not
    stripped, so the paragraph breaks survive: `\` → `\\`, CRLF/CR/LF → `\n`,
    TAB → `\t`. Reverse with `s.replace('\\n', '\n')` after un-doubling `\\`.
    """
    if not ("\\" in s or "\r" in s or "\n" in s or "\t" in s):
        return s
    return (s.replace("\\", "\\\\")
             .replace("\r\n", "\\n").replace("\r", "\\n").replace("\n", "\\n")
             .replace("\t", "\\t"))


def _tsv(rows: list[dict], columns: list[str]) -> str:
    def cell(r, c):
        v = r.get(c, "")
        if isinstance(v, bool):
            return "true" if v else "false"
        if isinstance(v, list):
            return ";".join(str(x) for x in v)
        if isinstance(v, float):
            return f"{v:g}"
        return _scrub(str(v))
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


def _spec_md(entry: dict, fetched: str, desc_source: str = "") -> str:
    counts = Counter(a["origin"] for a in entry["abilities"])
    head = _front_matter(
        f"{entry['class']} {entry['spec']} — ability inventory ({PATCH})", fetched,
        [desc_source] if desc_source else [])
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
    body.append(_descriptions_md(entry))
    return head + "".join(body)


def _blockquote(text: str) -> str:
    """Multi-paragraph description as a markdown blockquote."""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    return "".join((f"> {ln}\n" if ln.strip() else ">\n") for ln in lines)


def _descriptions_md(entry: dict) -> str:
    """The `## Descriptions` section — kept OUT of the table on purpose.

    The inventory table is already 10 columns; a 200-character tooltip in an
    eleventh makes every row unreadable. The numbering here is the table's `#`,
    so the two read together.
    """
    counts = Counter(a["description_source"] for a in entry["abilities"])
    out = [
        "\n## Descriptions\n",
        "\nOne entry per row of the table above, same numbering. `description_source`"
        " says which of the two sources rendered it — **read it before quoting a"
        " number**:\n",
        "\n| source | what you are reading |\n|---|---|\n",
        "| `api` | RESOLVED English from `GET /data/wow/spell/{id}`. Durations and"
        " magnitudes are real values. |\n",
        f"| `db2-plain` | `Spell.Description_lang` @ {PINNED_BUILD} carrying no `$`"
        " placeholder — readable as-is. |\n",
        f"| `db2-template` | `Spell.Description_lang` @ {PINNED_BUILD} with"
        " **unresolved `$…` placeholders**. `$s1`, `$d`, `$?s123[a][b]` are"
        " template slots, NOT text — do not quote one as a value. |\n",
        "| `…+redirect` | built by following a `$@spelldesc<id>` splice to another"
        " spell's text. |\n",
        "| `none` | neither source has text at this build. |\n",
        "\n" + " · ".join(f"`{s}` {counts[s]}" for s in sorted(counts)) + "\n\n",
    ]
    for i, a in enumerate(entry["abilities"], 1):
        out.append(f"**{i}. {a['name']}** `{a['spell_id']}` · `{a['description_source']}`\n\n")
        out.append(_blockquote(a["description"]) if a["description"]
                   else "> _(no description text in either source at this build)_\n")
        out.append("\n")
    return "".join(out)


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
| `spell-descriptions.tsv` | **distinct spellID** | the description join table |
| `pet-family-annex.tsv` | (pet skill line, spell) | "which pet/demon gives me X" — **incl. `description`** |
| `../<class>/<spec>/ability-inventory.tsv` | ability | per-spec data, **incl. `description`** |
| `../<class>/<spec>/ability-inventory.md` | ability | reading, citing (table + `## Descriptions`) |
| `section-3-corroborated.{{tsv,md}}` | (spec, reached ability) | section 3 — reached, not joined |
| `section-4-catalogue.{{tsv,md}}` | (spec, unplaced name) | section 4 — the catalogue |
| `residual-probe.json` | residual name | leg B's cached `/data/wow/spell/{{id}}` results |
| `spell-descriptions.json` | spellID | the cached RESOLVED `/data/wow/spell/{{id}}` descriptions |

## The four sections

| # | What | Where |
|---|------|-------|
| 1 | base spell list per class/spec — **mined** | `ability-inventory.{{tsv,md}}` |
| 2 | base talent list — **mined** | same, plus `../_talents/all-talents.tsv` |
| 3 | validated but not directly joined | `section-3-corroborated.{{tsv,md}}` |
| 4 | un-mined / uncorroborated | `section-4-catalogue.{{tsv,md}}` |

Sections 1 + 2 are a **join** — a row is there because a Tier-1 table says the
spec acquires it. Section 3 is **reached**: corroborated one hop out (an
`EffectAura 332` override row, or a 200 from `/data/wow/spell/{{id}}`) with no
acquisition row naming it. Section 4 is everything still unplaced.

⚠ **Section 4 is a catalogue, not a backlog.** Nothing in it is scheduled, aged
or chased; an entry is researched when someone **asks**, or when real work needs
that specific ability — use, not age, the same rule
`projects/addon-lab/docs/lab-process.md` sets for client unknowns. Do not open a
marker, a kb-inbox line or a lab test for a row just because it sits there.

⚠ **Neither section 3 nor section 4 writes into `ability-inventory.tsv`.** Neither
produces an acquisition row, and BucketBinds reads that file as the spec's real
kit — an override target folded in silently would re-band keybinds off evidence
that never said "this spec learns this".

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
| `description_source` | which source rendered the description — **see below** |
| `description` | the tooltip text. **Per-spec `ability-inventory.tsv` only**; `all-abilities.tsv` carries `description_source` and joins to `spell-descriptions.tsv` on `spell_id` |

## Descriptions

Two Tier-1 sources, complementary. Measured at **{build}** over the 7,065
inventory rows:

| | DB2 `Spell.Description_lang` | Blizzard API `/data/wow/spell/{{id}}` |
|---|---|---|
| row coverage | **7,039 = 99.6 %**, pets **6/6** | 6,928 = 98.1 %, pets **0/6** |
| readable as-is | **no** — mostly templates | **yes**, resolved English |
| offline / build-pinned | **yes** | no — network + a committed cache |

**DB2 is the spine; the API is the rendering.** The API wins wherever it has
text, because its numbers are real values. DB2 covers what the API cannot reach:
the entire pet leg, most of the `cdm-only` residue (API 43/109) and every 404.
Each row records which source served it — **check it before quoting a number.**

| `description_source` | What you are reading |
|---|---|
| `api` | RESOLVED English. Durations and magnitudes are real values. |
| `db2-plain` | DB2 text with no `$` placeholder — readable as-is. |
| `db2-template` | DB2 text with **unresolved `$…` slots**. `$s3`, `$d`, `$?s53376&c2[…][]` are template syntax, **not text** — never quote one as a value. |
| `…+redirect` | a `$@spelldesc<id>` splice was followed (target text from DB2). |
| `…+redirect-api` | a splice resolved from the API cache instead. |
| `…+redirect-unresolved` | a splice could **not** be resolved and is left in the text verbatim. |
| `none` | neither source has text at this build (26 rows). **Not "junk" — see below.** |

⚠ `$@spelldesc<id>` means *"render spell `<id>`'s description here"* — Hammer of
Light 427441 is **literally** `$@spelldesc427453`. Splices are followed before
storing, cycle-guarded and depth-capped, and **every bound hit is printed**.

⚠ `+redirect-unresolved` is not "this spell has no description". Three spells at
{build} point at a target with no DB2 text that also 404s on the API — Blade
Flurry 22482 → 319606, Ravager 156287 → 152277, Chakrams 259398 → 259381. **A 404
is not evidence of absence**; it is a pointer this build cannot follow.

### When a row has no description

`description_source == none` is **26 rows over 12 distinct spellIDs** at {build},
and it turns out to be a **signal about the row**, not an absence of data.
`AuraDescription_lang` — the other DB2 text column — is empty for all 12 as well,
so no third source rescues them. They split in two:

| kind | rows | what it is |
|---|---|---|
| **stub twin** | 6 (2 names) | The name **is** a real ability, but *this* spellID is a hollow shell carried by specs that do not have it. The real button is a different spellID with a real cooldown and full API text. |
| hidden / internal | 20 (10 names) | Spec identity auras, an internal driver, UI plumbing, internal class-line entries. Genuinely not player-facing. |

The two measured stub twins:

| name | hollow spellID | carried by | the real button |
|---|---|---|---|
| Force of Nature | `37846` cd 0, `SkillLineAbility:798` | Feral, Guardian, Restoration | `205636` cd 60, **Balance** `talent-active` |
| Incarnation: Tree of Life | `81098` cd 0, `NameSubtext_lang` "Passive" | Balance, Feral, Guardian | `33891` cd 180, **Restoration** `talent-choice` |

The other ten names — `Frost Death Knight` 137006, `Unholy Death Knight` 137007,
`Protection Paladin` 137028, `Enhancement Shaman` 137041 (spec identity auras,
all `cdm-only` and passive-flagged), `Pyroblast Clearcasting Driver` 44448,
`Hotbar Slot 01/02` 294184 / 294189, `Energy Usage` 119650,
`Zen Pilgrimage/Death Gate/Moonglade Storage Aura I` 126893, `Shapeshift Form`
228545 — have no twin and are fairly called junk.

⚠ **It under-detects; it is not "the stub detector".** 101 names in the inventory
carry more than one spellID, and **11** of those have the stub *shape* (a cd-0
`class-baseline` member beside a cd>0 member) — but only **2 of the 11** are
`none`. The other nine (Ardent Defender, Bestial Wrath, Bladestorm, Chi Burst,
Fists of Fury, Ravager, Track Beasts, Track Humanoids, Tranquility) carry full
API text on both spellIDs and this signal is silent about them. A `none` is a
free lead, not a survey.

⚠ **Nothing is fixed from this.** Dropping a stub row changes the union
BucketBinds reads as a spec's real kit. The generator **reports** the split on
every run and stops there. Also recorded in `knowledge/_meta/kb-inbox.md`
§ *Ability inventory — `none` descriptions*.

### The pet annex

`pet-family-annex.tsv` carries `description` + `description_source` on the same
contract. The Blizzard API serves **0** of its 169 distinct spellIDs (measured on
a 25-spell random sample, consistent with the inventory pet leg's 0/6), so the
annex is entirely the **DB2 spine** — which is precisely why the spine is there.
It covers the pet abilities the prose files actually cite: Spell Lock 19647, Axe
Toss 89766. `--descriptions` deliberately does **not** fetch annex-only spellIDs
— 169 GETs for a measured-zero return.

### Why `all-abilities.tsv` carries no `description`

Measured: the text is **990 KB** spread over the 7,065 rows but **561 KB** over
the 3,949 distinct spellIDs — 43 % of it is the same tooltip repeated for a spell
several specs share. A description is a property of the **spell**, not of the
`(spec, ability)` pair, so folding it into the cross-spec grep file would roughly
double that file (905 KB → ~1.9 MB) to hold nothing new. It lives once in
`spell-descriptions.tsv`; join on `spell_id`. `description_source` **does** stay
in `all-abilities.tsv`, because coverage is genuinely per row and "how much of
origin X is only a template?" must be answerable without the join.

### TSV safety

Descriptions carry `\\r\\n` and could carry a tab; either written raw silently
corrupts a TSV — `csv.DictReader` reads the damage as data, not as an error. Every
emitted cell is escaped: `\\` → `\\\\`, CRLF/CR/LF → `\\n`, TAB → `\\t`. Reverse with
`s.replace('\\\\n', '\\n')` after un-doubling `\\\\`.

### Refreshing the API cache

```bash
uv run python -m wowkb.gen_abilities --fetched <YYYY-MM-DD> --descriptions   # NETWORK
```

~3,950 GETs against `/data/wow/spell/{{id}}` (the inventory's distinct spellIDs
plus any DB2-dangling `$@spelldesc` target), written to
`spell-descriptions.json`. **Ordinary generation and `--check` never call out** —
they read the committed cache, so both stay offline and deterministic. With the
cache absent, every row falls back to its DB2 template and the run says so.

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
  Volley, Engulf, Heroic Strike. The override walk (leg A) reaches a **few** of
  them from `SpellEffect` alone — Templar Strike 407480, Cull 1245453, Voidblade
  1245412, Condemn 317485, Kill Shot 53351 — which is why ledger gap **G2** is
  partly refuted rather than confirmed. The rest still need an in-game spellbook
  enumeration (ClientLab), not another DB2 join.
- **A button and an internal effect are not mechanically distinguishable.**
  `override` is a good signal and `trigger` is a poor one, but Hammer of Light
  arrives via `trigger` (Light's Guidance 427445 → `EffectTriggerSpell`) and is a
  real pressed button, while `override` yields cross-spec leads like Spiritbloom
  for Devastation. Hence `spec_scope` on section-3 rows, and hence section 4.
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
uv run python -m wowkb.gen_abilities --fetched <YYYY-MM-DD> --descriptions  # NETWORK
```

`--check` re-renders in memory and byte-compares. **There is no CI in this repo**
(`.github/workflows/` holds one unrelated Pages job), so `--check` is a manual /
pre-commit gate — nothing enforces it automatically.
"""


_SECTION3_PREAMBLE = """# Section 3 — corroborated, not joined

Abilities that game data **reaches** but no acquisition row **names**. Sections 1
and 2 (`../<class>/<spec>/ability-inventory.tsv`, `../_talents/all-talents.tsv`)
are a join: a row is there because a Tier-1 table says the spec acquires it.
Everything here is one hop further out, and is here because that hop is itself
Tier-1 — an override aura at the pinned build, or a live Blizzard spell endpoint.

Regenerated by `tools/wowkb/gen_abilities.py`. Data twin: `section-3-corroborated.tsv`.

## How a row got here

| `reached_by` | The evidence |
|---|---|
| `override-aura` | A `SpellEffect` row on one of this spec's talent spells carries `EffectAura == 332` (`OVERRIDE_ACTIONBAR_SPELLS`) and names this spell in `EffectMiscValue_0`. |
| `spell-endpoint` | `GET /data/wow/spell/{{id}}` returned **200** for a name `--residual` could not place. The endpoint covers independently-castable spellbook entries, so a 200 is strong positive evidence that the button is live. |

⚠ `EffectMiscValue_0` is a spell reference **only** under aura 332. Under other
auras the same column is a skill line, a mechanic or an item id — reading it
unconditionally files Dry Pork Ribs and Teleport: Goldshire as Paladin abilities.

## `spec_scope` — read this before citing an override row

| value | What it proves |
|---|---|
| `spec-exclusive` | The anchor→target pair fires for exactly **one** spec of the class. The spec attribution is as good as the evidence. |
| `class-shared` | It fires for **several** specs of the class. The ability is real and reachable from that class's talent — but **which spec presses it is not decided here.** Font of Magic 375783 lists Spiritbloom for all three Evoker specs; only Preservation has it. |

A `class-shared` row is a lead, not a spec claim. Do not copy one into a spec's
`abilities.md` as an owned button without a second source.

## What is deliberately NOT here

`EffectTriggerSpell` hits. They are a genuine spell reference every time, but
mostly to internal effects (Bloodworm, Virulent Plague, "Visual Effect: Tree of
Life"), so they go to `section-4-catalogue.md` instead. **The split is not
clean:** Hammer of Light is a real pressed button and arrives via `trigger`
(Light's Guidance 427445), not via `override`. There is no mechanical rule
separating a button from an internal effect — that is what section 4 is for.
"""

_SECTION4_PREAMBLE = """# Section 4 — the catalogue

Abilities this KB cannot put in a spec's mined inventory. Each row carries **its
provenance and nothing else**, on purpose — an explanation here would be an
unmeasured claim wearing a Tier-1 file's clothes.

Regenerated by `tools/wowkb/gen_abilities.py`. Data twin: `section-4-catalogue.tsv`.

## ⚠ "In section 4" does not mean "not in the game data"

It is easy to misread this file, and the misreading has already happened once in
a summary. A row here means **this spec's inventory could not claim it** — not
that the spell is missing, unverified, or unknown to Blizzard. Hammer of Light is
the worked example, and every clause is measured at 12.0.7.67808:

* `SpellName` carries **eight** entries for it (160420, 160426, 427441, 427453,
  429826, 1217116, 1235934, 1246643). That is why Wowhead and WoWDB find it.
* `SpellEffect` reaches it: **Light's Guidance 427445 → 427441** via
  `EffectTriggerSpell`. That row is in this file.
* `CooldownSetSpell` set **637** carries 1246643, and set 637 belongs to
  **ChrSpecialization 66 — Protection**.
* So **Protection Paladin already has it in section 1**, as
  `Hammer of Light 1246643 cdm-only`. It is *Retribution* that has no
  acquisition row, on a hero tree (Templar) the two specs share.

The precise claim a `prose-only` row makes is therefore: **no table at this build
says "this spec learns this."** Nothing more. Before treating one as an open
question, check whether a **sibling spec of the same class already carries it** —
a shared hero tree makes that likely, and it turns a vague unknown into a
specific, checkable gap.

⚠ A `trigger-effect` row is **reached**, not unreached. It is filed here only
because `EffectTriggerSpell` cannot tell a button from an internal effect.

## ⚠ This is a catalogue, not a backlog

**Nothing here is scheduled, aged, or chased.** An entry is researched when
someone **asks** about it, or when real work needs that specific ability — for
example combat-assist reading a rotation source that names one. The trigger is
**use, not age**, exactly as `projects/addon-lab/docs/lab-process.md` sets it out
for client unknowns. A long-lived row is not a debt and must not be reported as
one.

Corollary: do **not** open a `@verify-ingame` marker, a kb-inbox line or a lab
test for a row merely because it appears here. The row *is* the record.

## How a row got here

| `reached_by` | Meaning |
|---|---|
| `trigger-effect` | A `SpellEffect` row on one of this spec's talent spells names this spell in `EffectTriggerSpell`. Always a genuine spell reference; usually an internal effect rather than a button. |
| `prose-only` | The name is asserted in this spec's `abilities.md` inventory table and no leg of the union reaches it. `--residual` is the same list. |

A `prose-only` row that the probe **did** resolve is not here — it is in
`section-3-corroborated.md`. A probe **404** leaves the row here unchanged: the
endpoint covers only independently-castable spellbook entries, so a 404 is not
evidence of absence (Hammer of Light 427441 and 427453 both 404 and are live).
"""


def _section3(data: dict, probe_cache: dict) -> list[dict]:
    """Override-aura hits + residual names the spell endpoint resolved."""
    rows = []
    for h in data["overrides"]:
        rows.append({
            "class": h["class"], "spec": h["spec"], "name": h["name"],
            "spell_id": h["spell_id"], "reached_by": "override-aura",
            "spec_scope": h["spec_scope"], "anchor": h["anchor"],
            "anchor_spell_id": h["anchor_spell_id"],
            "provenance": (f"SpellEffect.EffectAura 332 on {h['anchor']} "
                           f"{h['anchor_spell_id']} @ {PINNED_BUILD}"),
        })
    hits = probe_cache.get("hits", {})
    by_slug = {(_slug(v["class"]), _slug(v["spec"])): v for v in data["specs"].values()}
    for m in residual(data):
        found = hits.get(m["name"])
        if not found:
            continue
        entry = by_slug[tuple(m["spec"].split("/"))]
        for f in found:
            rows.append({
                "class": entry["class"], "spec": entry["spec"], "name": m["name"],
                "spell_id": f["spell_id"], "reached_by": "spell-endpoint",
                "spec_scope": "", "anchor": "", "anchor_spell_id": "",
                "provenance": (f"GET /data/wow/spell/{f['spell_id']} → 200 "
                               f"\"{f['live_name']}\" (probed {probe_cache.get('probed', '?')})"),
            })
    return sorted(rows, key=lambda r: (r["class"], r["spec"], r["name"], r["spell_id"]))


def _section4(data: dict, probe_cache: dict) -> list[dict]:
    """Trigger residue + prose names the probe did not resolve."""
    rows = []
    for h in data["triggers"]:
        rows.append({
            "class": h["class"], "spec": h["spec"], "name": h["name"],
            "spell_id": h["spell_id"], "reached_by": "trigger-effect",
            "provenance": (f"reached from {h['anchor']} {h['anchor_spell_id']} "
                           f"via SpellEffect.EffectTriggerSpell @ {PINNED_BUILD}"),
        })
    hits = probe_cache.get("hits", {})
    by_slug = {(_slug(v["class"]), _slug(v["spec"])): v for v in data["specs"].values()}
    # A name ANY leg already reached is not "unreached", and must not also get a
    # prose-only row saying so — the two framings contradict each other and the
    # pessimistic one is the one a reader believes.
    #
    # ⚠ This set must include the TRIGGER rows above, not just section 3. It did
    # not, and Hammer of Light was the casualty: reached from Light's Guidance
    # 427445 via EffectTriggerSpell AND simultaneously listed as "no acquisition
    # row; endpoint returned no 200". Anything that reaches a name belongs here.
    placed = {(r["class"], r["spec"], _norm(r["name"]))
              for r in _section3(data, probe_cache)}
    placed |= {(r["class"], r["spec"], _norm(r["name"])) for r in rows}
    annex = {_norm(r["name"]): r for r in data["pet_annex"]}
    for m in residual(data):
        if hits.get(m["name"]):
            continue
        entry = by_slug[tuple(m["spec"].split("/"))]
        if (entry["class"], entry["spec"], _norm(m["name"])) in placed:
            continue
        pet = annex.get(_norm(m["name"]))
        probed = m["name"] in probe_cache.get("misses", {})
        why = f"asserted in abilities.md; no spec-keyed acquisition row at {PINNED_BUILD}"
        if pet:
            # The pet path carries NO spec granularity (see the module docstring),
            # so this is a class-level fact stated as one — not a spec claim.
            why += (f"; present in pet-family-annex.tsv on SkillLine "
                    f"{pet['skill_line']} ({pet['line_name']}) as {pet['spell_id']} "
                    f"— class-level, the pet path has no spec granularity")
        elif probed:
            why += "; spell endpoint returned no 200 — not evidence of absence"
        else:
            why += "; not yet probed"
        rows.append({
            "class": entry["class"], "spec": entry["spec"], "name": m["name"],
            "spell_id": pet["spell_id"] if pet else "", "reached_by": "prose-only",
            "provenance": why,
        })
    return sorted(rows, key=lambda r: (r["class"], r["spec"], r["name"], str(r["spell_id"])))


def _section_md(title: str, preamble: str, rows: list[dict], columns: list[str],
                fetched: str, extra_sources: list[str] = ()) -> str:
    head = _front_matter(title, fetched, extra_sources)
    body = [preamble, f"\n## Rows ({len(rows)})\n\n",
            "| " + " | ".join(columns) + " |\n",
            "|" + "|".join("---" for _ in columns) + "|\n"]
    for r in rows:
        body.append("| " + " | ".join(str(r.get(c, "")) for c in columns) + " |\n")
    return head + "".join(body)


def render_all(data: dict, fetched: str) -> dict[Path, str]:
    """Every output file as {path: content}. Rendering is pure — `--check` byte-
    compares this against disk and `main` writes it."""
    files: dict[Path, str] = {}
    all_rows = []
    desc_src = (f"Blizzard Game Data API /data/wow/spell/{{id}} (Tier 1, resolved "
                f"descriptions, fetched "
                f"{_load_desc_cache().get('fetched') or 'NOT YET'})")
    for key, entry in data["specs"].items():
        cls, spec = _slug(entry["class"]), _slug(entry["spec"])
        d = CLASSES / cls / spec
        files[d / "ability-inventory.tsv"] = _tsv(entry["abilities"], SPEC_TSV_COLUMNS)
        files[d / "ability-inventory.md"] = _spec_md(entry, fetched, desc_src)
        all_rows.extend(entry["abilities"])
    files[ABIL_DIR / "all-abilities.tsv"] = _tsv(all_rows, ALL_TSV_COLUMNS)
    files[ABIL_DIR / "spell-descriptions.tsv"] = _tsv(data["descriptions"], DESC_COLUMNS)
    files[ABIL_DIR / "pet-family-annex.tsv"] = _tsv(data["pet_annex"], ANNEX_COLUMNS)

    probe_cache = _load_probe()
    s3, s4 = _section3(data, probe_cache), _section4(data, probe_cache)
    probe_src = [f"Blizzard Game Data API /data/wow/spell/{{id}} "
                 f"(Tier 1, probed {probe_cache.get('probed') or 'NOT YET'})"]
    files[ABIL_DIR / "section-3-corroborated.tsv"] = _tsv(s3, SECTION3_COLUMNS)
    files[ABIL_DIR / "section-3-corroborated.md"] = _section_md(
        f"Section 3 — corroborated, not joined ({PATCH})", _SECTION3_PREAMBLE,
        s3, SECTION3_COLUMNS, fetched, probe_src)
    files[ABIL_DIR / "section-4-catalogue.tsv"] = _tsv(s4, SECTION4_COLUMNS)
    files[ABIL_DIR / "section-4-catalogue.md"] = _section_md(
        f"Section 4 — the catalogue ({PATCH})", _SECTION4_PREAMBLE,
        s4, SECTION4_COLUMNS, fetched, probe_src)

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
    p.add_argument("--probe", action="store_true",
                   help="NETWORK: GET /data/wow/spell/{id} for every residual name "
                        "and refresh _abilities/residual-probe.json (leg B)")
    p.add_argument("--descriptions", action="store_true",
                   help="NETWORK: GET /data/wow/spell/{id} for every inventory "
                        "spellID and refresh _abilities/spell-descriptions.json "
                        "(the resolved-English cache for the description leg)")
    p.add_argument("--json", metavar="PATH", help="dump the computed union as JSON")
    args = p.parse_args(argv)

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.fetched):
        sys.exit(f"error: --fetched must be an ISO date, got {args.fetched!r}")

    data = build()

    if args.probe:
        print("probing /data/wow/spell/{id} for every residual name …")
        out = probe(data, args.fetched)
        n = sum(len(v) for v in out["hits"].values())
        print(f"wrote {PROBE_CACHE.relative_to(ROOT)} — "
              f"{len(out['hits'])} name(s) resolved, {n} live spellID(s)")
        if out["truncated"]:
            print("  candidate cap hit (NOT probed exhaustively): " +
                  ", ".join(f"{k} +{v}" for k, v in sorted(out["truncated"].items())))
        print("  re-run without --probe to fold these into section 3")
        return 0

    if args.descriptions:
        print("fetching /data/wow/spell/{id} for every inventory spellID …")
        out = fetch_descriptions(data, args.fetched)
        blank = sum(1 for v in out["descriptions"].values() if not v["description"])
        print(f"wrote {DESC_CACHE.relative_to(ROOT)} — "
              f"{len(out['descriptions'])}/{out['requested']} resolved "
              f"({blank} returned 200 with EMPTY description), "
              f"{len(out['misses'])} not returned")
        codes = Counter(out["misses"].values())
        if codes:
            print("  not-returned by status: " +
                  ", ".join(f"{k} ×{v}" for k, v in sorted(codes.items())))
        print("  ⚠ a 404 is NOT evidence of absence — those rows keep their DB2 "
              "template (Hammer of Light 427441/427453 both 404 and are live)")
        print("  re-run without --descriptions to fold these into the inventory")
        return 0

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
    cache = _load_probe()
    s3, s4 = _section3(data, cache), _section4(data, cache)
    scope = Counter(r["spec_scope"] for r in s3 if r["reached_by"] == "override-aura")
    print(f"  section 3: {len(s3)} rows "
          f"({scope['spec-exclusive']} spec-exclusive / {scope['class-shared']} "
          f"class-shared override, "
          f"{sum(1 for r in s3 if r['reached_by'] == 'spell-endpoint')} spell-endpoint)")
    print(f"  section 4: {len(s4)} rows — a CATALOGUE, not a backlog; "
          f"researched on ask, never on age")

    # description coverage — by ROW (what a reader of a spec file sees) and by
    # origin, plus every bound the redirect walk hit. No silent caps.
    by_src = Counter(a["description_source"]
                     for v in data["specs"].values() for a in v["abilities"])
    dcache = _load_desc_cache()
    covered = rows - by_src["none"]
    print(f"  descriptions: {covered}/{rows} rows ({covered / rows * 100:.1f} %) · " +
          " ".join(f"{s} {by_src[s]}" for s in sorted(by_src)))
    per_origin = defaultdict(Counter)
    for v in data["specs"].values():
        for a in v["abilities"]:
            per_origin[a["origin"]][a["description_source"]] += 1
    for o in ORIGIN_ORDER:
        c = per_origin.get(o)
        if c:
            n = sum(c.values())
            print(f"    {o:<15} {n - c['none']}/{n} · " +
                  " ".join(f"{s} {c[s]}" for s in sorted(c)))
    stub, alone = none_rows(data)
    if stub or alone:
        print(f"    `none` ({len(stub) + len(alone)} rows): {len(stub)} are STUB TWINS "
              f"(the name's real button is another spellID with text) — " +
              ", ".join(sorted({f"{a['name']} {a['spell_id']}→{a['twin_spell_ids']}"
                                for a in stub})) or "")
        print(f"      the other {len(alone)} are hidden/internal spells with no twin: " +
              ", ".join(sorted({f"{a['name']} {a['spell_id']}" for a in alone})))
        print(f"      REPORTED, NOT FIXED — dropping a row changes the union "
              f"BucketBinds consumes. See _abilities/README.md § 'When a row has no "
              f"description'.")
    ds = data["desc_stats"]
    if ds.get("redirect_via_api"):
        print(f"    {ds['redirect_via_api']} `$@spelldesc` splice(s) resolved from "
              f"the API cache (DB2 has no text for the target)")
    for k in ("redirect_depth_capped", "redirect_cycle", "redirect_unresolved"):
        if ds.get(k):
            print(f"    ⚠ {k}: {ds[k]} — bounded at depth {DESC_REDIRECT_DEPTH}; "
                  f"those splices are LEFT IN the text as a literal "
                  f"`$@spelldesc<id>` and tagged `+redirect-unresolved`")
    ac = data["annex_desc_stats"]
    an = sum(ac.values())
    print(f"  pet annex descriptions: {an - ac['none']}/{an} rows · " +
          " ".join(f"{s} {ac[s]}" for s in sorted(ac)))
    print(f"      the DB2 spine carries {an - ac['none'] - ac['api']} of them; the API "
          f"reaches {ac['api']} (only where an annex spell is ALSO in the inventory "
          f"and so in the cache — annex-only spellIDs are not fetched, measured 0/25)")
    if not dcache.get("fetched"):
        print("  ⚠ spell-descriptions.json absent — every row is on its DB2 "
              "TEMPLATE (placeholders unresolved). Run --descriptions (network).")
    if not cache.get("probed"):
        print("  ⚠ residual-probe.json absent — leg B contributed nothing. "
              "Run --probe (network) to fill it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
