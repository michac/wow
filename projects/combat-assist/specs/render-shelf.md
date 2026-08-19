# Combat Assist Plus — the render shelf

**What this file is for:** how cap is allowed to *look*. `pattern-shelf.md` answers **which facts
you may use**; this answers **how you may show them**. It owns every visual opinion in the
project — surfaces, primitives, colors, motion, placement, composition — so that trying something
new means editing this file, not amending `spec.md`.

**This file declares one style.** It is not a debate. Every primitive below states **the**
treatment, in the present tense, with no alternative beside it. If the style is wrong, the fix is
to *change this file*, not to add a second option next to the first — a preview rendered from a
shelf with two answers renders neither. Alternatives that were considered, the reasoning behind a
choice, and what was tried and rejected live in **`render-rationale.md`**, which has no authority
over anything.

**Opinions here are still cheap.** Nothing in this file is a boundary. The one boundary is
`spec.md` §3.6 — cap never branches on a sealed value — and it does not move.
Whether a hold reads as a red badge or a dimmed border, whether the scan edge pulses or sits still,
whether a cue lives in the icon's center or its corner: all of that lives here, and changing one
is a normal edit, not a spec amendment.

**Who reads it.** The preview generator (`wowkb.capart`, which renders a design preview as the
client would actually draw it) and the addon renderer (`Treatment.lua` / `Overlay.lua`). Both cite
this file rather than each carrying their own numbers — that divergence is the specific failure
this file exists to end.

**Where the numbers are.** In **Part 6**, the `render-tokens` JSON block, and nowhere else. Prose
in this file cites a token path (`tokens.arrival.duration_s`) and never restates its value, because
a number written twice is a number that will disagree with itself. `wowkb.capart` parses the block
for the preview and **generates the addon's `Style.lua` from it** — the two sides of the promise
above cannot drift, because neither transcribes anything by hand.

**Status vocabulary.** There is only one status word left, and it marks a *fact gap*, not a
design debate:

- **open** — the client capability this primitive would need has not been measured
  (`spec.md` §3.6 routing). The style is still declared; what is unknown is whether the client can
  draw it. A preview stamps a visible ⚠ chip on an `open` primitive so the preview never lies
  about what ships.

Everything not marked `open` is simply the style. **No primitive is currently `open`** — the
mechanism stays because it is how the preview refuses to lie about an unmeasured primitive, and
the next one that needs it will find it working.

---

## Part 0 — the loop this file is built for

1. Edit a recipe here — a color, a rate, a placement, a whole new primitive. Numbers go in
   **Part 6**.
2. `uv run python -m wowkb.capart build havoc` — the preview reads this file's tokens.
3. Look at it. Ask for tweaks. Go to 1.
4. When it looks right, `uv run python -m wowkb.capart export` writes Part 6 into the addon as
   `Style.lua` (data) plus the badge art as TGA, and `/cap style` draws every primitive in the
   client. `capart check` fails if either the committed HTML or the committed `Style.lua`
   disagrees with this file.

Nothing in steps 1–3 requires permission from `spec.md`. If a change here would make cap branch on
a sealed value, *that* is the one thing to stop and check — a §3.6 question, not a taste question.

**The preview is a reproduction, not a diagram.** It draws real Blizzard icon art at real
Cooldown Manager size, real vendored sprite frames at their real frame counts and durations,
and composites cap's treatments the way the client would composite them — `SetVertexColor` as a
multiply, never a hue rotation. A preview that recolors art the client could not recolor is worse
than no preview. `wowkb.capart` enforces that mechanically (Part 4).

---

## Part 0.5 — the reading model everything below serves

**Scan the row left to right and press the first button that is not ruled out.** That is the whole
interaction, and `spec.md` §3.1 already blesses it: *"A low-priority button is directed-to by
the **absence** of competing emphasis… the same holds for a hold mark's absence."*

### The operator heuristic

The sentence above is the *principle*. This is the procedure a human actually runs, written down so
that it can be changed on purpose. If a flight says scanning left-to-right is too hard, **this is
the thing that gets edited** — and every treatment below is then re-judged against the new version,
rather than each treatment being tweaked on its own.

```
pass 1 — scan left to right for a POSITIVE cue. If one is present, press it.
pass 2 — scan left to right, skipping:
           · anything Blizzard's swipe has already run down
           · anything wearing at least one RED cue
         press the first item that survives.
```

**The procedure is the authority.** Where a treatment below and the two passes disagree, the passes
win and the treatment is what gets edited. Two things moved to match it:

**What the procedure ruled out — the `withheld` verdict, now deleted.** A verdict may only be
*drawn* from a fact cap is allowed to read. `withheld` — a dim with no badge — was the one
verdict in the vocabulary that broke this: its only driver was that a readable fact came back
**secret**, so the refusal itself became a visible elimination. Pass 2 makes that obviously wrong —
an item cap cannot form an opinion about is an item the scan should simply *reach*, not one it
should skip. The vocabulary is nine verdicts, and a row cap has no opinion about draws whatever its
readable state says: the scan edge, or the swipe, and no badge.

**And `isActive` removed its last subject anyway.** `withheld`'s only user was a charge count read
below full. `C_Spell.GetSpellCharges` seals per member: `isActive` is `NeverSecret` and stays plain
in restricted combat, so "at max charges" is readable in **both** polarities — `false` at 2/2,
`true` below it. There is nothing left for the verdict to mean.

Two consequences the style is built on:

1. **The press is not a thing cap draws.** `press`, `press-promoted` and `below` render
   identically — the scan edge, nothing else. The press is *whatever the scan reaches first*. Cap's
   job is to rule things out convincingly, not to point.
2. **The cue vocabulary is negative by default, with exactly one positive exception.** A cue
   normally draws when a button is ruled *out* and draws nothing when it is clear. A satisfied
   dependency is silence. A red badge is the whole statement — it says *that* something is skipped
   and *why*, in one mark, and nothing else on the row says either.
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
gone. So `capped` is read first and it *redirects* the scan. It is drawn from **one readable fact
about one button**, never from a comparison across the row.

Its scope is narrow: **impending loss, nothing wider.** A positive cue for "you have enough" or
"this is favoured now" is a statement about **rank**, which elimination already carries, and would
be a second voice in pass 1 competing with the first.

The other positive signals (a "banked" light, a green dependency dot, a weave chevron, a promoted
press) remain **parked, not refuted**. `spec.md` §3.6 and `havoc/catalog.md` both record that a
sealed threshold is expressible in **either** polarity, and that stays true.

**Four gates in `wowkb.capart check` hold this line, one per pass plus two on the vocabulary.**

- **Pass 1.** If a scenario wears a positive cue at all, the leftmost entry wearing one must be the
  press. A positive cue is pre-emptive, so a scenario where it points somewhere other than the
  press is a scenario that reads wrong.
- **Pass 2** — the elimination gate (Part 5). The leftmost entry that is neither swiped nor wearing
  a negative badge must be the press, **counting negative cues only**, so the positive cue can ride
  the press without eliminating it.
- **A second positive cue fails `check`.** This is no longer only a vocabulary question: a second
  positive cue is a second pass-1 candidate, so two of them in one row makes pass 1 ambiguous about
  which to press. Adding one is a decision about the *ordering model*, and it means rewriting the
  procedure above to say how the two rank.
- **A declared cue worn by no scenario fails `check`**, since a cue that renders nowhere is
  `spec.md` §3.2's defect at shelf level.

One further `check` assertion keeps this part's own claims mechanical rather than promised: slot 3
belongs to the positive cue (Part 1).

---

## Part 1 — Surfaces (what there is to draw on)

A Cooldown Manager row is a small square icon. These are the places a cue can live. Placement is
a design choice, not a platform constraint, unless marked otherwise.

| Surface | Where | Carries | Notes |
| --- | --- | --- | --- |
| **Icon face** | the art itself | nothing — cap draws no treatment here | **Desaturation is Blizzard's and cap does not draw it.** The CDM already desaturates and re-tints the icon on its own refresh — `SPELL_UPDATE_USABLE` drives icon colour continuously (`cooldown-manager.md:700, :755`), which is the client's built-in "you cannot cast this" channel. cap adding a second one would restate a signal the player already has. |
| **Scan edge** | a thin additive line on the icon edge | one bit: the row is in the scan, or it is not | Static — nothing about it moves (V13). Drawn on cap's own frame, sized to the icon rect, so it needs no host scale-up and cannot reach a neighbour. |
| **Corner badge slots** | three discs hung off the **top-right** corner | one cue each — slots 1–2 (along the top edge) negative, slot 3 (down the right edge) the single positive cue | Filled circles at `tokens.badges.diameter_pct` of icon width, overhanging by `tokens.badges.overhang_px` (V5). Position carries polarity as well as colour. |
| **Cooldown swipe** | the radial dial | remaining time | Can be *restyled* without knowing the time (see V7). |
| **Count tile** | Blizzard's own aura count position | a sealed stack number | Client-owned; cap never learns the value. |
| **Independent bar** | anywhere on screen | one duration, large | Off-icon surface. |

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
Lua sample, and how the preview reproduces it.

### V1 · *(retired)*

The animated flipbook emphasis ring — a `visualalert_ants_flipbook` glow outside the icon edge,
tinted to the lane and pulsed forever. Retired 2026-08-13 in favour of V2's solid border plus the
arrival snap: a row of continuously-glowing rings reads as candles, and CDMProbe measured that
**60 % of real cue-set changes are swaps**, so continuous motion spends its budget on states that
are about to be replaced. The measurement that made the ants sheet the only usable ring — its
neutral saturation — is still true and is kept in `render-rationale.md`; it is simply no longer
load-bearing here.

### V2 · *(retired)*

The lane border — a solid rectangular edge in one of **four hues** (COOLDOWN, ROTATION, FALLBACK,
and CHARGES substituted in off a client charge read), drawn from a generated 16-frame ring flipbook
that played once as a one-shot **arrival snap** when the drawn lane changed. Retired 2026-08-19 in
favour of **V13**, one binary scan edge: the hue ladder had become an informational hint nobody was
reading off, and `spec.md` §3.1's emphasis ladder is carried by **left-to-right scan order plus the
overlays**, not by colour. A fourth hue that *replaced* the role lane made that worse rather than
better — it spent the one channel the ladder had on a fact (this ability has charges) the badge
vocabulary already carries.

**What survives, and where it went.** The role tiers COOLDOWN / ROTATION / FALLBACK are **model**,
not paint: they stay in `spec.md` §3.1, in `Catalog.TIERS`, and in every catalog's `| Lane |`
column, and they now decide only *whether* a row is in the scan. The `charged` flag stays authored
in the catalogs and read by the engine; nothing draws from it. The arrival machinery — the sheet,
its cadence, `tokens.ring` / `tokens.arrival` / `tokens.motion` and `Media/ring.tga` — stays
declared and on the ship path because **Part 7's `arrival-*` entries are still about it**; it is the
live overlay that stopped using it, so `Paint.Border` no longer creates an `AnimationGroup`, walks a
sheet, or owns a rate limiter. The generated sheet's neutral-saturation measurement, and the
argument for a flipbook over a `Scale` animation, are kept in `render-rationale.md`.

### V3 · *(retired)*

The lane pulse — three unequal rates driving the V1 ring's alpha, with a trough-invariant floor and
a per-icon phase offset. Retired with V1: there is no continuous motion left in the style to pace.
The arithmetic behind it (the trough invariant, the unequal-rate argument, the WCAG phase-offset
note) is kept in `render-rationale.md` because the *measurements* stay true and would have to be
re-derived if continuous motion ever came back.

**What survives:** the sealed-**text** flicker limits, which were never about the ring. They are
MIL-STD-1472F / WCAG constraints on blinking legends and they bind any text cue cap ever draws.
They now live at `tokens.text.max_hz` / `.duty` / `.alpha_floor` (see V8).

### V4 · *(retired)*

The veil — a flat dim over the icon face on every row cap had an opinion against. Retired
2026-08-16: **every** skip condition cap has (a readable hold, a sealed hold, `starved`, `overcap`
and both graded curves) expressed itself by dimming the *same* texture, on top of Blizzard's own
desaturation and swipe, so a dark row in flight was the sum of an unknown number of causes and no
one could see which fired. It was also strictly redundant — Part 2.5 *derived* it from cue
polarity, so it never carried a fact the badge beside it was not already carrying. Nothing replaces
it: a skipped row is now the scan edge, a red badge, and whatever Blizzard is already drawing.

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
  for neutral art we do not. Declared `tokens.badges.tint: "shelf"`, which is what puts these frames
  under the Part 4 tint guard.
- **Two shapes the browser gets free and the client does not.** A `border-radius` and a
  `radial-gradient` are one CSS property each; in the client the disc and the halo are art. Both
  are generated white-with-shape-in-alpha (`capart export badges`, Part 4's "author them from a
  script"), the halo fading out at `tokens.badges.halo_falloff` of its radius — the same stop the
  preview's gradient uses.
- **Lua:**
  ```lua
  local plate = slot:CreateTexture(nil, "OVERLAY", nil, 6)
  plate:SetColorTexture(unpack(T.badges.plate.rgb))
  plate:SetAlpha(T.badges.plate.alpha)

  local sprite = slot:CreateTexture(nil, "OVERLAY", nil, 7)
  sprite:SetTexture(T.badges.asset_root .. "/" .. frame)   -- neutral art: tints cleanly
  sprite:SetVertexColor(unpack(T.badges.rgb))              -- multiply, one shared red
  ```
- **Preview reproduction.** `mask-image` (the frame's alpha) + `background-color` (the red). For
  white-with-shape-in-alpha art that composite **is** what `SetVertexColor`'s multiply produces. It
  is not a hue-rotate.

### V5.1 · The four cues

The whole vocabulary. Each is a **single state** that either draws or does not — never a two-state
marker whose satisfied state happens to be invisible. `spec.md` §3.2 says *"a catalog form that
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
preview and the client show the same cadence. A `FlipBook` animation is the wrong tool here: it
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

### V11 · Cooldown hatch

A row the Cooldown Manager says is on cooldown draws diagonal stripes across its whole face:
`tokens.hatch.rgb` at `tokens.hatch.alpha`, offset by `tokens.hatch.phase_pct` of one pitch.
Promoted out of the lab on 2026-08-16 per Part 7 rule 4.

**This restates the swipe deliberately, and that is the point.** V7 says the swipe is the CDM's own
"ruled out" signal and cap has no reason to repeat it — that was true while the swipe was the only
thing on an unremarkable row, and it stopped being true once cap started drawing a scan edge and
badges on everything *around* it. A stock swipe next to a lit edge reads as *less*
marked than the thing beside it, which inverts the meaning. The hatch restores the asymmetry: on
cooldown is now the loudest thing on the row, not the quietest.

**The fact is the CDM's, not cap's, and it is READ rather than remembered.** The hatch draws while
the row's own Cooldown widget is shown *and* that widget is showing a cooldown rather than an
aura's remaining time — two plain booleans, both readable in restricted combat, both Blizzard's
verdict mirrored into widget state. cap computes no timer and reads no clock, and an **unknown**
readiness draws nothing: absence of a hatch is never a claim that a button is up.

⚠ **It is deliberately not an edge latch, and that is a correction rather than a preference.**
V11 shipped on one and the stripes stuck on for a whole flight. The Cooldown Manager's `Available`
alert is raised from the viewer's `OnUpdate`, which runs only for rows the **player** configured an
alert on — so `OnCooldown` arrives for everything and `Available` for almost nothing, and any latch
fed by that channel is a one-way door (`knowledge/addon-dev/cooldown-manager.md` §5.1; measured
320 against 35-on-a-single-row). A read has no memory and so has nothing to get stuck. The edges
stay underneath as the fallback for a client that will not hand over the boolean, with
**`OnCooldownDone`** — an engine-driven widget script, outside the alert system entirely —
supplying the ready edge the alert channel cannot.

⚠ **A charged ability answers differently**: "on cooldown" there means zero charges, a count cap
holds readably, not a recharge timer — a row with a charge banked must not hatch while it reloads
the next one.

The sheet is one tileable white-alpha texture generated by `capart.hatch_sheet` from
`tokens.hatch` (`tile_px`, `pitch_px`, `duty`, `direction`) — Blizzard ships no stripe, hazard or
hatch art, so Part 4's rule applies and this is authored from a script rather than vendored. It
ships to `Media/stripes.tga` under the tint guard, and Part 7's remaining stripe entries draw on
this same sheet at their own colours: geometry is shared because two stripes that disagree on angle
or pitch cannot interleave, and colour and phase are not, because they are what distinguish one
condition from another.

⚠ `pitch_px` must divide `tile_px` or the sheet seams where it wraps; `capart.hatch_sheet` asserts
it. Tiling is `SetTexture(path, "REPEAT", "REPEAT")` plus a `SetTexCoord` wider than 0–1, both set
**once at construction** — `[T2 bug: WoWUIBugs #250, created 2022-08-13, closed]` reports that
re-calling `SetTexture` with the same path and different wrap modes is ignored, so the wrap mode
cannot be changed later. Nothing about the hatch animates: in combat it is `Show`/`Hide` only.

**`phase_pct` is 50 with nothing to interleave with yet.** Half a period is reserved so that a
second stripe condition — if one is ever promoted — lands at phase 0 and the two read as two facts
rather than one mess. On its own the offset is invisible, and that is the correct cost of holding
the slot open.

---

### V12 · Virtual row — a cap-owned icon for a press with no CDM row

A press the Cooldown Manager does not carry draws as a **cap-owned icon** in its own panel:
the spell's icon at `tokens.panel.icon_px`, laid out left to right at `tokens.panel.gap_px`,
anchored per `tokens.panel.anchor`. It wears **V11's hatch, from the same sheet**, and nothing
else — no scan edge, no badge. One fact, one surface.

**Why it exists.** Devourer's Collapsing Star is a real press that outranks Void Ray and has no
frame anywhere in the CDM pool: the castable (`1221167`) is in no category, and the row named for
it (`1227702`) is the *aura*, not the button. An elimination scan cannot land on a button that has
no icon, and no cue can point at one either. The alternative considered and rejected was
re-anchoring the TrackedBuff row into the Essential line; `render-rationale.md` holds why.

**The hatch means the same thing it means on a CDM row** — *not now* — and is drawn from
`tokens.hatch`, the same generated `Media/stripes.tga`.

**A virtual row is one of two kinds, and the kind is fixed by the ability, not by the moment.**

- **Gated** — availability varies, so the row is **hatched by default and clears only on a
  positive readable verdict that the press is available**. Devourer's Collapsing Star is gated:
  access is granted every 30 souls harvested inside Void Metamorphosis.
- **Standing** — availability is a **constant**, so the row draws **clear, permanently**, and asks
  for no verdict at all. Devourer's Consume is standing: no cooldown, no resource cost, no aura
  gate, castable while moving.

⚠ **A standing row is not wallpaper, and the objection that it is misreads the reading model.**
"A badge lit in most states is a mis-ranked row" is a statement about *attention* — a cue must be
noticed, identified and interpreted on every scan, which is expensive when it is nearly always
lit. A permanently-clear icon at the **right end of the panel** costs nothing of the kind, because
elimination only ever reaches it once everything to its left is gone. **Its position already
encodes its rank**, which is Part 0.5's rule in its plainest form: when a fact is stable enough to
express as rank, express it as rank and spend no cue on it. The floor of a priority list is the
most stable fact in it.

**And a standing row is what keeps the sweep from ending in silence.** Without one there are real
states — everything on cooldown, the spender unaffordable — where every entry is swiped or badged,
nothing on either surface is the press, and the correct answer is reachable only from memory. A
standing row is the terminus that makes elimination total: the sweep always lands somewhere.

⚠ **The unknown polarity is inverted here, deliberately, and it is the one rule of V11 this entry
does not inherit.** On a CDM row the icon is present regardless of what cap knows, so an unknown
readiness draws bare and absence of a hatch asserts nothing. A virtual row exists *only* to say
"press this now", so there absence of a hatch is the entire signal — and an unknown drawn bare
would read as a positive instruction. **Unknown therefore draws hatched.** The safe direction on a
CDM row is "say nothing"; on a virtual row it is "say not yet".

**It is additive and it configures nothing.** cap owns these frames, so `spec.md` §4 is not
engaged the way re-anchoring another viewer's frames would be: the Cooldown Manager is neither
written to nor rearranged, and a virtual row appears beside it rather than inside it. The
precedent is `Bars.lua`'s independent countdown, which is likewise cap-owned and additive.

**Not flown.** Part 5 question 8.

---

### V13 · Scan edge — one binary treatment

**A row is in the scan, or it is not.** That is the whole primitive. A row cap has an opinion about
wears a `tokens.ready.line_px` line on the icon edge in `tokens.ready.rgb`; a row it does not, wears
nothing. There is no ladder, no hue, no thickness variation and no motion — **rank is carried by
left-to-right row order plus elimination** (Part 0.5), which is the only ranking channel that
survives a player not having memorised a legend.

- **Additive, at full brightness, on a restrained area.** `SetBlendMode("ADD")`, so the edge reads
  as a *hot line lit over* the icon rather than as a painted frame around it. Perceived glow is
  roughly luminance × area: this keeps the luminance and spends the area, which is what lets
  `tokens.ready.alpha` sit at 1.00 without the row shouting. (`SetBlendMode`'s five values are
  Tier-1 — `frames-textures-animation.md` §5.2.)
- **It sits ON the icon rect**, not outside it. It therefore has no falloff to overlap with, and
  **cannot bleed into a neighbour at any row gap** — the failure the retired V1 ring and the V2
  arrival were both priced against. cap's overlay frame is the item's own rect for the same reason;
  only the corner badges reach past it, deliberately.
- **Nothing moves.** No arrival, no pulse, no flipbook. The shared ticker still exists for the badge
  sprites and the scan edge does not register with it, so a screen full of in-scan rows contributes
  no motion at all.
- **Lua:**
  ```lua
  local edge = CreateFrame("Frame", nil, cap.overlay)   -- NOT the CDM item frame
  edge:SetPoint("CENTER", icon, "CENTER", 0, 0)         -- sized and centred, NOT SetAllPoints
  edge:SetSize(icon:GetWidth(), icon:GetHeight())

  -- Four colour strips, built once, out of combat. No texture file, no tex-coords, no group.
  for _, t in ipairs(Paint.buildRing(edge, T.ready.line_px)) do
    t:SetColorTexture(T.ready.rgb[1], T.ready.rgb[2], T.ready.rgb[3], T.ready.alpha)
    t:SetBlendMode("ADD")
  end

  edge:SetShown(inScan)          -- the only in-combat write this primitive makes
  ```
  The in-combat surface is one `Show`/`Hide`. Everything else happens when the roster is bound.
- **Preview reproduction.** A 1-element `box-shadow: inset 0 0 0 var(--ready-line)` in
  `--ready-rgb` at `--ready-alpha`, composited `screen` — the CSS analogue of an additive multiply
  on white. Same rect, same width, same colour, and nothing animates it there either.

---

## Part 2.5 — Composing a row

The primitives above are drawn together, and the order they compose in is fixed. **A row is a
hatch, a scan edge and badges** — nothing else is drawn on it, and in particular the icon face is not
cap's (Part 1).

1. **The cooldown hatch** (V11), or none. It sits under everything else, directly over the icon
   face, because it is a statement about the button rather than a mark placed on it.
2. **The scan edge** (V13), or none. It is one bit and has nothing to stack with.
3. **A badge per cue** (V5/V5.1), each in the slot its cue owns. A cue named twice is one badge —
   that is how a catalog authors an OR without an OR.

**One condition, one surface.** Every skip a row carries is carried by a mark of its own, in a
place of its own, and by nothing else — so two conditions on one button are two marks rather than
one shared dim that had to pick. That is the whole of the composition rule since V4 was retired:
there is no second surface for several conditions to write to, and therefore no row whose treatment
means an unknown number of things at once. A cue that declares no polarity reads as negative — the
reading that can only be stricter.

⚠ **V11 did not weaken that rule and it is worth saying why, because it looks like it did.** The
hatch is a third surface, but it carries exactly one condition — on cooldown, from the CDM's own
edges — and nothing else writes to it. What the rule forbids is a *shared* surface several
conditions feed; what it permits is as many surfaces as there are conditions. The count of surfaces
was never the invariant.

**The hatch is invisible to the elimination walk, by construction.** It is drawn exactly where the
swipe is drawn, so every row wearing it was already ruled out by *swiped* in pass 2 and no reading
changes. It adds emphasis to a decision the walk had already made — which is why `elimination_gate`
stays a two-term test and does not learn about it.

### The graded cue's curve drives its badge

A **graded** cue is one whose visibility the client decides: cap authors a curve (V9, V10), hands
it to the client with a secret, and the client returns a mapped result cap writes into an alpha
and never reads back. Its badge is present whenever the row draws, and the result *is* its
visibility.

**One curve, one sink: the badge's alpha.** The evaluated result is written straight to the badge
and nowhere else, so the graded cue fades in exactly as far as the client's answer says and the row
carries no second treatment that would have to agree with it. There was a second sink while the
veil existed — and it existed only to stop a badge fading in over a dim that snapped on, saying two
things about one moment. With one surface left that problem cannot arise.

⚠ The curve modulates **visibility, not meaning**. A graded badge at low alpha is the same
statement as the same badge at full, made about a smaller amount; it is never a different cue.

---

## Part 3 — Composition rules

- **`SetVertexColor` multiplies.** Baked-hue art can only be darkened toward its own hue. The
  style therefore uses neutral art wherever it tints — V5's Kenney frames, V11's generated stripe
  sheet and Part 7's generated ring sheet, all measured 0.000. Desaturate-then-tint
  (`SetDesaturated(true)` / `SetDesaturation(0..1)` first, tint the result —
  `knowledge/addon-dev/frames-textures-animation.md:1044-1052`) is the escape hatch for baked art,
  and whether it yields a *clean* hue is **open**: unmeasured in client. A primitive declaring
  `tint: "desaturate+shelf"` builds, but the preview stamps a visible ⚠ on it. Nothing declares it
  today.
- **Don't bundle Blizzard art.** Reference an atlas by name — that ships no asset. Extracted art is
  for measuring and for the preview, never for the addon's `Media/` folder. (Our own CC0 art is a
  different case: it ships, because it is ours.)
- **`SetGradient` resets vertex color to white.** Apply the gradient first, tint second.
- **`SetTexture` / `SetAtlas` / `SetColorTexture` are exclusive** — last call wins. `GetTexture()`
  after `SetAtlas` returns the backing fileID as a *number*, not nil; ask `GetAtlas()` first.
- **Animations don't restore vertex color on stop** without `SetToFinalAlpha`. Every fire-and-forget
  group in the style must land on its final values. V2 sidesteps it entirely — the arrival is a
  frame walk, not an animation — so the remaining subjects are the `capped` halo and the lab.
- **`Show`/`Hide`, never `SetShown`** — `SetShown` is a protected function. *(True but
  mis-framed: protection bites only on **protected** frames, and on cap's own `UIParent` child it
  is unrestricted and measured so. Left as-is because "always `Show`/`Hide`" is a cheap habit to
  keep and costs nothing.)*
- **Set frame strata/level out of combat only.** In combat, confine writes to
  `Show`/`Hide`/`SetVertexColor`/`SetAlpha`, plus the texture-level frame step
  (`SetTexture` for a badge, `SetTexCoord` for V2's ring) that the frame walk needs and that the
  badge vocabulary has been making in combat since it shipped. Nothing re-anchors, re-sizes or
  re-levels in combat; the arrival is painted into the art precisely so it does not have to.
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
uv run python -m wowkb.uiart icon 191427 198013 --data-uri              # spell icons for the preview
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
shape of the Kenney art CDMProbe already reads in client. `capart export ring` writes V2's ring
flipbook the same way, into `Media/` beside `Media/badges/`. The tint guard runs on both paths, so
a baked-hue frame cannot reach the client through a route the preview never rendered. This is not
the "don't bundle Blizzard art" rule's subject: our own CC0 and generated art ships, because it is
ours.

`capart check` gates the ring sheet the way it gates `Style.lua`: it must be on disk and
**byte-identical to what the generator produces today** — a generated asset nobody regenerates is a
stale asset that still passes an existence check.

**The preview contract, and the guard that enforces it.** Icons and sprites embed as base64
`data:` URIs — a preview must render from the file alone (and the Artifact CSP it could one day be
published under blocks every external host), so a CDN `<img src>` renders nothing.
`wowkb.capart` refuses to build a lie:

| Condition | What happens |
| --- | --- |
| `tint: "shelf"` on art the manifest measured non-neutral | **hard error**, naming the measured saturation |
| a CSS tint written as `hue-rotate` | not emitted — the tint path is `mask-image` + `background-color` (or `background-blend-mode: multiply`) |
| `tint: "desaturate+shelf"` | builds, and stamps a visible ⚠ *open* chip on that primitive |
| total base64 over `tokens.budget.max_base64_kb` | a **warning printed by `build`** (and a per-asset table from `capart assets`), never a blocked rebuild; `check` does not test it |

**The tint guard is the shelf's one mechanical promise and it is deliberately art-agnostic.** It
started life guarding the flipbook rings; it now guards the badge sprites and V11's stripe sheet,
because the claim it enforces was never about rings — it is *"art the shelf recolors must be art
`SetVertexColor` can actually recolor."* **`tint: "shelf"` is the token spelling of that claim**,
and the spelling is deliberately colour-source-neutral: it says the colour comes from this file
rather than from the art, and says nothing about *which* colour. ⚠ It used to be spelled `"lane"`,
which read like a reference to a hue that existed — so when the badges moved to `tokens.ready` and
were rewritten to `tint: "ready"`, the guard (which matches a literal) stopped covering them
silently, and `check`'s any-of test stayed green on the ring alone. `check` now asserts the
declaration **per primitive**: every art-bearing key in the token block must declare `"shelf"`,
`"desaturate+shelf"` or a deliberate `"none"`, so a subject can no longer drop out unnoticed.

The asset list and the budget are `tokens.assets` / `tokens.budget`.

---

## Part 5 — What a flight would settle

Look-at-it questions, not measurements. None of them is a reason to hold two styles in this file.

1. **Does a row at rest read as quiet?** Static scan edges and nothing moving — does that read
   as informative, or as furniture the eye stops seeing after ten minutes?
2. **Does the scan edge separate in-scan from out-of-scan at a glance?** V13 spends the whole
   emphasis budget on one bit, so its failure mode is the opposite of the retired V2's: not "a hue
   nobody decodes" but "a line nobody notices". The louder and quieter candidates are in the lab as
   `ready-*` and are meant to be judged beside it in `/cap style`. If a lit row and an unlit row are
   hard to tell apart in a pull, the fix is **area or blend, not a second colour** — a ladder is
   what V2 was retired for.
3. **Do the badges read without a legend at 56 px?** Specifically: does the timer sweep read as
   "waiting" or as a countdown? A countdown reading is a failure of the cue, not of the player.
4. **Does one shared red across three badges under-differentiate?** The shapes are meant to carry
   the distinction. If they do not, the fix is different shapes, not a second hue.
5. **Does elimination alone lead the eye?** The four scenarios with something to the *left* of the
   press (ST-7, ST-10, AoE-2, AoE-3) are the test. If a scenario needs a positive cue to be
   readable, that is the finding that un-parks the positive vocabulary.
6. Does desaturate-then-tint produce a clean hue on baked art? — **open**, needs the client.
   Nothing declares it today; the question stays because the escape hatch is worth having priced.
7. **Does the cooldown hatch add to the swipe or just restate it — and does it read as stripes at
   all?** V11's `--@unverified` marker is on the shipped path, so this is in the acceptance set.
   Three parts. Does a 16 px pitch authored on a 128 px sheet still read as *stripes* once tiled
   across a ~56 px icon, or does it flatten into a wash — `/cap style`'s V11 section draws
   swipe-only beside as-it-ships for exactly this comparison. Does black at 0.50 alpha read as
   **ruled out** rather than as **dimmed**, which is the failure the retired veil died of. And is
   the row now *more* legible in a pull, or merely busier — the honest possibility is that the
   swipe was already enough and the hatch is noise, in which case V11 goes back to the lab.
   ⚠ Watch specifically for the row that **cannot** wear it: one whose first edge has not landed.
   If a hatchless row on cooldown reads as "cap thinks this is up", the unknown-safe default is
   costing more than it saves and needs rethinking, not just documenting.
8. **Does a virtual row (V12) read as part of the same scan, or as a second UI?** It is cap's own
   panel rather than a CDM row, so the risk is that the eye finishes the CDM line and stops. And
   does a *standing* row — permanently clear, forever — read as the terminus of the sweep or as
   wallpaper?

⚠ **The arrival questions left this list with V2.** "Does the snap catch the eye", "does the band
survive minification", "does 16 frames at 40 fps read as motion" — nothing on the shipped path
asks them any more. They are still live questions and they are still asked, in Part 7, by the
`arrival-*` entries, which is where an unadopted treatment belongs.

**And one gate that does not wait for a flight.** `wowkb.capart check` asserts, for every
scenario: *the leftmost entry that is neither swiped (`cd`) nor carrying a red cue must
be the entry the doc calls the press* — `weave` skipped over, since it is off the GCD and pressed
in parallel. That is question 5, mechanised. All 13 Havoc scenarios pass it today. If a future
scenario cannot lead the eye to its press by elimination, this fails **by name** rather than
someone noticing months later.

---

## Part 6 — The tokens

**This block is the style.** Every number cap draws with is here and nowhere else. `wowkb.capart`
parses it for the preview and generates the addon's `Style.lua` from it verbatim; prose cites
paths into it. Editing a value here and rebuilding is the whole loop.

`Style.lua` carries data only — `Treatment.lua` and `Paint.lua` are the logic that reads it, which
is what keeps the generated file free of functions and diffable. One key never reaches it:
Part 7's `lab`, which is by construction not the
style. Everything else crosses unchanged, plus where the exported art landed.

Colors are `[r, g, b]` in 0–1, the way `SetVertexColor` wants them.

<!-- render-tokens v1 -->
```json
{
  "version": 2,
  "ready": {
    "_comment": "IN THE SCAN. One treatment, no roles, no motion. An icon either participates in the read or it does not; rank comes from row order and elimination, not from a hue ladder. Full brightness on a restrained AREA: additive, so it reads as a hot edge rather than as a wash, and it sits ON the icon rect so it can never bleed into a neighbour at any row gap.",
    "rgb": [1.00, 0.86, 0.45],
    "alpha": 1.00,
    "line_px": 2
  },
  "ring": {
    "texture": "ring",
    "tile_px": 64,
    "grid": 4,
    "frames": 16,
    "thickness_px": 2,
    "corner_px": 4,
    "travel_px": 5,
    "gutter_px": 1,
    "tint": "shelf"
  },
  "motion": {
    "tick_s": 0.025
  },
  "arrival": {
    "from_scale": 2.00,
    "duration_s": 0.40,
    "smoothing": "OUT",
    "from_alpha": 0.00
  },
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
    "tint": "shelf",
    "plate": { "rgb": [0.00, 0.00, 0.00], "alpha": 0.78, "scale": 1.12 },
    "halo_falloff": 0.70,
    "asset_root": "previews/assets/kenney",
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
  "hatch": {
    "texture": "stripes",
    "tile_px": 128,
    "pitch_px": 16,
    "duty": 0.5,
    "direction": "down",
    "rgb": [0.00, 0.00, 0.00],
    "alpha": 0.50,
    "phase_pct": 50,
    "tint": "shelf"
  },
  "panel": {
    "icon_px": 50, "gap_px": 6,
    "anchor": "BOTTOM", "x": 0, "y": 190, "grow": "RIGHT"
  },
  "verdicts": {
    "cd":             { "scan": false, "swipe": true,  "hatch": true, "cues": [] },
    "weave":          { "scan": true,  "swipe": false, "cues": [] },
    "hold-readable":  { "scan": true,  "swipe": false, "cues": ["blocked"] },
    "hold-sealed":    { "scan": true,  "swipe": false, "cues": ["blocked"] },
    "starved":        { "scan": true,  "swipe": false, "cues": ["starved"] },
    "overcap":        { "scan": true,  "swipe": false, "cues": ["overcap"] },
    "press":          { "scan": true,  "swipe": false, "cues": [] },
    "press-promoted": { "scan": true,  "swipe": false, "cues": [] },
    "below":          { "scan": true,  "swipe": false, "cues": [] }
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

  "lab": {
    "_comment": "NO AUTHORITY. Part 7. Nothing in `verdicts` or `cues` may name anything in here; capart enforces it. A treatment leaves the lab by being MOVED into Parts 1-6, never by being cited from here. The stripe entries below draw on `tokens.hatch`'s sheet, which is the STYLE's — a lab entry citing the style is the legal direction.",
    "_arrival_stage": { "neighbours": 2 },

    "stripes-l3-hold": {
      "draws": "stripes",
      "title": "Red stripes on a sequencing hold",
      "asks": "When cap is holding a button for something else, does a stated condition across the face read better than a badge alone — and does it still read as *held for a reason* rather than as *broken*?",
      "rgb": [0.95, 0.30, 0.30],
      "alpha": 0.45,
      "phase_pct": 0,
      "cells": [
        { "kind": "icon", "ability": "The Hunt", "verdict": "hold-readable",
          "stripes": ["self"],
          "caption": "<b>readable hold</b> — the corner badge says <em>why</em>, the stripes say <em>not this</em>. Both, on one icon." },
        { "kind": "icon", "ability": "Essence Break", "verdict": "hold-sealed",
          "stripes": ["self"],
          "caption": "<b>sealed hold</b> — the same statement drawn from a sealed fact. If the two holds do not look alike here, the player is being asked to decode where the fact came from." },
        { "kind": "icon", "ability": "The Hunt", "verdict": "below", "cues": [], "stripes": [],
          "caption": "<b>control</b> — the same icon untreated. The comparison is the point; a treatment that only reads beside its own caption has not read." },
        { "kind": "sheet",
          "caption": "the tiling sheet itself, at this entry's colour — pitch and angle, unmasked by any icon." }
      ]
    },

    "stripes-l5-starved": {
      "draws": "stripes",
      "title": "Red stripes on `starved`",
      "asks": "Does the same red that marks a hold also read as *you cannot afford this*, with only the badge to separate them — or does one red across two different reasons under-differentiate?",
      "rgb": [0.95, 0.30, 0.30],
      "alpha": 0.45,
      "phase_pct": 0,
      "cells": [
        { "kind": "icon", "ability": "Chaos Strike", "verdict": "starved",
          "stripes": ["self"],
          "caption": "<b>cannot afford it</b> — a Fury spender short of its cost, drawn by its own render with its own parameters." },
        { "kind": "icon", "ability": "Chaos Strike", "verdict": "below", "cues": [], "stripes": [],
          "caption": "<b>control</b> — affordable, untreated." },
        { "kind": "sheet",
          "caption": "the sheet at this entry's colour — the same red and the same phase as L3, because it is the same kind of statement." }
      ]
    },

    "arrival-control-sweep": {
      "draws": "arrival-sweep",
      "title": "The declared snap at four from_scale values, alone and beside neighbours",
      "asks": "Is the `#` the overhang? Today's border is drawn 2.00x on a frame 2px narrower than the row pitch, so it crosses its neighbours and their static borders. If the hash is absent in isolation at every value and appears beside neighbours only above the low values, the diagnosis holds and the fix is one number — and the three variants below are unnecessary.",
      "from_scale_sweep": [2.00, 1.50, 1.25, 1.10]
    },

    "arrival-b-relative": {
      "draws": "arrival-relative",
      "title": "The ring built from anchors alone — thickness as an offset, no SetWidth/SetHeight",
      "asks": "Does a strip that takes all four of its extents from anchors scale differently from one that takes a thickness from SetWidth/SetHeight? Pixel-identical at rest by construction; the question is whether the Scale animation treats the two the same. A negative result exonerates the ring construction in the client rather than only on paper."
    },

    "arrival-c-thickness": {
      "draws": "arrival-thickness",
      "title": "No Scale animation at all — a fat ring flashed alpha-only over the resting one",
      "asks": "Read as arrival without any geometry moving? Two pre-built rings, the resting one and a fat one; the fat one rests at alpha 0 and is flashed up and back. The border never exceeds its own rect, so it can never touch a neighbour at any value.",
      "fat_mult": 3.0,
      "duration_s": 0.35
    },

    "arrival-d-ghost": {
      "draws": "arrival-ghost",
      "title": "A ghost ring pings outward and fades; the declared border never animates",
      "asks": "Does an outward ping read as arrival better than an inward snap, and does it stay off the neighbours? The declared border is built as today and never touched; a second frame carries its own ring and is the only thing that scales.",
      "from_scale": 1.00,
      "to_scale": 1.25,
      "from_alpha": 1.00,
      "to_alpha": 0.00,
      "duration_s": 0.35,
      "smoothing": "OUT"
    },

    "ready-halo": {
      "draws": "ready-glow",
      "title": "An additive outer halo that flares on arrival, then decays to a resting floor",
      "asks": "Can a glow OUTSIDE the icon rect say `ready` without saying `press now`? The flare spends the arrival budget and then decays to rest_alpha rather than to nothing, so the resting row still reads as lit. The failure to watch for is the candles verdict: four of these at once smearing into one lit region rather than four ready buttons.",
      "rgb": [1.00, 0.86, 0.45],
      "inner_border": false,
      "rest_alpha": 0.26,
      "flare_alpha": 1.00,
      "glow_px": 7,
      "flare_mult": 1.8,
      "decay_s": 0.90,
      "cells": [
        { "ability": "Eye Beam", "verdict": "press", "caption": "Alone \u2014 the flare, then the resting floor." },
        { "kind": "row", "abilities": ["Eye Beam", "Blade Dance", "Chaos Strike", "Felblade"],
          "verdict": "below",
          "caption": "Four ready at the true row pitch \u2014 <b>the candles test</b>. If this reads as one lit region rather than four lit buttons, the halo is too wide for a 6\u202fpx gutter." }
      ]
    },

    "ready-hairline": {
      "draws": "ready-line",
      "title": "Full brightness, restrained area \u2014 a 1px hot line at the icon edge",
      "asks": "Does holding luminance and cutting AREA read as bright-but-quiet, where cutting alpha read as ghosted? Perceived glow is roughly luminance times area, so this keeps the first and spends the second. It also cannot smear: a hairline has no falloff to overlap a neighbour with.",
      "rgb": [1.00, 0.86, 0.45],
      "inner_border": false,
      "rest_alpha": 1.00,
      "line_px": 1,
      "cells": [
        { "ability": "Eye Beam", "verdict": "press", "line_px": 1, "caption": "<b>1px</b> \u2014 no flare, no motion, full brightness." },
        { "ability": "Eye Beam", "verdict": "press", "line_px": 2, "caption": "<b>2px</b>" },
        { "ability": "Eye Beam", "verdict": "press", "line_px": 3, "caption": "<b>3px</b>" },
        { "kind": "row", "abilities": ["Eye Beam", "Blade Dance", "Chaos Strike", "Felblade"],
          "verdict": "below",
          "caption": "Four at once. A hairline cannot bleed, so the question here is the opposite one: is it still visible in peripheral vision?" }
      ]
    },

    "ready-altglow": {
      "draws": "ready-glow",
      "title": "Blizzard's own downgrade \u2014 a static halo with no animation at all",
      "asks": "Is the loud part the GLOW or the MOTION? This is ProcAltGlow's answer transcribed: keep a small glow, delete every animation. It is the control for ready-halo \u2014 if the static version reads as ready just as well, the flare is decoration and the arrival belongs to the border alone.",
      "rgb": [1.00, 0.86, 0.45],
      "inner_border": false,
      "rest_alpha": 0.62,
      "glow_px": 11,
      "cells": [
        { "ability": "Eye Beam", "verdict": "press", "caption": "Alone \u2014 static. Nothing here moves, ever." },
        { "kind": "row", "abilities": ["Eye Beam", "Blade Dance", "Chaos Strike", "Felblade"],
          "verdict": "below",
          "caption": "Four at once, all static. A resting row that never changes is the cheapest thing to ignore \u2014 which may be the point, or may be the defect." }
      ]
    },

    "ready-breathe": {
      "draws": "ready-glow",
      "title": "A low-intensity breathe with a non-zero floor",
      "asks": "Does a slow breathe between a floor and full read as `alive and ready` rather than `press now`? The floor is what separates this from a blink: the treatment is never absent, only varying. The rate is deliberately slower than a proc loop \u2014 the question is whether ANY periodic motion reads as urgency once four of them are running out of phase.",
      "rgb": [1.00, 0.86, 0.45],
      "inner_border": false,
      "rest_alpha": 0.40,
      "flare_alpha": 1.00,
      "glow_px": 12,
      "period_s": 2.60,
      "cells": [
        { "ability": "Eye Beam", "verdict": "press", "caption": "Alone \u2014 floor to peak and back, continuously." },
        { "kind": "row", "abilities": ["Eye Beam", "Blade Dance", "Chaos Strike", "Felblade"],
          "verdict": "below",
          "caption": "Four at once. Each starts at its own phase, because four breathing in lockstep is one region blinking \u2014 the failure Part 3 already names for the retired lane pulse." }
      ]
    }
  }
}
```

**Reading the verdict table.** `scan` is whether the row is in the scan at all — `cd` is
the only row that is not, because Blizzard's swipe has already ruled it out and an edge would
just be noise on a dead button. `swipe` is Blizzard's own dial, which cap does not
draw and does not restyle (V7); it appears here so the preview can reproduce the row faithfully.
`cues` names badge cues (V5.1) by key into `tokens.cues`, and each cue's `slot` fixes where it
lands. A cue whose token carries `open: true` draws with a ⚠ chip in the preview and produces
**no hint in the addon** until it is measured (`spec.md` §3.6); none does today.

**`press`, `press-promoted` and `below` render identically, and that is the point.** The press is
"the leftmost thing not ruled out," not a thing cap draws (Part 0.5). The verdict *names* are kept
because `havoc/scenarios.md` needs them to state its argument — `press-promoted` still records
*why* a windowed spender outranks a lit cooldown, and re-drawing that distinction is a one-line
shelf edit if a flight asks for it.

**The verdict vocabulary is closed.** These nine keys are the whole set a scenario may use;
`wowkb.capart` errors on anything else.

---

## Part 7 — The lab

**Everything above this line is the style. Nothing below it is.**

Parts 1–6 declare one treatment per primitive because a document holding two answers cannot be
rendered — the generator would have to choose, which puts the decision back in the tool. That rule
stands. But it made *trying* something expensive: the only way to see a new idea was to overwrite
the declared style and remember to put it back. So the lab is where an idea gets drawn without
being adopted.

**The four rules, and `wowkb.capart` enforces rules 1 and 2.**

1. **Nothing in `verdicts` or `cues` may name anything in `lab`.** The lab is unreachable from
   `havoc/scenarios.md` by construction — a scenario cannot accidentally start depending on an
   experiment. `capart build` errors if the reference exists (`validate_lab_isolation`).
2. **The lab never draws in a CDM row.** It renders in its own section of the preview, under its
   own heading, after the declared primitives — **and, since 2026-08-16, it may also be drawn by
   the in-game `/cap style` gallery.** The gallery is exempt because it is not a live row: it draws
   on cap-owned frames, in a panel you opened on purpose, and shows nobody a CDM row. That exemption
   exists because you cannot judge whether a treatment *renders* — how a mask tiles, what a
   `SetVertexColor` multiply actually looks like over Blizzard's own icon art — from a browser. A
   preview is an argument about the client; the gallery is the client.
   **What has not moved is the live overlay.** So the lab crosses into the addon through its own
   generated file and its own global: `Lab.lua`, `ns.LabStyle`, written by
   `wowkb.capart export lab` alongside its art in `Media/lab/`. It is deliberately *not* a `lab`
   key on `ns.Style`, because every live module already reads `ns.Style` and that would leave the
   guarantee resting on everyone remembering. The enforcement is the **`LabStyle` reach gate** in
   `capart check`: `ns.LabStyle` may be named by `Lab.lua` and `StylePanel.lua` and by nothing
   else, and a reference from `Overlay.lua`, `Treatment.lua`, `Paint.lua`, `Sense.lua` or a catalog
   is a hard failure.
3. **The lab has no authority.** It is not a proposal, a shortlist, or a plan of record. It is
   pixels you can look at. `render-rationale.md` argues; the lab *shows*; neither decides. Shipping
   the art is not adoption — a texture on disk that only a gallery draws has decided nothing.
4. **A treatment leaves the lab by being MOVED**, into Parts 1–6 with its numbers, and deleted from
   here. Never by being cited from here. If two entries survive a flight, one of them still loses.
   Promotion is unchanged by the gallery: being *drawable in the client* is not being *drawn on a
   row*.

Each entry carries an `asks` — the question it exists to answer. An entry that cannot say what it
is asking is decoration and should be deleted.

**Three earlier entries are gone from here**, per rule 4. **L1 `border-arrival`** → **V2** and
**L2 `badge-slots`** → **V5** on **2026-08-13**, the latter with the cue vocabulary rewritten
negative-only; **L4 `stripes-l4-cooldown`** → **V11** on **2026-08-16**, taking the shared stripe
sheet with it. All three are drawn above, as the style, not here.

### The shared stripe asset — now the style's, at `tokens.hatch`

The two entries below draw diagonal stripes, and **the sheet is the only thing they share with each
other and with V11**. It used to live here as `lab._sheet`; when L4 was promoted on 2026-08-16 the
sheet went with it, because the style cannot depend on an asset the lab owns. It is now
`tokens.hatch` — geometry, and V11's own colour and phase — and these entries cite it.

**A lab entry naming the style is the legal direction.** Part 7 rule 1 forbids `verdicts` and
`cues` from naming the lab, so that an experiment cannot become load-bearing without being adopted.
The reverse carries no such risk: an experiment borrowing a shipped sheet decides nothing, and the
alternative is a second identical texture on disk that can silently drift from the first.

**Everything except the geometry is per-render, and deliberately so.** Each entry supplies its own
`rgb`, its own `alpha` and its own `phase_pct`; in the client that is `SetVertexColor` plus a
`SetTexCoord` offset, and in the preview it is `background-color` plus a `mask-position`. There is
**no shared "this row is striped" flag** for several conditions to write and something else to read
back. When a striped row turns up in a flight, the stripes belong to exactly one condition and you
can say which.

The one generator feeds every surface: the preview gets it as a `data:` URI, and `capart export
hatch` writes it as a 32-bit TGA to `Media/stripes.tga` — a **style** path, beside the ring, not
under `Media/lab/` — under the same tint guard the shipped badge art passes (measured 0.000 mean
saturation: white RGB, the pattern in alpha only, so no hue can be baked in without the guard
failing). The gallery reads the same file through `Lab.lua`'s `_sheet`, whose `texture_root` and
`texture` are generated; the addon never builds that string itself.

### L3 · `stripes-l3-hold` — red stripes on a sequencing hold

A row cap is holding for something else already wears the red `blocked` badge. This asks whether
it should also wear a **stated condition across the face**: `lab.stripes-l3-hold.rgb` at
`lab.stripes-l3-hold.alpha`, at the sheet's own phase (`phase_pct` 0).

The claim under test is that a badge says *why* in a corner and a stripe says *not this* across
the whole button, and that the second one is what the eye catches without decoding. It is drawn on
both a **readable** hold (The Hunt) and a **sealed** one (Essence Break) side by side, because if
those two do not look identical the player is being asked to decode where a fact came from — which
is a thing cap has no business making visible. The third cell is the same icon untreated.

⚠ Stripes subtract no light. This is not the veil in a new colour: nothing here dims, and if the
entry ends up reading as "dimmer" rather than as "conditioned", it has failed.

### L5 · `stripes-l5-starved` — red stripes on `starved`

A spender you cannot afford draws stripes from **its own** render, with its own parameters:
`lab.stripes-l5-starved.rgb` at `lab.stripes-l5-starved.alpha`, phase 0.

It uses **the same red as L3** because it is the same *kind* of statement — cap hinting against a
press — and for no other reason. There is no rule here that negative things are red, and none is
being proposed; if a later entry hints against a press in a different colour, nothing in this file
has to change. Equally, if the three renders turn out to be drawing something identical, **that is
an observation that may earn a shared recipe**, not a rule to author in advance.

⚠ One red across two different reasons may under-differentiate, with only the corner badge
separating "held" from "cannot afford". That is what the entry asks. The fix, if it fails, is not
automatically a second hue — Part 5 question 5 is the same question about the badges, and its
answer there was *different shapes, not a second colour*.

### The arrival-snap variants — `arrival-*`

Four entries that share a subject rather than an asset: **the one-shot arrival snap — retired from
the style with V2 — and what it draws when a row has neighbours.** They are the lab's first entries that **only** the `/cap style`
gallery can draw — CSS has no four-strip ring, so the preview shows their titles and their `asks`
and says where to look. That is the exemption's whole point: an argument about how the client
scales a frame is not settleable in a browser.

The shared stage is `lab._arrival_stage`, carrying **`neighbours`** — how many bordered rows sit on
each side of the subject. It deliberately does **not** restate the row pitch: that is
`surfaces.icon_px + surfaces.row_gap_px` and already declared, and a second copy of a number is a
second thing to keep true.

**The diagnosis under test**, argued from the declared values: at the time it was recorded the
border frame was the icon plus `2 × PAD` = 60 px, so `arrival.from_scale` 2.00 drew it 120 px wide
— **30 px of overhang per side** against a row pitch of 62 px. (V13's edge is on the icon rect and
`PAD` is gone, which shrinks the numbers but not the argument: 2.00× still overhangs 28 px.) `Overlay.lua` puts the overlay at `HIGH` level 4, so nothing
occludes the overhang; it crosses the neighbours and their own static borders, and two crossing
pairs of lines that overhang past the crossing is a `#`. The four-strip ring itself is **exonerated
on paper** — horizontals take both x-extents from anchors and verticals both y-extents, so no strip
can overhang its own frame at any scale.

- **`arrival-control-sweep` is the falsifier and comes first.** The **retired four-strip ring under
  a `Scale` animation** — `Paint.Ring`, which survives only to feed these four entries and is no
  longer what V2 draws — at each of `from_scale_sweep`, each drawn twice: once with nothing within
  reach, once with `_arrival_stage.neighbours` bordered rows on each side at the true pitch.
  ⚠ **What this now settles has changed.** V2 already moved to a flipbook that cannot draw outside
  its own cell, so this no longer chooses the fix. It tests the *reason* V2 was rebuilt: if the hash
  never appears in isolation and appears beside neighbours only at the high values, overhang was the
  cause and the flipbook removed it by construction. If the hash shows on an **isolated** icon at any
  value, the overhang story was wrong, the flipbook fixed it by accident, and B, C and D become live
  again.
- **`arrival-b-relative`** replaces `SetWidth`/`SetHeight` with a third anchor, so thickness lives in
  the same coordinate system as the rest of the rect. Pixel-identical at rest, by construction.
- **`arrival-c-thickness`** removes the `Scale` animation entirely: a resting ring and a **fat** one
  at `fat_mult`, flashed alpha-only over `duration_s`. It carries **no scale key, and that absence
  is the statement.** ⚠ The fat ring rests at alpha 0 and animates up from it — animations restore
  the *pre-animation* alpha on both exit paths, so a fat ring resting visible would leave every row
  wearing a permanent double border. ⚠ Nothing here animates `SetHeight`/`SetWidth`: those are
  protected resize calls and outside cap's in-combat allowance, which is exactly why the treatment
  is a **pre-built pair** rather than a growing strip.
- **`arrival-d-ghost`** leaves the declared border alone and gives the ping its own frame:
  `from_scale` → `to_scale` with alpha `from_alpha` → `to_alpha`, i.e. **outward and fading** rather
  than inward and arriving. At 1.25 it overhangs ~7.5 px and never reaches a neighbour's centre. ⚠ It
  must **land invisible**: scale restoration on `Stop()` is unmeasured, so the ghost is hidden
  explicitly on finish rather than trusted to restore.

### The readiness treatments — `ready-*`

Four entries sharing a subject: **what a row should look like when an ability is merely
ELIGIBLE.** They are the family **V13 came out of**: the declared style's answer is now the scan
edge, which is `ready-hairline` at 2 px, and the other three are the louder and quieter candidates
it was picked over. They stay because that choice was made on paper and Part 5 question 2 is the
one that settles it in the client. The client's own answer, the stock proc glow, over-claims: it fires off `SPELL_ACTIVATION_OVERLAY_GLOW_SHOW`, which means
*"the game core marked this spell empowered"* and knows nothing about whether pressing it wastes a
resource. A glow that says **press now** about a fact that is only **now available** is the thing
`spec.md` §1 exists to refuse.

**Why these are additive and the retired alpha ladder was not.** Reducing the alpha of a `BLEND`
layer does not dim a light, it makes the art partially present — the "ghosted" read that killed
earlier attempts. An `ADD` layer at low alpha is still emission, only less of it. The preview draws
this with `mix-blend-mode: plus-lighter`, which is exactly additive; the client spelling is
`SetBlendMode("ADD")`. There is a second reason to keep away from dimming: **the Cooldown Manager
already owns it.** It desaturates on cooldown and tints the icon through distinct not-usable /
not-enough-mana / out-of-range colours, so a dimmed row already means *you cannot press this*.

⚠ **Additive over a dark page flatters itself.** The preview's background is near-black and every
one of these will look better here than in a raid. That is a `/cap style` question.

**Every entry is drawn twice: alone, and as four at the true row pitch.** The second cell is the
**candles test** — the one flown verdict against continuous rings was *"the tier glows read as
candles"*, and it traced to how much of the row was lit at once, not to any single icon. An entry
that reads beautifully alone and smears into one lit region at four is a failure this file has
already seen once.

- **`ready-halo`** is the outer glow: a radial falloff drawn **outside** the icon rect at
  `glow_px`, flaring to `flare_alpha` at `flare_mult` and decaying over `decay_s` **to
  `rest_alpha`, not to zero** — so the arrival is spent on the transition and the row still reads
  as lit afterwards. ⚠ At `glow_px` 7 against a 6 px gutter it overhangs its neighbour's rect by
  1 px, measured. That is deliberate and is what the four-up cell is asking about; a falloff that
  reaches a neighbour is not automatically a smear, but it is the thing to look at first.
- **`ready-hairline`** is the opposite trade: **full brightness, minimal area.** Perceived glow
  goes roughly as luminance × area, so this holds the first and spends the second — where the
  retired ladder cut luminance and lost the emission. It has no falloff and therefore cannot bleed
  at any gutter, which turns the four-up question inside out: not *does it smear*, but *is it still
  there* in peripheral vision.
- **`ready-altglow`** is **Blizzard's own downgrade, transcribed**: `ProcAltGlow` is a static 49×49
  glow with **no animation at all**, swapped in for both proc flipbooks when the reduce-highlights
  setting is on. It is the control for `ready-halo` — if static reads as ready just as well, the
  flare is decoration and arrival stays the border's job alone.
- **`ready-breathe`** is the CDM's own visual-alert flash: a slow alpha cycle with a **non-zero
  floor**, so the treatment is never absent, only varying. Its four-up cell staggers the phase,
  because rings pulsing in lockstep read as one blinking *area* — the failure already recorded for
  the retired lane pulse.

- **`ready-flare-breathe`** is the two combined, and it is the client's own structure: on an action
  button `ProcStartAnim`'s `OnFinished` starts `ProcLoop`, a one-shot burst handing off to a steady
  loop. The preview does it by **delaying** the cycle by the burst's own `decay_s` — an animation
  with the default fill mode does not touch its property before it starts, so the flare owns the
  opacity alone and the cycle then takes over from the floor it landed on. It keeps `ready-breathe`
  beside it deliberately: without the pure cycle as a control there is no way to tell whether the
  burst added anything or was simply swallowed.

⚠ **These five are alternatives, not a set.** Rule 4 applies: at most one leaves, by being moved
into Parts 1–6 with its numbers. Two of them surviving a flight still means one loses.

### What is NOT here

None of these is on the **style's** ship path. `capart export badges` writes no lab art; the lab's
own generated textures go out under `capart export lab`, into `Media/lab/`, and `capart check`
requires a TGA for each asset the lab declares — which is a currency gate on a gallery, not
authority. The lab still has none (rule 3): art on disk that only `/cap style` draws has decided
nothing. Promotion means moving an entry into Parts 1–6, at which point it joins the style's export
like everything else there.
