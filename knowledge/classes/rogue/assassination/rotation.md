---
title: Assassination Rogue — Rotation (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight branch profiles/MID1/MID1_Rogue_Assassination.simc  # tier 1 APL (default profile runs Deathstalker), fetched 2026-07-11
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Rogue_Assassination.simc  # tier 1
  - https://www.method.gg/guides/assassination-rogue/playstyle-and-rotation  # tier 3, upd. 2026-06-16
  - https://www.icy-veins.com/wow/assassination-rogue-pve-dps-rotation-cooldowns-abilities  # tier 3, upd. 2026-06-15
confidence: high
---

# Assassination Rogue — Rotation (Midnight S1)

Distilled from the SimulationCraft default APL (Tier 1), corroborated with
Method and Icy Veins (Tier 3). The whole spec is about **keeping Garrote and
Rupture up, holding the Envenom buff, and dumping burst into the Deathmark +
Kingsbane window every 2 minutes.** Most damage is passive DoT ticks; the
active priority just refuels those DoTs and spends combo points on Envenom.

> **Hero-tree note:** the simc default profile is built around **Deathstalker**
> (`deathstalkers_mark` / `buff.darkest_night` / `shiv`+`toxic_stiletto`), and
> Deathstalker sims ahead. **Method recommends Fatebound** for its far better
> quality of life (a fully passive coin-flip package with no mark bookkeeping).
> The core loop below is identical either way; the Deathstalker-only additions
> are called out. See `builds.md`.

## Pre-combat

- **Apply poisons** (lethal + non-lethal) before the pull.
- **Stealth**, then pre-cast **Slice and Dice** (`slice_and_dice,precombat_seconds=1`).
- Set trinket-sync variables (simc auto-syncs a use-trinket to the Deathmark window).

## Cooldown rules

- **Deathmark** (2 min) is the anchor burst window. The APL fires it only when
  **both Garrote and Rupture are ticking, Kingsbane is ≤2s away, the Envenom
  buff has >2s left**, and the target will live >10s (or the fight is nearly
  over). Doubles bleeds + poisons for its duration.
- **Kingsbane** (1 min) is cast **into / synced with** Deathmark so its stacks
  ramp twice as fast (poison applications are duplicated). The APL requires
  Garrote + Rupture ticking, Envenom buff up, and Deathmark active or >52s out.
- **Trinkets / potion / racials** all fire under `debuff.deathmark.up` — sync
  everything to the 2-min window; don't bank a use past a lost cast.
- **Thistle Tea** is used for energy when it's low (`energy.pct<50` late in a
  fight, or generally to sustain during Kingsbane). Multi-charge.
- **Vanish** is a rotational button here: re-apply **Improved Garrote** on a
  single target when Garrote isn't already empowered (`pmultiplier<=1`) and
  Deathmark is up or further out than the target will live — i.e. refresh a
  strong Garrote right before/into the burst window.

## Single target

Maintain, then spend. In priority order (simc `core_dot` → `generate` → `spend`):

1. **Garrote** — keep it up; empowered from Stealth / Improved Garrote. Refresh
   when it will fall off and the target lives >12s longer than its remaining.
2. **Rupture** — refresh at **5+ CP** when refreshable and target lives >12s.
3. **Deathmark** on cooldown (gated on both bleeds up + Kingsbane ~ready +
   Envenom buff up — see cooldown rules).
4. **Kingsbane** on cooldown, synced with Deathmark.
5. **Envenom** at **5+ CP** — the primary spender; keeps the Envenom buff up.
   *(Deathstalker: cast at **7 CP** while **Darkest Night** is active for the
   massively-empowered Envenom.)*
6. **Ambush** when usable (from Stealth or via a **Blindside** proc).
7. **Mutilate** as the default combo-point builder (fills to 5 / to 7 under
   Darkest Night).
8. *(Deathstalker)* **Shiv** at 6 CP when Darkest Night is available (with
   Toxic Stiletto) to add poison stacks.

Deathstalker's Mark loop (Deathstalker only): **Garrote applies the Mark**;
each Envenom consumes a stack; when the last stack is consumed you gain
**Darkest Night**, which supercharges your next Envenom (cast at 7 CP) and
re-applies the Mark to that target. Keep near-100% Mark uptime; use **Mark for
Death** to move the Mark when swapping targets before a Darkest Night proc.

## Cleave / AoE (2+ targets)

Opener: **Vanish** (if not stealthed) → double **Garrote** application →
**Rupture** at 5+ CP → cooldowns + potion → **Crimson Tempest** to spread
bleeds → **Envenom**. Then, in priority:

1. **Crimson Tempest** — cast to spread Garrote/Rupture bleeds to enemies that
   lack them (the APL fires it when active bleeds < target count and Rupture
   has >5s or energy regen is high). This is the Midnight AoE engine.
2. **Garrote** — maintain the Mark / bleed on the primary; multi-dot key
   targets that will live (cycle_targets when not running Crimson Tempest).
3. **Rupture** at 5+ CP on the primary (Crimson Tempest carries it to the rest).
4. **Deathmark** + **Kingsbane** on cooldown as in ST.
5. **Fan of Knives** as the AoE builder once every target has bleeds — hits
   all, generates CP, applies poisons.
6. **Envenom** at 5+ CP (7 CP under Darkest Night) — still the spender.
7. **Shiv** at 6 CP under Darkest Night (Deathstalker, ≤3 targets).

Rule of thumb from the APL: use **Fan of Knives** as the builder on 2+ targets
(`spell_targets>1+talent.blindside`); on a single target you fall back to
Ambush/Mutilate. Crimson Tempest is the bleed-spreader, Fan of Knives is the
CP-and-poison filler once the pack is bleeding.

## Hero-tree branches

- **Deathstalker** (simc default, higher ceiling): adds the **Deathstalker's
  Mark → Darkest Night** layer — spend Envenoms to build to a Darkest Night
  proc, then dump a 7-CP empowered Envenom (and Shiv at 6 CP). Watch
  `buff.unshakeable_drive` stacks: the APL prefers Mutilate over Ambush until
  3+ stacks (or Bloodlust). Highest damage, highest bookkeeping.
- **Fatebound** (Method default, best QoL): **fully passive** — 5+ CP finishers
  flip a coin that always helps (extra Envenom damage, Caustic Spatter boosts).
  No Mark management. Same maintain-bleeds → Envenom loop without the Darkest
  Night 7-CP timing; simpler, slightly lower ceiling.

## TODO

- [x] Single-target + AoE priority — from simc APL (Deathstalker default) 2026-07-11
- [x] Cooldown sync rules (Deathmark ↔ Kingsbane ↔ trinkets) — simc APL
- [ ] Verify Crimson Tempest reworked behaviour + Shiv/Toxic Stiletto in-game
- [ ] Sanity-check opener vs a top WCL log (`wowkb.wcl rankings` → `casts`)
- [ ] Re-distill if simc publishes a Fatebound-default profile (current default
      is Deathstalker; Method runs Fatebound for QoL)
