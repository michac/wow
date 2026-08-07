---
title: Feral Druid — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree @ 12.0.7.67808
  - ../../_abilities/all-abilities.tsv  # tier 1 — the 40-spec union, for absence checks
  - ../../_abilities/spell-descriptions.tsv  # tier 1 — resolved English tooltips via /data/wow/spell/{id}
  - ../../_abilities/reconcile-ledger.md  # tier 1 derived — the per-row verdicts applied to this file
confidence: high
---

# Feral Druid — off-inventory abilities

**Everything about a Feral ability is in `ability-inventory.md`** — 189 rows
(specID 103), one row each carrying spellID, cooldown, cast time, origin,
talent/hero placement and the full tooltip. It is generated, Tier-1, DB2-pinned
to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Feral ability is not named below, do not research it — read its row in
> `ability-inventory.md` and go.** Builder/spender priority, bleed snapshotting
> and Tiger's Fury windows → `rotation.md`. Talents/hero pick → `builds.md`. Both
> sections here are **closed lists, not backlogs.**

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

_None known for this spec._ Every button the old prose named — including the
Midnight-new ones (**Ravage** `441583`, **Chomp**, **Panther's Guile** `1280316`,
**Frantic Frenzy** / **Focused Frenzy** `1244544`, **Hunger for Battle**,
**Unseen Predator** `1263657`) — resolves to a real row in
`ability-inventory.tsv`. Feral has no override-only or pet-line button.

## §B — Encountered, and we believe not valid

| name | verdict | evidence |
|---|---|---|
| Brutal Slash | **removed from the kit** | Zero rows in `all-talents.tsv` for **any** of the 40 specs and zero in `all-abilities.tsv`; nothing of that name in Feral's 189 inventory rows. **Swipe** is the AoE builder. |
| Renewal | **removed from the class tree** | Same double miss — no `all-talents.tsv` or `all-abilities.tsv` row for any spec. The only surviving near-match is the unrelated passive **Aessina's Renewal** `474678` (class tree, row 7). Feral's personal healing is Frenzied Regeneration (Bear), Survival Instincts and Regrowth. |

*[Tier 1: DB2 @ 12.0.7.67808 via `all-talents.tsv` + `all-abilities.tsv`;
`_abilities/reconcile-ledger.md`.]*

## Corrections this file has already made

Kept only because re-asserting it is the likely failure mode:

- **`Thrash` `77758` was NOT removed from the Feral kit.** An earlier revision of
  this file asserted *"Brutal Slash and Thrash were removed from the Feral kit
  this patch (per method.gg 12.0.7)"* and carried an `@verify-ingame` on it.
  Tier-1 disagrees on the Thrash half: Feral learns it as **class-baseline** via
  `SkillLineAbility:798`, `castable=true`, cooldown **6s** — the same row
  Guardian has. Only the Brutal Slash half held up (§B). The claim came from a
  Tier-3 guide and never should have outranked the acquisition table. ⚠ Feral's
  `rotation.md` does not mention Thrash at all, so the AoE priority there may be
  missing a real button — see the escalation, not this file.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The Energy cost / cast
time is uncertain"* is **not** one: `ability-inventory.md` carries the Tier-1
numbers, and the resource-cost markers an earlier revision left behind were
guesses at values nobody needed to log in to check.
