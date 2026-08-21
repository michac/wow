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
2. **The cue vocabulary is negative by default.** A cue
   normally draws when a button is ruled *out* and draws nothing when it is clear. A satisfied
   dependency is silence. A red badge is the whole statement — it says *that* something is skipped
   and *why*, in one mark, and nothing else on the row says either.
   Every cue declares its `polarity`, and a cue that declares none is read as negative.

### When elimination is the wrong tool — the density rule

**Pass 2 costs the reader one badge per skip, and that cost is not free.** Stepping over one or two
red badges to reach the press is a glance. Stepping over three or more is *counting*, and counting
is the thing the whole model exists to avoid — a row where most buttons are lit reads as "something
is wrong" long before it reads as "press the clean one."

```
1–2 HOLDS before the press — elimination. Draw the skips.
3+  HOLDS before the press — elimination is the wrong tool here.
                             Promote the press with `priority` instead.
```

**What counts is `budgeted`, and only `blocked` carries it.** A hold is cap making a claim the
player cannot check at a glance: *this button is castable, you can afford it, and you should skip
it anyway.* That is the mark which costs interpretation, and three of them in a row is the thing
that reads as noise. `starved` and `overcap` are not that — they restate a resource the player is
already reading off their own bar, on buttons that were never pressable in that state, and they
cluster on adjacent spender rows as one visual group. Counting them would push rows over budget
for being honest about Holy Power.

**This is a rule about the row, not about any one button**, which is what makes it different from
every other rule in this part. A hold is authored per ability and is true or false on its own
terms; the density rule can only be evaluated once you know what the *rest* of the row is doing in
that state. So it is enforced per **scenario** in `check` rather than per marker, and a catalog
satisfies it by choosing which of the two shapes to author, not by tuning a threshold.

⚠ **Swipes do not count.** Blizzard's dial already ran those buttons down and cap did not draw
them; the reader is not paying for them. Only cap's own negative badges count against the budget.

⚠ **`priority` removes the need for the holds that existed only to REACH the press.** It does not
silence holds that are true on their own terms — markers are authored per ability and cannot know
which scenario they are in, so a genuine hold still draws. What it retires is the *scaffolding*:
a hold whose only job was to stop elimination landing on the wrong row. Retribution's opener is the
worked example — promoting Blade of Justice let two markers be **deleted outright**
(`woa_awaits_wrath_ready`, `dt_awaits_wrath_ready`), because they existed solely so a left-to-right
scan would step over Wake of Ashes and Divine Toll to reach it.

⚠ **A promoted row is judged by pass 1, so the density gate does not run on it at all.** That is
not an exemption to be reached for — it is the rule working: once the press is pointed at, the
reader is no longer stepping over anything.

**And the reason a positive cue exists at all.** Elimination encodes **rank** — it answers "what is
the highest-priority thing not ruled out." Some facts are not about rank at all. *You are wasting a
charge right now* is urgent no matter what sits to its left, and it stays urgent when the answer to
"what is highest priority" is something else entirely. There is no negative phrasing of it: to say
it by ruling things out you would have to mark the buttons to its left as skippable, which would be
false.

So the vocabulary carries **two** positive cues, and they are positive for two different reasons:
`capped` because its fact is not about rank, and `priority` because the rank is real but expressing
it negatively costs more than the reader will pay. Both are scoped: `capped` to **impending loss**,
`priority` to the density rule above. Neither is a general-purpose "this is good" mark.

⚠ **There is no positive-cue budget, and there never was a reason for one.** Until 2026-08-19 the
shelf allowed exactly one positive cue and `check` enforced it. That was never a design finding —
it was the three-slot badge geometry (V5) read backwards, plus the fact that Havoc happened never
to need a second. What pass 1 actually requires is that *"scan for a positive cue"* have one
answer, and that is a constraint on a single **row**, not on the vocabulary: `check` now asserts
that no entry wears more than one positive cue, which is the real invariant.

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

**Five gates in `wowkb.capart check` hold this line: one per pass, two on the vocabulary, and one
keeping chrome out of both.**

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
- **Chrome takes part in neither pass, and `check` holds it there.** `tokens.hotkey` fails if it
  names a cue, if it declares a `polarity` or a `rank`, or if it anchors to the corner the badge
  stack flows from. This is the mechanical form of the chrome ruling: a label that can be mistaken
  for a signal is the one way V15 breaks the reading model, and geometry is where that mistake
  would start. ⚠ Nothing else needs exempting — every cue gate iterates `tokens.cues` and nothing
  enumerates top-level token keys, so a sibling of `cues` is invisible to all of them.

One further `check` assertion keeps this part's own claims mechanical rather than promised: every
positive cue ranks above every negative one, so a promotion always sits on the corner where the eye
lands first (Part 1).

---

## Part 1 — Surfaces (what there is to draw on)

A Cooldown Manager row is a small square icon. These are the places a cue can live. Placement is
a design choice, not a platform constraint, unless marked otherwise.

| Surface | Where | Carries | Notes |
| --- | --- | --- | --- |
| **Icon face** | the art itself | nothing — cap draws no treatment here | **Desaturation is Blizzard's and cap does not draw it.** The CDM already desaturates and re-tints the icon on its own refresh — `SPELL_UPDATE_USABLE` drives icon colour continuously (`cooldown-manager.md:700, :755`), which is the client's built-in "you cannot cast this" channel. cap adding a second one would restate a signal the player already has. |
| **Scan edge** | a thin additive line on the icon edge | one bit: the row is in the scan, or it is not | Static — nothing about it moves (V13). Drawn on cap's own frame, sized to the icon rect, so it needs no host scale-up and cannot reach a neighbour. |
| **Corner badge stack** | discs hung off the **top-right** corner, flowing **down** the right edge | one cue each, as many as the row wears | Filled circles at `tokens.badges.diameter_pct` of icon width, overhanging by `tokens.badges.overhang_px` (V5). The first badge always sits on the corner; further badges pack downward in `rank` order. **Polarity is carried by hue and glow, not by position** (V5). |
| **Hotkey text** | the icon's **top-left** corner | the key bound to this ability — nothing else | **Chrome, not a cue** (`spec.md` §3.8): it names the row and takes no part in the scan. One static outlined FontString on cap's own frame (V15), drawn from `tokens.hotkey`. Blank when the ability is unbound or reached only through a macro. It sits at the corner opposite the badge flow, so the two never negotiate a place. |
| **Cooldown swipe** | the radial dial | remaining time | Can be *restyled* without knowing the time (see V7). |
| **Count tile** | Blizzard's own aura count position | a sealed stack number | Client-owned; cap never learns the value. |
| **Independent bar** | anywhere on screen | one duration, large | Off-icon surface. |

**What Blizzard already occupies on a CDM item** — read off `Blizzard_CooldownViewer` at
**12.0.7**, under a standing ⚠ *12.1 rewrote this system and this has not been re-flown*:

- **BOTTOMRIGHT** — `ChargeCount.Current` on the cooldown tab and `Applications` on the aura tab,
  both anchored at −2 / +2.
- **Centre** — the countdown numbers the swipe draws.
- **Free:** bottom-centre. Both top corners were free until 2026-08-19; the badge stack flows
  from the **top-right** and the hotkey text (V15, chrome) now holds the **top-left**.

⚠ A previous revision of this table claimed Blizzard draws **keybind text** along the bottom of a
CDM item. It does not: `grep HotKey` over the whole `Blizzard_CooldownViewer` folder returns
**zero** — the CDM has no `HotKey` region at all (that is an ActionButton thing). Two things follow.
The badges start in the top-right because the top corners are free and the OS-badge convention
lives there, not because of a collision that does not exist. And cap's hotkey text (V15) is
**adding** a region the Cooldown Manager never had rather than restating one, which is most of why
it is worth drawing at all.

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

- **Geometry:** `tokens.badges.diameter_pct` of icon width. Badges **flow**: the first sits on the
  top-right corner, and each further badge steps one `diameter + tokens.badges.padding_px` **down**
  the right edge (`tokens.badges.flow`). Order is fixed by each cue's `rank`, never by arrival, so
  two rows wearing the same pair of cues always stack them the same way round. **There is no
  ceiling** — the vocabulary grows by declaring a cue, not by winning a slot.

  ⚠ **This replaced three fixed slots on 2026-08-19, and the thing that changed is what position
  MEANS.** The old layout ran negatives leftward along the top edge and put the one positive cue
  below the corner, so position carried polarity redundantly with hue — at the price of a hard
  ceiling of three cues, which is why a fourth could not be added without an argument about which
  of the three had stopped earning its place. That ceiling was geometry being read as design.
  Flowing gives up the redundancy: **hue and glow now carry polarity alone.** They carry it twice
  over (every positive cue is gold *and* glows; no negative does either), so the signal survives
  losing its third carrier — but a future negative cue that glows, or a gold one, would break
  something this layout no longer catches.

  ⚠ **One axis, deliberately.** An L — negatives left, positives down — was considered and
  rejected: the corner badge belongs to both arms, so a reader has to identify which arm a badge
  is on before its position means anything, and with a single badge present there is no arm to
  see. Flowing down also keeps clear of the neighbouring icon, since Cooldown Manager viewers lay
  their rows out horizontally.
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

| Cue | Polarity | Frames (`tokens.cues.<key>.frames`) | Loop | Rank | Means |
| --- | --- | --- | --- | --- | --- |
| **`priority`** | **positive** | `fire` (still — V14's ring is what moves) | `HOLD` | 1 | press this one — the scan would reach it late, or only after stepping over more skips than a reader can hold at once |
| **`capped`** | **positive** | `cards_stack → cards_stack_high` | `BOUNCE` | 2 | charges are at max and the recharge is stalled — you are losing one right now |
| **`blocked`** | negative | `timer_0 → CW_25 → CW_50 → CW_75 → timer_100` | `REPEAT` | 3 | held for a cooldown, or a readable dependency says the press would be wasted |
| **`starved`** | negative | `flask_empty → flask_half` | `BOUNCE` | 4 | you cannot afford it |
| **`overcap`** | negative | `flask_half → flask_full` | `BOUNCE` | 5 | pressing would waste resource |
| **`st_only`** | negative | `pawn` (still) | `HOLD` | 6 | the single-target spender while AoE mode is on |
| **`aoe_only`** | negative | `pawns` (still) | `HOLD` | 7 | the AoE spender in single target |

**The three negatives share one red** (`tokens.badges.rgb`) and carry no per-cue hue: one colour for
every "skip this" is what lets the row be read without decoding each glyph. **The positives share
one gold** for the same reason — one colour for every "act on this" — and they are told apart by
glyph, exactly as the negatives are. **Hue is the polarity carrier**, and since 2026-08-19 it is
the primary one rather than a reinforcement of position (V5).

**The two MODE cues are their own key for a reason.** A spec with two spenders has to say *which
one this is*, and until 2026-08-19 that was said with `blocked` — whose declared meaning is *"held
for a cooldown, or a readable dependency says the press would be wasted."* Neither clause is true
of the wrong-mode spender: nothing is held, nothing is wasted, it is simply the other one's turn.
One key answering two questions makes the badge stop carrying its *why*, which is the whole
justification for a vocabulary of negatives rather than a single "skip" mark.

⚠ **They are NOT budgeted** (Part 0.5's density rule), and the test is the same one `starved`
passes: a budgeted cue is cap claiming a castable, affordable button should be skipped **on
information the player cannot check at a glance**. Mode is the most checkable fact on the screen —
the player flipped the toggle themselves. The badge is a reminder of a choice they made, not a
claim they have to take on trust.

⚠ **Ranks put the positives on the corner.** `priority` and `capped` rank 1–2 and the negatives
3–5, so when a row wears both a promotion and a skip the promotion is the badge sitting where the
eye lands. `check` asserts the ordering rather than the absolute positions, which is what lets the
vocabulary grow without renegotiating geometry.

**`capped` animates exactly like the two flask cues** — a two-frame `BOUNCE` at the same
`duration_s`, a thin stack growing to a full one. Frame cadence is the *shared* idiom of the badge
vocabulary and carries no polarity; what separates this cue from the negatives is its hue, its
slot, and the glow below. Making it a still image had it reading as a different **kind** of widget
rather than a different **kind of statement**, which is not the distinction that matters.

⚠ **The positive cues glow; no negative does.** This is the second polarity carrier, and with
position no longer carrying it (V5) the two that remain are load-bearing: a negative cue that
glowed, or one tinted gold, would be indistinguishable from a promotion. `tokens.cues.capped.glow` pulses a halo *behind* the glyph
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

### V11 · Ruled-out hatch

**A row that is ruled out draws diagonal stripes across its whole face.** There are two ways to
be ruled out, they are drawn in two colours, and that is the whole primitive:

| Cause | Whose verdict | Colour |
| --- | --- | --- |
| the Cooldown Manager says the ability is down | Blizzard's | `tokens.hatch.rgb` at `tokens.hatch.alpha`, phase `tokens.hatch.phase_pct` |
| the row wears **any cue whose polarity is negative** | cap's | `tokens.hatch.skip.rgb` at `.alpha`, phase `.phase_pct` |

⚠ **This is Part 0.5's pass 2, drawn.** The procedure says *skip anything the swipe has run down,
and anything wearing a red cue; press the first that survives.* Until 2026-08-19 the first half was
drawn and the second was not — a swiped row was unmistakably out while a badged one relied on the
reader noticing a 22px disc. Now both halves look the same, and elimination is a thing you SEE
rather than a thing you perform.

⚠ **It generalises over polarity, not over cue keys.** `blocked`, `starved` and `overcap` all hatch
because all three are negative; a positive cue never hatches, and a future cue is covered the day it
declares its polarity rather than the day someone remembers to add it here. Promoted out of the lab
2026-08-19 (`stripes-l3-hold` and `stripes-l5-starved` together, since one rule answers both) per
Part 7 rule 4 — and the answer to those two entries' shared question, *"does one red across two
different reasons under-differentiate?"*, is that the **badge** carries the reason and the hatch
carries only the verdict. Two channels, two jobs.

⚠ **cap's half OVERHANGS the scan edge and carries its own border.** It is drawn
`tokens.hatch.skip.overhang_px` outside the icon rect, with a `tokens.hatch.skip.border` ring at
the same weight as V13's scan edge — so a ruled-out row's red replaces the yellow "in the scan"
line rather than sitting inside it. The two treatments would otherwise be making opposite
statements about the same row simultaneously, with the yellow reading as the louder of the two
because it is a hard line and the stripes are a wash. Blizzard's half stays inside the rect: its
cause is the CDM's own, and the swipe underneath it is already the client's statement.

⚠ **The two causes keep different phases** (`phase_pct` 50 against 0) so that a row which is
somehow both does not moiré into a flat wash. In practice markers are gated on readiness, so a
swiped row rarely wears a cue at all.

The cooldown half was promoted on 2026-08-16.

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

### V14 · Promotion ring

**A row wearing a positive cue draws a glowing ring around its badge**: `tokens.promotion`'s
flipbook, tinted `tokens.promotion.rgb`, at `tokens.promotion.spread` of the badge diameter,
walked at `tokens.promotion.fps`. Promoted out of the lab 2026-08-19 per Part 7 rule 4.

**It is a REPLICA of Blizzard's proc glow, and every number in it was measured rather than
chosen.** `wowkb.procring` generates the sheet against four properties read off
`ui-hud-actionbar-proc-loop-flipbook` (atlas 2476) on 2026-08-19:

| Measured on Blizzard's | Value | What it forced |
| --- | --- | --- |
| per-frame energy | varies **7%** | it does **not** pulse — the life is hot spots travelling the rim at constant total brightness |
| interior | flat **0.0** | it never touches the icon; the art underneath stays fully legible |
| radial falloff | ~9px out, ~3px in | **asymmetric** — light spilling off an edge, not a ring painted on one |
| band | centre ~17% in, ~20% wide | where the ring sits relative to what it surrounds |

⚠ **The first four candidates failed on the first property alone.** Every one of them breathed,
because "glow" reads as "pulse" until you measure one. A promotion that blinks makes its own
information come and go, which is what `tokens.text`'s flicker limits exist to forbid — the same
rule that keeps a badge glyph at full alpha while only its halo breathes (V5).

⚠ **Circular on purpose, and it is not a preference.** Blizzard's traces a rounded square because
an action button is square; cap's promotion sits on a round badge. A ring cropped from square art
reads as exactly that.

⚠ **It is NEUTRAL art, which the original is not.** White with the shape in alpha, so
`SetVertexColor` takes it to the authored hue — shown at Blizzard's own measured gold
(R.98 G.82 B.27) because that is what the player is trained on, but not bound to it. This is the
one way the replica beats the thing it replicates, and it is why generating beat vendoring.

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

⚠ **The preview draws a virtual row INLINE, and marks it.** In the client the panel is a separate
surface and that separation is what says *cap owns this frame*; a stepper page is one flat row, so
the separation is gone and the icon would read as a Cooldown Manager row cap has no right to. The
preview therefore draws every virtual entry in row order with a corner tick from
`tokens.preview.virtual_mark`, and a scenario writes the seam as `‖` on either side of the
Essential line. **This is a preview affordance and nothing else** — `preview` is excluded from
`Style.lua` by construction, so the addon cannot draw the tick and the panel geometry above is
unchanged.

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

### V15 · Hotkey text — the row's name

The one thing on a row that is not about the press. `spec.md` §3.8: it says **which button this
icon is**, and nothing about whether to press it. It exists because Blizzard's Cooldown Manager
draws no key at all (Part 1's ⚠), so "the third icon" and "the button under my ring finger" are
two thoughts the player has to join by memory.

- **Where:** the icon's **top-left**, inset `tokens.hotkey.offset` on both axes, anchored
  `tokens.hotkey.anchor`. That corner is free (Part 1) and stays free of cues — the badge stack
  flows from the opposite corner precisely so these two never have to negotiate a place.
- **Look:** `tokens.hotkey.font` at `tokens.hotkey.size` with `tokens.hotkey.outline`, in
  `tokens.hotkey.rgb` at `tokens.hotkey.alpha`. Off-white and a little under full alpha: legible at
  a glance without competing with a badge for the eye. It is the same outlined-static-text idiom
  Blizzard uses for the count tile (V8), which is what makes small text survive arbitrary icon art
  at 56 px.
- **The face is MONOSPACED, and that is the whole reason it is not the client's own.** A keybind
  is not prose: `csF1` sets four glyphs of four different widths hard against each other and reads
  as one smudge. A fixed advance gives the label internal rhythm, so the eye can count it instead
  of decoding it. The cost is paid honestly — monospace prices every glyph at the widest, so `M4`
  is wider than it would be in a proportional face — and it is bought back by choosing a
  *condensed* mono. Chosen over four alternatives, including Blizzard's own ARIALN, on the
  preview; `render-rationale.md` has none of this because the argument is above.
- ⚠ **cap ships this font**, which makes it the only third-party asset the addon redistributes.
  `tokens.preview.hotkey_font` carries the source, the licence and the rename OFL 1.1 clause 3
  requires; `capart export lua` writes the subset, `OFL.txt` and a `NOTICE.txt` into
  `Media/fonts/`, and `capart check` gates all three the way it gates `Style.lua`. Part 3's
  "don't bundle Blizzard art" is untouched by this and always was — the rule is about art that is
  **not ours to give away**, and this font is.
  ⚠ **`outline` is a client font FLAG, and it is the only dark edge cap can ask for.** `SetFont`
  takes `OUTLINE` or `THICKOUTLINE` — nothing between them and nothing wider — so readability here
  is bought with those two values and with `size`, and by nothing else. V15 spends both:
  `THICKOUTLINE` at the count tile's size rather than under it, because a label that cannot be read
  costs more than one that is a little loud. Two heavier treatments were tried and rejected on the
  preview — a plate sized to the label, which reads as something *stuck on* the icon, and a
  full-width title bar, which buys legibility with 16 of 56 px of art on every row forever.
- **It never moves, never blinks and never tints.** It carries no state, so it has nothing to
  animate: `tokens.text`'s flicker limits (`max_hz` / `duty` / `alpha_floor`) bind text that
  *changes*, and this does not, so they have no subject here. Part 4's tint guard likewise has no
  texture to guard, which is why `tokens.hotkey` carries no `tint` key.
- **Blank is a state it draws.** An unbound ability, or one reached only through a macro, gets the
  empty string — no placeholder glyph, no reserved box, no dash. An invented key is worse than an
  absent one.
- **Lua:**
  ```lua
  local hk = row:CreateFontString(nil, "OVERLAY")       -- cap's own frame, NOT the CDM item
  hk:SetFont("Fonts\\" .. T.hotkey.font, T.hotkey.size, T.hotkey.outline)
  hk:SetTextColor(T.hotkey.rgb[1], T.hotkey.rgb[2], T.hotkey.rgb[3])
  hk:SetAlpha(T.hotkey.alpha)
  hk:SetPoint(T.hotkey.anchor, row, T.hotkey.anchor, T.hotkey.offset.x, T.hotkey.offset.y)

  hk:SetText(ns.Binds.For(row.primary) or "")           -- a legal in-combat write (Part 3)
  ```
- **Preview reproduction.** Absolutely-positioned text in the icon box, off the `--hotkey-*`
  custom properties: same size in px against the same 56 px icon, same colour and alpha, same
  corner and inset, and the `OUTLINE` flag emulated as a real **stroke** (`-webkit-text-stroke`
  under `paint-order: stroke fill`), which is what the client's flag actually is.
  ⚠ **Offset `text-shadow` copies are not an outline and this file once said they were.** Every
  copy is antialiased, the overlaps accumulate alpha into a halo, and the diagonals sit at 2.83 px
  where the axials sit at 2 — so a 2 px "ring" rendered as a smudge with lumpy corners and made
  the preview's fonts look worse than any of them are. A stroke computed from the glyph outline is
  the only thing that converges on what the client draws from its SDF.
  **The preview draws the client's actual font.** `tokens.preview.hotkey_font_fdid` is
  `fonts/frizqt__.ttf`'s FileDataID — 615960, the same number the install's own
  `Fonts/615960.slug` carries — and `capart` pulls it out of CASC and embeds it as an `@font-face`
  data URI, exactly as it already embeds spell icons. **Part 3 permits this and always did:** its
  rule is *"extracted art is for measuring and for the preview, never for the addon's `Media/`
  folder"*, which is about what cap **redistributes**; nothing on this path reaches `Style.lua` or
  `Media/`. It matters because a substitute family gets **advance width** wrong, and "does
  `C-S-F1` fit the corner" is a width question — a near-enough letterform that lies about width
  answers it backwards. ⚠ The keys it draws are **simulated** — `tokens.preview.hotkeys`, a fixed
  cycle of the shapes real bindings take, assigned by roster position so the same ability always
  wears the same fake. The list is deliberately **longer than a spec's roster**, so no two rows in
  one scenario wear the same key — a duplicate would read as a bug in the hint rather than as an
  artefact of the fake. They are in `preview`, which `capart.NOT_THE_STYLE` excludes, so a fake key
  is structurally incapable of reaching the addon. The list deliberately includes a **wide** entry
  (`C-S-F1`): the corner has to be judged against the label that stresses it, not only against
  `3`.

---

## Part 2.5 — Composing a row

The primitives above are drawn together, and the order they compose in is fixed. **A row is a
hatch, a scan edge and badges** — the icon face is not cap's (Part 1), and nothing else takes part
in the composition. Chrome sits beside that rather than inside it: the hotkey text (V15) holds a
corner no cue may claim, carries no condition, and so has nothing to stack with or against. The
rule below is about conditions competing for a surface, and a label is not a condition.

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
  `Show`/`Hide`/`SetVertexColor`/`SetAlpha`, the texture-level frame step
  (`SetTexture` for a badge, `SetTexCoord` for V2's ring) that the frame walk needs and that the
  badge vocabulary has been making in combat since it shipped, and **`SetText` on cap's own
  FontStrings** — V15 re-reads its binding mid-pull, because a bar-page flip is a combat event and
  a label that waits for `PLAYER_REGEN_ENABLED` is wrong for the rest of the fight
  (`cdm-rider-patterns.md` §11 measured the read chain unfenced in Blizzard's own code). Nothing
  re-anchors, re-sizes or re-levels in combat; the arrival is painted into the art precisely so it
  does not have to.
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

9. **Does the hotkey read as a label or as another signal?** V15 is the only thing on a row that
   is not about the press, and its failure mode is being taken for one: a key the eye stops on
   during the scan costs exactly what a fourth badge would. Two specifics. A **wide** label —
   `C-S-F1` is the shape to look for — either fits the corner or starts crossing the icon. And the
   **gap**: a line of rows with one blank, from an unbound ability or a macro. Does that read as
   "you have not bound that" or as "cap is broken"? If the second, the finding is about the blank,
   not about the font.

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
    "flow": { "anchor": "top-right-corner", "direction": "down" }
  },
  "cues": {
    "blocked": {
      "means": "held for a cooldown, or a readable dependency says the press would be wasted. The sweep is a steady pace, NOT elapsed time.",
      "polarity": "negative",
      "frames": ["timer_0", "timer_CW_25", "timer_CW_50", "timer_CW_75", "timer_100"],
      "duration_s": 2.00, "loop": "REPEAT", "rank": 3, "open": false, "budgeted": true
    },
    "starved": {
      "means": "you cannot afford it",
      "polarity": "negative",
      "frames": ["flask_empty", "flask_half"],
      "duration_s": 1.20, "loop": "BOUNCE", "rank": 4, "open": false, "budgeted": false
    },
    "st_only": {
      "means": "the single-target spender, while AoE mode is on — the other one is the answer here",
      "polarity": "negative",
      "frames": ["pawn"],
      "duration_s": 1.20, "loop": "HOLD", "rank": 6, "open": false, "budgeted": false
    },
    "aoe_only": {
      "means": "the AoE spender, in single target — the other one is the answer here",
      "polarity": "negative",
      "frames": ["pawns"],
      "duration_s": 1.20, "loop": "HOLD", "rank": 7, "open": false, "budgeted": false
    },
    "overcap": {
      "means": "pressing would waste resource",
      "polarity": "negative",
      "frames": ["flask_half", "flask_full"],
      "duration_s": 1.20, "loop": "BOUNCE", "rank": 5, "open": false, "budgeted": false
    },
    "capped": {
      "means": "charges are at max and the recharge is stalled — you are losing one right now",
      "polarity": "positive",
      "rgb": [1.00, 0.78, 0.25],
      "glow": { "hz": 1.2, "alpha_min": 0.15, "alpha_max": 0.55, "scale": 1.55 },
      "frames": ["cards_stack", "cards_stack_high"],
      "duration_s": 1.20, "loop": "BOUNCE", "rank": 2, "open": false, "budgeted": false
    },
    "priority": {
      "means": "press this one — the scan would reach it late, or only after stepping over more skips than a reader can hold at once",
      "polarity": "positive",
      "rgb": [1.00, 0.78, 0.25],
      "glow": { "hz": 1.2, "alpha_min": 0.15, "alpha_max": 0.55, "scale": 1.55 },
      "frames": ["fire"],
      "duration_s": 1.20, "loop": "HOLD", "rank": 1, "open": false, "budgeted": false
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
    "tint": "shelf",
    "skip": {
      "rgb": [0.95, 0.30, 0.30], "alpha": 0.45, "phase_pct": 0,
      "overhang_px": 2,
      "border": { "rgb": [0.95, 0.30, 0.30], "alpha": 1.00, "line_px": 2 }
    }
  },
  "promotion": {
    "texture": "procring",
    "cols": 8, "rows": 4, "cell": 64, "frames": 32, "fps": 30,
    "rgb": [1.00, 0.82, 0.27],
    "alpha": 1.00,
    "spread": 2.00,
    "tint": "lane"
  },
  "hotkey": {
    "_comment": "V15. CHROME, not a cue (spec.md \u00a73.8): it names the row and asserts nothing about the press. No polarity, no rank, no badge slot, no motion \u2014 and deliberately NO `tint` key, because Part 4's tint guard scans art and this has none. `font` is a FULL CLIENT PATH, not a filename: this is cap's OWN shipped file, exported from tokens.preview.hotkey_font, which is the only third-party asset the addon redistributes. `outline` is a client FONT FLAG and the only dark edge cap can ask for: OUTLINE or THICKOUTLINE, nothing between them and nothing wider. Blank when the ability is unbound or reached only through a macro; never a placeholder.",
    "font": "Interface\\AddOns\\CombatAssistPlus\\Media\\fonts\\CapKeyMono.ttf",
    "size": 16,
    "outline": "THICKOUTLINE",
    "rgb": [0.92, 0.92, 0.90],
    "alpha": 0.85,
    "anchor": "TOPLEFT",
    "offset": { "x": 2, "y": -2 }
  },
  "preview": {
    "_comment": "NOT THE STYLE, and structurally incapable of becoming it: `preview` is in capart.NOT_THE_STYLE, so nothing here can reach Style.lua. It exists so the previews can draw a keybind hint before one exists in the game \u2014 the point of V15's preview is judging how the text sits in the corner, and that cannot be judged against an empty string. The strings are what `Binds.Shorten` PRODUCES, not what the client hands it: lowercase modifier letters closed up against the key (the client's own `SHIFT_KEY_TEXT_ABBR` is `s`), and `M4`/`N5` where the client would say `Mouse Button 4`/`Num Pad 5`.",
    "hotkeys": ["3", "s2", "M4", "csF1", "1", "4", "sE", "M5", "2", "a3",
                "5", "s4", "c1", "M3", "sF", "6", "asQ", "MU"],
    "hotkey_outline_rgb": [0.00, 0.00, 0.00],
    "hotkey_outline_px": 2,
    "hotkey_font": {
      "_comment": "The font V15 draws with, and the ONE third-party asset cap redistributes. The preview embeds this exact subset and the addon ships this exact subset, so the page and the game measure the same advance widths. `ship_as` is not a preference: the upstream family carries the Reserved Font Name 'Share', a subset is a Modified Version, and OFL 1.1 clause 3 forbids a Modified Version from using it \u2014 so the shipped file is renamed and `license_url` travels beside it.",
      "url": "https://raw.githubusercontent.com/google/fonts/main/ofl/sharetechmono/ShareTechMono-Regular.ttf",
      "family": "ShareTechMono",
      "ship_as": "CapKeyMono",
      "rfn": "Share",
      "license": "OFL 1.1",
      "license_url": "https://raw.githubusercontent.com/google/fonts/main/ofl/sharetechmono/OFL.txt",
      "shippable": true
    },
    "hotkey_font_stack": "'CapKeyMono', 'Trebuchet MS', var(--sans)",
    "virtual_mark": {
      "_comment": "PREVIEW ONLY, and it exists because the preview COMPRESSES a geometry the game does not have. In the client a virtual row (V12) lives in cap's own panel, physically separate from the Cooldown Manager, and the separation is what says 'cap owns this frame'. A stepper page draws one flat left-to-right row, so that separation is gone and the icon would read as a CDM row cap has no right to. The tick restores the one bit the compression lost. It is in `preview` deliberately: nothing here can reach Style.lua, and the addon must never draw it.",
      "rgb": [0.55, 0.82, 1.00],
      "size_px": 13,
      "line_px": 2,
      "overhang_px": 2,
      "corner": "bottom-left"
    },
    "unsure": {
      "_comment": "PREVIEW ONLY. The loud treatment for an `\u26a0 UNSURE` annotation under a row \u2014 a claim the authoring docs themselves doubt, drawn so it cannot be read past. Amber block, not a grey footnote. It says nothing about the press and takes no part in either reading pass; it is a note to the author about the DOC, not a mark on the button.",
      "rgb": [1.00, 0.74, 0.30],
      "bg_rgb": [0.23, 0.17, 0.06],
      "line_px": 2
    }
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
    "off-mode":       { "scan": true,  "swipe": false, "cues": [] },
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
  "budget": { "max_base64_kb": 300 },

  "lab": {
    "_comment": "NO AUTHORITY. Part 7. Nothing in `verdicts` or `cues` may name anything in here; capart enforces it. A treatment leaves the lab by being MOVED into Parts 1-6, never by being cited from there. A new idea gets a `lab` key, an `asks`, and a section in Part 7. \u26a0 The three entries below are FLIGHT-GATED, not look-gated: they draw no cells because what they ask is whether the CLIENT honours a rule cap authored, and Part 7 rule 2 already says a preview cannot answer that. They graduate on `aura-container-rule-formatter` / `aura-container-pandemic-region`, not on being looked at in a browser.",

    "count_band": {
      "asks": "Does a tainted-created NumericRuleFormatter get honoured on SetApplicationCount, so cap can author WHICH stack values show a number \u2014 including the complement and a middle band \u2014 rather than inheriting Blizzard's show-above-1 default?",
      "draws": "client-only",
      "pending_test": "aura-container-rule-formatter",
      "form": "S7",
      "font": "FRIZQT__.TTF", "size": 14, "outline": "OUTLINE",
      "anchor": "TOP", "y": 1,
      "bands": [
        { "threshold": 0, "format": "" },
        { "threshold": 4, "format": "%d" }
      ],
      "control_band": [
        { "threshold": 0, "format": "%d" }
      ]
    },

    "count_polarity": {
      "asks": "Can ONE count FontString carry two meanings \u2014 a negative band and a positive band in different hues \u2014 and if inline colour escapes are stripped, does a cap-shipped symbol font carry the same distinction as a SHAPE instead?",
      "draws": "client-only",
      "pending_test": "aura-container-rule-formatter",
      "form": "S8",
      "font": "FRIZQT__.TTF", "size": 14, "outline": "OUTLINE",
      "low_rgb": [1.00, 0.25, 0.25],
      "high_rgb": [0.25, 1.00, 0.44],
      "escape_bands": [
        { "threshold": 0, "format": "|cffff4040%d|r" },
        { "threshold": 6, "format": "|cff40ff70%d|r" }
      ],
      "static_fallback": "SetTextColor at setup carries ONE hue for the whole string and needs no markup at all; SetApplicationCount adds only Text and Shown, so VertexColor stays cap's."
    },

    "pandemic_mark": {
      "asks": "Does AddPandemicRegion drive a cap-owned texture from Blizzard's own refresh window, giving cap real ART out of a sealed fact with no curve and no ruleset to get wrong?",
      "draws": "client-only",
      "pending_test": "aura-container-pandemic-region",
      "form": "S9",
      "rgb": [1.00, 0.72, 0.20],
      "alpha": 0.85,
      "note": "The only Part 2 form that reaches cap-owned art without a font trick, and the only one that costs an OnUpdate."
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
2. **The lab never draws in a CDM row.** It renders on **its own page** — `previews/lab.html`,
   since 2026-08-19, rather than appended to every spec's page — **and, since 2026-08-16, it may
   also be drawn by the in-game `/cap style` gallery.**
   ⚠ **The split has a consequence for how an entry is written.** The declared style used to be
   one scroll away, so an entry could lean on the reader having just seen it. It cannot now:
   **an entry that needs a comparison must draw its own control cell**, the way `hotkey-l1` did.
   That convention was optional while the lab rode along beneath the style and is load-bearing
   now.
   The page is one for every spec because the lab is one for every spec: its cells resolve against
   the **shelf's reference roster**, never the spec being built, so a lab cell was never a claim
   about a spec's rotation — and drawing it under a spec's heading invited exactly that reading. The gallery is exempt because it is not a live row: it draws
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

**The lab was empty from 2026-08-19 until 2026-08-20**, when the three entries below were added.
An empty lab means every idea drawn here has been adopted or answered, not that nobody is trying
anything — and a lab that fills up again is the system working.

⚠ **These three are a different KIND of entry from every one in the ledger below, and the
difference matters.** Every previous entry was a *taste* question — five fonts, three stripe
phases, four glows — and the preview settled it by drawing them side by side. These three are
**capability** questions: they ask whether the client will honour a rule cap authored against a
secret. **Rule 2 already says a preview cannot answer that** ("a preview is an argument about the
client; the gallery is the client"), and here even the gallery cannot, because the gallery draws on
cap-owned frames with no secret in sight. So they draw **no cells**, and the page will correctly
say *"drawn in the client only"* for each.

**They graduate on a flight, not on being looked at.** `count_band` and `count_polarity` on
`aura-container-rule-formatter`; `pandemic_mark` on `aura-container-pandemic-region`. **All three
FLEW and PASSED `[client 2026-08-21]`** — the formatter is honoured (including the complement and
inline colour escapes), and `AddPandemicRegion` drives a cap-owned texture off Blizzard's real
window. The mechanism is measured, not a proposal; the drained findings and their working Lua are
`knowledge/addon-dev/security-taint-and-restricted-data.md` §3.5.2, and `../pattern-shelf.md`
S7–S9 are now `FLOWN`. **What remains is PROMOTION** — moving these three into Parts 1–6 with their
numbers and deleting them here (rule 4). That is a cap-pipeline step, not a prose edit: it re-runs
`capart export`, lifts `Catalog.lua:192`'s `min = 2`, and needs a cap release — **ask-first, not
yet done**. Until then they stay in the lab as *flown-and-passed*, and the tokens are measured
rather than proposed.

### L1 · `count_band` — a number that appears only inside a band

**Asks:** does a tainted-created `NumericRuleFormatter` get honoured on `SetApplicationCount`?

S2 draws a count above one fixed threshold, and cap has always read that threshold as the
platform's. It is not: it is `elseif applications > 1`, Blizzard's behaviour when **no formatter is
passed** (`Blizzard_CustomAuraButton.lua:351-368`). Passing one replaces it with a piecewise
function cap authors — so "blank until 4, then 4" is two breakpoints, and so are the complement
("blank above 1") and a middle band.

The entry declares its bands **and a control band** that shows the number at *every* value
including 1. That control is the load-bearing part: Blizzard's default never prints a "1", so a
lone `1` on screen is the only unambiguous proof the formatter ran. Without it, "our rules were
ignored" and "our rules correctly hid a low number" look identical, and the flight learns nothing.

**It flew and passed `[client 2026-08-21]`** — tile B drew a lone `1`, so a cap-authored ruleset
runs. Promoting it: `Catalog.lua`'s `min = 2` lifts to "a positive integer" and S7 moves into
Part 2, first consumers Demonology's Core-at-4 and Implosion's six-imp gate (the cap-pipeline +
release step above).

### L2 · `count_polarity` — two meanings in one count

**Asks:** can one FontString carry a negative band and a positive band in different hues — and if
inline colour escapes are stripped, does a symbol font carry the distinction as a **shape**?

Two routes, deliberately drawn as one entry because they are the same question asked of two
mechanisms. `escape_bands` puts `|c…|r` inside each band's format; the font route puts a PUA
codepoint there instead. `C_StringUtil` ships `EscapeQuotedCodes` and `StripHyperlinks`, so the
client sanitises markup *somewhere* — whether the formatter does is invisible from Lua.

⚠ **The routes have different blast radii and the entry exists to separate them.** A stripped
escape costs colour; a font that does not render costs the whole treatment. `static_fallback`
records what survives either failure: `SetApplicationCount` adds only `Text` and `Shown`
(`:59-68`), **not** `VertexColor`, so one static hue via `SetTextColor` at setup needs no markup
and cannot be stripped. That is the floor, and it is already ours.

⚠ **A font is a second art channel this repo does not own.** `render-shelf` → `capart export
badges` → `capart check` is what stops the preview and the addon drifting; a TTF sits outside it.
Adopting L2's font route means the shelf declares the glyph set and `check` gates the font the way
it gates badge TGAs. **That is a pipeline change, not a token change**, and it is the reason this
entry is not simply "add a font".

### L3 · `pandemic_mark` — cap-owned art from a sealed window

**Asks:** does `AddPandemicRegion` drive a cap-owned texture from Blizzard's own refresh window?

This is the odd one out and the most interesting. Every other sealed form makes cap author a
threshold — a curve break point, a breakpoint table — and every authored threshold is a thing to
get wrong. This one has **none**: the client computes the window itself as
`GetRefreshExtendedDuration − GetAuraBaseDuration` (`:612-628`), which is Blizzard's real
pandemic, not the community's 30 %, and simply calls `SetShown` on any Region cap registered
(`:567-573`).

**It is also the only sealed form that reaches cap's existing badge art directly** — a Texture
qualifies, so no font trick and no numeral. If L3 flies, the "sealed facts can only become text"
limit stops being general.

Two costs, both real: it is the only sink that carries an `OnUpdate` (`:634-641`, and Blizzard
`secretwrap`s even the *enablement*, because whether your update loop runs would otherwise leak the
aura's presence), and it has **no consumer yet** — Demonology's Doom is the obvious first, and
Affliction is most of a spec.

### What has left, and where it went

Every row is rule 4 in action: moved into Parts 1–6 with its numbers, or deleted because the
question it asked got an answer. Nothing here is cited by the style; this is a ledger, so that
"why is there no entry for X" has somewhere to be answered.

| Left | When | Where it went |
| --- | --- | --- |
| `border-arrival` (L1) | 2026-08-13 | → **V2**, the lane border and its arrival snap. Since retired itself. |
| `badge-slots` (L2) | 2026-08-13 | → **V5**, the corner badges, with the cue vocabulary rewritten negative-only. |
| `stripes-l4-cooldown` (L4) | 2026-08-16 | → **V11**, taking the shared stripe sheet with it — `tokens.hatch` now, `Media/stripes.tga` in the addon. |
| `stripes-l3-hold`, `stripes-l5-starved` | 2026-08-19 | Answered together when **V11 generalised** from "on cooldown" to "ruled out": a row wearing any negative cue stripes, which is Part 0.5's pass 2 drawn rather than merely stated. One rule answered both, so the family emptied. |
| `blaze-*`, `procglow-*` | 2026-08-19 | **V14**, the promotion ring, was picked out of this set — generated by `wowkb.procring` against four properties measured off Blizzard's own proc glow. The losing candidates are deleted rather than kept: they were alternatives to a decision that has been made, and a lab full of settled arguments is a lab nobody reads. |
| `arrival-*` | 2026-08-19 | Deleted with their subject. The arrival questions belonged to V2's animated border; **V13's scan edge is static**, so there is no snap to judge and the entries had outlived the thing they were asking about. |
| `ready-*` | 2026-08-19 | **V13**, the scan edge, was picked out of this set. Part 5 question 2 still asks whether a static line is loud enough in a pull — but that is a question about the *shipped* treatment, and it is asked there, not by keeping three unadopted alternatives drawn beside it. |
| `hotkey-l1` … `hotkey-l10` | 2026-08-19 | **V15**'s font, size and dark edge were chosen out of this set of ten — five faces, then a plate, then a title bar. The winner is `tokens.hotkey`; what the losers cost is written into V15 itself, which is the point of promotion rather than citation. |

⚠ **A deleted entry is not a refuted one.** Nothing in this table is a claim that the treatment
was bad — most of them lost to something, and one or two were simply asking about a primitive that
no longer exists. `git log` holds every one of them with its `asks` intact, which is where a
revived idea should be read from. Re-adding one is cheap: a `lab` key, an `asks`, and a section
here.
