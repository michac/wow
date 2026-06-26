---
title: Encomplete – Kil'jaeden (US) — main character snapshot
patch: 12.0.7
fetched: 2026-06-23
sources:
  - https://us.api.blizzard.com/profile/wow/character/kiljaeden/encomplete?namespace=profile-us
confidence: high
---

# Encomplete – Kil'jaeden (US)

> **Snapshot** — character data is volatile (updates on logout). Re-fetch
> before answering gear/progress questions; this file is for context, not
> live state. Raw JSON: `raw/blizzard/encomplete-*.json`.
>
> ⚠ For **sims**, item IDs below are not enough — SimC needs the full
> `bonus_id` strings. Use the in-game **SimulationCraft addon** (`/simc`,
> or `/simc [item link]` for a single piece) and paste the export.

**The user's current main.**

## Identity

- Gnome **Warlock**, active spec **Demonology** (switched from Affliction;
  Destruction + Affliction loadouts presumably still saved)
- Level **90** (cap), Alliance, guild **Dungeon Dojo** (was The Soggy
  Bottom Boys)
- Title: Champion of the Frozen Wastes · 7,630 achievement points

## Gear (equipped ilvl 266, API 2026-06-23)

4pc tier equipped: **Abyssal Immolator's** (head/shoulders/chest/legs, 276).

| Slot | ilvl | id | Item |
|---|---|---|---|
| Head | 276 | 250042 | Abyssal Immolator's Smoldering Flames *(tier)* |
| Neck | 263 | 249626 | Nocturnal Thorncharm (gem: Quick Garnet) |
| Shoulders | 276 | 250040 | Abyssal Immolator's Fury *(tier)* |
| Chest | 276 | 250045 | Abyssal Immolator's Dreadrobe *(tier)* — ench: Mark of the Worldsoul |
| Waist | 259 | 239649 | Martyr's Waistwrap |
| Legs | 276 | 250041 | Abyssal Immolator's Pillars *(tier)* — ench: +41 Int |
| Feet | 266 | 263783 | Voidwind Boots |
| Wrist | 259 | 263849 | Void Nemesis' Bracers |
| Hands | 266 | 263813 | Handguards of Voidcendence |
| Ring 1 | 259 | 259912 | Preyseeker's Signet — ench: Eyes of the Eagle (gem: Quick Garnet) |
| Ring 2 | 259 | 249620 | Vibrant Wilderloop (gem: Eversong Diamond) |
| Trinket 1 | 253 | 251785 | Void-Reaper's Libram |
| Trinket 2 | 259 | 251784 | Sylvan Wakrapuku |
| Back | 250 | 249619 | Sprawling Mycoshroud |
| Main Hand | 285 | 245770 | Aln'hara Cane — ench: Acuity of the Ren'dorei |

Enchanted slots: chest, legs, ring1, weapon. **Missing enchants:** neck,
wrist, feet, ring2, back (and cloak could take an embellishment-tier ench).
Weakest slots vs the 276 tier: **back (250)** and **trinket 1 (253)**.

## Season 1 progress

- **Mythic+**: no rated runs this season (keystone profile has no rating).
- **Raids**: no Midnight raid kills recorded. (Most recent recorded raid
  kills are Wrath-era — returning player.)

### Renown (API, 2026-06-03)

| Faction | Renown |
|---|---|
| Silvermoon Court | 10 |
| Amani Tribe | 6 |
| Hara'ti | 5 |
| The Singularity | 5 |
| Slayer's Rise | — (no standing; likely not unlocked) |

### Currencies (verified from in-game currency tab screenshot, 2026-06-03)

- **10 Sparks of Radiance** banked (user-reported) · **6 Catalyst charges**
- Dawncrests: **Adventurer 111 · Veteran 165 · Champion 84** (no
  Hero/Myth visible — ~0; note Champion is 84, not the "100+" earlier
  assumed)
- **Field Accolade 220** (banking to 750 for 12.0.7 slot-targeted caches
  → 530 to go)
- Coffer Key Shards **75** + Restored Coffer Keys **5**
- Undercoin 5,045 · Voidlight Marl 6,646 · Remnant of Anguish 1,520 ·
  Brimming Arcana 590 · Radiant Spark Dust 13 · Dawnlight Manaflux 6

### Season journeys (in-game Journeys UI, 2026-06-03)

- **Prey: Season 1 — rank 3, progress 0/4000 to rank 4.** Rank 4 rewards:
  **Prey: Nightmare Mode** + "A Plinth Above the Rest I" — confirms the
  plan's Preyseeker-rank-4 → Nightmare unlock. 4,000 pts = exactly this
  week's 4× 1,000-pt hunts → **rank 4 is reachable this week**.
- **Delves: Season 1 — rank 3 ("Treasure Hunter"), 1160/4200 to rank 4
  ("Gilded Jackpot"** — the Myth-crest gilded stashes). Rank 5 = "An
  Ethereal and a Golem walk into a Delve" (Valeera shown on the pane),
  rank 6 = "Keys and Coffers".

Delve tier / Brann level: not exposed by API.
User-reported 2026-06-03: **clears T9 delves solo at ~236, but some
pulls are rough** — calibration point for content recommendations.

## Professions

- **Skinning** (Midnight tier 2/100, Classic-era tiers maxed)
- **Tailoring** (Outland/Classic tiers maxed; no Midnight tailoring tier yet)
- Cooking 214/300, Fishing 135/300 (Classic tiers)

## Implications for advice

- Gearing phase: world content / heroics → delves, M+, spark crafts.
  ilvl 236 is well below the 246–259 base spark-craft bracket — **spark
  crafting (2 sparks + crests) is a big upgrade in the 214/224 slots**.
- Tailoring is leveled in old tiers only; picking up Midnight Tailoring
  would let them self-craft spark gear.
- Enchants/sockets are low-hanging fruit.
- Spec context for KB lookups: `knowledge/classes/warlock/demonology/`
  (active spec as of 2026-06-23; Affliction loadout still saved, see
  `knowledge/classes/warlock/affliction/`).

> **Active plan moved to `encomplete-plan.md`** (priority checklist,
> weekly rotation, spend rules, milestones). Section below kept as the
> 2026-06-03 reasoning record.

## Gearing plan (sketched 2026-06-03, ilvl 236 baseline)

Rationale: base spark crafts hit **259 at max quality with zero crests**
— 23 ilvls over current average. Tier slots (head/shoulders/chest/legs/
hands) are reserved for the Catalyst — **VERIFIED 2026-06-03: crafted
gear cannot be catalyzed in 12.0** (Icy Veins/Wowhead catalyst guides).
Craft crestless at 259 now; recraft to 285 with Myth Dawncrests later
(recrafts don't refund crests, so skip the Hero-crest detour).

Revised 2026-06-03 after digesting SignsOfKelani 12.0.5 gearing video —
**ritual sites are now the primary solo engine** (see
`../systems/ritual-sites.md`, `../systems/void-forge.md`):

1. Spark-craft (~10 sparks): belt 214→259, wrist 233→259, boots 227→259,
   and 2H staff 246→259 (4 sparks) — carries both embellishments.
   Recraft to 285 later with Myth Dawncrests (20/wk from 4× T11
   bountiful delves, or M+9s).
2. **Ritual sites** (start at whatever tier is comfortable at 236; T5 =
   100+ accolades + 20 Hero crests/run): T4–5 push the vault world row
   to 269; do the Silvermoon challenge-unlock quests early.
   ⚠ The 500-accolade hero piece is a **random slot** (video comments,
   unverified) — strong value *now* at zero hero pieces (any roll likely
   upgrades), decaying as slots fill. Front-load purchases early; once
   ~half the slots are hero-track, accolade runs are mainly for crests +
   vault and sparks/vault/M+ take over for targeting.
3. **Voidforge**: run Decimus's 6-quest line → 2 Nebulous Void Cores/wk
   (bonus-roll hero gear from delves/prey). Start Ascendant Nilhammer
   weekly chain now — 4 weeks to unlock weapon/trinket overcap
   (285 craft → 295).
4. Catalyst (6 charges): catalyze highest-ilvl non-tier drops in tier
   slots for 2pc→4pc; legs (214) and shoulders (224) most urgent —
   accolade champion/hero vendor pieces work as catalyst fodder
   (vendor gear ≠ crafted; verify once in-game).
5. Champion crests (100+): upgrade champion-track drops; don't
   over-invest — hero pieces from accolades/delve renown 9 supersede.
6. Enchants on everything (zero detected at the 2026-06-03 snapshot;
   **partially done by the 2026-06-23 fetch** — chest/legs/ring1/weapon
   now enchanted, see the Gear table; neck/wrist/feet/ring2/back still
   open).
7. Tailoring: commission first crafts via crafting orders now; level
   Midnight Tailoring in background for self-crafting later.
8. Prey: **exactly 4 hunts/week** until Preyseeker rank 4 (first 4 =
   1,000 pts each, then 50 — never grind past 4) → Nightmare unlock
   questline → then beacon-only. Nightmare hunts drop Ascendant
   Voidshards. (Slayer's Rise: cosmetics-only PvP rep — deprioritized.)
9. Delves: **6 keyed bountifuls + the weekly quest item ≈ 1.3 Delver's
   Journey ranks/week** → rank 5 gear vendor ("nightcoin"/Untainted
   Mana Crystals — name unconfirmed), rank 9 = 276 hero vendor gear.
   Extra unkeyed runs = 125 rep, skip unless near a rank breakpoint.

API-tracked progress 2026-06-03: Ritual Sites renown 1, Valeera lvl 20.

## Talent audit (2026-06-03)

Active Affliction loadout simmed **−12.7% ST / −3.9% @4T** vs the simc
MID1 reference string on identical gear — 5 spec points in ≤3/50-usage
nodes (Withering Bolt ×2, Xavius' Gambit ×2, Improved Shadow Bolt) at
the cost of Improved Haunt / Patient Zero / Sow the Seeds / Drain Soul /
Cunning Cruelty, plus fringe defensive class picks over Demonic Circle /
Empowered Healthstone / Improved Mortal Coil. Details:
`../classes/warlock/affliction/builds.md` + `sims.md`.

## TODO

- [ ] Re-snapshot after gearing sessions (or just fetch live per doctrine)
- [ ] Re-audit talents after they respec (and re-sim with enchants on)
- [ ] Add WCL character parses subcommand to `wowkb.wcl` for this character
- [x] Verified 2026-06-03: crafted gear CANNOT be catalyzed in 12.0
- [x] Crest names confirmed: **Dawncrests** (Adventurer/Veteran/Champion/
      Hero/Myth tiers)
- [ ] Midnight Tailoring leveling cost (knowledge points, recipe access)
