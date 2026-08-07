---
title: Protection Warrior — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ../../_abilities/reconcile-ledger.md  # tier 1 derived — the Warrior/protection verdicts + §5 G6
  - ../../_abilities/section-3-corroborated.tsv  # tier 1 derived — where Condemn is already recorded
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree @ 12.0.7.67808
  - ../arms/ability-inventory.tsv  # tier 1 — sibling-spec cross-check for the §B verdicts
  - ../fury/ability-inventory.tsv  # tier 1 — sibling-spec cross-check for the §B verdicts
confidence: high
---

# Protection Warrior — off-inventory abilities

**Everything about a Protection ability is in `ability-inventory.md`** — 165 rows,
one each carrying spellID, cooldown, cast time, origin, talent/hero placement and
the full tooltip. It is generated, Tier-1, DB2-pinned to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Protection ability is not named below, do not research it — read its
> row in `ability-inventory.md` and go.** Rotation → `rotation.md`. Talents/hero
> pick → `builds.md`. Both sections here are **closed lists, not backlogs.**

## §A — Real buttons the inventory cannot see

_None known for this spec._

All 48 ability names the previous revision of this file asserted resolve to a row
in the 165-row generated inventory — checked by exact name match against
`ability-inventory.tsv` @ 12.0.7.67808 — except `Seeing Red`, which is §B, not a
button. Protection's one runtime override, **`Condemn` `317485`**, is *not* a §A
case: Tier 1 reaches it by itself, via `SpellEffect.EffectAura 332` on `Massacre`
`206315`, and it is already recorded in `../../_abilities/section-3-corroborated.tsv`
for all three Warrior specs. The unreached-override problem that costs Arms
(`Heroic Strike`) and Fury (`Crushing Blow`) a hand-written row does not bite here.

> ⚠ **Keep this heading exactly as written even while the section is empty.**
> `wowkb.gen_abilities` matches it on the word **`inventory`** and harvests the
> `name` column of any table under it into the `prose-only` leg of
> `section-4-catalogue`. If a real override button is ever found for Protection,
> it goes here in a `| spellID | name | how we know… |` table — nowhere else. §B
> is deliberately *not* harvested: it asserts the opposite.

## §B — Encountered, and we believe not valid

Names that appear in guides, older builds or other people's notes, which we have
checked and believe are **not** part of this spec at 12.0.7. Listed so the next
reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| Seeing Red | **not in any Tier-1 Warrior table** | **zero** rows in all three Warrior `ability-inventory.tsv` files (Arms 159 / Fury 155 / Protection 165) and **zero** hits in `all-talents.tsv` across all 40 specs. It also has no `reconcile-ledger` verdict. Tier-3 guides still use "Seeing Red" for the stacking buff that feeds `Violent Outburst` `386477` (which **is** in the inventory) — treat it as a guide nickname for that stack, not a spell, until something Tier-1 says otherwise. |
| Protection Stance | **not a spell at 12.0.7** | same two checks, zero hits in either. The tanking stance is **`Defensive Stance` `386208`** — `talent-active`, class-tree node 90330 / entry 112187. The BucketBinds seed's "Protection Stance" is this spell under an old name. |

*[Tier 1: `all-talents.tsv` + the three Warrior `ability-inventory.tsv` files,
both @ 12.0.7.67808.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **`Defensive Stance` is a talent, not baseline** *[Tier 1]*. This file claimed
  baseline until 12.0.7 data said otherwise; `reconcile-ledger` records the origin
  mislabel. It is `talent-active` / `TraitNodeEntry`, class tree, for all three
  Warrior specs. An untalented Protection build genuinely does not have it — do
  not assume it on a fresh character or a borrowed loadout.
- **`Berserker Shout` is not a rename of `Berserker Rage`.** Both are live and
  distinct in all three Warrior inventories: `Berserker Rage 18499`
  (`class-baseline`, castable) and `Berserker Shout 384100` (`talent-choice`, 60s).
  Earlier text here said "formerly Berserker Rage".
- **Do not trust the `cooldown` column for a charge ability.** It is
  `SpellCooldowns` at DifficultyID 0, which returns the **GCD** for one: `Shield
  Block` reads `1`, `Ignore Pain` `1`, `Intervene` `1.5`. The real recharge lives
  in `SpellCategory.ChargeRecoveryTime`, unreachable without breaking the build pin
  (`reconcile-ledger` §5 **G6**). Any recharge number you have seen for these
  (Shield Block ~16s / 2 charges; Intervene 2 charges) is **Tier 3** — do not
  restate it as Tier 1.
- **No layer here carries Rage *costs*.** The generated tooltips state what a spell
  *generates* and never what it *costs*, so there is no Tier-1 cost floor anywhere
  in this KB. A Rage cost you read in a guide is Tier 3; the spend-side priority
  itself (Ignore Pain as the overflow valve, Shield Block uptime) is in
  `rotation.md`, which is better sourced.
- ⚠ **Two Mountain Thane tooltips in `ability-inventory.md` render Fury's branch.**
  `Burst of Power` `437118` resolves to *"…make your next 2 **Bloodthirsts** have
  no cooldown"* and `Thunder Blast` `435607` to *"**Shield Slam and Bloodthirst**
  have a 35% chance…"* — Bloodthirst is Fury's builder. These are class-shared
  hero-tree spells whose `$?spec[…][…]` conditional the spell API resolved without
  spec context. For Protection the trigger and the payoff are Shield Slam. This is
  a **generated-layer wart, not a data correction** — do not "fix" the tsv.

## Open in-game questions

One, and only because the Tier-1 layer has already answered wrongly and cannot be
re-asked: the spell API collapsed the `$?spec` conditional, so no offline source
carries Protection's branch of these two tooltips.

- Burst of Power `437118` + Thunder Blast `435607` — read both tooltips in the Protection spellbook: do they say Shield Slam or Bloodthirst? @verify-ingame
