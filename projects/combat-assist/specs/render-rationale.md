# Combat Assist Plus — why the render shelf says what it says

**What this file is for:** the reasoning, the alternatives, and the things tried and rejected
behind `render-shelf.md`. It has **no authority over anything**. The shelf declares; this
explains. If the two disagree, the shelf is right and this file is stale.

It exists because the shelf must declare exactly one style — an artifact generated from a document
holding two answers renders neither — and because deleting the reasoning along with the rejected
option is how a decision gets re-litigated six weeks later by someone who cannot see what was
already weighed.

---

## Why motion is the primary channel

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

## The trough invariant — where `tokens.pulse.floor` comes from

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

## The phase offset is a safety requirement, not a design flourish

`tokens.pulse.phase_offset_s` staggers each icon's pulse by its index. Fourteen icons flashing in
synchrony is a single large flashing area and lands squarely in WCAG 2.3.1 territory; fourteen
flashing independently do not sum into one perceived flash. The text-cue caps
(`tokens.pulse.text_max_hz` / `.text_duty` / `.text_alpha_floor`) are MIL-STD-1472F's numbers for
blinking legends, applied for the same reason.

Neither is negotiable in the way a hue is. They can be *implemented* differently; they cannot be
dropped.

## Why the neutral ants sheet, and not the prettier ones

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

## The static border, and why it stopped being the baseline

cap's shipped `Treatment.lua` draws four white `SetColorTexture` strips forming a rectangular ring,
1–3 px by lane, with a 2 px bleed. No art, no animation, no atlas — the cheapest possible
treatment.

It was not chosen on its merits. It was the only thing permitted by a rule the spec used to carry:
*treatments are static; motion is introduced only for a specific observed problem.* That rule was
an experiment written in as if it were a boundary, and it was struck on 2026-08-13 along with the
rest of the UI opinions that had leaked into `spec.md`. With the rule gone, the static border has
no argument for it beyond "it is what is compiled today," which is a `backlog.md` fact, not a
design one.

It remains an honest fallback if the flight says the rings are too much. That would be a shelf
edit, made by looking at something — not a rule.

## Where the three vocabularies came from

Three descriptions of cap's look existed simultaneously, which is the divergence the shelf exists
to end:

| Source | What it said | Fate |
| --- | --- | --- |
| `ClientLab/Mock.lua` | motion ladder, 2.5/1.2/0.5 Hz, pulse floor 0.68, veil 0.60, the hue set | **adopted** — the most considered design we had; its hues and rates are the shelf's |
| cap's `Treatment.lua` | static 4-strip border, gold/blue/slate at 3/2/1 px | superseded (above); a transcription task, not a design one |
| the scenario artifact | two-letter abbreviations on CSS gradients, invented cue shapes | replaced — the artifact is now generated from the shelf |

`Mock.lua` won because it is the only one of the three that was *designed* rather than
defaulted-into, and because its author had already made the accessibility argument and done the
trough arithmetic. Its hues needed one correction to be honest in game: it listed the gold
proc-loop ring first, which the tintability measurement rules out (above).

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
the shelf's rule that tinting is `background-color` + `background-blend-mode: multiply`, which is
what `SetVertexColor` does, and hence `wowkb.capart`'s hard error when a primitive asks for
`tint: "lane"` on art the manifest measured as non-neutral.

The same reasoning covers the grid check (a `rows × cols ≠ frames` sheet animates wrong in a way
that is easy to miss and easy to copy into Lua) and the ⚠ chip on `open` cues (a preview that
shows a cue we have not proven the client can draw is the same class of lie, one step softer).

## Rejected along the way

- **An A/B toggle in the artifact.** Tempting — show both styles, decide by looking. Rejected:
  it turns the shelf back into a debate file, and it removes the pressure to actually choose. The
  loop is *edit the shelf, regenerate, look*; a toggle short-circuits the edit.
- **A fourth lane / continuous grade.** A continuous brightness grade was tried and removed once
  already (see `notes.md`); three discrete lanes plus cue intensity is the contract `spec.md` §3.1
  now carries.
- **Cue placement in the bottom corners.** Blizzard already draws charges bottom-right and keybind
  text along the bottom. The top corners are free; using them is not a preference.
- **Bundling the extracted sheets into the addon's `Media/`.** Referencing an atlas by name ships
  no asset and stays correct across patches. Extraction is for measuring and for the artifact.
