---
title: Mistweaver Monk — Abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/mistweaver-monk/playstyle-and-rotation  # tier 3, upd. 2026-06-16
  - https://www.icy-veins.com/wow/mistweaver-monk-pve-healing-rotation-cooldowns-abilities  # tier 3, 12.0.7
  - https://www.icy-veins.com/wow/mistweaver-monk-pve-dps-guide  # tier 3, 12.0.7
  - raw/wago/SpellName.csv @ 12.0.7.67808  # tier 1, name reconciliation
confidence: medium
---

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

> **Seed reconciliation:** the seed omitted **Vivify** (spell 116670), the core
> Mistweaver cast/instant heal — added below. **Rushing Wind Kick** (467307),
> **Jade Empowerment** (467316), **Spiritfont** (1260511) and **Invoke Yu'lon,
> the Jade Serpent** (322118) are Midnight talent additions/choice-node
> partners not in the seed list. **Nimble Brew / Double Barrel / Reverse Magic**
> are PvP talents. All names verified against `SpellName.csv` @ 12.0.7.67808.

## Inventory

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| **Vivify** | Rotational-spender (heal) | Mana | 1.5s cast (instant w/ Vivacious Vivification proc) | Core heal — heals the target plus everyone with your Renewing Mist on them (cleave heal). Primary "spot heal." |
| **Renewing Mist** | Rotational-builder (HoT) | Mana | ~9s recharge, 2 charges | Bouncing HoT — keep on cooldown; jumps to a new injured ally each tick. Fuels Vivify's cleave and (via Rising Mist) is extended by RSK/Rushing Wind Kick. |
| **Enveloping Mist** | Rotational-spender (HoT) | Mana | ~2s cast (instant during Invoke Yu'lon/Chi-Ji or Thunder Focus Tea) | Strong single-target HoT; also amps healing the target receives. Instant + cheap while a Celestial is out. |
| **Soothing Mist** | Rotational-spender (channel) | Mana | Channel | Channeled single-target heal on a 1s GCD; lets you instant-cast your other single-target spells onto the target without breaking channel. Grants Elusive Mists damage reduction to the channeled ally. |
| **Rising Sun Kick** | Rotational-builder (damage→heal) | Energy | ~12s CD (Haste-reduced) | Core damage button; converted to healing by Ancient/Jadefire Teachings. TFT cuts its CD by 9s; Teachings of the Monastery gives a 15% reset chance off Blackout Kick. |
| **Rushing Wind Kick** | Rotational-builder (damage→heal) | Energy | ~12s CD | Talent that *replaces* Rising Sun Kick (all RSK modifiers transfer). Extends Renewing/Enveloping Mist via Rising Mist; favoured in raid. @verify-ingame |
| **Blackout Kick** | Rotational-builder (damage→heal) | Energy (free from RSK) | — | Filler strike; consumes Teachings of the Monastery stacks to hit extra times and can reset Rising Sun Kick. |
| **Tiger Palm** | Rotational-builder (damage→heal) | Energy | — | Cheapest filler; builds Teachings of the Monastery stacks (two stacks with Awakened Jadefire). |
| **Spinning Crane Kick** | Rotational-builder (AoE damage→heal) | Energy | — | AoE melee spender; primary damage-to-heal at 4+ targets. Empowered/free with Dance of Chi-Ji procs. |
| **Sheilun's Gift** | Rotational-spender (heal) | Mana | Instant | Charges "clouds" over time (up to 10); big burst heal scaling with clouds. Talent that can *replace* Vivify; favoured in M+. |
| **Thunder Focus Tea** | Utility (empower) | — | 30s CD, off-GCD | Empowers your next Renewing Mist (extends 10s), Rising Sun Kick (−9s CD), Enveloping Mist (instant), or Vivify. Triggers Secret Infusion (haste/vers) and Aspect of Harmony (MoH). |
| **Mana Tea** | Utility (resource) | — | Channel/off-GCD | Consumes stacks to reduce mana cost of spells; spend near ~20 stacks. Refreshment/Life Cocoon feed stacks. |
| **Invoke Yu'lon, the Jade Serpent** | Major cooldown (healing) | Mana | ~3 min CD, 25s | Summons the Jade Serpent effigy: periodic raid healing + Chi Cocoon shields; reduces Enveloping Mist cast time. Raid-leaning Celestial. |
| **Invoke Chi-Ji, the Red Crane** | Major cooldown (healing) | Mana | ~3 min CD, 25s | Choice-node Celestial: your damage procs Mastery heals on allies, makes Enveloping Mist instant + cheaper. M+/mana-efficient lean; grants 4 Teachings stacks on cast (Celestial Harmony). |
| **Celestial Conduit** | Major cooldown (heal/damage) | Mana | ~90s CD | Conduit of the Celestials — channeled AoE heal + damage; movement-enabled; can be recast to end early (Unity Within). Grants CDR to Rushing Wind Kick / Renewing Mist. |
| **Revival** | Major cooldown (heal + dispel) | Mana | ~3 min CD | Instant raid-wide heal + raid-wide Magic/Disease/Poison dispel (40yd). Scaling falls off past 5 targets — valued for the mass dispel. |
| **Restoral** | Major cooldown (heal + dispel) | Mana | ~3 min CD | Choice-node alt to Revival; avoids accidental Magic dispels (won't strip helpful magic effects). @verify-ingame |
| **Life Cocoon** | Defensive (external) | Mana | ~2 min CD | Large single-target absorb shield (~12s) + boosts HoT healing on the target while up. No damage reduction — pure absorb. Tank/clutch save. |
| **Fortifying Brew** | Defensive (personal) | — | 2 min CD (1.5 min w/ Expeditious Fortification) | Personal −20% damage taken + max-HP bump. Primary Monk defensive. |
| **Diffuse Magic** | Defensive (personal) | — | ~90s CD | Reduces magic damage taken and can send debuffs back to caster. Talent. |
| **Touch of Death** | Rotational (execute damage) | — | ~2 min CD (talent-reduced) | Execute-style burst damage on low-HP targets; feeds the damage→heal conversion. |
| **Crackling Jade Lightning** | Utility (ranged damage) | Mana | Channel | Ranged filler channel; empowered by **Jade Empowerment** (talent) after Thunder Focus Tea / Jade Empowerment procs to hit harder and chain. |
| **Spear Hand Strike** | Interrupt | Energy | 15s CD | Melee interrupt (kick). |
| **Paralysis** | CC (incap) | Energy | ~45s CD | Single-target incapacitate. |
| **Leg Sweep** | CC (stun) | — | ~60s CD | AoE stun around the Monk. |
| **Ring of Peace** | CC (utility) | — | ~30s CD | Knocks/keeps enemies out of a bordered zone. Choice node vs Song of Chi-Ji (root). |
| **Disable** | CC (slow/root) | Energy | — | Slows target; roots on repeat. |
| **Paralysis / Detox — dispel** | Dispel | Mana | 8s CD | **Detox** removes Poison/Disease (and Magic for Mistweaver) from an ally. |
| **Roll** | Movement | — | ~20s recharge, 2 charges | Short dash; Chi Torpedo choice-node variant rolls further + speed buff. |
| **Tiger's Lust** | Movement (external) | Energy | ~30s CD | Grants an ally (or self) a sprint and clears roots/snares. |
| **Transcendence** | Movement/utility | — | Places a spirit copy | Drops a stationary spirit; recastable to swap. |
| **Transcendence: Transfer** | Movement/utility | — | ~10–25s CD | Instantly swap places with your Transcendence spirit — a key mobility/positioning tool. |
| **Zen Flight** | Movement (utility) | Mana | Channel, out of combat | Slow flight/levitate channel; travel utility. |
| **Summon Jade Serpent Statue** | Pet | Mana | — | Statue that mirrors your Soothing Mist onto its target and can Provoke; choice node vs Jade Infusion. |
| **Provoke** | Utility (taunt) | — | 8s CD | Taunts a target (or directs the statue) — utility for controlling adds/statue. |
| **Resuscitate (Res)** | Utility (rez) | Mana | Out of combat | Out-of-combat resurrection. |
| **Crackling Jade / Expel Harm** | Defensive/self-heal | Energy | ~15s CD | **Expel Harm** — instant self-heal that also deals a bit of damage; personal sustain. @verify-ingame |
| **Nimble Brew** | Utility (PvP) | — | PvP talent | Removes stun/root/fear/horror/incapacitate effects. PvP talent. |
| **Double Barrel** | Utility (PvP) | — | PvP talent | PvP talent (burst/utility). @verify-ingame |
| **Reverse Magic** | Dispel (PvP) | — | PvP talent | Removes all magical effects from party/raid and sends harmful ones back to enemies. PvP talent. |
