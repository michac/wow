---
title: Brewmaster Monk — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree @ 12.0.7.67808
  - ../../_abilities/reconcile-ledger.md  # tier 1 adjudication of this file's former claims @ 12.0.7.67808
  - ../../_abilities/section-4-catalogue.tsv  # tier 1 — no Monk `prose-only` rows exist
confidence: high
---

# Brewmaster Monk — off-inventory abilities

**Everything about a Brewmaster ability is in `ability-inventory.md`** — 186 rows,
one row each carrying spellID, cooldown, cast time, origin, talent/hero placement
and the full tooltip. It is generated, Tier-1, DB2-pinned to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Brewmaster ability is not named below, do not research it — read its
> row in `ability-inventory.md` and go.** Rotation, priority and Brew usage →
> `rotation.md`. Talents / hero-tree pick → `builds.md`. Both sections here are
> **closed lists, not backlogs.**

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

_None known for this spec._

Checked, not assumed: `section-4-catalogue.tsv` carries **no `prose-only` row for
any Monk spec**, and every ability named in this file's previous prose table
resolves to a row in `ability-inventory.tsv`. Monk has no pet skill line and no
proc-replacement button of the `Devour` / `Templar Slash` shape.

## §B — Encountered, and we believe not valid

Names that appear in guides, older builds or other people's notes, which we have
checked and believe are **not** part of this spec at 12.0.7. Listed so the next
reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| Rising Sun Kick | **not in the Brewmaster kit** | `all-talents.tsv` carries RSK on node 101186 / entry 124985 for **mistweaver** and **windwalker** only — there is no Brewmaster row, and none in `ability-inventory.tsv`. Its Brewmaster grep hits are other talents' tooltips *mentioning* it. Midnight replaced the RSK slot with the Keg Smash / **Bring Me Another** loop. |
| Weapons of Order | **removed** | zero rows in `all-talents.tsv` for **every** spec, and zero rows in all three Monk `ability-inventory.tsv` files. The old TWW Master-of-Harmony capstone is gone. |
| Zen Meditation `115176` | **not acquirable — legacy tree only** | 115176's only trait attachment is Monk tree **781**, the legacy copy. The live Monk tree is **1000** (every `node_id` in all three Monk inventories resolves to 1000) and carries no Zen Meditation node; no row in `all-talents.tsv` for any spec. |
| Dampen Harm `122278` | **not acquirable — legacy tree only** | same shape: 122278 attaches only to tree **781** (nodes 80704 / 95171 / 95172 for BrM / MW / WW) and to nothing on live tree **1000**. Checked across all three Monk specs, not just this one. |

*[Tier 1: `all-talents.tsv` + all three Monk `ability-inventory.tsv` @ 12.0.7.67808,
adjudicated in `../../_abilities/reconcile-ledger.md` §Monk.]*

⚠ The Zen Meditation and Dampen Harm rows previously carried `@verify-ingame`
markers, so *"a marked claim you are about to build on is a STOP: ask"* fired on
them. The resolution was a talent-table lookup, not a login. **Settled. Do not
re-open.**

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **Brewmaster *does* have a resurrect: `Resuscitate` `115178`**, `class-baseline`
  via `SkillLineAbility:829`, present in all three Monk inventories. An earlier
  revision of this file asserted the seed checklist's *"Res"* row *"does not map to
  a real Brewmaster spell — Monk has no unique battle/out-of-combat resurrect."*
  That is false; it was a seed-naming artifact, not a missing ability.
- **`Nimble Brew` `354540` and `Double Barrel` `202335` are Brewmaster's, and only
  Brewmaster's.** `PvpTalent` @ 67808 maps both to Monk / Brewmaster alone, and
  they appear in `brewmaster/ability-inventory.tsv` and no other Monk file. The
  Mistweaver and Windwalker files both record *deleting* them as wrong-spec — a
  class-wide sweep that reads those notes and deletes here too would be wrong.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact recharge /
Energy cost is uncertain"* is **not** one: `ability-inventory.md` carries the
Tier-1 number, and the charge-recharge caveat is documented in
`../../_abilities/prose-conventions.md`.
