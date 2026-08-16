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
  reasoning moved to `render-rationale.md`, which is authoritative over nothing. ⚠ **Superseded
  the same day by the lab promotion below** — the style this bullet reconciled to (`Mock.lua`'s
  motion ladder) is no longer the declared style. The *structure* it established stands.
- **`wowkb.capart` renders the artifact from the docs (2026-08-13).** It reads the shelf's token
  block, `havoc/catalog.md`'s roster table and `havoc/scenarios.md`'s CDM-row bullets; the scenario
  sidecar is seeded by `capart import`. ⚠ **Corrected 2026-08-15 — the sidecar is NOT off the
  build path.** `build` renders scenario prose *from* the sidecar, and `check` compares doc against
  sidecar on `(name, verdict, cues)` only, so **prose edits to `scenarios.md` do not reach the
  artifact and no gate notices**. Measured: a citation fix in `scenarios.md` silently failed to
  render until `capart import scenarios` was re-run. Run `import` after editing scenario prose,
  not only after editing a row.
- **The render loop is closed, and the artifact has been looked at (2026-08-13).** `wowkb.serve`
  serves the artifacts directory, watches `specs/`, reruns `capart build havoc` on save and pushes
  an SSE reload — so *edit the shelf → look* is one gesture, with no publish in it. `capart build`
  was stripped to two hard failures (the tint guard; the closed verdict/roster vocabulary) so
  nothing can block a rebuild you want to look at; the byte budget, flipbook geometry and the
  literal-hex scan became a warning or a `check` concern. All 15 icons and 2 sheets are extracted
  from real client art (86 KB of a 512 KB budget) and `havoc-stepper.html` is republished to the
  same URL. The stylized two-letter-abbreviation diagram is **gone**: the artifact is now a
  transcription target. ⚠ Still true that `Treatment.lua` has not been changed to match.
- **The lab's two entries were promoted; the style is now borders + red-only badges (2026-08-13).**
  Part 7's lab existed so an idea could be drawn without being adopted. Both entries were drawn,
  looked at, judged better than the declared style, and **moved** into Parts 1–6 per rule 4 — the
  lab is now empty, which is its correct resting state.
  - **V2 · lane border.** A solid, static, per-lane border plus a one-shot arrival snap
    (2× → 1× over 0.35 s) fired when something *arrives* — a cooldown finishes, a charge returns, a
    spender becomes affordable. It is the only motion left in the style. **V1** (the
    `visualalert_ants_flipbook` emphasis ring) and **V3** (the lane pulse) are retired; their
    measurements — the trough invariant, the unequal-rate argument, the WCAG phase offset, the
    tintability table — moved to `render-rationale.md` because they stay true.
  - **A fourth lane, CHARGES**, which **replaces** the role lane on the border rather than
    stacking with it. Sourced from a new `Charges` column in `havoc/catalog.md`; the authored role
    lane is unchanged, because the substitution is a render-time fact. ⚠ Finding: both Havoc
    FALLBACK abilities have charges, so **no Havoc row draws a FALLBACK border** — `capart build`
    says so on the page rather than letting the lane silently vanish.
  - **V5 · corner badges.** OS-notification-style discs off the top-right corner, 40 % of icon
    width, overhanging 2 px (clears the 6 px row gap), on a dark contrast plate, from Kenney's CC0
    Board Game Icons. **V6** (the 7 px corner dot) and the old center cue row are retired.
  - **The cue vocabulary is now negative by default, and this is the real change.** Three cues —
    `blocked`, `starved`, `overcap` — one shared red, each a **single state** that draws when a
    button is ruled *out* and draws nothing otherwise. The reading model it serves: **scan the row
    left to right and press the first button not ruled out.** So `press`, `press-promoted` and
    `below` now render **identically** — the press is not a thing cap draws.
  - **One positive cue, added 2026-08-14: `capped`** (gold, glowing, badge slot 3, Kenney
    `cards_stack_high`), on Immolation Aura at max charges — ST-8 is its only subject. It exists
    because *impending loss* is urgent independently of **rank**, and rank is the only thing a
    left-to-right scan expresses; there is no negative phrasing of "you are wasting a charge right
    now". It does **not** direct the press — ST-8 is already led correctly by elimination. Scope is
    fenced by three `capart check` gates: the elimination gate counts
    **negative** cues only, a second positive cue fails `check`, and a cue no scenario wears
    fails `check`. ⚠ **"About to cap" is not attempted** — R6/OBS-066 measured `isActive` true
    at both 1/2 and 0/2, so a recharge threshold cannot tell "about to cap" from "about to regain
    your first charge", and would fire hardest while starved. That needs the napkin estimator,
    whose named worst case is Immolation Aura itself (R7).
  - **The other positive cues stay parked, not refuted.** The `banked` light (cue B positive), the
    green dependency dot, the weave chevron and the promotion (cue D) have no treatment today. A
    threshold remains expressible in **either** polarity — that finding is unchanged and
    `spec.md` §3.6 still carries it; what is deferred is *drawing* the positive half, because a
    positive cue is an **override** of left-to-right ordering and that is a harder problem.
  - **The escape hatch is mechanical.** `capart check` now asserts, for all 13 scenarios, that the
    leftmost entry that is neither swiped nor veiled nor wearing a **negative** badge is the entry
    the doc calls the press (`weave` skipped). All 13 pass. If one ever fails, that is the designed
    trigger for
    revisiting the positives — not someone quietly adding one.
  - **The tint guard survived its subject.** It guarded the flipbook rings; they are gone, so it
    was generalised (`assert_tintable`) onto the badge sprites, and `check` additionally fails if
    *nothing* declares `tint: "lane"` — a guard whose subject set empties keeps passing while
    guaranteeing nothing. Both failure paths were exercised deliberately.
- **The shelf is in Lua, and there is a gallery to look at it in (2026-08-14).** `capart export`
  generates `CombatAssistPlus/Style.lua` from Part 6 (data only) and vendors the badge art into
  `Media/badges/` as 32-bit TGA; `capart check` fails on a committed `Style.lua` that disagrees
  with the shelf, exactly as it already did for the HTML. `Paint.lua` holds one builder per
  primitive — border, arrival snap, veil, badge, glow — and **both** the live overlay and the new
  `/cap style` gallery draw through it, so the two cannot diverge. Frame stepping is one shared
  `C_Timer.NewTicker` computing the index off the clock, which is `stepper.js`'s walk exactly; the
  mechanism is now stated in the shelf. `Treatment.lua` is the tier→lane seam and holds no numbers.
  - **What `/cap style` can settle:** Q2 (the arrival snap without the ring), Q4 (badges at 56 px;
    does the sweep read as *waiting* or as a countdown), Q5 (one shared red across three badges),
    plus whether the gold `capped` is distinguishable at badge size and whether its glow rate is
    right. **What it cannot:** Q1 needs a real row at rest over time, and Q3 (does the CHARGES
    border carry meaning) and Q6 (does elimination lead the eye) both need the real Havoc row.
    Q7 stays unexercised — nothing declares `tint: "desaturate+lane"`.
  - ⚠ **The two Warlock context dots stopped drawing (2026-08-14).** `dreadstalkers` and
    `grimoire` were ad-hoc markers with their own hues; the shelf's cue vocabulary is a closed set
    of four, and inventing keys for them would break the "one shared red, shape carries identity"
    argument the set exists to protect. They are still evaluated and still reported in the `draw`
    capture's `M{}`; nothing is drawn for them. Re-authoring them as cues is `authoring.md`
    stages 1–5 work, and neither spec has ever flown.
  - **The arrival snap has its live trigger (2026-08-14).** It fires on a change of the drawn
    lane and on nothing else; the three suppressions are in `render-shelf.md` V2 and the rule
    itself is a pure function, so it is desk-tested while the frame work around it is not.
  - **Closed by deletion (2026-08-14): `verdicts.starved.desaturate` is gone from the shelf.** It
    had no live path — in the gallery cap owns the texture so desaturating is free, but on a live
    row the icon is Blizzard's. The right reading is not "find cap a legal way to desaturate": the
    CDM **already** desaturates and re-tints on usability (`cooldown-manager.md:700, :755`), so the
    token was cap proposing to restate a signal the client draws for free. It existed only because
    the HTML artifact has no Blizzard underneath it and had to draw its own de-emphasis, which then
    got filed as a cap treatment. cap's drawn primitives are the **lane border** and the **corner
    badges**; the icon face is not one of them. Revisit only if a flight shows the client's own
    dimming is too weak to read — and then as a new shelf entry, not as this one restored.
- Demonology remains the small pilot: Tyrant and Demonbolt are its only enhanced entries;
  Dreadstalkers and Grimoire are readable Tyrant dependencies.
- The corrective pass restored the three discrete tiers (then named ASAP / SOON / FALLBACK)
  without restoring continuous grades, pulse policy, exhaustive coverage or automatic sequences.
- **Tier vocabulary migrated (2026-08-12):** the spec now names the tiers **COOLDOWN / ROTATION /
  FALLBACK** as role lanes, and relaxes the single-hint rule so tier + cues may converge on the
  best press without a compute-the-answer channel (`spec.md` §1c / §3.1 / §4). **The source
  followed on 2026-08-14:** a catalog's tier names now *are* the shelf's lane names, with no
  mapping table between them — `Treatment.LANE` was deleted rather than turned into an identity
  map. Flight items below that still say SOON/FALLBACK describe a build older than that.
- Phase 9's source pass adds the minimal Destruction / Diabolist proof: Conflagrate tiers from
  readable shards and a seeded charge estimate, plus an independent sealed Backdraft count
  through Blizzard's 12.1 AuraContainer path. It has not flown as a CAP build.
- The engine supports only the readable predicates its catalogs use (`ready` · `proc` ·
  `identity` · `capped` · `affordable` · `resource`), propagates unknown safely, composes a row as
  lane + veil + badges, leaves Blizzard's proc glow intact, and owns one independent Tyrant bar.
- Engine guarantees and provisional Demonology examples are separate test groups. The old
  tier/channel policy suite and its visual-taste assertions are gone.
- The combined Demonology/Destruction checkpoint has not been judged in game. No
  release or deployment is implied.
- **The Havoc row flew on 2026-08-15** (Uncomplete / Kil'jaeden, cap v0.4.0, Fel-Scarred, on
  EllesmereUI). Five findings, in `notes.md`; the author decisions are `discussion.md` D22–D26 and
  the rest are work items above. The headline: the reading model's ordering assumption is
  **unconfirmed**, because `OrderCheck` reads Blizzard's `layoutIndex` while a CDM skin owns the
  drawn order. Shelf Q2/Q4/Q5 read positively in play; Q1, Q3 and Q6 are not yet answered.
- **The Havoc row is built (2026-08-14).** `Catalogs/Havoc.lua` carries twelve
  entries in authored priority order for **Fel-Scarred** (hero 34; Aldrachi Reaver is a separate
  future catalog and correctly gets nothing). What draws: the twelve lane borders, three of them
  purple `CHARGES`; Immolation Aura's two charge states (gold `capped` at max, red `blocked`
  below); `starved` on the two Fury spenders; the readable holds on Metamorphosis and The Hunt;
  the arrival snap; and two **graded** curves the client evaluates — the generators' overcap
  readout and Essence Break's hold while Eye Beam is within four seconds. Nothing has been
  released; **one flight covers the whole row** (`flight-reading.md` → *The Havoc row*).
  - **The composition seam held.** A row is lane + veil + badges, the veil **derived** from cue
    polarity, and adding the C1 holds and the C2 curve edited neither `Treatment.lua` nor
    `Overlay.lua`'s cue vocabulary — the renderer test in `authoring.md` stage 6, passed twice.
  - ⚠ **The structural risk is measured but unanswered.** cap does not own the row: the order is
    Blizzard's `layoutIndex`, filtered by the player's Cooldown Manager settings, and if it
    disagrees with the authored priority then elimination points at the wrong button *everywhere
    at once*. `Catalog.OrderCheck` reports it to the `bind` capture and to chat. One `/reload` on
    a Havoc character answers it; that has not been done. The fork it opens — a cap-owned row,
    which costs a `spec.md` §4 amendment — is not to be decided before the finding is in.
- The Havoc **design** docs (which the above transcribes) —
  `specs/havoc/catalog.md` (normative), `specs/havoc/fact-classification.md`,
  `specs/havoc/scenarios.md` (the single-row CDM elimination walk — one priority-ordered
  Cooldown-Manager row per state, walked left-to-right, naming why each off-cooldown button is
  skipped until the press; demon-form overrides rendered via R7; **revised 2026-08-13**, see
  Phase 10.1), the `spec.md` §3.7 product section, and five cues (A affordability / B sealed
  overcap / C readable + sealed hold / **D demon-form promotion** / E charges capped). See
  *Phase 10* below. Of those, **cue D is authored and not drawn** — a promotion is a positive cue
  and `press-promoted` renders identically to `press` — and so is cue B's positive "banked" half.
  The permission for both is unchanged; what is missing is pixels, not authority.

## Now

### CDM frame positioning — in-game verification (front of queue)

The D22 resolution (`discussion.md`) rests on one unproven claim: that cap can control CDM frame
position out of combat, without breaking the CDM, and have it persist through combat. Verify
before building anything on it. This is downstream of `spec.md` §3.6's setup-path principle —
positioning is setup-path work, so the test is "does it hold," not "is it combat-safe."

- [ ] **Out-of-combat re-anchoring holds.** Re-anchor the Essential viewer's item frames into a
      cap-chosen order (`ClearAllPoints` + `SetPoint` onto a cap-owned container, out of combat).
      Confirm the row draws in that order **and** the CDM keeps rendering each frame normally
      (swipe, charges, glow) — i.e. cap moved the frames without breaking Blizzard's per-frame paint.
- [ ] **Persistence through combat.** With the row set to always-show (no `HideWhenInactive`
      reflow), enter combat and confirm the positions hold — frames do not snap back to Blizzard's
      grid when abilities go on/off cooldown or when the viewer's `Layout` runs.
- [ ] **The re-apply edges.** Note which out-of-combat events rebuild the frame set (spec / talent /
      hero swap, `PLAYER_ENTERING_WORLD`, `CooldownViewerSettings.OnDataChanged`) and confirm
      re-anchoring after each restores the order.
- [ ] **The missing-spell half.** Confirm a `HideByDefault` row has no pooled frame, and that a
      surgical out-of-combat un-hide makes the CDM pool one cap can then reposition.
- [ ] Record the player/behaviour result. If positioning cannot be made to persist, **D22 reopens**.
      Client facts (protection status, reflow triggers, un-hide route) drain to
      `knowledge/addon-dev/`, not here.

### Re-fly Havoc to settle D23 with the `W{}` reason trace

v0.5.0 added `W{}` to the `tier` stream — per-marker decision plus the term values behind it
(`flight-reading.md`, `Signal.Explain`). The first Havoc flight could see that `hunt_awaits_meta`
fired, not *why*; this closes that gap. Fly before touching D23's gate options.

- [ ] Play Havoc, casting Metamorphosis roughly on cooldown as normal, then `/reload`.
- [ ] `wowkb.capture cap tier`, grep `the_hunt:hunt_awaits_meta` in `W{}`. Is Meta's readiness
      `off(ready:metamorphosis=F)` while you press it (rule working, so it's a tuning question), or
      stuck `on(...=T)` across the fight (a **latch bug**, likely the demon-form override-id flip —
      pattern-shelf R7)? Record which in `discussion.md` D23.
- [ ] If it is the latch bug, open a fix item and take D23 off the decision track until it's fixed.

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
pattern shelf: Fury is a *secret* primary, so the design is built on five cues (A/B/C/D/E) over
role-lane tiers instead of a resource gate. The design is complete and transcribed; what is left
is the flight.

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

#### 10.2 New readable providers / renderer work

Each is a *small named mechanism* under `authoring.md` stage 6's renderer test, confirmed against
`knowledge/addon-dev/` first, with one characterization example. **The list originally named four
providers and omitted a fifth the design needs — `affordable`, cue A's whole carrier — which is
added below.**

- [x] **"Affordable" readable provider** — `C_Spell.IsSpellUsable`'s **second** return
      (`insufficientPower`), never the first, which is false for anything merely on cooldown.
      Cue A rests entirely on it: a spender with no real cooldown never raises an alert edge, so
      its lane border is lit whatever the Fury and the border cannot carry affordability at all.
      First consumers: Chaos Strike, Blade Dance.
- [x] **"Capped" readable provider** — charges readable-at-full (R6): plain read iff at max *is*
      the capped signal; override-aware max + re-seed on transform (R7). First consumer:
      Immolation Aura / Consuming Fire. ⚠ **Re-grounded on `GetSpellCharges().isActive`**, which
      is `NeverSecret` and therefore answers in *both* directions — so below-max is a second
      readable state (the red `blocked` badge), not an unknown.
- [x] **Sealed Fury threshold cue (lever B), two polarities** — one S1-graded color-curve
      mechanism used both ways: **negative** per-generator overcap curve keyed to
      `(maxFury − generation)/maxFury` (Felblade +15, Demon's Bite ~20–30, authored **generation
      static table**; no generation API — R4), and **positive** "banked" curve at `35 / maxFury`
      on Essence Break. A threshold is a client-side paint, not a Lua branch, so both polarities
      are expressible; cap never reads which side the value fell on. First consumers: Felblade,
      Demon's Bite (negative); Essence Break (positive). ⚠ **Build the negative half only for
      now** — the shelf's single positive cue is spent on charges-capped, so the positive "banked"
      curve still has no treatment to drive and would ship as a mechanism with nothing on the other end. The
      mechanism is symmetric and the second consumer is a curve away when the shelf un-parks it.
      Built as the negative half only, as instructed. ⚠ `UnitPowerPercent`'s scale is unmeasured
      and unreadable back, so the curve encodes **both** readings (0..1 and 0..100); collapse it
      to two points once a flight settles which one fired.
- [x] **Sealed hold marker (cue C2)** — range step-curve → texture alpha on a sealed duration
      object (S4). ⚠ **One marker now serves both hold lanes**: C1 (readable) and C2 (sealed) both
      render as the shelf's `blocked` badge, since the difference between them is provenance, not
      appearance. Build one marker with two drivers. First check whether the current desktop
      renderer already has a `hold` marker
      slot; if so it reuses it and edits nothing in Treatment/Overlay (the 9.4 definition-of-done).
      It did, and it does: C1 and C2 both draw the `blocked` badge and neither edited a renderer.
      The two graded curves (B and C2) share one plan/arm/evaluate seam and differ only in their
      source — a power percentage on one side, a cooldown duration object on the other.
- [ ] **Demon-form promotion (cue D)** — plain emphasis raised on the empowered spenders while
      the readable demon-form window is active (R7). No new renderer; it is readable-driven
      emphasis. (Essence Break / Demonsurge promotion gated on open fact 10.3.) ⚠ **Also parked at
      the shelf level:** a promotion is a positive cue, and `press-promoted` currently renders
      identically to `press`. The permission is unchanged (`spec.md` §3.7 cue D) and the verdict
      name is kept because `scenarios.md` needs it to state ST-4's argument — what is missing is
      pixels, not authority.

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

#### 10.4 Transcription + flight (releasing ask-first)

- [x] Transcribe `catalog.md` into `Catalogs/Havoc.lua` against the current vocabulary; add to
      `.toc`, register, resolve override ids via `overrideSpellID` at bind (never hardcode).
      Twelve entries in authored priority order, base spell ids only, no `power` field.
      `Catalog.OrderCheck` ships with it: a diagnostic that compares the authored priority against
      the client's own row order, because the whole reading model assumes they agree.
- [x] Give the arrival snap a live trigger, and decide what counts as an arrival on a CDM row.
      It is a change of the **drawn lane** — absent → present or one lane → another — with three
      suppressions (a repaint, the first draw after a rebuild or resume, and a second snap inside
      the snap's own duration). `render-shelf.md` V2 states it.
- [x] Extend the `busted` suite for the new providers: capped/charge seeding + reseed-on-flip,
      lever-B curve guards, marker union (readable + sealed hold lanes). ⚠ `readCapped` and
      `readAffordable` call `C_Spell.*` and **cannot** be desk-tested; the blind-world path covers
      what is testable (a refused read yields no cue and no veil) and the rest is a flight
      question, not a busted one.
- [ ] Dry-run `wowkb.addon release cap`; releasing stays ask-first.
- [ ] **The flight — one, for the whole row.** Fly the affordability dim, the two Immolation
      states, the readable holds, the arrival snap and both graded curves *together*; per-slice
      flights would burn an evening testing instead of playing. The card is in
      `flight-reading.md` → *The Havoc row*: one player-experience question stated before playing,
      the player's judgment recorded in their own terms, captures read only afterwards to explain
      which route armed. It settles shelf Q1, Q3 and Q6 and all three open facts — including the
      structural one, whether the CDM's row order matches the authored priority.

### Out of the first Havoc flight (2026-08-15)

It flew: Uncomplete / Kil'jaeden, cap v0.4.0, Fel-Scarred, on **EllesmereUI**. The five findings
are in `notes.md`; the ones needing an author decision are `discussion.md` D22–D26. These are the
ones that do not.

- [ ] **Delete the `demons_bite` entry** (`Catalogs/Havoc.lua:24`, spell 344859) and the
      "two generators" framing around it. Midnight made **Demon Blades** baseline and removed the
      Demon's Bite choice node: it is absent from the 12.1 priority, appears zero times in the
      simc APL (`builds.md:153-157`, Tier 1), and the flight's `bind` capture shows it never
      bound. Felblade is the only generator press. Also drop it from `havoc/catalog.md` and the
      `scenarios.md` rows.
- [ ] **Split the Immolation Aura charge question in game** — the test behind D24's second half.
      The player's **active** loadout has no *A Fire Inside*, so `maxCharges` is 1 and
      `readCapped` (`Sense.lua:104-105`) should return unknown, drawing neither cue — yet the
      capture carries `immolation_capped` ×40 and `immolation_recharging` ×58. Either a different
      loadout was flown, or the guard is not holding. `/reload` on the single-target loadout and
      read the `draw` capture: no `CHARGES` and no charge cue = the guard works and the flight was
      on the AoE build; anything else is a real bug.
- [ ] **Root-cause the arrival snap's "hashtag" read.** The player reports the border resolving
      from something like a `#` into a rectangle rather than snapping in as a box. Not diagnosed:
      `Paint.lua:61-81` builds four separate strips and `Paint.Arrival` scales the group from
      `from_scale` about `CENTER`, and nothing in that geometry obviously explains it. It shows in
      the artifact as well as in client, so it is debuggable without a flight.
- [ ] **Check for a veil with no badge.** One icon in the flight screenshot reads veiled with no
      visible cue, which `render-shelf.md` Part 2.5 says cannot occur — a row is veiled *iff* it
      wears a negative cue, and `capart check` now gates the token table on that derivation. Could
      equally be screenshot resolution, or the curve-driven veil on a graded cue where the client
      owns the badge's visibility. Confirm before treating it as a defect.
- [ ] **Close the sidecar prose gap in `capart check`.** `check` compares doc against sidecar on
      `(name, verdict, cues)`, so scenario **prose** can drift ahead of the rendered artifact with
      no signal — the Status bullet above records the measured case. Either compare the rendered
      extras too, or have `build` read prose from the doc rather than the sidecar.
- [ ] **Teach `Catalog.OrderCheck` what it is actually checking** — whatever D22 decides. Today it
      compares the catalog against Blizzard's `layoutIndex` and reports as though that were the
      drawn order; under a re-skin it is neither right nor wrong but blind, which is the worse
      failure. At minimum its capture note should say which order it read.

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
