---
title: Source Trust Registry
patch: 12.0.5
fetched: 2026-06-03
sources: []
confidence: high
---

# Source Trust Registry

Tiers are about *how* a source derives its claims, not popularity. Cite the
tier-highest source available; corroborate tier-3/4 claims across two sources
when the answer matters.

## Tier 1 — Authoritative (ground truth)

| Source | What for |
|--------|----------|
| Blizzard Game Data / Profile APIs | Items, spells, journal encounters, token price, realm status, character data |
| wago.tools (DB2 client data) | Raw game tables — what's literally in the client build |
| Official patch notes / Blizzard news | What changed, when |
| SimulationCraft APLs (GitHub) | Canonical rotation priority lists per spec |

## Tier 2 — Empirical (derived from real gameplay data)

| Source | What for |
|--------|----------|
| Warcraft Logs (GraphQL API) | Top parses, real cast sequences, encounter timings |
| Archon.gg | Aggregated WCL builds/talents/gear (M+ and raid) |

## Tier 3 — Curated (expert-written, generally reliable)

| Source | What for |
|--------|----------|
| Icy Veins | Guides, weekly to-do list (our anchor), class guides |
| Method | Class guides, raid strategy |
| Maxroll | Class/season guides |
| Class Discords (e.g., Warlock: "Council of the Black Harvest") | Cutting-edge spec consensus |
| Trusted YouTubers (Signs of Kelani, etc.) | News, system explainers — pull transcripts via `wowkb.youtube` |

## Tier 4 — Use with care

| Source | Caveat |
|--------|--------|
| Wowhead | Database pages fine (near tier 1); editorial guides uneven |
| Reddit (r/wow, class subs) | Good for "is this bugged?", bad for authoritative numbers |
| Random SEO/boosting sites (skycoach etc.) | Often stale or padded; corroborate everything |

## Staleness heuristics

- WoW is 22 years old: **most search results describe a dead game version.**
- Require "Midnight" / "12.0" / 2026 signals before trusting web content.
- Undated content is suspect by default.
- Pre-Midnight expansion content (The War Within 11.x and earlier) is
  historical unless explicitly marked as such in the KB.
