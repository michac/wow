---
title: Frost Mage — Rotation (Midnight Season 1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Mage_Frost.simc  # tier 1 APL, 2026-07-11
  - https://www.method.gg/guides/frost-mage/playstyle-and-rotation  # tier 3, 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/frost-mage-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
confidence: high
---

# Frost Mage — Rotation (Spellslinger / Frostfire, Midnight S1)

Distilled from the SimulationCraft default APL (tier 1), corroborated by
method.gg and Icy Veins (tier 3). The APL branches by **hero tree**
(Spellslinger `ss_*` / Frostfire `ff_*`) and enemy count (single / AoE), with
`_tarswap` variants that always spread onto the lowest-Freezing target. Both
hero-tree ST lists are given below.

**The core loop (both trees):** press your cooldowns — **Frozen Orb**, **Comet
Storm** / **Ray of Frost**, **Glacial Spike** — on cooldown; **spend Freezing
stacks with Ice Lance**; then rebuild Icicles/stacks with **Frostbolt** (or
**Frostfire Bolt**). Never let **Freezing stacks** (cap 20), **Brain Freeze**,
or **Fingers of Frost** overcap — shattering stacks is your primary damage.

> **Meta note:** **Spellslinger** is the S1 recommendation for essentially all
> content (method.gg + Icy Veins builds page: "Frostfire is significantly
> behind"). The main behavioral difference is the Ice Lance spend threshold —
> **Spellslinger spends at 6+ Freezing stacks, Frostfire at 10+** — and which
> burst button leads (Comet Storm high for Spellslinger; Frostfire folds Ray of
> Frost into Comet Storm). Run Spellslinger unless you specifically want
> Frostfire's front-loaded outdoor burst. See `builds.md`.

## Pre-combat

- **Arcane Intellect**, `snapshot_stats`, **Summon Water Elemental**.
- AoE (3+ w/ Frostfire, or 4+ w/ Splinterstorm): pre-cast **Blizzard**.
- Otherwise pre-cast **Glacial Spike** (if it will be charged) → **Frostbolt**
  (Frostfire opener leads with a pre-cast Frostfire Bolt at ~2s).

## Cooldown rules

- **Potion + racials + trinkets** fire in the `cds` window, synced to the burst
  (Frostfire: after a Comet Storm; Spellslinger: at pull / after Frozen Orb with
  a Ray of Frost charge banked and low Freezing). Also potion if `fight_remains<35`.
- **Frozen Orb** and **Glacial Spike**: on cooldown, always.
- **Ray of Frost**: after the other rotational buttons; bank a charge (Hand of
  Frost gives 2) for burst/Bloodlust. `fight_remains<12` → dump it.
- **Comet Storm**: high priority; Frostfire's lead burst and consumes Freezing.
- **Icy Veins** (Thermal Void window): burst haste cooldown — hold **Flurry**
  while the Thermal Void buff is up (the APL gates Flurry on `buff.thermal_void.down`).
  @verify-ingame — the sim `cds` list does not explicitly cast Icy Veins; confirm
  it is still a manually-pressed cooldown in the Midnight build.
- **Shifting Power** (M+): channel to shave cooldowns between packs. @verify-ingame cadence.
- **Time Warp** / Bloodlust synced to the opener or a major burst window.

## Single target — Spellslinger (`ss_st`)

1. **Comet Storm**
2. **Flurry** — if **Brain Freeze** is up **and** Thermal Void is down
3. **Ice Lance** — at **2 stacks of Fingers of Frost** (don't overcap the proc)
4. **Frozen Orb**
5. **Glacial Spike** (when charged / off CD)
6. **Ice Lance** — with **Fingers of Frost** up
7. **Ice Lance** — at **Freezing ≥ 6**
8. **Ray of Frost** — if `icicles<3` (or within 25s of a potion)
9. **Flurry** — off cooldown (rebuild Freezing)
10. **Frostbolt** (filler / Icicle builder)
11. → movement list when forced to move

## Single target — Frostfire (`ff_st`)

1. **Flurry** — if **Brain Freeze** up **and** Thermal Void down
2. **Frozen Orb**
3. **Comet Storm**
4. **Glacial Spike**
5. **Ice Lance** — with **Fingers of Frost**
6. **Ice Lance** — at **Freezing ≥ 10** (note the higher threshold vs Spellslinger)
7. **Flurry** — off cooldown
8. **Ray of Frost**
9. **Frostfire Bolt** (filler)
10. → movement list

## AoE / cleave — Spellslinger (`ss_aoe`)

1. **Comet Storm**
2. **Blizzard** — while **Freezing Rain** is up (instant + buffed)
3. **Flurry** — Brain Freeze up & Thermal Void down
4. **Ice Lance** — at 2× Fingers of Frost
5. **Frozen Orb**
6. **Glacial Spike**
7. **Ice Lance** — with Fingers of Frost
8. **Ice Lance** — at Freezing ≥ 6
9. **Ice Nova** / **Cone of Cold** — with the Cone of Frost talent
10. **Blizzard** — with Freezing Winds
11. **Ray of Frost** (if `icicles<3`) → **Flurry** off CD → **Frostbolt**

## AoE / cleave — Frostfire (`ff_aoe`)

1. **Flurry** — Brain Freeze up & Thermal Void down
2. **Frozen Orb**
3. **Comet Storm**
4. **Glacial Spike**
5. **Blizzard** — at 6+ enemies (or 4+ with Freezing Rain, or with Freezing Winds)
6. **Ice Lance** — with Fingers of Frost
7. **Ice Lance** — at Freezing ≥ 10
8. **Flurry** off CD → **Ray of Frost** (if not holding Frostfire Empowerment) → **Frostbolt**

## Target-swapping (`_tarswap`)

In multi-target with priority swaps, the APL applies Freezing (Flurry / Ray of
Frost) `target_if=min:debuff.freezing` — always seed the **lowest-Freezing**
enemy so no target sits without stacks, then Ice Lance / Comet Storm shatter them.

## Hero-tree branches

- **Spellslinger** (`ss_*`, meta): Comet Storm leads, Ice Lance spends at 6+
  Freezing, Frozen Orb + Splinters shorten Ray of Frost, Splinterstorm dumps
  pooled Splinters. Smoother sustained profile.
- **Frostfire** (`ff_*`, alt): Frostbolt→Frostfire Bolt and Flurry become
  Frostfire spells, Glacial Spike explodes on impact, Ice Lance spends at 10+
  Freezing, Ray of Frost can transform into Comet Storm. More front-loaded burst.

## TODO

- [x] Single-target priority — both hero trees, from simc `ss_st`/`ff_st` (2026-07-11)
- [x] AoE priority — from simc `ss_aoe`/`ff_aoe` (2026-07-11)
- [x] Cooldown rules — from simc `cds` list + method/Icy Veins (2026-07-11)
- [ ] Resolve **Icy Veins** button status (pressed vs auto in Midnight) — @verify-ingame
- [ ] Sanity-check opener against a top WCL log (`wowkb.wcl rankings` → `casts`)
