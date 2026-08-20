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
    "size": 14,
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
    "hotkey_font_stack": "'CapKeyMono', 'Trebuchet MS', var(--sans)"
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
  "budget": { "max_base64_kb": 750 },

  "lab": {
    "_comment": "NO AUTHORITY. Part 7. Nothing in `verdicts` or `cues` may name anything in here; capart enforces it. A treatment leaves the lab by being MOVED into Parts 1-6, never by being cited from here. The stripe entries below draw on `tokens.hatch`'s sheet, which is the STYLE's — a lab entry citing the style is the legal direction.",
    "_arrival_stage": { "neighbours": 2 },

    "hotkey-l1-frizqt": {
      "draws": "hotkey",
      "title": "V15 as declared — FRIZQT__, the control",
      "asks": "This is what the style says today, drawn so the candidates below have something to beat. Friz Quadrata is the client's UI face and therefore the one that looks like it belongs — but it is a glyphic serif with wide letterforms, which is the opposite of what a four-character label in a 56 px corner wants. Does belonging beat fitting?",
      "font": { "fdid": 615960, "family": "FRIZQT__", "client_path": "Fonts\\FRIZQT__.TTF", "license": "Blizzard \u2014 in every install; cap may name it, never bundle it" },
      "size_px": 14, "outline": "THICKOUTLINE", "outline_px": 2,
      "cells": [{"ability": "Eye Beam", "verdict": "press", "key": "csF1", "caption": "the <b>widest</b> label, on dark art. If a candidate fails anywhere it fails here."}, {"ability": "Immolation Aura", "verdict": "press", "key": "sF", "caption": "a modified key on <b>bright, busy</b> art — the legibility case the outline exists for."}, {"ability": "Blade Dance", "verdict": "hold-readable", "key": "M4", "caption": "a mouse binding, <b>beside a badge</b>. The label must win the overlap outright."}, {"ability": "Throw Glaive", "verdict": "cd", "key": "3", "caption": "the common case, on a swiped row — does it stay readable through the dial?"}],
      "_note": "Same family and size the style declares, so this cell set is also the reference the other two are read against."
    },

    "hotkey-l2-arialn": {
      "draws": "hotkey",
      "title": "ARIALN \u2014 what Blizzard itself puts on a hotkey",
      "asks": "Blizzard's own action-button HotKey, reproduced EXACTLY: ARIALN.TTF at 12 with a NORMAL outline [T1 src: Blizzard_Fonts_Shared/Mainline/GameFonts.xml:59-61 via GameFontStyles.xml:18-23 and ActionButtonTemplate.xml:85]. Fifteen years of the player reading keybinds in this face, at this size, on buttons this big \u2014 the strongest prior in the set, and the only candidate that costs nothing to adopt. Note what it is NOT: not 14, and not thick. If the shipped answer to this exact problem is a point smaller and a stroke thinner than V15 declares, that is a finding about V15.",
      "font": { "fdid": 615958, "family": "ARIALN", "client_path": "Fonts\\ARIALN.TTF", "license": "Blizzard \u2014 in every install; cap may name it, never bundle it" },
      "size_px": 12, "outline": "OUTLINE", "outline_px": 1,
      "cells": [{"ability": "Eye Beam", "verdict": "press", "key": "csF1", "caption": "the <b>widest</b> label, on dark art. If a candidate fails anywhere it fails here."}, {"ability": "Immolation Aura", "verdict": "press", "key": "sF", "caption": "a modified key on <b>bright, busy</b> art — the legibility case the outline exists for."}, {"ability": "Blade Dance", "verdict": "hold-readable", "key": "M4", "caption": "a mouse binding, <b>beside a badge</b>. The label must win the overlap outright."}, {"ability": "Throw Glaive", "verdict": "cd", "key": "3", "caption": "the common case, on a swiped row — does it stay readable through the dial?"}],
      "_note": "⚠ NOT SHIPPABLE. It is Blizzard's font, so cap may READ it by name (`SetFont(\"Fonts\\\\ARIALN.TTF\", ...)`) exactly as any addon does — the client already has it — but it may never be bundled. That makes this candidate free if it wins: no Media/ file, no licence, no page weight in the addon."
    },

    "hotkey-l3-barlow": {
      "draws": "hotkey",
      "title": "Barlow Condensed SemiBold \u2014 ours to ship",
      "asks": "The one candidate that is genuinely OURS: OFL 1.1, so cap could bundle it and stop depending on what the client happens to have. Condensed and semibold is the shape a small high-contrast label wants \u2014 more characters per pixel of width, and enough weight to survive an outline at 14 px. Does a face the game does not use anywhere else read as deliberate, or as an addon that did not match?",
      "font": { "url": "https://raw.githubusercontent.com/google/fonts/main/ofl/barlowcondensed/BarlowCondensed-SemiBold.ttf", "family": "BarlowCondensed", "client_path": "Interface\\AddOns\\CombatAssistPlus\\Media\\lab\\BarlowCondensed.ttf", "license": "OFL 1.1", "shippable": true },
      "size_px": 14, "outline": "THICKOUTLINE", "outline_px": 2,
      "cells": [{"ability": "Eye Beam", "verdict": "press", "key": "csF1", "caption": "the <b>widest</b> label, on dark art. If a candidate fails anywhere it fails here."}, {"ability": "Immolation Aura", "verdict": "press", "key": "sF", "caption": "a modified key on <b>bright, busy</b> art — the legibility case the outline exists for."}, {"ability": "Blade Dance", "verdict": "hold-readable", "key": "M4", "caption": "a mouse binding, <b>beside a badge</b>. The label must win the overlap outright."}, {"ability": "Throw Glaive", "verdict": "cd", "key": "3", "caption": "the common case, on a swiped row — does it stay readable through the dial?"}],
      "_note": "Shipping it costs a Media/fonts/ file and an OFL.txt beside it. The subset `capart` already builds \u2014 the ~45 glyphs a keybind can contain \u2014 is what makes that cheap; the full face is 107 KB and the subset is a fraction of it. That subset is exactly as shippable as the full font under OFL 1.1."
    },

    "hotkey-l4-plexmono": {
      "draws": "hotkey",
      "title": "IBM Plex Mono SemiBold \u2014 fixed width, well drawn",
      "asks": "Every candidate above is PROPORTIONAL, and a keybind is not prose: `csF1` sets four glyphs of four different widths hard against each other and reads as one smudge. A monospaced face gives every character the same advance, so the label has internal rhythm and the eye can count it. The cost is real and is the thing to judge \u2014 monospace prices every glyph at the widest one, so `M4` gets wider even as `csF1` gets clearer. Does the rhythm buy more than the width costs?",
      "font": { "url": "https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexmono/IBMPlexMono-SemiBold.ttf", "family": "IBMPlexMono", "client_path": "Interface\\AddOns\\CombatAssistPlus\\Media\\lab\\IBMPlexMono.ttf", "license": "OFL 1.1", "shippable": true },
      "size_px": 13, "outline": "THICKOUTLINE", "outline_px": 2,
      "cells": [{"ability": "Eye Beam", "verdict": "press", "key": "csF1", "caption": "the <b>widest</b> label, on dark art. If a candidate fails anywhere it fails here."}, {"ability": "Immolation Aura", "verdict": "press", "key": "sF", "caption": "a modified key on <b>bright, busy</b> art — the legibility case the outline exists for."}, {"ability": "Blade Dance", "verdict": "hold-readable", "key": "M4", "caption": "a mouse binding, <b>beside a badge</b>. The label must win the overlap outright."}, {"ability": "Throw Glaive", "verdict": "cd", "key": "3", "caption": "the common case, on a swiped row — does it stay readable through the dial?"}],
      "_note": "A size SMALLER than the proportional candidates, deliberately: monospace is wider per character, so matching them on width means giving up a point. If it still reads at 13 it has won on more than rhythm."
    },

    "hotkey-l5-sharetechmono": {
      "draws": "hotkey",
      "title": "Share Tech Mono \u2014 fixed width that is also narrow",
      "asks": "The compromise entry, and the reason both mono candidates are here. Share Tech Mono is a CONDENSED monospace, so it takes the uniform advance that fixes the smudge without paying the usual width for it. The risk is the other direction: a narrow mono at 14 px with a thick outline can close its own counters \u2014 the holes in `e`, `a`, `0` fill in and every glyph turns into a blob. Does it stay open?",
      "font": { "url": "https://raw.githubusercontent.com/google/fonts/main/ofl/sharetechmono/ShareTechMono-Regular.ttf", "family": "ShareTechMono", "client_path": "Interface\\AddOns\\CombatAssistPlus\\Media\\lab\\ShareTechMono.ttf", "license": "OFL 1.1", "shippable": true },
      "size_px": 14, "outline": "THICKOUTLINE", "outline_px": 2,
      "cells": [{"ability": "Eye Beam", "verdict": "press", "key": "csF1", "caption": "the <b>widest</b> label, on dark art. If a candidate fails anywhere it fails here."}, {"ability": "Immolation Aura", "verdict": "press", "key": "sF", "caption": "a modified key on <b>bright, busy</b> art — the legibility case the outline exists for."}, {"ability": "Blade Dance", "verdict": "hold-readable", "key": "M4", "caption": "a mouse binding, <b>beside a badge</b>. The label must win the overlap outright."}, {"ability": "Throw Glaive", "verdict": "cd", "key": "3", "caption": "the common case, on a swiped row — does it stay readable through the dial?"}],
      "_note": "Only 42 KB before subsetting, the smallest source of the five \u2014 it carries a narrow character set, which is exactly what a keybind needs."
    },

    "hotkey-l6-sharetech-thin": {
      "draws": "hotkey",
      "title": "Share Tech Mono, NORMAL outline \u2014 is the thick edge the problem?",
      "asks": "The same face as l5 with the only other value the flag takes. A thick stroke is bought at the counters' expense: at 14 px it eats into the holes in `0`, `e` and `a` and closes the gap between neighbouring glyphs, so the thing meant to make the label legible is also what turns it to mush. Blizzard reached the same place from the other side \u2014 its own hotkey uses a NORMAL outline (l2). Read this beside l5 and answer one question: is the dark edge carrying the label over bright art, or is it the reason the label looks smudged?",
      "font": { "url": "https://raw.githubusercontent.com/google/fonts/main/ofl/sharetechmono/ShareTechMono-Regular.ttf", "family": "ShareTechMono", "client_path": "Interface\\AddOns\\CombatAssistPlus\\Media\\lab\\ShareTechMono.ttf", "license": "OFL 1.1", "shippable": true },
      "size_px": 14, "outline": "OUTLINE", "outline_px": 1,
      "cells": [{"ability": "Eye Beam", "verdict": "press", "key": "csF1", "caption": "the <b>widest</b> label, on dark art. If a candidate fails anywhere it fails here."}, {"ability": "Immolation Aura", "verdict": "press", "key": "sF", "caption": "a modified key on <b>bright, busy</b> art — the legibility case the outline exists for."}, {"ability": "Blade Dance", "verdict": "hold-readable", "key": "M4", "caption": "a mouse binding, <b>beside a badge</b>. The label must win the overlap outright."}, {"ability": "Throw Glaive", "verdict": "cd", "key": "3", "caption": "the common case, on a swiped row — does it stay readable through the dial?"}],
      "_note": "Costs nothing extra: same family as l5, so one @font-face and one shipped file serve both. The BRIGHT-art cell decides it \u2014 a thin edge is free on dark art, and bright art is exactly where a thick one earns its keep."
    },

    "hotkey-l7-arialn-14-plate": {
      "draws": "hotkey",
      "title": "ARIALN 14 on a plate \u2014 contrast from the ground, not from the stroke",
      "asks": "The other way to make small text survive arbitrary icon art. An outline fights the background at every glyph edge; a plate REPLACES the background, so the label is read against one known colour and the stroke stops having to do the work. It is also the badge's own move \u2014 `tokens.badges.plate` is why a 22 px sprite reads on any icon \u2014 so the row already contains this idea and the hint would be echoing it rather than introducing it. What it costs is ink: a filled rectangle in the corner is a second object on the row, and the whole claim of chrome is that it recedes. Does it still recede?",
      "font": { "fdid": 615958, "family": "ARIALN", "client_path": "Fonts\\ARIALN.TTF", "license": "Blizzard \u2014 in every install; cap may name it, never bundle it" },
      "size_px": 14, "outline": "OUTLINE", "outline_px": 1,
      "plate": { "rgb": [0.00, 0.00, 0.00], "alpha": 0.78, "pad_x_px": 3, "pad_y_px": 1 },
      "cells": [{"ability": "Eye Beam", "verdict": "press", "key": "csF1", "caption": "the <b>widest</b> label, on dark art. If a candidate fails anywhere it fails here."}, {"ability": "Immolation Aura", "verdict": "press", "key": "sF", "caption": "a modified key on <b>bright, busy</b> art — the legibility case the outline exists for."}, {"ability": "Blade Dance", "verdict": "hold-readable", "key": "M4", "caption": "a mouse binding, <b>beside a badge</b>. The label must win the overlap outright."}, {"ability": "Throw Glaive", "verdict": "cd", "key": "3", "caption": "the common case, on a swiped row — does it stay readable through the dial?"}],
      "_note": "Alpha matches `tokens.badges.plate.alpha` deliberately \u2014 if both plates on a row are read at the same weight they read as one system. The outline drops to NORMAL because a plate and a thick stroke are two solutions to one problem and stacking them is what makes a corner look armoured."
    },

    "hotkey-l8-arialn-16-plate": {
      "draws": "hotkey",
      "title": "ARIALN 16 on a plate \u2014 the same idea, spent on size",
      "asks": "If the plate carries the contrast, the size no longer has to be a compromise with legibility \u2014 so this asks what the label looks like when it is simply BIG. 16 px on a 56 px icon is a label you cannot fail to read. The question is the one chrome always faces: at what size does it stop naming the row and start competing with it? Read it against l7 and find the point where the answer flips.",
      "font": { "fdid": 615958, "family": "ARIALN", "client_path": "Fonts\\ARIALN.TTF", "license": "Blizzard \u2014 in every install; cap may name it, never bundle it" },
      "size_px": 16, "outline": "OUTLINE", "outline_px": 1,
      "plate": { "rgb": [0.00, 0.00, 0.00], "alpha": 0.78, "pad_x_px": 3, "pad_y_px": 1 },
      "cells": [{"ability": "Eye Beam", "verdict": "press", "key": "csF1", "caption": "the <b>widest</b> label, on dark art. If a candidate fails anywhere it fails here."}, {"ability": "Immolation Aura", "verdict": "press", "key": "sF", "caption": "a modified key on <b>bright, busy</b> art — the legibility case the outline exists for."}, {"ability": "Blade Dance", "verdict": "hold-readable", "key": "M4", "caption": "a mouse binding, <b>beside a badge</b>. The label must win the overlap outright."}, {"ability": "Throw Glaive", "verdict": "cd", "key": "3", "caption": "the common case, on a swiped row — does it stay readable through the dial?"}],
      "_note": "⚠ At 16 the plate for `csF1` is a visibly large rectangle. The `blocked` badge's disc is `tokens.badges.diameter_pct` (40%) of the icon \u2014 about 22 px \u2014 so compare the two areas directly: if the label's plate is bigger than the badge, chrome has become the loudest thing on the row."
    },

    "hotkey-l9-titlebar": {
      "draws": "hotkey",
      "title": "Title bar \u2014 the label stops being a sticker and becomes part of the frame",
      "asks": "l7/l8 put a plate the size of the text on the icon, and a small dark rectangle floating over art reads as something STUCK ON. A bar the full width of the icon reads as furniture instead: it has an edge the eye can resolve, it is in the same place on every row so the eye stops hunting for it, and a bar of constant width says nothing about the label inside it \u2014 which is exactly what chrome is supposed to say. The cost is icon: 16 of 56 px of art is now under a bar, on every row, forever. Is a row still identifiable by its picture?",
      "colour": "Near-black with a slight cool cast, at 0.85, and a one-pixel neutral rule along the bottom. NOT a cue colour and deliberately so: red is every negative cue and gold is every positive one (Part 0.5), so a bar in either would be the loudest false signal on the row. Neutral-cool also separates from the warm icon art most abilities carry, which is what makes the bottom rule readable at all.",
      "font": { "fdid": 615958, "family": "ARIALN", "client_path": "Fonts\\ARIALN.TTF", "license": "Blizzard \u2014 in every install; cap may name it, never bundle it" },
      "size_px": 12, "outline": "OUTLINE", "outline_px": 1,
      "bar": { "rgb": [0.04, 0.05, 0.07], "alpha": 0.85, "height_px": 16, "align": "center", "fade": false, "rule": { "rgb": [1.00, 1.00, 1.00], "alpha": 0.12, "px": 1 } },
      "cells": [{"ability": "Eye Beam", "verdict": "press", "key": "csF1", "caption": "the <b>widest</b> label, on dark art. If a candidate fails anywhere it fails here."}, {"ability": "Immolation Aura", "verdict": "press", "key": "sF", "caption": "a modified key on <b>bright, busy</b> art — the legibility case the outline exists for."}, {"ability": "Blade Dance", "verdict": "hold-readable", "key": "M4", "caption": "a mouse binding, <b>beside a badge</b>. The label must win the overlap outright."}, {"ability": "Throw Glaive", "verdict": "cd", "key": "3", "caption": "the common case, on a swiped row — does it stay readable through the dial?"}],
      "_note": "⚠ It runs UNDER the badge stack, which flows from the top-right corner and overhangs it by `tokens.badges.overhang_px`. The badge cell is the one to look at: a bar the badge sits on top of may be fine (the badge is the louder object and should win) or may look broken. Centred text is not decoration \u2014 left-aligned, a bar is just a plate that grew; centred, it reads as a field with something in it."
    },

    "hotkey-l10-titlebar-fade": {
      "draws": "hotkey",
      "title": "Title bar as a scrim \u2014 same geometry, no bottom edge",
      "asks": "The objection to l9 is that a hard-edged bar CUTS the icon in two, and a 56 px picture cannot afford to be bisected. This is the same 16 px of darkening with the edge taken away: opaque at the top, transparent at the bottom, no rule. It should read as the art fading out under the label rather than as a strip laid over it. The risk is the opposite one \u2014 a scrim with no edge may just look like the icon is damaged. Which failure is worse is the entire question, and it is not answerable by argument.",
      "colour": "The same near-black cool cast as l9 and the same 0.85 at its top, so the two differ in ONE property. A gradient is what the client actually does here (`SetGradient`, Part 3), not a CSS-only trick \u2014 and Part 3's warning applies: apply the gradient first and tint second, because SetGradient resets vertex colour to white.",
      "font": { "fdid": 615958, "family": "ARIALN", "client_path": "Fonts\\ARIALN.TTF", "license": "Blizzard \u2014 in every install; cap may name it, never bundle it" },
      "size_px": 12, "outline": "OUTLINE", "outline_px": 1,
      "bar": { "rgb": [0.04, 0.05, 0.07], "alpha": 0.85, "height_px": 16, "align": "center", "fade": true },
      "cells": [{"ability": "Eye Beam", "verdict": "press", "key": "csF1", "caption": "the <b>widest</b> label, on dark art. If a candidate fails anywhere it fails here."}, {"ability": "Immolation Aura", "verdict": "press", "key": "sF", "caption": "a modified key on <b>bright, busy</b> art — the legibility case the outline exists for."}, {"ability": "Blade Dance", "verdict": "hold-readable", "key": "M4", "caption": "a mouse binding, <b>beside a badge</b>. The label must win the overlap outright."}, {"ability": "Throw Glaive", "verdict": "cd", "key": "3", "caption": "the common case, on a swiped row — does it stay readable through the dial?"}],
      "_note": "⚠ A BAR ABOVE THE ICON was considered and is refuted, not parked. Scenario: the bar sits in the gap between rows so it covers no art at all. Failing rung: `tokens.surfaces.row_gap_px` is 6 and the client owns the layout \u2014 a 16 px bar would overlap the row above by 10 px, on a frame cap does not control and must not reparent (Part 1). Reopening condition: a CDM layout whose row pitch cap can read AND a gap of at least the bar height, or the bar shrinking to 6 px, which no font fits."
    },

    "procglow-l8-square": {
      "draws": "flipbook",
      "title": "Blizzard's OWN proc glow, unaltered — the control",
      "asks": "This is the effect the player already has fifteen years of training on, drawn at its real size on the icon. Every entry below has to beat it. Does a rounded-square glow still read correctly around a Cooldown Manager row, which is the same square shape as an action button?",
      "sheet": "procloop", "cols": 8, "rows": 4, "cell": 64, "frames": 30, "fps": 30,
      "tint": "none", "blend": "ADD", "scale": 1.45,
      "cells": [
        { "kind": "icon", "ability": "The Hunt", "verdict": "press",
          "caption": "<b>the control</b> — <code>ui-hud-actionbar-proc-loop-flipbook</code>, atlas 2476, exactly as the client draws it." },
        { "kind": "icon", "ability": "Essence Break", "verdict": "below",
          "caption": "<b>the neighbour</b> — an icon-scale effect is judged by what it does to the row, not to its own square." }
      ]
    },

    "procglow-l10-flame": {
      "draws": "flipbook",
      "title": "A flame flipbook — 64 frames of actual fire",
      "asks": "Fire is the most literal possible reading of *urgent*. Does an effect with this much internal motion still let the ICON be read — the thing the player actually has to identify — or does it win the row and lose the button?",
      "sheet": "flame", "cols": 8, "rows": 4, "cell": 64, "frames": 32, "fps": 15,
      "tint": "none", "blend": "ADD", "scale": 1.55,
      "cells": [
        { "kind": "icon", "ability": "The Hunt", "verdict": "press",
          "caption": "<b>flame</b> — vendored VFX, 64 frames. Baked hue by nature: fire is a gradient, not one colour multiplied." },
        { "kind": "icon", "ability": "Essence Break", "verdict": "below",
          "caption": "<b>the neighbour</b> — the honest question for this one is whether it reads as a cue or as the row being on fire." }
      ]
    },

    "procglow-l11-energy": {
      "draws": "flipbook",
      "title": "An energy burst — 36 frames, one shot rather than a loop",
      "asks": "A burst has a beginning, which a loop does not. Does a one-shot that fires WHEN the press becomes correct beat a loop that simply persists — and after it ends, is the button still marked, or has the information gone?",
      "sheet": "energy", "cols": 8, "rows": 3, "cell": 64, "frames": 18, "fps": 12,
      "tint": "none", "blend": "ADD", "scale": 1.70,
      "cells": [
        { "kind": "icon", "ability": "The Hunt", "verdict": "press",
          "caption": "<b>burst</b> — decoded from a 4K float16 EXR whose alpha channel was empty; visibility is its luminance." },
        { "kind": "icon", "ability": "Essence Break", "verdict": "below",
          "caption": "<b>the neighbour</b> — the widest of the five at 1.70x, so if anything reaches a neighbouring icon it is this." }
      ]
    },

    "procglow-l12-sparkler": {
      "draws": "flipbook",
      "title": "A sparkler, GENERATED — and the only one that can be re-hued",
      "asks": "The other four are art we found; this one is art we can change. It is white-on-alpha, so it takes the lane's own colour instead of dictating one. Does a neutral particle burst carry the same *press me* as baked fire, or is the heat of the colour doing most of the work?",
      "sheet": "sparkler", "cols": 8, "rows": 4, "cell": 64, "frames": 32, "fps": 30,
      "tint": "lane", "blend": "ADD", "scale": 1.60,
      "rgb": [1.00, 0.78, 0.25],
      "cells": [
        { "kind": "icon", "ability": "The Hunt", "verdict": "press",
          "caption": "<b>sparkler</b> — <code>wowkb.sparkler</code>, seeded and reproducible. Shown at the positives' gold; it can be any hue." },
        { "kind": "icon", "ability": "Essence Break", "verdict": "below",
          "caption": "<b>the neighbour</b> — the comparison that matters is against L8: does this beat the thing you are already trained on?" }
      ]
    },

    "blaze-l6-behind-glyph": {
      "draws": "blaze",
      "behind": "glyph",
      "title": "\"Press me!!!\" — the blaze BEHIND THE FLAME",
      "asks": "If a promotion shouts instead of pointing, is it still readable? This puts the bright field behind the flame's own silhouette, so the light has the glyph's shape. Does that read as one hot object — or does an irregular blob of light on a 56px icon just read as damage?",
      "sprite": "fire",
      "rgb": [1.00, 0.62, 0.12],
      "alpha": 0.95,
      "spread": 2.30,
      "glyph_rgb": [1.00, 1.00, 1.00],
      "period_s": 0.9,
      "rest_alpha": 0.55,
      "cells": [
        { "kind": "icon", "ability": "The Hunt", "verdict": "press",
          "caption": "<b>the shout</b> — the light wears the flame&rsquo;s own outline, so the glyph looks like the source of it rather than something sitting on a lamp." },
        { "kind": "icon", "ability": "Essence Break", "verdict": "below",
          "caption": "<b>the neighbour</b> — the row is read as a whole, so the question is not whether this is loud but whether it makes the icon BESIDE it harder to read." },
        { "kind": "icon", "ability": "The Hunt", "verdict": "below", "treat": false,
          "caption": "<b>control</b> — the same icon untreated. A treatment that only reads beside its own caption has not read." }
      ]
    },

    "blaze-l7-behind-plate": {
      "draws": "blaze",
      "behind": "plate",
      "title": "\"Press me!!!\" — the blaze BEHIND THE BLACK CIRCLE",
      "asks": "The same shout, with the light behind the badge's dark disc instead of the glyph. The plate keeps its job — contrast under the sprite — and the blaze becomes a halo with a hard edge. Does the disc make it read as a BADGE that is shouting, rather than as the icon being on fire?",
      "sprite": "fire",
      "rgb": [1.00, 0.62, 0.12],
      "alpha": 0.95,
      "spread": 2.30,
      "glyph_rgb": [1.00, 1.00, 1.00],
      "period_s": 0.9,
      "rest_alpha": 0.55,
      "cells": [
        { "kind": "icon", "ability": "The Hunt", "verdict": "press",
          "caption": "<b>the shout</b> — the dark disc sits over the light, so the blaze is a hard-edged halo and the glyph keeps its contrast plate." },
        { "kind": "icon", "ability": "Essence Break", "verdict": "below",
          "caption": "<b>the neighbour</b> — the row is read as a whole, so the question is not whether this is loud but whether it makes the icon BESIDE it harder to read." },
        { "kind": "icon", "ability": "The Hunt", "verdict": "below", "treat": false,
          "caption": "<b>control</b> — the same icon untreated. A treatment that only reads beside its own caption has not read." }
      ]
    },

    "blaze-l9-corona": {
      "draws": "blaze",
      "behind": "corona",
      "sheet": "corona", "cols": 1, "rows": 1, "cell": 128, "frames": 1, "fps": 0,
      "title": "\"Press me!!!\" — the blaze as a RING around the badge",
      "asks": "The third way to light the same badge. L6 gave the light the flame's silhouette and L7 gave it the plate's hard disc; this gives it a ring with a dark centre, so the glyph sits in a hole rather than on a field. Does a corona read as *hot* the way a filled disc does, or does the dark middle just make the flame look unlit?",
      "sprite": "fire",
      "rgb": [1.00, 0.62, 0.12],
      "alpha": 0.95,
      "spread": 2.30,
      "glyph_rgb": [1.00, 1.00, 1.00],
      "period_s": 0.9,
      "rest_alpha": 0.55,
      "cells": [
        { "kind": "icon", "ability": "The Hunt", "verdict": "press",
          "caption": "<b>the ring</b> — Blizzard's <code>Artifacts-PerkRing-MainProc-Glow</code> at BADGE scale, augmenting the fire cue rather than replacing it." },
        { "kind": "icon", "ability": "Essence Break", "verdict": "below",
          "caption": "<b>the neighbour</b> — a ring overhangs further than a disc, so this is where the corner crowding shows." },
        { "kind": "icon", "ability": "The Hunt", "verdict": "below", "treat": false,
          "caption": "<b>control</b> — the same icon untreated." }
      ]
    },

    "blaze-l13-energy-badge": {
      "draws": "blaze",
      "behind": "sheet",
      "sheet": "energy", "cols": 8, "rows": 3, "cell": 64, "frames": 18, "fps": 12,
      "title": "\"Press me!!!\" — the energy burst BEHIND THE BADGE",
      "asks": "L11 puts this burst around the whole icon, where it competes with the art. At badge scale it augments the fire cue instead. Is 18 frames of motion legible in a 22px disc at all, or does a burst need room to be a burst?",
      "sprite": "fire",
      "rgb": [1.00, 0.62, 0.12],
      "alpha": 0.95,
      "spread": 2.60,
      "glyph_rgb": [1.00, 1.00, 1.00],
      "rest_alpha": 0.55,
      "cells": [
        { "kind": "icon", "ability": "The Hunt", "verdict": "press",
          "caption": "<b>burst, badge scale</b> — the same 18 frames as L11, sized to augment rather than replace." },
        { "kind": "icon", "ability": "Essence Break", "verdict": "below",
          "caption": "<b>the neighbour</b> — the widest spread of the badge family at 2.60x." },
        { "kind": "icon", "ability": "The Hunt", "verdict": "below", "treat": false,
          "caption": "<b>control</b> — the same icon untreated." }
      ]
    },

    "blaze-l14-sparkler-badge": {
      "draws": "blaze",
      "behind": "sheet",
      "sheet": "sparkler", "cols": 8, "rows": 4, "cell": 64, "frames": 32, "fps": 30,
      "title": "\"Press me!!!\" — the sparkler BEHIND THE BADGE, and it takes the lane's colour",
      "asks": "The only badge-scale field that is NEUTRAL art, so it is tinted rather than baked. Against L13 beside it, this asks the question the whole family is really for: is the heat doing the work, or the motion? If a gold-tinted sparkler reads as urgently as a baked fire burst, the vocabulary can keep its own colours.",
      "sprite": "fire",
      "rgb": [1.00, 0.78, 0.25],
      "alpha": 0.95,
      "spread": 2.60,
      "tint": "lane",
      "glyph_rgb": [1.00, 1.00, 1.00],
      "rest_alpha": 0.55,
      "cells": [
        { "kind": "icon", "ability": "The Hunt", "verdict": "press",
          "caption": "<b>sparkler, badge scale</b> — generated, neutral, tinted to the positives' gold. It could be any hue." },
        { "kind": "icon", "ability": "Essence Break", "verdict": "below",
          "caption": "<b>the neighbour</b> — a particle field throws light further than a ring does." },
        { "kind": "icon", "ability": "The Hunt", "verdict": "below", "treat": false,
          "caption": "<b>control</b> — the same icon untreated." }
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
