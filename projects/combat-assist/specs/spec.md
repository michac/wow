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

The central expression of move 2 is the **tier signal** (§3.1): every ability cap
has an opinion about carries a **role lane** — COOLDOWN, ROTATION, or FALLBACK —
and the cues (§3.2) order things within and across those lanes. Read together, tier
and cues put your presses in roughly the order an authoritative priority list would.
Where the facts genuinely favor one option, cap layers emphasis and cues until that
press is obvious; making the right press findable is the product.

cap is **opinionated, not configurable**. You get recommendations derived from
your class and spec, chosen by us. It is deliberately not WeakAuras: there is no
trigger editor, no condition builder, no library of user-made packs. If cap's
opinion about your spec is wrong, the fix is to change cap's opinion, not to
expose a slider.

It **rides on the Cooldown Manager** rather than replacing it. The CDM already
knows what your spec cares about and already draws it legally. cap binds to it,
skins it, and extends past its edges where the icons are too small to carry what's
needed.

## 2. Scope

cap is built for the author first and may be published later. It has chosen defaults and no
settings panel. The player may move its independent surface and set single-target or AoE mode;
those are inputs, not a way to rewrite cap's opinions.

Specs are added one at a time. The first pilot is Demonology Warlock / Diabolist. A spec or
build cap has not deliberately authored is completely inert: no generic recommendations, no
fallback skin and no guesses.

cap is meant to work in the restrictive case—combat, instances and PvP—not only on a target
dummy in a city. Out of combat it is quiet apart from setup controls.

## 3. What the player sees

One precedence rule, and it is about the platform: **a rule that would require cap to branch on
sealed data is invalid**, wherever it is written. That boundary is §3.6's, the client enforces it,
and `Catalog.lua` / `Channel.lua` hold it in code. Everything else below is an ordinary detail —
if it is wrong, edit it.

### 3.1 Emphasis

cap assigns one of three discrete **emphasis tiers** to an ability it has a useful opinion
about. The tiers name the ability's **role**, not a raw urgency number:

- **COOLDOWN** — a cooldown, burst button, or window-opener (Metamorphosis, Eye Beam, The
  Hunt, Essence Break, Vengeful Retreat).
- **ROTATION** — the build/spend core you cycle between, where there is a reason to favor one
  over another right now (Chaos Strike/Annihilation, Felblade, Blade Dance/Death Sweep,
  Immolation Aura). The cues (§3.2) do the choosing *within* this lane.
- **FALLBACK** — a reasonable filler when nothing better is available (Throw Glaive, Fel Rush).

The lanes are the **coarse structure**; the cues carry the fine ordering. COOLDOWN is the
highest baseline and FALLBACK the lowest, but a lane is not a strict priority — a ROTATION
button inside a live window can outrank a lit COOLDOWN, and that is exactly what the cues
express. This is the point of the whole tiering: **tier plus cues, read together, put your
presses in roughly the order an authoritative priority list would** — which is why the player
still reads the cues rather than blindly pressing the top lane.

**Two tools, layered.** cap says things two ways. **Emphasis** is an on/off treatment driven by
comparisons over values cap is *allowed to read* (the lanes above, and readable markers).
**Cues** are additive display forms fed by values cap may *display but not read* — colors,
readouts, hold marks, bars — that stack and move but are never read back (§3.6). Author them
together; a well-built catalog reproduces the priority order by layering the two.

Because emphasis is comparison-driven, it may be moved only by a **readable** fact. A window
whose active-state is sealed still informs, but through a cue (§3.2), never through emphasis.
That is the §3.6 boundary, and it is the only thing this section constrains.

An ability's lane is fixed by its role; whether it is *lit* depends on readable facts
(readiness, affordability). It has no emphasis when no condition holds or a required read is
unknown.

**Emphasis has intensity, not just on/off.** For lane + cues to reproduce a priority order, "lit"
must **rank**: **promoted (a windowed spender) > lit COOLDOWN > lit ROTATION baseline > dim/off.**
The eye goes to the brightest. This is the mechanism by which tier and cues put presses in
priority order — a promoted spender inside a readable window out-shines a lit cooldown, which is
exactly why the empowered spender correctly outranks a ready cooldown in that window. *How* that
ladder is drawn — brightness, hue, motion, thickness, or several at once — is a
`render-shelf.md` question.

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
secret."** "Tier plus cues reproduce the priority order" holds wherever the ordering-reason is
readable *or expressible as an authored threshold on a secret value.* A **threshold comparison is
not a branch cap performs**: cap hands the client an authored break point (the `sealed-power-percent`
/ S1 graded curve, §3.6) and the client evaluates the secret value against it and paints the result
— in **either polarity**. So "avoid this generator when the secret resource is about to cap"
(negative) *and* "this press is preferred once the secret resource is banked past a threshold"
(positive) are both expressible sealed cues; cap authors the number and never learns which side the
value fell on. ⚠ The positive direction is **specified but has no live instance**: the vocabulary's
one positive cue reports a charge being lost, which is readable rather than sealed. An earlier
example here — Essence Break at Fury ≥ 35 — was deleted when the 12.1 APL turned out to put no Fury
term on Essence Break at all. What the platform does not allow is cap
**computing** with the value — reading it into a Lua branch, score, or verdict. A spec's catalog
says, per rung, whether its ordering-reason is a readable rank, a sealed threshold cue, or an
unmeasured (open) cue — the "secret ⇒ cap is blind" framing is wrong.

These rules are spec-wide, not spec-specific; the Havoc scenario catalog (§3.7) is the first
document to walk a full priority list against them, rung by rung, and to mark each rung's
ordering-reason readable / sealed / secret-gated / open.

**Every visual choice below the lane model belongs to `render-shelf.md`** — treatments, color,
alpha, blend mode, size, motion, placement, and how cap coexists with Blizzard's stock proc glow.
None of them are settled here, and changing one there is a normal edit, not a spec amendment.
What this section fixes is only the *model*: three role lanes, driven by readable facts, that must
rank.

### 3.2 Context markers

A marker adds a fact the player can combine with an emphasis; it does not collapse several
facts into a single verdict.

- A **readable marker** is driven directly by a fact Lua may read. It needs no sealed client
  half. Tyrant setup dots are the first example.
- A **sealed marker** is optional. The client may evaluate a sealed value and draw the result,
  but Lua never reads that value or branches on it. A catalog marker has exactly one form:
  readable `{ id, when }`, or sealed `{ id, display }`.
- A **hold marker** is context that says there is a reason to wait — "this is off cooldown,
  but there is a better moment coming." A hold marker has the same two
  lanes as any other marker: its gating fact is either **readable** (Lua evaluates the wait
  condition and drives the marker directly) or **sealed** (the client evaluates a sealed value
  — a duration counting down inside an authored band — and draws the marker; Lua never reads
  or branches on that value). The Havoc catalog (§3.7) is the first user of both hold lanes.

Every supported marker has a visible implementation. A catalog form that loads successfully
and then renders nothing is a defect.

⚠ **That test only works if a marker is single-state.** A marker authored as a *pair* — one
appearance for "wait", another for "go" — makes "it rendered nothing" ambiguous: it could be the
defect above, or it could be the satisfied state behaving correctly. So a marker declares the one
condition under which it draws, and its absence is the other condition. That is not a new rule;
it is what makes this one testable. (The render shelf spends this on a cue vocabulary that is
negative **by default** — a marker draws when the press is ruled out and never otherwise — with a
single scoped positive exception for impending loss. The single-state requirement stands whichever
polarity a marker is authored in.)

Marker shapes, colors, sizes and placement are `render-shelf.md`'s, not this section's. The
question a flight asks is whether the player can identify the fact without consulting the
catalog; the answer changes the shelf.

### 3.3 Tyrant cooldown experiment

One movable Tyrant countdown bar tests whether a larger surface adds information the CDM icon
cannot carry legibly. It is independent: it does not automatically inherit icon emphasis or
markers.

The client owns the remaining duration. cap may hand that duration to the bar but may not read
it back. Ready, counting-down and unreadable states must not be confused, and a capture may
report only which path cap armed—not what appeared on screen.

The bar is an experiment, not a required surface for every cooldown; play decides whether it
stays.

### 3.4 Demonology pilot

The first pilot is deliberately small:

| Ability | Player problem | Initial hypothesis |
| --- | --- | --- |
| **Demonbolt** | Blizzard's proc glow says available even when using the proc would waste readable Soul Shards. | Put a live proc in ROTATION; use the readable shard count as a cue that dims it where spending the proc would overcap shards. Exact threshold and stock-glow handling are chosen through play. |
| **Summon Demonic Tyrant** | Readiness alone does not show whether familiar setup pieces are present. | Put a ready Tyrant in COOLDOWN. Add separate readable markers for Dreadstalkers and Grimoire setup facts; do not combine them into a single verdict. |
| **Tyrant bar** | The icon may be too small to make the next burst window legible. | Test one independent countdown bar as described in §3.3. |

Everything else begins absent. An ability is added only after naming the player problem its
hint solves. Gameplay facts come from authoritative rotation sources; usefulness comes from
play.

### 3.5 Destruction authoring proof

Destruction / Diabolist is the second deliberately small catalog. It enhances only
Conflagrate and adds Backdraft as an independent context dependency:

| Ability | Player problem | Initial hypothesis |
| --- | --- | --- |
| **Conflagrate** | Its native count and swipe do not add readable Soul Shard context. Exact charges seal once recharge begins. | From an exact out-of-combat seed, put an estimated available charge in ROTATION, with the readable shard count as a cue that dims it above four shards. Withhold the tier when the estimate is zero or unknown. |
| **Backdraft** | The native aura count may be away from the Conflagrate row where the choice is made. | Let Blizzard display the application count at two stacks as independent context. It does not change Conflagrate's tier and does not encode press or hold. |

The charged-readiness estimate is intentionally small: exact current/max/recharge seed out of
combat, successful player casts as debits, and accepted `ChargeGained` alerts as credits. It
is clamped and re-seeded when combat ends. Captures distinguish exact `live` state from the
in-combat `napkin`.

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

The first sealed form is `player-aura-stacks`: a declared player-aura dependency and a
minimum of two. Blizzard's AuraContainer writes the application text directly into a static,
outlined FontString. CAP may report only `offered`, `armed`, or `refused`; it cannot report
whether the secret-driven glyph appeared.

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

Both obey the same rule as `player-aura-stacks`: the value flows only into a client-owned sink,
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

Demonology and Destruction were deliberately tiny proofs. Havoc is the first catalog authored
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
display it but never branch on it. The roster maps onto the §3.1 lanes the way the authoritative
priority does: the **COOLDOWN** lane (Metamorphosis, Eye Beam, The Hunt, Essence Break, Vengeful
Retreat) carries the burst/window buttons that dominate the top of the priority list, and the
**ROTATION** lane (the build/spend core) is where the cues do the choosing. Four cues turn the
secret resource into that ordering; each is a pattern-shelf recipe, and the full mapping lives in
`specs/havoc/catalog.md`.

- **A — Affordability cue (readable).** Within ROTATION, a Fury *spender* you can't afford is
  **dimmed**, while *generators* (no cost) stay at full ROTATION emphasis — the eye is pulled
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
  Both lanes are single-state markers: they draw when the press should wait and draw nothing when
  it should not.
- **D — Demon-form promotion (readable).** Demon form is a readable fact (the transform
  identity), so while it is active cap may **promote** the empowered spenders — Annihilation and
  Death Sweep — because that is genuinely the moment to spend. This is emphasis following a
  readable fact (§3.1), and it is why the raw spender, low in the
  baseline priority, correctly rises inside its window. ⚠ **Currently authored but not drawn:** a
  promotion is a positive cue, and the shelf's one positive cue is spent elsewhere (on impending
  loss, which no negative phrasing can carry) — the window still *explains* the ranking, it just
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
drawn:** `render-shelf.md` declares a cue vocabulary that is **negative by default**, and spends
its one positive slot on charges-capped (impending loss). So the positive half of *this* finding —
the "banked" light, and the demon-form promotion below — is authored and **parked**, not refuted. Which polarities get pixels is a shelf question and moves without touching
this section; that a threshold is expressible in either is the constitutional claim, and it
stands. The AoE
list adds no new cues — it re-weights via the player's AoE-mode input (§2), not a readable target
count. Cues still open (Inertia-proc rise, Demonsurge / Essence-Break window promotion, a
buff-maintenance marker) produce no hint until measured.

| Ability | Player problem | Lane + cues |
| --- | --- | --- |
| **Metamorphosis** | ~2 min burst whose payoff is its reset of Eye Beam + Death Sweep; pressing it while either is *ready* wastes that reset. | **COOLDOWN** + a readable reset mark off Eye Beam's & Death Sweep's cooldowns (C1), drawn only when a reset would be wasted. |
| **Eye Beam** | Keep the demon-form window rolling — it enables everything downstream. | **COOLDOWN**. |
| **The Hunt** | On cooldown, but hold if Metamorphosis is available (to buff Abyssal Gaze in the coming Meta window). | **COOLDOWN** + a readable sync-hold mark off Meta's cooldown state (C1), drawn only while Meta is up. |
| **Essence Break** | Mandatory in S2; opens the amp window you flood with spenders. | **COOLDOWN** + positive banked-Fury cue (B, expressible — currently **parked**, see above); sealed hold while Eye Beam's cooldown has ≤4s remaining (C2). |
| **Vengeful Retreat** | S2 maintain-on-cooldown press (Exergy / Initiative), woven before Eye Beam. | **COOLDOWN**. |
| **Chaos Strike / Annihilation** | Shown castable even when Fury-starved, and it is the *low-priority* dump — except inside a window. | **ROTATION**; dimmed when unaffordable (A); **promoted as Annihilation in demon form** (D). Re-skins across the flip. |
| **Blade Dance / Death Sweep** | The empowered Death Sweep is what you flood windows with; costs Fury. | **ROTATION**; **promoted as Death Sweep in demon form** (D); demon-form identity. |
| **Felblade / Demon's Bite** | The generator to favor when starved — and the one that overcaps Fury when flush. | **ROTATION**; stays lit when spenders dim (A); red Fury readout at the overcap break point (B). Felblade rises on a readable Inertia proc *if* measured. |
| **Immolation Aura / Consuming Fire** | The one Fury decision that matters: don't sit on capped charges. | **ROTATION**; lit as "spend it" only when charges read full (readable-at-full), id-safe across the transform. |
| **Demon form** | "Am I in the window where spenders hit hard?" | A readable marker while transformed (drives cue D), plus an optional independent countdown surface (§3.3). |
| **Throw Glaive / Fel Rush** | Filler when nothing better is up. | **FALLBACK**. |
| **Fel-Scarred Demonsurge** | The hero-tree signature empowerment. | **OPEN** — no hint until an in-client check confirms the empowerment state is readable. |

Each row begins as a hypothesis judged by play, exactly as the pilots did. Rows whose gating
fact is still open (Demonsurge, the Inertia proc-glow, the Essence-Break-window promotion)
produce no hint until the in-client test named in `specs/havoc/catalog.md` resolves.

## 4. What cap does not do

- It never presses, queues, macros or takes an action for the player.
- It does not automatically detect an opener or burst sequence and mark the current and next
  spell.
- It does not surface Blizzard's Assisted Combat recommendation as its own opinion.
- It is not a WeakAuras-style rule editor and does not accept user-authored priority packs.
- It does not replace or configure the Cooldown Manager.
- It does nothing on specs and builds without an authored experience.
- It does not own keybinds or action-bar layout; that is BucketBinds.
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
(`pattern-shelf.md` Part 2). Occupancy and refusal rates are diagnostics, not acceptance quotas.
