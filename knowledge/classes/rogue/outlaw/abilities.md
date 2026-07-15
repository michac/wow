---
title: Outlaw Rogue — Abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - raw/wago/SpellName.csv (Blizzard game data, Tier 1)   # tier 1, 2026-07-11
  - simc midnight branch profiles/MID1/MID1_Rogue_Outlaw.simc  # tier 1 APL (ability names / usage), 2026-07-11
  - https://www.method.gg/guides/outlaw-rogue  # tier 3, 2026-07-11
  - https://www.icy-veins.com/wow/outlaw-rogue-pve-dps-rotation-cooldowns-abilities  # tier 3, 2026-07-11
confidence: medium
---

# Outlaw Rogue — Abilities (Midnight S1)

## Overview

Outlaw is the swashbuckler melee-DPS Rogue spec: dual-wielding, pistol-toting,
buff-juggling. **Resource system:** **Energy** (0–100+, regenerates passively;
the primary spender fuel) plus **Combo Points** (build 0→6/7, spent by
finishers). Builders (Sinister Strike, Ambush, Pistol Shot) generate combo
points; finishers (Dispatch, Between the Eyes, Roll the Bones, Slice and Dice,
Kidney Shot) spend them.

**Hero trees (Midnight):** **Trickster** (Unseen Blade → Coup de Grace) is the
recommended tree for all Season 1 content; **Fatebound** (Hand of Fate →
Lucky Coin coin-flip passive) is the low-maintenance alternative and is the tree
the default SimulationCraft profile ships. Both slot into the same core spec
shell.

**Playstyle:** keep **Roll the Bones** and **Slice and Dice** rolling, keep
**Adrenaline Rush** and **Blade Flurry** up, then loop builder → finisher while
**Restless Blades** (passive) refunds cooldowns for every combo point spent —
so spending finishers *is* your cooldown-reduction engine. Opportunity procs
turn Pistol Shot into a free empowered builder.

> **Midnight rework flags:** **Roll the Bones** changed from a random-buff slot
> machine to a deterministic **staged buff (stages 1–4)** — see the table.
> **Killing Spree** is now used as a high-combo-point finisher in the APL rather
> than a standalone burst channel. Old Underhanded/Crackshot Adrenaline-Rush-
> extension play was removed. @verify-ingame (exact energy costs and whether
> Killing Spree consumes combo points)

## Inventory

Costs/cooldowns below reflect commonly-cited Midnight values; **energy costs and
some cooldowns are approximate — verify in-game** (Restless Blades and haste
also shorten most listed cooldowns dynamically). @verify-ingame

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Sinister Strike | Rotational-builder | ~45 Energy, +1 CP | Instant / — | Bread-and-butter builder. Can strike twice / proc **Opportunity** (free Pistol Shot); Roll the Bones stage 2 gives it a bonus combo point. |
| Ambush | Rotational-builder | ~50 Energy, +CP | Instant / — | Stealth/Vanish opener; hits harder and gives more CP than Sinister Strike. With **Hidden Opportunity / Audacity** it becomes usable outside stealth on proc. |
| Pistol Shot | Rotational-builder | 25 Energy (free w/ Opportunity), +1 CP | Instant / — | Ranged builder. **Opportunity** procs make it free and empowered; **Fan the Hammer** fires extra shots for extra combo points. |
| Dispatch | Rotational-spender (finisher) | ~35 Energy, spends CP | Instant / — | Primary single-target finisher — highest direct damage per combo point. |
| Between the Eyes | Rotational-spender (finisher) | ~25 Energy, spends CP | Instant / 30s | Ranged finisher; applies **Ruthless Precision** stacking crit/damage buff (each cast its own duration, can stack). Stuns in PvP. **Gravedigger** empowers it. Cooldown cut by Restless Blades. |
| Roll the Bones | Rotational-spender (buff) | spends CP | Instant / — | **Midnight staged rework:** applies/advances a combat buff by stage — **1:** ↑Opportunity proc chance · **2:** Sinister Strike gives +1 CP · **3:** stronger Restless Blades · **4:** ↑Critical Strike. Reroll to climb stages; **Loaded Dice** guarantees a higher roll. @verify-ingame |
| Slice and Dice | Rotational-spender (buff) | spends CP | Instant / — | Self haste buff. Maintained in **Improved Adrenaline Rush** builds (pre-cast in the opener). |
| Keep It Rolling | Major cooldown | — | Instant / ~6min (Restless Blades ≈1min effective) | Extends **all** active Roll the Bones buffs by 30s — used to bank a strong (stage 3+) roll. |
| Adrenaline Rush | Major cooldown | — | Instant / 3min | Signature DPS cooldown: big energy-regen + attack-speed boost (~20s). Cut heavily by Restless Blades (~40% uptime). |
| Blade Flurry | Rotational (cleave) / offensive CD | Energy | Instant / 30s (12s duration) | Echoes a share of single-target damage onto nearby enemies — the core AoE engine. **Deft Maneuvers** lets it also build combo points at 3+ targets. |
| Blade Rush | Movement / rotational CD | — (grants energy) | Instant / ~30s | Charge to target dealing AoE and briefly boosting energy regen; gap-closer used near on-cooldown. Cut by Restless Blades. |
| Killing Spree | Major cooldown (finisher) | high CP | Channel ~2s / ~60s | Teleporting flurry of strikes across targets; APL fires it at high combo points as a finisher-tier burst. @verify-ingame (CP cost) |
| Coup de Grace | Rotational (Trickster) | — | Instant / — | **Trickster** capstone (via Unseen Blade / Disorienting Strikes) — an empowered strike used in both builder and finisher windows when guaranteed. |
| Gravedigger | Passive (spec apex) | — | — | Apex talent: Between the Eyes gains a double-stack chance, Dispatch procs bonus damage at high CP, and a bullet-stack system grants free high-impact Between the Eyes. |
| Restless Blades | Passive (core) | — | — | Each combo point spent by a finisher reduces the cooldown of Adrenaline Rush, Between the Eyes, Blade Flurry, Blade Rush, Killing Spree, Keep It Rolling, Vanish, Sprint and Grappling Hook. |
| Opportunity | Passive (proc) | — | — | Sinister Strike can proc a free, empowered Pistol Shot; central to the builder loop. |
| Preparation | Major cooldown (reset) | — | Instant / CD | Resets the cooldown of Adrenaline Rush, Between the Eyes, Blade Flurry, Blade Rush and Killing Spree — press once all are down. |
| Vanish | Utility / stealth (defensive) | — | Instant / ~2min | Enter Stealth mid-combat, drop threat. Hidden Opportunity builds use it for an extra empowered Ambush. |
| Stealth | Utility (stealth) | — | Instant / — | Out-of-combat stealth; enables openers (Ambush / Cheap Shot / Sap). |
| Crimson Vial | Defensive (self-heal) | ~20 Energy | Instant / 30s | Heal-over-time on self; the spammable panic heal. |
| Evasion | Defensive | — | Instant / ~2min | Large dodge boost vs melee/ranged for its duration. |
| Feint | Defensive | 35 Energy | Instant / — | Reduces AoE damage taken (and threat); pressed pre-emptively for big raid hits. |
| Cloak of Shadows | Defensive (magic immunity) | — | Instant / ~2min | Removes and briefly grants immunity to magic effects/debuffs. |
| Thistle Tea | Defensive / resource | — | Instant / (charges) | Restores a chunk of energy and boosts Mastery; energy-panic + small throughput. |
| Kick | Interrupt | — | Instant / 15s | Melee interrupt. |
| Kidney Shot | CC (stun) | spends CP | Instant / 20s | Combo-point finisher stun. |
| Cheap Shot | CC (stun) | 40 Energy, +CP | Instant / — | Stealth-opener stun. |
| Gouge | CC (incapacitate) | ~25 Energy | Instant / 15s | Frontal incapacitate (choice node with Airborne Irritant). |
| Blind | CC (disorient) | — | Instant / ~2min | Disorients the target. |
| Sap | CC (out-of-combat) | — | Instant / — | Incapacitate a non-combat target from stealth. |
| Sprint | Movement | — | Instant / ~1–2min | Burst of movement speed. |
| Grappling Hook | Movement | — | Instant / CD | Pull yourself to a location; core Rogue mobility. |
| Shroud of Concealment | Utility (group stealth) | — | Instant / CD | Cloaks the party/raid in stealth for skips. |
| Tricks of the Trade | Utility (threat) | — | Instant / CD | Redirects your threat to a party member (choice node with Blackjack). |
| Distract | Utility | — | Instant / 30s | Diverts NPC attention to a location. |
| Shiv | Utility / dispel | ~20 Energy | Instant / CD | Applies nonlethal poison effect; can strip enrages / enable poison utility. |
| Poisons | Passive / utility | — | — | Apply weapon poisons out of combat: **lethal** (Deadly / Instant / Wound) for damage, **nonlethal** (Numbing / Atrophic / Crippling) for control. |
