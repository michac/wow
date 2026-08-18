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

### Superseded — the four `SetColorTexture` strips

V2 drew the border as four strips until the ring texture replaced them. The strips' argument was
that they cost **no art at all**: nothing to extract, nothing to put under the tint guard, no atlas
to go stale across a patch, and — the part that actually mattered — a band width that was a
per-lane argument rather than a baked property of a file, so four lanes at three thicknesses were
free. Their construction was also exonerated on paper against the `#` overhang: horizontals took
both x-extents from anchors and verticals both y-extents, so no strip could overhang its own frame
at any scale.

What they cost was four textures and four `SetVertexColor` calls per row per lane, four corner
joins that have to meet, and four animation subjects where the rest of the style has one. The ring
flipbook pays a real price for that — art on the ship path, a band width baked into the texture and
minified with it, and a ticker running at 40 Hz instead of 20 — and the author judged the trade
worth making.

**Per-lane thickness went with them, and that was a choice rather than a casualty.** The strips took
their band width as an argument, so the four lanes could declare three widths for free; a texture
bakes one. Rather than generate one sheet per width, the author collapsed the lanes onto a single
thickness: *"all the different items can have the same thickness."* `spec.md` §3.1 explicitly leaves
*how* the emphasis ladder is drawn — "brightness, hue, motion, thickness, or several at once" — to
the shelf, so this is a shelf decision it already permits, and the ladder now rests on hue and lane
alone. It was already resting there in practice: Part 0.5 made `press`, `press-promoted` and `below`
render identically, so band width was distinguishing lanes from each other, never ranks from ranks.

**And the `Scale` snap went with it**, which is the larger change. The border's arrival is now
painted into the frames of a sprite sheet and stepped in place, so nothing scales, nothing overhangs,
and the border cannot reach a neighbouring row at all. The lab's `arrival-*` entries were built to
diagnose exactly that overhang; they are kept untouched, because a prediction from geometry is not
the measurement they exist to take.

The four-strip construction is not gone from the source: `Paint.Ring` still builds it for Part 7's
arrival variants, which are experiments *about* that construction.

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

⚠ **This is deliberately not the struck wording.** *"A positive cue is not a second visual
language"* was struck from `spec.md` in the 2026-08-10 §3.1 cull (see *Struck visual rules* below)
and nothing here revives it. That was a claim about what a cue **may be**; this is a claim about what
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
- **A continuous grade.** A continuous brightness grade was tried and removed once already, in the
  2026-08-11 tier-preserving correction; discrete lanes plus cue intensity is the contract
  `spec.md` §3.1 carries. *(Note the
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

- **Desaturating the icon face.** `verdicts.starved.desaturate` was declared and then deleted on
  2026-08-14 because it had no live path: in the `/cap style` gallery cap owns the texture, so
  desaturating is free, but on a live row the icon is Blizzard's. The right reading is not "find cap
  a legal way to desaturate" — **the Cooldown Manager already desaturates and re-tints on
  usability** (`knowledge/addon-dev/cooldown-manager.md` :700, :755), so the token was cap proposing
  to restate a signal the client draws for nothing. It existed only because the HTML artifact has no
  Blizzard underneath it and had to draw its own de-emphasis, which then got filed as a cap
  treatment. **cap's drawn primitives are the lane border and the corner badges; the icon face is
  not one of them.** Revisit only if a flight shows the client's own dimming is too weak to read —
  and then as a new shelf entry, not as this one restored.

## Struck visual rules — the record of their removal

These were normative in `spec.md` §3.1 and were struck in the **2026-08-10 cull**, whose test was
*which principle is this downstream of?* **None of it is current, and none of it may be carried
forward.** It is written down only so that a later reader who finds the phrasing in an old commit,
a comment or a screenshot knows it was removed on purpose rather than lost.

- The emphasis ladder being **monotone** in brightness and in pulse rate.
- Each tier owning a **disjoint** brightness band.
- A marker having a **fixed place**, with two of them per row.
- ***"A positive cue is not a second visual language."***
- The shared-row pick taking the **brighter of the two**.
- The greyscale / colour-blind defence as a normative requirement.

What replaced them named its root each time: the ladder is *ordered* rather than monotone (three
emphasis levels are levels or they are three colours); a grade moves an entry only inside its own
tier's range; and cap's emphasis must be **distinguishable** from the stock proc glow, which is
strictly weaker than forbidding Blizzard's art — which is why the ring's atlas was left alone.

⚠ Two of these carry a second lesson worth keeping.

- **A cull can *add* a rule, and anything a cull introduces deserves the same test it applies to
  what it removes.** *"Polarity is carried by shape — press and hold may never differ only in hue"*
  entered during a **rule cull** whose entire purpose was cutting rules back to `spec.md` §1's three
  principles. It was then implemented, written into §3.1's treatment table and restated in two
  module headers, so within a week an unargued visual preference had three independent-looking
  sources and read as settled.
- **Striking the band rule broke one thing, and it took four lines to fix.** "Brighter" and "higher
  tier" were the same sentence only because of the struck disjoint-band rule; with it gone, a graded
  low tier could out-brighten a dim middle one and the shared-row pick could draw the *lower* tier.
  `Treatment.Rank` was added to compare tier order first and emphasis only inside one tier.

## Two things a preview must be, and the rules that follow from them

**A preview must be lookable-at, so nothing may block a rebuild you want to look at.** A gate on a
preview inverts what a preview is for: you reach for it precisely when something is wrong and you
want to see what wrong looks like. That is why `capart build` carries only two hard failures — the
tint guard and the closed verdict/roster vocabulary — and why the CI-shaped assertions live in a
separate verb (`capart check`). The tint guard survives the rule because it does not block looking
at a *mistake*, it blocks looking at a *lie*.

**A preview must render the unflattering case, or it is a worse instrument than no preview.** The
lab's badge entry computes its own overhang against the row gap and draws three adjacent icons, so
"these collide" is something the artifact *shows* rather than something a caption claims. A lab that
only renders the flattering case would have been a decoration.

## Retiring a primitive: the rule that produced it is what has to go

Recorded from the veil retirement of 2026-08-16, because the same shape will recur.

The veil was **derived** — a row was veiled *iff* it wore a negative cue — so it could only ever
restate what the badge already said, while stacking on Blizzard's own swipe and desaturation until a
dark row was the sum of causes you could not separate. That argument was **checkable rather than
rhetorical**, and the check is the reason to trust the deletion: the elimination gate resolved all
13 scenarios to the same presses with the veil term gone, and stripping a negative cue from an
eliminated entry still failed it. *A redundant signal is one whose removal changes no outcome and
whose remaining signals still discriminate* — both halves were measured, not asserted.

⚠ **The general lesson is about where an invariant hides.** Three of the sites that mattered were
not in the plan: the derivation lived in `Treatment.lua` rather than in the renderer, the reading
model was restated in the scenario doc as well as the shelf, and a cue's second sink was declared in
the catalog. **A primitive is retired only when the rule that produced it is gone, and rules
travel.**
