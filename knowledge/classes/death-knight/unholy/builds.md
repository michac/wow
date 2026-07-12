---
title: Unholy Death Knight — Talents & Builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Death_Knight_Unholy.simc  # tier 1, talents=CwPAAAAAAAAAAAAAAAAAAAAAAAwMjZMDDz2MzMTzmZmZMjBAAAAAAAgZGmZAw2MmZ2mZGjZAbmFDDZgZjhGLAYGAGzMjZAmZmxYA (Rider default), 2026-07-11
  - https://www.method.gg/guides/unholy-death-knight/talents  # tier 3, 12.0.7 (upd. 2026-06-16), 2026-07-11
  - https://www.method.gg/guides/unholy-death-knight  # tier 3, 12.0.7 overview, 2026-07-11
confidence: medium
---

# Unholy Death Knight — talents & builds (Midnight S1)

Layer this on top of `talents.md` / `talents.json` (the full node dump from the
Blizzard Game Data API + wago DB2, Tier 1). This file is the *narrative*: which
hero tree, which loadout, and why. The core spec engine — two diseases +
**Lesser Ghoul** stack loop + Putrefy on charges + minion cooldowns — is fixed;
talents tune it. See `abilities.md` for the Midnight mechanic rework.

## Hero tree: Rider of the Apocalypse (default), San'layn (alt)

- **Rider of the Apocalypse** — the **simc default** (shipped profile is
  `MID1_Death_Knight_Unholy_Rider`) and Method's pick for **single-target /
  raid**, "also has some strong cases for AoE/cleave." Passively summons the
  **Four Horsemen** (Trollbane, Whitemane, Nazgrim, Mograine) via **Rider's
  Champion**; capstone **Apocalypse Now** fires all four at once. No extra
  rotational button — the horsemen ride along with your cooldown windows.
- **San'layn** — the **sustained-cleave / self-sustain** alternative. Adds
  **Vampiric Strike** (replaces some Scourge Strikes) building **Essence of the
  Blood Queen** stacks for passive damage + healing, with **Gift of the San'layn**
  as a layered burst on Dark Transformation. Less raw single-target than Rider
  (Method). Pick it for heavy sustained multi-target or when the extra leech
  matters. @verify-ingame (San'layn vs Rider S1 usage split — no murlok/WCL
  aggregation pulled this pass)

## Reference loadout (simc default, Rider — Tier 1)

Talent import string straight from the MID1 profile (Rider):

```
CwPAAAAAAAAAAAAAAAAAAAAAAAwMjZMDDz2MzMTzmZmZMjBAAAAAAAgZGmZAw2MmZ2mZGjZAbmFDDZgZjhGLAYGAGzMjZAmZmxYA
```

> ⚠ Import strings are tree-version-sensitive — one wrong character breaks the
> import. This is the 12.0.7 simc string; re-verify if the tree changes. Confirm
> it loads **as Rider of the Apocalypse** in-game. @verify-ingame

Method.gg lists three named Rider builds (import strings on the site):
1. **[Raid] Riders Single Target** — leans the minion package: **Reanimation,
   Outnumber, Commander of the Dead** (buff/summon undead).
2. **[Raid/Mythic+] Riders Cleave** — adds **Menacing Magus** + **Sweeping Claws**
   for cleave off the Magus and the transformed Ghoul.
3. **[Raid/Mythic+] Riders AoE** — a slight variation on Cleave.

## Key talent interactions (the levers that change the rotation)

- **Festering Scythe** (`455397`) — turns Festering Strike into a maintained-buff
  builder; the APL keeps `festering_scythe` refreshed and gates Army of the Dead
  behind its trigger buff. Present in the default build.
- **Superstrain** (`390283`) — spreads your diseases automatically (and lets
  Scourge Strike apply Virulent Plague to fresh targets), the backbone of the
  low-maintenance disease model.
- **Sudden Doom** (`49530`) + **Harbinger of Doom** (`276023`) — the proc engine
  that makes Death Coil free + empowered; Sudden Doom procs are the top spend in
  the priority.
- **Commander of the Dead** (`390259`) — Dark Transformation (near Army / Raise
  Abomination) buffs minion damage; the APL times **Putrefy** to land while its
  buff has >9s left. This is why you bank Putrefy for the Dark Transformation window.
- **Cycle of Death** (`1290864`) — **Death and Decay reduces Putrefy's cooldown**;
  this is *why* DnD leads the AoE list even though it's not big raw damage.
- **Reaping** (`377514`) — grants near-free **Soul Reaper** casts tied to Dark
  Transformation, so Soul Reaper is pressed as burst well above 35% HP.
- **Forbidden Knowledge** (`1242158`, apex) — after **Army of the Dead**,
  transforms Death Coil → **Necrotic Coil** and empowers Epidemic for 30s, and
  raises the AoE spend breakpoint (epidemic_prio 4→6 targets while up). Changes
  the spend cadence during burst (`spending_rp` opens up to Rune<4 with it up).
- **Blightburst** (`1254552`) / **Blightfall** (`1271974`) — reorder the opener:
  Blightburst delays **Outbreak** behind the first **Putrefy**; Blightfall shifts
  the **Soul Reaper** condition. Both are conditional lines in the APL.
- **Choice nodes that matter:** **Clawing Shadows** (Scourge Strike becomes
  ranged shadow damage — QoL + range), **Plague Mastery / Grave Mastery**,
  **Raise Abomination / Summon Gargoyle** (the 90s summon — default leans Raise
  Abomination for the minion-damage-taken debuff), and **Asphyxiate / Death's
  Reach** in the class tree (stun vs long-range grip).

## Consumables & runes (from the simc profile, Tier 1)

- **Potion:** Potion of Recklessness (`potion_of_recklessness_2`)
- **Flask:** Flask of the Magisters
- **Food:** Silvermoon Parade feast
- **Augment rune:** Void-Touched
- **Weapon oil:** Thalassian Phoenix Oil (main hand)
- **Omnium runes** (Midnight Omnium Folio system): Rune of Unleashed Fire /
  Lynxlike Reflexes / Lingering / Critical Power / Overload.

## Stat priority

Not resolved from a Tier-1 sim sweep this pass. The simc reference gear skews
**Crit ≈ Mastery > Haste** (crit 1111 / mastery 1159 / haste 281 rating), but
that's one gear set, not a stat-weight run. Secondaries are typically flat in
Midnight — **ilvl and tier-set pieces win**; sim on Raidbots when it matters.
@verify-ingame (stat weights — no stat-priority source fetched)

## TODO

- [ ] Pull method.gg's three named Rider import strings verbatim (page is
      JS-rendered; only the build *names* came through this pass).
- [ ] Add a San'layn reference string + usage-split data (murlok / WCL) to
      settle the Rider-vs-San'layn recommendation with real numbers.
- [ ] Stat-priority + enchant/gem/embellishment section (as in the Affliction
      `builds.md`) — none sourced yet.
- [ ] Cross-check the 12.0.5 structural changes Method notes (removed Blightfall/
      March of Madness/Scythe of Decay; added Cycle of Death) against `talents.md`.
