---
title: Enhancement Shaman — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ./ability-inventory.tsv  # tier 1 — the data twin; name/spellID/origin/cooldown/tooltip source of record
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree @ 12.0.7.67808
  - ../../_abilities/reconcile-ledger.md  # tier 1 derived — the 12.0.7.67808 adjudication behind the removals below
confidence: high
---

# Enhancement Shaman — off-inventory abilities

**Everything about an Enhancement ability is in `ability-inventory.md`** — 171
rows, one row each carrying spellID, cooldown, cast time, origin, talent/hero
placement and the full tooltip. It is generated, Tier-1, DB2-pinned to
`12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If an Enhancement ability is not named below, do not research it — read its
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

_None known for this spec._

⚠ **This file used to contribute nothing to the catalogue at all** — its ability
tables sat under headings the harvester does not match (`## Rotational core`,
`## Weapon imbues`, `## Utility & totems`), so none of it was ever harvested. The
heading above **is** matched, so anything written into a table here now lands in
the catalogue as an asserted-but-unjoined ability. Before adding a row, grep
`ability-inventory.tsv` and confirm the name is genuinely absent.

Checked, not assumed: all 41 distinct ability names the replaced prose asserted —
including `Windstrike` `115356`, which reads like a runtime override but is a real
`class-baseline` row — resolve in `ability-inventory.tsv`. Enhancement has no pet
path (`Feral Spirit` `469314` is a `talent-passive` row, not a controllable pet
with its own skill line) and so no `Axe Toss`-style class-level button the join
would miss.

## §B — Encountered, and we believe not valid

Names that appear in guides, older builds or other people's notes, which we have
checked and believe are **not** part of this spec at 12.0.7. Listed so the next
reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| Elemental Blast `117014` | **wrong spec — not on any Enhancement tree** | `talent-choice` on **Elemental**'s spec tree only (`all-talents.tsv`, node 80984). Appears on no Enhancement tree — class, spec or hero — and is absent from the Enhancement `ability-inventory.tsv`. It used to be listed here as a Maelstrom Weapon spender; it is not one for this spec. |
| Thunderstorm `51490` | **wrong spec — Elemental-only** | `SpecializationSpells` → Shaman / **Elemental** (`class-baseline` there, cd 30s). **Absent from `PvpTalent` entirely**, so the old "maybe it's a PvP talent" hedge had no route to a yes; it is not a talent on any tree, and its only trait attachment is the **legacy** Shaman trees 1033/1034, not the live tree **786**. Enhancement's Tier-1 crowd-control rows are Capacitor Totem, Earthgrab Totem, Tremor Totem and Hex — plan peels off those, not off a knockback. |

*[Tier 1: DB2 @ 12.0.7.67808 via `../../_abilities/reconcile-ledger.md`; `all-talents.tsv` @ 12.0.7.67808, all 40 specs.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **`Wind Shear` `57994` is a TALENT, not baseline.** Origin `talent-active` on the
  class tree — **a build that skips the node has no kick.** Every Tier-3 guide
  writes it as baseline, and this file once did too. Check `builds.md` before
  assuming Enhancement brings an interrupt to a key.
- **`Sundering` `197214` is on a 30s cooldown, not 40s.** Tier-3 guides say 40s;
  DB2 says **30s**. The old file hedged over a "30–40s spread" — there is no
  spread.
- **`Stone Bulwark Totem` is gone**, which is why `Astral Shift` `108271`
  (`talent-active`, cd **120s** — not the ~90s Tier 3 carried) is the only planned
  mitigation. Its damage-reduction **percentage and duration are not readable from
  DB2**; treat any number for those as Tier 3.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact cooldown /
charges / cost is uncertain"* is **not** one: `ability-inventory.md` carries the
Tier-1 number. The five markers this file used to carry (Stormstrike charges,
Crash Lightning CD, Voltaic Blaze trigger, Skyfury's bonus, Feral Spirit
active-vs-passive) were all of that kind and are deleted with their guesses.
