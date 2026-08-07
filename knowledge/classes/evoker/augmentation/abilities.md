---
title: Augmentation Evoker — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree @ 12.0.7.67808
  - ../../_abilities/section-4-catalogue.tsv  # tier 1 derived — the prose-only catalogue this file feeds
  - ../../_abilities/reconcile-ledger.md  # tier 1 derived — the verdicts applied 2026-08-06
confidence: high
---

# Augmentation Evoker — off-inventory abilities

**Everything about an Augmentation ability is in `ability-inventory.md`** — 160
rows (specID 1473), each carrying spellID, cooldown, cast time, origin,
talent/hero placement and the full tooltip. It is generated, Tier-1, DB2-pinned
to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If an Augmentation ability is not named below, do not research it — read
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

| spellID | name | how we know, and why the join misses it |
|---|---|---|
| | Renewing | **Looks like a harvest artifact, kept verbatim anyway.** The prose this file replaces carried one composite row, `Renewing / Verdant Embrace`, and the catalogue harvester split it on the `/`. The two real buttons both *are* in the generated inventory — **Renewing Blaze** `374348` (`talent-active`, castable) and **Verdant Embrace** `360995` (`talent-active`, castable, 0.5s) — so there is no missing Evoker button named "Renewing". It stays here spelled exactly as `section-4-catalogue.tsv` records it; a separate deliberate pass retires artifacts. Not losing data and improving data are different jobs. |

## §B — Encountered, and we believe not valid

Names that appear in guides, older builds or other people's notes, which we have
checked and believe are **not** pressable buttons for this spec at 12.0.7.
Listed so the next reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| Black Attunement | **not a button — a state** | No row of this name in any acquisition table for any of the 40 specs (`all-talents.tsv`, and this spec's `ability-inventory.tsv`). It is one of the two states of the **Draconic Attunements** talent `403208`, whose tooltip enumerates both states. The nearest IDs that do exist are `Black Aspect's Favor` `407254` / `Bronze Aspect's Favor` `407244`, both `cdm-only` **buff** rows, and per `Aspects' Favor` `407243` they are activated by casting **Obsidian Scales** / **Hover** — not pressed. |
| Bronze Attunement | **not a button — a state** | Same check, same result: the other state of `Draconic Attunements` `403208`. |

*[Tier 1: `all-talents.tsv` + `ability-inventory.tsv` @ 12.0.7.67808.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **`Draconic Attunements` `403208` is a PASSIVE**, not a pressed group-buff
  cooldown — `talent-passive`, `castable=false`, node type `PASSIVE` on the
  tree, and Tier 1 has *no* castable spell of that name at all. An earlier
  revision of this file listed it as a button in the ability table. Don't assume
  a keybind exists for it. *[Tier 1: reconcile-ledger.md §4 @ 12.0.7.67808.]*
- **`Return` `361227` is the Evoker battle res, not a teleport.** Tooltip:
  *"Brings a dead party member back to life with 35% health and mana. Cannot be
  cast when in combat."* — `class-baseline`, 10s cast, no cooldown column. An
  earlier revision described it as "teleport back to a location you set with a
  portal", which is a different game's spell. The same wrong line was carried by
  all three Evoker specs.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact cooldown / cast
time / charge count is uncertain"* is **not** one: `ability-inventory.md`
carries the Tier-1 number.
