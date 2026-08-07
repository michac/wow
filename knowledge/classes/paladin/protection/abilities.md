---
title: Protection Paladin — off-inventory abilities (Midnight S1)
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

# Protection Paladin — off-inventory abilities

**Everything about a Protection ability is in `ability-inventory.md`** — 199 rows,
one row each carrying spellID, cooldown, cast time, origin, talent/hero placement
and the full tooltip. It is generated, Tier-1, DB2-pinned to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Protection ability is not named below, do not research it — read its
> row in `ability-inventory.md` and go.** Rotation → `rotation.md`. Talents/hero
> pick → `builds.md`. Both sections here are **closed lists, not backlogs.**

⚠ One caveat the inventory cannot flag: its **42 `class-baseline` rows are the
whole Paladin skill line, not Protection's bar** — mounts, Holy's Beacon of Light,
Retribution's Wake of Ashes. `SkillLineAbility:800` is a *class* attachment;
nothing generated filters it to a spec.

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
| — | Empyrean absorbs | ⚠ **Not a spell name — an obvious harvest artifact, reproduced verbatim on purpose (see below).** |
| — | Guardian's | ⚠ **Not a spell name — an obvious harvest artifact, reproduced verbatim on purpose (see below).** |
| — | Sacred Weapon | **One of the two outputs of `Holy Armaments` `432459`** (talent-active, Lightsmith subtree, node 95234), which alternates them: that spell's Tier-1 resolved tooltip ends *"Becomes Sacred Weapon after use."* No spell **named** Sacred Weapon attaches to a trait node, skill line, `SpecializationSpells` or `PvpTalent` row — 432472 / 432502 / 432616 / 432757 / 441590 all attach to nothing *(`reconcile-ledger.md`)* — so the join can never emit it. The other half, **Holy Bulwark**, *does* appear, as a `cdm-only` row on the same spellID 432459. ⚠ A spell-API 404 is **not** evidence of absence. |
| — | Concentration Aura | **Granted by the class-tree talent `Auras of the Resolute` `385633`** (node 102587, all three Paladin specs in `all-talents.tsv`), whose Tier-1 resolved tooltip reads *"**Learn Concentration Aura**, Devotion Aura, and Crusader Aura … Concentration Aura: Interrupt and Silence effects on party and raid members within 40 yds are 30% shorter."* `Aura Mastery` `31821` still carries a *"Concentration Aura: Affected allies immune to interrupts and silences"* clause. The aura has **no acquisition row of its own** (79963 / 81455 / 317920 / 344220 attach to nothing) — Devotion, Crusader and Retribution Aura each have a `class-baseline SkillLineAbility:800` row and this one does not. **This reverses the old "not acquirable" verdict — see Corrections.** |

⚠ **The first two rows are harvest artifacts and are kept spelled exactly as the
catalogue has them.** The prose this file replaces carried a single row headed
`Guardian's/Empyrean absorbs (Bulwark of Order)`;
`gen_abilities._inventory_names()` splits a name cell on `/` and strips
parentheticals, so that one cell became two catalogue entries, neither of which is
a spell. **Nothing is actually missing**: the real spells behind the fragment are
**`Bulwark of Order` `209389`** (talent-passive — *"Avenger's Shield also shields
you for 8 sec, absorbing 60% as much damage as it dealt, up to 50% of your maximum
health"*) and **`Guardian of Ancient Kings` `86659`** (talent-active, +
`Empyrean Authority` `1246481` for the second charge), both already in
`ability-inventory.md`. **Do not "fix" the two names here** — a separate
deliberate artifact pass owns that; not losing data and improving data are
different jobs.

## §B — Encountered, and we believe not valid

Names that appear in guides, older builds or other people's notes, which we have
checked and believe are **not** part of this spec at 12.0.7. Listed so the next
reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| Moment of Glory | **gone at 12.0.7** | the name appears **nowhere** in the generated layer: not in `all-talents.tsv` for any spec of any class, not in any of the 40 `ability-inventory.tsv` files, not in `section-3-corroborated.tsv` or `section-4-catalogue.tsv`. Do not author it. |
| Bastion of Light | **gone at 12.0.7** | same check, same result — zero hits across `all-talents.tsv`, all 40 spec inventories and both catalogue sections. |

*[Tier 1: `all-talents.tsv` + the 40 `ability-inventory.tsv` files @ 12.0.7.67808.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **`Concentration Aura` is acquirable at 12.0.7 — the old verdict was wrong.**
  Every Paladin `abilities.md`, `reconcile-ledger.md` and
  `../../_abilities/prose-conventions.md` §6 currently state *"Concentration Aura
  is not acquirable at 12.0.7"*. The measurement is sound (no spell of that name
  attaches to anything) but the **conclusion does not follow**: a *talent* grants
  it. See §A. The old "swap to Concentration Aura on silence-heavy pulls" advice
  is **not** dead — the earlier revision of this file said to plan without it.
- **`Eye of Tyr` still has a live acquisition row.** An earlier revision asserted
  *"Eye of Tyr, Moment of Glory and Bastion of Light were removed in Midnight —
  do not author Eye of Tyr as a live button."* Moment of Glory and Bastion of
  Light check out (§B); **Eye of Tyr does not.** `ability-inventory.tsv` carries
  `Eye of Tyr 209202 class-baseline SkillLineAbility:800`, castable, cd **60s**,
  for **all three** Paladin specs. Whether it is genuinely on the bar is a
  separate question (below) — but "it was removed" is contradicted by Tier 1 and
  must not be re-asserted.

## Open in-game questions

One, and it needs the spellbook — no table settles it:

- Is `Eye of Tyr` 209202 an actual spellbook button at 12.0.7, or a dead class-line row? Its acquisition row is live (class-baseline, cd 60) but its tooltip still describes the Legion artifact ("Releases a blinding flash from Truthguard"), and the Paladin class line demonstrably carries dead rows (Sense Undead, Contemplation). @verify-ingame
