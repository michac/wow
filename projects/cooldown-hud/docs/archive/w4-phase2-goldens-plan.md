# Cooldown HUD — W4 Phase 2 golden corpus (workflow scope)

> **STATUS: PLAN, 2026-07-25.** Scopes the *corpus-first* half of W4 Phase 2 — author
> the independent `State → Guidance` golden library **before** growing the Coach, so the
> corpus can catch flaws in the reused HudBoard/HudScore logic (build-plan **P2**).
> Standalone plan doc; ticks back to `w4-build-plan.md` Phase 2 (steps 4–5).
>
> **Contract under test:** `guidance-contract.json` (v1, committed). Visual:
> the *Guidance v1* artifact — https://claude.ai/code/artifact/bc090a68-468d-41f5-aa5b-e21f20b2cf56

## Two decisions that shape this plan

- **Synthetic baseline (2026-07-25).** Fixtures are **synthetic State, templated on real
  captures** — not an in-game grind. The independence P2 needs is in the *expected
  Guidance* (derived from the rotation source), which is Coach-independent whether the
  State is real or synthetic. Phase 1 already extracted the realism rules, so we synthesize
  pulses that obey them and gate each through the **State-contract validator** (below). Real
  snapshots are optional fidelity padding, added later.
- **Single top press (2026-07-25).** A per-button golden asserts **exactly one** cue holds
  the "press now" emphasis (`ROTATION`, or `LATE` when overdue — never both) = the rotation
  source's **#1 ready ability**; all other ready abilities cap at `AVAILABLE`. `SOON` and the
  resource bar may coexist (not "press now" claims). This makes the Coach a **ranked
  winner**, and is **expected to trip the ⛔ decision gate** — `HudScore` scores each ability
  independently and has no priority order, so satisfying this corpus needs a new
  priority-resolution step, not a port. That is the corpus doing its job.

## Why corpus-first

Phase 2 is *grow the Coach* (step 4) + *test it against the corpus* (step 5). We invert
them: author the goldens while **no Coach output exists to peek at** — the strongest form
of P2 independence, and it hands the ⛔ gate its arbiter before the first line of scoring is
ported. The model authors the static library **once** (P2); it is never in the live loop.

## The oracle

Expected Guidance is reasoned from **(State fixture + a primary rotation source + the
contract)** — never the old engine, never synthesized salience docs. The source's **priority
ORDER is now load-bearing** (single-top-press), not just its ability list. Sources in trust
order: `wowkb.simc demonology` (APL) · `diabolist-sequences.md` · `rotation.md` · maxroll
(corroboration only).

**Old-code comments and `notes.md` are LORE, not fact.** Verify each against a real capture
or the source before it shapes a golden — never inherit. (Worked example: the "Shadow Bolt
isn't CDM-tracked, so `SB→Infernal Bolt` can't cue" claim in `SpecProcGlow`/`notes.md §2` was
**stale** — the captures show `spellID 686` is one of the 64 enumerated CDM entries, so IB is
cueable and is a positive scenario below, not a blind spot.)

---

## Pre-work — deterministic, no agents (author)

1. **State-contract validator** — the realism gate on synthetic State. Reuse the
   `statelog`-baseline invariants (`wowkb.cdmp`): secrecy discipline (no live read on a
   combat pulse; secret → napkin), identity coherence (`liveSpellID` = `overrideSpellID or
   spellID`), enum/domain validity, napkin honesty (expired estimate = `unknown`, never
   `ready`), the spec-agnostic denylist. A synthetic pulse that passes is **physically
   realizable**; one that fails is fiction and never enters the corpus.
2. **Golden validator** — asserts a `guidance.json` against `guidance-contract.json`: every
   token in-vocabulary, **no RGBA anywhere**, well-formed keys, pass-through strings only in
   sanctioned fields, the **secrecy gate** (no expected cue derives from a `readable:false`
   field — a combat cue must trace to napkin / `buff.isActive` / `glow`), and the
   **single-top-press invariant** (≤1 cue at ROTATION/LATE). Hard gate.
3. **Fixture templating** — each synthetic pulse starts from the nearest real capture in
   `corpus/statelog/` (OOC vs combat context) and mutates only the rotational fields
   (shards, `cd.state`/`changedAt`, `buff.isActive`, `glow`, `history`). Keep the structural
   scaffolding real (the 64-entry CDM anchor, categories, keybinds, identity fields).

## The scenario matrix — per-button spine + cross-cutting

Grounded in `addon/CDMProbe/SpecDemonology.lua` (`ns.Spec`). Three groups:

### A · Positive priority — the target button is the single press (`ROTATION`)

| scenario | condition (why it's #1) | asserts |
|---|---|---|
| tyrant-go | Tyrant ready · 5 shards · pets out | Tyrant `ROTATION` (the go); bar full; others `AVAILABLE` |
| dreadstalkers | Dreadstalkers ready, on-cd use | Dreadstalkers `ROTATION` |
| hand-of-guldan | shards available, gated spender (primary) | HoG `ROTATION` |
| demonbolt-proc | Demonic Core up (`buff.isActive`+`glow`), <4 shards | Demonbolt `ROTATION`; others down |
| shadow-bolt-filler | nothing else lit, in combat | Shadow Bolt `ROTATION` (filler) |
| ruination | Diabolic Ritual armed, HoG→Ruination transform | Ruination `ROTATION` on HoG's live id |
| infernal-bolt | Diabolic Ritual armed, SB→Infernal Bolt transform | Infernal Bolt `ROTATION` on SB's live id (now a 3-shard builder) |

> ✅ **Both transform halves are cueable.** Real captures confirm Shadow Bolt (`spellID 686`)
> is one of the 64 enumerated CDM entries, so `SB→Infernal Bolt` rides the SB frame exactly as
> `HoG→Ruination` rides HoG. (The old `SpecProcGlow`/`notes.md §2` "SB not tracked" claim was
> stale — verified against `corpus/statelog/`, not inherited.)

### B · Negative / must-not-instruct — the audit's greatest hits

| scenario | rule | asserts |
|---|---|---|
| implosion-cap | `judgeable=false` (imp count is secret) | Implosion caps `AVAILABLE`/`JUDGE` + secret-gate note; **never** ROTATION |
| grimoire-nocue | `SpecNoCue` (pane owns Grimoires) | Grimoire up → **no independent cue**; the pane speaks |
| overcap-soften | Core up but ≥4 shards (`softenAbove`) | Demonbolt softened, **not** a green press |

### C · Cross-cutting — emphasis edges & channels per-button doesn't reach

| scenario | covers |
|---|---|
| overdue-late | sat on Dreadstalkers N s → `LATE` (the overdue top press) |
| soon-anticipated | Tyrant napkin-anticipated, not yet ready → `SOON` + countdown (not a press) |
| opener-midflight | sequence pane: `stepState` done/active/pending/blocked; `SEQUENCE` on the step cue |
| resource-states | resourceBar at 0 / 3 / 5 shards, `incoming` from an in-flight HoG |
| transient-edges | `cast_started` → `cast_ended`; a `ready` edge; a `proc` edge |
| secrecy-combat | combat pulse: cds secret → napkin fills; proc via `buff.isActive`/`glow`, `aura` `readable:false` |

~6 positive + 3 negative + 6 cross-cutting ≈ **15 scenarios** (prunable). Coverage target:
every `emphasis` / `transient` / `stepState` member and every channel exercised ≥ once.

## The fan-out — `pipeline` over scenarios

**Stage A — DERIVE** (1 agent / scenario). In: synthetic fixture + primary source + contract.
Out (schema-forced): candidate `guidance.json` + `rationale` (per cue: the APL rank or
sequence step that justifies it, **and why the losers are demoted**) + a `readableOnly`
self-check. **Hard constraint:** reason only from State + source + contract; do **not** read
HudBoard / HudScore / SpecDemonology scoring (that contaminates the oracle).

**Stage B — VERIFY** (adversarial, 2 diverse lenses, per scenario as A lands):
- **Rotation-correctness** — refute the winner against the source: is this really the APL's
  #1 ready ability here, and are the others correctly *not* the call? Default to flagging.
- **Contract + secrecy conformance** — validate against the contract (incl. the
  single-top-press invariant), and check no cue leans on a `readable:false` fact.

A scenario clears when both lenses pass (or DERIVE revised). Disagreements surface as a
flagged note — never a silent drop.

**Stage C — SYNTHESIZE** (1 agent, barrier). Coverage check (every vocab member + channel +
OOC/combat/secret exercised?), emit `coverage.md` + a **gaps** list. No silent truncation.

## Post-work — deterministic (author)

4. Run both validators over every pair (the gates).
5. **Busted harness** `tests/spec/coach_golden_spec.lua` — loads each pair; once the Coach
   exists (step 4) runs `Coach.Compute(state)` and diffs. Until then, **shape-validate**
   mode (each golden validates against the contract) so the suite is green-meaningful now
   and flips to full-diff when the Coach lands — the TDD red is the diff assertions.

## Deliverables

- `corpus/goldens/<scenario>/{state.json, guidance.json, rationale.md}` — the frozen library
- `corpus/goldens/coverage.md` — synthesis report + gaps
- the two validators (in `tools/`)
- the busted harness (in the CDMProbe repo)

## Open implementation decisions (resolve in pre-work)

- **Harness fixture format + path.** Goldens live here (`corpus/goldens/`), but busted runs
  in the **separate, gitignored CDMProbe repo**. Decide: JSON + a decoder (`dkjson`) via a
  relative path, vs. a generator that emits Lua-table fixtures into the addon's `tests/`.
- **Validator home** — a `wowkb.cdmp goldens` subcommand vs. a small standalone `wowkb`
  module (leans toward reusing the cdmp reader/assert scaffolding).

## Size & sequencing

Synthetic fixtures mean **no in-game gate** — the whole thing is deterministic and runnable
now. Start with a **proof-of-shape**: hand-author 2–3 goldens (e.g. `hand-of-guldan`,
`demonbolt-proc`, `implosion-cap`) to lock the golden format, the single-top-press assertion,
and the harness fixture-path decision. Then fan out: ~15 scenarios × (1 DERIVE + 2 VERIFY) +
1 SYNTH ≈ **~46 agents** — well above the session's default 15-agent guideline and needing an
explicit Workflow opt-in. Trim (single lens / fewer scenarios) or raise the cap at that point.

**Recommended order:** proof-of-shape (3 goldens, by hand) → confirm format → fan out the rest.
