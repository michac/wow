---
title: Beast Mastery Hunter — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ../../_abilities/reconcile-ledger.md  # tier 1 derived — gaps G3 (SkillLine 183) and G5 (pet path)
  - ../../_abilities/section-3-corroborated.tsv  # tier 1 — Primal Rage 264667, Kill Shot override link
  - ../../_abilities/pet-family-annex.tsv  # tier 1 — pet skill lines @ 12.0.7.67808
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree
confidence: high
---

# Beast Mastery Hunter — off-inventory abilities

**Everything about a Beast Mastery ability is in `ability-inventory.md`** — 189
rows, each carrying spellID, cooldown, cast time, origin, talent/hero placement
and the full tooltip. It is generated, Tier-1, DB2-pinned to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Beast Mastery ability is not named below, do not research it — read
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
> `section-4-catalogue.md`. Rename this heading or drop the `name` column header
> and these rows **silently vanish from the catalogue**, with no marker and no
> warning. §B is deliberately *not* harvested: it asserts the opposite.

| spellID | name | how we know, and why the join misses it |
|---|---|---|
| `75` | Auto Shot | Real and castable. `SkillLineAbility` on SkillLine **183 "GENERIC (DND)"**, which is outside the generator's two closed skill-line allowlists — so it is invisible for *every* Hunter spec. A **tool gap**, not a removal (ledger gap **G3**). No `@verify-ingame` on purpose: logging in cannot answer which DB2 skill line a generator reads. |
| `883`, `83242`–`83245` | Call Pet 1 … Call Pet 5 | ⚠ **This `name` string looks like a harvest artifact** — it is range notation, not a live spell name. Reproduced verbatim under rule R1; a separate deliberate pass owns fixing it, and this row must not be split or reworded here. The underlying reality: all **five** spells (`Call Pet 1` 883, `Call Pet 2` 83242, `Call Pet 3` 83243, `Call Pet 4` 83244, `Call Pet 5` 83245) **are** in `ability-inventory.tsv` as `class-baseline` / `SkillLineAbility:795`. Five separate spells, one per stable slot — each needs its own keybind. Bare "Call Pet" resolves in `SpellName` but attaches to nothing. |
| `264667` | Primal Rage | The pet-provided party-wide Lust. It rides `SpecializationSpells` → the **pet** spec *Ferocity*, and the pet path carries **no spec granularity in any DB2 table** (ledger gap **G5**), so no row can attribute it to Beast Mastery. ⚠ It is **not** in `pet-family-annex.tsv` either — the annex covers pet *skill lines*, and this is a pet *specialisation*. Already corroborated in `section-3-corroborated.tsv` (`GET /data/wow/spell/264667` → 200). **Whether you can Lust is decided by which pet you bring, not by a talent.** |

Also invisible per-spec for the same G5 reason, and recorded in
`../../_abilities/pet-family-annex.tsv` rather than here: the shared Hunter pet
line **270 "Pet - Generic Hunter"** (`Growl` 2649, `Dash` 61684, `Intimidation`
24394, …). Read the annex before concluding a pet button does not exist.

## §B — Encountered, and we believe not valid

Names that appear in guides, older builds or other people's notes, which we have
checked and believe are **not** part of this spec at 12.0.7. Listed so the next
reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| Kill Shot | **not on the Beast Mastery tree** | `all-talents.tsv` has exactly one Kill Shot node — 109490, spec tree, resolved by TraitCond → SpecSet to **hunter/marksmanship only**. Absent from BM's `ability-inventory.tsv`. ⚠ **It does appear in a BM row of `section-3-corroborated.tsv`** as `override-aura` reached from Black Arrow 466932 — that link is `class-shared`, i.e. join residue, **not** an acquisition. BM has no execute button; execute-window pressure comes from Black Arrow + Deathblow (Dark Ranger) instead. |
| Muzzle | **Survival's, not reachable from here** | `all-talents.tsv`: node 79837, class tree, gated to **hunter/survival only**. BM's kick is `Counter Shot` 147362 (node 102292, gated Beast Mastery), already in `ability-inventory.tsv` — and it is ranged, so BM never closes to melee to interrupt. |
| Ancient Hysteria | **does not exist at 12.0.7** | Neither 19372 nor 90355 attaches to a trait node, `SkillLineAbility`, `SpecializationSpells` or `PvpTalent` at 12.0.7.67808. The live pet Lust is **Primal Rage** 264667 (§A). |

*[Tier 1: `all-talents.tsv` + `ability-inventory.tsv` + `section-3-corroborated.tsv`,
all @ DB2 12.0.7.67808; verdicts recorded in `../../_abilities/reconcile-ledger.md`.]*

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact cooldown / Focus
cost is uncertain"* is **not** one: `ability-inventory.md` carries the Tier-1
number.
