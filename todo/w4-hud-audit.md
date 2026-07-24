# W4 — Cooldown HUD audit (working file)

> **Working audit doc for W4 of `addon-engineering.md`.** Findings captured
> 2026-07-24 from a read-only review of **CDMProbe v0.28.1** by a Fable subagent
> driven through the `wow-developer` skill (routed to `knowledge/addon-dev/`,
> anchors checked `file:line` against `wow-ui-source @ 4383ced`, build 12.0.7.68887).
> This is the audit W4 is measured against; the Cooldown HUD feature freeze lifts
> when it lands. Check items off / annotate as the refactor proceeds — this file is
> the live worklist, not a frozen report.

## Environment provisioned before the audit (this machine was a fresh checkout)

- **Checkout synced** — was v0.19.0 locally (10 releases / ~2,700 lines behind
  `origin/main`); pulled to **v0.28.1**. All line numbers below are v0.28.1.
- **`wow-ui-source` cloned** into `raw/addon-research/` at the KB-pinned commit
  `4383ced` (build 12.0.7.68887). CooldownViewer anchors verify
  (`ShouldBeShown` :311, `TriggerAlertEvent` :483 — as the KB cites).
- **`wowkb.uiapi` index built** (`lua5.1` installed; 6144 funcs / 1741 events /
  795 enums @ 12.0.7.68887) — structured `uiapi func/event/struct/enum` queries work.
- **Test toolchain installed** — `luarocks 3.8.0`, `busted 2.3.0`, `luacheck 1.2.0`
  under `~/.luarocks/bin` (targeting lua5.1). Existing suite green: **33 successes /
  0 failures** (`busted tests/spec` from the CDMProbe dir). This is the harness W4d
  extends. ⚠ `busted`/`luacheck` need `~/.luarocks/bin` on `PATH`
  (`export PATH="$HOME/.luarocks/bin:$PATH"`) — not yet in the shell profile.

## What's solid (keep)

Secret-value discipline at the read boundary is exemplary and consistent
(`Viewers.lua:49` `readable()`, `Util.lua ns.ReadCooldown` GCD trap, `SpecInfo`'s
refusal to table-key a secret). `HudScore` / `HudQueue` / `HudNapkin` / `HudBurst`
are genuinely pure and busted-tested. `Sc.Stabilise` was deliberately written pure.
Structured probe-store discipline is right. The findings below are where that
discipline frays — not a rewrite.

---

## A. Architecture / the data–display seam (the W4b target)

- [ ] **A1 (HIGH) — the cue decision is smeared across three modules.**
  `HudScore.For` decides level/`judgeReady`/`emphasis` (tested); `HudState.Recompute`
  re-decides (`Stabilise` `HudState.lua:674`, SOON-as-treatment `:684`, Tyrant paint-key
  rewrite + `S.tyrantShardHold` published as a side effect of the paint loop `:686–708`,
  `ns.SpecNoCue` suppression `:683`); `HudChrome.SetCue` (`HudChrome.lua:482`) decides
  *again* (level→`bkey` incl. `AVAILABLE+judgeReady→JUDGE`, draw/no-draw, palette
  `CUE` `:163`, `paintCue` `:434` turns emphasis into a fill fraction and picks a side).
  **Why:** the recent regressions (Tyrant-yellow-with-no-shards, churn gate, Grimoire
  double-voice) all live in `Recompute`'s middle layer — the one slice with **no busted
  coverage**. KB: `module-architecture.md` §4/rule 20 + Blizzard data/display mixin
  split (`confidence: medium`, corroboration).
  **Direction:** engine emits a complete per-key **cue descriptor**
  `{draw, colorKey, fill, pulse, emphasis, reasonTag}` from a pure fn of
  (score, prev-painted, mode, spec); `SetCue` renders it verbatim. `Stabilise` already
  shows the shape. `HudRow`'s `SHARDS!` special-case (`HudRow.lua:128`) then reads a
  descriptor field instead of a flag set mid-paint.

- [ ] **A2 (HIGH) — `Recompute` computes and paints in one pass**
  (`HudState.lua:594–760`): scores, clocks LATE, logs, paints cues + rail, ticks
  opener/burst, samples recorder — all one fn; the decision half isn't extractable for
  a client-free test. **Direction:** split `ComputeBoard(state) -> {descriptors, lit}`
  (pure) + thin `PaintBoard(descriptors)` dispatcher (keep the pcall-per-paint pattern).

- [ ] **A3 (MED) — three independent event-ingest points for the same events.**
  `Probe.lua`, `HudNapkin.lua`, `HudState.lua` each own a frame registering overlapping
  `UNIT_SPELLCAST_*` / `COOLDOWN_VIEWER_SPELL_OVERRIDE_UPDATED`, each with its own secret
  guard; `HudState`'s SUCCEEDED branch hand-fans to opener→burst→pane→endCast. Not a bug
  today; it's what W4a's game-state layer exists to collapse: one ingest, one guard, one
  reduced state, N subscribers.

- [ ] **A4 (MED) — `HudState.lua` is 1,254 lines of mixed responsibility** (stores,
  readers, mode spine, glow resolution, recede policy, LATE clock, seeding, event wiring,
  paint dispatch, 110-line status printer). Every seam defect routes through it. W4 gives
  each a home; minimum near-term: hoist the status printer and the seeding block.

- [ ] **A5 (LOW) — order-sensitive substring command dispatch**; `HudCore.lua` `hud`
  handler `rest:find("log")` with a bare-toggle tail — a typo mid-session flips the HUD
  off. Tokenise the first word; unknown subcommand prints help.

## B. Duplication / single-source-of-truth

- [ ] **B1 (HIGH) — live-identity resolution in three copies under a "there must be one"
  comment.** `S.LiveID` (`HudState.lua:550`, "ONE definition") re-derived inline in
  `HudScore.For` (`HudScore.lua:131–132`) and in `S.SeedFromReads` (`HudState.lua:941`,
  under its own "do NOT re-derive" comment). Devour-Magic bug came from this fact being
  wrong once. **Direction:** `S.LiveID` the only resolver; HudScore takes the resolved id
  as input (also simplifies its test fixture).

- [ ] **B2 (MED) — keybind cache has N consumers with ad-hoc per-consumer refresh**
  (chrome, rows per tick, sequence strip at arm time, probe/status). Strip went stale
  ("[Imp Lord]"); the fix `HudCore.RefreshKeybinds` reaches into the opener
  (`HudCore.lua:338`) — grows coupling the wrong way (the *caller* must know every
  consumer). **Direction:** `HudBinds` owns a subscriber list, notifies on map change;
  each consumer registers its own refresh — new consumers can't repeat the bug.

- [ ] **B3 (MED) — `HudOpener`/`HudBurst` duplicate three fns verbatim:** `enabled()`
  (`HudOpener.lua:48`/`HudBurst.lua:44`), `baseOfCast()` (`:59`/`:72`, reverse scan over
  `HudState.override`), `armSpec()` (`:74`/`:85`). `baseOfCast` belongs beside the
  override map (it's the inverse of `LiveID`); `armSpec`/`enabled` on a shared consumer
  base.

- [ ] **B4 (MED) — three ready/soon predicates with quietly different expiry semantics.**
  `S.readyOrSoon` (HudState), `HudPane.stepReady` (`HudPane.lua:109`), `evalPrereq` spell
  branch (`HudPane.lua:306`). `stepReady` treats napkin `Remaining()==0` ("should be up,
  unconfirmed") as *ready*; `evalPrereq` with `lead=0` marks a prereq *met* on that
  expired estimate — contradicts the napkin's "EXPIRY NEVER CLAIMS READINESS". Defensible
  for skip-an-optional-step, wrong for lighting a prereq met. **Direction:** one HudState
  predicate with explicit `treatUnconfirmedAs = "ready"|"unknown"`.

- [ ] **B5 (LOW) — palette constants copied into three files and diverged.**
  `TERM`/`TERM_DIM` "echoed, not a shared contract" in `HudQueue`/`HudPane` went neutral
  grey (M4.3) while `HudChrome`'s copies stayed CRT green; `H.DOT_COLORS`
  (`HudChrome.lua:173`) half-derives from `CUE`, half hardcodes. Apply the `H.CueColor`
  (`:520`) single-source rule to the rest.

- [ ] **B6 (NIT) — `SpecDemonology.lua:60` group hues cite retired `Resource.lua:12-27`
  as source of truth.** Move the triples' authority into SpecDemonology.

## C. Midnight 12.0 correctness (vs `knowledge/addon-dev/`)

- [ ] **C1 (HIGH) — `HudCueWatch` ships default-ON while its measurement channel is
  unproven** — an instrument that may not observe its subject, emitting numbers. Samples
  `GetVertexColor` @4 Hz vs the palette (`HudCueWatch.lua:97–125`), `cuewatch=true`. But
  `HudGradTest.lua`'s header records that read returned 1/1/1 for *every* level incl.
  confirmed-green — it may not see the rendered colour at all. KB marks the
  `SetVertexColor`-vs-`SetGradient` storage question a **`[gap]` at every tier**
  (`frames-textures-animation.md` §5.3). So mismatch/whiteish figures may be 100% phantom,
  by default, churning a 40-entry ring per pull. **Direction:** default it off until
  proven; gate `W.Start`/confidence wording on a stored gradtest verdict; when gradtest
  is run in-game, **write the result back to `frames-textures-animation.md` §5.3** (closes
  the KB gap — the wow-developer improve-the-KB rule). *Needs client — deferred.*

- [ ] **C2 (MED) — `HudBinds.scan`/`Explain` table-key raw action IDs with no secret
  guard** (`HudBinds.lua:84`, `:218`) while `B.Get` (`:171`) guards. KB security rule 14 /
  op table §4.2: table-key use of a secret is an immediate Lua error. `scan` is OOC-only
  (mitigated); `Explain` can run in combat. One `readable()`-style guard makes it
  self-consistent.

- [ ] **C3 (LOW) — secret-failure *comments* say "taint" where the client actually
  errors (or allows).** `HudCore.ItemCooldownID`, `HudBinds.Get`, `Core.lua` say
  index/format "taints"; per KB op table §4.2 (Tier 2 revid 6777907) disallowed ops raise
  an **immediate error**, and concat/`string.format` of string/number secrets is
  **allowed**. Guards are behaviorally correct; the wrong mental model breeds wrong future
  guards (KB Trap 1: the real trap is "comparison is safe if type-checked"). Comment-only
  sweep, no code change.

- [ ] **C4 (LOW) — `HudFloat` anchors pooled FontStrings to the player nameplate**
  (`HudFloat.lua:36–43`) — anchoring-secret exposure (KB rule 20, downward propagation
  Tier-2). Nothing measures the floats; `SetPoint` pcall'd; `ClearAllPoints` on re-anchor
  plausibly resets (rule 21, Tier-2). Watch-item: never measure these FontStrings; treat
  nameplate anchoring as `@verify-ingame`-class.

- **C5 (INFO) — SavedVariables/flush discipline correct** (`state-persistence` §2.1).
  Note `HudLog.EndPull` fires only on `PLAYER_REGEN_ENABLED` — a mid-combat DC/logout
  drops that pull; do **not** move pull-close to `PLAYER_LOGOUT` (KB §2.3 / WoWUIBugs
  #748: several APIs silently return nothing during a real logout while working in
  `/reload`). Current design is on the right side; keep it there.

- **C6 (INFO) — event registration + misc clean.** `RegisterUnitEvent`/`RegisterEvent`
  never collide on one event (api-events rule 18 not triggered); `date()` global exists;
  instance-hook rationale matches the mixin model (module-architecture rule 7).

## D. Dead / dormant / misplaced code (the W4a target)

- [x] **D1 (MED) — `HudTint.lua`: 72 provably-dead lines shipped in the `.toc`.** Nothing
  calls `T.Install`; `T.enabled=false`; all bodies gated on it. Worse, its revival notes
  predate the M3c-b identity-truth pass (`T.Apply` feeds `ns.ItemSpellID(item)` into
  `colorFor` with none of the current secret/override discipline) — reviving as-written
  reintroduces solved bugs. **Direction:** move out of the shipping `.toc` (git tag +
  `docs/notes-archive.md` pointer preserves the reference).
  **DONE 2026-07-24 (W4a):** deleted the file + its `.toc` line; reworded the
  `HudState.lua:38` "exactly as in HudTint" comment so it no longer points at a
  deleted file. Recoverable via `git log`/`git show` on the cdmp sub-repo (no
  archive file — decided against re-noting a superseded dead end).

- [x] **D2 (MED) — `Skin.lua` + `Resource.lua`: retired directions still shipped,
  reachable, doctrine-violating.** Live `/cdmp skin` / `/cdmp resource` run the 0.5s
  watchdog ticker the HUD's header forbids, keep spell tables duplicating SpecDemonology
  (`Resource.lua:30–45`), do `item.Icon:SetAlpha(0)` (the thing `SetHud` defends against),
  and extend the `reset`/`OnLogin` wrapper chain (Probe→Resource→HudCore rewrapping
  `ns.OnLogin`/`reset` — silently depends on `.toc` order; a reorder breaks it with no
  error). **Direction:** delete (history + `notes-archive.md` preserve findings) or
  quarantine behind one "retired experiments" module that owns the chain.
  **DONE 2026-07-24 (W4a) — scope decision taken: plain-skin + resource-centric
  directions are no longer pursued.** Deleted both files + their `.toc` lines and
  unwired the stragglers: the base `reset`/`OnLogin` in `Probe.lua` (dropped the
  `SetSkin`/`RestoreSkin` calls), the skin/resource-off lines in `HudCore.SetHud`,
  the `reset` help text, and the `skinOn=false` db default in `Core.lua`. The
  decorator chain auto-rewired (HudCore now wraps Probe's base directly; load order
  Probe→HudCore preserved). Grep confirms zero remaining refs; 33/33 busted +
  luacheck clean. Recoverable via `git log`/`git show`. ⚠ Follow-up left open:
  **B6** still cites the now-deleted `Resource.lua:12–27` as the group-hue source —
  move that authority into `SpecDemonology`.

- [ ] **D3 (LOW) — four const-false render paths** `SHOW_BRACKET`/`SHOW_GLOW`/`SHOW_SCAN`/
  `SHOW_TERMINAL` (`HudChrome.lua:185–201`), ~300 unreachable lines in the module W4 wants
  smallest. **Subtlety:** `SetGlow` still *records* glow state with drawing off and
  `HudState.quiet()` reads it — glow-as-state ≠ glow-as-pixels; split (state→HudState,
  drawing→archive) rather than deleting naively.
  **DEFERRED to W4b (2026-07-24):** not a clean delete — it's a state/pixel split
  inside the very file W4b reworks. When W4b lands: keep `SetGlow`'s state recording
  (HudState recede/quiet reads it) and the live `H.SetTerminalMode` (`HudChrome.lua:1257`);
  only `buildTerminal`/`H.ShowTerminal` (the CRT frame) and the unreachable draw code
  are dead.

- [x] **D4 (LOW) — `tests/` ships inside the installable addon folder.** `CDMProbe/tests/`
  is inert in-game (not in `.toc`) but rides every release zip into `Interface/AddOns/`.
  Move up a level (busted only needs a path).
  **DROPPED from W4a (2026-07-24):** release hygiene, not source-tree declutter.
  Tests aren't clutter (W4d grows them), and the move would churn `mock_ns.lua`'s
  path resolution right before we lean on the harness. Trivial packager-exclude
  later if shipping test files ever matters.

- [x] **D5 (NIT) — `HudQueue` vertical renderer has no consumer** (self-documented).
  Candidate for the same archive sweep as D3.
  **KEPT (2026-07-24):** deliberately retained as a documented future-consumer path
  (`orient="vertical"`), not accidental clutter — left as-is, no archive sweep.

## E. Other

- [ ] **E1 (MED) — two clocks + eager strings over one fact.** With HUD on: poll @10 Hz,
  score @4 Hz, row @~6.7 Hz, cuewatch @4 Hz. `HudRow` re-renders on its own clock reading
  `S.score` that `Recompute` just produced — rows should be driven from `Recompute`'s tail
  (countdown text is the only genuinely clocked part). `Sc.For` builds `string.format`
  reason strings for every item every pass — violates the "no string work on the sample
  path" discipline HudLog enforces. **Direction:** reasons as `(tag, args)` rendered on
  demand, or accept + document the cost.

- [ ] **E2 (NIT) — diagnostics classification is the W4 question.** Gradtest/CueWatch/
  Probe/HudLog are instruments, not product. Legit to ship (addon is a "probe/kitchen
  sink"), but W4's split should draw a fourth **diagnostics** box so instrument code stops
  interleaving with the render path (cuewatch reaching into `o.cue` internals is the
  current leak).

---

## Biggest wins (do in this order)

1. ~~**Sync the checkout** (v0.19.0 → v0.28.1).~~ **DONE 2026-07-24.**
2. **The cue descriptor (A1+A2)** — one pure presenter, `SetCue` renders verbatim; puts
   the thrice-regressed code inside the busted fence. *This is the heart of W4b.*
3. **One identity/readiness kernel (B1+B3+B4)** — `S.LiveID` the only resolver,
   `baseOfCast` beside the override map, one ready/soon predicate with explicit policy.
4. **Push-based keybind invalidation (B2)** — `HudBinds` notifies subscribers; retire the
   HudCore→HudOpener re-arm reach-through.
5. **Settle the gradient question and honor it (C1)** — run `/cdmp gradtest` in-game,
   default HudCueWatch off until its channel is proven, write the verdict to the KB.
   *Needs client access — deferred.*

## Verification status (per the wow-developer skill)

**Now verified** (wow-ui-source present @ 4383ced): CooldownViewer anchors
(`ShouldBeShown` :311, `TriggerAlertEvent` :483, and the alert paths).

**Still can't verify without the client** (KB `[gap]` / `@verify-ingame`, honest holes —
not blockers for the code refactor, which is what W4b/W4a are):
- `SetVertexColor` vs `SetGradient` storage interaction — `[gap]` at every tier
  (`frames-textures-animation.md` §5.3); `/cdmp gradtest` is the test, unrun. (C1)
- Nameplate-anchoring secret propagation — rule 20 downward half is Tier-2. (C4)
- `Texture:SetMask` / `SetGradient(...)` signature — not in KB topic files; both pcall'd
  in code so failure degrades rather than throws.
- The action-slot→binding-command table (`HudBinds.lua:25–34`) — not KB-covered.
