# Cooldown HUD — W4 build plan (the sequence)

> **STATUS: PLAN, agreed 2026-07-24.** This is the *order of operations* for the W4
> refactor. It is the third leg of a trio, and owns only sequencing:
>
> - **`architecture.md`** — the target *shape* (State → Coach → Guidance → Binder →
>   DrawList → Renderer, and the four data contracts). *What we're building toward.*
> - **`w4-hud-audit.md`** — the *problem inventory* (A/B/C/D/E findings against
>   v0.28.1). *Why we're building it.*
> - **this doc** — the *build sequence*. *In what order, and how we know each layer
>   works before the next leans on it.*
>
> Standalone — NOT part of the §0–§9 doc set. When a phase lands, tick it here and
> annotate the matching audit findings.

---

## Guiding principles (these outrank the step order)

Three commitments constrain *how* every phase below is built. They came out of the
2026-07-24 planning pass and matter more than the exact sequencing.

### P1 — Bottom-up build, integrate at the end. NOT strangler-fig.

We build each layer against its contract **in isolation**, verify it, and wire the
whole pipeline together at the end. We do **not** slide new pieces in behind the live
HUD one seam at a time.

**Why strangler-fig is off the table here:** that pattern needs clean seams to hide
new components behind — and the *absence* of those seams is the exact defect this
rewrite exists to fix. There is nothing well-abstracted to attach to. (A1/A2 was a
one-off partial extraction that happened to fit behind `SetCue`; it does not
generalize to the rest, and we should stop treating it as a template.)

**Consequence, accepted:** final integration is a **real cutover** from the old HUD to
the new pipeline, not a gradual slide. Bottom-up is what makes that safe: by the time
we integrate, every layer has already been verified against a **frozen contract**
(the four data shapes are pinned in `architecture.md`), so integration is *wiring
known-good parts*, and the only genuinely-unproven thing at the end is the wiring
itself. That is the trade we're making with eyes open.

*(Note — running State in-game to capture logs (Phase 1) is **parallel observation**,
not a seam-swap: State reads and logs while the existing HUD renders, unchanged. That
is not strangler-fig.)*

**Willing to redesign, not just port (audit #3).** Bottom-up does not mean faithfully
re-homing the existing scoring. If the reused logic can't be dialed in to pass the
independent corpus, that's the signal to try a *different approach*. See the decision
gate in Phase 2 — we want to know when we're shuffling deck chairs on a sinking ship.

### P2 — The test oracle is independent of the code under test.

**The single most important rule in this plan.** Coach test cases are authored by
taking **captured real State** (Phase 1's output) and applying a **primary rotation
source** to it *directly* to decide the expected output — reasoning from
(State + source guide) to (expected Guidance), model-*assisted* but frozen as static
golden files.

They are **NOT** authored by:
- running the old engine and freezing its output (that enshrines its bugs), or
- reasoning from synthesized intermediate docs (e.g. a "ranked salience moments"
  list) whose claims we haven't traced to a primary source.

The whole point: we intend to **reuse** HudScore/HudBoard logic, so the corpus must be
able to **catch flaws in that reused logic**. A corpus derived from the code it tests
cannot do that. Independence is the property that makes the tests worth having.

**Primary rotation sources (the oracle's inputs), in trust order:**
- `wowkb.simc demonology` — the MID1 default APL (Tier 1, reproducible, pinned to a
  commit SHA). The reproducible source `rotation.md` distills.
- `knowledge/classes/warlock/demonology/diabolist-sequences.md` — re-verified against
  the live #1 Demo WCL parse (Inphected, bracket 291).
- `knowledge/classes/warlock/demonology/rotation.md` — the distilled priority.
- `maxroll-raid.md` / `maxroll-mplus.md` — verbatim captures, corroboration only.

**The model's role is bounded:** it assists in *authoring the static library once*
(reason from State+source to expected output; perturb a real capture into a new
scenario). It is **never** in the live test loop — the busted suite is deterministic
and reproducible, per the M4.5 T1/T2 discipline. A model call at test time would make
the suite flaky and non-reproducible; that is a hard no.

### P3 — Three layers, each understands only its input contract.

The output side is **three distinct components**, and none reaches past its own
contract. This separation *is* the rewrite; do not collapse two of them for
convenience.

1. **Coach → Guidance.** Emits cue metadata keyed to **conceptual items**
   (cooldownIDs). No UI elements, no geometry, no API. "Cue for cooldownID 42, this
   colour, this emphasis."
2. **Binder → DrawList.** A *separate* layer that augments the Guidance to bind each
   conceptual item to an **actual UI element** (which panel/frame to attach to) plus
   geometry. This is the only layer that consults the live CDM layout.
3. **Draw (Renderer) → pixels.** Fed a DrawList — "draw this cue relative to this
   UI-element id." **Never reaches into the API. Never sees a Guidance.** Owns the
   frame pool and the `handle → frame` registry, nothing else.

**Testing follows the contracts, and DrawList-level fixtures for the Draw layer are
correct — not a shortcut.** The Draw layer's real input *is* a DrawList, so the test
mode feeds it DrawLists directly (registering fake UI-element ids) to iterate on the
visuals. What would be wrong is making the Draw layer understand a Guidance, or
skipping the Binder as a layer — neither happens here. The Binder is unit-tested on
its own as a pure Guidance+Layout → DrawList transform (golden files, no pixels).

---

## Where today's modules land (so "write X" reads as "grow Y")

Almost nothing is a blank page — the pipeline is mostly a re-homing of existing pure
code plus the new seams between:

| Pipeline layer | Today's code | Move |
|---|---|---|
| **State** | `HudState.lua` (the de-facto State, but 1,254 lines that also score+paint — audit A4); `HudNapkin` (anticipation input); `HudBinds` (keybind input) | Extract the reduced-State shape; unify napkin+binds as State inputs; collapse the 3 event-ingest frames (audit A3) to one |
| **Coach → Guidance** | `HudScore` + **`HudBoard`** (A1/A2 — a pure, tested seed that already emits `cues`) | Grow HudBoard's output from `cues` to `resourceBar → sequence → effects`; resolve `colorKey` → RGBA |
| **Binder → DrawList** | none — `HudChrome` reaches into the live CDM layout itself | New component |
| **Draw (Renderer)** | `HudChrome` draw paths, `HudRow`, `HudQueue` (a display widget), `HudPane` | Re-home as pure DrawList → pixels + frame pool + handle registry |

The risky-new work: the **State/Coach seam + log**, the **Binder**, and the **handle
registry / effects clock** in the Renderer. The rest is consolidation.

---

## The sequence (bottom-up)

### Phase 0 — reusable seed exists (A1/A2, v0.28.1)

`HudBoard.lua` — a pure `Compute(ctx)` emitting per-key cue descriptors, 19 busted
tests. It is the **seed the Coach grows from**, not a live-integration step. ⚠ It
emits `colorKey` (a class token), so it does **not** yet meet Guidance invariant #5
(resolved RGBA) — Phase 2 fixes that.

### Phase 1 — State + the capture loop (the keystone)  *(your steps 1–3)*

1. **Write the State component** to the reduced shape in `architecture.md` Stage 1:
   keyed by cooldownID, secrecy first-class (every live fact is a value **or**
   `readable:false` + null, never a raw secret), power by real power-type, keybind,
   and `events` as the delta-since-last-pulse. **Spec-agnostic** — no rotation groups,
   no builder/spender.
2. **Capture a subset of State pulses via a NEW `/cdmp statelog` command — new format,
   reused infrastructure.** *Not* the probe report (a two-snapshot capability diagnostic
   — the wrong shape for a stream of pulses) and *not* `HudLog` (compressed scoring
   output, not full State). A dedicated command records selected pulses — chosen to
   cover diverse moments — as full State objects into a **separate `CDMProbeDB.statelog`
   store**. The "not new plumbing" that mattered is the *infrastructure*, and we reuse
   all of it: the `CDMProbeDB` SavedVariables file, the `/reload`-flush discipline, the
   `wowkb.cdmp` reader, and the baseline-assert pattern — teach `wowkb.cdmp` to read +
   assert a new **`statelog`** baseline section (no new SavedVariables file, no new
   reader tool, no new baseline machine, no new addon). Runs as **parallel observation**
   — the live HUD is untouched.
   - **What the `statelog` baseline asserts is a *fixture-quality gate*, not a rotation
     gate:** per-pulse State-contract invariants (secrecy discipline, identity
     coherence, enum/domain validity, napkin honesty, the spec-agnostic denylist) as
     PASS/FAIL, plus corpus **coverage** (OOC + combat, the secret/unreadable path
     actually fired, a napkin-sourced `cd`, a shard spread, a transform + a proc) as
     PASS/not-covered. It says *nothing* about which cue lights or whether the advice is
     right — that is Phase 2's oracle, and folding it in here would re-couple the two.
3. **Verify in-game:** capture real pulls, `wowkb.cdmp check` (now covering the
   `statelog` section). Triple duty — validates State, **answers an open question in
   `architecture.md`** (do non-displayed CDM entries return live `cd`/`charge` values,
   or only structural metadata? — write the verdict back into that doc), and **its
   output is the fixture corpus for Phase 2.**

**Exit:** a corpus of real captured State pulses on disk, asserted against a baseline,
covering OOC + combat + the secret/unreadable cases.

> **STATUS (2026-07-24): ✅ PHASE 1 COMPLETE — all three steps done, exit criterion met.**
> A real `/cdmp statelog` capture (CDMProbe **v0.29.6**, Demonology) passes all **12**
> `statelog` baseline checks — the 5 State-contract invariants and 7 coverage moments
> (OOC + combat, secret/unreadable cd, napkin cd, a 0→5 shard spread, transforms, a live
> proc, and cast history). `wowkb.cdmp check` is green. The captured pulses are on disk
> as the **Phase-2 Coach corpus**, and both `architecture.md` open questions about the
> full-database read are answered below.
>
> **The in-game capture loop drove real design discoveries** (v0.29.3–v0.29.6), all
> folded into `State.lua` + `architecture.md`:
> - **Combat auras are Secret Values** — `C_UnitAuras` is dark in combat. The readable
>   proc signals are the buff-tracking item's **`buff.isActive`** (direct) and
>   **`glow`** via `IsSpellOverlayed` (on the empowered spell); they cross-validated on
>   all 32 pulses. `aura` is now honest (`readable:false` in combat, not a false absent).
> - **Sequence memory** — State carries a bounded cast **`history`** (`start` +
>   `succeeded` phases) + per-cooldown `cd.changedAt` + `combatStartedAt`, so the Coach
>   can compute sequence position as a *pure function of a pulse* (Phase-2 testability).
> - **Step 1 ✅** `CDMProbe/State.lua` — the reduced Stage-1 shape: CDM-database
>   anchor (all categories, `allowUnlearned=true`), secrecy first-class, one identity
>   resolver (`liveSpellID`) + inverse (`BaseOfCast`), napkin + keybinds consulted
>   *through* State, one event-ingest frame (`events` = delta since pulse), a ~10 Hz
>   change-detecting poll. Spec-agnostic (no `SpecDemonology`). Coexists with `HudState`
>   as parallel observation — P1, not a seam-swap.
> - **Step 2 ✅** `/cdmp statelog` (+ `guide`/`clear`) writes a bounded ring of diverse
>   moments to `CDMProbeDB.statelog`; `wowkb.cdmp` grew a **`statelog` baseline block**
>   (12 checks: 5 per-pulse contract invariants → PASS/FAIL, 7 corpus-coverage →
>   PASS/not-covered). Validated off-game against synthetic clean+dirty fixtures; against
>   a real (probe-only) capture it reports the statelog section **not-covered**, cleanly.
>   luacheck + busted (52) green.
> - **Step 3 ✅ (in-game, iterated v0.29.2 → v0.29.6)** — real pulls captured →
>   `wowkb.cdmp check` green. Early captures surfaced and fixed collection bugs (proc
>   auras are `selfAura` not `hasAura`; the napkin/keybind inputs must be started by
>   State; `GetPlayerAuraBySpellID` takes **one** arg; transform events fire redundantly
>   so we dedup like Blizzard's own `SetOverrideSpell`) and the deeper findings above
>   (combat auras secret → buff-item/glow proc channels; sequence history). **Verdict
>   written into `architecture.md`:** the full-database `C_Spell` read returns live
>   `cd` VALUES for undisplayed AND unlearned entries OOC, and goes secret uniformly
>   in combat — no undisplayed-entry loophole either way.

### Phase 2 — Coach + the independent corpus  *(your steps 4–5)*

4. **Write the Coach by growing `HudBoard`:** widen its pure output from `cues` to
   `resourceBar` → `sequence` → `effects`, and resolve `colorKey` → RGBA so it emits a
   real presentation-generic Guidance keyed to conceptual cooldownIDs (closes the
   Phase-0 ⚠). No UI elements, no geometry — that's the Binder's job (P3).
5. **Unit-test it heavily against the independent corpus (P2):** for each captured
   State fixture, apply a primary rotation source directly to reason out the expected
   Guidance, model-assisted *once*, frozen as golden files. Diversify by perturbing
   real captures (5 shards / Tyrant down / mid-opener / Core proc'd), not by inventing
   State. **Oracle = source guide applied to State. Not the old engine. Not synthesized
   salience docs.**

> **⛔ Decision gate (P1 / audit #3).** If the reused additive/heuristic scoring
> **cannot be tuned** to pass the independent corpus, **stop tuning and redesign the
> scoring approach** rather than porting it. The corpus is the arbiter that tells
> deck-chairs from seaworthy.

**Exit:** the Coach emits a spec-agnostic Guidance that passes the independent
corpus; no class token (`colorKey`) escapes its output.

### Phase 3 — Draw layer + UI test mode  *(your steps 6–8)*

6. **Write the Draw (Renderer) component:** fed a DrawList ("draw this cue relative to
   this UI-element id"), it owns the frame pool + `handle → frame` registry and applies
   colour/fill/animation. **It never touches the API and never sees a Guidance** (P3).
7. **Write the UI test mode:** register N placeholder icon frames under fake
   UI-element ids, hand-author **DrawLists** against them (the Draw layer's real
   contract), and screenshot real pixels — no game, no dummy, no RNG, no CDM.
8. **Wire the test mode to Draw and iterate** on look/juice against the DrawList
   fixtures. ⚠ **Effects get their own sub-step + verification story:** the `effects`
   channel (one-shot animations + combat text) is *temporal* (the Renderer owns its
   clock, starts on a new `id`, ages out on ttl). A still screenshot can't see a 0.4s
   flash — decide how we verify effects (fired-id event log? staged multi-frame
   capture?) rather than folding it into "write draw."

**Exit:** any hand-authored DrawList renders to correct pixels, off-game, and the
visual language is dialed in.

### Phase 4 — Binder  *(your step 9)*

9. **Build the layer that translates cooldownID → UI element + details:** takes the
   Coach's conceptual, cooldownID-keyed Guidance and augments each entry with the
   actual panel/frame to attach to plus geometry (from the live CDM layout), emitting
   the DrawList the Draw layer consumes. Pure Guidance+Layout → DrawList — unit-tested
   on its own with golden files, no pixels needed.

**Exit:** a real Guidance from Phase 2 flows through the Binder into a DrawList that
Phase 3 draws correctly.

### Phase 5 — Integrate, then waffles  *(your steps 10–11)*

10. **Hook everything together:** State → Coach → Binder → Draw, live, replacing the
    old HUD. A real cutover (P1) — de-risked because every layer was verified against
    its frozen contract first, so this step is wiring, not discovery.
11. **Waffles.** 🧇

---

## How this maps back

- **Audit findings closed along the way:** A3/A4 (Phase 1 extraction), A1 completion +
  B1/B3/B4 identity/readiness kernel (Phase 2, as the Coach consumes resolved State),
  E1 hot-path strings (Phase 1–2 change-detection at the seams), B2/B5 (Draw/Binder
  re-home in Phases 3–4), D3 glow state/pixel split (Phase 3). C-series correctness
  items are orthogonal and can land any time; C1 (gradtest) stays client-gated.
- **Contracts:** all four data shapes are already specified in `architecture.md`
  (State, Guidance, Layout, DrawList) — lock to them; don't re-derive.
