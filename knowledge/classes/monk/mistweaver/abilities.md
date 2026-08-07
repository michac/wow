---
title: Mistweaver Monk — off-inventory abilities (Midnight S1)
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

# Mistweaver Monk — off-inventory abilities

**Everything about a Mistweaver ability is in `ability-inventory.md`** — 188 rows,
one row each carrying spellID, cooldown, cast time, origin, talent/hero placement
and the full tooltip. It is generated, Tier-1, DB2-pinned to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Mistweaver ability is not named below, do not research it — read its
> row in `ability-inventory.md` and go.** Healing priority, Fistweaving loop and
> cooldown planning → `rotation.md`. Talents / hero-tree pick → `builds.md`. Both
> sections here are **closed lists, not backlogs.**

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
resolves to a row in `ability-inventory.tsv` — including the one apparent miss,
`Resuscitate (Res)`, which is a formatting artifact of **`Resuscitate` `115178`**,
`class-baseline` via `SkillLineAbility:829`.

## §B — Encountered, and we believe not valid

Names that appear in guides, older builds or other people's notes, which we have
checked and believe are **not** part of this spec at 12.0.7. Listed so the next
reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| Spear Hand Strike `116705` | **wrong spec — Mistweaver has no interrupt** | on the live Monk tree **1000**, 116705 sits on node 101152 gated **Brewmaster** and node 110098 gated **Windwalker**; `all-talents.tsv` has exactly those two rows and no Mistweaver row. Its only ungated node is on tree **781**, the legacy copy. Confirmed by absence from `mistweaver/ability-inventory.tsv` while both sibling files carry it. |
| Ancient Teachings | **renamed** | the live damage→heal passive is **`Jadefire Teachings` `467293`** (`talent-passive` in `mistweaver/ability-inventory.tsv`). "Ancient Teachings" has **zero** rows in `all-talents.tsv` for every spec and zero rows in all three Monk inventories at 12.0.7.67808. ⚠ `rotation.md` and `builds.md` still use the old name — see the escalation note below. |
| Nimble Brew `354540` | **wrong spec** | `PvpTalent` @ 67808 maps 354540 to Monk / **Brewmaster** only; it appears in `brewmaster/ability-inventory.tsv` and in no other Monk file. |
| Double Barrel `202335` | **wrong spec** | same check: `PvpTalent` 202335 → Monk / **Brewmaster** only. |
| Reverse Magic `205604` | **not a Monk ability at all** | `PvpTalent` 205604 → **Demon Hunter**, and all three of Havoc / Vengeance / Devourer carry it in their `ability-inventory.tsv`. No Monk spec does. |
| Zen Meditation `115176` | **not acquirable — legacy tree only** | 115176's only trait attachment is Monk tree **781**, the legacy copy; the live Monk tree is **1000** (every `node_id` in all three Monk inventories resolves to 1000) and has no such node. |
| Dampen Harm `122278` | **not acquirable — legacy tree only** | 122278 attaches only to tree **781** (nodes 80704 / 95171 / 95172 for BrM / MW / WW) and to nothing on live tree **1000**. Checked across all three Monk specs. |

*[Tier 1: `all-talents.tsv`, all three Monk `ability-inventory.tsv` files, and the
Demon Hunter inventories @ 12.0.7.67808; adjudicated in
`../../_abilities/reconcile-ledger.md` §Monk.]*

⚠ The `Double Barrel` row previously carried an `@verify-ingame` marker, so *"a
marked claim you are about to build on is a STOP: ask"* fired on it. The
resolution was a `PvpTalent` lookup, not a login. **Settled. Do not re-open.**

## Corrections this file has already made

Kept only because re-asserting it is the likely failure mode:

- **Mistweaver has no interrupt at 12.0.7.** Every Tier-3 Monk guide assumes a
  kick, and an earlier revision of this file listed Spear Hand Strike on the
  strength of that assumption. It is Brewmaster's and Windwalker's only (see §B).
  Plan interrupt rotations around a Mistweaver contributing none.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact cast time /
mana cost is uncertain"* is **not** one: `ability-inventory.md` carries the
Tier-1 number.
