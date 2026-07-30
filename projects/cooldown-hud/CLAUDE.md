# Cooldown HUD — project root

A standalone companion app (NOT the KB): a spec-specific overlay that skins
Blizzard's built-in **Cooldown Manager** under Midnight 12.0. v1 target spec:
**Demonology Warlock**.

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
  Diabolist, Hellcaller as a delta section). ⚠ **DRAFT / desk-derived** — distilled from
  the Tier-1 simc APL and game data, with **no live capture yet**: the tracked set is
  predicted, and three inputs (DoT uptime, charges, target health) are missing rather
  than merely secret. Read its status banners before treating anything as fact.

**Machine-readable contracts (source of truth — prose defers to these):**

- `guidance-contract.json` — the Stage-2 Guidance output contract.

**History — `docs/archive/`:** done/superseded plans — the whole W4 build sequence +
phase handoffs, the M-series plans, the frozen `milestones.md` log, and the retired
old-engine QA docs. **Nothing here is current**; read before re-proposing a dead end,
don't cite it as fact. See `docs/archive/README.md`.

## Layout

- `docs/` — the general design docs (above).
- `specs/<spec>/` — per-spec rotation brain + facts. `demonology/` (shipped) and
  `destruction/` (draft, docs only — no Coach spec table yet).
- `addon/` — the **CDMProbe addon** (`michac/CDMProbe`), its **own git repo**,
  **gitignored** from this workspace. Has its own `CLAUDE.md` for the
  deploy/release workflow (a plain push does NOT reach the game — cut a release).
  This is the code source of truth.
- `prototype/` — HTML design prototypes (layout directions + the CRT visual-style
  exploration that drove the v1 aesthetic).
