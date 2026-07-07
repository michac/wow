---
description: The one-door KB update. Detect what's shipped since the watermark, then quick-apply hotfixes or full-sweep a content patch.
argument-hint: "[optional: 'full' to force the full sweep, or a target patch e.g. 12.1]"
---

# /update — the single KB update entry point

One command. It **detects** what's changed in-game since the last review,
**gates** on whether there's anything new, and **offers** the right amount of
work: a **quick apply** (hotfixes / tuning / small content) or a **full apply**
(a real content patch — full-tree re-verify + bump the source of truth).

Follow the staleness doctrine in `CLAUDE.md` throughout. Arg `$1` may be empty,
`full` (force the full path), or a target patch like `12.1`.

> ## Provenance precedence — the rule both paths obey
> Authoritative feed data is the **floor**. A claim already sourced **Tier-1**
> (a Blizzard blue post, the `patch-notes/` verbatim archive, or the
> `moving-values.md` registry) may **not** be overwritten to match a lower-tier
> source (Icy Veins / Wowhead editorial / SEO). Lower tiers may **corroborate or
> add**, never **regress**. On disagreement: keep the Tier-1 value and **flag**
> it. Resolve proper-noun / name conflicts via **game data** (wago.tools DB2 or
> the Wowhead NPC/item DB page), not editorial prose. (This is why we keep
> `moving-values.md` + `patch-notes/` — they are the immune system for updates.)

---

## Step 0 — Detect (always runs)

1. Read `knowledge/_meta/feed-watermark.md` for the cursors: *reviewed-through*
   date, *latest build seen*, *newest blue-tracker post id*.
2. Live build: `curl -s "https://wago.tools/api/builds?product=wow"` → top
   `version` (Tier-1 "did the game change?" signal). Also glance
   `?product=wowt` (the **PTR** feed) — a new `wowt` build or a higher minor
   version there is the earliest signal of the *next* patch.
3. New blue posts since the watermark:
   `https://us.forums.blizzard.com/en/wow/groups/blizzard-tracker/posts.json?category_id=171`
   — JSON, 20 posts/page, newest first. Fields: `id`, `created_at`,
   `topic_title`, `excerpt`; full verbatim body per post at
   `…/en/wow/posts/<id>.json` (`cooked`). **Paginate with
   `&before=<URL-encoded ISO created_at of the oldest post on the current page>`**
   (NOT `offset` — that's ignored — and NOT `before=<post_id>` — that 500s; it
   must be the timestamp). Walk pages until `created_at` ≤ the watermark. For a
   full hotfix-thread backfill you can instead fetch the rolling thread directly:
   `…/t/<topic_id>.json` → `post_stream.stream`, then
   `…/t/<topic_id>/posts.json?post_ids[]=…`, keeping `staff:true` posts.
4. Glance the news feed `https://worldofwarcraft.blizzard.com/en-us/news` for
   non-forum items (event go-lives, Trading Post).
5. **If the live build == watermark build AND no new posts** → report
   "KB current as of `<watermark>`, live build `<X>`, nothing since" and **STOP.**

## Step 1 — Triage the delta & choose the mode

Classify each new post: `hotfix | tuning | content | event | not-KB`; note the
KB surface(s) it touches and a one-line what-changed. Then pick the recommended
mode:

| Signal | Mode |
|---|---|
| Only hotfix builds under the **same minor version**; no new "Content Update Notes" article; no NEW system/zone/raid in triage | **QUICK** |
| Minor version **bumped** (e.g. 12.0.7 → **12.1**), or a new content-update-notes article, or triage reveals a NEW system/zone/raid | **FULL** |
| Arg `$1` == `full` or names a target patch | **FULL** (forced) |

Present the delta summary + your recommendation, and **offer QUICK or FULL**.
Wait for the user's choice, then run that path. Both paths end by advancing the
watermark (Step W).

---

## QUICK apply  (hotfixes / tuning / small content)

Touches only files the feed names. This is the everyday path.

1. **Fetch full bodies** of the KB-relevant posts (`posts/<id>.json` → `cooked`).
2. **Auto-archive (verbatim, append-only):** append every hotfix batch, class-
   tuning announcement, and reward-change post to the live patch's
   `knowledge/_meta/patch-notes/<patch>.md` under its `## Hotfix & blue-post
   change log`, each as a dated `####` entry with its source URL. No interpretation.
3. **Gated content edits:** for each post that *changes a KB claim* (not just a
   bug fix), propose a precise edit (exact old→new), then **adversarially verify**
   it — you MAY spawn subagents to propose + refute in parallel. Apply only
   CONFIRMED edits. **Obey provenance precedence:** reject any edit that would
   overwrite a Tier-1-sourced claim with a lower-tier source; resolve name/number
   conflicts via game data. Bump `fetched:` + add the blue-post source URL on each
   edited file. If an applied edit leaves a claim that still needs **in-game**
   confirmation, tag that line `@verify-ingame` and re-run
   `uv run python -m wowkb.gen_verify` (see `_meta/verify-in-game.md`) so it lands
   on the in-game checklist instead of rotting as free text.
4. **Refresh `moving-values.md`** for any reward/tuning value that moved (old →
   `Was`, new → `Current value`, `Set by` = the hotfix date). Add a row only if
   it's volatile *and* commonly mis-stated on the web.
5. **Refresh `next-patch.md` on a PTR signal.** If Detect found a new `wowt`
   (PTR) build, a PTR/next-content-update blue post, or a datamining recap for a
   not-yet-live patch, rebuild `knowledge/_meta/next-patch.md` to the
   confirmed-on-PTR state (codename, PTR build, watch-list) at `confidence:
   medium` while PTR-only. (When that patch actually goes **live**, the Full
   path's F8 takes over.)
6. Go to **Step W**.

---

## FULL apply  (a real content patch)

Everything QUICK does, plus a whole-tree re-verify and a source-of-truth bump.
Migrated from the former `/update-patch`. **The full path is authorized to:**
spawn **subagents**; **author & run a Workflow** when the work benefits from
deterministic fan-out; and do **deeper research** when official notes are sparse
(events, brand-new content) — `WebSearch`/`WebFetch` and
`uv run python -m wowkb.youtube transcript <url>` on trusted creators — always
requiring Midnight / version / current-year signals and obeying provenance
precedence (never let a Tier-3/4 source overwrite Tier-1 feed data).

**F0 — Confirm the target patch.** From `$1` if given; else the newest live build
from Step 0. Confirm number, codename, go-live date. If `game-version.md` already
records it as live and the KB is on it, stop.

**F1 — Capture the notes (keystone).** Fetch Tier-1 first: the official
content-update notes + the running hotfix log through today (`wowkb.fetch` or
WebFetch). Confirm the version number on the page matches (codenames lie).
**Archive verbatim** to `patch-notes/<patch>.md` (committed copy against link
rot) under `##` headings with source URLs + today's date; standard front matter,
`confidence: high`. Don't summarize here.

**F2 — Change ledger.** Distill into `knowledge/_meta/changelog-<patch>.md` (full
front matter). Body grouped by KB surface, then a **KB file impact map** table,
one row per affected file with a verdict: **CHANGED** (content edit needed) /
**RESTAMP** (no change found — re-verify + bump front matter) / **NEW** (create).

**F3 — Work list.** `grep -rl '^patch: <old-version>' knowledge --include='*.md'`
for every file still on the old patch; reconcile against the impact map so every
file gets a verdict; add NEW rows. Result: `[{ file, verdict, why }]`.

**F4 — Fan-out sweep.** Run the saved workflow (per-file update + adversarial
verify, now provenance-aware):
```
Workflow({ name: "kb-patch-sweep", args: {
  repo: "<abs repo root>", patch: "<target>", build: "<build or ''>",
  fetched: "<today ISO>", ledger: "<abs path to changelog-<patch>.md>",
  items: [ { file, verdict, why }, ... ] } })
```
Returns `{ total, passed, failures, drift_flagged, tier_downgrades, new_files }`.

**F5 — Refresh `moving-values.md`** (same as QUICK step 4, but across the whole
ledger's reward/tuning changes).

**F6 — Triage failures by hand.** For each `failures` / `drift_flagged` /
`tier_downgrades` entry: fix real correctness bugs (and cross-check linked
siblings), fix cosmetic version labels, close citation gaps. A flagged
`tier_downgrade` means the sweep almost regressed Tier-1 data — restore the
Tier-1 value. Re-read after editing.

**F6.5 — Regenerate generated artifacts.** If any `planning/activities/*.md`
changed, regen the ranker input: `uv run python -m wowkb.gen_candidates` (verify
with `--check`). If `repeatables.json` changed, `uv run python -m
wowkb.gen_addon_quests`. These are generated *from* the `.md` — never hand-edit
the JSON, and never leave it stale after an activity edit. If any file gained or
resolved a `@verify-ingame` marker this sweep, refresh the in-game checklist too:
`uv run python -m wowkb.gen_verify` (verify with `--check`).

**F7 — Consistency & coverage sweep.**
`grep -rh '^patch:' knowledge --include='*.md' | sort | uniq -c` (no file left on
the old version) and `grep -rn '<old-version>' knowledge --include='*.md'` (every
remaining hit is a deliberate historical/provenance reference, never a live
claim). **Coverage:** `grep -rL 'reviewed: <today>' knowledge --include='*.md'`
(minus `_meta`) lists every file the sweep did NOT stamp — those are gaps to
re-run or explain, never silently left behind. Check files the workflow didn't
touch (`_meta/next-patch.md`).

**F8 — Bump the source of truth (LAST).** `game-version.md`: live patch/build/PTR
fields, new "<patch> highlights", demote the prior patch to "historical —
superseded". Reset `next-patch.md` from PTR notes (or "none confirmed").

**F9 —** Go to **Step W**, then report: files swept, NEW files, pass/fail tally,
every hand-fix, remaining low-confidence items, and the three durable artifacts
(`patch-notes/<patch>.md`, `changelog-<patch>.md`, refreshed `moving-values.md`).

---

## Step W — Advance the watermark (both paths)

Update `knowledge/_meta/feed-watermark.md`: set *reviewed-through* to today,
*latest build seen* to the live build, the *newest blue-tracker post* cursor to
the newest post id/timestamp reviewed, and append a **review-log row** recording
the window, posts triaged, what was archived / applied / **rejected** (e.g. a
caught Tier-1-vs-lower-tier conflict), and any gaps surfaced (stale `next-patch`,
files missed by a prior sweep). The review log is the running record — there is
no separate deferred ledger.
