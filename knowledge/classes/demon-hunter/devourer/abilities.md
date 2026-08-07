---
title: Demon Hunter Devourer — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ./talents.json  # tier 1 — Blizzard talent-tree capture, Devourer spec tree
  - ../../_abilities/reconcile-ledger.md  # tier 1 derived — the DH verdicts, §4 + §5 G1/G2/G6
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree @ 12.0.7.67808
  - ../../_abilities/section-3-corroborated.tsv  # tier 1 derived — override-aura reaches
confidence: high
---

# Demon Hunter Devourer — off-inventory abilities

**Everything about a Devourer ability is in `ability-inventory.md`** — 147 rows,
each carrying spellID, cooldown, cast time, origin, talent/hero placement and the
full tooltip. It is generated, Tier-1, DB2-pinned to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Devourer ability is not named below, do not research it — read its row
> in `ability-inventory.md` and go.** Rotation → `rotation.md`. Talents/hero pick
> → `builds.md`. Both sections here are **closed lists, not backlogs.**

## §A — Real buttons the inventory cannot see

Confirmed to exist, but no spec-keyed acquisition table names them, so they will
never appear in `ability-inventory.tsv`. **Absence there is not absence in game.**

> ⚠ **This section is a machine input.** `wowkb.gen_abilities` harvests the `name`
> column of the table below — the heading is matched on the word **`inventory`** —
> and feeds it to the `prose-only` leg of `section-4-catalogue.md`. Rename this
> heading or drop the `name` column header and these rows **silently vanish from
> the catalogue**, with no marker and no warning. §B is deliberately *not*
> harvested: it asserts the opposite.

| spellID | name | how we know, and why the join misses it |
|---|---|---|
| `1277736` | Demonic Wards | Passive baseline magic mitigation. It **is** attached — `SpecializationSpells` → Devourer — but the generator drops **passive** `SpecializationSpells` rows (431 of 458 lost), so no inventory row exists. Tool gap **G1**; the siblings `278386` Havoc / `203513` Vengeance are the same hole. |
| `1217610` | Devour | **The Void Metamorphosis form of Consume.** Parent `Consume` `473662` is `SpecializationSpells`/Devourer and live; a runtime override button has no acquisition row of its own, so no join can ever reach it. Tool gap **G2**. ⚠ `1217610` is a Tier-3 ID from the maxroll capture, not Tier-1-confirmed. **This prose is the only record of the button anywhere.** |
| `1245483` | Pierce the Veil | **Void-Scarred's empowered Voidblade inside Void Metamorphosis.** `1245483` is a Midnight-range ID present in `SpellName` @ `12.0.7.67808` but attached to nothing; the parent `Voidblade` `1245412` is `talent-active` on live tree 854. Tool gap **G2**. **This prose is the only record of the button anywhere.** |

**`Cull` deliberately has no row here.** It is the same shape — Reap's transform
form, `1245453` — but it is already reached as `override-aura` off `Eradicate`
`1239524` in `section-3-corroborated.tsv`, so the catalogue has it without prose.
Adding it here would duplicate a Tier-1 reach with a hand assertion.

## §B — Encountered, and we believe not valid

Checked, and believed **not** part of this spec at 12.0.7. Listed so the next
reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| Voidstep | **name drift — the live talent is `Voidrush`** | No `Voidstep` row in `all-talents.tsv` for **any** of the 40 specs. `talents.json` spec node `110173` carries **Voidrush** `1272422` ("Collapsing Star reduces the cooldown of Voidblade by 10 sec"), whose *icon file* is `inv_12_dh_void_ability_voidstep.jpg` — a dev-era filename is where the wrong name came from. |
| Fel Rush | **suspected join over-report, not a Devourer button** | It enters the inventory via `SkillLineAbility:1848`, the Demon Hunter **class** skill line, which carries no spec granularity. The control: the same join also hands **Vengeance** Fel Rush `344865`, alongside its real `Infernal Strike` `189110`. Devourer's own movement button is **Shift** `1234796` (`SpecializationSpells`). Not settled — the class line can say yes but never no. |

*[Tier 1: `all-talents.tsv` + `all-abilities.tsv` + this folder's `talents.json`,
all @ `12.0.7.67808`.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **`Blur`'s cooldown column in the tsv reads `0.5` — that is the GCD, not the
  cooldown.** Blur is charge-based and the generated schema has no charge-recharge
  column, so the cell is meaningless for planning. Do not quote 0.5s.
  *[reconcile-ledger §5 G6.]* Same trap on any charge ability in this spec.
- **`Reap` and `Blur` are `class-baseline`, not talents.** Every Devourer has them
  regardless of tree; an earlier revision of this file called both talented, off
  Tier-3 guides.

## Open in-game questions

@verify-ingame Does Devourer's spellbook actually contain Fel Rush 344865, or does Shift 1234796 replace it as Infernal Strike does for Vengeance? Class SkillLine 1848 has no spec granularity, so only a spellbook enumeration settles it.

Nothing else. A question belongs here only if it genuinely cannot be answered from
game data. *"The exact cooldown / Fury yield / charge count is uncertain"* is
**not** one: `ability-inventory.md` carries the Tier-1 number.
