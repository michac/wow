---
title: Arcane Mage — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree
  - ../../_abilities/reconcile-ledger.md  # tier 1 derived — per-row verdicts
confidence: high
---

# Arcane Mage — off-inventory abilities

**Everything about an Arcane ability is in `ability-inventory.md`** — 207 rows,
one row each carrying spellID, cooldown, cast time, origin, talent/hero placement
and the full tooltip. It is generated, Tier-1, DB2-pinned to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If an Arcane ability is not named below, do not research it — read its row
> in `ability-inventory.md` and go.** Rotation → `rotation.md`. Talents/hero pick
> → `builds.md`. Both sections here are **closed lists, not backlogs.**

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

_None known for this spec._ Arcane is petless and has no runtime-override button;
every name the previous prose carried resolves to an acquisition row in
`ability-inventory.tsv` (checked name-by-name, 2026-08-06).

## §B — Encountered, and we believe not valid

| name | verdict | evidence |
|---|---|---|
| Ice Barrier `11426` | **belongs to Frost, not on this tree** | the class barrier node resolves to **one spell per spec** — `all-talents.tsv` has node `62121`→Prismatic Barrier `235450` for Arcane, `62119`→Blazing Barrier `235313` for Fire, `62117`→Ice Barrier `11426` for Frost. Arcane cannot take the Frost entry. Arcane's inventory carries **no** Ice Barrier row at all (not even `cdm-only`). |
| Nether Precision | **removed in Midnight** | absent from `all-talents.tsv` for **every** spec of every class, and absent from Arcane's `ability-inventory.tsv` under any origin. The Arcane Missiles → Arcane Blast empowerment mechanic is gone; base Arcane Missiles damage was raised instead. `builds.md` and `rotation.md` already say so. |

*[Tier 1: `all-talents.tsv` + per-spec `ability-inventory.tsv`, DB2 @ 12.0.7.67808.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **`Touch of the Archmage` `1257942` is a PASSIVE**, not a pressed cooldown —
  `talent-passive`, `castable=false`, cd 0, cast 0. An earlier revision of this
  file listed it as a *"Major cooldown"* / *"capstone active (spec row 11)"* and
  hung an `@verify-ingame` on it. Both wrong, and it was never an in-game
  question: the inventory row answers it.
- Utility cooldowns that older prose halved: **Supernova** and **Cone of Cold**
  are **25s–45s class-baseline buttons**, not spammable fillers, and
  **Alter Time**'s `60s` is the *cooldown* — the ~10s people quote is the
  re-press window. Take all three from `ability-inventory.md`, not from memory.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact cooldown / cost
is uncertain"* is **not** one: `ability-inventory.md` carries the Tier-1 number.
