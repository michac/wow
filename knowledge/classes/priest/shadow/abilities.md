---
title: Shadow Priest — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree @ 12.0.7.67808
  - ../../_abilities/reconcile-ledger.md  # tier 1 adjudication of this file's earlier claims @ 12.0.7.67808
confidence: high
---

# Shadow Priest — off-inventory abilities

**Everything about a Shadow ability is in `ability-inventory.md`** — 170 rows, one
row each carrying spellID, cooldown, cast time, origin, talent/hero placement and
the full tooltip. It is generated, Tier-1, DB2-pinned to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Shadow ability is not named below, do not research it — read its row
> in `ability-inventory.md` and go.** Rotation → `rotation.md`. Talents/hero pick
> → `builds.md`. Both sections here are **closed lists, not backlogs.**

## §A — Real buttons the inventory cannot see

Confirmed to exist and be pressable, but no spec-keyed acquisition table names
them, so they will never appear in `ability-inventory.tsv`. **Absence there is not
absence in game.** Shadow carries **two**, and both are replacement buttons — a
button that replaces another is never *learned*, which is exactly why the join
misses it.

> ⚠ **This section is a machine input.** `wowkb.gen_abilities` harvests the `name`
> column of the table below — the heading is matched on the word **`inventory`** —
> and feeds it to the `prose-only` leg of `section-4-catalogue.md`. Rename this
> heading or drop the `name` column header and these rows **silently vanish from
> the catalogue**, with no marker and no warning. §B is deliberately *not*
> harvested: it asserts the opposite.

| spellID | name | how we know, and why the join misses it |
|---|---|---|
| — | Void Volley | **A Voidform-window override of the Voidform button itself.** `Voidform` `228260` (`talent-active`, 120s) carries it whole in its Tier-1 tooltip: *"This spell is replaced with **Void Volley** while Voidform is active.\n\n Void Volley\nReleases a volley of pure void energy, firing 10 bolts at your target and 1 bolt at all enemies within 10 yards of your target for 402 Shadow damage.\n\nGenerates 10 Insanity."* Three more inventory rows name it independently: `Crushing Void` `1279354` (*"+15% damage… when Voidform ends, you can cast Void Volley 1 additional time within 30 sec"*), Archon's `Focused Outburst` `1272320` (*"+15% damage and its cooldown is reduced by 4 sec"* — so it **has** its own cooldown) and `Insidious Ire` `373212`. Eight Midnight-range IDs (`1230903`…`1269563`) exist in `SpellName`@67808 with **no acquisition row of any kind**. |
| — | Mind Flay: Insanity | **An Archon proc-replacement of Mind Flay.** Both parents are live and in the inventory — `Surge of Insanity` `391399` (`talent-passive`, spec tree 795) and `Mind Flay` `15407` (`class-baseline`, `SpecializationSpells` → Shadow) — but the replacement buttons `391401`/`391403` attach to nothing. Corroborated by name in `Energy Cycle` `453828`: *"Casting **Mind Flay: Insanity** has a 100% chance to conjure Shadowy Apparitions."* |

**This category is real and measured, not an edge case.** Across all 40 specs,
runtime override / proc-replacement buttons live in no spec-keyed DB2 table:
`Devour`, `Pierce the Veil`, `Templar Slash`, `Void Volley` and `Heroic Strike`
are all real pressed buttons whose *only* record anywhere is a hand-written row
like these two. **`Void Volley` is one of the highest-value rows in the whole KB —
if this table is lost, nothing anywhere records that the button exists.**

## §B — Encountered, and we believe not valid

Names that appear in guides, older builds or other people's notes, which we have
checked and believe are **not** part of this spec at 12.0.7. Listed so the next
reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| Void Bolt | **gone — replaced by Void Volley** | zero hits in `ability-inventory.tsv`, zero in `all-talents.tsv` for **any** spec, zero across all Priest tooltips. Voidweaver (subtree 18) is live but carries `Void Blast` / `Entropic Rift`. The button that fills Void Bolt's old Voidform slot is `Void Volley` (§A). |
| Void Eruption | **gone — Voidform is now cast directly** | its only surviving trace is one **PvP-talent** tooltip, `Cascading Horrors` `357711`, which is itself stale text. `Voidform` `228260` is `talent-active` with a 120s cooldown and a 1.5s cast — there is no Eruption in front of it. |
| Devouring Plague | **renamed → Shadow Word: Madness** | no row and no tooltip mention anywhere in Priest data; `Shadow Word: Madness` `335467` (`talent-active`) occupies the spender slot and appears in 14 rows. Same role, new name. |
| Shadow Crash | **renamed/reworked → Tentacle Slam** | no row, no tooltip mention; `Tentacle Slam` `1227280` (`talent-active`) is the AoE DoT-applicator / Vampiric Touch spreader in its place. |
| Shackle Undead | **renamed → Shackle Horror** | no row, no tooltip mention; `Shackle Horror` `9484` (`talent-active`, 1.5s cast) is the live spell and appears on 3 talent nodes. |
| Void Apparitions | **a passive, not a button** | Tier 1 has **no castable spell of this name at any ID** — every one carries the passive attribute (`SpellMisc.Attributes_0 & 0x40`). It rides along with the Tentacle Slam / DoT package; there is nothing to press or bind. |

*[Tier 1: `all-talents.tsv` + `ability-inventory.tsv` @ 12.0.7.67808; adjudicated
in `../../_abilities/reconcile-ledger.md`.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **Void Volley is *not* a free-standing short-cooldown Insanity generator.** An
  earlier revision of this file described it as one you press on cooldown all
  pull. Tier-1 says it is the **Voidform button's replacement while Voidform is
  up**, plus one extra cast in the 30s after Voidform ends *if* `Crushing Void` is
  talented. That is a much narrower window than the old prose implied.
  ⚠ **`rotation.md` still carries the old framing** — it ranks Void Volley third
  in the single-target priority with *"don't lose charges"*, as if it were always
  available. `rotation.md` has **not** been edited; this file is the Tier-1 read.

## Open in-game questions

- Void Volley — its **cooldown and charge count**. `Focused Outburst` proves it has a cooldown ("reduced by 4 sec") but no Tier-1 table carries the base value, because the button has no acquisition row and therefore no reachable `SpellCooldowns` entry. Read cooldown + charges off the spellbook while Voidform is active; this is what settles whether `rotation.md`'s "don't lose charges" framing is salvageable. @verify-ingame

Nothing else. *"The exact cooldown / cost is uncertain"* is **not** an in-game
question when the spell has an inventory row — `ability-inventory.md` carries the
Tier-1 number.
