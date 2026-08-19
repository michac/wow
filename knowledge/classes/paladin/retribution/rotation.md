---
title: Retribution Paladin — Rotation
patch: 12.1
fetched: 2026-08-17
reviewed: 2026-08-17
augments: simc-apl.md @91e711b
sources:
  - knowledge/classes/paladin/retribution/simc-apl.md  # tier 1, the generated 12.1 priority list, commit 91e711b (2026-08-11)
  - knowledge/classes/paladin/retribution/ability-inventory.tsv  # tier 1, DB2 @ 12.1.0.69214 — tree/hero placement, node+entry, spell ids
confidence: high
---

# Retribution Paladin — Rotation

**The priority list is [`simc-apl.md`](simc-apl.md) in this folder.** Tier 1, generated
from SimulationCraft's `apl_paladin.cpp` by `wowkb.simc --kb`, pinned to commit
`91e711b` (2026-08-11). **This file does not restate it** — it explains why the rungs
sit where they do, and names what the sim does not model.

> ⚠ **The sim has perfect information and no legs.** It models neither movement nor
> mechanics and its dummy never leaves melee range. Read a line absent from the APL as
> *"no longer worth a global cooldown as damage"*, never as *"useless"*.

## The list is four lists, and rung numbers only mean something inside one

`actions.default` is four lines and carries almost no ordering: `auto_attack`,
`rebuke`, then `call_action_list,name=cooldowns` and `call_action_list,name=generators`.
Everything real happens in the three lists it calls, and **`generators` calls
`finishers` twice** — once conditionally at its first line, once unconditionally at its
sixth. Quote a rung number only with the list it counts within.

- **`cooldowns` (11 lines) yields two presses**: `execution_sentence` and
  `avenging_wrath`. The other nine are four `use_item` lines, a potion,
  `invoke_external_buff` and **two** racials (`lights_judgment`, `fireblood`). ⚠ The third
  racial, `arcane_torrent`, is **not** in this list — it is `generators` rung 14, the very
  bottom of the priority.
- **`precombat` (7 lines) yields none** — `snapshot_stats`, five `variable` lines and one
  `use_item`.
- **`finishers` (4 lines)**: the `ds_castable` variable, then `hammer_of_light` >
  `divine_storm` > `templars_verdict`.
- **`generators` (14 lines)** is the body. 12 of them are presses; the other two are the
  `call_action_list,name=finishers` rungs (1 and 6).

Flattened for a **Templar** build, the priority reads:

1. `execution_sentence`
2. `avenging_wrath`
3. **finishers**, but only at `holy_power=5` with Wake of Ashes on cooldown (or a free
   Hammer of Light about to expire)
4. `blade_of_justice` — opener only (`time<5`, Holy Flames, Expurgation not yet ticking)
5. `wake_of_ashes`
6. `divine_toll`
7. `blade_of_justice` on an Art of War / Righteous Cause proc
8. **finishers**, unconditionally
9. `blade_of_justice`
10. `hammer_of_wrath`
11. `judgment`
12. `templar_strike` → `templar_slash` → `crusader_strike`

## Why each rung sits there

**The finishers are called twice because Holy Power caps at 5.** The unconditional call
at generators line 6 is the ordinary "spend when you can afford it" rung — simc will not
cast a spender it cannot pay for, so no Holy Power term appears on the finisher lines
themselves. The *first* call exists only to jump the finishers above Wake of Ashes,
Divine Toll and the proc'd Blade of Justice **when you are sitting at 5 and would waste
the next builder's generation**. Its condition is
`holy_power=5&cooldown.wake_of_ashes.remains|buff.hammer_of_light_free.remains<gcd*2`,
and the `cooldown.wake_of_ashes.remains` half is the interesting one: **at 5 Holy Power
with Wake of Ashes *ready*, the list still presses Wake of Ashes**, because what Wake of
Ashes is worth is the Hammer of Light window, not the Holy Power it generates. Wake of
Ashes is the one builder you are allowed to overcap into.

**Hammer of Light replaces Wake of Ashes, not your spender.** Light's Guidance 427445 —
*"Wake of Ashes is replaced with Hammer of Light for 20 sec after it is cast"*
*[T1: resolved spell description @ 12.1.0.69214]*. So the top finisher and the window
opener are the **same button** at different moments, and `hammer_of_light` outranking
`divine_storm` and `templars_verdict` inside `finishers` is not a choice you make — it
is what that button *is* while the window is open.

**Both spender lines carry the same guard,
`(!buff.hammer_of_light_ready.up|buff.hammer_of_light_free.up)`** — do not spend Holy
Power on an ordinary finisher while a Hammer of Light is owed, unless the owed one is
the *free* Light's Deliverance cast, which costs nothing and therefore does not compete.

**`ds_castable` is the whole of the AoE decision.**
`(active_enemies>=3-(talent.tempest_of_the_lightbringer&!talent.jurisdiction)|buff.empyrean_power.up)&!buff.empyrean_legacy.up`.
Three independent clauses:
- the target threshold, **3** normally and **2** with Tempest of the Lightbringer taken
  and Jurisdiction dropped;
- an **Empyrean Power** proc makes Divine Storm free, so it beats the single-target
  spender at *any* target count (Empyrean Power 326732: *"Crusader Strike has a 15%
  chance to make your next Divine Storm free and deal 15% additional damage"*);
- an **Empyrean Legacy** proc suppresses Divine Storm entirely, because that proc is
  spent on the single-target spender.

**Execution Sentence is placed, not pressed on cooldown.** Its line is
`(cooldown.avenging_wrath.remains>15|talent.radiant_glory)&(target.time_to_die>10)&cooldown.wake_of_ashes.remains<gcd&(!talent.holy_flames|dot.expurgation.ticking)`.
Two real holds: keep it off the bar while Avenging Wrath is within ~15s (so its own 60s
cooldown comes back *inside* the wings rather than being burned just before them), and
do not cast it until Wake of Ashes is essentially ready, so the detonation lands with
the Templar window. Radiant Glory removes the first hold, because it removes Avenging
Wrath as a button at all.

**Wake of Ashes waits on the two cooldowns it wants to overlap.**
`(cooldown.avenging_wrath.remains>6|talent.radiant_glory)&(!talent.execution_sentence|cooldown.execution_sentence.remains>4|target.time_to_die<10)`
— hold it while Avenging Wrath is ≤6s out, and while Execution Sentence is ≤4s out or
ready.

**Divine Toll waits on Avenging Wrath the same way** (`cooldown.avenging_wrath.remains>15`),
and for the same reason: it is a large Holy Power injection plus, with Divine Hammer, the
seed of Templar's area damage, so it belongs inside the window rather than just before it.

**Blade of Justice has rungs on both sides of the finishers.** `generators` rung 5
(`(buff.art_of_war.up|buff.righteous_cause.up)`) puts a proc'd, free Blade of Justice
**above** spending; rung 8 puts the ordinary one **below** it (flattened item 9). Nothing else in the list does this, and it is the only place where the
right press changes with a buff rather than with a resource level.

**Hammer of Wrath needs no execute condition in the list because the button does not
exist outside its window.** It sits at `generators` rung 9, directly above Judgment
(rung 10), and both are
ranged builders; which one you have is decided by the target's health and by Avenging
Wrath, not by the priority.

**The filler tail is build-dependent and mostly not a button.** Templar Strikes turns
Crusader Strike into the Templar Strike → Templar Slash combo (*"Crusader Strike loses a
charge but is now a combo ability"*), so `generators` rungs 11–13 are one button in three
states.
**Crusading Strikes deletes the button entirely** — *"Crusader Strike replaces your
auto-attacks"* — and on that build the priority simply ends at Judgment.

## What is talent-dependent

The APL branches on `radiant_glory`, `holy_flames`, `walk_into_light`,
`execution_sentence`, `tempest_of_the_lightbringer` and `jurisdiction`.

⚠ **`walk_into_light` is a Herald of the Sun hero talent** (node 95094, entry 117691,
spell 1263782 — `ability-inventory.tsv` @ 12.1.0.69214), so on **Templar** both lines
that name it collapse:

- `hammer_of_wrath,if=talent.walk_into_light` (`generators` rung 7) **never fires**, and
  Hammer of Wrath falls to its unconditional rung 9 — *below* Blade of Justice's rung 8.
  That dead rung is also why the flattened Templar list above runs one short of the
  `generators` numbering from item 9 onward: it drops rung 7 entirely.
- `blade_of_justice,if=(buff.art_of_war.up|buff.righteous_cause.up)&(!talent.walk_into_light|!buff.avenging_wrath.up)`
  simplifies to `(buff.art_of_war.up|buff.righteous_cause.up)`.

**So the APL is written for both hero trees, not for Templar alone.** Any argument for
Templar has to come from a build source, not from the shape of this list — see
`builds.md`.

`holy_flames` gates on `dot.expurgation.ticking`, a **target** DoT, in four places
(Execution Sentence, Avenging Wrath, the potion, the external buff) plus the opener Blade
of Justice.

## What the list does not tell you

- **Rebuke** is line 2 of `actions.default` and has no condition, because simc has no
  model of an interruptible cast. It is not part of the damage priority.
- The trinket block, `potion`, `invoke_external_buff,name=power_infusion` and the three
  racials (`lights_judgment`, `fireblood`, `arcane_torrent`) are not spec presses.
- `raid_event.adds`, `fight_remains` and `target.time_to_die` are simulation state.

## Changelog

**2026-08-17** — written. The file had been deliberately emptied on 2026-08-17 (its
contents described 12.0.7); this is the supplement it was left open for, authored
against `simc-apl.md` @ `91e711b`. Two things it establishes that were not previously
written down: **Hammer of Light replaces Wake of Ashes** (Light's Guidance 427445),
not the Holy Power spender; and **`walk_into_light` is Herald of the Sun**, so two APL
lines are dead on a Templar build.
