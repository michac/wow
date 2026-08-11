# Glow palette — a highlight-picker in ClientLab

## Why this exists

We need to choose **highlight treatments for our own addons** (cap's tier signal first)
and there is no way to judge a glow except to look at one, at the real size, on the real
icon, in the real colour. This adds a browser to the lab: every glow LibOrbitGlow can
play, drawn on a sample square *and* on live Cooldown Manager item frames, in cap's tier
hues.

It is a **picker, not a test**. It registers no `ns.Test{}` ids and no `questions.json`
rows — same footing as `CDMSweep.lua`, which also probes without asserting. The lab's
registry cross-check must be untouched by this work.

**Nothing in a product addon may depend on ClientLab** (the one invariant). The output of
this work is a *decision* — "use glow X at colour Y for HIGH" — which later gets built
into cap by embedding LibOrbitGlow there directly.

## ⚠ Licensing — the hard constraint

Two upstream repos, two different licenses. Getting this wrong is the one unrecoverable
mistake in this task.

| Repo | License | What we may do |
|---|---|---|
| `raw/addon-research/LibOrbitGlow` | **MIT** | vendor the `LibOrbitGlow-1.0/` folder into ClientLab, keep its `LICENSE` alongside |
| `raw/addon-research/Orbit-Glow-Pack` | **All Rights Reserved** | read it to understand the registry contract. **Nothing else.** |

**Do NOT copy, move, re-encode, generate-from, or check in any file under
`Orbit-Glow-Pack/Textures/`** — not into ClientLab, not into cap, not anywhere. All 332
`.tga` files are the author's exclusive property. The pack is a *reference clone* only.

That costs us nothing, because the library is designed for exactly this: the pack is a
separate addon the **user installs themselves** from CurseForge ("Orbit Pack: Glows"),
and its 44 glows then appear in `lib:GetGlowList()` automatically with zero code on our
side. The palette must therefore be built to render **whatever is registered**, never a
hardcoded list of pack names.

## What gets built

### 1. Vendor the library

- `ClientLab/Libs/LibOrbitGlow-1.0/` ← copy of the MIT lib (`LibOrbitGlow-1.0.lua`,
  `GlowShowcase.lua`, `LibOrbitGlow-1.0.xml`, `LICENSE`).
- ClientLab has **no LibStub**. The lib needs one; vendor `LibStub` too, or the lib is
  dead on arrival. Take the copy bundled in the upstream repo.
- Wire into `ClientLab.toc` **before** `Glow.lua`. The lib's own `.toc` is a standalone
  manifest — embedders include the `.xml`, so the `.toc` lines are
  `Libs\LibStub\LibStub.lua` then `Libs\LibOrbitGlow-1.0\LibOrbitGlow-1.0.xml`.
- **Drop `GlowShowcase.lua` from the XML.** The upstream showcase reparents a pooled glow
  frame onto `ActionButton1` — a template-declared **protected** frame — with no combat
  guard anywhere in the file, and registers a `/orbitglow` slash command that never passes
  through `ns.RegisterCommand` (house rule 7's schema table). ClientLab is loaded during
  pulls. Our own panel covers the same ground under the lab's combat rules, so the
  showcase is cost with no benefit. Keep the file on disk, unreferenced by the XML.
- **`.luacheckrc`:** add `exclude_files = { "ClientLab/Libs/**" }`. Vendored third-party
  code is not ours to lint. This is not an inline suppression — the zero-suppression rule
  still binds every file we write.

### 2. `ClientLab/Glow.lua` — the palette

A movable panel, toggled from the `/clab` dump panel by a button (rule 4: **a
human-triggered thing is a button, never a slash subcommand** — there is no `/clab glow`).
Follow how `Dumps.lua` registers the button that calls `ns.Ask.Toggle()`.

The panel shows a **scrollable grid of every glow**, built from:

- the 6 engine types — `Pixel`, `Autocast`, `Classic`, `Thin`, `Thick`, `Medium`
- **plus** everything in `lib:GetGlowList()`, grouped by `lib:GetGlowInfo(name).source`
  so an installed pack reads as its own section.

Never hardcode the registered names. With no pack installed the list is just the
`blizzard` baseline, and that is a correct render, not a bug.

Each cell draws the glow on a **48px sample square** — a plain dark texture standing in
for an icon — using `lib.Apply` (which routes engine types *and* registered names) with
`loop = true` so it runs continuously.

### 3. The three controls that make it a decision tool

A palette of pretty rings answers nothing. These are what turn it into a pick:

- **Tier colour.** A three-way toggle — HIGH / MEDIUM / LOW — that recolours the whole
  grid to cap's actual hues, read from `projects/combat-assist/addon/CombatAssistPlus/Treatment.lua`:
  HIGH `{1.00, 0.92, 0.55}`, MEDIUM `{0.45, 0.70, 0.95}`, LOW is a veil with no hue.
  **Copy the numbers as data into `Glow.lua`; do not make ClientLab read cap's files.**
  Plus a "white" setting to judge the glow's own shape uncorrupted by tint.
  ⚠ **Tier alpha does not reach the whole of a *layered* pack glow.** `CoreColor`
  (`LibOrbitGlow-1.0.lua:341-344`) brightens the body colour toward white and hardcodes
  `a = 1` on the ADD core layer, so a `layered = true` glow renders its core at full
  opacity whatever alpha the tier carries — only the BLEND body honours it. Upstream
  behaviour, not ours, but a glow picked here for reading well at MEDIUM's 0.71 will not
  dim its core by that much in cap either.
- **Size.** Toggle the sample square between a few sizes (e.g. 32 / 48 / 64) — the pack
  README is explicit that a glow's corner art is baked at a reference size, and a glow
  that reads at 64 can be mud at 32. Size is the most common reason a pick fails.
- **Paint the live CDM.** A button that applies the selected glow to **every item frame
  of the real Cooldown Manager**, and a second that clears it. This is the only honest
  test of "would this work in cap", because it puts the glow on the actual frame, at the
  actual size, over the actual icon art.
  - Enumerate exactly the way cap does — `Bind.lua:240`: for each of
    `EssentialCooldownViewer`, `UtilityCooldownViewer`, `BuffIconCooldownViewer`,
    `BuffBarCooldownViewer`, `pcall(viewer.GetItemFrames, viewer)`.
  - **Composite the way cap will composite — this is what makes the pick transfer.**
    `AcquireFrameAndTex` (`LibOrbitGlow-1.0.lua:150-162`) makes the glow a *child* of the
    host and sets `frameLevel = host:GetFrameLevel() + 8`, so glowing an item frame
    directly inherits the CDM's strata and stacks against the icon and the cooldown swipe
    one way. cap draws somewhere else entirely: `Overlay.lua:127-164` creates its own
    frame on `UIParent` at strata `HIGH`, level 4, and **anchors** to the item frame
    without ever reparenting. A glow judged in the first compositing is not a glow
    judged in the second.
    So paint through a **proxy**: a plain frame parented to `UIParent`, `SetAllPoints` to
    the item frame, at cap's strata and level — and glow the proxy. Make that the
    **default**, with a toggle to paint the item frame directly, because comparing the two
    is itself the measurement (does drawing above the swipe change the read?).
    The proxy also sidesteps two open questions at once: the library's `owned` option
    exists for hosts in a forbidden hierarchy, and tearing down a frame parented to a
    protected frame under combat lockdown reaches `ClearAllPoints`, one of the 59
    protected widget methods whose in-combat behaviour the KB has measured for only four.
    Neither question arises when our frame's parent is `UIParent`.
  - **Pair every `Apply` with a `Remove` on the same key.** Painting Blizzard frames and
    leaving glow frames stranded on them is how this ends up a bug report against the
    game. Track what was painted; clear on hide, on toggle, and on `PLAYER_REGEN_DISABLED`.
  - **Refuse to paint in combat**, and refuse to build the panel in combat — the same
    rule `Ask.Toggle` already applies.

### 4. What NOT to build

- No `ns.Test{}`, no `questions.json` rows, no `Ask.Register` questions. This measures
  nothing; a human is picking a look.
- **No new capture stream, and no glow state in SavedVariables.** The output is a decision
  a person writes down, not rows a tool reads — rule 3 exists to stop a *second* capture
  path, and this opens none. The panel's tint / size / target / selection are file-locals
  and are deliberately not persisted. What *does* reach disk is one row per button press
  on the pre-existing `dump` stream, because §2 mandates the `ns.Dumps.Register` pattern
  and `D.Take` marks that stream; that is the cost of the mandated pattern, not a second
  path.
- No changes to cap. Choosing is this task; building it into cap is a later one.

## 5. Focus mode — the click-through, and the Blizzard atlas candidates

The grid was the wrong primary view. **You judge a glow on the Cooldown Manager, not in a
panel**, so the panel wants to be small and beside the thing being judged, and the primary
control is `next`. The grid survives as a secondary `[grid]` toggle.

```
┌─ ClientLab — glow palette ──────────── × ─┐
│   ┌──────────┐  blizzard                  │
│   │   ▓▓▓▓   │  LibOrbitGlow · atlas      │
│   │   ▓▓▓▓   │  ui-hud-actionbar-proc-loop│
│   └──────────┘  5×6 · 30 frames           │
│      64px       ◄  12 / 26  ►             │
│  [ < prev ]  [ next > ]   ☑ live on CDM   │
│  tint    [HIGH] MEDIUM  LOW   white       │
│  size      32   [48]    64                │
│  target  [proxy]  direct       [ grid ]   │
│  CDM: 8 frame(s) painted proxy            │
└───────────────────────────────────────────┘
```

With **live on CDM** ticked, `next` repaints the real Cooldown Manager on every press — so
the flow is *look at your action bars, click next, look again*. It obeys the same combat
refusal as the paint button: in combat the stepper still moves the card, it just does not
repaint, and says so once.

The card carries the **name**, the **family**, the **atlas or texture it actually resolves
to**, and the **flipbook grid that was read at build time** — not a guess. A candidate
whose grid could not be read says so on its face; that is a measurement, not a blank.

### The candidate run

One continuous `next`/`prev` sequence over four groups, each card labelled with its group:

| # | Group | Members |
|---|---|---|
| 1 | engine types | the 6 — `Pixel`, `Autocast`, `Classic`, `Thin`, `Thick`, `Medium` |
| 2 | **Blizzard atlases** | the ~15 below |
| 3 | LibOrbitGlow baselines | whatever `GetGlowList()` reports with `source == "LibOrbitGlow"` |
| 4 | installed packs | everything else `GetGlowList()` reports, grouped by `source` |

Groups 3 and 4 stay derived from `GetGlowList()` — never a hardcoded pack list.

**Group 2 is the point of this section.** These are shipping client assets: no dependency,
no license question, and the shortlist cap would actually draw from. Names are the
`CommittedName` values from `UiTextureAtlasMember` (12.0.7 — 17,472 atlases, 206 of them
flipbooks), so they are Tier 1 and offline-verifiable:

```
ui-cooldownmanager-alert-flipbook        the CDM's OWN alert art — try this first
ui-hud-actionbar-proc-loop-flipbook      what the lib calls "Medium"
ui-hud-actionbar-proc-start-flipbook     a START phase the lib never uses
ui-hud-actionbar-gcd-flipbook
rotationhelper-procloopblue-flipbook     "Thick"
rotationhelper-procstartblue-flipbook
rotationhelper_ants_flipbook             "Thin"
onebutton_procloop_flipbook              unused by the lib
onebutton_procstart_flipbook
visualalert_ants_flipbook
transmog-itemslot-flipbook-loop-top / -bottom / -left / -right
transmog-itemslot-flipbook-sparks
```

Each also has a `-2x` / `_2x` high-resolution variant; offer the `-2x` where it exists,
since a CDM icon is small and the 2x bake is the one that survives scaling.

### The declared grids — Tier 1, from shipped source

`C_Texture.GetAtlasInfo` does **not** hand back usable flipbook fields, so the grid cannot
be read at run time. Blizzard declares it per atlas in its own XML instead, via the native
`<FlipBook>` animation (`UI.xsd:1560-1571` — `flipBookRows` / `flipBookColumns` /
`flipBookFrames`). Grids across the shipped UI vary wildly (2×4/8, 9×9/77, 25×2/50,
11×4/44), so "assume 6×5/30" is wrong far more often than right.

`scale` is the drawn size as a multiple of the **host**, not of the sheet: the alert frame
that carries the action-bar flipbooks is itself sized `frameWidth * 1.4`
(`ActionButtonSpellAlerts.lua:20`), and the start texture is a fixed `150×150` centred over
a 45px button rather than stretched to it — which is why a start atlas reads as "a small
square inside the icon" if you draw it filled.

| atlas | rows × cols | frames | secs | scale | provenance |
|---|---|---|---|---|---|
| `ui-hud-actionbar-proc-loop-flipbook` | 6 × 5 | 30 | 1.0 | 1.4 | declared — `ActionButtonSpellAlerts.xml:25` + `.lua:20` |
| `ui-hud-actionbar-proc-start-flipbook` | 6 × 5 | 30 | 0.7 | 3.33 | declared — `ActionButtonSpellAlerts.xml:29` |
| `ui-hud-actionbar-gcd-flipbook` | 11 × 2 | 22 | 0.75 | 1.0 | declared — `CooldownViewer.xml:79` |
| `rotationhelper_ants_flipbook` | 6 × 5 | 30 | 1.0 | 1.47 | declared — `ActionButtonComponentTemplate.xml:80` (66×66 over 45px) |
| `visualalert_ants_flipbook` | 6 × 5 | 30 | 1.0 | 1.0 | declared — `CooldownViewerVisualAlertTemplates.xml:23` |
| `onebutton_procloop_flipbook` | 6 × 5 | 30 | 1.0 | 1.4 | declared — `ActionButtonSpellAlerts.lua:32` swaps it onto the `.xml:25` declaration |
| `onebutton_procstart_flipbook` | 6 × 5 | 30 | 0.7 | 3.33 | declared — `ActionButtonSpellAlerts.lua:31` onto `.xml:29` |
| `transmog-itemslot-flipbook-loop-top` / `-bottom` | 7 × 10 | 70 | 2.33 | 1.0 | declared — `Blizzard_TransmogTemplates.xml:938-939` |
| `transmog-itemslot-flipbook-loop-left` / `-right` | 3 × 30 | 70 | 2.33 | 1.0 | declared — `Blizzard_TransmogTemplates.xml:940-941` |
| `ui-cooldownmanager-alert-flipbook` | 11 × 2 | 22 | 0.75 | 1.0 | **inferred** — 94×517, byte-identical to the GCD sheet; 2×11 is its only square-cell grid |
| `rotationhelper-procloopblue-flipbook` | 6 × 5 | 30 | 1.0 | 1.4 | **inferred** — 333×400, byte-identical to proc-loop and ants, both declared 6×5/30 |
| `rotationhelper-procstartblue-flipbook` | 6 × 5 | 30 | 0.7 | 3.33 | **inferred** — 2x sheet divides square only at 5×6; sized as its proc-start sibling |
| `transmog-itemslot-flipbook-sparks` | 4 × 6 | 24 | 0.8 | 1.0 | **inferred** — no declaration; the gearSlot sparks sibling is 4×6/24 and 900×624 divides by it |

Dimensions are `Width`/`Height` from `UiTextureAtlasMember` (12.0.7), so every inference
above is offline-checkable. The card carries three provenance states — `declared`,
`inferred`, `assumed` — colour-coded, and reports what `GetAtlasInfo` actually said on a
separate line, which is the measurement rather than the input.

### Two implementation rules for group 2

**Do not register these with the library.** `lib:RegisterGlow` writes into a registry that
LibStub shares process-wide, so a user running Orbit alongside the lab would find fifteen
ClientLab entries injected into *Orbit's* glow picker. Keep them in a local table and drive
`lib.Flipbook:Show(frame, {...})` / `lib.Flipbook:Hide(frame, key)` — the documented raw
sink — with a third `kind` value, `"atlas"`, routed alongside `"engine"` and `"registry"`.
The teardown pairing rules are unchanged.

**Read the grid, do not assume it.** `C_Texture.GetAtlasInfo(name)` returns `flipBookRows`
/ `flipBookColumns` / `flipBookFrames`, and the library already prefers them
(`LibOrbitGlow-1.0.lua:234-236`). Whether they are populated for these specific atlases is
**unverified** — the DB2 tables do not carry the grid, so the runtime read is the only
confirmation. So: read per atlas at build, fall back to `5×6 / 30` only if the read comes
back empty, and **show on the card which of the two happened**. That readout is the first
real measurement this panel produces, and it settles a question the KB cannot answer from
source. `GetAtlasInfo` is `MayReturnNothing` (frames-textures-animation.md:1121) — treat a
nothing return as "not read", never as zero.

## Constraints every change is checked against

- **`wow-developer` house rules 1–7** (`.claude/skills/wow-developer/references/house-rules.md`).
  Rule 1 bites hardest: comments say what the code does **now**, no dates, no versions, no
  "used to", new files at comment:code ≤ 0.35.
- **Probe a maybe-missing global by string** — `ns.G` / `ns.GlobalType`, never a bare
  identifier. The four CDM viewer globals go through `ns.G`.
- **Secret values.** The lib's README warns you cannot branch Lua logic on a 12.0 secret.
  This panel is driven entirely by mouse clicks and plain numbers, so it never reads one —
  keep it that way. Do not "improve" it by driving a glow off a cooldown state.
- **`luacheck ClientLab/` clean, zero inline suppressions** (`export PATH="$HOME/.luarocks/bin:$PATH"`).
- **`uv run python -m wowkb.lab deploy --check` still passes** — 7 ids, 7 built questions,
  both directions. If this work changes that number, it is wrong.

## How it gets used

```bash
cd ~/code/fun/wow/tools && uv run python -m wowkb.lab deploy
```

In game: `/clab` → `[glow palette]`. Optionally install **Orbit Pack: Glows** from
CurseForge first to see its 44 glows alongside the built-ins; without it the panel shows
the engine types and the `blizzard` baseline.

### The acceptance set — what the first flight has to look at

House rule 5 requires every `--@unverified` path to sit in the current flight's acceptance
set, and a picker has no PASS/FAIL flight by construction: its only oracle is an eyeball.
This section **is** the acceptance set. Nothing else holds these two paths to being
exercised, so a session that skips them leaves them unverified and must say so.

1. **`direct` target.** Proxy mode is the default and touches no Blizzard frame. `direct`
   reparents a pooled library frame onto a CDM item frame and tears it down under combat
   lockdown — the one path here nobody has measured. Press it once, out of combat, and
   watch for a Lua error, a `ADDON_ACTION_BLOCKED`, or a glow left behind after `clear`.
2. **`Classic` in `direct`.** `Button:Hide` releases through an `animOut` that finishes
   ~0.4 s later, so a fast clear-then-repaint is the case most likely to strand or
   double-release. Select `Classic`, paint, clear, immediately repaint.

Everything the flight actually settles is a **fact about the client**, so it does not stay
in this doc: a value you read goes to `knowledge/addon-dev/` as a claim tagged
`[client YYYY-MM-DD]`, and something you looked for and did not find takes
`[searched YYYY-MM-DD: <instruments>]` phrased as a miss. The picker's own output — which
glow, which tint — is a decision for cap's spec, not a KB claim.
