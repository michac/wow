---
title: Balance Druid — Talents & Builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://github.com/simulationcraft/simc/blob/midnight/profiles/MID1/MID1_Druid_Balance.simc  # tier 1 talent string + APL, 2026-07-11
  - https://www.method.gg/guides/balance-druid/talents  # tier 3, Midnight 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/balance-druid-pve-dps-guide  # tier 3, 12.0.7, 2026-07-11
  - https://maxroll.gg/wow/class-guides/balance-druid-mythic-plus-guide  # tier 3, 12.0.7, 2026-07-11
  - knowledge/classes/druid/balance/talents.md  # tier 1 (wago DB2 + Blizzard talent API) — full node list
confidence: medium
---

# Balance Druid — talents & builds (Midnight S1)

Layered on top of the full node list in `talents.md` (Tier-1 game data — the
node names/IDs/prereqs there are the floor; this file is the *choices*).

## Hero tree — pick by content

Two hero trees, and unlike some specs the split is **real**:

- **Keeper of the Grove** — **raid / single-target (and spread cleave).** Built
  around **Treants** and **Harmony of the Grove**: Force of Nature becomes a core
  rotational button whose damage buff you overlap with CA/Incarnation + Convoke.
  **Treants of the Moon** makes the Treants also cast Moonfire, deepening spread
  cleave. Highest ceiling but demands per-fight cooldown planning.
- **Elune's Chosen** — **Mythic+ / sustained AoE.** **Disables Solar Eclipse
  (you always enter Lunar)** and revolves around **Fury of Elune**: **Lunation**
  shortens its cooldown the more you cast, and **Atmospheric Exposure**
  increases damage to Fury-of-Elune-hit targets (great on stacked cleave).
  Simpler cooldown management — no Convoke alignment puzzle.

The Tier-1 simc profile ships a **Keeper of the Grove** string as its default
(`hero_tree.elunes_chosen` branches exist but the shipped talents build Keeper):

```
CYGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWoMbNjxMDwsYmZmZhBjZZmlZYmZswyMLzMGzshhBYstMzgxsNCMBAAAYxMzMzgNDjxAAwMDMA
```

> ⚠ Import strings are tree-version-sensitive — one bad character breaks the
> import, and this string encodes the simc default (a Keeper raid/ST layout).
> Confirm it loads as **Keeper of the Grove** in-game, and pull a dedicated
> **Elune's Chosen M+ string** from Method/Wowhead before relying on it for
> dungeons. @verify-ingame

## Spec tree — the load-bearing choices

**The Eclipse core (all builds):** Eclipse, Improved Eclipse, Nature's Balance
(passive AP trickle), Umbral Intensity, Wild Surges, and the capstone
**Ascendant Eclipses** (active — empowered spenders / guaranteed-crit bolts that
stack the Eclipse debuff). This is the spine both hero trees plug into.

Key choice nodes and interactions:

- **Convoke the Spirits vs Incarnation: Chosen of Elune** — the big
  choice-node. **Convoke** wins on pure **single-target / raid** (huge burst,
  overlaps CA + Balance of All Things); **Incarnation** is preferred for
  **Mythic+ / council** fights (near-parity DPS, but a longer, more flexible
  burst window you can place on demand). Note the simc default takes Incarnation.
- **Fury of Elune vs New Moon** — Fury of Elune is the default (and mandatory
  for Elune's Chosen / Lunation). New Moon (the Moon chain: New → Half → Full)
  is the AP-generation alternative some ST builds run.
- **Starweaver vs Rattle the Stars** — Starweaver (free Starsurge/Starfall
  procs) is the general pick; with Midnight's Shooting Stars buffs + tier
  interactions, **Rattle the Stars is now a viable single-target choice**.
- **Aetherial Kindling vs Meteor Storm** — Aetherial Kindling for **prolonged
  AoE**; Meteor Storm for **sporadic adds / priority targets** in raid.
- **Whirling Stars vs Orbital Strike**, **Sundered Firmament vs Orbit Breaker**,
  **Sunseeker Mushroom vs Wild Mushroom**, **Nature's Grace vs Elune's
  Challenge** — tune per content; see `talents.md` for the node graph.
- **Starlord** (stacking haste on spend) + **Balance of All Things** (decaying
  crit on Eclipse entry) are the throughput passives you snapshot burst into.
- **Touch the Cosmos** — free spenders during CA/Incarnation; **Stellar
  Amplification** + **Meteorites** shape the Starfall proc build.

## Class tree — the standard skeleton

DPS-relevant picks (Method 12.0.7): **Nurturing Instinct, Lycara's Teachings,
Starlight Conduit, Circle of the Heavens** (the caster-side capstone vs Circle
of the Wild), **Lore of the Grove**, **Astral Influence** (range),
**Wild Charge / Tiger Dash** (mobility), **Stampeding Roar**.

Defensive / utility spine: **Barkskin + Improved Barkskin**, **Thick Hide**,
**Well-Honed Instincts**, **Aessina's Renewal**, **Oakskin**, **Natural
Recovery**, **Innervate**, **Remove Corruption**, plus a control choice
(**Mighty Bash / Incapacitating Roar**, **Mass Entanglement / Ursol's Vortex**,
**Typhoon**). **Solar Beam** (interrupt) and **Force of Nature** come from the
spec tree and are non-negotiable.

## Build split (12.0.7)

- **Raid / single-target:** **Keeper of the Grove** + **Convoke** + the Eclipse
  core; Fury of Elune before Eclipse, Force of Nature stacked into the CA/Convoke
  burst. Rattle the Stars is a live ST option now.
- **Mythic+ / AoE:** **Elune's Chosen** + **Incarnation** + Aetherial Kindling;
  always-Lunar, Fury-of-Elune / Atmospheric Exposure centric, Treants/Moonfire
  spread for pull-wide damage.

## TODO

- [x] Hero-tree split — Keeper (raid/ST) vs Elune's Chosen (M+/AoE), 2026-07-11
- [x] simc default talent string captured (Keeper raid/ST)
- [x] Key choice-node interactions (Convoke/Incarn, Starweaver/Rattle,
      Aetherial/Meteor, Fury/New Moon)
- [ ] Capture a dedicated **Elune's Chosen M+ import string** (Method/Wowhead)
      and a Convoke-ST string separate from the simc default
- [ ] Stat priority + gearing/enchants/gems/consumables (own file, like
      Affliction's) — not yet sourced this pass
