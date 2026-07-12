---
title: Hunter Survival — ability inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight branch profiles/MID1/MID1_Hunter_Survival.simc + engine/class_modules/apl/hunter/sv.txt  # tier 1 APL, commit 9cedf7c 2026-07-12, WoW 12.0.7
  - https://www.method.gg/guides/survival-hunter  # tier 3, Midnight 12.0.7 (upd. 2026-06-17)
  - https://www.method.gg/guides/survival-hunter/talents  # tier 3, 12.0.7
  - https://hackmd.io/@Azortharion/MidnightHunterChanges  # tier 3, Midnight SV redesign notes
  - https://raw/wago/SpellName.csv  # tier 1 game-data name reconcile (12.0.7.67808)
confidence: medium
---

# Hunter Survival — abilities (Midnight S1)

## Overview

Survival is the Hunter's **melee** spec: a pet class that fights in melee with a
spear/polearm (2H) or, new in Midnight, **dual-wielded one-handers (daggers)**.
Resource is **Focus** (0–100, passive regen boosted by auto-attacks — much more
so while dual-wielding, especially with the Pack Leader talent *Lethal Barbs*).
Kill Command is the builder and also grants **Tip of the Spear**, the spec's
signature buff (up to 2 stacks) that empowers the next ability cast — nearly the
whole kit wants to be "tipped." Raptor Strike is the primary spender and stacks
**Mongoose Fury** for a self-amplifying melee-window.

Two hero trees split the playstyle: **Pack Leader** (recommended for all PvE;
dual-wield, summons beasts via *Howl of the Pack Leader*) and **Sentinel**
(2H, defensive-leaning, adds the *Moonlight Chakram* button and *Sentinel's
Mark*). The Midnight redesign folded the old *Coordinated Assault* + *Flanking
Strike* into **Takedown**, turned *Fury of the Eagle* into **Boomstick**, and
added **Flamefang Pitch** as a ground-targeted fire cooldown.

> Focus costs / cooldowns below are cross-checked against the Tier-1 simc APL
> for rotational ordering; exact numbers on baseline utility come from
> long-stable Hunter values and Tier-3 guides — entries flagged @verify-ingame
> should be confirmed against live tooltips.

## Inventory

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Kill Command | Rotational-builder | Generates Focus + Tip of the Spear | Instant / charges (Howl-gated) | Pet lunges at the target for physical damage; grants **Tip of the Spear** (up to 2 stacks) and Focus. The core builder — recast whenever below 2 Tip stacks. @verify-ingame (exact Focus gen / charge count) |
| Raptor Strike | Rotational-spender | ~35–40 Focus | Instant / — | Primary melee strike and Focus dump; stacks **Mongoose Fury** (+10% Raptor Strike damage, 8s). Wants a Tip of the Spear stack. |
| Raptor Swipe | Rotational-spender (AoE) | ~35–40 Focus | Instant / — | Apex talent that converts/augments Raptor Strike into a cleave hitting up to 5 targets; the main multi-target spender. |
| Wildfire Bomb | Rotational-builder (bomb) | No Focus cost | Instant / ~18s recharge, 2 charges | Throws a fire bomb dealing AoE + a burning DoT; recharge is reduced by targets hit. Amplifies your fire damage. Choice of bomb type (Shrapnel / Flamebreak) via talent. |
| Takedown | Major cooldown | Generates 50 Focus | Instant / 90s (60s w/ Savagery) | Charges to the target, deals heavy up-front damage, gives 50 Focus, and **increases your and your pet's damage by 20% for 8s** — the spec's primary burst window (fold *Flanked* in for an AoE hit + attack-speed). Replaces Coordinated Assault + Flanking Strike. |
| Boomstick | Major cooldown | — | Instant / 60s | Shotgun-style blast; single-target damage bonus (~40%, reduced per extra target). Redesign of Fury of the Eagle. Used inside the Tip of the Spear / Takedown window. |
| Flamefang Pitch | Major cooldown (AoE) | — | Instant / ~60s (extra charge via talent) | Ground-targeted firebomb: damages enemies in the reticle and leaves a burning patch; feeds Wildfire Imbuement. Strong AoE cooldown. @verify-ingame (base CD 30 vs 60s) |
| Aspect of the Eagle | Utility (ranged enabler) | — | Instant / ~90s | Lets Survival use its melee abilities at range for the duration — the simc APL fires it when the target is ≥6 yds away, the melee-downtime / forced-ranged tool. @verify-ingame (duration / CD) |
| Mongoose Fury | Passive | — | — | Raptor Strike increases its own damage by 10% per stack for 8s — the self-amplifying melee window. "Essentially baseline" in the S1 build. |
| Tip of the Spear | Passive (mechanic) | — | — | Buff granted by Kill Command (up to 2 stacks) that empowers the next damaging ability; the spec's throughput engine. Nearly every button checks for it. |
| Hatchet Toss | Utility / ranged filler | Low Focus | Instant / — | Baseline thrown ranged attack; used at range and to spend Hogstrider stacks (Pack Leader). |
| Harpoon | Movement (gap closer) | — | Instant / 20s (2 charges w/ talent) | Grapples to a target, closing distance and rooting/slowing briefly — the melee engage tool. @verify-ingame |
| Hunter's Mark | Utility (debuff) | — | Instant / — | Marks the target, increasing damage it takes from you; persists until the target dies or is re-marked. |
| Misdirection | Utility (threat) | — | Instant / 30s | Redirects your (and pet's) threat to a friendly target or pet for a few seconds. |
| Intimidation | CC (stun) | — | Instant / 1min | Commands the pet to stun the target for a few seconds. |
| Binding Shot | CC (AoE) | — | Instant / 45s | Ground tether; enemies that move too far from it are stunned. @verify-ingame |
| Tar Trap | CC / Utility (slow) | — | Instant / 30s | Places a trap that coats the ground, heavily slowing enemies in it. Choice node vs Scare Beast. |
| Freezing Trap | CC (incap) | — | Instant / 30s | Trap that freezes the first enemy to enter in ice, incapacitating for up to ~1min (breaks on damage). |
| Flare | Utility (detect) | — | Instant / 20s | Reveals stealthed/invisible units and removes some ground effects in an area. @verify-ingame |
| Concussive Shot | CC (slow) | Low Focus | Instant / 5s | Ranged shot that slows the target's movement. |
| Tranquilizing Shot | Dispel | Low Focus | Instant / 10s | Removes one Enrage and one Magic effect from the target. |
| Muzzle | Interrupt | — | Instant / 15s (melee range) | Melee interrupt; locks the target's interrupted school briefly. The spec's kick. |
| Chimaeral Sting | CC / Utility | Low Focus | Instant / — | Disorienting sting (deals nature damage over time, breaks on significant damage). @verify-ingame |
| Camouflage | Utility (stealth) | — | Instant / — | Blends you (and nearby pet) into surroundings, breaking combat/aggro when out of combat; also a passive heal while active. |
| Aspect of the Cheetah | Movement | — | Instant / 3min | Large burst of movement speed for a few seconds, then a smaller sustained bonus. |
| Feign Death | Utility (threat drop) | — | Instant / 30s | Drops combat/aggro by faking death; core threat-shed and mechanic tool. |
| Survival of the Fittest | Defensive | — | Instant / ~3min | Reduces damage taken by you and your pet (~30%) for a short duration. |
| Exhilaration | Defensive (self-heal) | — | Instant / 2min | Instantly heals you and your pet for a percentage of max health. |
| Aspect of the Turtle | Defensive (immunity) | — | Instant / 3min | Immune to most attacks and prevents you from attacking for the duration — the panic button. |
| Roar of Sacrifice | Defensive (external) | — | Instant / — | Pet ability: protects a friendly target, redirecting a portion of damage/crit to you. Choice vs Guardian's Hide. |
| Call Pet | Pet | — | Instant / — | Summons one of your stabled pets (slots 1–5). |
| Revive Pet | Pet | — | Cast / — | Resurrects a dead pet. |
| Mend Pet | Pet (heal) | — | Instant / — | Heals the pet over several seconds. |
| Command Pet / Pet basics | Pet | — | — | Directs pet attack/follow/move; Pack Leader beasts (Boar/Bear/Wyvern) are summoned by *Howl of the Pack Leader*. |
| Ancient Hysteria | Pet (Bloodlust) | — | Instant / (raid CD) | Certain pets provide the Bloodlust/Heroism-equivalent haste burst to the group. @verify-ingame (pet family) |
| Howl of the Pack Leader | Passive / Pet (Pack Leader) | — | — | Periodically readies a beast summon (Boar single big charge / Bear / Wyvern) that adds burst; the Pack Leader engine, synced to Kill Command. |
| Moonlight Chakram | Rotational (Sentinel) | — | Instant / — | Sentinel hero ability: a thrown chakram used inside Tip of the Spear windows; part of the Sentinel priority. @verify-ingame |
