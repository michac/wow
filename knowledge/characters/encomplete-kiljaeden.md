---
title: Encomplete – Kil'jaeden (US) — main character snapshot
patch: 12.0.7
fetched: 2026-06-20          # identity/gear/renown/professions refreshed; currencies + season journeys still from 2026-06-03
sources:
  - https://us.api.blizzard.com/profile/wow/character/kiljaeden/encomplete?namespace=profile-us
confidence: high
---

# Encomplete – Kil'jaeden (US)

> **Snapshot** — character data is volatile (updates on logout). Re-fetch
> before answering gear/progress questions; this file is for context, not
> live state. Raw JSON: `raw/blizzard/encomplete-*.json` (refreshed 2026-06-20;
> last in-game logout 2026-06-21 UTC).

**The user's current main.**

## Identity

- Gnome (male) **Warlock**, active spec **Demonology** as of 2026-06-20
  (Affliction + Destruction loadouts also saved) — **spec change since the
  2026-06-03 audit; talent audit below is Affliction-only and now stale.**
- Level **90** (cap), Alliance, guild **Dungeon Dojo** (Proudmoore — joined a
  cross-realm guild; was "The Soggy Bottom Boys" on Kil'jaeden)
- Title: Champion of the Frozen Wastes · 7,435 achievement points

## Gear (equipped avg ilvl 261, overall avg 262, 2026-06-20)

| Slot | ilvl | id | Item |
|---|---|---|---|
| Head | 276 | 250042 | Abyssal Immolator's Smoldering Flames *(tier)* |
| Neck | 256 | 249626 | Nocturnal Thorncharm |
| Shoulders | 263 | 250040 | Abyssal Immolator's Fury *(tier; Champion-maxed)* |
| Chest | 276 | 250045 | Abyssal Immolator's Dreadrobe *(tier)* |
| Waist | 259 | 239649 | Martyr's Waistwrap *(crafted)* |
| Legs | 276 | 250041 | Abyssal Immolator's Pillars *(tier)* |
| Feet | 259 | 263783 | Voidwind Boots *(Hero 1/6 — accolade buy 2026-06-19)* |
| Wrist | 250 | 249636 | Sprawling Wristroots |
| Hands | 259 | 263813 | Handguards of Voidcendence *(Hero 1/6 — accolade buy 2026-06-19)* |
| Ring 1 | 259 | 259912 | Preyseeker's Signet *(vault pick 2026-06-18)* |
| Ring 2 | 253 | 249620 | Vibrant Wilderloop (gem `26stragiint`) |
| Trinket 1 | 250 | 251785 | Void-Reaper's Libram |
| Trinket 2 | 259 | 251784 | Sylvan Wakrapuku |
| Back | 250 | 249619 | Sprawling Mycoshroud |
| Main Hand | 272 | 245770 | Aln'hara Cane *(crafted)* |

**4-piece Abyssal Immolator tier** = head/shoulders/chest/legs (head/chest/legs
now crested to 276; shoulders the only tier slot still Champion-capped at 263 —
needs a Hero piece + Catalyst).

**Lowest / next upgrade targets:** Wrist 250, Back 250, Trinket 1 250,
Ring 2 253, Neck 256. Hero-track pieces to crest toward 276:
Hands/Feet/Signet (259, Hero 1/6). Shoulders (263) still the worst tier slot.

> Gear-decision rationale and sims: `../classes/warlock/affliction/sims.md`
> (vault pick + Field-Accolade slot priority, 2026-06-18/19).

> ⚠ **API-derived sections (identity, gear, renown, professions, M+/raid
> progress) were refreshed 2026-06-20.** The **Currencies** and **Season
> journeys** blocks below are still from the 2026-06-03 in-game screenshots
> (not exposed by the profile API) — re-verify those live before relying on them.

## Season 1 progress

- **Mythic+**: no rated runs this season (keystone profile has no rating).
- **Raids**: no Midnight raid kills recorded. (Most recent recorded raid
  kills are Wrath-era — returning player.)
- **Companions** (API, 2026-06-20): Brann Bronzebeard **Level 45**,
  Valeera Sanguinar **Level 37** (was 20 on 2026-06-03).

### Renown (API, 2026-06-20)

| Faction | Renown | Δ since 2026-06-03 |
|---|---|---|
| Council of Dornogal | 25 | (TWW carryover, maxed) |
| Silvermoon Court | 11 | +1 |
| Amani Tribe | 8 | +2 |
| The Singularity | 7 | +2 |
| Hara'ti | 6 | +1 |
| Ritual Sites | 2 | +1 |
| Slayer's Duellum | tier 3 (Neutral) | now showing (the Slayer's Rise PvP rep) |

### Currencies (verified from in-game currency tab screenshot, 2026-06-03 — STALE)

- **10 Sparks of Radiance** banked (user-reported) · **6 Catalyst charges**
- Dawncrests: **Adventurer 111 · Veteran 165 · Champion 84** (no
  Hero/Myth visible — ~0; note Champion is 84, not the "100+" earlier
  assumed)
- **Field Accolade 220** (banking to 750 for 12.0.7 slot-targeted caches
  → 530 to go)
- Coffer Key Shards **75** + Restored Coffer Keys **5**
- Undercoin 5,045 · Voidlight Marl 6,646 · Remnant of Anguish 1,520 ·
  Brimming Arcana 590 · Radiant Spark Dust 13 · Dawnlight Manaflux 6

### Season journeys (in-game Journeys UI, 2026-06-03 — STALE)

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

## Professions (API, 2026-06-20)

- **Skinning** — Midnight 2/100, Dragon Isles 12/100, Classic/Outland/
  Northrend tiers maxed.
- **Tailoring** — **Midnight Tailoring 97/100** (was 0 on 2026-06-03 — they
  leveled it nearly to cap; can now largely self-craft Midnight spark gear).
  Outland/Classic maxed; Northrend 37/75.
- Cooking 214/300 (Classic) + Draenor 1/100, Fishing 135/300 (Classic).

## Implications for advice

- Gearing phase: world content / heroics → delves, M+, spark crafts.
  ilvl 236 is well below the 246–259 base spark-craft bracket — **spark
  crafting (2 sparks + crests) is a big upgrade in the 214/224 slots**.
- **Midnight Tailoring is now 97/100** — they can self-craft spark gear
  (and the cloth spark pieces / embellishments) rather than commissioning
  crafting orders. Finish the last 3 points.
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

## Talent audit (2026-06-03 — ⚠ active spec is now Demonology; re-audit)

> As of 2026-06-20 the active spec is **Demonology**, not Affliction. The
> audit below describes the *Affliction* loadout and no longer reflects what
> they're playing — re-sim against the Demonology reference before advising.

Active Affliction loadout simmed **−12.7% ST / −3.9% @4T** vs the simc
MID1 reference string on identical gear — 5 spec points in ≤3/50-usage
nodes (Withering Bolt ×2, Xavius' Gambit ×2, Improved Shadow Bolt) at
the cost of Improved Haunt / Patient Zero / Sow the Seeds / Drain Soul /
Cunning Cruelty, plus fringe defensive class picks over Demonic Circle /
Empowered Healthstone / Improved Mortal Coil. Details:
`../classes/warlock/affliction/builds.md` + `sims.md`.

## TODO

- [x] Re-snapshot 2026-06-20 (identity/gear/renown/professions via API)
- [ ] **Re-audit talents — they respecced to Demonology.** Re-sim the active
      Demonology loadout (with enchants on) vs the simc reference.
- [ ] Re-verify Currencies + Season journeys live (still 2026-06-03 screenshots)
- [ ] Add WCL character parses subcommand to `wowkb.wcl` for this character
- [x] Verified 2026-06-03: crafted gear CANNOT be catalyzed in 12.0
- [x] Crest names confirmed: **Dawncrests** (Adventurer/Veteran/Champion/
      Hero/Myth tiers)
- [x] Midnight Tailoring now 97/100 (2026-06-20) — self-crafting unlocked
