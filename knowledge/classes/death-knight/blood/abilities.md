---
title: Blood Death Knight — off-inventory abilities (Midnight S1)
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

# Blood Death Knight — off-inventory abilities

**Everything about a Blood ability is in `ability-inventory.md`** — specID 250,
**165 rows**, one row each carrying spellID, cooldown, cast time, origin,
talent/hero placement and the full tooltip. It is generated, Tier-1, DB2-pinned
to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Blood ability is not named below, do not research it — read its row in
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
| `47481` | Gnaw | **Your ghoul's stun.** It sits on the **Ghoul's** skill line (782), not yours — the pet path has no spec granularity in any DB2 table, so no row can attribute it to Blood. Blood keeps a ghoul: **Raise Dead** `46585` is `class-baseline`/`talent-active` at 120s, the 1:1 Dancing Rune Weapon pairing. Tier-1 evidence it is real: `pet-family-annex.tsv` line 782 has it `castable=true`, cd 90 — and the **Unholy** inventory carries the same spellID `47481` as a `cdm-only` row (it fell out of Blizzard's own Cooldown Manager set there). The join reaches it for one DK spec out of three; that asymmetry is the join's, not the game's. |

The ghoul's other pet-bar actives (**Leap** `47482`, **Huddle** `47484`, **Claw**
`47468`, and the Dark-Transformation upgrades **Monstrous Blow** `91797`,
**Shambling Rush** `91802`, **Putrid Bulwark** `91837`, **Sweeping Claws**
`91778`) are enumerated in `../../_abilities/pet-family-annex.tsv`. They are not
repeated as rows here — read the annex.

**This category is real and measured, not an edge case.** Across all 40 specs,
pet-line and runtime-override buttons live in no spec-keyed DB2 table: `Axe Toss`,
`Devour`, `Pierce the Veil`, `Templar Slash`, `Void Volley` and `Heroic Strike`
are all real pressed buttons whose *only* record anywhere is a hand-written row
like this one.

## §B — Encountered, and we believe not valid

_None recorded for this spec._ The revision this file replaces made no
absence claim — everything it named resolves to a row in `ability-inventory.tsv`.

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **Take spellIDs from `ability-inventory.tsv`, never from `SpellName.csv` or
  memory.** An earlier revision restated three IDs off the raw name table and all
  three were wrong for the button Blood actually presses: Reaper's Mark is
  `439843` (not 434765), Vampiric Strike `433901` (not 433895), Exterminate
  `441378` (not 161362). A `SpellName` hit is not evidence a spec can cast
  something — that table keeps retired and variant spells indefinitely.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact cooldown / cost
is uncertain"* is **not** one: `ability-inventory.md` carries the Tier-1 number.
