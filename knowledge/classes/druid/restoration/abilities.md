---
title: Restoration Druid — off-inventory abilities (Midnight S1)
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

# Restoration Druid — off-inventory abilities

**Everything about a Restoration ability is in `ability-inventory.md`** — 192
rows (specID 105), one row each carrying spellID, cooldown, cast time, origin,
talent/hero placement and the full tooltip. It is generated, Tier-1, DB2-pinned
to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Restoration ability is not named below, do not research it — read its
> row in `ability-inventory.md` and go.** Ramp order, Swiftmend cadence and the
> Rejuv bed → `rotation.md`. Talents/hero pick → `builds.md`. Both sections here
> are **closed lists, not backlogs.**

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

_None known for this spec._ Every button the old prose named resolves to a real
row in `ability-inventory.tsv` — including the two the old "name reconciliation"
section flagged as uncertain (**Efflorescence** `145205`, `talent-active`, and
**Cenarion Ward** `102352`, class-baseline). Restoration has no override-only or
pet-line button; the Grove Guardians are summoned, not cast.

## §B — Encountered, and we believe not valid

| name | verdict | evidence |
|---|---|---|
| Nourish | **not a player button** | Zero rows in `all-talents.tsv` for **any** of the 40 specs, zero in `all-abilities.tsv`, none of Restoration's 192 inventory rows. ⚠ The name **does** still appear in game text — **Grove Guardians** `1226140` reads *"summons a Treant that casts **Nourish** on that target or a nearby ally periodically"* — which is why guides and notes keep surfacing it. It is the treant's spell, not yours. There is no slow-efficient filler heal to fall back on when mana-starved; that role is Regrowth under *Abundance* / *Clearcasting*. |
| Adaptive Swarm | **removed** | Zero rows in `all-talents.tsv` and zero in `all-abilities.tsv` across all 40 specs — no trait node, no SkillLineAbility, no PvP talent, and no trace in any spell tooltip. |
| Renewal | **removed from the class tree** | Same double miss across all 40 specs. The only surviving near-match is the unrelated passive **Aessina's Renewal** `474678` (class tree, row 7). |

*[Tier 1: DB2 @ 12.0.7.67808 via `all-talents.tsv` + `all-abilities.tsv`;
`_abilities/reconcile-ledger.md`.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **`Flourish` `197721` is a PASSIVE in Midnight, not a ~90s pressed cooldown.**
  Tier-1 tooltip: *"Tranquility extends the duration of all of your heal over
  time effects by 2 sec every 0.9 sec."* It is `talent-passive`,
  `castable=false`, cd 0 — a modifier on Tranquility, with no button and no
  cooldown of its own. An earlier revision listed it as *"Instant / ~90s"* with
  an `@verify-ingame`, which is the pre-Midnight Flourish and would have put a
  dead keybind on the bar.
- **`Cenarion Ward` `102352` IS available — the old "not in the 12.0.7 resto
  tree" line was misleading.** True as written (it is not a *talent node* — zero
  `all-talents.tsv` rows), but it is learned as **class-baseline** via
  `SkillLineAbility:798`, `castable=true`, by **all four** Druid specs. It is a
  real button; do not tell anyone it was removed. This is the general trap: *not
  on the tree* ≠ *not acquirable*, and only an acquisition table settles it.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"Is Swiftmend's cooldown
~15s? Is Ironbark's ~90s?"* are **not** such questions — `ability-inventory.md`
carries the Tier-1 numbers, and the markers an earlier revision left on them were
guesses, not observations.
