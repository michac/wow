---
title: Encomplete – Kil'jaeden (US) — main character snapshot
patch: 12.0.5
fetched: 2026-06-10
sources:
  - https://us.api.blizzard.com/profile/wow/character/kiljaeden/encomplete?namespace=profile-us
  - https://us.api.blizzard.com/profile/wow/character/kiljaeden/encomplete/equipment?namespace=profile-us
confidence: high
---

# Encomplete – Kil'jaeden (US)

> **Snapshot** — character data is volatile (updates on logout). Re-fetch
> before answering gear/progress questions; this file is for context, not
> live state. Raw JSON: `raw/blizzard/encomplete-*.json`.

**The user's current main.**

## Identity

- Gnome **Warlock**, active spec **Affliction** (Destruction + Demonology
  loadouts also saved)
- Level **90** (cap), Alliance, guild **The Soggy Bottom Boys** (Kil'jaeden)
- Title: Champion of the Frozen Wastes · 7,125 achievement points

## Gear (slot-average ilvl 251.2 — re-fetched live 2026-06-11)

| Slot | ilvl | Item |
|---|---|---|
| Head | **259** | **Abyssal Immolator's Smoldering Flames** (tier set piece — NEW; was 246 Silvermoon Sunspire) |
| Neck | 237 | Preyseeker's Choker (socket **1/1 filled** — was empty) |
| Shoulders | **263** | **Abyssal Immolator's Fury** (tier set piece) |
| Chest | **263** | **Abyssal Immolator's Dreadrobe** (tier set piece — NEW; was 253 Wretched Scholar's Gilded Robe) |
| Waist | 259 | Martyr's Waistwrap (spark craft) |
| Legs | **259** | **Abyssal Immolator's Pillars** (tier set piece — NEW; was Sprawling Rootstockings) |
| Feet | 250 | Sprawling Rootpads |
| Wrist | 233 | Sprawling Wristroots |
| Hands | 250 | Sprawling Tendrils (NEW 2026-06-11; was 233 Preyseeker's Refined Gloves) |
| Ring 1 | 246 | Preyseeker's Circle (socket **0/1 EMPTY**; NEW 2026-06-11, was 237 Forest Hunter's Hoop) |
| Ring 2 | 250 | Vibrant Wilderloop (socket 1/1) |
| Trinket 1 | 250 | Void-Reaper's Libram (NEW; was 246 Glorious Crusader's Keepsake) |
| Trinket 2 | 250 | Sylvan Wakrapuku |
| Back | 250 | Sprawling Mycoshroud (NEW; was 246 Voidbreaker's Cape) |
| Main Hand | 250 | Barbed Rootwand (NEW; was 246 2H Elderoot Spire) |
| Off Hand | 250 | Elderbloom Lantern (NEW — switched from a 2H staff to 1H wand + off-hand) |

**Major change since 06-07: 4-piece tier set is now active** —
Abyssal Immolator's head (259) / shoulders (263) / chest (263) /
legs (259) are all equipped, so the 4pc set bonus is live (was 1–2pc).
Neck socket is now filled; trinket/back/weapon all bumped to 250; moved
from a 2H staff to 1H wand + off-hand.

Notable gaps at 2026-06-11 fetch: **still ZERO enchants on every single
slot** (unchanged — biggest free upgrade outstanding). **One empty
socket**: the **new Ring 1 (Preyseeker's Circle) reads 0/1 — gem it**
(neck and Ring 2 sockets are both filled). Sub-250
slots are now **wrist 233** (the clear laggard), **neck 237**, and
**Ring 1 246**. Hands jumped 233→250 (Sprawling Tendrils).
Raw: `raw/blizzard/encomplete-equipment-2026-06-11.json`.

→ Tier set is complete, so the old "Catalyst the Hero legs into a 2pc
partner" plan is **DONE/obsolete**. Catalyst charges are now free to use
on non-tier upgrades elsewhere. Next gear priorities: **enchant
everything** + **gem the new Ring 1 socket**, then replace the lone
**233 wrist** (delve/ritual/spark) — it's the only sub-237 slot left.

## Season 1 progress

- **Mythic+**: no rated runs this season (keystone profile has no rating).
- **Raids**: no Midnight raid kills recorded. (Most recent recorded raid
  kills are Wrath-era — returning player.)

### Renown (API, re-fetched 2026-06-11)

| Faction | Renown | Progress to next |
|---|---|---|
| Silvermoon Court | **11** | 1235/2500 |
| The Singularity | **7** | 415/2500 |
| Amani Tribe | **7** | 1225/2500 |
| Hara'ti | **6** | 730/2500 |
| Ritual Sites | **2** | 632/2500 |
| Slayer's Duellum | Neutral | 300/3000 (now unlocked; API name is **Slayer's Duellum**, not "Slayer's Rise") |

→ All factions moved up since the 2026-06-03 fetch (Silvermoon 10→11,
Amani 6→7, Hara'ti 5→6, Singularity 5→7, Ritual Sites 1→2). Slayer's is
now showing on the API at Neutral standing.

Raw: `raw/blizzard/encomplete-reputations-2026-06-11.json`.

### Currencies (in-game screenshot, 2026-06-03 — ⚠ NOT API-exposed, likely stale)

> The profile API does **not** return character currencies or Delver's/
> Prey Journey ranks — these can only come from an in-game screenshot.
> Values below are from 2026-06-03 and were not refreshable on 2026-06-11.

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
- Spec context for KB lookups: `knowledge/classes/warlock/affliction/`.

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
6. Enchants on everything (zero detected at snapshot).
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
