---
title: Protection Paladin — Talents & Builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/protection-paladin/talents  # tier 3, upd. 2026-07-09
  - https://github.com/simulationcraft/simc/tree/midnight/profiles/MID1  # tier 1, MID1_Paladin_Protection.simc talent string
  - https://www.icy-veins.com/wow/protection-paladin-midnight-guide  # tier 3, 12.0.7
  - https://maxroll.gg/wow/class-guides/protection-paladin-raid-guide  # tier 3, 12.0.7
  - knowledge/classes/paladin/protection/talents.md  # tier 1 tree structure (Blizzard API + wago @ 12.0.7.67808)
confidence: medium
---

# Protection Paladin — talents & builds (Midnight S1)

Layer this over `talents.md` / `talents.json` (the full Tier-1 tree). This file
is the **narrative**: which hero tree, which loadout, and why.

## Hero tree

Both hero trees run the **same class and spec tree** — only the hero choice and a
single spec-tree point differ (method.gg). Pick by content:

- **Lightsmith — Mythic+ / dungeons (method's preferred).** Adds the **Holy
  Armaments** system (**Sacred Weapon** damage buff + **Holy Bulwark** absorb),
  **Rite of Sanctification** raid buff, and strong Apex synergy: **Reflection of
  Radiance** triggers extra **Grand Crusader** procs, feeding more Avenger's
  Shields. More absorb-heavy and forgiving; the straightforward pick for newer
  tanks.
- **Templar — raid / single-target (S1 raid edge).** Converts **Divine Toll**
  into a **Hammer of Light** burst button (12s window after Divine Toll) and
  layers **Shake the Heavens** (empowered hammers + damage reduction, extended by
  **Higher Calling**). Excels on single-target/patchwerk fights.

## Class + spec tree — the load-bearing talents

- **Righteous Protector** — flat cooldown reduction to Avenging Wrath (plus a
  duration trim), enabling the **~1-minute Wings** cadence that the whole
  rotation is tuned around. Near-mandatory.
- **Instrument of the Divine** — spends *excess* Holy Power into bonus Shield of
  the Righteous damage during high-resource phases (Wings / Divine Toll flood);
  the reason you SotR at 5 Holy Power inside burst instead of banking.
- **Divine Guidance / Blessed Assurance** (choice) — **Divine Guidance for M+**
  (5-stack Consecration → empowered Consecration/Shield of the Righteous),
  **Blessed Assurance for single-target raid** (empowers Hammer of the
  Righteous). Pick per content.
- **Grand Crusader + Bulwark of Order** — Avenger's Shield resets and grants an
  absorb; core to both the builder loop and the passive EHP layer.
- **Sanctified Plates / Holy Aegis / Faith's Armor** — passive mitigation floor.
- **Consecration in Flame / Sanctuary / Consecrated Ground** — reward staying in
  Consecration; big for AoE/M+.
- **Avenging Wrath vs Sentinel** (choice) — Avenging Wrath (offensive burst) is
  the default; **Sentinel** is the defensive-leaning alternative (stacking
  mitigation) for heavy-damage progression.
- **Improved Ardent Defender vs Blessing of Spellwarding** (choice) — extra
  Ardent Defender value vs a magic-immunity wall; pick per fight damage profile.
- **Final Stand** — makes Divine Shield also **taunt** (keeps threat during the
  immunity) — situational M+/raid utility pick.

## Hero-tree specifics

**Templar** — the Divine Toll → Hammer of Light loop is the identity:
- **Light's Guidance / Light's Judicator** wire Hammer of Light onto Divine Toll.
- **Shake the Heavens** upkeep is the skill test; **Higher Calling** extends it.
- **Undisputed Ruling**, **Endless Wrath / Sanctification**, **Hammerfall**,
  **Wrathful Descent** shape the burst; **Light's Deliverance** is the capstone.

**Lightsmith** — the Holy Armaments loop:
- **Holy Armaments** grants rechargeable **Sacred Weapon / Holy Bulwark** charges.
- **Rite of Sanctification / Rite of Adjuration** (choice) — raid buff.
- **Divine Guidance / Blessed Assurance**, **Solidarity**, **Hammer and Anvil**,
  **Reflection of Radiance** (extra Grand Crusader), **Blessing of the Forge**
  capstone.

## Build variants (method.gg 12.0.7)

- **Mythic+ (Lightsmith):** Divine Toll + **Divine Resonance** for interrupt
  coverage, **Blessed Hammer** over Hammer of the Righteous (AoE), **Punishment**
  for bonus casts on interrupt, **Divine Guidance** for the Consecration cluster.
- **Raid single-target (Templar):** **Shake the Heavens** maintenance, fewer
  Avenger's Shield casts, **Hammer of Light** burst windows, **Blessed
  Assurance** for empowered Hammer of the Righteous.

## Talent string (Tier-1 reference)

From the SimC **MID1_Paladin_Protection** profile (build 12.0.7.67808):

```
CIEAAAAAAAAAAAAAAAAAAAAAAsMzAzyMLmZMDLLDzYmFbzYAAAAAAAAg0MziZMmxYmt2AgBADsNAAwMTbzMbzAEYzADWMzMAzMAALzAMzAG
```

> Import strings are tree-version-sensitive — confirm the hero tree loads as
> intended before trusting. This SimC string is the profile's default loadout;
> the profile does not label its hero tree, so **verify Templar vs Lightsmith on
> import** and swap the hero + single spec point per content. @verify-ingame

## TODO

- [ ] Capture separate verified Templar (raid) and Lightsmith (M+) import
      strings from method.gg once its JS-rendered strings are extracted (the
      talents page confirms the split but the raw strings weren't in the fetch).
- [ ] Re-sim ST vs AoE hero-tree gap on the 12.0.7 build.
