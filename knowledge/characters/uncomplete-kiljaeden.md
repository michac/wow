---
title: Uncomplete – Kil'jaeden (US) — demon hunter leveling alt snapshot
patch: 12.0.7
fetched: 2026-07-05
reviewed: 2026-07-07
sources:
  - https://us.api.blizzard.com/profile/wow/character/kiljaeden/uncomplete?namespace=profile-us
confidence: high
---

# Uncomplete – Kil'jaeden (US)

> **Snapshot** — character data is volatile (updates on logout). The body
> below reflects the **2026-07-05** live profile fetch (last login
> 2026-07-06 06:14 UTC per the API). **Always re-fetch the live profile
> before answering any gear/level/progress question** — this is an actively
> leveling alt and numbers move fast. Pull with
> `uv run python -m wowkb.character Uncomplete --realm kiljaeden`.

**Alt on the user's account (LLOYDCHRISTMAS), alongside Encomplete (main,
Demonology warlock) and Hallick (Feral druid).** Earliest of the three by a
wide margin — mid-leveling, not yet in the Midnight endgame loop.
Achievement points 7,930 (account-wide).

## Identity

- Night Elf **Demon Hunter**, active spec **Vengeance** (tank), hero tree
  **Annihilator**. Second saved loadout present: **Devourer**.
- **Level 77** — mid-leveling, well below the Midnight cap (90).
- Alliance, Kil'jaeden · guild — · title —
- Last login at fetch: 2026-07-06 06:14 UTC

## State

- **Equipped ilvl 43** (API average 49). A grab-bag of leveling greens and
  old heirloom-era pieces spanning several expansions (Legion neck/shoulders,
  Cataclysm chest/belt/legs) — normal for a character being levelled, not a
  geared endgame set.
- **No endgame loop yet**: no rated M+ runs this season, no raid lockouts.
  The weekly-checklist / delve / crest / ritual-site playbook doesn't apply
  until 90. Priority is levelling to cap; then it joins the Season 1 gearing
  runway one full tier behind Hallick.

## Gear (equipped ilvl 43, API 2026-07-05)

| Slot | ilvl | id | Item |
|---|---|---|---|
| Head | 42 | 193751 | Crown of Roaring Storms |
| Neck | 14 | 128945 | Inquisitor's Glowering Eye |
| Shoulders | 17 | 128950 | Demon-Rend Shoulderblades |
| Chest | 69 | 59077 | Stoutfist Breastplate |
| Waist | 50 | 59009 | Vyrin's Belt |
| Legs | 65 | 59068 | Waterproof Leggings |
| Feet | 32 | 60935 | Raven Hill Sandals |
| Wrist | 61 | 59074 | Topsoil Bracers |
| Hands | 71 | 193721 | Ruby Contestant's Gloves |
| Ring 1 | 37 | 193708 | Platinum Star Band |
| Ring 2 | 31 | 60910 | Starry Band |
| Trinket 1 | 16 | 128959 | Seal of House Wrynn |
| Trinket 2 | 13 | 128958 | Lekos' Leash |
| Back | 75 | 193629 | Cloak of Lost Devotion |
| Main Hand | 43 | 193772 | Dragonscale Ripper |
| Off Hand | 57 | 58978 | Filthy Paw |

No enchants or gems — as expected for a levelling character.

## Delve companions

- Brann Bronzebeard lvl 45 · Valeera Sanguinar lvl 43 (account-wide).

## Professions

- None reported by the profile API at this fetch.

## Currencies

- Gold: **3,324g** (source: Syndicator SavedVariables, LLOYDCHRISTMAS account)
- Timewarped Badge **1,135** · Trader's Tender **4,000** ·
  Dawnlight Manaflux **8**
- ⚠ Sparks of Radiance (an item) and Catalyst charges are not in Syndicator's
  currency table — check those in-game.

## TODO

- [ ] **Level to 90** — the gating item before any endgame planning applies.
- [ ] Once at cap: Vengeance max-level build/rotation docs
      (`../classes/demon-hunter/vengeance/` — none exist yet) and reconcile
      the Annihilator vs. Devourer hero-tree choice.
- [ ] Pick up professions if this alt is meant to fill a gathering/crafting
      gap the other two don't cover.
- [ ] Add to `/sync-characters` re-sync rotation (it re-syncs every file in
      `knowledge/characters/`, so this file's presence already enrolls it).
