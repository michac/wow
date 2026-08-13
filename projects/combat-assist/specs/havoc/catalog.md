# Havoc Demon Hunter (Fel-Scarred) — comprehensive catalog

**Applies to:** Havoc (specID `577`), hero tree **Fel-Scarred**, Midnight 12.1. This is the
normative catalog document: the thing a future `Catalogs/Havoc.lua` transcribes. It is a
provisional product characterization for play, not a claim the rules are universally correct.
`../spec.md` §3.7 owns the intended experience; `../spec.md` §3.1 owns the tier model;
`../pattern-shelf.md` owns every recipe cited here (`R1`…`R10`, `S1`…`S6`);
`fact-classification.md` beside this file tags each fact readable / sealed-display / open with
its addon-dev evidence; `scenarios.md` beside this file walks the full Fel-Scarred priority
rung-by-rung and proves lane + cues reproduce the order (state → eye-direction → cue set →
status).

> **This catalog is Fel-Scarred, specifically.** A spec-and-hero pair is the unit cap authors.
> **Aldrachi Reaver is a separate catalog authored later** (its own `Reaver's Glaive` /
> `Reaver's Mark` / `Rending Strike` / `Glaive Flurry` shape), not a second overlay bolted on
> here. ⚠ *Mismatch to note, not act on:* the live Icy Veins 12.1 page **leads Aldrachi Reaver**
> for single-target while we author Fel-Scarred first (the easier build to pilot, the M+ pick).
> We hold that call until Season 2 sims/logs exist (post-2026-08-18).

> **Transcription is deferred.** This machine's `addon/` checkout is stale (v0.2.4, the old
> `HIGH/MEDIUM/LOW` vocabulary). The current design lives on the desktop, unpushed. This
> document is the machine-independent design; the Lua transcription (`../backlog.md` →
> *Phase 10.4*) waits until the desktop cap code is pushed. Every override spell ID below is
> **resolved at bind via `overrideSpellID` (R7)**, never hardcoded; the numbers are reference.

## The design in one paragraph

Havoc's defining constraint is that its primary resource, **Fury, is secret** (R3): cap may
*display* Fury but never branch on its value. The roster maps onto the §3.1 role lanes the way
the authoritative priority does — verified against the live Icy Veins 12.1 page (2026-08-12),
whose priority is **cooldown-dominated**, with the raw Fury dump (Chaos Strike / Annihilation)
near the **bottom**, rising only inside a window. So the **COOLDOWN** lane carries the burst /
window buttons, the **ROTATION** lane carries the build/spend core, and cap uses cap's **two
tools** — *emphasis* (readable on/off) and *cues* (additive display of sealed values) — to
reproduce that order. Four cues do the work: **A** affordability, **B** overcap, **C** hold/sync,
**D** demon-form promotion. Over it all runs the **demon-form transform** as the readable
identity spine (R7).

**The boundary (spec.md §3.1).** Layering emphasis + cues until the right press is obvious is the
**goal**, not something to design around; cap never withholds legal, displayable information to
keep a hint vague. What it must not become is a single channel that *computes* the answer and
hands it over (the Assisted-Combat shape §4 rules out, or branching on sealed data §3.6). The
line is the mechanism, not the count of lit buttons.

## Bound abilities

Base spell IDs are from `knowledge/classes/demon-hunter/havoc/ability-inventory.tsv`. Demon-form
override IDs are **invisible to Tier 1** and resolved live via R7 — the reference numbers carry ⚠.

| Key | Ability | Base spell ID | Demon-form override | Lane | Cues |
| --- | --- | ---: | --- | --- | --- |
| `metamorphosis` | Metamorphosis | `191427` | — | COOLDOWN | readable hold (C) |
| `eye_beam` | Eye Beam | `198013` | Abyssal Gaze ⚠ | COOLDOWN | — |
| `the_hunt` | The Hunt | `370965` | — | COOLDOWN | sealed hold (C) |
| `essence_break` | Essence Break | `258860` | — | COOLDOWN | positive Fury-banked cue (B, S1 graded); supplies The Hunt's hold window |
| `vengeful_retreat` | Vengeful Retreat | `198793` | — | COOLDOWN | — |
| `chaos_strike` | Chaos Strike | `344862` | Annihilation ⚠`201427` | ROTATION | affordability (A) + demon-form promotion (D) |
| `blade_dance` | Blade Dance | `188499` | Death Sweep ⚠`210152` | ROTATION | demon-form promotion (D) + identity |
| `felblade` | Felblade | `232893` | — | ROTATION | affordability hold (A) + overcap readout (B) |
| `demons_bite` | Demon's Bite | `344859` | — | ROTATION | affordability hold (A) + overcap readout (B) |
| `immolation_aura` | Immolation Aura | `258920` | Consuming Fire ⚠ | ROTATION | charge-at-full "don't cap" (R6) + identity |
| `throw_glaive` | Throw Glaive | `185123` | — | FALLBACK | — |
| `fel_rush` | Fel Rush | `344865` | — | FALLBACK | — |
| `demonsurge` | Demonsurge (buff) | `452402` | — | — | **OPEN** — hero-signature; no hint until measured |

`demon_form` is not a bound *ability* — it is a readable **marker** and an optional **bar**
surface, read from the transform identity fact (R7), and it drives cue D.

## The lanes, and why the priority falls out of them

The verified Fel-Scarred priority (Icy Veins 12.1, re-ordered 2026-08-12) is: Metamorphosis →
The Hunt → Felblade-w/Inertia → Vengeful Retreat → **windowed** Death Sweep / Annihilation →
Immolation-at-2 → Eye Beam → Essence Break → baseline Death Sweep → **raw Annihilation/Chaos
Strike (~#20 of 24)** → Felblade filler → Throw Glaive / Fel Rush. Read that against the lanes:

- **COOLDOWN** = the top of the priority (Meta, The Hunt, Eye Beam, Essence Break, Vengeful
  Retreat). They light when ready; a hold cue (C) says when to wait.
- **ROTATION** = the middle-to-bottom, where the cues do the ordering. The raw spender is *low*
  by default and only rises when cue **D** promotes it inside a readable window; the generator
  rises (relatively) when cue **A** dims the starved spender; the generator is pushed off by cue
  **B** near overcap; Immolation Aura lights only when its charges read full (R6).
- **FALLBACK** = pure filler (Throw Glaive, Fel Rush).

Tier + cues, read together, reproduce that priority — which is the §3.1 point. No lane is a
strict rank; the cues cross lanes (a promoted Death Sweep in a window outranks a lit Eye Beam,
exactly as the guide's #5 outranks its #8).

## Roster — player problem → fact → recipe → treatment

### COOLDOWN lane

- **Metamorphosis** (`191427`). *Problem:* ~2 min burst, and pressing it while Eye Beam is up
  wastes its Eye Beam reset. *Fact:* `ready` (R2) for the lane; the hold condition is
  **`ready(EyeBeam) AND NOT identity(demon-form)`** — both readable (R2 + R7). *Treatment:*
  COOLDOWN + **readable hold** cue (C1), reusing Demonology's readable-marker shape. The ✕ says
  "let Eye Beam go on cooldown first, so Meta's reset banks a second cast."
- **Eye Beam** (`198013` → Abyssal Gaze ⚠ in Meta). *Problem:* keep the demon-form window
  rolling — it enables everything downstream. *Fact:* `ready` (R2). *Treatment:* COOLDOWN, no
  hold. Same row across the FS override via R7.
- **The Hunt** (`370965`). *Problem:* on cooldown, but **not inside an Essence Break window**.
  *Fact:* `ready` (R2) for the lane; the hold depends on the **Essence Break amp remaining**, a
  **sealed duration** (S4 range step-curve on a duration object → texture alpha). *Treatment:*
  COOLDOWN + **sealed hold** cue (C2). If the remaining reads back secret, that is expected —
  only an eyeball proves the ✕ drew.
- **Essence Break** (`258860`). *Problem:* mandatory in S2 (+49% initial, tier-set keys off it);
  open the amp window with Fury banked (≥35) and flood it. *Fact:* `ready` (R2), plus the **"Fury
  banked ≥35"** precondition — secret, but **expressible as a positive sealed threshold cue**: cap
  cannot read Fury, but it hands the client an authored break point (`35 / maxFury`) via S1's
  `sealed-power-percent` power curve and the client lights a **"banked"** cue when secret Fury clears
  it — the *same S1 tool as the generator overcap readout (cue B), positive polarity*. cap authors 35
  and never learns the value. Also **supplies the sealed duration** gating The Hunt's hold.
  *Treatment:* COOLDOWN + positive Fury-banked cue (S1 graded). (This corrects an earlier design note
  that called the banked gate unreadable/unrankable: a threshold is a client-side paint, not a Lua
  branch, so it is expressible — `../spec.md` §3.1 honest-limit.)
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
  that matters — don't sit on capped charges (2/2 with A Fire Inside). *Fact:* charges are
  **readable only at full** (R6): `currentCharges` reads plain iff at max, secret below — the
  plain read *is* the "capped" signal, so R6's limit is a feature here. *Identity (R7):* Immolation
  Aura is *the* transform that corrupts charge math (→ Consuming Fire, different id/charges) — use
  override-aware max and **re-seed on the flip**. *Treatment:* ROTATION, lit as "spend it" only
  while it reads full; withhold otherwise (unknown ≠ "not capped"). Needs the "capped" provider
  (below).

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

## The four cues, collected

| Cue | What the player sees | Fact | Tool / lane | Recipe | Sink |
| --- | --- | --- | --- | --- | --- |
| **A** affordability | starved spenders dim; generators hold | `insufficientPower` | emphasis (readable) | R1 | ROTATION emphasis |
| **B** Fury threshold (two polarities) | **negative:** generator Fury readout turns red near overcap · **positive:** Essence Break lights a "banked" cue at Fury ≥35 | secret Fury-% vs authored break | cue (sealed) | S1 (graded) + R4 static table | color curve → text/color |
| **C1** readable hold | ✕ on Metamorphosis while Eye Beam ready & not transformed | `ready(EyeBeam) AND NOT identity` | emphasis-adjacent marker (readable) | R2 + R7 | hold marker (readable lane) |
| **C2** sealed hold | ✕ on The Hunt while the Essence Break window counts down | Essence Break amp remaining | cue (sealed) | S4 range step-curve on a duration object | curve → texture alpha |
| **D** demon-form promotion | Annihilation / Death Sweep brighten in demon form | `identity(transformed)` | emphasis (readable) | R7 | ROTATION emphasis (promotion) |

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
   object (S4). Before building, **check the current desktop renderer's marker vocabulary**: if
   it already has a `hold` marker slot (`Overlay.lua` `SLOTS`), C2 reuses it and edits nothing in
   Treatment/Overlay (the 9.4 definition-of-done). Demon-form promotion (D) is plain emphasis on a
   readable fact — no new renderer.

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
   `scenarios.md` walk (ST-4, ST-14). Does a self-buff expose a *readable* "present" boolean
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
- **Convergence is the goal, not a violation (§3.1):** cap layers emphasis + cues to make the
  right press findable and never withholds legal, displayable information to keep a hint vague.
  What it never builds is a single channel that computes the answer from your state.
- **Unknown never becomes confidence,** including through negation. A refused `affordable` or
  `ready` withholds; it does not assert the opposite.
- The catalog declares **no** continuous grade, no resource gate (Fury is secret), no silence
  list, no cast sequence, no coverage rule, and no vocabulary a cue does not use.
