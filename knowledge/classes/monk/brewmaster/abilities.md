---
title: Brewmaster Monk — Ability Inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight branch profiles/MID1/MID1_Monk_Brewmaster.simc  # tier 1 APL + talent string, WoW 12.0.7
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Monk_Brewmaster.simc  # tier 1, fetched 2026-07-11
  - https://www.wowhead.com/db2 SpellName @ 12.0.7  # tier 1 name reconciliation (raw/wago/SpellName.csv)
  - https://www.icy-veins.com/wow/brewmaster-monk-pve-tank-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
  - https://www.method.gg/guides/brewmaster-monk/playstyle-and-rotation  # tier 3, upd. 2026-06-17
confidence: medium
---

# Brewmaster Monk — Ability Inventory (Midnight S1)

## Overview

Brewmaster is Monk's tank spec: a dodge/active-mitigation bruiser that turns a
chunk of every hit into a delayed damage-over-time pool (**Stagger**) and then
proactively drains that pool with **Brews**. It is the only WoW tank that
tanks primarily by *deferring* damage and cleaning it up on its own schedule.

- **Resources:** **Energy** (0–100, steady regen) fuels the offensive/threat
  rotation — Keg Smash, Tiger Palm, Spinning Crane Kick, Expel Harm. **Mana**
  pays for the healing/dispel utility (Vivify, Soothing Mist, Detox). Brewmaster
  does **not** use Chi (that is Windwalker). **Brews** are their own charge/cooldown
  pool, off the global cooldown.
- **Stagger** (passive) + **Shuffle** (a buff kept up by Keg Smash / Blackout
  Kick that boosts the % of damage staggered) are the survival backbone;
  **Purifying Brew** is the button that turns Stagger into mitigation.
- **Midnight simplification (12.0.7):** Brewmaster lost **Rising Sun Kick** and
  **Weapons of Order** from the TWW kit. The spec now revolves around the apex
  talent **Bring Me Another** — Brews generate an **Empty Barrel** that supercharges
  the next **Keg Smash** — and, for Master of Harmony, the **Aspect of Harmony**
  accumulator that feeds a big Celestial Brew absorb.
- **Hero trees:** **Shado-Pan** (Flurry Strikes / physical burst, M+-leaning) and
  **Master of Harmony** (Aspect of Harmony vitality + a second Celestial Brew
  charge, raid/single-target-leaning). Both viable in all content.

## Inventory

Cast/CD values are for the live 12.0.7 baseline and shift with talents; entries
marked @verify-ingame are approximate and should be confirmed on a live character.

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Tiger Palm | Rotational-builder | ~25 Energy | Instant / — | Cheap Energy-spender and filler; consumes the **Blackout Combo** buff (empowers it) and helps keep Energy from capping. @verify-ingame (energy cost) |
| Keg Smash | Rotational-builder | ~40 Energy | Instant / ~8s (chargeable) | **Cornerstone.** AoE hit that applies the Keg Smash debuff (armor/vuln), reduces Brew cooldowns, generates **Shuffle**, and is the payoff for the **Empty Barrel** (Bring Me Another). Cast on cooldown — it drives threat, Brew CDR, and Shuffle. |
| Blackout Kick | Rotational-builder | None | Instant / ~3s (CDR from other casts) | Free strike that extends **Shuffle** and procs **Blackout Combo** (if talented). Woven between Keg Smash casts. |
| Breath of Fire | Rotational-spender | None | Instant / ~15s | Fire cone applying the Breath of Fire DoT (a damage-taken reduction debuff) and, with **Charred Passions**, a self-damage-amp/refresh loop via Blackout Kick. @verify-ingame (CD) |
| Spinning Crane Kick | Rotational-spender (AoE) | ~25 Energy | ~1.5s channel / — | Spin AoE for gathering/Charred-Passions cleave; used situationally, **not** on a strict priority — its own defensive value is minimal. |
| Rushing Jade Wind | Rotational-spender (AoE) | Energy | Instant / short (buff) | Whirling AoE buff; **choice node vs Special Delivery**. Feeds Walk with the Ox procs. Refresh before it drops. |
| Exploding Keg | Rotational-spender / minor CD | None | Instant / ~1min | Throws a keg: AoE fire pool + an accuracy debuff on enemies inside. Used when Keg Smash is on cooldown / in AoE windows. @verify-ingame (CD) |
| Chi Burst | Rotational (Master of Harmony) / Utility | None | ~1s cast / ~30s (choice) | Line-AoE damage + party heal. In the Master of Harmony tree it is pulled high in the rotation; for Shado-Pan it is a low-priority filler. Choice node vs **Chi Wave**. |
| Purifying Brew | Defensive (Brew) | None (Brew) | Off-GCD / 2 charges, ~15–20s recharge | Instantly clears **50% of the current Stagger pool**. The signature active mitigation — best used soon after a big hit lands. @verify-ingame (recharge) |
| Celestial Brew | Defensive (Brew) | None (Brew) | Off-GCD / ~60s (chargeable via Light Brewing) | Absorb shield scaled by recent Purifying (Purified Chi). **Choice node vs Celestial Infusion.** |
| Celestial Infusion | Defensive (Brew) | None (Brew) | Off-GCD / ~60s | Celestial Brew variant that spreads its absorb more smoothly ("easier to heal"); the common Master-of-Harmony/M+ pick. In MoH it is also the **Aspect of Harmony spender** trigger. |
| Black Ox Brew | Major cooldown (Brew) | None (Brew) | Off-GCD / ~2min | Instantly refills **Purifying Brew** charges and restores Energy — a burst-mitigation/reset button. @verify-ingame (CD) |
| Fortifying Brew | Major defensive | None (Brew) | Off-GCD / ~6–7min (talented) | +max health, reduced damage taken, increased Stagger for the duration. Big personal cooldown. **Fortifying Brew: Determination** talent strengthens/adjusts it. @verify-ingame (CD) |
| Invoke Niuzao, the Black Ox | Major cooldown / Pet | None | Instant / ~3min | Summons Niuzao, who Stomps for AoE damage and mirrors a portion of your purified Stagger back as damage — a coupled damage + mitigation cooldown. @verify-ingame (CD) |
| Bring Me Another | Passive / apex (rotational payoff) | None | Passive | **Apex talent.** Consuming a Brew has a chance to grant an **Empty Barrel** (max 1). Your next **Keg Smash** throws it for bonus physical damage; higher ranks reset Keg Smash's cooldown, cut its Energy cost, and hand nearby allies a **Refreshing Drink** heal. |
| Empty the Cellar | Passive / minor active | None | (per talent) | Reduces Brew cooldowns / feeds extra brew value; appears as its own action in the APL. @verify-ingame |
| Aspect of Harmony | Passive (Master of Harmony) | None | Passive | Accumulates a pool from damage/healing done, then discharges as a large absorb + damage tick when you spend it (via Celestial Brew/Infusion). MoH's signature sustain engine. |
| Touch of Death | Cooldown (execute) | None | Instant / ~2min (Improved reduces) | Large fixed/percentage strike, usable as an execute. @verify-ingame (CD) |
| Expel Harm | Defensive / self-heal | ~15 Energy | Instant / ~15s | Draws in **Gift of the Ox** healing orbs, healing you and dealing a bit of damage. Cheap self-sustain woven into downtime. @verify-ingame (cost/CD) |
| Vivify | Utility (heal) | Mana | ~1.5s cast | Direct heal on target (and Renewing-Mist targets); off-heal for self/allies. |
| Soothing Mist | Utility (heal) | Mana | Channel | Channeled heal; enables instant Vivify/Enveloping during the channel. |
| Detox | Dispel | Mana | Instant / ~8s | Removes Poison and Disease (Magic via talent) from a friendly target. @verify-ingame (dispel types) |
| Provoke | Utility (taunt) | None | Instant / 8s | Single-target taunt; can also be cast on the **Black Ox Statue** to taunt everything near it. |
| Spear Hand Strike | Interrupt | None | Instant / 15s | Melee kick interrupt + short school lockout. |
| Leg Sweep | CC | None | Instant / ~1min | AoE stun around the Monk. @verify-ingame (CD) |
| Paralysis | CC | Energy | Instant / ~45s | Single-target incapacitate (breaks on damage). @verify-ingame (CD/cost) |
| Ring of Peace | CC / Utility | None | Instant / ~45s | Zone that knocks back and bars enemies from entering. **Choice vs Song of Chi-Ji.** @verify-ingame (CD) |
| Disable | CC / Utility | Energy | Instant / — | Slows the target; re-cast roots a slowed target. **Choice vs Crashing Momentum.** |
| Roll | Movement | None | Instant / 2 charges (~20s) | Short dash in the movement direction. **Choice vs Chi Torpedo** (Chi Torpedo also does damage/heal along the path). |
| Chi Torpedo | Movement | None | Instant / 2 charges | Roll replacement: longer travel + minor damage/heal, small post-move speed buff. |
| Tiger's Lust | Movement | None | Instant / ~30s | Removes roots/snares and grants a short speed burst to self or an ally. @verify-ingame (CD) |
| Transcendence | Utility | None | Instant / — | Places a stationary spirit copy at your location. |
| Transcendence: Transfer | Movement / Utility | None | Instant / ~10–25s | Swaps places with your Transcendence spirit — repositioning/escape tool. @verify-ingame (CD) |
| Zen Flight | Utility (movement) | Mana | Channel (out of combat) | Slow-fall/flight cantrip; out-of-combat travel only. |
| Crackling Jade Lightning | Utility (ranged) | Energy/Mana | Channel | Ranged channel for pulling or poking untankable/ranged targets; knocks back attackers with Lightning Reflexes-type interactions per talent. |
| Summon Black Ox Statue | Utility / Pet | None | Instant | Drops a statue that can be **Provoke**-taunted to AoE-taunt and periodically heals via Gift of the Ox. |
| Zen Meditation | Defensive (major) | None | ~5s channel / ~5min | Channel that massively reduces damage taken (breaks on melee/move). Emergency mitigation. @verify-ingame (CD/values) |
| Diffuse Magic | Defensive (magic) | None | Instant / ~90s | Reduces magic damage taken and can bounce harmful magic effects back. Class-tree talent. @verify-ingame (CD) |
| Nimble Brew | Defensive (PvP) | None (Brew) | Off-GCD / (PvP talent) | Clears and reduces incoming loss-of-control effects. PvP talent. |
| Double Barrel | Offensive (PvP) | None | (PvP talent) | Empowers your next Keg Smash to also disorient targets hit. PvP talent. |

> Notes:
> - **Stagger** and **Shuffle** are passive/mechanic buffs, not cast buttons —
>   Shuffle is *maintained* by Keg Smash and Blackout Kick; Stagger is always on.
> - The seed checklist's **"Res"** does not map to a real Brewmaster spell —
>   Monk has no unique battle/out-of-combat resurrect. Treated as a seed
>   placeholder (see gaps), not an ability.
