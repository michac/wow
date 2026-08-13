# Havoc Demon Hunter (Fel-Scarred) — fact classification

**Purpose.** A single audit table for every fact the Havoc / **Fel-Scarred** catalog relies on.
For each fact it names the safety lane (readable / sealed-display / open), the canonical
pattern-shelf recipe it maps to, the `knowledge/addon-dev/` evidence behind that recipe, and the
catalog row(s) and cue that consume it. Read it as the proof obligation for `../spec.md` §3.6:
no sealed fact ever enters a Lua condition, and no open fact is silently treated as known. It
classifies **only** what `catalog.md` consumes — if a fact is not in that catalog, it is not
here. (Aldrachi Reaver is a **separate catalog authored later**; its `Reaver's Glaive` shape is
not classified here.)

**Cross-links.** Normative catalog: `catalog.md` (beside this file, Fel-Scarred). Priority walk
that consumes these facts scenario-by-scenario: `scenarios.md` (beside this file). Recipe bodies +
their evidence: `../pattern-shelf.md` (`R1`…`R10`, `S1`…`S6`, Part-3 seams). Safety boundary and
product surface: `../spec.md` §3.1 (the two-tools split — emphasis vs cues) and §3.6 (the
readable/sealed data-path rule). Sealed forms are `../spec.md` §3.6's `player-aura-stacks`,
`sealed-power-percent`, `sealed-duration-range`.

## Legend — the three lanes

- **readable** — Lua *may* compare, index, add, or truth-test it. It may drive an **emphasis**
  tier (the role lanes COOLDOWN / ROTATION / FALLBACK) or a readable marker.
- **sealed-display** — Lua may only forward the value to a client-owned display sink (color
  curve, texture alpha, duration-object bar). It is **never** compared, indexed, added, or
  tested for truthiness. cap reports `offered` / `armed` / `refused` and never reads back.
- **open** — unmeasured or no API. It produces **no hint**. A load-bearing open fact is a
  stop-and-ask (`../spec.md` §3.6), not a guess.

**The two tools (`../spec.md` §3.1).** cap says things two ways. **Emphasis** is an on/off
treatment driven by comparisons over values cap is allowed to *read* — it moves the role lanes
and readable markers, and it can be moved **only** by a readable fact. **Cues** are additive
display forms fed by values cap may *display but not read* — colors, readouts, hold marks, bars
— that stack and move but are never read back. Four cues do the fine ordering: **A** affordability
(readable), **B** overcap (sealed), **C** hold/sync (**C1** readable + **C2** sealed), **D**
demon-form promotion (readable).

## Main classification table

| Fact | Lane | Recipe | addon-dev evidence | Catalog rows / cue that consume it | Notes |
| --- | --- | --- | --- | --- | --- |
| `ready` — spell readiness / off cooldown | **readable** | R2 | `cooldown-manager.md`, `cdm-rider-patterns.md` — Settled | Metamorphosis, Eye Beam, The Hunt, Essence Break, Vengeful Retreat, Blade Dance/Death Sweep, Chaos Strike/Annihilation (and FALLBACK Throw Glaive / Fel Rush) | Alert-edge latch in combat, direct read out of combat. Supplies the readiness signal on every lit row. |
| `affordable` / `insufficientPower` — can I afford this cast | **readable** | R1 | `security-taint-and-restricted-data.md` — Settled | **Cue A.** Chaos Strike/Annihilation (dimmed when `insufficientPower`); Felblade & Demon's Bite (generators have no Fury cost → never unaffordable → stay lit) | Read the *second* return of `C_Spell.IsSpellUsable`; binary, so it cannot drive overcap (that is cue B). Reflects the secret Fury without exposing the number — the relative shift (starved spender dims while the lit generator holds) is the whole signal. |
| `identity` / demon-form transform (`overrideSpellID ~= spellID`) | **readable** | R7 | `cooldown-manager.md`, `observations.md` — Settled | Chaos Strike→Annihilation, Blade Dance→Death Sweep, Eye Beam→Abyssal Gaze, Immolation Aura→Consuming Fire, demon-form marker, **cue D promotion** | The readable identity spine. Bind static `primary = override or base`; keep a stable `spellIDs` union; check a `0`-override explicitly (Lua `0` is truthy). Never build identity on `item:GetSpellID()` (secret + moving in combat). |
| Immolation Aura **charges readable-at-full** ("capped" signal) | **readable (only at full)** | R6 (+ R7 identity safety) | `observations.md` (OBS-066, Conflagrate) — Settled | Immolation Aura / Consuming Fire "don't cap charges" row | `currentCharges` reads plain **iff** at max, secret below — the plain read *is* the capped signal, which is the one Fury-adjacent decision that matters, so R6's limit is a feature here. Override-aware max + re-seed on the transform flip (Immolation Aura → Consuming Fire). Unknown ≠ "not capped": withhold when not readable. |
| Secret **Fury value / Fury-%** | **sealed-display** (`sealed-power-percent`) | S1 (graded route) + R4 authored generation table | S1: `security-taint-and-restricted-data.md` — Settled · R4 generation: **no API, authored static table** | **Cue B, two polarities.** *Negative:* Felblade & Demon's Bite overcap readout. *Positive:* Essence Break "banked ≥35" cue | Fury is a **secret primary** (R3) — *unlike* Demonology's readable Soul Shards, cap may only *display* it, never branch. **A threshold is a client-side paint, not a Lua branch**, so an authored break point on secret Fury-% is expressible in either polarity: **negative** at `(maxFury − generation) / maxFury` ("don't overcap"), **positive** at `35 / maxFury` (Essence Break "banked" — enough to open the window). `maxFury` readable via `UnitPowerMax` (measured **170**, do not hardcode 120); `generation` from the authored table (Felblade +15, Demon's Bite ~20–30, honestly approximate). cap authors the number and never learns which side the value fell on; captures report `offered`. |
| Essence Break **amp window remaining** (a sealed duration) | **sealed-display** (`sealed-duration-range`) | S4 (range step-curve on a duration object → texture alpha) | `cdm-rider-patterns.md` (`Channel.Threshold`) — Settled | **Cue C2.** The Hunt sealed hold marker | Curve reads ~true only while the remaining sits inside the authored band, piped into the hold texture's alpha. Duration supplied by the Essence Break row; guard the Part-3 curve feature-gate. Lua never reads the clock. |
| Demon-form window **remaining duration** | **sealed-display** (`sealed-duration-range`) | S3 / S4 / S5 duration-object path (reuse the Tyrant-bar `Bars.lua` sink) | `observations.md` (OBS-034/035), `cooldown-manager.md` — Settled | Optional demon-form countdown bar (§3.3) | Client owns the remaining time; cap arms the bar and never reads it back. Reuses the existing Tyrant-bar duration-object sink — no renderer edit. Experiment: stays only if it earns screen space. Distinct from the *readable* identity marker above. |
| Readable hold `ready(EyeBeam) AND NOT identity(demon-form)` | **readable** | R2 + R7 (composed) | R2: `cooldown-manager.md`, `cdm-rider-patterns.md`; R7: `cooldown-manager.md`, `observations.md` — Settled | **Cue C1.** Metamorphosis hold marker | Two readable booleans AND-ed; no sealed value. ✕ fires while Eye Beam is ready and you are not transformed ("let Eye Beam go on cooldown first, so Meta's reset banks a second cast"). Reuses Demonology's readable-marker shape — no new renderer. |
| **Demon-form promotion** — the readable `identity(transformed)` fact drives emphasis | **readable** | R7 | `cooldown-manager.md`, `observations.md` — Settled | **Cue D.** Annihilation & Death Sweep brighten while transformed | Promotion is **emphasis** (readable-driven), not a cue that reads a value: the empowered spenders rise inside the demon-form window because a *readable* fact favors them — which is why the raw spender (~#20 baseline) correctly climbs in its window. It can **never** be driven by a sealed value; a window whose active-state is sealed may only inform via a cue, never promote. |
| **Essence Break / Demonsurge window active-state readable?** | **open** | — (would gate promote-vs-inform for those windows) | Open — unmeasured | (no hint until resolved) The Hunt / Essence Break window; Demonsurge | **The key new open fact.** Cue D promotes off a *readable* window; demon form is readable (R7) so it ships now. Whether the Essence Break amp and the Demonsurge empowerment expose a readable active-state decides whether those windows can **promote** (emphasis) or may only **inform via a marker** (cue). Until measured, they inform, never promote. Route `@verify-ingame` / `@pending-test`. |
| **Demonsurge readable at all?** (readable proc/aura vs sealed) | **open** | — (gates the Demonsurge row) | Open — unmeasured | (no hint until resolved) Demonsurge (Fel-Scarred hero-signature) | Does the Fel-Scarred Demonsurge empowerment expose a readable proc/aura, or is it sealed? Gates the Demonsurge row entirely. Route `@verify-ingame` / `@pending-test`. |
| **Inertia proc glow on Felblade** | **open** | — (gates the Felblade Inertia-rise cue) | Open — unmeasured | (no hint until resolved) Felblade | Does Inertia surface as a readable proc glow on Felblade? Gates the Felblade Inertia-rise cue. Load-bearing only on the Inertia build (the S2 Exergy build does not need it). Route `@verify-ingame`. |
| **Immolation Aura charge row readable-at-full in instanced combat** | **open-to-confirm** | R6 (candidate-settled by mechanism) | `observations.md` (OBS-066) — Candidate, confirm in-client | Immolation Aura "don't cap" row (before shipping) | Does Havoc's Immolation Aura charge row behave like the R6 Conflagrate measurement (readable at full, secret below) in instanced combat? Settled by mechanism; confirm the row behaves the same in instanced combat before shipping the tier. Route `@verify-ingame`. |
| **Buff-maintenance marker readability (Exergy / Serrated Glaive "present")** | **open** (candidate **readable** present + **sealed** remaining) | R2-adjacent aura read + S4 (sealed duration) | Open — unmeasured | (no hint until resolved) Vengeful Retreat (Exergy) `scenarios.md` ST-4; Throw Glaive (Serrated Glaive) ST-14 | **Newly named by the `scenarios.md` walk.** Does a self-buff expose a *readable* "present" boolean via `C_UnitAuras` while its **remaining duration stays sealed**? If yes: an optional readable "buff present / missing" marker on the maintain-on-cooldown press, with any countdown as a sealed duration (S4). Until measured it is **open** — the press is directed by readiness (lit COOLDOWN) alone, and the VR→Eye Beam weave stays player-trained (never a cap sequence, `../spec.md` §4). Route `@verify-ingame` / `@pending-test`. |

## Sealed facts — proof they are never branched

Each sealed fact flows to exactly one client-owned sink and is never compared in Lua:

- **Secret Fury value / Fury-%** (`sealed-power-percent`, S1 graded → cue B, **two polarities**) →
  a **color curve** whose break point is an authored Fury threshold, evaluated in C on the secret
  Fury-% and painted onto a sink. **Negative:** the generator's readout goes red at/above
  `(maxFury − generation)/maxFury` ("don't overcap"). **Positive:** Essence Break lights a "banked"
  cue at/above `35 / maxFury` ("enough to open the window"). Same mechanism, opposite polarity; a
  threshold is a paint, not a branch. Lua supplies the curve and the sink; it never learns the
  number or which side of the break it fell on. cap reports `offered` / `armed` / `refused`.
- **Essence Break amp remaining** (`sealed-duration-range`, S4 → cue C2) → a **range step-curve on
  the Essence Break duration object → texture alpha** on The Hunt's hold marker. Lua never reads
  the clock; the curve result goes straight to the draw call. Reported `offered` / `armed` /
  `refused`.
- **Demon-form window remaining** (`sealed-duration-range`, S3/S4/S5) → a **duration-object bar**
  (the Tyrant-bar sink); cap arms it and never reads it back. Reported `offered` / `armed` /
  `refused`.

None of these three ever appears in a Lua condition. **Emphasis — the role lanes, cue A
affordability, and the cue D demon-form promotion — is driven ONLY by readable facts** (`ready`
R2, `affordable` R1, `identity` R7, and the capped-at-full charge read R6). Sealed windows
(cues B and C2, and the demon-form bar) inform via a cue and never move emphasis; every
remaining-duration and the Fury value are sink-only.

## Open facts — the in-client tests

Route as `@verify-ingame` / ClientLab `@pending-test` markers, never guesses. Kept consistent
with `catalog.md` → *Open facts to measure in-client* (same five, same order):

1. **Essence Break / Demonsurge window active-state readable?** Question: do the Essence Break
   amp and the Demonsurge empowerment expose a *readable* active-state (vs sealed)? This decides
   whether those windows can **promote** (emphasis, cue D) or may only **inform via a marker**
   (cue). Demon form ships now (readable, R7); these are the open case — until measured they
   inform, never promote. Marker: `@verify-ingame` / `@pending-test`. *(The key new open fact.)*
2. **Demonsurge readable at all?** Question: does the Fel-Scarred Demonsurge empowerment expose a
   readable proc/aura, or is it sealed? Gates the Demonsurge row entirely. Marker:
   `@verify-ingame` / `@pending-test`.
3. **Inertia proc glow on Felblade.** Question: does Inertia surface as a readable proc glow on
   Felblade? Gates the Felblade Inertia-rise cue. (Load-bearing only on the Inertia build.)
   Marker: `@verify-ingame`.
4. **Immolation Aura charge row readable-at-full.** Question: does Havoc's Immolation Aura charge
   row behave like the R6 Conflagrate measurement (readable at full, secret below) in instanced
   combat? Candidate-settled by mechanism; confirm before shipping the "don't cap" tier. Marker:
   `@verify-ingame`.
5. **Buff-maintenance marker readability (Exergy / Serrated Glaive).** Question: does a self-buff
   expose a readable "present" boolean while its remaining duration stays sealed? Newly named by
   the `scenarios.md` walk (ST-4 Vengeful Retreat / Exergy, ST-14 Throw Glaive / Serrated Glaive).
   Gates an optional maintain-on-cooldown "buff present / missing" marker; the press ships on
   readiness alone until resolved. Marker: `@verify-ingame` / `@pending-test`.
