---
title: Frost Death Knight — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ../../_abilities/pet-family-annex.tsv  # tier 1 — pet skill lines @ 12.0.7.67808
  - ../../_abilities/all-abilities.tsv  # tier 1 — the 40-spec acquisition union, 7,065 rows
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree
confidence: high
---

# Frost Death Knight — off-inventory abilities

**Everything about a Frost ability is in `ability-inventory.md`** — specID 251,
**163 rows**, one row each carrying spellID, cooldown, cast time, origin,
talent/hero placement and the full tooltip. It is generated, Tier-1, DB2-pinned
to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Frost ability is not named below, do not research it — read its row in
> `ability-inventory.md` and go.** Rotation → `rotation.md`. Talents/hero pick →
> `builds.md`. Both sections here are **closed lists, not backlogs.**

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
| `47481` | Gnaw | **Your ghoul's stun.** It sits on the **Ghoul's** skill line (782), not yours — the pet path has no spec granularity in any DB2 table, so no row can attribute it to Frost. Frost gets the ghoul from **Raise Dead** `46585` (`class-baseline`/`talent-active`, 120s). Tier-1 evidence it is real: `pet-family-annex.tsv` line 782 has it `castable=true`, cd 90 — and the **Unholy** inventory carries the same spellID `47481` as a `cdm-only` row (it fell out of Blizzard's own Cooldown Manager set there). The join reaches it for one DK spec out of three; that asymmetry is the join's, not the game's. |

The ghoul's other pet-bar actives (**Leap** `47482`, **Huddle** `47484`, **Claw**
`47468`) are enumerated in `../../_abilities/pet-family-annex.tsv` and are not
repeated as rows here — read the annex.

**This category is real and measured, not an edge case.** Across all 40 specs,
pet-line and runtime-override buttons live in no spec-keyed DB2 table: `Axe Toss`,
`Devour`, `Pierce the Veil`, `Templar Slash`, `Void Volley` and `Heroic Strike`
are all real pressed buttons whose *only* record anywhere is a hand-written row
like this one.

## §B — Encountered, and we believe not valid

Names that appear in guides, older builds or other people's notes, which we have
checked and believe are **not** part of this spec at 12.0.7. Listed so the next
reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| Soul Reaper | **not in Frost's kit at all** | `all-talents.tsv` places Soul Reaper on **spec 252 (Unholy) only**, spec tree. Absent from Frost's 163 inventory rows and from every Frost row of the 40-spec union `all-abilities.tsv`. An earlier revision of this file called it an "off-meta talent for S1" — it is not selectable by Frost at any meta. |
| Chill Streak | **not acquirable by any spec at 12.0.7** | zero exact-name hits in `all-talents.tsv` (all 40 specs), zero in `all-abilities.tsv` (7,065 rows), zero across all 40 `ability-inventory.tsv` files. A historical Death Knight ability; the same earlier revision paired it with Soul Reaper as "exists but off-meta". It does not exist. |

*[Tier 1: `all-talents.tsv` + `all-abilities.tsv` + the 40 generated
`ability-inventory.tsv` files, all @ 12.0.7.67808.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **`Chosen of Frostbrood` `1265632` is a PASSIVE**, not a pressed cooldown —
  `talent-passive`, `castable=false`, cd 0. It reads *"Frostwyrm's Fury deals 100%
  increased damage to the first enemy it hits and grants you 15% Haste for 12
  sec."* An earlier revision listed it as a "Major cooldown / Instant" and hung an
  `@verify-ingame` on its effect. Both wrong, and it was never an in-game
  question — the tooltip is in `ability-inventory.md`.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact cooldown / cost
is uncertain"* is **not** one: `ability-inventory.md` carries the Tier-1 number.
