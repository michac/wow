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
- [ ] Lock the card-data shape: `{ cue, promptType, answer, archetypeRef,
      tags }` — defer to Phase 3 (engine); validate against this real content.

## Phase 3 — Engine (React shell, wired to Phase 1+2)

Single self-contained file. Build the rep loop end-to-end on real data.

- [ ] Scaffold single-file React app (`projects/mplus_memory/trainer.html` or
      equivalent).
- [ ] **Content layer:** load archetypes + dungeons + cards as plain data,
      separate from logic.
- [ ] **Engine layer:** SM-2 SRS scheduler.
- [ ] **Engine layer:** session builder — draws due cards through active
      filters; **interleaves dungeons** (don't block one at a time).
- [ ] **Engine layer:** grader (reveal → self-grade).
- [ ] **Persistence layer:** batch all scheduling state + settings into one
      `localStorage` object.
- [ ] **Drill mode:** stark cue→response screen; options at retrieval; motion
      only on correct/incorrect feedback.
- [ ] **Archetype mode:** learn the alphabet, made visual.
- [ ] **UI system:** dark default; consequence-tier semantic colors
      (🔴 wipe / 🟠 your death / 🔵 your job / ⚪ flavor); display vs body type.
- [ ] **Role filter:** wired in from the start (DPS now; healer/tank = filter
      flip later).
- [ ] Run through frontend-design guidelines so it doesn't read as a template.

## Phase 4 — Remaining modes

- [ ] **Route walk** mode — spatial; step through or drag pulls into order.
- [ ] **Dashboard** — mastery heatmap, solid vs shaky per dungeon (Leitner-style
      visual SRS).
- [ ] **Browse** — demoted plain reference.

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
