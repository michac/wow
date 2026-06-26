# M+ Memory Trainer — app

Spaced-repetition trainer for Midnight Season 1 Mythic+ dungeon mechanics.
Phase 3 (the engine) of [`../project-spec.md`](../project-spec.md). The static
KB in `knowledge/` is the content source; this app turns it into a rep loop.

## Stack

Bun · Vite · Svelte 5 (runes) · Tailwind v4. Builds to a static `dist/` for
GitHub Pages. State persists to `localStorage` under one versioned key
(`mplus.trainer.v1`).

## Develop

```bash
bun install
bun run dev        # regenerates content.json, then serves at /wow/
```

`predev`/`prebuild` run `scripts/build-content.mjs`, which parses the KB
markdown into `src/content.json` and **fails the build if any ability maps to a
non-canonical archetype** (the Phase-2 coverage guarantee).

```bash
bun run content    # just regenerate src/content.json + print the coverage report
bun run build      # → dist/  (static, base path /wow/)
bun run preview    # serve the built dist/ under /wow/
bun run test       # build + headless mount/flow smoke test (happy-dom)
```

## Content pipeline

`scripts/build-content.mjs` reads:

- `knowledge/systems/mechanic-archetypes.md` → the 21-slug archetype "alphabet".
- `knowledge/endgame/mythic-plus/<dungeon>.md` (8 files) → route, boss rows
  (`| Ability | What it does | Do | Archetype | Tier |`) and trash rows
  (`| Mob | Ability | See → Do | Archetype | Tier | Role |`).

It emits one **card per boss/trash ability row** (≈380), each:

```js
{ id, cue: { dungeon, dungeonHue, segment, caster, casterKind, spell },
  promptType: "classify", answer: archetypeSlug,
  reveal: { whatItDoes, response, tier, role, lowConfidence },
  options /* answer + 3 deterministic distractors */ }
```

Per-dungeon hues live in `DUNGEON_HUE` in the script and are mirrored as
`--color-dgn-*` tokens in `src/app.css`.

## Architecture (four layers, per the spec)

- **Content** — `src/lib/content.js`: imports `content.json`, selectors
  (`cardsForFilters`, archetype/dungeon/card lookups).
- **Engine** — `src/lib/srs.js` (SM-2) + `src/lib/session.js` (builds the queue,
  **interleaves dungeons**, never blocks one).
- **Persistence** — `src/lib/store.svelte.js`: a runes `$state` store mirrored to
  `localStorage` via `$effect`.
- **View** — `src/lib/components/*.svelte` (ported from
  `../prototypes/cards-phone.html`) + `App.svelte`. Modes: **Drill** and
  **Alphabet** are live; Route / Stats / Browse are in the nav, disabled (Phase 4).

## Boss art (follow-up)

Cards currently use a dungeon-tinted monogram placeholder. Real journal/creature
renders are a tracked backlog item (`scripts/fetch-boss-art.mjs` →
`src/assets/bosses/<slug>.webp`).

## Deploy to GitHub Pages

`vite.config.js` sets `base: "/wow/"` (override with `VITE_BASE`). To publish via
Actions, copy the sample workflow to the repo root and enable Pages
(Settings → Pages → Source: GitHub Actions):

```bash
mkdir -p ../../../.github/workflows
cp deploy.yml.example ../../../.github/workflows/mplus-trainer-pages.yml
```

Or build locally and push `dist/` with the `gh-pages` CLI.
