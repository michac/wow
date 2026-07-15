---
title: Protection Warrior — Talents & Builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Warrior_Protection.simc  # tier 1 talent string + APL, 2026-07-11
  - https://www.method.gg/guides/protection-warrior/talents  # tier 3, Midnight 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/protection-warrior-pve-tank-guide  # tier 3, 12.0.7, 2026-07-11
  - https://maxroll.gg/wow/class-guides/protection-warrior-mythic-plus-guide  # tier 3, 12.0.7, 2026-07-11
confidence: medium
---

# Protection Warrior — Talents & Builds (Midnight S1)

Layers on `talents.md` / `talents.json` (the full Tier-1 tree dump) — this file
is the *narrative*: which hero tree, which loadout, and why. See `rotation.md`
for how the picks drive the priority.

## Hero tree: Mountain Thane (meta), Colossus (alt)

**Mountain Thane is the 12.0.7 pick** for both raid and Mythic+, single-target
and AoE — and, per method.gg, "the comparison is not especially close." The
12.0.7 tuning pass buffed **Thunder Blast** and trimmed a Colossus defensive
node, widening a gap that already favored the storm tree.

- **Mountain Thane** turns the AoE builder into a proc engine: `Lightning
  Strikes` converts `Thunder Clap` casts into empowered **`Thunder Blast`**,
  `Burst of Power` grants free `Shield Slam`s, `Storm Surge` slashes Thunder
  Clap's cooldown, and `Avatar of the Storm` + `Capacitance` make the Avatar
  window a Thunder-Blast burst. The tree is **proc-reactive** — its ceiling
  comes from spending Thunder Blast / Burst of Power stacks correctly, not from
  a fixed sequence (see `rotation.md` proc watch-list).
- **Colossus** adds the channeled nuke **`Demolish`** (spend at ≥3 `Colossal
  Might`) and leans on **`Revenge`** over Thunder Clap. It plays more like a
  cooldown-burst tank. Viable, currently behind Mountain Thane; pick it for
  feel or a Demolish-centric single-target profile.

## Reference talent string (Tier-1, simc `midnight`)

```
CkEAAAAAAAAAAAAAAAAAAAAAA02AAAzMDzMzMzMzmxsMjxYmGGDLzMzMDGzMAAAAYZAYGDwAbwyiRjZAMbYmNYGzMY2GAMzAAwMgB
```

This is the simc default (Mountain Thane) profile string for
`MID1_Warrior_Protection`. Import strings are tree-version-sensitive — confirm
it loads as **Mountain Thane** in-game before trusting. @verify-ingame

## Spec tree — core picks (12.0.7)

The rage/mitigation backbone the APL assumes is present:

- **Devastator** — auto-attacks free-cast Shield Slam; smooths the builder loop
  and rage income.
- **Booming Voice** — Demoralizing Shout generates 20 Rage + amps damage,
  promoting Demo Shout to a rotational button (it's in the opener and on-CD).
- **Heavy Repercussions / Into the Fray** and **Practiced Strikes** — the
  Shield Slam / Shield Block damage cluster (the APL's Ignore Pain conditions
  explicitly key off `talent.heavy_repercussions` + `talent.practiced_strikes`).
  Practiced Strikes got a 12.0.7 buff (+15% to Shield Slam / Revenge / Thunder
  Clap).
- **Violent Outburst** (+ Seeing Red) — empowers the next Shield Slam / Thunder
  Clap; a proc the AoE list checks (`buff.violent_outburst.up`).
- **Ravager** (over Whirling Blade) — the AoE-DoT cooldown + big rage generator
  used in the APL's opener and on CD.
- **Avatar** + **Anger Management** — Avatar to ~90s effective CD, the offensive
  window everything syncs to.
- **Shield Charge** — the ~45s gap-close/burst that also grants a Shield-Block
  buff; always on CD offensively.
- **Sudden Death** (vs Bloodborne) — free/anytime Execute procs, referenced
  throughout the Execute lines.
- Defensive core: **Last Stand**, **Shield Wall**, **Enduring Defenses**,
  **Brace For Impact**, **Tough as Nails**, **Bloodsurge**.

## Class tree — utility layer

Standard tank utility: **Shockwave** + **Rumbling Earth** (AoE stun, reduced CD
on 3+), **Storm Bolt** (ST stun), **Champion's Spear** (ranged burst + tether,
`Anger Management` synergy), **Intervene** + **Bounding Stride** / **Double
Time** (mobility), **Rallying Cry**, **Spell Reflection**, **Berserker Shout /
Fearless** (fear break), **Piercing Howl** vs **Intimidating Shout** (AoE slow
vs fear — take slow for M+ pull control), **Wrecking Throw / Shattering Throw**
with **Javelineer** (the APL uses the thrown attack when Javelineer is talented).

## Build variants

- **Mythic+ (Mountain Thane):** favors AoE throughput and pull control —
  Thunder Blast/Storm Surge cluster, Ravager, Champion's Spear, Shockwave +
  Rumbling Earth, Piercing Howl. `Heavy Handed` enables the multi-target
  Execute line in the `*_aoe` lists.
- **Raid/ST (Mountain Thane):** same hero core; can lean the single-target
  Shield Slam / Execute cluster and drop some AoE reach. Sudden Death + Deep
  Wounds carry the execute phase.
- **Colossus (alt):** swap the hero tree for **Demolish + Colossal Might +
  Dominance of the Colossus**; play Revenge-forward with Thunder Clap only for
  Rend upkeep. Behind Mountain Thane in 12.0.7 sims but fine for content.

## Key interactions (why the loop works)

- **Shield Block is offense + defense:** +30% Shield Slam damage *and* melee
  block — near-permanent uptime is both a survival and a DPS lever.
- **Ignore Pain is the rage valve:** the APL never lets a builder overcap —
  Ignore Pain absorbs the overflow, so mitigation is "free" throughput you'd
  otherwise waste.
- **Thunder Blast before Avatar (MT):** Avatar of the Storm refills stacks;
  dumping first avoids overcap.
- **Burst of Power (MT):** free back-to-back Shield Slams — react to the buff.
- **Booming Voice** makes Demoralizing Shout a *rage-positive* mitigation
  button, not just a raid cooldown.

## TODO

- [ ] Add gearing / stat-priority / enchant section (currently deferred to the
      general tank-gearing flow; sim on Raidbots when gear matters).
- [ ] Capture the M+ vs raid talent-string split from method.gg/talents once a
      clean Mountain Thane import string per-scenario is confirmed in-game.
- [ ] Re-verify the simc talent string if the tree changes in a later 12.0.x.
