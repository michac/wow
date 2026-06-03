---
title: Current Game Version — Single Source of Truth
patch: 12.0.5
fetched: 2026-06-03
sources:
  - https://worldofwarcraft.blizzard.com/en-us/news (patch notes)
confidence: high
---

# Current Game Version

> **This file is the single source of truth for game state.** Every answer the
> agent gives must be consistent with this file. Update it on patch days.

| Field | Value |
|-------|-------|
| Expansion | **Midnight** (WoW's 11th expansion, 10th in numbering: 12.x) |
| Live patch | **12.0.5** |
| PTR patch | **12.0.7** — releases **2026-06-16** (confirmed); see `next-patch.md` |
| Level cap | **90** |
| Current season | **Midnight Season 1** |
| Season 1 start | Week of 2026-03-17 (raid/season open); M+ unlocked 2026-03-24 |
| Weekly reset | Tuesday (US region) |

## 12.0.5 patch highlights

- Ritual Sites (open-world activity, Field Accolades currency)
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
