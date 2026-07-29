# W4 Phase 5 — the Cutover: run the pipeline live, retire the old engine

*(Dated 2026-07-26. A fresh-context handoff, like `w4-phase4-binder-plan.md` before
it: the overall task, everything built through Phase 4, and the plan for the last
unit — wiring `State → Coach → Binder → Renderer` into the live HUD and deleting the
old engine. Companions: `w4-build-plan.md` = the phased sequence this executes (this
is its Phase 5, "Integrate, then waffles"); `architecture.md` = the target pipeline +
the four data contracts; `w4-phase4-binder-plan.md` = the Binder that just landed;
`todo/w4-hud-audit.md` = the live worklist.)*

---

## The overall task

Cooldown HUD is a spec-specific overlay (v1 = **Demonology Warlock**) that skins
Blizzard's built-in Cooldown Manager under Midnight 12.0. The **W4 refactor** rebuilds
its data/display seam into a clean, testable pipeline:

```
State  ->  Coach  ->  Guidance  ->  Binder  ->  DrawList  ->  Renderer
(pulse)   (decide)   (contract)   (geometry)  (contract)    (pixels)
```

Three guiding principles (from `w4-build-plan.md`): **build bottom-up, integrate at
the end** (the live HUD keeps running on the OLD engine until a single Phase-5
cutover — this doc); an **independent test oracle** (each stage arbitrated off-game
against a golden corpus / hand-authored fixtures, never against the old engine); and
**three-layer separation** (decide → bind geometry → draw pixels, each pure of the
next's concerns).

---

## Status — Phases 1–4 DONE, all four stages built + contract-tested off-game

Addon: `michac/CDMProbe`, checked out at `projects/cooldown-hud/addon/` (own git
root, gitignored). On a fresh machine run `wowkb.addon pull --all` first; current
version comes from `wowkb.addon list` (do not hardcode it). Off-game gate:
`busted CDMProbe/tests/spec` (125 green) + `luacheck CDMProbe/` (clean).

- **Phase 1 — State (`State.lua`).** `St.Build(drain)` emits the reduced, spec-
  agnostic, Secret-guarded **pulse** (cooldowns keyed by cooldownID, power, auras,
  cast history, events). Anchored on the **CDM database** (`C_CooldownViewer` category
  sets), not the live viewer frames. A ~10 Hz poll with cheap change-detection drives
  `St.Capture` — but **today its only consumer is the `/cdmp statelog` disk capture**
  (the Phase-2 corpus). Nothing scores the pulse in-game.
- **Phase 2 — Coach (`Coach.lua`).** `Coach.New(cfg):Compute(state) → Guidance`, the
  single-top-press ranked cascade. **Greened 23/23** against `corpus/goldens/*`. NOT
  wired live.
- **Phase 3 — Renderer (`Renderer.lua`, shipped v0.30.5).** `Renderer.New(cfg):Draw(drawList)`
  → pixels: corner cue dots (emphasis-coloured), keybind hints, a dot-scoped proc
  glow, a titled sequence panel, a discrete-pip resourceBar. The one impure line is
  `registry[anchorTo]` (handle → frame). Dialled in in-game via **`/cdmp rendertest`**
  against **hand-authored** DrawList fixtures. NOT wired live.
- **Phase 4 — Binder (`Binder.lua` + `HudGeometry.lua`, this session).** Pure
  `Binder.New(cfg):Bind(guidance, layout) → drawList`. cues → corner geometry +
  emphasis pass-through + keybind (cfg `keybindFor` seam) + glow rule + the
  layout-presence drop; sequence → panel; resourceBar → pip bar. The geometry
  constants live in the shared `ns.HudGeometry`, which the Renderer's fixtures read
  too (they agree by construction). Greened by `binder_spec.lua` (13 tests, incl. the
  close-the-loop: golden Guidance + a state-derived Layout → the exact rendertest
  fixture). NOT wired live.

**Every stage exists and is verified against its frozen contract. What does not exist
is anything that RUNS them in sequence on the live client.** That is Phase 5.

---

## The two worlds, side by side (what "cutover" replaces)

### The OLD engine — still the live `/cdmp hud` today

- `HudCore.lua` — `ns.SetHud(on)` lifecycle; **`rebind()`** is the `RefreshLayout`
  hooksecurefunc callback (+ `COOLDOWN_VIEWER_DATA_LOADED` / `PLAYER_ENTERING_WORLD`).
  It rebuilds the registry `M.items[key] = { item = <Blizzard frame>, spellID,
  baseSpellID, viewer, index, cooldownID }` and re-attaches chrome per icon.
- `HudChrome.lua` — draws directly onto/around the Blizzard item frames: the per-item
  dot (level), the group bracket, keybind text, proc glow, the viewer-anchored **shard
  rail**, the DEMO.SYS terminal + scanlines.
- `HudState.lua` (1,254 lines) — the de-facto state layer that ALSO scores and paints
  (audit A4); owns the AoE **mode** toggle, napkin sync, readiness seeding, level sync.
- `HudScore.lua` / `HudBoard.lua` — the per-ability dot score (no priority order).
- `HudPane.lua` / `HudOpener.lua` / `HudBurst.lua` — the movable **sequence pane** and
  the pre-pull opener strip.

### The NEW pipeline — built, tested, dormant

`State.Build()` → `Coach:Compute()` → `Binder:Bind(guidance, layout)` →
`Renderer:Draw(drawList)`. Coach/Binder/Renderer are pure; State touches the API. The
Renderer owns a `registry[handle] → frame` and a frame/texture pool.

The cutover makes the NEW path draw the live HUD and **deletes** HudBoard / HudScore /
HudChrome and the score/paint half of HudState — keeping only the **input plumbing**
State consumes (`HudBinds`, `HudNapkin`, the AoE toggle, readiness seeding).

---

## What Phase 5 must build (the wiring — the gaps between the stages)

1. **A live Layout producer.** The Binder needs `layout = { [cooldownID] =
   { spellID, side } }` for the **displayed** icon-viewer items, and the Renderer needs
   its `registry[cooldownID] = <Blizzard item frame>`. Both come from the SAME
   `RefreshLayout` pass — `HudCore.rebind()` already walks exactly those frames
   (cooldownID + spellID + item frame per icon), and `State.itemFrameMap()` already
   maps cooldownID → item frame. So this is re-homing an existing walk into a Layout
   emitter + a registry fill, not new discovery. (v1 uses `TOPRIGHT` for every dot, so
   `side` is carried but not yet consumed.)

2. **The `keybindFor` seam.** `Binder.New{ keybindFor = ns.HudBinds.Get }` — the live
   action-bar scan the Phase-4 test faked with a map. (Panel/sequence step keybinds
   already ride the Guidance from the Coach, which reads them off the State pulse.)

3. **Close the two State gaps** (flagged in the Phase-4 out-of-scope list):
   - **`mode`** — `St.Build` emits no `mode`; the goldens carry `"st"`/`"aoe"`. Source
     it from the existing single/multi toggle (`ns.HudState.aoe` / `/cdmp single|multi`).
   - **`power.SoulShards.incoming`** — `readOnePower` returns `{readable,value,max,type}`
     with no `incoming`; the goldens carry the in-flight shard projection. Source it
     from the napkin (`HudNapkin` / the projected-shards read the old HUD already uses).

4. **The driver.** Run `State → Coach → Binder → Renderer` on a trigger. Reuse State's
   ~10 Hz poll + change-detection for the **state pulse**, and the `RefreshLayout` hook
   for **layout/registry** changes (the two cadences the old engine already uses).
   State's header explicitly anticipates this: "nothing downstream cares what caused a
   pulse, so it can later become event-driven + napkin-scheduled wakeups." **Decide the
   trigger topology up front** (open question below).

5. **cooldownID key-type consistency, end to end.** Guidance cue keys, Layout keys, and
   the Renderer registry keys must be the SAME type. Live `St.Build` keys `cooldowns`
   by **number**; the golden JSON (and thus the Phase-4 tests) used **strings**. Pick
   one (numbers live) and make `Renderer:Register` + the Binder `layout` agree. A
   mismatch = every cue silently dropped (the layout-presence filter never matches).

6. **Renderer overlay above the LIVE CDM frame stack.** The Phase-3 rendertest put the
   overlay at `DIALOG` strata over BARE placeholder squares. Live CDM icons carry
   Blizzard's own swipe/cooldown child frames; the cue dot + glow + keybind must sit
   **above those**. Verify and adjust strata/level against real icons (the deferred
   "live-CDM frame-stack details" note — now in scope).

7. **resourceBar + panel reconciliation.** The Renderer draws its OWN pip resourceBar
   and titled panel. The old engine has the viewer-anchored **shard rail**
   (`HudChrome.ShowRail`) and the movable **sequence pane** (`HudPane`, saved position +
   lock). Decide whether v1 adopts the Renderer's fixed-geometry widgets as-is or ports
   the pane's drag/lock + the rail's viewer-anchoring first (open question below).

8. **Retire the old engine.** Once the Renderer path draws correctly, delete
   `HudBoard` / `HudScore` / `HudChrome` and the score/paint half of `HudState`,
   keeping the input plumbing State consumes. Staged, not a single `rm` — orphaned
   frames or a half-deleted HudState is how a cutover regresses silently.

---

## Suggested sub-phase sequence (de-risked: parallel-run before delete)

Each is checkpointable. Unlike Phases 2–4 (pure logic, no release), Phase 5 **touches
the live client**, so the later steps need a build + an in-game pass.

- **5a — Live Layout + registry.** Emit the Layout and fill a Renderer registry from
  the `RefreshLayout` pass. Inspection only (a `/cdmp` dump of the Layout); nothing
  drawn yet. Off-game where possible.
- **5b — State gaps.** Emit `mode` + `power.SoulShards.incoming`; extend the statelog /
  golden coverage so State stays contract-complete. Pure-ish; `wowkb.cdmp` verifiable.
- **5c — The driver behind a flag** (e.g. `/cdmp hud2`). Run the full pipeline +
  `Renderer:Draw` on the ticker, **alongside** the old HUD (old draw suppressed or
  side-by-side), so it can be dialled in on a live dummy without deleting anything.
  **This is the parallel-run that de-risks the cutover** — the P1 "integrate at the
  end" step, made reversible.
- **5d — Strata + positioning polish.** Dot/glow/keybind above the live icon stack;
  resourceBar + panel placement (port the pane's drag/lock if adopted).
- **5e — Cutover + retire.** Make the new path the default `/cdmp hud`; delete
  HudBoard/HudScore/HudChrome + HudState's score/paint; keep the input plumbing. Update
  `CLAUDE.md`, `architecture.md`, `milestones.md`.
- **5f — 🧇** (per the build plan).

---

## Open design questions — SETTLED (user, 2026-07-26)

All five are resolved; recorded here so a fresh-context agent reads a settled plan.

1. **Trigger topology → REUSE THE POLL.** 5c drives the whole draw off State's single
   ~10 Hz poll (the simplest thing that matches the old cadence). Event-driven +
   napkin-scheduled wakeups stay a later optimisation, exactly as State's header frames
   it. (Consequence: the driver also re-scans the live Layout each tick — cheap, a
   handful of frames — rather than coupling to HudCore's `RefreshLayout` hook; the
   hook-driven layout refresh is the same later optimisation.)
2. **Parallel-run vs hard cutover → FLAG-FIRST PARALLEL RUN, THEN DELETE.** Ship the new
   pipeline behind `/cdmp hud2` running **alongside** the old HUD; dial it in on a live
   dummy; delete the old engine only once proven (5e). Reversible by construction.
3. **panel/bar widgets → ADOPT THE RENDERER'S FIXED-GEOMETRY WIDGETS.** v1 uses the
   Renderer's built-in resourceBar + panel as-is for the live shard bar + opener panel.
   The old viewer-anchored **shard rail** (`HudChrome.ShowRail`) and the movable
   **sequence pane** (`HudPane`, drag/lock) **retire with the engine** — positioning
   polish (porting drag/lock or viewer-anchoring) is a later increment, **not** a
   cutover blocker.
4. **HudState boundary → KEEP THE INPUT PLUMBING, DELETE SCORE/PAINT.** At 5e delete the
   score/paint half; keep what State consumes: the AoE **mode** toggle (`SetAoE`/`aoe`),
   the shard-projection input the napkin/incoming ride on, napkin sync, readiness
   seeding, level sync. The exact keep/delete function list is named at the top of 5e
   (before touching the file), not now.
5. **The `transient` / animation channel → DEFERRED.** Kept out of v1. The cue still
   carries the `transient` token from the Coach and the Renderer keeps **ignoring** it
   for now; a minimal flash is a later increment with its own verification.

---

## Verification

- **Off-game gate stays green** throughout: `busted CDMProbe/tests/spec` +
  `luacheck CDMProbe/` + the luaparser syntax gate. New pure logic (5a/5b) gets its own
  busted coverage; State's new fields get statelog + `wowkb.cdmp` coverage.
- **In-game (the new part — first live phase since Phase 1).** A build + `/cdmp` pass on
  a target dummy: cue dots land on the right icons with the right emphasis / keybind /
  glow; the resourceBar tracks shards (+ the in-flight projection); the panel shows the
  opener; toggling off leaves Blizzard's UI pixel-clean with **no orphaned frames**.
  Use `/cdmp probe`, `/cdmp statelog`, and `wowkb.cdmp check` for the State layer.
- **This phase cuts releases** (unlike 2–4): 5c and 5e ship builds. Follow the addon
  release workflow (`wowkb.addon release cdmp`); a plain push does not reach the game.

---

## Critical files

- **Wire (read + extend):** `State.lua` (add `mode` + `incoming`; expose the pulse to a
  live driver), `HudCore.lua` (`rebind()` is the Layout/registry source; the lifecycle
  the new driver slots into), `HudBinds.lua` (`Get` = the `keybindFor` seam),
  `HudNapkin.lua` (the `incoming` source), `Binder.lua` / `Renderer.lua` /
  `HudGeometry.lua` (the consumers, already built).
- **Retire (delete at 5e):** `HudBoard.lua`, `HudScore.lua`, `HudChrome.lua`, and the
  score/paint half of `HudState.lua`. Reconcile `HudPane` / `HudOpener` / `HudBurst`
  with the Renderer panel per open question #3.
- **Contracts (lock to, don't re-derive):** `architecture.md` (State / Guidance /
  Layout / DrawList), `guidance-contract.json`.

---

## Fresh-context starting checklist

1. `wowkb.addon pull --all` (separate gitignored repos).
2. `cd projects/cooldown-hud/addon && export PATH="$HOME/.luarocks/bin:$PATH"` then
   `luacheck CDMProbe/` + `busted CDMProbe/tests/spec` — confirm the green baseline.
3. Read, in order: this doc → `w4-build-plan.md` §Phase-5 → `architecture.md` (all four
   contracts) → `HudCore.lua` `rebind()` (the Layout/registry source) → `State.lua`
   `Build`/`poll` (the pulse + the driver seam) → `Binder.lua` / `Renderer.lua` (the
   consumers).
4. The five open design questions are **SETTLED** (see that section) — don't re-ask.
   Start at 5a (Layout + registry) and keep the old HUD running until 5e.

## Progress (2026-07-26)

- **Decisions 1–5 settled** (folded above).
- **5a DONE (off-game).** `HudLayout.lua` — a pure `Build(entries) → layout, registry`
  + an impure `Scan()` that walks the two icon viewers (Essential + Utility) and
  resolves each item to `{ cooldownID (number), spellID (base), frame }`. cooldownID
  keys are **numbers** (key-type consistency #5). busted `hudlayout_spec.lua` covers
  Build; `/cdmp hud2 layout` dumps the live scan (inspection only, nothing drawn).
- **5b DONE (off-game).** `State.Build` now emits top-level `mode` ("st"|"aoe", from the
  AoE toggle) and `power.SoulShards.incoming` (net yield of in-flight **builder** casts
  via the injected `ns.SpecGhost` reader — builder-only, the safe direction, no
  double-deduction hazard; State stays spec-agnostic). `wowkb.cdmp` extended: the
  enum-domain check validates `mode`, and two coverage checks (mode captured, incoming
  captured) were added to `probe-baseline.json`.
- **5c CODE LANDED (off-game); in-game dial-in + release outstanding.** `HudDriver.lua`
  runs `State.Build → Coach:Compute → Binder:Bind(guidance, layout) → Renderer:Draw` on
  State's poll, **behind `/cdmp hud2`**, alongside the old HUD. `keybindFor =
  ns.HudBinds.Get`. Not yet built/dialled-in in-game; **no release cut** (that step is
  user-driven). The off-game gate stays green.
- **5c dial-in DONE (v0.31.0 tested in-game).** Foundation works. Live findings drive the
  revised worklist below.

## Revised worklist — 5d finish the cutover, then Phase 6 the Coach (2026-07-27)

5c's in-game pass surfaced four findings (2 draw-layer, 2 Coach-logic). We split them:
**finish Phase 5** (the cutover — draw-layer + retire the old engine) then **Phase 6**
(Coach & guidance quality — new scope, golden-gated, test-first).

### 5d — draw-layer polish (no Coach/golden churn)

- **Keybinds on every icon via EMPTY CUES (decided — not a side channel).** The Binder
  iterates the **layout** (every displayed item), not just the Coach's cues, and emits a
  cue when an item has an emphasis **OR** a keybind. An *empty cue* = no emphasis (no dot,
  no glow) + a keybind → the Renderer draws just the key hint. `G.cue(cid, nil, keybind)`
  already yields that shape (no `HudGeometry` change). Renderer tweak: decouple the key
  hint from the dot so a colourless cue still draws its key. **Re-points `binder_spec`
  (more cues emitted), NOT the Coach goldens.**
- **Strata / parenting (the "draws over the map/character panel" bug).** Parent each cue's
  dot/glow/keybind to its icon frame at the icon's strata, one frame-level above its
  swipe/cooldown children — instead of the global `DIALOG` root. Then a higher-strata
  panel (map, character screen) covers the dots exactly as it covers Blizzard's own
  spell-activation glow. The self-anchored panel + resourceBar drop off `DIALOG` too.
  **Needs in-game confirmation** (does the dot clear the swipe? does the map cover it?).

### 5e — cutover + retire

Make `hud2` the default `/cdmp hud`; delete `HudBoard`/`HudScore`/`HudChrome` + HudState's
score/paint half (keep the input plumbing). **Scope depends on 6e** (whether the sequence
panel survives ⇒ whether `HudPane`/`HudOpener`/`HudBurst` are deleted outright).

### Phase 6 — Coach & guidance quality (test-first; each step lands its goldens RED, then greens them)

- **6a — projected-shards goldens (RED).** Re-point `soon-incoming` (+ check
  `incoming-overcap`, add an Infernal-Bolt-in-flight `+3` case) to the new intent:
  *incoming promotes the spender to the press*. Commit with a run showing them failing.
- **6b — fix the Coach to green 6a.** State reports ONE shard number = `value + signed
  incoming` (incoming now includes in-flight SPENDS as negative, guarded by the old HUD's
  cast-start-snapshot against double-deduction, and cleared on cast interrupt/stop). The
  Coach treats it as "shards" everywhere — delete the value-vs-projected split
  (`Coach.lua:390` gates on live shards, `:468` on projected: that inconsistency is the
  bug). This fixes note 2 for free.
- **6c — the Tyrant-up burst mode (goldens first, RED → green).** When Tyrant is
  available / the window is being set up: **cap shards → drop demons (Dreadstalkers /
  Grimoire) → Summon Tyrant → flood HoG**. Formalize as an explicit Coach mode with new
  goldens. (If the cues walk this cleanly one press at a time, it's what makes the panel
  redundant — feeds 6e.)
- **6d — "properly prompt" (definition TBD at 6d).** Working read: the live cue
  *behaviour* — one-move-ahead, clearing the ability you're mid-casting, right emphasis at
  the right moment (possibly re-touching the deferred `transient` flash). Pin the exact
  scope when we reach it.
- **6e — the fate of the sequence panel.** Decide *after* 6a–6d, with the improved
  anticipatory cues in hand: **drop** it (simplest tool + simplest cutover — `HudPane`/
  `HudOpener`/`HudBurst` just get deleted) vs. **keep** it as a robust, additive
  burst/opener planner (shows when a Tyrant window is being set up, never suppresses the
  press underneath). Crutch-vs-trainer is the product call. Determines 5e's delete scope.

**Order:** 5d → 6a → 6b → 6c → 6d → 6e → 5e. Draw-layer + the clear shard win first; the
sequence decision and the final retirement last.
