# Cue treatments — making a cue draw the eye when a glow cannot

## Why this exists

The glow palette answers "which glow reads as HIGH on an icon". It does not answer the
harder half of cap's problem: **a subset of cues are text**, and text cannot wear a
flipbook. This is the lab for everything else that might draw the eye — motion, opacity,
scale, doubling, onset — measured the only way any of it can be: by looking at it.

Same footing as the glow palette. A **picker, not a test**: no `ns.Test{}` id, no
`questions.json` row, no new capture stream. Nothing in a product addon may depend on
ClientLab; the output is a decision that later gets built into cap directly.

## The constraint, precisely

"Secret font strings" is the shorthand, but the real constraints are three, and they are
already measured in `knowledge/addon-dev/security-taint-and-restricted-data.md` §4.8.1
`[client 2026-08-04]`. Read them before designing anything, because two of the three
obvious treatments are shaped by them:

1. **`FontString:SetText(secret)` poisons the anchor chain.** Finding 10: it records both
   the `{Text}` aspect *and* `anchor 0>1` on the FontString **and its dependent**. A
   FontString's extent is derived from its text, so a secret string implies a secret size.
   **The rule: a FontString you feed a secret must be a layout leaf.** Anchor it *to*
   things; never anchor anything *to* it.
2. **`DurationTextBinding` does not do this.** Same finding: it writes the text C-side and
   the anchor stays clean (`0>0`). It is *the* anchor-safe route to secret text, and
   `SetText` is not.
3. **A secret-fed FontString stops being measurable.** `RequiresFontStringTextAccess`
   (`SecretPredicatesDocumentation.lua:21-24`) makes
   `CalculateScreenAreaFromCharacterSpan` and `FindCharacterIndexAtCoordinate` reject
   tainted callers. So you cannot ask how wide the text is — a second, independent reason
   it must be a leaf.

**What this does NOT forbid.** Animating a widget with *plain numbers* is not a secret
operation at all. `SetAlpha(0.4)`, `SetScale(1.2)`, a `Translation` animation — none of
these read the secret; they move the widget the secret happens to live in. The prohibition
is on **branching on** a secret and on **anchoring to** a poisoned region. So every
treatment below is legal; what varies is whether it survives the leaf rule.

Three consequences that shape the design:

- **Anchor every text cue by `CENTER`, never by `LEFT`/`RIGHT`.** A scale or size animation
  on a centre-anchored string grows symmetrically without anyone needing to know its width
  — which is exactly what rule 3 says you cannot find out.
- **The two-copy treatment needs two leaves, not a parent and a child.** Both FontStrings
  get the secret, and **both anchor to a common non-secret frame** at different offsets.
  Anchoring copy B to copy A is the one thing rule 1 forbids.
- **A plain-text mock-up proves nothing.** Anchor contagion only happens with a *genuine*
  secret, so a treatment that looks fine on `"12.4"` may break on the real thing.

## The honest-test rule

**Every treatment renders twice, side by side: once on a plain string, once on a genuine
secret string.** That comparison *is* the experiment — anything that differs between the
two columns is the constraint biting, and is the finding.

The secret is real, and the recipe is already known (§4.8.1 finding 2, Demonology, Summon
Demonic Tyrant 265187):

```lua
local dur = C_Spell.GetSpellCooldownDuration(spellID, true)   -- ignoreGCD = true
local fmt = C_StringUtil.CreateSecondsFormatter()             -- StringUtilDocumentation.lua:29-37
local s   = dur:FormatRemainingDuration(fmt, Enum.DurationTimeModifier.RealTime)
fontString:SetText(s)                                          -- renders. In combat. Ticking.
```

⚠ **It is only secret IN COMBAT** (`HasSecretValues()` is true in combat, false out of
it), so the secret column is honest only during a pull. Out of combat it must say
*"not secret yet — pull something"* rather than draw a plain string in the secret column
and let it pass. ClientLab's `Secret.lua` already owns this gate; reuse it.

⚠ Reuse also **re-establishes a lost measurement**. The KB records finding 2's capture as
**GONE** — "re-establishing it means re-flying the recipe". A panel that runs this recipe
every pull is that re-flight, so wire it to be readable as such.

Also compare the `SetText` route against the **`DurationTextBinding`** route in the same
panel, and report `IsAnchoringSecret()` on the string and on a probe region anchored
beside it. That single readout settles, per treatment, whether the leaf rule is being
obeyed — and it is the difference between "this looks fine" and "this is safe to build
into cap".

## What the salience evidence changed

The treatment list below was reordered by a graded evidence review. Four findings did the
reordering, and they are the reason the panel has controls the original sketch did not:

1. **Exogenous attention answers *change*, not state.** Habituation to a repeated visual
   warning is measured within a single session and across a working week; warnings that
   *change form* resisted it. A steady loop is therefore the weaker default, and the panel
   carries an **onset mode** — full intensity for a 250–400 ms transient, then an
   exponential decay to a quiet state that carries the tier and alerts no further. Steady
   stays, because the comparison between the two is the finding.
2. **An opaque plate beat five other text styles** over six real textured backgrounds
   (Gabbard, Swan & Hix 2006), and text is unreadable outside central vision because of
   crowding. So a text cue is two jobs — *findability* (a non-text carrier summons the eye)
   and *legibility* (the string reads on arrival) — and the plate is the legibility floor
   under every row, not treatment #7. The principle: **animate the plate, never the
   glyphs**; glyph motion wrecks identification.
3. **Flicker has a ceiling and it is low for text.** MIL-STD-1472F allows 3–5 Hz for a
   warning light but caps flashing text at **2 Hz at ~70 % on-time**; human flicker
   sensitivity peaks at 8–15 Hz, which is also the band 96 % of photosensitive individuals
   respond in. The panel keeps an **opacity floor of 0.65** by default so glyphs stay
   legible through the cycle. Over-limit settings stay reachable and the row **says so** —
   silently withholding them would hide the cost being measured.
4. **Self-judgement is sabotaged twice.** *Dishabituation* makes anything new feel better
   in its first session; *contingent capture* gives the incumbent a home-field advantage.
   The answer is **within-session A/B**, so the panel can mark two treatments A and B, swap
   between them instantly mid-pull, and withholds the name while toggling.

## What to build — text treatments

A `[cue treatments]` button on the `/clab` dump panel (rule 4: a button, never a slash
subcommand). Movable panel, refuses to build in combat, same discipline as the others.

A column of rows. Each row is one treatment, drawn on a plain string and on a genuine
secret one, with the treatment's parameters exposed as steppers so a number can be tuned by
eye rather than guessed:

| # | Treatment | Parameters to expose |
|---|---|---|
| 1 | **plate pulse** — animate the backdrop, leave the text still | plate colour, period, floor, ramp |
| 2 | **static baseline** — tinted only | tier colour (global) |
| 3 | **alpha pulse** — fade in/out | period (to 3 s), floor/ceiling alpha, ramp |
| 4 | **colour pulse** — `VertexColor` between two tier hues | from, to, period, ramp |
| 5 | **scale pulse** — breathe | period, amplitude, **expand vs contract**, `scaleAnimationMode`, `smoothScaling` |
| 6 | **onset flash** — abrupt appearance, then settle | flash alpha, settle, decay, repeat interval |
| 7 | **font / outline** | face, height, outline flags, shadow offset + colour |
| 8 | **weight cross-fade** — two leaves at different outline weights | thin flags, thick flags, period, ramp |
| 9 | **offset double** — same string twice, two colours, small offset | offset x/y, the two colours |
| 10 | **jitter / translate** | amplitude, period |

**Treatment 1 is first on the evidence, not on taste** — see finding 2 above. A backing
plate is also a Texture, not a FontString, so it can wear a flipbook and is bound by none
of the three rules. Every *other* row gets a plate underneath as well, on by default.

**Treatment 4 exists because the type does.** `VertexColor` is one of the ten animation
types (`SetStartColor` / `SetEndColor`, both taking a **ColorMixin object**, not four
numbers), and it reaches text for a measured reason: `SetTextColor` and `SetVertexColor`
are one storage slot on a FontString `[client 2026-08-05]`. ⚠ §4.8.1's table lists the two
`AnimVertexColor` setters as "accepted, nothing observable changed" — but that was with a
*secret* colour and is explicitly the untried half of that question. This row passes plain
colours, so it should draw; if it does not, the row says so rather than looking idle.
⚠ Vertex colour is **not restored** when an animation ends, so the row's groups are
stopped before any base colour is written.

**Treatment 9 is in the panel to be falsified, not as a candidate.** It has **no**
supporting literature — not weak evidence, none — and every mechanism predicts a legibility
cost: reduced edge contrast and high-frequency noise exactly where letter identification
happens. It was asked for specifically and it stays; the note on its row says this.

Treatment 9 is also the one whose *implementation* is constrained — two leaves on a common
parent, per above. Get that right or it will look like it works and poison a layout later.

**Drive everything from plain numbers.** A tier decides which treatment and which
parameters; the secret is only ever the string's *content*. Do not "improve" this by
driving a parameter from a cooldown value.

### Motion is C-side, and that is a handoff decision as much as a performance one

The first cut drove every treatment from a 33 Hz Lua ticker. The rebuild puts all of it on
the client's own animation system (`knowledge/addon-dev/frames-textures-animation.md` §7),
and **FontString is an `AnimatableObject`**, so text is in scope.

Each treatment now returns a list of **animation descriptors** — `kind`, `from`, `to`,
`duration`, `smoothing`, `endDelay` — plus a `looping` mode. What that replaces:

| Was | Is |
|---|---|
| a 33 Hz ticker recomputing every widget | `AnimationGroup:Play()`, nothing per frame |
| hand-computed easing | `SetSmoothing` — `NONE / IN / OUT / IN_OUT / OUT_IN` |
| a hand-rolled sine pulse | one `Alpha` animation under `SetLooping("BOUNCE")` |
| ticker arithmetic for onset/decay | a hold and a decay at two `order`s, `SetToFinalAlpha(true)` so the settle survives |
| a timer for auto-fire | `endDelay` on the last animation under `REPEAT` |

**The descriptor list is the point.** It is data — type, endpoints, duration, smoothing,
order, looping — which is exactly what pastes into cap. A ticker's internal arithmetic is
not.

Two things the animation system genuinely cannot express, and what happens instead:

- **The 70 % duty cycle.** `BOUNCE` is symmetric by construction and `smoothing` cannot
  make one end dwell longer than the other. So `ramp = duty` builds **three** animations —
  hold at the ceiling, ramp down, ramp up — under `REPEAT`. The Lua wave is gone.
- **Stepped motion.** The system interpolates smoothly, so a step is a short *hold*, and a
  descriptor at 8 or 17 Hz expands into that many hold animations. Above a cap of 20 steps
  the row runs smooth and **says so** in its readout. `Translation` is excluded from the
  expansion: its offset is a delta, not a position, so a hold has nothing to hold.

⚠ **Two traps the KB calls out and this code obeys.** The direction word moves between
types — `Alpha` is `SetFromAlpha`/`SetToAlpha`, `Scale` is `SetScaleFrom`/`SetScaleTo` —
and `SetFromScale`/`SetToScale` **do not exist** at 12.0.7.68887 even though older addon
code uses them. Every setter goes through a probe that reports an absent method rather than
falling through, because a `Scale` animation that never received its endpoints looks
exactly like one that is playing and not helping.

⚠ **Animating a secret-fed FontString is untested.** `CreateAnimationGroup` and
`CreateAnimation` are `SecretArguments = NotAllowed`, which constrains their *arguments*,
not their target — so it *should* be legal. The middle column is exactly that case, the
`a` readout is where a refusal would appear, and the code carries the `--@unverified`.

⚠ **Whether `FontString` is an `AnimatableObject` rests on Tier 2 alone** (the wiki
transcluding it; the generated docs do not encode inheritance). With `glyphs` as the
default target, every animating row now exercises it on the first flight. A refusal shows
as `!` in the `a` group with the reason spelled out beside it — a measurement, not a dead
row.

### The binding column has to be able to say why it is blank

A `DurationTextBinding` that was created but never given a duration, or never enabled,
draws nothing — which is pixel-identical to a working binding whose duration is zero, and
to a route that does not exist. Three rules follow, all of them now in the code:

1. **Nothing on the install path is swallowed.** `SetFontString`, `SetFormatter`,
   `SetDuration` and `Enable` each report their own failure; `Enable` falls back to
   `SetEnabled(true)` and reports both if both miss.
2. **The binding's own diagnostics are on the row.** `CanFormatText()` and
   `CanUpdateFontString()` (both plain bools, purpose-built for exactly this question)
   plus `IsEnabled()` render as the `b` group.
3. **⚠ AN UNINSTALLED BINDING MAY NOT BORROW THE OTHER ROUTE'S READING.** The column's
   FontString exists whether or not a binding was attached to it, so reporting its
   aspects would attribute to the binding route a result the binding never produced —
   which is how *"the binding poisons the anchor too"* would reach the KB as an artefact
   contradicting §4.8.1 finding 10. With no binding installed the whole column reads `x`.

Expired text is `--` and zero-duration text is `0`, so **expired**, **zero** and **broken**
are three different sets of pixels.

### The binding isolation — what it is set up to answer

A binding-fed FontString has been observed reading **both** `IsAnchoringSecret` and the
`Text` aspect, which would contradict §4.8.1 finding 10's `0>0` and remove the only
anchor-safe route to secret text. It is not yet a finding, because that string's lifetime
could not be shown to be free of a `SetText` call.

So the panel now **seals every leaf**: `SetText`, `SetFormattedText` and `SetTextToFit`
are shadowed per instance with a counting wrapper, so a Lua write from *any* caller — ours
or foreign — is recorded on the string itself. A C-side write does not pass through Lua and
is therefore not counted, which is exactly the discrimination needed.

The readout's `b` group ends in that flag: `W` if any Lua text write has ever touched the
binding column's string, `-` if none, `?` if the seal did not take. The header carries the
**positive control** — the `SetText` column's string must read written, or the seal is not
catching writes and a `-` on the binding column proves nothing.

The question it answers, stated so the next flight can read it off in one glance:

| Reading | Means |
|---|---|
| `b …-` and `s` shows `++` on the binding column | **finding 10 is wrong** — the binding does mark anchoring secret, on a string Lua never wrote |
| `b …-` and `s` shows `--` | finding 10 stands, and the earlier `++` was contamination |
| `b …W` | not isolated — something wrote it, and nothing may be concluded from this row |
| `b …?` | the seal failed; the isolation is not running and the column's `-` is meaningless |
| header `seal control silent` | the control never fired — distrust every `-` on the panel |

**Build the isolation, do not draw the conclusion.** The KB entry for this is written as a
`[gap]` under §4.8.1 with the recipe, not as a claim.

### Ordering the source spell by base cooldown

A tracked Fury spender formats to zero and makes both secret columns read `0 Seconds`,
which looks like a broken panel. You cannot branch on the secret in combat to find one
that is *currently* running — but a cooldown's **length** is not secret out of combat
(§4.8.1 finding 1: `HasSecretValues()` is false there), so the candidates are sampled and
sorted **longest base cooldown first** while out of combat, and that order is kept into
the pull. `GetSpellBaseCooldown` is probed by string first (it is **not** in the generated
docs at 12.0.7.68887, so its presence is itself a measurement); `LuaDurationObject:GetTotalDuration`
is the fallback. If neither yields a non-zero anywhere the panel keeps the tracked order
and **says which happened** in the header.

⚠ **Ordering was necessary and not sufficient.** `GetSpellCooldownDuration` returns
*remaining*, not base, so a correctly-picked 300 s ability that the player has not cast is
still zero. The fix is the second argument: finding 2's recipe passes `ignoreGCD = true`,
which is precisely why a ready spell reads nothing. **`ignoreGCD = false` reports the
global cooldown instead**, and the GCD rolls on every cast for the whole pull — so it is
the `source` control's default and something always ticks. The header names which is live.

### Drawing on a simulated Cooldown Manager icon

The flat cell is not what any of this will sit on. `backdrop` replaced the old
`plate on/off` with three dresses on **one animatable region**: the real spell icon
(`C_Spell.GetSpellTexture` of the spell the secret columns are already feeding from, so
the header and the art cannot disagree), an opaque billboard, or nothing. `target = plate`
therefore animates whichever backdrop is current, which is what cap would actually do.

The icon is drawn at a **real Cooldown Manager item frame's size**, read out of combat off
the first readable frame across the four viewers; if none is readable it falls back to
40 px and the capability line says which happened. Because the cell height changes with
the backdrop, the rows live in a **ScrollFrame** — the panel keeps one height whatever the
row height and treatment count do.

### Font weight — asked, answered, and approximated

**WoW has no continuous font-weight axis.** `SetFont`'s flags are discrete (`OUTLINE`,
`THICKOUTLINE`, `MONOCHROME`) and outline thickness is not an animatable property, so
"weight along a curve" cannot be done directly. The closest approximation is a
**cross-fade between two FontStrings at different outline flags with opposed `Alpha`
animations**, and since the offset-double row already provides two leaves on a common
holder, that was cheap enough to build: it is the `weight cross-fade` row. It is an
approximation and the row's note says so.

### The global controls, and why each exists

| Control | Why |
|---|---|
| `mode` steady / onset | finding 1. Onset is what the evidence favours |
| `transient` · `decay` | the onset's shape, tunable by eye |
| `auto` off / 3 s / 6 s / 12 s, plus `[fire]` | repeat the onset without hand-clicking — and it is also how habituation becomes noticeable |
| `plate` on / off | finding 2. The legibility floor, on by default |
| `target` **glyphs** / plate | finding 2's principle, made falsifiable: the same modulation on the letters or on the carrier. ⚠ **glyphs is the default and that is deliberate** — "animate the plate, never the glyphs" is the thing being tested, and defaulting to the plate meant a person could press every treatment and never see text move once. Each row's readout says which target it is on, so "nothing is happening to the text" is never a silent state |
| `motion` smooth / 17 Hz / 8 Hz | whether motion-onset capture needs *jerky* motion is contested; a descriptor expands into that many hold animations to test it |
| `ramp` (per row) `duty` / the five `smoothing` modes | the ramp shape, taken from the animation system rather than hand-computed |
| `greyscale` | ~8 % of men are colour-deficient and a dichromat keeps luminance; peripheral vision degrades colour the same way. If the tiers cannot be ranked at zero saturation they cannot be ranked |
| A/B `set A` · `set B` · `swap` · `show all` | finding 4. The live row moves to a fixed position and its **name is withheld** |

The rate ceiling lives in code as `TEXT_MAX_HZ` / `TEXT_DUTY` / `TEXT_ALPHA_FLOOR` with the
reason attached, and a row outside it grows an amber tail in the readout.

### Text specifics wired as controls

- **`scaleAnimationMode`** (`FontSize` | `Vertex`, default `FontSize`) and
  **`smoothScaling`** (default false) are steppers on the scale-pulse row. This is the
  documented switch between re-rasterising glyphs at each animation step (crisp, costly)
  and scaling the vertices (cheap, soft), and it is the most likely single reason animated
  text has looked unconvincing.
- **`SetTextColor` and `SetVertexColor` are one storage slot on a FontString**
  `[client 2026-08-05]`. This file uses `SetTextColor` everywhere and never the region
  call, so nothing can clobber a text colour by writing the other name.
- **`SetFont` returns a success bool** and carries `RequiresValidFontAsset` +
  `RequiresValidFontHeight`. The font row checks it and the readout reports a refusal —
  it is the only failure signal that call has.
- **`GetFonts()` is reported on the capability line but not wired to the stepper.** It
  returns font *names* and `SetFont` takes a font *asset path*; whether those are the same
  namespace is unverified, so the `face` stepper offers four known shipped paths and the
  capability line records what `GetFonts` actually handed back.

⚠ **The ceiling is scoped to luminance modulation.** The jitter row modulates *position*,
not luminance, so the flash threshold does not bind it and its fast steps are deliberately
unflagged — its 10 Hz option sits in the 8–17 Hz band the contested jerky-motion result is
about, which is the point of offering it.

## What to build — icon treatments

The glow palette shows *which* glow. It does not vary *how it plays*. Add to the existing
palette panel:

- **speed** — the flipbook's `secs` per loop, stepped well either side of Blizzard's
  declared duration. Blizzard's own numbers are the anchor (proc-loop 1.0 s, GCD 0.75 s,
  transmog 2.33 s); the question is whether faster reads as more urgent or just as noise.
- **pulse envelope** — an alpha oscillation layered *on top of* the loop, so the glow
  breathes rather than running flat. Period and depth as parameters.
- **scale envelope** — the same idea on size, with an **expand / contract** toggle.
  Franconeri & Simons (2003) found expanding stimuli capture attention and contracting ones
  do not; Abrams & Christ (2005) published a rebuttal. At equal amplitude this is one
  toggle and a positive result is genuinely new information.
- **blend mode** — `ADD` against `BLEND`. ADD blows out over a bright icon and vanishes
  over a dark one; this is likely to matter more than it sounds.
- **motion quantisation** — smooth / 17 Hz / 8 Hz, the icon-side half of the contested
  jerky-motion result.
- **dim the un-emphasised** — salience is *relative* feature contrast, so contrast can be
  raised from the other side. One icon keeps the glow, every other painted icon takes a
  veil. No motion, no flash, no seizure exposure, and it is the only treatment here that
  structurally cannot produce "everything glows". ⚠ It dims by **occlusion**: the icon
  underneath is a Blizzard frame this panel never touches, so this is *not* a test of
  desaturating the art itself.
- **greyscale** — same one-glance check as the text panel.

### ⚠ The phase offset is a safety property

WCAG 2.3.1's general flash threshold is a ≥25 % relative-luminance swing over more than
25 % of a 10° field — about **21,824 px²** at the reference resolution. A 40×40 icon is
1,600 px², so **fourteen icons flashing individually are trivially compliant and the same
fourteen flashing in sync are not.** Every painted proxy therefore carries a small
per-index phase offset, and that is not a style choice to be tidied away.

MIL-STD-1472 tells you to *synchronise* warning flashes. The two standards genuinely
conflict here and this sides with the seizure floor. The code says so at the constant.

⚠ **One correction to the brief.** `ENVELOPES`' fastest period, 0.4 s, is 2.5 Hz — that is
over the **text** limit but inside the **3 Hz icon** allowance, and `ENVELOPES` drives
icons. It is kept. The text-side offenders were the cue panel's own lists (a 0.4 s alpha
period, and the jitter periods), which is where the flagging went.

## Constraints

- **wow-developer house rules 1–7.** Rule 1 comment budgets, rule 4 buttons-not-commands.
- **Probe maybe-missing globals by string** (`ns.G` / `ns.GlobalType`). `C_StringUtil`,
  `C_Spell.GetSpellCooldownDuration` and `Enum.DurationTimeModifier` all go that way.
- **Never record a value you did not measure.** If the secret gate is unmet, the secret
  column says so; it never falls back to a plain string and it never reports a verdict.
- `luacheck ClientLab/` clean, zero inline suppressions; `wowkb.lab deploy --check` still
  7 ids / 7 built questions.

## What this feeds

A decision for cap's spec — which treatment carries HIGH for a text cue — and, separately,
whatever the secret-column comparison teaches about §4.8.1. **A client fact learned here
goes to `knowledge/addon-dev/`** as a claim tagged `[client YYYY-MM-DD]` (a value seen) or
`[searched YYYY-MM-DD: …]` (looked for, absent) — not into this file, which is a project
doc and states only what the lab is for.
