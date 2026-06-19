---
description: Sweep the KB to a new WoW patch — capture notes, build a change ledger, fan out a verified per-file update, bump the source of truth
argument-hint: "[target patch e.g. 12.0.8] (optional — auto-detects latest if omitted)"
---

# /update-patch — patch-day KB sweep

Migrate the entire `knowledge/` tree from the current live patch to a newer one,
the same way it was done for the 12.0.5 → 12.0.7 sweep. Follow the staleness
doctrine in `CLAUDE.md` throughout: Tier-1 sources first, require
"Midnight"/version/current-year signals, cite the patch + at least one source in
every file.

Target patch (from the user, may be empty): **$1**

Work through these steps in order. Do not skip Step 0 — the workflow is only as
good as the ledger it diffs against.

## Step 0 — Determine the target patch
- If `$1` is given, that is the target (e.g. `12.0.8`).
- If empty, find the latest live build: check `knowledge/_meta/game-version.md`
  for the current value, then confirm the newest via WebSearch on the official
  content-update-notes page and/or `uv run python -m wowkb.wago` build feed.
  Confirm the patch number, its codename, and its go-live date before continuing.
- If the target equals what `game-version.md` already records as live and the KB
  is already on it, stop and say so — nothing to do.

## Step 1 — Capture the notes (the keystone)
Fetch, from Tier-1 first:
- the official **content-update notes** for the target patch
  (`worldofwarcraft.blizzard.com` / `news.blizzard.com`), and
- the running **hotfix log** through today.

Use `WebFetch`/`WebSearch` (load via `ToolSearch` if needed) or
`uv run python -m wowkb.fetch <url>`. Verify the version number on the page
matches the target (patches have codenames — confirm the number, not just the
name).

## Step 2 — Write the change ledger
Distill the notes into `knowledge/_meta/changelog-<patch>.md` with full front
matter (`patch`, `build`, `fetched: <today>`, real source URLs, `confidence`).
Structure it like `knowledge/_meta/changelog-12.0.7.md`:
- a "what changed" body grouped by KB surface (content adds, systems, raids,
  classes/PvP, prey/delves, factions, items), then
- a **"KB file impact map"** table with one row per affected file and a verdict:
  - **CHANGED** — notes touch this topic; content edit needed
  - **RESTAMP** — no change found; re-verify + bump front matter only
  - **NEW** — file must be created (new system/raid/zone)

## Step 3 — Build the work list
- `grep -rl '^patch: <old-version>' knowledge --include='*.md'` to list every
  file still on the old patch.
- Reconcile that list against the impact map. Every old-patch file gets a
  verdict; add NEW rows for genuinely new content. The result is an array of
  `{ file, verdict, why }`.

## Step 4 — Run the fan-out workflow
Invoke the saved workflow (one agent updates each file, a second adversarially
verifies it):

```
Workflow({
  name: "kb-patch-sweep",
  args: {
    repo:    "<absolute repo root>",
    patch:   "<target version>",
    build:   "<client build or ''>",
    fetched: "<today ISO date>",
    ledger:  "<absolute path to the changelog file from Step 2>",
    items:   [ { file, verdict, why }, ... ]
  }
})
```

It runs in the background and returns `{ total, passed, failures, drift_flagged,
new_files }`.

## Step 5 — Triage failures and fix by hand
For each entry in `failures` / `drift_flagged`, read the file and judge:
- **Real correctness bug** (stale claim, missed change, internal contradiction)
  → fix it, and cross-check sibling files it links to.
- **Cosmetic** (e.g. a version label left in a heading) → fix the label.
- **Citation gap** → add a real source URL; for a self-referential meta registry
  an empty `sources:` is an acceptable, documented exception.
Re-verify with a quick read after editing.

## Step 6 — Final consistency sweep
- `grep -rh '^patch:' knowledge --include='*.md' | sort | uniq -c` → confirm no
  file is left on the old version.
- `grep -rn '<old-version>' knowledge --include='*.md'` → every remaining hit
  must be a deliberate historical/provenance reference (e.g. "added in X", a sim
  binary caveat), never a live claim. Check files the workflow did NOT touch too
  (e.g. `_meta/next-patch.md`).

## Step 7 — Bump the source of truth (do this LAST)
- Update `knowledge/_meta/game-version.md`: live patch/build/PTR fields, a new
  "<patch> highlights" section, and demote the previous patch's highlights to
  "historical — superseded".
- Reset `knowledge/_meta/next-patch.md`: if no next patch is on the PTR, set it
  to a "none confirmed" watch-list state; otherwise rebuild it from PTR notes.

## Step 8 — Report
Summarize: files swept, NEW files, pass/fail tally, every fix you made in
Step 5, and any remaining low-confidence items needing in-game verification.
Note that `changelog-<patch>.md` is the reusable diff for that patch.
