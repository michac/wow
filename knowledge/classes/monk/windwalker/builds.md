---
title: Windwalker Monk — Talents & Builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/windwalker-monk/talents  # tier 3, upd. 2026-06-16, import strings
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Monk_Windwalker.simc  # tier 1, default sim talent string
  - knowledge/classes/monk/windwalker/talents.md  # tier 1 tree (Blizzard API + wago), 12.0.7.67808
  - https://www.icy-veins.com/wow/windwalker-monk-pve-dps-guide  # tier 3, 12.0.7 corroboration
confidence: medium
---

# Windwalker Monk — Talents & Builds (Midnight S1)

Layered on top of `talents.md` / `talents.json` (the Tier-1 tree dump — Blizzard
API + wago, build 12.0.7.67808). This file is the **narrative**: hero-tree choice,
recommended loadouts, and the key interactions that make the rotation in
`rotation.md` work. Do not regenerate the tree files from here.

## Hero tree: Conduit of the Celestials (default) vs Shado-Pan

Both hero trees are played in S1; **Conduit of the Celestials** is Method's
primary recommendation and the SimulationCraft default profile is built around it
(`talent.celestial_conduit` gating the `big_coc` action list). The genuine split:

- **Conduit of the Celestials** — grants **Celestial Conduit** (a big channeled
  nuke) and, more importantly, **Heart of the Jade Serpent**: *"the most important
  effect in this tree by far, due to the drastically sped-up rotation and quicker
  Fists of Fury channeling"* (Method). Smoother, burst-window-centric, strong ST
  and cleave. Pairs with **Unity Within** (the capstone that fuses Xuen/Celestial
  buffs).
- **Shado-Pan** — built on **Flurry Strikes**: spending resources accumulates
  charges that unleash bonus strikes, and **Efficient Training** drives a tighter,
  more frequent **Zenith** cadence. Leans faster/steadier and scales its Zenith
  timing off **Tigereye Brew** stacks. The APL's `talent.flurry_strikes` branch is
  fully supported, so it's a real alternative — pick per fight / personal feel.

## Recommended talent strings (Method, 12.0.7)

> Import strings are **tree-version-sensitive** — one wrong character breaks the
> import. Confirm they load as the intended hero tree in-game before trusting.
> Verify against the source if the trees change in a later patch. @verify-ingame

**Conduit of the Celestials — Single Target:**
```
C0QAAAAAAAAAAAAAAAAAAAAAAMzYM2GGsNzMbzAAAAAAAAAAAAsMMTYGGGwwwMzMDz2wMMLzEAwiZ2GDzMzMAAWMzysNmgAAwAYGgxyMImZmFD
```
**Conduit of the Celestials — Mythic+:**
```
C0QAAAAAAAAAAAAAAAAAAAAAAMzYMYMYbmZ2mxAAAAAAAAAAAALDzEmhhBMMMzMzwsNMDzyMBAsYmtxwYmZAAsYmlZbMBBAMMAmBYsMDiZmZxA
```
**Shado-Pan — Single Target:**
```
C0QAAAAAAAAAAAAAAAAAAAAAAMzMD2mxgtZGbzAAAAAAAAAAAAsMMTYGGGwwwMzMDz2wMMLzEAwiZ2GDzMzMAA2AgZbWamZmFAMwMDAjlZQMgB
```
**Shado-Pan — Mythic+:**
```
C0QAAAAAAAAAAAAAAAAAAAAAAMzYMYMYbmZ2mxAAAAAAAAAAAALDzEmhhBMMMzMzwsNMDzyMBAsYmtxwYmZAAsBAz2s0MzMLADDMzAwYZGEDYA
```

The SimulationCraft default WW profile ships its own string
(`C0QAAAAAAAAAAAAAAAAAAAAAAMzMD2mxgtZGbzAAAAAAAAAAAAsMMCzYbYAzYYmZmhZZYGmlZCAYxMbjhZmZGAAbAoZZWamZmFAMwMDAsMGwAG`)
— a Flurry-Strikes patchwerk sim config; treat Method's strings as the practical
loadouts and the sim string as the throughput baseline.

## Key talent interactions

- **Combo Strikes (Mastery) + Hit Combo** — the whole spec is built on *never
  repeating an ability*. Hit Combo stacks a growing damage buff for consecutive
  distinct casts and drops if you repeat; every APL line carries `combo_strike`.
- **Xuen's Battlegear** — *"drastically increases the value of Rising Sun Kick…
  higher crit chance AND massive cooldown reduction on your highest-damage
  ability"* (Method). Makes RSK a near-constant priority button.
- **Heart of the Jade Serpent** (Conduit) — the proc that speeds Fists of Fury
  and compresses the rotation; drives the "Fists of Fury when Heart ≤1s" top
  priority and the Celestial Conduit timing (cast when Heart is **down**).
- **Tigereye Brew** — spec capstone; **+1% crit per stack**, stacks from Chi
  spent during combat, then consumed for a burst window. The Flurry-Strikes
  Zenith lines in the APL key their timing off Tigereye Brew stack thresholds.
- **Dance of Chi-Ji** — procs a free, empowered Spinning Crane Kick (to 2
  stacks); the reason SCK ranks above raw fillers in single target.
- **Combo Breaker** — Tiger Palm procs a free *Blackout Kick!*; consume promptly.
- **Obsidian Spiral** — changes how Chi is spent inside Zenith (the APL uses it to
  **skip low-value Tiger Palm / Spinning Crane Kick inside cooldowns**).
- **Ascension** — +max Chi and Energy regen; shifts several APL Chi thresholds
  (`chi<3-1*!talent.ascension`).
- **Sequenced Strikes / Shadowboxing Treads** — AoE enablers: Sequenced Strikes
  governs Dance of Chi-Ji SCK usage; Shadowboxing Treads cleaves Blackout Kick
  and reshapes the multi-target Blackout/SCK ordering.
- **Spiritual Focus (Conduit) / Efficient Training (Shado-Pan)** — the two ways to
  cut **Zenith**'s cooldown; the reason each tree runs a different Zenith cadence.
- **Whirling Dragon Punch ↔ Strike of the Windlord** — a choice node in the spec
  tree (row 8). WDP requires both Fists of Fury and Rising Sun Kick on cooldown;
  SotW is an instant cone. Both slot high in the priority when taken; builds
  above pick one per hero tree / content.
- **Revolving Whirl / Echo Technique** and **Drinking Horn Cover / Spiritual
  Focus** are the other live choice nodes that shift Zenith timing and Chi flow
  (referenced throughout the APL's Zenith list).

## PvP talents (context, not PvE)

`Nimble Brew` (LoC removal), `Double Barrel` (empowered Fists of Fury stun), and
`Reverse Magic` (group magic reflect) are **PvP talents**, not part of the PvE
loadout — listed here only because they appear in the class's ability seed.

## TODO

- [ ] Confirm the four Method import strings load as the intended hero tree
      in-game (one bad character breaks an import). @verify-ingame
- [ ] Add stat priority / gems / enchants / consumables section (currently only
      talents + hero-tree narrative — mirror the Affliction builds.md depth).
- [ ] Pull murlok/Archon top-M+ usage to confirm Conduit vs Shado-Pan split for S1.
- [~] Re-verify strings + core picks if the WW tree changes in a later 12.0.x patch.
