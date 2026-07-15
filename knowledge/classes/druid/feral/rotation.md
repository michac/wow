---
title: Feral Druid — Rotation (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Druid_Feral.simc  # tier 1 APL (Wildstalker default), talent string, 2026-07-11
  - https://www.method.gg/guides/feral-druid/playstyle-and-rotation  # tier 3, 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/feral-druid-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
confidence: high
---

# Feral Druid — Rotation (Midnight S1)

Feral is a two-resource builder/spender: build **Combo Points** with
Shred/Rake/Swipe while spending **Energy**, then dump 5 CP into
Rip/Ferocious Bite/Primal Wrath. The whole spec is organized around
**bleed uptime** and **snapshotting** — a bleed applied or refreshed while
**Tiger's Fury** is up is frozen at that buffed strength for its full
duration, so DoTs are deliberately refreshed *inside* Tiger's Fury / Berserk
windows and never clipped outside pandemic range. The single-target APL below
is the simc **Wildstalker** default (Tier 1); method.gg / Icy Veins (Tier 3)
corroborate and add the Druid of the Claw AoE colour.

> **Golden rules (both guides):** finishers only at **5 combo points**;
> **pool to ~50 Energy before Ferocious Bite** so you spend the full 50; keep
> **Rake and Rip up at all times**; refresh bleeds only in **pandemic range**
> (last ~30% of duration) unless a Tiger's Fury snapshot makes clipping a net
> gain. "Never clip Rip."

## Pre-combat

- **Cat Form**, **Prowl**.
- Pre-pull **Tiger's Fury** (grants the Unseen Predator buff + 50 Energy
  immediately) and, if used, a pre-pot / on-use trinket (Algeth'ar Puzzle
  Box).

## Cooldown rules

- **Tiger's Fury on cooldown** (30s) — but only with room to spend the 50
  Energy it grants (ST: ~5 CP or 50 Energy below cap; AoE: ~70 Energy below
  cap). It's the snapshot anchor: refresh Rip/Rake inside its window.
- **Berserk** (or Incarnation) **synced to Tiger's Fury**; hold it a few
  seconds rather than desync from Tiger's Fury / Convoke.
- **Feral Frenzy** (and the **Frantic/Focused Frenzy** talent) on cooldown,
  lined up with Tiger's Fury.
- **Convoke the Spirits** always cast **inside Berserk + Tiger's Fury**, with
  Rip already on the target — it's the single biggest burst button, so never
  fire it naked. (Ashamane's Guidance halves its CD to 1 min.)
- Potion / racials / trinkets ride the **Berserk + Tiger's Fury** burst window.

## Single target (Wildstalker default APL)

Cooldowns first (see above), then, top-down:

1. **Ferocious Bite** the instant **Apex Predator's Craving** procs (free,
   full-damage Bite — jumps the queue). With Druid of the Claw this is
   **Ravage** when the proc is up.
2. **Rip** if missing or in pandemic range — 5 CP, **prefer refreshing it
   under Tiger's Fury** to snapshot. Never clip it early.
3. **Ferocious Bite** at **5 CP and ≥50 Energy** with Rip active (Sabertooth
   also extends Rip).
4. **Shred** with a **Sudden Ambush** proc (Midnight: Sudden Ambush no longer
   snapshots Rake, so spend it on Shred in ST).
5. **Rake** if missing or in pandemic (clip only if the new one is stronger —
   Tiger's Fury snapshot).
6. **Moonfire** if talented **Lunar Inspiration** and missing/pandemic (third
   bleed layer, also builds a CP).
7. **Shred** to build combo points (filler).

> **Panther's Guile (Midnight):** builders can proc extra Ferocious Bites —
> watch combo points and weave the free Bite instead of blindly queueing two
> Shreds in a row.

## Cleave / AoE (2+ targets)

Cooldowns first (Tiger's Fury, Berserk, Feral/Frantic Frenzy, Convoke), then:

1. **Ferocious Bite / Ravage** on an **Apex Predator's Craving** proc.
2. **Primal Wrath** at 5 CP when Rip is missing or in pandemic on the pack —
   it applies/refreshes Rip to **all** targets in range (the AoE Rip button).
3. **Ferocious Bite** at 5 CP + ≥50 Energy once Rips are out.
4. **Rake** on targets lacking it (up to the Rake target cap — see below).
5. **Swipe during Berserk** to feed **Claw Rampage / Ravage** (Druid of the
   Claw only).
6. **Swipe** with a **Clearcasting** (Omen of Clarity) and/or Sudden Ambush
   proc.
7. **Rake** refresh in pandemic; **Moonfire** cycle (Lunar Inspiration).
8. **Swipe** to build combo points (filler).

**Rake vs Swipe target cap** — above the cap, stop casting Rake and build
purely with Swipe:
- **Wildstalker / Double-Clawed Rake:** Rake on **all** targets, any count.
- **Druid of the Claw:** cap depends on **Infected Wounds** / **Wild Slashes**
  — 3 / 5 / 8 enemies (no-IW+WS → 3; base → 5; IW only → 8; IW+WS → 5). Beyond
  the cap, Swipe only.

## Openers

**Single target:** Prowl → (pre-pull Tiger's Fury) → Rake → Berserk →
Feral Frenzy (+ Frantic Frenzy) → Rip → Convoke the Spirits → Ferocious Bite
→ into the priority. (With Lunar Inspiration: apply Moonfire after Rip, rebuild
to 5 CP, Bite before Convoke.)

**AoE:** Prowl (optional) → Rake multiple targets to 5 CP → trinket →
Tiger's Fury → **Primal Wrath** → Berserk → Frantic/Feral Frenzy → Ravage →
Ferocious Bite → Convoke → into the priority.

## Hero-tree branches

- **Wildstalker (raid / single-target, simc default):** Rake/Rip ticks grow
  **Bloodseeker Vines** — maximize bleed uptime; every Tiger's Fury aims to
  re-snapshot Rip (and Rake). ~4% ahead on pure ST. Also stacks self-healing
  via **Symbiotic Bloom** Regrowths.
- **Druid of the Claw (Mythic+ / AoE):** auto-attacks + Berserk build
  **Ravage** procs (cone-AoE empowered Bite via **Claw Rampage**); Swipe
  during Berserk feeds it. Better cleave + defensives; the M+ default.

## TODO

- [x] ST priority — simc midnight APL (Wildstalker) 2026-07-11 + method/Icy Veins
- [x] AoE priority + Rake/Swipe caps — method.gg 12.0.7 2026-07-11
- [x] Cooldown sync rules (Tiger's Fury / Berserk / Convoke) — all three sources
- [ ] Sanity-check opener vs a top WCL Feral log (`wowkb.wcl rankings` → `casts`)
- [ ] Re-verify Midnight-new interactions in game (Unseen Predator buff,
      Panther's Guile double-Bite, Ravage proc conditions) @verify-ingame
