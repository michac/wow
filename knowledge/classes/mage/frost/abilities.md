---
title: Frost Mage — Ability Inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Mage_Frost.simc  # tier 1 APL, 2026-07-11
  - https://www.method.gg/guides/frost-mage/playstyle-and-rotation  # tier 3, 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/frost-mage-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
  - raw/wago/SpellName.csv  # tier 1 game-data name reconcile, 2026-07-11
confidence: high
---

# Frost Mage — Ability Inventory (Midnight S1)

## Overview

- **Hero trees:** **Spellslinger** (the S1 meta pick for essentially all content
  — Splinter procs off spells, cooldown reduction on Frozen Orb) and **Frostfire**
  (alternative; Frostbolt/Flurry become Frostfire spells, Glacial Spike explodes on
  impact, front-loaded burst better suited to outdoor content). See `builds.md`.
- **Resource:** **Mana** (rarely a constraint), plus four rotational
  proc/charge systems: **Freezing stacks** (the Midnight replacement for the old
  Winter's Chill debuff — applied to the target by Flurry/Ice Lance/Frozen Orb/
  Ray of Frost/Glacial Spike, capped at 20, consumed by Ice Lance & Comet Storm to
  trigger **Shatter** AoE damage scaled to stacks consumed), **Fingers of Frost**
  (proc → instant, max-Shatter Ice Lance), **Brain Freeze** (proc → instant Flurry),
  and **Icicles** (Frostbolt builds them; 5 Icicles enable/empower Glacial Spike).
- **Playstyle:** smash cooldowns (Frozen Orb, Ray of Frost / Comet Storm, Glacial
  Spike) on cooldown, then spend Freezing stacks with Ice Lance and rebuild with
  Frostbolt. A proc-reactive caster, not a fixed loop.

> **Midnight rework note:** the old **Winter's Chill** debuff is now **Freezing**
> (stacking to 20). **Glacial Spike** and **Comet Storm** are now core-build
> buttons. **Frostfire Bolt** (Frostfire hero) and **Splinterstorm** (Spellslinger
> hero) are new hero-tree spells. The seed ability list omitted Icy Veins, Glacial
> Spike, Comet Storm, Frostfire Bolt, Splinterstorm, Shifting Power and the pet
> abilities — all confirmed against `SpellName.csv` and added below.

## Inventory

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| **Frostbolt** | Rotational-builder | Mana | ~2s cast | Core filler. Builds Icicles + Fingers of Frost chance; applies a slow. Replaced by **Frostfire Bolt** under the Frostfire hero tree. |
| **Frostfire Bolt** | Rotational-builder | Mana | ~2s cast | Frostfire hero-tree builder (spell 51779) that replaces Frostbolt; deals Frost+Fire and builds Frostfire empowerment. |
| **Ice Lance** | Rotational-spender | Mana | Instant | Primary Freezing spender; instant when Fingers of Frost is up (deals max-Shatter damage regardless of stacks). Consumes Freezing stacks → Shatter. |
| **Flurry** | Rotational-builder | Mana | ~1.5s cast (instant w/ Brain Freeze) | Applies Freezing stacks; instant + off-cooldown when Brain Freeze procs. Held while Thermal Void window is active (see rotation). |
| **Glacial Spike** | Rotational-spender | Mana | ~2.5s cast | Available at 5 Icicles; big nuke that applies Freezing. Explodes on impact / cleaves under the right talents. Press on cooldown/when charged. |
| **Frozen Orb** | Major cooldown | Mana | 30s CD | Bouncing AoE bolt-storm (~15s), grants Fingers of Frost + Freezing; core burst button pressed on CD. Spellslinger: feeds Splinters and reduces Ray of Frost CD. |
| **Comet Storm** | Major cooldown | Mana | ~30s CD (talent) | Burst AoE that consumes Freezing stacks; Frostfire's primary channel-follow burst and a high-priority button for both hero trees. |
| **Ray of Frost** | Major cooldown | Mana | ~4s channel, 60s CD | Hard-hitting channel that stacks Freezing; **2 charges** with the Hand of Frost apex. Sync with potion/Bloodlust. Frostfire may transform it into Comet Storm. |
| **Icy Veins** | Major cooldown | Mana | ~3min CD | Haste/throughput burst cooldown; tied to the **Thermal Void** window. @verify-ingame — the simc `cds` list does not explicitly cast it; confirm it is still a pressed button (vs. auto/passive) in the Midnight build. |
| **Shifting Power** | Major cooldown / Utility | Mana | ~3–4s channel | Channel that reduces active cooldowns; primarily a Mythic+ cooldown-cycling tool. @verify-ingame usage cadence. |
| **Blizzard** | Rotational-spender (AoE) | Mana | Channel, ground-target | AoE ground effect; strongly favored when the **Freezing Rain** buff is up (instant, buffed). Core AoE button at 3+ targets. |
| **Cone of Cold** | Rotational-spender (AoE) | Mana | Instant, ~12s CD | Frontal AoE + slow; an AoE filler with the Cone of Frost talent. |
| **Ice Nova** | CC / AoE | Mana | Instant, charges (talent) | AoE nova: damage + root; also an AoE filler with the right talents. |
| **Arcane Explosion** | Rotational-spender (AoE) | Mana | Instant | Baseline PBAoE; largely off-meta for Frost (Blizzard/Cone preferred) but available. |
| **Frozen Orb / Splinters** | Passive (Spellslinger) | — | — | Spellslinger Splinter procs fire off casts, add cleave, and reduce Frozen Orb / Ray of Frost cooldowns. |
| **Splinterstorm** | Passive (Spellslinger) | — | — | Spellslinger capstone (spell 443783): pooled Splinters release as a burst-damage storm. |
| **Hand of Frost** | Rotational-spender / Passive | Mana | (apex spec talent) | Apex talent (spell 102593) granting a **2nd Ray of Frost charge** and triggering damage during its cast — pooling flexibility for burst. |
| **Icy Veins (Thermal Void)** | Passive | — | — | Thermal Void extends/empowers the Icy Veins window; Flurry is held while its buff is up. |
| **Counterspell** | Interrupt | Mana | Instant, 24s CD | Spell-school lockout interrupt. |
| **Frost Nova** | CC | Mana | Instant, charges | Roots all nearby enemies; a Freezing/Shatter setup and kite tool. |
| **Freeze** (Water Elemental) | CC / Pet | Mana | Instant, ~25s CD | Water Elemental AoE root (with Summon Water Elemental talented); Shatter/kite setup. |
| **Polymorph** | CC | Mana | ~1.5s cast | Single-target sheep; soft CC / crowd control. |
| **Mass Polymorph** | CC | Mana | Cast (talent) | AoE Polymorph (spell 29963); talent choice. |
| **Ring of Frost** | CC | Mana | Cast, ground (talent) | AoE hold/CC field; talent choice vs Mass Polymorph. |
| **Dragon's Breath / Supernova** | CC | Mana | Instant (class talent choice) | Dragon's Breath = frontal disorient; Supernova = AoE knock-up/damage. Choice node. |
| **Spellsteal** | Dispel / Utility | Mana | ~1.5s cast | Steals a beneficial magic buff from an enemy. |
| **Remove Curse** | Dispel | Mana | Instant | Removes a Curse from a friendly target. |
| **Ice Barrier** | Defensive | Mana | Instant, ~30s CD (25 talented) | Frost damage-absorb shield. |
| **Prismatic Barrier** | Defensive | Mana | Instant, ~25s CD | Magic-damage-absorb shield (reduces magic taken). |
| **Ice Block** | Defensive | Mana | Instant, ~3min CD | Full immunity + clears most debuffs; **Ice Cold** talent trades immunity for heavy damage reduction while still casting. |
| **Cold Snap** | Defensive / Utility | Mana | ~5min CD | Resets Ice Block / Ice Barrier / Frost Nova (and related defensive) cooldowns. |
| **Greater Invisibility** | Defensive | Mana | Instant, ~2min CD | Invisibility + damage reduction + threat drop. |
| **Mirror Image** | Defensive / Major cooldown | Mana | Instant, ~2min CD | Summons 3 images that cast and split threat; adds damage and a survivability buffer. |
| **Alter Time** | Utility / Defensive | Mana | Instant | Snapshots position + health, returns you to them within the window — escape / heal-undo tool. |
| **Blink / Shimmer** | Movement | Mana | Instant, charges | Blink teleport (~20yd); **Shimmer** talent makes it usable while casting with 2 charges. |
| **Ice Floes** | Movement | Mana | Instant, charges | Cast-while-moving enabler (talent). @verify-ingame — confirm presence in the current tree. |
| **Blazing Barrier**/**Mass Barrier** | Defensive | Mana | (talent) | Group barrier utility if talented. @verify-ingame availability for Frost. |
| **Time Warp** | Utility (Bloodlust) | Mana | Instant, ~5min CD | Raid Bloodlust/Heroism-equivalent 30% haste. |
| **Arcane Intellect** | Utility (raid buff) | Mana | Cast | +Intellect raid buff; cast pre-combat. |
| **Mass Invisibility** | Utility | Mana | Cast (talent) | Group invisibility (spell 198158); skip/reset utility. |
| **Slow Fall** | Utility | Mana | Instant | Slows a target's fall. |
| **Summon Water Elemental** | Pet | Mana | Instant (talent) | Summons the Water Elemental pet (choice vs Lonely Winter); provides **Freeze** and passive damage. |
