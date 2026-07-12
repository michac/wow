---
title: Hunter Beast Mastery — ability inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-07-12
reviewed: 2026-07-12
sources:
  - simc midnight branch profiles/MID1/MID1_Hunter_Beast_Mastery.simc  # tier 1 APL + talent string, WoW 12.0.x
  - https://www.method.gg/guides/beast-mastery-hunter/playstyle-and-rotation  # tier 3, 12.0.7
  - https://www.icy-veins.com/wow/beast-mastery-hunter-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7
  - raw/wago/SpellName.csv  # tier 1, name reconcile @ 12.0.7.67808
confidence: medium
---

# Beast Mastery Hunter — abilities (Midnight S1, 12.0.7)

## Overview

Beast Mastery is a **ranged physical** spec whose damage is delivered mostly
by the **pet(s)**, which means every ability is instant and castable while
moving — the spec's signature. Resource is **Focus** (0–100, passive regen),
generated chiefly by **Barbed Shot** (instant chunk via Pack Tactics) and
spent on **Kill Command** and the **Cobra Shot** filler. The core loop is a
two-charge juggle: never cap **Kill Command** or **Barbed Shot** charges, keep
the pet's **Frenzy** stacks rolling with Barbed Shot, and pour everything else
into Cobra Shot, all funnelled into the **Bestial Wrath** burst window every
30s.

Two hero trees in S1:
- **Pack Leader** — builds and spends **Howl of the Pack Leader** to summon a
  rotating cast of empowered beasts (Wyvern / Boar / Bear) plus a **Stampede**
  line on the first Kill Command inside Bestial Wrath. The default / recommended
  tree for both single-target and AoE.
- **Dark Ranger** — adds **Black Arrow** (a Deathblow-triggering shadow
  attack) and **Wailing Arrow**, with a **Withering Fire** burst window. An
  alternative single-target line.

> Names reconciled against `raw/wago/SpellName.csv` (12.0.7.67808): Cobra Shot
> (145654), Barbed Shot (62318), Kill Command (34026), Wild Thrash (238250),
> Bestial Wrath (19574), Black Arrow (Dark Ranger, 466930), Dire Beast (120679)
> / Dire Beast: Hawk (208652), Wild Kingdom (356707), Chimaeral Sting (356719),
> Ancient Hysteria (90355). **Interrupt note:** the seed listed *Muzzle*, but
> Muzzle is the **Survival** melee interrupt — Beast Mastery's interrupt is
> **Counter Shot** (147362, in the class tree). @verify-ingame

## Inventory

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Barbed Shot | Rotational-builder | Generates ~25 Focus (Pack Tactics) | Instant · 2 charges, ~12s recharge | Applies/refreshes a bleed and stacks the pet's **Frenzy** (attack-speed buff). The spec's Focus engine and Frenzy-uptime button; never let charges cap. In Midnight it functions as a rolling DoT that stacks rather than resetting. @verify-ingame (recharge/Focus exact) |
| Kill Command | Rotational-spender | 30 Focus | Instant · 2 charges (Alpha Predator), ~7.5s recharge | Commands the pet to savage the target — the primary spender and hardest hit. Empowered when **Nature's Ally** or **Howl of the Pack Leader** is up. Killer Cobra / Killer Instinct interactions in-tree. |
| Cobra Shot | Rotational-builder/filler | 35 Focus | Instant | Focus-dump filler between Kill Command and Barbed Shot; reduces Kill Command's cooldown (strongly with **Killer Cobra** during Bestial Wrath). Decrements the Howl of the Pack Leader timer. @verify-ingame (Focus cost) |
| Wild Thrash | Rotational-spender (AoE) | Focus | Instant · short CD | Midnight's primary AoE ability — **replaces Multi-Shot**. Enables/maintains **Beast Cleave** so the pet's Kill Commands hit all nearby enemies. Press whenever 2+ targets are up, even briefly. @verify-ingame (Focus cost/CD) |
| Bestial Wrath | Major cooldown | No cost | Instant · 30s CD, ~15s duration | The core burst window: **+20% damage** (Midnight redesign, down from 30%) plus an upfront burst on activation. Triggers the capstones of **both** hero trees — Pack Leader's Howl summon + Stampede, Dark Ranger's Withering Fire. Dump Barbed Shot charges before pressing. |
| Bloodshed | Passive | — | — | In the Midnight tree Bloodshed is a **passive** pet-damage talent (not the old active button). |
| Dire Beast | Passive | — | — | Passively summons a short-lived beast to attack (procs off rotation). Pack Leader summons flavoured variants (**Dire Beast: Hawk** etc.). |
| Nature's Ally | Rotational-empower (active) | — | Instant · CD | Spec capstone active that grants the **Nature's Ally** buff, empowering the next Kill Command(s). @verify-ingame (exact effect) |
| Black Arrow | Rotational-spender (Dark Ranger) | Focus | Instant · CD | Dark Ranger shadow attack; low-health execute that can trigger **Deathblow** (free reset) and, in AoE, helps re-apply **Beast Cleave**. Spammable during **Withering Fire**. Dark Ranger only. |
| Wailing Arrow | Rotational-spender (Dark Ranger) | Focus | ~2s cast | Dark Ranger nuke that guarantees a **Deathblow** proc and interrupts/silences targets hit for 1s. Replaces the Bestial Wrath button after activation in the Dark Ranger build. Dark Ranger only. @verify-ingame |
| Hunter's Mark | Utility (buff) | No cost | Instant | Marks the target (bonus damage; reveals if stealthed). Apply pre-pull on the main target. |
| Kill Shot | Execute | Focus | Instant · CD | Not present in the Midnight BM tree as a core button — execute pressure comes from Black Arrow / Deathblow instead. @verify-ingame (confirm absence) |
| Counter Shot | Interrupt | No cost | Instant · 24s CD | Ranged interrupt (3s school lockout). BM's kick (class tree). Not Muzzle. |
| Tranquilizing Shot | Dispel | 10 Focus | Instant · ~10s CD | Removes an Enrage or a Magic buff from the target. |
| Intimidation | CC | No cost | Instant · ~60s CD | Commands the pet to stun the target ~5s. |
| Binding Shot | CC | No cost | Instant · ~45s CD | Ground zone; enemies that move too far are stunned. AoE control. |
| Freezing Trap | CC | No cost | Instant · 30s CD | Incapacitates the first enemy that enters (breaks on damage). |
| Tar Trap | CC / slow | No cost | Instant · CD | Ground slow field; **Tar-Coated Bindings** synergy with Binding Shot. Choice-node vs Scare Beast. |
| Scare Beast | CC | Focus | Cast | Fears a beast; choice-node alternative to Tar Trap. |
| Concussive Shot | CC / slow | No cost | Instant · 5s CD | Single-target movement slow. |
| Chimaeral Sting | CC | No cost | Instant · CD | Applies a disorienting poison (utility/PvP-leaning control). @verify-ingame |
| Muzzle | Interrupt (Survival) | — | — | **Not a Beast Mastery ability** — Survival's melee interrupt; listed only to disambiguate the seed. BM uses Counter Shot. |
| Exhilaration | Defensive (self-heal) | No cost | Instant · 2min CD | Heals a large chunk of your (and your pet's) max health; boosted by **Wilderness Medicine / Natural Mending**. |
| Aspect of the Turtle | Defensive (immunity) | No cost | Instant · 3min CD | ~8s immunity to all damage/CC; you cannot attack while active. The panic button. |
| Survival of the Fittest | Defensive | No cost | Instant · ~3min CD | Reduces damage taken by you and your pet (~30%) for a short window. |
| Roar of Sacrifice | Defensive (external) | No cost | Instant · CD | Places a buff on a party member redirecting a share of damage they take to you. Choice-node vs Guardian's Hide. |
| Survival cooldown — Aspect of the Cheetah | Movement | No cost | Instant · ~3min CD | Burst movement speed (then a lingering lesser boost); **Improved Aspect of the Cheetah** in tree. |
| Disengage | Movement | No cost | Instant · ~20s CD | Leap backwards; disengages from melee. |
| Feign Death | Utility | No cost | Instant · 30s CD | Drops combat / threat; also used to cancel casts and dodge mechanics. |
| Misdirection | Utility (threat) | No cost | Instant · ~30s CD | Redirects your next few seconds of threat to your pet or a target ally. |
| Camouflage | Utility (stealth) | No cost | Instant · CD | Stealth + minor heal-over-time; used to skip packs / reset. |
| Flare | Utility | No cost | Instant · ~20s CD | Reveals stealth and removes some tracking/stealth effects in an area. |
| Call Pet (1–5) | Pet | No cost | Cast | Summons one of your five stabled pets. |
| Revive Pet | Pet | No cost | Cast | Resurrects a dead pet. |
| Mend Pet | Pet (heal) | No cost | Channel · 10s CD | Heals the pet over time. |
| Command Pet | Pet (utility) | — | — | Pet control (attack/follow/passive, special abilities). |
| Wild Kingdom | Pet (utility/heal) | No cost | Instant · CD | Instantly heals/revives your pet and briefly calls additional pets to attack. @verify-ingame |
| Ancient Hysteria / Primal Rage | Utility (Bloodlust) | No cost | Instant · long CD | Pet-provided Bloodlust/Heroism-equivalent (+30% haste, party-wide; exhaustion after). Availability depends on pet family / Primal Rage. @verify-ingame |
| Auto Shot | Passive/auto | No cost | Auto | Automatic ranged attack; ticks in the background (in the APL as `auto_shot`). |
