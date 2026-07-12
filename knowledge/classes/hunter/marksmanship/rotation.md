---
title: Marksmanship Hunter — Rotation (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Hunter_Marksmanship.simc  # tier 1 APL (primary), fetched 2026-07-11, WoW 12.0.7 profile
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/engine/class_modules/apl/apl_hunter.cpp  # tier 1 APL source
  - https://www.method.gg/guides/marksmanship-hunter/playstyle-and-rotation  # tier 3, upd. 2026-06-16 (12.0.7), corroboration + opener
  - https://maxroll.gg/wow/class-guides/marksmanship-hunter-raid-guide  # tier 3, 12.0.7, hero-tree framing
confidence: high
---

# Marksmanship Hunter — Rotation (Midnight S1)

Distilled from the SimulationCraft default APL (Tier 1) for the MID1 profile,
corroborated with method.gg (Tier 3, 12.0.7). The APL branches by **hero tree**
(`sentst`/`sentaoe` for Sentinel, `drst`/`draoe` for Dark Ranger) and by enemy
count (AoE lists fire at **>2 targets** once Trick Shots is talented). Sentinel
is the S1 default across nearly all content; Dark Ranger is the pure-single-
target alternative (see `builds.md`).

The engine is: keep **Aimed Shot** and **Rapid Fire** rolling on cooldown, spend
**Precise Shots** with the right instant (Arcane/Multi-Shot or Kill/Black Arrow),
never overcap Precise Shots or Aimed Shot charges, and pool cooldowns into the
**Trueshot** window. **Aimed Shot is the only stand-still cast** — everything else
is instant or a channel, so use Arcane/Steady Shot to fill movement.

## Pre-combat

- Summon pet **only if** running **Unbreakable Bond** (`summon_pet,if=talent.unbreakable_bond`).
- Apply **Hunter's Mark**.
- Pre-cast **Aimed Shot** (APL: `if=active_enemies<3` or Dark-Ranger-with-Headshot),
  then **Steady Shot** to top Focus.

## Cooldown rules (APL `cds`)

- **Trueshot** is the burst spine. The APL gates it on
  `!buff.double_tap.up & variable.trueshot_ready` — i.e. **don't fire Trueshot
  while a Double Tap charge from Volley is still up** (consume Double Tap first:
  ST → with Rapid Fire; AoE → with Aimed Shot). `trueshot_ready` also holds
  Trueshot if a Bullseye stack window would be wasted, or dumps it if the fight
  is ending (`fight_remains<25`).
- **Racials** (Berserking / Blood Fury / Ancestral Call / Fireblood) and
  **on-use trinkets** sync to Trueshot being up. Damage trinkets fire when
  Trueshot has >20s left on CD; buff trinkets align to the Trueshot window
  (the APL matches trinket CD to Trueshot CD).
- **Potion** with Trueshot up + Bloodlust (or in the last ~30s).
- **Power Infusion** (external) wants `buff.trueshot.remains>12`.

## Single target — Sentinel (APL `sentst`)

1. **Volley** — if no Double Tap buff up (grants Trick Shots / Double Tap).
2. **Trueshot** — if no Double Tap up and `trueshot_ready`.
3. **Rapid Fire** — while `buff.bulletstorm.stack<18` (build Bulletstorm).
4. **Aimed Shot** — target with Sentinel's Mark up, when about to cap charges
   (`full_recharge_time<gcd+cast_time`).
5. **Arcane Shot** — spend **Precise Shots** (during Trueshot only right after
   an Aimed Shot; freely outside Trueshot).
6. **Rapid Fire** — when Bulletstorm is about to fall off, or (with Unload) the
   target is <20% HP.
7. **Kill Shot** — spend Precise Shots at 1 target.
8. **Moonlight Chakram** — if Trueshot is about to expire (fit it in the window).
9. **Aimed Shot** — otherwise (Mark-up target).
10. **Moonlight Chakram** → **Rapid Fire** → **Explosive Shot** → **Steady Shot**
    (Focus filler).

## Single target — Dark Ranger (APL `drst`)

1. **Black Arrow** — spend **Precise Shots** (this is the Kill Shot slot).
2. **Aimed Shot** — during Trueshot with no Precise Shots and Black Arrow ready,
   or when about to cap charges.
3. **Trueshot** — if no Double Tap up and `trueshot_ready`.
4. **Rapid Fire**.
5. **Wailing Arrow** — while Black Arrow is on CD (generates Deathblow).
6. **Arcane Shot** — spend Precise Shots.
7. **Volley** — if no Double Tap up.
8. **Aimed Shot** — otherwise.
9. **Explosive Shot** → **Steady Shot** (filler).

> Dark Ranger loop: maximize **Black Arrow** casts by burning **Deathblow**
> procs (one on Trueshot activation, one after Wailing Arrow, one per Rapid
> Fire, chance from Aimed Shot). Queue Black Arrow at the end of an Aimed Shot
> cast so the same hit can proc another Deathblow. Black Arrow triples during
> the Trueshot/Withering Fire window.

## AoE / cleave (3+ targets, Trick Shots talented)

**Setup:** you need **Multi-Shot on 3+** (or **Volley**) to light **Trick
Shots** before Aimed Shot / Rapid Fire cleave. With **Aspect of the Hydra** the
shots hit 2 targets with no setup.

### Sentinel AoE (APL `sentaoe`)
1. **Multi-Shot** — spend Precise Shots, or when Trick Shots is down (re-light it).
2. **Rapid Fire** — maintain Bulletstorm (`<18` stacks / about to expire, or Unload <20%).
3. **Trueshot** — if no Double Tap up.
4. **Volley** — if no Double Tap up.
5. **Explosive Shot** — with Shrapnel Shot, outside Trueshot/Lock-and-Load, near-capped Aimed charges.
6. **Aimed Shot** — while Trick Shots is up (Mark target).
7. **Moonlight Chakram** → **Rapid Fire** (Trick Shots up) → **Multi-Shot** (Windrunner Quiver) → **Explosive Shot** → **Steady Shot**.

### Dark Ranger AoE (APL `draoe`)
1. **Aimed Shot** — while Trick Shots up and about to cap charges.
2. **Black Arrow** — spend Precise Shots.
3. **Multi-Shot** — spend Precise Shots (not with Aspect of the Hydra; re-light Trick Shots when down).
4. **Trueshot** — if no Double Tap up.
5. **Rapid Fire** — while Trick Shots outlasts the channel (feed Bulletstorm/Unload).
6. **Wailing Arrow** — while Black Arrow on CD.
7. **Volley** — if no Double Tap up.
8. **Aimed Shot** (Trick Shots up) → **Multi-Shot** (Precise Shots) → **Explosive Shot** → **Steady Shot**.

## Hero-tree branch summary

- **Sentinel** — build/spend around **Sentinel's Mark** + **Bulletstorm** (Rapid
  Fire fuel), with **Volley/Double Tap** and **Moonlight Chakram** in the ST list;
  **Lunar Storm** procs automatically on Mark consumption (no positioning). S1
  default for raid and M+.
- **Dark Ranger** — **Black Arrow** replaces Kill Shot and is spammed via
  **Deathblow**; **Trueshot → Wailing Arrow** during Withering Fire. Preferred
  for pure single-target (defensively stronger too).

## TODO

- [x] ST + AoE priority for both hero trees — from simc midnight APL 2026-07-11
- [x] Cooldown/Trueshot + Double Tap rules — simc `cds` + method.gg
- [ ] Sanity-check opener vs a top WCL log (`wowkb.wcl rankings` → `casts`)
- [ ] Re-distill if simc publishes a retuned 12.0.7 MM APL (current profile
      is the live midnight-branch default as of 2026-07-11)
