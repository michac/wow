---
title: Subtlety Rogue — Rotation (Midnight Season 1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight branch profiles/MID1/MID1_Rogue_Subtlety.simc  # tier 1 APL — primary rotation source
  - https://www.method.gg/guides/subtlety-rogue/playstyle-and-rotation  # tier 3, 12.0.7 — priority corroboration + openers
  - https://www.wowhead.com/guide/classes/rogue/subtlety/rotation-cooldowns-pve-dps  # tier 4, 12.0.7 (author fuu1, upd 2026-06-18) — corroboration
confidence: medium
---

# Subtlety Rogue — Rotation (Midnight S1)

Distilled from the SimulationCraft default APL (**Tier 1**), corroborated
against method.gg (Tier 3). Subtlety is a **Shadow Dance-centric** builder/
finisher spec: you bank combo points, then unload finishers inside short
Shadow Dance windows, and stack a pair of Shadow Dance charges onto each
**Shadow Blades** use for the burst window. The APL covers **both** hero
trees — lines branch on `talent.deathstalkers_mark` (Deathstalker) vs
`talent.unseen_blade` / Supercharge (Trickster). See `builds.md` for the
tree choice (Trickster is the general recommendation).

> **Midnight changes baked into the S1 priority:** no **Rupture**, no
> **Symbols of Death** casts; **Slice and Dice** is a maintained buff, not a
> spammed button (the APL only *reads* `buff.slice_and_dice.up`). **Deepening
> Shadows** now extends Shadow Dance duration with Haste instead of reducing
> its cooldown. @verify-ingame

## Pre-combat

- Apply **poisons** (lethal + utility), buff up, snapshot.
- Enter **Stealth** before the pull.

## Cooldown rules

- **Goal: two Shadow Dance charges available for every Shadow Blades.** The
  whole cadence is "line up 2× Shadow Dance on each Shadow Blades." (method)
- **Shadow Blades** — use when your combo/CP condition is met, you have
  ≥1 Shadow Dance charge banked (≥~1.8 charges with Deathstalker), and
  **Secret Technique is ready**; also dump it if the fight/target has ≤20s
  left. Sync racials/on-use trinkets to the Shadow Blades + Shadow Dance
  overlap.
- **Shadow Dance** — enter when not already stealthed, the CP condition
  (`shd_cp`) is met, energy ≥30, and **Secret Technique is ready** (or
  Darkest Night is up) with Shadow Blades timing lined up. Also pop it to
  finish a fight (≤10s / target ≤9s).
- **Vanish** — used offensively when out of stealth with energy ≥50, no
  Subterfuge, and low combo points, to get another Shadowstrike + Find
  Weakness window.
- **Potion / racials** — inside the Shadow Blades window (or fight <30s).

## Combo-point / finisher framing

- **`shd_cp` (when to Dance/spend):** with Deathstalker, dance early — Slice
  and Dice up and **combo points ≤2** (build → Shadowstrike → Secret
  Technique from low CP); otherwise (Trickster / big AoE) dance at
  **6+ combo points**.
- **Finish at max combo points** (`cp_max_spend`; one lower while Darkest
  Night is up so an empowered Eviscerate spends sooner).

## Single-target priority

1. **Shadow Blades** / **Shadow Dance** per the cooldown rules above (open
   and re-enter their windows).
2. **Finisher** (at 6+/max combo points), in order:
   - **Eviscerate** if **Darkest Night** is up (Deathstalker's empowered
     finisher — top priority).
   - **Secret Technique** during Shadow Dance (or when its short CD lines up).
   - **Coup de Grace** (Trickster) when its CD is up / during Shadow Dance.
   - **Eviscerate** otherwise (during Dance/Shadow Blades, or with
     Deathstalker's Mark stacked).
3. **Builder** (below finisher CP):
   - **Shadowstrike** during Shadow Dance / Stealth (and to apply/refresh
     **Deathstalker's Mark** when talented).
   - **Goremaw's Bite** when combo-point deficit ≥3 (weave on CD).
   - **Backstab** (or **Gloomblade** if talented) outside stealth.

## Cleave / AoE (2 targets)

- On exactly **2 targets** the APL still favors **Shadowstrike** as the
  builder during Shadow Dance (`variable.targets<=2`); Shuriken Storm takes
  over at 3+.

## AoE (3+ targets)

1. **Shadow Blades** / **Shadow Dance** (as ST).
2. **Finisher** at max CP:
   - **Secret Technique** (during Dance / when CD aligns).
   - **Coup de Grace** (Trickster).
   - **Black Powder** on **3+ targets** (AoE finisher — applies Find
     Weakness in AoE).
3. **Builder**:
   - **Shuriken Storm** during Shadow Dance at **3+ targets** (2 targets →
     Shadowstrike).
   - **Shuriken Storm** outside Shadow Dance whenever `targets>1`.
   - **Goremaw's Bite** on CD (CP deficit ≥3).

## Opener (method)

- **Single-target:** Stealth → **Shadowstrike** → on-use trinket →
  **Shadow Dance + Shadow Blades + Secret Technique** → alternate
  Shadowstrike / Eviscerate inside the window.
- **AoE:** Stealth → **Shuriken Storm** → trinket → **Shadow Dance +
  Shadow Blades + Secret Technique** → Black Powder / Shuriken Storm cycle.

## Hero-tree branches

- **Trickster (recommended):** finishers start firing at **6+ combo
  points**; **Unseen Blade** builds **Flawless Form** stacks (+4% finisher
  damage each, up to 5) and applies **Fazed**, feeding the **Coup de Grace**
  capstone as a heavy finisher. Well-rounded ST + AoE.
- **Deathstalker (ST-leaning):** **Shadowstrike** applies **Deathstalker's
  Mark**; you **dance from low combo points** (build → Shadowstrike → Secret
  Technique), and consuming the Mark grants **Darkest Night**, making the
  next **Eviscerate** the top-priority empowered finisher. Best on
  single-target / focused encounters.

## TODO

- [x] Single-target priority — from simc MID1_Rogue_Subtlety APL 2026-07-11
- [x] AoE / cleave priority — same APL
- [x] Cooldown rules (Shadow Dance ↔ Shadow Blades pairing, Vanish) — APL
- [x] Hero-tree branch summary (Trickster / Deathstalker) — APL + method
- [ ] Confirm Rupture / Symbols of Death / Slice-and-Dice status in-game
      (APL implies removed/passive; verify) @verify-ingame
- [ ] Nail exact CDs (Shadow Dance recharge, Goremaw's Bite, Secret
      Technique) against Blizzard spell API / in-game tooltips
- [ ] Sanity-check opener vs a top WCL log (`wowkb.wcl rankings` → `casts`)
