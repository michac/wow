# Combat Assist Plus — spec

**What this file is for:** what the addon is supposed to do. The product
definition, not the implementation. If you're about to build something and this
file doesn't say what it should do, the answer is to write it here first (or ask),
not to infer it from the code.

---

## 1. What it is

`/cap` — **Combat Assist Plus**, an addon that makes Blizzard's Cooldown Manager
carry more of what you already know: the same facts, re-presented, graded and put
in context, in the place you are already looking.

The platform draws the shape of the work. Since 12.1 an addon can *display* much of
your combat state but cannot read it back to reason about it — Secret Values seal
the primary resource, the cooldown numbers, the cast identity. Rather than fight
that, cap treats it as the design brief. **cap presents information you already
have, differently.**

**Two principles:**

- **a)** **cap does not fight the secret restrictions.** The readable/sealed split
  (§3.6) is the platform boundary, and it is the one line enforced in code —
  `Catalog.lua` and `Channel.lua` hold it, and `capart` gates the vocabulary that
  reaches it.
- **b)** **cap freely uses non-secret information to give good hints.** Whatever the
  client hands an addon in the clear is fair material, and using it well is the job.

Underneath them, three moves, in order of preference:

1. **Re-present.** Take something the game already tells you and put it where you
   can actually use it — the right place on screen, the right size, the right
   moment.
2. **Grade.** Turn a yes/no signal into a *how much*. Blizzard's proc glow says
   "this is available." cap says "this is available, and right now it's worth
   about this much." A dim thing and a bright thing are the same information with
   a decision half-made by your eyes instead of by a rules engine.
3. **Contextualise.** Show what a moment *is* — an opener, a burst window, a
   cooldown coming back — so the choice you make is an informed one.

The central expression of move 2 is **scan membership plus the augments** (§3.1):
a row is either in the scan or it is not — the border is a castable-or-not flag —
and the cues (§3.2) and sealed displays carry every finer statement. Read together,
membership and cues put your presses in roughly the order an authoritative priority list would.
Where the facts genuinely favor one option, cap layers emphasis and cues until that
press is obvious; making the right press findable is the product.

cap is **opinionated, not configurable**. You get recommendations derived from
your class and spec, chosen by us. It is deliberately not WeakAuras: there is no
trigger editor, no condition builder, no library of user-made packs. If cap's
opinion about your spec is wrong, the fix is to change cap's opinion, not to
expose a slider. The few controls that exist are **inputs and placement**, never
opinions: single-target/AoE mode (§2), where cap's own panel sits, and whether it
re-anchors the Cooldown Manager's rows (§3.9).

**The vocabulary, in one place, and this is the only place.** Eleven words carry most of the
weight below. Each is defined here and **nowhere else** — `render-shelf.md` and the catalogs point
at this table rather than restating it, because two glossaries where one cites the other are still
two glossaries.

| Term | Means | Owned by |
| --- | --- | --- |
| **scan membership** | The single boolean cap asserts about a row: is it still in the running? A member draws the scan edge; a non-member draws none of cap's emphasis. Default is "the ability is ready"; `scan_when` overrides it. | §3.1 |
| **readable** | A fact Lua may read *and compare*. cap may branch on it, rank by it, and drive emphasis with it. | §3.6 |
| **sealed** | A fact the client will let cap *display* but never read back. cap authors a rule, hands it to the client, and never learns which branch fired. Branching on one is the one invalid rule in this file. | §3.6 |
| **cue** | An additive badge on a row, from a closed vocabulary, saying *why* a press is ruled out (or, rarely, promoted). Negative by default; catalog-authored per ability. | §3.2, `render-shelf.md` |
| **verdict** | The closed set of row states the docs are written in: `cd`, `open`, `press`, `ruled-sealed`, `weave`. The catalogs, the scenarios and the preview are all written in it. Not player-facing: `press` and `open` render identically, because the press is not a thing cap draws. | `render-shelf.md` Part 6 |
| **evaluation** | The engine's per-row struct — `member` · `oncd` · `cues` — that `Signal` builds and `Treatment.For` draws from. It carries **no name**, which is why a row can never be looked up in the verdict table: the verdict is how a human states a row's state, the evaluation is how cap computes one. ⚠ **The code still calls this struct a verdict** (88 occurrences in the addon). Renaming it has real blast radius and is a separate job; the debt is named here so the next reader is not misled by it. | §3.1 |
| **elimination** | The reading itself: the eye finds the press by *absence* — the leftmost row neither swiped nor wearing a negative badge. Three signals eliminate: Blizzard's cooldown swipe, cap's negative badge, and a sealed band the client evaluates. | §3.1, `render-shelf.md` Part 0.5 |
| **surface** | Something there is to draw *on*: the CDM item face and its edges, the corners Blizzard leaves free, and cap's own panel. What a surface already carries is a constraint on what may be put there. | `render-shelf.md` Part 1 |
| **primitive** | A reusable drawing **element** cap builds — a badge, a hatch, a bar, an edge. It has a registry id (`V5`, `V11`…), `Paint.lua` holds one builder per primitive, and a catalog state names the ones that draw it in `drawn_by`. | `render-primitives.json`, `render-shelf.md` Part 2 |
| **treatment** | What a **verdict draws** on one row: the composition of primitives a row gets, which `Treatment.For` returns as scan edge / cues / hatch / skip. Primitive = the element, treatment = the composition. They are near-synonyms in English and are not synonyms here; this row is what stops them drifting back together. | `render-shelf.md` Part 2.5, `Treatment.lua` |
| **mechanism** | *How* a sealed fact reaches a pixel — a formatter, a colour curve, a range-gated texture. A primitive is built **on** a mechanism; a mechanism draws nothing by itself and can never be cited as what a state draws. | `render-primitives.json`, `render-shelf.md` Part 2 |
| **slot** | Where a drawn thing sits: `flow` (the badge stack, flowing down the right edge) or an integer corner claim. ⚠ **A dead meaning is still gated against** — `slot 1` / `slot 2` / `slot 3` were three fixed badge positions, deleted 2026-08-19, and `capart`'s vocabulary gate fails a catalog that names one. | `render-shelf.md` Part 1, `capart` |

It **rides on the Cooldown Manager** rather than replacing it. The CDM already
knows what your spec cares about and already draws it legally. cap binds to it,
skins it, and extends past its edges where the icons are too small to carry what's
needed.

## 2. Scope

cap is built for the author first and may be published later. It has chosen defaults and no
settings panel. The player may move its independent surface and set single-target or AoE mode;
those are inputs, not a way to rewrite cap's opinions.

Specs are added one at a time, and **the unit is a spec-and-hero pair** (`authoring.md` §0). A
spec or build cap has not deliberately authored is completely inert: no generic recommendations,
no fallback skin and no guesses. Which specs are authored, transcribed or flown is
`backlog.md` → `## Status` and is deliberately not restated here.

cap is meant to work in the restrictive case—combat, instances and PvP—not only on a target
dummy in a city. Out of combat it is quiet apart from setup controls.

## 3. What the player sees

One precedence rule, and it is about the platform: **a rule that would require cap to branch on
sealed data is invalid**, wherever it is written. That boundary is §3.6's, the client enforces it,
and `Catalog.lua` / `Channel.lua` hold it in code. Everything else below is an ordinary detail —
if it is wrong, edit it.

### 3.1 Emphasis

cap's coarse statement about an ability is a single boolean: **is this row in the scan?**
A member row draws the one scan treatment — the lane border, which devolved by measurement
into a castable-or-not flag — and a non-member row draws none of cap's emphasis. There is no
finer gradation in that treatment: cues (§3.2) and sealed displays carry every statement
finer than membership. *(Until 2026-08-25 this section defined three role tiers — COOLDOWN /
ROTATION / FALLBACK — and mandated an emphasis ladder over them. The shipped renderer had
already collapsed every tier onto the one scan treatment — `presentation_spec.lua` asserts
there is nothing to tell them apart — so the model now says what the product does. The three
names survive only as prose grouping in the catalogs.)*

The boolean serves the reading the pilot actually runs — the two-pass scan that
`render-shelf.md` Part 0.5 owns:

> "I'm scanning left to right to decide what to do. First I'm looking for positive cues,
> which override the normal priority order with something time sensitive or normally very
> out of order. Then I'm scanning left to right with each CDM item being augmented to
> indicate it's unavailable for various reasons until I get to one that's ready."

Membership plus cues, read together, put your presses in roughly the order an authoritative
priority list would — which is why the player reads the cues rather than blindly pressing
the leftmost lit thing.

**Two tools, layered.** cap says things two ways. **Emphasis** is an on/off treatment driven by
comparisons over values cap is *allowed to read* (membership above, and readable markers).
**Cues** are additive display forms fed by values cap may *display but not read* — colors,
readouts, hold marks, bars — that stack and move but are never read back (§3.6). Author them
together; a well-built catalog reproduces the priority order by layering the two.

Because emphasis is comparison-driven, it may be moved only by a **readable** fact. A window
whose active-state is sealed still informs, but through a cue (§3.2), never through emphasis.
That is the §3.6 boundary, and it is the only thing this section constrains.

By default a row is in the scan exactly when the ability itself is ready. A row whose
membership is genuinely conditional declares `scan_when` — alternatives of readable terms,
any one of which suffices. A row is withheld when no alternative holds or a required read
is unknown: unknown never lights.

**Membership does not rank.** One lit row is not brighter than another lit row; the eye is
directed by cues and by elimination, never by comparing intensities. (The emphasis ladder that
used to stand here — promoted > lit COOLDOWN > lit ROTATION > dim/off — described a product
the renderer never shipped, and `presentation_spec.lua` exists to forbid it.)

**Eye-direction by elimination.** A low-priority button is directed-to by the **absence** of
competing emphasis, not by a bright cue of its own. The default spender and the filler need no
signal — they win when they are the only lit button left. The same holds for a hold mark's absence
— an un-held, ready cooldown is directed-to precisely because the hold mark is *not* drawn. This
is not a stance: it is `wowkb.capart check`'s **elimination gate** (`capart.py`,
`elimination_gate`), which asserts for every scenario that the leftmost entry neither swiped nor
wearing a negative badge is the one the doc calls the press. A catalog that breaks it fails by
name.

What this section fixes is that principle. **The procedure a player actually runs is
`render-shelf.md` Part 0.5's**, and that file owns it: it states how the row is scanned, in what
order, and how the one positive cue interacts with the scan. That is a reading-model question, not
a constitutional one, and changing it is a shelf edit. This section does not restate it — a
procedure written down twice is a procedure that will disagree with itself.

**A priority list is a dependency graph, and emphasis may follow a readable *relationship*, not
only a button's own state.** An ability's place in the order is usually set by *why* it ranks
there — a reset it grants, a window it opens, a buff it maintains, a resource it needs — and that
reason often rests on the state of a *different* ability. Metamorphosis leads the Havoc priority
because it resets Eye Beam and Death Sweep; pressing it while either of those is ready throws that
reset away, so its rank is set by *their* state and not its own. Emphasis is therefore allowed to
compare *related* facts — one ability's cooldown against another's — not just each button's own
readiness. This is still emphasis moved by facts cap may use; it is not a computed press.

**Whether the related fact is readable or sealed is a separate axis, and the same hold can
straddle both.** Metamorphosis is the worked example twice over: "is Death Sweep ready" is a
readable boolean, while the rest of the same hold — "is Eye Beam more than eight seconds away" —
is a remaining time, which is sealed and must be handed to the client as an authored band (§3.6).
One rule, two mechanisms, one badge. So do not read *relationship* as a synonym for *readable*:
the relationship is what licenses the comparison, and the data class only decides who performs it.

This is also where the honest limit sits — and it is **narrower than "the ordering-reason is
secret."** "Membership plus cues reproduce the priority order" holds wherever the ordering-reason is
readable *or expressible as an authored threshold on a secret value.* A **threshold comparison is
not a branch cap performs**: cap hands the client an authored break point (the `sealed-power-percent`
/ S1 graded curve, §3.6) and the client evaluates the secret value against it and paints the result
— in **either polarity**. So "avoid this generator when the secret resource is about to cap"
(negative) *and* "this press is preferred once the secret resource is banked past a threshold"
(positive) are both expressible sealed cues; cap authors the number and never learns which side the
value fell on. ⚠ The positive direction is **specified but has no live SEALED instance**: both of
the vocabulary's positive cues — `capped` (a charge being lost) and `priority` (press this one) —
are driven by readable facts. An earlier
example here — Essence Break at Fury ≥ 35 — was deleted when the 12.1 APL turned out to put no Fury
term on Essence Break at all. What the platform does not allow is cap
**computing** with the value — reading it into a Lua branch, score, or verdict. A spec's catalog
says, per rung, whether its ordering-reason is a readable rank, a sealed threshold cue, or an
unmeasured (open) cue — the "secret ⇒ cap is blind" framing is wrong.

These rules are spec-wide, not spec-specific; the Havoc scenario catalog (§3.7) is the first
document to walk a full priority list against them, rung by rung, and to mark each rung's
ordering-reason readable / sealed / secret-gated / open.

**Every visual choice below the model belongs to `render-shelf.md`** — treatments, color,
alpha, blend mode, size, motion, placement, and how cap coexists with Blizzard's stock proc glow.
None of them are settled here, and changing one there is a normal edit, not a spec amendment.
What this section fixes is only the *model*: scan membership, driven by readable facts, with
cues and sealed displays carrying everything finer.

### 3.2 Context markers

A marker adds a fact the player can combine with an emphasis; it does not collapse several
facts into a single verdict.

- A **readable marker** is driven directly by a fact Lua may read. It needs no sealed client
  half. Demonology's five-shard Tyrant hold is the model: `UnitPower` is readable, so the hold
  is an exact Lua comparison.
- A **sealed marker** is optional. The client may evaluate a sealed value and draw the result,
  but Lua never reads that value or branches on it. A catalog marker has exactly one form:
  readable `{ id, when }`, or sealed `{ id, display }`.
- A **hold marker** is context that says there is a reason to wait — "this is off cooldown,
  but there is a better moment coming." A hold marker has the same two
  routes as any other marker: its gating fact is either **readable** (Lua evaluates the wait
  condition and drives the marker directly) or **sealed** (the client evaluates a sealed value
  — a duration counting down inside an authored band — and draws the marker; Lua never reads
  or branches on that value). The Havoc catalog (§3.7) is the first user of both hold routes.

Every supported marker has a visible implementation. A catalog form that loads successfully
and then renders nothing is a defect.

⚠ **That test only works if a marker is single-state.** A marker authored as a *pair* — one
appearance for "wait", another for "go" — makes "it rendered nothing" ambiguous: it could be the
defect above, or it could be the satisfied state behaving correctly. So a marker declares the one
condition under which it draws, and its absence is the other condition. That is not a new rule;
it is what makes this one testable. (The render shelf spends this on a cue vocabulary that is
negative **by default** — a marker draws when the press is ruled out and never otherwise — with
narrowly scoped positive exceptions. The single-state requirement stands whichever
polarity a marker is authored in.)

Marker shapes, colors, sizes and placement are `render-shelf.md`'s, not this section's. The
question a flight asks is whether the player can identify the fact without consulting the
catalog; the answer changes the shelf.

Not everything cap draws is a marker. A keybind hint identifies a row rather than gating a press —
it has no `when`, no `display`, and no catalog authors it — so **§3.8** holds it outside this
taxonomy on purpose, rather than admitting a marker that is exempt from the rules above.

### 3.3 Tyrant cooldown experiment

One movable Tyrant countdown bar tests whether a larger surface adds information the CDM icon
cannot carry legibly. It is independent: it does not automatically inherit icon emphasis or
markers.

The client owns the remaining duration. cap may hand that duration to the bar but may not read
it back. Ready, counting-down and unreadable states must not be confused, and a capture may
report only which path cap armed—not what appeared on screen.

The bar is an experiment, not a required surface for every cooldown; play decides whether it
stays.

### 3.4 Demonology Warlock / Diabolist

**Authored to the comprehensive standard** (§3.7) as three files under `specs/demonology/` — a
definition, its proof and its safety case. **Those documents own the roster and every rule in it;
this section owns only what is approved behaviour and does not restate a roster.**

It began as a *deliberately tiny proof* — four entries demonstrating readable readiness plus a
readable marker — and was replaced on 2026-08-19. That history is §3.7 and `notes.md`; **nothing
in it is a present-tense rule.** Two of the pilot's three hypotheses were carried and one was
corrected, on evidence:

- **Demonbolt's overcap threshold was three Soul Shards and is four.** The APL term is
  `soul_shard<4`; at three shards a Demonbolt leaves exactly five, which is full and is not waste.
  The shape of the hypothesis — Blizzard's proc glow says *available* where spending would waste a
  readable resource, so cap marks the waste — is unchanged and shipped.
- **A ready Tyrant in the scan survives**, and the "familiar setup pieces" markers it proposed do
  not. The setup facts the pilot wanted to draw (Dreadstalkers' and Grimoire's commitment state)
  turned out to be weaker than the one the priority actually gates on: **enter the window at five
  shards.** Soul Shards are never-secret, so that is an exact Lua comparison and it is the
  catalog's centrepiece.
- **The Tyrant countdown bar is not authored.** §3.3 still owns the bar's safe-state semantics and
  the permission is unchanged; the catalog declares none, because the fact it would draw is
  Tyrant's own **sealed** cooldown remaining and the row already carries the **readable** half of
  the same decision.

**A spec-and-hero pair is the unit.** Soul Harvester is a separate future catalog, never an
overlay on this one; the reopening condition is stated in the catalog that declines it.

### 3.5 Destruction Warlock / Diabolist

**Authored to the comprehensive standard** (§3.7) as three files under `specs/destruction/`, on
the same terms as §3.4. It began as the *authoring proof* for the sealed-display sink — two
entries, Conflagrate and Backdraft — and was replaced on 2026-08-19.

Two of the proof's three claims survive and one is **withdrawn**:

- **Backdraft is sealed, and Blizzard's AuraContainer owns its whole display.** Unchanged, and
  still the shipped precedent other catalogs cite. What changed is that the single-target rotation
  **does not need it**: its Conflagrate rungs ask whether Backdraft is *absent*, which is a
  boolean the Cooldown-Manager aura latch answers. The sealed count is the right shape for the AoE
  rung that asks for two stacks, and that rung is not authored here.
- **Conflagrate is the charge row.** Unchanged.
- **The charged-readiness estimate is withdrawn.** The proof proposed recovering a live charge
  *count* — exact out-of-combat seed, debit on a cast, credit on an accepted `ChargeGained` alert,
  clamp, re-seed at combat end, with captures distinguishing exact `live` from in-combat
  `napkin`. **No rung in the 12.1 priority wants the number.** The one Conflagrate rung that reads
  charges asks `charges>=2`, and R6 reads exactly that and only that — charges
  are readable at full and seal below it. The recipe stays on the shelf, unbuilt, for a spec that
  needs a number; the `live` / `napkin` capture labels have no producer.

**A spec-and-hero pair is the unit**, and here the pick itself is provisional: Hellcaller is a
separate future catalog and the condition that would make it the next one is stated in the
catalog that declines it.

### 3.6 Safety boundary

The implementation distinguishes two data paths:

- **Readable facts** may enter Lua conditions and drive emphasis or markers.
- **Sealed facts** may flow only into client-owned display sinks. They never enter a Lua
  condition, comparison, score or verdict.

**What this permits, and it is more than the two rules first read.** The split constrains what cap
may *compare*, never what it may *show*:

- **A secret value can drive a widget, including conditionally.** *"Draw this while the count is at
  least two"* is evaluated in the client, so the condition ships as authored data and the answer
  never enters Lua. A threshold is a paint, not a branch.
- **Readable facts combine without limit.** Anything Lua may read may be ANDed, ORed and negated
  as freely as ordinary code, to reach an ordinary code decision.
- **Those decisions may aim a sealed widget.** cap does not need to know what a widget contains in
  order to place it, gate it, hide it or stack it — so combined readable logic decides *whether* and
  *where* a secret-driven mark appears, without ever learning the secret.
- **Widgets compose visually.** Two marks overlaid, adjacent or stacked express a relationship cap
  itself cannot evaluate: the compositor draws both, and the reading happens on screen.
- **So the last combining step may belong to the player's eye, and often should.** cap's job is to
  put the facts where the answer is obvious, not to compute the answer. A rule that will not reduce
  to one mark is usually still expressible as two.

- **Polarity is not the boundary — a sealed value may drive a POSITIVE paint.** A cue whose curve
  the client evaluates is legal in either direction, because the display does the reading: cap
  hands over a rule and a sink, the client decides whether the mark is opaque, and no value crosses
  back. So *"sealed-driven"* is a statement about **who evaluates**, not about which polarity may
  be drawn; a sealed positive cue is one secret with a fence of readable gates around it, exactly
  like a sealed negative one. §3.6 forbids cap **comparing** a secret, not showing one. *(Havoc's
  rung 2 is the first — `talent ∧ talent ∧ sealed-cooldown-range`, 2026-08-26. Nothing in
  `Channel`, `Catalog` or `Overlay` knows a cue's polarity when it arms a curve; what made this
  look forbidden was a doc habit — every prior positive cue happened to be readable — not a code
  constraint.)*

**And two things it does NOT permit, both discovered by trying.** These are limits of the *grammar*,
not of the platform, and neither is closed by a measurement:

- **A sealed display may assert an aura's PRESENCE. It may never assert its ABSENCE.** Presence
  draws by the container existing; absence draws nothing — and **nothing is indistinguishable from
  a refusal, a wrong spell id, or a display that never armed**. So *"this aura is up"* is
  expressible and *"this aura is down"* is not, and the pair is not symmetric however it is
  phrased. *(This is what separates Protection's Defeats 1 and 2: `!consecration.up` routes as a
  presence band, `buff.avenging_wrath.up` needs a boolean in a Lua condition and still owes one.
  It will separate the same pair in every future catalog.)*
- **A negative badge cannot say *"I am ranked below the rows to my right."*** A hold is binary and
  a scan is left-to-right, so a row whose rung sits *below* rows drawn to its right has no way to
  say so — releasing the hold makes it leftmost-and-clean and names the wrong button, while
  keeping it holds a press that is sometimes correct. ⚠ **Enumerating the outrankers in `when` is
  not a fix, and is unsound where the roster is incomplete:** Protection's rung 23 is outranked by
  a bare `hammer_of_wrath` that has **no roster row at all**, so a marker listing its outrankers
  would be blind to one of them and fire when that button is the press. *(Protection's Defeat 4.
  The honest exits are a per-marker rank or alternatives in `when` — `backlog.md` → Tooling.)*

**Be optimistic about carrying a priority list.** Most rules that look sealed-and-therefore-out-of-
reach turn out to be a readable gate plus a client-side paint, or two marks the player reads
together. Reach for those before concluding anything cannot be done — and when something genuinely
resists, record the *scenario* that defeated us, not a claim about the platform.

**These two data paths are properties of cap's *combat* context — not of the whole addon.** The
readable/sealed split above, and on the platform side the protected-action and taint rules the
client enforces in combat, govern cap's **evaluation path**: the in-combat, tainted context where
cap reads facts and paints. There cap is bound absolutely. cap also has a **setup path** — out of
combat, on an untainted execution path — where those restrictions do not hold: a Secret Value read
untainted is an ordinary value (`security-taint-and-restricted-data.md` §0), protected frames
accept `SetPoint`, and the Cooldown Manager's own layout is readable and writable. Frame
positioning, un-hiding rows, reading or writing CDM configuration, and any other arrangement work
live on the setup path and are judged by its rules, not the combat path's. **Ask which path a
mechanism runs on before applying that path's constraints** — a setup-time action is not made
illegal by a rule about combat, and combat-safety is not a test it has to pass. The setup path's
one discipline is **restore-on-exit**: cap records whatever it changes about the player's UI or
Blizzard's settings and reverts it when disabled, so the player is never left holding a state cap
made and does not own.

The first sealed form is **`sealed-count-bands`**: a declared aura dependency and a table of
breakpoints cap authored. Blizzard's AuraContainer evaluates the table against the application
count and writes the result into a FontString cap handed it — which may draw a number, a mark, a
hatch across the whole icon, or nothing at all. CAP may report only `offered`, `armed`, or
`refused`; it cannot report whether the secret-driven glyph appeared.

⚠ **This replaced `player-aura-stacks` on 2026-08-22, and the difference is the whole of it.**
That form declared a *minimum of two*, which read as a platform limit and is not one: `applications
> 1` is Blizzard's behaviour when **no formatter is passed**. Passing one replaces it with a
piecewise function cap authors, so a threshold anywhere, a complement, a fixed glyph and a
texture escape are all one form. And because a band may draw the hatch, **a sealed fact can now
ELIMINATE a row** rather than only decorate it — the third eliminating signal, beside Blizzard's
swipe and cap's own badge.

Two further count forms ride the same slot. **`sealed-count-bar`** drives a StatusBar from the
same sealed count (only `BarValue` is sealed, so the shape is cap's) and says *how far toward N*
where the bands say *yes or no* — at the cost of having **no blank state**.
**`sealed-pandemic`** is the odd one and the safest: `AddPandemicRegion` seals a Region's
`Shown` and drives it from the client's own per-spell refresh arithmetic, so cap authors **no
threshold at all**, and a Frame with children appears and vanishes whole.

The Havoc catalog (§3.7) adds two further sealed forms, and neither one lets Lua learn the
value it acts on:

- **Graded secret power** (`sealed-power-percent`). A secret primary resource cap cannot read
  — Havoc's Fury — is handed to the client with an authored **color curve**, and the client
  evaluates the curve against the secret value and paints the result. The authored break point
  (e.g. "would this generator overcap") is a static number baked into the curve, not a
  comparison cap performs. cap reports only that the curve was offered; it never learns the
  Fury value or which side of the break point it fell on.
- **Graded secret duration** (`sealed-cooldown-range`). A sealed remaining-duration is handed
  to the client with a **range curve**, and the client drives a texture's visibility from the
  result. This is how a sealed hold marker (above) is drawn without Lua reading the clock. It has
  **two senses, exactly one per marker**: `within` reads on while the remaining time sits inside
  an authored band ("it is nearly up, so wait for it"), and `beyond` reads on while at least that
  long is left ("it is nowhere near, so this is not its moment"). Both are the same step curve
  read at a different point, and in both a dependency that is *ready* reads nothing — a cooldown
  that has come back is neither imminent nor far away.

  ⚠ **Two sealed markers naming one cue is a union, and the union happens in the compositor.**
  Readable markers may share a badge because Lua ORs their results; sealed ones may not, because
  each writes that badge's visibility from its own curve and those values cannot be compared. Each
  sealed marker therefore owns an instance stacked at the same slot. The union pattern is not
  uniform across the two classes, and authoring a sealed pair as though it were readable produces
  a badge whose state depends on write order.

  **An AND of two sealed facts has no single-mark form yet.** A marker carries one curve and two
  sealed markers union rather than intersect, so *"X is far **and** Y is far"* is not one badge
  today. Both halves are expressible, and **drawing both is a working answer** — two marks appear
  together and the conjunction is read on screen. What is unsolved is folding them into one mark.
  That is an operator nobody has designed yet, not a limit the client imposes.

Both obey the same rule as the count forms: the value flows only into a client-owned sink,
CAP reports `offered` / `armed` / `refused`, and only an eyeball proves a pixel appeared.

**One secret per curve; readable gates without limit.** A sealed form carries exactly **one**
secret — that is what the client-owned sink can evaluate, and a second would be a second break
point. But the *condition under which the curve is offered at all* is ordinary Lua, so a graded
cue may be ANDed with as many **readable** facts as the rule needs: another ability's readiness,
a talent, affordability, one of cap's own toggles. The seal constrains what may be compared, not
how narrowly the comparison may be aimed.

The practical consequence is a diagnosis. **A graded cue that fires too eagerly is usually missing
a readable gate, not a better curve.** Havoc's charge cue is the worked example: it curves on the
one secret it must, and its correctness comes entirely from the readable terms beside it — the two
talents that create a charge worth losing, and the higher-priority cooldowns whose readiness means
the player should be pressing something else. Reach for the readable gate before anything
cleverer, and before concluding a rule is inexpressible.

A refused readable fact is **unknown**, not false. Unknown input produces no confident hint,
and negation never turns unknown into confidence.

The catalog contains only abilities cap enhances and only data forms the current renderer
supports. Unclaimed CDM rows may appear in diagnostics but are not authoring failures and need
no silence declarations. Unused or unwired vocabulary is not admitted in anticipation of a
future spec.

No catalog, no matching build, an unsafe read, or an unsupported binding all fail inert. The
capture names developer-actionable failures without turning them into player-facing noise.

### 3.7 Havoc Demon Hunter — the first comprehensive catalog

Demonology and Destruction **began** as deliberately tiny proofs; both were replaced by
comprehensive catalogs on 2026-08-19 (§3.4), so this section records where the standard came from
rather than a current difference between specs. Havoc is the first catalog authored
to be **comprehensive**: it covers the spec's whole rotational roster, because the pattern shelf
now exists and adding a spec is meant to be "which known recipes apply," not another tour of the
APIs. Comprehensive does not mean exhaustive of every button — it means every ability with a
*named player problem* gets a hint, and no problem is skipped for being awkward. A rule whose ordering-reason
is sealed is authored down §3.6's ladder — a readable gate plus a client-painted mark, or two marks
the player reads together — and only a rule the whole ladder fails to express is recorded as a
defeat, in the form `authoring.md` requires: the scenario, the rung that failed, and what would
reopen it.

**This catalog is Fel-Scarred, specifically.** A spec-and-hero pair is the unit cap authors, and
this one is Havoc / Fel-Scarred. Aldrachi Reaver is a **separate catalog authored later** — not
a second overlay bolted on here. We author Fel-Scarred first because it is the easier build to
pilot and the M+ pick, and hold the hero-tree call until Season 2 sims and logs exist
(post-2026-08-18); the AR catalog follows then. *(An earlier note here said the live Icy Veins
12.1 page leads Aldrachi Reaver. It does not — the page has one hero-filtered priority tool, and
selecting Fel-Scarred renders a Vengeful-Retreat-led list. The deferral rests on the absent Season
2 evidence alone, never on a guide preference.)*

Havoc's defining constraint is that its primary resource, **Fury, is secret** — cap can
display it but never branch on it. The roster reads the way the authoritative priority does:
the burst/window buttons (Metamorphosis, Eye Beam, The Hunt, Essence Break, Vengeful Retreat)
dominate the top of the list and are pressed on sight when nothing marks a hold, and the
build/spend core is the decision surface where the cues do the choosing. Four cues turn the
secret resource into that ordering; each is a recipe in `authoring.md`'s index, and the full mapping lives in
`specs/havoc/catalog.md`.

- **A — Affordability cue (readable).** Within the build/spend core, a Fury *spender* you can't
  afford is **dimmed**, while *generators* (no cost) stay lit in the scan — the eye is pulled
  toward building, with no Fury value ever compared. This is the inverse of Demonology's
  readable-Soul-Shards move.
- **B — Overcap cue (sealed).** A Fury readout on a generator that turns red once pressing it
  would waste Fury. cap cannot compute that in Lua (the arithmetic is on secret Fury); it hands
  the client a color curve whose authored break point is the overcap threshold, and the client
  paints it. Honestly approximate, and it says so.
- **C — Hold / sync marker.** A hold marker (§3.2) — "don't press this on cooldown yet." A
  **readable** hold, driven by a related ability's *readiness* (Metamorphosis — hold while Eye Beam
  or Death Sweep is ready, so its reset banks a cast), and a **sealed** hold, driven by a related
  ability's *remaining time* (hold Essence Break while Eye Beam's cooldown has ≤4s remaining, so the
  amp window is not clipped into Eye Beam; hold Metamorphosis while Eye Beam is ≤8s out, the sealed
  half of the same rule as its readable one; hold The Hunt while Metamorphosis is **close**, so its
  empower lands on the Eye Beam that Metamorphosis will reset — the APL *casts* The Hunt once
  Metamorphosis is ready, so this hold clears exactly where an earlier draft said it should fire).
  Both routes are single-state markers: they draw when the press should wait and draw nothing when
  it should not.
- **D — Demon-form promotion (readable).** Demon form is a readable fact (the transform
  identity), so while it is active cap may **promote** the empowered spenders — Annihilation and
  Death Sweep — because that is genuinely the moment to spend. This is emphasis following a
  readable fact (§3.1), and it is why the raw spender, low in the
  baseline priority, correctly rises inside its window. ⚠ **Currently authored but not drawn:**
  a promotion is a positive cue, and the shelf carries one — `priority` — but Havoc's catalog does
  not spend it here; the window still *explains* the ranking, it just
  gets no pixels of its own. Permission unchanged;
  only the shelf moved. Essence Break's and
  Demonsurge's windows would promote the same way *if* their active-state proves readable; that
  is an open in-client measurement, and until it resolves they inform through a marker, never a
  promotion.

The demon-form transform is also the readable **spine**: cap re-skins Chaos Strike→Annihilation,
Blade Dance→Death Sweep, Eye Beam→Abyssal Gaze and Immolation Aura→Consuming Fire across the
flip, keeping charge math correct when Immolation Aura changes id in demon form.

**Scenario catalog.** `specs/havoc/scenarios.md` walks the full Fel-Scarred priority (single-target
+ AoE, re-verified 2026-08-12) rung by rung. For each it names **why the press ranks there** (the
ordering-reason: reset relationship, demon-form window, charge cap, buff maintenance, Fury
threshold, elimination) and classifies how cap orders it — **readable rank / sealed cue (incl. an
authored Fury threshold, either polarity) / open**. It is the proof behind the §3.1 rules above, all
three of which were
lifted from the walk (the intensity hierarchy, elimination, and the dependency-graph /
readable-relationship rule). The headline finding: the Havoc order is *mostly a readable dependency
graph* — Metamorphosis leads because it resets Eye Beam and Death Sweep, and cap ranks it off Eye
Beam's readable cooldown state — and even the secret-Fury decisions are expressible: cap can't read
Fury, but it hands the client an authored threshold and lets it paint "banked" (Essence Break at
Fury ≥ 35, a positive S1 cue) or "about to cap" (the generator overcap readout), either polarity,
never reading the value. ⚠ **Expressible is not the same as
drawn:** `render-shelf.md` declares a cue vocabulary that is **negative by default**, and its two
positive cues — charges-capped (impending loss) and `priority` — are both driven by readable facts,
neither by a sealed threshold. So the positive half of *this* finding —
the "banked" light, and the demon-form promotion below — is authored and **parked**, not refuted. Which polarities get pixels is a shelf question and moves without touching
this section; that a threshold is expressible in either is the constitutional claim, and it
stands. The AoE
list adds no new cues — it re-weights via the player's AoE-mode input (§2), not a readable target
count. Cues still open (Inertia-proc rise, Demonsurge / Essence-Break window promotion, a
buff-maintenance marker) produce no hint until measured.

| Ability | Player problem | Treatment |
| --- | --- | --- |
| **Metamorphosis** | ~2 min burst whose payoff is its reset of Eye Beam + Death Sweep; pressing it while either is *ready* wastes that reset. | scan + a readable reset mark off Eye Beam's & Death Sweep's cooldowns (C1), drawn only when a reset would be wasted. |
| **Eye Beam** | Keep the demon-form window rolling — it enables everything downstream. | scan. |
| **The Hunt** | On cooldown, but hold if Metamorphosis is available (to buff Abyssal Gaze in the coming Meta window). | scan + a readable sync-hold mark off Meta's cooldown state (C1), drawn only while Meta is up. |
| **Essence Break** | Mandatory in S2; opens the amp window you flood with spenders. | scan + positive banked-Fury cue (B, expressible — currently **parked**, see above); sealed hold while Eye Beam's cooldown has ≤4s remaining (C2). |
| **Vengeful Retreat** | S2 maintain-on-cooldown press (Exergy / Initiative), woven before Eye Beam. | scan. |
| **Chaos Strike / Annihilation** | Shown castable even when Fury-starved, and it is the *low-priority* dump — except inside a window. | scan; dimmed when unaffordable (A); **promoted as Annihilation in demon form** (D). Re-skins across the flip. |
| **Blade Dance / Death Sweep** | The empowered Death Sweep is what you flood windows with; costs Fury. | scan; **promoted as Death Sweep in demon form** (D); demon-form identity. |
| **Felblade / Demon's Bite** | The generator to favor when starved — and the one that overcaps Fury when flush. | scan; stays lit when spenders dim (A); red Fury readout at the overcap break point (B). Felblade rises on a readable Inertia proc *if* measured. |
| **Immolation Aura / Consuming Fire** | The one Fury decision that matters: don't sit on capped charges. | scan; lit as "spend it" only when charges read full (readable-at-full), id-safe across the transform. |
| **Demon form** | "Am I in the window where spenders hit hard?" | A readable marker while transformed (drives cue D), plus an optional independent countdown surface (§3.3). |
| **Throw Glaive / Fel Rush** | Filler when nothing better is up. | scan. |
| **Fel-Scarred Demonsurge** | The hero-tree signature empowerment. | **OPEN** — no hint until an in-client check confirms the empowerment state is readable. |

Each row begins as a hypothesis judged by play, exactly as the pilots did. Rows whose gating
fact is still open (Demonsurge, the Inertia proc-glow, the Essence-Break-window promotion)
produce no hint until the in-client test named in `specs/havoc/catalog.md` resolves.

### 3.8 Chrome

Not everything cap draws is a hint. **Chrome tells you which row you are looking at; it asserts
nothing about pressing it.** The keybind hint is the whole category today — the key you have
actually bound to an ability, drawn small in a corner the cue vocabulary does not use
(`render-shelf.md` Part 1), so that "the third icon" and "the button under my ring finger" stop
being two thoughts.

It is placed here rather than inside §3.2 because it is a *peer* of emphasis and context markers,
not an exception to them. Every difference below is a rule of §3.1 or §3.2 that simply does not
reach it:

- **It is not a cue and not a marker.** It has no gating fact, so it has neither of §3.2's two
  forms — no `when` to be readable by, no `display` for the client to evaluate. The binding is an
  ordinary readable fact (§3.6) that drives no comparison: cap shows it and ranks nothing by it. It
  takes no badge, joins no cue vocabulary, and the elimination walk (§3.1, `render-shelf.md`
  Part 0.5) does not see it — a bound button is not thereby ruled in, and an unbound one is not
  ruled out. Were it otherwise, the reading gates would begin ranking rows on the basis of a
  keyboard layout.
- **It is not catalog-authored.** A marker is authored per ability by a spec's catalog; chrome
  applies to every row cap draws on every spec, and no catalog can add one or take one away.
- **Drawing nothing is legal for it.** §3.2's "a form that loads and then renders nothing is a
  defect" is a test on a marker's one declared state, and chrome has no state to be single. An
  ability you have not bound has no key to show, and blank is the complete answer. ⚠ **Never a
  placeholder** — an invented key is worse than an absent one. That holds equally for a key cap
  merely failed to find: the lookup is spell-keyed, so a slot holding a *macro* that casts the
  ability reads blank, and that is the shipped behaviour rather than a gap papered over.
- **It is always on.** That is not a settings decision. §2 says cap is opinionated and not
  configurable; there is no opinion here to configure, only a fact that is either available or
  absent.

The boundary it stays inside is §4's: cap *reads* a binding to label a row and owns none of them.
Nothing here sets, changes, or offers to change a binding, and the place to fix one is still
BucketBinds. What the hint looks like and where it sits are `render-shelf.md`'s (`tokens.hotkey`,
V15).

### 3.9 Row order

**The reading model has a precondition nothing else in this file states: the rows must actually
be in the catalog's order.** §3.1's whole scan — *"left to right, press the first thing not ruled
out"* — is a claim about position, and Blizzard's Cooldown Manager lays the Essential viewer out
in the player's own saved order, which has no relationship to a spec's priority. So cap
**re-anchors** that viewer's rows into the order its catalog authored.

It is on by default. There is no opinion here to configure — the order is the catalog's, and the
catalog is cap's — but the *placement* is the player's screen, so two controls exist:
`/cap anchor [on|off|retry|rows]` and the position of cap's own panel (`/cap move`).

Five properties are the whole of the promise, and each is a boundary rather than a feature:

- **It re-anchors, and only re-anchors.** The player's saved Cooldown Manager layout is never
  written. No row is added or removed, and none is hidden except under the parking rule below.
  Turn it off and the next layout pass restores Blizzard's order.
- **It orders the Essential viewer only** — which is the viewer the reading model walks. A row in
  any other viewer is untouched, and a scan edge there marks membership in a scan that does not
  happen (`discussion.md` carries the open question that follows from this).
- **It yields rather than fights.** Something else moving the same icons is a real possibility
  (another addon, or Blizzard's own layout engine). cap samples position, attributes a
  displacement it caused to itself, and treats a run of unattributable moves as **contention** —
  at which point it *asks the player*, out of combat, and stops only when told to. It never
  latches itself off silently, and it never opens a dialog mid-pull.
- **It holds through a pull.** Re-anchoring is a `SetPoint` on frames the Cooldown Manager does
  not protect, so combat lockdown does not govern it, and waiting for the pull to end was not
  free: a full aura update makes the viewer release its whole item-frame pool mid-fight, so a
  re-anchor that waited left the row in Blizzard's order for the rest of the pull while it still
  *read* as a priority scan. **The accepted cost is the other way round: an icon can move during
  a pull.** That is the trade — a row that is briefly unsettled over a row that is quietly wrong.
  The contention dialog is the one thing still held out of combat, because a question mid-pull is
  its own problem.
- **It parks a row it can no longer place.** An icon cap has moved, and can no longer say where
  in the order it belongs, is taken out of the row rather than left sitting inside it. This is
  the one case where cap hides something the player configured, and the argument for it is
  §3.1's: a row that keeps its full length while part of it is in nobody's order still reads as a
  priority scan, and a scan that is wrong is worse than a scan that is short. It is placement
  like the rest — the saved layout is untouched, the row is moved and not disabled, and turning
  ordering off restores every parked row with the next layout pass. cap parks a frame **it has
  claimed**; a row it never touched is never parked.

⚠ **This is the one place cap touches Blizzard's own frames rather than drawing beside them**,
which is why the yield rule is a product promise and not an implementation detail.

### 3.10 When cap draws nothing, and why the player is told

cap can be installed, enabled, and correct, and still draw nothing. Three states produce that,
and **all three are reportable through `/cap status`** — because a dark overlay and a working one
are visually identical on a row that happens to need no cue, so the screen alone can never
distinguish "nothing to say" from "broken".

- **Not bound.** No catalog entry reached a Cooldown Manager row: an unauthored spec (§2), or a
  viewer cap could not read. This is the designed inert case, not a failure.
- **Not settled.** cap has bound but is still waiting for the roster to stop changing. It clears
  on its own within seconds.
- **Dark for this fight.** ⚠ **If combat begins before the roster has settled, cap draws nothing
  for the entire pull** and resumes at combat end. This is deliberate: committing to a roster
  mid-pull would change what is emphasised while the player is in the middle of reading it, and a
  scan whose contents move under the eye is worse than no scan. The cost is a whole fight of
  nothing, so it is stated here rather than left as behaviour — a player who sees a blank pull
  must be able to find out that it was intended, and `/cap status` says so in those words.

## 4. What cap does not do

- It never presses, queues, macros or takes an action for the player.
- It does not automatically detect an opener or burst sequence and mark the current and next
  spell.
- It does not surface Blizzard's Assisted Combat recommendation as its own opinion.
- It is not a WeakAuras-style rule editor and does not accept user-authored priority packs.
- It does not replace the Cooldown Manager, and it does not write the player's saved Cooldown
  Manager configuration. It does **re-anchor** the Essential viewer's rows into the catalog's
  order while it is running, and **park** — move out of the row — one it has claimed but can no
  longer place (§3.9). Both are placement, neither touches the player's configuration, and both
  are reversible by turning ordering off.
- It does nothing on specs and builds without an authored experience.
- It does not own keybinds or action-bar layout; that is BucketBinds. It may *show* you the
  binding you already have (§3.8), which is a read and changes nothing.
- It supports Retail / Midnight only.

Combat Assist Plus supersedes the old Cooldown HUD product. Its measured client facts remain
in `knowledge/addon-dev/`; its decision-engine code is not carried forward.

## 5. Platform constraints

Secret Values and combat lockdown bound the implementation. The authoritative facts live in
`knowledge/addon-dev/`, not in this product spec.

- Secret Values decide which facts are readable and which may only be displayed through a
  client-owned sink.
- Combat lockdown decides when binding, placement and protected-frame work may happen.

The product consequence is §3.6. The source enforces that boundary and safe failure.

## 6. How a hypothesis becomes a feature

New hints begin as small hypotheses. Before a flight, state the player-experience question.
Play first and record the player's report in their own terms. Use captures afterward to
explain whether the authored mechanism ran and why the observed result may have happened.

Captures never overrule the player's visual judgment; **accepted is not drawn**
(`authoring.md` → *Accepted is not drawn*). Occupancy and refusal rates are diagnostics, not acceptance quotas.
