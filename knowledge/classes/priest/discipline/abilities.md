---
title: Discipline Priest — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree @ 12.0.7.67808
  - ../../_abilities/reconcile-ledger.md  # tier 1 adjudication of this file's earlier claims @ 12.0.7.67808
confidence: high
---

# Discipline Priest — off-inventory abilities

**Everything about a Discipline ability is in `ability-inventory.md`** — 164 rows,
one row each carrying spellID, cooldown, cast time, origin, talent/hero placement
and the full tooltip. It is generated, Tier-1, DB2-pinned to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Discipline ability is not named below, do not research it — read its
> row in `ability-inventory.md` and go.** Rotation → `rotation.md`. Talents/hero
> pick → `builds.md`. Both sections here are **closed lists, not backlogs.**

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
| — | Void Shield | **A Power Word: Shield override**, so it has no acquisition row of its own — an override button is never *learned*, it replaces one you already have. The granting talent **`Master the Darkness` `1253590`** *is* in the inventory (`talent-passive`, spec tree) and its Tier-1 tooltip carries the whole button: *"Penance has a high chance to upgrade Power Word: Shield into Void Shield.\n\n Void Shield:\nShields 3 allies for 15 sec, absorbing 2,607 damage."* Corroborated by Oracle's `Unfolding Vision` `1272363`, which also names it. Eight Midnight-range IDs (`1213562`…`1293007`) exist in `SpellName`@67808 with no attachment. |

**This category is real and measured, not an edge case.** Across all 40 specs,
runtime override / proc-replacement buttons live in no spec-keyed DB2 table:
`Devour`, `Pierce the Veil`, `Templar Slash`, `Void Volley`, `Void Shield` and
`Heroic Strike` are all real pressed buttons whose *only* record anywhere is a
hand-written row like this one.

⚠ **Void Shield's numbers are no longer an open question.** An earlier revision of
this file carried an `@verify-ingame` on them; the answer was sitting in the
sibling inventory's `Master the Darkness` tooltip the whole time. **Settled. Do
not re-open.**

## §B — Encountered, and we believe not valid

Names that appear in guides, older builds or other people's notes, which we have
checked and believe are **not** part of this spec at 12.0.7. Listed so the next
reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| Premonition | **removed — the button is gone** | `Premonition` appears **nowhere** in `all-talents.tsv` for **any** of the 40 specs, and nowhere in Discipline's inventory. The four spells of that name (`188779`/`428924`/`443056`/`450796`) are all TWW-era and attach to no trait node, `SkillLineAbility`, `SpecializationSpells` or `PvpTalent`. **Oracle is still live** on the Priest tree (**795**) and still the default hero pick — it now carries `Prophet's Insight`, `Prophet's Will`, `Piety`, `Twinsight` (+ `Assured Safety`, `Preemptive Care`, `Save the Day`, `Unfolding Vision`, `Words of the Wise`…). No Premonition node and no `Premonition of *`. |
| Silence | **Shadow's, not Discipline's** | `Silence` `15487` appears in **`priest/shadow/ability-inventory.tsv` only** (`class-baseline`) and in neither Discipline's nor Holy's. **Discipline has no interrupt and no school lockout** — a real gap to plan group composition around, and one a generated inventory structurally cannot state, because it lists what *is*. |
| battle rez (Rebirth / Raise Ally / Intercession / Soulstone) | **Priest has none, in any spec** | zero rows matching those four names across all three Priest inventories. `Resurrection` `2006` and `Mass Resurrection` `212036` are both out-of-combat. |

*[Tier 1: `all-talents.tsv` + the three Priest `ability-inventory.tsv` files, both
@ 12.0.7.67808; adjudicated in `../../_abilities/reconcile-ledger.md`.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **`builds.md` is stale on Oracle and contradicts §B above.** Its hero-tree
  section still sells Oracle on a *"**Premonition** toolkit for reactive
  throughput/defense"*. That button does not exist at 12.0.7 (§B, Tier-1). Oracle
  remains the recommended default — the reason given for it is what is wrong.
  **This file wins; `builds.md` has not been edited.**
- **Shadow Word: Pain is `class-baseline`, Shadowfiend is `talent-active`** — an
  earlier revision had these exactly the wrong way round. Both origins are now in
  the generated inventory; read them there.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact cooldown / cost
is uncertain"* is **not** one: `ability-inventory.md` carries the Tier-1 number.
