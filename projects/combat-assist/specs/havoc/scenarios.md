# Havoc Demon Hunter (Fel-Scarred) — the scenario catalog

**What this file is for.** `catalog.md` maps every ability to a role lane and the four cues.
This file proves that lane + cues actually **reproduce the priority order** — scenario by
scenario. It walks the live Icy Veins 12.1 Fel-Scarred priority (single-target + AoE,
re-verified 2026-08-12) and, for each realistic game state, models **what the player actually
sees in the Cooldown Manager** and **why the eye lands on the one press the rotation would
choose**.

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
high because it **resets** Eye Beam and Death Sweep, so cap ranks it off *their* readable cooldown
state, not its own. Walking the list this way forces out (a) the **skip-reason** behind every
rung and whether cap can express it, (b) the **complete** cue set comprehensive coverage needs,
(c) the **gaps** — cues we would need but have not measured, and (d) the three general principles
now lifted into the constitution (`../spec.md` §3.1). This is a design characterization for play,
not a claim the order is universally correct.

**Cross-links.** Constitution: `../spec.md` §3.1 (the emphasis-intensity hierarchy + the
elimination principle live there now) and §3.7 (the Havoc product section, which points here).
Normative roster + the four cues: `catalog.md` (beside this file). Fact safety lanes:
`fact-classification.md`. Priority source: `knowledge/classes/demon-hunter/havoc/rotation.md`
(Fel-Scarred sustained + AoE, re-verified against the live Icy Veins 12.1 page 2026-08-12).

> **Fel-Scarred, specifically.** Aldrachi Reaver is a separate catalog authored later. The
> Icy Veins 12.1 page has **one hero-filtered priority tool**, not two lists; selecting
> Fel-Scarred renders a **13-item, Vengeful-Retreat-led** priority (the Exergy build). That is
> the list walked here. (The page's *static HTML* is a 24-item both-heroes union the JavaScript
> filters — a prior draft transcribed the union and mis-ordered Metamorphosis to #1; corrected
> 2026-08-13. See `rotation.md`'s sourcing-gotcha note.)

---

## How to read a scenario

Every scenario is the **same eleven-icon CDM row**, in priority order, in a different state:

```
 Vengeful Retreat · Metamorphosis · The Hunt · Eye Beam · Essence Break ·
 Blade Dance · Chaos Strike · Immolation Aura · Felblade · Demon's Bite · Fel Rush
```

Each icon carries a **walk verdict** — one of a closed vocabulary of ten. A verdict says what cap
has concluded about that button; it does **not** say what the button looks like. **The pixels are
`../render-shelf.md`'s**, and every scenario below renders from its token block, so a treatment
changes by editing the shelf, never by editing this file.

| Verdict | What cap concluded | Whose signal |
| --- | --- | --- |
| `cd` | on cooldown — ruled out natively, no cap opinion | Blizzard CDM (not a cap signal) |
| `weave` | off the GCD: pressed *alongside* the GCD press, never instead of it | readiness (R2) |
| `hold-readable` | wait — a dependency's *readable* cooldown state says the press would be wasted | cue C1 / dots (readable, R2 + R7) |
| `hold-sealed` | wait — a *sealed* duration says don't clip the window | cue C2 (sealed, S4) |
| `starved` | unaffordable right now | cue A (readable, R1) |
| `overcap` | a generator whose press would waste Fury | cue B negative (sealed, S1) |
| `withheld` | cap has no opinion because the fact reads secret — unknown ≠ "not capped" | R6 (readable *only* at full) |
| `press` | the first available button with no skip-reason — the chosen press | elimination of everything above it |
| `press-promoted` | the press, additionally promoted because a readable demon-form window favors it | cue D (readable, R7) |
| `below` | shown, but never reached — lower priority than the press | — |

The walk stops at the press. Buttons to its right are lower priority and are not evaluated; they
render, but carry no verdict beyond `below`. **Vengeful Retreat is the exception** — it is off the
GCD, so it is "pressed" in parallel and the walk continues past it to find the GCD press.

### The **CDM row** bullet is machine-read

Every scenario carries one `- **CDM row.**` bullet, and `wowkb.capart` parses it to render the
artifact — so it is written in a fixed grammar rather than prose:

```
- **CDM row.** <Ability> `<verdict>` [{dots: <Ability> go|wait, …}] [{cues: <cue>, …}] · <Ability> `<verdict>` · …
```

The ability name is the one the client would *show* — so a demon-form scenario writes
**Death Sweep**, not Blade Dance, and the artifact draws that icon (R7 resolves the live
`overrideSpellID`; cap authors none of it). A `dots` group is the C1 readable dependency dots:
`go` = the related ability is on cooldown, so the dependency is satisfied; `wait` = it is ready and
the press would waste it. A `cues` group names center-row cues by their `render-shelf.md` key.

`wowkb.capart check havoc` re-scrapes these bullets and fails if they disagree with the generated
artifact's sidecar — this file leads, the artifact follows.

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

So a Metamorphosis scenario's row reads *Abyssal Gaze · … · Death Sweep · Annihilation · Consuming
Fire*, and an Eye-Beam-window scenario shows *Death Sweep · Annihilation* but still *Eye Beam* and
*Immolation Aura*. (⚠ The Eye-Beam-window-vs-Meta split of the Abyssal Gaze / Consuming Fire
override is a **display-fidelity** expectation to confirm in-client; R7 renders whatever is live
regardless, so cap is correct either way — it only affects which icon a scenario should *draw*.)

---

## The three general principles this walk proved (now `../spec.md` §3.1)

The walk does not just list cues — it establishes *how* tier + cues reproduce an APL, and where
they cannot. Three rules fell out that are **spec-wide**, not Havoc-specific, and are now normative
in the constitution:

1. **A priority list is a dependency graph; emphasis may follow a readable *relationship*, not
   only a button's own state.** A press's rank is set by *why* it belongs there, and that reason
   often rests on a *related* ability's readable state. cap may compare those — one ability's
   cooldown against another's — and still be moving emphasis only by readable facts, not computing
   a press. **ST-1/ST-2** are the archetype: Metamorphosis is "go" or "wait" entirely off Eye
   Beam's readable cooldown state (its reset target), shown as two dependency **dots**.
2. **Emphasis has intensity, not just on/off.** To reproduce the order, "lit" must rank:
   **promoted (a windowed spender) > lit COOLDOWN > lit ROTATION baseline > dim/off.** The eye
   goes to the brightest — several scenarios are only correct because a promoted spender
   out-shines a lit cooldown (**ST-4**).
3. **Eye-direction by elimination.** A low-priority button is directed-to by the **absence** of
   competing emphasis, not by a bright cue of its own. The default spender and the filler need no
   signal; they win when they are the only button the walk reaches (**ST-6**, **ST-9**, **ST-10**).
   Every scenario in this file is, structurally, an elimination walk — the press is the first
   available button no cue rules out.

**The honest limit — and it is narrower than "secret."** "Tier plus cues reproduce the priority
order" holds wherever the ordering-reason is readable *or expressible as an authored threshold on a
secret value.* A **threshold comparison is not a branch cap performs**: cap hands the client an
authored break point (S1's `sealed-power-percent` power curve) and the client evaluates the secret
Fury against it and paints the result — in **either polarity**. So "avoid the generator when Fury is
about to cap" (negative, cue B — **ST-7**) *and* "prefer Essence Break once Fury is banked ≥35"
(positive — **ST-5**) are both expressible sealed cues; cap authors the number and never learns
which side the value fell on. The one thing genuinely off-limits is cap **computing** with Fury —
reading it into a Lua branch/score, or combining secret values into one verdict. That is the §4
oracle, forbidden by choice, not a wall the restriction builds. So there is **no "cap is blind"
bucket** in the Havoc priority; the "secret ⇒ can't rank" framing is wrong.

## Where cap can express the skip — the tally

Classifying every single-target scenario by how cap directs the eye to its press:

| Verdict | Meaning | Scenarios |
| --- | --- | --- |
| **readable rank** | every skip above the press is a readable fact — a cooldown, a dependency dot, affordability, a demon-form window, or plain elimination | ST-1, ST-2, ST-3, ST-4, ST-6, ST-7, ST-8, ST-9, ST-10 |
| **sealed-modulated** | at least one *load-bearing* skip rides a sealed value the client paints and cap never reads — the banked-Fury open cue and the sealed hold | ST-5 |

No scenario is a genuine "cap can't rank it." The open facts (Demonsurge / Essence-Break-window
promotion, the Inertia proc, buff-maintenance markers) only **sharpen** a scenario that already
resolves via a readable cue or elimination — they never gate a press. The finding: the Havoc order
is **mostly a readable dependency graph**, with sealed cues doing targeted work at the Fury edges
(ST-5 open, ST-7 overcap counter).

## Status legend — every cue is classified

| Status | Meaning |
| --- | --- |
| **have** | Readable cue already in the catalog's core: readiness (R2), affordability (A), readable hold / dots (C1), demon-form promotion (D), Immolation-at-full (R6). Reads a readable fact; ships now. |
| **sealed** | A specified sealed-display cue: overcap readout (B), sealed hold (C2), banked-Fury threshold (S1 positive), demon-form bar. The client paints it from a secret value; cap reports `offered`/`armed`/`refused` and never reads back. |
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

### ST-1 · Metamorphosis — the reset is banked

- **State.** Not transformed, Fury ~50. Vengeful Retreat and Metamorphosis are up; **Eye Beam and
  Blade Dance are both on cooldown**. The Hunt is up. Nothing is in a window.
- **CDM row.** Vengeful Retreat `weave` · Metamorphosis `press` {dots: Eye Beam go, Death Sweep go}
  · The Hunt `below` · Eye Beam `cd` · Essence Break `cd` · Blade Dance `cd` · Chaos Strike `below`
  · Immolation Aura `below` · Felblade `below` · Demon's Bite `below` · Fel Rush `below`
- **Walk.**
  1. **Vengeful Retreat** — off the GCD; weave it now, for free (holds Exergy). Continue for the
     GCD press.
  2. **Metamorphosis** — available, and it carries **two dependency dots**, shown only while it is
     castable: Eye Beam and Death Sweep, each driven by that ability's readable cooldown state.
     `go` = on cooldown (the reset is valuable); `wait` = ready (the reset would be wasted). Both
     read `go` here → the reset banks two casts → **press.**
- **Eye-direction.** Meta's *own* readiness didn't decide it — the state of the two abilities it
  *resets* did. Two dots are richer than one hold marker: they say *why* it is go, and they say it
  from readable facts.
- **Cue set.** Readiness (R2) → **have**. Reset dots — Eye Beam & Death Sweep cooldowns (R7,
  readable) → **have**.

### ST-2 · Eye Beam — Metamorphosis waits (the counter)

- **State.** Same as ST-1, but **Eye Beam is *ready*** (Blade Dance still on cooldown). Meta is up.
- **CDM row.** Vengeful Retreat `weave` · Metamorphosis `hold-readable` {dots: Eye Beam wait} ·
  The Hunt `cd` · Eye Beam `press` · Essence Break `cd` · Blade Dance `cd` · Chaos Strike `below` ·
  Immolation Aura `below` · Felblade `below` · Demon's Bite `below` · Fel Rush `below`
- **Walk.**
  1. **Vengeful Retreat** — weave, off-GCD.
  2. **Metamorphosis** — available, but its **Eye Beam dot flips to `wait`**: Eye Beam is ready, so
     resetting it would waste the reset. Meta reads `hold-readable` → skip.
  3. **The Hunt** — on cooldown → skip.
  4. **Eye Beam** — available, no skip-reason → **press.** Cast it now; Meta resets it a moment
     later for a banked second cast.
- **Eye-direction.** The mirror of ST-1, and the strongest demonstration: cap re-ranks the press
  from a *readable relationship* between two buttons, computing nothing.
- **Cue set.** Readiness (R2) → **have**. Reset dot — Eye Beam cooldown (R7, readable) → **have**.

### ST-3 · The Hunt — Metamorphosis is down

- **State.** Not transformed. The Hunt is up; **Metamorphosis is on cooldown**. Eye Beam on
  cooldown. Fury mid.
- **CDM row.** Vengeful Retreat `weave` · Metamorphosis `cd` · The Hunt `press`
  {dots: Metamorphosis go} · Eye Beam `cd` · Essence Break `cd` · Blade Dance `below` ·
  Chaos Strike `below` · Immolation Aura `below` · Felblade `below` · Demon's Bite `below` ·
  Fel Rush `below`
- **Walk.**
  1. **Vengeful Retreat** — weave, off-GCD.
  2. **Metamorphosis** — on cooldown → skip.
  3. **The Hunt** — available; its one dependency dot reads **Meta's cooldown state**. Meta is on
     cooldown → dot reads `go` → there is no upcoming Meta to sync with, so cast now → **press.**
- **Counter.** If Metamorphosis were *up*, The Hunt's dot flips to `wait` — hold, to save The Hunt
  to buff Abyssal Gaze inside the coming Meta window (the guide's "hold if Metamorphosis is
  available"). You would skip The Hunt and press the next GCD button.
- **Cue set.** Readiness (R2) → **have**. Sync-hold dot — Meta cooldown state (R7, readable) →
  **have**. *(Corrects an earlier draft that made this a sealed Essence-Break-window hold — the
  live guide's hold is Meta-availability, which cap reads directly.)*

### ST-4 · Death Sweep — flood the window (demon-form override)

- **State.** **Transformed — Metamorphosis is active.** You have just opened an Essence Break
  window with Fury banked. Eye Beam (→ Abyssal Gaze) and Essence Break are on cooldown.
- **CDM row (Meta overrides live).** Vengeful Retreat `weave` · Metamorphosis `cd` · The Hunt `cd`
  · Abyssal Gaze `cd` · Essence Break `cd` · Death Sweep `press-promoted` · Annihilation `below` ·
  Consuming Fire `below` · Felblade `below` · Demon's Bite `below` · Fel Rush `below`
- **Walk.**
  1. **Vengeful Retreat** — weave, off-GCD.
  2. **Metamorphosis / The Hunt / Abyssal Gaze / Essence Break** — all on cooldown (spent to build
     and open the window) → skip.
  3. **Death Sweep** — available, and the readable **demon-form window promotes it** above what a
     lit COOLDOWN would be (promoted > lit COOLDOWN) → **press.** Flood the window.
- **Fidelity.** This is the override showcase: the row now reads *Abyssal Gaze · Death Sweep ·
  Annihilation · Consuming Fire*. cap authors none of it — R7 resolves the live `overrideSpellID`,
  so the CDM shows precisely what the client shows.
- **Cue set.** Demon-form promotion (D, R7) → **have**. Demonsurge-active promotion → **open**.
  Essence-Break-window promotion → **open**. *(Demon form carries the promotion today; the two
  windows would sharpen it if their active-state proves readable — until then they mark, never
  promote.)*

### ST-5 · Essence Break — open the window (sealed cues)

- **State.** Not transformed, **Fury banked (≥35)**, no window live. Essence Break is up. Eye
  Beam's cooldown has **more than 4s** remaining (safe to open).
- **CDM row.** Vengeful Retreat `weave` · Metamorphosis `cd` · The Hunt `cd` · Eye Beam `cd` ·
  Essence Break `press` {cues: banked} · Blade Dance `below` · Chaos Strike `below` ·
  Immolation Aura `below` · Felblade `below` · Demon's Bite `below` · Fel Rush `below`
- **Walk (press).**
  1. **Vengeful Retreat** — weave, off-GCD.
  2. **Metamorphosis / The Hunt** — on cooldown → skip.
  3. **Eye Beam** — on cooldown, long remaining → skip.
  4. **Essence Break** — available, and it carries the **banked** cue: the client evaluated secret
     Fury against an authored break point (35 / maxFury, S1) and painted it — cap never read the
     value → **press**, then flood the ~4s window with Death Sweep + Annihilation. ⚠ The banked cue
     is **open** (below), so it produces nothing until measured; the artifact marks it as such.
- **Counter (sealed hold).** If Eye Beam's cooldown had **≤4s** remaining instead, Essence Break
  would read `hold-sealed` — don't clip the window into Eye Beam. That hold rides a sealed
  duration (S4 curve on Eye Beam's cooldown), painted client-side; cap never reads the clock. You
  would skip Essence Break, spend the baseline spender, and open the window after Eye Beam.
- **Cue set.** Readiness (R2) → **have**. Banked-Fury ≥35 threshold (S1 positive, painted) →
  **open** *(the positive-polarity threshold cue is specified but unmeasured; until confirmed the
  press ships on readiness + player judgment, no banked light)*. Sealed hold — Eye Beam CD ≤4s
  (C2, S4) → **sealed**.

### ST-6 · Death Sweep / Blade Dance — the baseline spender

- **State.** Not transformed, Fury mid (affordable). **Every cooldown above is on cooldown.**
  Immolation Aura is not full.
- **CDM row.** Vengeful Retreat `cd` · Metamorphosis `cd` · The Hunt `cd` · Eye Beam `cd` ·
  Essence Break `cd` · Blade Dance `press` · Chaos Strike `below` · Immolation Aura `below` ·
  Felblade `below` · Demon's Bite `below` · Fel Rush `below`
- **Walk.**
  1. **Vengeful Retreat … Essence Break** — all on cooldown → skip.
  2. **Blade Dance** — available and affordable → **press.** The ordinary spender; it wins **by
     elimination** — nothing above it is up, and it needs no cue of its own.
- **Eye-direction.** The canonical elimination case for the *middle* of the list. Whenever a
  cooldown returns, the field re-lights above it and the eye moves up — which is exactly the
  priority order.
- **Cue set.** Readiness (R2) → **have**. Affordability (A) → **have** *(dims if Fury-starved —
  see ST-7)*.

### ST-7 · Felblade — Fury-starved (affordability, with overcap counter)

- **State.** Not transformed, **Fury low**, no cooldown up, Immolation not full.
- **CDM row.** Vengeful Retreat `cd` · Metamorphosis `cd` · The Hunt `cd` · Eye Beam `cd` ·
  Essence Break `cd` · Blade Dance `starved` · Chaos Strike `starved` · Immolation Aura `withheld`
  · Felblade `press` · Demon's Bite `below` · Fel Rush `below`
- **Walk.**
  1. **Vengeful Retreat … Essence Break** — on cooldown → skip.
  2. **Blade Dance** — available but reads `starved`: you cannot afford it (cue A, the
     `insufficientPower` read) → skip.
  3. **Chaos Strike** — same, `starved` → skip.
  4. **Immolation Aura** — available, but its charges read below full → **secret**, so cap
     **withholds** the "spend it" opinion (unknown ≠ capped) → skip, no signal.
  5. **Felblade** — a generator with no Fury cost, so it is never unaffordable; it keeps its
     emphasis while the spenders lose theirs → **press.** Rebuild Fury; the generator correctly
     rises past the starved spenders because the field around it fell away.
- **Counter (overcap).** With Fury **near cap** instead, the same Felblade reads `overcap` (cue B,
  negative) — pressing it would waste Fury. You skip the generator and spend a spender. The break
  point is authored (S1); the client paints it; cap reads nothing.
- **Cue set.** Readiness (R2) → **have**. Affordability (A) → **have**. Immolation withhold (R6) →
  **have**. Overcap readout (B, S1 negative) → **sealed**.

### ST-8 · Immolation Aura — don't cap the charges

- **State.** Not transformed, Immolation Aura at **full (2/2** with A Fire Inside**)**. The spenders
  are on cooldown (just spent). Fury mid.
- **CDM row.** Vengeful Retreat `cd` · Metamorphosis `cd` · The Hunt `cd` · Eye Beam `cd` ·
  Essence Break `cd` · Blade Dance `cd` · Chaos Strike `cd` · Immolation Aura `press` ·
  Felblade `below` · Demon's Bite `below` · Fel Rush `below`
- **Walk.**
  1. Everything above, **including both spenders**, is on cooldown → skip.
  2. **Immolation Aura** — its charges **read full** (R6: the charge count reads plain *only* at
     max), so cap emphasises it as "spend it" → **press.** Don't waste a charge; dump both before
     Meta so A Fire Inside / Demonic Intensity refunds them.
- **Eye-direction.** Below full the count is secret and the button reads `withheld` — the plain
  **full** read *is* the whole capped signal. This is the one Fury-adjacent decision that matters,
  and R6's read-at-full limit is a feature here, not a hole.
- **Cue set.** Immolation-at-full (R6) → **have** *(open-to-confirm: does the charge row read
  readable-at-full in instanced combat? confirm before shipping the tier)*.

### ST-9 · Annihilation / Chaos Strike — the raw dump (elimination, low)

- **State.** Not transformed, **Fury flush**, no window live. Blade Dance is on cooldown; Immolation
  not full.
- **CDM row.** Vengeful Retreat `cd` · Metamorphosis `cd` · The Hunt `cd` · Eye Beam `cd` ·
  Essence Break `cd` · Blade Dance `cd` · Chaos Strike `press` · Immolation Aura `withheld` ·
  Felblade `overcap` · Demon's Bite `overcap` · Fel Rush `below`
- **Walk.**
  1. Everything above, and Blade Dance, is on cooldown → skip.
  2. **Chaos Strike** — available and affordable (Fury flush) → **press.** The raw dump lives near
     the *bottom* of the list; it is the press only **by elimination** — it is the only emphasised
     spender — and cap gives it **no more** than its baseline lane treatment. It wins by being
     alone.
- **Eye-direction.** The reason cap must *not* over-emphasise the bottom: the raw dump stands out
  only relative to a quieter field. The generators to its right read `overcap` (Fury is flush), so
  the eye is pushed *toward* spending, not generating. Were Fury low, Chaos Strike would read
  `starved` (cue A) and a generator would rise past it (ST-7).
- **Cue set.** Readiness (R2) → **have**. Affordability (A) → **have**. Overcap readout on the
  generators (B) → **sealed**.

### ST-10 · Fel Rush — last-resort filler

- **State.** Not transformed. Both spenders were just spent and are on cooldown, Immolation Aura is
  not full, and Fury is flush — so both generators would waste it.
- **CDM row.** Vengeful Retreat `cd` · Metamorphosis `cd` · The Hunt `cd` · Eye Beam `cd` ·
  Essence Break `cd` · Blade Dance `cd` · Chaos Strike `cd` · Immolation Aura `withheld` ·
  Felblade `overcap` · Demon's Bite `overcap` · Fel Rush `press`
- **Walk.** Every cooldown and both spenders are on cooldown; Immolation Aura is `withheld`; both
  generators read `overcap` → skip → **Fel Rush** is all that is left → **press.** The fallback has
  **no signal of its own**; the eye lands here purely by elimination.
  *(An earlier draft wrote this row as an ellipsis — "every rotation button cd / starved" — which
  no state actually produces: a generator has no Fury cost and so can never be `starved`. The row
  above is the state that genuinely reaches the filler.)*
- **Cue set.** Readiness (R2) → **have**. *(Throw Glaive is not in the Fel-Scarred priority — a rare
  filler unless Screaming Brutality routes it through Blade Dance; with Serrated Glaive it buffs
  *you* for 12s, a candidate buff-maintenance marker, open.)*

---

## AoE / cleave variants (3+ targets)

The AoE list shares the same row and only **re-weights the middle** — the single-target raw
spender drops, and Immolation Aura + Blade Dance/Death Sweep rise. It adds **no new cues.** The
re-weight is selected by the **player's AoE-mode input** (`../spec.md` §2 — the player sets
single-target or AoE), *not* by a readable target count (cap has no readable enemy count and would
not compute one). So these are the ST scenarios above with the mode input shifting which button
the walk reaches first.

### AoE-1 · Immolation Aura — pressed more aggressively

- **Delta.** In AoE mode Immolation Aura is a top source, pressed harder than the single "don't cap
  at 2" rule. cap's cue is unchanged — the readable-at-full "don't cap" signal (R6) still fires;
  the *press-it-more* is the **AoE-mode input**, not a new cue and not a computed count.
- **CDM row (AoE order).** Vengeful Retreat `cd` · Metamorphosis `cd` · The Hunt `cd` ·
  Eye Beam `cd` · Essence Break `cd` · Immolation Aura `press` · Blade Dance `below` ·
  Felblade `below` · Demon's Bite `below` · Chaos Strike `below` · Fel Rush `below`
- **Cue set.** Immolation-at-full (R6) → **have**. AoE-mode weighting → mode input, **not a cue**.

### AoE-2 · Blade Dance / Death Sweep — primary

- **Delta.** In AoE mode these rise to primary (they trigger Glaive Tempest at 3+). The rise is the
  AoE-mode input; the demon-form promotion (D) still stacks on top when transformed, and the
  single-target Chaos Strike dump falls beneath it.
- **CDM row (AoE order, Meta overrides live).** Vengeful Retreat `weave` · Metamorphosis `cd` ·
  The Hunt `cd` · Abyssal Gaze `cd` · Essence Break `cd` · Consuming Fire `withheld` ·
  Death Sweep `press-promoted` · Felblade `below` · Demon's Bite `below` · Annihilation `below` ·
  Fel Rush `below`
- **Cue set.** Readiness (R2) → **have**. Demon-form promotion (D) → **have**. AoE-mode weighting →
  mode input, **not a cue**.

### AoE-3 · Chaos Strike / Annihilation — de-emphasised

- **Delta.** In AoE mode the single-target dump drops *further* beneath Blade Dance — spend into
  Blade Dance instead. The AoE-mode input **re-ranks** an already-by-elimination button (ST-9)
  below the generators; the re-rank is the narrowing, no new cue.
- **CDM row (AoE order).** Vengeful Retreat `cd` · Metamorphosis `cd` · The Hunt `cd` ·
  Eye Beam `cd` · Essence Break `cd` · Immolation Aura `withheld` · Blade Dance `press` ·
  Felblade `below` · Demon's Bite `below` · Chaos Strike `below` · Fel Rush `below`
- **Cue set.** Readiness (R2) → **have**. Affordability (A) → **have**. AoE-mode weighting → mode
  input, **not a cue**. *(Still reached only by elimination, just lower.)*

*(Burning-Wound tab-targeting and the Meta + Essence Break AoE burst add no cap cue: tab-targeting
is target selection cap does not hint, and the Meta/EB burst is the same COOLDOWN readiness as ST.)*

---

## What the walk surfaced — cue completeness + gaps

**Complete cue set for comprehensive coverage (have / sealed):** readiness (R2), affordability
(A), readable hold / dependency dots C1 (incl. the reset dots and the sync-hold dot), sealed hold
C2, demon-form promotion (D), Immolation-at-full (R6), overcap readout (B negative), banked-Fury
threshold (S1 positive), identity re-skin (R7), and the demon-form bar. Plus **two non-cue
mechanisms** the walk made explicit: the **emphasis-intensity hierarchy** and **eye-direction by
elimination** (both now `../spec.md` §3.1), and the **AoE-mode input** that re-weights without a
readable count.

**Gaps — cues the walk would use but we have not measured (open, produce no hint until resolved):**

| Named cue | Where it appears | Status | Gates |
| --- | --- | --- | --- |
| **Banked-Fury threshold (positive)** | ST-5 | **open** (specified S1 positive) | Whether the positive-polarity "banked ✓" light draws correctly on Essence Break from the authored 35/maxFury break. Until confirmed, ST-5 ships on readiness + player judgment. |
| **Demonsurge-active promotion** | ST-4 | **open** | Whether the Demonsurge window exposes a *readable* active-state so cap may **promote** (else it may only mark). |
| **Essence-Break-window promotion** | ST-4 | **open** | Whether the Essence Break amp window's active-state is readable (else promote → mark). |
| **Inertia-proc rise** | (Inertia build only) | **open** | Whether Felblade shows a readable Inertia proc that lifts it above baseline. Not load-bearing on the S2 Exergy build walked here. |
| **Buff-maintenance marker** (Exergy / Serrated Glaive) | ST-1 (weave), ST-10 | **open** (candidate readable-present + sealed-remaining) | Whether "buff present" reads as a plain boolean while the remaining time stays sealed. If so it is a readable marker; the countdown is a sealed duration. |

These are the same open facts tracked in `catalog.md` → *Open facts to measure in-client* and
`fact-classification.md` → *Open facts*. Route every one as `@verify-ingame` / ClientLab
`@pending-test`, never a guess. **None gates a press** — each only sharpens a scenario that already
resolves by a readable cue or elimination.
