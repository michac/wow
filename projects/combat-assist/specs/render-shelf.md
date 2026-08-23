# Combat Assist Plus — the render shelf

**What this file is for:** how cap is allowed to *look*. `authoring.md`'s recipe index answers
**which facts you may use** and where the client evidence for each one lives; this answers **how
you may show them**. It owns every visual opinion in the
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
| **Scan edge** | a thin opaque line on the icon edge | one bit: the row is in the scan, or it is not | Static — nothing about it moves (V13). Drawn on cap's own frame, sized to the icon rect, so it needs no host scale-up and cannot reach a neighbour. |
| **Corner badge stack** | discs hung off the **top-right** corner, flowing **down** the right edge | one cue each, as many as the row wears | Filled circles at `tokens.badges.diameter_pct` of icon width, overhanging by `tokens.badges.overhang_px` (V5). The first badge always sits on the corner; further badges pack downward in `rank` order. **Polarity is carried by hue and glow, not by position** (V5). |
| **Hotkey text** | the icon's **top-left** corner | the key bound to this ability — nothing else | **Chrome, not a cue** (`spec.md` §3.8): it names the row and takes no part in the scan. One static outlined FontString on cap's own frame (V15), drawn from `tokens.hotkey`. Blank when the ability is unbound or reached only through a macro. It sits at the corner opposite the badge flow, so the two never negotiate a place. |
| **Cooldown swipe** | the radial dial | remaining time | Can be *restyled* without knowing the time (see V7). |
| **Count tile** | Blizzard's own aura count position | a sealed stack number | Client-owned; cap never learns the value. |
| **Independent bar** | anywhere on screen | one duration, large | Off-icon surface. |

⚠ **And they stack in one DECLARED order: an ELIMINATING mark draws over an INCLUDING one.**
Several of these surfaces sit on the same pixels — a scan edge saying *this row is in the read*
and a hatch saying *this row is out* are contradictory statements about one icon, and the reader
resolves the contradiction by whichever is on top. Until 2026-08-23 neither frame declared a
level, so the client resolved it by construction order: the yellow edge drew over the red hatch,
which is the wrong way round, and it was wrong by accident rather than by argument. The container
that carries an eliminating mark now sets its own frame level explicitly above the row's, so the
skip always wins the overlap. **Draw order across frames is decided by frame level, not by draw
layer**, so this cannot be expressed by choosing a layer and hoping.

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

### V5.1 · The cue vocabulary

The whole vocabulary. Each is a **single state** that either draws or does not — never a two-state
marker whose satisfied state happens to be invisible. `spec.md` §3.2 says *"a catalog form that
loads successfully and then renders nothing is a defect"*, and that test only keeps meaning if
"drew nothing" is unambiguously a bug rather than a legal second state.

| Cue | Polarity | Frames (`tokens.cues.<key>.frames`) | Loop | Rank | Means |
| --- | --- | --- | --- | --- | --- |
| **`priority`** | **positive** | `fire` (still — V14's ring is what moves) | `HOLD` | 1 | press this one — the scan would reach it late, or only after stepping over more skips than a reader can hold at once |
| **`capped`** | **positive** | `cards_stack → cards_stack_high` | `BOUNCE` | 2 | charges are at max and the recharge is stalled — you are losing one right now |
| **`blocked`** | negative | `timer_CW_50` (still) | `HOLD` | 3 | held for a cooldown, or a readable dependency says the press would be wasted |
| **`starved`** | negative | `flask_empty` (still) | `HOLD` | 4 | you cannot afford it |
| **`overcap`** | negative | `flask_full` (still) | `HOLD` | 5 | pressing would waste resource |
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

⚠ **Every negative is a STILL IMAGE, and motion is the third polarity carrier.** Until 2026-08-23
the negatives animated — `blocked` swept a clock through five frames, `starved` and `overcap`
bounced a flask — and frame cadence was declared the *shared* idiom of the vocabulary, carrying no
polarity. That was wrong, and the thing that proved it is **dwell time**. A positive cue is up for
the moment you are meant to act on; a negative is up for as long as the skip is true, which in a
real pull is most of the fight. Motion the eye cannot finish reading is motion it keeps returning
to, so a vocabulary whose *skips* move spends the player's attention on exactly the rows that
wanted none of it. Stillness is not a downgrade here — it is the correct rendering of "nothing is
happening on this row."

So the carriers run **hue, glow, motion**, and all three agree: gold + halo + animation says act,
red + still says skip. `priority` was already still by this logic before there was a rule for it
(V14's promotion ring is what moves), and `st_only` / `aoe_only` were still from the day they were
authored. This ruling generalises what those three were already doing rather than inventing
anything, and `capart check` gate **0e** enforces it — a negative cue declaring more than one frame
is a hard failure, because this is exactly the rule that decays back into prose the moment someone
adds a cue and copies the two-frame `BOUNCE` off a neighbour.

**It also removed a real collision.** `starved` bounced `flask_empty → flask_half` and `overcap`
bounced `flask_half → flask_full`, so the two cues **shared a frame**: at any instant either could
be showing the identical half-full flask, and the only way to tell "you cannot afford it" from
"pressing would waste it" was to watch which way the animation was travelling. Two negatives with
opposite meanings were distinguishable only over time. The stills — empty for starved, full for
overcap — are unambiguous in a glance, which is the only budget a corner badge has.

⚠ **Dropping `blocked` to one frame took `timer_CW_75` off the badge sheet, and V19 draws it.**
The pandemic badge names a sprite it does not ship, borrowing off the cue vocabulary's frame list;
nothing declared the borrow, so it would have silently stopped shipping — no missing file, no
failing gate, a corner of the overlay simply blank. `capart.BORROWED_FRAMES` declares it now, and
`export badges` prunes what the shelf no longer names.

**`capped` keeps its `BOUNCE`** and is now the only cue in the vocabulary whose glyph moves at all:
a thin stack growing to a full one, which is the loss it is warning about, drawn. It is positive,
it is up for as long as you are wasting a charge, and it is meant to be chased.

⚠ **The positive cues glow; no negative does.** This is the second polarity carrier, and with
position no longer carrying it (V5) the two that remain are load-bearing: a negative cue that
glowed, or one tinted gold, would be indistinguishable from a promotion. `tokens.cues.capped.glow` pulses a halo *behind* the glyph
between `alpha_min` and `alpha_max` at `hz`. The **glyph itself holds full alpha** — a cue that
faded would blink the fact it carries, which is exactly what the `tokens.text` flicker limits exist
to forbid, and those limits (`max_hz` 2.0) are the ceiling this rate sits under. The halo may
breathe; the information may not. The glow is what earns the extra attention impending loss needs
in peripheral vision, and since 2026-08-23 the frame bounce reinforces it rather than being house
style a negative also wore.

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

- **Opaque, at full brightness, on a restrained area.** `SetBlendMode(tokens.ready.blend)`, which
  reads `BLEND`. Perceived glow is roughly luminance × area: this keeps the luminance and spends
  the area, which is what lets `tokens.ready.alpha` sit at 1.00 without the row shouting.
  (`SetBlendMode`'s five values are Tier-1 — `frames-textures-animation.md` §5.2.)

  ⚠ **`ADD` was a correction, not a preference, and the shelf now declares the mode so it cannot
  be re-chosen in Lua.** Additive is destination + source, so it can only ever brighten toward
  white — and adding `rgb(1.00, 0.86, 0.45)` saturates red unconditionally, green above 0.14 and
  blue above 0.55. On any icon that is not near-black the line clipped to **WHITE**, measured on
  Demonology's purple roster `[client 2026-08-23]`. The colour declared three lines above this was
  not reaching a pixel. A blend mode that makes the authored hue undrawable is the thing that gives
  way, not the hue.
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
    t:SetBlendMode(T.ready.blend)
  end

  edge:SetShown(inScan)          -- the only in-combat write this primitive makes
  ```
  The in-combat surface is one `Show`/`Hide`. Everything else happens when the roster is bound.
- **Preview reproduction.** A 1-element `box-shadow: inset 0 0 0 var(--ready-line)` in
  `--ready-rgb` at `--ready-alpha`, composited `mix-blend-mode: var(--ready-blend)` — `capart` maps
  the client's mode to the CSS one (`BLEND` → `normal`, `ADD` → `plus-lighter`), so the preview
  cannot show a hue the client would clip. Same rect, same width, same colour, and nothing animates
  it there either.

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

### V16 · Banded count — a sealed number as a numeral, a mark, or both

**A secret aura application count reaches pixels through a rule cap authored and the client
alone evaluated.** cap builds a `C_StringUtil.CreateNumericRuleFormatter()`, hands it a rising
list of `{ threshold, format }` breakpoints, and passes it to `SetApplicationCount(fontString,
{ formatter = … })`. The client compares the secret against those thresholds and writes the
winning format into the FontString. **cap never receives the count, never compares it, and never
reads the text back** — which is why this is a display and not a read. Promoted out of the lab
2026-08-22 per Part 7 rule 4, out of `count_band` (L1), `count_polarity` (L2) and `count_mark`
(L5).

**A band is authored as MEANING, never as a format string.** A catalog picks from a closed
vocabulary and the shelf owns what each one resolves to:

| `draw` | What the client draws for a value in this band |
| --- | --- |
| `none` | nothing at all — the resting state, and the thing a bar cannot do |
| `count` | the number, while *how many more* is still the live question |
| `mark` | one badge — plate and glyph — once *how many more* has stopped mattering |
| `count+mark` | both, which the client accepts out of a single band |

plus `polarity`, which picks the hue (V5.1 — hue carries polarity and only polarity), and `hatch`,
which lays V11's stripe sheet across the face. `hatch` is the only item on that list that changes
the elimination walk: it says the row is **ruled out**, not decorated. The format strings are built
in `Channel.CountRules` out of `tokens.count`, and that is the only place pixels enter.

⚠ **`threshold` is the MINIMUM input a band applies to, so a value ON a threshold takes the
UPPER band.** Bands must be authored in rising order and the first must be `0`. Rising order is
*required* rather than sorted at build time: a table that does not rise is a table whose author
believed something false about what draws, and silently repairing it would hide that.

⚠ **ONE AURA CONTAINER SLOT PER ELEMENT, and this is a platform property rather than a trick.**
`AuraContainerAuraSlotManagerMixin:UpdateAura` offers **every aura to every slot** — it walks the
whole slot list with no consume — while `ShouldIncludeAuraInSlot` evaluates each slot's own
`filterString` `[T1 src @12.1.0: Blizzard_AuraContainer/Blizzard_AuraContainerSlots.lua —
UpdateAura, ShouldIncludeAuraInSlot]`. So several slots filtered to the same spell each take it
independently, each gets its own button, and each button takes its own count sink. The hatch, the
mark and the numeral are therefore **three FontStrings with three band tables**, each anchored
where it belongs — not three escapes crammed into one string. That erased the whole of the earlier
design: the ~96px advance run, the offset arithmetic, and the stacking rules were consequences of
forcing several statements through one string, not of the sink.

⚠ **Within one element, several escapes in one band is still the trick.** A band's `format` may
carry `|T…|t` / `|A:…|a` and it renders; the second and later ones take `:xoff:yoff` and are
*placed* rather than flowed. So one band can hatch the face and hang a badge on the corner, and
the band above the threshold clears both together — one client decision, several marks.

⚠ **A colour escape does not reach art** `[client 2026-08-22]`. `|cAARRGGBB…|r` tints the band's
**text** and leaves an inline `|T…|t` at full white — measured as an A/B against `SetVertexColor`
on the same stripe sheet, which came out correctly red two icons away. There is no texture object
to recolour either: the sink owns a FontString and the art inside it is named by a path. So every
mark names a **pre-tinted file** (`capart export count` generates one crop per hue) and only the
numeral is wrapped in an escape. The plate is deliberately *not* hue-varied — its job is contrast,
and contrast is not polarity.

⚠ **Motion comes free and is gated on nothing.** The sink adds `Text` and `Shown` to the
FontString and nothing else, so the animation channel is still cap's: a `Paint.Breathe` group
created at setup and looped forever is **invisible while the band draws nothing**, and the mark
arrives already breathing. There is no threshold in that anywhere — the client's own blank is the
gate. Part 3's one-motion-per-region rule still binds, so **only the mark breathes**, never the
hatch and never the numeral.

**The floor, if a later build starts sanitising markup.** `SetApplicationCount` seals `Text` and
`Shown` and never `VertexColor`, so one static hue set with `SetTextColor` at setup needs no markup
at all and cannot be stripped. That is already ours and it is what V16 degrades to, rather than to
nothing.

- **Lua:**
  ```lua
  -- One SLOT, one FontString, one band table — repeated per element (hatch / mark / count).
  local fs = button:CreateFontString(nil, "OVERLAY")
  fs:SetFont(T.count.font, T.count.size, T.count.outline)
  fs:SetPoint("CENTER", host, "TOPRIGHT", Paint.BadgeCentre())

  local formatter = C_StringUtil.CreateNumericRuleFormatter()
  formatter:SetBreakpoints(Channel.CountRules(plan.bands, T.count, size, element))
  button:SetApplicationCount(fs, { formatter = formatter })   -- the client owns Text + Shown

  -- Free, gated on nothing: invisible while the band is blank (the mark only — Part 3).
  if element == "mark" then Paint.Breathe(fs, T.count.pulse):Play() end
  ```
  cap makes the widget and the rule. Every in-combat write after this is the client's.
- **Preview reproduction.** `--count-size`, `--count-rgb`, `--count-low`, `--count-mark`,
  `--count-mark-x`, `--count-mark-y`, `--count-plate`, `--count-hatch`, and the breath as
  `--count-pulse-dur` / `--count-pulse-a0` / `--count-pulse-a1` / `--count-pulse-scale`. The
  preview draws the band the scenario declares, because it has no secret to evaluate against —
  which is the one thing the client does that a browser cannot.

### V17 · The complement — a row that rules ITSELF out below a threshold

**The same machinery, authored the other way round: the marks draw BELOW the threshold and the
band above clears them.** A row wearing this is ruled out until the count reaches the number the
catalog named, and at that number it goes clean and becomes a live candidate. Promoted out of the
lab 2026-08-22 per Part 7 rule 4, out of `count_complement` (L6).

**It is the third eliminating signal, and that is the whole novelty.** Until 2026-08-22 a row
could be eliminated by Blizzard's swipe or by cap's own negative badge, and both are things cap
either reads or decides. This one is neither: **the client evaluated cap's rule against a secret
and drew the hatch itself.** The reading model gained an eliminator that no Lua branch stands
behind.

⚠ **Its verdict is `ruled-sealed`, and it carries NO cue.** There is nothing for a cue key to
name — the hatch and the mark come out of a FontString the client writes, and a cue is a badge cap
shows. `tokens.verdicts["ruled-sealed"]` declares `eliminates: true` so that `capart check`'s
elimination gate counts it, which is what keeps the mostly-negative vocabulary safe: a scenario
whose press sits behind a self-ruled-out row must still lead the eye to the press.

**What it buys is the state a threshold cue could never say.** Implosion below six Wild Imps is
not *held*, not *unaffordable* and not *the wrong mode* — it is simply not worth pressing yet, on a
number nobody may read. Before this, that row drew nothing and the player was expected to count
imps. Its `blank at 6` band is the whole statement.

### V18 · Sealed radial — the same secret as a SHAPE

**`SetApplicationBar` drives a StatusBar from the sealed count, so the number becomes an arc
instead of a numeral.** cap creates the bar, its track, its fill and its size as ordinary setup
calls; the client sets the range from cap's own `maxApplications` and the value from the secret.
**Only `BarValue` is sealed** — the aspect goes on the value, not on the widget. Promoted out of
the lab 2026-08-22 per Part 7 rule 4, out of `count_bar` (L4).

**Radial is a RENDER MODE, not a mask.** `Enum.StatusBarRenderMode.Radial` gives a circular fill
with no `MaskTexture` anywhere, which is why the arc costs one texture and not a stencil. A client
that does not have the mode gets the linear fill rather than nothing: the value is the fact, and
the circle is only how it is drawn.

⚠ **A BAR HAS NO BLANK STATE, and this is the straight trade against V16.** `SetValue` clamps
into `[0, max]`, so at zero the **track still draws**. V16 can be silent and cannot be a shape;
V18 is a shape and is always on the row. That is why the track's colour and alpha are declared
rather than incidental — the track is what decides whether an empty arc reads as *nothing yet* or
as clutter, and it is on screen for every value the ability ever has.

**`max` is what turns "or more" into "full".** The clamp is the expression: a catalog that wants
*four Cores is everything* declares `max = 4`, and five Cores is a full circle rather than an
overflow cap has to detect.

⚠ **It ships no art at all** — the fill is a flat colour — so it is absent from Part 4's tint
guard subject list on purpose, not by omission.

- **Lua:**
  ```lua
  local bar = CreateFrame("StatusBar", nil, button)
  bar:SetPoint("TOPRIGHT", button, "TOPRIGHT", Paint.StackOffset(0))
  track:SetColorTexture(T.arc.track_rgb[1], T.arc.track_rgb[2], T.arc.track_rgb[3],
                        T.arc.track_alpha)          -- on screen at EVERY value, including zero
  fill:SetColorTexture(T.arc.rgb[1], T.arc.rgb[2], T.arc.rgb[3], T.arc.alpha)
  bar:SetStatusBarTexture(fill)
  pcall(bar.SetRenderMode, bar, Enum.StatusBarRenderMode.Radial)   -- linear if absent, not blank
  button:SetApplicationBar(bar, { maxApplications = plan.max })
  ```
- **Preview reproduction.** `--arc-inset`, `--arc-rgb`, `--arc-track`, `--arc-full`, drawn as a
  `conic-gradient` inside the badge plate.

### V19 · Refresh window — a badge the client alone shows and hides

**`AddPandemicRegion` takes any Region — a Frame with children included — seals its `Shown`, and
drives it off the client's own `GetRefreshExtendedDuration − GetAuraBaseDuration`, per spell.** So
a whole badge, plate and glyph together, appears and vanishes on Blizzard's real refresh window.
Promoted out of the lab 2026-08-22 per Part 7 rule 4, out of `pandemic_mark` (L3).

⚠ **It is the ONE sealed display cap authors no threshold for.** Every other form here makes cap
name a number — a breakpoint table, a curve break point — and every authored number is a thing to
get wrong. This one has none. It is also **Blizzard's real pandemic** rather than the community's
30 %, computed per spell by the code that owns the spell.

**A Frame, not a texture, and that is what makes it a badge.** The client seals `Shown` and
nothing else, so a plate and a sprite parented under the region appear and vanish together — the
same picture the cue vocabulary draws, out of a fact cap may not read. Its breath is gated for free
exactly as V16's is: the client hides the region, so a loop running forever on it is invisible
until the window opens.

⚠ **Two real costs.** It is the only sink carrying an `OnUpdate`, and Blizzard `secretwrap`s even
the **enablement** — whether cap's update loop runs would otherwise leak the aura's presence. So
**budget one per armed tile and never attach speculatively.**

- **Lua:**
  ```lua
  local region = CreateFrame("Frame", nil, button)   -- a FRAME, so plate + glyph travel together
  region:SetPoint("TOPRIGHT", button, "TOPRIGHT", Paint.StackOffset(0))
  -- …plate and sprite parented under `region`, from T.pandemic and T.badges.plate…
  Paint.Breathe(region, T.pandemic.pulse):Play()     -- invisible until the client shows it
  button:AddPandemicRegion(region)                   -- no threshold anywhere in this file
  ```
- **Preview reproduction.** `--pd-rgb`, `--pd-size`, and the breath as `--pd-pulse-dur` /
  `--pd-pulse-a0` / `--pd-pulse-a1`.
---

## Part 2.5 — Composing a row

The primitives above are drawn together, and the order they compose in is fixed. **A row is a
hatch, a scan edge, badges, and whatever sealed display it declares** — the icon face is not cap's
(Part 1), and nothing else takes part in the composition. Chrome sits beside that rather than inside it: the hotkey text (V15) holds a
corner no cue may claim, carries no condition, and so has nothing to stack with or against. The
rule below is about conditions competing for a surface, and a label is not a condition.

1. **The cooldown hatch** (V11), or none. It sits under everything else, directly over the icon
   face, because it is a statement about the button rather than a mark placed on it.
2. **The scan edge** (V13), or none. It is one bit and has nothing to stack with.
3. **A badge per cue** (V5/V5.1), each in the slot its cue owns. A cue named twice is one badge —
   that is how a catalog authors an OR without an OR.
4. **A sealed display** (V16–V19), or none. Its widgets are the client's to show, so cap places
   them and stops: a banded count takes the badge corner and the icon face, the radial takes the
   corner plate, the refresh badge takes the corner. **At most one per entry** — the three sinks
   all need an AuraContainer slot and a marker is at most one of them (`Channel.ContainerPlan`).

⚠ **An ELIMINATING mark draws over an INCLUDING one, and the frame level says so** (Part 1). The
sealed hatch and the scan edge occupy the same pixels and make opposite statements; the skip wins,
declared rather than left to construction order.

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

**V11's hatch is invisible to the elimination walk, by construction.** It is drawn exactly where
the swipe is drawn, so every row wearing it was already ruled out by *swiped* in pass 2 and no
reading changes. It adds emphasis to a decision the walk had already made — which is why
`elimination_gate` stays a two-term test over `swiped` and `wearing a negative badge`, and does not
learn about it.

⚠ **V17's hatch is the exception, and it is the one place a THIRD eliminator exists.** A row that
rules itself out on a sealed count was not swiped and wears no badge, so neither term of that test
covers it. Its verdict `ruled-sealed` declares `eliminates: true` and the gate reads that flag
explicitly. This is the only signal in the style that eliminates without cap having decided
anything — the client evaluated cap's rule against a secret and drew the mark itself.

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
started life guarding the flipbook rings; it now guards the badge sprites, V11's stripe sheet,
V14's promotion ring and the art V16 and V19 draw through the client's own sinks,
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
   nobody decodes" but "a line nobody notices". The louder and quieter candidates were deleted with
   the `ready-*` entries on 2026-08-19 rather than kept drawn beside the winner, so this is a
   question about the **shipped** treatment and there is nothing to A/B it against. If a lit row
   and an unlit row are hard to tell apart in a pull, the fix is **area, not a second colour** — a
   ladder is what V2 was retired for, and the blend is now spent (V13, 2026-08-23: `ADD` clipped
   the authored hue to white, so there is no headroom left on that axis).
3. **Do the badges read without a legend at 56 px?** Every negative is a still image since
   2026-08-23, which removed the version of this question that used to matter most — whether a
   sweeping clock read as *waiting* or as a countdown. What is left is the harder half: does a
   **motionless** red glyph in a corner get noticed at all in a pull, or does stillness cost the
   thing it was meant to buy?
4. **Does one shared red across five negative badges under-differentiate?** The shapes are meant to
   carry the distinction. If they do not, the fix is different shapes, not a second hue.
5. **Does elimination alone lead the eye where no positive cue fires?** Most rows wear no promotion,
   and for those the walk is the whole reading. The scenarios with something to the *left* of the
   press are the test. If a scenario is unreadable without a positive cue that its catalog cannot
   honestly declare, that is a finding about the walk rather than about the vocabulary.
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
    "_comment": "IN THE SCAN. One treatment, no roles, no motion. An icon either participates in the read or it does not; rank comes from row order and elimination, not from a hue ladder. Full brightness on a restrained AREA, drawn ON the icon rect so it can never bleed into a neighbour at any row gap. `blend` is NORMAL and that is a correction: under additive the edge could not carry the hue declared right here. Adding rgb(1.00, 0.86, 0.45) to a destination saturates red unconditionally, green above 0.14 and blue above 0.55, so on any icon that is not near-black the line clipped to WHITE — measured on Demonology's purple roster [client 2026-08-23]. The declared colour was not reaching a pixel, so the blend mode gave way rather than the colour.",
    "blend": "BLEND",
    "rgb": [
      1.0,
      0.86,
      0.45
    ],
    "alpha": 1.0,
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
    "from_scale": 2.0,
    "duration_s": 0.4,
    "smoothing": "OUT",
    "from_alpha": 0.0
  },
  "text": {
    "max_hz": 2.0,
    "duty": 0.7,
    "alpha_floor": 0.65
  },
  "badges": {
    "diameter_pct": 40,
    "overhang_px": 2,
    "padding_px": 3,
    "sprite_inset_pct": 16,
    "rgb": [
      0.95,
      0.3,
      0.3
    ],
    "tint": "shelf",
    "plate": {
      "rgb": [
        0.0,
        0.0,
        0.0
      ],
      "alpha": 0.78,
      "scale": 1.12
    },
    "halo_falloff": 0.7,
    "asset_root": "previews/assets/kenney",
    "flow": {
      "anchor": "top-right-corner",
      "direction": "down"
    }
  },
  "cues": {
    "blocked": {
      "means": "held for a cooldown, or a readable dependency says the press would be wasted",
      "polarity": "negative",
      "frames": [
        "timer_CW_50"
      ],
      "duration_s": 1.2,
      "loop": "HOLD",
      "rank": 3,
      "open": false,
      "budgeted": true
    },
    "starved": {
      "means": "you cannot afford it",
      "polarity": "negative",
      "frames": [
        "flask_empty"
      ],
      "duration_s": 1.2,
      "loop": "HOLD",
      "rank": 4,
      "open": false,
      "budgeted": false
    },
    "st_only": {
      "means": "the single-target spender, while AoE mode is on — the other one is the answer here",
      "polarity": "negative",
      "frames": [
        "pawn"
      ],
      "duration_s": 1.2,
      "loop": "HOLD",
      "rank": 6,
      "open": false,
      "budgeted": false
    },
    "aoe_only": {
      "means": "the AoE spender, in single target — the other one is the answer here",
      "polarity": "negative",
      "frames": [
        "pawns"
      ],
      "duration_s": 1.2,
      "loop": "HOLD",
      "rank": 7,
      "open": false,
      "budgeted": false
    },
    "overcap": {
      "means": "pressing would waste resource",
      "polarity": "negative",
      "frames": [
        "flask_full"
      ],
      "duration_s": 1.2,
      "loop": "HOLD",
      "rank": 5,
      "open": false,
      "budgeted": false
    },
    "capped": {
      "means": "charges are at max and the recharge is stalled — you are losing one right now",
      "polarity": "positive",
      "rgb": [
        1.0,
        0.78,
        0.25
      ],
      "glow": {
        "hz": 1.2,
        "alpha_min": 0.15,
        "alpha_max": 0.55,
        "scale": 1.55
      },
      "frames": [
        "cards_stack",
        "cards_stack_high"
      ],
      "duration_s": 1.2,
      "loop": "BOUNCE",
      "rank": 2,
      "open": false,
      "budgeted": false
    },
    "priority": {
      "means": "press this one — the scan would reach it late, or only after stepping over more skips than a reader can hold at once",
      "polarity": "positive",
      "rgb": [
        1.0,
        0.78,
        0.25
      ],
      "glow": {
        "hz": 1.2,
        "alpha_min": 0.15,
        "alpha_max": 0.55,
        "scale": 1.55
      },
      "frames": [
        "fire"
      ],
      "duration_s": 1.2,
      "loop": "HOLD",
      "rank": 1,
      "open": false,
      "budgeted": false
    }
  },
  "hatch": {
    "texture": "stripes",
    "tile_px": 128,
    "pitch_px": 16,
    "duty": 0.5,
    "direction": "down",
    "rgb": [
      0.0,
      0.0,
      0.0
    ],
    "alpha": 0.5,
    "phase_pct": 50,
    "tint": "shelf",
    "skip": {
      "rgb": [
        0.95,
        0.3,
        0.3
      ],
      "alpha": 0.45,
      "phase_pct": 0,
      "overhang_px": 2,
      "border": {
        "rgb": [
          0.95,
          0.3,
          0.3
        ],
        "alpha": 1.0,
        "line_px": 2
      }
    }
  },
  "promotion": {
    "texture": "procring",
    "cols": 8,
    "rows": 4,
    "cell": 64,
    "frames": 32,
    "fps": 30,
    "rgb": [
      1.0,
      0.82,
      0.27
    ],
    "alpha": 1.0,
    "spread": 2.0,
    "tint": "shelf"
  },
  "count": {
    "_comment": "V16/V17. A SEALED aura application count reaching a pixel. cap hands the Cooldown Manager a FontString and a NumericRuleFormatter it AUTHORED; the client evaluates the bands against the secret and calls SetText, and cap never learns which band fired. The sink seals `Text` and `Shown` and nothing else — which is why the hue below is reachable through a static SetTextColor as well as through a band's own escape, and why the FontString's animation channel is still cap's. `threshold` is the MINIMUM input a band applies to, so a value ON a threshold takes the UPPER band.",
    "font": "FRIZQT__.TTF",
    "size": 15,
    "outline": "OUTLINE",
    "rgb": [
      1.0,
      0.78,
      0.25
    ],
    "low_rgb": [
      0.95,
      0.3,
      0.3
    ],
    "mark": "cards_stack_high",
    "mark_px": 15,
    "mark_offset_px": [
      20,
      -18
    ],
    "plate_px": 25,
    "plate_offset_px": [
      20,
      -18
    ],
    "hatch_px": 56,
    "hatch_offset_px": [
      2,
      0
    ],
    "pulse": {
      "duration_s": 1.9,
      "alpha": [
        0.72,
        1.0
      ],
      "scale": 1.1
    },
    "tint": "shelf"
  },
  "arc": {
    "_comment": "V18. The same sealed number as a SHAPE. SetApplicationBar drives a StatusBar from the count and SetDurationBar from the remaining duration; only the VALUE is sealed, so texture, size, orientation and colour stay ordinary setup calls. Radial is a RENDER MODE (Enum.StatusBarRenderMode.Radial), not a masked fill, so the circle needs no MaskTexture. ⚠ A bar has NO BLANK STATE: SetValue clamps into [0, max], so at zero the track still draws. That is the straight trade against V16, which can be silent and cannot be a shape. It ships no art at all — the fill is a flat colour — so it is absent from the tint guard's subject list on purpose.",
    "inset_px": 3,
    "rgb": [
      1.0,
      1.0,
      1.0
    ],
    "alpha": 0.85,
    "track_rgb": [
      0.0,
      0.0,
      0.0
    ],
    "track_alpha": 0.55,
    "full_rgb": [
      1.0,
      0.78,
      0.25
    ]
  },
  "pandemic": {
    "_comment": "V19. The refresh window, which is the ONE sealed display cap authors no threshold for: AddPandemicRegion takes any Region — a Frame with children included — seals its `Shown`, and drives it off the client's own GetRefreshExtendedDuration - GetAuraBaseDuration, per spell. So the whole badge, plate and sprite together, appears and vanishes on Blizzard's real window. ⚠ It carries an OnUpdate and Blizzard secretwraps even the enablement, so budget one per armed tile and do not attach speculatively.",
    "frame": "timer_CW_75",
    "size_px": 15,
    "rgb": [
      1.0,
      0.78,
      0.25
    ],
    "pulse": {
      "duration_s": 1.6,
      "alpha": [
        0.62,
        1.0
      ]
    },
    "tint": "shelf"
  },
  "hotkey": {
    "_comment": "V15. CHROME, not a cue (spec.md §3.8): it names the row and asserts nothing about the press. No polarity, no rank, no badge slot, no motion — and deliberately NO `tint` key, because Part 4's tint guard scans art and this has none. `font` is a FULL CLIENT PATH, not a filename: this is cap's OWN shipped file, exported from tokens.preview.hotkey_font, which is the only third-party asset the addon redistributes. `outline` is a client FONT FLAG and the only dark edge cap can ask for: OUTLINE or THICKOUTLINE, nothing between them and nothing wider. Blank when the ability is unbound or reached only through a macro; never a placeholder.",
    "font": "Interface\\AddOns\\CombatAssistPlus\\Media\\fonts\\CapKeyMono.ttf",
    "size": 16,
    "outline": "THICKOUTLINE",
    "rgb": [
      0.92,
      0.92,
      0.9
    ],
    "alpha": 0.85,
    "anchor": "TOPLEFT",
    "offset": {
      "x": 2,
      "y": -2
    }
  },
  "preview": {
    "_comment": "NOT THE STYLE, and structurally incapable of becoming it: `preview` is in capart.NOT_THE_STYLE, so nothing here can reach Style.lua. It exists so the previews can draw a keybind hint before one exists in the game — the point of V15's preview is judging how the text sits in the corner, and that cannot be judged against an empty string. The strings are what `Binds.Shorten` PRODUCES, not what the client hands it: lowercase modifier letters closed up against the key (the client's own `SHIFT_KEY_TEXT_ABBR` is `s`), and `M4`/`N5` where the client would say `Mouse Button 4`/`Num Pad 5`.",
    "hotkeys": [
      "3",
      "s2",
      "M4",
      "csF1",
      "1",
      "4",
      "sE",
      "M5",
      "2",
      "a3",
      "5",
      "s4",
      "c1",
      "M3",
      "sF",
      "6",
      "asQ",
      "MU"
    ],
    "hotkey_outline_rgb": [
      0.0,
      0.0,
      0.0
    ],
    "hotkey_outline_px": 2,
    "hotkey_font": {
      "_comment": "The font V15 draws with, and the ONE third-party asset cap redistributes. The preview embeds this exact subset and the addon ships this exact subset, so the page and the game measure the same advance widths. `ship_as` is not a preference: the upstream family carries the Reserved Font Name 'Share', a subset is a Modified Version, and OFL 1.1 clause 3 forbids a Modified Version from using it — so the shipped file is renamed and `license_url` travels beside it.",
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
      "rgb": [
        0.55,
        0.82,
        1.0
      ],
      "size_px": 13,
      "line_px": 2,
      "overhang_px": 2,
      "corner": "bottom-left"
    },
    "unsure": {
      "_comment": "PREVIEW ONLY. The loud treatment for an `⚠ UNSURE` annotation under a row — a claim the authoring docs themselves doubt, drawn so it cannot be read past. Amber block, not a grey footnote. It says nothing about the press and takes no part in either reading pass; it is a note to the author about the DOC, not a mark on the button.",
      "rgb": [
        1.0,
        0.74,
        0.3
      ],
      "bg_rgb": [
        0.23,
        0.17,
        0.06
      ],
      "line_px": 2
    }
  },
  "panel": {
    "icon_px": 50,
    "gap_px": 6,
    "anchor": "BOTTOM",
    "x": 0,
    "y": 190,
    "grow": "RIGHT"
  },
  "verdicts": {
    "cd": {
      "scan": false,
      "swipe": true,
      "hatch": true,
      "cues": []
    },
    "weave": {
      "scan": true,
      "swipe": false,
      "cues": []
    },
    "hold-readable": {
      "scan": true,
      "swipe": false,
      "cues": [
        "blocked"
      ]
    },
    "hold-sealed": {
      "scan": true,
      "swipe": false,
      "cues": [
        "blocked"
      ]
    },
    "ruled-sealed": {
      "_comment": "V17. The row is RULED OUT by a sealed count band — the client evaluated cap's own rule against a secret and drew the hatch and the mark itself. It carries no `cues` because there is no cue: the marks come out of one FontString the client writes, and a cue is a badge cap shows. It eliminates anyway, which is the whole novelty — this is the first eliminating signal that is neither Blizzard's swipe nor cap's own badge.",
      "scan": true,
      "swipe": false,
      "eliminates": true,
      "cues": []
    },
    "starved": {
      "scan": true,
      "swipe": false,
      "cues": [
        "starved"
      ]
    },
    "overcap": {
      "scan": true,
      "swipe": false,
      "cues": [
        "overcap"
      ]
    },
    "off-mode": {
      "scan": true,
      "swipe": false,
      "cues": []
    },
    "press": {
      "scan": true,
      "swipe": false,
      "cues": []
    },
    "press-promoted": {
      "scan": true,
      "swipe": false,
      "cues": []
    },
    "below": {
      "scan": true,
      "swipe": false,
      "cues": []
    }
  },
  "surfaces": {
    "icon_px": 56,
    "row_gap_px": 6,
    "border_px": 1,
    "swipe": {
      "color": [
        0.0,
        0.0,
        0.0
      ],
      "alpha": 0.72
    },
    "count_tile": {
      "font": "FRIZQT__.TTF",
      "size": 14,
      "outline": "OUTLINE"
    },
    "proc_glow_alpha": 0.5
  },
  "assets": {
    "icon_size": 56,
    "encode": "webp",
    "quality": 90
  },
  "budget": {
    "max_base64_kb": 300
  },
  "lab": {
    "_comment": "NO AUTHORITY. Part 7. Nothing in `verdicts` or `cues` may name anything in here; capart enforces it. A treatment leaves the lab by being MOVED into Parts 1-6, never by being cited from there. A new idea gets a `lab` key, an `asks`, and a section in Part 7. ⚠ ONE entry since 2026-08-22, and it is the leftover of an eight-entry intake whose other seven were promoted (V16-V19) or deleted. `duration_band` bands a CLOCK rather than a count, which is why no composite needed it and why it did not go with them. Its cells draw the `RemainingPercent` route, which is a SOURCE READ and has never been flown \u2014 the flown route (a bare `textFormatter`) gives thresholds in seconds. So every percentage in it is a proposal about a mechanism, clearly labelled, exactly as `count_bar` was before its flight settled it.",
    "duration_band": {
      "title": "L7 · duration_band — the same bands, on the DoT's CLOCK instead of a count",
      "asks": "`SetDurationText` takes a `textFormatter` of type NumericFormatter — the same object the count sink takes — bound to a DurationTextBindingProperty such as RemainingPercent. If a rule formatter is accepted there, every band shape L5 and L6 draw becomes available on a DoT's remaining time, INCLUDING the inversion `AddPandemicRegion` structurally cannot express. What does that cost, and is it worth authoring the threshold the pandemic sink computes for you?",
      "draws": "duration",
      "form": "S12",
      "flown": "2026-08-21",
      "size_px": 15,
      "rgb": [
        0.45,
        0.86,
        0.85
      ],
      "alt_rgb": [
        0.95,
        0.3,
        0.3
      ],
      "pulse": {
        "duration_s": 1.9,
        "alpha": [
          0.72,
          1.0
        ],
        "scale": 1.1
      },
      "cells": [
        {
          "ability": "Immolation Aura",
          "verdict": "below",
          "remaining_pct": 80,
          "place": "centre",
          "bands": [
            {
              "threshold": 0,
              "format": "%d"
            }
          ],
          "caption": "<b>control — the sink's own job</b>. `SetDurationText` normally draws a countdown, and with no rule it is Blizzard's seconds formatter. Everything to the right replaces that text with a rule cap wrote."
        },
        {
          "ability": "Immolation Aura",
          "verdict": "below",
          "remaining_pct": 20,
          "place": "badge",
          "composited": true,
          "bands": [
            {
              "threshold": 0,
              "format": "|A:timer_CW_75:15:15|a"
            },
            {
              "threshold": 31,
              "format": ""
            }
          ],
          "caption": "<b>the pandemic mark, re-created</b> — a mark only in the last 30 %. Same picture as L3's badge, and ⚠ NOT the same fact: this threshold is cap's guess, where L3's is the client computing `GetRefreshExtendedDuration − GetAuraBaseDuration` per spell."
        },
        {
          "ability": "Immolation Aura",
          "verdict": "below",
          "remaining_pct": 80,
          "place": "badge",
          "composited": true,
          "bands": [
            {
              "threshold": 0,
              "format": "|A:timer_CW_75:15:15|a"
            },
            {
              "threshold": 31,
              "format": ""
            }
          ],
          "caption": "<b>the same rule, early in the DoT</b> — clear, because 80 % takes the upper band. The pair to its left is the whole of L3's behaviour reproduced out of two breakpoints."
        },
        {
          "ability": "Immolation Aura",
          "verdict": "below",
          "remaining_pct": 80,
          "place": "badge",
          "bands": [
            {
              "threshold": 0,
              "format": ""
            },
            {
              "threshold": 31,
              "format": "|TInterface/AddOns/CombatAssistPlus/Media/stripes:56:56|t"
            }
          ],
          "caption": "<b>THE INVERSION</b> — hatched while there is plenty left, which is `do not refresh yet`. This is the direction `AddPandemicRegion` cannot express at all: it calls `SetShown(inWindow)` with no rule to flip."
        },
        {
          "ability": "Immolation Aura",
          "verdict": "press",
          "remaining_pct": 20,
          "place": "badge",
          "bands": [
            {
              "threshold": 0,
              "format": ""
            },
            {
              "threshold": 31,
              "format": "|TInterface/AddOns/CombatAssistPlus/Media/stripes:56:56|t"
            }
          ],
          "caption": "<b>the inversion, refreshable</b> — the hatch clears as the DoT enters the last 30 %, so the row becomes a live candidate exactly when refreshing it stops clipping. Read it against the cell to its left."
        },
        {
          "ability": "Immolation Aura",
          "verdict": "below",
          "remaining_pct": 80,
          "place": "badge",
          "composited": true,
          "alt_hue": true,
          "bands": [
            {
              "threshold": 0,
              "format": ""
            },
            {
              "threshold": 31,
              "format": "|TInterface/AddOns/CombatAssistPlus/Media/stripes:56:56|t|A:timer_CW_75:15:15:20:-18|a"
            }
          ],
          "caption": "<b>hatch and badge, inverted</b> — two escapes, one band, the second offset onto the corner. Identical machinery to L6's imp shape; the only difference is which sealed number the client feeds the formatter."
        },
        {
          "ability": "Immolation Aura",
          "verdict": "below",
          "remaining_pct": 45,
          "place": "badge",
          "composited": true,
          "bands": [
            {
              "threshold": 0,
              "format": "|A:timer_CW_75:15:15|a"
            },
            {
              "threshold": 31,
              "format": ""
            },
            {
              "threshold": 61,
              "format": "|TInterface/AddOns/CombatAssistPlus/Media/stripes:56:56|t"
            }
          ],
          "caption": "<b>three bands, mid-DoT</b> — hatched above 60 %, SILENT between 30 and 60, marked below 30. The quiet middle is the shape only a band table can draw: neither `do not` nor `now`, which is most of a DoT's life."
        }
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

**The lab was empty from 2026-08-19 until 2026-08-20**, when eight entries were added at once —
the first *capability* questions the lab had ever held. Seven of them left on 2026-08-22: **six
were promoted into four primitives** (V16–V19 — three of them fold into V16 alone) and one,
`composites`, was deleted as an argument its subject had overtaken. **One remains**, and an
empty-or-nearly-empty lab means every idea drawn here has been adopted or answered, not that
nobody is trying anything.

⚠ **That intake was a different KIND of entry from most of the ledger below, and the difference
matters.** Almost every earlier entry was a *taste* question — five fonts, three stripe phases,
four glows — and the preview settled it by drawing them side by side. Those eight were
**capability** questions: they asked whether the client would honour a rule cap authored against a
secret. **Rule 2 already says a preview cannot answer that** ("a preview is an argument about the
client; the gallery is the client"), and here even the gallery cannot, because the gallery draws on
cap-owned frames with no secret in sight. So a capability entry **graduates on a flight, not on
being looked at** — and once the flight has answered *will this work at all*, what is left is a
look question and the entry starts drawing cells again.

⚠ **The 2026-08-22 promotion taught the one thing worth carrying forward: nothing new was learned
about the client to make it possible.** Every measurement was in hand on 2026-08-21. What was in
the way was rule 1 — a catalog may not cite a lab entry — so the fact was expressible and unusable
at the same time. **Promotion is a pipeline step, and it was the entire cost.** Budget it as work,
not as paperwork.

### L7 · `duration_band` — the same bands, on the DoT's CLOCK instead of a count

**Asks:** `SetDurationText` takes a `textFormatter` of type `NumericFormatter` — the same object
the count sink takes — bound to a `DurationTextBindingProperty` such as `RemainingPercent`. If a
rule formatter is accepted there, every band shape V16 and V17 draw becomes available on a DoT's
**remaining time**, including the inversion `AddPandemicRegion` structurally cannot express. What
does that cost, and is it worth authoring the threshold the pandemic sink computes for you?

**It survived the promotion because no composite needed it**, not because it lost. V16–V19 all
band a *count*; this bands a *clock*, and no built spec has yet wanted one badly enough to pay for
it. Havoc's `buff.demonsurge.remains < gcd.max` is the nearest real subject.

⚠ **Its open half is a route, not a look.** `SetDurationText` reached through a bare
`textFormatter` gives thresholds in **SECONDS**, measured `[client 2026-08-21]`. The
`RemainingPercent` route — via `options.textFormat`'s `{property, formatter}` components, which is
what the cells below draw — is **source-read only** and has never been flown. Every percentage in
this entry is therefore a proposal about a mechanism, and the entry says so rather than quietly
drawing what it hopes for.

⚠ **The duration sink seals MORE than the count sink does, and it costs the free motion.**
`SetApplicationCount` adds `Text` and `Shown`, which is what leaves V16's animation channel in
cap's hands. `SetDurationText` adds `Text`, **`Alpha`** and **`VertexColor`** — so an alpha
animation cannot run on a FontString whose `Alpha` the client owns. **No cell here pulses, and
that is not an oversight.** What cap gets instead is `SetTextColorCurve`, bound to the same clock:
colour that moves with the remaining time rather than a breath the sink would overwrite. That
asymmetry is the strongest argument against assuming the two sinks are interchangeable just
because they take the same formatter object.

**What the cells are for.** The three that matter are the last three: the **inversion** — hatched
while there is plenty of DoT left, clearing as it enters the refresh window — and the **quiet
middle**, three bands where the row says neither *do not* nor *now* for most of the DoT's life.
V19 cannot express either. It calls `SetShown(inWindow)` and has no rule to flip, which is the
straight trade against it authoring no threshold at all: `AddPandemicRegion` is right for free and
cannot be asked a different question.
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
| `count_band` (L1), `count_polarity` (L2), `count_mark` (L5) | 2026-08-22 | → **V16**, the banded count and its mark, with `tokens.count`. L5's composited crop won: put the plate inside the art the escape names so the whole badge rides the band, where L1's `place: "badge"` cells left an empty disc at every resting value. L2's hue question came with it — per-band escape, static floor, or no hue at all — and V16 answers it by spending hue only on polarity, which is V5.1's rule rather than a new one. |
| `count_complement` (L6) | 2026-08-22 | → **V17**. It is the same sink as V16 and it is a separate primitive because it is a separate *statement*: the row rules ITSELF out, which made a sealed fact the third eliminating signal and forced `capart check`'s elimination gate to learn about it. |
| `count_bar` (L4) | 2026-08-22 | → **V18**, `tokens.arc`. Its cells had been drawn as an explicitly-labelled proposal off a source read; the flight settled it. What promotion added is the honest half — a bar has no blank state, so the track is declared rather than incidental. |
| `pandemic_mark` (L3) | 2026-08-22 | → **V19**, `tokens.pandemic`. The only sealed display cap authors no threshold for, and the only one whose cost is a per-tile `OnUpdate`. |
| `composites` (L8) | 2026-08-22 | **Deleted, not promoted.** It was the argument that the four above compose on one row — three whole Demonology scenarios built out of them. Once Demonology was built its subject became a real spec's walk, drawn by `demonology-stepper.html` against a shipped catalog. An argument that has been overtaken by the thing it argued for is not an experiment. |
| `hotkey-l1` … `hotkey-l10` | 2026-08-19 | **V15**'s font, size and dark edge were chosen out of this set of ten — five faces, then a plate, then a title bar. The winner is `tokens.hotkey`; what the losers cost is written into V15 itself, which is the point of promotion rather than citation. |

⚠ **A deleted entry is not a refuted one.** Nothing in this table is a claim that the treatment
was bad — most of them lost to something, and one or two were simply asking about a primitive that
no longer exists. `git log` holds every one of them with its `asks` intact, which is where a
revived idea should be read from. Re-adding one is cheap: a `lab` key, an `asks`, and a section
here.
