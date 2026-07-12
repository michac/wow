---
title: Windwalker Monk — Ability Inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/windwalker-monk/playstyle-and-rotation  # tier 3, 2026-07-11 (upd. 2026-06-16)
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Monk_Windwalker.simc  # tier 1 APL, 2026-07-11
  - raw/wago/SpellName.csv  # tier 1 game data, name reconciliation, 2026-07-11
  - https://www.icy-veins.com/wow/windwalker-monk-pve-dps-rotation-cooldowns-abilities  # tier 3, 2026-07-11 (12.0.7)
confidence: high
---

# Windwalker Monk — Ability Inventory (Midnight S1)

## Overview

Windwalker is the melee-DPS Monk spec. **Resource system: Energy + Chi.** Energy
(0–100/130) regenerates passively and fuels *builders*; those builders generate
**Chi** (0–5/6), the secondary resource that *spenders* consume. Two build-around
passives shape the flow: **Combo Strikes** (Mastery — never use the same ability
twice in a row, or you lose a large damage buff; `combo_strike` gates nearly every
APL line) and **Hit Combo** (talent — consecutive *distinct* abilities stack an
escalating damage buff). The rotation is a **priority list, not a fixed sequence** —
weave builders and spenders so you neither cap Energy/Chi nor break Combo Strikes.

**Hero trees (Midnight):**
- **Conduit of the Celestials** — adds **Celestial Conduit** (a big channeled
  nuke) and **Heart of the Jade Serpent** (a proc that sharply accelerates the
  rotation and speeds Fists of Fury). The current top pick for most content.
- **Shado-Pan** — builds around **Flurry Strikes**, accumulating charges from
  spending resources and unleashing them; leans into a faster, more frequent
  **Zenith** cadence via Efficient Training.

**Primary cooldown:** **Zenith** (Midnight's flexible burst window; it replaced the
old Storm, Earth, and Fire / Serenity capstone) plus **Invoke Xuen, the White
Tiger** (the summoned tiger). Defensives are thin: only **Fortifying Brew** and
**Touch of Karma**.

## Inventory

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Tiger Palm | Rotational-builder | ~25 Energy, **+2 Chi** (more with Ascension) | Instant / — | Core Chi builder / Combo-Strikes filler. Lowest-priority "don't cap Energy, top up Chi" button. |
| Blackout Kick | Rotational-spender | 1 Chi (often free) | Instant / — | Cheap spender; **Combo Breaker** and the *Blackout Kick!* proc make it free and reset other cooldowns. High press-count filler-spender. |
| Rising Sun Kick | Rotational-spender | 2 Chi | Instant / ~10s (resets/CDR via procs) | High-damage kick, key with **Xuen's Battlegear** (crit + cooldown reduction on it). Priority spender. |
| Fists of Fury | Rotational-spender / cleave | 3 Chi | ~4s channel (hasted) / ~24s | Channeled front-cone burst; primary Chi dump and a major share of damage. Cooldown sped up by Heart of the Jade Serpent. |
| Strike of the Windlord | Rotational-spender | 2 Chi | Instant / ~40s | Twin fist strike hitting all in front; choice-node vs Whirling Dragon Punch. High-priority when talented. @verify-ingame (Chi cost/CD) |
| Whirling Dragon Punch | Rotational-spender / AoE | — | Instant / ~24s | Only usable while **both** Fists of Fury and Rising Sun Kick are on cooldown; spinning AoE. Choice-node vs Strike of the Windlord. |
| Spinning Crane Kick | Rotational-spender / AoE | 2 Chi (free w/ Dance of Chi-Ji) | ~1.5s channel / — | AoE spinning attack; **Dance of Chi-Ji** procs make it free and hard-hitting. Main multi-target spender. |
| Rushing Wind Kick | Rotational-spender | — | Instant / — | Talent-granted strike woven high in the priority when talented; interacts with Strike of the Windlord / Thunderfist. @verify-ingame (exact mechanic) |
| Slicing Winds | Rotational-spender / Movement | — | ~1s channel / ~30s | Talent; dashes forward dealing AoE. Doubles as a gap-closer but **stops at ledges** (won't cross gaps). @verify-ingame |
| Zenith | Major cooldown | — | Instant / ~90s (reducible) | The flagship DPS window — buffs output / spawns celestial pressure for its duration. Cooldown shrinks via Spiritual Focus (Conduit) or Efficient Training (Shado-Pan). @verify-ingame (exact effect/CD) |
| Zenith Stomp | Rotational-spender | Chi (spends into Zenith) | Instant / — | Talent (**Zenith Stomp**); an extra spender used inside a Zenith window to convert spare Chi into damage. @verify-ingame |
| Celestial Conduit | Major cooldown | — | ~4s channel / ~90s | **Conduit of the Celestials** hero ability; channeled nuke cast when Heart of the Jade Serpent is down. Can be cancelled early. @verify-ingame (CD) |
| Invoke Xuen, the White Tiger | Major cooldown / Pet | — | Instant / ~120s | Summons Xuen to attack your target for the duration; the burst anchor synced with potions/racials/trinkets. |
| Touch of Death | Rotational-spender (execute) | — | Instant / ~1.5–2 min | Instant large flat/execute hit; **Improved Touch of Death** lets it hit any target. Woven on cooldown. @verify-ingame (CD) |
| Tigereye Brew | Major cooldown | — | Instant / — | Spec capstone; stacks (**+1% crit per stack**, built from Chi spent) then consumed for a burst buff window. @verify-ingame |
| Flying Serpent Kick | Movement | ~Energy | Instant / ~25s | Launch forward through the air, then land with an AoE slow. Primary movement/gap-closer; can cross gaps. |
| Roll | Movement | — | Instant / 2 charges, ~20s | Short dash; baseline mobility. **Chi Torpedo** is the talent replacement (rolls farther, +movement speed buff). |
| Tiger's Lust | Movement / Utility | — | Instant / ~30s | Removes roots/snares and grants a burst of movement speed to you or an ally. |
| Transcendence | Utility / Movement | — | Instant / — | Places a spirit; recast to swap. Setup for Transcendence: Transfer. |
| Transcendence: Transfer | Movement / Utility | — | Instant / ~10–25s | Teleports you to your placed Transcendence spirit — a mobility/escape/skip tool. |
| Crackling Jade Lightning | Utility / ranged | Energy | Channel / — | Ranged channeled Nature damage; used to pull or as a ranged option (knockback with Combat Wisdom / talents). |
| Spear Hand Strike | Interrupt | — | Instant / ~15s | Melee interrupt + short school lockout. |
| Leg Sweep | CC | — | Instant / ~60s | Short AoE stun around you. |
| Paralysis | CC | Energy | Instant / ~45s | Single-target incapacitate (breaks on damage). |
| Ring of Peace | CC / Utility | — | Instant / ~45s | Knocks enemies out of a zone; choice-node vs **Song of Chi-Ji** (a targeted disorient). |
| Disable | CC / Utility | Chi/Energy | Instant / — | Slow that roots on reapplication; choice-node vs Crashing Momentum. |
| Provoke | Utility (taunt) | — | Instant / ~8s | Taunt; also redirects Xuen. Niche for DPS (add pickup). |
| Fortifying Brew | Defensive | — | Instant / ~6 min | +max health and damage reduction for the duration; core panic button. |
| Touch of Karma | Defensive / Utility | — | Instant / ~90s | Redirects a chunk of incoming damage and deals it back to the target — usable defensively (absorb a spike / stall for heals) **or** offensively as a damage cooldown. |
| Diffuse Magic | Defensive (magic) | — | Instant / ~90s | Magic damage reduction + returns debuffs to caster. Class talent. @verify-ingame |
| Dampen Harm | Defensive | — | Instant / ~120s | Reduces large incoming hits (percentage of health). Talent if picked. @verify-ingame (talented) |
| Detox | Dispel | Energy | Instant / ~8s | Removes Poison and Disease effects from a friendly target. |
| Vivify | Utility (heal) | Mana | ~1.5s cast (instant w/ proc) | Direct heal; **Vivacious Vivification** can make it instant. Self/ally topping. |
| Soothing Mist | Utility (heal) | Mana | Channel / — | Channeled heal; enables instant Vivify while active. Rarely used by WW. |
| Resuscitate | Utility (rez) | Mana | ~10s cast / — | Out-of-combat resurrection of a dead player. @verify-ingame (name) |
| Zen Flight | Movement / travel | — | — | Slow-fall / flight travel spell (out of combat). |
| Nimble Brew | Utility (PvP) | — | Instant / — | **PvP talent** — removes and reduces incoming loss-of-control effects. @verify-ingame |
| Double Barrel | Utility (PvP) | — | — | **PvP talent** — empowers Fists of Fury (stun). @verify-ingame |
| Reverse Magic | Dispel / Utility (PvP) | — | Instant / — | **PvP talent** — sends the group's harmful magic auras back to casters. @verify-ingame |
| Combo Strikes (Mastery) | Passive | — | — | Repeating an ability loses a large damage buff; every APL spender/builder is gated on `combo_strike` (alternate abilities). |
| Hit Combo | Passive | — | — | Talent; consecutive **distinct** abilities stack a growing damage buff (dropped if you repeat). |
| Combo Breaker | Passive (proc) | — | — | Tiger Palm can proc a **free Blackout Kick** (*Blackout Kick!*); high-value to consume promptly. |
| Dance of Chi-Ji | Passive (proc) | — | — | Talent; procs a free, empowered Spinning Crane Kick (stacks to 2). |
| Heart of the Jade Serpent | Passive (proc) | — | — | **Conduit** hero passive; a proc that accelerates the whole rotation and speeds Fists of Fury channels — the tree's defining effect. |
| Flurry Strikes | Passive | — | — | **Shado-Pan** hero mechanic; resource spending accumulates charges that unleash extra strikes. |
| Xuen's Battlegear | Passive | — | — | Talent; raises Rising Sun Kick crit and grants big cooldown reduction on it. |
