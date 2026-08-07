---
title: Vengeance Demon Hunter — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ../../_abilities/reconcile-ledger.md  # tier 1 derived — the DH verdicts, §4 + §5 G1/G2
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree @ 12.0.7.67808
  - ../../_abilities/all-abilities.tsv  # tier 1 — the 40-spec acquisition union
confidence: high
---

# Vengeance Demon Hunter — off-inventory abilities

**Everything about a Vengeance ability is in `ability-inventory.md`** — 155 rows,
each carrying spellID, cooldown, cast time, origin, talent/hero placement and the
full tooltip. It is generated, Tier-1, DB2-pinned to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Vengeance ability is not named below, do not research it — read its row
> in `ability-inventory.md` and go.** Rotation → `rotation.md`. Talents/hero pick
> → `builds.md`. Both sections here are **closed lists, not backlogs.**

## §A — Real buttons the inventory cannot see

Confirmed to exist and be pressable, but no spec-keyed acquisition table names
them, so they will never appear in `ability-inventory.tsv`. **Absence there is not
absence in game.**

> ⚠ **This section is a machine input.** `wowkb.gen_abilities` harvests the `name`
> column of the table below — the heading is matched on the word **`inventory`** —
> and feeds it to the `prose-only` leg of `section-4-catalogue.md`. Rename this
> heading or drop the `name` column header and these rows **silently vanish from
> the catalogue**, with no marker and no warning. §B is deliberately *not*
> harvested: it asserts the opposite.

| spellID | name | how we know, and why the join misses it |
|---|---|---|
| `1283344` | Reaver's Glaive | Aldrachi Reaver's proc button: **Art of the Glaive** `442290` is `talent-passive` in this spec's tsv, subtree 35, live on tree 854, and converts your next `Throw Glaive` `185123` into it. A runtime override / granted proc has no acquisition row of its own, so no join can reach it — tool gap **G2**, identical to Havoc's row. `1283344` is a Midnight-range `SpellName` ID. ⚠ The maxroll captures in this folder link `442294`, a War Within-era ID; **Tier 1 is the floor, so `1283344` is the one to carry.** |

**Vengeance gets off lightly with one.** Havoc's whole demon-form kit is in this
category (five rows) and Devourer's transform buttons are three more — the same
`G2` hole, not a spec-specific defect.

## §B — Encountered, and we believe not valid

Checked, and believed **not** part of this spec at 12.0.7. Listed so the next
reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| Shear | **retired name that still appears in a live tooltip** | Zero rows in `all-talents.tsv` and `all-abilities.tsv` for **any** of the 40 specs @ `12.0.7.67808`. It survives only inside the Aldrachi Reaver tooltip text this spec inherits — Art of the Glaive, Reaver's Mark and Fury of the Aldrachi all say "Shear". The Midnight builder those tooltips actually mean is **Fracture** `263642` (`class-baseline`), paired with `Soul Cleave` `228477`. Do not go looking for a Shear button. |
| Bulk Extraction | **replaced** | Zero rows in `all-talents.tsv` and `all-abilities.tsv` for any spec @ `67808`. Its Midnight successor is `Sigil of Spite` `390163`, which is present in this spec's tsv as `talent-active` (node `90978`) and is the fragment-burst button. |
| Fel Rush | **suspected join over-report, not a Vengeance button** | It enters this spec's inventory via `SkillLineAbility:1848`, the Demon Hunter **class** skill line, which carries no spec granularity — the same join hands Fel Rush to all three specs. Vengeance's real movement button is `Infernal Strike` `189110` (`SpecializationSpells`), which sits in the tsv alongside it. The open in-game question is tracked on the Devourer file, which has the same shape. |

*[Tier 1: `all-talents.tsv` + `all-abilities.tsv` @ `12.0.7.67808`, plus
reconcile-ledger §4.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **Spirit Bomb now carries a real 25s cooldown** (haste-reduced) — it is no
  longer a pure fragment-dump, which is the single biggest change to how the AoE
  loop is played. Tier 1 in the generated inventory; an earlier revision guessed
  it and marked it. The rotational consequence belongs to `rotation.md`.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact Fury value or
cooldown is uncertain"* is **not** one: `ability-inventory.md` carries the Tier-1
number for every row it has.
