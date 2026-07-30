# Cooldown HUD — project root

A standalone companion app (NOT the KB): a spec-specific overlay that skins
Blizzard's built-in **Cooldown Manager** under Midnight 12.0. Registered specs:
**Demonology** (266, play-settled) and **Destruction** (267, shipped 2026-07-29,
awaiting its first live pass). Every other spec resolves passive by design.

**The W4 pipeline is LIVE** (`/cdmp hud` runs `State → Coach → Binder → Renderer`; the
old engine was deleted at the W4 cutover).

## Auto-deploy is OK for this project

Standing exception to the workspace-wide "cutting a release is ask-first" rule
(root `CLAUDE.md`), **scoped to the CDMProbe addon only**: when a change is ready
for me to eyeball/test in-game, **just cut it and deploy** — commit the feature
work, `wowkb.addon release cdmp --patch`, and tell me to `/reload`. No need to ask
first for a test build; iterating on the HUD *is* the loop. (This covers routine
test cuts; still flag anything genuinely irreversible or out-of-band.)

## Doc map

The docs split **general** (spec-agnostic — the product, the pipeline) from
**per-spec** (the rotation brain for one spec). Adding a 2nd spec is additive: a new
`specs/<spec>/` folder + a Coach spec table, with **no edits to the general docs**.

**General — `docs/`:**

- **`docs/design.md`** — the vision + design language (the non-technical *what & why*:
  what the product is, how it looks/feels, the enhance-don't-replace stance).
- **`docs/architecture.md`** — **THE technical design doc.** The
  `State → Coach → Guidance → Binder → Renderer` pipeline, the data-shape contracts, the
  invariants, and the Secret-Values reality the pipeline is shaped around. Read it before
  touching the data/display seam.
- **`docs/virtual-cdm-plan.md`** — the **current active plan**: the virtual CDM panel — the
  HUD draws its own icons for abilities Blizzard's Cooldown Manager does not track, so a
  spec's floor press stops being invisible (Destruction was blank for 31 % of a pull).
  `status.md`'s Active-work line points here.
- **`docs/field-fixes-plan.md`** — ✅ **done, history** (Phases A/B/C/C2, v0.32.28–31): the
  correctness + capability fixes the first live session surfaced, and the record of the live
  pass that confirmed them. Read it for the field evidence, not for outstanding work.
- **`docs/status.md`** — **THE live worklist.** Released version, the phase ledger, open
  items, and the **improvements/backlog** (the single place feature + quality work lands).
  **Routing — "plan / do the next cooldown-HUD thing" starts HERE:** read `status.md`
  first. If **Current state → Active work** names an item, *continue that* (it points at a
  plan doc + the current phase — pick up the next phase); if there is **no** Active-work
  line, pull the next item from **Improvements / backlog** and, once chosen, add an
  Active-work line for it. Only fall back to asking the user when both are empty/ambiguous.

**Per-spec — `specs/<spec>/`:**

- **`specs/demonology/rotation.md`** — the flat priority list (APL) the Coach implements.
  The rotation spec of record.
- **`specs/demonology/notes.md`** — Demonology facts: ability roster, the burst window
  (Tyrant + Dreadstalkers), Demonic Core proc, shard mechanics.
- **`specs/demonology/input-contract.md`**, **`observability-map.md`** — reference-only:
  the evaluator's inputs and what the game exposes vs. hides.
- **`specs/destruction/`** — the same four docs for **Destruction Warlock** (v1 profile
  Diabolist, Hellcaller as a delta section). **Shipped 2026-07-29** —
  `SpecDestruction.lua` + `CoachDestruction.lua` implement `rotation.md` L1–L13, with a
  57-test branch oracle. ⚠ Still **desk-derived**: the tracked set is DB2-predicted with
  **no live capture yet**, and three inputs (DoT refresh uptime, in-combat charges, target
  health) are missing rather than merely secret. `rotation.md` → *Implementation notes* and
  `docs/status.md` → *Open items* carry what the live pass has to settle.

**Machine-readable contracts (source of truth — prose defers to these):**

- `guidance-contract.json` — the Stage-2 Guidance output contract.

**History — `docs/archive/`:** done/superseded plans — the whole W4 build sequence +
phase handoffs, the M-series plans, the frozen `milestones.md` log, and the retired
old-engine QA docs. **Nothing here is current**; read before re-proposing a dead end,
don't cite it as fact. See `docs/archive/README.md`.

## Layout

- `docs/` — the general design docs (above).
- `specs/<spec>/` — per-spec rotation brain + facts. `demonology/` (shipped, play-settled)
  and `destruction/` (shipped, not yet flown). Adding a third is `docs/adding-a-spec.md`.
- `addon/` — the **CDMProbe addon** (`michac/CDMProbe`), its **own git repo**,
  **gitignored** from this workspace. Has its own `CLAUDE.md` for the
  deploy/release workflow (a plain push does NOT reach the game — cut a release).
  This is the code source of truth.
- `prototype/` — HTML design prototypes (layout directions + the CRT visual-style
  exploration that drove the v1 aesthetic).
