---
title: Hunter Survival — Rotation (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight branch profiles/MID1/MID1_Hunter_Survival.simc + engine/class_modules/apl/hunter/sv.txt  # tier 1 APL, commit 9cedf7c 2026-07-12, WoW 12.0.7 (profile: MID1_Hunter_Survival_PL_DW)
  - https://www.method.gg/guides/survival-hunter/playstyle-and-rotation  # tier 3, Midnight 12.0.7 (upd. 2026-06-17)
  - https://hackmd.io/@Azortharion/MidnightHunterChanges  # tier 3, Midnight SV redesign notes
confidence: medium
---

# Hunter Survival — Rotation (Midnight S1)

Distilled from the SimulationCraft default APL (Tier 1). The simc default
profile is **Pack Leader, dual-wield** (`MID1_Hunter_Survival_PL_DW`); the APL
branches by **hero tree** (Pack Leader vs Sentinel) × **enemy count** (1–2 vs
3+). Method.gg corroborates the ordering.

The whole spec runs on two loops: **Kill Command → Tip of the Spear** (build the
buff, then spend it on everything else) and **Raptor Strike → Mongoose Fury**
(each Raptor Strike amps the next). **Takedown** is the ~90s burst window
(+20% damage, 8s) that every cooldown and racial lines up behind.

## Pre-combat

- **Summon pet**, snapshot stats.
- Pre-cast **Wildfire Bomb** if pulling a single target (ST opener only).
- Pull with **Takedown** (charges in, +20% window, 50 Focus) → **Boomstick** /
  **Wildfire Bomb** / **Kill Command** to establish Tip of the Spear.

## Cooldown rules (APL `cds`)

- **Takedown is the burst anchor.** Fire on-use trinkets, potion, and
  DPS racials (Blood Fury / Berserking / Fireblood / Ancestral Call) **when
  Takedown is up or ready** (`buff.takedown.up | cooldown.takedown.ready`).
- **External Power Infusion** (if handed one) goes on the Takedown window.
- **Potion**: on Takedown, or when `target.time_to_die < 25`.
- **Muzzle** whenever an interrupt is needed (lives in the CD list, high value).
- **Aspect of the Eagle** when the target is **≥6 yds away** — the forced-ranged
  / melee-downtime tool so you never idle out of melee.
- **Boomstick** and **Flamefang Pitch** are short cooldowns woven into the
  priority (below), not held for Takedown specifically — but they hit hardest
  when tipped inside the window.

## Single target — Pack Leader (APL `plst`)

1. **Kill Command** — if `<2` Tip of the Spear stacks **and** a Howl beast
   summon is ready (keeps Howl fed).
2. **Kill Command** — if Takedown comes off CD within a GCD and `<2` Tip stacks
   (and not talented into *Twin Fangs*) — pre-load Tip before the burst.
3. **Takedown** — with a Tip stack up (or, with *Twin Fangs*, at 0 Tip stacks).
4. **Flamefang Pitch**.
5. **Wildfire Bomb** — while Tip of the Spear is up (with *Lethal Calibration*,
   only when about to cap charges).
6. **Boomstick** — while Tip of the Spear is up.
7. **Raptor Strike** — while Tip is up, or when *Raptor Swipe* isn't buffed.
8. **Wildfire Bomb** — while Tip is up (second window).
9. **Kill Command** — as filler while Takedown is still on cooldown.
10. **Takedown** (fallback).

## Single target — Sentinel (APL `sentst`)

1. **Kill Command** — at 0 Tip stacks (when Takedown is on CD, or not *Twin Fangs*).
2. **Boomstick** — tipped, when **Sentinel's Mark** is *not* active.
3. **Wildfire Bomb** — tipped, when Sentinel's Mark is up or charges about to cap.
4. **Kill Command** — Takedown within a GCD and `<2` Tip stacks (no *Twin Fangs*).
5. **Takedown** — with Tip stacks (or at 0 stacks with *Twin Fangs*).
6. **Boomstick** — tipped (fallback).
7. **Moonlight Chakram** — tipped.
8. **Flamefang Pitch**.
9. **Raptor Strike** — tipped, or when *Raptor Swipe* isn't buffed.
10. **Kill Command** filler → **Takedown** fallback.

## AoE / cleave (3+ targets)

**Pack Leader (`plcleave`):**
1. **Kill Command** — `<2` Tip stacks while a Howl beast (Wyvern/Boar/Bear) buff is up.
2. **Kill Command** — Takedown within a GCD, `<2` Tip stacks (no *Twin Fangs*).
3. **Takedown** — with Tip stacks (*Flanked* makes it cleave + grant attack speed).
4. **Flamefang Pitch**.
5. **Wildfire Bomb** — when about to cap charges (`full_recharge_time < gcd`).
6. **Boomstick** — tipped.
7. **Wildfire Bomb** — tipped.
8. **Raptor Strike / Raptor Swipe** — tipped, or when Raptor Swipe isn't buffed
   (Raptor Swipe is the apex talent that makes the spender cleave up to 5).
9. **Kill Command** filler → **Wildfire Bomb** → **Takedown**.

**Sentinel (`sentcleave`):** same shape, but Boomstick/Wildfire Bomb timing keys
off **Sentinel's Mark** and Boomstick's cooldown (with *Wildfire Shells*), and
**Moonlight Chakram** slots in after Takedown. Raptor Strike is spent tipped
when Raptor Swipe is up (or whenever Raptor Swipe isn't buffed).

## Hero-tree branches (summary)

- **Pack Leader** (default, dual-wield daggers): Kill Command is gated on
  **Howl of the Pack Leader** beast readiness — you're weaving Kill Command to
  keep the Boar/Bear/Wyvern summons rolling. Higher Focus regen from dual-wield
  auto-attacks (+ *Lethal Barbs*) pays for the extra Raptor Strikes.
- **Sentinel** (2H): revolves around **Sentinel's Mark** windows and the
  **Moonlight Chakram** button; more defensive, slightly behind on raw DPS in
  S1 (see `builds.md`). Boomstick/Wildfire timing is Sentinel's-Mark-driven.

## Core mechanics to keep straight

- **Never let Tip of the Spear sit unused at 2 stacks** — Kill Command refills
  it, everything else spends it. The `<2 stacks` Kill Command lines exist purely
  to avoid capping/wasting it.
- **Raptor Strike maintains Mongoose Fury** — during Takedown especially, chain
  Raptor Strikes to stack the self-buff (Azortharion's window sketch:
  `WFB > Pitch/Boomstick > Takedown > RS×several > KC > RS`).
- **Wildfire Bomb recharges faster the more targets it hits** — in AoE it's an
  almost-on-cooldown button; in ST it's Tip-gated.

## TODO

- [ ] Re-distill numeric Focus costs / exact cooldowns from live tooltips
      (@verify-ingame flags in `abilities.md`) once confirmed in-game.
- [ ] Sanity-check the opener vs a top WCL Survival log (`wowkb.wcl rankings`
      → `casts`).
- [ ] Confirm Sentinel is genuinely behind Pack Leader in current S1 tuning
      (Tier-3 guides agree as of 2026-06-17; re-verify after any hotfix).
