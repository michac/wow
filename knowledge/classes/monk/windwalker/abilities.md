---
title: Windwalker Monk — off-inventory abilities (Midnight S1)
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

# Windwalker Monk — off-inventory abilities

**Everything about a Windwalker ability is in `ability-inventory.md`** — 183 rows,
one row each carrying spellID, cooldown, cast time, origin, talent/hero placement
and the full tooltip. It is generated, Tier-1, DB2-pinned to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Windwalker ability is not named below, do not research it — read its
> row in `ability-inventory.md` and go.** Combo Strikes gating, priority and
> burst-window sequencing → `rotation.md`. Talents / hero-tree pick → `builds.md`.
> Both sections here are **closed lists, not backlogs.**

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
resolves to a row in `ability-inventory.tsv`. **`Mastery: Combo Strikes` `115636`
is the near-miss and it does resolve** — `reconcile-ledger.md` G1 says passive
`SpecializationSpells` rows are dropped by the generator, but this one is
recovered through the `CooldownSetSpell` residue leg and reads `cdm-only`. It
therefore does **not** belong in §A.

## §B — Encountered, and we believe not valid

Names that appear in guides, older builds or other people's notes, which we have
checked and believe are **not** part of this spec at 12.0.7. Listed so the next
reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| Storm, Earth, and Fire | **gone — superseded by Zenith** | **zero** rows in `all-talents.tsv` for every spec and zero rows in all three Monk `ability-inventory.tsv` files. The slot it occupied is now **`Zenith` `1249625`**, `talent-active` on the Windwalker spec tree at node 101053 / entry 124826, whose tooltip reduces Chi costs, lets Blackout Kick accelerate cooldowns, and resets Rising Sun Kick. The absence is measured; the succession is the reading of it. |
| Serenity | **gone — superseded by Zenith** | same check, same result. The only `Serenity` in any Monk inventory is the unrelated PvP talent **`Absolute Serenity` `455945`**; the only `all-talents.tsv` hits are Priest's Holy Word: Serenity and Ultimate Serenity. |
| Dampen Harm `122278` | **not acquirable — legacy tree only** | 122278 attaches only to Monk tree **781** (nodes 80704 / 95171 / 95172 for BrM / MW / WW), the legacy copy, and to nothing on the live Monk tree **1000**. Windwalker's defensives are Fortifying Brew and Touch of Karma. |
| Zen Meditation `115176` | **not acquirable — legacy tree only** | same shape: 115176's only trait attachment is tree **781**; no node on live tree **1000**, no row in `all-talents.tsv` for any spec. |
| Nimble Brew `354540` | **wrong spec** | `PvpTalent` @ 67808 maps 354540 to Monk / **Brewmaster** only; it appears in `brewmaster/ability-inventory.tsv` and in no other Monk file. |
| Double Barrel `202335` | **wrong spec** | same check: `PvpTalent` 202335 → Monk / **Brewmaster** only. |
| Reverse Magic `205604` | **not a Monk ability at all** | `PvpTalent` 205604 → **Demon Hunter**, and all three of Havoc / Vengeance / Devourer carry it in their `ability-inventory.tsv`. No Monk spec does. |

*[Tier 1: `all-talents.tsv`, all three Monk `ability-inventory.tsv` files, and the
Demon Hunter inventories @ 12.0.7.67808; adjudicated in
`../../_abilities/reconcile-ledger.md` §Monk.]*

⚠ **Dampen Harm, Nimble Brew, Double Barrel and Reverse Magic all previously
carried `@verify-ingame` markers**, so *"a marked claim you are about to build on
is a STOP: ask"* fired on four rows at once. Every one resolved to a table
lookup, not a login. **Settled. Do not re-open.**

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **`Zenith` `1249625` is a 16s baseline cooldown, not a two-minute raid
  cooldown.** Tier-3 guides describe the old Storm, Earth, and Fire / Serenity
  capstone cadence and an earlier revision of this file carried ~90s. It is a
  recurring window you press many times a fight, and `rotation.md`'s whole
  structure depends on that. **Spiritual Focus** cuts it a further 20s.
- **`Tigereye Brew` `1261703` is a PASSIVE**, not a pressed burst cooldown —
  `talent-passive`, `castable=false`, cd 0. Every 3 Chi spent generates a stack;
  **Zenith** consumes up to 20 stacks for +1% crit each for its duration. An
  earlier revision called it a *"spec capstone… consumed for a burst buff window"*
  and put an `@verify-ingame` on it, implying a button. There is no button.
- **The row name is `Mastery: Combo Strikes` `115636`**, not `Combo Strikes
  (Mastery)`. A `SpecializationSpells` passive for Windwalker; it is in the
  generated inventory as `cdm-only`.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact Chi cost / cast
time / effect magnitude is uncertain"* is **not** one: `ability-inventory.md`
carries the Tier-1 number and the full tooltip.
