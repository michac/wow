# Backlog — M+ Memory Trainer

*Ordered per the build sequence in [`project-spec.md`](./project-spec.md) §9:
foundation data → one proven dungeon → engine → modes → fill out the rest.
Check items off as they land.*

---

## Phase 1 — Archetype glossary (foundation, no live data)

The ~15–20 mechanic "alphabet." Dungeon-agnostic, so nothing here can go stale.

**Done 2026-06-24.** Derived **empirically** from the real boss + trash ability
corpus of all 8 dungeons (380 abilities pooled), not armchair — so it covers
exactly what the dungeons use. **Trash is first-class** in the taxonomy.

- [x] Draft the archetype list — **21 archetypes** (slightly over the ~15–20
      target; the two extra, `burn-window` and `balance-kill`, were forced by
      real unmapped abilities — Siphon Void and Broken Bond).
- [x] For each archetype: name, one-line tell ("what you see"), default
      response, typical consequence tier, role relevance (DPS/healer/tank).
- [x] Written to `knowledge/systems/mechanic-archetypes.md` (note: filename is
      `mechanic-archetypes`, not the old `m+-archetypes` placeholder) with full
      front matter (patch, fetched, sources, confidence).
- [x] Diagram idea noted per archetype (feeds the visual Archetype mode).

## Phase 2 — One dungeon's content (prove the data pipeline) ⚠ needs live data

**Done 2026-06-24 — and scaled to all 8 in the same push** (this absorbed
Phase 5; see below). Pipeline: Method + Icy Veins scraped via `wowkb.fetch`,
staleness-gated on Midnight/12.0/2026 signals, boss names corroborated against
the Blizzard journal API, distilled to one file per dungeon, then archetype-
tagged with a coverage assertion (every ability → exactly one slug).

- [x] First dungeon chosen: **Magisters' Terrace** (then all 8).
- [x] Sourced tier-highest-first: Blizzard journal (`journal-instance` /
      `journal-encounter`) + Method + Icy Veins guides.
- [x] Route segments, key trash, boss abilities captured per dungeon.
- [x] Every ability mapped → an archetype slug (coverage-checked).
- [x] Each item tagged: dungeon, consequence tier, role. *(Per-segment tagging
      is coarse — route is listed but abilities aren't yet pinned to a specific
      segment; tighten when the trainer's Route mode needs it.)*
- [x] Distilled to `knowledge/endgame/mythic-plus/<dungeon>.md` w/ front matter;
      `season-1-overview.md` `## TODO` for per-dungeon files resolved.
- [x] Lock the card-data shape — **done in Phase 3** and validated against all
      8 real dungeon files (380 cards). Final shape (evolved from the spec's
      `{cue, promptType, answer, archetypeRef, tags}`):
      `{ id, cue:{dungeon,dungeonHue,segment,caster,casterKind,spell},
      promptType:'classify', answer:archetypeSlug,
      reveal:{whatItDoes,response,tier,role,lowConfidence}, options }`.
      The build **fails** if any `answer` falls outside the 21 canonical slugs.

## Phase 3 — Engine (Svelte 5 app, wired to Phase 1+2)

**Done 2026-06-24.** Lives in `projects/mplus_memory/app/`. Rep loop runs
end-to-end on the real 380-card corpus.

**Stack decision (supersedes the spec's "single self-contained React file"):**
the single-file/React+CDN constraint was an artifact-era assumption. Target is
**GitHub Pages** (static host, multi-file fine), so: **Bun + Vite + Svelte 5
(runes) + Tailwind v4** (`@theme` tokens), `localStorage` persistence, a Bun
prebuild script (`scripts/build-content.mjs`) that compiles the KB → `content.json`.
A one-file build remains a one-plugin toggle if ever needed.

- [x] Scaffold the app (Vite + Svelte 5 + Tailwind v4 under `app/`; builds to
      static `dist/` for Pages with `base:'/wow/'`).
- [x] **Content layer:** `scripts/build-content.mjs` parses KB md →
      `src/content.json` (archetypes + dungeons + cards) with a **coverage
      assertion**; `src/lib/content.js` exposes selectors.
- [x] **Engine layer:** SM-2 SRS scheduler (`src/lib/srs.js`).
- [x] **Engine layer:** session builder (`src/lib/session.js`) — due cards
      through active filters; **interleaves dungeons** (round-robin, never blocks
      one at a time).
- [x] **Engine layer:** grader (reveal → Again/Hard/Good/Easy self-grade).
- [x] **Persistence layer:** one versioned `localStorage` key
      (`mplus.trainer.v1`: schedule + settings + stats) auto-persisted via a runes
      store (`src/lib/store.svelte.js`).
- [x] **Drill mode:** cue → cast-bar-timed classify-the-archetype MC → rich
      reveal (Do / What's happening / the mechanic) → self-grade; motion only on
      correct/incorrect.
- [x] **Archetype ("Alphabet") mode:** all 21 archetypes, made visual
      (letter chips, expand for tell/do/stakes/role).
- [x] **UI system:** dark default; consequence-tier semantic colors driven by a
      single `--tier` knob; per-dungeon `--dgn` hue rings the device; display vs
      body type. Ported from the approved `prototypes/cards-phone.html`.
- [x] **Role filter:** wired in from the start (defaults to DPS; All/Healer/Tank
      = filter flip) plus per-dungeon toggles, in a Settings sheet.
- [x] Ran through frontend-design guidelines (token-driven, not utility-soup;
      stark drill screen) so it doesn't read as a template.

### Follow-ups from the Phase-3 build (2026-06-24)

- [ ] **Boss art:** cards use a dungeon-tinted monogram placeholder. Add
      `scripts/fetch-boss-art.mjs` to pull encounter/creature renders (Blizzard
      media API / zamimg) → `src/assets/bosses/<slug>.webp`, glyph fallback.
- [x] **GH Pages wiring (2026-06-24):** copied `app/deploy.yml.example` →
      `.github/workflows/mplus-trainer-pages.yml`, enabled Pages (Actions
      source). **Live at https://michac.github.io/wow/.** (See the GitHub Pages
      deployment item below.)
- [ ] **Card budget balance:** all 380 rows currently become cards; consider
      down-weighting ⚪-flavor / low-confidence trash so the pool isn't bloated.
- [ ] **Boss strategy prose is dropped (content fidelity):** each boss `###`
      section has an intro paragraph (e.g. Overgrown Ancient "stay stacked, move
      together during Germinate…"). `build-content.mjs` only harvests the ability
      *table*, so that prose never reaches `content.json`, the reveal, or a future
      Browse mode. Parse it into `boss.note` and surface it.
- [ ] **Boss cards aren't role-filtered (filter semantics):** only trash rows
      carry a Role column; boss abilities parse to `role: null`, which
      `cardsForFilters` treats as universal — so with role=DPS every boss card
      stays in the pool (that's why DPS is 313, not lower) and only trash filters.
      Defensible (everyone should know boss mechanics) but currently *implicit*.
      Decide: keep-all-bosses by design (document it), or infer a boss role from
      the ability's archetype / DPS-notes section.
- [ ] **Cast-bar timeout UX (minor polish):** when the timer expires the card
      auto-reveals and scores as wrong, but there's no "ran out of time" signal
      beyond the red badge — looks identical to a wrong pick. Add a distinct
      timed-out state.
- [ ] **Test-harness deps (open decision):** `bun run test` (build + headless
      mount/flow smoke via `scripts/smoke.mjs`) pulled in `happy-dom` +
      `@testing-library/svelte` as devDeps (no browser binary). Keep the smoke
      test as a regression guard, or drop it to keep the dep list minimal.

### GitHub Pages deployment (2026-06-24)

- [x] **Shipped the trainer to GitHub Pages.** Committed the previously-untracked
      `projects/mplus_memory/app/` + `prototypes/`, added the deploy workflow at
      `.github/workflows/mplus-trainer-pages.yml` (copied from
      `app/deploy.yml.example`; `bun install --frozen-lockfile` → `bun run build`
      → `upload-pages-artifact` → `deploy-pages@v4`), and enabled Pages with the
      **GitHub Actions** source. Pushed to `main`; the path filter auto-triggers
      the deploy. **Live: https://michac.github.io/wow/.**

## Phase 4 — Remaining modes

Stubbed in the nav (disabled) by Phase 3; routes are already parsed into
`content.json` ready for Route Walk. Split into discrete, separately-shippable
items below (simplest first).

- [ ] **Identify the dungeons & their bosses** — a lightweight roster/reference:
      the 8 dungeons and each boss enumerated (names, order). Listed first as the
      simplest; seeds the Browse mode.
- [ ] **Dashboard + Browse** — one item: mastery heatmap (solid-vs-shaky per
      dungeon, Leitner-style visual SRS, driven off `store.schedule`) plus the
      demoted plain Browse reference.
- [ ] **Route walk** — second item: step-through memory-palace walk **plus** an
      order drill (shuffle the route steps, player taps them back into sequence)
      for the generation effect.

## Phase 5 — Fill out the other 7 dungeons

**Content done 2026-06-24** — pulled forward into the Phase 1/2 push instead of
waiting for the engine (the agreed scope was all 8 now). All 8 `knowledge/`
files exist, tagged and journal-corroborated.

- [x] Maisara Caverns
- [x] Nexus-Point Xenas
- [x] Windrunner Spire
- [x] Algeth'ar Academy
- [x] Seat of the Triumvirate
- [x] Skyreach
- [x] Pit of Saron
- [x] Magisters' Terrace (the "first" dungeon)
- [ ] Final pass: balance card budget per dungeon (all 8 lightly, not deep-few)
      — defer to Phase 3/4 (a card-authoring concern, not content).

### Known follow-ups from the content push (2026-06-24)

- [x] **Boss third-source cross-check (2026-06-24):** compared all 8 files
      against the Dalaran Gaming "All 8 Dungeons" video (launch day, 2026-03-24,
      added as a tier-3 source in each file). Strong agreement; it independently
      confirmed the `burn-window` and `balance-kill` archetypes. Two minor
      discrepancies recorded in-file (Algeth'ar: Crawth Savage Peck bleed-vs-DoT,
      Vexamus Mana Bombs 2-vs-3 targets).
- [x] **Format consistency (2026-06-24):** all 8 trash sections normalized to one
      schema — `| Mob | Ability | See → Do | Archetype | Tier | Role |` (emoji-only
      tier, bare canonical slug, single-source rows flagged inline). Boss + trash
      now share a column contract, so the Phase 3 card builder can parse both.
- [x] **Boss-name field markup (2026-06-24):** the encounter id was riding *in*
      the boss `###` heading (display string) in four inconsistent spellings
      (`(journal-encounter 610)`, `(journal 2495)`, `(enc 1982)`, bare `(2662)`),
      so the card builder regex-scraped it — and `journal-encounter`/`enc` slipped
      through, leaking e.g. "Scourgelord Tyrannus (journal-encounter 610)" onto a
      live card. Fixed at the **format** level: moved the id to a `<!-- enc:NNN -->`
      HTML comment on all 29 boss headings (invisible when rendered, unambiguous to
      parse), and the builder now strips the marker at the h3 capture +
      defensively. Principle: structured fields get explicit markup; nothing is
      scraped out of a display string. Descriptive parens (`(immune to CC)`) are
      untouched.
- [ ] **Trash confidence (still open):** several dungeons' trash is **Method-only**
      (Icy Veins detailed bosses but few trash mobs) and flagged `confidence: low`
      in-file — Magisters' Terrace especially. The launch video is **boss-only**, so
      it did **not** close this gap. Re-corroborate trash from a real second source
      before drilling it hard.
- [ ] **Algeth'ar boss tables:** 5-col header but 6-col rows (an extra Role cell) —
      renders fine but technically malformed. Tidy if boss tables should be strict.

---

## Cross-cutting / later (not yet scheduled)

- [ ] **Mnemonic nicknames** (idea, 2026-06-24): give abilities/packs/archetypes
      optional cutesy aliases as memory hooks — "red blobbie blast", "trollie and
      birdie", "boom magnet". Distinctive, silly labels stick harder than canonical
      spell names (distinctiveness + generation effect, per spec §2). Shape: an
      optional `nickname` on a card/ability (and maybe a default per archetype);
      surface it on the drill reveal and in Browse, never as the *cue* (the cue must
      match the in-game tell). Could be a fun "name this mechanic" generation
      exercise where the player coins their own — self-generated names stick best.
- [ ] Role expansion: enable healer + tank card sets behind the existing filter.
- [ ] Verify Xal'atath's Bargain affix rotation (open TODO in overview).
- [ ] Patch-watch: re-verify content if game state moves past 12.0.5.
