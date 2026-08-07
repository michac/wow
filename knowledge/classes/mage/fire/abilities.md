---
title: Fire Mage — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree
  - ../../_abilities/reconcile-ledger.md  # tier 1 derived — per-row verdicts
confidence: high
---

# Fire Mage — off-inventory abilities

**Everything about a Fire ability is in `ability-inventory.md`** — 209 rows, one
row each carrying spellID, cooldown, cast time, origin, talent/hero placement and
the full tooltip. It is generated, Tier-1, DB2-pinned to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Fire ability is not named below, do not research it — read its row in
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

_None known for this spec._ Fire is petless and has no runtime-override button;
every name the previous prose carried resolves to an acquisition row in
`ability-inventory.tsv` (checked name-by-name, 2026-08-06).

## §B — Encountered, and we believe not valid

| name | verdict | evidence |
|---|---|---|
| Phoenix Flames | **removed in Midnight** | absent from `all-talents.tsv` for **every** spec, and from Fire's `ability-inventory.tsv` under any origin. Its Fire Blast-refund role is covered by the **Fired Up** apex proc `1257343`. `builds.md` already records the removal. |
| Shifting Power | **not acquirable by any Mage spec** | absent from `all-talents.tsv` for every spec. Its only DB2 attachment is a SkillLineAbility row on the dead Shadowlands *Night Fae* covenant line — not a live acquisition path. |
| Sun King's Blessing | **folded into Pyroclasm** | absent from `all-talents.tsv` for every spec; **Pyroclasm** is the live node that carries the effect. Not a separate button or buff to track. |
| Mass Barrier `414660` | **not acquirable at 12.0.7** | attaches to no trait node, SkillLineAbility, SpecializationSpells or PvpTalent entry (`reconcile-ledger.md`). It survives only as a Cooldown-Manager set entry, which is why it can surface in *Frost's* inventory as `cdm-only`. **A CooldownSet row is not an acquisition row.** |
| Prismatic Barrier `235450` | **belongs to Arcane, not on this tree** | the class barrier node resolves to one spell per spec — `all-talents.tsv` node `62119`→Blazing Barrier `235313` for Fire, `62121`→Prismatic Barrier for Arcane, `62117`→Ice Barrier for Frost. The BucketBinds seed once listed Prismatic Barrier for Fire; Fire's only barrier is **Blazing Barrier**. |
| Ice Barrier `11426` | **appears in Fire's inventory as `cdm-only` — still not castable by Fire** | Fire's `ability-inventory.tsv` genuinely has an `Ice Barrier` row, origin `cdm-only`, source `CooldownSetSpell`. That is Blizzard's Cooldown-Manager set leaking Frost's barrier into Fire's set; there is **no** Fire trait node for it. Same trap as Mass Barrier, in the opposite direction — listed here precisely because the inventory *does* show it. |

*[Tier 1: `all-talents.tsv` + per-spec `ability-inventory.tsv`, DB2 @ 12.0.7.67808;
`_abilities/reconcile-ledger.md`.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **`Fired Up` `1257343` is a PASSIVE** — `talent-passive`, `castable=false`,
  cd 0. An earlier revision hung an `@verify-ingame` on *"whether there is a
  pressable component"* because `talents.md` flags the row-11 node ACTIVE. The
  inventory row settles it: **there is no button.** Do not put it on a bar.
- **Cone of Cold is a 25s class-baseline cooldown**, not an AoE filler you weave.
  Older prose halved it. Take the number from `ability-inventory.md`.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact charges /
recharge is uncertain"* is **not** one: `ability-inventory.md` carries the Tier-1
number (e.g. Fire Blast `108853`).
