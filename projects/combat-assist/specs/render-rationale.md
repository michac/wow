# Combat Assist Plus — why the render shelf says what it says

**What this file is for:** the reasoning, the alternatives, and the things tried and rejected
behind `render-shelf.md`. It has **no authority over anything**. The shelf declares; this
explains. If the two disagree, the shelf is right and this file is stale.

It exists because the shelf must declare exactly one style — an artifact generated from a document
holding two answers renders neither — and because deleting the reasoning along with the rejected
option is how a decision gets re-litigated six weeks later by someone who cannot see what was
already weighed.

---

## Retired 2026-08-13 — the ring ladder, and why its arithmetic is kept

**Everything under this heading described the animated flipbook ring (shelf V1) and the lane pulse
that drove it (V3), both retired on 2026-08-13 when the lab's solid-border-plus-arrival entry was
promoted into V2.** None of it describes what cap draws today.

It is kept, in full, because the **measurements** stay true and would otherwise have to be
re-derived from scratch. The trough invariant is arithmetic about lane alphas; the unequal-rate
argument and the phase-offset note are perception and safety findings; the tintability table is a
measurement of real Blizzard art that has not changed. If continuous motion ever comes back — and
Part 5's question 2 is exactly the flight that could bring it back — this is the file that says
what was already known, rather than the file that says the decision was arbitrary.

The one piece of it that did **not** retire is the sealed-text flicker cap
(MIL-STD-1472F / WCAG). It was never about the ring; it now lives at `tokens.text.*` and binds any
text cap blinks.

### Why motion was the primary channel

The lane ladder has to survive three things at once: peripheral vision (the player is watching the
boss, not the CDM), dichromacy (~8 % of men), and a small icon at real size.

- **Hue alone fails all three.** Gold-vs-blue collapses under greyscale and is nearly invisible at
  the edge of the visual field.
- **Luminance alone works but is coarse.** Three brightness steps on top of *arbitrary spell art*
  is a low-contrast ladder — the art underneath already varies more than the ladder does.
- **Rate is pre-attentive and survives everything.** Different flicker rates are separable in
  peripheral vision and are entirely orthogonal to color.

So: rate is the signal, luminance is monotone underneath it, hue is redundant reinforcement. That
ordering is what `render-shelf.md` V3 encodes. The greyscale-collapse control in `ClientLab/Mock.lua`
existed to test exactly this — collapse hue to luminance and see whether the ladder still ranks. It
did.

**The rates are deliberately unequal** (`tokens.lanes.*.pulse_hz`). Three rings pulsing in lockstep
read as one flashing *area*, which is the opposite of a ladder: the eye sees a region blinking, not
an ordering. Unequal rates also make the set impossible to perceive as a single event, which is
half of why the WCAG argument below holds.

### The trough invariant — where the retired `tokens.pulse.floor` came from

The pulse multiplies its lane's alpha, so pulse *depth* eats lane *separation*. With the shelf's
lane alphas (COOLDOWN 1.00, ROTATION 0.78, FALLBACK 0.50) and a floor `f`, the middle lane's
trough is `0.78 × f` and the low lane's peak is `0.50`:

| floor | ROTATION trough | FALLBACK peak | margin |
| ---: | ---: | ---: | ---: |
| 0.68 | 0.530 | 0.500 | **0.030** |
| 0.65 | 0.507 | 0.500 | 0.007 |

0.030 is a margin; 0.007 is not — at 0.65 the ladder's bottom two rungs visually merge at the
wrong moment in the cycle. Hence the floor. The top two lanes *do* cross (COOLDOWN's trough 0.680
sits below ROTATION's peak 0.780) and that is intentional: they are told apart by **rate**, the
primary channel, and forcing brightness separation there would only flatten the pulse into
near-nothing.

This is arithmetic, not taste. If a lane alpha changes, the floor has to be re-derived.

### The phase offset was a safety requirement, not a design flourish

`tokens.pulse.phase_offset_s` staggers each icon's pulse by its index. Fourteen icons flashing in
synchrony is a single large flashing area and lands squarely in WCAG 2.3.1 territory; fourteen
flashing independently do not sum into one perceived flash. The text-cue caps
(`tokens.pulse.text_max_hz` / `.text_duty` / `.text_alpha_floor`) are MIL-STD-1472F's numbers for
blinking legends, applied for the same reason.

Neither is negotiable in the way a hue is. They can be *implemented* differently; they cannot be
dropped.

### Why the neutral ants sheet, and not the prettier ones

`SetVertexColor` **multiplies**. Baked-hue art can therefore only ever be darkened toward its own
hue — a gold ring cannot be made blue. That single fact decides the ring, because a three-lane
ladder needs three hues from one sheet.

Measured mean saturation over visible pixels (`raw/uiart/manifest.json`, `wowkb.uiart`):

| Atlas | Grid / frames | Mean saturation | Verdict |
| --- | --- | ---: | --- |
| `visualalert_ants_flipbook` | 6×5 / 30 | **0.00** | neutral — reaches any hue at full strength |
| `ui-cooldownmanager-alert-flipbook` | 11×2 / 22 | 0.31 | baked; Blizzard ships its own tints of it |
| `onebutton_procloop_flipbook` | 6×5 / 30 | 0.69 | gold only |
| `ui-hud-actionbar-proc-loop-flipbook` | 6×5 / 30 | 0.74 | gold only |
| `rotationhelper_ants_flipbook` | 6×5 / 30 | 0.91 | blue only |

The proc-loop ring is the better-looking one and was the ring `Mock.lua` listed first, on the
grounds that it "was flown and chosen." It is still not usable as the lane ring: it can carry
COOLDOWN and nothing else. Choosing it would mean either three different sheets with three
different symmetry orders and felt speeds (see the shelf's "one dial, three parts"), or abandoning
the hue channel entirely.

**The escape hatch, and why it is not the plan.** `SetDesaturated(true)` first, then tint, should
in principle make any sheet neutral. Whether the result is a *clean* hue rather than a muddy one
is unmeasured in client — so it stays `open`, and any primitive declaring
`tint: "desaturate+lane"` renders with a visible ⚠ in the artifact. If that measurement comes back
clean, the proc-loop ring becomes available again and this decision is worth revisiting.

## The static border: dismissed, then chosen — and the difference between the two

cap's shipped `Treatment.lua` draws four white `SetColorTexture` strips forming a rectangular ring,
1–3 px by lane, with a 2 px bleed. No art, no animation, no atlas — the cheapest possible
treatment.

**It was dismissed on 2026-08-13 for a good reason and re-chosen the same day for a better one,**
and those are not the same event.

The dismissal: the border was never *chosen*. It was the only thing permitted by a rule the spec
used to carry — *treatments are static; motion is introduced only for a specific observed
problem* — and that rule was an experiment written in as if it were a boundary. When it was struck,
the border lost its only argument, which was "it is what is compiled today." That is a
`backlog.md` fact, not a design one. The paragraph that replaced it said the border *"remains an
honest fallback if the flight says the rings are too much,"* and that *"would be a shelf edit, made
by looking at something — not a rule."*

Which is precisely what happened. Part 7's lab was built so an idea could be drawn without being
adopted, `border-arrival` was drawn, it was looked at, and it won on its merits:

- **It says when something changed.** A ring that pulses forever is loudest exactly when nothing is
  happening. The arrival snap spends its whole motion budget on the transition and then shuts up —
  and CDMProbe measured that **60 % of real cue-set changes are swaps**, so continuous motion is
  mostly decorating a state about to be replaced.
- **It leaves the resting row quiet.** The one flown verdict on continuous rings was *"the tier
  glows read as candles"*, which traced to how much of the row was lit at once. A static border
  makes that free.
- **It carries a second axis for nothing.** Thickness and hue are already two channels on a
  primitive that costs four textures, which is what made a fourth **CHARGES** lane affordable at
  all. A fourth ring would have meant a fourth sheet.

So the border is now V2 on its merits, not on inertia — and the ring's arithmetic is preserved
above rather than deleted, so the reverse move stays cheap if a flight asks for it.

## Why the cue vocabulary went negative — and where the one exception came from

`badge-slots` was promoted at the same time, and the harder decision rode along with it: the cue
set was rewritten so **every cue means "ruled out."** A satisfied dependency draws nothing.

The reading model is *scan left to right, press the first thing not ruled out*. Under that model a
negative cue and a positive cue are not two flavours of the same thing:

- A **negative** cue is *local*. It says "not this one," the scan continues, and the ordering the
  row was authored in still holds. It cannot be wrong about anything except its own button.
- A **positive** cue is an *override*. It says "jump here" — it asks the eye to leave the ordering
  and trust a signal instead. That is a strictly larger claim, and it is the claim that gets
  expensive to be wrong about.

Deferring the positives is therefore a scoping decision about *ordering overrides*, not a retreat
from the finding that a sealed threshold is expressible in either polarity. That finding
(`havoc/catalog.md:113-122`) **corrected** an earlier wrong note claiming the banked-Fury gate was
unrankable, and it stays corrected: the mechanism is V9, it works both ways, and cap authors the
break point without ever reading which side the value fell on. What is parked is *drawing* the
positive half, not the ability to.

⚠ **This is deliberately not the struck wording.** `notes.md:385-389` records that *"a positive cue
is not a second visual language"* was struck from `spec.md` in the 2026-08-10 §3.1 cull, and
nothing here revives it. That was a claim about what a cue **may be**; this is a claim about what
the current style **chooses to draw**, in a document with no authority. The escape hatch is
mechanical rather than editorial: `capart check` fails by name if any scenario stops leading the
eye to its press by elimination alone (shelf Part 5).

**One shared red, three shapes.** Giving each *negative* cue its own hue would have made colour the
discriminator, which puts three near-identical reds on one small icon and asks the player to tell
them apart under a boss's lighting. Instead the hue carries the *polarity* and the shape carries
the *identity*. If the shapes turn out not to be separable at 56 px, the fix is different shapes.

### The exception, added 2026-08-14 — and why it is not the thing that was deferred

The argument above still stands, and `capped` does not contradict it, because **it is not an
ordering override.** Its subject (ST-8) is a row that elimination already leads correctly: every
button to Immolation Aura's left is on cooldown. The badge is not saying "jump here."

What it is saying is a fact the reading model *structurally cannot carry*. Elimination encodes
**rank** — "the highest-priority thing not ruled out." *You are wasting a charge right now* is
urgent independently of rank, and remains urgent when the rank answer is something else. There is
no negative phrasing available: to say it by ruling things out you would have to mark the buttons
to its left as skippable, which would be false. So the choice was between drawing it positively and
not drawing it at all.

Three things were rejected on the way to that:

- **Reordering the row** so ready abilities float left. This is closed twice over — `spec.md` §4
  says sorting by readiness *is* computing the press, and the seal says you cannot rank on secret
  durations in Lua anyway. Two independent reasons agreeing is worth recording, because
  reordering is the intuitive fix and it is the wrong one.
- **A general positive channel.** The other parked positives (`banked`, the promotion, the green
  dependency dot, the weave chevron) are all statements about **rank**, which elimination already
  expresses. Admitting them buys a second way to say something already said; admitting `capped`
  buys the only way to say something otherwise unsayable. That is the whole test, and it is why
  the gate is "at most one" rather than "positives allowed."
- **"About to cap" instead of "capped."** Better warning, not expressible: R6/OBS-066 measured
  `isActive` true at both 1/2 and 0/2, so it means *recharge running*, not *which charge*. A
  threshold on the recharge duration would fire identically when the player is about to cap and
  when they are about to regain their first charge — i.e. loudest while starved, which is worse
  than silence. `capped` fires on the exact readable full state instead.

**Why it gets the only own hue, and the only motion.** Colour carries polarity, so a cue that means
the opposite of its neighbours must not share their red. It also takes slot 3 rather than the top
edge, so polarity is legible from position as well as hue — a badge meaning "act" can never occupy
a place a badge meaning "skip" has used. And it is the one thing that moves in a row at rest,
because impending loss has to survive peripheral vision. The **glyph holds full alpha and only the
halo breathes**: a cue that faded would blink the fact it carries, which is exactly what the text
flicker limits (`tokens.text`) exist to forbid, and the glow rate sits under that ceiling.

## Where the three vocabularies came from

Three descriptions of cap's look existed simultaneously, which is the divergence the shelf exists
to end:

| Source | What it said | Fate |
| --- | --- | --- |
| `ClientLab/Mock.lua` | motion ladder, 2.5/1.2/0.5 Hz, pulse floor 0.68, veil 0.60, the hue set | **adopted 2026-08-13, then superseded the same day** — its veil and its hue *family* survive into V2/V4; its ring and its pulse do not |
| cap's `Treatment.lua` | static 4-strip border, gold/blue/slate at 3/2/1 px | **the shape that won** — V2 is this primitive, re-chosen on its merits with a fourth CHARGES lane and an arrival snap it never had. Still a transcription task, but now the transcription target agrees with it |
| the scenario artifact | two-letter abbreviations on CSS gradients, invented cue shapes | replaced — the artifact is now generated from the shelf |

`Mock.lua` won the first round because it was the only one of the three that was *designed* rather
than defaulted-into, and because its author had already made the accessibility argument and done
the trough arithmetic. Its hues needed one correction to be honest in game: it listed the gold
proc-loop ring first, which the tintability measurement rules out (above).

It lost the second round to a thing that could be **looked at**, which is the whole argument for
Part 7 existing. The lesson is not that `Mock.lua` was wrong — it is that a design nobody had seen
rendered at 56 px beat a design nobody had seen rendered at 56 px, and then lost the moment one of
them was.

`Mock.lua` is retired from `ClientLab.toc` and is not a live document. It is cited here as the
provenance of the numbers, not as an authority over them — the numbers now live in
`render-shelf.md` Part 6.

## What the artifact is allowed to do, and why the guard is mechanical

The artifact's whole value is being a *faithful preview*: real icon art at real size, real sheets
at real frame counts, cap's treatments composited the way the client composites them. A preview
that is merely stylish is worse than none, because it makes the eventual Lua a fresh design
exercise while looking like a transcription target.

The specific lie worth guarding against is `filter: hue-rotate`. It is the obvious CSS way to
recolor a sprite, it looks great, and it can recolor art the client **cannot** recolor — so a
hue-rotated gold ring would show a blue ROTATION lane that is simply not drawable in game. Hence
the shelf's rule that tinting is `mask-image` + `background-color` (or `background-blend-mode:
multiply`), which is what `SetVertexColor` does, and hence `wowkb.capart`'s hard error when a
primitive asks for `tint: "lane"` on art the manifest measured as non-neutral.

**The guard outlived its first subject, which is the test of whether it was a guard or a
ring-specific check.** V1 is retired and there are no atlas sheets in the style any more; the
guard now covers the Kenney badge frames, and `capart check` additionally asserts that *something*
still declares `tint: "lane"` — because a guard whose subject set quietly emptied would keep
passing while guaranteeing nothing. The ⚠ chip on `open` primitives is the same instinct one step
softer (a preview that shows a cue we have not proven the client can draw), and it is kept
unexercised for the same reason.

## Rejected along the way

- **An A/B toggle in the artifact.** Tempting — show both styles, decide by looking. Rejected:
  it turns the shelf back into a debate file, and it removes the pressure to actually choose. The
  loop is *edit the shelf, regenerate, look*; a toggle short-circuits the edit.
- **A continuous grade.** A continuous brightness grade was tried and removed once already (see
  `notes.md`); discrete lanes plus cue intensity is the contract `spec.md` §3.1 carries. *(Note the
  fourth **lane** is no longer in this bullet: CHARGES shipped with V2. A fourth discrete lane and a
  continuous grade were never the same proposal — the grade was rejected for having no rungs, and
  CHARGES is a rung.)*
- **Stacking CHARGES on top of the role lane.** Two borders, or a border plus an inner strip, so
  Immolation Aura could read ROTATION *and* charged. Rejected: an ability has one border, and a
  compound border is a legend the player has to learn. CHARGES **replaces** the role lane at render
  time; the role lane it displaced is still authored in `havoc/catalog.md`, which is where priority
  lives anyway.
- **Cue placement in the bottom corners.** Blizzard draws `ChargeCount.Current` / `Applications`
  bottom-right, at −2/+2. The top corners are free, and the OS-notification convention puts a badge
  there regardless. *(An earlier version of this bullet also claimed Blizzard draws keybind text
  along the bottom of a CDM item. It does not — `grep HotKey` over `Blizzard_CooldownViewer`
  returns zero. The conclusion was right for one of the two reasons it gave.)*
- **Bundling the extracted sheets into the addon's `Media/`.** Referencing an atlas by name ships
  no asset and stays correct across patches. Extraction is for measuring and for the artifact.
