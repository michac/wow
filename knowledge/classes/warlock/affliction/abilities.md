---
title: Affliction Warlock — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ../../_abilities/pet-family-annex.tsv  # tier 1 — pet skill lines @ 12.0.7.67808
  - ../../_abilities/all-abilities.tsv  # tier 1 — every spec's acquisition rows @ 12.0.7.67808
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree
  - ../../_abilities/reconcile-ledger.md  # tier 1 derived — the name/origin verdicts applied here
confidence: high
---

# Affliction Warlock — off-inventory abilities

**Everything about an Affliction ability is in `ability-inventory.md`** — 164
rows, one row each carrying spellID, cooldown, cast time, origin, talent/hero
placement and the full tooltip. It is generated, Tier-1, DB2-pinned to
`12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If an Affliction ability is not named below, do not research it — read its
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
| `19647` | Spell Lock | **Your only kick.** It is on the **Felhunter's** skill line (189), not yours — the pet path has no spec granularity in any DB2 table, so no row can attribute it to Affliction. In `../../_abilities/pet-family-annex.tsv` (cd 24s). Pressed via *Command Demon* `119898`, which **is** in the inventory and carries the `Interrupt` seed bucket — but Command Demon has no interrupt of its own, it delegates. ⚠ **Lose the Felhunter, lose the kick.** The Felhunter's `Devour Magic` `19505` reaches Affliction by the same path and is likewise uncatalogued. |

**Affliction has no baseline personal interrupt, and that claim holds.** The only
`Interrupt`-bucketed row in its 164-row inventory is *Command Demon*, which is a
delegator. Plan interrupt assignments around the pet, not a self-cast.

**This category is real and measured, not an edge case.** Across all 40 specs,
pet-path and runtime-override buttons live in no spec-keyed DB2 table: `Devour`,
`Pierce the Veil`, `Templar Slash`, `Void Volley` and `Heroic Strike` are all real
pressed buttons whose *only* record anywhere is a hand-written row like this one.

## §B — Encountered, and we believe not valid

Names that appear in guides, older builds or other people's notes, which we have
checked and believe are **not** part of this spec at 12.0.7. Listed so the next
reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| Summon Felguard `30146` | **Demonology-only — Affliction cannot summon a Felguard** | `all-abilities.tsv` @ 12.0.7.67808 carries exactly one row for this name, `Warlock / Demonology / 266 / talent-active`, and `all-talents.tsv` places it on the **demonology spec tree**. An earlier revision of this file listed Felguard among the pets Affliction may pick "on utility" — wrong. ⚠ *Fel Domination*'s tooltip still names Felguard; that is shared class text, not an acquisition claim. Consequence: **`Axe Toss` `89766` is unreachable for Affliction**, so Spell Lock is the only kick. |
| Healthstone `6262` | **not a learned player ability** | `6262` is the **item-use** spell and attaches to no acquisition table. The player ability is **`Create Healthstone`** `6201`, a SkillLineAbility on line 849 (Warlock) — already an inventory row under that name. Name-drift verdict recorded in `../../_abilities/reconcile-ledger.md`. |
| Health Funnel | **not acquirable at 12.0.7** | zero rows across `all-abilities.tsv` (all 40 specs), `all-talents.tsv`, `pet-family-annex.tsv` and both catalogue tables. No talent node, no class skill line, no spec grant, no pet line. Pet healing is the pet's own business now; don't plan around funnelling. Measured absence, not merely unconfirmed. |

*[Tier 1: `all-abilities.tsv` / `all-talents.tsv` / `pet-family-annex.tsv`
@ 12.0.7.67808.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **`Shadow of Nathreza` `1261984` is a PASSIVE**, not a pressed cooldown —
  `talent-passive`, `castable=false`, cd 0, no resource. It makes *Haunt* call a
  demonic soul that damages the host and 3 nearby enemies suffering your
  Corruption. An earlier revision called it a *"rotational cooldown (spec apex,
  **active**), Soul Shards, ~instant · CD"* and put an `@verify-ingame` on the
  "exact cost/effect". Wrong on origin, resource and castability, and it was
  never an in-game question.
- **`Malefic Grasp` `1261149` is likewise `talent-passive`, `castable=false`.**
  The talent is passive; the *button* is Shadow Bolt, which transforms into
  Malefic Grasp while Darkglare is up. Do not file it as a separately-learned
  channel.
- **`Curse of Weakness` `702` is class-baseline**, castable, cd 0. An earlier
  revision carried an `@verify-ingame` asking "baseline vs talent availability in
  12.0.7" — the inventory answered it.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact cooldown / cost
is uncertain"* is **not** one: `ability-inventory.md` carries the Tier-1 number.
