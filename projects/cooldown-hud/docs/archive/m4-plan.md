# M4 — The Sequence Helper (opener + burst)

## Context

M4 was "Burst window"; it is now reframed as **the sequence helper**, one feature
with two starter use-cases (opener + burst), absorbing the opener that shipped
under the M3c-c2 label. Three things drive this pass:

1. **A real bug.** The shipped opener (`HudQueue` drop-through) advances on *any*
   matching cast. Shadow Bolt is a step *inside* the opener (step 4 `SB/DB`, step 7
   `SB×3`), so a **pre-pull SB to cap shards drop-through-matches the later SB step
   and silently consumes Dreadstalkers → Imp Lord → Tyrant** (`HudQueue.lua:223-240`).
   By pull time the queue thinks the opening is done.
2. **A placement need.** The helper is *instructional* and wants central vision
   (over the character), but every current HUD surface is **viewer-anchored** to the
   CDM column (`HudChrome`/`HudQueue.lua:72-84`). It needs its own movable pane.
3. **A root fix in the engine, not the queue.** Pre-pull the correct play is *cap
   shards without overcapping* (build to 5), but `HudScore` only knows the sustain
   loop (≥3 → SPEND → press HoG). The fix: make PREP/BURST-mode scoring promote the
   builder and hold HoG — then the pre-pull capping casts are engine-directed setup,
   not sequence steps, and the queue is right to ignore them.

Intended outcome: a positionable **SequencePane** (prereqs row + keybind strip),
**primed until the first sequence key** (kills the desync), reused by the opener and
the burst window, backed by a mode-aware capping rule, with asymmetric minigame
juice. Audio stays deferred to M6 (`HudChrome.lua:920-924` fence).

## Approach

- **New `HudPane.lua`** — a **movable, `UIParent`-anchored** container (drag + save,
  ported from the parked prototype `Resource.lua:147-159`) that hosts a **prereqs
  row** (FontString) above a **`HudQueue` step-strip**. It is the shared surface;
  the opener and burst are two *consumers* that arm it (the documented
  "second consumer = data + a trigger" pattern, `HudOpener.lua:6-8`).
- **`HudQueue` gains two small capabilities:** (a) an optional **host frame** arg so
  its strip mounts *inside* the pane instead of anchored above the viewer; (b) a
  **`primed` state** — while primed the cursor sits at step 1 and `Advance` only
  fires on a press matching step 1's `spell`/`alt`, which un-primes and begins the
  drain. Non-matching presses while primed are ignored (this is what makes pre-pull
  SB a no-op).
- **One pane, re-armed** for the two use-cases, never two panes.
- **Engine root-fix (the load-bearing half):** build the **BURST mode** branch at
  the existing `HudState.lua:276` vacancy, then add the **"cap without overcapping"**
  inversion to `HudScore`'s context-pruning block.
- **Visual minigame juice only**; audio arrives in M6 with the mute contract.

## Files & key anchors

| File | Change | Reuse / anchor |
|---|---|---|
| **`HudPane.lua`** *(new)* | Movable UIParent container + drag/save + prereqs row + juice hooks; API `Arm(spec,prereqs)` / `Advance` / `SetPrimed` / `Dissolve` / `Info`. | Drag pattern ← `Resource.lua:153-158`; frame/level idiom ← `HudChrome.lua:813,991`; never `EnableMouse` when locked (clicks pass through). |
| **`HudQueue.lua`** | Optional `host` arg on `Q.Ensure`; add `primed` flag + start-on-first-key gate in `Advance`. | `Q.Ensure` `:266`; `QueueMeta:Advance` `:223`; `Arm` `:203`. |
| **`HudState.lua`** | Add **BURST** branch at the `-- [M4] BURST goes here` slot; author a `board_staged` predicate; add a sibling `pcall(ns.HudBurst.OnCast, a3)` dispatch. | Vacancy `:276`; mode fn `S.Mode()` `:272`; cast dispatch `:972-973`; Tick tail `:649`; combat-end `:935`; `N.Remaining(TYRANT)` `HudNapkin.lua:123`. |
| **`HudScore.lua`** | The mode-aware capping inversion in the context-pruning block: in PREP/BURST, promote a non-primary generator to ROTATION until near-cap, demote HoG to AVAILABLE ("hold for Tyrant"). | Prune block `:318-343` (the `M4, not built` comment is `:337-338`); overcap guard to reuse `:387`; ROTATION chain `:358-380`; `mode` read `:154`. |
| **`HudOpener.lua`** | Re-point at `HudPane` instead of `HudQueue.Ensure(viewer,…)`; pass `prereqs`; mark primed on Arm. | `armSpec()` `:65-77`; `O.OnCast` `:103`; lifecycle unchanged. |
| **`HudBurst.lua`** *(new)* | Second consumer: arm the pane on Tyrant-window open, steps = the burn sequence, dissolve on window close. Sibling of `HudOpener`. | Same hook seams: `Arm` from `HudCore.lua:275`, `OnCast` from `HudState.lua:972`, `Tick` `:649`. |
| **`SpecDemonology.lua`** | `ns.SpecOpener` gains a `prereqs` list; add `ns.SpecBurst` (steps + prereqs). | `ns.SpecOpener` `:267`; `goGate`/`burstAlign` bits `:29-33,99-111` feed `board_staged`. |
| **`Core.lua` / `HudCore.lua`** | Default + back-fill `ns.db.hud.sequence = {point,x,y}`; wire `HudBurst`/`HudPane` into the lifecycle (Arm/OnCast/Tick/Hide) the way `HudOpener` is. | `DEFAULTS` `Core.lua:19`; `ensureDB()` `HudCore.lua:67`; opener seams `HudCore.lua:275,366,554`. |
| **`CDMProbe.toc`** | Add `HudPane.lua` (after `HudQueue`) and `HudBurst.lua` (after `HudOpener`). | Load order `:8-26`. |

## Implementation phases

**Phase 1 — SequencePane + opener rework (fixes the bug, ships the pane).**
`HudPane` (movable, drag-to-`ns.db.hud.sequence`, lock/unlock; prereqs row hosting a
`HudQueue` strip). Add `primed`/start-on-first-key to `HudQueue`. Port `HudOpener`
onto the pane, pass `prereqs` (`Tyrant · Dreadstalkers · 5 shards`), evaluated OOC
(wall down): readiness via `N.Remaining`/ready-edge, shards via `UnitPower`.
*Exit:* pre-pull SB no longer desyncs; the pane drags and persists.

**Phase 2 — BURST mode (engine).** Fill `HudState.lua:276`: `BURST` when
`N.Remaining(TYRANT) <= HOLD_LEAD (~5s)` **and** `board_staged`. Author `board_staged`
from `goGate` readiness (Tyrant + Dreadstalkers) — best-guess, ground-truth (native
ready-alert) always wins. Add `HOLD_LEAD` knob (distinct from `N.SOON_LEAD=3`).

**Phase 3 — HudScore "cap without overcapping" (depends on P2).** In the prune block
`:337-343`: if `mode == PREP or BURST` and a non-primary `info.generates` would *not*
overcap (reuse `:387` logic) → promote to ROTATION ("cap for Tyrant"); and demote the
primary spender (HoG) from ROTATION to AVAILABLE with "hold for Tyrant". **Co-design
with #11's HOLD telegraph** so the dot and the telegraph never disagree.

**Phase 4 — HudBurst consumer.** New sibling module; arm the same pane when BURST
opens, steps = `ns.SpecBurst` (Tyrant → HoG HoG → …), dissolve on window close
(reuse the elapsed-time clock idiom, `HudOpener.lua:120-123`).

**Phase 5 — Visual minigame juice.** Correct key → one-shot flash (template:
`H.Settle` `HudChrome.lua:515`); completion → glitter-style flourish (`fireGlitter`
`:1087`, throttled); **miss → gentle dim only, never scold** (a "wrong" press is
often a valid opener branch — §0.5.8.7). Design the juice as `onCorrect/onMiss/
onComplete` hooks so **M6 can wire sound in without refactoring** (respect the
`HudChrome.lua:920` fence — no `PlaySound` in M4).

*Out of scope for this plan:* the ambient burst-**board** cues (#9 lane / #10 BURST
tint / #11 telegraph / #12 pings) remain M4 milestone work but are separate from the
sequence pane; #11 must be built *alongside* Phase 3 (shared HOLD window).

## Verification (in-game, at a target dummy)

Deploy (`ghaddons update michac/CDMProbe` → `/reload`), then:
1. **Desync fix (Phase 1):** OOC, target the dummy, `/cdmp hud opener on`. Cast SB/DB
   to cap shards → **the queue must not advance** (stays primed on Dreadstalkers).
   Press Dreadstalkers → it starts and drains correctly.
2. **Pane (Phase 1):** unlock, drag the pane over your head, `/reload` → position
   persists (`ns.db.hud.sequence`).
3. **Capping rule (Phase 3):** OOC / low shards → the builder (SB) reads ROTATION and
   **HoG reads "hold for Tyrant"**, not ROTATION; verify in `/cdmp hud status` +
   `hud debug` reasons. Confirm it does not fire mid-sustain (GENERATE/SPEND).
4. **Burst (Phases 2/4):** pull, reach a Tyrant window → mode flips BURST, the pane
   re-arms with the burn sequence, the capping rule holds pre-Tyrant, dissolves on
   window close.
5. **`/cdmp hud log`** — the pull recorder (M3e) captures the transitions for review;
   no need to type mid-pull.

Then luaparser-check and follow the CDMProbe release workflow (bump `.toc`, commit,
`gh release`, `ghaddons update`).

## Open questions / risks

- **BURST mode + the capping rule ride the napkin Tyrant clock** — i.e. on
  `UNIT_SPELLCAST_SUCCEEDED` reading non-secret, which we treat as settled. Keep
  BURST a best-guess; the native ready-alert is ground truth; the capping rule only
  ever *holds* HoG (safe direction), never invents a press.
- **`board_staged` is new** — start minimal (Tyrant + Dreadstalkers ready) and tune;
  never let it force a wrong instruction (§0.5.8.7).
- **Minigame miss feedback must stay gentle** — asymmetric juice; a deviation may be
  a legit branch, so never a red "WRONG".
- **Audio is M6, not here** — juice ships visual-only with hooks; wiring sound now
  would breach the `HudChrome.lua:920` fence and the mute contract.
- **Pane vs viewer-anchored tension** — `HudPane` is the addon's first `UIParent`
  frame; it does not ride Edit Mode, so its lock/unlock + saved position is the only
  positioning path (by design, since over-the-head placement is the point).
