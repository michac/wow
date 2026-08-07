---
title: Preservation Evoker — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree @ 12.0.7.67808
  - ../../_abilities/section-3-corroborated.tsv  # tier 1 derived — spells reached indirectly
  - ../../_abilities/reconcile-ledger.md  # tier 1 derived — the verdicts applied 2026-08-06
confidence: high
---

# Preservation Evoker — off-inventory abilities

**Everything about a Preservation ability is in `ability-inventory.md`** — 154
rows (specID 1468), each carrying spellID, cooldown, cast time, origin,
talent/hero placement and the full tooltip. It is generated, Tier-1, DB2-pinned
to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Preservation ability is not named below, do not research it — read
> its row in `ability-inventory.md` and go.** Rotation → `rotation.md`.
> Talents/hero pick → `builds.md`. Both sections here are **closed lists, not
> backlogs.**

## §A — Real buttons the inventory cannot see

Confirmed to exist and be pressable, but no spec-keyed acquisition table names
them, so they will never appear in `ability-inventory.tsv`. **Absence there is
not absence in game.**

> ⚠ **This section is a machine input.** `wowkb.gen_abilities` harvests the
> `name` column of the table below — the heading is matched on the word
> **`inventory`** — and feeds it to the `prose-only` leg of
> `section-4-catalogue`. Rename this heading or drop the `name` column header
> and these rows **silently vanish from the catalogue**, with no marker and no
> warning. §B is deliberately *not* harvested: it asserts the opposite.

_None known for this spec._

Every ability name the previous hand-written prose listed resolves to a row in
this spec's `ability-inventory.tsv`. The override-reached empowers
(**Eternity Surge** `359073` and **Upheaval** `396286` off *Font of Magic*) are
already recorded in `../../_abilities/section-3-corroborated.tsv` and do not
belong here.

## §B — Encountered, and we believe not valid

Names that appear in guides, older builds or other people's notes, which we have
checked and believe are **not** pressable buttons for this spec at 12.0.7.
Listed so the next reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| Engulf | **does not exist at 12.0.7** | Zero rows named Engulf in `all-talents.tsv` across **all 40 specs**, in any of the three Evoker `ability-inventory.tsv`, or in `section-3-corroborated.tsv` / `section-4-catalogue.tsv`, and no Midnight-range ID of that name was ever minted. Gone **class-wide**, not just from Preservation. The **Flameshaper** subtree is still live for this spec — its actives-and-passives enumerate with **Fire Torrent** `1265992` and **Consume Flame** `444088` (both `talent-passive`), and neither is a measured rename of Engulf. *[Tier 1: reconcile-ledger.md §4 @ 12.0.7.67808.]* |
| Spiritbloom | **no longer acquirable** | No acquisition row for **any** of the 40 specs: absent from `all-talents.tsv` and from all three Evoker `ability-inventory.tsv`. The only surviving trace anywhere is residue in `section-3-corroborated.tsv` — `Spiritbloom` `367226` reached as an `override-aura` off **Font of Magic** `375783` — which is exactly the indirect-reach class that table exists to record, and Font of Magic's live 12.0.7 tooltip is only *"Your empower spells' maximum level is increased by 1."* The removal was previously a Tier-3 (maxroll) claim carrying an `@verify-ingame`; Tier-1 data now settles it. **Do not re-open.** |

*[Tier 1: `all-talents.tsv` + `ability-inventory.tsv` @ 12.0.7.67808.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- ⚠ **`Emerald Communion` `370960` was NOT removed.** An earlier revision of this
  file grouped it with Spiritbloom and Engulf as a "Midnight removal" on the
  strength of a Tier-3 maxroll guide. Tier 1 disagrees: it is **live in this
  spec's `ability-inventory.tsv`** as a `pvp-talent`, `castable=true`, **180s**,
  tooltip *"Commune with the Emerald Dream, restoring 20% health and 2% mana
  every 0.9 sec for 4.5 sec…"*. It did not vanish — it moved to the PvP talent
  row, so it is unselectable in raid/M+ but perfectly real in PvP. Do not
  re-assert the removal.
- **`Return` `361227` is the Evoker battle res, not a teleport.** Tooltip:
  *"Brings a dead party member back to life with 35% health and mana. Cannot be
  cast when in combat."* — `class-baseline`, 10s cast, no cooldown column. An
  earlier revision described it as "teleport back to a previously placed point".
  The same wrong line was carried by all three Evoker specs.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. The Spiritbloom /
Emerald Communion marker this file used to carry was never an in-game question:
`all-talents.tsv` and `ability-inventory.tsv` answered both, and in opposite
directions.
