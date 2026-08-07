---
title: Marksmanship Hunter — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ../../_abilities/reconcile-ledger.md  # tier 1 derived — gaps G3 (SkillLine 183) and G5 (pet path)
  - ../../_abilities/section-3-corroborated.tsv  # tier 1 — the Takedown override link
  - ../../_abilities/pet-family-annex.tsv  # tier 1 — pet skill lines @ 12.0.7.67808
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree
confidence: high
---

# Marksmanship Hunter — off-inventory abilities

**Everything about a Marksmanship ability is in `ability-inventory.md`** — 195
rows, each carrying spellID, cooldown, cast time, origin, talent/hero placement
and the full tooltip. It is generated, Tier-1, DB2-pinned to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Marksmanship ability is not named below, do not research it — read
> its row in `ability-inventory.md` and go.** Rotation → `rotation.md`.
> Talents/hero pick → `builds.md`. Both sections here are **closed lists, not
> backlogs.**

## §A — Real buttons the inventory cannot see

Confirmed to exist and be pressable, but no spec-keyed acquisition table names
them, so they will never appear in `ability-inventory.tsv`. **Absence there is
not absence in game.**

> ⚠ **This section is a machine input.** `wowkb.gen_abilities` harvests the
> `name` column of the table below — the heading is matched on the word
> **`inventory`** — and feeds it to the `prose-only` leg of
> `section-4-catalogue.md`. Rename this heading or drop the `name` column header
> and these rows **silently vanish from the catalogue**, with no marker and no
> warning. §B is deliberately *not* harvested: it asserts the opposite.

| spellID | name | how we know, and why the join misses it |
|---|---|---|
| `75` | Auto Shot | Real and castable. `SkillLineAbility` on SkillLine **183 "GENERIC (DND)"**, which is outside the generator's two closed skill-line allowlists — so it is invisible for *every* Hunter spec. A **tool gap**, not a removal (ledger gap **G3**). No `@verify-ingame` on purpose: logging in cannot answer which DB2 skill line a generator reads. |
| `883`, `83242`–`83245` | Call Pet 1 … Call Pet 5 | ⚠ **This `name` string looks like a harvest artifact** — it is range notation, not a live spell name. Reproduced verbatim under rule R1; a separate deliberate pass owns fixing it, and this row must not be split or reworded here. The underlying reality: all **five** spells (`Call Pet 1` 883, `Call Pet 2` 83242, `Call Pet 3` 83243, `Call Pet 4` 83244, `Call Pet 5` 83245) **are** in `ability-inventory.tsv` as `class-baseline` / `SkillLineAbility:795`. Baseline means the *summon* is always available; what MM chooses is whether to run a pet at all (`Unbreakable Bond`) or go Lone Wolf. Note the Tier-1 tooltip on `Spotter's Mark` 1219616 opens *"Replaces Call Pet"* — the Spotting Eagle takes that button. |

Also invisible per-spec because the pet path carries **no spec granularity in any
DB2 table** (ledger gap **G5**), and recorded in
`../../_abilities/pet-family-annex.tsv` rather than here: the shared Hunter pet
line **270 "Pet - Generic Hunter"** (`Growl` 2649, `Dash` 61684, `Intimidation`
24394, …). Read the annex before concluding a pet button does not exist.

⚠ **`Primal Rage` is not a Marksmanship row.** MM's Lust is `Harrier's Cry`
466904 — `class-baseline` / `SpecializationSpells`, 360s — and it **is** in
`ability-inventory.tsv`, so it is not an off-inventory ability. ⚠ Measured
2026-08-06: at 12.0.7.67808 Harrier's Cry joins to **Marksmanship only** — it is
in no other Hunter spec's `ability-inventory.tsv` — so "every Hunter brings Lust
baseline" is **not** what the data currently says. Unresolved; do not restate the
class-wide claim from this file.

## §B — Encountered, and we believe not valid

Names that appear in guides, older builds or other people's notes, which we have
checked and believe are **not** part of this spec at 12.0.7. Listed so the next
reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| Muzzle | **Survival's, not reachable from here** | `all-talents.tsv`: node 79837, class tree, gated by TraitCond → SpecSet to **hunter/survival only**. MM's kick is `Counter Shot` 147362 (node 102402, gated Marksmanship), already in `ability-inventory.tsv`, and it is the only one MM has. |
| Takedown | **Survival's; the section-3 row is join residue** | `all-talents.tsv` has one Takedown node — 109323, spec tree, **hunter/survival only**. ⚠ It nevertheless appears in an **MM** row of `section-3-corroborated.tsv` as `override-aura` reached from `Moonlight Chakram` 1264946. That link is `class-shared` — an override relation between two spells, **not** an acquisition row — so it is not evidence MM can press Takedown. |

*[Tier 1: `all-talents.tsv` + `ability-inventory.tsv` + `section-3-corroborated.tsv`,
all @ DB2 12.0.7.67808; verdicts recorded in `../../_abilities/reconcile-ledger.md`.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **`Kill Shot` 53351 is `talent-active`, not baseline.** It is a spec-tree node
  (109490), so a loadout can genuinely arrive without an execute. An earlier
  revision of this file called it baseline.
- **`Sentinel's Mark` is real** — do not file it as a removed/renamed name. It
  has no acquisition row because it is a *buff*, not an acquirable ability;
  Tier-1 API tooltips for `Sentinel` 1253599, `Lunar Storm` 1253732 and
  `Don't Look Back` 450373 all name it. Acquisition tables never list auras.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact cooldown / Focus
cost is uncertain"* is **not** one: `ability-inventory.md` carries the Tier-1
number.
