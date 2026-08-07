---
title: Fury Warrior — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ../../_abilities/reconcile-ledger.md  # tier 1 derived — the Warrior/fury TOOL-GAP verdict + §5 G2
  - ../../_abilities/section-4-catalogue.tsv  # tier 1 derived — the prose-only leg this file feeds
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree @ 12.0.7.67808
  - ../arms/ability-inventory.tsv  # tier 1 — sibling-spec cross-check for the §B verdicts
  - ../protection/ability-inventory.tsv  # tier 1 — sibling-spec cross-check for the §B verdicts
confidence: high
---

# Fury Warrior — off-inventory abilities

**Everything about a Fury ability is in `ability-inventory.md`** — 155 rows, one
each carrying spellID, cooldown, cast time, origin, talent/hero placement and the
full tooltip. It is generated, Tier-1, DB2-pinned to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Fury ability is not named below, do not research it — read its row in
> `ability-inventory.md` and go.** Rotation → `rotation.md`. Talents/hero pick →
> `builds.md`. Both sections here are **closed lists, not backlogs.**

## §A — Real buttons the inventory cannot see

Confirmed to exist and be pressable, but no spec-keyed acquisition table names
them, so they will never appear in `ability-inventory.tsv`. **Absence there is not
absence in game.**

> ⚠ **This section is a machine input.** `wowkb.gen_abilities` harvests the `name`
> column of the table below — the heading is matched on the word **`inventory`** —
> and feeds it to the `prose-only` leg of `section-4-catalogue`. Rename this
> heading or drop the `name` column header and these rows **silently vanish from
> the catalogue**, with no marker and no warning. §B is deliberately *not*
> harvested: it asserts the opposite.
>
> ⚠ **This file was dark to that harvester until now.** Its ability tables sat
> under headings the matcher never hit, so `Crushing Blow` contributed nothing to
> `section-4-catalogue.tsv` — the Warrior/Fury rows there are all `trigger-effect`
> ones the generator found by itself. Under this heading the row starts counting.

| spellID | name | how we know, and why the join misses it |
|---|---|---|
| `1215563`, `1270646` | Crushing Blow | **The Recklessness-window override of `Raging Blow`.** The mechanism is stated by Tier 1 *inside this spec's own inventory*: `Reckless Abandon` `396749` (`talent-passive`, spec tree node 90388) reads *"Activating Recklessness generates 50 Rage and while Recklessness is active, Raging Blow and Bloodthirst are upgraded to **Crushing Blow** and Bloodbath."* The upgraded button is never *learned* — it replaces `Raging Blow` on the bar for the window — so no `SpecializationSpells` / `SkillLineAbility` / `TraitNodeEntry` row can name it and the join emits nothing. Both IDs are Midnight-range `SpellName` entries with **no** acquisition row (`reconcile-ledger` → Warrior/fury: verdict **TOOL-GAP**, class **G2**). Its parent `Raging Blow` `85288` is live on the Midnight Warrior tree *[Tier 1]*. ⚠ **Do not reason from `Bloodbath`.** The *other half of the same sentence* behaves differently: `Bloodbath 113344 class-baseline SkillLineAbility:840 castable=true` **is** in the inventory. Same mechanic, different DB2 treatment — so Bloodbath's presence is no argument that Crushing Blow's absence means it isn't real. |

**This category is real and measured, not an edge case.** `reconcile-ledger` §5 G2
counts ~19 such buttons across the 40 specs — `Devour`, `Templar Slash`,
`Void Volley`, `Heroic Strike`, `Crushing Blow` — every one a pressed button whose
only record is a hand-written row like this one. Delete the row and the ability
leaves the KB.

## §B — Encountered, and we believe not valid

Names that appear in guides, older builds or other people's notes, which we have
checked and believe are **not** part of this spec at 12.0.7. Listed so the next
reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| Thunderous Roar | **not in current game data at all** | **zero** rows for the name in `all-talents.tsv` (all 40 specs, every tree) and zero in any of the three Warrior `ability-inventory.tsv` files. A pre-Midnight Warrior talent; gone at 12.0.7, not merely off Fury's tree. |
| Onslaught | **not a Warrior ability** | zero rows named exactly `Onslaught` in any Warrior inventory or in the Warrior legs of `all-talents.tsv`. The only `Onslaught` in `all-talents.tsv` is **Evoker** Scalecommander's passive `441245`. Warrior has `Unrelenting Onslaught` `444780` — a Slayer hero *passive*, present for Arms and Fury — which is what guides using the short name are pointing at. |
| Protection Stance | **not a spell at 12.0.7** | zero hits in `all-talents.tsv` and in all three Warrior inventories. Fury's damage-reduction stance is **`Defensive Stance` `386208`** — a `talent-active` class-tree node (entry 114644) for all three specs. The BucketBinds seed's "Protection Stance" is this. |

*[Tier 1: `all-talents.tsv` + the three Warrior `ability-inventory.tsv` files,
both @ 12.0.7.67808.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **`Ravager` IS a Fury ability.** An earlier revision asserted *"Thunderous Roar,
  Ravager, and Onslaught are NOT in the Fury tree"*. Two of three hold (above);
  `Ravager` does not — `ability-inventory.tsv` carries **`Ravager 156287
  class-baseline SkillLineAbility:840 castable=true`**. What is true is that it is
  not a *talent node* for Fury: `all-talents.tsv` has `Ravager 228920` only as an
  Arms and a Protection choice node. **Different spellID, different acquisition
  path** — which is almost certainly how the negative got written. Do not re-assert
  it.
- **`Berserker Rage` and `Berserker Shout` are two live spells, not a rename.**
  This file said Berserker Shout was "the Midnight delivery of Berserker Rage".
  Tier 1 has both, in all three Warrior inventories: `Berserker Rage 18499`
  (`class-baseline`, castable) **and** `Berserker Shout 384100` (`talent-choice`,
  60s, vs `Fearless`).
- **`all-talents.tsv` types the `Rampaging Berserker` node `ACTIVE`; it is not a
  button.** The inventory has `1269308` as `talent-passive` / `castable=false`,
  tooltip *"Rampage damage increased by 10% and Rampage makes you go Berserk…"*.
  **`node_type` is not a castability signal** — `origin`/`castable` are. This is
  what the old "exact active component vs passive empower is uncertain" marker was
  asking, and it was never an in-game question.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact cooldown / cost
is uncertain"* is **not** one: `ability-inventory.md` carries the Tier-1 number.
