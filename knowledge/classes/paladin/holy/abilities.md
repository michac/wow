---
title: Holy Paladin — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree
  - ../../_abilities/spell-descriptions.tsv  # tier 1 — resolved Blizzard spell-API tooltips, fetched 2026-08-06
  - ../../_abilities/section-4-catalogue.tsv  # tier 1 derived — the unreached-name catalogue
  - ../../_abilities/reconcile-ledger.md  # tier 1 adjudication of this file's earlier claims
confidence: high
---

# Holy Paladin — off-inventory abilities

**Everything about a Holy ability is in `ability-inventory.md`** — 206 rows, one
row each carrying spellID, cooldown, cast time, origin, talent/hero placement and
the full tooltip. It is generated, Tier-1, DB2-pinned to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Holy ability is not named below, do not research it — read its row in
> `ability-inventory.md` and go.** Rotation → `rotation.md`. Talents/hero pick →
> `builds.md`. Both sections here are **closed lists, not backlogs.**

⚠ One caveat the inventory cannot flag: its **46 `class-baseline` rows are the
whole Paladin skill line, not Holy's bar** — mounts, Protection's Ardent Defender
and Eye of Tyr, Retribution's Wake of Ashes. `SkillLineAbility:800` is a *class*
attachment; nothing generated filters it to a spec.

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
| — | Sacred Weapon | **One of the two outputs of `Holy Armaments` `432459`** (talent-active, Lightsmith subtree, node 95234), which alternates them: that spell's Tier-1 resolved tooltip ends *"Becomes Sacred Weapon after use."* No spell **named** Sacred Weapon attaches to a trait node, skill line, `SpecializationSpells` or `PvpTalent` row — 432472 / 432502 / 432616 / 432757 / 441590 all attach to nothing *(`reconcile-ledger.md`)* — so the join can never emit it. The other half, **Holy Bulwark**, *does* appear, as a `cdm-only` row on the same spellID 432459. Catalogued `prose-only` in `section-4-catalogue.tsv`. ⚠ A spell-API 404 is **not** evidence of absence. |
| — | Concentration Aura | **Granted by the class-tree talent `Auras of the Resolute` `385633`** (node 102587, all three Paladin specs in `all-talents.tsv`), whose Tier-1 resolved tooltip reads *"**Learn Concentration Aura**, Devotion Aura, and Crusader Aura … Concentration Aura: Interrupt and Silence effects on party and raid members within 40 yds are 30% shorter."* `Aura Mastery` `31821` still carries a *"Concentration Aura: Affected allies immune to interrupts and silences"* clause. The aura has **no acquisition row of its own** (79963 / 81455 / 317920 / 344220 attach to nothing) — Devotion, Crusader and Retribution Aura each have a `class-baseline SkillLineAbility:800` row and this one does not, which is exactly why the join misses it. **This reverses the old "not acquirable" verdict — see Corrections.** |

## §B — Encountered, and we believe not valid

Names that appear in guides, older builds or other people's notes, which we have
checked and believe are **not** part of this spec at 12.0.7. Listed so the next
reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| Barrier of Faith | **not acquirable at 12.0.7** | 148039 / 388536 / 395180 attach to no trait node, skill line, `SpecializationSpells` or `PvpTalent` row; the name is absent from `all-talents.tsv` for **every** spec of every class; the live Holy spec tree carries **Seraphic Barrier** `1241714` (node 102579, row 20 col 11) where it used to sit. Do not author it as a live talent. |

*[Tier 1: `all-talents.tsv` + `ability-inventory.tsv` @ 12.0.7.67808;
adjudication in `../../_abilities/reconcile-ledger.md`.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **`Concentration Aura` is acquirable at 12.0.7 — the old verdict was wrong.**
  Every Paladin `abilities.md`, `reconcile-ledger.md` (Holy L93 / Protection L80 /
  Retribution L81) and `../../_abilities/prose-conventions.md` §6 currently state
  *"Concentration Aura is not acquirable at 12.0.7"* — prose-conventions even uses
  it as its worked example of a negative claim. The measurement behind it is
  sound (no spell of that name attaches to anything) but the **conclusion does not
  follow**: the aura is granted by a *talent*, `Auras of the Resolute` `385633`,
  whose live API tooltip names it with a current value. See §A. The "swap to
  Concentration on interrupt-heavy pulls" advice is **not** dead.
- Earlier revisions of this file guessed cooldowns and resource costs from Tier-3
  guides and marked each guess `@verify-ingame`. Every one of those numbers is in
  `ability-inventory.md`, measured. **Do not re-introduce a guessed number here.**

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact cooldown / cost
is uncertain"* is **not** one: `ability-inventory.md` carries the Tier-1 number.
