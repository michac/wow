---
title: Protection Warrior — Rotation (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Warrior_Protection.simc  # tier 1 APL, 2026-07-11
  - https://www.method.gg/guides/protection-warrior/playstyle-and-rotation  # tier 3, Midnight 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/protection-warrior-pve-tank-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
  - https://maxroll.gg/wow/class-guides/protection-warrior-mythic-plus-guide  # tier 3, 12.0.7, 2026-07-11
confidence: high
---

# Protection Warrior — Rotation (Midnight S1)

Distilled from the SimulationCraft default APL (Tier 1, simc `midnight`
branch `MID1_Warrior_Protection.simc`), corroborated by method.gg and Icy
Veins (12.0.7). The APL splits by **hero tree** (`colossus_*` vs `thane_*`)
and by **target count** (single-target vs `*_aoe` at 3+). **Mountain Thane is
the meta build for 12.0.7** in raid and M+ — its lists (`thane_st` / `thane_aoe`)
are the primary path below; Colossus differences are noted inline.

The through-line: **spend Rage on active mitigation, then on damage, and never
overcap.** `Ignore Pain` is woven into the top of the list as a rage-dump so a
builder never wastes Rage — it out-prioritizes damage whenever the next cast
would overflow.

## Pre-combat

- `Battle Stance` on; Battle Shout up; snapshot stats. Pre-pot syncs to the
  first Avatar (APL potions on `buff.avatar.up`).

## Opener (ST and AoE identical, per method.gg)

1. **Charge** (into melee, seeds Rage — APL: `charge,if=time=0`)
2. **Avatar** + **Shield Block**
3. **Demoralizing Shout** (with Booming Voice)
4. **Ravager**
5. **Champion's Spear**
6. **Demolish** (Colossus only, at ≥3 Colossal Might)
7. **Shield Charge**
8. → into the general priority

## Cooldown rules

- **"Use everything on cooldown."** Avatar (~90s via Anger Management),
  Shield Charge (~45s), Demoralizing Shout, Ravager, Champion's Spear are
  all pressed on CD — they're rage generators as well as damage/defense.
- **Avatar timing (Mountain Thane):** dump your banked `Thunder Blast` stacks
  **before** pressing Avatar — Avatar of the Storm grants 2 fresh stacks, so
  you don't want to overcap. The APL gates it:
  `avatar,if=buff.thunder_blast.down|buff.thunder_blast.stack<=2`.
- **Potions/racials** fire inside the Avatar window (`buff.avatar.up`).
- **Defensives are separate from the damage loop:** `Shield Wall` (−40%,
  biggest personal), `Last Stand` (+30% HP), `Rallying Cry` (raid +15% HP),
  `Spell Reflection` (magic), `Demoralizing Shout` (−20% enemy damage) —
  pre-plan against boss casts / heavy hits, don't hold them to death.

## Active mitigation (always-on layer)

- **Shield Block** — keep it up while tanking; the APL refreshes at
  `buff.shield_block.remains<=10` and reacts to `Shield Slam` about to land.
  It also buffs Shield Slam +30%, so it's offense **and** defense.
- **Ignore Pain** — cast when Rage would otherwise overflow (the APL's long
  `ignore_pain,if=...rage.deficit<=15/17/18/20/40...` block), or when banking
  ≥70 Rage with a Shield Block window. **This is the rage-overflow valve** —
  it jumps ahead of any builder that would cap Rage.

## Single target — Mountain Thane (`thane_st`)

1. **Thunder Blast** (consume proc stacks — top priority when a stack is up)
2. **Thunder Clap** while **Ravager** is active
3. **Shield Slam** (on cooldown; watch **Burst of Power** for free casts)
4. **Thunder Clap** (filler / Rend upkeep)
5. **Thunder Blast** when Shield Slam is on CD and you'd otherwise idle
6. **Execute** with a **Sudden Death** proc, or at Rage ≥40
7. **Wrecking Throw / Shattering Throw** (with `Javelineer`)
8. **Revenge** — high Rage (≥80 outside execute), or on a `Revenge!` proc
9. **Devastate** (last-resort filler)

## Single target — Colossus (`colossus_st`)

1. **Shield Slam** (top priority)
2. **Thunder Clap** (Colossus presses it mainly to keep **Rend** up and to
   feed the Apex talents — *not* spammed)
3. **Revenge** while **Ravager** is up
4. **Execute** with `Sudden Death`, or with Deep Wounds at Rage ≥40
5. **Revenge** — high Rage or on proc
6. **Wrecking / Shattering Throw** (`Javelineer`)
7. **Devastate** filler
- Plus **Demolish** at ≥3 Colossal Might, folded in near the top of the shared
  action list (before the ST/AoE split).

## AoE / cleave (3+ targets)

Shared top of the list (both trees): **Ignore Pain** (overflow) → **Ravager**
→ **Demoralizing Shout** → **Champion's Spear** → **Thunder Blast** at 2 stacks
(≥2 targets) → **Demolish** (Colossus, ≥3 Might) → **Shield Charge** →
**Shield Block**, then branch:

**Mountain Thane (`thane_aoe`):**
1. **Thunder Blast** / **Thunder Clap** to refresh **Rend** (`rend_dot<=1`)
2. **Shield Slam** with **Violent Outburst** + **Phalanx** up
3. **Thunder Blast** on 2+ targets under **Avatar** (Capacitance)
4. **Shield Slam** with Phalanx up
5. **Thunder Clap** on 4+ under Avatar
6. **Revenge** at Rage ≥70 on 3+ targets
7. **Shield Slam** at Rage ≤60 or with Violent Outburst
8. **Thunder Blast** → **Thunder Clap** (filler / uptime)
9. **Execute** on 2+ with `Heavy Handed` (Rage ≥50 or Sudden Death)
10. **Revenge** at Rage ≥30 (≥40 with Barbaric Training)

**Colossus (`colossus_aoe`):** same shape but **Revenge is the primary spender**
and **Thunder Clap is only pressed to refresh Rend or as filler** — Colossus
leans on Revenge for AoE. Shield Slam still fires with Violent Outburst/Phalanx.

> **M+ threat note (Icy Veins/maxroll):** in dungeons, when new packs pull in,
> press **Thunder Clap** (or **Revenge** if Thunder Clap isn't ready, *even if
> it costs Rage*) **over Shield Slam** to snap aggro on the fresh mobs before
> returning to the single-target loop.

## Proc watch-list (Mountain Thane)

- **Thunder Blast** (2 stacks) — spend before it overcaps and before Avatar.
- **Burst of Power** — next 2 Shield Slams have no cooldown; chain them.
- **Storm Surge** — cuts Thunder Clap's CD hard; you can weave it ~every other
  GCD.
- **Seeing Red → Violent Outburst** (both trees) — empowers the next Shield
  Slam / Thunder Clap; don't let it fall off.

## TODO

- [ ] Sanity-check the opener against a top WCL Prot Warrior log
      (`wowkb.wcl rankings` → `casts`).
- [ ] Re-distill if simc publishes a retuned 12.0.7 `MID1_Warrior_Protection`
      APL (current pull is the live `midnight` branch as of 2026-07-11).
