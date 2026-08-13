# Combat Assist Plus — backlog

**What this file is for:** the current implementation status and the ordered work list.
`spec.md` owns intended behavior; `notes.md` owns completed history; `discussion.md` owns only
questions that still require an author decision.

The live addon version comes from `wowkb.addon list`, never from prose here.

## Status

This is the project's only implementation-status source.

- **The visual vocabulary moved to `render-shelf.md` (2026-08-13).** Every UI opinion — surfaces,
  primitives, colors, motion, placement, composition — now lives there with a
  an `open` status only where a *client capability* is unmeasured, and `spec.md` §3.1/§3.2 keep
  only the model. The old "treatments are static / motion only for a specific observed problem"
  rule is **struck**: it was an experiment written in as a boundary. Trying a look is a shelf edit.
  Assets come from `wowkb.uiart` (real client art; `raw/uiart/manifest.json` records tintability).
- **The shelf declares one style (2026-08-13).** `render-shelf.md` states one treatment per
  primitive and holds every number in its Part 6 `render-tokens` JSON block; alternatives and
  reasoning moved to `render-rationale.md`, which is authoritative over nothing. The three
  vocabularies are reconciled **on paper**: `ClientLab/Mock.lua`'s motion ladder is the style
  (hues, rates, pulse floor, veil), the static four-strip border in cap's `Treatment.lua` is
  superseded, and the artifact's invented style is replaced by a generator. ⚠ **The code has not
  been changed to match** — `Treatment.lua` still draws the static border, and making it match the
  shelf is transcription work that follows the flight.
- **`wowkb.capart` renders the artifact from the docs (2026-08-13).** It reads the shelf's token
  block, `havoc/catalog.md`'s roster table and `havoc/scenarios.md`'s CDM-row bullets; the scenario
  sidecar is seeded by `capart import` and then sits off the build path.
- **The render loop is closed, and the artifact has been looked at (2026-08-13).** `wowkb.serve`
  serves the artifacts directory, watches `specs/`, reruns `capart build havoc` on save and pushes
  an SSE reload — so *edit the shelf → look* is one gesture, with no publish in it. `capart build`
  was stripped to two hard failures (the tint guard; the closed verdict/roster vocabulary) so
  nothing can block a rebuild you want to look at; the byte budget, flipbook geometry and the
  literal-hex scan became a warning or a `check` concern. All 15 icons and 2 sheets are extracted
  from real client art (86 KB of a 512 KB budget) and `havoc-stepper.html` is republished to the
  same URL. The stylized two-letter-abbreviation diagram is **gone**: the artifact is now a
  transcription target. ⚠ Still true that `Treatment.lua` has not been changed to match.
- Demonology remains the small pilot: Tyrant and Demonbolt are its only enhanced entries;
  Dreadstalkers and Grimoire are readable Tyrant dependencies.
- The corrective pass restored the three discrete tiers (then named ASAP / SOON / FALLBACK)
  without restoring continuous grades, pulse policy, exhaustive coverage or automatic sequences.
- **Tier vocabulary migrated (2026-08-12):** the spec now names the tiers **COOLDOWN / ROTATION /
  FALLBACK** as role lanes, and relaxes the single-hint rule so tier + cues may converge on the
  best press without a compute-the-answer channel (`spec.md` §1c / §3.1 / §4). The **built addon
  still emits `ASAP` / `SOON` / `FALLBACK`** (stale v0.2.4 here); the token rename lands at
  transcription (Phase 10.4). Product docs (spec, all three catalogs) use the new names; flight
  items below that still say SOON/FALLBACK describe the current build.
- Phase 9's source pass adds the minimal Destruction / Diabolist proof: Conflagrate tiers from
  readable shards and a seeded charge estimate, plus an independent sealed Backdraft count
  through Blizzard's 12.1 AuraContainer path. It has not flown as a CAP build.
- The engine supports only the readable predicates the pilot uses, propagates unknown safely,
  draws static tier borders and two fixed context dots, leaves Blizzard's proc glow intact,
  and owns one independent Tyrant bar.
- Engine guarantees and provisional Demonology examples are separate test groups. The old
  tier/channel policy suite and its visual-taste assertions are gone.
- The combined Demonology/Destruction checkpoint has not been judged in game. No
  release or deployment is implied.
- Havoc is the first **comprehensive** catalog (**Fel-Scarred specifically**; Aldrachi Reaver is
  a separate future catalog), but it exists **only as machine-independent design** —
  `specs/havoc/catalog.md` (normative), `specs/havoc/fact-classification.md`,
  `specs/havoc/scenarios.md` (the single-row CDM elimination walk — one priority-ordered
  Cooldown-Manager row per state, walked left-to-right, naming why each off-cooldown button is
  skipped until the press; demon-form overrides rendered via R7; **revised 2026-08-13**, see
  Phase 10.1), the `spec.md` §3.7 product section, and four cues (A affordability / B sealed overcap / C
  readable + sealed hold / **D demon-form promotion**). No `Catalogs/Havoc.lua` exists and none of
  it has flown.
  Transcription is blocked on the desktop cap code being pushed (this checkout is the stale
  v0.2.4 vocabulary). See *Phase 10* below.

## Now

### The render shelf — reconcile and regenerate

- [x] Author `specs/render-shelf.md` (surfaces, V1–V10 primitives, composition rules, assets).
- [x] Build `wowkb.uiart` — atlas member → sheet FileDataID → CASC → BLP decode → crop, with
      flipbook grid/CSS recipe, tintability measure, spell icons and a manifest.
- [x] Strip the UI opinions out of `spec.md` §3.1 / §3.2 and point them at the shelf.
- [x] **Reconcile the three divergent vocabularies** onto the shelf (on paper): `Mock.lua`'s motion
      ladder is the style, `Treatment.lua`'s static border is superseded, the artifact's invented
      style is replaced by a generator. Making the *code* match is transcription work, not this.
- [x] Split `render-rationale.md` out so the shelf can declare one style without losing the
      arguments; add both to the doc map and `authoring.md`'s standing rules.
- [x] Add the Part 6 `render-tokens` block — every number in one place, prose citing paths.
- [x] Strip the pixel prose out of `specs/havoc/scenarios.md`; rewrite the CDM-row bullets into a
      machine-read grammar and give ST-10 + the three AoE variants the explicit rows they lacked.
- [x] Build `wowkb.capart` (tokens / assets / import / build / check) and the template trio;
      extract `atlas_image` / `icon_image` from `uiart` with a FileDataID route for slugless icons.
- [x] **Build `wowkb.serve`** — stdlib static server + mtime watch + rebuild command + SSE reload.
      The design loop runs against `file://`-speed local HTML; the published artifact is the
      checkpoint, not the iteration surface.
- [x] **Cut the four ceremony guards from `capart build`.** Only the tint check (a `lane` tint on
      baked-hue art) earns a hard failure — it is the one that stops the preview becoming a lie.
      Drop the byte budget, downgrade the flipbook-grid check to a warning, and move `strict-css`
      and `check` out of `build` so nothing can block a rebuild you want to *look* at.
- [x] Extract the 15 icons + 2 sheets, build the artifact, and **look at it** — icon size, spacing,
      swipe, and whether the ring reads as a ring rather than a CSS glow. 86 KB of a 512 KB budget.
      Four override forms needed the FileDataID route, not three: `Annihilation` 201427 → 1303275,
      `Abyssal Gaze` 452497 → 136149 and `Consuming Fire` 452487 → 135794 join the registered
      three, all read off `SpellMisc.SpellIconFileDataID` rather than guessed.
- [x] Prove the loop: flip one token, rebuild, confirm the change is visible and that only the
      shelf was edited. Prove the guard: point a ring at baked-hue art and confirm it hard-errors.
      Both pass — `pulse.floor` 0.68 → 0.50 reached the live ring through a real page reload with
      only `render-shelf.md` touched; the emphasis ring pointed at `ui-hud-actionbar-proc-loop-flipbook`
      hard-errors naming measured saturation 0.736 and the three fixes.
- [x] Republish the existing artifact URL (`589b5eca-…`) once the local render looks right.

- [x] **Add Part 7, the lab** — a sandbox for treatments that are drawn but not adopted, with the
      isolation rule enforced mechanically (`capart build` errors if `verdicts`/`cues` names a lab
      entry) rather than by convention. Two entries authored and rendering:
      **L1 `border-arrival`** (a solid static border carrying the lane + a one-shot 2×→1× snap on
      arrival, fired by three different causes — cooldown ready, charge returned, now affordable —
      plus a fourth CHARGES lane), and **L2 `badge-slots`** (OS-style circular badges, slot 1's
      centre on the icon's top-right corner, from Kenney's CC0 Board Game Icons vendored at
      `artifacts/assets/kenney/`, measured saturation 0.000 so they tint to any lane hue).

**What the lab's first render showed:**

- **The badges collide in a real row.** At `diameter_pct` 34 on a 56 px icon a corner-centred badge
  overhangs **9.5 px**, and `surfaces.row_gap_px` is **6**. The entry draws three adjacent icons so
  this is visible rather than asserted. Either the diameter comes down, the badge stops being
  corner-centred, or the row gap grows.
- **Solid borders read far cleaner than the ants ring** at the same size — three lanes, instantly
  separable, no ghosting. The arrival snap is legible without being loud.
- The flask and timer glyphs are legible at ~19 px against busy icon art *because of* the dark
  contrast plate, which is CDMProbe's lesson re-confirmed: additive art over icon work washes out,
  and a black disc is the cheap fix.

**What the first honest render showed** — the reason the loop exists, recorded so the next shelf
edit starts from evidence rather than from the same guesses:

- The ants ring **reads as a ring, not a CSS glow** — but Blizzard's own art is a *soft glowing
  rounded square*, not crisp marching dashes. The blur is in the sheet; nothing to fix, and worth
  knowing before anyone tries to "sharpen" it in `Treatment.lua`.
- The flipbook walks all 30 cells and the pulse rides between the declared 0.68 floor and 1.0 —
  measured in the live page, not asserted.
- `starved` (greyscale + veil) is by far the strongest read in the row; it is unmistakable next to
  a plain `cd`.
- **`withheld` is the weakest.** Veil 0.60 alone barely separates bright art (Immolation Aura)
  from an untreated `below` neighbour. It is the one verdict whose treatment is worth revisiting.
- The 62 % swipe covers most of a 56 px icon, so `cd` icons read as "dark" more than as "dialled".
  Faithful to the client, but it means the swipe is carrying less information than it looks like.

### Corrective pass — tier-preserving simplification

- [x] Archive the failed simplification plan and record the false binary it presented.
- [x] Restore the discrete tier contract in the spec, catalog, engine and mechanical tests.
- [x] Reconcile the flight guide around categorical tier recognition rather than graduated
      brightness.

### Checkpoint — static tier baseline

- [ ] Install a test build only after separate release approval, then fly the questions in
      `flight-reading.md` → `Phase 5 checkpoint flight`.
- [ ] Judge whether ASAP / SOON / FALLBACK are immediately distinguishable, plus brightness,
      contrast, size, stock-proc coexistence and whether both setup facts are identifiable.

### Phase 3 — catalog and source migration (complete)

- [x] Remove continuous grades, cue coupling and the rest of the old tier ontology while
      retaining readable markers, optional sealed display bindings and one independent bar.
- [x] Re-author Demonology around Demonbolt, Tyrant and the Tyrant bar only; remove every
      ability without a named pilot problem. §3.4.
- [x] Make readable-only Tyrant setup markers first-class. Keep sealed values out of every Lua
      branch. §3.2, §3.6.
- [x] Remove exhaustive silence coverage and treat unclaimed rows as optional diagnostics.
      §3.6.
- [x] Remove unused or unwired `talent`, `elapsed` and `casts` vocabulary plus automatic
      sequence preparation. §3.6, §4.
- [x] Admit no sealed display binding until one has a live renderer; no successful `nodraw`
      form.
      §3.2, §3.6.
- [x] Replace the four-bar roster with one independent Tyrant bar that does not inherit icon
      treatment. §3.3.
- [x] Update capture fields only where the smaller live model requires it; preserve the shared
      capture wire contract.

## Next

### Phase 4 — tests that say only what tests can know (complete)

- [x] Keep synthetic engine tests for readable branching, sealed-data isolation, unknown-safe
      evaluation, deterministic binding, supported displays and inert failure.
- [x] Move a few Demonology examples into an explicitly provisional characterization suite.
- [x] Delete tests for tier population, silence exhaustiveness, visual taste, automatic
      sequences and the removed vocabulary.
- [x] Keep the Python release runner invoking the suite; it enforces mechanics, not
      product prose.

### Static visual baseline

- [x] Draw three static tier treatments and two fixed readable context markers as a flight
      hypothesis.
- [x] Remove default pulse behavior and unsupported flash-safety arithmetic.
- [x] Leave stock proc glow intact for the baseline and record that route explicitly.
- [ ] Ask for an in-game judgment of tier recognition, brightness, contrast, size and marker
      readability.

### Phase 6 — small Demonology pilot

- [ ] Fly Demonbolt's SOON / FALLBACK transition across low and high readable shard states.
- [ ] Fly Tyrant's SOON tier with separate Dreadstalkers and Grimoire context markers.
- [ ] Fly the independent Tyrant countdown bar and decide whether it earns its screen space.

### Phase 7 — qualitative iteration

- [ ] State one experience question per flight, record play first, then use captures to
      diagnose mechanism behavior.
- [ ] Change one conceptual variable at a time and ask at every product judgment.

### Phase 8 — close the migration

- [ ] Remove obsolete modules, fields, tests and vocabulary rather than retaining compatibility
      scaffolding for an unreleased design.
- [x] Reduce `flight-reading.md` to the fields and criteria the live source still emits.
- [x] Re-derive the Demonology catalog reference around the small pilot.
- [ ] Collapse migration history into `notes.md`, reconcile this status, and delete or archive
      the temporary plan and audit.

### Phase 9 — canonical spec-authoring examples

Make the next spec primarily a gameplay-authoring job rather than another tour through the
Secret Values and Cooldown Manager APIs. Do this with a few concrete vertical examples and
small reusable helpers—not a generalized APL DSL, capability registry or vocabulary for
mechanisms no authored experience uses.

#### 9.1 Name and preserve the examples that already exist

- [x] Treat Demonbolt as the canonical **readable proc + secondary resource → emphasis tier**
      example. Keep the catalog opinion in `Catalogs/Demonology.lua`, the unknown-safe
      evaluation in `Signal.lua`, and all pixels in the shared treatment/overlay path.
- [x] Treat Tyrant as the canonical **readable readiness → emphasis tier** example and its two
      setup dots as the canonical **readable fact → context marker** example. Make the source
      comments name the reusable seam without turning the provisional Demonology opinion into
      engine policy.
- [ ] Treat the Tyrant bar as the canonical **spell duration object → client-owned countdown**
      example if the checkpoint flight says the surface earns its space. If it does not, retain
      the duration-object recipe in the addon-dev KB rather than preserving dead product code as
      an example.

#### 9.2 Establish one real sealed-marker vertical slice

- [x] Choose an approved player problem whose useful fact is sealed and whose marker can inform
      a choice without becoming a next-action verdict. Amend `spec.md` and the relevant spec
      catalog before building it; do not invent a dummy production marker solely to exercise an
      API.
- [x] Carry that one example through the implemented vertical slice: declare the aura dependency,
      let Blizzard's AuraContainer acquire it, and hand its application count directly to the
      FontString sink. Lua never receives or reads back the sealed value.
- [x] Generalize only the seams the completed example actually repeats: marker construction and
      placement belong in the shared renderer; aura/cooldown/totem acquisition and curve guards
      belong in small mechanism helpers; the gameplay threshold and meaning remain in the spec
      catalog/module.
- [ ] Fly the marker in restricted combat in the combined CAP build. Record the player's visual
      judgment first and use the capture only to prove which route armed; an accepted secret
      sink is not evidence that a pixel appeared.

#### 9.3 Build a small pattern shelf as real specs require it

- [x] Remove the obsolete 12.0 `Channel.StackText` acquisition path. Backdraft is the canonical
      **AuraContainer applications → sealed FontString** example on 12.1.
- [ ] Make the first real use of each duration source its canonical example: spell cooldown via
      `C_Spell.GetSpellCooldownDuration`, aura via `C_UnitAuras.GetAuraDuration`, and totem via
      `GetTotemDuration`. Share curve and sink plumbing only after the examples demonstrate the
      same shape; keep source-specific identity and liveness work explicit.
- [ ] When a spec needs a new readable fact, add one narrow, unknown-safe provider with one
      characterization example. Prefer established client verdicts such as cooldown `isActive`,
      CDM alert state, proc state, aura/bar liveness and `IsSpellUsable` over reconstructing a
      sealed value.
- [x] Add focused mechanical tests for charge seeding, spending, gaining, duplicate refusal,
      clamping and reseeding; marker union validation, sealed-data isolation, dependency binding,
      unsupported displays and legal sink routing; and provisional Destruction states.

#### 9.4 Leave a short authoring route for the next spec

- [x] Add a compact “authoring another spec” route: start from the APL, list the facts each useful
      rule needs, classify each as readable / sealed-display-only / unavailable, map readable facts
      to broad tiers and sealed facts to independent context, then point each mechanism to its
      canonical source example and addon-dev evidence. **Superseded 2026-08-13** — the route grew
      into `specs/authoring.md`, the permanent process file (eight stages, entry/exit criteria).
      `CLAUDE.md` and `pattern-shelf.md` now point at it instead of each carrying a copy.
- [x] Keep the route honest about where normal Lua is expected. A new spec may compose existing
      patterns directly; a genuinely new Blizzard mechanism gets researched once, written into
      `knowledge/addon-dev/`, and becomes a shared helper only after a concrete vertical slice
      proves it.
- [ ] Definition of done: a second authored spec can reuse emphasis and at least one context-
      marker pattern without editing the shared renderer, while any engine change it does require
      is a small named mechanism rather than spec-specific Blizzard API plumbing.

### Phase 10 — Havoc comprehensive catalog

The first catalog authored to be comprehensive (whole rotational roster, **Fel-Scarred
specifically** — Aldrachi Reaver is a separate future catalog), and the first stress of the
pattern shelf: Fury is a *secret* primary, so the design is built on four cues (A/B/C/D) over
role-lane tiers instead of a resource gate. Design is machine-independent and complete; Lua
transcription is deferred until the desktop cap code is pushed.

#### 10.1 Design (complete — machine-independent)

- [x] Correct the Season-2 rotation/build KB (Exergy the S2 pick / Inertia still live, VR
      maintain-on-cooldown, Essence Break mandatory, Eternal Hunt apex, Dancing with Fate
      low-mover fallback) — `rotation.md` + `builds.md`, reviewed 2026-08-12. Re-verified the
      priority order against the live Icy Veins 12.1 page (cooldown-dominated; raw spender ~#20).
- [x] Amend the constitution: rename tiers to **COOLDOWN / ROTATION / FALLBACK** role lanes and
      relax the single-hint rule (converge via tier + cues, no compute-the-answer channel) —
      `spec.md` §1c / §3.1 / §4. Migrate the Demonology + Destruction tables to the new vocabulary.
- [x] Author `specs/havoc/catalog.md` — Fel-Scarred-specific normative roster, the four cues, the
      demon-form identity spine, and the authoring route (APL → problem → fact → recipe →
      treatment).
- [x] Author `specs/havoc/fact-classification.md` — every fact tagged readable / sealed-display
      / open, each pointed at its pattern-shelf recipe and addon-dev evidence.
- [x] Author `specs/havoc/scenarios.md` — the normative scenario catalog: walk the full
      Fel-Scarred priority (single-target + AoE, re-verified 2026-08-12) rung-by-rung. Each rung is
      classed by **its ordering-reason and whether cap can read it** (readable rank / sealed cue /
      open). The walk reframed the priority as a **dependency graph** and lifted **three** spec-wide
      rules into `spec.md` §3.1: the dependency-graph / **readable-relationship** rule (Meta ranks #1
      because it resets Eye Beam + Death Sweep, and cap reads Eye Beam's cooldown state to know it),
      the **emphasis-intensity hierarchy** (promoted > lit-cooldown > lit-rotation > dim/off), and
      **eye-direction by elimination**. Key correction from the walk: a secret-resource threshold is
      **expressible** as an authored S1 cue in either polarity (Essence Break "banked ≥35" positive;
      generator overcap negative) — there is **no "cap can't rank" bucket**; the only line is the §4
      oracle (computing on the value). §3.7 gained a Scenario-catalog pointer. Published a second
      Havoc artifact — the scenario stepper (the concept-overview artifact stays).
- [x] **Scenario model revised to the single-row CDM elimination walk (2026-08-13).** Reframed
      `specs/havoc/scenarios.md` from the rung-by-rung "ordering-reason" table to the model the
      author asked for: **one priority-ordered Cooldown-Manager row per state**, walked
      **left-to-right**, naming — for every button that is *not* on cooldown — the reason it is
      skipped (weave off-GCD · hold·readable dot · hold·sealed · starved · overcap · withheld)
      until the press. Adds **demon-form override fidelity** (the row shows Abyssal Gaze / Death
      Sweep / Annihilation / Consuming Fire; cap authors none of it — R7 resolves the live icon)
      and the corrected holds: **The Hunt's hold is a readable Meta-availability dot** (not sealed),
      and the **sealed C2 hold now sits on Essence Break's "Eye Beam ≤4s" condition**. VR-led
      throughout; ten single-target scenarios + three AoE mode-variants, with state toggles on ST-3
      / ST-5 / ST-7. The scenario-stepper artifact was regenerated as a faithful rendering of the
      doc (`https://claude.ai/code/artifact/589b5eca-eb73-424e-8ee8-95d23d22c2ff`). (Docs lead
      artifacts — the standing rule now lives in `authoring.md` §0.) The artifact's data
      model mirrors the doc 1:1 (each scenario = state → per-button walk verdict → press), so a
      doc change is a JS-array change.
- [x] **Reconciled the sibling docs to the corrected holds (2026-08-13).** Fixed `catalog.md`,
      `fact-classification.md` **and** `spec.md` (§3.7 roster table + §3.1 cue-C definition) so all
      four Havoc docs agree: cue **C2 (sealed hold)** belongs to **Essence Break** (hold while Eye
      Beam's cooldown has ≤4s remaining, a sealed duration), **The Hunt's hold is a readable Meta-sync
      dot** (C1), and Metamorphosis's C1 is its **two reset dots** (Eye Beam + Death Sweep cooldowns).
      Also corrected the stale scenario references (buff-maintenance → ST-1 / ST-10; Demonsurge /
      Essence-Break-window promotion → ST-4), struck the "leads Aldrachi Reaver" claim (one
      hero-filtered VR-led list), and re-ordered `catalog.md`'s Meta-led priority summary to VR-led.
      Grep-clean: no doc still ties a sealed hold to The Hunt. *(The full three-docs→one consolidation
      is still open, next item.)*
- [ ] **Owed: consolidate the three Havoc docs → one `catalog.md`** — the one-`catalog.md`-per-spec
      rule is now `authoring.md` §0, and Havoc is the standing violation of it. Fold `scenarios.md` +
      `fact-classification.md` back into `catalog.md` and make `rotation.md` the sole home of the
      priority order. Same deferred cleanup pass. (The scenario-stepper artifact is the standalone
      visual; it renders whatever the consolidated doc says.)
- [x] Amend `spec.md`: §3.7 Havoc catalog section; §3.2 hold-marker two-lane wording (cue C);
      §3.6 the two new sealed forms `sealed-power-percent` (cue B) and `sealed-duration-range`
      (cue C2 + demon-form bar).

#### 10.2 New readable providers / renderer work (deferred to transcription)

Each is a *small named mechanism* under `authoring.md` stage 6's renderer test, confirmed against
`knowledge/addon-dev/` first, with one characterization example:

- [ ] **"Capped" readable provider** — charges readable-at-full (R6): plain read iff at max *is*
      the capped signal; override-aware max + re-seed on transform (R7). First consumer:
      Immolation Aura / Consuming Fire.
- [ ] **Sealed Fury threshold cue (lever B), two polarities** — one S1-graded color-curve
      mechanism used both ways: **negative** per-generator overcap curve keyed to
      `(maxFury − generation)/maxFury` (Felblade +15, Demon's Bite ~20–30, authored **generation
      static table**; no generation API — R4), and **positive** "banked" curve at `35 / maxFury`
      on Essence Break. A threshold is a client-side paint, not a Lua branch, so both polarities
      are expressible; cap never reads which side the value fell on. First consumers: Felblade,
      Demon's Bite (negative); Essence Break (positive).
- [ ] **Sealed hold marker (cue C2)** — range step-curve → texture alpha on a sealed duration
      object (S4). First check whether the current desktop renderer already has a `hold` marker
      slot; if so it reuses it and edits nothing in Treatment/Overlay (the 9.4 definition-of-done).
- [ ] **Demon-form promotion (cue D)** — plain emphasis raised on the empowered spenders while
      the readable demon-form window is active (R7). No new renderer; it is readable-driven
      emphasis. (Essence Break / Demonsurge promotion gated on open fact 10.3.)

#### 10.3 Open facts — measure in-client before authoring the hint (spec.md §3.6)

Routed per `authoring.md` stage 5.

- [ ] Does **Inertia** surface as a readable proc glow on Felblade? (gates any Felblade `proc`
      hint; only load-bearing on the legacy Inertia build).
- [ ] Do **Demonsurge / Reaver's Glaive** empowerment states expose a readable proc/aura, or are
      they sealed? (gates the two hero-signature rows).
- [ ] Does Havoc's **Immolation Aura** charge row read readable-at-full (R6 Conflagrate shape) in
      instanced combat? (candidate-settled by mechanism; confirm before shipping the "don't cap"
      tier).
- [ ] **Buff-maintenance marker (Exergy / Serrated Glaive)** — newly named by the `scenarios.md`
      walk (ST-1 VR weave / ST-10): does a self-buff expose a readable "present" boolean while its remaining
      duration stays sealed? (gates an optional maintain-on-cooldown "buff present / missing"
      marker; the press ships on readiness alone until resolved).

#### 10.4 Transcription + flight (deferred — blocked on desktop push, releasing ask-first)

- [ ] After the desktop cap code is pushed, transcribe `catalog.md` into `Catalogs/Havoc.lua`
      against the *real* current vocabulary; add to `.toc`, register, resolve override ids via
      `overrideSpellID` at bind (never hardcode).
- [ ] Extend the `busted` suite for the new providers: capped/charge seeding + reseed-on-flip,
      lever-B curve guards, marker union (readable + sealed hold lanes).
- [ ] Dry-run `wowkb.addon release cap`; releasing stays ask-first.
- [ ] Fly the affordability tier shift (spenders drop when Fury-starved), the demon-form marker,
      the Immolation-Aura capped tier, and the hold ✕ / overcap-red cues. Record the player's
      visual judgment first; read `wowkb.capture cap` streams only to prove which route *armed*.

## Ideas

- A player-armed sequence-context experiment, only if it can inform a choice without becoming
  a current/next spell guide.
- A second spec chosen because it stresses the simplified design differently.
- Prior-art research after the pilot behavior is concrete enough to ask a narrow question.

## Done

- [x] Simplification Phase 1 — baseline, test classification, normative ledger and approved
      A1–G1 decision packet — 2026-08-11
- [x] First drawn-surface flight and time-weighted capture interpretation — 2026-08-10/11
- [x] Initial icon overlays, sealed markers, proc-glow attempt and cooldown bars — 2026-08-08/10
- [x] Pure catalog/tier/track core and first Demonology catalog — 2026-08-07
- [x] CDM binding, movable panel and standard capture foundation — 2026-08-05/06
- [x] Project scaffold and Cooldown HUD product boundary — 2026-08-05
