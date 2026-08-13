# Combat Assist Plus — the render shelf

**What this file is for:** how cap is allowed to *look*. `pattern-shelf.md` answers **which facts
you may use**; this answers **how you may show them**. It owns every visual opinion in the
project — surfaces, primitives, colors, motion, placement, composition — so that trying something
new means editing this file, not arguing with the constitution.

**This file declares one style.** It is not a debate. Every primitive below states **the**
treatment, in the present tense, with no alternative beside it. If the style is wrong, the fix is
to *change this file*, not to add a second option next to the first — an artifact rendered from a
shelf with two answers renders neither. Alternatives that were considered, the reasoning behind a
choice, and what was tried and rejected live in **`render-rationale.md`**, which has no authority
over anything.

**Opinions here are still cheap.** Nothing in this file is a boundary. `spec.md` says cap must
never compute the press or branch on a sealed value — those are *product boundaries* and they do
not move. Whether a hold reads as an ✕ or a dimmed border, whether lanes pulse or sit still,
whether a cue lives in the icon's center or its corner: all of that lives here, and changing one
is a normal edit, not a spec amendment.

**Who reads it.** The artifact generator (`wowkb.capart`, which renders a design artifact as the
client would actually draw it) and the addon renderer (`Treatment.lua` / `Overlay.lua`). Both cite
this file rather than each carrying their own numbers — that divergence is the specific failure
this file exists to end.

**Where the numbers are.** In **Part 6**, the `render-tokens` JSON block, and nowhere else. Prose
in this file cites a token path (`tokens.pulse.floor`) and never restates its value, because a
number written twice is a number that will disagree with itself. `Treatment.lua` transcribes the
block; `wowkb.capart` parses it.

**Status vocabulary.** There is only one status word left, and it marks a *fact gap*, not a
design debate:

- **open** — the client capability this primitive would need has not been measured
  (`spec.md` §3.6 routing). The style is still declared; what is unknown is whether the client can
  draw it. An artifact stamps a visible ⚠ chip on an `open` primitive so the preview never lies
  about what ships.

Everything not marked `open` is simply the style.

---

## Part 0 — the loop this file is built for

1. Edit a recipe here — a color, a rate, a placement, a whole new primitive. Numbers go in
   **Part 6**.
2. `uv run python -m wowkb.capart build havoc` — the artifact reads this file's tokens.
3. Look at it. Ask for tweaks. Go to 1.
4. When it looks right, `Treatment.lua` transcribes Part 6 verbatim.

Nothing in steps 1–3 requires permission from `spec.md`. If a change here would make cap compute
the press or branch on a sealed value, *that* is the one thing to stop and check — and it is a
§3.6 / §4 question, not a taste question.

**The artifact is a reproduction, not a diagram.** It draws real Blizzard icon art at real
Cooldown Manager size, real extracted flipbook sheets at their real frame counts and durations,
and composites cap's treatments the way the client would composite them — `SetVertexColor` as a
multiply, never a hue rotation. A preview that recolors art the client could not recolor is worse
than no preview. `wowkb.capart` enforces that mechanically (Part 4).

---

## Part 1 — Surfaces (what there is to draw on)

A Cooldown Manager row is a small square icon. These are the places a cue can live. Placement is
a design choice, not a platform constraint, unless marked otherwise.

| Surface | Where | Carries | Notes |
| --- | --- | --- | --- |
| **Icon face** | the art itself | desaturation, veil, whole-icon alpha | Blizzard's own dim/uninteractable channel. |
| **Border ring** | just outside the icon edge | emphasis / role lane | Flipbook glows draw *outside* the host, hence `tokens.rings.emphasis.host_scale` > 1. |
| **Center cue row** | horizontal strip across the icon's middle | 1–`tokens.surfaces.center_row.max` small textures side by side | The general slot for non-numeric cues (hold, overcap, banked). Grows outward from center. |
| **Corner slots** | the four corners | one dot / small glyph each | Blizzard already uses bottom-right for charges and bottom for keybind text — cap uses the **top** corners. |
| **Cooldown swipe** | the radial dial | remaining time | Can be *restyled* without knowing the time (see V7). |
| **Count tile** | Blizzard's own aura count position | a sealed stack number | Client-owned; cap never learns the value. |
| **Independent bar** | anywhere on screen | one duration, large | Off-icon surface; costs screen space and must earn it. |

⚠ **Not a design choice:** cap draws on its **own frame parented to `UIParent`**, anchored to the
CDM item frame — it must never reparent onto or restyle a live Cooldown Manager frame. Since 12.1
those frames participate in secure aura plumbing, and decorating them is what got ClientLab's
`Glow.lua` and `Cue.lua` retired from the `.toc`. This is a platform rule, not taste.

---

## Part 2 — Primitives

Each recipe: what it means, the Blizzard art (or ours), the token path its numbers come from, a
Lua sample, and how the artifact reproduces it.

### V1 · Emphasis ring — flipbook glow

The role-lane treatment: an animated glow ring outside the icon edge, tinted to the lane's hue and
pulsed at the lane's rate.

- **Art:** `visualalert_ants_flipbook` (`tokens.rings.emphasis.atlas`). It is the **neutral**
  sheet — measured mean saturation **0.00** in `raw/uiart/manifest.json` — which is what makes a
  multi-hue lane ladder drawable at all: `SetVertexColor` multiplies, so only near-neutral art
  reaches an arbitrary hue at full strength. Every other candidate ring carries a baked hue and
  can therefore carry exactly one lane. That measurement, not taste, is why this sheet is the one.
- **Geometry:** `tokens.rings.emphasis.grid` / `.frames` / `.duration_s`, and
  `.host_scale` because the ring draws *outside* the host and would otherwise sit on the icon edge.
- **Tint:** `tokens.rings.emphasis.tint` = `lane` — the ring takes the hue of whichever lane the
  row is in (`tokens.lanes.<LANE>.rgb`).
- **Lua:**
  ```lua
  local ring = frame:CreateTexture(nil, "OVERLAY")
  ring:SetAtlas(T.rings.emphasis.atlas)              -- neutral art: tints cleanly
  ring:SetPoint("CENTER")
  ring:SetSize(icon:GetWidth() * T.rings.emphasis.host_scale,
               icon:GetHeight() * T.rings.emphasis.host_scale)
  ring:SetVertexColor(unpack(T.lanes[lane].rgb))     -- multiply: works because the art is neutral
  local anim = ring:CreateAnimationGroup()
  local flip = anim:CreateAnimation("FlipBook")
  flip:SetChildKey("Texture")
  flip:SetFlipBookRows(T.rings.emphasis.grid.rows)
  flip:SetFlipBookColumns(T.rings.emphasis.grid.cols)
  flip:SetFlipBookFrames(T.rings.emphasis.frames)
  flip:SetDuration(T.rings.emphasis.duration_s)
  anim:SetLooping("REPEAT"); anim:Play()
  ```
- **Artifact reproduction.** A sprite sheet laid out `rows × cols` cannot be walked by one
  `steps()` animation on one axis — that plays only the first row. It takes **two** animations,
  the fast one stepping columns and the slow one stepping rows:
  ```css
  .ring {
    background-image: url(<sheet data URI>);
    background-size: calc(100% * var(--ring-cols)) calc(100% * var(--ring-rows));
    animation: flipx calc(var(--ring-dur) / var(--ring-rows)) steps(var(--ring-cols)) infinite,
               flipy var(--ring-dur) steps(var(--ring-rows)) infinite;
  }
  @keyframes flipx { to { background-position-x: calc(100% * var(--ring-cols) / (var(--ring-cols) - 1) * -1 + 0%); } }
  @keyframes flipy { to { background-position-y: 100%; } }
  ```
  (`capart` emits the exact percentages; the shape is what matters here.) The tint is
  `background-color` + `background-blend-mode: multiply`, which is what `SetVertexColor` does —
  **never** `filter: hue-rotate`, which would recolor art the client cannot recolor.
- **Extract it:** `uv run python -m wowkb.uiart atlas visualalert_ants_flipbook --grid 6x5`

### V2 · *(retired)*

The four-strip static `SetColorTexture` border. Superseded by V1 + V3; it existed only to satisfy
the "motion only for a specific observed problem" rule, which is struck. What the shipped addon
still draws is not a shelf statement — see `backlog.md` → `## Status`, and `render-rationale.md`
for why the static border was the baseline and why it stopped being one. The number is kept out of
this file deliberately: two border vocabularies in one shelf is the divergence this file exists to
end.

### V3 · Pulse

Motion is the **primary** ranking channel; hue is redundant reinforcement. Each lane pulses its
emphasis ring at its own rate.

- **Rates:** `tokens.lanes.<LANE>.pulse_hz` — three *different* rates, deliberately. A set that
  pulses in lockstep reads as one flashing area rather than a ladder.
- **Depth:** `tokens.pulse.floor` is the trough invariant — the pulse multiplies the lane's alpha,
  so depth eats separation, and the floor is the number that keeps the middle lane's trough clear
  of the low lane's peak. It is load-bearing arithmetic, not a taste dial; the derivation is in
  `render-rationale.md`. The top two lanes cross by design and are told apart by *rate*.
- **Safety, not taste:** every icon gets a phase offset, `tokens.pulse.phase_offset_s` × its index.
  A row of icons flashing in sync is a WCAG 2.3.1 problem; the same row flashing independently is
  not. Text cues additionally cap at `tokens.pulse.text_max_hz` / `tokens.pulse.text_duty` with an
  alpha floor of `tokens.pulse.text_alpha_floor` (MIL-STD-1472F).
- **Lua:** one `Alpha` animation, `tokens.pulse.smoothing`, `tokens.pulse.loop`, duration
  `0.5 / hz` — `BOUNCE` plays forward then back, so half a cycle is the whole pulse and no timer
  runs.
  ⚠ `SetFromScale` / `SetToScale` **do not exist**; the setters are `SetScaleFrom` / `SetScaleTo`.
  Probe before calling — an animation that silently never received its endpoints looks exactly
  like a live one.

### V4 · Veil (de-emphasis)

Dim what cap has an opinion *against*, rather than only brightening what it favors. A veiled row
is still perfectly legible; it has just stopped competing.

- **Value:** `tokens.veil.alpha` of `tokens.veil.rgb` over the icon face.
- **Applies to:** every verdict whose `veil` is true in `tokens.verdicts` — the skipped rows of a
  walk, in short.

### V5 · Center cue row

The general answer to "a non-numeric cue needs a texture, in the middle, and several may coexist."

- **Layout:** up to `tokens.surfaces.center_row.max` textures at
  `tokens.surfaces.center_row.height_pct` of icon height, laid out horizontally and centered as a
  group, so one cue sits dead center and two straddle it. Order is fixed by cue identity, never by
  arrival, so a given cue is always in the same place.
- **Members:** hold ✕ (C2, sealed), overcap mark (B negative), banked ✓ (B positive, **open**).
- **Art:** ours to author (Part 4) — white-alpha shapes, so each tints independently.
- **Rule of thumb:** if a fourth cue wants in, one of the three is not earning its slot.

### V6 · Corner dot

A `tokens.surfaces.corner_dot.size_px` square in a **top** corner, one readable dependency fact
each: **green = the related ability is on cooldown** (the dependency is satisfied — go),
**red = it is ready** (wait). Colors are `tokens.cues.dot.go` / `tokens.cues.dot.wait`.

- Demonology uses one dot per row (Dreadstalkers, Grimoire). Havoc needs **two on one icon** —
  Metamorphosis's Eye Beam and Death Sweep reset dots — so cap fills `TOPLEFT` first, then
  `TOPRIGHT`. The bottom corners stay Blizzard's: charges bottom-right, keybind text bottom.

### V7 · Swipe restyle

The dial can be repainted without knowing the time it shows: `SetSwipeColor`, `SetSwipeTexture`,
`SetEdgeTexture`, `SetDrawSwipe`, `SetDrawEdge`, `SetHideCountdownNumbers`, `SetCountdownFont`,
`SetReverse`, `SetRotation` carry **no timing**.

cap leaves the swipe at Blizzard's default: `tokens.surfaces.swipe.color` is the stock dark wash,
and the swipe is the CDM's own "ruled out" signal, which cap has no reason to restate.

⚠ `RefreshSpellCooldownInfo` re-applies `SetSwipeColor` + `SetDrawSwipe` on **every** refresh, so
a one-shot restyle is silently clobbered — `hooksecurefunc` per instance and be the last writer.

### V8 · Sealed count tile

An `AuraContainer` writes a secret application count straight into a static outlined FontString
(`FRIZQT__.TTF`, `tokens.surfaces.count_tile.size`, `OUTLINE`, anchored `TOP` +1). Human verdict
recorded: at 1 stack, icon and swipe with no number; at 2 stacks, the number appeared. cap reports
`offered` / `armed` / `refused` and never learns whether the glyph drew.

### V9 · Sealed color curve

A secret resource is handed to the client with an authored **color curve**; the client evaluates it
against the value and paints. The break point is a baked number, not a comparison cap performs.
Both polarities work — the negative overcap readout and the positive banked cue are the same
mechanism. Feature-gate `C_CurveUtil.CreateCurve` / `Enum.LuaCurveType.Step` /
`Enum.DurationTimeModifier.RealTime`; on any missing piece take the inert path. Curves and
durations are `userdata`, not tables.

### V10 · Sealed range-gated texture

A sealed remaining-duration drives a texture's visibility only while the time sits inside an
authored band — the hold ✕ drawn without Lua reading the clock. Sinks that carry secrecy inside a
duration object: `SetTimerDuration`, `SetCooldownFromDurationObject`. Sinks that take a secret
directly: `SetAlpha`, `SetDesaturation`, `SetValue`, `SetText`, `SetApplicationCount`.
**Never read back** — a capture may say `offered` / `armed` / `refused`, never `drew`.

---

## Part 3 — Composition rules

- **`SetVertexColor` multiplies.** Baked-hue art can only be darkened toward its own hue. The
  style therefore uses neutral art (V1). Desaturate-then-tint (`SetDesaturated(true)` /
  `SetDesaturation(0..1)` first, tint the result — `knowledge/addon-dev/frames-textures-animation.md:1044-1052`)
  is the escape hatch for baked art, and whether it yields a *clean* hue is **open**: unmeasured
  in client. A primitive declaring `tint: "desaturate+lane"` builds, but the artifact stamps a
  visible ⚠ on it.
- **Don't bundle Blizzard art.** Reference an atlas by name — that ships no asset. Extracted art is
  for measuring and for the artifact, never for the addon's `Media/` folder.
- **One dial, three parts.** Perceived spin rate = angular velocity × the sprite's symmetry order.
  Art, scale and duration are not independent; changing the sheet changes the felt speed.
- **`SetGradient` resets vertex color to white.** Apply the gradient first, tint second.
- **`SetTexture` / `SetAtlas` / `SetColorTexture` are exclusive** — last call wins. `GetTexture()`
  after `SetAtlas` returns the backing fileID as a *number*, not nil; ask `GetAtlas()` first.
- **Animations don't restore vertex color on stop** without `SetToFinalAlpha`.
- **`Show`/`Hide`, never `SetShown`** — `SetShown` is a protected function.
- **Set frame strata/level out of combat only.** In combat, confine writes to
  `Show`/`Hide`/`SetVertexColor`/`SetAlpha`.
- **Stock proc glow coexists.** cap dims Blizzard's own overlay to `tokens.surfaces.proc_glow_alpha`
  via `hooksecurefunc(frame, "RefreshOverlayGlow")`. That is a dial for an eyeball, not a measured
  value, and `SetAlpha` reports nothing back.

---

## Part 4 — Assets

**Extraction is a tool, not a chore:** `wowkb.uiart`.

```bash
uv run python -m wowkb.uiart find flipbook                              # search atlas members
uv run python -m wowkb.uiart atlas visualalert_ants_flipbook --grid 6x5 # extract + grid + CSS recipe
uv run python -m wowkb.uiart icon 191427 198013 --data-uri              # spell icons for the artifact
uv run python -m wowkb.uiart manifest                                   # what we have, with tintability
```

It resolves `UiTextureAtlasMember` → sheet `FileDataID` → CASC bytes → BLP decode → the member's
crop, records everything in `raw/uiart/manifest.json`, and **measures tintability** (mean HSV
saturation over visible pixels; `< 0.15` = neutral) so "can this carry our hues" is data.

Two gotchas it already handles, both real: `wago.tools/api/casc` needs a **browser User-Agent** or
it stalls silently, and Pillow raises `Unknown BLP encoding 3` on Blizzard's uncompressed-BGRA UI
sheets, which we decode ourselves.

**Our own art.** For shapes the client has no neutral version of (hold ✕, cue pips, bands): author
white-alpha sheets from a script beside this file, so they regenerate rather than accumulate as
binary mystery. Fully tintable, fully ours, no licence question. CC0 packs (Kenney) are the other
acceptable source; there is precedent.

**The artifact contract, and the guard that enforces it.** Icons and sheets embed as base64
`data:` URIs — the artifact CSP blocks every external host, so a CDN `<img src>` renders nothing.
`wowkb.capart` refuses to build a lie:

| Condition | What happens |
| --- | --- |
| `tint: "lane"` on art the manifest measured `tintable: false` | **hard error**, naming the measured saturation |
| a CSS tint written as `hue-rotate` | not emitted — the tint path is `background-color` + `multiply` |
| `tint: "desaturate+lane"` | builds, and stamps a visible ⚠ *open* chip on that primitive |
| `grid.rows × grid.cols ≠ frames`, or a grid that does not divide the crop evenly | **hard error** |
| total base64 over `tokens.budget.max_base64_kb` | **hard error**, with a per-asset table |

The asset list and the budget are `tokens.assets` / `tokens.budget`.

---

## Part 5 — What a flight would settle

Look-at-it questions, not measurements. None of them is a reason to hold two styles in this file.

1. Do the three lanes rank on real icon art at real size — with motion primary, does the eye go
   to the fastest ring first?
2. Does the veil (V4) read as helpful contrast or as cap hijacking the whole CDM?
3. Two dots on one icon (V6) — do green/red read as go/wait without a legend?
4. Does the neutral ants ring (V1) tinted to a lane hue coexist with Blizzard's stock proc glow,
   or compete with it?
5. Does desaturate-then-tint produce a clean hue on baked art? — **open**, needs the client.

---

## Part 6 — The tokens

**This block is the style.** Every number cap draws with is here and nowhere else. `Treatment.lua`
transcribes it; `wowkb.capart` parses it; prose cites paths into it. Editing a value here and
rebuilding the artifact is the whole loop.

Colors are `[r, g, b]` in 0–1, the way `SetVertexColor` wants them.

<!-- render-tokens v1 -->
```json
{
  "version": 1,
  "lanes": {
    "COOLDOWN": { "rgb": [1.00, 0.92, 0.55], "alpha": 1.00, "thickness_px": 3, "pulse_hz": 2.5 },
    "ROTATION": { "rgb": [0.45, 0.70, 0.95], "alpha": 0.78, "thickness_px": 2, "pulse_hz": 1.2 },
    "FALLBACK": { "rgb": [0.80, 0.82, 0.88], "alpha": 0.50, "thickness_px": 1, "pulse_hz": 0.5 }
  },
  "pulse": {
    "floor": 0.68,
    "phase_offset_s": 0.11,
    "smoothing": "IN_OUT",
    "loop": "BOUNCE",
    "text_max_hz": 2.0,
    "text_duty": 0.70,
    "text_alpha_floor": 0.65
  },
  "veil": { "rgb": [0.00, 0.00, 0.00], "alpha": 0.60 },
  "promotion": { "scale": 1.08, "alpha": 1.00, "ring_boost_hz": 0.0 },
  "rings": {
    "emphasis": {
      "atlas": "visualalert_ants_flipbook",
      "grid": { "rows": 6, "cols": 5 },
      "frames": 30,
      "duration_s": 1.0,
      "host_scale": 1.47,
      "tint": "lane"
    },
    "alert": {
      "atlas": "ui-cooldownmanager-alert-flipbook",
      "grid": { "rows": 11, "cols": 2 },
      "frames": 22,
      "duration_s": 0.75,
      "host_scale": 1.40,
      "tint": "none"
    }
  },
  "surfaces": {
    "icon_px": 56,
    "row_gap_px": 6,
    "border_px": 1,
    "swipe": { "color": [0.00, 0.00, 0.00], "alpha": 0.72 },
    "center_row": { "max": 3, "height_pct": 40, "gap_px": 2 },
    "corner_dot": { "size_px": 7, "inset_px": 1 },
    "count_tile": { "font": "FRIZQT__.TTF", "size": 14, "outline": "OUTLINE" },
    "proc_glow_alpha": 0.5
  },
  "cues": {
    "dot": { "go": [0.30, 0.85, 0.35], "wait": [0.95, 0.30, 0.30] },
    "hold": { "glyph": "cross", "rgb": [0.95, 0.30, 0.30], "open": false },
    "overcap": { "glyph": "bar", "rgb": [0.95, 0.30, 0.30], "open": false },
    "banked": { "glyph": "check", "rgb": [0.45, 0.95, 0.55], "open": true },
    "weave": { "glyph": "chevron", "rgb": [1.00, 0.92, 0.55], "open": false }
  },
  "verdicts": {
    "cd":             { "emphasis": "none",      "veil": false, "swipe": true,  "cues": [] },
    "weave":          { "emphasis": "lane",      "veil": false, "swipe": false, "cues": ["weave"] },
    "hold-readable":  { "emphasis": "none",      "veil": true,  "swipe": false, "cues": [], "dots": true },
    "hold-sealed":    { "emphasis": "none",      "veil": true,  "swipe": false, "cues": ["hold"] },
    "starved":        { "emphasis": "none",      "veil": true,  "swipe": false, "cues": [], "desaturate": 1.0 },
    "overcap":        { "emphasis": "none",      "veil": true,  "swipe": false, "cues": ["overcap"] },
    "withheld":       { "emphasis": "none",      "veil": true,  "swipe": false, "cues": [] },
    "press":          { "emphasis": "lane",      "veil": false, "swipe": false, "cues": [] },
    "press-promoted": { "emphasis": "promoted",  "veil": false, "swipe": false, "cues": [] },
    "below":          { "emphasis": "none",      "veil": false, "swipe": false, "cues": [] }
  },
  "assets": {
    "sheets": ["visualalert_ants_flipbook", "ui-cooldownmanager-alert-flipbook"],
    "icon_size": 56,
    "encode": "webp",
    "quality": 90
  },
  "budget": { "max_base64_kb": 512 },

  "lab": {
    "_comment": "NO AUTHORITY. Part 7. Nothing in `verdicts` or `cues` may name anything in here; capart enforces it. A treatment leaves the lab by being MOVED into Parts 1-6, never by being cited from here.",
    "asset_root": "artifacts/assets/kenney",

    "border-arrival": {
      "title": "Solid border, animated only on arrival",
      "asks": "Does a static border plus a one-shot snap-in read better than a ring that pulses forever? And does a fourth CHARGES lane on the border carry its own meaning, or just add a colour nobody decodes?",
      "lanes": {
        "COOLDOWN": { "rgb": [1.00, 0.82, 0.22], "thickness_px": 3 },
        "ROTATION": { "rgb": [0.35, 0.68, 1.00], "thickness_px": 2 },
        "FALLBACK": { "rgb": [0.78, 0.80, 0.86], "thickness_px": 1 },
        "CHARGES":  { "rgb": [0.62, 0.42, 0.95], "thickness_px": 2 }
      },
      "arrival": {
        "from_scale": 2.00,
        "duration_s": 0.35,
        "smoothing": "OUT",
        "from_alpha": 0.00,
        "replay_every_s": 5.0
      },
      "triggers": [
        { "key": "cooldown-ready", "lane": "COOLDOWN", "ability": "Metamorphosis",
          "label": "came off cooldown" },
        { "key": "charge-returned", "lane": "CHARGES", "ability": "Immolation Aura",
          "label": "a charge came back" },
        { "key": "now-affordable", "lane": "ROTATION", "ability": "Chaos Strike",
          "label": "resource arrived — was starved, now castable" }
      ]
    },

    "badge-slots": {
      "title": "OS-style corner badges",
      "asks": "Read at 56px without a legend? Does a filled badge at ~1/3 icon width beat a 7px pip, and do three slots crowd the face?",
      "diameter_pct": 34,
      "padding_px": 3,
      "slots": [
        { "id": 1, "anchor": "top-right-corner" },
        { "id": 2, "anchor": "left-of-1-along-top" },
        { "id": 3, "anchor": "below-1-along-right" }
      ],
      "plate": { "rgb": [0.00, 0.00, 0.00], "alpha": 0.78, "scale": 1.12 },
      "badges": {
        "flask": {
          "means": "resource — filling toward a bank, or blocked short of overflowing",
          "frames": ["flask_empty", "flask_half", "flask_full"],
          "duration_s": 1.60, "loop": "BOUNCE", "rgb": [0.45, 0.95, 0.55]
        },
        "timer": {
          "means": "held for a cooldown, or deprioritised while something else is up. The sweep is a steady pace, NOT elapsed time.",
          "frames": ["timer_0", "timer_CW_25", "timer_CW_50", "timer_CW_75", "timer_100"],
          "duration_s": 2.00, "loop": "REPEAT", "rgb": [1.00, 0.72, 0.25]
        }
      }
    }
  }
}
```

**Reading the verdict table.** `emphasis` is which ring a row wears — `none`, its `lane` ring, or
the `promoted` form (the lane ring plus `tokens.promotion`). `veil` is V4. `swipe` is Blizzard's
own dial, which cap does not draw and does not restyle (V7); it appears here so the artifact can
reproduce the row faithfully. `cues` names center-row members (V5) by key into `tokens.cues`;
`dots` turns on the V6 corner dots the scenario supplies. A cue whose token carries `open: true`
draws with a ⚠ chip in the artifact and produces **no hint in the addon** until it is measured
(`spec.md` §3.6).

**The verdict vocabulary is closed.** These ten keys are the whole set a scenario may use;
`wowkb.capart` errors on anything else.

---

## Part 7 — The lab

**Everything above this line is the style. Nothing below it is.**

Parts 1–6 declare one treatment per primitive because a document holding two answers cannot be
rendered — the generator would have to choose, which puts the decision back in the tool. That rule
stands. But it made *trying* something expensive: the only way to see a new idea was to overwrite
the declared style and remember to put it back. So the lab is where an idea gets drawn without
being adopted.

**The four rules, and `wowkb.capart` enforces the first one.**

1. **Nothing in `verdicts` or `cues` may name anything in `lab`.** The lab is unreachable from
   `havoc/scenarios.md` by construction — a scenario cannot accidentally start depending on an
   experiment. `capart build` errors if the reference exists.
2. **The lab never draws in a CDM row.** It renders in its own section of the artifact, under its
   own heading, after the declared primitives.
3. **The lab has no authority.** It is not a proposal, a shortlist, or a plan of record. It is
   pixels you can look at. `render-rationale.md` argues; the lab *shows*; neither decides.
4. **A treatment leaves the lab by being MOVED**, into Parts 1–6 with its numbers, and deleted from
   here. Never by being cited from here. If two entries survive a flight, one of them still loses.

Each entry carries an `asks` — the question it exists to answer. An entry that cannot say what it
is asking is decoration and should be deleted.

### L1 · `border-arrival` — a solid border, animated only when something arrives

The declared style rings every emphasised icon and pulses it forever. This asks whether the
opposite reads better: a **static** solid border carrying the lane, plus a **one-shot** animation
at the moment the state changes — the border drawn at `arrival.from_scale` (2×) and snapping down
onto the icon over `arrival.duration_s`.

It reverts V2's superseded four-strip border deliberately. Two reasons it is worth re-asking:
CDMProbe measured that **60 % of real cue-set changes are swaps**, so continuous motion spends its
budget on states that are about to be replaced, while an arrival transient spends it exactly on the
change; and the one flown verdict we have on continuous rings — *"the tier glows read as candles"*
— traced to how much of the row was lit at once, which a static border makes cheap.

It adds a fourth lane, **CHARGES**, which the declared style does not have. Three triggers fire the
same animation from three different causes: a cooldown finishing, a charge returning, and a spender
becoming affordable. If one animation cannot carry three meanings, this entry has answered its own
question.

⚠ The artifact replays each trigger on a timer (`arrival.replay_every_s`) so it can be watched. In
the addon the animation fires **on the event and then stops**; the loop is a viewing aid and is not
part of what is being proposed.

### L2 · `badge-slots` — OS-style corner badges

Windows/mobile-style: a filled circular badge whose centre sits **on** the icon's top-right corner,
so it half-overhangs the face. Slot 2 sits one diameter-plus-padding to its left along the top
edge; slot 3 the same distance below it down the right edge. Three slots, `diameter_pct` of the
icon width each, each on a dark plate for contrast against busy icon art.

The art is Kenney's CC0 **Board Game Icons** (`lab.asset_root`, license vendored beside it),
measured **saturation 0.000** — white with the shape in the alpha channel, so `SetVertexColor`
multiplies it to any lane hue at full strength. This is the same reason CDMProbe shipped Kenney's
`star_07` rather than a Blizzard atlas: neutral art we own beats hunting for neutral art we do not.

Two badges animate:

- **`flask`** — `flask_empty → half → full`, bouncing. Resource filling toward a bank, or a press
  blocked short of overflowing.
- **`timer`** — `timer_0 → CW_25 → CW_50 → CW_75 → timer_100`, repeating. Held for a cooldown, or
  deprioritised while something else is up. ⚠ **The sweep is a steady pace and does not signify
  elapsed time** — it is a "waiting" glyph, not a dial. If it reads as a countdown, that is a
  finding and the entry has failed.

It replaces the 7 px V6 corner dot with something roughly a third of the icon width, which is the
size the flat-UI convention uses for exactly this job.

⚠ **Slot 3 runs toward BOTTOMRIGHT, which Blizzard owns** (`ChargeCount` on tab 1, `Applications`
on tab 2, both anchored −2/+2). Slot 3 should clear it at these numbers, but that is arithmetic on
a 12.0.7 source read, not a measurement. Slots 1 and 2 are on the top edge, which is free.
