---
title: Elemental Shaman — Ability Inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - raw/wago/SpellName.csv (Blizzard game data, Tier 1)   # tier 1, 2026-07-11
  - simc midnight profiles/MID1/MID1_Shaman_Elemental.simc   # tier 1, 2026-07-11
  - https://www.method.gg/guides/elemental-shaman/playstyle-and-rotation   # tier 3, upd 2026-06-16
  - https://www.icy-veins.com/wow/elemental-shaman-pve-dps-rotation-cooldowns-abilities   # tier 3, 12.0.7
confidence: high
---

# Elemental Shaman — abilities (Midnight S1, 12.0.7)

## Overview

Elemental is a ranged spell-caster that builds and spends **Maelstrom** (a
0–100 resource, raised by talents such as Swelling Maelstrom). Builders —
**Lightning Bolt**, **Chain Lightning**, **Lava Burst**, **Frost Shock** —
generate Maelstrom; spenders — **Earth Shock**, **Earthquake**, **Elemental
Blast** — dump it. **Flame Shock** is a maintained DoT that fuels **Lava
Surge** procs (free instant Lava Bursts) and enables **Lava Burst**. Mastery
(Elemental Overload) gives spells a chance to fire a second, free ~75%-damage
copy — the whole kit is tuned around maximizing overloads.

**Two hero trees:**
- **Stormbringer** — the lightning/single-target tree. Spending Maelstrom
  charges **Tempest**, a hard-hitting overloading nuke that supercharges the
  next Lightning Bolt (stacks to 2). Applies **Lightning Rod**. Default for
  raid / low target counts.
- **Farseer** — the summoning/cleave tree. **Call of the Ancestors** summons
  ancestor spirits (via Stormkeeper / Ancestral Swiftness) that copy your
  casts. Stronger in 2–3 target cleave and Mythic+.

## Ability inventory

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| **Lightning Bolt** | Rotational-builder | Generates Maelstrom | ~2s cast | Primary single-target filler; generates Maelstrom, can Overload. Supercharged by Tempest / instant under Stormkeeper. |
| **Chain Lightning** | Rotational-builder (AoE) | Generates Maelstrom/target | ~2s cast | AoE builder, bounces between targets; the AoE replacement for Lightning Bolt (worth it at ~3 targets Stormbringer / 2 Farseer). |
| **Lava Burst** | Rotational-builder | Generates Maelstrom | 2 charges / ~8s recharge | Guaranteed crit vs a Flame Shocked target. Instant and free when **Lava Surge** is up — the rule is "never hardcast Lava Burst, cast only on Lava Surge." |
| **Flame Shock** | Rotational-builder (DoT) | Generates Maelstrom | instant, 6s CD | Maintained fire DoT; each tick can proc **Lava Surge**. Enables Lava Burst crits. Refresh at ≤ ~6s / pandemic. |
| **Voltaic Blaze** | Rotational-builder (AoE Flame Shock) | Generates Maelstrom | instant (proc-gated) | Talent (Voltaic Blaze). Instant nature/fire hit that also applies Flame Shock to up to 5 nearby targets — the AoE Flame Shock spreader. @verify-ingame |
| **Frost Shock** | Rotational-builder / movement filler | Generates Maelstrom | instant, no CD | Instant filler; usable while moving. Slows the target. Low priority — a movement/overcap-dump button. |
| **Earth Shock** | Rotational-spender | Spends Maelstrom | instant | Single-target Maelstrom dump (choice node vs Elemental Blast). Instant, so the mobility spender. |
| **Elemental Blast** | Rotational-spender | Spends Maelstrom | ~2s cast | Alternative spender (choice vs Earth Shock): higher damage + grants a random secondary-stat buff, but has a cast time and higher cost. |
| **Earthquake** | Rotational-spender (AoE) | Spends Maelstrom | instant (ground-target) | AoE Maelstrom dump; soft-caps ~20 targets. The AoE replacement for Earth Shock/Elemental Blast. |
| **Tempest** | Rotational-spender (proc) | Charged by spending Maelstrom | instant | **Stormbringer** signature. Charges up after spending Maelstrom; overloads hard and supercharges the next Lightning Bolt/Chain Lightning (stacks to 2). Applies Lightning Rod. |
| **Stormkeeper** | Major cooldown | — | instant, ~1min | Next 2 Lightning Bolts / Chain Lightnings are instant and empowered. On Farseer also summons an ancestor; shorter CD / stacks on Stormbringer. Pair with Ascendance. |
| **Ascendance** | Major cooldown | — | instant, ~3min (First Ascendant/Preeminence adjust) | Burst window: Lava Burst gains charges / no cooldown and overload damage is boosted. Always cast **after** Stormkeeper. Sync with Heroism + trinkets. |
| **Ancestral Swiftness** | Major cooldown / Utility | — | instant, ~1.5min | **Farseer** active (replaces Nature's Swiftness when talented). Makes the next spell instant, grants haste, and summons an ancestor. Use on cooldown; follow with a cast-time spell. |
| **Nature's Swiftness** | Utility | — | instant, ~1min | Class talent (used when NOT running Ancestral Swiftness): next Nature/Frost spell is instant and empowered. Often spent on an instant Chain Heal / Lava Burst / hardcast filler. |
| **Fire Elemental** | Major cooldown / Pet | — | instant, ~2.5min | Summons a Fire Elemental (Call of Fire talent) for a burst-damage window; with Primal Elementalist it is directly controllable and buffs you. |
| **Storm Elemental** | Major cooldown / Pet | — | instant, ~2.5min | Alternative to Fire Elemental (via talent choice): a lightning burst-damage elemental with the Wind Gust ramp. |
| **Wind Shear** | Interrupt | — | instant, ~12s | The interrupt — a short-cooldown, no-GCD spell kick. |
| **Astral Shift** | Defensive | — | instant, ~1.5min | −40% damage taken for ~8s (Nature's Guardian etc. improve). Core personal defensive. |
| **Earth Elemental** | Defensive / Pet | — | instant, ~5min | Summons a tanky Earth Elemental to taunt/soak; a threat/defensive tool, strong solo/delve. |
| **Skyfury** | Utility (raid buff) | — | instant, 1hr buff | The Shaman group buff: empowers you and party/raid members' attack and spell power. Cast pre-pull. @verify-ingame |
| **Heroism** | Major cooldown (party) | — | instant, ~5min (10min exhaustion) | Bloodlust/Heroism — party/raid +30% haste for 40s. Sync with Ascendance. (Alliance = Heroism, Horde = Bloodlust.) |
| **Healing Surge** | Utility (heal) | Mana | ~1.5–2s cast | Emergency direct self/ally heal. |
| **Chain Heal** | Utility (heal) | Mana | ~2.5s cast | Bouncing group heal — off-heal utility. |
| **Healing Stream Totem** | Utility (heal) | Mana | instant, ~30s | Drops a totem that trickle-heals the lowest-health nearby ally. |
| **Earth Shield** | Defensive / Utility | Mana | instant, ~1min | Places a charge-based shield on self (Elemental Orbit) or an ally that heals on hit and reduces damage. |
| **Spiritwalker's Grace** | Movement | — | instant, ~1min | Lets you cast normally-stationary spells while moving for ~15s. The caster-mobility button. |
| **Ghost Wolf** | Movement | — | instant | Travel form; +movement speed, quick in/out. |
| **Spirit Walk** | Movement | — | instant, ~1min | Removes movement-impairing effects + speed burst (choice vs Gust of Wind). |
| **Wind Rush Totem** | Movement (group) | — | instant, ~2min | Totem that grants passing allies a movement-speed burst — group mobility. |
| **Capacitor Totem** | CC | — | instant, ~1min | Totem that charges up then AoE-stuns nearby enemies. |
| **Earthgrab Totem** | CC | — | instant, ~1min | Totem roots nearby enemies, then slows them. |
| **Thunderstorm** | CC / Defensive | — | instant, ~30s | Knocks back nearby enemies and slows them; Elemental signature control/peel. |
| **Hex** | CC | Mana | ~1.5s cast, ~30s | Transforms a humanoid/beast enemy into a frog (incapacitate). |
| **Tremor Totem** | Utility (CC break) | — | instant, ~1min | Totem that removes and prevents Fear/Sleep/Charm for nearby allies (choice vs Poison Cleansing Totem). |
| **Purge** | Dispel (offensive) | Mana | instant | Removes a beneficial Magic effect from an enemy (choice vs Greater Purge). |
| **Cleanse Spirit** | Dispel | Mana | instant, ~8s | Removes a Curse from a friendly target. |
| **Totemic Projection** | Utility | — | instant, ~10s | Relocates your active totems to a targeted location. |
| **Ancestral Spirit** | Utility (battle rez) | Mana | ~10s cast | Combat resurrection of a fallen ally (out-of-combat res too). |
| **Lightning Shield** | Passive/buff (maintain) | — | instant | Self-buff that damages melee attackers; kept up (precombat). |
| **Flametongue Weapon** | Utility (imbue) | — | instant | Weapon imbue (talent); maintained buff, applied precombat. |
| **Thunderstrike Ward** | Defensive/buff (imbue) | — | instant | Talent weapon enchant / ward that retaliates with lightning; applied precombat (choice vs Elemental Resonance). |
