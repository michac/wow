---
title: Devastation Evoker — Rotation (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Evoker_Devastation.simc  # tier 1 APL (st_fs / aoe_fs / sc / es lists), 2026-07-11
  - https://www.method.gg/guides/devastation-evoker/playstyle-and-rotation  # tier 3, 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/devastation-evoker-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
confidence: medium
---

# Devastation Evoker — Rotation (Midnight S1)

Distilled from the SimulationCraft default APL (Tier 1), which routes by hero
tree and enemy count: `sc` (**Scalecommander**, when *Mass Disintegrate* is
talented), then `aoe_fs` / `st_fs` (**Flameshaper**). method.gg + Icy Veins
corroborate the priority. The engine of the spec is simple — **keep Fire Breath
and Eternity Surge on cooldown, pool them into Dragonrage, and chain Disintegrate
to spend Essence without gaps** — and the difficulty is entirely in *movement /
Hover* uptime and empower timing.

> **General priority (both hero trees, from method.gg):** Dragonrage → Fire
> Breath (Rank 1) on CD → Eternity Surge (Rank 1) on CD → Deep Breath on CD
> (Scalecommander) → spend Essence Burst / Essence on Disintegrate → 2nd Fire
> Breath charge (Flameshaper) → Living Flame filler.

## Core rules (apply to every list)

- **Fire Breath and Eternity Surge are cast at Rank 1** (Empower I) on cooldown
  — short cast, maximum casts per minute. Push higher ranks only for wide AoE
  (see the `es` rank table below) or when *Tip the Scales* makes it instant.
- **Chain Disintegrate**: recast just before the channel's last tick
  (`early_chain_if=ticks_remain<=1`) so ticks never gap. This is a net DPS gain.
- **Essence spender by target count** (method.gg): **≤3 targets → Disintegrate;
  4+ stacked → Pyre.** (With *Volatility* rank 2 or *Feed the Flames*, Pyre wins
  at 3.)
- **Hover is a mobility tool, not a filler**: cast it right after an instant so
  its animation hides inside the GCD, then keep casting/channeling while moving.
- **Spend Essence Burst on Disintegrate**, not on Living Flame, whenever you can
  stand still to channel (Blue *Iridescence* procs likewise → Disintegrate).

## Cooldown rules

- **Dragonrage on cooldown** when the target will live ≥30s (or adds are
  imminent) — it's the 2-minute burst window; *Animosity* extends it every time
  you empower inside it, so **line up Fire Breath + Eternity Surge to fire during
  Dragonrage** and keep it alive.
- **Potion + external Power Infusion**: only during Dragonrage (or `fight_remains<35`).
- **Trinkets** sync to Dragonrage windows (the APL's `trinkets` list weights
  on-use effects to the Dragonrage cadence — don't bank past a lost use).
- **Tip the Scales** inside Dragonrage → instant max-rank **Eternity Surge**
  (`st_fs`: when Eternity Surge is usable at least as soon as Fire Breath).
- **Scalecommander Deep Breath**: use on cooldown, then a **second Deep Breath
  ~7–8s later** once you've banked ≥2 charges of *Imminent Destruction*; time it
  to keep *Strafing Run* rolling (`sc`: recast when `buff.strafing_run.remains <=
  ~2 GCDs`).
- **End of fight** (`fight_remains<35`): pop everything — potion, cooldowns.

## Single-target priority (Flameshaper — `st_fs`)

1. **Dragonrage** (target lives ≥30s / adds not imminent)
2. **Hover** if movement is coming (off-GCD, weave after an instant)
3. **Tip the Scales** during Dragonrage → next empower instant (favor Eternity Surge)
4. **Eternity Surge** — Rank 1 on cooldown (Rank 2 at exactly 2 targets without
   *Eternity's Span*)
5. **Fire Breath** — Rank 1 on cooldown when the DoT is refreshable and it fits
   the Dragonrage window (don't clip a full-recharge)
6. **Disintegrate** — Essence spender; **chain-cast** it (target the enemy with
   the most Fire Breath DoT remaining)
7. **Azure Sweep** when available
8. **Living Flame** filler — cast when *Burnout* / *Leaping Flames* / *Ancient
   Flame* is up (or when forced to move and it's still a cast-time gain)
9. **Azure Strike** — lowest filler (instant; the movement/last-resort button)

Icy Veins ST summary (Flameshaper): "Fire Breath on cooldown always at Empower
Rank 1; Eternity Surge on cooldown; Disintegrate as your Essence spender; Azure
Sweep when available; Living Flame as filler."

## Single-target priority (Scalecommander — `sc`)

1. **Deep Breath** to keep *Strafing Run* up (recast when it's ~2 GCDs from
   falling off)
2. **Dragonrage** (as ST rule above)
3. **Hover** for movement / with *Slipstream*
4. **Azure Sweep** if Eternity Surge is ≤6s away and Essence Burst isn't capped
   (2pc set bonus feed)
5. **Eternity Surge** — Rank 1
6. **Tip the Scales** when Fire Breath is ready → instant Fire Breath
7. **Fire Breath** — Rank 1
8. **Deep Breath** again for the *Imminent Destruction* AoE dump (when Pyre is the
   spender)
9. **Mass Disintegrate** cleave — chain Disintegrate while `mass_disintegrate`
   stacks are up (target the lowest *Bombardments* remaining)
10. **Pyre** when no Mass Disintegrate stacks and Pyre is the chosen spender
11. **Disintegrate** — normal chain spender (most Fire Breath DoT remaining)
12. **Azure Sweep** → **Living Flame** (Burnout/Leaping/Ancient procs) → green
    spell (Emerald Blossom/Verdant Embrace to arm *Ancient Flame* out of Dragonrage)
    → **Azure Strike**

Icy Veins SC note: "Deep Breath on cooldown, then a second cast ~7–8s later after
spending ≥2 charges of Imminent Destruction; Fire Breath and Eternity Surge always
at Empower Rank 1."

## Empower-rank selection (`es` sub-list)

Eternity Surge rank scales with target count (doubled per rank by *Eternity's
Span*):

- **Rank 1** — 1 target (or ≤`1+span`), or inside Dragonrage, or Scalecommander/Mass Disint.
- **Rank 2** — ≤`2+2×span` targets.
- **Rank 3** — ≤`3+3×span` targets.
- **Rank 4** — ≤`4+4×span` targets (max spread).

Fire Breath is empowered to Rank 1 in the standard rotation; higher ranks come
from Tip the Scales or very wide pulls.

## AoE / cleave (Flameshaper — `aoe_fs`, 3+ targets)

1. **Hover** if movement in <6s (and ≤4 targets)
2. **Fire Breath** (Rank 1) — get the DoT up before Dragonrage; refresh with
   *Consume Flame* logic
3. **Tip the Scales** during Dragonrage → Eternity Surge
4. **Dragonrage** (highest-time-to-die target)
5. **Eternity Surge** via the `es` rank table (spread across targets)
6. **Pyre** — when `charged_blast` is stacked (≥12), or at 4+ targets, or 3
   targets with *Feed the Flames*/*Volatility*
7. **Deep Breath** with *Imminent Destruction* (dump when no Fire Breath DoT out)
8. **Azure Sweep** (highest-health target)
9. **Living Flame** with *Leaping Flames* (to feed Essence Burst before Fire Breath)
10. **Azure Strike** filler

**Scalecommander AoE**: leads with Eternity Surge → **Mass Disintegrate** →
Deep Breath ×2 → Dragonrage → Fire Breath → Mass Disintegrate → Pyre. method.gg:
"Mass Disintegrate has higher priority than Pyre at any target count, but **weave
a Pyre between Mass Disintegrate casts** to build *Charged Blast*."

## Openers

**Scalecommander (ST):** precast Hover → precast Living Flame → **Dragonrage**
(potion) → **Tip the Scales** + on-use trinket → **Fire Breath** → **Eternity
Surge** → **Deep Breath ×2** → **Mass Disintegrate** → chain Disintegrate.

**Flameshaper (ST):** precast Living Flame → **Dragonrage** (potion + trinket) →
**Fire Breath** (Rank 1) → **Tip the Scales** → **Eternity Surge** (Rank 1) →
chain Disintegrate → **Fire Breath** (2nd charge) → chain Disintegrate.

## Hero-tree branch summary

- **Scalecommander** (meta): Deep Breath is a rotational button; empowers feed
  **Mass Disintegrate** cleave; keep *Strafing Run* up and weave Pyre for
  *Charged Blast*. Best all-rounder, strongest on target swaps.
- **Flameshaper**: a **2nd Fire Breath charge** — don't sit on both charges; stagger
  them to keep the DoT rolling for **Consume Flame** to detonate. **Engulf**
  consumes the Fire Breath DoT for burst. Excels at concentrated AoE, weaker when
  swapping.

## TODO

- [ ] Re-distill numeric empower/Essence-Burst weights once a 12.0.7-tagged simc
      re-sim is published (current APL string matches build 12.0.5/12.0.7 tree).
- [ ] Sanity-check the opener against a top WCL log (`wowkb.wcl rankings` →
      `casts`) once encounter IDs for S1 are wired up.
- [ ] Confirm exact CDs / cast times flagged @verify-ingame in `abilities.md`.
