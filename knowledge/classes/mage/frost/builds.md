---
title: Frost Mage — Talents & Builds (Midnight Season 1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.icy-veins.com/wow/frost-mage-pve-dps-spec-builds-talents  # tier 3, 12.0.7, 2026-07-11
  - https://www.method.gg/guides/frost-mage/playstyle-and-rotation  # tier 3, 12.0.7, 2026-07-11
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Mage_Frost.simc  # tier 1 talent string, 2026-07-11
  - knowledge/classes/mage/frost/talents.md  # tier 1 tree (Blizzard API / wago), 12.0.7.67808
confidence: medium
---

# Frost Mage — talents & builds (Midnight Season 1)

Layered on top of `talents.md` / `talents.json` (the full tree, from Blizzard
game data — don't restate node lists here). This file is the **build narrative**:
hero-tree choice, loadouts, and the interactions that make them work.

## Hero tree: Spellslinger everywhere

**Spellslinger** is the S1 pick for all content. Icy Veins: "Spellslinger is the
go-to for all content, as Frostfire is significantly behind." Method agrees it is
the main hero talent for both single-target and AoE. Spellslinger generates
**Splinters** off your casts that fire as extra hits, reduce **Frozen Orb** /
**Ray of Frost** cooldowns (via **Spellfrost Teachings**), and pool into
**Splinterstorm** for a burst release — a smoother, more sustained profile.

**Frostfire** is the alternative: it drops the Excess Fire/Excess Frost layer for
core-spell buffs — **Frostbolt→Frostfire Bolt**, **Flurry** becomes a Frostfire
spell, **Glacial Spike explodes on impact**. More front-loaded, burstier damage
that suits **outdoor / world content** but trails in group PvE.

Key Spellslinger nodes: **Splintering Sorcery / Splintering Orbs**,
**Spellfrost Teachings** (Frozen Orb CD reduction), **Controlled Instincts**,
**Signature Spell**, **Splinterstorm** (capstone). Frostfire's identity nodes:
**Frostfire Bolt**, **Frostfire Empowerment**, **Isothermic Core**, **Flash
Freezeburn**, **Elemental Conduit**.

## Core spec talents (both trees)

The redesigned Frost tree centers on the **Freezing** system (the old
Winter's Chill, now a stacking-to-20 debuff) and **Shatter** payoff:

- **Fingers of Frost** + **Frozen Touch** — instant, max-Shatter Ice Lance procs.
- **Brain Freeze** — free instant Flurry; the Freezing applicator.
- **Icicles** → **Glacial Spike** — Frostbolt banks 5 Icicles into a Glacial
  Spike nuke; a core builder→spender button now, not a niche pick.
- **Comet Storm** — burst AoE that consumes Freezing; taken in both builds.
- **Ray of Frost** + **Hand of Frost** (apex) — a **2nd Ray of Frost charge**
  and damage triggered during the channel; the guides call the pooling
  flexibility a defining strength of the current build.
- **Thermal Void** — extends/empowers the **Icy Veins** burst window; you hold
  Flurry while its buff is up (the APL gates Flurry on `thermal_void.down`).
- **Splitting Ice** (cleave), **Splintering Ray / Frigid Focus** (AoE vs ST
  choice), **Piercing Cold** / **Rimecaster** / **Heart of Ice** (ST scaling),
  **Deep Shatter** / **Improved Shatter** (Shatter amp), **Everlasting Frost**,
  **Glacial Assault**, **Freezing Rain** (instant/buffed Blizzard) for AoE.
- **Cold Snap / Glacial Bulwark**, **Ice Cold** (Ice Block → damage-reduction you
  can cast through), **Permafrost Bauble** (Ice Block CD), **Winter's Protection**
  — defensive layer from the class tree.

## Reference talent import strings (12.0.7)

**simc default (Spellslinger)** — tier 1, from the MID1 profile:

```
CAEAAAAAAAAAAAAAAAAAAAAAAYGGLzMzsMmZmYmZmZMjZWMzMzMjZAAAgZmZWWmZaDAAAAAAsBw2yYmZGMLzDYMDLAAAMzCwMhBMDGA
```

**Icy Veins (Spellslinger), 12.0.7:**
- Single-target:
  `CAEAAAAAAAAAAAAAAAAAAAAAAYGGLzMzsMmZmYmZmZMjZWMzMzMjZAAAgZmZWWmZaDAAAAAAsBw22YmZGMLzDYMDLAAAMzCwMwAmBD`
- Raid / light cleave:
  `CAEAAAAAAAAAAAAAAAAAAAAAAYGGLzMzsMmZmYmZmZmZmZWMzMjZMDAAAMzMzyyMTbAAAAAAgNA22GzMzgZbYMDLAAAMzGwMwAmBD`
- Mythic+ / AoE:
  `CAEAAAAAAAAAAAAAAAAAAAAAAYGGLzMzsMmZmYmxMzMzMziZmZMjZAAAgZmZWWmZaDAA2AAAAWAYbbMzMDmthxMsAAAwMbAzADYGMA`

> ⚠ Import strings are tree-version-sensitive — confirm they load as
> **Spellslinger** in-game before trusting (one bad char breaks the import).
> @verify-ingame

The ST vs AoE Spellslinger strings mostly swap the AoE cluster (**Splintering
Ray**, **Freezing Rain**, **Cone of Frost**, **Ice Nova**) against ST scaling
(**Frigid Focus**, **Piercing Cold**, **Heart of Ice**), and shift the Ice Lance
Freezing threshold behavior — the rotation payoff, not new buttons.

## Stat priority

Sources lean **Crit ≈ Haste > Mastery > Versatility** for Frost, but secondaries
are flat this expansion — **ilvl generally wins**, tier pieces always win. Sim on
Raidbots when it's close. @verify-ingame — confirm the live S1 stat ordering
before committing gems/enchants (not deeply sourced here).

## Tier set (Midnight S1)

- **2pc:** Flurry damage +10%, and Flurry has a 10% chance to grant Fingers of Frost.
- **4pc:** Fingers of Frost increases Shatter damage +15%.

(From the Icy Veins rotation page; @verify-ingame the exact values against the
in-game set tooltip.)

## TODO

- [x] Hero-tree choice — **Spellslinger everywhere**, Frostfire = outdoor/alt (2026-07-11)
- [x] Reference talent strings — simc (tier 1) + Icy Veins ST/raid/M+ (2026-07-11)
- [ ] Confirm stat priority + tier-set values against live in-game data (@verify-ingame)
- [ ] Add gems/enchants/consumables + crafted/embellishment meta (not yet sourced)
