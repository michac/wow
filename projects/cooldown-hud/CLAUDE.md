# Cooldown HUD — project root

A standalone companion app (NOT the KB): a spec-specific overlay that skins
Blizzard's built-in **Cooldown Manager** under Midnight 12.0. v1 target spec:
**Demonology Warlock**.

**The W4 pipeline is LIVE** (`/cdmp hud` runs `State → Coach → Binder → Renderer`; the
old engine was deleted at the W4 cutover). Two docs are the entry points:

- **`docs/architecture.md`** — **THE design doc.** How the HUD works today: the
  `State → Coach → Guidance → Binder → DrawList → Renderer` pipeline, the data-shape
  contracts, and the "Live wiring" section. Read it before touching the data/display seam.
- **`docs/status.md`** — **THE live worklist.** Released version, the phase ledger, open
  items, and the **improvements/backlog** (where feature + quality work lands now).

Supporting docs:

- **`docs/spec.md`** — guiding spec: the vision + design language (non-technical
  *what & why*, how it should look/feel).
- **`docs/guidance-model.md`** — the rotation-helper contract (§0.5): what to signal,
  when, and how. The §0.5 salience contract is still valid; its *implementation* is now
  the Coach/pipeline (not the retired M3–M6 HudScore/HudChrome widgets).
- **`docs/notes.md`** — technical findings: the Secret-Values capability map, the
  positioning/anchoring architecture, provenance.
- **`docs/notes-archive.md`** — superseded / parked work. **Nothing here is current** —
  each entry says why it's parked and what would revive it. Read before re-proposing a
  dead end; don't cite it as fact.
- **`docs/milestones.md`** — **historical** milestone log (froze at M4.4/v0.24.0, before
  the pipeline went live). Design/build provenance, not current status → see `status.md`.
- **`docs/m4.5-t3-plan.md`** — the collect-vs-assert doctrine `wowkb.cdmp` enforces
  (still current: collect → addon release; assert → local, no release).
- **`docs/archive/`** — done/superseded plans: the whole W4 build sequence + phase
  handoffs (`w4-build-plan.md`, `w4-phase2..7-*.md`), the M-series plans, the retired
  old-engine QA docs (`qa-pending.md`, `verify-runbook.md`), and
  `m4.5-playtest5-feedback.md`. See `docs/archive/README.md`.
- **`apl-prototype/`** — the rotation spec of record (`pseudocode.md`, the flat priority
  list the Coach implements) + reference-only input/observability maps (`apl.lua` retired).

Section numbers (§0–§9, plus §0.5) are shared across `spec.md`/`guidance-model.md`/
`notes.md`/`milestones.md`; each opens with a "Doc map" legend saying which § lives where.

## Layout

- `docs/` — the split design docs (above). *(Was one `project-spec.md`; split
  2026-07-18.)*
- `addon/` — the **CDMProbe addon** (`michac/CDMProbe`), its **own git repo**,
  **gitignored** from this workspace. Has its own `CLAUDE.md` for the
  deploy/release workflow (a plain push does NOT reach the game — cut a release).
  This is the code source of truth.
- `prototype/` — HTML design prototypes (layout directions + the CRT visual-style
  exploration that drove the v1 aesthetic).
