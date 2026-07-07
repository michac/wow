---
title: Patch-Notes Archive — verbatim official notes
patch: 12.0.7
fetched: 2026-07-07
sources: []
confidence: high
---

# Patch-Notes Archive

**Verbatim, committed copies of Blizzard's official content-update notes and
hotfix logs, one file per patch.** This is a pure archive — *never edited after
capture*. It exists because Blizzard rotates and retires `news`/`worldofwarcraft`
article URLs, so the `sources:` links elsewhere in the KB rot over time. When
that happens, this is where the original text still lives.

## Relationship to the other `_meta` files

- **`patch-notes/<patch>.md`** (here) — the raw source, captured verbatim. What
  Blizzard actually said, preserved against link rot. Provenance only.
- **`changelog-<patch>.md`** — the *distilled diff* between the previous live
  patch and this one, plus the KB file impact map. Curated; drops detail.
- **`moving-values.md`** — the flattened, latest-value-wins registry of volatile
  facts (reward tiers, ilvls, tuning) used to catch stale web sources.
- **`game-version.md`** — the single source of truth for current game state.

The pipeline: **archive (verbatim) → changelog (distilled diff) → KB topic files
(current state) + moving-values (stale-catcher).**

## File convention

- **Filename:** `<patch>.md` (e.g. `12.0.8.md`), lowercase, dotted version.
- **Front matter:** standard block. `sources:` lists every URL captured;
  `fetched:` is the capture date; `confidence: high` (it's a verbatim copy).
- **Body:** the content-update notes first, then the hotfix log, each under a
  clear `##` heading with its source URL and the date fetched. Paste the text
  as-is; do not summarize, reorder, or "clean up." If a page is long, keep it
  long — that's the point.
- **Multiple captures:** hotfix logs grow over time. Append later hotfix
  snapshots under dated sub-headings rather than overwriting the first capture.

## Coverage

| Patch | Codename | Live | Content notes | Hotfix log |
|---|---|---|---|---|
| 12.0.5 | Lingering Shadows | 2026-04-21 | ✅ captured | ✅ 17 batches (Apr 23 – Jun 9) |
| 12.0.7 | Revelations | 2026-06-16 | ✅ captured | ✅ 5 batches (Jun 18 – Jun 30) + tuning/reward |

The archive was introduced on 2026-07-07, after both patches shipped, so their
content-update notes were backfilled verbatim from the official pages, and the
dated hotfix batches were pulled from the Blizzard blue-post tracker's rolling
hotfix thread (`.../t/2296045`, staff posts filtered by date). Going forward,
`/update` appends new hotfixes here automatically. There is no 12.0.6 (Blizzard
skipped it: retail went 12.0.5 → 12.0.7).
