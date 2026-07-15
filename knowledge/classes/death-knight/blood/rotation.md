---
title: Blood Death Knight — Rotation (Midnight Season 1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight branch engine/class_modules/apl/apl_death_knight.cpp  # tier 1 APL (blood_apl_start → blood_apl_end), fetched 2026-07-11
  - https://www.method.gg/guides/blood-death-knight/playstyle-and-rotation  # tier 3, Midnight 12.0.7 (author: Reholy)
  - https://www.method.gg/guides/blood-death-knight  # tier 3, Midnight 12.0.7 intro
confidence: high
---

# Blood Death Knight — Rotation (Midnight S1)

Distilled from the SimulationCraft default Blood APL (Tier 1) and corroborated
by method.gg's 12.0.7 playstyle guide (Tier 3). The APL branches by hero tree:
**Deathbringer** and **San'layn** (with a separate `san_gift` list for the
Gift of the San'layn burst window). Both share the same high-priority defensives
and Bone Shield upkeep.

Blood is resource/buff management, not a fixed rotation. The universal rules
(method.gg): **never overcap Runic Power, never sit on capped Blood Boil charges,
keep 3 runes recharging as often as possible, and use cooldowns on cooldown.**

## Pre-combat

- `snapshot_stats`
- **Death's Caress** — applies Blood Plague + first Bone Shield stack at range
  before the pull.

## Cooldown / high-priority rules (both hero trees)

These fire before the hero-tree list every GCD (`high_prio_actions`):

1. **Raise Dead** off-GCD (opener / when the ghoul is down).
2. **Death Strike** immediately if **Coagulopathy** is about to expire
   (`buff.coagulopathy.remains<=gcd`) — don't drop the stacking heal-amp.
3. **Dancing Rune Weapon** when it won't clip an Exterminate/Reaper's Mark
   window and DRW isn't already up, gated to `fight_remains>95 | fight_remains<25
   | time>300` (i.e. use it early, at execute, or once the fight is long enough
   to get full value).

Defensive/throughput layer (from `default`):

- **Vampiric Blood** whenever it isn't already up — the most-used defensive; the
  APL keeps near-100% uptime. method.gg: "Vampiric Blood takes precedent in a
  cooldown plan" because it comes back so often.
- **Potion / racials** (fireblood, blood_fury, berserking, ancestral_call) and
  **on-use trinkets** sync to the Dancing Rune Weapon window
  (`cooldown.dancing_rune_weapon.remains>78`) or the execute (`fight_remains` low).
- Reactive defensives by damage type (method.gg): **Anti-Magic Shell** vs magic,
  **Icebound Fortitude** as the standard big-hit button, **Lichborne** for
  throughput/self-heal during high-damage phases, **Death Pact** as an emergency
  ~50% top-up.

## Deathbringer priority (M+ default)

Opener: Death's Caress (pre) → Death and Decay → **Reaper's Mark** + Raise Dead →
Dancing Rune Weapon (+ potion) → Blood Boil → Marrowrend (consume Exterminate).
Reaper's Mark goes **before** DRW so the two stay synced (DRW doesn't duplicate
the Mark).

Sustained list (simc `deathbringer`):

1. **Death Strike** when Runic Power is near cap (`deficit<20`, or `<26` during
   Dancing Rune Weapon) — dump RP, don't overcap.
2. **Death and Decay** if its buff isn't up (maintenance).
3. **Reaper's Mark** on cooldown.
4. **Marrowrend** if **Exterminate** is up (consume the proc).
5. **Death's Caress** if Bone Shield is missing / <3s / <6 stacks **and** rune-starved (`rune<4`).
6. **Marrowrend** if Bone Shield is missing / <3s / <6 stacks.
7. **Death Strike** (spend RP).
8. **Blood Boil** (keep charges/Blood Plague flowing).
9. **Consumption** (empowered rank 1) when **not** inside Dancing Rune Weapon.
10. **Heart Strike** (filler).
11. **Consumption** (empowered rank 1) — fallback.
12. (Arcane Torrent for RP if racial.)

## San'layn priority (raid default)

Opener: Death's Caress (pre) → Death and Decay → Dancing Rune Weapon + Raise Dead
(+ potion) → Blood Boil → Vampiric Strike ×2 → Death Strike.

Sustained list (simc `sanlayn`):

1. **Death's Caress** if Bone Shield is basically gone (`stack<=1` / <1.5s).
2. **Blood Boil** if **Blood Plague** has <3s left (keep the disease up).
3. **Heart Strike** if **Essence of the Blood Queen** is about to fall off
   (`remains<1.5`) and a Vampiric Strike is active — refresh the buff.
4. **Death Strike** when RP is near cap (`deficit<20`).
5. **Death's Caress** / **Marrowrend** if Bone Shield <6 stacks.
6. **Death and Decay** on a **Crimson Scourge** proc (free/instant).
7. **Heart Strike** when **Vampiric Strike** is up (spend the proc, stack Essence).
8. **Death Strike** (spend RP).
9. **Blood Boil** on a **Boiling Point** proc (and echo not up).
10. **Consumption** (empowered rank 1).
11. **Heart Strike** if `rune>=2`.
12. **Blood Boil** → **Heart Strike** (fillers).

### San'layn — Gift of the San'layn window (`san_gift`)

While **Gift of the San'layn** is up (the burst window; Heart Strike is
temporarily the Vampiric Strike-empowered button):

1. **Heart Strike** if Essence of the Blood Queen is about to expire.
2. **Death Strike** if `runic_power.deficit<36`.
3. **Blood Boil** if the rune weapon's Blood Plague isn't ticking.
4. **Death and Decay** on a Crimson Scourge proc.
5. **Heart Strike** while Essence stacks `<7` (build to max).
6. **Death Strike**.
7. **Blood Boil** on a Boiling Point proc (echo not up).
8. **Heart Strike** → **Blood Boil** (fillers).

## AoE / multi-target

Blood does not swap to a separate AoE action list — the same priority scales:
**Blood Boil** (cleave + Blood Plague on everything), **Death and Decay** (kept
down as a maintenance + AoE zone, free on Crimson Scourge), and **Heart Strike**
(hits up to 5 with Cleaving Strikes) carry multi-target. **Consumption** (frontal
cone) and **Gorefiend's Grasp** (mass grip) are the AoE pickup/burst tools. Keep
Bone Shield and RP-dumping identical to single target — survival first.

## Hero-tree summary

- **Deathbringer (M+):** press **Reaper's Mark** and **Dancing Rune Weapon** on
  cooldown and synced; consume **Exterminate** with Marrowrend; more approachable,
  tankier (doubled Blood Plague healing + steady damage reduction).
- **San'layn (raid):** keep **Essence of the Blood Queen** stacks alive via
  Vampiric Strike/Heart Strike, line **Consumption** and **Dancing Rune Weapon**
  up, and exploit the **Gift of the San'layn** burst window.

## TODO

- [ ] Sanity-check the opener against a top WCL Blood log (`wowkb.wcl` casts).
- [ ] Re-distill if the simc midnight branch publishes a retuned 12.0.7 Blood APL
      (current pull is the midnight-branch `blood_apl_start` as of 2026-07-11).
