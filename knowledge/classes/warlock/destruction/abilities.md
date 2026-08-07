---
title: Destruction Warlock — off-inventory abilities (Midnight S1)
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

# Destruction Warlock — off-inventory abilities

**Everything about a Destruction ability is in `ability-inventory.md`** — 169
rows, one row each carrying spellID, cooldown, cast time, origin, talent/hero
placement and the full tooltip. It is generated, Tier-1, DB2-pinned to
`12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Destruction ability is not named below, do not research it — read its
> row in `ability-inventory.md` and go.** Rotation and the shard economy →
> `rotation.md`. Talents/hero pick → `builds.md`. Both sections here are
> **closed lists, not backlogs.**

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
| `19647` | Spell Lock | **Your only kick.** It is on the **Felhunter's** skill line (189), not yours — the pet path has no spec granularity in any DB2 table, so no row can attribute it to Destruction. In `../../_abilities/pet-family-annex.tsv` (cd 24s); catalogued `prose-only` in `section-4-catalogue.md`. Pressed via *Command Demon* `119898`, which **is** in the inventory and carries the `Interrupt` seed bucket — but Command Demon has no interrupt of its own, it delegates. ⚠ **Lose the Felhunter, lose the kick.** The Felhunter's `Devour Magic` `19505` reaches Destruction by the same path and is likewise uncatalogued. |

**Destruction has no baseline personal interrupt, and that claim holds.** The only
`Interrupt`-bucketed row in its 169-row inventory is *Command Demon*, a delegator.
Plan interrupt assignments around the pet; the fallbacks are stops, not kicks
(Shadowfury / Howl of Terror / Mortal Coil / Sayaad's Seduction).

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
| Health Funnel | **not acquirable at 12.0.7** | zero rows across `all-abilities.tsv` (all 40 specs), `all-talents.tsv`, `pet-family-annex.tsv` and both catalogue tables. Nine spells carry the name in raw `SpellName` and **not one** attaches to an acquisition table — no talent node, no class skill line, no spec grant. It had a row here as a pet-sustain channel; deleted rather than left open, because the absence is measured. Pet healing is the pet's own business; don't plan around funnelling. |
| Summon Felguard `30146` | **Demonology-only — Destruction cannot summon a Felguard** | `all-abilities.tsv` carries exactly one row for this name, `Warlock / Demonology / 266 / talent-active`, and `all-talents.tsv` places it on the **demonology spec tree**. The spec seed listed it; wrong. ⚠ *Fel Domination*'s tooltip still names Felguard — shared class text, not an acquisition claim. Consequence: **`Axe Toss` `89766` is unreachable for Destruction.** |
| Healthstone `6262` | **not a learned player ability** | `6262` is the **item-use** spell and attaches to no acquisition table. The player ability is **`Create Healthstone`** `6201`, a SkillLineAbility on line 849 (Warlock) — already an inventory row under that name. Name-drift verdict recorded in `../../_abilities/reconcile-ledger.md`. |
| Curse of Weakness → "the Hellcaller curse" | **Curse of Weakness is baseline; the Hellcaller line is a separate choice node** | `Curse of Weakness` `702` is class-baseline. The Hellcaller choice is **Blight of Weakness / Blight of Tongues**, both present as their own inventory rows. Do not merge them into one upgraded curse. |

*[Tier 1: `all-abilities.tsv` / `all-talents.tsv` / `pet-family-annex.tsv`
@ 12.0.7.67808.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **`Fire and Brimstone` `196408` does NOT grant fragments.** `talent-passive`,
  `castable=false`; its 12.0.7 tooltip is damage-only — *"Incinerate now also hits
  all enemies near your target for 25% damage."* Verified in the generated
  inventory, 2026-08-06. An earlier revision of this file said otherwise.
- **`Embers of Nihilam` `1265770` is a PASSIVE**, not a button — `talent-passive`,
  `castable=false`. Casting Incinerate has a chance to evoke *Echo of Sargeras*.
  An earlier revision called it a "situational burst button"; nothing in the
  rotation is waiting on you to press it. Same for **`Ruination` `428522`**
  (`talent-passive`): the *button* is Chaos Bolt, which becomes Ruination after a
  Pit Lord summon.
- **`Shadowburn` `17877` does not have 2 charges.** DB2 gives it
  `ChargeCategory = 0` and `RecoveryTime = 0` (against Conflagrate `17962`,
  `ChargeCategory = 672`), the inventory records cd 0, and a live in-client
  capture found Shadowburn raising **no** `Available` / `OnCooldown` /
  `ChargeGained` Cooldown-Manager alerts while Conflagrate raised all three. The
  old "2 charges, ~12s recharge" is a pre-Midnight tooltip. ⚠ Note the spell's
  *own* 12.0.7 tooltip still reads *"…and refunds a charge if the target dies"* —
  legacy wording against four Tier-1 signals; the charge fields win.
- **`Infernal Bolt`: 3 Soul Shards (30 fragments) on Destruction, not 2.** The
  `Infernal Bolt` `433891` row is an unresolved DB2 template
  (`generating ${$s2/10} Soul Shards`), but the Destruction-keyed **`Secrets of
  the Coven` `428518`** row resolves the same text: *"…generating **3 Soul
  Shards**."* That settles the old "20 or 30 and the sources disagree" note, which
  carried an `@verify-ingame`. The sibling capture `maxroll-raid.md` (Tier 3,
  `verbatim: true`) says **2** — a lower tier may corroborate Tier 1 but must
  never overwrite it.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact cooldown /
charges / shard yield is uncertain"* is **not** one: `ability-inventory.md`
carries the Tier-1 number.
