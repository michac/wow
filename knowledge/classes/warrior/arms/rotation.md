---
title: Arms Warrior — Rotation (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight branch profiles/MID1/MID1_Warrior_Arms.simc  # tier 1 APL, talents=CcEAAAA..., WoW 12.0.7, fetched 2026-07-11
  - https://www.method.gg/guides/arms-warrior/playstyle-and-rotation  # tier 3, 12.0.7, 2026-07-11
  - https://www.method.gg/guides/arms-warrior/talents  # tier 3, 12.0.7, 2026-07-11
confidence: high
---

# Arms Warrior — Rotation (Slayer / Colossus, Midnight S1)

Distilled from the SimulationCraft default APL (Tier 1). The list is a **priority
queue**: after every cast, restart from the top. The whole rotation orbits the
**`Colossus Smash` window** — a ~45s armor-ignore/damage-amp debuff you sync
`Avatar`, `Champion's Spear`, and your hero finisher (`Demolish` or a
`Bladestorm`/`Ravager`) into. The APL forks first on **hero tree**
(`talent.demolish` → Colossus lists; `talent.slayers_dominance` → Slayer lists),
then on **enemy count** (`active_enemies>2` → AoE) and **execute phase**
(`variable.execute_phase` = target <35% with `Massacre`, else <20%).

> **Hero-tree split (method.gg, 12.0.7):** **Slayer** is the single-target /
> execute build — spam `Execute` with `Sudden Death`; rage-starves mainly in
> execute. **Colossus** is the AoE / M+ build — keep `Mortal Strike` and `Cleave`
> on cooldown and land `Demolish` inside `Colossus Smash`; can rage-starve any
> time procs go dry. `Anger Management` makes cooldowns cheap to press, so use
> them on cooldown as long as you get the full window.

## Pre-combat

- Toggle **Battle Stance** on (`actions.precombat+=/battle_stance,toggle=on`).
- `snapshot_stats`; set trinket variables.

## Cooldown & interrupt rules

- **`Pummel`** the instant a target is casting an interruptible (`pummel,if=target.debuff.casting.react`) — sits above the whole rotation.
- **`Charge`** at pull (`time<=0.5`) or whenever out of melee (`movement.distance>5`); charge-weaving back in refunds ~20 Rage.
- **Potion / racials / trinkets** fire **inside the `Colossus Smash` window** (`debuff.colossus_smash.remains>8`, or `buff.avatar.up`) — see the trinket sub-list, gated on `buff.avatar.up`.
- **`Avatar` + `Colossus Smash`** are pressed together as the burst pair; the sub-lists call `avatar` then `colossus_smash` near the top.

## Opener (method.gg)

`Charge` → `Rend` → `Avatar` + `Colossus Smash` → `Mortal Strike` →
**Slayer:** `Bladestorm` · **Colossus:** `Demolish` → resume priority.

## Single target — Slayer (`slayer_st`)

1. **Sweeping Strikes** if 2 targets and it's down (or no `Broad Strokes`)
2. **Avatar**
3. **Champion's Spear** if `Colossus Smash` up or `Avatar` up
4. **Ravager** if `Colossus Smash` comes off CD within a GCD
5. **Colossus Smash**
6. **Bladestorm** while `Colossus Smash` is up
7. **Heroic Strike** (the `Master of Warfare` apex filler)
8. **Mortal Strike**
9. **Execute** on a `Sudden Death` proc
10. **Overpower**
11. **Rend** if the bleed has <5s left
12. **Slam** (filler) → `Wrecking Throw` (single-target ranged filler)

## Single target — Colossus (`colossus_st`)

1. **Rend** if <1 GCD left, or if `Colossus Smash` is <2s away and Rend <10s
2. **Sweeping Strikes** (2-target, as above)
3. **Ravager** if `Colossus Smash` within a GCD (with `Cleave` talented)
4. **Avatar** → **Colossus Smash** → **Champion's Spear**
5. **Demolish** while `Colossus Smash` is up and `Colossal Might` has stacks
6. **Heroic Strike** → **Mortal Strike**
7. **Overpower** → **Execute**
8. **Rend** if <5 GCDs left → **Slam** (filler) → `Wrecking Throw`

## Execute phase (<35% Massacre / <20%)

**Slayer (`slayer_execute`):** `Sweeping Strikes` (2-tgt) → `Rend` if <2s (no
`Bloodletting`) → `Avatar` → `Colossus Smash` → `Heroic Strike` → `Bladestorm`
in `Colossus Smash` → **`Mortal Strike` at 2 stacks of `Executioner's Precision`
(inside `Colossus Smash`)** → `Overpower` on `Opportunist`/low-rage →
**`Execute` if rage>40 or `Sudden Death`** → `Overpower` → `Execute` (Improved
Execute) → `Slam` filler → `Execute`.

**Colossus (`colossus_execute`):** as ST but `Mortal Strike` only at 2 stacks of
`Executioner's Precision` (or with `Battlelord`), then **`Execute` if
`Deep Wounds`+rage>75 or `Sudden Death`**, `Overpower`, `Execute` if rage>75,
`Slam`, `Execute`.

> The through-line both trees share: **funnel `Mortal Strike` and `Execute` into
> the `Colossus Smash` window**, and in execute **hold `Mortal Strike` for 2
> stacks of `Executioner's Precision`** so it lands amplified.

## AoE / cleave (3+ targets)

**2 targets** is handled inside the ST/execute lists via **`Sweeping Strikes`**
(and `Cleave`/`Whirlwind` when `Collateral Damage` is at 3 stacks). True AoE
(`active_enemies>2`) runs the dedicated lists:

**Colossus (`colossus_aoe`):**
1. **Thunder Clap** / **Rend** to apply the bleed if missing
2. **Sweeping Strikes** (if `Colossus Smash` >10s out, or no `Broad Strokes`)
3. **Ravager** as `Colossus Smash` approaches → **Avatar** → **Colossus Smash** → **Champion's Spear**
4. **Cleave** at **2+ `Collateral Damage`** stacks
5. **Demolish** at **10 `Colossal Might`** (inside/near `Colossus Smash`)
6. **Cleave** → **Demolish** (if `Colossus Smash` ≥2s) → **Whirlwind** at 3 stacks (Fervor of Battle)
7. **Rend** refresh → **Mortal Strike** → **Overpower** → filler (`Execute`/`Slam`/`Bladestorm`/`Whirlwind`)

**Slayer (`slayer_aoe`):**
1. **Rend** if missing → **Sweeping Strikes** → **Avatar** → **Champion's Spear**
2. **Ravager** / **Bladestorm** while `Colossus Smash` up → **Colossus Smash**
3. **Cleave** at 3 `Collateral Damage` → **Cleave** → **Whirlwind** at 3 stacks (Fervor of Battle)
4. **Execute** on `Sudden Death` → **Mortal Strike** on `Battlelord` → **Overpower** (Dreadnaught) → **Mortal Strike**
5. **Thunder Clap** to refresh Rend spread → **Whirlwind** (Fervor of Battle) → filler

Across both: **`Cleave` on cooldown is the top multi-target contributor at 3+**,
`Collateral Damage` (built by `Cleave`) is spent by `Whirlwind`, and `Rend` +
`Deep Wounds` bleeds are kept rolling on the pack.

## Hero-tree branches (summary)

- **Slayer** — `Slayer's Dominance` (Marked for Execution) turns `Execute` +
  `Sudden Death` into the ST/execute engine; `Bladestorm` is the burst button
  fired inside `Colossus Smash`. Better single target.
- **Colossus** — `Demolish` is the payoff, gated on **10 `Colossal Might`**
  stacks and the `Colossus Smash` window; `Cleave` uptime + `Broad Strokes`
  (free `Sweeping Strikes` on every `Colossus Smash`) drive its AoE lead.

## TODO

- [ ] Sanity-check the opener/execute against a top WCL Arms log
      (`wowkb.wcl rankings` → `casts`) once S1 raid parses stabilize.
- [ ] Re-distill if the simc midnight branch publishes a retuned 12.0.7 APL
      (current file talents string `CcEAAAA...`, fetched 2026-07-11).
