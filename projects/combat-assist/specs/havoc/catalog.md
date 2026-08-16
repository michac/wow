# Havoc Demon Hunter (Fel-Scarred) — comprehensive catalog

**Applies to:** Havoc (specID `577`), hero tree **Fel-Scarred**, Midnight 12.1. This is the
normative catalog document: the thing a future `Catalogs/Havoc.lua` transcribes. It is a
provisional product characterization for play, not a claim the rules are universally correct.
`../spec.md` §3.7 owns the intended experience; `../spec.md` §3.1 owns the tier model;
`../pattern-shelf.md` owns every recipe cited here (`R1`…`R10`, `S1`…`S6`);
`fact-classification.md` beside this file tags each fact readable / sealed-display / open with
its addon-dev evidence; `scenarios.md` beside this file walks the Fel-Scarred priority as a
single-row Cooldown-Manager elimination walk and proves lane + cues reproduce the order (state →
why each off-cooldown button is skipped → the press → cue status).

> **This catalog is Fel-Scarred, specifically.** A spec-and-hero pair is the unit cap authors.
> **Aldrachi Reaver is a separate catalog authored later** (its own `Reaver's Glaive` /
> `Reaver's Mark` / `Rending Strike` / `Glaive Flurry` shape), not a second overlay bolted on
> here. ⚠ *Hero-tree pick, not acted on yet:* the Icy Veins 12.1 page has **one hero-filtered
> priority tool** (selecting Fel-Scarred renders a 13-item, Vengeful-Retreat-led list — *not* an
> AR-led list; an earlier note here claiming it "leads Aldrachi Reaver" was wrong). We author
> Fel-Scarred first (the easier build to pilot, the M+ pick) and hold the hero-tree call until
> Season 2 sims/logs exist (post-2026-08-18).

> Every override spell ID below is **resolved at bind via `overrideSpellID` (R7)**, never
> hardcoded; the numbers here are reference. What has been transcribed and what has flown is
> `../backlog.md` → `## Status`, and nowhere else. *(The "transcription is deferred" banner that
> stood here described a stale checkout on one machine and is struck.)*

> ⚠ **cap cannot deliver the AoE re-weight, and the scenarios section that describes it is
> honest about being a design walk rather than a render.** The re-weight is a change in which
> button the *walk* reaches — and the walk's order is the Cooldown Manager's, which cap neither
> authors nor can reorder. `press` and `below` render identically (both are a lane border and no
> cue), so AoE-1/2/3 draw pixel-for-pixel what their single-target counterparts draw. There is
> consequently nothing to wire: `ns.Mode.IsAoE()` needs no route into `Signal`, and adding one
> would only let a mode toggle change pixels that carry no such meaning. If the re-weight is ever
> to reach the screen it needs a new treatment argued at the shelf, not a wire.

## The design in one paragraph

Havoc's defining constraint is that its primary resource, **Fury, is secret** (R3): cap may
*display* Fury but never branch on its value. The roster maps onto the §3.1 role lanes the way
the authoritative priority does — verified against the live Icy Veins 12.1 page (2026-08-12),
whose priority is **cooldown-dominated**, with the raw Fury dump (Chaos Strike / Annihilation)
near the **bottom**, rising only inside a window. So the **COOLDOWN** lane carries the burst /
window buttons, the **ROTATION** lane carries the build/spend core, and cap uses cap's **two
tools** — *emphasis* (readable on/off) and *cues* (additive display of sealed values) — to
reproduce that order. Five cues do the work: **A** affordability, **B** overcap, **C** hold/sync,
**D** demon-form promotion, **E** charges capped (the one positive cue). Over it all runs the **demon-form transform** as the readable
identity spine (R7).

## Bound abilities

Base spell IDs are from `knowledge/classes/demon-hunter/havoc/ability-inventory.tsv`. Demon-form
override IDs are **invisible to Tier 1** and resolved live via R7 — the reference numbers carry ⚠.
⚠ Metamorphosis's override is **not** Void Metamorphosis (`471306`); `abilities.md:183` flags that
as an unconfirmed 12.1 API description bleed, so it is not substituted anywhere.

| Key | Ability | Base spell ID | Demon-form override | Lane | Charges | Cues |
| --- | --- | ---: | --- | --- | --- | --- |
| `metamorphosis` | Metamorphosis | `191427` | — | COOLDOWN | — | readable reset marks (C1) — Eye Beam + Death Sweep cooldowns |
| `eye_beam` | Eye Beam | `198013` | Abyssal Gaze ⚠`452497` | COOLDOWN | — | — |
| `the_hunt` | The Hunt | `370965` | — | COOLDOWN | — | readable sync-hold mark (C1) — Meta cooldown |
| `essence_break` | Essence Break | `258860` | — | COOLDOWN | — | positive Fury-banked cue (B, S1, **parked**); sealed hold (C2) — hold if Eye Beam CD ≤4s |
| `vengeful_retreat` | Vengeful Retreat | `198793` | — | COOLDOWN | ⚠ open | — |
| `chaos_strike` | Chaos Strike | `344862` | Annihilation ⚠`201427` | ROTATION | — | affordability (A) + demon-form promotion (D) |
| `blade_dance` | Blade Dance | `188499` | Death Sweep ⚠`210152` | ROTATION | — | affordability (A) + demon-form promotion (D) + identity |
| `felblade` | Felblade | `232893` | — | ROTATION | — | relative affordability (A — no cue of its own) + overcap readout (B) |
| `demons_bite` | Demon's Bite | `344859` | — | ROTATION | — | relative affordability (A — no cue of its own) + overcap readout (B) |
| `immolation_aura` | Immolation Aura | `258920` | Consuming Fire ⚠`452487` | ROTATION | 2 | **two** charge states off `isActive` — gold `capped` at max, red `blocked` below (E) + identity |
| `throw_glaive` | Throw Glaive | `185123` | — | FALLBACK | yes | — |
| `fel_rush` | Fel Rush | `344865` | — | FALLBACK | 2 | — |
| `demonsurge` | Demonsurge (buff) | `452402` | — | — | — | **OPEN** — hero-signature; no hint until measured |

`demon_form` is not a bound *ability* — it is a readable **marker** and an optional **bar**
surface, read from the transform identity fact (R7), and it drives cue D.

### The Charges column, and what it does *not* mean

**Charges are a render fact, not a priority fact.** `../render-shelf.md` V2 says an ability wears
exactly one border and that the **CHARGES** lane *replaces* the role lane when the client reports
charges. So the `Lane` column above stays exactly as the rotation authored it — Immolation Aura is
**ROTATION**, and always was — and this column only tells the renderer that its border will draw
purple instead of blue. Nothing here re-ranks anything.

Sources, per `knowledge/classes/demon-hunter/havoc/abilities.md` (12.1.0.69214):

- **Immolation Aura — 2**, with **A Fire Inside**. Without that talent it is a single-charge
  button, which is one of the reasons the "don't cap the charges" cue (R6) is the interesting one
  on this row at all.
- **Fel Rush — 2** (~10 s recharge), baseline.
- **Throw Glaive — `yes`**, ~9 s recharge. The *count* is not Tier-1 sourced: the tsv's `cooldown`
  column is `max(RecoveryTime, CategoryRecoveryTime)` and returns the **GCD** for a charge ability,
  so it settles nothing, and the real recharge lives in `SpellCategory.ChargeRecoveryTime` which is
  unreachable without breaking the build pin. `yes` is deliberately not a guessed number — the
  border only needs the boolean.
- **Vengeful Retreat — ⚠ open, and it therefore draws COOLDOWN.** It read **25 s** in the
  12.0.7.67808 tsv and **0.5 s** at 12.1.0.69214, which is the charge-ability artifact, and 12.1
  gives Devourer's Hungering Slash *"a temporary charge of Vengeful Retreat"*. That is suggestive,
  not measured, and an unmeasured fact must never render as a measured one. `@verify-ingame`
  (Vengeful Retreat cooldown / charges) is already open in `abilities.md`; when it resolves, this
  cell becomes a number and the border colour follows.

⚠ **A finding, surfaced rather than hidden:** both FALLBACK abilities in this catalog (Throw Glaive,
Fel Rush) have charges, so under the substitution **no Havoc row ever draws a FALLBACK border**.
The lane is still declared and still correct; it simply has no subject in this spec. `capart build`
prints this as a page-level note rather than letting the lane silently vanish, and it is
`../render-shelf.md` Part 5's question 3 — whether a fourth colour that displaces the third is
carrying meaning or eating it.

## The lanes, and why the priority falls out of them

The verified Fel-Scarred priority (Icy Veins 12.1 tool, Fel-Scarred tab, corrected 2026-08-13) is
**Vengeful-Retreat-led**: Vengeful Retreat → Metamorphosis → The Hunt → **windowed** Death Sweep /
Annihilation → Eye Beam → Essence Break → baseline Death Sweep → Consuming Fire → **raw
Annihilation / Chaos Strike** → Immolation-at-2 → Felblade → Fel Rush. Read that against the lanes:

- **COOLDOWN** = the top of the priority (Meta, The Hunt, Eye Beam, Essence Break, Vengeful
  Retreat). They light when ready; a hold cue (C) says when to wait.
- **ROTATION** = the middle-to-bottom, where the cues do the ordering. The raw spender is *low*
  by default and only rises when cue **D** promotes it inside a readable window; the generator
  rises (relatively) when cue **A** dims the starved spender; the generator is pushed off by cue
  **B** near overcap; Immolation Aura wears one of two badges, gold at full charges and red below.
- **FALLBACK** = pure filler (Throw Glaive, Fel Rush).

Tier + cues, read together, reproduce that priority — which is the §3.1 point. No lane is a
strict rank; the cues cross lanes (a promoted Death Sweep in a window outranks a lit Eye Beam,
exactly as the guide's windowed spender outranks the baseline spender below it).

## Roster — player problem → fact → recipe → treatment

### COOLDOWN lane

- **Metamorphosis** (`191427`). *Problem:* ~2 min burst whose payoff is its **reset** of Eye Beam
  and Death Sweep — pressing it while either is *ready* wastes that reset. *Fact:* `ready` (R2) for
  the lane; the go/wait read is the **cooldown state of Eye Beam and Death Sweep** (both readable,
  R2), shown only while not already transformed (R7). *Treatment:* COOLDOWN + a **readable
  dependency mark** (C1), drawn **only when the dependency blocks**: if either Eye Beam or Death
  Sweep is *ready*, the reset would be wasted and Meta wears the red `blocked` badge. Both on
  cooldown → nothing is drawn, and Meta is simply the leftmost button no cue rules out — see
  `scenarios.md` ST-1/ST-2. *(Until 2026-08-13 this was a green/red **dot pair**, one per reset
  target. The render shelf's cue vocabulary is negative by default, so the satisfied state draws
  nothing; the underlying fact — two readable cooldown states, compared — is unchanged.)*
- **Eye Beam** (`198013` → Abyssal Gaze ⚠ in Meta). *Problem:* keep the demon-form window
  rolling — it enables everything downstream. *Fact:* `ready` (R2). *Treatment:* COOLDOWN, no
  hold. Same row across the FS override via R7.
- **The Hunt** (`370965`). *Problem:* on cooldown, but **hold if Metamorphosis is available** — to
  buff Abyssal Gaze inside the coming Meta window. *Fact:* `ready` (R2) for the lane; the hold is
  **Meta's cooldown state**, a **readable** fact (R2 on Meta). *Treatment:* COOLDOWN + a **readable
  sync-hold mark** (C1) driven by Meta's cooldown — Meta available ⇒ the red `blocked` badge (hold
  to buff Abyssal Gaze inside the coming window); Meta on cooldown ⇒ nothing drawn, cast now.
  *(Corrects an earlier draft that made this a sealed Essence-Break-window hold —
  the live guide's hold is Meta-availability, which cap reads directly; `scenarios.md` ST-3.)*
- **Essence Break** (`258860`). *Problem:* mandatory in S2 (+49% initial, tier-set keys off it);
  open the amp window with Fury banked (≥35) and flood it. *Fact:* `ready` (R2), plus the **"Fury
  banked ≥35"** precondition — secret, but **expressible as a positive sealed threshold cue**: cap
  cannot read Fury, but it hands the client an authored break point (`35 / maxFury`) via S1's
  `sealed-power-percent` power curve and the client lights a **"banked"** cue when secret Fury clears
  it — the *same S1 tool as the generator overcap readout (cue B), positive polarity*. cap authors 35
  and never learns the value. Essence Break *also* carries its **own sealed hold** (C2): hold it
  while **Eye Beam's cooldown has ≤4s remaining** (don't clip the amp window into Eye Beam) — a
  sealed duration (S4 range step-curve on Eye Beam's cooldown → texture alpha), painted client-side;
  cap never reads the clock. *Treatment:* COOLDOWN + positive Fury-banked cue (S1) + **sealed hold**
  cue (C2). (This corrects an earlier design note that called the banked gate unreadable/unrankable:
  a threshold is a client-side paint, not a Lua branch, so it is expressible — `../spec.md` §3.1
  honest-limit.)
- **Vengeful Retreat** (`198793`). *Problem:* S2 maintain-on-cooldown press — holds **Exergy**
  (or arms Inertia, build-dependent) and refreshes **Initiative**, woven before Eye Beam.
  *Fact:* `ready` (R2). VR is off the GCD, so "ready" is the whole story. *Treatment:* COOLDOWN.

### ROTATION lane

- **Chaos Strike / Annihilation** (`344862` → ⚠`201427`). *Problem:* shown castable even when
  Fury-starved, and it is the *low-priority* dump — except inside a window. *Facts:* `affordable`
  (R1) + `identity` (R7). *Treatment:* ROTATION; **dimmed when `insufficientPower`** (cue A); the
  demon-form promotion (cue D) brightens **Annihilation** while transformed — which is why the
  raw spender, ~#20 baseline, correctly rises in its window. Re-skins across the flip.
- **Blade Dance / Death Sweep** (`188499` → ⚠`210152`). *Problem:* the empowered Death Sweep is
  what you flood windows with; it costs Fury. *Facts:* `ready` (R2) + `identity` (R7); optionally
  `affordable` (R1). *Treatment:* ROTATION; **promoted as Death Sweep in demon form** (cue D).
- **Felblade / Demon's Bite** (`232893` / `344859`). *Problem:* the generator to favor when
  starved — and the one that overcaps Fury when flush. *Facts (A):* generators have no Fury cost,
  so `insufficientPower` is never true — they **stay lit** while starved spenders dim; the
  relative shift is the whole signal. *Facts (B):* the overcap decision is `secret Fury-% ≥
  (maxFury − generation)/maxFury` — pushed engine-side (S1 graded) as a color curve on the Fury
  readout, red at/above the break. `maxFury` readable (`UnitPowerMax`, R4 — measured **170**, do
  not hardcode 120); `generation` from an **authored static table** (no API, R4: Felblade +15,
  Demon's Bite ~20–30). Honestly approximate. *Treatment:* ROTATION + cue A + cue B. Felblade
  additionally rises on a **readable Inertia proc** *if* that proves readable (open, below).
- **Immolation Aura / Consuming Fire** (`258920` → ⚠ in Meta). *Problem:* the one Fury decision
  that matters — don't sit on capped charges (2/2 with A Fire Inside). *Fact:* the charge state is
  **readable in BOTH directions** — `GetSpellCharges().isActive` is annotated `NeverSecret`, and
  it is false exactly when charges are at max (a recharge that is not running). This is stronger
  than the R6 limit an earlier draft was built on, which said charges are readable *only* at full
  (`currentCharges` plain iff at max, secret below) and therefore left "below max" as an unknown.
  It is not an unknown: it is the second state. *Identity (R7):* Immolation Aura is *the* transform
  that corrupts charge math (→ Consuming Fire, different id/charges) — R7's job here is reading the
  **right spell's** charges across the flip, not a priority override. *Treatment:* ROTATION plus
  one of two badges, never neither and never both:

  | Charge state | `isActive` | Badge | Says |
  | --- | --- | --- | --- |
  | at max, recharge stalled | `false` | gold `capped` (slot 3), positive | you are losing a charge right now |
  | below max, recharging | `true` | red `blocked` (slot 1), negative | hold the one you have, let the other come back |
  | the read refused | `nil` | none | unknown is not a state — draw nothing |

  The gold badge is the one place the style says something other than "skip" — see cue E below for
  why impending loss earns that exception, and why "about to cap" is not attempted.

### FALLBACK lane

- **Throw Glaive** (`185123`) / **Fel Rush** (`344865`). *Problem:* filler when nothing better is
  up. *Fact:* `ready` (R2). *Treatment:* FALLBACK. (Throw Glaive climbs into ROTATION only with
  Soulscar / Furious Throws / Screaming Brutality — a build variant to author if it proves worth
  a hint.)

### Demon form — marker + optional bar (drives cue D)

- *Problem:* "Am I in the window where spenders hit hard?" The icon is small for a 20s window.
- *Fact:* `identity(transformed)` — `overrideSpellID ~= spellID` on a transforming row (R7),
  readable. The window's *remaining* is a sealed duration.
- *Treatment:* a **readable marker** while transformed (drives cue D's promotion), plus an
  optional **independent sealed countdown bar** (§3.3), reusing the Tyrant-bar duration-object
  path (`Bars.lua`). The bar stays only if it earns its screen space.

## The five cues, collected

| Cue | What the player sees | Fact | Tool / lane | Recipe | Sink |
| --- | --- | --- | --- | --- | --- |
| **A** affordability | starved spenders dim; generators hold | `insufficientPower` | emphasis (readable) | R1 | ROTATION emphasis |
| **B** Fury threshold (two polarities) | **negative (drawn):** the generator wears the red `overcap` badge at/above the break · **positive (parked):** Essence Break would light a "banked" cue at Fury ≥35 — expressible, and deliberately not drawn — the vocabulary's one positive slot is spent on cue E, and a "you have enough" light is a statement about **rank**, which elimination already carries | secret Fury-% vs authored break | cue (sealed) | S1 (graded) + R4 static table | color curve → texture alpha |
| **C1** readable hold | the red `blocked` badge — on Metamorphosis while Eye Beam or Death Sweep is *ready* (the reset would be wasted), on The Hunt while Meta is *available* (hold for the window). A satisfied dependency draws **nothing**. | related-ability cooldown states | emphasis-adjacent marker (readable) | R2 + R7 | corner badge (readable lane) |
| **C2** sealed hold | the same red `blocked` badge on Essence Break while Eye Beam's cooldown is running and ends within 4s | Eye Beam cooldown remaining | cue (sealed) | S4 range step-curve on a duration object, `ignoreGCD` | curve → badge alpha |
| **D** demon-form promotion | Annihilation / Death Sweep brighten in demon form | `identity(transformed)` | emphasis (readable) | R7 | ROTATION emphasis (promotion) |
| **E** charges capped | Immolation Aura wears the **gold `capped` badge** in slot 3 at max charges — the vocabulary's one positive cue — and the red `blocked` badge below max, which is the same fact read the other way | `GetSpellCharges().isActive`, `NeverSecret` and therefore readable in **both** directions | cue (readable) | R6 + R7 | corner badge, own hue + glow |

⚠ **Cue E is positive, and that is a deliberate, scoped exception** (`../render-shelf.md` Part 0.5).
It reports **impending loss**, which is urgent regardless of priority rank — and rank is the only
thing a left-to-right scan can express, so there is no negative phrasing of it. It does **not**
direct the press: ST-8's row is already led correctly by elimination.

⚠ **"About to cap" is NOT expressible and is not attempted.** R6 (`../pattern-shelf.md:125`) and
OBS-066 measured that below full `currentCharges` is secret and `isActive` reads `true` at **both**
1/2 and 0/2 — it means *recharge running*, not *which charge*. (That is also exactly why the
below-max state can carry only the flat red `blocked` badge and not a countdown toward the cap.) So a threshold on the recharge
duration cannot tell "about to cap" from "about to get your first charge back", and would fire the
warning hardest while the player is charge-starved. Cue E therefore fires on the exact, readable
**full** state only. Closing the gap needs R6's napkin estimator, whose named worst case is
Immolation Aura itself (R7: the demon-form id/charge change) — so it is a decision, not a tweak.

Sealed-form names are `spec.md` §3.6's: cue B is `sealed-power-percent`; the cue-C2 hold and the
demon-form bar are `sealed-duration-range`.

## Demon-form identity spine (R7)

- Bind a **static identity** at load: `primary = overrideSpellID or base`, keep a stable
  `spellIDs` union so the row matches on either id across the flip. Never build identity on
  `item:GetSpellID()` (secret and moving in combat).
- The `identity`/`transformed` gate is `overrideSpellID ~= spellID` (Lua `0` is truthy — check
  an override of `0` explicitly).
- Charge/napkin safety: override-aware max, debit on the normalised identity, **re-seed on
  override change** — the Immolation Aura → Consuming Fire fix.

## New readable providers / renderer work this catalog implies

Per §9.4, a genuinely new mechanism becomes a *small named mechanism*, never spec-specific
Blizzard plumbing. Three, each with one characterization example, each confirmed against
`knowledge/addon-dev/` before building:

1. **"Capped" readable provider** — "charges readable-at-full" (R6): `currentCharges` reads plain
   iff at max; the plain read *is* the capped signal. Override-aware max + re-seed on transform
   (R7). First consumer: Immolation Aura.
2. **Sealed Fury threshold cue (B), two polarities** — one S1 graded **color curve** mechanism,
   authored break point on secret Fury-%, used both ways: **negative** on a generator (red near
   `(maxFury − generation) / maxFury` — "don't overcap"; first consumers Felblade, Demon's Bite,
   with the authored **generation static table**) and **positive** on Essence Break (lit "banked" at
   `35 / maxFury` — "you have enough to open the window"). Same sink, same rule; only the curve and
   the ability it rides differ. cap authors the number and never reads which side the value fell on.
3. **Sealed hold marker (C2)** — a **range step-curve → texture alpha** on a sealed duration
   object (S4). First consumer: **Essence Break**'s Eye-Beam-cooldown-≤4s hold. Before building,
   **check the current desktop renderer's marker vocabulary**: if it already has a `hold` marker
   slot (`Overlay.lua` `SLOTS`), C2 reuses it and edits nothing in Treatment/Overlay (the 9.4
   definition-of-done). The C1 **dependency marks** (Metamorphosis's resets, The Hunt's sync) drive
   the *same* `blocked` badge from a readable fact instead of a sealed one, so they add no new
   provider either — and because C1 and C2 now render identically, the renderer needs **one**
   marker, not two. Demon-form promotion (D) is plain emphasis on a readable fact — no new
   renderer. ⚠ **Cue B's positive half and cue D are authored but not currently drawn:** the render
   shelf's single positive cue is spent on charges-capped (cue E), so the "banked" light and the
   promotion have no treatment today. Both stay expressible (the sealed curve works in either polarity) and both are
   **parked, not refuted** — `../render-shelf.md` Part 0.5.

## Open facts to measure in-client (produce no hint until resolved — spec.md §3.6)

Route as `@verify-ingame` / ClientLab `@pending-test` markers, not guesses.

1. **Essence Break / Demonsurge window active-state readable?** Cue D promotes off a *readable*
   window; demon form is readable (R7) so it ships. Whether the **Essence Break** amp and the
   **Demonsurge** empowerment expose a *readable* active-state (vs sealed) decides whether those
   windows can **promote** (emphasis) or may only **inform via a marker** (cue). Until measured,
   they inform, never promote. @verify-ingame / @pending-test
2. **Demonsurge readable at all?** Does the Fel-Scarred Demonsurge empowerment expose a readable
   proc/aura, or is it sealed? Gates the Demonsurge row entirely. @verify-ingame / @pending-test
3. **Inertia proc glow on Felblade.** Does Inertia surface as a readable proc glow on Felblade?
   Gates the Felblade Inertia-rise cue. (Load-bearing only on the Inertia build.) @verify-ingame
4. **Immolation Aura charge row readable-at-full.** Does Havoc's Immolation Aura charge row behave
   like the R6 Conflagrate measurement (readable at full, secret below) in instanced combat?
   Candidate-settled by mechanism; confirm before shipping the "don't cap" tier. @verify-ingame
5. **Buff-maintenance marker readability (Exergy / Serrated Glaive).** Newly named by the
   `scenarios.md` walk (ST-1 VR weave, ST-10). Does a self-buff expose a *readable* "present" boolean
   (via `C_UnitAuras`) while its **remaining duration stays sealed**? If so, a maintain-on-cooldown
   press (Vengeful Retreat holding Exergy; Throw Glaive granting Serrated Glaive) could carry an
   optional readable "buff present / missing" marker, with any countdown drawn as a sealed
   duration. Until measured it is **open** — no marker; the press is directed by readiness (a lit
   COOLDOWN) alone, and the VR→Eye Beam weave stays player-trained (never a cap sequence).
   @verify-ingame / @pending-test

## Contract boundary

- **Emphasis (Lua conditions) uses only readable facts:** `ready` (R2), `affordable` (R1),
  `identity` (R7), and the "capped-at-full" charge read (R6). Fury value, Fury-%, and every
  remaining-duration are **never** read into a Lua condition.
- **Cues carry sealed facts to client-owned sinks:** the cue-B color curve (secret Fury-%) and
  the cue-C2 range curve (sealed duration) go straight to a draw call; cap reports `offered` /
  `armed` / `refused` and never reads back.
- **Unknown never becomes confidence,** including through negation. A refused `affordable` or
  `ready` withholds; it does not assert the opposite.
- The catalog declares **no** continuous grade, no resource gate (Fury is secret), no silence
  list, no cast sequence, no coverage rule, and no vocabulary a cue does not use.
