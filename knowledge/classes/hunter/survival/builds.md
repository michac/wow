---
title: Hunter Survival — talents & builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight branch profiles/MID1/MID1_Hunter_Survival.simc  # tier 1 talent string, commit 9cedf7c 2026-07-12, WoW 12.0.7 (profile: MID1_Hunter_Survival_PL_DW)
  - https://www.method.gg/guides/survival-hunter/talents  # tier 3, Midnight 12.0.7 (upd. 2026-06-17)
  - https://hackmd.io/@Azortharion/MidnightHunterChanges  # tier 3, Midnight SV redesign notes
  - https://maxroll.gg/wow/class-guides/survival-hunter-mythic-plus-guide  # tier 3, 12.0.7
confidence: medium
---

# Hunter Survival — talents & builds (Midnight S1)

Layer this on top of `talents.md` / `talents.json` (the full node tree, from
Blizzard game data). This file is the **narrative**: hero-tree choice,
recommended loadouts, and the interactions that matter.

## Hero tree — Pack Leader (default) vs Sentinel

- **Pack Leader is the recommended pick for all PvE** (M+ and raid) after the
  12.0.5 buffs — Method: "Packleader currently outperforms Sentinel in all
  content." It **dual-wields** (daggers preferred): *Lethal Barbs* makes
  auto-attacks regenerate Focus, and two weapons roughly offsets the WDPS loss
  from not using a 2H. The engine is **Howl of the Pack Leader** — periodic
  Boar / Bear / Wyvern summons that add burst, kept fed by weaving Kill Command.
- **Sentinel is the 2H, defensive-leaning alternative.** It adds **Sentinel's
  Mark** (its rotation keys off the debuff) and the **Moonlight Chakram** button,
  and picks up *Don't Look Back* for defensives. Slightly behind Pack Leader on
  raw throughput in S1, but a fine survivability pick.

**Weapon rule:** Pack Leader → dual-wield (fast daggers help CDR/Focus);
Sentinel → two-hander. Manage loot spec accordingly — dual-wield roughly doubles
your usable weapon drops.

## Reference talent string (Tier 1, simc default — Pack Leader dual-wield)

```
C8PAAAAAAAAAAAAAAAAAAAAAAMgxMGWgNYGGawiZmZmZYZAAAAAAwMmZmx2MGzYGWGTzAAAAwAAjllZmZxMzMYMGwMbAGGjZmNDA
```

> This is the simc `MID1_Hunter_Survival_PL_DW` profile string (WoW 12.0.7).
> ⚠ Import strings are tree-version-sensitive — confirm it loads as **Pack
> Leader** in-game before trusting. Method.gg publishes **four** curated imports
> (Pack Leader ST + AoE, Sentinel ST + AoE) — pull the matching one for content
> type; captured here is the Tier-1 default. @verify-ingame

## Core spec talents (the build's spine)

The kit revolves around **Tip of the Spear** (Kill Command → up-to-2-stack buff
that empowers your next ability) and **Mongoose Fury** (Raptor Strike self-amp).
Near-universal picks:

- **Tip of the Spear** — the throughput engine; almost every button checks it.
- **Mongoose Fury** — "essentially baseline"; Raptor Strike stacks +10% dmg.
- **Takedown** — the 90s burst cooldown (+20% dmg 8s, 50 Focus, charge). Take
  **Savagery** to cut its cooldown toward 60s, and **Flanked** to make it cleave
  4 extra targets + grant attack speed (big in AoE).
- **Boomstick** — short-CD nuke, strong in both M+ and raid; choice node
  **Mongoose Rounds / Wildfire Shells** tunes its CD interactions.
- **Flamefang Pitch** — ~60s ground-fire AoE cooldown; extra charge via talent;
  feeds **Wildfire Imbuement**.
- **Wildfire Bomb** cluster — *Improved Wildfire Bomb*, *Wildfire Infusion*,
  *Grenade Juggler*; recharge scales with targets hit (AoE glue).
- **Raptor Swipe** (apex) — converts the Raptor Strike spender into a 5-target
  cleave; the single biggest AoE multiplier — take it for M+.
- **Twin Fangs** — changes Takedown/Kill Command sequencing (the APL has
  explicit `!talent.twin_fangs` branches); pick per build.
- **Lethal Calibration** — gates Wildfire Bomb usage in the ST APL (only bomb
  near charge cap when talented).

## Build split (ST vs M+/AoE)

- **Single target / raid:** Pack Leader, lean the Takedown + Mongoose Fury
  single-target cluster (Twin Fangs sequencing, Lethal Calibration bomb-gating).
- **M+ / AoE:** Pack Leader with **Raptor Swipe** (cleave spender) + **Flanked**
  Takedown + the Wildfire Bomb/**Flamefang Pitch** AoE cluster; Wildfire Bomb
  becomes near-on-cooldown as its recharge drops with targets hit.
- **Sentinel variants** exist for both (2H); run when you want the extra
  defensives / *Don't Look Back*, accepting a small DPS trade.

## Class-tree utility staples

Standard Hunter survivability/utility (see `talents.md` class tree): **Survival
of the Fittest**, **Born To Be Wild** (aspect CD reduction), **Natural Mending**
(Exhilaration CDR from Focus spend), **Misdirection**, **Muzzle**, **Intimidation**,
**Binding Shot**, **Tranquilizing Shot**, **Camouflage**, and the trap/CC picks
(**Tar Trap** vs Scare Beast, **Improved Traps**). Choice nodes worth noting:
**Roar of Sacrifice / Guardian's Hide** (external vs personal defensive),
**Trailblazer / Moment of Opportunity**, **Territorial Instincts / Guttural Roar**.

## Pet

Keep a pet out at all times (Kill Command and Howl beasts depend on it). Pick
family for utility — most bring a raid buff via a shared ability, and certain
families provide **Ancient Hysteria** (Bloodlust). Pack Leader's Howl summons
(Boar/Bear/Wyvern) are separate temporary beasts, not your permanent pet.

## TODO

- [ ] Capture Method.gg's four exact import strings (PL/Sent × ST/AoE) once the
      JS-rendered talents page yields them (only the simc default is stored).
- [ ] Confirm Savagery reduces Takedown to 60s and Flamefang Pitch base CD
      (30 vs 60s) against live tooltips — @verify-ingame in `abilities.md`.
- [ ] Add a gems/enchants/consumables section (mirror the Affliction builds.md
      layout) — not yet sourced for Survival.
- [ ] Re-verify Pack Leader > Sentinel after the next tuning pass.
