---
title: Economy — Live Data Only
patch: 12.0.5
fetched: 2026-06-03
sources: []
confidence: high
---

# Economy: never cache, always fetch

Prices are volatile by the hour. **Nothing in this directory should ever
contain a cached price.** Answer economy questions by calling live tools:

| Question | Tool |
|----------|------|
| WoW Token price | `uv run python -m wowkb.blizzard token-price` |
| Item identity/vendor price | `uv run python -m wowkb.blizzard item <id>` |
| AH commodity prices | Blizzard AH API (TODO: add `wowkb.blizzard auctions`) |
| Market trends | point user at TSM / undermine.exchange — don't quote numbers |

What *can* live here: structural knowledge (how the AH works, region-wide
commodities, posting cutoffs) — with normal front matter.
