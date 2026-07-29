# W4 Phase 2 — the Coach: ⛔ gate verdict + redesign notes

*(Dated 2026-07-25. Records what the decision gate decided and why, so a later
reader doesn't re-litigate the "why not just port HudScore" question. Companions:
`w4-build-plan.md` §Phase-2 is the plan; `guidance-contract.json` the output shape;
`corpus/goldens/` the arbiter.)*

## Status

**Green — 23/23.** `ns.Coach.Compute(state) → Guidance` reproduces the frozen
23-scenario golden corpus. Verified by `busted CDMProbe/tests/spec/coach_golden_spec.lua`
(the ⛔ arbiter, `Coach.Compute` diffed against every `guidance.json`), plus
`coach_classify_spec.lua` (Classify in isolation). `luacheck CDMProbe/` clean; the
frozen corpus still validates `wowkb.cdmp goldens` 23/0 (the Coach matched the
goldens, the goldens were not moved to the Coach).

Scope was **pure Coach + green corpus** — the live HUD stays on HudState→HudScore→
HudBoard→HudChrome, **untouched**. Wiring (State.lua `mode`/`incoming` emission, a
Binder feeding HudChrome, a release, in-game QA) is the separate Phase-3–5 work.

## The ⛔ gate verdict: REDESIGN, not port

The gate (build-plan P1 / audit #3) asks: can the reused additive/per-ability
scoring be *tuned* to pass the independent corpus, or must the decision be
redesigned? **Verdict: redesign.** Two corpus scenarios are unreachable by a thin
ranker bolted onto the ported `HudScore.For` cascade:

- **`tyrant-ready`.** `HudScore` floors a napkin-*probably-up* hard-CD to `NEVER`
  (`cdReady` needs `ready == true`, `HudScore.lua:234-236,283`). So it blacks out
  Tyrant and greens HoG — the *wrong winner*, and a top-of-board ranker can't
  recover a candidate the scorer already zeroed. **Fix (Classify):** a hard-CD whose
  napkin estimate has *elapsed* (`cd.state=="unknown" & source=="napkin"`) is
  `napkinProbablyUp` = **ROTATION-eligible**, not NEVER.
- **`in-tyrant-window`.** `HudScore`'s context-prunes (`:353-482`) lower levels
  *per ability*, so both HoG and Demonbolt reach `ROTATION` — two presses — and
  "Tyrant window ⇒ HoG-spam" is nowhere encoded. **Fix (cascade):** phase resolution
  makes `TYRANT_WINDOW` its own branch where HoG *outranks* a Core dump (the inverse
  of steady state), producing one winner.

So the Coach is **two stages**: `Classify` REUSES the auditable readable sub-logic
(identity/override resolution, the napkin distillation, the armed-proc/transform
detector, the `reasons` contract) re-pointed at the State *pulse*; `Context +
RankWinner + Escalate + Emit` REPLACE the caps/prune/`rot` block with an explicit
priority cascade. The pruning knowledge isn't lost — it's re-expressed as cascade
*ordering* (e.g. HudScore's "Demonbolt overcaps above 4 shards" softenAbove guard is
now the cascade step `coreUp & shards < 4 → Demonbolt`, so at 4 shards HoG wins).

## Deviation from build-plan step 4 (recorded, deliberate)

Build-plan step 4 reads "**write the Coach by growing `HudBoard`**." We did **not** —
we built a **new `ns.Coach`** module and left `HudBoard`/`HudScore` running the live
HUD. Reason: honoring P1 (**build in isolation, integrate at the end — not
strangler-fig**). Growing HudBoard in place would have coupled the redesign to the
live cue path mid-flight; the gate wanted freedom to redesign the *decision*, not
port it, and a parallel module gives that freedom with the live HUD as a working
fallback until the Phase-5 cutover. `HudBoard`'s factory shape (`New(cfg)`/`__index`,
cfg-injectable cost fn) is mirrored, so the two share a pattern without sharing state.

## Rules that are genuine redesigns (not tunes)

Each is a cascade/phase decision with **no** HudScore analogue — flagged so a future
reader knows these are load-bearing, not incidental:

1. **Phase resolution** (`OPENER | TYRANT_WINDOW | TYRANT_ENTRY | TYRANT_STAGING |
   BURST_IMMINENT | STEADY`). The Tyrant↔Dreadstalkers priority *inverts* with phase
   (stage Dreadstalkers before the window vs. press Tyrant entering it), which is why
   there is **no static per-ability `rank`** field and **no `ns.Spec` schema change** —
   the order is context, read from existing bits.
2. **Napkin-probably-up ⇒ ROTATION-eligible** (Classify) — the direct fix for the
   `tyrant-ready`/`dreadstalkers`/`overdue-late` winners HudScore floored to NEVER.
3. **Single-press by construction** — `Emit` is a *separate* pass over the abilities
   the winner did **not** claim, so `SOON`/`JUDGE`/`SEQUENCE` can never be a press.
   This is the structural guarantee of the contract's single-top-press invariant,
   versus HudScore's per-ability levels that could green two calls at once.
4. **Readable-only LATE** — `Escalate` promotes ROTATION→LATE only from single-pulse
   readable overdue-ness: a probably-up summon elapsed past `LATE_LEAD`
   (`overdue-late`, via `cd.changedAt`), or HoG parked at a *full* bar
   (`hog-overcap-late`, via actual — not projected — shards). Secret buckets (Demonic
   Core stacks) can never go LATE (§0.5.8.2c). The live `candidateSince` clock is a
   Phase-3+ concern the goldens don't exercise (each is one pulse).
5. **Demonbolt JUDGE only on a fresh proc *edge*** (`glow.changedAt == at`) with a
   readable competitor — the press-vs-hold turns on the secret Core stack count, so
   inform (JUDGE), don't instruct. A *steady* proc (no edge) stays unlisted
   AVAILABLE. This is what separates `transient-edges` (Demonbolt JUDGE+proc) from
   `overcap-soften`/`in-tyrant-window` (Demonbolt silent).

## Readable proxies + tunables (where the synthetic corpus pinned a constant)

The goldens are single synthetic pulses, so a few live-only signals are approximated
from one pulse; the constants live at the top of `Coach.lua`:

- `SOON_LEAD 3.0` — napkin remaining under this draws the SOON anticipation cue.
- `STAGE_LEAD 5.0` / `BURST_LEAD 20.0` — Tyrant-anticipated thresholds that separate
  `TYRANT_STAGING` (press Dreadstalkers, `soon-anticipated`) from `BURST_IMMINENT`
  (hold it JUDGE, `burst-hold`) from `STEADY` (press it on CD, `overdue-late` at 31s).
- `LATE_LEAD 4.0`, `CAST_FRESH 1.0` (a `history.start` fresher than this is the
  `cast_started` edge — the razor that fires `transient-edges` @0.5s but not
  `soon-incoming` @1.1s), `IMP_WINDOW 6.0`, `OPENER_MAX 15.0`.
- **Opener vs. recurring-entry discriminator:** Tyrant `cd.source=="none"` (never
  cast this pull) ⇒ `OPENER`; `"napkin"` (been cast) ⇒ recurring `TYRANT_ENTRY`. This
  is what tells `opener-midflight` from `tyrant-ready`, both of which read
  "Dreadstalkers + a summon just cast, Tyrant is next."
- **HoG shard cost** is the one talent-dependent number; taken through `cfg.shardCost`
  (the live `ns.ShardCost` reader when wired) with a Demo fallback of 3 for the
  clientless golden harness.

Retuning any of these is a **local logic edit + `busted`** — no release (the collect
vs. assert rule: only *collecting a new observation* needs an addon release).

## The opener panel is authored in the Coach (a Demo detail)

`opener-midflight` is the only `sequence.show:true` golden. Its panel labels/shape
diverge from `ns.SpecOpener` (full spell-name labels, `count:2` HoG expanded to two
steps, the `SB/DB` step dropped), so the panel template is authored as pass-through
display data in `Coach.lua` (`OPENER_STEPS`) rather than forced back into `ns.Spec`
(no schema change). Keybinds and the drop-through cursor come from the pulse
(`state.cooldowns[].keybind` + `history`). A second sequence golden (a burst-branch
panel) would de-single-source the `SEQUENCE`/`stepState` coverage but is not required.
