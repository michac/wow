---
title: Brewmaster Monk — Talents & Builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight branch profiles/MID1/MID1_Monk_Brewmaster.simc  # tier 1 talent string, WoW 12.0.7, fetched 2026-07-11
  - https://www.method.gg/guides/brewmaster-monk/talents  # tier 3, upd. 2026-06-17
  - https://www.icy-veins.com/wow/brewmaster-monk-pve-tank-spec-builds-talents  # tier 3, 12.0.7
  - https://www.wowhead.com/guide/classes/monk/brewmaster  # tier 4, corroboration
confidence: medium
---

# Brewmaster Monk — Talents & Builds (Midnight S1)

Layer this on top of `talents.md` / `talents.json` (the full tree dump). This
file is the *narrative*: which hero tree, which build, and why. See `rotation.md`
for how the picks are actually pressed.

## Hero tree: Shado-Pan vs Master of Harmony

Both are **fully viable** in all content in 12.0.7 — the choice is content-lean
and playstyle preference, not a hard performance gate (Method, Icy Veins).

- **Shado-Pan** — the **Mythic+ / big-pull** pick. Physical burst AoE via
  **Flurry Strikes** plus passive defense, and an empowered **Invoke Niuzao**
  window. Simpler to pilot: press Keg Smash, cleave, and lean on Niuzao. Key
  nodes: **Martial Precision** (physical amp), **Predictive Training** (dodge →
  damage resistance), **Against All Odds**, **Whirling Steel**.
- **Master of Harmony** — the **raid / single-target** pick. **Aspect of
  Harmony** banks a fraction of your damage/healing into a large **Celestial
  Brew** discharge (absorb + damage), and the tree grants a **second Celestial
  Brew/Infusion charge** for smoother, more self-reliant mitigation. Pushes
  single-target the highest and is the more defensively flexible tree. Key nodes:
  **Manifestation**, **Balanced Stratagem**, **Overwhelming Force**,
  **Mantra of Purity / Mantra of Tenacity** (choice), **Coalescence** (capstone).

> Midnight simplification: **Weapons of Order** (the old TWW Master-of-Harmony
> keystone) is **gone** from Brewmaster — MoH now runs on **Aspect of Harmony**.
> **Rising Sun Kick** is also no longer in the Brewmaster kit.

## The apex talent: Bring Me Another

`Bring Me Another` (spec tree row 12, spell 1265129) is the Midnight capstone the
whole rotation orbits:

- Consuming a **Brew** has a chance (~20%) to grant an **Empty Barrel** (hold max 1).
- Your next **Keg Smash** throws the barrel for **bonus physical damage** (and it
  **ricochets** to extra targets in AoE).
- Higher ranks: the barrel **resets Keg Smash's cooldown** and cuts its **Energy
  cost (~50–100%)**, and **Fortifying/Celestial Brew** hand nearby allies a
  **Refreshing Drink** heal.

In the APL this surfaces as `buff.empty_barrel` and `apex.1 / apex.3` rank checks
— many brew casts are guarded with `!(apex.N & buff.empty_barrel.up)` so you don't
waste a brew (or the barrel state) at those ranks. Practically: **when an Empty
Barrel is up, get a Keg Smash out to spend it.** @verify-ingame (exact proc % and
rank behavior)

## Core spec talents (both builds)

Near-universal picks (Method / Icy Veins, 12.0.7):

- **Keg Smash**, **Purifying Brew**, **Shuffle** — the mandatory backbone.
- **Blackout Combo** (choice vs Press the Advantage) — Blackout Kick empowers the
  next Tiger Palm; the standard ST-facing pick and a rotation cornerstone.
- **Charred Passions** (choice vs Dragonfire Brew) — Blackout Kick refreshes/echoes
  Breath of Fire fire damage; strong cleave and the Sal'salabim's/Scalding synergy.
- **Sal'salabim's Strength** (choice vs Scalding Brew) — keeps Breath of Fire's
  debuff up and lets Keg Smash reset it; the APL leans on it during Niuzao.
- **Stormstout's Last Keg** — a second Keg Smash charge; smooths the "never miss
  Keg Smash" rule.
- **Empty the Cellar** — brew cooldown value; "nearly always recommended" (Method).
- **Niuzao's Resolve** + **Tranquil Spirit** — passive self-sustain; recommended
  for learning/durability.
- **Elixir of Determination** — 1-point absorb that fires on purification.
- **Invoke Niuzao, the Black Ox**, **Exploding Keg**, **Fortifying Brew:
  Determination** — the cooldown package.
- **Celestial Brew vs Celestial Infusion** (choice, row 6): **Celestial Infusion**
  is the common M+/MoH pick (spreads the absorb, "easier to heal"); **Celestial
  Brew** is the burstier single-absorb option. Swap per encounter.

## Build differences

- **Rushing Jade Wind vs Special Delivery** (choice): **Rushing Jade Wind** procs
  Walk with the Ox more and gives better sustained threat but demands the button
  press; **Special Delivery** is passive AoE with less rotation pressure — the
  simplicity pick for M+.
- **Shado-Pan (M+)** leans burst-AoE + Predictive Training defense; the standard
  M+ build.
- **Master of Harmony (raid)** leans Aspect-of-Harmony sustain + the extra
  Celestial charge for progression fights.

## Talent import strings (12.0.7)

**Tier-1 — simc MID1 default** (Shado-Pan, from `MID1_Monk_Brewmaster.simc`):

```
CwQAAAAAAAAAAAAAAAAAAAAAAAAAAgZbzYGzM2mxGmZAAAAAAAYZBjYmBmhBzYMzMzwsMmZMzywymttxMmFAAYZWmWmtZWGAAIAzwGYmBMNGAAwA
```

**Tier-3 — Method / Icy Veins** (re-verify the hero tree on import; one bad char
breaks the string):

- Raid Standard / Defensive (Master of Harmony), Method:
  `CwQAAAAAAAAAAAAAAAAAAAAAAAAAAwMbbGzYGzyM2wMjBAAAAAAYZBzEzMwMMzGDmZmZY2GmxMLPALbW2mlhZBAA2QAAAmtZpZmZ2YYDgZGmGDAAYA`
- Raid Advanced / Offensive (Black Ox Brew lean), Method:
  `CwQAAAAAAAAAAAAAAAAAAAAAAAAAAwMbbGzYGWmxGmZMAAAAAAALLYmYmBmhZ2YwMzMDz2wMmZ5BYZz22YGzCAAshAAAMbzSzMzsZG2AYmhpxAAAG`
- M+ Standard (Shado-Pan), Method:
  `CwQAAAAAAAAAAAAAAAAAAAAAAAAAAwMbbGDPwYWmx2wMjBAAAAAAYZBzEzMwMMzmBmZmZY2YmxYZYZ7BW2mthZBAA2QAAAmtZpZmZ2YYDgZGmGDAAYA`
- Defensive Raid (Master of Harmony), Icy Veins:
  `CwQAAAAAAAAAAAAAAAAAAAAAAAAAAgZbzYGPwYWM2mxMDAAAAAAALLYEmBmhxmZMmZmZMzywMmZZYZzy2sMMLAAwysMtMbzsMAAAAzwGYmBMNGAAwA`
- Standard M+ (Shado-Pan), Icy Veins:
  `CwQAAAAAAAAAAAAAAAAAAAAAAAAAAwMLbGDzwyM2MmZAAAAAAAYZBmYmBmhBzgZmZGzsNMjZWGW2ssNbzYWAAglZZaZ2mZZAAAAMsBmZATjBMAgB`

> ⚠ Import strings are tree-version-sensitive; these are captured for 12.0.7.
> Re-check after any talent-tree change. The simc string is the Tier-1 floor.

## TODO

- [ ] Confirm Bring Me Another apex numbers (proc %, cost cut, Refreshing Drink)
      from game data — @verify-ingame.
- [ ] Add stat priority + gearing (crests/embellishments/enchants) once a
      Brewmaster-specific 12.0.7 gearing source is distilled (parallel to the
      Affliction `builds.md` gearing section).
- [ ] Verify each Tier-3 import string loads as the stated hero tree in-game.
