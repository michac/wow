---
title: Activity Catalog — outline (browse by goal / venue / cadence)
patch: 12.0.7
fetched: 2026-07-06
reviewed: 2026-07-07
sources:
  - knowledge/planning/activities/_facets.md
confidence: high
---

# Activity catalog — the outline

> **The reviewable index.** One line per activity; details live in the per-activity
> file. This is a **projection over tags** (`_facets.md`) — the same 25 activities
> shown three ways. Intended to be **generated** from the front matter eventually;
> hand-maintained for now (seed 2026-07-06; YouTube research pass 2026-07-06).
>
> Read the contract first: [`_facets.md`](_facets.md). Include-by-default —
> `status: invalidated` hides a file; low `confidence` does **not**.

## Seed status

**25 activities.** 13 seed (migrated from `candidates.json`) + **12 net-new** from the
2026-07-06 YouTube research pass (tier-3 transcripts, include-by-default). M+, delves, raid,
and rated PvP each *fill* the single Great Vault via a `breakpoint`, so there's **one**
vault-claim entry, not four. The named gaps are now filled: **`story`** (campaign, Omnium
Folio), **`pvp`/`venue:pvp`** (Conquest, Honor), **`raid`/`venue:raid`** (Sporefall), and
**`professions`** thickened (weekly knowledge, crafting orders, + Darkmoon). Darkmoon Faire,
the Val/Naigtal **zone farm** (Field Accolades → Hero-track slot gear), and its Showdown
weekly now exist.

**Remaining thin spots / research targets:** `goal:leveling` still only rides
`turbulent-timeways`; several gates are `manual`/best-effort (see per-file **Gate TODO**s) —
resolving detectable signals is the separate ranker-wiring phase, not this md pass.

## By goal (default view — "what am I working on")

**gearing** (20)
- `great-vault` — claim the one weekly Great Vault reward
- `mplus` — Mythic+ dungeons: loot, crests, IO; fills the Vault's M+ column
- `sporefall-raid` — weekly Rotmire kill(s); fills the Vault's raid column *(new)*
- `delve-bountiful` — Bountiful delves: weekly cache + fills the Vault's world column
- `prey-weekly` — 3 Nightmare Prey hunts
- `liadrin-spark` — world-event weekly, Spark (also professions)
- `world-boss` — weekly world boss (also collectibles)
- `voidcores` — 2 Nebulous Voidcores, bonus-roll gear
- `ritual-sites` — Hero/Myth crests + accolades (repeatable)
- `void-assault` — Void Assault weekly (also collectibles)
- `renown-dungeon-weekly` — 1500 choice-rep → gear unlock
- `val-naigtal` — Val/Naigtal zone farm: Field Accolades → Hero-track slot gear (also collectibles) *(new)*
- `showdown-weekly` — Val/Naigtal Showdown weekly; hero-track WT boss (also collectibles) *(new)*
- `faction-weeklies` — faction events → champion ilvl-246 gear (also collectibles) *(new)*
- `omnium-folio` — weekly power-track rune (also story) *(new)*
- `midnight-campaign` — campaign gear + unlocks (also story) *(new)*
- `crafting-orders` — orders → crafted gear (also professions) *(new)*
- `pvp-conquest` — weekly Conquest → gear/tier; fills the Vault's PvP column (also rating) *(new)*
- `pvp-honor` — honor set + weekly PvP quests *(new)*
- `turbulent-timeways` — Timewalking gear/mounts (also leveling, collectibles)

**leveling** (1) — `turbulent-timeways`
**professions** (4) — `liadrin-spark` · `profession-weekly`* · `crafting-orders`* · `darkmoon-faire`*
**collectibles** (10) — `world-boss` · `void-assault` · `housing-weekly` · `trading-post` · `turbulent-timeways` · `faction-weeklies`* · `showdown-weekly`* · `val-naigtal`* · `darkmoon-faire`* · `abyss-anglers`*
**rating** (2) — `mplus` · `pvp-conquest`*
**story** (2) — `midnight-campaign`* · `omnium-folio`*    _(gap filled)_

_\* = net-new this research pass_

## By venue (the gather axis)

- **meta** — `great-vault` · `voidcores` · `trading-post`
- **dungeon** — `mplus` · `renown-dungeon-weekly` · `turbulent-timeways`
- **delve** — `delve-bountiful`
- **world** — `prey-weekly` · `liadrin-spark` · `world-boss` · `ritual-sites` · `void-assault` · `faction-weeklies`* · `showdown-weekly`* · `val-naigtal`* · `darkmoon-faire`* · `abyss-anglers`*
- **housing** — `housing-weekly`
- **raid** — `sporefall-raid`*    _(gap filled)_
- **pvp** — `pvp-conquest`* · `pvp-honor`*    _(gap filled)_
- **quest** — `midnight-campaign`* · `omnium-folio`*    _(new venue this pass)_
- **profession** — `profession-weekly`* · `crafting-orders`*    _(new venue this pass)_

## By cadence / time (the urgency lens)

- **event · time-boxed** (U↑) — `turbulent-timeways`
- **monthly · time-boxed** (U↑ recurring) — `darkmoon-faire`*
- **weekly · standing** (expires this reset) — `great-vault` · `mplus` · `sporefall-raid`* · `delve-bountiful` · `prey-weekly` · `liadrin-spark` · `world-boss` · `voidcores` · `void-assault` · `renown-dungeon-weekly` · `housing-weekly` · `omnium-folio`* · `profession-weekly`* · `faction-weeklies`* · `showdown-weekly`* · `pvp-conquest`*
- **monthly · standing** — `trading-post`
- **repeatable · standing** (no expiry) — `ritual-sites` · `pvp-honor`* · `crafting-orders`* · `val-naigtal`* · `abyss-anglers`*
- **one-time · standing** — `midnight-campaign`*
