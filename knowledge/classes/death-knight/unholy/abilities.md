---
title: Unholy Death Knight — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ../../_abilities/spell-descriptions.tsv  # tier 1 — api-resolved tooltips @ 12.0.7.67808
  - ../../_abilities/all-abilities.tsv  # tier 1 — the 40-spec acquisition union, 7,065 rows
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree
confidence: high
---

# Unholy Death Knight — off-inventory abilities

**Everything about an Unholy ability is in `ability-inventory.md`** — specID 252,
**164 rows**, one row each carrying spellID, cooldown, cast time, origin,
talent/hero placement and the full tooltip. It is generated, Tier-1, DB2-pinned
to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If an Unholy ability is not named below, do not research it — read its row
> in `ability-inventory.md` and go.** Rotation → `rotation.md`. Talents/hero pick
> → `builds.md`. Both sections here are **closed lists, not backlogs.**

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
| `` | Necrotic Coil | **Runtime replacement for Death Coil.** Named in the Tier-1 api-resolved tooltip of **Forbidden Knowledge** `1242158`: *"Army of the Dead siphons the power of the fallen, transforming Death Coil and Epidemic into Necrotic Coil and Graveyard for 30 sec."* An override swaps the button in place, so no acquisition table ever lists it: zero exact-name rows in `all-talents.tsv`, in `all-abilities.tsv` (7,065 rows) and in all 40 `ability-inventory.tsv` files — it exists only inside that one tooltip string. Its own text is spliced into Forbidden Knowledge's row, so read the ID off that row rather than guessing one. |
| `` | Graveyard | Same mechanism, same sentence, same 30s window — the **Epidemic** side of the Forbidden Knowledge transform. Recorded here for the same reason: an override-only name that no join can reach. |

The ghoul's pet-bar buttons are **not** listed here for Unholy: **Gnaw** `47481`
is already a row in `ability-inventory.tsv` (`cdm-only`, from Blizzard's Cooldown
Manager set), and the rest of skill line 782 — **Leap** `47482`, **Huddle**
`47484`, **Claw** `47468`, and the Dark-Transformation upgrades **Monstrous
Blow** `91797`, **Shambling Rush** `91802`, **Putrid Bulwark** `91837`,
**Sweeping Claws** `91778` — is enumerated in
`../../_abilities/pet-family-annex.tsv`. (Blood and Frost *do* carry Gnaw in their
§A: the CDM residue only rescues it for Unholy.)

## §B — Encountered, and we believe not valid

Names that appear in guides, older builds or other people's notes, which we have
checked and believe are **not** part of this spec at 12.0.7. Listed so the next
reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| Vile Contagion | **not acquirable by any spec at 12.0.7** | zero exact-name hits in `all-talents.tsv` (all 40 specs), zero in `all-abilities.tsv` (7,065 rows), zero across all 40 `ability-inventory.tsv` files. A War Within Unholy talent, gone in the Midnight rework. |
| Unholy Assault | **not acquirable by any spec at 12.0.7** | same check, same result |
| Defile | **not acquirable by any spec at 12.0.7** | same check, same result |
| Festering Wound | **no longer the live maintenance mechanic** | **Festering Strike** `85948` (class-baseline) now reads *"corrupt your weapon with blight, causing your next 2-3 Scourge Strikes to summon a **Lesser Ghoul**"*; Soul Reaper `343294` consumes Lesser Ghouls. No `Festering Wound` row in any acquisition table. ⚠ **One Tier-1 string still contradicts this:** the class-baseline **Apocalypse** `220143` tooltip says *"bursting up to 6 Festering Wounds"*. Treat that tooltip as stale — the rest of the 12.0.7 kit resolves to Lesser Ghoul — but do **not** delete Apocalypse over it (see Corrections). |

*[Tier 1: `all-talents.tsv` + `all-abilities.tsv` + the 40 generated
`ability-inventory.tsv` files + `spell-descriptions.tsv`, all @ 12.0.7.67808.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode — all three were
stated flatly in the revision this file replaces:

- **`Apocalypse` `220143` was NOT removed.** It is `class-baseline` via
  `SkillLineAbility:796`, `castable=true`, cd **90s**, and it is a row in **all
  three** DK specs' inventories. What is true is narrower: it has **zero** hits in
  `all-talents.tsv`, i.e. it is not on the 12.0.7 talent tree. **"Not on the tree"
  is not "not learned"** — the earlier "removed since The War Within" line
  collapsed the two.
- **`Zombify` `210128` is a live spell** — a castable Unholy **PvP talent**
  (`origin=pvp-talent`, source `PvpTalent`): reanimates a corpse into a zombie
  that walks at your target and explodes for a stun. The earlier revision said
  *"'Zombify' is not a live spell name"*. It is.
- **`Raise Abomination` `1242608` and `Summon Gargoyle` `1242147` are PASSIVES**,
  not pressed summons — `talent-passive`, `castable=false`, cd 0. Both *modify*
  Army of the Dead (*"Army of the Dead now raises an Abomination…"* / *"…now
  summons a Gargoyle…"*). The earlier revision listed them as separate "Major
  cooldown (summon)" buttons with their own cooldowns and an `@verify-ingame` on
  Raise Abomination's CD. There is no such button and there was no such question.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact cooldown / RP
cost is uncertain"* is **not** one: `ability-inventory.md` carries the Tier-1
number.
