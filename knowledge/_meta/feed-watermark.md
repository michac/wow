---
title: Feed Watermark — line in the sand for incremental KB review
patch: 12.0.7
fetched: 2026-07-07
sources:
  - https://us.forums.blizzard.com/en/wow/groups/blizzard-tracker/posts.json?category_id=171
  - https://worldofwarcraft.blizzard.com/en-us/news
  - https://wago.tools/api/builds?product=wow
confidence: high
---

# Feed Watermark

**The cursor for incremental KB updates.** A patch-day sweep no longer means
re-reading the whole tree — it means "pull every blue post / news item / build
since the watermark below, triage, apply, and advance the line." Update this
file at the **end** of every feed review.

## Current watermark — reviewed through 2026-07-07

| Cursor | Value |
|---|---|
| Reviewed through (date) | **2026-07-07** |
| Latest retail build seen | **12.0.7.68453** (2026-07-06) |
| Newest blue-tracker post | id **29711270** @ `2026-07-02T17:00:17Z` ("WoW Weekly…") |
| Newest news article seen | `24287398` (WoW Weekly, ~2026-07-02) |
| Live patch at review time | 12.0.7 "Revelations" |

> **"Since last update" = anything after these cursors.** The blue-tracker post
> id and build number are both monotonic, so they're the reliable diff keys;
> the date is the human-readable fallback.

## The feeds (poll these, in trust order)

1. **Build trigger (Tier 1):** `https://wago.tools/api/builds?product=wow` — a
   new build number is the authoritative "the game changed" signal. Compare the
   top `version` against *Latest retail build seen*.
2. **Blue-post tracker (Tier 1 text):**
   `https://us.forums.blizzard.com/en/wow/groups/blizzard-tracker/posts.json?category_id=171`
   — JSON, 20 posts/page newest-first, fields `id` / `created_at` /
   `topic_title` / `excerpt`. Paginate with
   `&before=<URL-encoded ISO created_at of the oldest post on the page>` (NOT
   `offset` — ignored; NOT `before=<post_id>` — 500s). Full verbatim body per
   post at `…/en/wow/posts/<id>.json` (`cooked`). This carries hotfixes, class
   tuning, and reward-change posts — the KB-relevant core.
3. **News feed (Tier 1, broader):** `https://worldofwarcraft.blizzard.com/en-us/news`
   — HTML, monotonic article IDs; catches non-forum items (Trading Post, event
   go-lives). Corroboration + event coverage.
4. Blizzard's own RSS is **dead** (redirects to a 404). Wowhead's
   `https://www.wowhead.com/news/rss/all` works as a firehose fallback but is
   Tier-4 and unfiltered.

## Review log

| Reviewed on | Window | Posts triaged | Applied | Notes |
|---|---|---|---|---|
| 2026-07-07 | 2026-06-19 → 2026-07-07 | 15 blue-tracker | **Archived:** Jun 18/22/23/25/30 hotfix batches + 2 tuning announcements + Showdown reward post → `patch-notes/12.0.7.md`. **Applied (verified):** world-boss loot supersede + rare/crest/Dark-Particle bullet → `world-events.md`; matching rows → `moving-values.md`; Omnium Folio account-wide weekly + Ritual Sites T6 quest pickup → `systems/`. **Rejected:** blue-post "Maren Silversong" name "fix" — game data (wowhead npc=255473) confirms **Silverwing**; the hotfix post has a typo. **Archive-only:** all June 30 class tuning (KB class files are stubs / PvP-scoped, no claim contradicted). | First run. Baseline = last KB sweep 2026-06-19. Surfaced two gaps: **12.1 "Curse of Ula'tek" has a live PTR** (build 68412) — `next-patch.md` stale; and `classes/warlock/demonology/{rotation,builds}.md` are still `patch: 12.0.5` (missed by the 12.0.7 sweep). |

## Full-tree verify sweeps

Whole-KB re-verification runs (`/update` Full path → `kb-patch-sweep`). Per-file
coverage lives in each file's `reviewed:` stamp; `grep -rL 'reviewed: <date>'` is
the audit.

| Swept on | Target | Scope | Result |
|---|---|---|---|
| 2026-07-07 | 12.0.7 | whole tree, 131 files (excl. `_meta`) | 128 passed · 7 drift auto-fixed (half-Spark→whole-Spark in `liadrin-spark`, removed Conquest cap, world-boss loot supersede, faction event/rank names, Sporefall mount cadence, Omnium quest-giver, trinkets relabel) · 3 hand-fixed (Affliction Seed-detonation PvE over-read → scoped PvP-unconfirmed; `weekly-checklist` + `ritual-sites` Field-Accolades gear vendor 100/750 slot-targeted). 0 tier-downgrades (guard held). All 16 files stranded on 12.0.5 brought current. Manifest: `scratchpad/sweep-items-2026-07-07.json`. |
