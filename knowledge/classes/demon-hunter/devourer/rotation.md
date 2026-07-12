---
title: Demon Hunter Devourer — Rotation (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight branch profiles/MID1/MID1_Demon_Hunter_Devourer.simc  # tier 1 APL, 2026-07-11 (talents=CgcBAAAAAAAAAAAAAAAAAAAAAAA2MmZmZmZmBzMAAAAAAALzYAzAAAAAAAAwMGMmZmZMzMzYmFzYsotNmZmZ2abmZGAjZAIwMzgxMA)
  - simc midnight branch profiles/MID1/MID1_Demon_Hunter_Devourer_Void-Scarred.simc  # tier 1 APL variant, 2026-07-11
  - https://www.method.gg/guides/devourer-demon-hunter/playstyle-and-rotation  # tier 3, Hype, upd. 2026-06-17, 2026-07-11
  - https://www.icy-veins.com/wow/devourer-demon-hunter-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
confidence: medium
---

# Demon Hunter Devourer — Rotation (Annihilator, Midnight S1)

Devourer has **no fixed rotation — it is a priority system that flips between two
states**: a build phase **outside Void Metamorphosis** (generate Fury + bank Soul
Fragments to 50) and a spend phase **inside Void Metamorphosis** (dump Souls into
Collapsing Star + empowered casts before Fury drains out). As a mid-range caster
the golden rule is **always be casting** — use the mobility kit (Shift, Vengeful
Retreat) to reposition between/around casts rather than dropping a global.

Distilled from the Tier-1 SimulationCraft APL (`MID1_Demon_Hunter_Devourer.simc`,
sub-lists `math_for_wizards` / `reaps` / `melee_combo` / `illicit_doping`)
corroborated against method.gg and Icy Veins (both Tier-3, 12.0.7). **Annihilator
is the S1 default in every scenario** (see `builds.md`); Void-Scarred variants are
noted at the end.

> ⚠ Brand-new Midnight spec, **no Warcraft Logs sanity-check distilled yet** and
> several thresholds come from Tier-3 guides — treat exact Soul/Fury/stack numbers
> as `@verify-ingame`. The state-machine shape (bank Souls → Meta → spend) is
> solid across all sources.

## Pre-combat / opener (Annihilator)

1. **Soul Immolation** ~2s before pull.
2. **Consume** ~1s before pull.
3. **Consume** spam until **100 Fury or 3 Voidfall stacks**.
4. **Reap** (at 3 Voidfall) → **Void Ray** → **Void Metamorphosis** once at 50 Souls.
5. On-use trinket + potion inside the Meta window (see cooldown rules).
6. Inside Meta: **Void Ray → Voidblade → Collapsing Star → Cull/Eradicate → Devour**.

## Cooldown rules

- **Void Metamorphosis is the whole game** — it is fragment-gated, not on a timer.
  Bank to **50 Souls** (35 with *Soul Glutton*) and pop it, then extract as many
  **Collapsing Star** + empowered casts as possible before Fury drains and the
  form drops. Don't sit on 50 Souls (Feast of Souls caps out and you overflow).
- **Trinkets / potion / Power Infusion** sync to the Void Metamorphosis window
  (the APL's `illicit_doping` list gates them on the burst window / on-use logic).
- **The Hunt** (90s) — weave into a Meta window for burst; a core damage button in
  the Void-Scarred melee build, a lesser priority for Annihilator ST.
- **Don't overcap Souls or Fury.** *Soul Glutton* lowers the Meta requirement to
  35 but drains Fury ~25% faster, shortening windows ~30% — spend faster inside.

## Single target (Annihilator)

**Outside Void Metamorphosis:**
1. **Reap / Eradicate** at **3 Voidfall stacks** (spend the stacks → Void Meteors)
2. **Void Metamorphosis** as soon as it's available (50 Souls)
3. **Void Ray** at 100 Fury (main spender + Soul generation)
4. **Soul Immolation** if not active
5. **Consume** (filler / Fury + Soul builder)
6. **Reap** at 4+ Souls if it pushes you to Void Metamorphosis access

**Inside Void Metamorphosis:**
1. **Collapsing Star** if Meta is about to expire (don't lose the cast)
2. **Void Ray** if Meta is about to expire
3. **Cull / Eradicate** if Meta is expiring and it makes enough Souls for one more Collapsing Star
4. **Voidblade** (if *Devourer's Bite* talented — damage amp)
5. **Collapsing Star** at **35+ stored Souls** (don't overcap)
6. **Void Ray**
7. **Cull / Eradicate** at 3 Voidfall stacks, <30 Souls
8. **Collapsing Star**
9. **Devour** (filler)

## Cleave / AoE (Annihilator)

**Outside Void Metamorphosis:**
1. **Void Metamorphosis** when available
2. **Eradicate** at **3 Voidfall stacks**
3. **Eradicate** with *Moment of Craving* active + 10 Souls on the ground
4. **Void Ray**
5. **Soul Immolation** if not active
6. **Consume**
7. **Reap** at 4+ Souls (grants Meta access)

**Inside Void Metamorphosis:**
1. **Collapsing Star** (before overcapping ~40 Souls)
2. **Eradicate** with *Moment of Craving* + 10 Souls
3. **Void Ray**
4. **Devour**

*Eradicate* (the AoE frontal that Reap becomes after a full Void Ray channel) is
the multi-target backbone — it "stands for a massive portion" of Devourer's AoE.

## Void-Scarred branches

Two Void-Scarred variants exist (`MID1_Demon_Hunter_Devourer_Void-Scarred.simc`,
Tier-1) and are single-target-competitive but weaker the moment targets are added:

- **Void-Scarred caster** — outside Meta: Voidblade (if *Devourer's Bite*, next
  cast is Meta) → Void Metamorphosis → Void Ray → Soul Immolation → Reap →
  Consume. Inside Meta: Collapsing Star / Void Ray (if expiring) → **Cull on CD**
  → Pierce the Veil (if *Devourer's Bite*) → Void Ray → Collapsing Star → Cull
  (Student of Suffering-buffed) → Cull → Devour → Soul Immolation (fallback).
- **Void-Scarred melee** — adds a `melee_combo` layer: **Vengeful Retreat** (if
  *Voidstep*-buffed) → **Hungering Slash** → **The Hunt** → **Voidblade** before
  transforming, then inside Meta: Reaper's Toll → Pierce the Veil → Predator's
  Wake weave between Void Ray / Collapsing Star / Devour. Stat priority shifts
  toward Crit (see `builds.md`).

Gameplay difference: **Annihilator** ramps *Voidfall* → Void Meteors and does
little outside Meta (sharp in-window play required); **Void-Scarred** ramps
*Burning Blades* with Reap/Cull and lines big hits inside *Student of Suffering*,
so it has more consistent out-of-Meta damage.

## TODO

- [ ] Sanity-check the opener + Meta window against a top WCL log
      (`wowkb.wcl rankings` → `casts`) — none distilled yet (new spec).
- [ ] Re-distill exact Soul/Fury/Voidfall thresholds from a fuller simc APL dump
      (the sub-list conditions were summarized, not reproduced line-for-line).
- [ ] Confirm Void Ray in-Meta cooldown (14s vs 16s) and Collapsing Star Soul
      cost (30) in-game.
