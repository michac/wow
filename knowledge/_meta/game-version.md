---
title: Current Game Version — Single Source of Truth
patch: 12.0.7
build: 12.0.7.68453
fetched: 2026-07-07
reviewed: 2026-07-07
sources:
  - https://worldofwarcraft.blizzard.com/en-us/news (patch notes)
  - https://wago.tools/api/builds (live client build)
  - https://us.api.blizzard.com (Game Data API static namespace = 12.0.7)
confidence: high
---

# Current Game Version

> **This file is the single source of truth for game state.** Every answer the
> agent gives must be consistent with this file. Update it on patch days.

| Field | Value |
|-------|-------|
| Expansion | **Midnight** (WoW's 11th expansion, 10th in numbering: 12.x) |
| Live patch | **12.0.7** (live client build `12.0.7.68453`, 2026-07-06; Game Data API static namespace = 12.0.7) |
| PTR patch | **12.1 "Curse of Ula'tek"** on PTR (build `12.1.0.68412`) — opens Midnight Season 2; see `next-patch.md` |
| Level cap | **90** |
| Current season | **Midnight Season 1** |
| Season 1 start | Week of 2026-03-17 (raid/season open); M+ unlocked 2026-03-24 |
| Weekly reset | Tuesday (US region) |

> **12.0.7 "Revelations" went live 2026-06-16.** The `knowledge/**` tree was
> swept from 12.0.5 → 12.0.7 on 2026-06-19 against the change ledger at
> `knowledge/_meta/changelog-12.0.7.md` (distilled from the official Revelations
> content-update notes + hotfix log through 2026-06-19). All KB files now carry
> `patch: 12.0.7`. The ledger is the canonical 12.0.5→12.0.7 diff; consult it
> before re-editing patch-era claims.

## 12.0.7 "Revelations" highlights (live 2026-06-16)

- **New zones: Val and Naigtal** — two worlds via portal from Voidstorm,
  rotating weekly (hostile factions: Domanaar on Val, Hal'hadar on Naigtal).
- **Omnium Folio** — new runic-power progression system (`systems/omnium-folio.md`).
- **Sporefall raid** — single-boss raid vs Rotmire, RF→Mythic, ilvl 259–298
  (`endgame/raids/sporefall.md`).
- **Ritual Sites Tier 6** — 3-site rotation now (Daggerspine Point / Broken
  Throne / Blinding Bloom); repeatable solo Myth Dawncrests.
- **Void Assaults** — XP doubled, higher drop rates, new cosmetic vendors.
- **Durability** — gear no longer takes durability damage from combat.
- **Turbulent Timeways** (Jun 30–Aug 11, Dragonflight dungeons); Amani troll
  story (Zul'jan, Jan'alai); Prey custom-hunt cap removed; PvP gear ilvl +9.

## 12.0.5 patch highlights (historical — superseded by 12.0.7)

- Ritual Sites (instanced scenario, Field Accolades currency; 2-site rotation,
  5 tiers — now 3 sites / 6 tiers in 12.0.7)
- Void Incursions / Void Strikes (rotating weekly: Eversong Woods / Zul'Aman)
- Abyss Anglers (fishing activity, Depthdiver Jeju off Zul'Aman coast)
- Decor Duels (hide-and-seek PvP in Silvermoon City)
- Voidforge questline (Decimus, The Voidstorm 51.2 68.4) → weekly bonus-roll
  tokens (Nebulous Voidcores) + Ascendant Voidcore looting

## Update checklist (patch day)

1. Bump `patch:` / PTR fields above.
2. Re-verify `knowledge/endgame/weekly-checklist.md` against Icy Veins.
3. Sweep `knowledge/**` front matter: anything with `patch:` older than the
   live version needs re-verification or a `confidence: low` downgrade.
