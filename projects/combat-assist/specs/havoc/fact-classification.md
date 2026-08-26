# Havoc Demon Hunter (Fel-Scarred) — fact classification

**Purpose.** A single audit table for every fact the Havoc / **Fel-Scarred** catalog relies on.
For each fact it names the safety lane (readable / sealed-display / open), the canonical
recipe ID it maps to, the `knowledge/addon-dev/` evidence behind that recipe, and the
catalog row(s) and cue that consume it. Read it as the proof obligation for `../spec.md` §3.6:
no sealed fact ever enters a Lua condition, and no open fact is silently treated as known. It
classifies **only** what `catalog.md` consumes — if a fact is not in that catalog, it is not
here. (Aldrachi Reaver is a **separate catalog authored later**; its `Reaver's Glaive` shape is
not classified here.)

**Cross-links.** Normative catalog: `catalog.md` (beside this file, Fel-Scarred). Priority walk
that consumes these facts scenario-by-scenario: `scenarios.md` (beside this file). Recipe bodies +
their evidence: `../authoring.md`'s recipe index (`R1`…`R10`, `S1`…`S9`, the mechanism seams). Safety boundary and
product surface: `../spec.md` §3.1 (the two-tools split — emphasis vs cues) and §3.6 (the
readable/sealed data-path rule). Sealed forms are named here as the **code** names them — `player-aura-stacks`,
`sealed-power-percent`, `sealed-cooldown-range` — and `../spec.md` §3.6 uses the same three.
`sealed-duration-range` names a **different, unbuilt** form (the demon-form window bar, §3.3).

## Legend — the three lanes

- **readable** — Lua *may* compare, index, add, or truth-test it. It may drive **scan
  membership** — the one bit cap decides, castable-or-not — or a readable marker
  (`../spec.md` §3.1). (The role lanes COOLDOWN / ROTATION / FALLBACK this legend used to name
  were removed 2026-08-25: membership does not rank, and one lit row is not brighter than
  another.)
- **sealed-display** — Lua may only forward the value to a client-owned display sink (color
  curve, texture alpha, duration-object bar). It is **never** compared, indexed, added, or
  tested for truthiness. cap reports `offered` / `armed` / `refused` and never reads back.
- **open** — unmeasured or no API. It produces **no hint**. A load-bearing open fact is a
  stop-and-ask (`../spec.md` §3.6), not a guess.

**The two tools (`../spec.md` §3.1).** cap says things two ways. **Emphasis** is an on/off
treatment driven by comparisons over values cap is allowed to *read* — it moves scan membership
and readable markers, and it can be moved **only** by a readable fact. **Cues** are additive
display forms fed by values cap may *display but not read* — colors, readouts, hold marks, bars
— that stack and move but are never read back. Six cues do the fine ordering: **A** affordability
(readable), **B** overcap (sealed), **C** hold/sync (**C1** readable + **C2** sealed), **D**
demon-form promotion (readable), **F** the talent gate (readable) and **G** the single-target
skip (readable). **E**, charges capped, is the seventh and the only positive one.

⚠ **The readable/sealed line moved on 2026-08-17, in one direction: toward sealed.** Re-sourcing
the catalog from the Tier-1 simc APL replaced three *readiness* conditions with *remaining-time*
ones, and a remaining time is sealed. Metamorphosis's Eye Beam hold, both of The Hunt's holds and
both of Vengeful Retreat's sync holds are `sealed-cooldown-range` bands; only Metamorphosis's
two **reset marks** (Eye Beam ready, Blade Dance ready) remain readable. The badge is identical
either way — the difference is entirely on cap's side, and it is a **verification** difference: a
sealed rule is reported `offered`, never *lit*, so it is confirmed by eye in game rather than
from a capture.

**A structure this pass made concrete: a marker carries one `display`, two markers union (OR)
rather than intersect (AND) — but a sealed marker MAY carry readable gates.** A `when` beside a
`display` shipped this pass (cue F's mechanism), so *"this sealed value, but only while these
readable things hold"* is one authored mark. What has no single-mark form is a value-to-value
comparison across the line. Three conditions cross it — The Hunt's rung-4 hold, Vengeful Retreat's
rung-5 alignment gate, and Metamorphosis's rung-3 condition. The first is gated rather than
sliced; the second is authored as the **actionable slice** of the real condition and marked as
such; the third splits cleanly, because its two halves are an OR (`meta_wastes_eye_beam` ∪
`meta_awaits_eye_beam` ∪ `meta_wastes_death_sweep`) rather than an AND of a readable and a sealed
term.

## Main classification table

| Fact | Lane | Recipe | addon-dev evidence | Catalog rows / cue that consume it | Notes |
| --- | --- | --- | --- | --- | --- |
| `ready` — spell readiness / off cooldown | **readable** | R2 | `cooldown-manager.md`, `cdm-rider-patterns.md` — Settled | Metamorphosis, Eye Beam, The Hunt, Essence Break, Vengeful Retreat, Blade Dance/Death Sweep, Chaos Strike/Annihilation (and Throw Glaive / Fel Rush) | Alert-edge latch in combat, direct read out of combat. Supplies the readiness signal on every lit row. |
| `affordable` / `insufficientPower` — can I afford this cast | **readable** | R1 | `security-taint-and-restricted-data.md` — Settled | **Cue A.** Chaos Strike/Annihilation (`chaos_strike_starved`) **and Blade Dance / Death Sweep** (`blade_dance_starved`) — both spenders wear `starved` when `insufficientPower`; Felblade & Demon's Bite (generators have no Fury cost → never unaffordable → stay lit) | Read the *second* return of `C_Spell.IsSpellUsable`; binary, so it cannot drive overcap (that is cue B). Reflects the secret Fury without exposing the number — the relative shift (starved spender dims while the lit generator holds) is the whole signal. |
| `identity` / demon-form transform (`overrideSpellID ~= spellID`) | **readable** | R7 | `cooldown-manager.md`, `observations.md` — Settled | Chaos Strike→Annihilation, Blade Dance→Death Sweep, Eye Beam→Abyssal Gaze, Immolation Aura→Consuming Fire, demon-form marker, **cue D promotion** | The readable identity spine. Bind static `primary = override or base`; keep a stable `spellIDs` union; check a `0`-override explicitly (Lua `0` is truthy). Never build identity on `item:GetSpellID()` (secret + moving in combat). |
| Immolation Aura **charge state** (the "capped" signal) | **readable, in BOTH directions — one drawn, and talent-gated** | R6 (+ R7 identity safety) | `observations.md` (OBS-066, Conflagrate) — Settled; `GetSpellCharges().isActive` is annotated `NeverSecret` | Immolation Aura / Consuming Fire "don't cap charges" row | ⚠ **Re-grounded 2026-08-14 from `currentCharges` onto `isActive`**, and **narrowed 2026-08-17 to the capped direction only.** `isActive` is `NeverSecret` and answers both ways, but the below-max half was `capped` negated and therefore drew a negative badge across the whole steady state — against APL rungs 20 and 25, which press this button at one charge. Below max now draws **nothing** from this fact. ⚠ **And the capped direction is gated on A Fire Inside** (row below): on a one-charge button `isActive` is `false` whenever it is merely ready, so ungated it asserts "you are losing a charge" for the entire fight. What `isActive` still cannot say is *which* charge is recharging (true at both 1/2 and 0/2), which is why "about to cap" still has no authored form (`catalog.md` cue E). R7 is about reading the right spell's charges across the flip. A refused read is still no cue at all. |
| Secret **Fury value / Fury-%** | **sealed-display** (`sealed-power-percent`) | S1 (graded route) + R4 authored generation table | S1: `security-taint-and-restricted-data.md` — Settled · R4 generation: **no API, authored static table** | **Cue B, negative only.** Felblade & Demon's Bite break-point readout | Fury is a **secret primary** (R3) — *unlike* Demonology's readable Soul Shards, cap may only *display* it, never branch. **A threshold is a client-side paint, not a Lua branch**, so an authored break point on secret Fury-% is expressible. `maxFury` readable via `UnitPowerMax` (measured **170**, do not hardcode 120). The break is authored **two ways**: as a **`generation`** amount, breaking at `(maxFury − generation)/maxFury` (Demon's Bite 25, from the authored table — no API reports generation); or as an absolute **`threshold`** lifted off an APL condition, breaking at `threshold/maxFury` (Felblade 100, from rung 22's `fury<=100`). ⚠ `threshold` is new mechanism (`Channel.ThresholdBreak`), added because an absolute Fury level cannot be authored as a generation without smuggling a hardcoded `maxFury` into the catalog. Either way cap authors one number, performs one division, and never learns which side the value fell on; captures report `offered`. ⚠ **The positive "banked ≥35" half is DELETED** — the APL puts no Fury term on Essence Break at all. |
| **A related ability's cooldown REMAINING** (a sealed duration) | **sealed-display** (`sealed-cooldown-range`) | S4 (step-curve on a duration object → texture alpha) | `cdm-rider-patterns.md` (`Channel.Threshold`) — Settled | **Cue C2**, in TWO senses. `within` — Essence Break (Eye Beam ≤4s) · Metamorphosis (Eye Beam ≤8s) · The Hunt (Meta ≤15s) · Vengeful Retreat (Eye Beam ≤8s **or** Meta ≤4s). `beyond` — The Hunt (Eye Beam ≥10s) | The curve reads ~true only while the named ability's cooldown-remaining sits inside (`within`) or past (`beyond`) the authored threshold, piped into the holder's badge alpha. **`beyond` is two points, not three** (`Channel.BeyondPoints`): Step holds the last value out to infinity, so a rise at the threshold with nothing after it IS "far away". ⚠ **Both senses read NOTHING at zero remaining** — a band means *imminent* or *far*, never *ready*. For `within` that gap is mostly harmless, because elimination reaches a ready dependency sitting to the holder's **left** anyway; where the holder sits to the dependency's left it is **not** harmless, which is why Metamorphosis carries a readable `ready(eye_beam)` marker beside its band and Essence Break does not need one. ⚠ **ANDing two sealed facts has no single-mark form yet** — one `display` per marker, and two markers union — so Vengeful Retreat's "both are far" hold is unauthored; two `beyond` bands as separate instances would draw it, at the cost of a reading in which one lit band does not mean hold (`catalog.md` C2). ⚠ All five widths are **authored guesses until flown**. |
| Demon-form window **remaining duration** | **sealed-display** (`sealed-duration-range`) | S3 / S4 / S5 duration-object path (reuse the Tyrant-bar `Bars.lua` sink) | `observations.md` (OBS-034/035), `cooldown-manager.md` — Settled | Optional demon-form countdown bar (§3.3) | Client owns the remaining time; cap arms the bar and never reads it back. Reuses the existing Tyrant-bar duration-object sink — no renderer edit. Experiment: stays only if it earns screen space. Distinct from the *readable* identity marker above. |
| Readable **dependency readiness** — is a related ability off cooldown | **readable** | R2 + R7 (composed) | R2: `cooldown-manager.md`, `cdm-rider-patterns.md`; R7: `cooldown-manager.md`, `observations.md` — Settled | **Cue C1.** Metamorphosis's two reset marks — Eye Beam *ready* and Blade Dance / Death Sweep *ready* | Readable readiness, no sealed value. Either one says Meta's reset would be thrown away, so each raises the red `blocked` badge and the two union into one. A satisfied dependency draws **nothing**. Shown only while the parent is castable / not transformed. Reuses Demonology's readable-marker shape — no new renderer. ⚠ **The Hunt's sync mark left this row on 2026-08-17.** It was `ready(metamorphosis)` and the polarity was inverted: the APL *casts* The Hunt when Meta is ready and holds it while Meta is close. Readiness was the wrong fact; the hold is now a sealed band on Meta's remaining time (row below). |
| **Demon-form promotion** — the readable `identity(transformed)` fact drives emphasis | **readable** | R7 | `cooldown-manager.md`, `observations.md` — Settled | **Cue D.** Annihilation & Death Sweep brighten while transformed | Promotion is **emphasis** (readable-driven), not a cue that reads a value: the empowered spenders rise inside the demon-form window because a *readable* fact favors them — which is why the raw spender (~#20 baseline) correctly climbs in its window. It can **never** be driven by a sealed value; a window whose active-state is sealed may only inform via a cue, never promote. |
| **Essence Break / Demonsurge window active-state readable?** | **open** | — (would gate promote-vs-inform for those windows) | Open — unmeasured | (no hint until resolved) Essence Break window promotion; Demonsurge | **The key new open fact.** Cue D promotes off a *readable* window; demon form is readable (R7) so it ships now. Whether the Essence Break amp and the Demonsurge empowerment expose a readable active-state decides whether those windows can **promote** (emphasis) or may only **inform via a marker** (cue). Until measured, they inform, never promote. Route `@verify-ingame` / `@pending-test`. |
| **Demonsurge readable at all?** (readable proc/aura vs sealed) | **open** | — (gates the Demonsurge row) | Open — unmeasured | (no hint until resolved) Demonsurge (Fel-Scarred hero-signature) | Does the Fel-Scarred Demonsurge empowerment expose a readable proc/aura, or is it sealed? Gates the Demonsurge row entirely. Route `@verify-ingame` / `@pending-test`. |
| **Inertia proc glow on Felblade** | **open** | — (gates the Felblade Inertia-rise cue) | Open — unmeasured | (no hint until resolved) Felblade | Does Inertia surface as a readable proc glow on Felblade? Gates the Felblade Inertia-rise cue. Load-bearing only on the Inertia build (the S2 Exergy build does not need it). Route `@verify-ingame`. |
| **Immolation Aura charge row behaves as measured in instanced combat** | **open-to-confirm** | R6 (candidate-settled by mechanism) | `observations.md` (OBS-066, Conflagrate) — Candidate, confirm in-client | Immolation Aura's two-state row | Re-grounded with the row above: the question is no longer "is it readable at full" but whether **`isActive`** answers on Havoc's row in instanced combat as it did on Conflagrate's. `NeverSecret` says it must; the whole two-state treatment rests on it, so it is a named flight question rather than an assumption. Route `@verify-ingame`. |
| **Buff-maintenance marker readability (Exergy / Serrated Glaive "present")** | **open** (candidate **readable** present + **sealed** remaining) | R2-adjacent aura read + S4 (sealed duration) | Open — unmeasured | (no hint until resolved) Vengeful Retreat (Exergy) in the `scenarios.md` VR sequences; Throw Glaive (Serrated Glaive) in ST-12's tail | **Named by the `scenarios.md` walk.** Does a self-buff expose a *readable* "present" boolean via `C_UnitAuras` while its **remaining duration stays sealed**? If yes: an optional readable "buff present / missing" marker on the maintain-on-cooldown press, with any countdown as a sealed duration (S4). Until measured it is **open** — the press is directed by readiness (lit COOLDOWN) alone, and the VR→Eye Beam weave stays player-trained (never a cap sequence, `../spec.md` §4). Route `@verify-ingame` / `@pending-test`. |
| **Is a talent taken?** — the active trait config's node/entry selection | **readable** ⚠ `[gap]` on the call | new `talent` predicate (no shelf recipe — it is a gate, not a display) | ⚠ **`knowledge/addon-dev/` records NOTHING about `C_Traits.GetNodeInfo`** — not its shape, not whether `ranksPurchased` / `activeEntry` survive combat restriction | **Cue F.** Gates `immolation_capped` on **A Fire Inside + Burning Wound** (rung 10's own pair) and both of The Hunt's C2 bands on **Eternal Hunt** | ⚠ **It reads the trait config, NOT a proxy.** `C_SpellBook.IsSpellKnown` answers about a *spell* and a max-charge count answers about a *button*; each stands in for the talent rather than being it, and a proxy that diverges fails silently. Key off what the APL keys off, whenever that is readable. *(An `IsSpellKnown` route was proposed earlier in this file's lineage and is superseded.)* ⚠ **Not a fix for a stuck badge.** An earlier draft claimed a one-charge Immolation Aura would wear the gold badge for the whole fight; it would not. `Sense.readCapped` returns `nil` at `maxCharges <= 1` — a guard predating this work — so `capped` there is UNKNOWN and the badge would be **blind**. What the gate buys is that the rule is *deliberate* and stated where the rule is, rather than resting on a guard in another module that nobody would think to preserve. The genuine defect in that area is the opposite one, and it is the skip's: a bare `!capped` marker is permanently blind on a one-charge build, which is why the skip is a De Morgan union. **Unknown-safety:** every read is `pcall`ed and every unrecognised shape becomes `nil` → UNKNOWN → **nothing drawn**. A refusal costs the badge; it can never invent one. Cached, dropped on the CDM/talent event set — every one of which is a **hint**, per `cooldown-manager.md` §4's measured ~4.7 s lead. Route `@verify-ingame`. |
| **Is the player in AoE mode?** — cap's own `/cap aoe` toggle | **readable, and not a game read at all** | new `aoe` predicate (subject-less) | n/a — cap owns the value; there is nothing to measure and nothing to restrict | **Cue G.** Gates the `immolation_single_target` union — the Fel-Scarred priority's one target-count term, rung 20's `active_enemies>1` | The client will not tell an addon how many things it is fighting, so cap asks the player and branches on **its own state** (`Mode.lua`). That makes this the safest fact in the table — it cannot be secret, cannot go unknown in the client, and needs no evidence row. It is also the **weakest**: a player who forgets to toggle gets the wrong badge and cap will not know. ⚠ The toggle now calls `Bind.Evaluate`, which re-runs the verdict without re-resolving rows, so it is combat-safe — which matters, because mid-pull is exactly when it is reached for. |

## Sealed facts — proof they are never branched

Each sealed fact flows to exactly one client-owned sink and is never compared in Lua:

- **Secret Fury value / Fury-%** (`sealed-power-percent`, S1 graded → cue B, **negative only**) →
  a **color curve** whose break point is an authored Fury number, evaluated in C on the secret
  Fury-% and painted onto a sink. Two authoring forms, one mechanism: `generation` → break at
  `(maxFury − generation)/maxFury` (Demon's Bite 25); `threshold` → break at `threshold/maxFury`
  (Felblade 100, off APL rung 22). A threshold is a paint, not a branch. Lua supplies the curve
  and the sink; it never learns the number or which side of the break it fell on. cap reports
  `offered` / `armed` / `refused`.
- **A dependency's cooldown remaining** (`sealed-cooldown-range`, S4 → cue C2) → a **step-curve
  on that ability's cooldown duration object → texture alpha** on the holder's badge. Five
  consumers: Essence Break (Eye Beam within 4s — don't clip the amp window into Eye Beam),
  Metamorphosis (Eye Beam within 8s — don't spend the reset on a cooldown about to return),
  The Hunt (Eye Beam **beyond** 10s — the empower would burn long before its Eye Beam — **or**
  Meta within 15s — save it for the Eye Beam the reset hands you), and Vengeful Retreat (Eye Beam
  within 8s **or** Meta within 4s). Lua never reads the clock; the curve result goes straight to
  the draw call. Reported `offered` / `armed` / `refused` — or **`gated`**, when a readable term
  beside the display withheld the paint.
- **Demon-form window remaining** (`sealed-duration-range` in `spec.md`'s vocabulary; not yet
  built, so no shipped name contradicts it — S3/S4/S5) → a **duration-object bar**
  (the Tyrant-bar sink); cap arms it and never reads it back. Reported `offered` / `armed` /
  `refused`.

None of these three ever appears in a Lua condition. **Emphasis — scan membership, cue A
affordability, the cue D demon-form promotion, and the two new gates F and G — is driven ONLY by
readable facts** (`ready` R2, `affordable` R1, `identity` R7, the capped-at-full charge read R6,
the trait-config `talent` read, and `aoe`, which is cap's own state rather than a read at all).
Sealed windows (cues B and C2, and the demon-form bar) inform via a cue and never move emphasis;
every remaining-duration and the Fury value are sink-only.

⚠ **Cue G is the one place a marker's AND-only grammar was not enough**, and the workaround is
worth recording because it is reusable. `immolation_single_target` means
`!aoe & ready & affordable(chaos_strike) & !(capped & a_fire_inside & burning_wound)`, and that
last conjunct is a *negated conjunction* — a disjunction. A marker cannot hold one, but markers
naming the same cue **union**, so it is authored as the triple `!capped` /
`!talent(a_fire_inside)` / `!talent(burning_wound)`. **De Morgan through the union is the general
move: `!(P & Q & R)` is three markers, `P & Q & R` is one.**

⚠ **A union of SEALED markers needs one badge frame each, and that is a render fact worth
recording beside the grammar.** Two readable markers naming a cue simply both add the key, and the
badge draws once. Two sealed bands each write the badge's *alpha* from their own curve — and those
values are secret, so they cannot be compared or maxed to take the larger. A shared frame would
show whichever band wrote last. `Overlay` therefore gives each graded marker its own instance,
stacked at the same slot, and lets the compositor do the OR.

⚠ **And the gate form has its own audit state.** A sealed marker carrying readable `when` terms
reports `gated` when they withhold — distinct from `refused`, because nothing failed: the curve
armed fine and cap chose not to let the client paint it.

## Open facts — the in-client tests

Route as `@verify-ingame` / ClientLab `@pending-test` markers, never guesses. Kept consistent
with `catalog.md` → *Open facts to measure in-client* (same eight, same order):

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
   expose a readable "present" boolean while its remaining duration stays sealed? Named by
   the `scenarios.md` walk (the VR sequences / Exergy; ST-12's tail / Serrated Glaive).
   Gates an optional maintain-on-cooldown "buff present / missing" marker; the press ships on
   readiness alone until resolved. Marker: `@verify-ingame` / `@pending-test`.
6. **Is an owed empowered cast readable?** (`action.death_sweep.demonsurge_available` /
   `action.annihilation.demonsurge_available`.) Rung 3's third hold — don't recast Metamorphosis
   while empowered casts are still owed — is drawn by nothing. `proc` already exists in the
   grammar, so if an owed cast surfaces as a readable proc this is cheap. **Not built** — filed in
   `../backlog.md` as an optimisation over the baseline. Marker: `@verify-ingame`.
7. `[gap]` **What does `C_Traits.GetNodeInfo` actually return, and does it survive combat?**
   The `talent` predicate is **built and shipping**, keyed on `ranksPurchased` and
   `activeEntry.entryID` for the active config. Nothing in `knowledge/addon-dev/` records that
   shape, whether either field is secret in instanced combat, or whether the config id is
   available before `PLAYER_ENTERING_WORLD`. The code is unknown-safe in every direction, so this
   is a **fidelity** question, not a safety one: a silent refusal costs Havoc its gold badge and
   frees the single-target skip, and nobody is told. Measure, then rewrite the claim with
   `[client YYYY-MM-DD]`. Marker: `@verify-ingame`.
8. **Do the five sealed hold bands have the airtime they were authored for?** Question: are
   within-8s (Metamorphosis on Eye Beam), beyond-10s and within-15s (The Hunt), within-8s and
   within-4s (Vengeful Retreat) the right widths? cap reports that it *offered* a sealed rule, never whether the badge lit, so this is
   an eyeball in game rather than a capture. Cycle of Hatred makes Vengeful Retreat's Eye Beam
   band the most likely to never fire at all. Marker: `@verify-ingame`.
