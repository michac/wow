---
title: Subtlety Rogue — off-inventory abilities (Midnight S1)
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

# Subtlety Rogue — off-inventory abilities

**Everything about a Subtlety ability is in `ability-inventory.md`** — specID
**261**, **180 rows**, each carrying spellID, cooldown, cast time, origin,
talent/hero placement and the full tooltip. It is generated, Tier-1, DB2-pinned to
`12.0.7.67808`, and regenerated on patch day.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Subtlety ability is not named below, do not research it — read its row
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
resolves to a row in `ability-inventory.tsv`. Two Subtlety names reached
*indirectly* are already recorded in `../../_abilities/section-3-corroborated.tsv`
and do not belong here: **`Amplifying Poison` `381664`** (`trigger-effect`, reached
from Master Poisoner `378436`) and **`Cold Blood` `1264297`** (`trigger-effect`,
from Cold Blooded Killer `382245`). That file also carries a **`Dispatch` `2098`**
row for Subtlety — see the escalation note under Corrections before believing it.

## §B — Encountered, and we believe not valid

Names that appear in guides, older builds or other people's notes, which we have
checked and believe are **not** part of this spec at 12.0.7. Listed so the next
reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| `Poisons` | **not a spell** | no row named `Poisons` in the 180-row inventory, and no `Poisons` talent in `all-talents.tsv` for any spec of any class — only `Virulent Poisons` `381543`, a passive. "Applying poisons" means casting one of the six concrete imbues that *are* rows: Deadly `2818`, Wound `8679`, Instant `315584`, Crippling `3408`, Numbing `5761`, Atrophic `381637`. An earlier revision carried a single catch-all "Poisons (apply)" row naming no Tier-1 spell. |
| Symbols of Death | **not acquirable at 12.0.7** | none of `212283` / `227151` / `247895` / `319063` / `328077` appears in any of the three rogue inventories, none attaches to a trait node, `SkillLineAbility`, `SpecializationSpells` or `PvpTalent`, and there is no Symbols of Death node on the live Rogue tree (852) in `all-talents.tsv` for **any** spec. An earlier revision hedged with "appears removed/reworked in Midnight" — settled: it is **gone**, not merely off the APL. Do not restore the row. *(via `../../_abilities/reconcile-ledger.md`)* |
| Rupture | **not a Subtlety ability** | `Rupture` `1943` is `class-baseline` → **Assassination** only; neither the name nor the ID appears anywhere in Subtlety's 180 rows, and it is not a talent for Subtlety in `all-talents.tsv`. The previous revision's softer "not an active ability in the S1 APL" understated this: Subtlety cannot cast it at all. Its bleed pressure is Find Weakness + Black Powder. |
| Grappling Hook | **Outlaw-only** | `195457`, `class-baseline` → **Outlaw** only; the string does not occur anywhere in Subtlety's inventory, not even in tooltip text. It is **absent from `PvpTalent` entirely** (Subtlety's 11 `pvp-talent` rows are Smoke Bomb, Dismantle, Death from Above, Control is King, Dagger in the Dark, Distracting Mirage, Maneuverability, Preemptive Maneuver, Silhouette, Thick as Thieves, Thief's Bargain), so any "PvP talent" framing is wrong twice over. Subtlety's mobility is Shadowstep and Sprint. |
| Marked for Death | **wrong name** | nothing named `Marked for Death` in any rogue inventory, and the historic `137619` appears in none of them. The live spell is **`Mark for Death` `1293340`** (`cdm-only`), which *is* a Subtlety inventory row. |
| Improved Shadow Dance | **not on the tree** | absent from `all-talents.tsv` for every spec of every class. Controls present in the same check: `Double Dance`, `Danse Macabre`, `Premeditation`, `Shadow Focus`, `The Rotten`, `Perforated Veins`, `Shuriken Tornado` — all live Subtlety talents. |
| Sepsis | **not on the tree** | same check, same result |

*[Tier 1: `ability-inventory.tsv` + `all-talents.tsv`, both DB2 @ 12.0.7.67808.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **Subtlety's `Coup de Grace` empowers Eviscerate, not Dispatch.** The Tier-1
  tooltip on `441423` reads *"…your next **Eviscerate** will be performed as a Coup
  de Grace…"*. ⚠ `../../_abilities/section-3-corroborated.tsv` nonetheless carries
  a **`Dispatch` `2098` → Subtlety** row, reached by an `override-aura` on Coup de
  Grace `462127` and flagged `class-shared`. Dispatch is the **Outlaw** finisher
  and has no row in Subtlety's inventory. Treat that corroborated row as the
  class-shared spell leaking across specs, **not** as a Subtlety button — and do
  not add Dispatch to §A on the strength of it. (Left as-is here; that file is out
  of this file's scope to edit.)

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. The `@verify-ingame` this
file used to carry ("confirm Rupture/SnD are truly off the bars and exact reworked
numbers") is answered at Tier 1: Rupture is not acquirable by this spec at all
(§B), `Slice and Dice` `315496` **is** a live `class-baseline` row, and
`Deepening Shadows` `185314`'s tooltip states the rework verbatim — *"Shadow Dance
duration is increased by 150% of your Haste stat."*
