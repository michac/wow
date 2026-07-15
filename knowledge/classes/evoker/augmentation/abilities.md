---
title: Augmentation Evoker — Abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight branch engine/class_modules/apl/apl_evoker.cpp augmentation_12_0_5  # tier 1, 2026-07-11
  - https://www.method.gg/guides/augmentation-evoker/playstyle-and-rotation  # tier 3, 2026-07-11
  - https://www.icy-veins.com/wow/augmentation-evoker-pve-dps-rotation-cooldowns-abilities  # tier 3, 2026-07-11
  - raw/wago/SpellName.csv (Tier 1 game data — name canonicalization)  # tier 1, 2026-07-11
confidence: medium
---

# Augmentation Evoker — Abilities (Midnight S1)

## Overview

Augmentation is Evoker's **support DPS** spec: a large share of its damage
lands as **buffs on allies** rather than its own meter. The rotation exists to
keep two team buffs alive — **Ebon Might** (grants your primary stat to your
4 highest-damage nearby allies) and **Prescience** (crit/versatility on a
chosen ally) — and to funnel a raid-wide burst into **Breath of Eons**, which
banks a slice of everyone's damage and detonates it.

- **Resource: Essence** (max 5, or 6 with Font of Magic). Regenerates slowly on
  its own; you build it faster with **Living Flame / Azure Strike** and
  **Essence Burst** procs, then spend it on **Eruption** (the signature
  spender, which also **extends Ebon Might**).
- **Empowers:** Fire Breath and Upheaval are hold-to-rank spells — holding the
  key charges the empower level. Augmentation deliberately casts them at **low
  rank** most of the time (fast, keeps the Ebon Might loop moving).
- **Hero trees:** **Scalecommander** (adds a personal-damage bombardment layer
  via Breath of Eons; the general default and the clear M+ pick) and
  **Chronowarden** (time-magic buff-extension, ~3% more single-target). See
  `builds.md`.

Empowered/support kit is a small set of buttons pressed constantly; most of the
inventory below is utility, defensives, and CC that you press reactively.

## Ability inventory

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| **Ebon Might** | Rotational-builder (maintain) | — (Essence-free) | Instant · GCD, no CD | Grants your primary stat to your top ~4 nearby allies and buffs your own damage; ~10s base, **extended by Eruption/Fire Breath/Upheaval**. The buff you keep up at all times. |
| **Prescience** | Rotational-builder (maintain) | — | Instant · ~2 charges | Buffs an ally with crit + versatility (~18s). Cast on your best damage dealers; casting while targeting an enemy smart-buffs a random DPS. @verify-ingame (charge count / recharge) |
| **Eruption** | Rotational-spender | 3 Essence (2 w/ Volcanism) | ~2.5s cast | Signature spender: earth erupts on the target for AoE damage and **extends Ebon Might**. Spend Essence here during an Ebon Might window. @verify-ingame (cast time) |
| **Living Flame** | Rotational-builder / filler | — | ~2s cast | Filler nuke (or heal). Feeds Essence Burst / Leaping Flames procs. Chronowarden turns this into **Chrono Flame**. |
| **Azure Strike** | Rotational-builder / filler | — | Instant | Instant ranged filler, hits 2 targets. The APL's default instant filler; press when Living Flame's cast doesn't fit. |
| **Fire Breath** | Major cooldown (empower) | — | Empower · ~30s CD | Frontal empowered fire DoT. Cast **rank 4 with Leaping Flames, rank 1 without** (per the APL) during Ebon Might. |
| **Upheaval** | Major cooldown (empower) | — | Empower · ~40s CD | Empowered ground burst (AoE knock-up + damage). APL casts **rank 1**; guides suggest upranking for AoE radius coverage. |
| **Breath of Eons** | Major cooldown | — | ~30s?/2 min CD | Fly across the battlefield banking allies' damage as **Temporal Wound**, then detonate it. The spec's big burst window; stack ally cooldowns into it. Replaces Deep Breath. @verify-ingame (CD) |
| **Blistering Scales** | Utility / ally-defensive | — | Instant · ~30s CD | Armor buff (stacks) on an ally, usually the **tank**; also does damage when the tank is hit. Applied pre-pull and re-applied when stacks run low. @verify-ingame (charges/CD) |
| **Time Skip** | Major cooldown (CD acceleration) | — | Channel · ~1.5 min CD | Channel that **advances your own cooldowns** (Fire Breath/Upheaval/Breath of Eons). Woven in when the empowers are down. @verify-ingame (CD / amount) |
| **Tip the Scales** | Major cooldown (empower enabler) | — | Instant · 2 min CD | Makes your **next empowered spell instant and max rank**. Paired with Fire Breath (or Breath of Eons on some builds). |
| **Hover** | Movement | — | Instant · 2 charges, ~35s | Lets you **cast while moving** for the duration. Off-GCD; used to weave casts around movement. |
| **Deep Breath** | Movement / cooldown (situational) | — | ~1 min CD | Fly forward dealing damage along the path. Present in the APL/Scalecommander kit alongside Breath of Eons. @verify-ingame (availability/CD for Aug) |
| **Quell** | Interrupt | — | Instant · 40s CD | Ranged interrupt. |
| **Obsidian Scales** | Defensive | — | Instant · 2 charges, ~90s | −30% damage taken. Core personal mitigation. @verify-ingame (values) |
| **Renewing Blaze** | Defensive / self-heal | — | Instant · ~90s CD | Damage taken over the next 8s is healed back. @verify-ingame (CD) |
| **Zephyr** | Defensive (group) / movement | — | ~2 min CD | Group damage reduction + minor movement speed for nearby allies. @verify-ingame (CD) |
| **Renewing / Verdant Embrace** | Utility / heal + movement | — | Instant · ~24s CD | Heal an ally and **pull yourself to them** (or them to you). Also triggers Ancient Flame. @verify-ingame (CD) |
| **Emerald Blossom** | Utility / AoE heal | Essence | Instant | Ground-target AoE heal; used with Dream of Spring builds to spend Essence Burst as a heal. |
| **Cauterizing Flame** | Dispel / heal | — | Instant · ~1 min CD | Removes Bleed/Poison/Curse/Disease from an ally and heals them. @verify-ingame (CD) |
| **Expunge** | Dispel | — | Instant · ~8s CD | Removes a Poison effect from an ally. @verify-ingame (CD) |
| **Source of Magic** | Utility (mana battery) | — | Instant | Assign to a healer: they gain mana whenever you deal damage. Drop if another Evoker covers it. |
| **Rescue** | Movement (ally) | — | Instant · ~1 min CD | Fly to an ally and carry them back to safety; grants them a small shield. @verify-ingame (CD) |
| **Sleep Walk** | CC | — | ~1.5s cast | Puts an enemy to sleep (disorient); breaks on damage. Pack-skip / kite tool. |
| **Landslide** | CC (root) | — | Instant · ~1.5 min CD | Roots enemies in a line. @verify-ingame (CD) |
| **Oppressing Roar** | CC (amplify) | — | Instant · ~2 min CD | Roar that increases the duration of loss-of-control on affected enemies; with Overawe also soothes enrages. @verify-ingame (CD) |
| **Tail Swipe** | CC (knockback) | — | Instant · ~3 min CD | AoE knockback behind you. @verify-ingame (CD) |
| **Fury of the Aspects** | Major cooldown (Bloodlust) | — | ~5 min CD | Raid Heroism/Bloodlust equivalent (+30% haste); causes Exhaustion. |
| **Spatial Paradox** | Utility (haste burst) | — | 2 min CD | Empowers you **and an ally** with a large haste/casting buff. Choice node vs Time Spiral. @verify-ingame (values) |
| **Draconic Attunements** | Utility (group aura) | — | Instant (toggle) | Talent granting a group aura toggled between **Black Attunement** (armor/stamina) and **Bronze Attunement** (movement speed). |
| **Blessing of the Bronze** | Utility (raid buff) | — | Instant | Raid-wide movement-speed / cooldown buff; cast pre-combat. |
| **Return** | Utility (teleport) | — | ~2s cast, long CD | Teleport back to a location you set with a portal. Out-of-combat mobility. |
| **Swoop Up** | CC / utility (PvP talent) | — | Instant | Grab a target into the air. PvP-oriented. @verify-ingame |
| **Chrono Loop** | CC (PvP talent) | — | Instant | Traps an enemy; after a few seconds returns them to their earlier position and health. PvP-oriented. @verify-ingame |
| **Time Stop** | Utility (PvP talent) | — | Instant | Freezes an ally in stasis — invulnerable but unable to act — for a few seconds. PvP-oriented. @verify-ingame |
| **Essence Burst** | Notable passive | — | Passive | Your builders/empowers proc a charge that makes the **next Eruption free**. Drives the spender cadence. |
| **Leaping Flames** | Notable passive | — | Passive | After an empower, Living Flame gains extra bounces / an Essence Burst chance; changes Fire Breath to rank-4 usage in the APL. |

> **Name-reconciliation notes (vs `raw/wago/SpellName.csv`, Tier 1):** all seed
> names verify as current game-data names — Ebon Might (395152), Breath of Eons
> (403631), Blistering Scales (360827), Fire Breath (37985), Time Skip (404977),
> Sleep Walk (360806), Spatial Paradox (406732), Tip the Scales (370553), Source
> of Magic, Verdant Embrace, Swoop Up (370388), Chrono Loop (383005), Time Stop.
> **Black/Bronze Attunement (403264/403265)** are the two toggle states of the
> **Draconic Attunements** talent, not standalone buttons. **Prescience (409311)**
> is the Augmentation version (the seed's generic name maps to it). No renames
> detected for Midnight.
