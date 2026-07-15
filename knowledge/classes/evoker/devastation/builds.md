---
title: Devastation Evoker — Talents & Builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Evoker_Devastation.simc  # tier 1 default SC talent string, 2026-07-11
  - https://www.method.gg/guides/devastation-evoker/talents  # tier 3, 12.0.7 (upd. 2026-06-16), 2026-07-11
  - https://www.icy-veins.com/wow/devastation-evoker-pve-dps-spec-builds-talents  # tier 3, 12.0.7 (upd. 2026-06-15), 2026-07-11
confidence: medium
---

# Devastation Evoker — talents & builds (Midnight Season 1)

Layer this on top of `talents.md` / `talents.json` (the full tree dump from
Blizzard game data, Tier 1) — this file is the **narrative**: which hero tree,
which loadout, and why. The tree itself did not get a rework in 12.0.7; the S1
meta is a tuning/usage picture, so treat exact node-by-node picks as
**medium-confidence** and re-verify import strings in-game before trusting them.

## Hero tree: Scalecommander (meta for everything)

Both method.gg and Icy Veins (12.0.7) recommend **Scalecommander as the primary
hero tree for all content** — pure single target, cleave, and AoE. method.gg:
"Scalecommander outperforms Flameshaper in almost all types of damage profiles."
It turns **Deep Breath** into a rotational damage button and grants **Mass
Disintegrate**, which makes Disintegrate a 3-target cleave off empower casts.

**Flameshaper** is the alternative — a concentrated-AoE / Fire-Breath-DoT build
(2nd Fire Breath charge, **Engulf**, **Consume Flame** capstone). Icy Veins:
"only recommend playing this if you really enjoy the Flameshaper playstyle." It
is weaker on target swaps and less flexible; the simc default profile is named
`MID1_Evoker_Devastation_SC` (Scalecommander) but ships **Flameshaper `st_fs` /
`aoe_fs`** action lists too — the engine models both. @verify-ingame (whether a
Flameshaper build out-sims Scalecommander on any live raid encounter this tier)

### Scalecommander hero picks (method.gg / Icy Veins)

- **Mass Disintegrate** — the defining node; empower casts bank charges that make
  the next Disintegrate(s) cleave. Synergizes "extremely well" with Charged Blast.
- **Bombardments** + **Extended Battle** — the bulk of the hero-tree throughput;
  damage during/after empowered phases.
- **Wingleader** — reduces **Deep Breath** cooldown when it hits marked targets
  (feeds the "second Deep Breath ~7–8s later" rotation).
- **Command Squadron**, **Melt Armor**, **Onslaught**, **Maneuverability** round
  out the tree. Choice nodes: **Nimble Flyer / Slipstream** (movement),
  **Hardened Scales / Menacing Presence**, **Extended Battle / Diverted Power**.
  @verify-ingame (exact choice-node picks per content type)

## Spec-tree core (near-universal, 12.0.7)

The engine of every Devastation build is the same cluster:

- **Animosity** — empowering during Dragonrage **extends it ~5s per empower**;
  this is why the rotation lines Fire Breath + Eternity Surge inside the window.
- **Causality** — empower casts (Fire Breath / Eternity Surge) **reduce the
  cooldown** of your other empowers; keeps them rolling.
- **Tyranny** — maximizes Mastery scaling during the Dragonrage burst window.
- **Charged Blast** — Pyre casts stack a buff that amps Spellfrost (Eternity
  Surge / Azure Strike); the M+ build weaponizes this by weaving Pyre between
  Mass Disintegrate casts.
- **Essence Burst** enablers — **Ruby Essence Burst** + **Azure Essence Burst**
  (+ **Essence Attunement** to bank 2 stacks) — the free-spender economy.
- **Font of Magic** (faster empower ranks) + **Power Nexus** (6th Essence) are
  standard baseline-throughput picks.
- Apex: **Rising Fury** (14,18 — 4 ranks) enhances Dragonrage (haste + Essence
  Burst generation as you empower inside it). @verify-ingame (exact effect/ranks)

Class-tree staples: **Tip the Scales** (instant max-rank empower — the burst
enabler), **Blast Furnace** (extends the Fire Breath DoT), **Obsidian Bulwark**
(2nd Obsidian Scales charge), plus utility (**Cauterizing Flame**, **Rescue**,
**Sleep Walk**, **Landslide**). The **Time Spiral / Spatial Paradox** choice node
is a group-utility pick (Spatial Paradox for the instant-empower haste burst).

## Build split: single-target vs M+/AoE

The two builds share the Scalecommander frame; they differ in the AoE-lean spec
nodes:

- **Single-target / raid** — controlled cleave. Leans the pure-throughput and
  Fire-Breath-amp nodes; **Eternity's Span is dropped or de-emphasized** (Rank 1
  Eternity Surge on one target), Disintegrate is the spender at ≤3 targets.
- **M+ / cleave / AoE** — "stacking Charged Blast and spreading damage across
  multiple targets" (method.gg). Picks up **Eternity's Span** (Eternity Surge
  hits **2× targets per rank**) and the **Pyre pushers** — **Feed the Flames** /
  **Volatility** (rank 2) tip the ≤3-target spender from Disintegrate toward
  **Pyre**, and **Firestorm** for a ground AoE. **Charged Blast** uptime is the
  build's engine here.

## Import strings (12.0.7 — verify hero tree on import)

> ⚠ Talent strings are tree-version-sensitive; one bad char breaks the import.
> Confirm each loads as **Scalecommander** in-game before trusting.

**Scalecommander — simc default profile (Tier 1, `MID1_Evoker_Devastation_SC`):**
```
CsbBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAzMDMDzgBmZGjZaYmpZMWmxMzMz8AzMzAmxMGzMLzMDMwYwCsMGN2GQmBBbYGMzghB
```

**Scalecommander — single-target / raid (method.gg):**
```
CsbBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAzMDMDzYmBMYMTzMzMNjx2MmZmZmHYmZGwMmxYmZZmZgBGDWglxox2AyMIYDDMzghB
```

**Scalecommander — M+ / cleave (method.gg):**
```
CsbBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgZmZgZ8AzgBGGjZaMzMNjx2MmZmZGzMzAmZmxYmZZmZgBGDWglxox2AyMIYDzgZGMMA
```

Flameshaper alternative strings exist on method.gg (Titanic Precision + Essence
Well + Consume Flame capstone) but were not captured this pass — pull them from
the guide if a Flameshaper variant is wanted. @verify-ingame

## Stat priority (brief)

Icy Veins / method.gg (12.0.7): Devastation values **Mastery** and **Crit**
highly, with **Haste** for empower speed and GCD, **Versatility** last. As with
other Midnight specs, secondaries are relatively flat vs ilvl — sim on Raidbots
when it matters rather than hard-stacking. @verify-ingame (exact S1 stat order —
not re-derived from a Tier-1 sim this pass)

## TODO

- [ ] Capture the Flameshaper import strings + exact node list from method.gg.
- [ ] Re-derive the spec-tree pick list node-by-node from `talents.json` +
      a murlok/Archon top-key usage aggregation (Tier 2) — current picks are
      distilled from method.gg/Icy Veins prose (Tier 3), not a usage census.
- [ ] Re-sim on a 12.0.7-tagged simc build for a numeric ST-vs-M+ split and a
      confirmed stat order; bump confidence to high once done.
