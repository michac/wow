---
title: Outlaw Rogue — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.tsv  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ./ability-inventory.md  # tier 1 — same data, rendered (tooltips quoted below come from here)
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree
  - ../../_abilities/section-3-corroborated.tsv  # tier 1 derived — indirectly-reached spells
  - ../../_abilities/section-4-catalogue.tsv  # tier 1 derived — the off-inventory catalogue
  - ../../_abilities/reconcile-ledger.md  # tier 1 derived — the 12.0.7.67808 adjudication
confidence: high
---

# Outlaw Rogue — off-inventory abilities

**Everything about an Outlaw ability is in `ability-inventory.md`** — specID
**260**, **171 rows**, each carrying spellID, cooldown, cast time, origin,
talent/hero placement and the full tooltip. It is generated, Tier-1, DB2-pinned to
`12.0.7.67808`, and regenerated on patch day.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If an Outlaw ability is not named below, do not research it — read its row
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

_None known for this spec._

Checked, not assumed: `section-4-catalogue.tsv` carries **no `prose-only` row for
any Rogue spec**, and every ability named in this file's previous prose table
resolves to a row in `ability-inventory.tsv` — with the single exception of
**`Restless Blades` `79096`**, which is a **passive**, not a button, and already
has a Tier-1 record elsewhere. See the correction below; do not promote it here.

## §B — Encountered, and we believe not valid

Names that appear in guides, older builds or other people's notes, which we have
checked and believe are **not** part of this spec at 12.0.7. Listed so the next
reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| `Poisons` | **not a spell** | no row named `Poisons` in the 171-row inventory, and no `Poisons` talent in `all-talents.tsv` for any spec of any class — only `Virulent Poisons` `381543`, a passive. "Applying poisons" means casting one of the six concrete imbues that *are* rows: Deadly `2818`, Wound `8679`, Instant `315584`, Crippling `3408`, Numbing `5761`, Atrophic `381637`. An earlier revision carried a single catch-all "Poisons (apply)" row naming no Tier-1 spell. ⚠ Note **Deadly Poison is `2818` for Outlaw**, not Assassination's `2823`. |
| Crackshot | **not on the tree** | absent from `all-talents.tsv` for **every** spec of **every** class, and absent from all three rogue inventories. The old "Crackshot / Adrenaline-Rush-extension" play the previous revision flagged as removed is confirmed gone at Tier 1. |
| Underhanded Upper Hand | **not on the tree** | same check, same result |
| Ghostly Strike | **not on the tree** | same check, same result |
| Dreadblades | **not on the tree** | same check, same result |
| Greenskin's Wickers | **not on the tree** | same check, same result |
| Count the Odds | **not on the tree** | same check, same result. Controls present in the same check: `Loaded Dice`, `Ace Up Your Sleeve`, `Fan the Hammer`, `Deft Maneuvers`, `Hidden Opportunity`, `Audacity` — all live Outlaw talents. |
| Take 'em by Surprise | **not on the tree** | same check, same result |
| Sepsis | **not on the tree** | same check, same result |
| Mark for Death / Marked for Death | **not an Outlaw ability** | `Mark for Death` `1293340` is a real spell but its `cdm-only` rows exist for **Assassination and Subtlety only** — neither name appears anywhere in Outlaw's 171 rows, and the historic `Marked for Death` `137619` appears in no rogue inventory at all. |

*[Tier 1: `ability-inventory.tsv` + `all-talents.tsv`, both DB2 @ 12.0.7.67808.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **`Restless Blades` `79096` was not removed — the generator drops it by
  design.** It *is* Tier-1 attached to Outlaw (`SpecializationSpells`), but it is
  **passive**, and `gen_abilities` drops passive `SpecializationSpells` rows
  (`../../_abilities/reconcile-ledger.md` §5 G1). It is carried instead in
  `../../_abilities/section-3-corroborated.tsv`, confirmed live by
  `GET /data/wow/spell/79096` → 200. It is a passive, so it does **not** belong in
  §A either. Do not "correct" its absence from the inventory into a removal.
- **`Killing Spree` `51690` has a base cooldown of `180s`, not ~60s.** Tier-1
  `ability-inventory.tsv` reads `180`; the ~60s figure Tier-3 guides quote is the
  *effective* cooldown after Restless Blades refunds, not the base. Its tooltip
  also settles what it costs: *"Finishing move that unleashes a barrage of
  gunfire… Number of strikes increased per combo point"* — it **is** a combo-point
  finisher (and restores 1 CP every 0.45s while channelling).

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. Every `@verify-ingame` this
file used to carry is answered by the Tier-1 tooltip and cooldown columns in
`ability-inventory.md`: Roll the Bones' staged rework is spelled out verbatim in
`1214909`'s tooltip ("1 set or better… 2 sets or better… 3 sets or better…
Jackpot"), and Killing Spree's combo-point behaviour is in the row above.
