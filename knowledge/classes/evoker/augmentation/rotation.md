---
title: Augmentation Evoker — Rotation (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight branch engine/class_modules/apl/apl_evoker.cpp augmentation_12_0_5  # tier 1 APL, 2026-07-11
  - https://www.method.gg/guides/augmentation-evoker/playstyle-and-rotation  # tier 3, 2026-07-11
  - https://www.icy-veins.com/wow/augmentation-evoker-pve-dps-rotation-cooldowns-abilities  # tier 3, 2026-07-11
confidence: medium
---

# Augmentation Evoker — Rotation (Midnight S1)

Distilled from the SimulationCraft Augmentation APL (Tier 1;
`augmentation_12_0_5` in `apl_evoker.cpp` — the latest published Augmentation
action list, no separate `MID1_Evoker_Augmentation.simc` profile exists yet),
corroborated by method.gg and Icy Veins (both 12.0.7). Augmentation is a
**buff-maintenance** spec: the "rotation" is really the loop that keeps
**Ebon Might** and **Prescience** alive on your allies while you funnel Essence
into **Eruption** and align your big buttons with **Breath of Eons**. It plays
in roughly **30-second cycles** built around the Fire Breath / Upheaval
cooldowns.

> **Empower ranks matter more than damage math here.** The APL casts **Fire
> Breath at rank 4 when Leaping Flames is talented, rank 1 otherwise**, and
> **Upheaval at rank 1** — low ranks are fast and keep the Ebon Might loop
> moving. Method's advice to "uprank Upheaval for radius" is a situational AoE
> coverage call, not the default. When in doubt, follow the APL rank.

## Pre-combat

- **Blistering Scales** on the tank (if talented).
- Pre-cast **Living Flame** (and **Chrono Flame** first on Chronowarden).
- Have **Blessing of the Bronze** up on the group.

## Opener

1. **Ebon Might**
2. **Prescience ×2** on your preferred buff targets (best damage dealers)
3. **Breath of Eons** (bank the raid's burst) — Scalecommander may weave
   **Deep Breath** here as well
4. **Trinkets + DPS potion** (synced to the Breath window)
5. **Tip the Scales → Fire Breath** (instant, highest rank)
6. **Upheaval** (rank 1)
7. Fully channel **Time Skip** (if talented) to reset the empowers
8. **Prescience** on a target missing the buff
9. Spend Essence on **Eruption**

## Cooldown rules

- **Ebon Might is the floor** — never let it drop. The APL refreshes it inside
  the last ~40% of its duration (pandemic window); practically, recast at
  **~3–4s remaining**. Eruption, Fire Breath, and Upheaval each **extend** it,
  so casting spenders during the window is what sustains it.
- **Cast Fire Breath / Upheaval only while Ebon Might is up** — casting them
  outside the buff wastes their extension.
- **Breath of Eons on cooldown**, but only if the target will live ≥20s. Stack
  as many **allied DPS cooldowns, trinkets, and your potion** into the Breath
  window as possible — that is where the spec's damage concentrates.
- **Tip the Scales** just before Fire Breath (when Breath of Eons is **not**
  available), to make it an instant max-rank cast.
- **Time Skip** when the empowers are on cooldown and Breath of Eons is ≥15s
  out (or to reset Tip the Scales) — it drags your cooldowns forward.
- **Prescience:** keep it on your top damage dealers; don't overcap charges
  (roughly every ~15s). The APL prioritizes the ally whose buff is closest to
  expiring, weighted toward attackers/casters.
- **Potion / Fury of the Aspects (lust):** sync to the Breath of Eons window
  (or when Breath is ≥90s away / the fight is nearly over).

## Single-target priority

1. **Hover** if you need to move (off-GCD, cast-while-moving)
2. **Ebon Might** if ≤~4s remaining (pandemic refresh)
3. **Prescience** if a tracked ally's buff is about to expire / on the opener
4. **Tip the Scales** (when Breath of Eons is down and Fire Breath is ready)
5. **Breath of Eons** on cooldown (target lives ≥20s)
6. **Fire Breath** during Ebon Might — **rank 4 with Leaping Flames, else rank 1**
7. **Upheaval** during Ebon Might — **rank 1**
8. **Time Skip** when both empowers are cooling and Breath is ≥15s out
9. **Eruption** to spend Essence while Ebon Might is up (also extends it) —
   consume **Essence Burst** procs here
10. Filler: **Living Flame** (when it procs Leaping Flames / on the move via
    Hover) → **Azure Strike** as the default instant filler

## Cleave / AoE

The core loop is unchanged — the opener and cooldown order are the **same for
multiple targets**. Adjustments:

- **Azure Strike over Living Flame** as filler (it hits 2 targets and is
  instant).
- **Upheaval** can be **upranked** for radius so it covers the whole pack
  (guide advice; the APL still defaults to rank 1).
- **Eruption** targets by **Bombardments** stacks on Scalecommander (the APL
  spends on the highest-Bombardment target, and dumps **Mass Eruption** stacks
  immediately) — Bombardments turns Eruption into the spec's AoE damage engine.
- Keep **Ebon Might / Prescience** discipline exactly as single-target; the
  buffs are what matter, the AoE filler just fills gaps.

## Hero-tree branches

- **Scalecommander** (default / M+): adds **Bombardments** (Eruption stacks a
  debuff that explodes) and **Extended Battle** pooling. The APL runs the
  **filler action list to pool Essence Burst** when an empower is ~4 GCDs away
  and Bombardments pooling is on, then dumps Eruption on the highest-stack
  target. This is the "fire and forget" burst-AoE build.
- **Chronowarden** (single-target raid, ~3% more ST): leans on **time-magic
  buff extension** and **Chrono Flame** (replaces Living Flame as filler,
  synergizes with **Afterimage**). **Duplicate** copies your Ebon Might
  extensions. Plays more around precise buff timing; some builds use a
  **Tip the Scales cancelaura** macro (see the `cancel_buff,name=tip_the_scales`
  line in the APL) to avoid wasting the instant-empower on the wrong spell.

## TODO / gaps

- [ ] No dedicated `MID1_Evoker_Augmentation.simc` profile in the simc midnight
      branch (only Devastation profiles exist). Rotation distilled from the
      **`augmentation_12_0_5` APL function** (Tier 1) + Tier-3 guides. Re-distill
      when a MID1 Augmentation profile / 12.0.7 APL revision publishes.
- [ ] Confirm exact empower ranks and Bombardments targeting in-game; the
      APL rank choices (FB r4/r1, Upheaval r1) disagree with method's
      "uprank Upheaval" colour — verify which wins in current tuning.
