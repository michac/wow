# Combat Assist Plus — backlog

**What this file is for:** the current implementation status and the ordered work list.
`spec.md` owns intended behavior; `notes.md` owns completed history; `discussion.md` owns only
questions that still require an author decision.

The live addon version comes from `wowkb.addon list`, never from prose here.

## Status

This is the project's only implementation-status source.

- The source has migrated to the approved small pilot: Tyrant and Demonbolt are the only
  enhanced entries; Dreadstalkers and Grimoire are readable Tyrant dependencies; unclaimed
  CDM rows need no silence declaration.
- The engine supports only the readable predicates the pilot uses, propagates unknown safely,
  draws a static border and two fixed context dots, leaves Blizzard's proc glow intact, and
  owns one independent Tyrant bar.
- Engine guarantees and provisional Demonology examples are separate test groups. The old
  tier/channel policy suite and its visual-taste assertions are gone.
- Simplification Phases 0–4 are complete. Phase 5's static baseline is built and mechanically
  tested but has not been judged in game. No release or deployment is implied.

## Now

### Phase 5 checkpoint — static baseline

- [ ] Install a test build only after separate release approval, then fly the questions in
      `flight-reading.md` → `Phase 5 checkpoint flight`.
- [ ] Judge brightness, contrast, size, stock-proc coexistence and whether both setup facts
      are identifiable and useful.

### Phase 3 — catalog and source migration (complete)

- [x] Replace the tier/band/cue ontology with the smallest contract needed for one emphasis,
      readable markers, optional sealed display bindings and one independent bar. §3.
- [x] Re-author Demonology around Demonbolt, Tyrant and the Tyrant bar only; remove every
      ability without a named pilot problem. §3.4.
- [x] Make readable-only Tyrant setup markers first-class. Keep sealed values out of every Lua
      branch. §3.2, §3.5.
- [x] Remove exhaustive silence coverage and treat unclaimed rows as optional diagnostics.
      §3.5.
- [x] Remove unused or unwired `talent`, `elapsed` and `casts` vocabulary plus automatic
      sequence preparation. §3.5, §4.
- [x] Admit no sealed display binding until one has a live renderer; no successful `nodraw`
      form.
      §3.2, §3.5.
- [x] Replace the four-bar roster with one independent Tyrant bar that does not inherit icon
      treatment. §3.3.
- [x] Update capture fields only where the smaller live model requires it; preserve the shared
      capture wire contract.

## Next

### Phase 4 — tests that say only what tests can know (complete)

- [x] Keep synthetic engine tests for readable branching, sealed-data isolation, unknown-safe
      evaluation, deterministic binding, supported displays and inert failure.
- [x] Move a few Demonology examples into an explicitly provisional characterization suite.
- [x] Delete tests for tier population, silence exhaustiveness, visual taste, automatic
      sequences and the removed vocabulary.
- [x] Keep the Python release runner invoking the suite; it enforces mechanics, not
      product prose.

### Phase 5 — static visual baseline

- [x] Draw one static emphasis and two fixed readable context markers as a flight hypothesis.
- [x] Remove default pulse behavior and unsupported flash-safety arithmetic.
- [x] Leave stock proc glow intact for the baseline and record that route explicitly.
- [ ] Ask for an in-game judgment of brightness, contrast, size and marker readability.

### Phase 6 — small Demonology pilot

- [ ] Fly Demonbolt emphasis across low and high readable shard states.
- [ ] Fly Tyrant base emphasis with separate Dreadstalkers and Grimoire context markers.
- [ ] Fly the independent Tyrant countdown bar and decide whether it earns its screen space.

### Phase 7 — qualitative iteration

- [ ] State one experience question per flight, record play first, then use captures to
      diagnose mechanism behavior.
- [ ] Change one conceptual variable at a time and ask at every product judgment.

### Phase 8 — close the migration

- [ ] Remove obsolete modules, fields, tests and vocabulary rather than retaining compatibility
      scaffolding for an unreleased design.
- [x] Reduce `flight-reading.md` to the fields and criteria the live source still emits.
- [x] Re-derive the Demonology catalog reference around the small pilot.
- [ ] Collapse migration history into `notes.md`, reconcile this status, and delete or archive
      the temporary plan and audit.

## Ideas

- A player-armed sequence-context experiment, only if it can inform a choice without becoming
  a current/next spell guide.
- A second spec chosen because it stresses the simplified design differently.
- Prior-art research after the pilot behavior is concrete enough to ask a narrow question.

## Done

- [x] Simplification Phase 1 — baseline, test classification, normative ledger and approved
      A1–G1 decision packet — 2026-08-11
- [x] First drawn-surface flight and time-weighted capture interpretation — 2026-08-10/11
- [x] Initial icon overlays, sealed markers, proc-glow attempt and cooldown bars — 2026-08-08/10
- [x] Pure catalog/tier/track core and first Demonology catalog — 2026-08-07
- [x] CDM binding, movable panel and standard capture foundation — 2026-08-05/06
- [x] Project scaffold and Cooldown HUD product boundary — 2026-08-05
