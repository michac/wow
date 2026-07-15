---
title: Havoc Demon Hunter — Talents & Builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Demon_Hunter_Havoc.simc  # tier 1, simc default talent string (Fel-Scarred), 2026-07-11
  - https://www.method.gg/guides/havoc-demon-hunter/talents  # tier 3, 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/havoc-demon-hunter-pve-dps-spec-builds-talents  # tier 3, 12.0.7, 2026-07-11
  - https://maxroll.gg/wow/class-guides/havoc-demon-hunter-mythic-plus-guide  # tier 3, 12.0.7, 2026-07-11
confidence: medium
---

# Havoc Demon Hunter — Talents & Builds (Midnight S1)

Layers on top of `talents.md` / `talents.json` (the full Tier-1 tree dump). This
file records the **choices** — which hero tree, which loadouts, and the key
interactions — not the whole tree.

## Hero tree: Fel-Scarred (default), Aldrachi Reaver (alternative)

**Fel-Scarred is the S1 recommendation for nearly all content** — the simc
default profile is `MID1_Demon_Hunter_Havoc_Fel-Scarred`, and method.gg calls it
"slightly stronger than Aldrachi Reaver in almost all situations" (strongest
single-target with solid cleave, higher/more-frequent burst in M+). Its identity:

- **Demonsurge** — Eye Beam / Metamorphosis empower the next Annihilation +
  Death Sweep. Each demon-form entry wants ~2 Death Sweep + 1 Annihilation to
  cash the procs.
- **Demonic Intensity** — during Metamorphosis, Eye Beam becomes **Abyssal Gaze**
  and Immolation Aura becomes **Consuming Fire** (empowered), and Meta refunds
  Immolation charges — so spend Immolation before Meta.
- Pairs with **Inertia** (choice node vs Exergy): a movement ability (Felblade /
  Fel Rush / Vengeful Retreat) triggers a big damage amp to line up before every
  Eye Beam and burst window. This is the skill-expression knob of the build.

**Aldrachi Reaver** is the funnel/cleave alternative: "consistent damage output,
good passive cleave and strong funnel damage." Identity is the **Reaver's Glaive**
combo — 6 soul fragments (**Art of the Glaive**) turn Throw Glaive into Reaver's
Glaive, which applies **Reaver's Mark** and empowers the next Chaos Strike
(**Rending Strike**) + Blade Dance (**Glaive Flurry → Fury of the Aldrachi**).
**The Hunt** every ~min guarantees a proc; **Wounded Quarry** drives the funnel.

## Talent strings (Fel-Scarred)

Tier-1 simc default (Fel-Scarred, whole loadout):

```
CEkAAAAAAAAAAAAAAAAAAAAAAYgZmZMjZmZmhJjZGAAAAAAwsZMbzMmZmtZmx2sNPwMMGzYZgtZxMGmNNNmZGDbAAAAAAAAMzgBAAAgB
```

method.gg loadouts (Tier 3, 12.0.7):

- **Raid / single-target (Fel-Scarred):**
  `CEkAAAAAAAAAAAAAAAAAAAAAAYGMzMz2MmZmxMzkxMDAAAAAAY2MmtZYmZ2mZGbz28AzwYYsMwysYGDzmmGzMjhNAAAAAAAAmZwAAAAwA`
- **Mythic+ / AoE (Fel-Scarred, Glaive Tempest lean):**
  `CEkAAAAAAAAAAAAAAAAAAAAAAYmZmZmZ2mxMzMzYmMmZAAAAAAAzmxsNDzMwM2mtZmZMGYZglZzMGmFNNmZGDbAAAADAAAgZGMAAAAM`

> Import strings are tree-version-sensitive — one bad char breaks the import.
> **Confirm they load as Fel-Scarred in-game** before trusting.
> @verify-ingame

## Core talent package (all builds)

Spec-tree backbone (method / Icy Veins / maxroll agree):

- **Demonic** — Eye Beam grants a Demonic demon-form window; the whole loop hangs
  off this. Mandatory.
- **Chaotic Transformation** (vs Inner Demon) — Metamorphosis resets Eye Beam +
  Blade Dance cooldowns, making Meta a real damage cooldown, not just a transform.
- **The Hunt** + **Eternal Hunt** — primary burst button; Eternal Hunt lowers its
  CD and ties it into the Eye Beam cadence.
- **Essence Break** — the ~4s Chaos-Strike/Blade-Dance amp window; core burst.
- **Cycle of Hatred** — Fury spending shaves Eye Beam's cooldown → more Demonic
  windows.
- **A Fire Inside** — Immolation Aura gains a 2nd charge and hits harder; drives
  the Fel-Scarred Immolation/Consuming-Fire play and Ragefire AoE.
- **Demon Blades** — passive Fury generation from auto-attacks (replaces Demon's
  Bite as a manual builder).

## Build split (12.0.7)

- **Single-target / raid** leans the **Inertia** amp cluster plus Throw-Glaive
  empowerment — **Soulscar** + **Burning Blades** (Throw Glaive spreads a copy of
  its damage / empowers it) and **Shattered Destiny** (Fury spending extends
  demon form). Screaming Brutality makes Throw Glaive auto-fire off Blade Dance.
- **Mythic+ / AoE** leans **Glaive Tempest** (Blade Dance/Death Sweep at 3+
  targets release spinning glaives), **Trail of Ruin** (lowers the Blade Dance
  target threshold), **Ragefire** + **A Fire Inside** for Immolation AoE, and
  **Burning Wound** (tab-spread DoT). **Collective Anguish** is the heavy-AoE
  alternative on that choice node.

Choice-node highlights (see `talents.md` for the full node list):

- **Inertia** vs **Exergy** — Inertia (the amp-window playstyle) is the S1 pick.
- **Chaotic Transformation** vs **Inner Demon** — Chaotic Transformation.
- **Soulscar** vs **Relentless Onslaught** — Soulscar for the ST/Throw-Glaive
  build; Relentless Onslaught for a "CS machine" variant (see the APL's
  `cs_machine` flag: Relentless Onslaught + Chaos Theory).
- **Shattered Destiny** vs **Collective Anguish** — Shattered Destiny (ST),
  Collective Anguish (heavy AoE).

## Class-tree notes

Standard Havoc class-tree utility/defense: **Blur**, **Darkness**,
**Chaos Nova**, **Sigil of Misery** (+ Improved), **Imprison**, **The Hunt**,
**Felblade**, **Master of the Glaive / Champion of the Glaive**, **Disrupting
Fury** + **Improved Disrupt** (interrupt value), **Soul Rending** (leech/
survivability), **Infernal Armor**, **Blazing Path** (Fel Rush charge/mobility),
**Pursuit**, **Vengeful Bonds**. **Long Night vs Pitch Black** on the Darkness
choice node (Pitch Black = shorter CD, stronger defensive).

## TODO

- [x] Hero tree resolved — **Fel-Scarred default**, Aldrachi Reaver alt
  (simc default profile + method.gg, 2026-07-11)
- [x] Talent strings captured (simc Tier-1 + method.gg ST/M+ 12.0.7)
- [x] Gearing / stat priority / enchants / consumables — split into
  **`gearing.md`** (2026-07-14, backfilled from maxroll Tier-3; sim-verify
  numbers). builds.md is now talents/loadouts/hero-tree only.
- [ ] Verify import strings load as Fel-Scarred in-game (@verify-ingame)
- [ ] Cross-check talent picks vs a murlok.io / Archon top-M+ usage snapshot
