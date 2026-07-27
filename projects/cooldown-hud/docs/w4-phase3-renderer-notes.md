# W4 Phase 3 — the Renderer (bare-bones) + in-game test mode

*(Dated 2026-07-25. Records the DrawList-token decision, the bare-bones scope, and
the in-game screenshot findings, so a later reader doesn't re-litigate why colour
lives in the Renderer or why v1 draws static dots. Companions: `architecture.md`
§Stage-4 is the target shape; `w4-build-plan.md` §Phase-3 the plan;
`guidance-contract.json` the token→pixels rule; `corpus/goldens/` the states the
fixtures are mapped from.)*

## Status

**Off-game gate green.** `ns.Renderer.New(cfg)` turns a hand-authored DrawList into
pixels; `busted CDMProbe/tests/spec/renderer_spec.lua` (18 cases) drives it through
the recording CreateFrame stub and asserts per-handle colour, point, size,
shown-state, and the panel rows. Full suite `busted CDMProbe/tests/spec` stays green
(101/0 — the Phase-2 specs untouched by the mock change); `luacheck CDMProbe/` clean.

Scope was **the Renderer + an in-game test mode**, built in ISOLATION and driven by
hand-authored DrawLists — **no Binder** (that is Phase 4). The live HUD still paints
through `HudChrome`; the cutover is Phase 5. This is bottom-up build, integrate at
the end (build-plan P1).

## What shipped (bare-bones, the user's call)

- **Cue = a solid DOT in the icon's upper-right corner** (inside it, 3px inset),
  coloured by its `emphasis` token. No bar, no fill fraction. Diff-by-key on
  `anchorTo`: only handles in this DrawList are repainted; a dropped handle is
  hidden, never destroyed. *(Moved from below-the-icon to the corner at the user's
  request, 2026-07-25.)*
- **Keybind hint in the icon's upper-left.** The cue descriptor gained an optional
  `keybind` string; when present the Renderer draws an outlined hint (mono 14px,
  `ns.SetFont(..,"OUTLINE")`, KEY_COL near-white green) pinned to the icon's
  TOPLEFT. Live, the Binder fills it from the action-bar scan. *(Added 2026-07-25.)*
- **Proc glow on the press cue — the DOT glows, not the icon.** A `glow` flag on the
  cue draws a soft additive halo tinted to the dot's own emphasis hue, **~4.5× the dot**
  and centred on it — so it blooms **past the icon edges** (2026-07-26: "more
  prominent, even if it overlaps the edges") — breathing on a looping alpha bounce
  (**0.45→1.0**, high floor so it's always lit), one layer below the dot so the dot
  stays crisp. Scoped to the little
  cue like Demonic Core lighting Demonbolt, not the whole button. The fixtures glow
  ROTATION/LATE (the "press this now" signals) and leave JUDGE/SOON/SEQUENCE as plain
  dots so the glow keeps its meaning. *(Added 2026-07-25 — deliberately revises the
  bare-bones "static dots only" decision for this one element, at the user's request;
  the `transient` phase-edge flash below is still deferred. First cut glowed the
  whole icon via Blizzard's `ActionButton_ShowOverlayGlow`; changed to a
  dot-scoped self-rolled halo when the user asked to glow just the dot.)*
- **Sequence panel** — a plain titled list, one FontString row per step
  (`"<state>  <keybind>  <label>"`, tinted by state). Shown only when the DrawList
  carries `panel`; rows pooled, surplus hidden.
- **resourceBar** — a minimal discrete-pip row (`value` filled of `max`, powerType
  colour). Kept because it was trivial and every fixture wanted the shard count;
  happy to trim to dots+panel on review.
- **CRT chrome stays retired** (bracket / proc-glow *ring* / DEMO.SYS / scanlines —
  off in `HudChrome.lua:186-202`). Not revived. (The new proc glow is Blizzard's
  overlay-alert, a different thing from the retired hand-drawn border ring.)
- **No transient/animation for the DOTS.** They draw STATIC (the glow is a steady
  proc-style alert, not a transient). The `transient` phase-edge flash (the 0.4s
  juice) and its verification story (fired-id log vs staged capture, build-plan
  step 8's ⚠) are a **later Phase-3 increment**, not this item.

## The DrawList-token decision (why colour lives in the Renderer)

DrawList v1 carries the **emphasis TOKEN** (`ROTATION`/`LATE`/`SOON`/`JUDGE`/
`SEQUENCE`), **not** resolved RGBA. The Renderer resolves token → colour via a
built-in theme, injectable through `cfg.theme`.

This follows `guidance-contract.json`'s committed rule ("the Renderer owns
token → pixels for v1") and keeps colour **out of the Binder** — Phase 4 stays a
pure *geometry* merge (cooldownID → frame + anchor rect), with nothing to decide
about hue. It **deliberately supersedes** `architecture.md`'s older DrawList sketch
(`:326-337`), which showed a pre-resolved `color:[r,g,b,a]`; that doc itself says
the Stage-3/4 shape "is revised when the Binder is actually built (Phase 4)." So the
sketch's `color`/`fill`/`pulse`/`effects` fields are **not** the v1 contract — the
v1 DrawList is geometry + the emphasis token, and the Renderer is where a token
becomes a pixel.

### The theme (token → RGBA)

| token | RGBA | provenance |
|-------|------|-----------|
| `ROTATION` | `0.30 1.00 0.48` (green) | copied from `HudChrome` `CUE` (`:167`) — the canonical press-green |
| `LATE` | `1.00 0.42 0.10` (amber) | **diverged** from `CUE`'s green — see glanceability note |
| `SOON` | `1.00 0.86 0.15` (yellow) | copied from `HudChrome` `CUE` (`:166`) |
| `JUDGE` | `0.27 0.88 1.00` (cyan) | copied from `HudChrome` `CUE` (`:165`) |
| `SEQUENCE` | `0.64 0.42 1.00` (violet) | **diverged** from the summon fel-green — see glanceability note |
| `SOUL_SHARDS` (power) | `0.690 0.420 1.000` | `HudChrome` rail GENERATE soul-violet (`:1051`) |

**Glanceability (2026-07-26).** The first cut kept `ROTATION`/`LATE`/`SEQUENCE` all
in the green family (`LATE` a brighter green, `SEQUENCE` the summon fel-green) and
in-game they read as the same colour. So `LATE` and `SEQUENCE` were pulled off the
green — `LATE` = hot amber ("overdue, catch up"), `SEQUENCE` = violet ("look at the
panel, not a press"). `ROTATION`/`SOON`/`JUDGE` still match `HudChrome`'s `CUE`. The
five tokens are now guarded pairwise-distinct by a busted test (min colour distance
> 0.30). Retuning the theme is a local edit, no release (no new observation — same
collect-vs-assert rule).

### The registry — the one impure line

`registry[anchorTo]` is the sole impure surface in the draw path. `anchorTo` is an
opaque handle or a root token; the Renderer never interprets it beyond the lookup.
Live mode will map `cooldownID → CDM item frame`; test mode maps `"fake1" → a
placeholder square`. `UIPARENT` is pre-registered in `New` so a hand-authored panel
/ bar can anchor to the screen with no ceremony. An unknown emphasis token draws
**nothing** (never guess a colour) — an unknown handle skips its `SetPoint` but the
dot is still created (colour is honest even if the anchor is missing).

## The in-game test mode — `/cdmp rendertest [<name>|off|list]`

Registered in `Core.lua`, implemented in `Renderer.lua` (`ns.RenderTest`). Builds N
bordered placeholder icon squares in a centred row, registers them under
`fake1..fakeN`, and renders a hand-authored DrawList **fixture** through a persistent
test Renderer. No game decisions — placeholder frames + fixtures + Renderer, the
exact shape Phase 4's Binder will one day produce.

The scenario fixtures are each mapped **by hand** from a representative golden state
(that by-hand cooldownID → fake-handle mapping is precisely the Binder's Phase-4
job). Two non-scenario views round out the dial-in kit:

| view | what it draws | purpose |
|------|---------------|---------|
| `inventory` | one dot of EVERY emphasis token side by side, captioned (ROTATION·LATE·SOON·JUDGE·SEQUENCE) | the reference card — the whole palette + which tokens glow, at a glance. Bare `/cdmp rendertest` defaults here |
| `rotate` | 5 panels, one ROTATION cue hopping between them on a 0.8s `C_Timer` | live demo of diff-by-key movement + the glow tracking the dot across icons. `off` (or any view change) stops the ticker |
| `hand-of-guldan` | one ROTATION dot + 3/5 shards | the single gated press |
| `burst-hold` | ROTATION + 2× JUDGE + 3/5 shards | one press, two your-call holds |
| `opener-midflight` | SEQUENCE dot + OPENER panel (done/active/pending/blocked/skipped) + 3/5 | the panel carries the plan |
| `secrecy-combat` | ROTATION + SOON + 2/5 shards | press + napkin anticipation |

## In-game screenshot findings (3f)

> **TODO — fill after the release + in-game pass.** Deploy `wowkb.addon release
> cdmp`, `/reload`, cycle `/cdmp rendertest <name>` for each fixture, screenshot,
> and record: does the green ROTATION dot read under its icon? Are the cyan JUDGE
> dots distinct from green? Is the yellow SOON legible? Does the OPENER panel's
> done/active/pending/blocked/skipped tinting read at a glance? Note any size /
> offset / hue tuning applied (theme + `DOT`/pip constants are the dials).
