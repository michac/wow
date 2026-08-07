---
title: Reading the ability layer — the traps, and what it cannot tell you
patch: 12.0.7
build: 12.0.7.67808
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - knowledge/classes/_abilities/README.md  # tier 1 derived — the generated layer's schema and join model
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 derived — the per-row adjudication, and §5 G6
  - tools/wowkb/gen_abilities.py  # the generator, and the §A harvester
confidence: high
---

# Reading the ability layer

**Hand-written. Not generated** — unlike its neighbour `README.md`, which
`wowkb.gen_abilities` writes.

Two files per spec:

| file | what | generated? |
|---|---|---|
| `<class>/<spec>/ability-inventory.md` / `.tsv` | **every** ability the spec can have — one row each with spellID, cooldown, cast time, origin, tree/hero placement and the resolved tooltip | **yes**, DB2-pinned to `12.0.7.67808` |
| `<class>/<spec>/abilities.md` | **only** what the generated file structurally cannot say — §A real buttons it cannot see, §B names encountered and believed invalid | no |

**Read the generated row first. If it answers you, stop.** This file exists for
the cases where it is silent or misleading, and every one of those below is
measured, not theorised.

---

## 1. The floor, and its one systematic error

The generated inventory is a **join**: a row exists because a Tier-1 acquisition
table says the spec **learns** the spell. So it is authoritative for what it
carries, and it can only ever list what **is**.

⚠ **Absence from it is not absence in game.** Runtime override and
proc-replacement buttons live in **no spec-keyed DB2 table** at 12.0.7.67808 —
`Devour`, `Pierce the Veil`, `Templar Slash`, `Void Volley`, `Heroic Strike`,
`Crushing Blow`, `Necrotic Coil` are all real pressed buttons whose only record
anywhere is a hand-written §A row. That is what §A is for.

## 2. `cooldown` is wrong for charge abilities

It is `SpellCooldowns` at DifficultyID 0, i.e. `max(RecoveryTime,
CategoryRecoveryTime)`. For a **charge** ability that returns the **GCD** — Fire
Blast `0.5`, Purifying Brew `1`. The real recharge is
`SpellCategory.ChargeRecoveryTime`, unreachable without breaking the build pin
(`reconcile-ledger.md` §5, gap **G6**). **194 rows** across the 40 specs read 0
or sub-10s for this reason.

⚠ It has teeth: for Holy Priest the Holy Word charge cadence *is* the rotation,
and both Holy Words read `cooldown = 0`. Measured related case: `Shiv 5938` reads
`0` while `Toxic Stiletto`'s own tooltip says its cooldown is *"reduced by 15
sec"* — so the base is not 0 and no reachable table carries it.

## 3. `cast_time` is the BASE cast, and a channel reads 0.0

`SpellMisc.CastingTimeIndex` → `SpellCastTimes.Base`. **94.3 %** of inventory
spellIDs are instant; only 226 carry a number.

- Not haste-adjusted, and not adjusted by a talent that shortens a cast.
- **A channel reads `0.0`** — Divine Hymn, Tranquility, Mind Flay and Penance all
  do. Channel length is `SpellDuration` via `DurationIndex`, a table we do not
  join. Read `0.0` as *"no cast time"*, never *"no cast bar"*. (39 of 52
  channel-flagged spells do state their duration inside the tooltip text.)

## 4. There is no `cost` column, deliberately

Measured over the 3,949 distinct inventory spellIDs: only **487 (12.3 %)** have
any `SpellPower` row, **406 of those are Mana**, **155 of the 624 rows are gated
on `RequiredAuraSpellID`** (a *conditional* cost — a talent or buff changes it),
and **81 spellIDs carry more than one cost row**. A generated cost column would
be mostly empty, dominated by irrelevant mana values, and ambiguous on a quarter
of what it did cover. Resource costs are **not recorded anywhere** in this layer.
Full measurement: `todo/ability-inventory-rollout.md` §3-B1.

## 5. A tooltip can be resolved and still be wrong

`description_source: api` means the text was **resolved**, not that it is
**current** or **yours**. Two measured failure modes:

- **Wrong spec's branch.** The API resolves `$?spec[…]` conditionals *without
  spec context*, so a shared hero-tree passive can render a sibling's text.
  Confirmed: Protection Warrior's `Burst of Power 437118` and `Thunder Blast
  435607` both name **Bloodthirst**, which is Fury's.
- **Stale text from Blizzard.** `Art of the Glaive`, `Reaver's Mark` and `Fury of
  the Aldrachi` all say **"Shear"** in both Havoc's and Vengeance's generated
  inventories — and `Shear` exists in no acquisition table for any spec at
  12.0.7. Havoc's copy also references casting `Sigil of Spite`, which is
  Vengeance-only.

## 6. `node_type` is not a castability signal

`all-talents.tsv`'s `node_type` describes the **node**, not the granted spell. It
reads `ACTIVE` for spells the inventory correctly types `talent-passive` /
`castable=false`. Independently hit on four classes: Druid (`Wild Guardian`,
`Ascendant Eclipses`, `Unseen Predator`, `Everbloom`), Priest (`Master the
Darkness`), Paladin (`Auras of the Resolute`), Warrior (`Master of Warfare`,
`Rampaging Berserker`). **The resolved tooltip is what settles it.**

## 7. The class line over-reports, and it has no spec granularity

`SkillLineAbility` attaches to a **class**, so a spec inherits its whole class
line. Retribution's inventory carries all 44 Paladin class-line rows — 11 mounts,
8 Holy spells, 2 Protection spells, Sense Undead. Measured cross-spec case:
`Fel Rush 344865` is handed to Devourer, Havoc **and Vengeance** off
`SkillLineAbility:1848`, and Vengeance demonstrably does not have it.

The class line also carries **dead rows** (Sense Undead, Contemplation), so
presence there is not proof of liveness either.

## 8. The pet path has NO spec granularity at all

Not in `SkillLine`, `SkillLineAbility`, `SkillRaceClassInfo` or `CreatureFamily`.
Every pet claim is **class-level**, so no pet button can ever be attributed to a
spec by the join — yet several are buttons you press constantly:

| class | pet buttons invisible to the join |
|---|---|
| Warlock | `Axe Toss 89766` (Felguard), `Spell Lock 19647` + `Devour Magic 19505` (Felhunter) — **the spec's only interrupt** |
| Death Knight | `Gnaw 47481`, plus `Leap`, `Huddle`, `Claw`, `Monstrous Blow`, `Shambling Rush`, `Putrid Bulwark`, `Sweeping Claws` |
| Hunter | `Growl 2649`, `Dash 61684`, `Intimidation 24394`, `Primal Rage 264667` |
| Mage | `Freeze 33395` (Water Elemental) |

`pet-family-annex.tsv` is the Tier-1 record. ⚠ **This catalogue is incomplete** —
a §A row exists only where someone happened to write the button down. Absence of
a pet button from §A means nobody catalogued it, not that it doesn't exist.

## 9. Section 3 is *reached*, not *acquired* — and it leaks across specs

`section-3-corroborated.tsv` records a spell reached one hop out via
`SpellEffect` (an `EffectAura 332` override, or a 200 from the spell endpoint).
A `class-shared` row proves the **class** can reach it, **not that this spec
presses it.** Measured leaks: `Dispatch 2098` attributed to Subtlety (it is the
Outlaw finisher), `Spiritbloom 367226` to all three Evoker specs off a `Font of
Magic` effect row its live tooltip no longer describes, and
`Kill Shot` / `Takedown` / `Trueshot` cross-attributed among the Hunter specs.

⚠ **Neither section 3 nor section 4 is a backlog.** An entry is researched when
someone **asks**, or when real work needs that specific ability — never because
it has sat there. Same use-not-age rule as `projects/addon-lab/docs/lab-process.md`.

## 10. Evidence rules that have each cost someone a session

- **A `SpellName` hit is not evidence a spec can cast something.** That table
  keeps retired spells indefinitely.
- **A spell-API 404 is not evidence of absence.** `Hammer of Light` 427441 and
  427453 both 404 and are demonstrably live.
- **"Absent from `all-talents.tsv`" is not evidence against an aura or a buff.**
  `Sentinel's Mark` has no talent node and no inventory row because it is a
  *buff* — but it is real, named by Tier-1 tooltips on `Sentinel 1253599`.
- **A talent can grant an ability that has no row of its own.** ⚠ *"Concentration
  Aura is not acquirable at 12.0.7"* was asserted across five files and is
  **FALSE**: `Auras of the Resolute 385633` is a class-tree node for all three
  Paladin specs whose tooltip reads *"**Learn Concentration Aura**, Devotion
  Aura, and Crusader Aura…"*. The underlying measurement (spells 79963 / 81455 /
  317920 / 344220 attach to nothing) was right; the conclusion drawn from it was
  not. **Measuring an absence and concluding a removal are different steps.**
- **Before calling anything absent, check a sibling spec of the same class.** A
  shared hero tree or class line makes a one-sided gap likely — Hammer of Light
  is absent for Retribution and present for Protection.

## 11. §A is a machine input

`gen_abilities._inventory_names()` harvests the `name` column of the table under
the heading **`## §A — Real buttons the inventory cannot see`** (matched on the
word `inventory`) and feeds it to the `prose-only` leg of `section-4-catalogue`.

- **Do not rename that heading**, and keep the `| spellID | name | … |` header —
  a name deleted from that column silently disappears from the catalogue, with no
  marker and no warning.
- **§B must not contain `inventory` or `notes` in its heading.** It asserts the
  opposite; harvesting it would record "not an ability" as "an asserted ability".
- Before restructuring an `abilities.md`, diff `_inventory_names()` across the
  change. That check caught two silent losses during the 2026-08-06 rollout.
