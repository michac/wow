# Cooldown HUD — project root

A standalone companion app (NOT the KB): a spec-specific overlay that skins
Blizzard's built-in **Cooldown Manager** under Midnight 12.0. v1 target spec:
**Demonology Warlock**.

**The W4 pipeline is LIVE** (`/cdmp hud` runs `State → Coach → Binder → Renderer`; the
old engine was deleted at the W4 cutover).

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
- **`docs/status.md`** — **THE live worklist.** Released version, the phase ledger, open
  items, and the **improvements/backlog** (the single place feature + quality work lands).
- **`docs/cdmp-doctrine.md`** — the collect-vs-assert rule `wowkb.cdmp` enforces
  (collect a new observation → addon release; assert / interpret / re-verify → local, no
  release).

**Per-spec — `specs/<spec>/`:**

- **`specs/demonology/rotation.md`** — the flat priority list (APL) the Coach implements.
  The rotation spec of record.
- **`specs/demonology/notes.md`** — Demonology facts: ability roster, the burst window
  (Tyrant + Dreadstalkers), Demonic Core proc, shard mechanics.
- **`specs/demonology/input-contract.md`**, **`observability-map.md`** — reference-only:
  the evaluator's inputs and what the game exposes vs. hides.

**Machine-readable contracts (source of truth — prose defers to these):**

- `guidance-contract.json` — the Stage-2 Guidance output contract.
- `probe-baseline.json` — the tested-assumptions-of-record (`wowkb.cdmp check`).

**History — `docs/archive/`:** done/superseded plans — the whole W4 build sequence +
phase handoffs, the M-series plans, the frozen `milestones.md` log, and the retired
old-engine QA docs. **Nothing here is current**; read before re-proposing a dead end,
don't cite it as fact. See `docs/archive/README.md`.

## Layout

- `docs/` — the general design docs (above).
- `specs/<spec>/` — per-spec rotation brain + facts. `demonology/` is the only one today.
- `addon/` — the **CDMProbe addon** (`michac/CDMProbe`), its **own git repo**,
  **gitignored** from this workspace. Has its own `CLAUDE.md` for the
  deploy/release workflow (a plain push does NOT reach the game — cut a release).
  This is the code source of truth.
- `prototype/` — HTML design prototypes (layout directions + the CRT visual-style
  exploration that drove the v1 aesthetic).
