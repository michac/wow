---
title: Assassination Rogue — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.tsv  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ./ability-inventory.md  # tier 1 — same data, rendered (tooltips quoted below come from here)
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree
  - ../../_abilities/section-4-catalogue.tsv  # tier 1 derived — the off-inventory catalogue
  - ../../_abilities/section-3-corroborated.tsv  # tier 1 derived — indirectly-reached spells
confidence: high
---

# Assassination Rogue — off-inventory abilities

**Everything about an Assassination ability is in `ability-inventory.md`** —
specID **259**, **172 rows**, each carrying spellID, cooldown, cast time, origin,
talent/hero placement and the full tooltip. It is generated, Tier-1, DB2-pinned to
`12.0.7.67808`, and regenerated on patch day.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If an Assassination ability is not named below, do not research it — read
> its row in `ability-inventory.md` and go.** Rotation → `rotation.md`.
> Talents/hero pick → `builds.md`. Both sections here are **closed lists, not
> backlogs.**

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
resolves to a row in `ability-inventory.tsv` — including the two that look like
gaps. **`Mark for Death` `1293340`** is present with origin `cdm-only` (carried by
the Cooldown-Manager set, no acquisition table — but still *in* the inventory), and
**`Cold Blood` `1264297`** is already catalogued in
`../../_abilities/section-4-catalogue.tsv` as `trigger-effect`, reached from
Cold Blooded Killer `382245`. Neither needs a row here.

## §B — Encountered, and we believe not valid

Names that appear in guides, older builds or other people's notes, which we have
checked and believe are **not** part of this spec at 12.0.7. Listed so the next
reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| `Poisons` | **not a spell** | no row named `Poisons` in the 172-row inventory, and no `Poisons` talent in `all-talents.tsv` for any spec of any class — only `Improved Poisons` `381624` and `Virulent Poisons` `381543`, both passives. "Applying poisons" means casting one of the eight concrete imbues/spells that *are* rows: Deadly `2823`, Amplifying `381664`, Wound `8679`, Instant `315584`, Crippling `3408`, Numbing `5761`, Atrophic `381637`, plus Poisoned Knife `185565`. An earlier revision carried a single catch-all "Poisons (apply)" row naming no Tier-1 spell. |
| Indiscriminate Carnage | **not on the tree** | absent from `all-talents.tsv` for **every** spec of **every** class, and absent from all three rogue inventories. Method (Tier 3, 2026-06-16) says removed in Midnight; Tier 1 agrees. |
| Master Assassin | **not on the tree** | same check, same result. ⚠ Do not confuse with `Master Poisoner` `378436`, which **is** a live passive on all three rogue specs. |
| Exsanguinate | **not on the tree** | same check, same result |
| Vendetta | **not on the tree** | same check, same result — the live 2-min burst cooldown is **Deathmark**, which is in the inventory. |
| Sepsis | **not on the tree** | same check, same result |
| Serrated Bone Spike | **not on the tree** | same check, same result |
| Marked for Death | **wrong name** | nothing named `Marked for Death` in any rogue inventory, and the historic `137619` appears in none of them. The live spell is **`Mark for Death` `1293340`** (`cdm-only`), which *is* an inventory row. |
| Grappling Hook | **Outlaw-only** | `195457`, `class-baseline` → **Outlaw** only; absent from Assassination's 172 rows. ⚠ The trap: the string *does* occur in this spec's inventory, inside the **tooltip of `Death's Arrival` `454433`** (Fatebound hero passive, which references it) — that is description text, not a name row. Assassination's mobility is Shadowstep and Sprint. |

*[Tier 1: `ability-inventory.tsv` + `all-talents.tsv`, both DB2 @ 12.0.7.67808.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **Shiv is not "the Toxic Stiletto talent".** `Shiv` `5938` is its own
  **`talent-active`** node on the class tree; `Toxic Stiletto` `1267182` is a
  separate class-tree **passive** whose entire Tier-1 tooltip is *"Shiv's Energy
  cost is reduced by 20, its cooldown is reduced by 15 sec, and its range is
  increased by 3 yds."* It **modifies** Shiv, it does not grant it — and Shiv is an
  off-hand attack, not the "thrown poison applicator" an earlier revision (from
  Tier 3) described. Both spells are inventory rows; read them there.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. Every `@verify-ingame` this
file used to carry (Crimson Tempest's Midnight rework, the Shiv/Toxic Stiletto
attribution, per-ability cooldowns) is answered by the Tier-1 tooltip and cooldown
columns in `ability-inventory.md`.
