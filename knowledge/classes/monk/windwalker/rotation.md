---
title: Windwalker Monk — Rotation (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Monk_Windwalker.simc  # tier 1 APL, WoW 12.0.x, fetched 2026-07-11
  - https://www.method.gg/guides/windwalker-monk/playstyle-and-rotation  # tier 3, upd. 2026-06-16, priority corroboration
  - https://www.icy-veins.com/wow/windwalker-monk-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7
confidence: high
---

# Windwalker Monk — Rotation (Midnight S1)

Distilled from the SimulationCraft default APL (Tier 1: `actions.default_st`,
`actions.multitarget`, `actions.zenith`, `actions.big_coc`) and corroborated
against the Method 12.0.7 guide. Windwalker plays a **priority list, not a fixed
rotation** — always take the highest-priority ready ability, and never delay a
higher-priority button for a lower one.

**The two rules underneath everything:**
- **Combo Strikes (Mastery):** never cast the same ability twice in a row — you
  lose a large damage buff. In the APL this is the ubiquitous `combo_strike`
  gate; in practice, alternate builders and spenders.
- **Don't cap resources:** feed **Tiger Palm** in whenever Energy is about to cap
  or Chi is low; spend Chi before it caps. Tiger Palm is the lowest-priority
  filler that keeps both resources flowing without breaking Combo Strikes.

> **Hero-tree split.** The APL branches on `talent.celestial_conduit` (Conduit of
> the Celestials) vs `talent.flurry_strikes` (Shado-Pan). Conduit adds the
> **Celestial Conduit** channel and the **Heart of the Jade Serpent** proc that
> reorders priorities; Shado-Pan folds **Flurry Strikes** in and runs a faster
> **Zenith** cadence. Both share the same core builders/spenders — see the
> hero-tree branches at the bottom.

## Pre-combat

- `snapshot_stats`; pre-pot per the APL (`potion` fires when Xuen will be up >15s,
  or for Flurry Strikes on an early-Zenith opener).
- **Opener** (`actions.opener`, `time<2`): **Tiger Palm** to seed Chi
  (`combo_strike&chi<4`), then trinket use (e.g. Algeth'ar Puzzle Box) lined up
  with Invoke Xuen / Zenith coming off cooldown.

## Cooldown rules

- **Invoke Xuen, the White Tiger** is the burst anchor — open with it and sync
  **potion, racials, and on-use trinkets** into the Xuen window (the APL gates
  `potion`/`berserking`/`blood_fury` on `buff.invoke_xuen_the_white_tiger.remains`).
- **Zenith** is the flexible primary cooldown. The APL fires it when Xuen is up
  (`buff.invoke_xuen_the_white_tiger.up`), on Bloodlust, and otherwise when
  Fists of Fury + (Strike of the Windlord / Whirling Dragon Punch) are about to
  be available so the window is fed. Its cooldown shrinks via **Spiritual Focus**
  (Conduit) or **Efficient Training** (Shado-Pan) — hence method's cadences of
  ~2:00/1:30 (Conduit) or ~1:30/1:20/1:00 (Shado-Pan).
- **Celestial Conduit** (Conduit only): cast it when **Heart of the Jade Serpent
  is NOT active** (`!buff.heart_of_the_jade_serpent.up`) and Zenith is up — timing
  matters, don't cast it early over an active Heart window.
- **Touch of Death** on cooldown, generally outside the Zenith burst
  (`if=!buff.zenith.up`) unless the fight is ending.
- **Trinkets** sync to the Xuen/Zenith window; Algeth'ar Puzzle Box is pre-used.
- End-of-fight (`fight_remains<...`): dump Zenith, Celestial Conduit, Touch of
  Death, and spare Chi rather than banking a lost use.

## Single target (`actions.default_st`, Conduit framing)

The Method-summarized order (matches the APL's spirit):

1. **Fists of Fury** if Heart of the Jade Serpent has ≤1s left (don't waste the proc)
2. **Touch of Death**
3. **Celestial Conduit** if Heart of the Jade Serpent is inactive (Conduit only)
4. **Whirling Dragon Punch** (if talented)
5. **Tiger Palm** if <4 Chi / <2 Blackout Kick stacks / about to cap Energy
6. **Strike of the Windlord** (if talented)
7. **Fists of Fury**
8. **Rushing Wind Kick** (if talented)
9. **Spinning Crane Kick** with a **Dance of Chi-Ji** proc about to expire (not at 2 stacks)
10. **Rising Sun Kick**
11. **Zenith Stomp** during Zenith when higher-priority strikes are ready but Chi is short
12. **Tiger Palm** when higher strikes are ready but Chi is short
13. **Blackout Kick** with a **Blackout Kick!** (Combo Breaker) proc
14. **Slicing Winds** (if talented)
15. **Zenith Stomp** during Zenith
16. **Spinning Crane Kick** with a Dance of Chi-Ji proc
17. **Blackout Kick**
18. **Tiger Palm**

> Inside Zenith, skip the "top-up" Tiger Palm and the low-value Spinning Crane
> Kick when talented into **Obsidian Spiral** — the goal is to **minimize Tiger
> Palm casts inside cooldowns** and spend Chi on real damage.

## Cleave / AoE (`actions.multitarget`)

Same skeleton; the spender emphasis shifts to **Spinning Crane Kick** and the
cone/AoE hitters (Fists of Fury, Whirling Dragon Punch, Strike of the Windlord).
Method's Conduit AoE order:

1. **Fists of Fury** if Heart of the Jade Serpent ≤1s left
2. **Touch of Death** (on the lowest-time-to-die add is fine)
3. **Celestial Conduit** if no active Heart of the Jade Serpent
4. **Whirling Dragon Punch** (if talented)
5. **Tiger Palm** to keep Chi/Energy flowing (<4 Chi, about to cap Energy)
6. **Strike of the Windlord** (if talented)
7. **Fists of Fury**
8. **Rushing Wind Kick** (if talented)
9. **Spinning Crane Kick** with a Dance of Chi-Ji proc about to expire
10. **Rising Sun Kick**
11. **Tiger Palm** / **Zenith Stomp** when higher strikes are ready but Chi is short
12. **Blackout Kick** with a Combo Breaker proc
13. **Slicing Winds** (if talented)
14. **Spinning Crane Kick** with a Dance of Chi-Ji proc
15. **Zenith Stomp** during Zenith
16. **Blackout Kick** → **Spinning Crane Kick** → **Tiger Palm** as filler

Notes from the APL: at higher target counts Rising Sun Kick is de-prioritized
while Fists of Fury is off cooldown; **Spinning Crane Kick** becomes the dominant
Chi dump (especially with **Shadowboxing Treads** cleaving Blackout Kicks, and
with two banked **Dance of Chi-Ji** stacks). Touch of Death targets the add that
will die soonest.

## Hero-tree branches

### Conduit of the Celestials (`talent.celestial_conduit`)
- Adds **Celestial Conduit** — a channeled nuke cast in the Zenith window when
  **Heart of the Jade Serpent** is down; can be cancelled early if you must move.
- **Heart of the Jade Serpent** procs re-order the priority: Fists of Fury jumps
  up when the proc is about to fall off, and it speeds Fists channels — the
  rotation visibly accelerates during a Heart window.
- **Zenith Stomp** and extra Tiger Palms are used to keep Chi fed through the
  faster Conduit windows.

### Shado-Pan (`talent.flurry_strikes`)
- Built around **Flurry Strikes** — spending resources accrues charges that
  discharge as bonus strikes; the APL keeps resources moving to feed it and
  fires **Fists of Fury** more freely (`talent.flurry_strikes` short-circuits
  many of the Zenith/Xuen gates).
- Runs a **tighter, more frequent Zenith** (Efficient Training CDR) — the
  `actions.zenith` list has many Flurry-specific early-Zenith lines keyed off
  **Tigereye Brew** stacks and Bloodlust.
- No Celestial Conduit; Blackout Kick and Spinning Crane Kick see more use inside
  Zenith (the APL adds `buff.zenith.up` Blackout/Spinning lines for Shado-Pan).

## Defensives & utility (press reactively)

- **Touch of Karma** — pre-cast before a known spike, or bottom out and use it to
  stall for heals; can also be used offensively as a damage cooldown.
- **Fortifying Brew** — hard panic button (big CD).
- **Diffuse Magic / Dampen Harm** (if talented) — magic / big-hit mitigation.
- **Spear Hand Strike** — interrupt (APL: `if=target.debuff.casting.react`).
- **Leg Sweep** (AoE stun), **Paralysis** (single-target CC), **Ring of Peace /
  Song of Chi-Ji** — control.
- **Roll / Chi Torpedo**, **Flying Serpent Kick**, **Tiger's Lust**,
  **Transcendence: Transfer**, **Slicing Winds** — mobility (the APL uses
  Roll/Chi Torpedo/Flying Serpent Kick when `movement.distance>5`).
- **Detox** — poison/disease cleanse.

## TODO

- [ ] Sanity-check the opener against a top WCL log (`wowkb.wcl rankings` →
      `casts`) once S1 logs are pulled.
- [ ] Confirm exact Zenith / Celestial Conduit / Touch of Death cooldowns and the
      Rushing Wind Kick / Zenith Stomp mechanics in-game (@verify-ingame markers
      in `abilities.md`).
- [~] Re-distill if the simc midnight branch publishes a retuned 12.0.7 WW APL.
