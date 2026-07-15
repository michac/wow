---
title: Outlaw Rogue — Rotation (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight branch profiles/MID1/MID1_Rogue_Outlaw.simc  # tier 1 APL (default profile = Fatebound talents, handles both hero trees), 2026-07-11
  - https://www.method.gg/guides/outlaw-rogue/playstyle-and-rotation  # tier 3, updated 2026-06-16, 12.0.7
  - https://www.icy-veins.com/wow/outlaw-rogue-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7 corroboration
confidence: high
---

# Outlaw Rogue — Rotation (Midnight S1)

Distilled from the SimulationCraft default APL (Tier 1) and corroborated against
the method.gg and Icy Veins 12.0.7 guides (both updated 2026-06-16). Outlaw is a
buff-maintenance spec: keep **Roll the Bones** and **Slice and Dice** up, keep
**Adrenaline Rush** and (on 2+ targets) **Blade Flurry** running, then loop
**builder → finisher** while **Restless Blades** refunds cooldowns for every
combo point spent. The single-target and AoE priorities are nearly identical —
Blade Flurry is what makes them the same rotation. The APL branches lightly by
hero tree (Trickster's **Coup de Grace** vs Fatebound's Dispatch-at-−2 handling).

> **Combo-point targets.** Builders push to **cp_max − 1** before finishing
> (**cp_max − 2** when Killing Spree is up, or for Fatebound Dispatch). Practically:
> finish at **6+** combo points, spend Between the Eyes / Killing Spree slightly
> earlier when they're ready. Don't overcap combo points or energy.

## Pre-combat

1. Apply poisons (lethal + nonlethal).
2. **Stealth** (~2s before pull).
3. With **Improved Adrenaline Rush**: pre-cast **Adrenaline Rush**, then
   **Slice and Dice**.
4. Pre-roll **Roll the Bones** if a **Loaded Dice** proc is banked (guarantees a
   better opening roll).

## Cooldown rules

- **Adrenaline Rush** — keep it up; use on cooldown. With Improved Adrenaline
  Rush, fire it at **low combo points** (it's part of the builder loop, not a
  finisher window). Skip only if immediate downtime is expected.
- **Blade Flurry** — refresh whenever **2+ targets** are in range and it's about
  to fall off (`remains < gcd`).
- **Preparation** — press once **Adrenaline Rush and Between the Eyes are both on
  cooldown** (resets them + Blade Rush / Blade Flurry / Killing Spree). Also used
  in the last <30s of a fight.
- **Keep It Rolling** — use once you're at **Roll the Bones stage 3+** to bank the
  strong buff set. Restless Blades turns its ~6min cooldown into ~1min effective.
- **Roll the Bones** — roll if it's **not up**, or **reroll off stage 1** to climb
  to stage 2; roll over stage 2 too when Loaded Dice is active **and** Keep It
  Rolling is ready.
- **Blade Rush** — use on cooldown with the tier set, in AoE, or on single-target
  when energy won't overcap within the GCD.
- **Vanish / Shadowmeld** — Hidden Opportunity builds only, to squeeze an extra
  **Ambush** in between Audacity/Opportunity procs (when not finishing and no
  proc is currently up).
- **Potion / racials / trinkets** — line up with Adrenaline Rush; trinkets also
  fire during Between the Eyes windows or on any-stat procs, and in the last ~20s.

## Single target

Builders and finishers interleave — cast a **finisher** whenever the finish
condition is met (≈6+ CP), otherwise cast a **builder**:

**Finishers (when at finish CP):**
1. **Between the Eyes** — on cooldown (hold only under Supercharger + Zero In for
   an imminent Adrenaline Rush).
2. **Killing Spree** — at high combo points; cancel it with a builder/finisher if
   you're about to cap energy.
3. **Coup de Grace** (Trickster) — when available/guaranteed.
4. **Dispatch** — default single-target finisher.

**Builders (when below finish CP):**
1. **Ambush** — with Hidden Opportunity **+ Audacity proc** up.
2. **Blade Flurry** — with Deft Maneuvers at 3+ targets (to build CP).
3. **Coup de Grace** — when Disorienting Strikes guarantees an Unseen Blade.
4. **Pistol Shot** — to consume an **Opportunity** proc: with Audacity+Hidden
   Opportunity to re-proc Audacity when Ambush isn't up; with Fan the Hammer at
   max Opportunity stacks / about to expire, or when it won't overcap combo
   points; without Fan the Hammer, spend by energy / when it exactly caps CP / to
   feed Quick Draw or Audacity.
5. **Ambush** (Hidden Opportunity, pooling energy for it if needed).
6. **Sinister Strike** — fallback builder / default filler.

## AoE / cleave (2+)

Same priority as single target, with these overrides:

- **Blade Flurry** up whenever there are **2+ targets** (it echoes your damage to
  everything nearby — the AoE lives here). Recast at low combo points when 4+
  targets are up so you don't clip it mid-cleave.
- With **Deft Maneuvers**, use Blade Flurry as a **combo-point builder** at 3+
  targets.
- **Blade Rush** on cooldown (it's AoE and refunds energy).
- Finishers stay the same — **Between the Eyes / Dispatch** cleave through Blade
  Flurry, so you don't switch spenders for AoE. **Grand Melee** and **Dancing
  Steel** (dungeon talents) raise the Blade Flurry target cap and duration.

## Hero-tree branches

- **Trickster** (recommended, all content): **Coup de Grace** enters both the
  builder and finisher lists — press it whenever it's guaranteed (Disorienting
  Strikes) or otherwise available. Smoothest and highest for S1.
- **Fatebound** (the APL's default profile): no active hero button — the coin-flip
  (**Hand of Fate → Lucky Coin**) is passive. The only rotational difference is
  Fatebound spends **Dispatch at cp_max − 2** rather than holding for −1.

## TODO

- [ ] Sanity-check the opener against a top WCL log (`wowkb.wcl rankings` →
      `casts`) once S1 logs are pulled.
- [ ] Re-distill if the simc midnight branch publishes a Trickster-default
      profile (current default profile ships Fatebound talents but the APL
      handles both trees).
