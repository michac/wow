---
title: Evoker Preservation — Rotation & healing priority (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/preservation-evoker/playstyle-and-rotation  # tier 3, 2026-07-11 — PRIMARY (no simc healer APL exists)
  - https://www.icy-veins.com/wow/preservation-evoker-pve-healing-rotation-cooldowns-abilities  # tier 3, 2026-07-11
  - https://maxroll.gg/wow/class-guides/preservation-evoker-mythic-plus-guide  # tier 3, 2026-07-11
  - https://www.method.gg/guides/preservation-evoker  # tier 3, 2026-07-11
confidence: medium
---

# Evoker Preservation — Rotation (Midnight S1, 12.0.7)

Preservation is a **preparation healer**, not a fixed-rotation one — you read the
incoming damage pattern, **pre-build Echoes and HoTs**, then release them into the
hit. There is a maintenance layer (keep HoTs rolling) and a response layer (ramp +
dump for predictable spikes). Priorities below are distilled from **method.gg**
(primary), corroborated by Icy Veins and maxroll.

> ⚠ **No Tier-1 rotation source.** SimulationCraft does **not** model healers —
> there is no `MID1_Evoker_Preservation.simc` APL (only Devastation profiles
> exist). This priority is therefore built from Tier-3 guides that agree with one
> another; confidence is **medium**, not high. There is no shard/APL-style hard
> ordering to cite. @verify-ingame

## Core loop (the one sentence)

**Keep Reversion rolling on the whole group, double-stacked on the tank (via
Echo → Reversion), generate Essence Burst, and consume Echoes with Merithra's
Blessing / Verdant Embrace when damage lands.**

## Pre-combat / opener

- Pre-spread **Reversion** across important targets; **double-Reversion the tank**
  through **Echo → Reversion**.
- Optionally pre-cast **Temporal Anomaly** so its orb blankets weak Echoes +
  shields on the group as the pull starts.
- **Blessing of the Bronze** up on the raid; **Source of Magic** on a co-healer /
  mana user.

## Essence economy

- **Reversion** casts generate ~15% Essence Burst; **Living Flame** ~20%. Keep
  both flowing to fuel free Essence spells.
- **Spend Essence Burst on Emerald Blossom** by default (more healing per proc
  than Echo). **Exception:** if you're sitting on **2 Twin Echoes charges**, spend
  the proc on **Echo** instead so you don't waste the charges.
- On the **Energy Loop** mana build only, dump surplus Essence into **Disintegrate**
  for mana return.

## Cooldown rules

- **Rewind** — the strongest heal; fire it **right after** a big raid-wide hit
  (it heals off recent damage taken), not before.
- **Stasis** — record 3 high-impact heals, then release the stored burst into a
  known spike. Gap-filler / planned-burst tool.
- **Dream Flight** (if talented over Stasis) — big raids (20+); pre-position and
  fly through the stack.
- **Tip the Scales** — instant max-rank empower (usually into Dream Breath) as a
  panic button; in Chronowarden it also grants haste + CDR via Temporal Burst, so
  it's a *throughput* button you plan around, not just an emergency.
- **Zephyr / Time Dilation / Obsidian Scales** — spend on predictable damage; see
  Defensives below.
- **Fury of the Aspects** — the group Bloodlust; coordinate with the raid.

## Single-target / spot-heal priority

1. **Maintain double Reversion** on the target (Echo → Reversion) — Grace Period
   amp + Merithra's Blessing damage reduction.
2. **Merithra's Blessing** when available — strongest heal; bounces to lowest
   health. Default Echo finisher.
3. **Echo → Verdant Embrace** — strongest *direct* single-target combo; applies
   Lifebind.
4. **Verdant Embrace** (raw) — quick spot heal + Lifebind; triggers Twin Echoes.
5. **Dream Breath** (Rank 1) on cooldown — guaranteed Merithra's Blessing proc.
6. **Reversion** — proactively refresh; generates Essence Burst.
7. **Living Flame** — filler when nothing else is needed (keeps Essence Burst up).

## AoE / raid-healing priority

1. **Dream Breath** on cooldown (Rank 1 default) for throughput + the Merithra's
   proc; max rank only when heavy AoE healing is needed *right now*.
2. **Temporal Anomaly** on cooldown — spreads the weak-Echo + Reversion blanket
   and shields the group; reduces Dream Breath CD. **Missing Temporal Anomaly
   casts is the single biggest rotation error** (method.gg).
3. **Merithra's Blessing** to consume Echoes — especially strong with **Golden
   Hour** after recent damage.
4. **Echo ramp** before *predictable* damage: stack multiple Echoes (Temporal
   Anomaly + Emerald Blossom / Verdant Embrace for Twin Echoes), then consume with
   one big heal into the hit.
5. **Verdant Embrace** for stabilization (and to bank Twin Echoes).
6. **Reversion** maintenance across the group.
7. **Living Flame** / **Fire Breath** (Chronowarden) as Essence-Burst fillers.

**Echo finisher order** (which heal to duplicate): Merithra's Blessing →
Verdant Embrace → Dream Breath → Reversion.

## Mythic+ layer system (method.gg framing)

- **Layer 1 — Maintenance:** keep **Reversion rolling on the whole party**,
  double on the tank via **Temporal Anomaly → Reversion**.
- **Layer 2 — Damage response:** open with **Verdant Embrace** (grants Twin
  Echoes), **layer Echo setups**, then consume with a healing finisher; Verdant
  Embrace-echoed for the strongest single-target save.

> maxroll's M+ ordering leads with **max-rank Fire Breath** (for Leaping Flames /
> Life-Giver's Flame healing + DPS) ahead of Merithra's Blessing — a more
> damage-weave-forward read than method's. Both agree on the Temporal Anomaly /
> Echo / Reversion backbone; treat Fire Breath weaving as a Chronowarden DPS-uptime
> optimization on top of the heal priority.

## Hero-tree branches

- **Chronowarden (default, raid + M+):** **Tip the Scales** becomes a real
  throughput cooldown via **Temporal Burst** (haste + move speed + CDR), and
  **Chronoboon** lowers its CD so you press it often. Extra haste from **Primacy**
  tightens the **Temporal Anomaly** CD loop. Play it as a more deliberate,
  cooldown-planned spec.
- **Flameshaper (alt, +11 and lower keys):** leans into **Dream Breath / Fire
  Breath** breath interactions — steadier group HoT healing that can be converted
  into targeted burst. Weaker ceiling than Chronowarden but simpler sustained
  throughput.

## Defensives

1. **Obsidian Scales** — ~30% DR, 2 charges (triggers Renewing Blaze healing).
2. **Reversion on self** — small passive DR via Merithra's Blessing.
3. **Time Dilation** — emergency personal / ally defensive.
4. **Zephyr** — party-wide DR for stacked groups.

## Mana

If mana-starved, swap **Dream Simulacrum** or **Temporal Artificer** for **Energy
Loop** and spend excess Essence on **Disintegrate** for returns (see `builds.md`).

## TODO

- [ ] No Tier-1 APL exists (healer) — re-verify priority against a top WCL
      Preservation log (`wowkb.wcl rankings` → `casts`) for opener/CD timing.
- [ ] Confirm the Spiritbloom/Emerald Communion/Engulf removal in-game and scrub
      any lingering references. @verify-ingame
- [ ] Pull exact empower CDs (Temporal Anomaly, Dream Breath, Fire Breath) from a
      Tier-1 tooltip to firm up the cooldown-rule timings.
