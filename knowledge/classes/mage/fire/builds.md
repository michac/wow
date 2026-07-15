---
title: Fire Mage — Talents & Builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight branch profiles/MID1/MID1_Mage_Fire.simc  # tier 1, Sunfury talent string, WoW 12.0.x
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Mage_Fire.simc  # tier 1
  - https://www.method.gg/guides/fire-mage/talents  # tier 3, 12.0.7, upd. 2026-06-16
  - https://www.method.gg/guides/fire-mage  # tier 3, 12.0.7 (Midnight ability changes)
  - https://www.wowhead.com/spell=1257349/fired-up  # tier 4, Fired Up apex proc
confidence: medium
---

# Fire Mage — Talents & Builds (Midnight S1)

Layers on top of `talents.md` / `talents.json` (the full tree, from Blizzard
game data — tier 1). This file is the *narrative*: which hero tree, which
loadouts, and the interactions that matter.

## Hero tree: Sunfury (everywhere)

**Sunfury is the S1 recommendation for all content** (method.gg 12.0.7:
"Frostfire numbers just aren't quite there... Sunfury is pulling ahead in most
content"). The simc default profile is `MID1_Mage_Fire_Sunfury`.

- **Sunfury** revolves around **Spellfire Spheres** → **Meteorites** (proc chance
  raised to ~20% in S1) and **Invocation: Arcane Phoenix**, which grants a ~15%
  Haste buff after it expires and feeds **Fire Blast** cooldown reduction. It
  scales single target *and* AoE, and drives Pyroclasm-based AoE burst.
- **Frostfire** (the other tree) swaps **Fireball → Frostfire Bolt** (a Fire+Frost
  filler) and layers frost/fire cross-buffs, but is **undertuned in S1** — a
  personal-preference pick only. Its APL lists exist (`ff_*`) if you run it.

**Tier-1 Sunfury talent string** (from the simc profile — import-ready):

```
C8DAAAAAAAAAAAAAAAAAAAAAAYGGLzMzswMDZmZGAAAGAwMz0sssMDAwmZmx2wYmBAAAAAsZmZmZAAwYGzYmZMz2AwMDxMGDmhB
```

method.gg publishes three loadouts (import strings on the guide page):
**Sunfury Single Target**, **Sunfury Mythic+**, and **Frostfire Single Target &
Mythic+**. ST vs M+ is a small reshuffle around AoE talents (Flamestrike/Fuel the
Fire count-gating, Blast Zone, Burnout), not a hero-tree change.

> Import strings are tree-version-sensitive — confirm a string loads as **Sunfury**
> in-game before trusting it (one bad character breaks the import). @verify-ingame

## Core spec-tree package

The engine talents that define the build (from the tree in `talents.md`, matched
to the simc string + method.gg):

- **Combustion + Kindling** — Kindling now applies a **static 60s reduction**,
  giving Combustion a **~1-minute** cooldown. This is *the* defining S1 change:
  Combustion comes up roughly twice as often as its base cooldown.
- **Firestarter** — targets above 90% HP take guaranteed crits; shapes the pull
  (the APL delays the opener Combustion ~18s to not waste it).
- **Fired Up (apex, row 11)** — consuming Hot Streak has a chance (much higher
  during Combustion) to grant **Fired Up**: a stacking +fire-damage buff **and a
  ~2.5s-per-rank Fire Blast cooldown reduction**, extending Combustion by 1s while
  active. This **replaces the removed Phoenix Flames** as the Combustion Fire Blast
  engine — "set and forget," always taken.
- **Hot Streak / Heating Up / Hyperthermia** cluster — Hyperthermia (post-
  Combustion window of free instant Pyroblasts) is core; keep converting Heating
  Up with Fire Blast even under Hyperthermia for the Ignite bonus.
- **Pyroclasm** — now carries the folded-in **Sun King's Blessing** and empowers
  hardcast **Flamestrike**; the AoE-burst enabler. Spend at 2 stacks.
- **Scorch + Scald / Heat Shimmer** — execute filler (<30%) and the Heat Shimmer
  instant-Scorch proc.
- **Meteor + Blast Zone / Sunfury Execution** — the AoE/burst nuke, timed into
  Combustion (or late, with **Burnout**, to bank Ignite for an AoE detonation).
- **Fuel the Fire** — gates the Flamestrike-vs-Pyroblast AoE spender threshold in
  the APL (`flamestriking` at ≥4 targets).

## ST vs M+ split

- **Single target:** lean the Combustion/Ignite-throughput talents; Pyroblast is
  the spender; Meteor purely into the burst window.
- **Mythic+ / AoE:** take **Flamestrike/Fuel the Fire** count-gating, **Blast
  Zone** (Meteor on cooldown), and **Burnout** (Combustion-expiry AoE). Spender
  flips to Flamestrike at 4+ targets. Pyroclasm drives the AoE burst.

## Midnight talent-relevant removals

Per method.gg, these prior-expansion staples are **gone / folded** — don't build
around them:

- **Phoenix Flames — removed** (role covered by Fired Up).
- **Shifting Power — removed.**
- **Sun King's Blessing — folded into Pyroclasm** (now also affects hardcast
  Flamestrike).
- Ice Floes, Blast Wave, Mass Barrier, and Greater Invisibility's defensive
  component were also removed/trimmed (method intro).

## TODO

- [x] Hero tree — **Sunfury everywhere** (method.gg 12.0.7 + simc default)
- [x] Tier-1 talent string captured from simc profile
- [ ] Capture the three method.gg import strings verbatim (ST / M+ / Frostfire)
- [ ] Stat priority + enchants/gems/consumables pass (not yet sourced here)
- [ ] Re-verify against a fresh simc midnight APL + murlok top-50 usage snapshot
