---
title: Restoration Shaman — Ability Inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/restoration-shaman/playstyle-and-rotation  # tier 3, 12.0.7, 2026-07-11
  - https://www.method.gg/guides/restoration-shaman/talents  # tier 3, 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/restoration-shaman-pve-healing-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
  - https://us.api.blizzard.com/data/wow/talent-tree (Blizzard Game Data API, Tier 1)  # names reconciled vs raw/wago/SpellName.csv
  - knowledge/classes/shaman/restoration/talents.md  # tier 1 game-data tree (12.0.7.67808)
confidence: medium
---

# Restoration Shaman — Ability Inventory (Midnight S1)

## Overview

Restoration is the Shaman healing spec. **Resource: Mana** (kept topped by
**Water Shield** and the **Mana Spring** passive; **Resurgence** returns mana on
Riptide/Chain Heal/Healing Wave/Healing Surge crits). It plays off a short
priority list rather than a fixed rotation — keep totems down and cooldowns
rolling, then fill with direct heals. Two engines drive the toolkit:
**Tidal Waves** (Riptide and Chain Heal charge Tidal Waves, which makes the next
**Healing Wave** cast faster / next **Healing Surge** crit harder) and **Lava
Surge** (procs an instant, free **Lava Burst** for damage weaving).

Two hero trees:
- **Totemic** — recommended for all content in S1. Replaces Healing Rain with
  **Surging Totem** and adds **Stormstream Totem** (apex) plus free totem-cast
  Chain Heals via **Lively Totems**. Totem-centric, mobile, lower APM.
- **Farseer** — cast-time-centric; **Call of the Ancestors** spawns Ancestors
  that mirror your heals, and **Ancestral Swiftness** replaces Nature's
  Swiftness. Weaker in Midnight (lost Whispering Waves); niche/solo pick.

## Inventory

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| **Riptide** | Rotational-builder | Mana | Instant / ~6s CD (2 charges w/ talent) | Instant HoT + upfront heal; core maintenance button, generates a Tidal Waves charge; enables Chain Heal's Flow of the Tides bounce. |
| **Chain Heal** | Rotational-spender | Mana | ~2.5s cast / — | Bouncing group heal; primary AoE/spread heal, jumps to injured allies (extra jumps under Ascendance / Flow of the Tides on Riptide targets). |
| **Healing Wave** | Rotational-spender | Mana | ~2.5s cast / — | Efficient single-target heal; sped up / empowered by a Tidal Waves charge. Main filler. |
| **Healing Surge** | Rotational-spender | Mana | ~1.5–2s cast / — | Fast, expensive emergency single-target heal; consumes Tidal Waves for a bigger crit. @verify-ingame |
| **Healing Stream Totem** | Rotational-builder | Mana | Instant / ~30s CD (2 charges) | Drop-and-forget single-target totem heal; keep on cooldown; feeds Lively Totems / Stormstream procs. |
| **Surging Totem** | Rotational-builder | Mana | Instant / CD (Totemic) | Totemic hero replacement for Healing Rain — an instant totem that heals allies (and damages enemies) in an area; relocate with Totemic Projection. Keep active. @verify-ingame |
| **Healing Rain** | Rotational-spender | Mana | ~2s cast / ~10s CD | Ground-targeted AoE HoT puddle; the non-Totemic AoE anchor (Surging Totem replaces it under Totemic). |
| **Downpour** | Rotational-spender | Mana | Instant / CD | Talented burst-AoE heal on the lowest allies in an area; used before Surging Totem/Healing Rain expires in the Downpour build. @verify-ingame |
| **Unleash Life** | Rotational-builder | Mana | Instant / ~15s CD | Empowers the next Healing Wave / Riptide / Chain Heal by ~100% and shortens its cast; use on cooldown. Tier 4-set can affect two spells. |
| **Nature's Swiftness** | Major cooldown | — | Instant / ~1 min CD | Makes the next heal instant and free; best on Chain Heal. Guarantees a Stormstream Totem proc. |
| **Ancestral Swiftness** | Major cooldown | — | Instant / ~1 min CD | Farseer upgrade to Nature's Swiftness — instant free cast that also spawns an Ancestor and deals damage. Replaces Nature's Swiftness when talented. |
| **Stormstream Totem** | Rotational-spender | — | Instant / proc (apex) | Apex spec talent; empowered Healing Stream Totem, proc'd by Riptide (chance) or Nature's/Ancestral Swiftness (guaranteed); banks up to 2 charges outside normal HST charges. |
| **Spirit Link Totem** | Major cooldown | Mana | Instant / ~3 min CD | Equalizes group health each second and grants ~10–15% damage reduction inside its radius; big Spouting Spirits upfront heal. Raid-stack cooldown. |
| **Healing Tide Totem** | Major cooldown | Mana | Instant / ~3 min CD | Flat raid-wide heal for all allies within 40yd (scales inversely with count, max value at 5+). Totemic's primary raid CD (choice-node vs Ascendance). |
| **Ascendance** | Major cooldown | — | Instant / ~3 min CD | Instant group heal; for the duration Healing Wave always crits + heals a 2nd ally, and Chain Heal gains 3 extra jumps with reduced falloff. Farseer's primary raid CD. |
| **Earth Shield** | Utility / Defensive | Mana | Instant / — (charges) | Tank/target shield; heals on hit and boosts healing taken by the shielded target by ~20%. Keep on the tank when talented. |
| **Lava Burst** | Rotational (damage) | Mana | ~2s cast (instant w/ Lava Surge) / ~8s recharge | Damage weave; guaranteed crit on Flame Shock target; free instant when Lava Surge procs — the main DPS button while healing. |
| **Flame Shock** | Rotational (damage) | Mana | Instant / — | Fire DoT that enables Lava Burst crits and feeds Lava Surge procs; the damage-weave setup. |
| **Lightning Bolt** | Rotational (damage) | Mana | ~2s cast / — | Single-target filler nuke; restores mana via Mana Spring. Used when no one needs healing. |
| **Chain Lightning** | Rotational (damage) | Mana | ~2s cast / — | Multi-target damage nuke; Mana Spring mana return; AoE DPS filler. |
| **Wind Shear** | Interrupt | Mana | Instant / ~12s CD | The Shaman interrupt; short cooldown, no GCD. |
| **Purify Spirit** | Dispel | Mana | Instant / ~8s CD | Restoration's friendly dispel — removes Magic and Curse effects (Curse added by Improved Purify Spirit). |
| **Purge** | Dispel (offensive) | Mana | Instant / — | Removes a beneficial Magic effect from an enemy (Greater Purge choice removes 2). |
| **Astral Shift** | Defensive | — | Instant / ~1.5 min CD | Personal ~40% damage reduction for 8s (talents raise it / add duration). |
| **Spirit Walk** | Movement / Defensive | — | Instant / ~1 min CD | Removes movement-impairing effects and grants a speed burst. |
| **Ghost Wolf** | Movement | — | Instant / — | Travel form; +movement speed, minor toolkit for kiting/positioning. |
| **Spiritwalker's Grace** | Movement / Utility | Mana | Instant / ~2 min CD | Lets you cast while moving for ~15s — the healer mobility cooldown. |
| **Totemic Projection** | Utility | — | Instant / short CD | Relocates your active totems (Surging/Healing Stream/Spirit Link/Healing Tide) to a new spot. @verify-ingame |
| **Heroism** / **Bloodlust** | Major cooldown (raid) | Mana | Instant / ~5 min CD | Raid-wide ~30% haste for 40s; applies Sated/Exhaustion. |
| **Skyfury** | Utility (raid buff) | Mana | Instant / — | Applies the Shaman raid buff (Skyfury) to the group. @verify-ingame |
| **Capacitor Totem** | CC | Mana | Instant / ~1 min CD | Totem that stuns nearby enemies after a short charge-up (AoE stun). |
| **Earthgrab Totem** | CC | Mana | Instant / ~30s CD | Roots enemies in its radius (then slows). |
| **Thunderstorm** | CC / Utility | Mana | Instant / ~30–45s CD | Knocks back nearby enemies and slows them; minor mana return. @verify-ingame |
| **Tremor Totem** | Utility (dispel) | Mana | Instant / ~1 min CD | Breaks/prevents Fear, Charm, and Sleep on allies in radius. |
| **Hex** | CC | Mana | ~1.7s cast / — | Transforms a single humanoid/beast enemy into a critter (incapacitate); breaks on damage. |
| **Wind Rush Totem** | Movement (utility) | Mana | Instant / ~2 min CD | Totem that repeatedly grants passing allies a movement-speed burst. |
| **Earth Elemental** | Pet / Defensive | Mana | Instant / ~5 min CD | Summons a tanky earth elemental to soak/taunt; personal panic-button add. |
| **Ancestral Vision** | Utility | — | Instant / — | Raid utility (battle-rez–style ancestral effect). Uncommon/situational; confirm current behavior. @verify-ingame |
| **Water Shield** | Passive (resource) | — | Instant toggle / — | Self-buff shield that restores mana when you take hits; the resto mana-upkeep buff (keep active). |
| **Mana Spring** | Passive (resource) | — | — | Lightning Bolt / Chain Lightning restore mana to you (and party); damage-weaving is also mana regen. |
| **Tidal Waves** | Passive | — | — | Riptide and Chain Heal grant Tidal Waves charges → next Healing Wave faster / next Healing Surge stronger. The core cast-economy passive. |
| **Lava Surge** | Passive | — | — | Flame Shock ticks can reset Lava Burst and make the next cast instant — enables free damage weaving. |
| **Resurgence** | Passive (resource) | — | — | Crits from your core heals return a chunk of mana; scales with Ascendance's guaranteed crits. |
| **Lively Totems** | Passive (Totemic) | — | — | Your totems (e.g. Healing Stream) periodically cast free Chain Heals — Totemic's passive AoE throughput. |
| **Call of the Ancestors** | Passive (Farseer) | — | — | Casting core heals spawns Ancestors that mirror them (Healing Wave→Healing Wave, Riptide/Unleash Life→Healing Surge, Chain Heal/AoE→Chain Heal). |
