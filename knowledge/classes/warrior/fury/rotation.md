---
title: Fury Warrior — Rotation (Midnight Season 1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight branch profiles/MID1/MID1_Warrior_Fury.simc  # tier 1 APL, 2026-07-11 (talents=CgEAAAAA...)
  - https://www.method.gg/guides/fury-warrior/playstyle-and-rotation  # tier 3, 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/fury-warrior-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
  - knowledge/classes/warrior/fury/talents.md  # sibling tier-1 talent inventory
confidence: high
---

# Fury Warrior — Rotation (Midnight S1)

Distilled from the SimulationCraft default APL (Tier 1), corroborated by
method.gg and Icy Veins (both 12.0.7). The APL branches by **hero tree** and
**enemy count**: `slayer` / `slayer_aoe` for Slayer, `thane` / `thane_aoe` for
Mountain Thane. Both are S1-viable (see `builds.md`) — the ordering below shows
each.

**The core loop.** Generate Rage → spend it on **Rampage** to keep **Enrage**
up → hammer your empowered strikes while Enraged (which builds more Rage).
Two hard rules underpin everything: **never let Enrage fall off** for a filler
you could have delayed, and **don't overcap Rage** (~100, or 120 with
Overwhelming Rage). Rampage is deliberately delayed slightly past its 80-Rage
cost to pool — but only while Enrage is safely up.

## Pre-combat

- `berserker_stance` on (APL precombat toggle).
- `snapshot_stats`; set up trinket variables.
- Open with **Charge** into the pack (`charge,if=time<=0.5|movement.distance>5`),
  then straight into cooldowns.

## Cooldown rules

- **Recklessness (+ Avatar if talented) on cooldown**, unless a damage-amp or an
  AoE moment is coming in the next ~10s — then hold for it. Off the GCD.
- **Potion / racials** with Recklessness up (`potion,if=...buff.recklessness.up`;
  Berserking/Blood Fury/etc. gated on Recklessness). `invoke_external_buff`
  (Power Infusion) wants Recklessness up with >15s left, or the execute phase, or
  the last 25s of the fight.
- **Trinkets** sync to the Recklessness window (the APL's trinket list gates the
  on-use pieces on `buff.recklessness.up`; Algeth'ar Puzzle Box fires ~2s before
  Recklessness comes up).
- **Bladestorm** (Slayer): use Enraged and preferably after Rampage; hold ≤15s to
  line up with Recklessness (`buff.recklessness.up|cooldown.recklessness.remains>30`).
- **Pummel** interrupt is checked every action (`pummel,if=target.debuff.casting.react`).
- **Champion's Spear** (if talented) fits into the burst window.

## Single target — Slayer (`actions.slayer`)

1. **Recklessness** → **Avatar** (burst window, off GCD)
2. **Rampage** if Enrage is about to drop (`buff.enrage.remains<gcd`) **or** Rage ≥ 100
3. **Bladestorm** if Enraged (`buff.enrage.up&talent.deft_experience` or
   `buff.enrage.remains>1`) and lined up with Recklessness
4. **Odyn's Fury** (triggers Enrage; press early in its window)
5. **Execute** (in execute range / on Sudden Death)
6. **Bloodbath** (empowered Bloodthirst during Recklessness window)
7. **Rampage** if Recklessness is up
8. **Crushing Blow** (empowered Raging Blow during Recklessness window)
9. **Bloodthirst**
10. **Rampage**
11. **Wrecking Throw** (if talented)
12. **Rend** if `dot.rend.duration<6` (refresh the bleed)
13. **Raging Blow**
14. **Whirlwind** (filler)
15. **Storm Bolt** if Bladestorm is up (weave during the channel)

## Single target — Mountain Thane (`actions.thane`)

1. **Odyn's Fury** (top of the Thane list — Enrage + burst)
2. **Recklessness** → **Avatar**
3. **Rampage** if Enrage about to drop or Rage ≥ 100
4. **Thunder Blast** at 2 stacks
5. **Bloodbath**
6. **Rampage** if Recklessness up
7. **Thunder Blast** if Avatar is up
8. **Bloodthirst**
9. **Execute**
10. **Crushing Blow**
11. **Thunder Blast**
12. **Rampage**
13. **Thunder Clap** if Avatar up and not **Wrath and Fury**
14. **Raging Blow**
15. **Thunder Clap** → **Whirlwind** (fillers)

Mountain Thane's key idea: **Thunder Clap replaces Whirlwind** as the filler, and
**Thunder Blast** (empowered Thunder Clap) is worth more than its tooltip — it
extends Avatar and always fires a Lightning Strike, so press it at 2 stacks or
while Avatar is up.

## Cleave / AoE — Slayer (`actions.slayer_aoe`)

1. **Whirlwind** if `talent.improved_whirlwind&buff.whirlwind.stack=0` (get the
   cleave buff up first)
2. **Recklessness** → **Avatar**
3. **Rampage** if Enrage about to drop or Rage ≥ 110
4. **Bladestorm** (Enraged, lined to Recklessness)
5. **Odyn's Fury**
6. **Execute** on **Sudden Death** proc
7. **Rampage** if Recklessness up
8. **Bloodbath**
9. **Whirlwind** if Improved Whirlwind and Recklessness up
10. **Crushing Blow** → **Execute** → **Rampage**
11. **Rend** if `dot.rend_dot.duration<6&!talent.improved_whirlwind`
12. **Bloodthirst** → **Whirlwind** (Improved WW) → **Raging Blow**
13. **Storm Bolt** if Bladestorm up

## Cleave / AoE — Mountain Thane (`actions.thane_aoe`)

1. **Odyn's Fury**
2. **Recklessness** → **Avatar**
3. **Thunder Blast** at 2 stacks; then **Thunder Blast** if Avatar up
4. **Thunder Clap** to get the Whirlwind/cleave buff up
   (`talent.improved_whirlwind&buff.whirlwind.stack=0`) or on 6+ enemies under Avatar
5. **Rampage** if Enrage about to drop or Rage ≥ 100
6. **Bloodbath** → **Rampage** (Reck up) → **Thunder Clap** (Avatar up)
7. **Bloodthirst** → **Thunder Blast** → **Execute** → **Thunder Clap**
8. **Crushing Blow** → **Rampage** → **Raging Blow** → **Whirlwind**

Mountain Thane routes AoE through **Thunder Clap / Thunder Blast** (Lightning
Strikes) rather than Bladestorm — it wins most **sustained** AoE; Slayer wins
**burst** AoE and single target.

## Hero-tree branches (summary)

- **Slayer** — Sudden Death / Execute-window build. Bloodthirst→**Bloodbath** and
  Raging Blow→**Crushing Blow** during Recklessness (**Reckless Abandon**);
  **Bladestorm** is the signature AoE/burst cooldown (fed by **Unrelenting
  Onslaught**). Best ST and burst AoE.
- **Mountain Thane** — Whirlwind→**Thunder Clap**, plus **Thunder Blast** and
  **Lightning Strikes**; **Avatar** over Bladestorm. Best sustained AoE.

## Execute phase

`variable.execute_phase` = target <20% HP (or <35% with **Massacre**). In execute
range, **Execute** climbs the priority and Sudden Death procs make it usable/free
even earlier — but Rampage/Enrage upkeep still comes first (Enrage must stay up).

## TODO

- [x] Single-target priority (Slayer + Mountain Thane) — from simc APL 2026-07-11
- [x] AoE/cleave priority (both hero trees) — from simc APL 2026-07-11
- [x] Cooldown usage rules (Recklessness/Bladestorm/trinket/potion sync) — simc + method
- [ ] Sanity-check the opener against a top WCL log (`wowkb.wcl rankings` → `casts`)
- [ ] Confirm exact base cooldowns (Odyn's Fury tier-set reduction, Champion's
      Spear) against the Blizzard spell API for the live 12.0.7 build
