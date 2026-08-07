---
title: Elemental Shaman — off-inventory abilities (Midnight S1)
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

# Elemental Shaman — off-inventory abilities

**Everything about an Elemental ability is in `ability-inventory.md`** — 181 rows,
one row each carrying spellID, cooldown, cast time, origin, talent/hero placement
and the full tooltip. It is generated, Tier-1, DB2-pinned to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If an Elemental ability is not named below, do not research it — read its
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

Checked, not assumed: every ability name the replaced prose asserted resolves to a
row in `ability-inventory.tsv` (spell-ID and origin both), and Shaman contributes
**zero** `prose-only` rows to `_abilities/section-4-catalogue.tsv`. Elemental has no
pet path (its one summon, `Earth Elemental` `198103`, is a normal `talent-active`
row) and no runtime override button of the `Windstrike` / `Devour` kind that the
join would miss. Add a row here **only** after grepping the `.tsv` and finding the
name genuinely absent.

## §B — Encountered, and we believe not valid

Names that appear in guides, older builds or other people's notes, which we have
checked and believe are **not** part of this spec at 12.0.7. Listed so the next
reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| Fire Elemental `198067` | **removed — not acquirable** | attaches to **no** live acquisition row. Its only trait attachment is the **legacy** Shaman trees **1033/1034** (the trees still carrying the pre-Midnight set — Icefury, Primordial Wave, Liquid Magma Totem, Stormstrike). The **live** Shaman tree is **786**, which carries `Earth Elemental` `198103` and the `Primal Elementalist` / `Call of Fire` passives but no Fire Elemental node. Absent from `all-talents.tsv` for **every** spec. |
| Storm Elemental `192249` | **removed — not acquirable** | same measurement, same result: legacy trees 1033/1034 only, nothing on live tree 786, absent from `all-talents.tsv` for every spec. |

*[Tier 1: DB2 @ 12.0.7.67808 via `../../_abilities/reconcile-ledger.md`; `all-talents.tsv` @ 12.0.7.67808, all 40 specs.]*

⚠ **A Tier-3 guide that describes Fire/Storm Elemental is describing The War
Within.** Do not restore either row without a fresh DB2 read. The burst window they
used to anchor is Stormkeeper → Ascendance (`rotation.md`).

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **`Thunderstorm` `51490` is Elemental-only, and is not a PvP talent.**
  `SpecializationSpells` → Shaman / **Elemental**, `class-baseline`, cd **30s**. It
  is **absent from `PvpTalent` entirely** and is not a talent on any tree. The
  Enhancement and Restoration files each used to claim it (Enhancement's row even
  labelled it "PvP talent"); both rows are deleted and it is listed in their §B.
  It is a real Elemental button — read its row in `ability-inventory.md`.
- **`Ancestral Spirit` `2008` is NOT a combat resurrection.** Its Tier-1 tooltip
  ends *"Cannot be cast when in combat."* An earlier revision of this file called
  it a battle rez. **Shaman has no battle rez.** `Ancestral Vision` `212048` is the
  out-of-combat **mass** res, also non-combat.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact cooldown / cast
time / cost is uncertain"* is **not** one: `ability-inventory.md` carries the
Tier-1 number. The two markers this file used to carry (Voltaic Blaze's cooldown,
Skyfury's exact bonus) were both of that kind and are deleted with their guesses.
