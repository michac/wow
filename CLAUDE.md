# WoW Q&A Agent Workspace

This repo is a knowledge base + ingestion toolkit for answering World of
Warcraft questions **reliably**. Scope: **Retail, Midnight expansion only**
(no Classic, no leveling-era content unless asked historically).

## Current game state

- **Live: patch 12.0.5** — Midnight expansion, level cap **90**, Season 1.
- **PTR: 12.0.7.**
- `knowledge/_meta/game-version.md` is the **single source of truth** for
  game state and must be updated on patch days. If anything in this file
  disagrees with it, that file wins.

## Staleness doctrine (read this before answering anything)

WoW is 22 years old. **Most of the internet describes a dead version of the
game.** Defenses, in order:

1. Answer from `knowledge/` first — it carries provenance.
2. Every KB file has YAML front matter: `patch`, `fetched`, `sources`,
   `confidence`. Treat `patch` older than live as needing re-verification.
3. When web-searching, require **"Midnight" / "12.0" / 2026** signals in
   results. Undated or pre-2026 content is suspect by default; pre-Midnight
   mechanics (The War Within 11.x and earlier) are historical.
4. Trust tiers live in `knowledge/_meta/sources.md`:
   1 = Blizzard API / wago.tools / patch notes / simc APLs,
   2 = Warcraft Logs / Archon, 3 = Icy Veins / Method / class Discords /
   trusted YouTubers, 4 = Wowhead editorial / Reddit / SEO sites (corroborate).
5. **Answers must cite the patch version and at least one source.** If
   confidence is low or data is stale, say so explicitly.
6. Volatile data (AH prices, token price, realm status, "what event is up
   this week") is **never** answered from the KB — fetch live.

## Directory map

- `knowledge/_meta/` — game version (source of truth), source trust registry
- `knowledge/endgame/` — `weekly-checklist.md` (the anchor doc), `raids/`,
  `mythic-plus/`, `delves/`, `prey.md`, `great-vault.md`, `world-events.md`
- `knowledge/factions/` — one file per renown faction (5)
- `knowledge/classes/<class>/<spec>/` — rotation.md, builds.md, sims.md
- `knowledge/systems/` — housing, ritual sites, void incursions, professions
- `knowledge/economy/` — pointers to live tools only; never cached prices
- `tools/` — uv project, `wowkb` package
- `raw/` — gitignored fetch cache; distill into `knowledge/`, don't cite raw/

### Front-matter convention (every knowledge/**.md)

```yaml
---
title: Midnight Season 1 Mythic+ Overview
patch: 12.0.5            # game version the content describes
fetched: 2026-06-03      # when sourced
sources:
  - https://...
confidence: high          # high | medium | low
---
```

## Tools (run from `tools/`, needs `.env` at repo root — see `.env.example`)

```bash
uv run python -m wowkb.youtube transcript <url>      # → raw/youtube/<id>.md
uv run python -m wowkb.youtube channel <url> --limit 10
uv run python -m wowkb.blizzard token-price          # also: item/spell/journal-*/realms/get
uv run python -m wowkb.wcl rankings <encounter-id> --class Warlock --spec Affliction
uv run python -m wowkb.wcl casts <report-code> --fight <id>
uv run python -m wowkb.wago <Db2Table> [--build 12.0.5.xxxxx]   # → raw/wago/
uv run python -m wowkb.fetch <url>                   # → raw/pages/
```

Blizzard + WCL commands require credentials in `.env` (user-registered).

## Workflow: the KB grows through use

1. **Answer from `knowledge/`** when fresh (`patch` == live, decent confidence).
2. **If missing or stale**: fetch with the tools (tier-highest source first),
   distill, and **write back** to the right `knowledge/` file with full front
   matter and resolved TODOs.
3. Stubs with `## TODO` sections name their intended sources — follow them.
4. Keep `raw/` as scratch; the curated claim + citation goes in `knowledge/`.
