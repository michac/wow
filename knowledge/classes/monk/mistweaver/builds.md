---
title: Mistweaver Monk — Talents & Builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/mistweaver-monk/talents  # tier 3, upd. 2026-06-16
  - https://www.method.gg/guides/mistweaver-monk/playstyle-and-rotation  # tier 3, upd. 2026-06-16
  - https://www.icy-veins.com/wow/mistweaver-monk-pve-healing-rotation-cooldowns-abilities  # tier 3, 12.0.7
  - knowledge/classes/monk/mistweaver/talents.md  # tier 1 tree (Blizzard API + wago @ 12.0.7.67808)
confidence: medium
---

# Mistweaver Monk — Talents & Builds (Midnight S1)

Layer this on top of the full tree in `talents.md` (Tier-1, Blizzard API +
wago @ 12.0.7.67808). Builds below are Tier-3 (method.gg 12.0.7, upd.
2026-06-16; Icy Veins 12.0.7). No Tier-1 simc talent string exists for the
spec (simc doesn't model Mistweaver) — **confidence medium**.

## Hero tree: Conduit of the Celestials (raid + M+)

**Conduit of the Celestials is the favoured hero tree for both Raid and
Mythic+**, outperforming Master of Harmony across content. It adds
**Celestial Conduit** (a ~90s channeled AoE heal+damage nuke, movement-enabled),
routes cooldown reduction through **Heart of the Jade Serpent** after Thunder
Focus Tea, and caps out with **Unity Within**.

Key Conduit talents:
- **Celestial Conduit** — burst heal/damage channel; grants CDR to Rushing Wind
  Kick and Renewing Mist, driving the ramping loop.
- **Temple Training** (vs Xuen's Guidance) — boosts Enveloping Mist, Vivify and
  Sheilun's Gift healing; the **healing** pick for raid.
- **Courage of the White Tiger** — passive procs from Tiger Palm/Vivify;
  guaranteed proc after a Celestial cooldown.
- **Restore Balance** (vs Yu'lon's Knowledge) — healing amplification in the
  major-cooldown window; the raid pick.
- **Heart of the Jade Serpent** — CDR on key abilities after Thunder Focus Tea.
- **Jade Sanctuary** (vs Niuzao's Protection) — damage reduction while
  channeling Celestial Conduit (raid pick — separate DR instance).
- **Unity Within** — keystone; massively amplifies celestial effects (recast
  Celestial Conduit early to trigger it).

## Hero tree: Master of Harmony (alternative)

Underperforms Conduit but is more **damage-oriented in M+**. Everything hinges
on **Aspect of Harmony**: Thunder Focus Tea procs it, it **banks vitality** from
your healing and damage, and releases it as healing/damage later. Most of its
throughput comes through **Ancient Teachings** (damage→heal). Play is largely
passive beyond activating Thunder Focus Tea on cooldown. Requires engaging with
**Harmonic Surge** for its ceiling.

## Core spec talents & interactions

Near-mandatory / build-defining picks:

- **Save Them All** (class) — heals scale up on low-health targets; mandatory.
- **Rising Mist** (vs Tear of Morning) — Rising Sun Kick / **Rushing Wind Kick**
  extends the duration of your Renewing Mist and Enveloping Mist HoTs. The
  backbone of HoT-extension play.
- **Secret Infusion** — Thunder Focus Tea grants **haste** (Yu'lon path) or
  **versatility** (Chi-Ji path) after empowering a spell.
- **Ancient Teachings / Jadefire Teachings** — the damage→heal conversion.
  **Jadefire Teachings** (choice vs Rushing Wind Kick at 10,16) makes melee
  abilities (Tiger Palm, Blackout Kick, Rising Sun Kick) passively heal — the
  M+/Master-of-Harmony damage-healing engine.
- **Dance of Chi-Ji** — Spinning Crane Kick procs a free, empowered cast; key
  AoE damage→heal.
- **Awakened Jadefire** — Tiger Palm strikes twice, granting **two** Teachings
  of the Monastery stacks, smoothing the Fistweaving loop. @verify-ingame
- **Vivacious Vivification** (vs Serene Surge, class) — periodic **instant
  Vivify**, used in the cooldown loops.
- **Teachings of the Monastery** — Blackout Kick consumes stacks to strike extra
  times and has a 15% chance to reset Rising Sun Kick; **Celestial Harmony**
  grants 4 stacks when you summon Chi-Ji.
- **Refreshment** (vs Calming Coalescence) — Life Cocoon feeds Mana Tea stacks;
  supports casting Life Cocoon on cooldown in raid.

## Build variants (choice-node splits)

- **Rising Sun Kick vs Rushing Wind Kick** — Rushing Wind Kick *replaces* RSK
  (all modifiers transfer). **Rushing Wind Kick + Vivify** lean sees more play in
  **raid**; **Rising Sun Kick + Sheilun's Gift** in **Mythic+**.
- **Vivify vs Sheilun's Gift** — Sheilun's Gift replaces Vivify and shifts
  Invigorating Mists toward primary-target burst healing (raid uses Vivify's
  cleave; M+ uses Sheilun's burst).
- **Invoke Yu'lon vs Invoke Chi-Ji** — **Yu'lon** for raid (Chi Cocoon shields,
  cheaper Enveloping Mist), **Chi-Ji** for M+/mana-efficiency (Mastery procs off
  damage, instant Enveloping Mist, 4 Teachings stacks on cast).
- **Revival vs Restoral** — **Restoral** avoids stripping helpful Magic when you
  want the mass heal without a Magic dispel.
- **Ring of Peace vs Song of Chi-Ji** — CC utility preference.

## Import strings (method.gg, 12.0.7)

> Tier-3 strings — **confirm they load as the correct hero tree in-game** before
> trusting (one bad char breaks the import). No Tier-1 simc string exists to
> cross-check against. @verify-ingame

**Raid — Conduit of the Celestials (Rushing Wind Kick / Vivify):**
```
C4QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAghx2MwmFzYmZbGbYmZYmlttZGLMjmxMgBDGWmZmZYWGMYxEAAAAABYxyMLz2MDAAMgBYGwYYsMZMDA
```

**Raid — Conduit, Sheilun's Gift variant:**
```
C4QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAghx2MLDbWMjZmtZstsMjZYmlttZGLMjmxMgBDGWmZmZYWGMMLmAAAAAIALWmZZ2mZAAgBAYGwYYsIjZA
```

**Mythic+ — Conduit of the Celestials:**
```
C4QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMWmZZYxixMzsZsssND2Mz22yMjFmRzYGwgBDGWmZmhZbYGmlZCAAAAgAsYbmlZbmBAAAGgZADwiMmBA
```

**Mythic+ — damage-oriented (Master-of-Harmony-lean):**
```
C4QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgxMWGLjZz2MmZsYstsNjZ2Mz2yyMjFmRzYGwgBDLzMzMMbYGmlZCAAAAgAsYbmlZbmBAAAAMDYMwiMmBA
```

## Defensives / survivability

- **Fortifying Brew** — primary personal defensive, 2 min (1.5 min with
  **Expeditious Fortification**): −damage taken + max-HP bump.
- **Diffuse Magic** — magic damage reduction + debuff reflect.
- **Life Cocoon** — external absorb (also self-usable).
- Passive layers: **Yu'lon's Grace** (magic absorb shield), **Martial
  Instincts** (avoidance), **Flow of Chi** (5% DR at 35–90% HP), **Dance of the
  Wind** (stacking physical DR), **Elusive Mists** (6% DR on the Soothing Mist
  target), **Diffuse Magic**.

## TODO

- [ ] No Tier-1 simc talent string exists — corroborate the import strings and
      the raid/M+ split against a WCL top-parse loadout when available; raise
      confidence.
- [ ] Confirm Awakened Jadefire wording + the exact raid vs M+ hero-tree
      loadouts in-game.
