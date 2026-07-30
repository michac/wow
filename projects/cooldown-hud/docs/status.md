# Cooldown HUD — status & worklist

**The live worklist.** Current state, what's done, and the improvement backlog. Vision +
design language live in `design.md`; the pipeline in `architecture.md`; the Secret-Values
reality in `notes.md`; the rotation in `specs/demonology/rotation.md`. Historical
milestone provenance is in `archive/milestones.md` (frozen log) and `docs/archive/`.

## Current state

- **Addon:** CDMProbe (`michac/CDMProbe`). The **W4-cutover release shipped** and the live
  build is in sync (multi-spec Phase 5 released as v0.32.22). Run `wowkb.addon list` for the
  live version — never hardcode it.
- **The HUD is the W4 pipeline.** `/cdmp hud` runs `State → Coach → Binder → Renderer`
  (see `architecture.md` → "Live wiring"). `/cdmp hud2` is a transitional alias. The old
  HudChrome/HudBoard/HudScore engine + the opener/burst/pane widgets were **deleted at
  the W4 cutover**; the pipeline is the sole engine.
- **Target spec:** Demonology Warlock. The domain view / fold + the flat priority list
  (`specs/demonology/rotation.md`) are spec-agnostic; the spec data lives in
  `SpecDemonology.lua`.
- **Instrument:** the **decision log** — `CDMProbeDB.decisionlog`, one `S{…} G{…} B{…}`
  line per pipeline decision change, extracted by `wowkb.cdmp decisionlog` (`hud2log` is a
  back-compat alias). The old-engine `statelog`/`pulls` recorders were retired at the
  cutover; the `/cdmp probe` + `probe-baseline.json` assertion suite was retired 2026-07-29
  (settled readability rules + DB2-sourced tracked set made per-spec re-measurement moot).
- **Gates:** `luaparser` (release) + `luacheck CDMProbe/` + `busted CDMProbe/tests/spec`
  (141 tests).
- **Active work:** none committed — **the multi-spec refactor is complete**
  (`multispec-plan.md`, all 6 phases done 2026-07-29, shipped v0.32.22). The framework is
  one spec-agnostic pipeline + a per-spec brain that plugs in: registry + resolver
  (`SpecRegistry.lua`), per-spec Coach brain (`CoachDemonology.lua`), array-of-powers
  resources (`resourceBars[]` + N stacked meters), the decision-log seam (`DecisionLog`),
  and live spec detection (login + `PLAYER_SPECIALIZATION_CHANGED`, registered-or-passive).
  Demo stays the sole registered/live spec; every other spec resolves passive by design.
  Phase 6 (docs) synced `architecture.md`/`notes.md`/addon `CLAUDE.md` to the code; the
  contract needed no edit. **⏳ One follow-up owed: the in-game Demo smoke on v0.32.22**
  (deferred — no game access at completion; the checklist is in `multispec-plan.md`'s
  Phase-6 row / Verification, and mirrors the "In-game verification of the pipeline output"
  open item below). Next: pull an item from **Improvements / backlog** when picking up work.

## Phase ledger (the W4 build)

| Phase | What | Status |
|---|---|---|
| 0 | Audit + baseline (dead-code strip W4a) | ✅ done |
| 1 | State — the reduced client picture (`State.lua`) | ✅ done |
| 2 | Coach → Guidance + the independent test corpus | ✅ done |
| 3 | Renderer (semantic tokens → pixels) | ✅ done |
| 4 | Binder (spellID cue → display cooldownID) | ✅ done |
| 5 | Live driver (`HudDriver`), flag-gated parallel run | ✅ done |
| 6 | TCT redesign (one-press cue walk; sequence panel retired) | ✅ done |
| 7 | 3-state CD model (`ready`/`on-cooldown`/`unknown`) | ✅ done |
| 8 | Ranked-winner guidance (winner + `ROTATION_FALLBACK` + `SOON`) | ✅ done |
| — | **Cutover & cleanup** — reclaim `/cdmp hud`, delete old engine + statelog, consolidate docs | ✅ done (released) |

## Open items (verify / close)

- **Release the W4 cutover** — ✅ **shipped.** The cutover build released and the live addon
  is in sync (`wowkb.addon list`): `/cdmp hud` is the default and draws (summon cues
  included), `/cdmp reset` clean, toggle off ⇒ Blizzard UI pixel-clean, migration folds a
  prior `hud2` flag into `hud`.
- **In-game verification of the pipeline output** — the domain-view re-layer and the
  ranked-winner guidance want an eyeball pass at a dummy + a read of the hud2 log.
- **`charge` half of the full-database read** — stays `@verify-ingame` until a charged
  spec is captured (Demo has no charged tracked ability). See `architecture.md` open Qs.

## Improvements / backlog

The container for what's next. The old engine is gone, so this is where feature/quality
work lands now — the user drives the list; a few already-surfaced items are seeded:

- **Proc-glow obscures our chrome — subdue or replace it.** ✅ **Shipped v0.32.17 (dim,
  not replace):** `HudProcGlow.lua` post-hooks each CDM item's `RefreshOverlayGlow` and
  sets `item.SpellActivationAlert:SetAlpha(0.5)` while the HUD is on (gated on
  `ns.HudOn()`; restored to full on toggle-off). Frame-level alpha multiplies the whole
  glow without fighting the proc animation. *In-game eyeball still owed:* confirm 0.5 is
  the right level (the `DIM` constant is a dial) — recolor+dim remains available if
  dim-alone isn't enough.
- **Main-choice vs backup-choice distinction is too subtle.** ✅ **Shipped v0.32.17
  (motion, not colour):** every cue now shows a solid circle **+ a spinning glow ring**;
  the winner (`ROTATION`) and softer cues spin+pulse, while the runner-up
  (`ROTATION_FALLBACK`) shows a **static** ring in ROTATION's green — so primary vs backup
  reads by *movement*, not a dim-vs-bright hue. Driven by `GLOW_SPEC` in the Renderer
  (`guidance-contract.json` is authoritative for the `emphasis` set); this was a
  Renderer treatment change, the Guidance already carries the two distinct tokens.
- **Imp napkin count** — a rough running **minimum** Wild-Imp count, in the napkin
  spirit (honest under the Secret-Values wall, where the real `Applications` stack is
  secret). Ingredients: seed an initial count OOC (readable there), then keep a running
  tally off `State.history` (the bounded cast window it already carries — start+succeeded,
  `architecture.md`): **+shards-spent** per Hand of Gul'dan, **−all** on Implosion,
  **−2** on Power Siphon, and **decay** each imp after its lifespan. ⚠ **Lifespan is a
  research sub-task** — the KB has the mechanics (imps are **energy-limited**: they cast
  Fel Firebolt until out of energy; Tyrant **extends every active demon ~15 s**; a
  passive summons one every 12 s) but **no clean seconds figure**; pin it (Wowhead /
  wago / an in-game test) before trusting the decay. Note `State.history` is a **bounded window**,
  so spanning a full imp lifetime likely needs a dedicated accumulator, not just the
  window. Explicitly a *minimum* (secret refunds/procs can only add imps we didn't count).
- **`abilities[base].uptime`** — surface a buff/DoT uptime off the TrackedBar duration in
  the domain view, so the Coach can reason about "keep this up" abilities.
- **Roll the domain view to other specs** — ✅ **framework complete** (`multispec-plan.md`,
  all 6 phases done 2026-07-29, shipped v0.32.22): registry + resolver + per-spec Coach
  brain + array-of-powers resources + live spec detection, Demo the sole registered spec.
  **What remains is a real 2nd spec** — a new `specs/<spec>/` doc set + a `Coach<Spec>.lua`
  brain + a `RegisterSpec` call. The recipe is `adding-a-spec.md`. Destruction is the
  candidate but wants a live in-game confirmation of its predicted tracked set (see the
  Destruction backlog item + `specs/destruction/`). ⏳ The framework's own in-game Demo
  smoke (v0.32.22) is still owed — see Active work above.
- **Warlock Destruction spec folder** — ✅ **docs authored** (2026-07-28):
  `specs/destruction/` carries the same four docs as `demonology/` (rotation · notes ·
  input-contract · observability-map), v1 profile **Diabolist** with a Hellcaller delta.
  All four are **DRAFT / desk-derived** — distilled from the Tier-1 simc APL +
  `wowkb.spec_inventory`, with **no live capture**. What it surfaced, and what is left:
  - **Fragments force a contract edit.** `resourceDisplay` has only `discrete` and
    `percentage`; Destruction is segments-**with**-partial-fill. The contract already
    invites the addition. Also: `State.lua`'s `UnitPower` call has no unmodified flag, so
    the fragment value is not read at all today — the rotation's shard gates are rounded
    conservatively until it is.
  - **`dot_refreshable` is the gating item, not a polish item.** Immolate/Wither
    maintenance is the spec's spine and it is blocked on `abilities[base].uptime`
    (below). Until that lands, the DoT line cannot fire honestly.
  - **Destruction closes the `charge` open item** — Conflagrate + Shadowburn are the
    project's first charged tracked abilities. Worth capturing early.
  - **Predicted-vs-live tracked set needs `/cdmp hud status` on a Destruction character.**
    Two specific things to check: **Incinerate appears untracked** (the floor press, and
    it would make the Infernal Bolt transform blind the way Shadow Bolt does for Demo),
    and the **Diabolist proc IDs differ from Demo's** — Destruction's residue names
    `433885`/`433891`, the pair `SpecDemonology.lua` labels "alt ID, unconfirmed".
  - **Still to do:** a `SpecDestruction.lua` Coach spec table, a `coach_apl_spec`-style
    branch oracle, and a live in-game confirmation of the predicted tracked set
    (`/cdmp hud status` / `hud layout` on a Destruction character).
- **Coach rotation logic** — any real rotation-quality tuning (the cutover was
  behaviour-preserving; the flat priority list is the place to iterate).
- **Layer-① curated Cooldown Layout override (deferred).** v1 ships no profile and binds
  by `GetCooldownID()` to the active layout (`design.md` pillar 1). If the DB2 defaults
  prove insufficient — the noisy Utility default, or the per-stage Diabolic Ritual auras a
  predictive Art tracker needs (only the `428514` container is tracked today) — this
  returns as a curated layout string, where enforcement strength (auto-apply →
  import-and-verify → nag) becomes the UX question. Binding-by-ID gives determinism
  without it, so it stays parked until a concrete need forces it.
