---
title: Demonology Warlock — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ../../_abilities/pet-family-annex.tsv  # tier 1 — pet skill lines @ 12.0.7.67808
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree
  - https://us.api.blizzard.com/data/wow/talent-tree/720/playable-specialization/266  # tier 1, static-12.0.7
confidence: high
---

# Demonology Warlock — off-inventory abilities

**Everything about a Demonology ability is in `ability-inventory.md`** — 167 rows,
one row each carrying spellID, cooldown, cast time, origin, talent/hero placement
and the full tooltip. It is generated, Tier-1, DB2-pinned to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Demonology ability is not named below, do not research it — read its
> row in `ability-inventory.md` and go.** Rotation → `rotation.md`. Talents/hero
> pick → `builds.md`. Both sections here are **closed lists, not backlogs.**

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
| `89766` | Axe Toss | **Your interrupt.** It is on the **Felguard's** skill line (761), not yours — the pet path has no spec granularity in any DB2 table, so no row can attribute it to Demonology. In `../../_abilities/pet-family-annex.tsv`; catalogued `prose-only` in `section-4-catalogue.md`. Pressed via *Command Demon*. ⚠ **Lose the pet, lose the kick.** |
| `19647` | Spell Lock | Same mechanism, **Felhunter's** line (189). Interrupt + purge, also via *Command Demon* — and only if you give up Axe Toss to run the Felhunter instead of the Felguard. |

**This category is real and measured, not an edge case.** Across all 40 specs,
runtime override / proc-replacement buttons live in no spec-keyed DB2 table:
`Devour`, `Pierce the Veil`, `Templar Slash`, `Void Volley` and `Heroic Strike`
are all real pressed buttons whose *only* record anywhere is a hand-written row
like these. Demonology gets off lightly with two.

## §B — Encountered, and we believe not valid

Names that appear in guides, older builds or other people's notes, which we have
checked and believe are **not** part of this spec at 12.0.7. Listed so the next
reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| Bilescourge Bombers | **not on the tree** | absent from the Blizzard Game Data API tree (720 / spec 266) whose 147 talent names were enumerated, and absent from `all-talents.tsv` for **every** spec — so not a talent anywhere at 12.0.7. Controls present in the same check: Hand of Gul'dan, Implosion, Summon Demonic Tyrant, Doom. |
| Nether Portal | **not on the tree** | same check, same result |
| Demonic Strength | **not on the tree** | same check, same result |
| Guillotine | **not on the tree** | same check, same result |
| Grimoire: Felguard `111898` | **exists in game data, not on this tree** | the live choice node is **Grimoire: Fel Ravager** `1276467` vs Grimoire: Imp Lord. ⚠ A `SpellName` hit is **not** evidence a spec can cast something — that table keeps retired spells indefinitely. |

*[Tier 1: Blizzard Game Data API static-12.0.7 — the API's current static
namespace, not a stale pin — plus `all-talents.tsv` @ 12.0.7.67808.]*

⚠ **The first four rows are the claim that once halted a combat-assist session.**
They carried an `@verify-ingame` marker, so "a marked claim you are about to build
on is a STOP: ask" fired — and the resolution was a Tier-1 table lookup, not a
login. **Settled. Do not re-open.**

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **`Dominion of Argus` `1276163` is a PASSIVE**, not a pressed cooldown —
  `talent-passive`, `castable=false`, cd 0. Summoning Demonic Tyrant opens a
  portal for 15s; every 2 Hand of Gul'dan casts then summon a subjugated demon.
  An earlier revision of this file called it an *"active major cooldown"* and put
  an `@verify-ingame` on it. Both wrong, and it was never an in-game question.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact cooldown / cost
is uncertain"* is **not** one: `ability-inventory.md` carries the Tier-1 number.
