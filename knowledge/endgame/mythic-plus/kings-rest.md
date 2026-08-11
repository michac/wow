---
title: Kings' Rest — Midnight S2 M+ dungeon guide (STUB, day-1)
patch: 12.1
build: 12.1.0.69214
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24294369   # "Midnight Season 2" overview — S2 dungeon pool + returning dungeons (tier 1)
  - https://worldofwarcraft.com/en-us/news/24293281   # 12.1 "Curse of Ula'tek" Content Update Notes (tier 1)
  - https://us.forums.blizzard.com/en/wow/posts/29833350  # S1 ending / S2 pre-season schedule (tier 1)
  - https://us.api.blizzard.com/data/wow/journal-instance/1041  # Blizzard Dungeon Journal, live 12.1 namespace (tier 1 game data)
  - https://us.api.blizzard.com/data/wow/journal-encounter/2165  # The Golden Serpent (tier 1)
  - https://us.api.blizzard.com/data/wow/journal-encounter/2171  # Mchimba the Embalmer (tier 1)
  - https://us.api.blizzard.com/data/wow/journal-encounter/2170  # The Council of Tribes (tier 1)
  - https://us.api.blizzard.com/data/wow/journal-encounter/2172  # Dazar, The First King (tier 1)
  - https://www.wowhead.com/guide/midnight/kings-rest-dungeon-overview-mythic-plus  # (tier 4, listed as updated 2026-08-11 — body not retrievable on patch day)
confidence: low
---

# Kings' Rest — Midnight Season 2 Mythic+

> 🟡 **STUB, written on patch day (2026-08-11).** This file carries only what is
> confirmed by **Tier-1** sources: Blizzard's Season 2 announcement and the
> **live 12.1 Dungeon Journal** read straight off the game-data API. It has
> **no route, no pull order, no trash table, no affix interactions and no loot
> table** — those come from Tier-3 guides (Method / Icy Veins) and from actually
> running it, and on day 1 no updated Tier-3 guide exists. Do not treat the
> absence of a mechanic here as evidence it isn't in the dungeon, and do not
> fill this in from a **pre-12.1** guide: Blizzard says the dungeon shipped with
> **design and quality-of-life updates**, so a Battle-for-Azeroth-era or War
> Within-era Kings' Rest guide is actively misleading about this version.
> See `## TODO` at the bottom.

## What it is

**Kings' Rest** is a **Battle for Azeroth** dungeon — the royal mausoleum of the
Zandalari, located in **Zuldazar** — returning as one of the eight dungeons in
the **Midnight Season 2** Mythic+ pool. **Four bosses.**

| Fact | Value | Source |
|---|---|---|
| Expansion of origin | Battle for Azeroth | journal-instance/1041 |
| Zone | Zuldazar | journal-instance/1041 |
| Bosses | 4 | journal-instance/1041 |
| S2 M+ pool | yes — one of 8 | Season 2 blog (tier 1) |
| Returning-dungeon changes | "design and quality of life updates" — **not enumerated by Blizzard** | 12.1 Content Update Notes (tier 1) |
| Follower Dungeon version | **no** (follower pool is DF / TWW / Midnight only) | `season-2-overview.md` |

**Season timing (both halves matter):** the S2 pool is live **now** (week of
2026-08-11) on **Heroic and Mythic 0 only**, with **Mythic 0 on a weekly lockout
for this week only**, dropping **Champion 1/6 (292)**. **Mythic+ difficulties and
keystones do not exist until 2026-08-18.** So there is no such thing as a
Kings' Rest key this week. `season-2-overview.md` is the file of record for the
pool, crests (Mistcrests), rating and rewards; nothing season-scoped is repeated
here.

## Bosses (Dungeon Journal, live 12.1 build)

Names and abilities below are read from the **Blizzard journal API at the live
12.1 namespace** — i.e. this is the Adventure Guide *as it stands after the
12.1 updates*, not a BfA memory. It is Tier-1 for **what exists**; it is **not**
a strategy guide and carries no "see → do", no consequence tier and no route.

Encounter order as listed by the journal:

1. **The Golden Serpent** <!-- enc:2165 -->
2. **Mchimba the Embalmer** <!-- enc:2171 -->
3. **The Council of Tribes** <!-- enc:2170 -->
4. **Dazar, The First King** <!-- enc:2172 -->

### The Golden Serpent <!-- enc:2165 -->

A Zandalari construct guarding the tomb. Journal abilities: **Spit Gold**
(Fire DoT on a player, leaves a **Molten Gold** pool where they stand) ·
**Lucre's Call** (animates every Molten Gold pool into **Animated Gold** that
walks toward the boss; each one that reaches it is absorbed for a stack of
**Luster**, which shields the boss and increases its damage — killing an Animated
Gold reverts it to a pool) · **Serpentine Gust** (damage to all players) ·
**Tail Thrash** (Physical damage to the tank's current target).

### Mchimba the Embalmer <!-- enc:2171 -->

Journal abilities: **Drain Fluids** (Nature DoT that completes into
**Desiccation** — reduced damage done and movement speed until the player is
healed above **90%** health) · **Entomb** (seals a player inside one of the
chamber's crypts; trapped players can **Struggle** to signal where they are) ·
**Open Coffin** (opens crypts one at a time; every crypt that does **not** hold a
player releases a **Finished Mummy**) · **Burn Corruption** (Fire damage +
**Burning Ground** patch) · **Command Constructs** (**Interment Construct** /
**Embalm**) · **Awakening Slam** (**Half-Finished Mummy** / **Wretched
Discharge**) · **Explosive Acids**.

### The Council of Tribes <!-- enc:2170 -->

Three councilors fought in sequence; a defeated councilor returns to their urn
and periodically rejoins to use a **single** ability before returning.

⚠ **This is where a 12.1 design change is visible in Tier-1 data.** The live
journal now states outright: *"The battle will begin with **Kula the
Butcher**."* Tier-4 coverage claims the whole order is now fixed as **Kula the
Butcher → Aka'ali the Conqueror → Zanazal the Wise**, removing the old weekly
variance — the journal confirms only the **opening**, so the rest of that
ordering is **unverified**. Confirm it in game.

| Councilor | Journal abilities |
|---|---|
| **Kula the Butcher** | Whirling Axes · Severing Axe (Physical DoT on random players) |
| **Aka'ali the Conqueror** | Barrel Through (charge at a player; heavy Physical damage **split among all players hit**) · Debilitating Backhand (tank hit + knockback + **Shattered Defenses**, increasing Physical damage taken) |
| **Zanazal the Wise** | Arc Lightning · Poison Nova (Nature DoT on all players) · Call of the Elements — summons **Explosive Totem** (Explode), **Torrent Totem** (Torrent) and **Thundering Totem** (Disruption) |

⚠ Note the proper-noun spelling: the game data says **Aka'ali** the Conqueror
(one `a` in the second syllable). Several third-party write-ups render it
"Aka'alil". Game data wins.

### Dazar, The First King <!-- enc:2172 -->

Journal: Dazar fights on foot and **at 80% health mounts T'zala**, his raptor.
**Reban** also appears in the encounter.

| Actor | Journal abilities |
|---|---|
| **King Dazar** | Eternal Bond · Gilded Destruction (Fire damage to all players; leaves **Searing Gold**) · Blade Combo (heavy hit on its target) · Aerial Smash (Physical damage to all players at the destination) · Impaling Spear (springs from the **ceiling**; heavy Physical damage + bleed to players hit) |
| **T'zala** (from 80%) | Eternal Bond · Savage Maul (increases its target's Physical damage taken) · Quaking Leap (Physical damage at the destination) |
| **Reban** | Hunting Leap · Deathly Roar |

## Difficulty availability quirk

The Dungeon Journal for every Kings' Rest encounter still carries the line
**"Kings' Rest is not available in Normal Difficulty."** That is journal text
read live on 12.1 — but it predates this season's re-tuning and the Season 2
notes explicitly put the pool on **Heroic and Mythic 0** during the pre-season
week, so the practical answer is "Heroic and up". @verify-ingame whether Normal
difficulty is actually absent from the dungeon finder for Kings' Rest in 12.1.

## TODO

Fill this file to the standard of `skyreach.md` / `pit-of-saron.md` — route,
trash table (mob · ability · see→do · archetype · consequence tier · role),
per-boss ability tables with consequence tiers, and a DPS-notes section — once
sources exist. Intended sources, in order:

1. **The 12.1 dungeon-change list (Tier 1 / Tier 4 reporting).** Blizzard did
   **not** enumerate the "design and quality of life updates" in the content
   update notes. Chase: the 12.1 PTR dungeon-tuning blue posts, and Wowhead's
   PTR coverage — `wowhead.com/news/midnight-season-2-dungeon-tuning-for-patch-12-1-382238`
   (trash removals) and `wowhead.com/news/additional-nerfs-to-kings-rest-and-ruby-life-pools-on-patch-12-1-ptr-382135`
   (2026-07-09). Both were unfetchable on patch day; retry. Specific claims to
   confirm or kill: **shortened roleplay sequences**, **fixed Council of Tribes
   order**, **Shadow of Zul adjustments**, a **reworked Dazar encounter**,
   **trash removed**, and the season-wide **clearer cone/line telegraph visuals**.
2. **Method** — `method.gg/guides/dungeons/kings-rest` (Tier 3; the trash tables
   in the sibling files come from here).
3. **Icy Veins** — `icy-veins.com/wow/kings-rest-dungeon-guide` (Tier 3;
   corroborate every trash claim against Method, flag single-sourced ones
   `confidence: low`, as `skyreach.md` does).
4. **Wowhead's S2 dungeon overview** — `wowhead.com/guide/midnight/kings-rest-dungeon-overview-mythic-plus`
   (Tier 4, corroborate only; listed as updated 2026-08-11 but body not
   retrievable).
5. **A Season 2 M+ walkthrough video** via `wowkb.youtube transcript` — the S1
   files used Dalaran Gaming's 8-dungeon walkthrough for boss corroboration; the
   S2 equivalent should exist within a week or two of 2026-08-18.
6. **Loot** — do not write a loot table from a pre-12.1 source. S2 drop ilvls
   belong in `loot.md`; per-slot trinkets belong in `classes/*/trinkets.md`.

When filling in: **re-read the boss sections above against the journal again**
rather than trusting a guide's ability list, and keep `season-2-overview.md` as
the owner of anything season-scoped. Raise `confidence:` off `low` only once at
least two independent sources agree on the trash and route.
