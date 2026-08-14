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
not move. Whether a hold reads as a red badge or a dimmed border, whether lanes pulse or sit still,
whether a cue lives in the icon's center or its corner: all of that lives here, and changing one
is a normal edit, not a spec amendment.

**Who reads it.** The artifact generator (`wowkb.capart`, which renders a design artifact as the
client would actually draw it) and the addon renderer (`Treatment.lua` / `Overlay.lua`). Both cite
this file rather than each carrying their own numbers — that divergence is the specific failure
this file exists to end.

**Where the numbers are.** In **Part 6**, the `render-tokens` JSON block, and nowhere else. Prose
in this file cites a token path (`tokens.arrival.duration_s`) and never restates its value, because
a number written twice is a number that will disagree with itself. `wowkb.capart` parses the block
for the artifact and **generates the addon's `Style.lua` from it** — the two sides of the promise
above cannot drift, because neither transcribes anything by hand.

**Status vocabulary.** There is only one status word left, and it marks a *fact gap*, not a
design debate:

- **open** — the client capability this primitive would need has not been measured
  (`spec.md` §3.6 routing). The style is still declared; what is unknown is whether the client can
  draw it. An artifact stamps a visible ⚠ chip on an `open` primitive so the preview never lies
  about what ships.

Everything not marked `open` is simply the style. **No primitive is currently `open`** — the
mechanism stays because it is how the artifact refuses to lie about an unmeasured primitive, and
the next one that needs it will find it working.

---

## Part 0 — the loop this file is built for

1. Edit a recipe here — a color, a rate, a placement, a whole new primitive. Numbers go in
   **Part 6**.
2. `uv run python -m wowkb.capart build havoc` — the artifact reads this file's tokens.
3. Look at it. Ask for tweaks. Go to 1.
4. When it looks right, `uv run python -m wowkb.capart export` writes Part 6 into the addon as
   `Style.lua` (data) plus the badge art as TGA, and `/cap style` draws every primitive in the
   client. `capart check` fails if either the committed HTML or the committed `Style.lua`
   disagrees with this file.

Nothing in steps 1–3 requires permission from `spec.md`. If a change here would make cap compute
the press or branch on a sealed value, *that* is the one thing to stop and check — and it is a
§3.6 / §4 question, not a taste question.

**The artifact is a reproduction, not a diagram.** It draws real Blizzard icon art at real
Cooldown Manager size, real vendored sprite frames at their real frame counts and durations,
and composites cap's treatments the way the client would composite them — `SetVertexColor` as a
multiply, never a hue rotation. A preview that recolors art the client could not recolor is worse
than no preview. `wowkb.capart` enforces that mechanically (Part 4).

---

## Part 0.5 — the reading model everything below serves

**Scan the row left to right and press the first button that is not ruled out.** That is the whole
interaction, and `spec.md:137-141` already blesses it: *"A low-priority button is directed-to by
the **absence** of competing emphasis… the same holds for a hold mark's absence."*

### The operator heuristic

The sentence above is the *principle*. This is the procedure a human actually runs, written down so
that it can be changed on purpose. If a flight says scanning left-to-right is too hard, **this is
the thing that gets edited** — and every treatment below is then re-judged against the new version,
rather than each treatment being tweaked on its own.

```
pass 1 — scan left to right for a POSITIVE cue. If one is present, press it.
pass 2 — scan left to right, skipping:
           · anything dimmed with no border
           · anything wearing at least one RED cue
         press the first item that survives.
```

**The procedure is the authority.** Where a treatment below and the two passes disagree, the passes
win and the treatment is what gets edited. Two things moved to match it:

**What the procedure ruled out — the `withheld` verdict, now deleted.** A verdict may only be
*drawn* from a fact cap is allowed to read. `withheld` — border + veil, no badge — was the one
verdict in the vocabulary that broke this: its only driver was that a readable fact came back
**secret**, so the refusal itself became a visible elimination. Pass 2 makes that obviously wrong —
an item cap cannot form an opinion about is an item the scan should simply *reach*, not one it
should skip. The vocabulary is nine verdicts, and a row cap has no opinion about draws whatever its
readable state says: a lane border, or the swipe, and no veil.

**And `isActive` removed its last subject anyway.** `withheld`'s only user was a charge count read
below full. `C_Spell.GetSpellCharges` seals per member: `isActive` is `NeverSecret` and stays plain
in restricted combat, so "at max charges" is readable in **both** polarities — `false` at 2/2,
`true` below it. There is nothing left for the verdict to mean.

Two consequences the style is built on:

1. **The press is not a thing cap draws.** `press`, `press-promoted` and `below` render
   identically — a lane border, nothing else. The press is *whatever the scan reaches first*. Cap's
   job is to rule things out convincingly, not to point.
2. **The cue vocabulary is negative by default, with exactly one positive exception.** A cue
   normally draws when a button is ruled *out* and draws nothing when it is clear. A satisfied
   dependency is silence. Red says *why* something is skipped; the veil says *that* it is skipped.
   Every cue declares its `polarity`, and a cue that declares none is read as negative.

**The one exception, and the reason it exists.** Elimination encodes **rank** — it answers "what is
the highest-priority thing not ruled out." Some facts are not about rank at all. *You are wasting a
charge right now* is urgent no matter what sits to its left, and it stays urgent when the answer to
"what is highest priority" is something else entirely. There is no negative phrasing of it: to say
it by ruling things out you would have to mark the buttons to its left as skippable, which would be
false. So the vocabulary carries **one** positive cue, `capped`, scoped to **impending loss** and
nothing wider.

**Pass 1 makes it pre-emptive, and that is the point.** A cue that reports impending loss and then
waits its turn in the scan has reported it too late — by the time the eye arrives the charge is
gone. So `capped` is read first and it *redirects* the scan. What keeps that inside `spec.md` §4 is
not that the cue is passive; it is that cap draws it from **one readable fact about one button**
and never from a comparison across the row. Cap still computes no press: it says *this specific
thing is being wasted right now*, and the player decides what that is worth. The §4 oracle is a
channel that weighs the whole state into one answer, and one badge on one row is not that.

Its scope is what keeps this honest, and the scope is narrow: **impending loss, nothing wider.** A
positive cue for "you have enough" or "this is favoured now" is a statement about **rank**, which
elimination already carries, and would be a second voice in pass 1 competing with the first.

The other positive signals (a "banked" light, a green dependency dot, a weave chevron, a promoted
press) remain **parked, not refuted**. `spec.md` §3.6 and `havoc/catalog.md` both record that a
sealed threshold is expressible in **either** polarity, and that stays true.

**Four gates in `wowkb.capart check` hold this line, one per pass plus two on the vocabulary.**

- **Pass 1.** If a scenario wears a positive cue at all, the leftmost entry wearing one must be the
  press. A positive cue is pre-emptive, so a scenario where it points somewhere other than the
  press is a scenario that reads wrong.
- **Pass 2** — the elimination gate (Part 5). The leftmost entry that is neither swiped nor veiled
  nor wearing a negative badge must be the press, **counting negative cues only**, so the positive
  cue can ride the press without eliminating it.
- **A second positive cue fails the build.** This is no longer only a vocabulary question: a second
  positive cue is a second pass-1 candidate, so two of them in one row makes pass 1 ambiguous about
  which to press. Adding one is a decision about the *ordering model*, and it means rewriting the
  procedure above to say how the two rank.
- **A declared cue worn by no scenario fails the build**, since a cue that renders nowhere is
  `spec.md:194-195`'s defect at shelf level.

---

## Part 1 — Surfaces (what there is to draw on)

A Cooldown Manager row is a small square icon. These are the places a cue can live. Placement is
a design choice, not a platform constraint, unless marked otherwise.

| Surface | Where | Carries | Notes |
| --- | --- | --- | --- |
| **Icon face** | the art itself | desaturation, veil, whole-icon alpha | Blizzard's own dim/uninteractable channel. |
| **Lane border** | a solid rectangular border on the icon edge | the role lane, or CHARGES | Static. Its only motion is the one-shot arrival snap (V2). Drawn on cap's own frame, so it needs no host scale-up. |
| **Corner badge slots** | three discs hung off the **top-right** corner | one cue each — slots 1–2 (along the top edge) negative, slot 3 (down the right edge) the single positive cue | Filled circles at `tokens.badges.diameter_pct` of icon width, overhanging by `tokens.badges.overhang_px` (V5). Position carries polarity as well as colour. |
| **Cooldown swipe** | the radial dial | remaining time | Can be *restyled* without knowing the time (see V7). |
| **Count tile** | Blizzard's own aura count position | a sealed stack number | Client-owned; cap never learns the value. |
| **Independent bar** | anywhere on screen | one duration, large | Off-icon surface; costs screen space and must earn it. |

**What Blizzard already occupies on a CDM item** — read off `Blizzard_CooldownViewer` at
**12.0.7**, under a standing ⚠ *12.1 rewrote this system and this has not been re-flown*:

- **BOTTOMRIGHT** — `ChargeCount.Current` on the cooldown tab and `Applications` on the aura tab,
  both anchored at −2 / +2.
- **Centre** — the countdown numbers the swipe draws.
- **Free:** both top corners, and bottom-centre.

⚠ A previous revision of this table claimed Blizzard draws **keybind text** along the bottom of a
CDM item. It does not: `grep HotKey` over the whole `Blizzard_CooldownViewer` folder returns
**zero** — the CDM has no `HotKey` region at all (that is an ActionButton thing). The corner slots
still live in the top-right, but the reason is now "the top corners are free and the OS-badge
convention lives there," not a collision that does not exist.

⚠ **Not a design choice:** cap draws on its **own frame parented to `UIParent`**, anchored to the
CDM item frame — it must never reparent onto or restyle a live Cooldown Manager frame. Since 12.1
those frames participate in secure aura plumbing, and decorating them is what got ClientLab's
`Glow.lua` and `Cue.lua` retired from the `.toc`. This is a platform rule, not taste.

---

## Part 2 — Primitives

Each recipe: what it means, the art (Blizzard's or ours), the token path its numbers come from, a
Lua sample, and how the artifact reproduces it.

### V1 · *(retired)*

The animated flipbook emphasis ring — a `visualalert_ants_flipbook` glow outside the icon edge,
tinted to the lane and pulsed forever. Retired 2026-08-13 in favour of V2's solid border plus the
arrival snap: a row of continuously-glowing rings reads as candles, and CDMProbe measured that
**60 % of real cue-set changes are swaps**, so continuous motion spends its budget on states that
are about to be replaced. The measurement that made the ants sheet the only usable ring — its
neutral saturation — is still true and is kept in `render-rationale.md`; it is simply no longer
load-bearing here.

### V2 · Lane border — solid, with a one-shot arrival

**The role-lane treatment.** A solid rectangular border on the icon edge, in the lane's hue at the
lane's thickness, **static**. It sits there and says which lane the button is in; it does not
compete for attention while it is doing that.

Its only motion is the **arrival snap**: when something *arrives* — a cooldown finishes, a charge
returns, a spender becomes affordable — the border is drawn at `tokens.arrival.from_scale` and
`tokens.arrival.from_alpha` and snaps down onto the icon over `tokens.arrival.duration_s` with
`tokens.arrival.smoothing`. One shot, then it rests. There is deliberately **no looping variant**:
the whole claim of this primitive is that motion marks *the change of state* and then stops.

- **Lanes:** `tokens.lanes.<LANE>.rgb` / `.thickness_px`. Four of them — COOLDOWN, ROTATION,
  FALLBACK, and **CHARGES**.
- **CHARGES replaces the role lane**, it does not stack. An ability has exactly one border, and if
  the client says the ability has charges, the border is `CHARGES`. This is a **render-time**
  substitution off a readable client fact — it is not a re-authoring of the ability's priority, and
  `havoc/catalog.md` still records the role lane the rotation puts it in.
- **Art:** none. Four `SetColorTexture` strips on cap's own frame. Nothing to extract, nothing to
  tint-guard, no atlas to go stale across a patch.
- **Lua:**
  ```lua
  local edge = CreateFrame("Frame", nil, cap.overlay)   -- NOT the CDM item frame
  edge:SetAllPoints(icon)
  for _, side in ipairs({"TOP", "BOTTOM", "LEFT", "RIGHT"}) do
    local strip = edge:CreateTexture(nil, "OVERLAY")
    strip:SetColorTexture(unpack(T.lanes[lane].rgb))    -- solid color; no art, no multiply
    -- …anchor `side` at T.lanes[lane].thickness_px
  end

  local snap = edge:CreateAnimationGroup()              -- fired ON THE EVENT, then it stops
  local grow = snap:CreateAnimation("Scale")
  grow:SetScaleFrom(T.arrival.from_scale, T.arrival.from_scale)   -- ⚠ NOT SetFromScale
  grow:SetScaleTo(1, 1)
  grow:SetDuration(T.arrival.duration_s)
  grow:SetSmoothing(T.arrival.smoothing)
  local fade = snap:CreateAnimation("Alpha")
  fade:SetFromAlpha(T.arrival.from_alpha); fade:SetToAlpha(1)
  fade:SetDuration(T.arrival.duration_s)
  snap:SetToFinalAlpha(true)                            -- animations don't restore alpha on stop
  ```
  ⚠ `SetFromScale` / `SetToScale` **do not exist**; the setters are `SetScaleFrom` / `SetScaleTo`.
  Probe before calling — an animation that silently never received its endpoints looks exactly
  like a live one.
  ⚠ Per CDMProbe's hardest-won rule, nothing that is an *ancestor* of a rotating texture may be
  animated. Nothing in this primitive rotates, by design.
- **Artifact reproduction.** A `border` on a positioned box, plus a keyframe from
  `scale(tokens.arrival.from_scale)` at `opacity: tokens.arrival.from_alpha` to `scale(1)` at
  full — `animation-fill-mode: both`, run once. The artifact re-fires it on a timer
  (`tokens.artifact.arrival_replay_s`) purely so it can be watched; that interval is declared under
  `tokens.artifact` precisely because it is **not part of the style**.

### V3 · *(retired)*

The lane pulse — three unequal rates driving the V1 ring's alpha, with a trough-invariant floor and
a per-icon phase offset. Retired with V1: there is no continuous motion left in the style to pace.
The arithmetic behind it (the trough invariant, the unequal-rate argument, the WCAG phase-offset
note) is kept in `render-rationale.md` because the *measurements* stay true and would have to be
re-derived if continuous motion ever came back.

**What survives:** the sealed-**text** flicker limits, which were never about the ring. They are
MIL-STD-1472F / WCAG constraints on blinking legends and they bind any text cue cap ever draws.
They now live at `tokens.text.max_hz` / `.duty` / `.alpha_floor` (see V8).

### V4 · Veil (de-emphasis)

Dim what cap has an opinion *against*, rather than only brightening what it favors. A veiled row
is still perfectly legible; it has just stopped competing.

- **Value:** `tokens.veil.alpha` of `tokens.veil.rgb` over the icon face.
- **Applies to:** every verdict whose `veil` is true in `tokens.verdicts` — the skipped rows of a
  walk, in short.
- **The veil says "skip"; the badge says "why."** That division is the whole cue design, and it is
  mechanical rather than authored: a row is veiled **iff** it wears at least one negative cue. So a
  veil with no badge cannot occur — there is no "skipped, and cap will not say why" state — and a
  badge with no veil is exactly the positive cue, which does not skip anything.

### V5 · Corner badge — OS-style

The general answer to "a non-numeric cue needs a texture that catches the eye at 56 px."
Windows/mobile notification-badge convention: a filled circular disc hung off the icon's
**top-right** corner, overhanging by `tokens.badges.overhang_px` past the top and right edges so it
reads as *on top of* the icon rather than *inside* it.

- **Geometry:** `tokens.badges.diameter_pct` of icon width. Slot 1 sits on the top-right corner;
  slot 2 is one `diameter + tokens.badges.padding_px` to its left along the top edge; slot 3 the
  same distance below it down the right edge. Order is fixed by cue identity, never by arrival, so
  a given cue is always in the same place. Three slots is the ceiling; if a fourth cue wants in,
  one of the three is not earning its slot.
- **Plate:** every badge sits on a dark disc, `tokens.badges.plate`, scaled
  `tokens.badges.plate.scale` past the sprite. Additive art over busy icon work washes out, and
  contrast is the cheap fix — more light is not (CDMProbe, learned the expensive way).
- **Sprite inset:** the glyph is inset `tokens.badges.sprite_inset_pct` *inside* the disc, so a
  square sprite fits within the circle instead of poking out at the corners.
- **Colour:** one shared red, `tokens.badges.rgb`, for **every negative cue**. A second *red* would
  be a second visual language for the same job; the badge shape and its animation carry the
  distinction between one "skip this" and another. **Colour carries polarity, and only polarity** —
  so the single positive cue overrides it (`tokens.cues.capped.rgb`, gold) and nothing else may.
- **Art:** Kenney's CC0 **Board Game Icons**, vendored at `tokens.badges.asset_root` with its
  licence beside it. Measured **saturation 0.000** — white with the shape in the alpha channel — so
  `SetVertexColor` multiplies it to the authored hue at full strength. This is the same reason
  CDMProbe shipped Kenney's `star_07` rather than a Blizzard atlas: neutral art we own beats hunting
  for neutral art we do not. Declared `tokens.badges.tint: "lane"`, which is what puts these frames
  under the Part 4 tint guard.
- **Two shapes the browser gets free and the client does not.** A `border-radius` and a
  `radial-gradient` are one CSS property each; in the client the disc and the halo are art. Both
  are generated white-with-shape-in-alpha (`capart export badges`, Part 4's "author them from a
  script"), the halo fading out at `tokens.badges.halo_falloff` of its radius — the same stop the
  artifact's gradient uses.
- **Lua:**
  ```lua
  local plate = slot:CreateTexture(nil, "OVERLAY", nil, 6)
  plate:SetColorTexture(unpack(T.badges.plate.rgb))
  plate:SetAlpha(T.badges.plate.alpha)

  local sprite = slot:CreateTexture(nil, "OVERLAY", nil, 7)
  sprite:SetTexture(T.badges.asset_root .. "/" .. frame)   -- neutral art: tints cleanly
  sprite:SetVertexColor(unpack(T.badges.rgb))              -- multiply, one shared red
  ```
- **Artifact reproduction.** `mask-image` (the frame's alpha) + `background-color` (the red). For
  white-with-shape-in-alpha art that composite **is** what `SetVertexColor`'s multiply produces. It
  is not a hue-rotate.

### V5.1 · The four cues

The whole vocabulary. Each is a **single state** that either draws or does not — never a two-state
marker whose satisfied state happens to be invisible. `spec.md:194-195` says *"a catalog form that
loads successfully and then renders nothing is a defect"*, and that test only keeps meaning if
"drew nothing" is unambiguously a bug rather than a legal second state.

| Cue | Polarity | Frames (`tokens.cues.<key>.frames`) | Loop | Slot | Means |
| --- | --- | --- | --- | --- | --- |
| **`blocked`** | negative | `timer_0 → CW_25 → CW_50 → CW_75 → timer_100` | `REPEAT` | 1 | held for a cooldown, or a readable dependency says the press would be wasted |
| **`starved`** | negative | `flask_empty → flask_half` | `BOUNCE` | 2 | you cannot afford it |
| **`overcap`** | negative | `flask_half → flask_full` | `BOUNCE` | 2 | pressing would waste resource |
| **`capped`** | **positive** | `cards_stack → cards_stack_high` | `BOUNCE` | 3 | charges are at max and the recharge is stalled — you are losing one right now |

**The three negatives share one red** (`tokens.badges.rgb`) and carry no per-cue hue: one colour for
every "skip this" is what lets the row be read without decoding each glyph. **`capped` is the only
cue with its own** — gold, `tokens.cues.capped.rgb` — because it is the only one saying something
other than "skip". It also takes **slot 3** (down the right edge) rather than the top edge the
negatives use, so polarity is legible from position as well as colour, and a badge that means the
opposite of its neighbours can never sit in the same place as one of them.

**`capped` animates exactly like the two flask cues** — a two-frame `BOUNCE` at the same
`duration_s`, a thin stack growing to a full one. Frame cadence is the *shared* idiom of the badge
vocabulary and carries no polarity; what separates this cue from the negatives is its hue, its
slot, and the glow below. Making it a still image had it reading as a different **kind** of widget
rather than a different **kind of statement**, which is not the distinction that matters.

⚠ **`capped` glows; nothing else does.** `tokens.cues.capped.glow` pulses a halo *behind* the glyph
between `alpha_min` and `alpha_max` at `hz`. The **glyph itself holds full alpha** — a cue that
faded would blink the fact it carries, which is exactly what the `tokens.text` flicker limits exist
to forbid, and those limits (`max_hz` 2.0) are the ceiling this rate sits under. The halo may
breathe; the information may not. The glow is what earns the extra attention impending loss needs
in peripheral vision; the frame bounce is just the house style.

**How the frames step.** One shared `C_Timer.NewTicker` walks every visible badge; each one
shows frame `floor(elapsed / (duration_s / #frames))` mapped through its `loop`, so the cadence is
computed from the clock rather than accumulated per badge and cannot drift. `REPEAT` wraps;
`BOUNCE` turns around at each end. This is the same walk `stepper.js` does, which is why the
artifact and the client show the same cadence. A `FlipBook` animation is the wrong tool here: it
needs one sheet rather than a frame list, and it carries a standing `SetParent` crash report
(`knowledge/addon-dev/frames-textures-animation.md:1386`).

⚠ **The timer sweep is a pace, not elapsed time.** It is a "waiting" glyph, not a dial, and it
carries no clock — cap never reads one. If it reads as a countdown, that is a finding and this cue
has failed.

`blocked` covers what were previously two separate treatments — the readable dependency dot's
`wait` state and the sealed hold ✕. They are the same sentence to the player ("not yet"), and the
difference between them is a *provenance* fact (`spec.md` §3.2's two hold lanes), not a visual one.

### V6 · *(retired)*

The 7 px corner dot with a green `go` / red `wait` pair. Retired 2026-08-13: green `go` said a
dependency was *satisfied*, which is a statement about **rank** — exactly what elimination already
carries — so under the vocabulary that replaced it a satisfied dependency draws nothing at all.
(The one positive cue added since, `capped`, is not a counter-example: it carries impending loss,
which elimination cannot express. See Part 0.5.) The `wait` half is now the `blocked` badge (V5.1), which is roughly three times the
size and actually catches the eye at 56 px.

### V7 · Swipe restyle

The dial can be repainted without knowing the time it shows: `SetSwipeColor`, `SetSwipeTexture`,
`SetEdgeTexture`, `SetDrawSwipe`, `SetDrawEdge`, `SetHideCountdownNumbers`, `SetCountdownFont`,
`SetReverse`, `SetRotation` carry **no timing**.

cap leaves the swipe at Blizzard's default: `tokens.surfaces.swipe.color` is the stock dark wash,
and the swipe is the CDM's own "ruled out" signal, which cap has no reason to restate. The
elimination walk leans on it directly — a swiped row is the cheapest possible "skip this."

⚠ `RefreshSpellCooldownInfo` re-applies `SetSwipeColor` + `SetDrawSwipe` on **every** refresh, so
a one-shot restyle is silently clobbered — `hooksecurefunc` per instance and be the last writer.

### V8 · Sealed count tile

An `AuraContainer` writes a secret application count straight into a static outlined FontString
(`FRIZQT__.TTF`, `tokens.surfaces.count_tile.size`, `OUTLINE`, anchored `TOP` +1). Human verdict
recorded: at 1 stack, icon and swipe with no number; at 2 stacks, the number appeared. cap reports
`offered` / `armed` / `refused` and never learns whether the glyph drew.

**Any text cap blinks** — here or anywhere else — is capped at `tokens.text.max_hz` with duty
`tokens.text.duty` and an alpha floor of `tokens.text.alpha_floor`. Those are MIL-STD-1472F's
numbers for blinking legends and they are a safety constraint, not a taste dial. They can be
*implemented* differently; they cannot be dropped.

### V9 · Sealed color curve

A secret resource is handed to the client with an authored **color curve**; the client evaluates it
against the value and paints. The break point is a baked number, not a comparison cap performs.
Both polarities work — this is the mechanism, and the mechanism is unchanged. What the *style*
currently draws is only the negative one (`overcap`, `starved`); the positive readout is parked,
not unavailable. Feature-gate `C_CurveUtil.CreateCurve` / `Enum.LuaCurveType.Step` /
`Enum.DurationTimeModifier.RealTime`; on any missing piece take the inert path. Curves and
durations are `userdata`, not tables.

### V10 · Sealed range-gated texture

A sealed remaining-duration drives a texture's visibility only while the time sits inside an
authored band — the `blocked` badge drawn without Lua reading the clock. Sinks that carry secrecy
inside a duration object: `SetTimerDuration`, `SetCooldownFromDurationObject`. Sinks that take a
secret directly: `SetAlpha`, `SetDesaturation`, `SetValue`, `SetText`, `SetApplicationCount`.
**Never read back** — a capture may say `offered` / `armed` / `refused`, never `drew`.

---

## Part 3 — Composition rules

- **`SetVertexColor` multiplies.** Baked-hue art can only be darkened toward its own hue. The
  style therefore uses neutral art wherever it tints (V5's Kenney frames, saturation 0.000) and
  plain `SetColorTexture` where there is no art at all (V2's border). Desaturate-then-tint
  (`SetDesaturated(true)` / `SetDesaturation(0..1)` first, tint the result —
  `knowledge/addon-dev/frames-textures-animation.md:1044-1052`) is the escape hatch for baked art,
  and whether it yields a *clean* hue is **open**: unmeasured in client. A primitive declaring
  `tint: "desaturate+lane"` builds, but the artifact stamps a visible ⚠ on it. Nothing declares it
  today.
- **Don't bundle Blizzard art.** Reference an atlas by name — that ships no asset. Extracted art is
  for measuring and for the artifact, never for the addon's `Media/` folder. (Our own CC0 art is a
  different case: it ships, because it is ours.)
- **`SetGradient` resets vertex color to white.** Apply the gradient first, tint second.
- **`SetTexture` / `SetAtlas` / `SetColorTexture` are exclusive** — last call wins. `GetTexture()`
  after `SetAtlas` returns the backing fileID as a *number*, not nil; ask `GetAtlas()` first.
- **Animations don't restore vertex color on stop** without `SetToFinalAlpha`. This bites V2's
  arrival snap specifically: it is fire-and-forget, so it must land on its final values.
- **`Show`/`Hide`, never `SetShown`** — `SetShown` is a protected function. *(True but
  mis-framed: protection bites only on **protected** frames, and on cap's own `UIParent` child it
  is unrestricted and measured so. Left as-is because "always `Show`/`Hide`" is a cheap habit to
  keep and costs nothing.)*
- **Set frame strata/level out of combat only.** In combat, confine writes to
  `Show`/`Hide`/`SetVertexColor`/`SetAlpha`. The arrival snap is an in-combat animation on a frame
  whose level was fixed at bind — that is the reason it is a `Scale`/`Alpha` group and not a
  re-anchor.
- **Stock proc glow coexists.** cap dims Blizzard's own overlay to `tokens.surfaces.proc_glow_alpha`
  via `hooksecurefunc(frame, "RefreshOverlayGlow")`. That is a dial for an eyeball, not a measured
  value, and `SetAlpha` reports nothing back. With V1 retired there is no longer a cap animation
  competing with it, which is most of why the dim is a dial and not a fight.

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

**Our own art.** The badge sprites are Kenney's CC0 **Board Game Icons**, vendored under
`tokens.badges.asset_root` with `LICENSE.txt` beside them. For shapes no CC0 pack has, author
white-alpha sheets from a script beside this file, so they regenerate rather than accumulate as
binary mystery — the badge disc and its halo are generated exactly that way. Fully tintable, fully
ours, no licence question.

**This is also the art that ships.** `capart export badges` writes every frame the cue vocabulary
names, plus the two generated shapes, into the addon as 32-bit RLE TGA — the format and header
shape of the Kenney art CDMProbe already reads in client. The tint guard runs on that path too, so
a baked-hue frame cannot reach the client through a route the artifact never rendered. This is not
the "don't bundle Blizzard art" rule's subject: our own CC0 art ships, because it is ours.

**The artifact contract, and the guard that enforces it.** Icons and sprites embed as base64
`data:` URIs — the artifact CSP blocks every external host, so a CDN `<img src>` renders nothing.
`wowkb.capart` refuses to build a lie:

| Condition | What happens |
| --- | --- |
| `tint: "lane"` on art the manifest measured non-neutral | **hard error**, naming the measured saturation |
| a CSS tint written as `hue-rotate` | not emitted — the tint path is `mask-image` + `background-color` (or `background-blend-mode: multiply`) |
| `tint: "desaturate+lane"` | builds, and stamps a visible ⚠ *open* chip on that primitive |
| total base64 over `tokens.budget.max_base64_kb` | reported by `capart assets`; a `check` concern, never a blocked rebuild |

**The tint guard is the shelf's one mechanical promise and it is deliberately art-agnostic.** It
started life guarding the flipbook rings; the rings are gone and it now guards the badge sprites,
because the claim it enforces was never about rings — it is *"art the shelf recolors must be art
`SetVertexColor` can actually recolor."* `tint: "lane"` is the token spelling of that claim (the
colour comes from the shelf, not from the art; whether that colour happens to be a lane hue or the
cue red is beside the point). Any future primitive that tints art inherits the guard by declaring
it, and any primitive that stops declaring it silently loses the guarantee — which is why
`capart check` also asserts that at least one declared asset still carries it.

The asset list and the budget are `tokens.assets` / `tokens.budget`.

---

## Part 5 — What a flight would settle

Look-at-it questions, not measurements. None of them is a reason to hold two styles in this file.

1. **Does a row at rest read as quiet?** Four static borders and nothing moving — does that read
   as informative, or as furniture the eye stops seeing after ten minutes?
2. **Does the arrival snap catch the eye without the ring?** One `tokens.arrival.duration_s`
   transient per state change, against a boss fight's worth of screen motion. If it is missed, the
   alternative is a *slower* snap, not a louder resting state.
3. **Does the CHARGES border carry meaning, or is it a fourth colour nobody decodes?** It replaces
   the role lane, so the cost of it being noise is that a button's lane became unreadable. ⚠ On
   Havoc specifically this bites: **both** FALLBACK abilities (Throw Glaive, Fel Rush) have
   charges, so no Havoc row ever draws a FALLBACK border at all. `capart build` prints that as a
   page-level note rather than letting the lane silently vanish.
4. **Do the badges read without a legend at 56 px?** Specifically: does the timer sweep read as
   "waiting" or as a countdown? A countdown reading is a failure of the cue, not of the player.
5. **Does one shared red across three badges under-differentiate?** The shapes are meant to carry
   the distinction. If they do not, the fix is different shapes, not a second hue.
6. **Does elimination alone lead the eye?** The four scenarios with something to the *left* of the
   press (ST-7, ST-10, AoE-2, AoE-3) are the test. If a scenario needs a positive cue to be
   readable, that is the finding that un-parks the positive vocabulary.
7. Does desaturate-then-tint produce a clean hue on baked art? — **open**, needs the client.
   Nothing declares it today; the question stays because the escape hatch is worth having priced.

**And one gate that does not wait for a flight.** `wowkb.capart check` asserts, for every
scenario: *the leftmost entry that is neither swiped (`cd`) nor veiled nor carrying a red cue must
be the entry the doc calls the press* — `weave` skipped over, since it is off the GCD and pressed
in parallel. That is question 6, mechanised. All 13 Havoc scenarios pass it today. If a future
scenario cannot lead the eye to its press by elimination, this fails **by name** rather than
someone noticing months later.

---

## Part 6 — The tokens

**This block is the style.** Every number cap draws with is here and nowhere else. `wowkb.capart`
parses it for the artifact and generates the addon's `Style.lua` from it verbatim; prose cites
paths into it. Editing a value here and rebuilding is the whole loop.

`Style.lua` carries data only — `Treatment.lua` and `Paint.lua` are the logic that reads it, which
is what keeps the generated file free of functions and diffable. Two keys never reach it:
`artifact`, annotated below as a viewing aid, and Part 7's `lab`, which is by construction not the
style. Everything else crosses unchanged, plus where the exported art landed.

Colors are `[r, g, b]` in 0–1, the way `SetVertexColor` wants them.

<!-- render-tokens v1 -->
```json
{
  "version": 2,
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
    "from_alpha": 0.00
  },
  "veil": { "rgb": [0.00, 0.00, 0.00], "alpha": 0.60 },
  "text": {
    "max_hz": 2.0,
    "duty": 0.70,
    "alpha_floor": 0.65
  },
  "badges": {
    "diameter_pct": 40,
    "overhang_px": 2,
    "padding_px": 3,
    "sprite_inset_pct": 16,
    "rgb": [0.95, 0.30, 0.30],
    "tint": "lane",
    "plate": { "rgb": [0.00, 0.00, 0.00], "alpha": 0.78, "scale": 1.12 },
    "halo_falloff": 0.70,
    "asset_root": "artifacts/assets/kenney",
    "slots": [
      { "id": 1, "anchor": "top-right-corner" },
      { "id": 2, "anchor": "left-of-1-along-top" },
      { "id": 3, "anchor": "below-1-along-right" }
    ]
  },
  "cues": {
    "blocked": {
      "means": "held for a cooldown, or a readable dependency says the press would be wasted. The sweep is a steady pace, NOT elapsed time.",
      "polarity": "negative",
      "frames": ["timer_0", "timer_CW_25", "timer_CW_50", "timer_CW_75", "timer_100"],
      "duration_s": 2.00, "loop": "REPEAT", "slot": 1, "open": false
    },
    "starved": {
      "means": "you cannot afford it",
      "polarity": "negative",
      "frames": ["flask_empty", "flask_half"],
      "duration_s": 1.20, "loop": "BOUNCE", "slot": 2, "open": false
    },
    "overcap": {
      "means": "pressing would waste resource",
      "polarity": "negative",
      "frames": ["flask_half", "flask_full"],
      "duration_s": 1.20, "loop": "BOUNCE", "slot": 2, "open": false
    },
    "capped": {
      "means": "charges are at max and the recharge is stalled — you are losing one right now",
      "polarity": "positive",
      "rgb": [1.00, 0.78, 0.25],
      "glow": { "hz": 1.2, "alpha_min": 0.15, "alpha_max": 0.55, "scale": 1.55 },
      "frames": ["cards_stack", "cards_stack_high"],
      "duration_s": 1.20, "loop": "BOUNCE", "slot": 3, "open": false
    }
  },
  "verdicts": {
    "cd":             { "border": false, "veil": false, "swipe": true,  "cues": [] },
    "weave":          { "border": true,  "veil": false, "swipe": false, "cues": [] },
    "hold-readable":  { "border": true,  "veil": true,  "swipe": false, "cues": ["blocked"] },
    "hold-sealed":    { "border": true,  "veil": true,  "swipe": false, "cues": ["blocked"] },
    "starved":        { "border": true,  "veil": true,  "swipe": false, "cues": ["starved"], "desaturate": 1.0 },
    "overcap":        { "border": true,  "veil": true,  "swipe": false, "cues": ["overcap"] },
    "press":          { "border": true,  "veil": false, "swipe": false, "cues": [] },
    "press-promoted": { "border": true,  "veil": false, "swipe": false, "cues": [] },
    "below":          { "border": true,  "veil": false, "swipe": false, "cues": [] }
  },
  "surfaces": {
    "icon_px": 56,
    "row_gap_px": 6,
    "border_px": 1,
    "swipe": { "color": [0.00, 0.00, 0.00], "alpha": 0.72 },
    "count_tile": { "font": "FRIZQT__.TTF", "size": 14, "outline": "OUTLINE" },
    "proc_glow_alpha": 0.5
  },
  "assets": {
    "icon_size": 56,
    "encode": "webp",
    "quality": 90
  },
  "budget": { "max_base64_kb": 512 },

  "artifact": {
    "_comment": "NOT THE STYLE. Viewing aids the preview needs and the addon does not. The addon fires the arrival snap on the event and stops; the artifact replays it so it can be watched.",
    "arrival_replay_s": 5.0
  }
}
```

**Reading the verdict table.** `border` is whether the row wears its lane border at all — `cd` is
the only row that does not, because Blizzard's swipe has already ruled it out and a border would
just be noise on a dead button. `veil` is V4. `swipe` is Blizzard's own dial, which cap does not
draw and does not restyle (V7); it appears here so the artifact can reproduce the row faithfully.
`cues` names badge cues (V5.1) by key into `tokens.cues`, and each cue's `slot` fixes where it
lands. A cue whose token carries `open: true` draws with a ⚠ chip in the artifact and produces
**no hint in the addon** until it is measured (`spec.md` §3.6); none does today.

**`press`, `press-promoted` and `below` render identically, and that is the point.** The press is
"the leftmost thing not ruled out," not a thing cap draws (Part 0.5). The verdict *names* are kept
because `havoc/scenarios.md` needs them to state its argument — `press-promoted` still records
*why* a windowed spender outranks a lit cooldown, and re-drawing that distinction is a one-line
shelf edit if a flight asks for it.

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

### The lab is currently empty.

Its two entries were promoted on **2026-08-13** and are gone from here, per rule 4:

- **L1 `border-arrival`** → **V2**, the lane border and its arrival snap, with the fourth
  **CHARGES** lane. It retired V1's flipbook ring and V3's pulse.
- **L2 `badge-slots`** → **V5**, the corner badges, with the cue vocabulary rewritten
  negative-only. It retired the old center cue row and V6's corner dot. *(The vocabulary gained
  one positive cue on 2026-08-14 — see Part 0.5; the promotion itself is unchanged.)*

There is no `lab` block in Part 6 right now, and that is the correct resting state — an empty lab
is a lab, not a defect. The next idea gets a `lab` key, an `asks`, and a section here.
