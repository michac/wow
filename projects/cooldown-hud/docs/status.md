# Cooldown HUD — status & worklist

**The live worklist.** Current state, what's done, and the improvement backlog. Design
lives in `architecture.md` (the single design doc); vision in `spec.md`; the rotation
salience contract in `guidance-model.md §0.5`. Historical milestone provenance is in
`milestones.md` (frozen log) and `docs/archive/`.

## Current state

- **Addon:** CDMProbe (`michac/CDMProbe`). Released **v0.32.8**; the **W4-cutover release
  is pending** (`wowkb.addon release cdmp --patch` → v0.32.9). Run `wowkb.addon list` for
  the live version — never hardcode it.
- **The HUD is the W4 pipeline.** `/cdmp hud` runs `State → Coach → Binder → Renderer`
  (see `architecture.md` → "Live wiring"). `/cdmp hud2` is a transitional alias. The old
  HudChrome/HudBoard/HudScore engine + the opener/burst/pane widgets were **deleted at
  the W4 cutover**; the pipeline is the sole engine.
- **Target spec:** Demonology Warlock. The domain view / fold + the flat priority list
  (`apl-prototype/pseudocode.md`) are spec-agnostic; the spec data lives in
  `SpecDemonology.lua`.
- **Instruments:** `/cdmp probe` (Secret-Value / override / cast-readability capture,
  asserted by `wowkb.cdmp check` vs `probe-baseline.json`) + the **hud2 decision log**
  (`CDMProbeDB.hud2log`, `wowkb.cdmp hud2log`). The old-engine `statelog` and `pulls`
  recorders were retired at the cutover.
- **Gates:** `luaparser` (release) + `luacheck CDMProbe/` + `busted CDMProbe/tests/spec`
  (126 tests) + `wowkb.cdmp check` (probe-only, 6 pass · 0 fail).

## Phase ledger (the W4 build)

| Phase | What | Status |
|---|---|---|
| 0 | Audit + baseline (`w4-hud-audit.md`, dead-code strip W4a) | ✅ done |
| 1 | State — the reduced client picture (`State.lua`) | ✅ done |
| 2 | Coach → Guidance + the independent test corpus | ✅ done |
| 3 | Renderer (semantic tokens → pixels) | ✅ done |
| 4 | Binder (spellID cue → display cooldownID) | ✅ done |
| 5 | Live driver (`HudDriver`), flag-gated parallel run | ✅ done |
| 6 | TCT redesign (one-press cue walk; sequence panel retired) | ✅ done |
| 7 | 3-state CD model (`ready`/`on-cooldown`/`unknown`) | ✅ done |
| 8 | Ranked-winner guidance (winner + `ROTATION_FALLBACK` + `SOON`) | ✅ done |
| — | **Cutover & cleanup** — reclaim `/cdmp hud`, delete old engine + statelog, consolidate docs | ✅ code done; release pending |

## Open items (verify / close)

- **Release the W4 cutover** — `wowkb.addon release cdmp --patch`, then in-game: `/cdmp
  hud` is the default and draws (summon cues included), `/cdmp reset` clean, toggle off ⇒
  Blizzard UI pixel-clean, migration folds a prior `hud2` flag into `hud`.
- **In-game verification of the pipeline output** — the domain-view re-layer and the
  ranked-winner guidance want an eyeball pass at a dummy + a read of the hud2 log.
- **`charge` half of the full-database read** — stays `@verify-ingame` until a charged
  spec is captured (Demo has no charged tracked ability). See `architecture.md` open Qs.

## Improvements / backlog

The container for what's next. The old engine is gone, so this is where feature/quality
work lands now — the user drives the list; a few already-surfaced items are seeded:

- **Proc-glow fidelity** — motion / layered-additive / soft sprite for the proc glow
  (from the recent Q&A on making the glow read better). Currently a flat treatment.
- **`abilities[base].uptime`** — surface a buff/DoT uptime off the TrackedBar duration in
  the domain view, so the Coach can reason about "keep this up" abilities.
- **Roll the domain view to other specs** — the fold + priority list are spec-agnostic;
  the spec data (`SpecDemonology.lua`) is the seam a 2nd spec plugs into.
- **Coach rotation logic** — any real rotation-quality tuning (the cutover was
  behaviour-preserving; the flat priority list is the place to iterate).
