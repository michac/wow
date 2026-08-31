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
in this file cites a token path (`tokens.badges.diameter_pct`) and never restates its value, because
a number written twice is a number that will disagree with itself. `wowkb.capart` parses the block
for the preview and **generates the addon's `Style.lua` from it** — the two sides of the promise
above cannot drift, because neither transcribes anything by hand.

**Where the vocabulary is.** In **`spec.md` §1**, once. Every word this file leans on — surface,
primitive, treatment, mechanism, cue, verdict, scan membership, elimination, readable, sealed, slot
— is defined there and nowhere else. A second glossary here that cited that one would still be two
glossaries.

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
           · anything the CLIENT has hatched, having evaluated a band this
             catalog authored against a value cap never saw
         press the first item that survives.
```

**The procedure is the authority.** Where a treatment below and the two passes disagree, the passes
win and the treatment is what gets edited. Two things moved to match it:

**What the procedure ruled out — the `withheld` verdict, now deleted.** A verdict may only be
*drawn* from a fact cap is allowed to read. `withheld` — a dim with no badge — was the one
verdict in the vocabulary that broke this: its only driver was that a readable fact came back
**secret**, so the refusal itself became a visible elimination. Pass 2 makes that obviously wrong —
an item cap cannot form an opinion about is an item the scan should simply *reach*, not one it
should skip. The vocabulary is five verdicts, and a row cap has no opinion about draws whatever its
readable state says: the scan edge, or the swipe, and no badge.

**And `isActive` removed its last subject anyway.** `withheld`'s only user was a charge count read
below full. `C_Spell.GetSpellCharges` seals per member: `isActive` is `NeverSecret` and stays plain
in restricted combat, so "at max charges" is readable in **both** polarities — `false` at 2/2,
`true` below it. There is nothing left for the verdict to mean.

Two consequences the style is built on:

1. **The press is not a thing cap draws.** `press` and `open` render identically — the scan
   edge, nothing else. The press is *whatever the scan reaches first*. Cap's
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
for being honest about Holy Power. **`building` is not budgeted for the same reason read the
other way** (2026-08-24): a ramp's holds are ONE fact — the resource is below the window's
number — worn by a block of adjacent rows at once, and the player is reading that resource off
their own bar the whole time. Five `building` badges are one statement with five subjects, not
five claims to interpret; hatching the whole cooldown sequence while it waits is the reading
Demonology's pilot chose over a promotion, and the gate stays open to revisit after it flies
(`demonology/catalog.md`, changelog 2026-08-24). `noproc` is likewise unbudgeted — the proc's
absence is on the icon already (no glow); the badge names it rather than claims it.

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
| **Icon face** | the art itself | nothing — cap draws no treatment here | **The icon face is Blizzard's and cap draws nothing on it.** The client already writes two signals here and they say different things: **desaturation means ON COOLDOWN and nothing else** (`cooldownDesaturated` is the literal `false` or `self.isOnActualCooldown` at every assignment), while **usability is a vertex-colour tint** re-applied continuously off `SPELL_UPDATE_USABLE` — the built-in "you cannot cast this" channel (`cooldown-manager.md` §3.4). Reading a greyed icon as *unusable* imports a meaning the client does not put there, and a fragment- or aura-gated ability is tinted but never swiped or desaturated. cap draws neither: a second usability channel would restate a signal the player already has, and cap's own eliminating statements go on the badge stack and the hatch instead. |
| **Scan edge** | a thin opaque line on the icon edge | one bit: the row is in the scan, or it is not | Static — nothing about it moves (V13). Drawn on cap's own frame, sized to the icon rect, so it needs no host scale-up and cannot reach a neighbour. |
| **Corner badge stack** | discs hung off the **top-right** corner, flowing **down** the right edge | one cue each, as many as the row wears | Filled circles at `tokens.badges.diameter_pct` of icon width, overhanging by `tokens.badges.overhang_px` (V5). The first badge always sits on the corner; further badges pack downward in `rank` order. **Polarity is carried by hue and glow, not by position** (V5). |
| **Hotkey text** | the icon's **top-left** corner | the key bound to this ability — nothing else | **Chrome, not a cue** (`spec.md` §3.8): it names the row and takes no part in the scan. One static outlined FontString on cap's own frame (V15), drawn from `tokens.hotkey`. Blank when the ability is unbound or reached only through a macro. It sits at the corner opposite the badge flow, so the two never negotiate a place. |
| **Cooldown swipe** | the radial dial | remaining time | Can be *restyled* without knowing the time (see V7). |
| **Count tile** | Blizzard's own aura count position | a sealed stack number | Client-owned; cap never learns the value. |
| **Independent bar** | anywhere on screen | one duration, large | Off-icon surface. |

⚠ **Two of these surfaces make CONTRADICTORY statements about one icon, and nothing arbitrates
them.** A scan edge says *this row is in the read*; cap's half of V11 says *this row is out*. A
row wearing a negative cue wears **both** — the verdicts carrying `blocked` are `scan: true`, and
V11 generalises over polarity — so the contradiction is the normal case, not an edge case.

**GEOMETRY separates them and ORDER arbitrates them, and until 2026-08-29 only the first was
declared.** `Paint.Hatch` draws cap's half `overhang_px` OUTSIDE the icon rect, so its red *ring*
sits around the yellow scan edge rather than on it — the two rings are adjacent, red at −2 and
yellow at 0. But the red *stripes* start at 0 and run inward, so the pixels the yellow line
occupies are shared, and nothing said who won them: neither `Paint.Border` nor `Paint.Hatch`
called `SetFrameLevel`, and the stripe texture sat on the row's own frame while the scan edge was
a child frame of it — which a child frame beats regardless of draw layer.

**The ruling: cap's half draws OVER the scan edge** (`Paint.Z.edge` = 1 < `Paint.Z.skip` = 2, both
declared). An eliminating mark is the later word than *this row is in the read*, and this is the
rule the shelf already held everywhere else — `Channel.Arm` lifts the client's own sealed hatch
above the edge for exactly this reason, and cap's own hatch was the one layer left behind. The
asymmetry, not the ordering, was the defect: the same row read one way in the client (creation
order happened to put the red ring on top) and the other way in the preview (DOM order put the
yellow line on top of the stripes). Two answers to a question nobody had asked is what an
undeclared order buys.

**And the yellow is then GONE, not muted** (2026-08-29). Ordering alone left it dulled under the
stripes and muddy where a stripe crossed it — which is a third thing, neither *in* nor *out*. So
cap's outline moved from the overhung rect onto the **icon rect**: the same sheet at the same place
as V13's edge, in the skip ink, opaque. A ruled-out row wears one outline and it is red. What still
overhangs is the STRIPES, which is the part that reads as the hatch spilling past the button.

This is the second candidate — *suppress the scan edge on a row wearing a negative cue* — reached
by COVERING rather than by not drawing, and that difference is the whole reason it is safe.
`Treatment.For` still sets `scan = member`, membership is still ready-self, and the edge still
means exactly what it meant on every row in every spec. Nothing about the model moved; one layer
draws over another. Suppression proper would have changed what the edge *means*, which an ordering
complaint does not authorise.

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

**The headings are a registry, and it lives in `render-primitives.json`.** Each `### Vn ·` below
has an entry there carrying the same name and one of five **kinds** — `primitive` (a drawing
element cap builds), `mechanism` (*how* a secret reaches a pixel; a primitive is built on one),
`platform` (Blizzard draws it, cap leaves it alone), `declared` (specified, not built) and
`retired` (gone, and kept so a citation to it fails loudly). `capart check` gates the two against
each other in both directions, name included.

The kinds exist because the **numbering is invention order, not identity** — V14 sits between V11
and V12 here — and because a catalog state's `drawn_by` has to name something a reader can *see*.
So `drawn_by` accepts `kind: "primitive"` and nothing else: `drawn_by: ["V9"]` would name the
sealed colour curve, which is a mechanism and draws no pixel of its own.

⚠ **V5.1 is not in the registry.** It is the cue *vocabulary* — what may be said — and V5 is the
one primitive that draws every member of it. A vocabulary is not a thing that draws.

**Authority markers.** A recipe below mixes three kinds of sentence, and a reader deciding whether
they may change something needs to know which one they are looking at:

| Marker | Means |
| --- | --- |
| `[platform]` | A measured client fact, carrying its `[client …]` / `[T1 …]` citation. Argue with the client, not with the shelf. |
| `[gated]` | An invariant a gate in `wowkb.capart` fails on, and the marker **names the gate**. |
| *unmarked* | The current choice, with its reason. **This is the default and it means "not a wall."** |

⚠ Nothing is `[gated]` unless you can name the gate. The convention is applied in **V21's section
only** so far — retro-marking the rest is its own job, and half-marked prose that looks complete
would be worse than none.

### V1 · Emphasis ring *(retired)*

The animated flipbook emphasis ring — a `visualalert_ants_flipbook` glow outside the icon edge,
tinted to the lane and pulsed forever. Retired 2026-08-13 in favour of V2's solid border plus the
arrival snap: a row of continuously-glowing rings reads as candles, and CDMProbe measured that
**60 % of real cue-set changes are swaps**, so continuous motion spends its budget on states that
are about to be replaced. The measurement that made the ants sheet the only usable ring — its
neutral saturation — is still true and is kept in `render-rationale.md`; it is simply no longer
load-bearing here.

### V2 · Lane border *(retired)*

The lane border — a solid rectangular edge in one of **four hues** (COOLDOWN, ROTATION, FALLBACK,
and CHARGES substituted in off a client charge read), drawn from a generated 16-frame ring flipbook
that played once as a one-shot **arrival snap** when the drawn lane changed. Retired 2026-08-19 in
favour of **V13**, one binary scan edge: the hue ladder had become an informational hint nobody was
reading off, and priority is carried by **left-to-right scan order plus the
overlays**, not by colour. A fourth hue that *replaced* the role lane made that worse rather than
better — it spent the one channel the ladder had on a fact (this ability has charges) the badge
vocabulary already carries.

**What survives, and where it went.** The role tiers COOLDOWN / ROTATION / FALLBACK outlived
their paint by six days and left the model on 2026-08-25: membership is now a boolean
(`scan_when`, default ready-self) in `spec.md` §3.1, `Catalog.TIERS` is deleted, and the
catalogs' grouping is prose. While they lasted, the tiers decided only *whether* a row was
in the scan — which is why a boolean replaced them without a pixel moving. The `charged` flag stays authored
in the catalogs and read by the engine; nothing draws from it. `Paint.Border` stopped creating an
`AnimationGroup`, walking a sheet or owning a rate limiter the day V2 retired.

⚠ **The arrival machinery is gone entirely as of 2026-08-25**, and the reason is that the
justification for keeping it had been refuted by this file's own Part 7 ledger. It stayed declared
and on the ship path *"because Part 7's `arrival-*` entries are still about it"* — but Part 7
recorded those entries as **"Deleted with their subject" on 2026-08-19**, six days earlier. So the
sheet, its cadence, `tokens.ring` / `tokens.arrival` / `tokens.motion`, `Media/ring.tga`,
`capart export ring` and the `frames × tick == duration` gate all went together, along with
`Paint.Arrival` and the gallery tab that drew them. The generated sheet's neutral-saturation
measurement, and the argument for a flipbook over a `Scale` animation, are kept in
`render-rationale.md`, which is where a treatment's reasoning outlives its code.

### V3 · Lane pulse *(retired)*

The lane pulse — three unequal rates driving the V1 ring's alpha, with a trough-invariant floor and
a per-icon phase offset. Retired with V1: there is no continuous motion left in the style to pace.
The arithmetic behind it (the trough invariant, the unequal-rate argument, the WCAG phase-offset
note) is kept in `render-rationale.md` because the *measurements* stay true and would have to be
re-derived if continuous motion ever came back.

**What survives:** the sealed-**text** flicker limits, which were never about the ring. They are
MIL-STD-1472F / WCAG constraints on blinking legends and they bind any text cue cap ever draws.
They now live at `tokens.text.max_hz` / `.duty` / `.alpha_floor` (see V8).

### V4 · Veil *(retired)*

The veil — a flat dim over the icon face on every row cap had an opinion against. Retired
2026-08-16: **every** skip condition cap has (a readable hold, a sealed hold, `starved`, `overcap`
and both graded curves) expressed itself by dimming the *same* texture, on top of Blizzard's own
desaturation and swipe, so a dark row in flight was the sum of an unknown number of causes and no
one could see which fired. It was also strictly redundant — Part 2.5 *derived* it from cue
polarity, so it never carried a fact the badge beside it was not already carrying. Nothing replaces
it: a skipped row is now the scan edge, a red badge, and whatever Blizzard is already drawing.

### V5 · Corner badge

The general answer to "a non-numeric cue needs a texture that catches the eye at 56 px."
Windows/mobile notification-badge convention: a filled circular disc hung off the icon's
**top-right** corner, overhanging by `tokens.badges.overhang_px` past the top and right edges so it
reads as *on top of* the icon rather than *inside* it.

- **Geometry:** `tokens.badges.diameter_pct` of icon width, on the **top-right** corner
  (`tokens.badges.flow.anchor`) — and every badge a row wears draws at that one place. They are
  separated by frame LEVEL rather than by position (Part 2.5's z-stack), so exactly one is
  visible and order is fixed by polarity and then by each cue's `rank`, never by arrival: two
  rows wearing the same pair of cues always resolve the same way round. **There is no ceiling** —
  the vocabulary grows by declaring a cue, not by winning a slot. ⚠ Badges stepped **down** the
  right edge until 2026-08-27, and `tokens.badges.flow.direction` said so; the corner is one badge
  deep now and the key is gone. `Paint.StackOffset` survives for the `/cap style` gallery, which
  draws a vocabulary rather than a row.

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
| **`blocked`** | negative | `timer_CW_50` (still), **or the live cooldown dial** (V21) where the block is a cooldown | `HOLD` | 3 | held for a cooldown, or a readable dependency says the press would be wasted |
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

⚠ **No negative DECORATES ON A LOOP, and motion is the third polarity carrier.** Until 2026-08-23
the negatives animated — `blocked` swept a clock through five frames, `starved` and `overcap`
bounced a flask — and frame cadence was declared the *shared* idiom of the vocabulary, carrying no
polarity. That was wrong, and the thing that proved it is **dwell time**. A positive cue is up for
the moment you are meant to act on; a negative is up for as long as the skip is true, which in a
real pull is most of the fight. Motion the eye cannot finish reading is motion it keeps returning
to, so a vocabulary whose *skips* loop spends the player's attention on exactly the rows that
wanted none of it. Stillness is not a downgrade here — it is the correct rendering of "nothing is
happening on this row."

So the carriers run **hue, glow, motion**, and all three agree: gold + halo + animation says act,
red + still says skip. `priority` was already still by this logic before there was a rule for it
(V14's promotion ring is what moves), and `st_only` / `aoe_only` were still from the day they were
authored.

⚠ **What that ruling forbids is a LOOP, not motion.** It was written from a flight whose finding
was *"the blinking negatives were too much"*, and what the player was shown was a **five-frame
flipbook of a clock that was not telling the time** — decoration, cycling forever, conveying
nothing whichever frame you caught it on. That is the thing that does not come back. A negative
may carry a **real, terminating countdown**: a radial that drains once on a real remaining time,
ends, and is gone. It is the swipe mechanic the player already reads on every button in the game,
it answers *how long* rather than restating *held*, and it stops. `blocked` draws exactly that
whenever its block is a cooldown (**V21**, 2026-08-28) — a red radial with a white numeral in it,
in place of `timer_CW_50`, a picture of a clock face frozen at 50 % on a row where the real time
is right there and reachable. Same cue, same polarity, same rank, same red hatch beside it.

⚠ **This is a rule with no gate behind it, deliberately.** `capart check` gate **0e** used to fail
any negative cue declaring more than one frame; it was **deleted** on 2026-08-28 rather than
widened. A gate earns its place when it compares two things that can drift apart on their own, and
that one restated a literal in its own body against `tokens.cues[k].frames` — one source, checked
against itself. It could not have caught the case it was written for either: the dial is a
StatusBar and declares no frames at all. Measured before deleting it: every negative cue had
exactly one frame and the only multi-frame cue was `capped`, which is positive — so the deletion
removed nothing that was firing.
⚠ **The consequence to know about:** `Paint.Badge` branches on `#cue.frames` and builds a FlipBook
for any cue declaring more than one, so a future multi-frame negative would silently animate again
with nothing to stop it. That is now a thing an author has to not do, held by this paragraph
rather than by code. If it ever happens twice, the gate to write is one that reads the ART, not
one that re-reads the token.

**It also removed a real collision.** `starved` bounced `flask_empty → flask_half` and `overcap`
bounced `flask_half → flask_full`, so the two cues **shared a frame**: at any instant either could
be showing the identical half-full flask, and the only way to tell "you cannot afford it" from
"pressing would waste it" was to watch which way the animation was travelling. Two negatives with
opposite meanings were distinguishable only over time. The stills — empty for starved, full for
overcap — are unambiguous in a glance, which is the only budget a corner badge has.

**The two card stills** (2026-08-24) extend the same grammar. `building` wears
`card_outline_lift` — a card being set down: *the board is still being built, keep placing* —
on the rows a ramp holds while resource climbs to its window. `noproc` wears `card_outline` —
an empty card slot: *the card that makes this play is not in your hand* — on a row whose whole
value is a proc that is currently absent. Both are negatives: one red, told apart by shape,
still images like every other negative. `noproc` exists apart from `blocked` because the two
answer differently — `blocked` says *wait for a dependency's clock*, `noproc` says *nothing to
wait on; the press belongs elsewhere until the proc returns* — and a reader mid-pull acts on
that difference.

⚠ **A non-cue group that names a sprite off the cue sheet must DECLARE the borrow.** The
count mark names a sprite it does not ship, riding the cue vocabulary's frame list — and an
undeclared borrow silently stops shipping the day the last cue drops the frame: no missing
file, no failing gate, a corner of the overlay simply blank (found 2026-08-23, when dropping
`blocked` to one frame took V19's then-glyph off the sheet). `capart.BORROWED_FRAMES` declares
it, and `export badges` prunes what the shelf no longer names — which is what retired
`timer_CW_75` entirely when V19 moved to `fire`, and what ended V19's own borrow when the
glyph became the dial: `fire` stays on the sheet as the `priority` cue's frame, and
`tokens.pandemic` names no sprite at all.

**`capped` keeps its `BOUNCE`** and is the only cue in the vocabulary whose *glyph* moves: a thin
stack growing to a full one, which is the loss it is warning about, drawn. It is positive, it is
up for as long as you are wasting a charge, and it is meant to be chased. `blocked`'s dial is not
a counter-example — it is a countdown, not a glyph on a loop, and it ends.

⚠ **The positive cues glow; no negative does.** This is the second polarity carrier, and with
position no longer carrying it (V5) the two that remain are load-bearing: a negative cue that
glowed, or one tinted gold, would be indistinguishable from a promotion. `tokens.cues.capped.glow` pulses a halo *behind* the glyph
between `alpha_min` and `alpha_max` at `hz`. The **glyph itself holds full alpha** — a cue that
faded would blink the fact it carries, which is exactly what the `tokens.text` flicker limits exist
to forbid, and those limits (`max_hz` 2.0) are the ceiling this rate sits under. The halo may
breathe; the information may not. The glow is what earns the extra attention impending loss needs
in peripheral vision, and since 2026-08-23 the frame bounce reinforces it rather than being house
style a negative also wore.

**How the frames step.** A multi-frame cue's frames are baked into a `strip_<cue>` sheet
(capart bakes it beside the single frames) and a **FlipBook AnimationGroup** walks it — the
client steps the frames, no Lua runs per tick, and a group armed before a handover keeps
rendering where a ticker's writes are sealed (`security-taint-and-restricted-data.md` §3.5.3).
`REPEAT` wraps; `BOUNCE` turns around at each end, which is the animation system's own loop
type. `stepper.js` shows the same cadence from the same numbers, which is why the preview and
the client agree. (The addon-wide ticker this paragraph used to describe was deleted 2026-08-24
with the AnimationGroups conversion; the `SetParent` crash report on FlipBook is against
re-parenting a playing one, which nothing here does — `frames-textures-animation.md` §7.1.)

⚠ **The timer sweep is a pace, not elapsed time.** It is a "waiting" glyph, not a dial, and it
carries no clock — cap never reads one. If it reads as a countdown, that is a finding and this cue
has failed.

`blocked` covers what were previously two separate treatments — the readable dependency dot's
`wait` state and the sealed hold ✕. They are the same sentence to the player ("not yet"), and the
difference between them is a *provenance* fact (`spec.md` §3.2's two hold lanes), not a visual one.

### V6 · Corner dot *(retired)*

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

**A row wearing a positive cue draws a glowing ring around its badge — and so does V19's
window badge, which is a promotion the client decides**: `tokens.promotion`'s
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

### V12 · Virtual row

A press the Cooldown Manager does not carry draws as a **cap-owned icon** in its own panel:
the spell's icon at `tokens.panel.icon_px`, laid out at `tokens.panel.gap_px`, anchored per
`tokens.panel.anchor` / `x` / `y` and filling along `tokens.panel.grow`.

**It takes part in the scan, and it draws like a row.** V11's hatch from the same sheet, V13's
scan edge, the skip layer, and any cue badges its readable markers earn — the same treatment a
Cooldown Manager row gets, because it is the same `Treatment.For` answer painted through the same
`Paint` builders. Two things separate it from a CDM row and only two: it has **no Cooldown
Manager frame** behind it, and its **unknown polarity is inverted** (below).

**Why it exists.** Devourer's **Consume** is the most-pressed button in its branch and has no
Cooldown Manager frame in any category — not Essential, not Utility, not a tracked buff. An
elimination scan cannot land on a button that has no icon, and no cue can point at one either. So
without a cap-owned frame there are ordinary states where every entry on both surfaces is swiped or
badged and the correct answer is reachable only from memory. The alternative considered and
rejected was re-anchoring a TrackedBuff row into the Essential line; `render-rationale.md` holds
why.

⚠ **This section used to argue from Collapsing Star, and that example was WRONG** — corrected
2026-08-27. The premise held (neither `1221150` nor `1221167` has a `CooldownSetSpell` row of its
own) but the inference did not: it is a **spell override** on the Void Metamorphosis row, measured
in the client, and an override borrows the row of the spell it replaces. R7 draws it and it is not
cap-owned at all. V12 is unaffected — Consume has no frame either, which is why the primitive is
still right — but the row it was designed around turned out not to need it.

**The hatch means the same thing it means on a CDM row** — *not now* — and is drawn from
`tokens.hatch`, the same generated `Media/stripes.tga`.

**A virtual row is one of two kinds, and the kind is fixed by the ability, not by the moment.**

- **Gated** — availability varies, so the row is **hatched by default and clears only on a
  positive readable verdict that the press is available**. ⚠ **No catalog has one, and none has
  ever had one.** It was authored for Devourer's Collapsing Star and that row turned out to be an
  override on a real CDM frame (above), so the kind is **built, tested and unexercised**. It is
  kept rather than deleted because the inverted-unknown rule it carries is the reason a gated row
  is hard — a read that comes back UNKNOWN hatches the row forever with nothing saying why, which
  is why `Catalog.Check` refuses any subject predicate naming a virtual ability. **The next spec
  that wants one meets that rule before authoring, not after.** Until then it cannot be flown, and
  an in-game pass must record it as unexercised rather than as passed.
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

### V13 · Scan edge

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
- **ONE SHEET, NINE-SLICED — and it is shared with cap's ruled-out outline** (2026-08-29). It was
  four `SetColorTexture` strips until then. The strips cost no art, but they are a **drawn artifact
  in a stack of texture layers**, and that mismatch is what broke the preview's other outline: it
  was a CSS `border` on the striped element, and a mask clips an element's border, so the stripe
  sheet had been cutting it into dashes. It was never an outline. One sheet through the one
  pipeline gets the tint guard, the byte gate, and a flipbook path back if V13 ever wants motion
  again — at one texture per outline instead of four.
  ⚠ **The slice is what keeps it a hairline.** Stretched whole, a sheet authored against a 56 px
  icon draws a fatter, filtered line on a larger one — the defect frozen escape sizes had, arriving
  through the art. Sliced, the corners draw at native size and each edge stretches along one axis.
  `tokens.outline.line_px` is the width, declared **once**, which is what makes *cap's ruled-out
  outline exactly overlays the scan edge* true by construction rather than by two numbers agreeing.
  ⚠ It is **not** `tokens.ring` — that was V2's arrival machinery, deleted 2026-08-25, and
  `style_spec` guards the name dead.
- **Lua:**
  ```lua
  local edge = CreateFrame("Frame", nil, cap.overlay)   -- NOT the CDM item frame
  edge:SetPoint("CENTER", icon, "CENTER", 0, 0)         -- sized and centred, NOT SetAllPoints
  edge:SetSize(icon:GetWidth(), icon:GetHeight())

  -- ONE nine-sliced texture, built once, out of combat. White with the outline in its alpha,
  -- so the hue is a multiply at draw time and none is baked in.
  for _, t in ipairs(Paint.buildOutline(edge)) do
    t:SetVertexColor(T.ready.rgb[1], T.ready.rgb[2], T.ready.rgb[3])
    t:SetAlpha(T.ready.alpha)
    t:SetBlendMode(T.ready.blend)
  end

  edge:SetShown(inScan)          -- the only in-combat write this primitive makes
  ```
  The in-combat surface is one `Show`/`Hide`. Everything else happens when the roster is bound.
- **Preview reproduction.** The same generated sheet as a data: URI, nine-sliced through
  `mask-box-image` over a `--ready-rgb` fill at `--ready-alpha`, composited
  `mix-blend-mode: var(--ready-blend)` — `capart` maps the client's mode to the CSS one
  (`BLEND` → `normal`, `ADD` → `plus-lighter`), so the preview cannot show a hue the client would
  clip. A plain CSS border in the same ink is the fallback where `mask-border` is unsupported; the
  two draw the same line, so which one you get is invisible.

### V15 · Hotkey text

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

### V16 · Banded count

**A secret aura application count reaches pixels through a rule cap authored and the client
alone evaluated.** cap builds a `C_StringUtil.CreateNumericRuleFormatter()`, hands it a rising
list of `{ threshold, format }` breakpoints, and passes it to `SetApplicationCount(fontString,
{ formatter = … })`. The client compares the secret against those thresholds and writes the
winning format into the FontString. **cap never receives the count, never compares it, and never
reads the text back** — which is why this is a display and not a read. Promoted out of the lab
2026-08-22 per Part 7 rule 4, out of `count_band` (L1), `count_polarity` (L2) and `count_mark`
(L5).

⚠ **A ONE-BAND table is a legal and now-shipping use of V16, and it answers a different question:
*does this exist* rather than *how many*.** A single band at `threshold: 0` draws for any value the
container reports, so the mark tracks the aura's **presence** — it appears while the aura is on the
unit and vanishes with it, needing no latch, no alert edge and no count the catalog can name.
**It is the only form available on an aura whose `Duration` is `-1`**, where V19 and V20 have no
clock to ride: such an aura is present-or-absent and nothing else.
*(First shipped 2026-08-26 — Protection's `cons_field_up` on the Consecration player aura `188370`,
`Duration = -1`, one band `{threshold 0, mark, hatch, negative}` saying "the field is already
down".)* ⚠ Read it together with `spec.md` §3.6's limit: this asserts an aura's **presence** only.
The complement — *this aura is absent* — draws nothing, and nothing cannot be told apart from a
refused display or a wrong spell id.

**A band is authored as MEANING, never as a format string.** A catalog picks from a closed
vocabulary and the shelf owns what each one resolves to:

| `draw` | What the client draws for a value in this band |
| --- | --- |
| `none` | nothing at all — the resting state, and the thing a bar cannot do |
| `count` | the number, while *how many more* is still the live question |
| `mark` | one badge — plate and glyph — once *how many more* has stopped mattering |

⚠ **`count` and `mark` are EXCLUSIVE, and a band that asks for both is rejected.** The client
accepts both out of one band, and for a while the vocabulary offered that as `count+mark` — but
the numeral and the mark are anchored on the same badge corner, in the same polarity hue, so what
it actually draws is a glyph with a digit on top of it. Reviewed on screen 2026-08-24: unreadable,
and unreadable in a way that reads as a rendering fault rather than as a statement. There is no
offset that fixes it either — separating them spends a second corner, and the badge stack already
wants that pixel. **It SHIPPED** — Demonology's Implosion band declared it, in cap `v0.12.0`, and
it is the row this review was looking at when the combination was rejected; the `/cap style`
gallery drew it too. That band is now `draw = "count"`, and `count+mark` is gone from the
vocabulary rather than deprecated in place.

The two are a real choice, and the question they answer is different: `count` while *how many
more* is still live, `mark` once the answer has stopped being a number.

plus `polarity`, which picks the hue (V5.1 — hue carries polarity and only polarity), and `hatch`,
which lays V11's stripe sheet across the face. `hatch` is the only item on that list that changes
the elimination walk: it says the row is **ruled out**, not decorated. The format strings are built
in `Channel.CountRules` out of `tokens.count`, and that is the only place pixels enter.

⚠ **Every SIZE in a band string is a ratio of the row's measured width, and none of them is a
token.** An escape carries its size as a literal in the string, baked when the sink is armed, so
the three of them — hatch, plate, mark — are computed from what the row actually draws at
(`Channel.CountGeometry`, off `tokens.badges.diameter_pct`, `plate.scale` and `sprite_inset_pct`,
the same arithmetic `Paint.Ratios` does for every other badge). Frozen numbers here were right at
one icon size and wrong at every other, on every row at once. The OFFSETS stay tokens
(`count.hatch_offset_px`) — where an escape sits on the text
baseline is a judgment nobody can derive — and `/cap band` nudges those and only those. ⚠ Only
`hatch_offset_px` remains: the mark and the plate became their own AuraContainer slots, each with
its own button, so neither shares an advance width with the numeral any more and neither had an
offset anything read. `count.mark_offset_px` and `count.plate_offset_px` were deleted 2026-08-28. Its
no-argument readout prints the measured width beside the drawn diameter, which is the assertion:
the diameter must be `badges.diameter_pct` of the width.

⚠ **`hatch` is therefore legal only on a NEGATIVE band.** A hatch means *ruled out* and a
positive band means *enough* — one band declaring both is a contradiction wearing pixels, and it
was on screen until 2026-08-24: the gallery's positive V16 swatch drew the face hatched in gold,
which reads as "eliminated, but approvingly". The positive direction of this display is the badge
corner and nothing else; the face stays clean, exactly as it does under a positive cue.

**The numeral sits on the badge plate, like every other corner mark.** A bare digit floating on
icon art is unreadable on half the roster; the plate is what buys the badge stack its contrast and
the numeral was the one corner element not wearing it. It cannot ride in the numeral's own band
string — the first escape in a string is *flowed*, so a plate escape before the digit pushes the
digit off the plate rather than under it, and a plate escape after the digit paints over it — so
**the plate is its own element**: one more AuraContainer slot with the same thresholds, whose
bands draw the plate crop exactly when the numeral's draw `count`, built before the numeral's slot
so it sits under the digit the way the hatch sits under both. Same mechanism as the flown
hatch/mark/count split; the client blanks both together.

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

### V17 · Count complement

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

### V18 · Sealed bar

**`SetApplicationBar` drives a StatusBar from the sealed count; drawn as a left-to-right bar on
the row's BOTTOM edge, over a segment grid, flipping the whole bar to the negative red at full.**
cap creates the bar, its track, its fill, its size and its segment ticks as ordinary setup calls;
the client sets the range from cap's own `maxApplications` and the value from the secret. **Only
`BarValue` is sealed** — the aspect goes on the value, not the widget. Promoted out of the lab
2026-08-22 as the radial (`count_bar`, L4) and re-formed 2026-08-24 out of `segment_bar` (L8):
the segment grid is what makes the value read as *N of 4* at a glance where an arc read only as
fullness, and the bottom edge is a surface nothing else on a cap row claims — which also ends the
corner collision with V19's badge that Part 5 used to carry as an open question.

**The segment grid is cap's own track art.** One tick per application boundary, drawn under the
fill; nothing sealed touches it, and it is on the row at every value — which is what tells the
reader a half bar is *2 of 4* rather than *some*.

**Red at full is a WARNING, and it is the whole bar that flips.** Full stacks on the first
consumer (Demonic Core) means *procs about to be wasted* — a negative statement, so it takes the
negative red (V5.1: hue carries polarity and only polarity). The flip cannot be the fill
recolouring — the value is sealed and `SetStatusBarTexture` is a setup call, not a curve sink —
so it is **a second AuraContainer slot's count band** (V16's machinery, one slot per element)
drawing a full-width pre-tinted red crop over the bar at `threshold = max`. The client decides,
exactly as it decides every band; no Lua ever learns the count reached the cap.
⚠ The rejected variant — the full-state hue baked into the fill art's last cell, revealed by the
measured crop (*the bar crops its texture, it does not stretch it* `[client 2026-08-21]`) —
changes only the tip, and a warning wants the whole bar. It cost nothing to keep expressible: the
crop fact stands, and the flip band reuses it in spirit (the red exists before the count does).

⚠ **A BAR HAS NO BLANK STATE, and this is the straight trade against V16.** `SetValue` clamps
into `[0, max]`, so at zero the **track still draws**. V16 can be silent and cannot be a shape;
V18 is a shape and is always on the row. The track's colour and alpha are declared rather than
incidental — the track is what decides whether an empty bar reads as *nothing yet* or as clutter.

**`max` is what turns "or more" into "full".** The clamp is the expression: a catalog that wants
*four Cores is everything* declares `max = 4`, and five Cores is a full bar rather than an
overflow cap has to detect. The flip band fires on the same number.

**The radial render mode is retired with this form** — `Enum.StatusBarRenderMode.Radial` remains
measured and available (`[client 2026-08-21]`), and nothing in the style draws it.

- **Lua:**
  ```lua
  -- Slot 1: the bar. Track, ticks and fill are ordinary setup art on the row's bottom edge.
  local bar = CreateFrame("StatusBar", nil, button)
  bar:SetPoint("BOTTOMLEFT", host, "BOTTOMLEFT", 0, 0)
  bar:SetPoint("BOTTOMRIGHT", host, "BOTTOMRIGHT", 0, 0)
  bar:SetHeight(T.bar.height_px)
  button:SetApplicationBar(bar, { maxApplications = plan.max })
  -- Slot 2: the flip. A count band drawing the red crop at threshold = max; client-decided.
  formatter:SetBreakpoints(Channel.BarFlipRules(plan.max, T.bar, width))
  button2:SetApplicationCount(fs, { formatter = formatter })
  ```
- **Preview reproduction.** `--bar-h`, `--bar-rgb`, `--bar-track`, `--bar-full`, the ticks from
  the scenario's own `max`, drawn at a nominal fraction — full only where a swatch demonstrates
  the flip, because a scenario states "there is a bar here", never a value.

### V19 · Pandemic window

**`AddPandemicRegion` takes any Region — a Frame with children included — seals its `Shown`, and
drives it off the client's own `GetRefreshExtendedDuration − GetAuraBaseDuration`, per spell.** So
a whole badge, plate and dial together, appears and vanishes on Blizzard's real pandemic window.
Promoted out of the lab 2026-08-22 per Part 7 rule 4, out of `pandemic_mark` (L3).

⚠ **It is the ONE sealed display cap authors no threshold for.** Every other form here makes cap
name a number — a breakpoint table, a curve break point — and every authored number is a thing to
get wrong. This one has none. It is also **Blizzard's real pandemic** rather than the community's
30 %, computed per spell by the code that owns the spell.

**A Frame, not a texture, and that is what makes it a badge.** The client seals `Shown` and
nothing else, so a plate and a dial parented under the region appear and vanish together — the
same picture the cue vocabulary draws, out of a fact cap may not read. Its breath is gated for free
exactly as V16's is: the client hides the region, so a loop running forever on it is invisible
until the window opens.

⚠ **Two real costs.** It is the only sink carrying an `OnUpdate`, and Blizzard `secretwrap`s even
the **enablement** — whether cap's update loop runs would otherwise leak the aura's presence. So
**budget one per armed tile and never attach speculatively.**

**The full positive-cue treatment: V14's promotion ring AND the halo.** The badge wears
everything a promoted positive cue wears — the promotion ring blazing around it and the halo
breathing behind the plate — because it IS a promotion, decided by the client instead of by
cap: *the window is open* and *press this* are the same statement in the same grammar, and a
badge with only the halo read as a faint gold mist beside a real promotion (measured on screen,
which is what this file's preview exists for). Consistent with V5.1's polarity carrier: only
positives glow. Both motions are **AnimationGroups armed before the handover** — the ring a
FlipBook, the halo an Alpha loop — the only motion that survives on a handed-over region: in
combat the armed subtree is a forbidden object and the seal covers writes
(`security-taint-and-restricted-data.md` §3.5.3, `[client 2026-08-24]`). Gated for free: the
client hides the region, so both loops are invisible until the window opens.

**The pair: a running DoT has TWO states, and each draws its own way.** Aura up but **outside**
its refresh window: a **gold hatch across the face** — *do not refresh yet*, an eliminating
statement for the refresh press, in the window's own gold so it cannot be read as the cooldown's
black or the skip's red. Aura up and **inside** the window: the badge above. The hatch cannot
come from the pandemic sink — `ApplyPandemicRegions` calls `SetShown(inWindow)` with no reverse
flag (§3.5.2, Tier 1) — so it rides `SetDurationText` band tables on the aura's remaining
SECONDS, on a slot of its own (`{threshold 0 → blank, threshold outside_s → the gold hatch
crop}`; the crop is the count vocabulary's pre-tinted positive hatch). ⚠ **The two edges are
not the same fact**: the badge appears on Blizzard's real window, computed per spell; the hatch
clears at `outside_s`, a number the **catalog** authors. They can disagree near the boundary —
authoring `outside_s` at the ability's nominal window makes the seam small, and whether it is
visible is a flight question. A catalog that declares no `outside_s` gets the badge alone.

⚠ **`outside_s` has a FIRST CONSUMER as of 2026-08-26, so the seam is no longer hypothetical.**
Protection's `ha_weapon_healthy` declares `outside_s: 6` on Sacred Weapon `432502` — `6` is the
APL's own number (rung 10's `buff.sacred_weapon.remains<6`) and the buff runs **20s**, so the
catalog's hatch edge falls at 30 % of the life and should very nearly coincide with the client's
own window edge. **That near-coincidence is exactly the case that makes the seam measurable**, and
it is marked `@verify-ingame` on the claim rather than assumed either way. Demonology declares V19
without `outside_s`, so it exercises the badge half only.

**The badge's centre is a DIAL — a real radial countdown of the DoT's own lifetime.** Plate at
`badges.plate.alpha`, no region-wide pulse, and where the glyph sat, a radial `StatusBar` the
**client** drains: `SetDurationBar(bar, options)` seals only `BarValue` and its whole apply path
is `statusBar:SetTimerDuration(auraDuration, interpolation, options.direction)` — with
`direction = RemainingTime`, the gold arc empties as the DoT expires
(`security-taint-and-restricted-data.md` §3.5.2, T1). Radial render mode is measured working on
a `SetTimerDuration`-driven bar `[client 2026-08-21]`, pcall'd with linear fallback.
⚠ **`ApplyDurationBar` never calls `SetMinMaxValues`** — cap calls `SetMinMaxValues(0, 1)` at
setup or the bar draws 0 % forever (§4.8.1 finding 3). Cap reads nothing: the value is sealed on
the bar and the drain is the client's, which is what separates this from every predecessor.
⚠ Both predecessor glyphs are retired, and the distinction matters in prose: `timer_CW_75` was
**static art** — a baked 75 % wedge that read as a live radial attached to nothing, a timer a
reader watched and it never moved — where the dial is **a value the client drains**: the wedge's
claim made true. The `fire` glyph that briefly replaced the wedge said nothing the ring and halo
were not already saying. The badge still carries **no numeral** — a number invites reading
mid-pull; the arc is a shape, read peripherally like everything else here. A separate NUMERIC
countdown was drawn and removed the same day the wedge was, and stays removed. ⚠ The dial lives
**inside the handed-over wrapper** — that is what makes it appear only in the refresh window —
and the `AddPandemicRegion` + `SetDurationBar` one-button pair is **unflown**: each half is
measured alone (§3.5.1's sink fill, §3.5.2's region), never together (Part 5). The outside
hatch's `SetDurationText` sink still rides its own slot, which is the measured pattern.

- **Lua:**
  ```lua
  local region = CreateFrame("Frame", nil, button)   -- a FRAME, so plate + glyph travel together
  region:SetPoint("TOPRIGHT", button, "TOPRIGHT", Paint.StackOffset(0))
  -- the FULL positive-cue treatment, armed BEFORE the handover (§3.5.3): V14's ring + the halo
  Paint.PromotionRing(region):SetShown(true)
  local halo = region:CreateTexture(nil, "OVERLAY", nil, 5)   -- badges.halo art, T.pandemic.glow
  -- …plate parented under `region` from T.badges.plate, then the dial:
  local bar = CreateFrame("StatusBar", nil, region)
  bar:SetMinMaxValues(0, 1)                          -- FIRST — ApplyDurationBar never does (§4.8.1 f3)
  -- track + flat gold fill from T.pandemic.dial; pcall(SetRenderMode, Radial) linear-fallback
  pcall(button.SetDurationBar, button, bar,
    { direction = Enum.StatusBarTimerDirection.RemainingTime })  -- the client drains it
  button:AddPandemicRegion(region)                   -- no threshold anywhere in this file
  ```
- **Preview reproduction.** `--pd-rgb`, the dial as a `--pd-dial-*` conic-gradient arc that
  counts down in real time over a nominal looping window (the swatch's job is showing a live
  drain), and the halo as the cues' own `--badge-halo-stop` gradient at `--pd-glow-*`.

### V20 · Proc bar

**A thin client-drained bar on the row's bottom edge, directly above V18's charge bar when one
is declared: the proc's own remaining duration, emptying right-to-left as it expires.** The
slot filters to the proc aura (`includeSpellIDs`) on the ability's own declared `unit` — HELPFUL
on `player`, HARMFUL on `target`, which is the same derivation all four container kinds use;
while the aura is up
the client shows the button and `SetDurationBar` → `SetTimerDuration(auraDuration,
interpolation, RemainingTime)` drains the fill (§3.5.2, T1 — with the same trap as every
duration bar: `SetMinMaxValues(0, 1)` FIRST or 0 % forever). Linear render mode — no radial,
no pcall dance. When the aura drops, the client hides the whole button and the bar vanishes —
visibility is free (§3.5.1). cap reads nothing, authors no threshold, never learns where the
fill is.

⚠ **A V20 carries no POLARITY, and that is now load-bearing in a gate.** It says only how long
an armed thing has left — the duration of a face the row is already wearing — where a *count* in
the priority hue asserts *press this*. That difference is why Retribution's Light's Deliverance
band was deleted (it drew a positive count the APL never reads) while Demonology's `ib_art_clock`
was kept over an aura, `art_mother_of_chaos`, that appears in **no rung of its list**. The
display-provenance gate (2026-08-27) makes every sealed display cite a rung or argue itself in a
sentence, and that clock's sentence is this paragraph. **Meet it before authoring a second V20
over an unread aura** — the exception is declared per marker, deliberately, so the next case is
argued on its own rather than exempted by category.

**Why a bar and not the corner dial it replaces** (2026-08-25, stepper feedback): the dial sat
in the badge column, where **hue carries polarity** (V5.1) — a gold arc beside a red cue badge
and a red hatch read as two verdicts arguing, exactly on the held rows where the countdown
matters most (DEM-10). Edges carry no polarity grammar: the bottom edge already speaks
quantity (V18), and time-remaining is quantity, not verdict. Moving it also un-crowds the
densest corner (Demonbolt's declared stack was window badge + dial + two possible cue badges).
The corner-dial form lived one day; `tokens.pandemic.dial` stays, because V19's badge dial —
INSIDE the promoted badge, where gold is the promotion's own language — was never the problem.

**Geometry is static, from declarations.** A row that also declares V18's charge bar lifts the
proc bar to sit directly above it (`tokens.procbar.gap_px` between them); a row without one
puts it on the bottom edge itself. Declaration-driven for the same reason as Part 2.5's
cession rule: whether either bar is currently drawn is sealed.

**Consumers:** Demonic Core on Demonbolt (gold time draining over the white Core count — "this
many banked, this long to use one"), and the armed Demonic Art on the Shadow Bolt row while it
displays Infernal Bolt (⚠ the art aura id `432794` is Tier-3-sourced and the slot dies silent
on a wrong id — flight question).

⚠ **Unflown**: `SetDurationBar` on its own slot is §3.5.1's measured fill, but a 3 px
full-width duration bar has never been watched, and neither has two client-drained bars
stacked on one row's bottom edge.

- **Preview reproduction.** `--procbar-*` vars; a thin bar above the charge bar whose fill
  drains in real time over a nominal looping window, gold over a dark track.

### V21 · Live cooldown dial

**The `blocked` badge, when the block is a cooldown: a client-drained radial on the real
remaining time with a legible countdown numeral inside it.**

⚠ **This is not a fourth badge — it is what `blocked` draws.** A held row whose hold is a clock
used to wear `timer_CW_50`, a picture of a clock face frozen at 50 %, while the number the reader
actually wanted existed and was reachable. Now the badge tells the time. Same cue, same polarity,
same rank, same red hatch beside it; V5.1 carries the rule and the reasoning.

**Three catalog displays reach this picture, and they stay separate.** They differ in *whose*
clock, which is a fact about `Channel.lua` and not about the pixels:

| Display | Whose clock | How it resolves |
| --- | --- | --- |
| `sealed-base-cooldown` | **this row's own base spell**, hidden under a transform | the BOUND ROW's `base` |
| `sealed-cooldown-range` | **another ability's cooldown**, named by catalog key | `abilities[plan.ability].spell`, with a Step curve deciding visibility |
| `sealed-aura-remaining` | **an aura's remaining**, named by catalog key | an AuraContainer slot filtered to that aura; the client drains the arc off the aura's own duration object |

The second was already resolving a duration object — its band spends it on the badge's alpha — and
it now hands that same object to the arc and the numeral instead of drawing a still glyph.
Demonology's cue J (Dreadstalkers' Tyrant dead zone) and Havoc's Essence Break reading Eye Beam
inherited the dial the day it existed, with no change to either marker.

The row the base-cooldown form exists for is the transformed one. While a Grimoire is talented its Cooldown Manager
row spends its whole 120 s wearing the dispel it becomes — and the swipe on it is that dispel's
15 s, because `GetSpellCooldownInfo` reads `C_Spell.GetSpellCooldown(self:GetSpellID())` and
`GetSpellID()` is the display-identity ladder `[platform]` *(`cooldown-manager.md` §3.1.1)*. So the
two-minute cooldown a reader is waiting on is drawn **nowhere**. Cue K already rules the row out on
identity; it says nothing about when the row comes back, and that is the fact a ramp needs.

**Two calls, and the split between them is the whole design.**

| Question | Call | |
| --- | --- | --- |
| May the badge be shown at all? | `C_Spell.GetSpellCooldown(baseID).isActive` | **plain in restricted combat** — NeverSecret, 90/90 in-combat samples, false ×71 / true ×19 `[platform]` *(`cooldown-manager.md` §7 `[client 2026-08-09]`)* |
| What does it draw? | `C_Spell.GetSpellCooldownDuration(baseID, ignoreGCD)` | a duration object whose **every getter is secret** `[platform]` *(`security-taint-and-restricted-data.md` §4.8.4)* |

The first is a readable gate and reaches the catalog as the `baseoncd` predicate. The second is
never read: the object goes straight into `SetTimerDuration(d, Immediate, RemainingTime)` for the
arc and into `FormatRemainingDuration` for the numeral, which is a **secret string that renders** —
`SetText` puts it on screen, ticking, in combat `[platform]` *(§4.8.1 finding 2)*. The FontString
is therefore a **leaf**: it is anchored TO the badge and nothing is ever anchored to it, because
`SetText` with a secret marks the string and its dependent anchoring `[platform]` *(§4.8.1
finding 10)*.

⚠ **`SetMinMaxValues(0, 1)` goes in BEFORE the timer, or a correct duration draws at 0 % width**
with no error and nothing downstream to say so `[platform]` *(§4.8.1 finding 3)*. On this dial it
happens at build time, in `Channel.buildDial`, which is strictly before any draw pass — there is
exactly one such call on the bar and adding a second would make it unclear which one the guarantee
rests on.

⚠ **The predicate reads only on a TRANSFORMED row.** Untransformed, the base *is* the display and
the row's own dial already answers; a second supplier for one fact is a second thing to disagree.
`baseoncd` is UNKNOWN there, which closes the badge rather than opening it.

⚠ **`ignoreGCD` is true.** With false, every global cooldown reads as a live cooldown and the badge
appears for 1.5 s after every cast.

**Red, and it IS the verdict.** The arc is `blocked`'s own red, not V19's and V20's gold — under
V5.1 hue carries polarity and only polarity, and gold here would be cap promoting a row it is
ruling out. This is the one dial in the shelf that is not a quantity drawn beside a verdict: it is
the verdict, saying *held* and *for this long* in one mark. The **numeral is white**, so the number
reads against the arc it sits inside rather than competing with it.

⚠ **A marker that declares both a `cue` and one of these displays draws that cue AS the dial**, and
the sprite for it is not drawn at all — the two would be the same statement made twice, once
falsely: a frozen clock face on top of a running one. `catalog_cue_dials` is where the preview
reads that and `f.dialCues` where the overlay does, and both take it from the DECLARATION rather
than from what the client is currently showing, for Part 2.5's reason — that fact is sealed.

**The third one resolves no cooldown at all, and it is the only one that is a CONTAINER.** The
slot filters to an aura, so the badge exists exactly while that aura does and its visibility *is*
the gate — the same property `ib_art_clock` already relies on one row over. Because a container's
aura is the one the **marker** names rather than the bound row's, it reaches **across rows** with
no new mechanism: Demonbolt held because row 9 is showing Infernal Bolt draws the armed Art's
clock, which is precisely how long that hold lasts. It must declare a cue — it stands in for that
cue's badge — and `Catalog.Check` refuses one without.

⚠ **It has NO NUMERAL, and that is a limit rather than a choice.** The number above comes from
`FormatRemainingDuration` on a **cooldown** duration object cap holds and hands over. The aura's
duration object is the client's; the only aura-side text sink is `SetDurationText`, whose
breakpoints emit **fixed strings** — `""` or a texture escape, never a value over the remaining
seconds (`outsideSink` is its one use anywhere). The arc alone is still strictly more than a clock
face frozen at 50 %, and the numeral arrives the day a breakpoint is measured to interpolate one.
⚠ Which means the argument below — *"the numeral is the point, and it needs room"* — is an
argument the two cooldown forms make and this one does not. It keeps the diameter because it keeps
the corner, not because it earned it the same way.

⚠ **A dial whose marker declares no cue is still legal and still draws.** `grimoire_dispel_on_cd`
is the case: the row is swiped by the dispel's own 15 s, Blizzard has already ruled it out, cap
adds no cue of its own, and the dial underneath says when the row stops being the dispel. There
the countdown is a quantity again, because nothing is claiming a verdict over it.

**Why the badge grew.** A dial alone says the row will come back and not when, which is the half
cue K already covers. The numeral is the point, and it needs room: `badges.diameter_pct` is what
makes it legible at icon scale, and it costs nothing now that the corner is one badge deep.

**Not implemented, and named so the next reader does not re-derive them:** Devourer's **Voidblade**
is the second known instance and this is built so it can inherit — it needs a catalog marker and
nothing else. **Hand of Gul'dan / Shadow Bolt transform but have no base cooldown**, so there is
nothing underneath to draw. And `protection/holy_armaments` *looks* like a third instance —
it carries both `identity(…, "transformed")` and a `cd` state — but its two forms alternate on
**one shared cooldown**, so nothing is hidden and the swipe on that row is already the right one.

`[gated]` `capart check` gate 0 (the tint guard) names `tokens.basecd`, which declares
`tint: "none"`: the arc is a StatusBar fill and the numeral is text, so there is no art for the
guard to measure and the group says so explicitly rather than by omission.

- **Tokens.** `tokens.basecd` — `dial.size_px` / `dial.rgb` / `dial.track_rgb` / `dial.track_alpha`
  for the arc, `font` / `size` / `outline` / `rgb` for the numeral.
- **Preview reproduction.** `--basecd-*` vars; the arc drains over a nominal looping window and
  the numeral is a nominal number — cap never learns a real one, and what the swatch is for is
  judging whether the number is legible at this diameter. Where the row's winning cue is one the
  entry declares as a dial, the dial is drawn IN THE BADGE'S PLACE and the sprite is not built.

### V22 · Count badge

**The badge, with a number cap authored where the glyph would be.** One kind so far, and one
value: the `0` Implosion wears when no Wild Imp is out.

⚠ **This is not a fourth badge either — it is what a cue draws when cap holds the count.** Its
plate, diameter, corner, hue and frame level are the cue's own (V5/V5.1); the only thing it
replaces is the sprite. `implosion_no_imps` used to wear `timer_CW_50`, a picture of a clock face
frozen at 50 %, on a row where nothing is on cooldown and nothing is being waited out — while the
three states beside it on the same row drew a **number**: red at 1–5 imps, gold at 6 or more. The
zero was the one value in that sequence drawn as a symbol, and it is the one value cap holds
outright. The row now reads **0 → 1–5 red → 6+ gold**, one grammar.

**The licence, and it is the whole of what makes this legal.** Everywhere else in this project a
count is the CLIENT's — a FontString in an AuraContainer slot whose text Blizzard writes from a
rule cap handed over (V16/V17), never read back. This number is a **constant a readable term has
already established**: `!aura(wild_imp)` *means* zero. ⚠ **A numeral whose value its own marker's
`when` does not fix would be cap asserting a count it does not hold**, which is the one thing this
must never become; `Catalog.Check` refuses a `badge` on a marker with no `cue`, and refuses one on
a marker carrying a `display` — a display marker never contributes a cue (`Signal.markersOf`), so
such a numeral would build, arm nothing and be invisible forever.

**Red, and it is the SAME red the numeral beside it uses.** `tokens.count.low_rgb` — byte-identical
to `badges.rgb` — because a `0` and a `1` are the same statement about the same row and must not be
two reds. ⚠ A positive numeral would take `tokens.count.rgb`, the gold V16 recolours to at six; no
cue asks for one, and until one does the code path exists and is unexercised.

- **Tokens.** No group of its own. `tokens.count.font` / `size` / `outline` for the text,
  `count.low_rgb` for the ink, `badges.plate` for the disc under it — the cue's own diameter and
  corner offsets from `tokens.badges`.
- **Preview reproduction.** The `.slot` badge shape with a `.cue-numeral` text child in place of
  the sprite, drawn wherever the winning cue is one the entry declares a numeral for
  (`catalog_cue_numerals`).

## Part 2.5 — Composing a row

The primitives above are drawn together, and the order they compose in is fixed. **A row is a
hatch, a scan edge, badges, and whatever sealed display it declares** — the icon face is not cap's
(Part 1), and nothing else takes part in the composition. Chrome sits beside that rather than inside it: the hotkey text (V15) holds a
corner no cue may claim, carries no condition, and so has nothing to stack with or against. The
rule below is about conditions competing for a surface, and a label is not a condition.

1. **Blizzard's half of the cooldown hatch** (V11), or none. It sits under everything else,
   directly over the icon face, because it is a statement about the button rather than a mark
   placed on it. It never meets the scan edge: `cd` is the only verdict carrying it and `cd` is
   `scan: false`.
2. **The scan edge** (V13), or none. It is one bit, and the only thing it stacks against is the
   layer above it.
3. **cap's half of the hatch** (V11's second cause), or none — **over the scan edge**, which is
   the one place in this list where two treatments make opposite statements about the same row.
   An edge says *this row is in the read*; this says *this row is out*. A row wearing a negative
   cue wears both, so the contradiction is the normal case rather than an edge case, and **the
   later word wins**. Declared as a frame level (`Paint.Z.edge` < `Paint.Z.skip`), never left to
   the order two frames were built in — draw order across frames is decided by level and not by
   draw layer, so a texture on the row's own frame can never beat a child frame however high its
   layer.
4. **A badge per cue** (V5/V5.1), all on the one corner, of which exactly one is visible — see
   the z-stack below. A cue named twice is one badge — that is how a catalog authors an OR
   without an OR.
5. **A sealed display** (V16–V21), or none per marker. Its widgets are the client's to show, so
   cap places them and stops: a banded count takes the badge corner and the icon face, the
   segmented bar takes the bottom edge, the refresh badge takes the corner, and the cooldown dial
   takes the badge's own place when its marker declares a cue and the corner when it does not. **At most one per marker** — the four container kinds each need an AuraContainer slot
   and a marker is at most one of them (`Channel.ContainerPlan`), and V21 is not a container at
   all; a row may carry several markers (DEM-8, DEM-10).

   ⚠ **THE CORNER IS A Z-STACK, ONE BADGE DEEP.** Every badge on a row — cue badges, graded
   badges, corner sealed displays — draws at the **same** place, and what separates them is
   frame level. The order is Part 0.5's reading model:

   > **Negatives occlude positives. Within a polarity, rank decides. Sealed corner displays lose
   > to every negative and win against nothing else.**

   **It is not the cue rank**, and the reason is that the two failure directions are not the same
   size: hiding a **negative** behind a positive makes a held row look pressable, so you press it;
   hiding a **positive** behind a negative makes a pressable row look held, so you miss a beat.
   Only the second is survivable. Ranking by rank alone would draw gold over red on
   `havoc/ia_pre_meta_and_skip`, the one state that declares both — a state whose own note says
   the pair *"is declared rather than denied,"* because *"a sealed fact cannot be negated into a
   readable `when`."*

   ⚠ **This is what lets cap never learn whether a sealed display is drawing.** That fact is
   sealed, which is why the corner claim is unconditional — and under this order the question
   never arises: a row wearing a negative is out, so whatever is painting underneath is
   information about a row nobody is pressing; a row wearing none has nothing over the display at
   all. **Do not add a read to decide it.**

   Among the corner displays themselves, **declaration order is the tiebreak** — first declared
   draws over the ones after it — and the last of them sits on the level the eliminating hatch has
   always needed, one above the scan edge. Cap hides its OWN losers rather than covering them: a
   badge is a pooled frame, and one nobody took down is invisible until the thing above it stops
   drawing and it shows the state before last. The claimers are V19's window badge, V21's dial,
   and V16's corner elements (plate, mark, numeral). V20 claims nothing here: it lives on the
   bottom edge, which has its own static rule in its own section.

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
shape of the Kenney art CDMProbe already reads in client. `capart export hatch` and
`export promotion` write V11's stripe sheet and V14's proc ring the same way, into `Media/` beside
`Media/badges/`. The tint guard runs on every one of those paths, so
a baked-hue frame cannot reach the client through a route the preview never rendered. This is not
the "don't bundle Blizzard art" rule's subject: our own CC0 and generated art ships, because it is
ours.

`capart check` gates the stripe sheet the way it gates `Style.lua`: it must be on disk and
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
| total PAGE WEIGHT over `tokens.budget.max_page_kb` | a second, separate **warning printed by `build`**, never a blocked rebuild. ⚠ Distinct from the row above and added 2026-08-27: `build` used to measure the whole HTML against the *base64* ceiling, so markup was being reported as asset bloat and the asset number had been raised twice to accommodate pages that had simply grown more HTML. Each ceiling now measures the quantity it is named after |

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
   ⚠ **On a RULED-OUT row there is no yellow to judge, since 2026-08-29**: cap's own outline draws
   over it in red, from the same sheet at the same place (Part 3). What to watch there is whether
   one red outline plus a striped overhang reads as *out* at a glance — and, separately, whether
   the nine-slice holds the line at whatever icon size Edit Mode is set to, which is a source read
   and has never been seen in a client.
3. **Do the badges read without a legend at 56 px?** The negatives stopped looping on 2026-08-23,
   which removed the version of this question that used to matter most — whether a sweeping *fake*
   clock read as *waiting* or as a countdown. What is left is the harder half: does a
   **motionless** red glyph in a corner get noticed at all in a pull, or does stillness cost the
   thing it was meant to buy? ⚠ **`blocked` is the first partial answer and it is UNFLOWN.** Where
   its block is a cooldown it draws a real one (V21, 2026-08-28) — motion that terminates and says
   *how long* — so the flight has two things to report separately: whether the dial reads better
   than the frozen glyph did, and whether the remaining stills are noticed at all.
4. **Does one shared red across seven negative badges under-differentiate?** The shapes are meant
   to carry the distinction — and the two card stills added 2026-08-24 (`building`, `noproc`)
   push this question harder than the original five did. If they do not, the fix is different
   shapes, not a second hue.
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

10. **Does the segmented bar's bottom edge read as part of the row?** V18 moved off the badge
    corner and onto the bottom edge when the radial was re-formed as the segmented bar — which
    ended the corner collision with V19's badge that this question used to carry (DEM-8 declares
    both, and they no longer share a pixel). What is left to look at: does a 6 px bar under the
    icon read as *this row's* count, or as furniture between rows? And does the whole-bar red
    flip at full read as *stop banking* in peripheral vision, which is its entire job?

11. **Does the `AddPandemicRegion` + `SetDurationBar` one-button pair work at all?** Each half
    is measured alone — the duration-bar sink fills (§3.5.1), a handed-over wrapper appears and
    vanishes on the window with its subtree (§3.5.2) — but a `SetDurationBar` widget living
    *inside* the pandemic wrapper, on the same button, has never run. `--@unverified` on the
    composition; the failure to watch for is a dial that never draws, or one the handover
    orphans. And the look-at-it half: does a draining gold arc inside the window read as *time
    left to act*, or does motion in the badge corner pull the eye harder than the promotion
    deserves?

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
> **The tokens are `render-tokens.json`, beside this file** — and Part 7's are
> `render-lab.json`. They were a 664-line JSON fence in this section until they were split out;
> the reason is mechanical rather than tidiness. `capart` hashes whole files to stamp provenance,
> so while the data lived here a typo fix in Part 0.5's prose restamped every built page and
> every generated Lua file. Now the stamp moves if and only if the style moved.
>
> **This part is still the authority on what each token MEANS** — every group below is
> documented here and cited by name, never by restating its value. The two files carry the
> numbers and nothing else. Edit the JSON, then `uv run python -m wowkb.capart build --all`.
>
> Part 7's split is the same rule made physical: *nothing below Part 7 is the style*, and a
> separate file is harder to violate than a convention. `capart`'s `validate_lab_isolation`
> already treated it as its own namespace.

**What reaches the client, and what does not.** `Style.lua` is `render-tokens.json` minus
`capart.NOT_THE_STYLE`, and that list is not tidiness — five groups are declared here and
deliberately never shipped:

| Group | Why it stays out of `Style.lua` |
| --- | --- |
| `preview` | Fakes. Values that exist so the preview can draw a plausible row; the client has the real ones. |
| `lab` | Part 7. It decides nothing, and the gallery reads it through `Lab.lua` instead. |
| `text` · `assets` · `budget` | **capart's own generation inputs** — the preview's flicker limits, the icon encoder's settings, the base64 ceiling. They are style decisions about the *documents*, not about the overlay. |

⚠ **A group in that list is not a dead group, and the test for membership is not "does an addon
file read it".** Every entry above is excluded because the CLIENT is the wrong audience for it —
the preview's fakes, the gallery's lab, capart's own generation inputs — not because nothing has
got round to reading it yet. A style may legitimately be declared here before the code that draws
it exists; the shelf declares exactly one style per primitive and writing it first is the point.
What such a group is waiting for is its primitive, and it joins `Style.lua` the day one arrives —
`panel` did exactly that when V12 was built. Nothing in this table may be deleted on the grounds
that "no addon file reads it".

⚠ **The converse is not the same rule.** `tokens.ring` / `tokens.motion` / `tokens.arrival` were
deleted on 2026-08-25, and they were never on that list — they shipped. What killed them is that their
**subject** went: V2 retired, then Part 7's `arrival-*` entries were judged and deleted, and a
declared style whose primitive no longer exists in either half of the project is not a style
written ahead of its code. The arrival had a primitive that had already been taken out; a style
written ahead of its code has one still coming.


**Which half of the project reads which field.** `swipe` is the only one the ADDON reads, in the
`/cap style` gallery, so a lab swatch shows Blizzard's dial exactly where a real row would. Every
other field — `scan`, `hatch`, `cues`, `eliminates` — is read by the PREVIEW and by `capart
check`'s elimination gate, and by nothing in the client. ⚠ **`Treatment.For` does not read this
table and cannot**: the engine's verdict is a struct (`member` · `oncd` · `cues`) with no name in
it, so there is no key to look up. This table is the vocabulary a human writes a row's state in;
the struct is what cap computes. `spec.md` §1's anchor names both.

**Reading the verdict table.** `scan` is whether the row is in the scan at all — `cd` is
the only row that is not, because Blizzard's swipe has already ruled it out and an edge would
just be noise on a dead button. `swipe` is Blizzard's own dial, which cap does not
draw and does not restyle (V7); it appears here so the preview can reproduce the row faithfully.
`cues` names badge cues (V5.1) by key into `tokens.cues`, and each cue's `slot` fixes where it
lands. A cue whose token carries `open: true` draws with a ⚠ chip in the preview and produces
**no hint in the addon** until it is measured (`spec.md` §3.6); none does today.

**`press` and `open` render identically, and that is the point.** The press is
"the leftmost thing not ruled out," not a thing cap draws (Part 0.5). `press` is kept as a name
because the scenario docs need it to state their falsifiable claim — the elimination gate
re-derives it from the grammar and fails a row that disagrees. *(The 2026-08-25 collapse folded
the eight cue-flavored verdicts into these two: a verdict like `starved` was a cue name wearing a
second hat, and the cue now rides an explicit `{cues: …}` group instead. `press-promoted` folded
into `press` — the positive cue on the row is what pass 1 reads; `below` folded into `open` —
"right of the press" is a position, not a state.)*

**The verdict vocabulary is closed.** These five keys are the whole set a scenario may use;
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
`composites`, was deleted as an argument its subject had overtaken. The eighth, `duration_band`,
was cleared on 2026-08-27, and `ring_collision` — added and withdrawn — left on 2026-08-28.
**The lab is empty again**, and an empty lab means every idea drawn here has been adopted or
answered, not that nobody is trying anything.

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
| `segment_bar` (L8) | 2026-08-24 | → **V18 re-formed**: the radial became the segmented lateral bar with the whole-bar red flip at full. The crop-revealed-tip variant was not taken — it changes only the tip, and a capped-stacks warning wants the whole bar. Same-day promotion; the entry lived for one review round. |
| `blaze-*`, `procglow-*` | 2026-08-19 | **V14**, the promotion ring, was picked out of this set — generated by `wowkb.procring` against four properties measured off Blizzard's own proc glow. The losing candidates are deleted rather than kept: they were alternatives to a decision that has been made, and a lab full of settled arguments is a lab nobody reads. |
| `arrival-*` | 2026-08-19 | Deleted with their subject. The arrival questions belonged to V2's animated border; **V13's scan edge is static**, so there is no snap to judge and the entries had outlived the thing they were asking about. |
| `ready-*` | 2026-08-19 | **V13**, the scan edge, was picked out of this set. Part 5 question 2 still asks whether a static line is loud enough in a pull — but that is a question about the *shipped* treatment, and it is asked there, not by keeping three unadopted alternatives drawn beside it. |
| `count_band` (L1), `count_polarity` (L2), `count_mark` (L5) | 2026-08-22 | → **V16**, the banded count and its mark, with `tokens.count`. L5's composited crop won: put the plate inside the art the escape names so the whole badge rides the band, where L1's `place: "badge"` cells left an empty disc at every resting value. L2's hue question came with it — per-band escape, static floor, or no hue at all — and V16 answers it by spending hue only on polarity, which is V5.1's rule rather than a new one. |
| `count_complement` (L6) | 2026-08-22 | → **V17**. It is the same sink as V16 and it is a separate primitive because it is a separate *statement*: the row rules ITSELF out, which made a sealed fact the third eliminating signal and forced `capart check`'s elimination gate to learn about it. |
| `count_bar` (L4) | 2026-08-22 | → **V18**, `tokens.arc`. Its cells had been drawn as an explicitly-labelled proposal off a source read; the flight settled it. What promotion added is the honest half — a bar has no blank state, so the track is declared rather than incidental. |
| `pandemic_mark` (L3) | 2026-08-22 | → **V19**, `tokens.pandemic`. The only sealed display cap authors no threshold for, and the only one whose cost is a per-tile `OnUpdate`. |
| `composites` (L8) | 2026-08-22 | **Deleted, not promoted.** It was the argument that the four above compose on one row — three whole Demonology scenarios built out of them. Once Demonology was built its subject became a real spec's walk, drawn by `demonology-stepper.html` against a shipped catalog. An argument that has been overtaken by the thing it argued for is not an experiment. |
| `duration_band` (L7) | 2026-08-27 | **Cleared, not promoted.** Its cells had drifted out of agreement with its own `asks`: they drew the `RemainingPercent` route as an open question after V19 had promoted the SECONDS form, so the entry was arguing for a mechanism half of which was already the style. Part 7 says an entry that cannot say what it is asking is decoration — and one whose cells no longer draw its question is the same thing arrived at by drift. The open half is real and unchanged: `RemainingPercent` via `options.textFormat` is **source-read only**, never flown, and the quiet-middle band shapes V19 cannot express are still unexpressed. Re-add it from `git log` with cells that draw *that*, when a built spec wants a banded clock. |
| `ring_collision` (L9) | 2026-08-28 | **Withdrawn without an answer.** It drew the collision Part 3 records as an open design question and Part 4 as a settled rule: a row wearing a negative cue is `scan: true`, so V13's yellow edge and cap's half of V11's red hatch say opposite things about the same button. Two controls, the subject, and one proposal — occlusion, red over yellow, the edge still drawn underneath — were built and then removed before the look was called. **The question is untouched by this**: geometry, not order, still keeps the two rings apart (`hatch.skip.overhang_px` holds red 2px outside the rect), and neither `Paint.Border` nor `Paint.Hatch` calls `SetFrameLevel`, so both implementations are still right by accident and neither declares anything. The three candidates — overlap, suppression, adjacency — are in Part 3, where they were before the entry existed. The `skip_overrides` machinery it needed went with it; `git log` has both. |
| `hotkey-l1` … `hotkey-l10` | 2026-08-19 | **V15**'s font, size and dark edge were chosen out of this set of ten — five faces, then a plate, then a title bar. The winner is `tokens.hotkey`; what the losers cost is written into V15 itself, which is the point of promotion rather than citation. |

⚠ **A deleted entry is not a refuted one.** Nothing in this table is a claim that the treatment
was bad — most of them lost to something, and one or two were simply asking about a primitive that
no longer exists. `git log` holds every one of them with its `asks` intact, which is where a
revived idea should be read from. Re-adding one is cheap: a `lab` key, an `asks`, and a section
here.
