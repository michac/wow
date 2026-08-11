---
title: Mistweaver Monk — Abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - knowledge/classes/monk/mistweaver/ability-inventory.tsv  # tier 1, generated from DB2 @ build 12.0.7.67808 — name/spellID/origin/cooldown floor
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 adjudication of this file's claims @ 12.0.7.67808
  - https://www.method.gg/guides/mistweaver-monk/playstyle-and-rotation  # tier 3, upd. 2026-06-16
  - https://www.icy-veins.com/wow/mistweaver-monk-pve-healing-rotation-cooldowns-abilities  # tier 3, 12.0.7
  - https://www.icy-veins.com/wow/mistweaver-monk-pve-dps-guide  # tier 3, 12.0.7
  - raw/wago/SpellName.csv @ 12.0.7.67808  # tier 1, name reconciliation
confidence: medium
---

> ⚠ **NOT RE-VERIFIED FOR 12.1 (as of 2026-08-11).** This file still describes
> **Midnight Season 1 / patch 12.0.7** and its `patch:`/`reviewed:` stamps are
> deliberately left at that, because nobody checked its claims against 12.1.
> Patch **12.1 "Curse of Ula'tek"** went live 2026-08-11 and changed things that
> affect **every** spec:
>
> - **Player health and creature damage +25%** at max level, health consumables
>   rescaled, and some DPS/Tank healing + absorb spells retuned. Any absolute
>   HP / healing / consumable number below is now wrong.
> - **Major DPS cooldowns lowered and steady-state damage raised** for several
>   specs — so a spec's burst/sustained split may have moved.
> - **Interrupts** now show a "missed" visual + sound when the target was not casting.
> - **Diminishing-return categories reset after 20s** (was 16s).
> - A game-wide **PvP snare tier-down** (70%→50%, 50%→30%, …). PvP only.
>
> Per-spec 12.1 changes for this spec, if any, are in
> `knowledge/_meta/patch-notes/12.1.md` under the **CLASSES** section — read that
> before trusting anything here. The **regenerated** siblings in this directory
> (`talents.md`, `talents.json`, `ability-inventory.md`) *are* current: they were
> rebuilt on 2026-08-11 from live 12.1 game data and are Tier 1. Where this file
> and they disagree about whether a talent exists, **they win**.


# Mistweaver Monk — Abilities (Midnight S1)

## Overview

Mistweaver is Monk's healing spec. It heals through a **"Fistweaving"** loop:
it deals melee/ranged damage (Tiger Palm, Blackout Kick, Rising Sun Kick,
Spinning Crane Kick) and that damage is converted into raid healing by
**Ancient Teachings / Jadefire Teachings**, on top of a bed of HoTs
(**Renewing Mist**, **Enveloping Mist**) and the **Soothing Mist** channel.
The playstyle is "keep everything on cooldown" and pre-plan the big cooldowns
against known damage events.

**Resources:** **Mana** is the primary pool (all direct heals cost mana);
**Energy** fuels the martial abilities (Tiger Palm, Blackout Kick, Spinning
Crane Kick). Modern Mistweaver does **not** use Chi. **Mana Tea** stacks are a
secondary economy that discount mana spent while its channel is up.

**Hero trees (Midnight):**
- **Conduit of the Celestials** — the favoured tree for both Raid and M+.
  Adds **Celestial Conduit** (a channeled AoE heal/damage nuke), **Heart of
  the Jade Serpent** cooldown reduction, and **Unity Within**. Builds a ramping
  Renewing Mist / Rushing Wind Kick loop.
- **Master of Harmony** — alternative, more damage-leaning in M+. Routes
  healing/damage through **Aspect of Harmony**, banked and released; largely
  passive beyond activating Thunder Focus Tea.

> **Seed reconciliation:** the seed omitted **Vivify**, the core Mistweaver cast/instant
> heal — added below. **Rushing Wind Kick**, **Jade Empowerment**, **Spiritfont** and
> **Invoke Yu'lon, the Jade Serpent** are Midnight talent additions / choice-node partners
> not in the seed list. The PvP talents the seed listed here (**Nimble Brew**, **Double
> Barrel**, **Reverse Magic**) are **not Mistweaver's** — see the reconciliation notes at
> the foot of this file.

## Inventory

**`ability-inventory.tsv` in this directory is the Tier-1 floor** — canonical name, spellID,
origin and baseline cooldown are regenerated there from DB2 and are not duplicated here.
This file is the prose layer: role, rotational context, and when to press it.

A cooldown written **`10s [T1]`** was read off that tsv (DB2 @ build 12.0.7.67808) and is
the baseline before talents and Haste; a `~` value is guide-derived. `@verify-ingame` marks
what Tier 1 could not settle (costs, cast times, effect magnitudes, charge recharge).

> **What the Tier-1 floor does and does not cover.** A **bold `[T1]`** cooldown
> below was read straight out of `ability-inventory.tsv` (wago DB2 @ 12.0.7.67808).
> A `~` value was **not**: it is a Tier-3 guide number that the tsv could not
> settle, and it is kept on purpose. The tsv's `cooldown` column is
> `SpellCooldowns` at DifficultyID 0 — `max(RecoveryTime, CategoryRecoveryTime)` —
> which is the real cooldown for a normal button and is **wrong for a charge
> ability**, where it returns the GCD (Fire Blast 0.5s, Purifying Brew 1s). The
> recharge lives in `SpellCategory.ChargeRecoveryTime`, unreachable without
> breaking the build pin (`_abilities/reconcile-ledger.md` §5 G6). **So "the tsv
> wins" applies to the values it actually carries, not to every row** — 194 rows
> across the 40 files read 0 or sub-10s there and keep their `~` prose instead.
>
> Names this file asserts that **no** acquisition row reaches are catalogued in
> `../../_abilities/section-4-catalogue.md`; ones game data reaches indirectly are
> in `section-3-corroborated.md`. ⚠ Neither is a backlog — an entry there is
> researched when someone **asks**, never because it has sat there a while.

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| **Vivify** | Rotational-spender (heal) | Mana | 1.5s cast (instant w/ Vivacious Vivification proc) | Core heal — heals the target plus everyone with your Renewing Mist on them (cleave heal). Primary "spot heal." |
| **Renewing Mist** | Rotational-builder (HoT) | Mana | ~9s recharge, 2 charges | Bouncing HoT — keep on cooldown; jumps to a new injured ally each tick. Fuels Vivify's cleave and (via Rising Mist) is extended by RSK/Rushing Wind Kick. |
| **Enveloping Mist** | Rotational-spender (HoT) | Mana | ~2s cast (instant during Invoke Yu'lon/Chi-Ji or Thunder Focus Tea) | Strong single-target HoT; also amps healing the target receives. Instant + cheap while a Celestial is out. |
| **Soothing Mist** | Rotational-spender (channel) | Mana | Channel | Channeled single-target heal on a 1s GCD; lets you instant-cast your other single-target spells onto the target without breaking channel. Grants Elusive Mists damage reduction to the channeled ally. |
| **Rising Sun Kick** | Rotational-builder (damage→heal) | Energy | **10s** `[T1]` (Haste-reduced) | Core damage button; converted to healing by Ancient/Jadefire Teachings. TFT cuts its CD by 9s; Teachings of the Monastery gives a 15% reset chance off Blackout Kick. |
| **Rushing Wind Kick** | Rotational-builder (damage→heal) | Energy | 10s [T1] | Talent that *replaces* Rising Sun Kick (all RSK modifiers transfer). Extends Renewing/Enveloping Mist via Rising Mist; favoured in raid. |
| **Blackout Kick** | Rotational-builder (damage→heal) | Energy (free from RSK) | — | Filler strike; consumes Teachings of the Monastery stacks to hit extra times and can reset Rising Sun Kick. |
| **Tiger Palm** | Rotational-builder (damage→heal) | Energy | — | Cheapest filler; builds Teachings of the Monastery stacks (two stacks with Awakened Jadefire). |
| **Spinning Crane Kick** | Rotational-builder (AoE damage→heal) | Energy | — | AoE melee spender; primary damage-to-heal at 4+ targets. Empowered/free with Dance of Chi-Ji procs. |
| **Sheilun's Gift** | Rotational-spender (heal) | Mana | Instant | Charges "clouds" over time (up to 10); big burst heal scaling with clouds. Talent that can *replace* Vivify; favoured in M+. |
| **Thunder Focus Tea** | Utility (empower) | — | 30s CD, off-GCD | Empowers your next Renewing Mist (extends 10s), Rising Sun Kick (−9s CD), Enveloping Mist (instant), or Vivify. Triggers Secret Infusion (haste/vers) and Aspect of Harmony (MoH). |
| **Mana Tea** | Utility (resource) | — | Channel/off-GCD | Consumes stacks to reduce mana cost of spells; spend near ~20 stacks. Refreshment/Life Cocoon feed stacks. |
| **Invoke Yu'lon, the Jade Serpent** | Major cooldown (healing) | Mana | ~3 min CD / **120s** `[T1]` | Summons the Jade Serpent effigy: periodic raid healing + Chi Cocoon shields; reduces Enveloping Mist cast time. Raid-leaning Celestial. |
| **Invoke Chi-Ji, the Red Crane** | Major cooldown (healing) | Mana | ~3 min CD / **120s** `[T1]` | Choice-node Celestial: your damage procs Mastery heals on allies, makes Enveloping Mist instant + cheaper. M+/mana-efficient lean; grants 4 Teachings stacks on cast (Celestial Harmony). |
| **Celestial Conduit** | Major cooldown (heal/damage) | Mana | 90s [T1] | Conduit of the Celestials — channeled AoE heal + damage; movement-enabled; can be recast to end early (Unity Within). Grants CDR to Rushing Wind Kick / Renewing Mist. |
| **Revival** | Major cooldown (heal + dispel) | Mana | ~3 min CD | Instant raid-wide heal + raid-wide Magic/Disease/Poison dispel (40yd). Scaling falls off past 5 targets — valued for the mass dispel. |
| **Restoral** | Major cooldown (heal + dispel) | Mana | ~3 min CD | Choice-node alt to Revival; avoids accidental Magic dispels (won't strip helpful magic effects). @verify-ingame |
| **Life Cocoon** | Defensive (external) | Mana | ~2 min CD | Large single-target absorb shield (~12s) + boosts HoT healing on the target while up. No damage reduction — pure absorb. Tank/clutch save. |
| **Fortifying Brew** | Defensive (personal) | — | 360s [T1] (Expeditious Fortification reduces) | Personal −20% damage taken + max-HP bump. Primary Monk defensive. |
| **Diffuse Magic** | Defensive (personal) | — | ~90s CD | Reduces magic damage taken and can send debuffs back to caster. Talent. |
| **Touch of Death** | Rotational (execute damage) | — | 180s [T1] | Class-baseline, not a talent [T1]. Execute-style burst damage on low-HP targets; feeds the damage→heal conversion. |
| **Crackling Jade Lightning** | Utility (ranged damage) | Mana | Channel | Class-baseline, not a talent [T1]. Ranged filler channel; empowered by **Jade Empowerment** (talent) after Thunder Focus Tea / Jade Empowerment procs to hit harder and chain. |
| **Paralysis** | CC (incap) | Energy | 45s [T1] | Single-target incapacitate. |
| **Leg Sweep** | CC (stun) | — | 60s [T1] | AoE stun around the Monk. |
| **Ring of Peace** | CC (utility) | — | 45s [T1] | Knocks/keeps enemies out of a bordered zone. Choice node vs Song of Chi-Ji (root). |
| **Disable** | CC (slow/root) | Energy | — | Slows target; roots on repeat. |
| **Detox** | Dispel | Mana | Instant / **8s** `[T1]` | Removes Poison/Disease (and Magic for Mistweaver) from an ally. `Detox` 115450 `class-baseline` *[Tier 1]*. (This row was headed "Paralysis / Detox" — a compound-name seed artefact; Paralysis has its own row above.) |
| **Roll** | Movement | — | ~20s recharge, 2 charges | Short dash; Chi Torpedo choice-node variant rolls further + speed buff. |
| **Tiger's Lust** | Movement (external) | Energy | 30s [T1] | Grants an ally (or self) a sprint and clears roots/snares. |
| **Transcendence** | Movement/utility | — | Places a spirit copy / **10s** `[T1]` | Drops a stationary spirit; recastable to swap. |
| **Transcendence: Transfer** | Movement/utility | — | 45s [T1] | Instantly swap places with your Transcendence spirit — a key mobility/positioning tool. |
| **Zen Flight** | Movement (utility) | Mana | Channel, out of combat | Slow flight/levitate channel; travel utility. |
| **Summon Jade Serpent Statue** | Pet | Mana | **10s** `[T1]` | Statue that mirrors your Soothing Mist onto its target and can Provoke; choice node vs Jade Infusion. |
| **Provoke** | Utility (taunt) | — | 8s CD | Taunts a target (or directs the statue) — utility for controlling adds/statue. |
| **Resuscitate (Res)** | Utility (rez) | Mana | Out of combat | Out-of-combat resurrection. |
| **Expel Harm** | Defensive/self-heal | Energy | 15s [T1] | Class-baseline instant self-heal that also deals a bit of damage; personal sustain. |

## Reconciliation notes — Tier 1 @ 12.0.7.67808

Four rows this file carried belong to someone else and have been deleted:

- **Spear Hand Strike** is not on the Midnight Mistweaver tree. On the live Monk tree
  (**1000**) it sits on node 101152, gated **Brewmaster**, and node 110098, gated
  **Windwalker** — there is no Mistweaver node. Its only ungated node is on tree 781, the
  legacy copy. Mistweaver has no kick; plan interrupts around that.
- **Nimble Brew** and **Double Barrel** are `PvpTalent` rows for Monk / **Brewmaster** only.
- **Reverse Magic** is not a Monk ability at all — it is a **Demon Hunter** PvP talent
  (Havoc, Vengeance and Devourer).

Also corrected: **Touch of Death** and **Crackling Jade Lightning** are class-baseline, not
talents; **Rushing Wind Kick** is 10s, not ~12s; and Ring of Peace (45s), Transcendence:
Transfer (45s) and Fortifying Brew (360s) were carried at guide values that Tier 1 overrules.
