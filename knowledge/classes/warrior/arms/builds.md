---
title: Arms Warrior — Talents & Builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/arms-warrior/talents  # tier 3, 12.0.7, 2026-07-11
  - https://www.method.gg/guides/arms-warrior/playstyle-and-rotation  # tier 3, 12.0.7, 2026-07-11
  - simc midnight branch profiles/MID1/MID1_Warrior_Arms.simc  # tier 1, talents string below, WoW 12.0.7
  - knowledge/classes/warrior/arms/talents.md  # tier 1, Blizzard talent-tree API node/spell IDs
confidence: medium
---

# Arms Warrior — Talents & Builds (Midnight S1)

Layered on top of the full tree in `talents.md` (Tier-1 Blizzard talent-tree
API). This file is the **narrative**: hero-tree choice, loadout leans, and key
interactions. See `rotation.md` for how the picks are pressed.

## Hero tree: Slayer (ST) vs Colossus (AoE/M+)

Both hero trees are viable in S1; the gap narrowed in 12.0.5 so **preference
matters** (method.gg). The rule of thumb:

- **Slayer** — **best single target**, execute-focused. `Slayer's Dominance`
  applies **Marked for Execution**; the branch weaponizes `Execute` + `Sudden
  Death`. Default for raid single-target / pure ST.
- **Colossus** — **best AoE / Mythic+**. Adds the finisher **`Demolish`**,
  which triggers several talented effects and wants to land inside `Colossus
  Smash` at **10 stacks of `Colossal Might`**, plus stronger `Cleave` cleave.
  Default for M+ / add-heavy content.

method.gg publishes **six preset loadouts** (importable strings): Slayer
Single-Target / Cleave / AoE-M+ and Colossus Single-Target / Cleave / AoE-M+.

**Tier-1 reference talent string** (simc `MID1_Warrior_Arms`, a **Colossus**
profile — it runs the `demolish` action list):

```
CcEAAAAAAAAAAAAAAAAAAAAAAAzMzsMzMzMDAAAghphxYmxyMzMzgxMDAAAAgZWmZAZMWWGYBMgZYCZGsBMjNz2YwMGgZGAmxwA
```

> ⚠ Import strings are tree-version-sensitive — one changed node breaks the
> import. Confirm the hero tree loads correctly in-game before trusting any
> string. The six method.gg strings are the maintained per-scenario set;
> the simc string above is the sim's single Colossus default. @verify-ingame

## Core spec talents & why

**Colossus Smash package (both trees):**
- **`Colossus Smash`** → the whole rotation's amp window. `Anger Management`
  refunds cooldown from Rage spent, so Colossus Smash / Avatar / Bladestorm come
  back fast — press them on cooldown as long as the window is full.
- **`Mortal Strike` + `Overpower`** — MS is the signature builder (Mortal Wounds
  + Deep Wounds); `Overpower` empowers the next MS (`Martial Prowess`) and is
  reset by **`Tactician`** (auto-attacks) and **`Battlelord`** (MS/Cleave). Keep
  Overpower charges flowing into MS.
- **`Deep Wounds` + `Rend`** — the maintained bleeds; `Thunder Clap` spreads Rend
  in AoE.

**Execute cluster (Slayer-leaning):**
- **`Sudden Death`** — free/anytime `Execute` procs; the Slayer engine.
- **`Massacre`** — raises the Execute threshold to **35%**, a big uptime gain.
- **`Executioner's Precision`** — stacks (to 2) on Execute and amplifies the next
  `Mortal Strike`; the rotation **holds MS for 2 stacks** in execute.
- **`Improved Execute`, `Mass Execution`** — Execute damage / cleaving Execute.

**AoE / cleave cluster (Colossus-leaning):**
- **`Cleave`** — top 3+ target button; applies `Deep Wounds` and builds
  **`Collateral Damage`** (to 3 stacks), which **`Whirlwind`** consumes.
- **`Fervor of Battle`** — `Whirlwind` also lands a `Slam`-equivalent on the
  primary, keeping priority damage up while cleaving.
- **`Sweeping Strikes` + `Broad Strokes`** — Broad Strokes grants **free Sweeping
  Strikes on every `Colossus Smash`**, driving 2-target cleave uptime.
- **`Dreadnaught`** — `Overpower` cleaves; **`Bladestorm`/`Ravager`** choice for
  AoE burst (Ravager deploys into the Colossus Smash window).

**Hero-signature interactions:**
- **Colossus** — `Colossal Might` builds to 10; **`Demolish`** cashes it in
  during `Colossus Smash`. `Dominance of the Colossus` is the capstone.
- **Slayer** — `Slayer's Dominance` / `Imminent Demise` / `Overwhelming Blades`
  feed the Bladestorm-in-Colossus-Smash burst and Marked for Execution.

**Apex spec talent — `Master of Warfare`:** transforms **`Slam` into `Heroic
Strike`** with a stacking **Armor Penetration** buff. This is why the Tier-1 APL
emits `heroic_strike` as filler; treat Heroic Strike as your Slam in that build.

## Utility / defensive talent notes

- **`Javelineer`** — adds a **3s silence** to `Wrecking Throw`/`Shattering Throw`;
  method.gg calls it "incredible utility" for M+ pack control.
- **Class-tree survivability** — `Ignore Pain` (absorb, choice vs `Fueled by
  Violence`), `Die by the Sword`, `Rallying Cry` (raid), `Spell Reflection`,
  `Impending Victory` (self-heal), `Bounding Stride`/`Double Time` (mobility),
  `Shockwave`/`Storm Bolt` (CC), `Piercing Howl` vs `Intimidating Shout`.

## Stat priority & gearing

The simc profile gears **Strength > Haste ≈ Crit > Mastery** for this build
(gear summary: high crit/haste, low mastery). Secondaries are relatively flat
for Arms — **ilvl generally wins**; sim on Raidbots for near-ties and trinkets.
@verify-ingame (stat order is inferred from the simc gear block + general Arms
consensus, not a dedicated Tier-1/2 stat-weight source this pass)

Season 1 tier set **"Rage of the Night Ender"** (method.gg summary):
- **2pc** — +5% `Mortal Strike` and `Cleave` damage; the `Colossus Smash` target
  takes +5% damage.
- **4pc** — hitting **3+ targets** with `Mortal Strike`/`Cleave` during the
  window **extends `Colossus Smash`**.

Take/upgrade tier pieces regardless of secondaries. @verify-ingame (tier bonus
numbers pending a Blizzard-tooltip / wago cross-check)

## TODO

- [ ] Capture the six method.gg per-scenario import strings verbatim (JS-rendered
      page returned a summary, not the raw strings, on 2026-07-11).
- [ ] Cross-check the "Rage of the Night Ender" 2pc/4pc exact values against the
      Blizzard item/spell API or wago DB2 (currently from method.gg prose).
- [ ] Add Warcraft Logs / Archon usage split (Slayer vs Colossus) once S1 raid +
      M+ parses aggregate.
