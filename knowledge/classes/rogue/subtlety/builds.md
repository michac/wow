---
title: Subtlety Rogue — Talents & Builds (Midnight Season 1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/subtlety-rogue/talents  # tier 3, 12.0.7 — hero choice + import strings
  - simc midnight branch profiles/MID1/MID1_Rogue_Subtlety.simc  # tier 1 — default talent string
  - https://www.method.gg/guides/subtlety-rogue/playstyle-and-rotation  # tier 3, 12.0.7 — mechanic corroboration
confidence: medium
---

# Subtlety Rogue — talents & builds (Midnight S1)

Layers on top of `talents.md` / `talents.json` (the full Tier-1 tree dump).
This file is the **narrative**: which hero tree, which loadout, and why.

## Hero tree: **Trickster** (recommended)

method.gg: *"the general recommended Hero talent to play is Trickster as it
is more well rounded and does well on both single target and AoE."*
**Deathstalker** is viable and can edge ahead on **pure single-target /
focused** fights, but is less versatile.

- **Trickster** — **Unseen Blade** procs off builders, dealing bonus damage
  and applying **Fazed** (+damage taken, target can't parry). Stacks
  **Flawless Form** (+4% finisher damage per stack, max 5) and charges the
  **Coup de Grace** capstone — a heavy finisher that lands after building
  Unseen Blade procs. Finishers fire from **6+ combo points**.
- **Deathstalker** — **Shadowstrike** applies **Deathstalker's Mark**; you
  **dance from low combo points** and consuming the Mark grants **Darkest
  Night**, which makes the next **Eviscerate** an empowered top-priority
  finisher. Single-target-leaning. Key nodes: Deathstalker's Mark, Hunt Them
  Down, Singular Focus, Darkest Night (capstone).

The S1 simc APL supports **both** — its lines branch on
`talent.deathstalkers_mark` vs `talent.unseen_blade`/Supercharge.

## Recommended loadouts (method.gg, 12.0.7)

**Trickster — Single Target / Raid:**
```
CUQAAAAAAAAAAAAAAAAAAAAAAAgx2MAAAAAwsMGLTMbbjxMjZwDMzMzYMbjZGbbzMzMzMjBjZWGAAAAGMGwY2MMwAzCL0iNMDYmBzYA
```

**Trickster — Mythic+:**
```
CUQAAAAAAAAAAAAAAAAAAAAAAAgx2MAAAAAwsMGLTMbbjxMjZMegZmZGjZbYGbbzMzMzMjBjZWGAAAAGMGwY2MMwAzCL0iNMDYmBzYA
```

**simc default profile string (Tier 1 — build the sim uses):**
```
talents=CUQAAAAAAAAAAAAAAAAAAAAAAAgx2MAAAAAwsMGLTMbbjxMjZwMzMzYMbDzYbbmZmZmZMYMz2AAAAwgxAGzmhBGYW0CtYDzAmZwMGA
```

> ⚠ Import strings are tree-version-sensitive. Confirm each loads as the
> intended **hero tree** in-game before trusting (one bad character breaks an
> import). The M+ string differs from the ST string only in the mid-tree
> cluster (AoE-leaning choices). @verify-ingame

## Core spec talents (method + APL)

Foundation nodes the build is built on:

- **Relentless Strikes** — finishers refund energy (fuels the builder→
  finisher tempo).
- **Deepening Shadows** — **reworked in Midnight**: extends **Shadow Dance
  duration** by Haste instead of shortening its cooldown. @verify-ingame
- **Double Dance** — **2 charges of Shadow Dance** (the enabler for
  "2 dances per Shadow Blades").
- **Death Perception** — damage/Find-Weakness amp inside Shadow Dance.
- **Secret Stratagem** / **Deeper Stratagem** — **+combo points** (up to 7)
  and finisher damage.
- **Improved Secret Technique** — buffs the Secret Technique finisher (the
  in-Dance burst button).
- **Goremaw's Bite** — the combo-point-burst builder woven on cooldown.
- **Ancient Arts** (apex, all ranks) — spending Shadow Techniques stacks
  triggers shadow-clone strikes / combo-point refunds; gates a couple of
  opener lines in the APL (`talent.ancient_arts_3`).
- **Danse Macabre** — rewards varying which abilities you cast inside Shadow
  Dance (ramping damage) — reinforces alternating Shadowstrike/finisher.

## Key interactions

- **Shadow Dance ↔ Shadow Blades:** the entire build exists to stack two
  Shadow Dance charges onto each Shadow Blades. Double Dance + the reworked
  Deepening Shadows (Haste → longer Dance) means Haste directly buys more
  in-window casts.
- **Find Weakness:** Shadowstrike (and openers / Black Powder in AoE) apply
  Find Weakness — an armor-ignoring damage window; keeping it up during
  Shadow Dance is a big chunk of throughput.
- **Trickster loop:** builders → Unseen Blade procs → Flawless Form stacks →
  bigger finishers → Coup de Grace payoff.
- **Deathstalker loop:** Shadowstrike → Deathstalker's Mark → consume →
  Darkest Night → empowered Eviscerate (the APL puts `eviscerate,if=
  buff.darkest_night.up` at the top of the finisher list).

## Notable choice nodes

- **Backstab vs Gloomblade** — Gloomblade (Shadow damage, no positional) is
  the common builder pick over Backstab.
- **Trickster capstone: Coup de Grace** vs **Deathstalker capstone: Darkest
  Night** — this is the hero-tree split.
- Class-tree utility choices (Tricks of the Trade vs Blackjack, Gouge vs
  Airborne Irritant, Elusiveness vs Cheat Death, etc.) are situational —
  default to the throughput/utility picks in `talents.md`.

## TODO

- [x] Hero-tree recommendation — **Trickster** default (method 12.0.7),
      Deathstalker as ST-lean alt; both supported by the simc APL.
- [x] ST + M+ import strings captured (method 12.0.7) + simc default string.
- [ ] Cross-check strings decode to the right hero tree in-game
      @verify-ingame
- [ ] Add stat priority / gearing / enchants section (pull Icy Veins +
      simc; not yet sourced this pass)
- [ ] Confirm Deepening Shadows rework numbers + Rupture/Symbols removal
      against Blizzard spell API @verify-ingame
