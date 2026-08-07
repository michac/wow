---
title: Restoration Shaman — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ./ability-inventory.tsv  # tier 1 — the data twin; name/spellID/origin/cooldown/tooltip source of record
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree @ 12.0.7.67808
  - ../../_abilities/reconcile-ledger.md  # tier 1 derived — the 12.0.7.67808 adjudication behind the removal below
confidence: high
---

# Restoration Shaman — off-inventory abilities

**Everything about a Restoration ability is in `ability-inventory.md`** — 185
rows, one row each carrying spellID, cooldown, cast time, origin, talent/hero
placement and the full tooltip. It is generated, Tier-1, DB2-pinned to
`12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Restoration ability is not named below, do not research it — read its
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

Checked, not assumed: every ability and passive name the replaced prose asserted
resolves to a row in `ability-inventory.tsv`, and Shaman contributes **zero**
`prose-only` rows to `_abilities/section-4-catalogue.tsv`. Restoration has no pet
path (`Earth Elemental` `198103` is a normal `talent-active` row) and no runtime
override button of the `Windstrike` / `Devour` kind that the join would miss —
`Surging Totem`'s overrides of Healing Rain and Windfury Totem are already carried
by `_abilities/section-3-corroborated.tsv`, not here. Add a row **only** after
grepping the `.tsv` and finding the name genuinely absent.

## §B — Encountered, and we believe not valid

Names that appear in guides, older builds or other people's notes, which we have
checked and believe are **not** part of this spec at 12.0.7. Listed so the next
reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| Thunderstorm `51490` | **wrong spec — Elemental-only** | `SpecializationSpells` → Shaman / **Elemental** (`class-baseline` there, cd 30s), and absent from the Restoration `ability-inventory.tsv`. **Absent from `PvpTalent` entirely**; not a talent on any tree in `all-talents.tsv`; its only trait attachment is the **legacy** Shaman trees 1033/1034, not the live tree **786**. There is no route by which a Resto build acquires it. Resto's Tier-1 crowd-control rows are Capacitor Totem, Earthgrab Totem, Tremor Totem and Hex — plan peels off those, not off a knockback. |

*[Tier 1: DB2 @ 12.0.7.67808 via `../../_abilities/reconcile-ledger.md`; `all-talents.tsv` @ 12.0.7.67808, all 40 specs.]*

⚠ `rotation.md` still lists Thunderstorm as a Resto pack-control tool. That file is
out of this pass's scope; the Tier-1 finding above is the one to believe.

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **`Ancestral Vision` `212048` is the out-of-combat MASS resurrection, not a
  battle rez.** Tier-1 tooltip: *"Returns all dead party members to life with 35%
  of maximum health and mana. Cannot be cast when in combat."* An earlier revision
  called it a "battle-rez–style ancestral effect" and put an `@verify-ingame` on
  it; it was never an in-game question. **Shaman has no combat resurrection** —
  `Ancestral Spirit` `2008` is the single-target out-of-combat res and carries the
  same "cannot be cast when in combat" clause.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact cooldown / cast
time / cost is uncertain"* is **not** one: `ability-inventory.md` carries the
Tier-1 number. The four markers this file used to carry (Healing Surge, Downpour,
Skyfury, Ancestral Vision) were all of that kind and are deleted with their
guesses.
