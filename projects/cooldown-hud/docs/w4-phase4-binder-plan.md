# W4 Phase 4 — the Binder: handoff + plan

*(Dated 2026-07-26. A fresh-context handoff: the overall task, what's built through
Phase 3, and the plan for the next unit — the **Binder**. Companions:
`w4-build-plan.md` is the phased sequence this executes; `architecture.md` the
target-state pipeline; `w4-phase2-coach-notes.md` + `w4-phase3-renderer-notes.md`
the two stages already built.)*

---

## The overall task

Cooldown HUD is a spec-specific overlay (v1 = **Demonology Warlock**) that skins
Blizzard's built-in Cooldown Manager under Midnight 12.0. The **W4 refactor** is
rebuilding its data/display seam into a clean, testable pipeline:

```
State  ->  Coach  ->  Guidance  ->  Binder  ->  DrawList  ->  Renderer
(pulse)   (decide)   (contract)   (geometry)  (contract)    (pixels)
```

Three guiding principles (from `w4-build-plan.md`): **build bottom-up, integrate at
the end** (the live HUD keeps running on the old engine until a single Phase-5
cutover); an **independent test oracle** (each stage is arbitrated off-game against
hand-authored fixtures / a golden corpus, never against the old engine); and
**three-layer separation** (decide → bind geometry → draw pixels, each pure of the
next's concerns).

---

## Status — what's built (Phases 1–3 done)

Addon: `michac/CDMProbe`, checked out at `projects/cooldown-hud/addon/` (own git
root, gitignored). **Current version: v0.30.5.** On a fresh machine run
`wowkb.addon pull --all` before touching it.

- **Phase 1 — State (`State.lua`).** Enumerates the full CDM category set and does a
  separate live `C_Spell` read per entry, emitting a reduced **State pulse**
  (readable/Secret-guarded). Captured to `CDMProbeDB.statelog` (`/cdmp statelog`) —
  the independent corpus the Coach is tested against.
- **Phase 2 — Coach (`Coach.lua`).** `ns.Coach.New(cfg)` → `Coach.Compute(state)` →
  **Guidance**. A single-top-press ranked cascade (Classify → Context → RankWinner →
  Escalate → Emit). Pure factory; **greened 23/23** against `corpus/goldens/*`
  (`busted coach_golden_spec.lua`). Output shape = the **Guidance contract**
  (`guidance-contract.json`). NOT wired live.
- **Phase 3 — Renderer + test mode (`Renderer.lua`).** `ns.Renderer.New(cfg)` →
  `:Draw(drawList)` turns a **DrawList** into pixels. Pure of decisions; the one
  impure line is the `handle → frame` registry. Bare-bones v1: **corner cue dots**
  (coloured by emphasis token, upper-right of the icon), **upper-left keybind
  hints**, a **proc glow** on the press cues (dot-scoped additive halo), a **titled
  sequence panel**, and a **discrete-pip resourceBar**. Driven by hand-authored
  DrawList fixtures via **`/cdmp rendertest <view>`** (`inventory`, `rotate`,
  `hand-of-guldan`, `burst-hold`, `opener-midflight`, `secrecy-combat`). Arbitrated
  by `busted renderer_spec.lua` (recording CreateFrame stub asserts colour / point /
  size / shown / rows). In-game verified + dialled in (distinct emphasis hues,
  prominent glow). Details: `w4-phase3-renderer-notes.md`. NOT wired live.

**The decision half and the draw half both exist and are tested in isolation. What
does not exist is the layer that connects them** — that is Phase 4.

---

## The two contracts the Binder sits between

### Input — Guidance (Coach output, cooldownID-keyed, colour-free)

```jsonc
{
  "resourceBar": { "value": 3, "max": 5, "incoming": 0, "display": "discrete",
                   "powerType": "SOUL_SHARDS" },
  "cues": {                                   // keyed by cooldownID (string)
    "34991": { "draw": true, "emphasis": "ROTATION" },
    "671":   { "draw": true, "emphasis": "JUDGE", "note": "hold for the window" }
  },
  "sequence": {                                // omitted/false => no panel
    "show": true, "title": "OPENER", "cursor": 2,
    "steps": [ { "spellID": 104316, "label": "Dreadstalkers", "keybind": "E",
                 "state": "done" }, /* … */ ]
  }
}
```

### Output — DrawList v1 (Renderer input, handle-keyed, geometry + token)

```jsonc
{
  "cues": [                                    // ARRAY; anchorTo = opaque handle / root token
    { "anchorTo": "<cooldownID>", "point": "TOPRIGHT", "relPoint": "TOPRIGHT",
      "dx": -3, "dy": -3, "size": 12, "emphasis": "ROTATION",
      "keybind": "R", "glow": true }
  ],
  "panel":       { "anchorTo": "UIPARENT", "point": "TOP", "dx": 0, "dy": -200,
                   "title": "OPENER", "steps": [ { "label": "…", "keybind": "E",
                   "state": "done" } ] },
  "resourceBar": { "anchorTo": "UIPARENT", "point": "BOTTOM", "value": 3, "max": 5,
                   "powerType": "SOUL_SHARDS" }
}
```

The Phase-3 fixtures in `Renderer.lua` (the `cue()` helper: `DOT` corner geometry +
`GLOW_EMPHASIS`, plus the `panel`/`shards` helpers) are the **reference for exactly
what a correct Binder must emit** — hand-authored today, Binder-produced next.

---

## Phase 4 — the Binder (the next unit)

**Goal:** a pure `Guidance + Layout → DrawList` translator, unit-tested off-game with
hand-authored Guidance + Layout fixtures. It is a **geometry/binding merge** — colour
stays out of it (the Renderer owns `emphasis → pixels`). Mirror the factory pattern:
`ns.Binder.New(cfg)` / `__index`, `Binder:Bind(guidance, layout) → drawList`.

**What it does:**
1. **cues:** `Guidance.cues{cooldownID → {emphasis, note}}` → `DrawList.cues[]`. For
   each cooldownID **present in the Layout** (i.e. currently displayed by the CDM),
   emit a cue with the corner-dot geometry, the `emphasis` token passed through, the
   **keybind** (from the action-bar scan, `HudBinds`, keyed by the entry's spellID),
   and the **glow** flag. Drop a cue whose cooldownID isn't in the Layout.
2. **panel:** `Guidance.sequence` → `DrawList.panel` (map `show`→present/omit,
   `title` through, `steps[].{label,keybind,state}` → rows; `cursor` is advisory).
   Self-anchored to `UIPARENT` at a config position.
3. **resourceBar:** `Guidance.resourceBar` → `DrawList.resourceBar` (value/max/
   powerType through; `incoming`/`display` handling per the bar's v1 capabilities).
   Self-anchored.

**The Layout input** (per `architecture.md` Stage 3): per-handle geometry from the
live CDM `RefreshLayout` hook — live, the set of displayed cooldownIDs (+ side/
column for corner choice); in test, a fixture supplies it directly. Because cues
anchor *relative to their frame* (`anchorTo` + corner offset), the Binder mostly
needs the Layout to know **which handles are displayed** and their side, not pixel
rects — keep the cue path handle-relative, reserve absolute rects for our own
self-anchored widgets (panel, bar).

**Open design questions to settle at the top of Phase 4** (don't assume):
- **Where does `glow` live?** Today the Phase-3 fixture `cue()` helper sets
  `glow = GLOW_EMPHASIS[emphasis]` (ROTATION/LATE). Recommend the **Binder** owns
  this rule (it's a binding decision), keeping the Renderer "draw what you're told."
  Confirm before coding.
- **Keybind source.** `Guidance.sequence` steps already carry `keybind`; the cue
  keybind must come from the **binds scan** (`HudBinds`) by spellID. Decide the
  lookup seam (cfg-injected function, like the Coach's `shardCost`).
- **cooldownID vs spellID.** Guidance keys cues by **cooldownID**; the binds scan and
  `SpecDemonology` key by **spellID**. The Layout/State is the bridge (it carries
  both). Pin down where the id-mapping happens (State pulse already has it).
- **Geometry constants** (dot corner/size, keybind corner, panel + bar positions):
  Binder config vs shared with the Renderer's fixtures. Recommend a single
  `layout`/`cfg` table so the fixtures and the Binder agree by construction.

**Verification (the off-game gate):** `busted CDMProbe/tests/spec/binder_spec.lua` —
hand-author a Guidance (or reuse a `corpus/goldens/*/guidance.json`) + a Layout
fixture, run `Binder:Bind`, and assert the DrawList matches the Phase-3 fixture for
that scenario (this **closes the loop**: Coach golden → Binder → the exact DrawList
the Renderer was dialled in against). Full suite + `luacheck CDMProbe/` stay green.
No release needed — Phase 4 is pure logic (like Phase 2). Syntax gate + luacheck +
busted only.

---

## Explicitly out of scope for Phase 4 (that's Phase 5 — live cutover)

- Populating the Renderer registry from the live CDM `RefreshLayout` hook
  (`cooldownID → Blizzard item frame`).
- State emitting live `mode` / `power.SoulShards.incoming`.
- Wiring `State → Coach → Binder → Renderer` on a ticker/event and running it live.
- Retiring `HudBoard` / `HudScore` / `HudChrome` (the old engine keeps painting the
  real `/cdmp hud` until this cutover).
- Live-CDM frame-stack details (sitting above Blizzard's swipe/cooldown child frames;
  the Phase-3 `DIALOG`-strata fix is for the bare test rig, not live icons).
- The `transient`/animation channel (phase-edge flash) and its verification story —
  a deferred later increment.

---

## Fresh-context starting checklist

1. `wowkb.addon pull --all` (these are separate gitignored repos).
2. `cd projects/cooldown-hud/addon && export PATH="$HOME/.luarocks/bin:$PATH"` then
   `luacheck CDMProbe/` + `busted CDMProbe/tests/spec` — confirm green baseline.
3. Read, in order: this doc → `w4-build-plan.md` §Phase-4 → `architecture.md`
   §Stage-3 (Binder/Layout) → `guidance-contract.json` → `Renderer.lua` fixtures
   (the target output) → `Coach.lua` Emit (the input producer).
4. Settle the four open design questions above (ask the user), then TDD the Binder
   against a golden-derived Guidance + a hand-authored Layout.

---

## Status — Phase 4 BUILT (2026-07-26)

The Binder is implemented and off-game-green. The four open questions were settled
per the plan's recommendations:

1. **`glow` lives in the Binder** — via the shared `G.glowFor(emphasis)` rule
   (ROTATION/LATE), so the Renderer stays "draw what you're told".
2. **Keybind via a cfg-injected `keybindFor(spellID)` seam** — live wraps
   `HudBinds`; the golden harness builds the map from the scenario's `state.json`.
3. **cooldownID ↔ spellID bridge is the Layout** — each displayed cooldownID carries
   its spellID; the Binder reads that map, never re-deriving identity.
4. **One shared geometry table** — `CDMProbe/HudGeometry.lua` (`ns.HudGeometry`)
   owns `DOT` / `GLOW_EMPHASIS` / `PANEL` / `BAR` and the `cue`/`resourceBar`/`panel`
   builders. **Both** the Binder and the Renderer's `/cdmp rendertest` fixtures call
   in, so they agree by construction (the fixtures' old `DOT`/`GLOW_EMPHASIS`/
   `shards()` locals were extracted into it).

**Files.** New: `CDMProbe/HudGeometry.lua`, `CDMProbe/Binder.lua`,
`CDMProbe/tests/spec/binder_spec.lua` (13 tests: cues geometry/keybind/glow/drop,
panel, resourceBar, and the close-the-loop against the fixtures). Modified:
`CDMProbe/Renderer.lua` (fixtures read `ns.HudGeometry`; pip layout reads
`BAR.pip/gap`) and `CDMProbe.toc` (HudGeometry + Binder before Renderer).

**One fixture correction found while closing the loop:** the `secrecy-combat`
rendertest fixture had the ROTATION cue's keybind as `"Q"` (Shadow Bolt's key) —
the golden state binds Demonbolt to `"F"`. Corrected to `"F"` so the fixture equals
what the Binder emits from that golden. No Renderer behaviour change.

**Gate:** `busted CDMProbe/tests/spec` 125/125 green, `luacheck CDMProbe/` clean,
luaparser syntax OK. No release (pure logic, like Phase 2).

**Phase 5 picks up** (unchanged from "out of scope" below): populate the Renderer
registry from the live CDM `RefreshLayout` hook, build the live Layout + the
`keybindFor` wrap of `HudBinds`, and wire `State → Coach → Binder → Renderer` on a
ticker/event.
