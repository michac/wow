---
title: Feed Watermark — line in the sand for incremental KB review
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
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

## Current watermark — reviewed through 2026-08-11

| Cursor | Value |
|---|---|
| Reviewed through (date) | **2026-08-11** |
| Latest retail build seen | **12.1.0.69214** (2026-08-10 22:33) |
| Newest blue-tracker post | id **29877114** @ `2026-08-11T17:21:08Z` ("Epic Savings Await: 40% off…") |
| Newest news article seen | `24296228` (Discord account linking, ~2026-08-06) |
| Live patch at review time | **12.1 "Curse of Ula'tek"** — went live **2026-08-11** |

> **"Since last update" = anything after these cursors.** The blue-tracker post
> id and build number are both monotonic, so they're the reliable diff keys;
> the date is the human-readable fallback.

> ⚠ **A dated follow-up is owed on 2026-08-18.** 12.1 shipped into a **pre-season
> week**; Midnight Season 2 opens with that reset. Roughly forty claims across
> `endgame/`, `planning/activities/` and `game-version.md` are written as
> "opens Aug 18" and become present tense that day, and seven planner activities
> are parked `status: invalidated` pending re-activation. This is a **calendar
> event with no build behind it** — the feeds will not signal it. See
> `_meta/next-patch.md` for the full unlock schedule.

## The feeds (poll these, in trust order)

1. **Build trigger (Tier 1):** `https://wago.tools/api/builds?product=wow` — a
   new build number is the authoritative "the game changed" signal. Compare the
   top `version` against *Latest retail build seen*. ⚠ The endpoint **ignores
   the `?product=` filter** and returns every product keyed by name — read
   `["wow"]` for retail and `["wowt"]` for PTR out of the same payload.
2. **Blue-post tracker (Tier 1 text):**
   `https://us.forums.blizzard.com/en/wow/groups/blizzard-tracker/posts.json?category_id=171`
   — JSON, 20 posts/page newest-first, fields `id` / `created_at` /
   `topic_title` / `excerpt`. Paginate with
   `&before=<URL-encoded ISO created_at of the oldest post on the page>` (NOT
   `offset` — ignored; NOT `before=<post_id>` — 500s). Full verbatim body per
   post at `…/en/wow/posts/<id>.json` (`cooked`). ⚠ The response shape is **not
   stable** — it comes back sometimes as a bare JSON array and sometimes as
   `{"posts": [...]}`. Handle both or the diff silently reads zero new posts.
   ⚠ Many posts are **teasers** whose `cooked` is one line plus a "View Full
   Article" link; the substance is in the linked `worldofwarcraft.com/news/<id>`
   article, which needs its own fetch.
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
| 2026-08-11 | 2026-07-02 → 2026-08-11 | **41** blue-tracker (14 content · 5 hotfix/tuning · 22 not-KB) | **FULL apply — 12.1 "Curse of Ula'tek" went live this day.** **Archived verbatim:** the content-update notes + the "S1 Ending / S2 Information" post → **new** `patch-notes/12.1.md`; the Jul 7/14/21/28 hotfix batches + the Jul 17 tuning post → `patch-notes/12.0.7.md` (they were issued under 12.0.7). **Ledger:** new `changelog-12.1.md`. **Swept:** 97 files (`endgame/` `systems/` `factions/` `planning/` `economy/` `_meta/`) + 26 warlock/DH class files, each adversarially verified, with three fix-up rounds. **Created 16 NEW files** — `endgame/lairs.md`, `endgame/raids/venomous-abyss.md`, `endgame/mythic-plus/season-2-overview.md` + 8 S2 dungeon stubs, `systems/coiled-isle.md`, `factions/zuljarras-forces.md`, and 3 planner activities. **Regenerated from live 12.1 game data:** 40 `talents.md`/`.json`, 40 `ability-inventory.md` (7,105 rows), 12 maxroll captures, `candidates.json`, `verify-in-game.md`. **`addon-dev/` handled separately** under its own evidence rules; `wowkb.kblint` now exits 0 (it was failing with 52 hits at HEAD). **Rejected / caught:** three PTR-era claims that never shipped (one-time Profession Knowledge reset, account-wide UI settings, "no gear-upgrade cost scaling") — recorded in `next-patch.md` so a stale pre-release source is recognisable; and 5 maxroll guides that bumped their headers to 12.1 while still recommending talents 12.1 **deleted** (flagged via `kb_caveat`, disproved against Tier-1 talent data). | **Best find:** `CurrencyTypes` DB2 @ 12.1.0.69214 gave the complete S2 crest ladder — Adventurer/Veteran/Champion/Hero/Myth **Mistcrest**, IDs 3437–3441, bands **269→334** vs S1's 224→289 (a clean +45 shift). Tier-1, no editorial source needed. **Three ledger errors of mine that the adversarial verifiers caught and I corrected mid-sweep:** (1) I told the sweep the Adventurer/Myth Mistcrest names were unconfirmed — the DB2 pull disproved it an hour later, after ~10 files had written the caution in as fact; (2) I truncated the Lairs reward table and suppressed the **Mythic row (312 → 318, Myth 1/6, Myth Mistcrest)**, which is in the source; (3) I wrote the Altar of Corrosion as fed by "Spirits of Corrosion" — it is fed by **Corrosive Coins**; Spirit of Corrosion I/II are discrete renown-8/14 grants. **Tooling defect found:** `spec_inventory.PINNED_BUILD` and `gen_abilities.PATCH` are hardcoded, so a "regeneration" silently re-emits the old patch — bumped, and a patch-day checklist item added to `game-version.md`. **Structural finding worth carrying forward:** Ritual Sites T6 no longer prints Myth crests, so Season 2 currently has **no repeatable solo Myth-crest source** — this invalidated the headline worked example in `planning/redesign-needs-first.md`. **Coverage gap, deliberate and declared:** the 34 non-warlock/DH specs' 102 `rotation`/`builds`/`abilities`/`gearing`/`sims` files were **not** re-verified; they keep `patch: 12.0.7` and carry an explicit dated "NOT RE-VERIFIED FOR 12.1" banner naming the four global class changes, rather than a false `reviewed:` stamp. `verify-in-game.md` grew 315 → 445 open items. |

## Full-tree verify sweeps

Whole-KB re-verification runs (`/update` Full path → `kb-patch-sweep`). Per-file
coverage lives in each file's `reviewed:` stamp; `grep -rL 'reviewed: <date>'` is
the audit.

| Swept on | Target | Scope | Result |
|---|---|---|---|
| 2026-07-07 | 12.0.7 | whole tree, 131 files (excl. `_meta`) | 128 passed · 7 drift auto-fixed · 3 hand-fixed · 0 tier-downgrades. All 16 files stranded on 12.0.5 brought current. Manifest: `scratchpad/sweep-items-2026-07-07.json`. |
| 2026-08-11 | 12.1 | game-KB core (`endgame` `systems` `factions` `planning` `economy` `_meta`) = 97 files, + 26 warlock/DH class files. **Excluded by design:** `addon-dev/` (own pass, own lint gates), `characters/` (volatile), 102 files across the other 34 specs (banner'd, see review log), generated artifacts (regenerated instead of swept). | Round 1: 97 items → **56 passed / 41 failed**. Round 2 (failures re-dispatched with the verifiers' own findings + the two corrected ledger facts): **25 more passed**, 16 left. Round 3: **14 more passed**; final 2 hand-fixed. Classes: 26 items → 19 passed, 7 re-dispatched. **`grep -rL 'reviewed: 2026-08-11'` over the swept scope returns ZERO** — no file was silently left behind. Fix-up workflows kept at `.claude/workflows/kb-12.1-*.js`. |
