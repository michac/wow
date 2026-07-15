---
title: Balance Druid — Rotation (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://github.com/simulationcraft/simc/blob/midnight/profiles/MID1/MID1_Druid_Balance.simc  # tier 1 APL (midnight branch), 2026-07-11
  - https://github.com/dreamgrove/dreamgrove/blob/master/sims/owl/balance.txt  # tier 1, APL source referenced by simc
  - https://www.method.gg/guides/balance-druid/playstyle-and-rotation  # tier 3, Midnight 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/balance-druid-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
  - https://www.wowhead.com/guide/classes/druid/balance/rotation-cooldowns-pve-dps  # tier 4, Midnight, 2026-07-11
confidence: high
---

# Balance Druid — Rotation (Midnight S1)

Distilled from the SimulationCraft **midnight** APL (`MID1_Druid_Balance.simc`,
Tier 1), corroborated against Method / Icy Veins 12.0.7 guides. Balance is a
strict-priority caster: every GCD, walk the list top-to-bottom and cast the
first applicable button.

> **Midnight Eclipse rework (read first).** Eclipse is no longer a passive that
> toggles when you alternate fillers — it is now an **activated button with
> charges**. Your **last builder arms it**: cast **Wrath** → the button becomes
> **Solar Eclipse**; cast **Starfire** → it becomes **Lunar Eclipse**. You then
> **press Eclipse** to enter that state and empower the matching filler.
> Celestial Alignment / Incarnation grant **both** Eclipses at once. The whole
> rotation is built around not overcapping Eclipse charges and lining Eclipse
> windows up with your ~2-min cooldown stack. The APL branches by hero tree
> (`kotg_st` Keeper single-target, `ec_st` Elune's Chosen single-target, `aoe`)
> and by opener vs sustain.

## Pre-combat

- **Moonkin Form**, then hard-cast **Wrath ×2** into the pull (from max range,
  ~3–4s before combat). If Dream Surge (Keeper) and single target, a 3rd Wrath;
  if Elune's Chosen or 3+ targets, open with **Starfire** instead (arms Lunar).
- Snapshot stats; pre-pot timed to land in the opener burst (see below).

## Cooldown rules

The whole point is to dump your ~2-min stack **inside an Eclipse window** and
keep **Convoke on cooldown**:

- **Stack the burst:** Force of Nature → Celestial Alignment / Incarnation →
  Convoke the Spirits, with an on-use trinket + racial (Berserking) + external
  Power Infusion all synced to the **CA/Incarnation** window. Repeat every 2 min.
- **Force of Nature first** — the APL fires CA/Incarnation on the GCD right
  after Force of Nature (Keeper: `prev_gcd.1.force_of_nature`) so Treants +
  Harmony of the Grove overlap the burst.
- **Convoke** only inside CA/Incarnation and at **< 40 Astral Power** (so its
  generation isn't wasted), or off-cooldown late if CA is > 50s away.
- **Fury of Elune:** Keeper casts it **before entering Eclipse** for AP
  generation into the window; Elune's Chosen casts it **inside** Eclipse (near
  the Atmospheric Exposure debuff refresh) — Lunation keeps shortening its CD.
- **Potion / racials / trinkets:** only while the CA/Incarnation (and Keeper's
  Harmony of the Grove) buff is up, or in the last ~30s of the fight.
- **Don't overcap** Eclipse charges or CA charges; **don't cap Astral Power** —
  a spender always beats overcapping.
- **< ~20s left on the fight:** dump everything — remaining cooldowns, Eclipse
  charges, and Astral Power into spenders.

## Single target — Keeper of the Grove (`kotg_st`)

1. **Celestial Alignment / Incarnation** right after Force of Nature (burst
   window; gated on target living long enough).
2. **Moonfire** — keep it up; refresh when it (and Harmony of the Grove) allow.
3. **Sunfire** — keep it up; refresh when it falls / outside Eclipse.
4. **Fury of Elune** — when Harmony of the Grove is up, or Force of Nature is
   about to come up / is held (Radiant Moonlight).
5. **Solar Eclipse** (enter) — when you have the charges and you're in the
   cooldown window (don't overcap charges).
6. **Force of Nature** — right before entering Eclipse or when CA/Incarnation is
   ready (and Convoke will be up too).
7. **Convoke the Spirits** — inside CA (< 40 AP) or off-cooldown w/ Harmony up.
8. **Starfall** on a **Starweaver's Warp** proc, or the wider Starfall proc
   window (Meteorites / Touch the Cosmos overlaps).
9. **Starsurge** — main Astral Power spender: at high AP, in Eclipse, or on a
   Starweaver's Weft / Touch the Cosmos proc. Don't cap AP.
10. **Ascendant / Moon fillers:** Starfire on Ascendant Fires + Lunar Eclipse;
    then the **Moon chain (New → Half → Full Moon)** to generate AP.
11. **Wild Mushroom** when in Eclipse / when it'd recharge before CA.
12. **Wrath** — generator / filler of last resort.

## Single target — Elune's Chosen (`ec_st`)

Same maintenance + cooldown spine, but **Solar Eclipse is disabled — you always
enter Lunar Eclipse** and lean on Fury of Elune (Lunation cooldown reduction) +
Atmospheric Exposure:

1. **Celestial Alignment / Incarnation** (Eclipse down, Convoke ~ready).
2. **Moonfire** / **Sunfire** — maintain (refresh when Eclipse is down).
3. **Convoke the Spirits** — in CA at < 40 AP, or off-CD late.
4. **Lunar Eclipse** (enter) whenever the target will live > 5s.
5. **Starfall** on Starweaver's Warp / Touch the Cosmos procs.
6. **Starsurge** — spend at high AP, in Eclipse, or on procs.
7. **Fury of Elune** — inside Eclipse near the Atmospheric Exposure refresh.
8. **Force of Nature**.
9. **Moon chain (New → Half → Full)** while below AP cap and Atmospheric
   Exposure is about to fall — the Moons re-apply it.
10. **Wild Mushroom**, then **Starfire** (fits inside Eclipse) → **Wrath**.

## Cleave / AoE (`aoe`, 2+ targets)

1. **Celestial Alignment** after Force of Nature (or, with Boundless Moonlight,
   when Eclipse is down and charges are ready), synced to trinkets.
2. **Eclipse** if it's about to full-recharge (don't waste a charge).
3. **Moonfire** — spread across targets (up to ~10; Treants of the Moon /
   Force of Nature help), refresh where it'll live.
4. **Sunfire** — apply/refresh (its spread is free AoE).
5. **Fury of Elune** — Elune's Chosen always; Keeper when Harmony is up / Force
   of Nature is imminent.
6. **Force of Nature** — before Eclipse / with CA, spreads Moonfire to ~8.
7. **Convoke the Spirits** — in CA at < 40 AP.
8. **Starsurge** on a Starweaver's Weft proc.
9. **Starfall** — the primary AoE spender: at high AP, in Eclipse, or on a
   Touch the Cosmos / Starweaver's Warp proc. Don't cap AP on 2+ targets.
10. **Moon chain (New → Half → Full)** to generate, refreshing Atmospheric
    Exposure (Elune's Chosen).
11. **Wild Mushroom** in Solar Eclipse / before CA.
12. **Filler:** **Starfire** (≤3 targets in Lunar/CA, and the AoE generator on
    4+) → **Wrath** (Solar filler, ≤3 targets).

**Eclipse-side rule for AoE:** enter **Solar Eclipse + Wrath filler up to and
including 3 targets**; enter **Lunar Eclipse + Starfire filler on 4+ targets**.
Elune's Chosen enters **Lunar for every situation**.

## Hero-tree branches (summary)

- **Keeper of the Grove** (raid / ST, and spread cleave): Force-of-Nature-centric
  burst — overlap **Harmony of the Grove** with CA/Incarnation + Convoke +
  Fury of Elune, Treants of the Moon adds Moonfire spread. Cast Fury of Elune
  **before** Eclipse for AP.
- **Elune's Chosen** (Mythic+ / sustained AoE): **Solar Eclipse disabled — always
  Lunar**; maintain cast uptime so **Lunation** shortens Fury of Elune, and keep
  **Atmospheric Exposure** on target (Fury of Elune / Moon chain refresh it).
  Simpler CD management without Convoke alignment.

## TODO

- [x] ST priority (Keeper + Elune's Chosen) — from simc midnight APL 2026-07-11
- [x] AoE priority — from simc midnight APL 2026-07-11
- [x] Eclipse-as-button rework captured (Wrath→Solar / Starfire→Lunar)
- [x] Cooldown stacking + hero-tree branches
- [ ] Sanity-check opener vs a top WCL log (`wowkb.wcl rankings` → `casts`)
- [ ] Confirm exact Eclipse charge count / recharge + CA charges in-game
      (@verify-ingame in `abilities.md`)
