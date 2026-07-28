# W4 Phase 6 — the TCT redesign (burst + opener unified)

*(Dated 2026-07-27. A fresh-context handoff. Supersedes the phased 6a–6e burst plan in
`w4-phase5-cutover-plan.md` after in-game testing of v0.32.2. **Part 1 AND Part 2 are now
DONE on disk (uncommitted, off-game gate GREEN — busted 157/157, luacheck + luaparser clean,
`wowkb.cdmp check` exit 0).** The remaining step is the **live in-game verification + the
Part 1+2 release cut** (ask-first). A fresh agent picking this up should read this
top-to-bottom, then do the live verification and release.)*

---

## The overall task (context)

**Cooldown HUD** is a Demonology-Warlock overlay skinning Blizzard's Cooldown Manager
(Midnight 12.0). The **W4 refactor** rebuilt its guidance engine into a testable pipeline
`State → Coach → Guidance → Binder → DrawList → Renderer`, wired live behind `/cdmp hud2`.
The addon (`michac/CDMProbe`) is a **separate gitignored git root** at
`projects/cooldown-hud/addon/`; goldens/docs/tools live in the parent wow repo. Current live
version: run `wowkb.addon list` (last released **v0.32.2**).

**The Coach** (`Coach.lua`) is a pure `Compute(state) → Guidance` ranked cascade, arbitrated
off-game against `corpus/goldens/*` (each = a hand-authored `state.json` + oracle
`guidance.json`, reasoned from `knowledge/classes/warlock/demonology/{rotation,
diabolist-sequences}.md`, never from code). `busted CDMProbe/tests/spec` runs the gate.

**Why this redesign:** in-game testing of v0.32.2 (phases 6a–6c) surfaced two bugs:
1. **HoG mid-cast didn't clear** — 6b projected only the *builder* direction (in-flight Shadow
   Bolt could promote HoG); an in-flight **spender** (HoG) didn't subtract, so the overlay kept
   saying "HoG" while you were already casting it.
2. **Opener was wrong** — out of combat at 3 shards it prompted HoG. `OPENER` was gated on
   *in combat AND past Dreadstalkers*, so pre-pull fell through to steady and dumped HoG.

The user's fix (agreed) is a simpler, unified model — see below.

---

## The model (target — fully specified)

### Tyrant Condition (TCT)
```
TCT = Tyrant off cooldown (napkin probably-up OR never cast)  OR  napkin remaining <= 3s
```
One condition. Replaced the old OPENER / TYRANT_ENTRY / TYRANT_STAGING / BURST_IMMINENT
phases. When TCT is true, Tyrant shows a bare **SOON** anchor the whole time (until it's the
press).

### Phase select (`Coach:Context`)
```
OOC_IDLE      : not in combat AND no cast committed (anyCastFresh) -> the dumb SB+DB display.
                Ends on the cast-START edge, so Coach kicks in on the cast, not the land;
                pre-pull Tyrant is off cd (source "none") => TCT => the walk.
TYRANT_WINDOW : Tyrant buff active -> flood HoG.
BURST         : TCT true -> cap -> demons -> Summon Tyrant -> flood.
STEADY        : else -> the resource cascade.
```

### OOC-idle display (deliberate single-top-press EXCEPTION)
Light **Shadow Bolt + Demonbolt both as ROTATION**, no calculation — the pre-pull "here are
your two openers."

### The BURST walk (`RankWinner`), one press at a time, on PROJECTED shards
1. **projected < cap** → cap shards: **Demonbolt if a Core's up** (dumps it AND refunds +2),
   else **Shadow Bolt**.
2. **capped, Dreadstalkers up & not committed** → **Call Dreadstalkers**.
3. **Dreadstalkers committed, Grimoire up & not committed** → **Grimoire: Imp Lord**.
   Steps 2–3 advance on the cast-START edge (`committedWithin`).
4. **demons committed/unavailable, Tyrant off cd** → **Summon Tyrant**.
5. else (Tyrant not up yet) → fall through to steady → **HoG** (lay imps for Tyrant).

### Projected shards ("after current cast")
Every shard read is `projected = value + signed incoming`. **Signed** incoming: an in-flight
builder is `+`, an in-flight **spender** (HoG) is `−3`. The **Coach already ranks on
projected** — the missing half is `State.lua` emitting the signed number (Part 2).

### Retired
- **OPENER phase + the sequence panel** (6e = drop). `Sequence()` returns `show:false`;
  `OPENER_STEPS` deleted. 5e later deletes `HudPane`/`HudOpener`/`HudBurst`.
- **BURST_IMMINENT** (the 20s "hold for the window" JUDGE band).

---

## Part 1 — DONE (on disk, uncommitted, off-game gate GREEN)

**Gate:** `luacheck CDMProbe/` clean · `busted CDMProbe/tests/spec` **148/148** · luaparser OK.

**`Coach.lua` changes:**
- Tunables: `TCT_LEAD = 3.0` (replaced STAGE_LEAD/POOL_UNTIL/BURST_LEAD/OPENER_MAX).
- New helper `anyCastFresh(state)` (any 'start' within CAST_FRESH → ends OOC-idle).
- `Context`: `ctx.tct`; `ctx.tyrantProbablyUp` now true for **never-cast Tyrant**
  (`cdSource == "none"`), so the pull bursts; phase select rewritten to the 4 phases above;
  removed `openerActive`/`tyrantImminent`/`boardFresh`.
- `RankWinner`: `OOC_IDLE` returns nil; `BURST` walk (cap→demons→summon, projected shards);
  steady's "Tyrant far" is now `not ctx.tct`; **projected used throughout** (window HoG, Core
  dump <4, Infernal Bolt overcap, HoG press).
- `Escalate`: HoG-at-full-bar LATE **suppressed during burst/window** (a full bar there is
  intentional pooling, not overcap).
- `Emit`: `OOC_IDLE` lights SB+DB then returns; Tyrant SOON gated on `ctx.tct`; dropped the
  panel SEQUENCE emit and the BURST_IMMINENT Dreadstalkers JUDGE; Implosion JUDGE note fixed.
- `Sequence`: stub returning `{show=false}`.

**Goldens (parent repo `corpus/goldens/`):**
- NEW: `opener-ooc` (idle → SB+DB), `opener-ooc-casting` (SB committed → walk kicks in, cap),
  `tyrant-hog-spam` (TCT, demons down, shards → HoG).
- RE-POINTED: `soon-anticipated` (4 shards ~2s → cap/Shadow Bolt), `burst-hold` (15s = not
  TCT → steady overdue-Dreadstalkers LATE + Implosion JUDGE), `opener-midflight` (never-cast
  Tyrant, demons done, 3 shards → cap/Shadow Bolt; **panel dropped**), `tyrant-pool` /
  `tyrant-stage-dread` (Tyrant → off-cd so they're TCT).
- Verified green unchanged: `secrecy-combat`, `tyrant-ready`, `tyrant-stage-grimoire`,
  `in-tyrant-window`, and the steady corpus.
- `coach_golden_spec.lua` SCENARIOS = 29; **rendertest fixtures** (`Renderer.lua`
  `burst-hold`/`opener-midflight`) + `binder_spec.lua` HANDLE_MAP + `coverage.md` updated.

**Files touched (Part 1):** addon — `Coach.lua`, `Renderer.lua`, `tests/spec/binder_spec.lua`,
`tests/spec/coach_golden_spec.lua`. Parent — `corpus/goldens/{opener-ooc,opener-ooc-casting,
tyrant-hog-spam}/*`, re-pointed goldens, `corpus/goldens/coverage.md`, this doc.

**What Part 1 fixes live:** the opener (OOC SB+DB, cast-start kick-in, pull bursts) and the
whole Tyrant burst walk. **What it does NOT fix:** the HoG-mid-cast-clear (needs Part 2).

---

## Part 2 — DONE: `State.lua` signed `incoming` (the live half)

**Done on disk (uncommitted), 2026-07-27.** All five steps landed; off-game gate green
(busted 157/157, luacheck + luaparser clean, `wowkb.cdmp check` exit 0). What shipped:

- **`ns.SpecShardDelta(base)`** (`SpecDemonology.lua`, beside `SpecGhost`) — the injected
  **signed** reader: `(generates or 0) − (live ns.ShardCost iff spends=="shards")`. SB +1,
  Demonbolt +2 (uncosted — spends a Core), Infernal Bolt +3, Ruination 0, **HoG −cost**;
  unreadable cost drops the spend term (safe direction). Locked by `tests/spec/specdelta_spec.lua` (8 tests).
- **`inflightIncoming(now, liveShards)`** (`State.lua`) now sums the **signed** delta (drops the
  old `g > 0` builder-only filter) and applies a **double-deduction guard**: `spendStartShards`
  snapshots the shard `value` at each spender's `UNIT_SPELLCAST_START`; the −delta applies only
  while live `value` hasn't dropped below the snapshot (covers the completion-frame race).
- **Terminal cast phases** — registered `UNIT_SPELLCAST_INTERRUPTED / _FAILED / _FAILED_QUIET /
  _STOP`; each pushes a `"stopped"` phase that supersedes the `"start"` so a cancelled HoG stops
  projecting −3 (and clears its snapshot).
- **Golden `hog-inflight`** (combat, steady, value 3 / incoming −3 → Shadow Bolt ROTATION, HoG
  unlit) — added to `SCENARIOS` (→30) + `coverage.md` (negative-incoming sign now covered, 3/3).
  Passes against the current Coach (it already ranks on projected).
- **State contract** — added `statelog-coverage-incoming-negative` to `probe-baseline.json` +
  its checker in `wowkb.cdmp` (assert-only, no release). Reports **not-covered** until a live
  capture with an in-flight HoG lands (the old capture predates signed incoming).

**Original goal (kept for reference):** make `power.SoulShards.incoming` **signed** so an
in-flight **HoG** projects **−3**, and the Coach (already ranking on projected) clears HoG to
Shadow Bolt while you cast it.

**Where it lives:** `State.lua` `inflightIncoming(now)` (~line 550) currently sums
`ns.SpecGhost(id)` for in-flight 'start's and **only counts `g > 0`** (builder-only, by
design — see its header comment). `ns.SpecGhost(base)` returns the spec's `generates` (Shadow
Bolt +1, Demonbolt +2, Infernal Bolt +3); it does **not** encode the spend cost. HoG has
`spends="shards"` (cost 3, talent-dependent via `ns.ShardCost`/`hogCost`) and no `generates`.

**Steps:**

1. **A signed per-cast delta.** Add an injected reader (keep State spec-agnostic — same seam
   as SpecGhost): net shard delta = `(generates or 0) − (shard cost if spends=="shards" else
   0)`. Cleanest: a new `ns.SpecShardDelta(base)` from `SpecDemonology.lua` (it knows
   `spends`) combined with the live cost, returning **signed** (SB +1, HoG −3, Infernal Bolt
   +3, Demonbolt +2). Then drop the `g > 0` filter in `inflightIncoming` and sum the signed
   delta for every in-flight 'start'.

2. **Double-deduction guard (the subtle part).** HoG's shards are consumed on **completion**,
   not cast-start (that's WHY the overlay currently doesn't clear — during flight `value`
   still reads 3). So while HoG is in flight, `projected = 3 + (−3) = 0` → Coach shows Shadow
   Bolt. ✅ But at the completion frame `value` drops to 0 *and* the 'start' may briefly still
   be in the flight window before 'succeeded' is recorded → a 1-frame `0 + (−3) = −3`.
   **Guard:** snapshot the shard `value` at each spender's `UNIT_SPELLCAST_START`; in
   `inflightIncoming`, only apply the spend's negative delta while the live `value` has **not
   dropped below** that snapshot (i.e. the deduction hasn't landed). The old HUD used exactly
   this "atStart snapshot" pattern. (Builders need no guard — they credit, never over-credit.)

3. **Clear on interrupt / stop.** Only `UNIT_SPELLCAST_START` + `_SUCCEEDED` are registered
   (`State.lua` ~848). A **cancelled** HoG leaves a 'start' with no 'succeeded' for up to
   `INFLIGHT_WINDOW` (3s) → wrongly projects −3 for 3s. Register
   `UNIT_SPELLCAST_INTERRUPTED`, `UNIT_SPELLCAST_FAILED` (`_QUIET`), `UNIT_SPELLCAST_STOP` and
   `pushCast` a terminal phase (e.g. `"stopped"`) that supersedes the 'start' so
   `inflightIncoming`'s latest-phase-per-base check stops counting it. (Note: `STOP` fires
   after `SUCCEEDED` on a normal cast too — that's fine, it just confirms the clear.)

4. **Golden (Coach contract pin — passes immediately).** Add `hog-inflight`: combat, steady
   (Tyrant far), `value 3`, `incoming −3`, projected 0, no Core → **Shadow Bolt ROTATION**,
   HoG **not** lit (it's the cast in flight). This passes against the *current* Coach (it
   already ranks on projected) — it documents the contract and closes the **negative incoming
   sign** gap in `coverage.md`. Add it to `SCENARIOS` (→ 30) and update coverage.md's incoming
   table (negative row → `hog-inflight`).

5. **State contract (`wowkb.cdmp` / `probe-baseline.json`).** The signed incoming is a new
   observation. Update the `statelog-coverage-incoming` check / add a "negative incoming
   observed" assertion in `projects/cooldown-hud/probe-baseline.json` so a live capture with
   an in-flight HoG asserts the negative projection. (`collect` = addon change → release;
   `assert` = local JSON, no release — governing rule `docs/m4.5-t3-plan.md`.)

**Verification:**
- Off-game: `busted CDMProbe/tests/spec` (add `hog-inflight`) + `luacheck` + luaparser.
- Live (`/cdmp hud2` on a dummy): start casting HoG at 3 shards → the cue **clears to Shadow
  Bolt mid-cast** (not on land); cancel a HoG → it snaps back to HoG (no lingering −3).
  `cd tools && uv run python -m wowkb.cdmp check` for the signed-incoming assertion.
- **Release Part 1 + Part 2 together:** commit the addon feature work, then
  `wowkb.addon release cdmp --patch` (bumps .toc, luacheck, push, GitHub release,
  ghaddons-deploy). A plain push does not reach the game.

---

## Fresh-start checklist

1. `wowkb.addon pull --all` (the addon is a separate gitignored repo).
2. `cd projects/cooldown-hud/addon && export PATH="$HOME/.luarocks/bin:$PATH"` →
   `luacheck CDMProbe/` + `busted CDMProbe/tests/spec` — **confirm 157/157 green** (Part 1 **and
   Part 2** are already on disk; the tree is dirty — that's expected, both are uncommitted).
3. Read this doc top-to-bottom. Coach + State are done — the only remaining work is the **live
   in-game verification** (below) and the **release cut** (ask-first).
4. Live-verify on a dummy (`/cdmp hud2`: cast HoG at 3 shards → cue clears to Shadow Bolt
   mid-cast, not on land; cancel a HoG → snaps back, no lingering −3; `/cdmp probe` +
   `/reload` then `wowkb.cdmp check` should flip `statelog-coverage-incoming-negative` to PASS),
   then release Part 1+2 together: `wowkb.addon release cdmp --patch`.

## State of the tree at handoff

- **Part 1 AND Part 2 are uncommitted** in both repos.
  - Addon (`CDMProbe`): `Coach.lua`, `Renderer.lua`, `State.lua`, `SpecDemonology.lua`,
    `tests/spec/{binder_spec,coach_golden_spec,specdelta_spec}.lua`.
  - Parent (wow repo): the goldens (incl. new `corpus/goldens/hog-inflight/`) + `coverage.md`,
    `probe-baseline.json`, `tools/wowkb/cdmp.py`, this doc.
  - Normal resting state per the repo doctrine. The release flow commits the addon feature work
    as part of the cut; the parent-repo files commit whenever the wow repo is next pushed.
- Last **released** addon version: v0.32.2 (phases 6a–6c). Part 1+2 will be the next cut.
