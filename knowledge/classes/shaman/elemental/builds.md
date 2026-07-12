---
title: Elemental Shaman — Talents & Builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight profiles/MID1/MID1_Shaman_Elemental.simc   # tier 1, talents string fetched 2026-07-11
  - https://www.method.gg/guides/elemental-shaman/talents   # tier 3, upd 2026-06-16
  - https://www.icy-veins.com/wow/elemental-shaman-pve-dps-guide   # tier 3, 12.0.7
  - https://maxroll.gg/wow/class-guides/elemental-shaman-mythic-plus-guide   # tier 3, 12.0.7
confidence: medium
---

# Elemental Shaman — talents & builds (Midnight S1, 12.0.7)

Layered on top of `talents.md` / `talents.json` (the full tree with spell
IDs). This file is the *narrative* — which hero tree, which loadout, and
the interactions that matter.

## Hero tree choice

Elemental picks between two hero trees, and the split is genuinely
content-dependent (unlike some specs with one dominant tree):

- **Stormbringer** — the **lightning / single-target / raid** tree. Spending
  Maelstrom charges **Tempest**, a heavy overloading nuke that supercharges
  the next Lightning Bolt/Chain Lightning (up to 2 stacks) and applies
  **Lightning Rod**. Best where target count is low and sustained
  single-target matters.
- **Farseer** — the **summoning / cleave / Mythic+** tree.
  **Call of the Ancestors** makes Stormkeeper and **Ancestral Swiftness**
  summon ancestor spirits that copy your casts. Excels at 2–3 target cleave
  and dungeons.

Rule of thumb (method.gg / maxroll 12.0.7): **Stormbringer for raid and
pure single-target, Farseer for Mythic+ / heavy cleave.** Both are
competitive — pick to the content.

## Reference talent string (Tier 1, simc MID1)

```
CYQAAAAAAAAAAAAAAAAAAAAAAAAAAAzMbLzMzMzMLbbDMmZAAAAAbmZbzMzwmhFmtZmGamNAYWmZmxYbxEmZ2GLzMzMGWmlZsYmhZWAAGAzMzMGGG
```

This is the SimC default profile loadout (fetched from the midnight branch
2026-07-11). ⚠ Import strings are tree-version-sensitive — **confirm it
loads and reports the intended hero tree in-game** before trusting it, and
re-check if the tree changes in a later patch. @verify-ingame

## Core spec talents & why

- **Ascendance** — the primary burst cooldown; boosts overload damage
  (~+75%) and turbo-charges Lava Burst. First Ascendant / Preeminence is a
  choice node that trades **Ascendance cooldown length** (shorter, more
  frequent vs longer, bigger) — tune to encounter.
- **Stormkeeper** — enables the hero-tree engine (ancestors on Farseer,
  stacks/short CD on Stormbringer); always paired with Ascendance.
- **Master of the Elements** (choice vs **Molten Wrath**) — the ST damage
  amp: Lava Burst / Voltaic Blaze build the MotE buff, which then empowers
  the next Tempest / Elemental Blast / Lightning Bolt. Drives the priority
  loop in the rotation. Molten Wrath is the Fire-lean / AoE alternative.
- **Elemental Blast vs Earth Shock** (choice node) — the Maelstrom spender.
  Elemental Blast hits harder and grants a random secondary-stat buff but
  has a cast time and higher cost; Earth Shock is instant (mobility). Most
  builds take **Elemental Blast**.
- **Mountains Will Fall** — lets Earth Shock and Elemental Blast **Overload**
  (with a small damage penalty), adding free spender copies.
- **Voltaic Blaze** — instant Flame Shock spreader (up to 5 targets); the
  AoE maintenance button, core in Farseer / M+.
- **Lightning Rod** — applied by Tempest (Stormbringer): tagged targets take
  bonus lightning damage; the Stormbringer burst multiplier the AoE APL
  spreads via `target_if=min:debuff.lightning_rod.remains`.
- **Power of the Maelstrom / Swelling Maelstrom / Primordial Fury** — the
  Maelstrom economy passives (extra Lightning Bolt charges, higher cap,
  stronger overloads). Power of the Maelstrom caps at 2 stacks — respect it
  in the rotation.
- **Feedback Loop** (Apex) — capstone boosting overload chance and crit
  scaling.
- **Fire Elemental vs Storm Elemental** — the summoned-elemental cooldown
  (Call of Fire → Fire Elemental by default; Storm Elemental via the choice
  path). **Primal Elementalist** makes the pet controllable and buffs you.

## Class-tree staples

Interrupt/utility/defensive backbone taken near-universally: **Wind Shear**
(interrupt), **Astral Shift** + **Nature's Guardian** (defensives),
**Spiritwalker's Grace** (caster mobility), **Wind Rush Totem** /
**Spirit Walk** / **Ghost Wolf** (movement), **Capacitor Totem** (stun),
**Earthgrab Totem** (root), **Tremor Totem** (fear break), **Hex** (CC),
**Elemental Orbit** (self Earth Shield), **Totemic Projection** (totem
repositioning). **Ancestral Swiftness** (Farseer) replaces **Nature's
Swiftness** as an active when that hero path is taken.

## Build split

- **Raid / single-target (Stormbringer):** Tempest + Lightning Rod + Master
  of the Elements loop; Elemental Blast spender; First Ascendant/Preeminence
  tuned to the fight's burst cadence.
- **Mythic+ / AoE (Farseer):** Call of the Ancestors + Ancestral Swiftness +
  Stormkeeper for ancestor copies; **Voltaic Blaze** + **Earthquake** for
  cleave; Chain Lightning at low target counts (Farseer's 2-target Chain
  Lightning APL line).

## TODO

- [x] Hero-tree recommendation (Stormbringer raid / Farseer M+) — method +
      maxroll 12.0.7
- [x] Tier-1 talent string captured from simc MID1 (2026-07-11)
- [ ] Store per-content import strings from method.gg /talents once the
      JS-rendered page yields them (currently only the SimC default string)
- [ ] Stat priority + gearing/enchants pass (separate from this loadout doc)
- [ ] Confirm First Ascendant vs Preeminence and Fire vs Storm Elemental
      picks against top-M+/raid usage aggregation (murlok/Archon) @verify-ingame
