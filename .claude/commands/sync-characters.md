---
description: Re-sync every previously-synced character in knowledge/characters/ — fetch live data + currencies, then update each snapshot file with deltas
argument-hint: "[name ...] (optional — limits to these characters; default: all)"
---

# /sync-characters — refresh all character snapshots

Re-pull live data for every character already tracked in
`knowledge/characters/` and write the updates back into their snapshot files.
Uses the `wowkb.character` tool (see `CLAUDE.md`), which stitches together the
Blizzard profile API and on-disk Syndicator currencies. Follow the staleness
doctrine throughout: cite the live patch + the fetch date in front matter.

Optional filter (may be empty): **$1** — if given, only sync the named
character(s); otherwise sync all.

## Step 0 — Build the character list (no master list; derive it)
The snapshot files carry a profile API URL in their `sources:` front matter,
which encodes `character/<realm>/<name>`. That is the source of truth:

```bash
grep -rhoE 'character/[a-z0-9-]+/[a-z0-9-]+' knowledge/characters/ \
  | sort -u | awk -F/ '{print $3, $2}'   # → "<name> <realm>" per line
```

This deliberately skips non-snapshot files (e.g. `encomplete-plan.md`) because
they have no profile URL. If `$1` is non-empty, intersect the list with it.
Map each `<name> <realm>` to its file `knowledge/characters/<name>-<realm>.md`.

## Step 1 — Stamp values
- Live patch = the `patch:` in `knowledge/_meta/game-version.md` (source of
  truth). Use it for every file's front-matter `patch:`.
- `fetched:` = today's date.

## Step 2 — Per character: fetch, then update its file
For each `<name> <realm>`:

1. Run the tool from `tools/`:
   ```bash
   uv run python -m wowkb.character <name> --realm <realm>
   ```
   It fetches all profile endpoints (→ `raw/blizzard/`) and reads currencies
   from Syndicator. Read the digest it prints.
2. **Before rewriting, read the existing file** so you can diff — the value of
   the snapshot is the *deltas* (ilvl moved, new renown, crest stock changed,
   spec/hero-tree swap, professions leveled). The tool emits **data only**; the
   narrative/deltas are yours to add.
3. Update the file:
   - Front matter: bump `patch:` (Step 1) and `fetched:` (today). Keep the
     existing `sources:` URL.
   - Refresh the data sections (Identity, Gear, Mythic+, Renown, Professions,
     Currencies) from the digest. For **Renown**, keep the Midnight-relevant
     factions (the tool lists all renown, including maxed old-expansion ones —
     curate down to what matters).
   - Call out what changed vs the prior snapshot, and **correct** anything the
     old file got wrong (screenshot-era guesses especially).
   - **Preserve** historical/reasoning sections and plan pointers (e.g. the
     dated "Gearing plan (sketched …)" / "Talent audit (…)" records and the
     `encomplete-plan.md` pointer). Do not touch `*-plan.md` files — those are
     hand-authored plans, not snapshots.

## Step 3 — Currency caveats (always)
- The tool reads Syndicator, which only flushes on in-game `/reload` or logout.
  If a character's currency numbers are identical to the prior snapshot **and**
  its `last login` is old, note that the currencies may be stale and suggest a
  `/reload` on that character before trusting them for spend advice.
- **Sparks of Radiance** (an item) and **Catalyst charges** (separate system)
  are NOT in Syndicator's currency table. Leave them flagged "check in-game";
  never invent numbers for them.

## Step 4 — Summarize
Report per character: the headline changes (level/ilvl/spec, notable renown or
crest movement) and anything still stale or needing in-game confirmation.
Then ask whether to commit.

## Step 5 — Surface open in-game verifications (you're logged in — knock some out)
A sync means the user is **in-game right now**, which is the one moment the KB's
"confirm in-game" backlog can actually be resolved. Refresh and show it:

```bash
uv run python -m wowkb.gen_verify --print   # from tools/ — the current checklist
```

From `knowledge/_meta/verify-in-game.md`, surface the handful of items **relevant
to the characters just synced** (their `characters/<name>*.md` items) plus any
account-wide ones — a short, opt-in "while you're on, could you check…" list, not
a wall. For each one the user confirms, follow that file's **resolution
protocol**: edit the source claim (apply the finding, bump `confidence:`, stamp
the date), delete the `@verify-ingame` marker, then re-run `gen_verify` so it
drops off. Never force it — the point is that these stop rotting, not that every
sync clears them.
