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

- [x] **Boss art (2026-06-24):** boss cards now show official journal portrait
      renders; trash + any un-fetched boss keep the dungeon-tinted monogram. The
      fetcher lives in **Python** (`tools/wowkb/bossart.py`, run
      `uv run python -m wowkb.bossart`), **not** the originally-guessed
      `scripts/fetch-boss-art.mjs` — Blizzard OAuth + the `get()` helper already
      exist in `wowkb.blizzard`, so re-implementing creds in Bun would duplicate
      them. Pipeline: `journal-encounter/{enc}` → `creatures[].creature_display.id`
      → `media/creature-display/{id}` `zoom` asset → download → Pillow resize 480px
      + webp q80 → `app/src/assets/bosses/<dungeonSlug>__<bossSlug>.webp` (29 files,
      committed). `build-content.mjs` emits a deterministic `cue.artKey` on boss
      cards; `DungeonFrame.svelte` resolves it via a Vite glob with a monogram
      fallback. The `<bossSlug>` slug rule is shared between `bossart.py` and
      `build-content.mjs` `slugify()`.
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
- [x] **Cast-bar timeout UX (minor polish):** when the timer expires the card
      auto-reveals and scores as wrong, but there's no "ran out of time" signal
      beyond the red badge — looks identical to a wrong pick. Add a distinct
      timed-out state. *(Done as part of the auto-grade item below — `NextButton`
      shows distinct "⏱ Ran out of time" copy; a timeout maps to `again`.)*
- [x] **Drop the reveal Hard/Easy buttons → auto-grade on hesitation (UX +
      engine):** the cast bar is already a solve-timer — the longer you take to
      classify, the harder the card was for you. So stop asking the player to
      self-grade Again/Hard/Good/Easy on the reveal and instead **infer the SM-2
      grade from time-to-answer** (and correctness), then show a single big
      **NEXT** button. Mapping: wrong pick or timeout → `again`; correct maps on
      elapsed fraction of the cast-bar `duration` (7s) — snap-fast → `easy`,
      comfortable → `good`, slow/last-second → `hard`.
      - Shipped (2026-06-24). `gradeFromLatency(wasCorrect, elapsedMs, durationMs)`
        in `srs.js` (unit-checked at the 0.33/0.66 boundaries); fed into the
        unchanged `recordReview()` / `review()` path — **no SRS engine change**.
        `CastBar.progress` is now `$bindable`; `Drill` reads elapsed straight off
        the visible clock via a shared `DURATION` const. `GradeBar` deleted,
        `NextButton` added.
      - **Resolved decisions:** thresholds locked at **33% / 66%** of duration
        (tunable later by feel). **No fast-wrong differentiation** — any wrong
        answer maps to `again`. **No manual override** — the whole point is one
        tap; revisit only if retention data argues otherwise.
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
- [x] **Test mode (doubles as intro mode):** a single, ordered pass through **one
      dungeon's** casts — boss-by-boss in **route/pull order**, one shot at each
      card (no re-queue on a miss, no second look). Ends on a score/report card
      ("11 / 14 — shaky on Skyreach's frontals"). Two jobs in one mode:
      - **Intro / first-contact:** this is the *blocked* acquisition pass the
        interleaving research says novices need before the interleaved Drill pays
        off — pure random interleaving is confusing with no mental model yet; a
        short in-order pass through a single dungeon builds the gist, then the
        player graduates to the mixed Drill. (Grounds the "hybrid onboarding"
        recommendation from the interleaving-vs-blocking discussion.)
      - **Test / assessment:** an honest one-shot check — no SRS safety net, no
        hesitation auto-grade leniency — that surfaces *where* you're weak before
        a key.
      - **Shape (mostly reuses Drill):** same classify cue + cast bar + reveal;
        the differences are the *queue source* and *termination*. Queue = one
        dungeon, filtered and **sorted by boss/route order** (not SRS-due-
        interleaved); within a boss, the several casts can go in **definition
        order or shuffled** (pick one — definition order is simplest and
        deterministic for a "test"). One pass, no `again`-requeue.
      - **SRS interaction (decide on impl):** still call `recordReview()` so a
        first-contact pass *seeds* the schedule (intro framing) — but because
        it's one-shot, a miss just schedules normally; no in-session relearn loop.
        Alternatively make it schedule-neutral (pure assessment) and gate behind a
        toggle. Lean: seed the schedule — an intro that teaches nothing to the SRS
        wastes the pass.
      - **Plumbing already present:** the filter sheet already narrows to one
        dungeon, and `content.json` carries `route[]` + per-boss ability order, so
        ordering the queue is a sort, not new data. New surface area is mainly a
        ModeNav entry, the one-shot queue/termination logic, and the score screen.
      - **Shipped 2026-06-24** — `Test.svelte` (setup → run → report), a
        `buildTestQueue()` in `session.js`, an enabled ModeNav `test` entry, and
        an `App.svelte` branch. Resolved decisions: queue = `content.json`
        **definition/emission order** for the chosen dungeon (no SRS-due filter,
        no shuffle, no interleave — the blocked acquisition pass by intent);
        dungeon picked on Test's own setup screen via component-local `$state`
        (independent of Drill's `enabledDungeons`, role inherited from
        `store.settings.role`); **seeds the SRS** via `recordReview` +
        `gradeFromLatency` (intro framing); **score = raw correctness**
        (right-first-try / wrong / timed-out, no auto-grade leniency); cast bar +
        7s timeout-as-miss kept; weakest-spot peg = most-missed archetype.
        Route-interleave (trash-before-its-boss) **deferred** — trash segment
        names don't cleanly map to route step titles. Cast-bar `DURATION` lifted
        to `timing.js` so Drill and Test can't drift.

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
- [x] **Archetype re-classification — bosses (2026-06-25):** ran a per-boss
      second-opinion pass (`projects/mplus_memory/reclassify-workflow.js`): blind
      Sonnet re-tag with the Archetype column stripped + cast/effect merge
      detection, then an Opus tie-break, **multi-tag aware**. Fixed two systematic
      defects from the original pooled tagging: (1) cast + lingering zone/DoT
      *duplicate cards* — 15 merges folded into the cast card (e.g. Arcane Residue
      → Arcane Expulsion); (2) lexical misclassification, esp. `stack-up` absorbing
      personal stacking DoTs / soak-failure markers (collapsed 6 → 3 cards; the
      survivors are genuine converge-to-split). Hardened `mechanic-archetypes.md`
      with the cast+effect de-dup rule, the `stack-up` guard, and **Tagging rule 3**
      (a card may carry a primary + also-valid archetypes). `build-content.mjs`
      now parses `primary; secondary` cells and the quiz **grades any accepted slug
      correct**. 366 cards (was 380), 39 multi-tag.
- [x] **Archetype re-classification — trash (2026-06-25):** ran the proven boss
      workflow against the trash tables via a dedicated
      `reclassify-trash-workflow.js` (Extract → blind Sonnet Classify → Opus
      Adjudicate, multi-tag aware, now with a per-decision `confidence`). Scope:
      **204 trash rows across 8 dungeons**. Outcome: **41 primary re-tags · 21
      rows gained an also-valid secondary · 1 cast+effect merge** (Algeth'ar
      *Vicious Ambush* folded *Rift Breath*); 162 unchanged. Fixed the known
      defect (Magisters' *Arcane Volley* `stack-up` → `pulsing-aura`) and many
      more lexical misses (`spread-out` random-target hits → `raid-damage`/`flavor`,
      passive chip → `flavor`, etc.). All changes **applied directly**; the **19
      lowest-confidence** (1 merge + 1 low + 17 medium; 23 high omitted) are surfaced in
      `reclassify-trash-report.md` for spot-check (rest reviewable via git diff).
      Card count 366 → **365** (the merge); multi-tag 39 → **60**. Build coverage
      assertion passes (all 365 cards canonical).

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
- [x] **Per-boss one-line hint (2026-06-24):** every boss carries one short
      factual peg — its signature mechanic as a minimalistic fragment
      (`soak the refuel orbs`, `step into the silence zone`, `cover the pizza
      slices`). Resolved the open question: the field lives as an explicit
      `**Hint:** <peg>` line directly under each `### Boss <!-- enc:NNN -->`
      heading (structured markup, same principle as the enc marker — not scraped
      from intro prose). `build-content.mjs` `parseDungeon()` captures it into
      `boss.hint` and emits `cue.hint` on boss cards (trash → none).
      `DungeonFrame.svelte` shows it as a small muted/italic line under the caster
      name **only on reveal** (gated on `status`) so it can't leak the cue-phase
      classify answer. All 29 hints authored. Distinct from [[Mnemonic nicknames]]
      above: one factual mechanic-first hook per boss, not a cutesy alias per
      ability.
- [ ] Role expansion: enable healer + tank card sets behind the existing filter.
- [ ] Verify Xal'atath's Bargain affix rotation (open TODO in overview).
- [ ] Patch-watch: re-verify content if game state moves past 12.0.5.
- [ ] **Boss / trash scope filter for Drill + Test (2026-06-25):** let the learner
      restrict the quiz **and** Test to (a) bosses + boss abilities only, (b) trash
      only, or (c) both (default). Cards already carry `cue.casterKind`
      (`"boss"` | `"trash"`), so this is a session-builder predicate
      (`src/lib/session.js`) plus a control in `FilterSheet.svelte`, sitting
      alongside the existing role filter. Rationale: prepping a key, a player may
      want just boss kits (fewer, higher-stakes tells) or to grind trash separately.
- [ ] **Boss portraits crop in the frame (2026-06-25):** boss art is often cut off
      (heads/feet) for lack of vertical room. **Cause:** the source renders are
      **square** — raw `raw/bosses/*.jpg` are a uniform **600×600**, built to
      **480×480** webp (all 29) — but `DungeonFrame.svelte` shows them in a short,
      full-width **landscape band** (`height` 210px cue / 150px reveal) with
      `object-cover`, so a 1:1 image scaled to cover the width has its top+bottom
      cropped. We're in **portrait**, so there's vertical headroom to spend. Options,
      cheapest first: (1) tune `object-position` (e.g. keep ~25% from top) so the
      crop preserves the face — one-line CSS; (2) give the cue band a **taller
      portrait-ish height** (~300–340px) since portrait has the room; (3) the real
      fix — **regenerate the art at a portrait aspect** (≈2:3 / 3:4, framed on the
      boss's upper body) via `tools/wowkb/bossart.py` so `object-cover` crops far
      less; (4) `object-contain` on the hued field (letterbox — no crop, smaller
      boss). Recommend (1)+(2) as a quick win now and (3) as the durable fix. Dim
      review already done: uniform 600×600 square, so any non-square framing needs
      a re-crop/re-render, not just CSS.
- [ ] **Flag an entry as inaccurate (2026-06-25):** let the user mark a card as
      wrong/suspect from the drill reveal. **No API endpoints yet** → persist flags
      to `localStorage` (a versioned key alongside the SRS state) capturing card id,
      spell, dungeon/boss, timestamp, and an optional note. Add an **"Error report"
      screen** (a new entry in `ModeNav`) that lists flagged items read from
      localStorage for review/export back into the KB; clearing a flag removes it.
      Forward-compatible: when an endpoint exists, the same store slice can sync
      upstream. Surface: a small flag affordance on `RevealPanel` (Drill + Test), a
      store slice, and the report screen.
