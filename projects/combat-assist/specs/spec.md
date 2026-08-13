# Combat Assist Plus — spec

**What this file is for:** what the addon is supposed to do. The product
definition, not the implementation. If you're about to build something and this
file doesn't say what it should do, the answer is to write it here first (or ask),
not to infer it from the code.

---

## 1. What it is

`/cap` — **Combat Assist Plus**, an addon that makes Blizzard's Cooldown Manager
tell you more without telling you what to press.

Blizzard's position on combat addons is that they should not be decision engines.
The 12.1 restrictions are that position expressed as code: an addon can *display*
your combat state but can't read it back to reason about it. Rather than fight
that, cap treats it as the design brief. **cap presents information you already
have, differently.**

**Three principles. Everything else in this file is downstream of them:**

- **a)** **cap does not fight the secret restrictions.** The gate/channel split
  (§3.6) already expresses this, and it is the one line worth enforcing in code.
- **b)** **cap freely uses non-secret information to give good hints.** Whatever the
  client hands an addon in the clear is fair material, and using it well is the job.
- **c)** **cap does not try to *always* present a single best decision.** This is
  distinct from "never present a single decision" and from "always present several
  options of equal status". Sometimes one option genuinely is best and the game hands
  us the data to say so — show it. Same for the inverse: sometimes everything is on
  cooldown and nothing is good, and that is worth showing too.

Underneath them, three moves, in order of preference:

1. **Re-present.** Take something the game already tells you and put it where you
   can actually use it — the right place on screen, the right size, the right
   moment.
2. **Grade.** Turn a yes/no signal into a *how much*. Blizzard's proc glow says
   "this is available." cap says "this is available, and right now it's worth
   about this much." A dim thing and a bright thing are the same information with
   a decision half-made by your eyes instead of by a rules engine.
3. **Contextualise.** Show what a moment *is* — an opener, a burst window, a
   cooldown coming back — so the choice you make is informed rather than made for
   you.

The central expression of move 2 is the **tier signal** (§3.1): every ability cap
has an opinion about carries a **role lane** — COOLDOWN, ROTATION, or FALLBACK —
and the cues (§3.2) order things within and across those lanes. Read together, tier
and cues put your presses in roughly the order an authoritative priority list would.
**How many are lit at any one moment is a property of the spec and the situation, not
a quota** — which is principle (c). Where the facts genuinely favor one option, cap may
layer emphasis and cues until that press is obvious; that convergence is the goal (§3.1),
not a banned "single winner." The only forbidden shape is a channel that *computes* the
answer for you (§4) — not the clarity that honest, layered, legal signals produce.

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

Section 1 wins over every detail below. A later rule that produces a next-action engine,
requires cap to branch on sealed data, or prevents a useful hint from readable data is invalid.

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

**Two tools, layered — convergence is the goal, not a violation.** cap says things two ways.
**Emphasis** is an on/off treatment driven by comparisons over values cap is *allowed to read*
(the lanes above, and readable markers). **Cues** are additive display forms fed by values cap
may *display but not read* — colors, readouts, hold marks, bars — that stack and move but are
never read back (§3.6). Author them together. Their combination will often make one button the
obvious press, and a well-built catalog reproduces the priority order exactly this way:
**that convergence is the point, not a rule to design around.** cap does **not** withhold
information it is legally allowed to show in order to keep the answer deliberately vague —
making the right press findable is the whole product.

The line cap does not cross is a **mechanism, not an outcome.** Forbidden is a single channel
whose job is to *compute* the answer and hand it over — an oracle that reads your state
(especially by working around the secret restrictions) and outputs one "press this." That is
the Assisted-Combat shape §4 rules out, and it is what branching on sealed data (§3.6) would
enable. Allowed — and wanted — is many honest, legal signals that happen to converge. So
"promoting the empowered spenders in demon form" is not "marking the next spell": it brightens
whatever a *readable* window genuinely favors — sometimes several buttons, sometimes one — and
the count is an outcome of the facts, never a quota cap imposes on itself. Because emphasis is
comparison-driven, it may be moved only by a readable fact; a window whose active-state is
sealed still informs, but through a cue (§3.2), never through emphasis.

An ability's lane is fixed by its role; whether it is *lit* depends on readable facts
(readiness, affordability). It has no emphasis when no condition holds or a required read is
unknown. Tier selection is discrete: the player reads lane and cues, not small brightness
differences within a lane's baseline.

**Emphasis has intensity, not just on/off.** For lane + cues to reproduce a priority order, "lit"
must **rank**: **promoted (a windowed spender) > lit COOLDOWN > lit ROTATION baseline > dim/off.**
The eye goes to the brightest. This is the mechanism by which tier and cues put presses in
priority order — a promoted spender inside a readable window out-shines a lit cooldown, which is
exactly why the empowered spender correctly outranks a ready cooldown in that window. The
intensities are discrete steps, not a continuous urgency number.

**Eye-direction by elimination.** A low-priority button is directed-to by the **absence** of
competing emphasis, not by a bright cue of its own. The default spender and the filler need no
signal — they win when they are the only lit button left. So cap does **not** over-light the
bottom of the list: the raw dump and the fallback carry no special brightness, and are correctly
found only when everything above them is dim or unlit. The same holds for a hold mark's absence —
an un-held, ready cooldown is directed-to precisely because the hold ✕ is *not* drawn.

**A priority list is a dependency graph, and emphasis may follow a readable *relationship*, not
only a button's own state.** An ability's place in the order is usually set by *why* it ranks
there — a reset it grants, a window it opens, a buff it maintains, a resource it needs — and that
reason often rests on the readable state of a *different* ability. Metamorphosis leads the Havoc
priority because it resets Eye Beam and Death Sweep; pressing it while those are on cooldown is the
high-leverage play, and cap can rank it because Eye Beam's cooldown state is readable (the hold cue
flips on exactly that). So emphasis is allowed to compare *related* readable facts — one ability's
cooldown against another's — not just each button's own readiness. This is still emphasis moved
only by readable facts; it is not a computed press.

This is also where the honest limit sits — and it is **narrower than "the ordering-reason is
secret."** "Tier plus cues reproduce the priority order" holds wherever the ordering-reason is
readable *or expressible as an authored threshold on a secret value.* A **threshold comparison is
not a branch cap performs**: cap hands the client an authored break point (the `sealed-power-percent`
/ S1 graded curve, §3.6) and the client evaluates the secret value against it and paints the result
— in **either polarity**. So "avoid this generator when the secret resource is about to cap"
(negative) *and* "this press is preferred once the secret resource is banked past a threshold"
(positive, e.g. Havoc's Essence Break at Fury ≥ 35) are both expressible sealed cues; cap authors
the number and never learns which side the value fell on. The one thing genuinely off-limits is cap
**computing** with the value — reading it into a Lua branch, score, or verdict, or combining several
secret values into one answer. That is the §4 oracle, forbidden by choice, not a wall the
restriction builds. A spec's catalog says, per rung, whether its ordering-reason is a readable rank,
a sealed threshold cue, or an unmeasured (open) cue — the "secret ⇒ cap is blind" framing is wrong.

These rules are spec-wide, not spec-specific; the Havoc scenario catalog (§3.7) is the first
document to walk a full priority list against them, rung by rung, and to mark each rung's
ordering-reason readable / sealed / secret-gated / open.

The baseline treatments are static and visibly distinct. Color, alpha, blend mode, size and
interaction with Blizzard's proc glow are tuning hypotheses until judged in the game. Motion
is added only to solve a specific observed problem.

An ability cap does not enhance remains visually untouched. cap does not dim the rest of the
Cooldown Manager merely to make its own signals look stronger.

### 3.2 Context markers

A marker adds a fact the player can combine with an emphasis; it does not collapse several
facts into a single verdict.

- A **readable marker** is driven directly by a fact Lua may read. It needs no sealed client
  half. Tyrant setup dots are the first example.
- A **sealed marker** is optional. The client may evaluate a sealed value and draw the result,
  but Lua never reads that value or branches on it. A catalog marker has exactly one form:
  readable `{ id, when }`, or sealed `{ id, display }`.
- A **hold marker** is context that says there is a reason to wait — "this is off cooldown,
  but there is a better moment coming." It is visually distinct from emphasis and does not
  silently turn an available ability into an unavailable one. A hold marker has the same two
  lanes as any other marker: its gating fact is either **readable** (Lua evaluates the wait
  condition and drives the marker directly) or **sealed** (the client evaluates a sealed value
  — a duration counting down inside an authored band — and draws the marker; Lua never reads
  or branches on that value). The Havoc catalog (§3.7) is the first user of both hold lanes.

Every supported marker has a visible implementation. A catalog form that loads successfully
and then renders nothing is a defect.

The initial marker shapes, colors and placement are provisional. The first flight asks
whether the player can identify the fact without consulting the catalog.

### 3.3 Tyrant cooldown experiment

One movable Tyrant countdown bar tests whether a larger surface adds information the CDM icon
cannot carry legibly. It is independent: it does not automatically inherit icon emphasis or
markers.

The client owns the remaining duration. cap may hand that duration to the bar but may not read
it back. Ready, counting-down and unreadable states must not be confused, and a capture may
report only which path cap armed—not what appeared on screen.

The bar is an experiment, not a required surface for every cooldown. It remains only if play
shows that it earns the extra screen space.

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
in-combat `napkin`; the player surface does not claim exactness beyond availability.

### 3.6 Safety boundary

The implementation distinguishes two data paths:

- **Readable facts** may enter Lua conditions and drive emphasis or markers.
- **Sealed facts** may flow only into client-owned display sinks. They never enter a Lua
  condition, comparison, score or verdict.

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
- **Graded secret duration** (`sealed-duration-range`). A sealed remaining-duration is handed
  to the client with a **range curve** that reads on only while the remaining time sits inside
  an authored band, and the client drives a texture's visibility from the result. This is how a
  sealed hold marker (above) is drawn without Lua reading the clock.

Both obey the same rule as `player-aura-stacks`: the value flows only into a client-owned sink,
CAP reports `offered` / `armed` / `refused`, and only an eyeball proves a pixel appeared.

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
*named player problem* gets a hint, and no problem is skipped for being awkward. Nothing here
overrides §1; a row that would require branching on a sealed value, or that would collapse the
rotation into one next press, is not authored.

**This catalog is Fel-Scarred, specifically.** A spec-and-hero pair is the unit cap authors, and
this one is Havoc / Fel-Scarred. Aldrachi Reaver is a **separate catalog authored later** — not
a second overlay bolted on here. ⚠ *Mismatch to note, not to act on yet:* the live Icy Veins
12.1 page leads **Aldrachi Reaver** for single-target while we author Fel-Scarred first (it is
the easier build to pilot and the M+ pick). We hold that call until Season 2 sims/logs exist
(post-2026-08-18); the AR catalog follows then.

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
  **readable** hold (hold Metamorphosis while Eye Beam is ready and you are not yet transformed,
  so Meta's Eye Beam reset banks a second cast) and a **sealed** hold (hold The Hunt while an
  Essence Break amp window is still counting down).
- **D — Demon-form promotion (readable).** Demon form is a readable fact (the transform
  identity), so while it is active cap **promotes** the empowered spenders — Annihilation and
  Death Sweep brighten within ROTATION — because that is genuinely the moment to spend. This is
  emphasis following a readable fact, not a computed "press this" (§3.1), and it is why the raw
  spender, low in the baseline priority, correctly rises inside its window. Essence Break's and
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
never reading the value. The only thing off-limits is *computing* the answer from Fury — the §4
oracle cap forbids by choice, not the secret restriction. The AoE
list adds no new cues — it re-weights via the player's AoE-mode input (§2), not a readable target
count. Cues still open (Inertia-proc rise, Demonsurge / Essence-Break window promotion, a
buff-maintenance marker) produce no hint until measured.

| Ability | Player problem | Lane + cues |
| --- | --- | --- |
| **Metamorphosis** | ~2 min burst; pressing it while Eye Beam is up wastes its Eye Beam reset. | **COOLDOWN** + readable hold while Eye Beam is ready and you are not transformed (C). |
| **Eye Beam** | Keep the demon-form window rolling — it enables everything downstream. | **COOLDOWN**. |
| **The Hunt** | On cooldown, but not inside an Essence Break window. | **COOLDOWN** + sealed hold while the Essence Break window counts down (C). |
| **Essence Break** | Mandatory in S2; opens the amp window you flood with spenders. | **COOLDOWN**; supplies The Hunt's hold window. |
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
  spell. A future sequence idea must first show how it informs a choice rather than choosing
  the next press. (Brightening whatever a live **readable** window genuinely favors — e.g. the
  empowered spenders in demon form — is not this: it follows a current fact, does not *compute*
  the answer for you, and lights however many buttons the fact favors. §3.1.)
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

The product consequence is §3.6. The source may enforce that boundary and safe failure. It
must not turn provisional gameplay or visual opinions into platform rules.

## 6. How a hypothesis becomes a feature

New hints begin as small hypotheses. Before a flight, state the player-experience question.
Play first and record the player's report in their own terms. Use captures afterward to
explain whether the authored mechanism ran and why the observed result may have happened.

Captures never overrule the player's visual judgment and never reveal what a sealed sink drew.
Occupancy and refusal rates are diagnostics, not acceptance quotas. A green unit suite means
the engine obeys its mechanical and platform contracts; it does not prove that a gameplay
opinion is useful or a treatment looks good.
