---
title: Uncomplete – Kil'jaeden (US) — fresh-90 demon hunter gearing snapshot
patch: 12.0.7
fetched: 2026-07-09
reviewed: 2026-07-09
sources:
  - https://us.api.blizzard.com/profile/wow/character/kiljaeden/uncomplete?namespace=profile-us
confidence: high
---

# Uncomplete – Kil'jaeden (US)

> **Snapshot** — character data is volatile (updates on logout). The body
> below reflects the **2026-07-09** live fetch. **Always re-fetch the live
> profile before answering any gear/level/progress question** — this alt is
> actively gearing and numbers move fast. Pull with
> `uv run python -m wowkb.character Uncomplete --realm kiljaeden`.

**Alt on the user's account (LLOYDCHRISTMAS), alongside Encomplete (main,
Demonology warlock) and Hallick (Feral druid).** **Just hit the level cap
(90)** and is entering the Season 1 gearing runway. Got a **running start**
from Champion/Hero pieces the user pulled from the warband bank — most of the
body is already Champion-to-Hero; the naked slots are leveling greens.
Achievement points ~7,930 (account-wide).

## Identity

- Night Elf **Demon Hunter**, active spec **Vengeance** (tank), hero tree
  **Annihilator**. Second saved loadout: **Devourer**. (Vengeance tank is
  ideal for the solo gearing loop — delves, ritual sites, Val/Naigtal.)
- **Level 90 (cap)** — freshly dinged 2026-07-09.
- Alliance, Kil'jaeden · guild — · title —

## State — fresh 90, mid-gearing

- **Equipped ilvl ~215** (grab-bag): weapons + several slots are Champion/
  Hero from the warband bank, but **7 slots are still leveling greens**
  (head/neck/chest/waist/legs/hands/back). See the per-slot gearing chart in
  the plan below — the immediate job is stopping the leveling-green bleed.
- **No endgame loop started**: no rated M+ this season, no raid lockouts.
  20 Hero Dawncrests and 4 Restored Coffer Keys already banked — enough to
  start upgrading/delving on day one.
- **Gearing doctrine (this alt): don't target below Champion.** Encomplete
  can farm Field Accolades and buy **warbound** slot-specific caches
  (Champion 100 / Hero 750) to mail over; crests do **not** transfer, so
  Uncomplete earns his own upgrade crests.

## Gear (equipped, live 2026-07-09)

| Slot | ilvl | id | Item | Assessment |
|---|---|---|---|---|
| Head | 165 | 249640 | Osseoclad Saberteeth | leveling green · **tier slot** |
| Neck | 159 | 248049 | Eversong Chain | leveling green |
| Shoulders | 253 | 275225 | Toxic Voidscythe Spaulders | Champion+ · **tier slot** |
| Chest | 159 | 263343 | Snapdragon Tunic | leveling green · **tier slot** |
| Waist | 159 | 248041 | Belt of Herbicide | leveling green |
| Legs | 220 | 264543 | Snapdragon Pantaloons | Adventurer · **tier slot** |
| Feet | 246 | 249638 | Osseoclad Bonecrushers | Champion |
| Wrist | 256 | 274843 | Pincher-Proof Wristguards | Hero-ish |
| Hands | 145 | 249639 | Osseoclad Spinegrapplers | **weakest** · **tier slot** |
| Ring 1 | 246 | 251217 | Occlusion of Void | Champion (ring ≠ tier) |
| Ring 2 | 246 | 249621 | Voodoo Band | Champion |
| Trinket 1 | 253 | 250462 | Forgotten Farstrider's Insignia | Champion+ |
| Trinket 2 | 246 | 252418 | Solar Core Igniter | Champion |
| Back | 198 | 257022 | Deepvine Shroud | leveling |
| Main Hand | 266 | 275216 | Phaseblade's Edges | Hero |
| Off Hand | 269 | 275217 | Nexus-Captain's Phaseblade | Hero |

No enchants or gems detected — add once slots stabilize on Champion+.

## Delve companions

- Brann Bronzebeard lvl 45 · Valeera Sanguinar lvl 46 (account-wide).

## Professions

- **Fishing** (secondary) only — Classic 1/300, Midnight 1/300. No primary
  professions. (Open question: should this alt take a gathering/crafting pair
  to fill a warband gap? — the other two cover Tailoring/Enchanting on
  Encomplete.)

## Currencies (Syndicator SavedVariables, 2026-07-09)

- Gold: **13,358g** (LLOYDCHRISTMAS account)
- **Season 1**: Hero Dawncrest **20** · Restored Coffer Key **4** · Coffer
  Key Shards 8 · Undercoin 1,875 · Radiant Spark Dust 6 · Dawnlight Manaflux 8
- **Midnight**: Voidlight Marl 1,514 · Remnant of Anguish 461 · Brimming
  Arcana 90
- Timewarped Badge 1,490 · Trader's Tender 4,200 · Community Coupons 19
- **No Field Accolades on this character** — the accolade bank for cache
  purchases lives on **Encomplete** (~1,309 at last check). Caches are
  warbound; buy on Encomplete, mail to Uncomplete.
- ⚠ Sparks of Radiance (an item) and Catalyst charges are NOT in Syndicator's
  currency table — check those in-game. @verify-ingame

## Gearing plan — see the per-slot chart

The active plan (per-slot cache/crest targets + the accolade-allocation
heuristic) lives in **`uncomplete-plan.md`** (mirrors `encomplete-plan.md`).
Headline: Champion-cap the 7 leveling slots first, convert non-tier slots to
Hero as accolades allow, let the free Decimus "Knocking Off the Top" quest fill
one of cloak/belt/bracers, then move to T6 ritual sites for the 285 tail.

## TODO

- [x] **Level to 90** — done 2026-07-09.
- [ ] Vengeance max-level build/rotation docs (`../classes/demon-hunter/
      vengeance/` — none exist yet); reconcile Annihilator vs Devourer.
- [ ] Confirm in-game: Sparks of Radiance count + Catalyst charges (not in
      Syndicator). @verify-ingame
- [ ] Decide professions (gathering/crafting gap the other two don't cover).
- [ ] Re-sync after gearing sessions (enrolled in `/sync-characters`).
