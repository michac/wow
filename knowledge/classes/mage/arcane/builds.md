---
title: Arcane Mage — Talents & Builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight branch profiles/MID1/MID1_Mage_Arcane.simc  # tier 1, default talent string
  - https://www.method.gg/guides/arcane-mage/talents  # tier 3, upd. 2026-06-29 (12.0.7)
  - https://www.method.gg/guides/arcane-mage/playstyle-and-rotation  # tier 3, upd. 2026-06-29
  - https://www.icy-veins.com/wow/arcane-mage-pve-dps-guide  # tier 3, 12.0.7
confidence: medium
---

# Arcane Mage — Talents & Builds (Midnight S1)

Layered on top of `talents.md` / `talents.json` (the full Tier-1 tree dump — do
not duplicate node lists here). This file is the **narrative**: hero choice,
recommended loadouts, and the interactions that drive them.

## Hero tree: Spellslinger vs Sunfury

Both hero trees are live in S1, and method.gg (12.0.7, upd. 2026-06-29) presents
them as **two real playstyles**, not a solved single pick:

- **Spellslinger** (*Splintering Sorcery* gateway) — the aggressive, orb-centric
  build. **All current Spellslinger builds take *Orb Mastery***, which makes
  **Arcane Orb** the Arcane Salvo builder and **Arcane Missiles obsolete**. A
  Clearcasting Orb fires **three** orbs (2 Salvo each) and spawns passive
  **Arcane Splinters** (~25% Salvo proc). Touch of the Magi is cast immediately
  after Arcane Surge. Salvo caps at **20**; *Polished Focus* refunds 5 Salvo and
  adds +15% Barrage damage, so you dump Barrage at **exactly 20**.
- **Sunfury** (*Spellfire Spheres* gateway) — the Clearcasting-scaling,
  Arcane-Soul build. Salvo caps at **25**, and the payoff is the **Arcane Soul**
  window where **Arcane Barrage is free + instant**. **Clearcasting is the
  engine** (guaranteed off Arcane Surge, Touch of the Magi, and Arcane-Soul
  Barrages), feeding **Arcane Missiles** as the Salvo builder. Touch of the Magi
  is **delayed** to ~5s left on Arcane Surge so both carry into Arcane Soul.

**Rule of thumb:** Spellslinger for the orb-spam / splinter identity and simpler
burst sequencing; Sunfury for the burst-window Arcane Soul payoff. Sim on
Raidbots for your gear/content before committing — the gap is small and shifts
with tuning. @verify-ingame

## Reference talent string (simc default, 12.0.7)

The SimulationCraft midnight default profile (Tier 1) ships this string:

```
C4DAAAAAAAAAAAAAAAAAAAAAAYGGLzMzswMzQzMzAAAwAAgAmZmZZZmZYBAgtxMzMmtFLzMzYmxYMzMGLMzMjZAAGAAAzsAAmBADD
```

> Import strings are tree-version-sensitive — one bad character breaks the load.
> Confirm it imports as the intended hero tree in-game before trusting it, and
> re-verify against method.gg / Icy Veins if the tree changes. @verify-ingame

## Core spec picks (near-universal)

From the spec tree (`talents.md`), the throughput backbone both hero trees share:

- **Builders / spenders:** Arcane Missiles, Arcane Orb, **Charged Orb**,
  **Arcane Barrage** amp cluster (*Arcane Salvo*, *Reverberate*).
- **Salvo / charge economy:** **Arcane Salvo** (the stacking engine),
  **Aether Attunement**, **Intuition**, **Consortium's Bauble**.
- **Cooldowns:** **Touch of the Magi**, **Arcane Surge**, **Touch of the
  Archmage** (capstone). *Presence of Mind* over *Slipstream* for the instant
  Blasts (movement + rebuild).
- **Amp passives:** **Prodigious Savant**, **Illuminated Thoughts**
  (Clearcasting chance), **Eureka**, **Arcane Singularity**.
- **Choice nodes:** *Evocation* over *Mana Adept* (mana sustain); *Arcane Echo* /
  *Aegwynn's Technique* per burst preference.

### Spellslinger-specific

- **Orb Mastery** (mandatory for the build) — Arcane Orb becomes the Salvo
  builder; enables the triple-orb Clearcasting cast.
- **Orb Barrage**, **Overpowered Missiles**, **Overflowing Insight** — orb/salvo
  amplifiers.
- **High Voltage** (choice vs *Charged Missiles*) — Arcane Barrage restores
  Arcane Charges below the Salvo threshold (charge smoothing in AoE).
- Hero-tree passives: **Splintering Sorcery / Splintering Orbs / Controlled
  Instincts / Splinterstorm** — the Arcane Splinter damage/Salvo package.

### Sunfury-specific

- **Charged Missiles** (choice vs *High Voltage*) tends to pair with the
  Missiles-driven Salvo build.
- Hero-tree passives: **Spellfire Spheres, Invocation: Arcane Phoenix, Burden of
  Power, Glorious Incandescence, Mana Cascade** — the Clearcasting/Arcane-Soul
  and Arcane Phoenix package. **Arcane Soul** (free instant Barrages) is the
  window everything builds toward.

## Class-tree universals

Standard Mage class-tree utility/defense that Arcane runs regardless of hero
tree (see `talents.md` for the full node map): **Prismatic Barrier**
(+*Improved Prismatic Barrier*), **Alter Time** (+*Master of Time*), **Ice
Block** / **Ice Cold**, **Shimmer** (over *Improved Blink*), **Greater
Invisibility**, **Mirror Image**, **Counterspell** (+*Improved Counterspell*),
**Remove Curse**, **Spellsteal**, **Mass Polymorph** / **Ring of Frost**
(choice), **Mass Invisibility**, **Time Manipulation**, **Flow of Time**,
**Incantation of Swiftness**. **Supernova** over *Dragon's Breath* is the
common choice-node pick for the extra AoE burst/knock-up.

## Key interactions

- **Arcane Salvo is the spec's pacing clock.** Barrage damage scales with Salvo,
  so the entire rotation is "reach the Salvo threshold, then Barrage in the burst
  window." Overcapping Salvo is wasted throughput; *Polished Focus* (Spellslinger)
  and the 25-cap (Sunfury) set the exact dump point.
- **Big Burn = Arcane Surge + Touch of the Magi.** Touch of the Magi stores 20%
  of the damage you pour into it and detonates — so you cram Barrages + the burst
  cooldowns into its ~12s window. Arcane Surge drains all mana up front, then
  regenerates it and grants ~35% spell damage.
- **Clearcasting is free Salvo.** *Illuminated Thoughts* raises its rate; every
  proc is a free Arcane Missiles (Sunfury) or Arcane Orb (Spellslinger) that
  stacks Salvo without spending mana.
- **Nether Precision is gone (Midnight).** Old guides that route Arcane Missiles
  into an empowered Arcane Blast are stale — base Missiles damage absorbed it.
  @verify-ingame

## TODO

- [x] Hero-tree framing (Spellslinger/Orb Mastery vs Sunfury) — method.gg + APL, 2026-07-11
- [x] simc default talent string captured — MID1_Mage_Arcane.simc, 2026-07-11
- [ ] Confirmed hero-tree win-rate/usage split (murlok/Archon) for S1 — not yet
      pulled; both presented as viable. Flag as `medium` confidence until sourced.
- [ ] Stat priority / gearing / enchants pass (out of scope for this file; add
      alongside a future gearing doc)
