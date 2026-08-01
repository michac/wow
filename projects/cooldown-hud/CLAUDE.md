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
- **`docs/virtual-cdm-plan.md`** — ✅ **built and flown**: the virtual CDM panel — the
  HUD draws its own icons for abilities Blizzard's Cooldown Manager does not track, so a
  spec's floor press stops being invisible (Destruction was blank for 31 % of a pull).
  Only the v0.32.36 **re-fly** is outstanding, and that needs a live session, not code.
- **`docs/roster-state-plan.md`** — **Phases 1 + 2 + 3 + 4 DONE (2026-07-31); ▶ Phase 6 is
  CURRENT; Phase 5 after it**: anchor State on the spec's declared **roster** (abilities + auras)
  rather than on the CDM database, plus the correctness fixes and the **fixture inventory** of
  CDM edges that had to come first. Written out of a client-correctness review of `State.lua`
  against `knowledge/addon-dev/cooldown-manager.md`.
  **Phase 1 shipped the inventory** — `addon/CDMProbe/tests/fixtures/cdm-cases.lua`, now 99
  declarative cases — where a `pinned-defect` case asserts the contract answer and FAILS ON
  PURPOSE, so the fix turns its own case red and flips the status in the same diff.
  **Phase 2 (v0.32.46) landed all ten correctness fixes** and cleared every pin. The
  headline: the DoT read now has a channel that
  **self-clears** (`item.auraDataUnit` + `item.PandemicIcon`), where before a whole pull
  produced 169 "refresh the DoT" cues and **zero** "apply it".
  **Phase 3 (v0.32.48) separated the keybind from the cue channel** — the DrawList gained a
  `keybinds[]` channel so `cues[]` means *decisions*, and the keybind now resolves down the
  **rung ladder** (3 → 4 → 5), which is what gives **Hellcaller its key hint** — ✅ **flown
  the same day**: `cd=164597 … (Wither) key=F drew=F`, 16 key hints against 2 cues. Corpus
  **0 `pinned-defect` / 21 `fixed`**.
  **Phase 4 shipped the roster coverage probe** — `Coverage.lua` + `/cdmp hud coverage`:
  does the CDM actually *track* every id the spec declares, or is the HUD silently blind to
  one? It is also the required replacement for `pulse.dropped`, which Phase 5 deletes. Its
  wholesale guard (an empty scan reports "the read refused", never "your roster is blind")
  is the load-bearing part; Crashing Chaos 417234, its one live instance, was **deleted**
  rather than covered — so the `blind` verdict is fixture-proven only. ⚠ The first flight
  then found `blind` was **crying wolf** (every instance was an ability the character does
  not have), so v0.32.54 fenced it on knownness — see §5.2.
  ✅ **Flown 2026-08-01** — one `/cdmp flight` pass discharged Phases 2, 3 and 4, the
  `ChargeGained` re-fly and the `C_AssistedCombat` rider. **§5.2 is the flight record.**
  ⏳ Two things remain and neither is a re-pull: the **v0.32.36 re-fly is BLOCKED** (the
  decision log carries no combat flag, so its `w:-` acceptance cannot be read — fix the log,
  then re-read the capture already on disk), and the `/cdmp rt states` visual card.
  `status.md` → *Owed: the v0.32.36 re-fly* has both.
  **§3.11, §4.2, §5.1 and §5.2 are the records of what actually changed**, including the deliberate
  deviations — read them before "fixing" any of those back, and read §3.1–§3.10 / §4.1
  before "fixing" anything a case pins.
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
  57-test branch oracle. ⚠ Of the three inputs once listed as *missing rather than merely
  secret*, **DoT presence + refresh is now solved** (roster-state-plan §3.10, v0.32.46 — the
  per-frame `auraDataUnit`/`PandemicIcon` verdict); **in-combat charges** and **target health**
  are still missing. `rotation.md` → *Implementation notes* and
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
