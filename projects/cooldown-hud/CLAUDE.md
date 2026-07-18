# Cooldown HUD — project root

A standalone companion app (NOT the KB): a spec-specific overlay that skins
Blizzard's built-in **Cooldown Manager** under Midnight 12.0. v1 target spec:
**Demonology Warlock**.

**Project notes & status live in `docs/` — read them before touching the code:**

- **`docs/spec.md`** — guiding spec: the vision + design language (non-technical
  *what & why*, how it should look/feel).
- **`docs/notes.md`** — technical findings: the Secret-Values capability map, the
  config/positioning architecture, the M1 build findings (§9), and provenance.
- **`docs/milestones.md`** — roadmap, milestone log, current status, and the
  open-questions / verify-in-game queue.

Section numbers (§0–§9) are shared across the three docs; each doc opens with a
"Doc map" legend saying which § lives where.

## Layout

- `docs/` — the split design docs (above). *(Was one `project-spec.md`; split
  2026-07-18.)*
- `addon/` — the **CDMProbe addon** (`michac/CDMProbe`), its **own git repo**,
  **gitignored** from this workspace. Has its own `CLAUDE.md` for the
  deploy/release workflow (a plain push does NOT reach the game — cut a release).
  This is the code source of truth.
- `prototype/` — HTML design prototypes (layout directions + the CRT visual-style
  exploration that drove the v1 aesthetic).
