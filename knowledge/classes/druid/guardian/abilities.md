---
title: Guardian Druid — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree @ 12.0.7.67808
  - ../../_abilities/all-abilities.tsv  # tier 1 — the 40-spec union, for absence checks
  - ../../_abilities/section-4-catalogue.tsv  # tier 1 derived — the trigger-effect reach-out rows
  - ../../_abilities/spell-descriptions.tsv  # tier 1 — resolved English tooltips via /data/wow/spell/{id}
  - ../../_abilities/reconcile-ledger.md  # tier 1 derived — the per-row verdicts applied to this file
confidence: high
---

# Guardian Druid — off-inventory abilities

**Everything about a Guardian ability is in `ability-inventory.md`** — 192 rows
(specID 104), one row each carrying spellID, cooldown, cast time, origin,
talent/hero placement and the full tooltip. It is generated, Tier-1, DB2-pinned
to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Guardian ability is not named below, do not research it — read its row
> in `ability-inventory.md` and go.** Rage economy, active-mitigation priority and
> Wild Guardian's window → `rotation.md`. Talents/hero pick → `builds.md`. Both
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

_None known for this spec._ Guardian's one genuinely mis-rendered button —
**Wild Guardian** — *does* have an inventory row, so it belongs under
Corrections below rather than here; filing it in §A would assert a `prose-only`
name that already carries an acquisition row.

## §B — Encountered, and we believe not valid

| name | verdict | evidence |
|---|---|---|
| Rage of the Sleeper | **removed for Guardian** | Zero rows in `all-talents.tsv` for **any** of the 40 specs, and zero in `all-abilities.tsv`; nothing of that name in Guardian's 192 inventory rows. The row-12 spec capstone active is now **Wild Guardian** (node `110431`, entry `137061`). Do not expect a Rage of the Sleeper button on the bar. |
| Renewal | **removed from the class tree** | Same double miss across all 40 specs. The only surviving near-match is the unrelated passive **Aessina's Renewal** `474678` (class tree, row 7). Guardian's personal healing is Frenzied Regeneration, Barkskin and Survival Instincts. |

*[Tier 1: DB2 @ 12.0.7.67808 via `all-talents.tsv` + `all-abilities.tsv`;
`_abilities/reconcile-ledger.md`.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **`Wild Guardian`'s generated `castable` flag is WRONG — the button is real.**
  `ability-inventory.tsv` computes `origin`/`castable` from the **trait entry's
  visible spell**, which for this node is `1269614` — a passive *enabler* aura.
  Its Tier-1 tooltip reads *"After you cast Berserk or Incarnation: Guardian of
  Ursoc, **you gain access to Wild Guardian**: … causing your next 2 casts of
  Ironfur, Maul, and Frenzied Regeneration to be echoed"* — i.e. `1269614` grants
  access to something else. That something else is a **distinct spell**: the
  reach-out in `../../_abilities/section-4-catalogue.tsv` anchors *Gift of
  Ironfur* `1269659`, *Gift of Maul* `1269660` and *Gift of Frenzied
  Regeneration* `1269661` on **`Wild Guardian` `1269658`**, and *Mastery:
  Nature's Guardian* `155783` on **`Wild Guardian` `1269617`** — neither of which
  has an inventory row of its own. So: **row present, `castable=false`, button
  real.** Do not "clean up" the keybind. `rotation.md` and `builds.md` both treat
  it as the pressed row-12 capstone, correctly.
- ⚠ **`node_type` in `all-talents.tsv` is not the check that proves this.** That
  column describes the *node*, not the granted spell. Four Druid nodes read
  `ACTIVE` while the inventory says passive — Wild Guardian `1269614`, Ascendant
  Eclipses `1261564`, Unseen Predator `1263657`, Everbloom `392167` — and only
  the first is a real button. The tooltip text is what separated them.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact Rage cost is
uncertain"* is **not** one, and neither is *"is Rage of the Sleeper still on the
bar?"* — an earlier revision carried an `@verify-ingame` for exactly that, and
two Tier-1 table lookups answered it.
