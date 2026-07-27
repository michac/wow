# Cooldown HUD — project root

A standalone companion app (NOT the KB): a spec-specific overlay that skins
Blizzard's built-in **Cooldown Manager** under Midnight 12.0. v1 target spec:
**Demonology Warlock**.

**Project notes & status live in `docs/` — read them before touching the code:**

- **`docs/spec.md`** — guiding spec: the vision + design language (non-technical
  *what & why*, how it should look/feel).
- **`docs/guidance-model.md`** — the rotation-helper contract (§0.5): what to
  signal, when, and how — the builder/spender mode model, ranked salience moments,
  attention-mechanism research, and the moment→readable-signal map M3–M6 implement.
- **`docs/notes.md`** — technical findings, **current framing only**: the
  Secret-Values capability map, the positioning/anchoring architecture, the M1
  build findings (§9), and provenance.
- **`docs/notes-archive.md`** — superseded / parked work, split out of `notes.md`
  2026-07-20. The green-phosphor icon-tint era, the curated-layout machinery we
  proved and chose not to ship (M7 revival), and the assumptions we got wrong.
  **Nothing here is current** — each entry says why it's parked and what would
  revive it. Don't cite it as fact; do read it before re-proposing a dead end.
- **`docs/milestones.md`** — roadmap, milestone log, current status, and the
  open-questions / verify-in-game queue.
- **`docs/verify-runbook.md`** — *(disposable, dated)* the §7.3–§7.6 verify
  checklists re-ordered into **one playable session** with exact commands and
  expected output. Read it while logged in.
- **`docs/qa-pending.md`** — the **checkbox of record** for in-game verification of
  already-shipped code. **QA / clean-up, not roadmap blockers** — M4+ doesn't wait on
  them. (`verify-runbook.md` is the *how*; this is the *what + why + checkbox*;
  `milestones.md` keeps the design history.)
- **`docs/architecture.md`** — *(target-state design, agreed 2026-07-24)* the
  **State → Engine → ViewModel → Binder → DrawList → Renderer** pipeline the **W4**
  refactor builds toward, with the four data-shape contracts (the two hand-authorable
  fixture formats are the W4c test-mode payoff). **Standalone** — NOT part of the
  §0–§9 set. Read it before touching the data/display seam; `todo/w4-hud-audit.md` is
  the live worklist that executes it.
- **`docs/w4-build-plan.md`** — *(build sequence, agreed 2026-07-24)* the **order of
  operations** for the W4 refactor: the trio's third leg (`architecture.md` = target
  shape, `w4-hud-audit.md` = problem inventory, this = the phased sequence + how each
  stage is verified before the next leans on it). Owns three guiding principles that
  outrank the step order — **bottom-up build, integrate at the end** (NOT strangler-fig:
  the seams don't exist yet; willing to redesign the engine, not just port), an
  **independent test oracle** (primary rotation source applied to captured State, never
  the old engine), and **three-layer separation** (Engine → ViewModel keyed to concepts;
  a separate Binder → DrawList bound to UI elements; Draw → pixels, never the API).

Section numbers (§0–§9, plus §0.5) are shared across the four docs; each doc opens
with a "Doc map" legend saying which § lives where.

## Layout

- `docs/` — the split design docs (above). *(Was one `project-spec.md`; split
  2026-07-18.)*
- `addon/` — the **CDMProbe addon** (`michac/CDMProbe`), its **own git repo**,
  **gitignored** from this workspace. Has its own `CLAUDE.md` for the
  deploy/release workflow (a plain push does NOT reach the game — cut a release).
  This is the code source of truth.
- `prototype/` — HTML design prototypes (layout directions + the CRT visual-style
  exploration that drove the v1 aesthetic).
