# docs/archive — spent milestone & phase working docs

Dated, **spent** working docs. Kept for design history, not as live plans — recover
anything here via `git log`/`git show`; nothing points to these as current. Live status
is `../status.md`; live design is `../architecture.md`.

## M4 milestone push (M4 → M4.5), archived 2026-07-24

- `m4-plan.md` — the M4 master plan (movable pane, prereqs, burst-window queue).
- `m4.1-plan.md` — M4.1 phased plan (A→B→C→D).
- `m4.4-plan.md` — the M4.4 HUD pass (5 workstreams A–E).
- `m4.4-feedback.md` — play-test-4 feedback that seeded M4.4.
- `m4.5-plan.md` — the M4.5 tooling track (luacheck / busted / selftest sketch).

## W4 refactor build + phase handoffs, archived 2026-07-28 (the cutover)

The whole W4 build sequence and its per-phase handoff notes — the pipeline they describe
shipped and is documented current in `../architecture.md`, so these are history.

- `w4-build-plan.md` — the phased Phase 0–5 build sequence + the three guiding principles.
- `w4-phase2-coach-notes.md`, `w4-phase2-scenarios.md`, `w4-phase2-goldens-plan.md` — the
  Coach + independent-corpus work (the golden corpus was later retired for the hud2 log).
- `w4-phase3-renderer-notes.md` — the Renderer build notes.
- `w4-phase4-binder-plan.md` — the Binder build plan.
- `w4-phase5-cutover-plan.md` — the cutover plan (its 5e is executed by the W4 cutover).
- `w4-phase6-tct-redesign.md` — the TCT (one-press cue walk) redesign; sequence panel retired.
- `w4-phase7-cd-state-model.md` — the 3-state CD model (`ready`/`on-cooldown`/`unknown`).

## Retired old-engine QA docs, archived 2026-07-28

Both were disposable QA docs for the old engine that the W4 cutover deleted.

- `qa-pending.md` — the old-engine in-game verification checkbox (never fully run before
  the pipeline superseded the code it verified).
- `verify-runbook.md` — the dated, self-labeled-disposable playable-session verify script.

## Play-test feedback

- `m4.5-playtest5-feedback.md` — play-test-5 feedback. §4.5.c carries the SetGradient /
  vertex-colour finding the cue paint path designs around (the `gradient-clobbers-vertex-
  colour` probe that read it was retired at the cutover; the finding is preserved here).

## Still live, deliberately NOT archived (one level up in `../`)

- `m4.5-t3-plan.md` — the **collect/assert** governing doctrine, cited by the root
  `CLAUDE.md`, `wowkb.cdmp`, and ClientLab. Load-bearing, not history.
