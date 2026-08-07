---
title: Arms Warrior — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ../../_abilities/reconcile-ledger.md  # tier 1 derived — the Warrior/arms TOOL-GAP verdict + §5 G2
  - ../../_abilities/section-4-catalogue.tsv  # tier 1 derived — the prose-only leg this file feeds
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree @ 12.0.7.67808
  - simc midnight branch profiles/MID1/MID1_Warrior_Arms.simc  # tier 1 APL — emits `heroic_strike`
confidence: high
---

# Arms Warrior — off-inventory abilities

**Everything about an Arms ability is in `ability-inventory.md`** — 159 rows, one
each carrying spellID, cooldown, cast time, origin, talent/hero placement and the
full tooltip. It is generated, Tier-1, DB2-pinned to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If an Arms ability is not named below, do not research it — read its row in
> `ability-inventory.md` and go.** Rotation → `rotation.md`. Talents/hero pick →
> `builds.md`. Both sections here are **closed lists, not backlogs.**

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

| spellID | name | how we know, and why the join misses it |
|---|---|---|
| `1269383` | Heroic Strike | **A runtime override of `Slam`, and this prose is its only record anywhere.** The apex spec talent **`Master of Warfare` `1269314`** produces it; that talent *is* in the inventory (`talent-passive`, `castable=false`, spec tree node 110407) and its Tier-1 tooltip reads: *"Your single target melee abilities have a chance to upgrade Slam to Heroic Strike. All modifiers and talents that affect Slam also affect Heroic Strike."* The upgraded button is never *learned* — it replaces `Slam` on the bar at runtime — so no `SpecializationSpells` / `SkillLineAbility` / `TraitNodeEntry` row can ever name it, and the join has nothing to emit. `1269383` is a Midnight-range `SpellName` ID with **no** acquisition row (`reconcile-ledger` → Warrior/arms: verdict **TOOL-GAP**, class **G2** "runtime override / proc-replacement buttons have no acquisition row"). ⚠ A `SpellName` hit alone is not evidence a spec can cast something — two independent Tier-1 corroborations are what settle it: (1) `Heroic Might` `1292058` (`cdm-only`, `CooldownSetSpell`) sits in this spec's own inventory and its tooltip *names the button* — "**Heroic Strike** increases the damage you deal to enemies affected by your next Colossus Smash…"; (2) the Tier-1 simc APL `MID1_Warrior_Arms.simc` emits **`heroic_strike`**, not `slam`, as the filler in that build. |

**This category is real and measured, not an edge case.** `reconcile-ledger` §5 G2
counts ~19 such buttons across the 40 specs — `Devour`, `Templar Slash`,
`Void Volley`, `Crushing Blow`, `Heroic Strike` — every one of them a pressed
button whose only record is a hand-written row like this one. Delete the row and
the ability leaves the KB.

## §B — Encountered, and we believe not valid

_None recorded for this spec._ The previous revision made no "not on the tree" /
"removed" / "renamed" claim, and every ability name it *did* assert resolves to a
row in the 159-row generated inventory — 52 names checked by exact match against
`ability-inventory.tsv` @ 12.0.7.67808, one miss, `Heroic Strike`, which is §A.

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **`Master of Warfare` is a passive proc, not a permanent transform.** This file
  and `builds.md` both said it *"transforms `Slam` into `Heroic Strike`"*. The
  Tier-1 tooltip says **"have a chance to upgrade Slam to Heroic Strike"** — a
  proc. `Slam` does not go away; the APL's `heroic_strike` line is what you press
  when the proc is up. Do not write "Slam is replaced" back in.
- **`all-talents.tsv` types the `Master of Warfare` node `ACTIVE`; it is not a
  button.** The inventory has it `talent-passive` / `castable=false` / cd 0, and
  the tooltip agrees. **`node_type` in the trait tables is not a castability
  signal** — the inventory's `origin`/`castable` columns are. (Same trap on
  `Rampaging Berserker` for Fury.)

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact cooldown / cost
is uncertain"* is **not** one: `ability-inventory.md` carries the Tier-1 number.
