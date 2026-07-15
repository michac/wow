---
title: Havoc Demon Hunter — Ability Inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Demon_Hunter_Havoc.simc  # tier 1, simc midnight branch APL + default profile (Fel-Scarred), 2026-07-11
  - https://www.icy-veins.com/wow/havoc-demon-hunter-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
  - https://www.method.gg/guides/havoc-demon-hunter/playstyle-and-rotation  # tier 3, 12.0.7, 2026-07-11
  - raw/wago/SpellName.csv  # tier 1 game data, name canonicalization, 2026-07-11
confidence: high
---

# Havoc Demon Hunter — Ability Inventory (Midnight S1)

## Overview

Havoc is the melee-DPS Demon Hunter spec. Its resource is **Fury** (0–120+),
generated mostly passively (auto-attacks via **Demon Blades**, plus **Immolation
Aura** ticks) and spent on **Chaos Strike** (single-target) and **Blade Dance**
(AoE). The whole spec is built around the **demon-form (Demonic) window**:
casting **Eye Beam** briefly transforms you, and while transformed Chaos Strike
and Blade Dance are replaced by the stronger **Annihilation** and **Death Sweep**.
**Metamorphosis** is the big transform on a ~2-min cadence. High mobility
(Fel Rush, Vengeful Retreat, Felblade, The Hunt) is core to both damage and
positioning.

Two hero trees in S1:

- **Fel-Scarred** — the S1 default (the simc profile is `..._Fel-Scarred`).
  Adds **Demonsurge** (Eye Beam/Meta empower next Annihilation + Death Sweep) and,
  via **Demonic Intensity**, the empowered forms **Abyssal Gaze** (Eye Beam) and
  **Consuming Fire** (Immolation Aura). Frontloads burst inside Metamorphosis.
- **Aldrachi Reaver** — collect 6 soul fragments (via **Art of the Glaive**) to
  turn Throw Glaive into **Reaver's Glaive**, which applies **Reaver's Mark** and
  empowers the next Chaos Strike (**Rending Strike**) and Blade Dance
  (**Glaive Flurry** → **Fury of the Aldrachi** slashes). Strong funnel/cleave.

> Midnight note: a **third** Demon Hunter spec, **Devourer**, exists in 12.0.7
> game data (separate simc profile). This file is Havoc only.

## Inventory

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| **Chaos Strike** | Rotational-spender | ~40 Fury | Instant | Core single-target spender; a crit refunds ~20 Fury. Replaced by Annihilation in demon form. @verify-ingame (exact Fury cost) |
| **Annihilation** | Rotational-spender | ~40 Fury | Instant | Demon-form (Metamorphosis/Demonic) version of Chaos Strike; higher damage. Consumes **Demonsurge** for Fel-Scarred. |
| **Blade Dance** | Rotational-spender (AoE) | ~35 Fury | Instant, ~9s CD | Spin dealing AoE around you; triggers **Glaive Tempest** passive at 3+ targets. Replaced by Death Sweep in demon form. @verify-ingame (exact Fury cost) |
| **Death Sweep** | Rotational-spender (AoE) | ~35 Fury | Instant, ~9s CD | Demon-form version of Blade Dance; higher damage. Consumes **Demonsurge** for Fel-Scarred. |
| **Eye Beam** | Rotational-builder / burst | ~30 Fury | ~2s channel, ~40s CD | Channel that triggers the **Demonic** demon-form window; primary damage cooldown. **Chaotic Transformation** resets its CD on Meta; **Cycle of Hatred** lowers it. @verify-ingame (exact Fury cost) |
| **Immolation Aura** | Rotational-builder | Free (generates Fury) | Instant, ~30s CD (2 charges w/ **A Fire Inside**) | AoE fire aura + steady Fury generation; **Ragefire** stores its damage to detonate. |
| **Felblade** | Movement / builder | Free (generates Fury) | Instant, ~15s CD | Gap-closer that generates Fury; used to trigger **Inertia** before burst windows. |
| **Demon's Bite** | Rotational-builder | Generates Fury | Instant | Baseline Fury builder — **replaced by the passive Demon Blades** in the S1 build, so rarely a manual press. |
| **Essence Break** | Rotational (burst amp) | Free | Instant, ~40s CD | Short window (~4s) that hugely amplifies Chaos Strike / Blade Dance damage; filled with Death Sweep + Annihilation. |
| **Metamorphosis** | Major cooldown | Free | Instant, ~2 min | Leap to target (stuns on land), transform: +Haste, empowers Chaos Strike/Blade Dance, and (w/ Chaotic Transformation) resets Eye Beam + Blade Dance. Core 2-min burst. |
| **The Hunt** | Major cooldown | Free | ~1.5s cast, ~90s CD | Charge dealing heavy nature damage + DoT; central burst button, reduced CD via **Eternal Hunt**. For Aldrachi Reaver, guarantees a Reaver's Glaive proc. |
| **Throw Glaive** | Rotational / ranged | Free (charges) | Instant, ~9s recharge | Ranged glaive throw; becomes a rotational button with **Soulscar** / **Furious Throws**. Turns into **Reaver's Glaive** for Aldrachi Reaver. |
| **Reaver's Glaive** | Rotational-spender enabler (AR) | Free | Instant | Aldrachi Reaver: replaces Throw Glaive after 6 soul fragments; applies **Reaver's Mark** and empowers the next Chaos Strike + Blade Dance. |
| **Abyssal Gaze** | Major cooldown (FS) | ~30 Fury | ~2s channel | Fel-Scarred **Demonic Intensity** empowered Eye Beam during Metamorphosis. |
| **Consuming Fire** | Rotational-builder (FS) | Free | Instant | Fel-Scarred **Demonic Intensity** empowered Immolation Aura during Metamorphosis. |
| **Demonsurge** | Passive/proc (FS) | — | — | Fel-Scarred proc from Eye Beam/Meta; makes the next Annihilation + Death Sweep hit harder (tracked as "demonsurge available"). |
| **Glaive Tempest** | Passive | — | — | S1 talent: Blade Dance/Death Sweep at 3+ targets releases spinning glaives for AoE (a passive, not a pressed button). |
| **Fel Rush** | Movement | Free (2 charges) | Instant, ~10s recharge | Dash forward dealing damage; mobility + an **Inertia** trigger / filler. |
| **Vengeful Retreat** | Movement | Free | Instant, ~20s CD | Backflip away, slows nearby enemies; procs **Initiative** / **Tactical Retreat**; woven before Eye Beam windows. |
| **Blur** | Defensive | Free | Instant, ~1 min CD | +50% dodge and −20% damage taken for a short time; core personal defensive. |
| **Darkness** | Defensive (raid) | Free | Instant, ~5 min CD | Ground AoE giving allies a chance to avoid incoming attacks; group cooldown. |
| **Disrupt** | Interrupt | Free | Instant, ~15s CD | Kick/interrupt a spellcast; the primary interrupt. |
| **Consume Magic** | Dispel | Free | Instant, ~10s CD | Interrupt + consume a beneficial magic effect from the target (offensive dispel). @verify-ingame (exact CD) |
| **Chaos Nova** | CC (AoE stun) | ~Free | Instant, ~45s CD | Burst of fel energy stunning nearby enemies (~2s). |
| **Sigil of Misery** | CC (AoE) | Free | Instant, ~90s CD | Places a delayed sigil that causes enemies in its area to cower/disorient. |
| **Imprison** | CC | Free | Instant, ~45s CD | Incapacitates a target (Demon/Beast/Humanoid/Undead) for the duration. |
| **Torment** | Utility (taunt) | Free | Instant, ~8s CD | Taunts the target to attack you; single-target threat/utility. |
| **Spectral Sight** | Utility | Free | Instant, ~30s CD | See hidden/stealthed enemies and through obstacles; reduced movement speed while active. |
| **Sigil of Spite** | Rotational (talent) | Free | Instant, CD | Talent sigil: detonates for damage / soul fragments; niche in some builds. @verify-ingame (Havoc uptake) |
| **Fel Barrage** | Major cooldown (talent) | Fury | Channel, ~60s CD | Talent: rapid barrage of Fel damage to nearby enemies; AoE-burst alternative. @verify-ingame (Havoc uptake) |
| **Rain from Above** | CC / utility (PvP talent) | Free | Instant | PvP talent: lift into the air, immune to melee, rain glaives; not a PvE button. |
| **Illidan's Grasp** | CC (PvP talent) | Free | Channel | PvP talent: seize a target, then throw or slam them. |
| **Reverse Magic** | Dispel (PvP talent) | Free | Instant, ~1 min CD | PvP talent: remove harmful magic from party/raid and send it back to enemies. |
