---
title: Devastation Evoker — Abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Evoker_Devastation.simc  # tier 1 APL + talent string, 2026-07-11
  - https://wago.tools/db2 SpellName @ 12.0.7  # tier 1 game-data name reconcile, 2026-07-11
  - https://www.method.gg/guides/devastation-evoker/playstyle-and-rotation  # tier 3, 2026-07-11
  - https://www.icy-veins.com/wow/devastation-evoker-pve-dps-rotation-cooldowns-abilities  # tier 3, 2026-07-11
confidence: medium
---

# Devastation Evoker — Abilities (Midnight S1)

## Overview

Devastation is Evoker's ranged-caster DPS spec — a mid-range (25 yd) "empower"
caster built around two resources:

- **Essence** — a passively-regenerating point pool (base **5**, or **6** with
  *Power Nexus*). Spent on **Disintegrate** (single-target channel) and **Pyre**
  (instant AoE). **Essence Burst** is the key proc: it makes the next Essence
  spender **free**, and stacks to 2 with *Essence Attunement*. Empowered casts
  and Living Flame (via *Ruby/Azure Essence Burst* and *Leaping Flames*) generate
  it.
- **Empowerment** — **Fire Breath**, **Eternity Surge**, and **Deep Breath** are
  *empower* spells: you hold the cast to raise its rank (I–IV), trading cast time
  for more targets / more damage. In practice Devastation casts **Fire Breath and
  Eternity Surge at Rank 1** (short cast, on cooldown) and only pushes higher
  ranks when *Tip the Scales* makes the cast instant or for wide AoE.

Playstyle: keep the two short empower cooldowns rolling, pool them into
**Dragonrage** (the 2-minute burst window), and chain **Disintegrate** to spend
Essence without gaps. Mobility is skill-expressed through **Hover**, which lets
you cast and channel while moving (weave it right after an instant so it hides
inside the GCD).

**Hero trees (Midnight S1):**
- **Scalecommander** — the meta pick across most content. Empower casts grant
  **Mass Disintegrate** charges that turn Disintegrate into a multi-target cleave,
  and **Deep Breath** becomes a rotational damage button (via *Imminent
  Destruction* / *Onyx Legacy* / *Bombardments*).
- **Flameshaper** — a concentrated-AoE / DoT-focused alternative. Grants a
  **second Fire Breath charge** and the **Engulf** button, and **Consume Flame**
  detonates the remaining Fire Breath DoT for a burst. Weaker on target swaps.

## Ability inventory

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Living Flame | Rotational-builder (filler) | — | 1.9s cast (instant while Hover/Burnout) | Baseline filler; deals Fire dmg (heals when cast on an ally). Chance to grant Essence Burst; with *Leaping Flames* bounces to extra targets after an empower. |
| Azure Strike | Rotational-builder (filler) | — | Instant | Instant Spellfrost bolt hitting the target + 1 nearby enemy (2 total). Low-priority filler / movement filler. |
| Disintegrate | Rotational-spender (ST) | 3 Essence | ~3s channel (3 ticks) | Primary single-target spender. **Chain-cast** it (recast just before the channel ends) to avoid tick gaps. *Mass Disintegrate* (Scalecommander) makes it cleave. |
| Pyre | Rotational-spender (AoE) | 3 Essence | Instant | Instant AoE Fire nova at the target. Preferred spender at 3–4+ stacked targets; builds *Charged Blast*. |
| Fire Breath | Major cooldown / DoT | — | Empower (hold), ~30s CD | Frontal cone: burst on cast + a Fire DoT. Cast at **Rank 1** on cooldown; generates Essence Burst. Flameshaper gets a **2nd charge**. @verify-ingame (exact CD) |
| Eternity Surge | Major cooldown (burst) | — | Empower (hold), ~30s CD | Focused Spellfrost burst; higher ranks split across more targets (with *Eternity's Span* it hits 2× targets per rank). Cast on cooldown, Rank 1 in ST. @verify-ingame (exact CD) |
| Dragonrage | Major cooldown | — | Instant, 120s CD | The burst window: buffs damage, fires Pyre volleys, and (with *Animosity*) is **extended** each time you empower during it. Line Fire Breath + Eternity Surge inside it. |
| Deep Breath | Major cooldown / Movement | — | ~120s CD (reduced by *Onyx Legacy* / *Imminent Destruction*) | Fly across the target area dealing Fire damage along the path. Doubles as a gap-closer. Core rotational button for **Scalecommander**. |
| Tip the Scales | Major cooldown (utility) | — | Instant, 120s CD | Makes your next empower spell cast **instantly at max rank**. Usually spent on Eternity Surge (or Fire Breath) inside Dragonrage. |
| Firestorm | Rotational / AoE (talent) | — | Instant, ~20s CD | Ground-targeted swirling Fire AoE over several seconds. AoE-lean talent. @verify-ingame |
| Shattering Star | Rotational (talent) | — | Instant, ~20s CD (2 charges) | Spellfrost hit that grants Essence Burst and applies a damage-amp debuff (armor/damage-taken). @verify-ingame |
| Azure Sweep | Rotational (Midnight-new, spec talent) | — | Passive/triggered | Midnight addition: empower/Eternity-Surge casts unleash a Spellfrost sweep on nearby enemies; appears in the APL as its own priority entry (`azure_sweep`). @verify-ingame |
| Mass Disintegrate | Passive (Scalecommander hero) | — | Passive | Empower casts grant charges that make the next Disintegrate(s) hit all nearby enemies. Defining Scalecommander mechanic. |
| Engulf | Rotational (Flameshaper hero) | — | ~short CD | Flameshaper button: consumes/empowers the Fire Breath DoT on the target for a burst. @verify-ingame |
| Unravel | Rotational (talent, situational) | 1 Essence | Instant | Shatters an enemy absorb shield for Spellfrost damage; listed PASSIVE in the 12.0.7 tree — may be reworked from the old active. @verify-ingame |
| Rising Fury | Apex (talent, active) | — | during Dragonrage | Midnight apex: active/effect tied to Dragonrage granting stacking haste and Essence Burst. Listed ACTIVE row 14,18 in the tree. @verify-ingame |
| Obsidian Scales | Defensive | — | Instant, ~150s CD (2 charges w/ *Obsidian Bulwark*) | Reduces damage taken (~30%). Core survival cooldown. @verify-ingame (value/CD) |
| Renewing Blaze | Defensive / self-heal (talent) | — | Instant, ~90s CD | Heals a % of damage taken over the following seconds — a self-heal-over-time. @verify-ingame |
| Zephyr | Defensive (raid) | — | Instant, 120s CD | Grants you + nearby allies a burst of movement speed and damage reduction. @verify-ingame |
| Verdant Embrace | Movement / heal | — | Instant, ~24s CD | Fly to an ally (or pull them) and heal them. Doubles as mobility; triggers *Ancient Flame*. @verify-ingame |
| Emerald Blossom | Self-heal / AoE heal | Essence (or free proc) | Instant | Ground heal at the target area; used off *Ancient Flame*/green procs for damage builds. |
| Rescue | Movement / utility | — | Instant, ~60s CD | Grip a friendly target to your location (intervene-style save). @verify-ingame |
| Cauterizing Flame | Dispel / heal | — | Instant, ~60s CD | Removes a Bleed/Poison/Curse/Disease and heals the target. @verify-ingame |
| Expunge | Dispel | — | Instant, ~8s CD | Removes a Poison effect from a friendly target. @verify-ingame |
| Quell | Interrupt | — | Instant, 40s CD | Spell interrupt (kick) + short school lock. The APL fires it off-GCD on `target.debuff.casting.react`. |
| Sleep Walk | CC | — | ~1.5s cast, ~15s CD | Puts an enemy to sleep (incapacitate), broken by damage. Single-target CC. @verify-ingame |
| Oppressing Roar | CC (talent) | — | Instant, ~120s CD | Roar that increases the duration of crowd-control on nearby enemies; AoE CC utility. @verify-ingame |
| Landslide | CC (talent) | — | ~2s cast, ~90s CD | Roots enemies in a line. @verify-ingame |
| Tail Swipe | CC | — | Instant, ~180s CD | Knock-back / stagger the enemies behind you. @verify-ingame |
| Hover | Movement | — | Instant, ~35s CD (2 charges) | Lets you cast and channel while moving for its duration; not on the GCD. Central to Devastation mobility. @verify-ingame |
| Spatial Paradox | Major cooldown (utility, choice) | — | Instant, ~120s CD | External: grants you or an ally a large haste/empower burst (allows empowers to cast instantly). Choice-node vs *Time Spiral*. @verify-ingame |
| Source of Magic | Utility (mana) | — | Instant | Buffs a healer/ally, returning mana when you deal damage. Assign to a mana user. |
| Blessing of the Bronze | Utility (raid buff) | — | Instant | Raid buff: movement-speed / snare component (the Evoker raid-wide buff). |
| Fury of the Aspects | Utility (Bloodlust) | — | Instant, 300s CD | Evoker's Bloodlust/Heroism-equivalent 30% haste raid cooldown (Exhaustion applies). |
| Time Spiral | Utility (talent, choice) | — | Instant, ~120s CD | Lets you + nearby allies cast while moving briefly. Choice-node vs *Spatial Paradox*. @verify-ingame |
| Return | Utility (teleport) | — | Cast, ~long CD | Bronze teleport back to a stored location; out-of-combat travel utility. @verify-ingame |
| Swoop Up | Utility (PvP talent) | — | Instant | **PvP talent** — grab an ally/enemy into the air. Not part of the PvE kit. @verify-ingame |
| Chrono Loop | CC (PvP talent) | — | Instant | **PvP talent** — traps a target, returning them to their earlier position/health. Not part of the PvE kit. @verify-ingame |
| Time Stop | CC / utility (PvP talent) | — | Instant | **PvP talent** (Preservation-flavored) — freezes a target in time. Not part of the Devastation PvE kit. @verify-ingame |

> Name-reconcile notes (Tier-1 game data, SpellName @ 12.0.7):
> - **Azure Sweep** (1265867) and **Mass Disintegrate** (401642 / Scalecommander
>   passive 436335) are Midnight-relevant spec/hero additions confirmed in the
>   live spell table.
> - **Sleep Walk** (360806) is the current name for the old "Sleep" CC.
> - **Swoop Up** (370388), **Chrono Loop** (383005), **Time Stop** are Evoker
>   **PvP talents** — the seed list carried them, but they are not PvE
>   rotational/utility buttons; flagged accordingly.
