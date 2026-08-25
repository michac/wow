# Havoc Demon Hunter (Fel-Scarred) — the scenario catalog

**What this file is for.** `catalog.md` maps every ability to a role lane and the seven cues.
This file proves that lane + cues actually **reproduce the priority order** — scenario by
scenario. It walks the **Tier-1 simc action priority list** for 12.1
(`knowledge/classes/demon-hunter/havoc/simc-apl.md`) and, for each realistic game state, models
**what the player actually sees in the Cooldown Manager** and **why the eye lands on the one
press the rotation would choose**.

> **The model: a single CDM row, walked left-to-right.** The Cooldown Manager shows one
> priority-ordered row of your tracked abilities. The player scans it left-to-right and presses
> the first ability that isn't ruled out. So each scenario below is that row in a specific state,
> and the walk names — for **every ability that is *not* on cooldown** — the reason it is skipped,
> until we reach the press. An ability already on cooldown is ruled out by the CDM natively (the
> swipe); it needs no explanation. The interesting work is the **available-but-skipped** buttons:
> that is exactly where cap's cues (or the honest gaps) do their job.

The priority is not a flat power list where cap lights the field and the player guesses the top.
It is a **dependency graph**: each press's rank is set by *why* it belongs there — a reset it
grants, a window it opens, a buff it maintains, a resource it needs — and that reason usually
rests on the readable state of some ability, sometimes a *different* ability. Metamorphosis ranks
high because it **resets** Eye Beam and Death Sweep, so cap ranks it off *their* cooldown state,
not its own. Walking the list this way forces out (a) the **skip-reason** behind every rung and
whether cap can express it, (b) the **complete** cue set comprehensive coverage needs, (c) the
**gaps** — cues we would need but have not measured, and (d) the three general principles now
lifted into the constitution (`../spec.md` §3.1). This is a design characterization for play,
not a claim the order is universally correct.

## ⚠ Stated once: the sim has perfect information and no legs

Every rung cited below comes from a simulator. It models neither movement nor mechanics, its
dummy never leaves melee range, and it always knows what is coming. So **absent from the APL ≠
irrelevant in play**, and no scenario below may be read as saying otherwise. 12.1 deleted all
eight Fel Rush lines and all four Throw Glaive lines from the damage priority; what that says is
*"no longer worth a global cooldown as damage"*, not *"useless"*. Demon's Bite's absence is a
third thing again — the sim's build takes **Demon Blades**, which replaces the button with a
passive, so there is no button to press at all.

**Icy Veins is corroboration, not authority.** It agrees with the APL through the entire middle
of the list and on Essence Break's `>4`; where it is cited below it is cited as confirmation.
Where the two disagreed, the APL won and `catalog.md`'s changelog records what changed.

**Cross-links.** Constitution: `../spec.md` §3.1 (the emphasis-intensity hierarchy + the
elimination principle live there now) and §3.7 (the Havoc product section, which points here).
Normative roster + the seven cues: `catalog.md` (beside this file). Fact safety lanes:
`fact-classification.md`. Priority source: `knowledge/classes/demon-hunter/havoc/simc-apl.md`
(Tier 1, generated); `knowledge/classes/demon-hunter/havoc/rotation.md` augments it.

> **Fel-Scarred, specifically.** Aldrachi Reaver is a separate catalog authored later. It
> *inserts* a button (`reavers_glaive`, rung 9) rather than reordering the shared nine, which is
> what makes a later one-catalog merge viable.

---

## How to read a scenario

Every scenario is the **same twelve-icon CDM row**, in priority order, in a different state:

```
 Vengeful Retreat · Metamorphosis · The Hunt · Eye Beam · Essence Break · Blade Dance ·
 Immolation Aura · Chaos Strike · Felblade · Demon's Bite · Fel Rush · Throw Glaive
```

The first **nine** are the 12.1 damage priority. The last three — **Demon's Bite, Fel Rush,
Throw Glaive** — are a tail: they still render if the player tracks them, and they carry no
verdict beyond `open`.

Each icon carries a **walk verdict** — one of a closed vocabulary of five. A verdict says what cap
has concluded about that button; it does **not** say what the button looks like. **The pixels are
`../render-shelf.md`'s**, and every scenario below renders from its token block, so a treatment
changes by editing the shelf, never by editing this file.

⚠ **`press` and `open` render identically.** Both draw a plain scan edge and nothing else,
because under the shelf's reading model *the press is not something cap draws* — it is whatever
an unobstructed left-to-right scan reaches first. `press` is kept because this file needs it to
state its falsifiable claim; everything an `open` row says beyond membership is in its explicit
`{cues: …}` group. *(The 2026-08-25 collapse folded `press-promoted` into `press` — the
promotion is the positive cue on the row, which pass 1 already reads — and `below` into `open`:
"right of the press" is a position, not a state.)*

⚠ **A `blocked` badge has two routes, and they render identically** — that is correct: a hold
is a hold. The distinction is entirely on cap's side. A readable hold is a Lua condition over a
cooldown *state*; a sealed hold is a curve cap hands the client, which paints it against a
*remaining time* cap never sees. The practical consequence is verification: cap reports that it
**offered** a sealed rule, never whether the badge lit, so a sealed hold is confirmed by eye in
game rather than by a capture.

⚠ **And `capart check` enforces the reading model — both passes of it.** The model itself is
`../render-shelf.md` Part 0.5's two-pass operator heuristic, which is the authority; this file
does not restate it. What the gates assert for every scenario below is that it reads correctly
under that procedure:

- **Pass 1 (the positive cue).** If a scenario wears a positive cue, the leftmost entry wearing
  one must be the press — a positive cue is pre-emptive, so it may not point elsewhere.
- **Pass 2 (elimination), *otherwise*.** The leftmost entry that is neither swiped nor carrying a
  **negative** cue must be the entry this file calls the press (`weave` skipped, since it is off
  the GCD).

⚠ **It is a chain, and the word *otherwise* is load-bearing.** Each scenario is judged by the one
pass a reader would actually reach: a row wearing the positive cue answers to pass 1, every other
row to pass 2. Until 2026-08-17 `capart check` ran both on every scenario, so both had to name the
same press — which made *pass 1 overriding elimination* unrepresentable, and that override is the
entire reason a positive cue exists. ST-10 is the case.

All fourteen pass. A scenario that fails its pass fails **by name**, and a second declared positive
cue fails `check` outright, since pass 1 does not say how two of them would rank.

⚠ **One positive cue exists** (`capped`, ST-10). No scenario relies on it to *reach* its press by
elimination; it carries a fact — *you are wasting a charge right now* — that elimination
structurally cannot carry, because elimination expresses rank and that fact is about loss.

| Verdict | What cap concluded | Whose signal |
| --- | --- | --- |
| `cd` | on cooldown — ruled out natively, no cap opinion | Blizzard CDM (not a cap signal) |
| `weave` | off the GCD: pressed *alongside* the GCD press, never instead of it | readiness (R2) |
| `ruled-sealed` | ruled out by a band the CLIENT evaluated against a secret | the sealed count sink (unused in this catalog) |
| `open` | shown, in the scan; every finer statement is an explicit `{cues: …}` badge — `blocked` C1/G (readable) or C2 (sealed), `starved` A (readable, R1), `overcap` B (sealed, S1) | the named cue |
| `press` | the first available button with no skip-reason — the chosen press | elimination of everything above it, or the positive cue pass 1 reads |

The walk stops at the press. Buttons to its right are lower priority and are not evaluated; they
render, but carry no verdict beyond `open`. **Vengeful Retreat is the exception** — it is off the
GCD, so it is "pressed" in parallel and the walk continues past it to find the GCD press.

### The **CDM row** bullet is machine-read

Every scenario carries one `- **CDM row.**` bullet, and `wowkb.capart` parses it to render the
preview — so it is written in a fixed grammar rather than prose:

```
- **CDM row.** <Ability> `<verdict>` [{cues: <cue>, …}] · <Ability> `<verdict>` · …
```

The ability name is the one the client would *show* — so a demon-form scenario writes
**Death Sweep**, not Blade Dance, and the preview draws that icon (R7 resolves the live
`overrideSpellID`; cap authors none of it). A `cues` group names corner-badge cues by their
`../render-shelf.md` key.

⚠ **The cue vocabulary is negative by default**, so a group almost always appears on a button that
is ruled out, and a satisfied dependency draws **nothing** — there is no `go` state to write. The
one exception is `capped` (ST-10), the vocabulary's single positive cue: it reports **impending
loss**, which is urgent regardless of rank, so it may ride a button that is *not* ruled out —
including the press itself. `capart`'s elimination gate counts **negative** cues only, precisely so
that cue cannot eliminate its own button. (The retired
`{dots: X go|wait}` grammar is rejected by name if it reappears: `capart` errors rather than
silently ignoring it, because a silently-ignored group would let this file keep asserting a cue the
style no longer draws.)

`wowkb.capart check havoc` re-scrapes these bullets and fails if they disagree with the generated
preview's sidecar — this file leads, the preview follows.

### What the CDM shows in demon form (the override fidelity)

cap does **not** author these overrides. The demon-form identity is **readable** (R7): the addon
resolves the live `overrideSpellID` and the row shows exactly what the client shows. The
scenarios depict the expected live state:

| Base button | In an Eye-Beam demon-form window | In Metamorphosis (Fel-Scarred / Demonic Intensity) |
| --- | --- | --- |
| Blade Dance | **Death Sweep** | **Death Sweep** |
| Chaos Strike | **Annihilation** | **Annihilation** |
| Eye Beam | Eye Beam | **Abyssal Gaze** |
| Immolation Aura | Immolation Aura | **Consuming Fire** |

So a Metamorphosis scenario's row reads *Abyssal Gaze · … · Death Sweep · Consuming Fire ·
Annihilation*, and an Eye-Beam-window scenario shows *Death Sweep · Annihilation* but still *Eye
Beam* and *Immolation Aura*. (⚠ The Eye-Beam-window-vs-Meta split of the Abyssal Gaze / Consuming
Fire override is a **display-fidelity** expectation to confirm in-client; R7 renders whatever is
live regardless, so cap is correct either way — it only affects which icon a scenario should
*draw*.)

---

## The three general principles this walk proved (now `../spec.md` §3.1)

The walk does not just list cues — it establishes *how* tier + cues reproduce an APL, and where
they cannot. Three rules fell out that are **spec-wide**, not Havoc-specific, and are now normative
in the constitution:

1. **A priority list is a dependency graph; emphasis may follow a readable *relationship*, not
   only a button's own state.** A press's rank is set by *why* it belongs there, and that reason
   often rests on a *related* ability's state. cap may compare those — one ability's cooldown
   against another's — and still be moving emphasis only by readable facts, not computing a
   press. **ST-1/ST-3** are the archetype: Metamorphosis is "go" or "wait" entirely off its reset
   targets' state, shown as a dependency **mark** that draws only when the reset would be wasted.
2. **Emphasis has intensity, not just on/off.** To reproduce the order, "lit" must rank:
   **promoted (a windowed spender) > lit COOLDOWN > lit ROTATION baseline > dim/off.** The eye
   goes to the brightest — several scenarios are only correct because a promoted spender
   out-shines a lit cooldown (**ST-6**).
3. **Eye-direction by elimination.** A low-priority button is directed-to by the **absence** of
   competing emphasis, not by a bright cue of its own. The default spender and the filler need no
   signal; they win when they are the only button the walk reaches (**ST-0**, **ST-9**,
   **ST-12**). The procedure a reader actually runs is `../render-shelf.md` Part 0.5's two passes,
   and that file is the authority for it — this one supplies the fourteen worked examples it is
   checked against, and does not carry a second copy of the rule.

**The honest limit — and it is narrower than "secret."** "Tier plus cues reproduce the priority
order" holds wherever the ordering-reason is readable *or expressible as an authored threshold on
a secret value.* A **threshold comparison is not a branch cap performs**: cap hands the client an
authored break point and the client evaluates the secret against it and paints the result. That is
true of a resource level (S1's `sealed-power-percent` — Felblade's `100/maxFury`, **ST-12**) and
of a cooldown's remaining time alike (S4's `sealed-cooldown-range` — every hold in **ST-2**,
**ST-5** and **ST-8**). What the platform does not allow is cap **computing** with the secret —
reading it into a Lua branch or score. So there is **no "cap is blind" bucket** in the Havoc
priority; the "secret ⇒ can't rank" framing is wrong.

**A readable fact and a sealed one meet in two legal places, and one of them is new.** A sealed
marker may carry readable *gates* — a `when` beside its `display`, cue F's mechanism — so *"sealed
value, but only while these readable things hold"* is one authored mark: one secret, many readable
gates. What has no single-mark form is a value-to-value comparison across the line, and that folds
the other way — author the actionable slice, and let separate marks compose on screen where a slice
is not enough. The three APL conditions that cross the line here each land on one of those: The
Hunt's hold (**ST-5**, gates), Vengeful Retreat's alignment gate (the sequence family below,
slice), and Immolation Aura's talent gate (cue F, gates).

## Where cap can express the skip — the tally

Classifying every single-target scenario by how cap directs the eye to its press:

| Verdict | Meaning | Scenarios |
| --- | --- | --- |
| **readable rank** | every skip above the press is a readable fact — a cooldown, a readiness mark, affordability, a demon-form window, the AoE toggle, or plain elimination | ST-0, ST-1, ST-3, ST-4, ST-6, ST-7, ST-9, ST-10, ST-11, ST-12 |
| **sealed-modulated** | at least one *load-bearing* skip rides a sealed value the client paints and cap never reads | ST-2, ST-5, ST-8 |

No scenario is a genuine "cap can't rank it." The open facts (Demonsurge / Essence-Break-window
promotion, the Inertia proc, buff-maintenance markers) only **sharpen** a scenario that already
resolves via a readable cue or elimination — none gates a press. The finding: the Havoc order is a
**readable dependency graph with sealed timing on top**, and the sealed half grew this pass, from
one hold to four.

⚠ **Two of the readable facts are not game reads at all**, and that is worth separating out. The
`aoe` gate is cap's **own** toggle, and the `talent` gate is the player's trait config — neither
is a resource, a clock or a proc, so neither can be secret and neither needs measuring for
*safety*. The trait-config **call** is `[gap]` unmeasured for *fidelity* only: if it refuses, the
gold badge quietly stops appearing and nobody is told.

## Status legend — every cue is classified

| Status | Meaning |
| --- | --- |
| **have** | Readable cue already in the catalog's core: readiness (R2), affordability (A), readable hold (C1), demon-form promotion (D), Immolation-at-full (R6), the talent gate (F) and the single-target skip (G). Reads a readable fact; ships now. ⚠ *Ships* is about the **fact**, not the pixels — a cue whose only expression would be positive (demon-form promotion) is `have` and currently undrawn. |
| **sealed** | A specified sealed-display cue: the Fury break-point readout (B) and every hold band (C2), plus the demon-form bar. The client paints it from a secret value; cap reports `offered`/`armed`/`refused` and never reads back. |
| **open** | Needs in-client measurement; **produces no hint until resolved** (`../spec.md` §3.6). Where an open cue would apply, the press is already carried by a **have** cue or by elimination; the open cue is flagged as "would additionally sharpen *if* measured," never relied on. |

⚠ **No scenario asserts an unmeasured readable cue as available.** Where an open cue would apply
(Demonsurge / Essence-Break-window promotion, Inertia-proc rise, a buff-maintenance marker), the
eye-direction is carried by a **have** cue or by elimination, and the open cue is flagged, never
relied on.

---

## Single-target priority walk (Fel-Scarred)

Each scenario: the **state** → the **CDM row** (every icon's state, in priority order) → the
**walk** (left-to-right, the skip-reason for each available button until the press) → the **cue
set** and its status.

**ST-0 is the simplest walk** — the case elimination resolves with no cue doing any work. It is
first because it is the easiest to read, not because the others are measured against it.

### ST-0 · Eye Beam — the clean walk

- **State.** Not transformed, Fury mid, **single-target mode**. **Eye Beam is ready.**
  Metamorphosis and The Hunt are on cooldown. **Immolation Aura has spent both charges**, so it
  is swiped. Nothing is in a window.
- **CDM row.** Vengeful Retreat `weave` · Metamorphosis `cd` · The Hunt `cd` · Eye Beam `press` ·
  Essence Break `open` · Blade Dance `open` · Immolation Aura `cd` · Chaos Strike `open` ·
  Felblade `open` · Demon's Bite `open` · Fel Rush `open` · Throw Glaive `open`
- **Walk.**
  1. **Vengeful Retreat** — off the GCD; weave it now, for free. Continue for the GCD press.
  2. **Metamorphosis / The Hunt** — on cooldown → skip.
  3. **Eye Beam** — available, and **nothing rules it out** → **press.** Rung 14, and the button
     the whole rotation is built around keeping rolling.
- **Eye-direction.** No cue does any work: the press is simply where an unobstructed
  left-to-right scan stops, and every button between the swipes and it is a button the walk had
  no reason to stop at. That is the plainest form of the reading model, which is why it is worth
  one scenario — not because it is a yardstick.
- ⚠ **Do not read this as "the row is normally empty."** A different Immolation Aura charge state
  would put the rung-25 skip badge on this very row (ST-12), and other buttons carry standing
  reasons of their own. Whether badges read as **events rather than wallpaper** is a claim about
  how often they fire *in play*; it is settled on a flight, not by picking a quiet scenario.
- ⚠ **What no longer happens: a badge on every below-max charge.** An earlier draft red-badged
  Immolation Aura whenever it was recharging, which fires across the entire steady state. The
  current badge fires on a *rung* (25, and only when the button is pressable and there is a
  spender to be sent to), not on a charge count.
- **Cue set.** Readiness (R2) → **have**. Nothing else fires.

### ST-1 · Metamorphosis — the reset is banked

- **State.** Not transformed, Fury ~50. Vengeful Retreat and Metamorphosis are up. **Eye Beam is
  on cooldown with well over 8s left, and Blade Dance is on cooldown.** The Hunt is up.
- **CDM row.** Vengeful Retreat `weave` · Metamorphosis `press` · The Hunt `open` ·
  Eye Beam `cd` · Essence Break `open` · Blade Dance `cd` · Immolation Aura `open` ·
  Chaos Strike `open` · Felblade `open` · Demon's Bite `open` · Fel Rush `open` ·
  Throw Glaive `open`
- **Walk.**
  1. **Vengeful Retreat** — off the GCD; weave it now, for free (holds Exergy). Continue for the
     GCD press.
  2. **Metamorphosis** — available, and nothing cap can see rules it out. The half of rung 3 the
     catalog covers is `!cooldown.blade_dance.up & cooldown.eye_beam.remains>8`, and both terms
     are satisfied, so all three of its markers stay dark: the reset banks two casts. It is the
     first button the scan reaches with no swipe and no badge → **press.**
- **Eye-direction.** Meta's *own* readiness didn't decide it — the state of the two abilities it
  *resets* did, and it decided it **by not objecting**. The dependency comparison is still
  happening; it just has nothing to say when the answer is "go." ST-2 and ST-3 are the same fact
  speaking.
- ⚠ **The three markers are a SLICE of rung 3, and one hold is missing entirely.** The full rung is
  `(!talent.chaotic_transformation | !cooldown.blade_dance.up & cooldown.eye_beam.remains>8) &
  !action.death_sweep.demonsurge_available & !action.annihilation.demonsurge_available`. Those two
  Demonsurge terms — *don't recast Metamorphosis while empowered casts are still owed* — are a
  third real hold, and cap draws nothing for it. It is **open**, not covered: whether an ability's
  empowered state is readable is unmeasured (see the gaps table). Read "nothing rules it out" here
  as *nothing cap can see*, which is the honest reading everywhere in this file.
- **Cue set.** Readiness (R2) → **have**. Reset marks — Blade Dance ready and Eye Beam ready
  (readable, R2 + R7) → **have**. Reset band — Eye Beam's cooldown ≤8s (C2, S4) → **sealed**.
  All three drawn only in their blocking state.

### ST-2 · Metamorphosis held — Eye Beam ≤8s out

- **State.** Deviation from ST-0. Metamorphosis is **up**, Blade Dance is on cooldown, and **Eye
  Beam's cooldown has ~6s left**. The Hunt is on cooldown. Essence Break is up.
- **CDM row.** Vengeful Retreat `open` {cues: blocked} · Metamorphosis `open` {cues: blocked} ·
  The Hunt `cd` · Eye Beam `cd` · Essence Break `press` · Blade Dance `cd` ·
  Immolation Aura `open` · Chaos Strike `open` · Felblade `open` · Demon's Bite `open` ·
  Fel Rush `open` · Throw Glaive `open`
- **Walk.**
  1. **Vengeful Retreat** — available, and its own `blocked` badge lights for the same reason
     Metamorphosis's does: Eye Beam is inside the 8s band, so the retreat is worth holding a
     moment to weave into it. Off the GCD, so it does not compete for the press either way.
  2. **Metamorphosis** — available, but the **`blocked` badge lights**: Eye Beam returns in ~6s,
     inside the authored 8s band, so the reset would be thrown away on a cooldown about to come
     back by itself. Wears `blocked` from the sealed route → skip.
  3. **The Hunt / Eye Beam** — on cooldown → skip.
  4. **Essence Break** — available, and Eye Beam's remaining is **more than 4s**, so its own hold
     band is dark → **press.** Rung 17.
- **Eye-direction.** ⚠ **This is the scenario that did not previously exist**, and the reason it
  had to. The old marker was `!cooldown.eye_beam.up` — Eye Beam *ready*. The APL's term is
  `cooldown.eye_beam.remains>8`, which is a clock, and a clock is secret. So the hold is now the
  same red badge driven by a curve the client evaluates: cap hands over the 8s band and never
  learns where inside it the value fell.
- **Counter (the readable half).** With Eye Beam **ready** instead of 6s out, Metamorphosis wears
  the same badge from a *readable* marker; the press moves to Eye Beam.
  ⚠ **Both markers are needed and neither is redundant.** The sealed band deliberately reads
  nothing at zero remaining, and Metamorphosis sits at position 2 — **left of** Eye Beam — so a
  quiet Meta would be pressed before the eye ever reached Eye Beam. Essence Break, sitting to Eye
  Beam's *right*, needs only the band; elimination covers its zero case. Row position decides
  which halves a hold needs.
- **Cue set.** Reset band — Eye Beam cooldown ≤8s (C2, S4) → **sealed**. Reset mark — Eye Beam
  ready (C1) → **have**, the counter above. Both name one cue and union into one badge.

### ST-3 · Metamorphosis held — Blade Dance is ready

- **State.** Not transformed. Metamorphosis is up; **Blade Dance is ready**. Eye Beam is on
  cooldown with well over 8s left. The Hunt and Essence Break are on cooldown.
- **CDM row.** Vengeful Retreat `weave` · Metamorphosis `open` {cues: blocked} ·
  The Hunt `cd` · Eye Beam `cd` · Essence Break `cd` · Blade Dance `press` ·
  Immolation Aura `open` · Chaos Strike `open` · Felblade `open` · Demon's Bite `open` ·
  Fel Rush `open` · Throw Glaive `open`
- **Walk.**
  1. **Vengeful Retreat** — weave, off-GCD.
  2. **Metamorphosis** — available, but the **`blocked` badge lights** from a readable fact:
     Blade Dance is ready, so half the reset would be wasted (`!cooldown.blade_dance.up` in rung
     3). Wears `blocked` (readable) → skip.
  3. **The Hunt / Eye Beam / Essence Break** — on cooldown → skip.
  4. **Blade Dance** — available and affordable → **press.** Spend the charge Meta would have
     wasted; Meta becomes correct the moment it is down.
- **Eye-direction.** The plainest demonstration that cap re-ranks the press from a *readable
  relationship between two buttons*, computing nothing. ✅ This marker is the one the APL
  re-source confirmed **unchanged** — `!cooldown.blade_dance.up`, exactly as authored.
- **Cue set.** Readiness (R2) → **have**. Reset mark — Blade Dance ready (C1, readable) →
  **have**. Affordability (A) → **have**.

### ST-4 · The Hunt — Metamorphosis is ready, so cast it

- **State.** Not transformed. The Hunt is up. **Metamorphosis is ready**, and **Blade Dance is
  ready too**, so Meta itself is held. Eye Beam is on cooldown, ~12s out.
- **CDM row.** Vengeful Retreat `weave` · Metamorphosis `open` {cues: blocked} ·
  The Hunt `press` · Eye Beam `cd` · Essence Break `open` · Blade Dance `open` ·
  Immolation Aura `open` · Chaos Strike `open` · Felblade `open` · Demon's Bite `open` ·
  Fel Rush `open` · Throw Glaive `open`
- **Walk.**
  1. **Vengeful Retreat** — weave, off-GCD.
  2. **Metamorphosis** — held: Blade Dance is ready (ST-3's mark) → skip.
  3. **The Hunt** — available, and **its hold band is dark**: rung 4's second disjunct is
     `!cooldown.eye_beam.up & cooldown.metamorphosis.up`, and Meta being *ready* is exactly the
     state that says **cast**. Eternal Hunt's empower will land on the Eye Beam that
     Metamorphosis is about to reset → **press.**
- **Eye-direction.** ⚠ **The polarity here is the inverse of what an earlier draft asserted.** The
  old marker held The Hunt *because* Meta was available. The APL casts on that state. The rule was
  not merely mis-tuned, it pointed the wrong way, and the flight finding that the badge "fired
  almost constantly" was the symptom: Meta is a ~2-minute cooldown the player sits on, so a hold
  keyed to its readiness is lit most of the fight.
- **Cue set.** Readiness (R2) → **have**. Sync-hold band — Meta cooldown ≤15s (C2, S4) →
  **sealed**, and **dark here**, which is the point.

### ST-5 · The Hunt held — Metamorphosis ≤15s away

- **State.** Not transformed. The Hunt is up. **Metamorphosis's cooldown has ~12s left.** Eye Beam
  is ready.
- **CDM row.** Vengeful Retreat `weave` · Metamorphosis `cd` · The Hunt `open` {cues: blocked} ·
  Eye Beam `press` · Essence Break `open` · Blade Dance `open` ·
  Immolation Aura `open` · Chaos Strike `open` · Felblade `open` · Demon's Bite `open` ·
  Fel Rush `open` · Throw Glaive `open`
- **Walk.**
  1. **Vengeful Retreat** — weave, off-GCD.
  2. **Metamorphosis** — on cooldown → skip.
  3. **The Hunt** — available, but the **`blocked` badge lights**: Meta is ~12s away, inside the
     authored 15s band, and rung 4 wants `cooldown.metamorphosis.remains>15` before spending The
     Hunt bare. Save the empower for the Eye Beam Meta will reset. Wears `blocked` from the sealed route → skip.
     *(Eye Beam is ready here, so the other band — Eye Beam **far** — is dark; either alone
     raises the same badge.)*
  4. **Eye Beam** — available, nothing rules it out → **press.** ST-0's press, reached with one
     badge on the row instead of none.
- **Eye-direction.** **This is the least intuitive line in the whole APL and it is invisible
  without the badge.** Holding a two-charge-worth cooldown while it sits lit and ready is not
  something a player discovers; the badge is the only thing that says the window is coming.
- **Counter — the OTHER hold, and the commoner one.** With Metamorphosis simply **down** and Eye
  Beam **far** (≥10s), The Hunt wears the same badge from the other band. That is most of a 90s
  cooldown's return moments, and it is where the cost bites hardest: cast here and Eternal Hunt's
  empower burns up to ~20s before the Eye Beam it was saved for. An earlier draft had only the
  Meta band and missed this entirely.
- **Both bands are gated on Eternal Hunt.** Without that talent rung 4 is unconditional and there
  is no hold at all, so a badge would be asserting a rule this build has not got. This is the
  `talent` predicate's first use outside Immolation Aura, and it works because **a graded cue may
  curve on exactly one secret while being gated on as many *readable* facts as you like** — the
  Eye-Beam-far band additionally stands down while Metamorphosis is *ready*, since that is the
  APL's other cast case.
- ⚠ **Still a slice, not rung 4's literal negation.** Each band is a sound subset of the hold; the
  union covers more of it than either alone, and neither ever fires when the APL would cast.
- **Cue set.** Readiness (R2) → **have**. Two sync-hold bands — Eye Beam **beyond** 10s and Meta
  **within** 15s (C2, S4) → **sealed**, gated on Eternal Hunt (F) → **have**. ⚠ Both widths are
  **authored guesses until flown**.

### ST-6 · Death Sweep — flood the Essence Break window (demon-form override)

- **State.** **Transformed — Metamorphosis is active.** You have just opened an Essence Break
  window. Abyssal Gaze and Essence Break are on cooldown.
- **CDM row (Meta overrides live).** Vengeful Retreat `weave` · Metamorphosis `cd` · The Hunt `cd`
  · Abyssal Gaze `cd` · Essence Break `cd` · Death Sweep `press` · Consuming Fire `open`
  · Annihilation `open` · Felblade `open` · Demon's Bite `open` · Fel Rush `open` ·
  Throw Glaive `open`
- **Walk.**
  1. **Vengeful Retreat** — weave, off-GCD.
  2. **Metamorphosis / The Hunt / Abyssal Gaze / Essence Break** — all on cooldown (spent to build
     and open the window) → skip.
  3. **Death Sweep** — available, and nothing rules it out → **press.** Rung 12,
     `death_sweep,if=debuff.essence_break.up`, which is six rungs above the baseline Death Sweep
     at 18 — the promotion the APL performs and cap can only imply. The readable **demon-form
     window** is *why* it belongs here (promoted > lit COOLDOWN, `../spec.md` §3.1) — but the
     ranking argument does no work in this particular state: everything above it is on cooldown,
     so elimination alone reaches it. The promotion would matter in a state where a COOLDOWN
     button were also up, and that is the state a flight should build if it wants to test whether
     the promotion needs to be *drawn*.
- **Fidelity.** This is the override showcase: the row reads *Abyssal Gaze · Death Sweep ·
  Consuming Fire · Annihilation*. cap authors none of it — R7 resolves the live `overrideSpellID`,
  so the CDM shows precisely what the client shows.
- **Cue set.** Demon-form promotion (D, R7) → **have**. Demonsurge-active promotion → **open**.
  Essence-Break-window promotion → **open**. *(Demon form carries the promotion today; the two
  windows would sharpen it if their active-state proves readable — until then they mark, never
  promote.)*

### ST-7 · Essence Break — open the window

- **State.** Not transformed, no window live. Essence Break is up. **Eye Beam's cooldown has ~12s
  remaining** — comfortably past the 4s that would hold Essence Break, and past the 8s that would
  hold Vengeful Retreat. Everything above is on cooldown.
- **CDM row.** Vengeful Retreat `weave` · Metamorphosis `cd` · The Hunt `cd` · Eye Beam `cd` ·
  Essence Break `press` · Blade Dance `open` · Immolation Aura `open` · Chaos Strike `open` ·
  Felblade `open` · Demon's Bite `open` · Fel Rush `open` · Throw Glaive `open`
- **Walk.**
  1. **Vengeful Retreat** — weave, off-GCD.
  2. **Metamorphosis / The Hunt / Eye Beam** — on cooldown → skip.
  3. **Essence Break** — available, and nothing rules it out → **press**, then flood the window
     with Death Sweep + Annihilation (ST-6).
- ⚠ **There is no Fury precondition on Essence Break.** An earlier draft specified — and parked —
  a positive "banked ≥35" cue on this button. The APL carries **no Fury term on Essence Break at
  all**; the number came from prose. It is **deleted, not deferred**, and the vocabulary is one
  parked positive lighter for it.
- **Cue set.** Readiness (R2) → **have**. Sealed hold — Eye Beam CD ≤4s (C2, S4) → **sealed**,
  drawn in ST-8. ✅ The `>4` itself is the one number Icy Veins was already giving, now confirmed
  Tier 1.

### ST-8 · Essence Break held — Eye Beam ≤4s

- **State.** Deviation from ST-7: **Eye Beam's cooldown has ~2s left** instead of more than 4s.
  Blade Dance is up and affordable.
- **CDM row.** Vengeful Retreat `open` {cues: blocked} · Metamorphosis `cd` ·
  The Hunt `cd` · Eye Beam `cd` ·
  Essence Break `open` {cues: blocked} · Blade Dance `press` · Immolation Aura `open` ·
  Chaos Strike `open` · Felblade `open` · Demon's Bite `open` · Fel Rush `open` ·
  Throw Glaive `open`
- **Walk.**
  1. **Vengeful Retreat** — available, and **held**: its `blocked` badge is lit, because Eye Beam
     is inside the 8s band. ⚠ *Not* "weave it now, for free" — an earlier draft said that and it
     was wrong by the APL as well as by the Lua. The Eye Beam weave wants
     `cooldown.eye_beam.remains<gcd.max*0.3` — about **0.45s**, not two seconds — and the Meta
     path wants Metamorphosis ready, which it is not. Two seconds out is *nearly*, and nearly is
     what the badge is for.
  2. **Metamorphosis / The Hunt / Eye Beam** — on cooldown → skip.
  3. **Essence Break** — available, but the **`blocked` badge lights**: Eye Beam returns in ~2s,
     inside the authored 4s band, and opening now would clip the amp window into Eye Beam. Reads
     `blocked` (sealed) → skip.
  4. **Blade Dance** — available and affordable → **press.** Spend the baseline spender and open
     the window after Eye Beam.
- **Eye-direction.** The archetype of a sealed hold: the fact is a *clock*, cap never reads it,
  and the badge still appears **before** the thing it is waiting for arrives. Anticipation is
  expressible without cap knowing the number.
- **Cue set.** Sealed hold — Eye Beam CD ≤4s (C2, S4) → **sealed**. Affordability (A) → **have**.

### ST-9 · Blade Dance / Death Sweep — the baseline spender

- **State.** Not transformed, Fury mid (affordable). **Every cooldown above is on cooldown**,
  including Vengeful Retreat. Immolation Aura is recharging.
- **CDM row.** Vengeful Retreat `cd` · Metamorphosis `cd` · The Hunt `cd` · Eye Beam `cd` ·
  Essence Break `cd` · Blade Dance `press` · Immolation Aura `open` · Chaos Strike `open` ·
  Felblade `open` · Demon's Bite `open` · Fel Rush `open` · Throw Glaive `open`
- **Walk.**
  1. **Vengeful Retreat … Essence Break** — all on cooldown → skip.
  2. **Blade Dance** — available and affordable → **press.** Rung 18/19, the ordinary spender; it
     wins **by elimination** — nothing above it is up, and it needs no cue of its own.
- **Eye-direction.** The canonical elimination case for the *middle* of the list. Whenever a
  cooldown returns, the field re-lights above it and the eye moves up — which is exactly the
  priority order.
- **Cue set.** Readiness (R2) → **have**. Affordability (A) → **have** *(dims if Fury-starved —
  see ST-11)*.

### ST-10 · Immolation Aura — the charges are capped

- **State.** Not transformed, **A Fire Inside and Burning Wound both taken**, Immolation Aura at
  **full (2/2)**. Everything above it — Metamorphosis and The Hunt included — is on cooldown.
  Fury mid. Single-target mode, and it does not matter, which is the point.
- **CDM row.** Vengeful Retreat `cd` · Metamorphosis `cd` · The Hunt `cd` · Eye Beam `cd` ·
  Essence Break `cd` · Blade Dance `cd` · Immolation Aura `press` {cues: capped} ·
  Chaos Strike `open` · Felblade `open` · Demon's Bite `open` · Fel Rush `open` ·
  Throw Glaive `open`
- **Walk.**
  1. Everything above, **including Blade Dance**, is on cooldown → skip.
  2. **Immolation Aura** — its charges **read full** (`isActive` is `false`, and `NeverSecret`),
     so the second charge is not recharging and time on it is being thrown away → **press.**
     Rung 10 is exactly this: `charges=2` spends the surplus rather than sitting on it.
- ⚠ **This is the row that carries the vocabulary's one positive cue, and rung 10 is why it earns
  the exception.** Rung 10 carries **no target term** — a banked charge outranks the spenders,
  and Eye Beam, at any target count. Row position cannot express that: encoding rung 10 would
  demand a slot above Eye Beam in *every* state, which is wrong in the far commoner state where
  no charge is banked. A cue that jumps the queue on a condition is exactly what pass 1 of the
  reading model is, so the gold badge is not decoration on top of elimination — **it is the only
  thing carrying rung 10.**
- ⚠ **Rung 10 is not the top of the list, and the badge is gated accordingly.** It sits *below*
  rung 3 (Metamorphosis) and rung 4 (The Hunt), so with a charge banked and either of those
  **ready**, the APL presses those — and a positive cue, which overrides the elimination scan by
  design, would be pointing straight past them. Two readable terms fix it: the badge fires only
  while Metamorphosis is **not** ready and The Hunt is **not** ready. That is the general shape —
  **one secret, many readable gates** — and anywhere a cue looks over-eager, a missing readable
  gate is the first thing to check.
- **The talent gate (cue F).** The badge fires only with **both** of rung 10's talents,
  A Fire Inside *and* Burning Wound, read from the trait config. Without them the rung does not
  exist and the badge would be asserting a rank this build has not got.
  ⚠ **The gate is not there to stop a badge that would otherwise be stuck on.** An earlier draft
  said a one-charge Immolation Aura would wear this badge for the whole fight; it would not.
  `Sense.readCapped` returns `nil` when `maxCharges <= 1` — a guard that long predates this work —
  so on such a build `capped` is **UNKNOWN**, and unknown withholds. The badge would have been
  *blind*, not lit. What the gate buys is that the behaviour is **deliberate** rather than an
  accident of a guard elsewhere in the engine: it is stated where the rule is, and it survives
  someone changing that guard.
- **This is the scenario the reading chain was fixed for.** Here elimination happens to reach
  Immolation Aura too, so both passes agree. In the state where Eye Beam or Essence Break sits
  clean to its left, they do not — pass 1 says Immolation Aura, pass 2 says the button on the
  left, and **pass 1 is right**, because rung 10 outranks rung 14 and no row position can say so.
  `capart check` used to demand both passes name the same press, which made that row
  unrepresentable; since 2026-08-17 it runs the passes as the ordered chain Part 0.5 defines.
- **Cue set.** Immolation's charge state (`GetSpellCharges().isActive`, `NeverSecret`) →
  **have**, drawn in the capped direction only *(open-to-confirm: does that read behave the same
  on Havoc's row in instanced combat? OBS-066 measured Conflagrate)*. Talent gate (F) →
  **have**, with the exact trait-config call marked `[gap]` — unmeasured, and unknown-safe, so a
  refusal costs the badge rather than inventing one. Cooldown gates — Metamorphosis and The Hunt
  readiness (R2) → **have**.

### ST-11 · Felblade — Fury-starved

- **State.** Not transformed, **Fury low** (~25 — under Chaos Strike's cost), no cooldown up, and
  **Immolation Aura has no charges left**.
- **CDM row.** Vengeful Retreat `cd` · Metamorphosis `cd` · The Hunt `cd` · Eye Beam `cd` ·
  Essence Break `cd` · Blade Dance `open` {cues: starved} · Immolation Aura `cd` · Chaos Strike `open` {cues: starved} ·
  Felblade `press` · Demon's Bite `open` · Fel Rush `open` · Throw Glaive `open`
- **Walk.**
  1. **Vengeful Retreat … Essence Break** — on cooldown → skip.
  2. **Blade Dance** — available but reads `starved`: you cannot afford it (cue A, the
     `insufficientPower` read) → skip.
  3. **Immolation Aura** — no charges left → swiped by the CDM → skip.
  4. **Chaos Strike** — same as Blade Dance, `starved` → skip.
  5. **Felblade** — a generator with no Fury cost, so it is never unaffordable; it keeps its
     emphasis while the spenders lose theirs → **press.** Rung 22/24. Rebuild Fury; the generator
     correctly rises past the starved spenders because the field around it fell away.
- **Eye-direction.** The generator is reached by *subtraction*: nothing promotes it, two things
  above it demote themselves. ⚠ Note **Immolation Aura has to be genuinely out of charges** for
  the walk to pass it, and this is the one state the single-target skip cannot cover: the skip
  requires Chaos Strike to be **affordable** (it means *press the spender instead*), and here it
  is not. With a charge banked the row would stop at Immolation Aura while the APL presses
  Felblade at rung 22. Narrow, and mild — Immolation Aura generates Fury too. `catalog.md`,
  misordering 1.
- **Cue set.** Readiness (R2) → **have**. Affordability (A) → **have**. Fury break-point readout
  (B, S1) → **sealed**, and **dark here**: at ~25 Fury nothing is near any break.

### ST-12 · Chaos Strike — the single-target skip does real work

- **State.** Not transformed, **single-target mode**, **Fury flush (~150 of 170)**, no window
  live. Blade Dance is on cooldown. **Immolation Aura has one charge banked** — available, and
  not capped. A Fire Inside is taken.
- **CDM row.** Vengeful Retreat `cd` · Metamorphosis `cd` · The Hunt `cd` · Eye Beam `cd` ·
  Essence Break `cd` · Blade Dance `cd` · Immolation Aura `open` {cues: blocked} ·
  Chaos Strike `press` · Felblade `open` {cues: overcap} · Demon's Bite `open` {cues: overcap} · Fel Rush `open` ·
  Throw Glaive `open`
- **Walk.**
  1. Everything above Immolation Aura is on cooldown → skip.
  2. **Immolation Aura** — available, but the **`blocked` badge lights**. At one target with no
     charge banked, Immolation Aura's rung is **25** — *below* Chaos Strike's 23 — and row
     position 7 says the opposite, so the badge is what corrects it. Wears `blocked` →
     skip.
  3. **Chaos Strike** — available and affordable (Fury flush) → **press.** Rung 21/23. The raw
     dump lives near the *bottom* of the list; cap gives it **no more** than its baseline lane
     treatment. It wins because everything above it either swiped or badged itself out.
- ⚠ **This is the AoE re-weight, and it is the same row as AoE-1 with one toggle flipped.** Read
  the two together: the badge is the *only* difference, and it moves the press from Chaos Strike
  to Immolation Aura. cap has no readable enemy count and would not compute one — the `aoe`
  predicate is cap's **own** `/cap aoe` toggle, so there is no secret here and nothing to measure.
- ⚠ **Four terms, and each one is load-bearing.** Drop `!aoe` and the badge fires in AoE mode,
  where rung 20 makes position 7 correct. Drop `ready` and it stands on a greyed-out recharging
  icon the player was never going to press — `Treatment.For` passes cues through for swiped rows,
  so nothing else was stopping it. Drop `affordable(chaos_strike)` and it fires when there is no
  spender to be sent to (ST-11). Drop the rung-10 term and it fights the gold badge on the same
  button.
- ⚠ **That last term is authored as THREE markers unioned** — `!capped`, `!a_fire_inside`,
  `!burning_wound` — because it means `!(capped & a_fire_inside & burning_wound)`, the exact
  negation of the gold badge's own rung-10 test, and a marker's grammar is AND-only. Union is the
  OR: `!(P & Q & R)` is three markers, `P & Q & R` is one. A bare `!capped` would not do, for a
  reason that is easy to get backwards — `Sense.readCapped` returns `nil` when `maxCharges <= 1`,
  so on a build without A Fire Inside `capped` is **UNKNOWN**, and `!unknown` is still unknown.
  The single marker would be permanently **blind** there and the skip would never draw at all.
  The talent halves are what answer in that state.
- **Eye-direction.** The reason cap must *not* over-emphasise the bottom: the raw dump stands out
  only relative to a quieter field. The generators to its right read `overcap`, so the eye is
  pushed *toward* spending, not generating. Were Fury low, Chaos Strike would read `starved`, the
  Immolation Aura badge would clear with it, and the walk would land differently (ST-11).
- **Counter (the two break points, which are different numbers from different sources).**
  Felblade breaks at **`100 / maxFury` ≈ 59 %**, straight off rung 22
  (`felblade,if=hero_tree.felscarred&fury<=100`); Demon's Bite breaks at
  **`(maxFury − 25) / maxFury` ≈ 85 %**, a true-overcap number off the authored generation table.
  ⚠ Felblade's is **not an overcap number and never was** — rung 22 is a *promotion* rule, putting
  Felblade above Chaos Strike while Fury is low, and the badge draws its negation. The earlier
  ≈91 % figure was authored from the overcap formula and matched no source.
- ⚠ **This badge is informational, not eliminating, and always has been.** Felblade sits at
  position 9, to the right of Chaos Strike; the walk only reaches it when Chaos Strike is
  unaffordable — under ~40 Fury, far below either break. So no generator's `overcap` badge has
  ever changed which button elimination reaches. Correcting the number makes the readout *true*,
  not louder.
- ⚠ **And a documented misordering runs the other way.** Rung 22 puts Felblade **above** Chaos
  Strike whenever Fury ≤ 100; this row puts it below, using Felblade's unconditional rung 24.
  Fury is secret, so the promotion is not expressible as an *order* — only as this readout, which
  speaks in the opposite direction. `catalog.md`, misordering 3.
- **Cue set.** Readiness (R2) → **have**. Affordability (A) → **have**. Fury break-point readout
  on both generators (B, S1) → **sealed**.

---

## The Vengeful Retreat sequences — compositions, not row states

This is the material the row cannot hold, and the reason it gets a section rather than a
scenario. **Every case below is a composition of scenarios already walked above**, so **none of
them adds an elimination-gate obligation** and none appears in `capart check`'s count. That is
precisely why they are documented as a family: they are what the row *produces over time*, not a
state it is ever in.

**Framing.** Vengeful Retreat is off the GCD, so it is never *the* press — but it is also not a
free on-cooldown weave. Rung 5 is **alignment-gated**, two disjuncts:

```
the Eye Beam weave: gcd.remains<0.3 & cooldown.metamorphosis.remains
                    & cooldown.eye_beam.remains<gcd.max*0.3 & !buff.initiative.up
the Meta path:      cooldown.metamorphosis.up & cooldown.eye_beam.remains
                    & cooldown.blade_dance.remains & !buff.eternal_hunt.up
```

In the normal flow the alignment arrives about when Vengeful Retreat returns, which is why "press
on cooldown" reads as true. It is not: when Eye Beam and Metamorphosis are both far away, the APL
sits on it. cap expresses the actionable slice of that with **two sealed bands unioned onto one
`blocked` badge** — `vr_awaits_eye_beam` (Eye Beam ≤8s) and `vr_awaits_meta` (Meta ≤4s). The
player reads one meaning: **hold, something is coming.**

| # | State | Sequence | Steps |
| --- | --- | --- | --- |
| **VR-1** | Eye Beam ready, The Hunt down | VR → Eye Beam | the Eye Beam weave fires (`remains` 0 satisfies `<gcd.max*0.3`) · then **ST-0** |
| **VR-2a** | The Hunt + Eye Beam ready, **Meta >15s away** | VR → The Hunt → Eye Beam | **ST-4** · **ST-0**. Eternal Hunt's empower lands on that Eye Beam |
| **VR-2b** | The Hunt + Eye Beam ready, **Meta ≤15s away** | VR → Eye Beam *(The Hunt held)* | **ST-5** · **ST-0**. The empower is saved for the Eye Beam that Meta will reset — the least intuitive line in the APL, and invisible without the hold badge |
| **VR-3** | Eye Beam down, Meta ready | VR → Meta → Abyssal Gaze | **ST-1** · **ST-0**. Note the Meta path *and* rung 3 both require Blade Dance on cooldown |
| **VR-4** | Eye Beam down, Meta + The Hunt ready | VR → Meta → The Hunt → Abyssal Gaze | **ST-1** · **ST-4** · **ST-0**. After Meta, rung 4's *first* disjunct fires — Eye Beam has been reset to 0 (`remains<10`) and Metamorphosis has just gone on a full cooldown (`remains>15`). ⚠ a Demonsurge Death Sweep may interleave — verify in play |
| **VR-5** | Only Felblade available | the APL holds VR → Felblade | Neither disjunct is satisfiable. ⚠ **cap draws nothing** — see below |
| **VR-6** | Everything far away | the APL holds VR → the raw spender | Same. ⚠ **cap draws nothing** — see below |

⚠ **VR-5 and VR-6 are the two cases today's catalog does not author, and they are listed to say
so.** The authored bands light while Eye Beam is ≤8s **or** Metamorphosis is ≤4s; the APL's hold
in these two rows is the opposite — *both* are far. That is a conjunction of two sealed facts, and
no single mark carries one: a marker holds one `display`, and two markers union rather than
intersect. **Two marks would draw it.** An inverted band per ability is already authorable (the
mechanism gained that sense on 2026-08-17 — Eye Beam **beyond** 10s is exactly it), so two
`beyond` bands as separate badge instances put both facts on the row and let the eye AND them.
What that costs is a **reading inversion**: with the OR bands one lit badge means *hold*, and here
one lit badge must mean *not yet*. Nobody has ruled on that, so in an everything-is-far state
**Vengeful Retreat draws clean** today and the player is not told to hold it — a named, unflown
candidate rather than a refusal.

⚠ **And VR-1 through VR-4 are compositions of the ST scenarios only in their GCD presses.** Each
cited scenario has Vengeful Retreat either woven or swiped — none of them shows it *held* — so the
citations describe the sequence the row produces, not a row state in which the retreat itself is
badged. ST-2 and ST-8 are the two scenarios where the retreat's badge is actually drawn.

**Without Chaotic Transformation**, VR-3 and VR-4 dissolve — Metamorphosis stops resetting Eye
Beam, rung 3 goes unconditional, and Meta becomes a plain on-cooldown press. VR-1, VR-2 and
VR-5/6 are unaffected, running off Eye Beam and Eternal Hunt.

**Three things the bands do not claim:**

1. **Neither band is the APL's literal condition.** Authored literally, "everything that is not
   one of these two alignments" is a negative badge lit across the whole steady state — the
   failure that retired the below-max Immolation Aura badge (ST-0). These narrow bands are the
   **actionable slice**, authored the same way Felblade's break point is.
2. **The widths price a real cost.** Every second Vengeful Retreat is held is Initiative uptime
   not gained. 8s and 4s are guesses until flown.
3. **It may fire less than expected.** Cycle of Hatred shaves 2.5s off Eye Beam per cast, stacking
   to 10s; at full stacks Eye Beam (~20s) is *shorter* than Vengeful Retreat (~25s), so Eye Beam
   waits on Vengeful Retreat and the badge never lights. Airtime is build- and stack-dependent.

⚠ **One correction for the record: nothing in the APL is held *for* Vengeful Retreat.** It is the
reverse — Vengeful Retreat waits on Eye Beam or Metamorphosis. Practically that is mild, since its
~25s cooldown and Eye Beam's ~30s are close enough that pressing it when it is up usually lands in
the right place. *"Press on cooldown, ideally just before Eye Beam"* is a fair player-facing rule,
and the badge is the "ideally" half made visible.

**What this section proves**, and why it belongs here rather than in `rotation.md`: the sequence
is never *named* by cap. Each step is reached because everything above it is wearing a hold badge,
and each badge clears on a fact about a *different* button. The player is never told the order —
everything that is not the order is removed. Anticipation is real and expressible, because a hold
badge appears **before** the thing it waits for arrives.

---

## AoE / cleave variants

⚠ **The Fel-Scarred priority has exactly one target-count term** — rung 20's `active_enemies>1` —
and it moves exactly one button. *(Rung 11 carries `active_enemies>=2` as well, but it is
Aldrachi-Reaver-gated and so is not on this list; an earlier draft said "the entire 25-line
priority", which overstates it.)* 12.1 deleted Havoc's AoE branching, so the
three AoE scenarios an earlier draft carried collapse to one.

**And it is delivered.** An earlier draft of this file, and of `catalog.md`, said cap could not
draw an AoE re-weight because "the row's order is the client's". That premise stopped being true
when `Anchor.lua` shipped (2026-08-16): the row is re-anchored to the authored order, on by
default. The argument had a second flaw independent of the first — it surveyed only **positive**
treatments ("show that Immolation Aura matters more here"), found none the shelf allows, and
wrote that down as an impossibility. The negative route was always open: **mark Immolation Aura
skippable when AoE mode is off.** Same information, opposite polarity, and it fits a
negative-by-default vocabulary without asking the shelf for anything new.

### AoE-1 · Immolation Aura — the only target-count term in the APL

- **State.** **ST-12's state exactly, with the mode toggle flipped to AoE.** Two or more targets.
  Not transformed, Fury flush, every cooldown and Blade Dance on cooldown, **Immolation Aura
  holding one charge** (not capped), A Fire Inside taken.
- **Delta.** Rung 20 —
  `immolation_aura,if=active_enemies>1&(talent.a_fire_inside|talent.burning_wound)` — puts
  Immolation Aura **above** Chaos Strike (rung 21/23), which is what row position 7 encodes. So
  in AoE mode the row is already right and there is nothing to say: the single-target skip badge
  clears, and the walk reaches Immolation Aura on its own. **Compare the row below with ST-12's
  line by line — one badge is the entire difference, and it moves the press.**
- **CDM row.** Vengeful Retreat `cd` · Metamorphosis `cd` · The Hunt `cd` · Eye Beam `cd` ·
  Essence Break `cd` · Blade Dance `cd` · Immolation Aura `press` · Chaos Strike `open` ·
  Felblade `open` {cues: overcap} · Demon's Bite `open` {cues: overcap} · Fel Rush `open` · Throw Glaive `open`
- **Cue set.** Readiness (R2) → **have**. Single-target skip (G) → **have**, and **dark here**,
  which is the whole scenario. Immolation's charge state (`isActive`) → **have**, dark. The mode
  itself is cap's own state, read through the `aoe` predicate — not a game read, so nothing about
  it is secret or unmeasured.
- ⚠ **AoE mode does not silence the row, it silences one badge.** `immolation_capped` carries no
  `aoe` term — correctly, since rung 10 has none either — so at 2/2 charges the gold badge appears
  in AoE exactly as it does at one target. Only the rung-25 skip is mode-dependent.
- ⚠ **What this still does not do.** The mode is a *player input*, not a target count: a player
  who forgets to toggle gets the wrong badge, and cap will not know. That is the honest cost of
  having no readable enemy count, and it is unchanged. What changed is that the toggle now
  reaches the row at all.

*(Burning-Wound tab-targeting adds no cap cue: tab-targeting is target selection cap does not
hint. The Meta + Essence Break burst is the same COOLDOWN readiness as single target.)*

---

## What the walk surfaced — cue completeness + gaps

**Complete cue set for comprehensive coverage (have / sealed):** readiness (R2), affordability
(A), readable holds C1 (Metamorphosis's two reset marks), sealed holds C2 (four of them —
Metamorphosis, The Hunt, Essence Break, Vengeful Retreat), demon-form promotion (D),
Immolation-at-full (R6) with its talent gate (F), the single-target skip (G), the Fury
break-point readout (B), identity re-skin (R7), and the demon-form bar. Plus **two non-cue mechanisms** the walk made explicit: the
**emphasis-intensity hierarchy** and **eye-direction by elimination** (both now `../spec.md`
§3.1), and the **AoE-mode input** that re-weights without a readable count.

**Deleted this pass, and why the deletions matter as much as the additions:**

| Cue | Why it is gone |
| --- | --- |
| Immolation Aura's below-max `blocked` badge | `capped` negated — it fired across the entire steady state, against rungs 20 and 25. ST-0 could not exist while it did. |
| Essence Break's parked "banked ≥35" positive | The APL has no Fury term on Essence Break. The number came from prose, not a source. |
| The claim that cap *cannot* deliver the AoE re-weight | Wrong twice. Its premise ("the row's order is the client's") stopped being true when `Anchor.lua` shipped; and it surveyed only positive treatments, so "no treatment exists" was a statement about half the vocabulary. Shipped as cue G. |
| The claim that Immolation Aura's single-target rung "is 25" | It ignored rung 10, which has no target term at all. |

**Gaps — cues the walk would use but we have not measured (open, produce no hint until resolved):**

| Named cue | Where it appears | Status | Gates |
| --- | --- | --- | --- |
| **The trait-config call** `[gap]` | ST-10, ST-12 | **built, unmeasured** | The `talent` predicate ships, keyed on `ranksPurchased` + `activeEntry.entryID`. `knowledge/addon-dev/` records nothing about that shape or whether it survives combat restriction. The code is unknown-safe, so this is a **fidelity** question, not a safety one: a silent refusal costs the gold badge and frees the skip, and nobody is told. |
| **Demonsurge-active promotion** | ST-6 | **open** | Whether the Demonsurge window exposes a *readable* active-state so cap may **promote** (else it may only mark). |
| **An owed empowered cast** (`action.<x>.demonsurge_available`) | ST-1 | **open** | Rung 3's third hold — *don't recast Metamorphosis while empowered Death Sweep or Annihilation casts are still owed* — is drawn by nothing. `proc` already exists in `Catalog.PREDICATES`, so if an owed empowered cast surfaces as a readable proc on the row this is cheap; it is filed in `../backlog.md` as an optimisation over the baseline, not built. |
| **Essence-Break-window promotion** | ST-6 | **open** | Whether the Essence Break amp window's active-state is readable (else promote → mark). |
| **Inertia-proc rise** | (Inertia build only) | **open** | Whether Felblade shows a readable Inertia proc that lifts it above baseline. Not load-bearing on the Exergy build walked here. |
| **Buff-maintenance marker** (Exergy / Serrated Glaive) | the VR sequences, ST-12's tail | **open** (candidate readable-present + sealed-remaining) | Whether "buff present" reads as a plain boolean while the remaining time stays sealed. If so it is a readable marker; the countdown is a sealed duration. |
| **Hold-band airtime** | ST-2, ST-5, the VR sequences | **open — measurement, not a cue** | Whether 8s / 15s / 8s / 4s are the right widths. cap reports that it *offered* a sealed rule, never whether the badge lit, so this is an eyeball in game rather than a capture. |

These are the same open facts tracked in `catalog.md` → *Open facts to measure in-client* and
`fact-classification.md` → *Open facts*. Route every one as `@verify-ingame` / ClientLab
`@pending-test`, never a guess. **None gates a press** — each only sharpens a scenario that
already resolves by a readable cue or elimination.
