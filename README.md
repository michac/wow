# WoW Q&A Agent Workspace

A local, versioned knowledge base + ingestion tooling for answering World of
Warcraft questions reliably. Scope: **Retail, Midnight expansion** (currently
patch 12.0.5, Season 1).

WoW is 22 years old, so the internet is full of stale advice. The core design
idea here is **provenance and staleness defense**: every knowledge file
declares the patch it describes, when it was sourced, and from where. Volatile
data (auction house, token price, realm status) is never cached — it's fetched
live via the API clients.

## Layout

| Path | Purpose |
|------|---------|
| `CLAUDE.md` | Agent instructions: game state, trust tiers, workflow |
| `knowledge/` | Curated, versioned KB — markdown with YAML front matter |
| `knowledge/_meta/game-version.md` | Single source of truth for live/PTR versions |
| `knowledge/_meta/sources.md` | Source trust registry |
| `tools/` | Python (uv) ingestion utilities (`wowkb` package) |
| `raw/` | Gitignored fetch cache (transcripts, JSON, CSV) |

## Tools

From `tools/` (requires [uv](https://docs.astral.sh/uv/)):

```bash
cp ../.env.example ../.env   # then fill in API credentials
uv sync

uv run python -m wowkb.youtube transcript <video-url-or-id>
uv run python -m wowkb.youtube channel <channel-url> [--limit 10]
uv run python -m wowkb.blizzard token-price
uv run python -m wowkb.blizzard item 19019
uv run python -m wowkb.wcl rankings <encounter-id> --class Warlock --spec Affliction
uv run python -m wowkb.wago JournalEncounter
uv run python -m wowkb.fetch <url>
```

Outputs land in `raw/` for review before being distilled into `knowledge/`.
