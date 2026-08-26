# Combat Assist Plus — backlog

**What this file is for:** the current implementation status and the ordered work list.
`spec.md` owns intended behavior; `notes.md` owns completed history; `discussion.md` owns only
questions that still require an author decision.

The live addon version comes from `wowkb.addon list`, never from prose here.

**An item here has to keep earning its place.** Completed phases, migration checkpoints and
corrective passes are history and belong in `notes.md`; the measurement behind a status line
belongs in `notes.md` or `knowledge/addon-dev/`. If an item's premise stopped being true, rewrite
it or delete it — never leave it standing with a note underneath.

## Status

This is the project's only implementation-status source. It says what is built and what has flown,
and nothing about how it was measured.

### The engine

- The engine supports the readable predicates its catalogs use — `ready` · `proc` · `identity` ·
  `capped` · `affordable` · `resource` · `talent` · `aoe` — propagates unknown safely, composes a
  row as **scan membership + badges**, dims Blizzard's proc glow to
  `tokens.surfaces.proc_glow_alpha` so cap's own emphasis is not competing with it
  (`render-shelf.md` Part 3), and owns one independent
  Tyrant bar. Sealed facts reach client-owned display sinks only, never a Lua branch.
- **The Tyrant bar is DORMANT and that is the decision** (2026-08-25). `Bars.lua` is in the
  `.toc` and fully wired — `Overlay` calls `Bars.Report`, which calls `Bars.Plan(Sense.Roster())`
  — but `Sense.Roster()` reads `catalog.bar` and no catalog declares one, so it plans nothing on
  every pass. It is kept rather than deleted because `catalog.json`'s schema and `capart export
  catalog` already emit `bar`, so one authored key makes it execute. `spec.md` §3.3 is the
  permission it is waiting on, not a gap.
- **The role tier is REMOVED** (paint 2026-08-19, model 2026-08-25). Membership is a boolean:
  a row is in the scan when its `scan_when` alternatives (default: ready-self) read ON, withheld
  when required reads are unknown. `Catalog.TIERS` is deleted, the catalogs' `| Lane |` columns
  became `| Scan |`, and the lane names **COOLDOWN / ROTATION / FALLBACK** survive only as prose
  grouping in the catalogs. `Treatment.For` reads the one bit, which `presentation_spec` asserts.
  **Authored, not flown:** the uniform blind rule (no ON alternative + any BLIND alternative ⇒
  withheld) and the two accepted behavior changes — Demonology Shadow Bolt and Destruction
  Incinerate/Conflagrate now stay lit under blindness where their deleted two-band flips
  darkened them. Both join the flight acceptance set.
- Engine guarantees and provisional per-spec examples are separate test groups.

### The style

- **The style is the scan edge + corner badges + the cooldown hatch, over Blizzard's own swipe and
  desaturation.** The veil is deleted; the addon carries zero occurrences of `veil` (2026-08-16).
  `render-shelf.md` declares what each token MEANS, `specs/render-tokens.json` holds the numbers,
  `capart export` generates `Style.lua` and the badge / hatch / promotion art from them, and
  `capart check` fails on a committed asset that disagrees.
  `Paint.lua` holds one builder per primitive and the live overlay draws through it. ⚠ **The
  gallery does not, for the sealed bars** — V18's charge bar, its dial and V20's proc bar are
  built by hand in `StylePanel.buildSealed` from four near-identical `StatusBar` constructors,
  because a swatch is driven to a stated value and a live sink is driven by the client. The
  duplication is real and is a known cleanup, not a claim that it does not exist.
- **V13's scan edge is one binary treatment** (2026-08-19): a `tokens.ready.line_px` additive line
  on the icon rect, drawn on a row cap has an opinion about and absent on one it does not. No hue
  ladder, no motion, no art — four `SetColorTexture` strips with `SetBlendMode("ADD")`, and the
  only in-combat write is `Show`/`Hide`. It replaced V2's four-hue ring flipbook and its arrival
  snap, and as of 2026-08-25 **nothing of the arrival is left**: `tokens.ring` / `.motion` /
  `.arrival`, `Media/ring.tga`, `capart export ring` and `Paint.Arrival` went with Part 7's
  `arrival-*` entries, which had been deleted six days earlier. **Not flown** — Part 5 question 2.
- **V11's cooldown hatch is shipped** (2026-08-16), on every row the CDM says is down.
  `verdicts.cd` is the only verdict carrying `hatch: true`, and **only `false` draws** — an
  `UNKNOWN` or absent readiness draws bare, so absence of a hatch never asserts a button is up.
  ⚠ A **charged** ability and a row whose first readiness edge has not landed will not wear it, so
  the hatch is not a complete census of what is down. **Not flown** — Part 5 question 9.
- **The cue vocabulary is negative by default** (positives: `capped` and `priority`, gold). The
  negatives — `blocked`, `starved`, `overcap`, `st_only`/`aoe_only`, and since 2026-08-24 the two
  cards `building` (a ramp holds this while resource climbs) and `noproc` (the proc that makes
  this worth pressing is not up) — share one red and are told apart by shape. `open`, `press`
  and `weave` render identically: the press is not a thing cap draws.
  ⚠ `building` is deliberately UNBUDGETED on the density rule's own starved/overcap grounds
  (one fact, a block of subjects) — Demonology's ramp wears up to six cards before the press,
  the pilot's chosen reading over a promotion, playtest-gated (demonology/catalog.md changelog
  2026-08-24).
- The reading model is mechanised rather than minuted. `capart check`'s `reading_gate` is an
  ordered chain: a scenario wearing a positive cue is judged by pass 1, every other scenario by
  pass 2 — the leftmost entry that is neither swiped nor wearing a negative badge must be the
  press. A scenario that stops leading the eye to its press fails **by name**.
- **A marker may carry no `cue` at all**, and `Catalog.Check` keeps `cue` optional for exactly
  that: such a marker is still evaluated and still reported in the `draw` capture's `M{}`, but
  draws nothing. Every marker in every shipped catalog either carries a cue from the closed set
  or exists to arm a sealed *display* — the cue-less-and-display-less shape survives only in the
  engine fixtures, which is where the shape is tested.
- **Motion is AnimationGroups only — the addon holds no ticker** (2026-08-24). Every sheet walk
  is a client FlipBook animation (`Paint.FlipBook`): the badge strips (`capart export badges`
  bakes `strip_<cue>` for every multi-frame cue), the promotion ring, and every strip to come. The
  shared `C_Timer` stepper and `Paint.FrameIndex` are deleted; `style_spec` asserts Paint holds
  no ticker. Motivated by the measured seal on handed-over regions (security-taint §3.5.3).
  **Not flown** — FlipBook semantics are a source read (`--@unverified` on `Paint.FlipBook`), so
  the capped badge and the promotion ring are in the next flight's acceptance set.
- **V18 is the segmented bar, red at full** (2026-08-24, replacing the radial). The sealed
  count draws as a left-to-right bar on the row's BOTTOM edge over a segment grid (cap's own
  track art), and at `max` the **whole bar flips to the negative red** — a second slot's count
  band (`Channel.BarFlipRules` → the pre-tinted `bar_full` crop) at threshold = max,
  client-decided. First consumer: Demonic Core (full stacks = procs about to be wasted). The
  move off the corner also ends the DEM-8 geometry conflict with V19's badge (Part 5 #10 is now
  a readability question). Radial render mode retired from the style. **Not flown.**
- **V19 is a two-state DoT pair; V16/V17 changed shape** (2026-08-24). Aura up but OUTSIDE its
  refresh window: a gold do-not-refresh hatch, drawn by `SetDurationText` band tables on
  remaining seconds off an optional catalog `outside_s` (the threshold is the catalog's; the
  badge's edge stays the client's — the shelf carries the seam caveat). Inside the window: the
  badge at **cue-badge brightness exactly** — at its centre the **dial** (2026-08-24, replacing
  the `fire` glyph): a radial `StatusBar` the CLIENT drains off the DoT's own remaining
  lifetime — `SetDurationBar` → `SetTimerDuration(auraDuration, interpolation, direction)`,
  `RemainingTime`, cap reading nothing (KB §3.5.2); `SetMinMaxValues(0, 1)` FIRST per §4.8.1
  finding 3, Radial pcall'd with linear fallback. It is the retired `timer_CW_75` wedge's claim
  made true — that was static art; this is a value the client drains. Around it the FULL
  positive-cue treatment — V14's promotion ring plus the halo behind the plate; no region
  pulse, no numeral. The halo alone read as a faint gold mist beside a real promotion,
  measured in the preview. ⚠ The `AddPandemicRegion` + `SetDurationBar` **one-button pair is
  unflown** (each half measured alone — Part 5 #11) and joins the flight acceptance set. Count bands: the hatch is
  legal on **negative** bands only (`Channel.CountRules` refuses a positive hatch), and the
  numeral rides ON the badge plate as its own `plate` element/slot (`Channel.CountElements` is
  now hatch → plate → mark → count). No catalog declares `outside_s` yet. **Not flown.**
- **V20 is the proc bar; the two-sided band and the corner cession rule shipped beside it**
  (2026-08-24/25, the stepper-feedback rounds). V20 = the proc's remaining lifetime as a thin
  client-drained bar directly above V18's charge bar — a `sealed-proc-bar` slot filtered to
  the proc aura, `SetDurationBar`/RemainingTime, linear. Born as a corner dial and re-formed
  onto the edge after ONE stepper round: gold in the badge column (hue = polarity) read as a
  verdict arguing with the red holds. Consumers: Demonic Core on Demonbolt (every Core-up
  scenario — the client owns visibility) and the armed Art under Infernal Bolt (aura id
  Tier-3-sourced, dies silent if wrong — flight question). The imp band recolors instead of
  clearing: red count + hatch below six, GOLD count at six (DEM-12) — a loaded Implosion no
  longer looks unremarkable. `Channel.BandPoints(beyond, within)` closes demonology
  catalog.md's Defeats item 1 — Dreadstalkers' two-sided "waiting on Tyrant's cooldown" hold
  (DEM-15) — with `Catalog.Check` demanding `beyond < within`. Part 2.5 gained the CESSION
  RULE: corner sealed displays (V19's badge, V16's corner elements) claim stack slots 0..n−1
  by declaration (static — whether one is showing is sealed) and cue badges start below them;
  DEM-8's Demonbolt — two stacked bars plus the window badge — is the densest row in any
  catalog. Demonology also grew the ramp holds (cue I, `building`, authored PAST the
  unconditional APL rungs — playtest-gated), re-badged Demonbolt's core hold to `noproc`, and
  its scenarios now wear the Implosion imp band everywhere imps are out (the "no markup on
  Implosion" gap), with DEM-13's Tyrant-ready/Tyrant-far contradiction fixed in passing.
  **All of it authored, not flown** — the dial pair, the three-point band, and the cession
  geometry all join the flight acceptance set.
- **Part 7's lab is populated and decides nothing.** The 2026-08-20 eight-entry intake flew on
  2026-08-21 and left on 2026-08-22 — four promoted as **V16–V19**, one (`composites`) deleted as
  the argument that those four compose — leaving `duration_band` (band tables on a DoT's clock;
  its seconds-form inversion has since been promoted as V19's outside-window hatch).
  `segment_bar` lived for one review round on 2026-08-24 and left the same day as V18's
  re-form. Part 7's ledger says where everything went; do not restate a count here —
  `capart export lab` prints the current set.

### The client seam

- **Readiness is a read, not a latch** (2026-08-16). `Sense.readRowCooldown` asks the item's own
  Cooldown widget whether it is shown and `wasSetFromCooldown` whether the dial means a cooldown;
  `Track:World` prefers that over the alert latch, and `Sense` additionally hooks `OnCooldownDone`
  as the ready edge. ⚠ The edge latch still runs underneath, because the Cooldown widget's
  `IsShown()` is not yet measured plain in combat — `@pending-test:
  cdm-cooldown-widget-shown-in-combat`.
- **Authored ordering ships, on by default** (2026-08-16). `Anchor.lua` re-anchors the Essential
  viewer's item frames into the catalog's authored order a second after `PLAYER_ENTERING_WORLD`,
  re-applies out of combat on layout stomps and on the spec / talent / settings edges, samples at
  2 Hz, and **asks before it stops**. `/cap anchor [on|off|retry|rows]`; the setting persists at
  `ns.db.anchor`.
  - **Flown 2026-08-16** (cap v0.7.0, Havoc / Fel-Scarred, nine Essential rows): the drawn order
    read back byte-identical to the authored order right after the apply and again at both edges of
    a 138 s fight, `disp:0 cont:0 stomp:0`. ⚠ `RefreshLayout` never fired, so the in-combat
    pool-release path that would break it is **untested** — persistence is supported, not proven.
- **Ordering recovers instead of latching** (2026-08-17). Three defects made a scrambled row
  permanent for a session: the first displacement after arming had no prior cause to be
  attributed to and so read as another addon by construction; the contention response was a
  session-long silent latch that only `off`+`on` cleared; and `refresh` re-applied rather than
  rebuilt, so a `RefreshLayout` that re-pooled the item frames left cap placing frames whose
  identity it no longer knew. Now: `arm` seeds the cause; `Anchor.Judge` is a pure classifier
  requiring a run of strikes inside a window; exhausting it opens a **yes/no dialog** ("Turn it
  off" / "Keep trying") and cap never stops on its own; a destructive stomp or a live
  `GetCooldownID()` mismatch triggers a **rebuild** from a fresh bind; `X{STALE:<n>}` reports the
  mismatch the old `X{ok}` could not see; and `/cap anchor retry` is the manual recovery.
  - **Not flown.** The classifier has unit coverage; the dialog, the rebuild and the stale
    detector have only been reasoned about. Fly before believing the counts.
  - ⚠ **What moved the frames in the stuck sessions is still unattributed.** The capture shows
    displacement with neither `Layout` nor `RefreshLayout` firing, which is either a competitor
    or a layout path `Anchor.lua` does not hook. The new behaviour is correct either way, but it
    does not answer this.
  - ⚠ **Not built:** the always-show / un-hide half. `SetCooldownToCategory` writes the player's
    saved CDM layout, which the ordering design deliberately avoided, and it needs an author call.
  - `Anchor.lua`'s `InCombatLockdown()` guard on `apply()` is **caution, not a restriction**:
    `IsProtected()` returned `false, false` on 9 of 9 Havoc rows, in and out of combat
    (`knowledge/addon-dev/cooldown-manager.md` §4.1).

### The specs

- **Havoc / Fel-Scarred is the live spec.** `Catalogs/Havoc.lua` carries twelve entries in authored
  priority order; Aldrachi Reaver is a separate future catalog and correctly gets nothing. What
  draws: twelve scan edges, the holds on Metamorphosis / The Hunt / Essence Break / Vengeful
  Retreat, `starved` on the two Fury spenders, Immolation Aura's gold `capped` and its
  single-target skip badge, the cooldown hatch, and the generators' graded overcap readout.
  - **The composition seam held.** Adding the holds and the graded curves edited neither
    `Treatment.lua` nor `Overlay.lua`'s cue vocabulary — `authoring.md` stage 6's renderer test,
    passed repeatedly.
  - **Re-sourced from the Tier-1 simc APL on 2026-08-17**, which corrected several rules and
    reversed one. `specs/havoc/catalog.md` → `## Changelog` is the record, and its *Open facts*
    section owns every unmeasured Havoc fact. **The row has not flown since.**
  - The Havoc design lives in three files — `catalog.md` (the definition),
    `scenarios.md` (the walk), `fact-classification.md` (the safety case) — which is the
    **model every spec follows** (`authoring.md` §0, revised 2026-08-19).
- **The Havoc row flew once, 2026-08-15** (cap v0.4.0, Fel-Scarred, on EllesmereUI), against the
  pre-APL catalog. Its structural finding — the reading model assumes the CDM's row order matches
  the authored priority — is what `Anchor.lua` was built to answer.
- **Demonology / Diabolist is BUILT and has never flown** (2026-08-22). `Catalogs/Demonology.lua`
  is the roster its three documents describe — nine entries in the authored priority order,
  fifteen scenarios, and `demonology-stepper.html` generated from them. `authoring.md` stages 6
  and 7 have run; stage 8 has not.
  - It carries **three new sealed-display kinds**, promoted out of Part 7 as V16–V19:
    `sealed-count-bands` (Power Siphon and Implosion, the second in its complement direction),
    `sealed-count-bar` (Demonbolt's segmented Core bar) and `sealed-pandemic` (Doom, gated on the
    talent). `player-aura-stacks` and its `min = 2` guard are retired; Destruction's Backdraft was
    migrated mechanically and draws exactly what it did.
  - **A sealed fact can now ELIMINATE a row**, which is the substantive change: the reading model
    has three eliminating signals instead of two. `catalog.md`'s second defeat is closed and its
    two states are DEM-13 and DEM-14.
  - ⚠ **Nothing about the client was learned to make this possible.** The measurements were in
    hand on 2026-08-21; what was in the way was that a catalog may not cite a lab entry, so the
    fact was expressible and unusable at once. **Promotion is a pipeline step, and it was the
    whole cost.**
- **Destruction / Diabolist is authored and has never been built or flown** (2026-08-19). Three
  files — `catalog.md` / `scenarios.md` / `fact-classification.md` — twelve scenarios, and a
  generated `destruction-stepper.html` registered in `capart.SPECS_BUILT`. There is no
  `Catalogs/Destruction.lua` **of the current design**: the file in the addon is the *pilot*
  catalog and predates those documents, so what the addon draws on Destruction is the old
  two-entry proof and **not** what `specs/**` now says.
  ⚠ **That is the one place left in the project where a shipped catalog and its document
  disagree**, and it is deliberate — `authoring.md` stage 6 has not run for it. Do not read the
  `.lua` as the design. It wants the same count primitive for Backdraft that Demonology now uses,
  which is now a transcription rather than a promotion.
  - ⚠ **It has no `catalog.json`, and unlike Devourer's absence that is a finding rather than a
    not-yet** (2026-08-25). Two of the six authored specs lack one. **Devourer** has never been
    transcribed at all — it is still hand-written `catalog.md`, and its blocker is V12 (see its
    entry below). **Destruction** was attempted, and the scenario↔state gate refused it —
    **five scenarios, three cues**. `DES-1` draws Conflagrate
    wearing `capped`, `DES-2` and `DES-5` `blocked`, `DES-6` `overcap`, and the pilot declares
    none of those markers. Declaring the states would require declaring the markers, which is
    *authoring the catalog*, not transcribing it. So the gap between the pilot and its documents
    now has a **measurement** instead of a paragraph, and the measurement is the entry criterion:
    when stage 6 runs, it is `specs/destruction/catalog.json` that gets authored, and `capart
    check destruction` goes green the moment the design and the addon agree.
  - **One real defect was fixed on the way past** (2026-08-25): `backdraft` declared no
    `family`, and `Catalog.findRow` defaults a missing family to `"spells"`. Backdraft is a
    TrackedBuff row, so it could never resolve — the sealed count band naming it as its subject
    had no subject, and `Sense` would have seeded it with `readCooldown`. Every other aura
    subject in every other catalog already declared the key. Hand-edited, since this file stays
    hand-written.
  - **It replaced a pilot**, which was a single-mechanism proof rather than a roster
    (`spec.md` §3.5 records what carried and what was withdrawn).
  - **It has never flown as a cap build**, in either form.
- **Retribution / Templar is authored and has never flown.** Three files
  (`catalog.md` / `scenarios.md` / `fact-classification.md`, split 2026-08-19), 13 scenarios, and a
  generated `retribution-stepper.html` preview.
  ⚠ **It HAS been transcribed.** `Catalogs/Retribution.lua` exists (216 lines) and is registered
  in the `.toc`, so the addon **does** draw on the spec. This entry previously said the file did
  not exist and that the addon drew nothing; that was wrong, and the correction is recorded here
  rather than left as a note under a dead claim. What is still true is that **nothing about it has
  been judged in play** — `authoring.md` stage 8 has not run.
  - **A recorder rides the next flight** (2026-08-22). Its one unexpressible rung — hold a FREE
    Hammer of Light, press an ordinary one on sight — turns on a separation cap does not have
    (*Open facts* 3), and two candidate separators are on the table with **neither measured**.
    The first, that a free Hammer glows without transforming its row, was contradicted by direct
    player observation the same day. So `Sense.lua` now writes proc-glow edges and identity flips
    (with the row's own cooldown state) to the `edge` stream and **nothing reads them**:
    no predicate, no verdict, no pixel. `flight-reading.md` owns how to read the lines.
    ⚠ The 60-stack counter behind the free cast is **not** logged and cannot be — an aura's
    application count is sealed in combat. The player watches it on a Tracked Buff row.
  - ⚠ **`Sense.lua`'s `proc` reads the BASE spell id** while `capped` and `affordable` two lines
    below read the LIVE one, so `proc(wake_of_ashes)` polls a spell that never glows. It looks
    accidental rather than authored. **Deliberately not changed in the same pass** — it would move
    what draws on the live Havoc spec on an inference, and the recorder above is about to say
    whether it matters.
- **Protection / Lightsmith is authored, transcribed, and has never flown.** Three files
  (`catalog.md` / `scenarios.md` / `fact-classification.md`), 14 scenarios, nine entries over 28
  states, a `protection-stepper.html` preview, and `Catalogs/Protection.lua` migrated from
  `catalog.json` like the other three. `authoring.md` stage 8 has not run. **Its three honesty
  banners used to live only in `capart.py`'s `SPECS_BUILT` and on the preview page** — which is
  the wrong place for them, since this file is the project's only status block, so they are
  restated here:
  - **Nothing on that page has run in the client.** It exists to be reviewed and argued with, not
    to record a decision. The transcription existing is not the same as the design having been
    judged in play.
  - **The armament row's identity DIRECTION is marked, not measured**
    (`protection/fact-classification.md` §5.1). Sacred Weapon `432472` has no Cooldown-Manager row
    of its own anywhere in the game data, so it can only reach the CDM as an override on Holy
    Bulwark `432459` — that much is Tier 1. Which of base/transformed is which armament is not.
  - **Two rungs are undrawn because a Category-3 TrackedBar row's alert edges are unmeasured**
    (`protection/catalog.md` Defeats 1 and 2). It is the same unmeasured fact as Demonology's
    Dominion of Argus, and one measurement closes it for both.
- **Devourer is authored and has never been built or flown**, on the same terms: three files, and
  the first spec whose definition needed **V12's virtual row** (Collapsing Star has no CDM frame at
  all). No catalog Lua. **It does now have a preview** — registered in `SPECS_BUILT` on 2026-08-19,
  10 scenarios (B-1…B-5 build phase, M-1…M-5 window phase), and the first page any spec has drawn a
  virtual row on. Two things about it are deliberate and should not be read as settled work:
  **M-3's row was DERIVED, not authored** (the doc had it as a prose delta on M-2 with no row of its
  own), and the page carries **loud `⚠ UNSURE` annotations** wherever the authoring docs doubt
  themselves — position 1's desaturation assumption, misordering 2, cue D's sound slice, cue B's
  fitted break point, the owed Voidsurge. The page exists to be **argued with**, not to record a
  decision, and the gates prove only that each row is self-consistent. (One of those annotations
  is gone: position 1's *"the client desaturates a below-bank Void Metamorphosis"* premise was
  **false**, not merely unmeasured — desaturation is Blizzard's cooldown statement and nothing
  else — so that row is `ruled-sealed` off cap's own count band now, and the spec's open fact 7
  collapsed into open fact 3.)
- **Cue D (demon-form promotion) is authored and not drawn.** A promotion is a positive cue and
  `press-promoted` renders identically to `press`. The permission is unchanged; what is missing is
  pixels, not authority. **Cue B's positive "banked" half is not parked beside it — it is deleted**,
  and by the 2026-08-17 APL re-source rather than by any cue budget: the priority list puts no Fury
  term on Essence Break at all, so there is nothing for the half to say.

### Tooling

- **Every generation input is its own structured file, and the per-ability state table is the
  source of truth** (2026-08-25). `specs/render-tokens.json` (the style's numbers) and
  `specs/render-lab.json` (Part 7) came out of `render-shelf.md`, which dropped 2313 → 1677
  lines; `specs/<spec>/catalog.json` came out of `catalog.md` and **generates
  `Catalogs/<Spec>.lua`**, byte-gated; `specs/<spec>/scenarios.json` came out of `scenarios.md`,
  which keeps the walk prose keyed by the same ids. The prose keeps the *why* and cites the data
  by path; it has stopped *being* the data.
  - **Four specs are migrated** — Demonology, Havoc, Protection, Retribution. Each round-trip was
    proven DATA-IDENTICAL by loading the committed and the generated Lua through a
    `ns.Catalog.Register` stub and deep-comparing, never by reading a diff. **Two authored specs
    are not migrated**, for different reasons: Destruction was attempted and refused by the
    scenario↔state gate (measured above), while Devourer has not been attempted, because V12's
    virtual row is `declared` and `drawn_by` rejects a `declared` primitive — the gate would
    refuse precisely the two rows the design exists for.
  - **Six catalog gates**, applied to any spec that has a `catalog.json` and skipped by absence,
    so the remaining rollout needs no second list: Lua byte-compare, marker↔state,
    closed vocabulary, scenario↔state, co-occurrence, and validator parity (`Catalog.Check` run
    outside the client by `tests/check_catalog.lua`). **Every one has been seen to fail by name**
    on every migrated spec — a gate never watched failing is not known to work.
  - **Scenario polarity is chosen by a file existing**, not by a list: a spec with
    `scenarios.json` leads from it and its `previews/data/` sidecar is deleted; a spec without
    one still leads from the doc. `check` reports which.
  - ⚠ **`check` is not sufficient and never was.** It passed for the whole of the Demonology
    scenarios split over a stepper whose walk steps had stopped rendering, and it passed over a
    `page.html` lede naming two verdicts that do not exist. Both were found by opening the page.
    Serve it and look.
- `wowkb.capart` renders the preview and the addon's `Style.lua` from the docs, and `wowkb.serve`
  closes the *edit the shelf → look* loop. The scenario sidecar is on the build path, and since
  2026-08-19 `check` compares the **whole scenario** doc-vs-sidecar rather than a chosen tuple of
  fields, so a prose-only edit fails the gate and names the field. The old advice — *"remember to
  re-import after editing prose, not only after editing a row"* — is retired; it was a human
  standing in for a comparison the tool can do. ⚠ A field whitelist was wrong by construction
  here: `{client: …}` was outside it from the day it shipped, so the client-paint layer could be
  edited in the doc and never reach the page.

## Now

### Keybind hint on the CDM row — built, not flown

The key you have bound, drawn in each row's top-left corner, because Blizzard's Cooldown Manager
draws none: `grep HotKey` over `Blizzard_CooldownViewer` returns zero. The API chain is
`knowledge/addon-dev/cdm-rider-patterns.md` §11, Tier-1 against shipped 12.1 source.

✅ **The three decisions are settled (2026-08-19)** — chrome not a cue, macros blank in v1, always
on with no toggle. They live in `spec.md` §3.8 and `render-shelf.md` V15 now, and
`keybind-hint-plan.md` was deleted on landing, as it said it would be.

✅ **Built 2026-08-19.** `Binds.lua` (the two-stage lookup, cached, debounced, no combat fence),
`tokens.hotkey` + V15 in the shelf, `Paint.Hotkey`/`Paint.Label`, the draw in `Overlay.paint()`
with the widget added to `quiet()`, 21 pure specs in `binds_spec.lua`, and a `capart check` gate
(0e) asserting chrome names no cue, declares no polarity or rank, and does not anchor to the
corner the badge stack flows from.

⚠ **The slot arithmetic the plan file specified was not built, deliberately.** It hardcoded
`page = floor((slot-1)/12)+1` plus a page→binding table, which §11 explicitly rejects: the real
button frames already carry `frame.action`, and reading it handles paged, bonus and override
numbering with no ranges. The KB won.

- [ ] **The flight.** Six states, all six or the phase has not passed: spec swap · bar page flip ·
      shapeshift · combat entry · combat exit · CDM re-layout. Plus Part 5 question 9 — does the
      hint read as a label or as another signal, and does the blank read as "unbound" or "broken".
      ⚠ Havoc has not flown since it was re-sourced from the Tier-1 APL on 2026-08-17 and carries
      an unflown V11 hatch and V13 scan edge, so judge those together rather than the hint alone.
✅ **The font is settled and cap ships it** (2026-08-19). Ten lab candidates — five faces, then a
plate, then a title bar — judged on real rows in the preview. **Share Tech Mono won**, promoted to
`tokens.hotkey` and shipped as `Media/fonts/CapKeyMono.ttf`: monospaced, because a keybind is not
prose and `csF1` in a proportional face reads as one smudge; condensed, which buys back most of
what a fixed advance costs. ⚠ **Renamed on the way out** — the upstream family carries the Reserved
Font Name `'Share'`, a subset is a Modified Version, and OFL 1.1 clause 3 forbids one from using
it. `OFL.txt` and a `NOTICE.txt` ship beside it and `capart check` gate 0f byte-compares all three.
This is the first third-party asset the addon redistributes.

✅ **A preview-fidelity bug found by looking, which is what the preview is for** (2026-08-19). The
dark edge was eight stacked `text-shadow` copies; every copy is antialiased, the overlaps
accumulate alpha into a halo, and the diagonals sit at 2.83 px where the axials sit at 2 — so it
rendered as a smudge with lumpy corners and made every font candidate look worse than it is. The
client computes its outline from the glyph (from its SDF); the faithful analogue is a real stroke.

✅ **The lab is empty** (2026-08-19). Nothing left in it was still being evaluated. Part 7 keeps the
ledger of what left and where; `git log` keeps the entries.

✅ **The preview draws the client's own font** (2026-08-19). `capart` pulls `fonts/frizqt__.ttf`
out of CASC by FileDataID and embeds it as an `@font-face` data URI, the way it already embeds
spell icons — so advance width in the preview is the game's, which is what "does `C-S-F1` fit the
corner" actually asks. Part 3 permitted this all along: its rule bans extracted art in the addon's
`Media/`, not in the preview, and nothing on this path reaches `Style.lua`. The page grew ~50 KB
and `tokens.budget.max_base64_kb` went 512 → 600 to match, rather than leaving a standing warning
that would blunt the signal.

- [ ] **Readability was bought with the only two dials the client has** — `size` 12 → 14 and
      `outline` `OUTLINE` → `THICKOUTLINE`. `SetFont` offers nothing between them and nothing
      wider, so if 14/THICK still does not read over bright icon art, the next move is a dark
      backdrop texture behind the FontString (the badge plate is the precedent), not a bigger
      number. Judge it in the flight.

### Anchor — what the one flight did not exercise

The feature ships and holds; these are the things to notice in play, not a gate in front of it.

- [ ] **The re-apply edges.** Spec / talent / hero swap, `PLAYER_ENTERING_WORLD`,
      `CooldownViewerSettings.OnDataChanged`. `Anchor.lua` hooks all of them and marks
      `# reapply why=<reason>`; confirm the order is restored after each.
- [ ] **The mid-combat teardown, watched rather than gated.** `UNIT_AURA` is the only layout
      teardown that reaches combat and it is unfiltered by unit, so a full aura update on your
      *target* rebuilds the whole layout (`knowledge/addon-dev/cooldown-manager.md` §4.1). If the
      order reverts mid-pull the capture says so: grep
      `# stomp RefreshLayout destructive=1 combat=1`.
- [ ] ⚠ **Watch for `# contended`.** A displacement with no hooked layout call behind it is another
      addon winning the frame. cap now re-asserts and counts strikes rather than stopping, and the
      third inside the window opens the dialog — so a contended row still keeps the *other* addon's
      order and must not be read as a priority, but you are told. (It can also mean a layout path
      `Anchor.lua` does not hook, e.g. the `BottomManagedFrame` container — **which is the standing
      unattributed case**, see Status.)
      ⚠ **A frozen sample is not evidence of a failed apply.** A competitor that wins
      deterministically every round produces a byte-identical `D{}` across every sample, because
      each sample catches the frames in *its* layout. `stomp:0` is what separates the two.
- [ ] **Fly the recovery.** Force a re-pool (spec swap, or a settings change that alters the row
      count) and confirm `# stale` → `# rearmed` → `X{ok}`, rather than a silently scrambled row.
      Then answer the dialog both ways and confirm `# restored` / `# armed` follow.
- [ ] **Decide whether `Anchor` re-applies in combat now that it may.** The cheap version is to drop
      the `InCombatLockdown()` guard in `apply()` and let the existing `# stomp` path re-anchor; the
      question is whether re-anchoring mid-pull is *desirable*, since a row that moves during combat
      is its own kind of wrong.
- [ ] **The un-hide half needs an author call** before anything is built. `/cap anchor rows` reports
      which catalog entries have no pooled frame; making one appear means `SetCooldownToCategory`,
      a write to the player's saved CDM layout, which sits against `spec.md` §4's "does not replace
      or configure the Cooldown Manager" and carries an open `[gap] @verify-ingame` for whether an
      un-hidden row lands in a viewer end to end.

### The swipe says two different things and cap could make it say which

**The author's report, 2026-08-16, after hours of play and independent of cap:** *"the distinction
between I have two seconds left on Tyrant, and I have 2 seconds left until it's off cooldown is
constantly mixing me up in the chaos of combat."* This is a Cooldown Manager problem cap happens to
be able to fix, not a cap problem.

Blizzard already distinguishes them, too weakly: `ITEM_AURA_COLOR = (1, 0.95, 0.57, 0.7)` — pale
cream — versus `ITEM_COOLDOWN_COLOR = (0, 0, 0, 0.7)` — black
`[T1 src @12.1.0: CooldownViewer.lua:20-21]`. Same shape, same direction, same alpha, and the pale
one sits over bright icon art that fights it. Hue alone is losing in combat.

`render-shelf.md` V7 lists the swipe setters that carry no timing and are therefore safe, so all
three of these are available:

- [ ] **Recolour** the aura sweep to read as *a thing running* rather than *a thing dimmed* — the
      pale wash is the same visual move as the veil cap retired.
- [ ] **Reverse one of them** (`SetReverse`). This is the strong one: a dial that FILLS versus one
      that EMPTIES is a **shape** difference, and shape survives peripheral vision and combat chaos
      in a way hue does not. Nothing else in cap's vocabulary uses direction yet.
- [ ] **Suppress** it entirely on one side (`SetDrawSwipe(false)`) — listed because it is available,
      not because it is recommended: the swipe is the elimination walk's first term, and removing it
      takes a term out of the reading model.

⚠ `RefreshSpellCooldownInfo` re-applies `SetSwipeColor` + `SetDrawSwipe` on **every** refresh, so a
one-shot write is silently clobbered. `hooksecurefunc` per instance and be the last writer — the
same shape `Glow.lua` already uses for the proc overlay.

⚠ **This needs a shelf amendment before it is built.** V7 currently declares the opposite — that cap
leaves the swipe at Blizzard's default because the swipe is the CDM's own "ruled out" signal. That
was written before the aura/cooldown ambiguity was named. Amend V7 or this contradicts the shelf.

**Why it may be worth more than it looks.** If *buff running* and *cooldown running* become
unmistakably different sweeps, Metamorphosis during demon form stops reading as available without
cap drawing anything extra on it.

### There is no positive-cue budget — say so in the docs

Author's correction, 2026-08-16: **the single-positive-cue rule is being read as a budget, and it is
not one.** The docs present it as a scarce resource — the Status bullet above says the vocabulary is
negative by default *with exactly one positive cue*, and `capart check` gate 0b hard-fails a second
`polarity: "positive"`. The intent was a guardrail against adding positives casually; the effect is
that a reader reasons about *spending* the positive and declines to propose one that is justified.
Measured: it happened twice in one session, in prose written to the author.

Half of the original contradiction is already fixed. `reading_gate` became an ordered chain on
2026-08-17 — a row wearing a positive cue is judged by pass 1 alone — which is what made a
legitimate pass-1 override representable at all. What is left is the wording and gate 0b.

- [ ] Decide whether pass 1's left-to-right language is real. If it is, multiple positives are fine
      and leftmost wins; if positives really are capped at one, pass 1 is *"is `capped` present"* and
      the scan language should go. Gate 0b's fate is downstream of this.
- [ ] Rewrite the Status bullet and `render-shelf.md` Part 0.5 so the rule reads as **"a positive cue
      is an override of left-to-right ordering, so it carries a burden of proof"** — not as a count.
      The cost of a positive is that it breaks the reading model, and that is a per-cue argument.
- [ ] Decide what happens to **gate 0b**. Options: delete it (the burden of proof is editorial, not
      mechanical); downgrade it to a warning that names the argument a second positive must make; or
      keep it hard and rename it so it stops reading as a cap — its current message is what teaches
      the budget. ⚠ Gates 0d (slot 3) and 1c (every declared cue is worn) are unaffected.
- [ ] Re-examine what the rule caused. `spec.md` §3.6 records a threshold as expressible in
      **either** polarity, and the positive halves — cue B's "banked", cue D's promotion, the green
      dependency dot, the weave chevron — are all parked as "pixels, not authority". Check whether
      any of them was parked for the budget rather than on its merits.

### Ordering versus conditionals — ordering is cheaper to read

Author's position, 2026-08-16, correcting an equivalence stated in review: *"conditionals require
more mental energy than ordering, especially for items already mostly on the far left."*

Two encodings can produce **identical presses** and still not be equivalent to a player. Ranking A
above B with a condition that skips A, versus ranking B above A outright, are behaviourally the same
and cognitively are not: a badge must be seen, identified and interpreted before the eye moves on,
while a position costs nothing. The tax is worst on a **leftmost** entry, where the eye arrives first
and pays it on every scan — including the majority of scans where the condition is false.

- [ ] State it in `spec.md` §3.1 beside eye-direction-by-elimination: **when a fact is stable enough
      to express as rank, express it as rank; reserve a cue for what genuinely varies within a
      state.** A cue that is nearly always lit is a mis-ranked row wearing a badge.
- [ ] Audit the Havoc row for that shape — any marker lit in most states is a candidate for becoming
      rank instead. ⚠ **Decide it from the APL, not from the page.** The row order is now the
      APL's rung order and `Anchor.lua` draws it; a re-rank means `catalog.md` + `scenarios.md` +
      `Catalogs/Havoc.lua` moving together.

### Diagonal stripes — cap hinting *against* an ability

Author's direction, 2026-08-15/16. Stripes say something narrower than the retired veil did — **cap
is hinting against pressing this ability** — and they say it by stating a condition across the icon
rather than by subtracting light from it.

> ⚠ **Build it per-render.** No `stripes` boolean on `tokens.verdicts`, no derivation from cue
> polarity, no shared "is this row striped" state that several conditions write to and something
> else reads back. **Each render that hints against its ability draws its own stripes, owning its own
> parameters.** That is the whole point: when a striped row shows up in flight, the stripes belong to
> exactly one condition and you can say which. A global that three conditions feed is the failure the
> veil retirement removed, re-created in a new colour.

**L4 (black stripes on a detected cooldown) was promoted to V11 on 2026-08-16** and took the shared
stripe sheet with it. The other two remain lab entries — Part 7, deciding nothing, and nothing in
`verdicts`/`cues` may name them until they are *moved* into Parts 1–6.

- [ ] **L3 — red stripes on the sequencing hold.** A row held for a cooldown draws its corner badge
      **and** red diagonal stripes across the icon face, on the phase complementary to V11's, so a
      row that is both held and on cooldown reads as alternating red/black — two conditions visibly
      present at once, which a single shared surface could never show. Drawn by the hold's own
      render, not by a rule about holds.
- [ ] **L5 — red stripes on `starved`.** From *its own* render. It uses the same red as L3 because it
      is the same kind of statement, not because a rule says every negative thing is red. If after
      flying all three the renders turn out to be drawing something identical, **that is an
      observation that may earn a shared recipe later**, not a rule to author up front.
- [ ] **No dim comes back with them.** Stripes state a condition without subtracting light.

### Add a shelf section for what Blizzard already draws on a CDM icon

Read off the Tier-1 source at
`raw/addon-research/wow-ui-source-12.1.0/Interface/AddOns/Blizzard_CooldownViewer/` — swipe,
charge/count text, desaturation, the proc/visual alert overlay, pandemic alert, and their layers. It
is the inventory of what cap gets for free and must not restate or fight, and the preview reads it
to draw a faithful row. Client facts drain to `knowledge/addon-dev/cooldown-manager.md`; the shelf
section is the *rendering* view of them.

### ~~Close the sidecar prose gap in `capart check`~~ — DONE 2026-08-19

`check` compared doc against sidecar on `(name, verdict, cues)`, so scenario **prose** could drift
ahead of the rendered preview with no signal — measured twice, once on a citation fix and again
during the veil retirement, when the walk still said "veiled" and `check` passed. It now compares
the **whole scenario** and names the differing field. Verified by probe: a one-word edit to a
`State` bullet fails with `RET-1: … state: doc and sidecar disagree`.

The general lesson, since the same shape recurs: **a whitelist of compared fields fails on the
next field added, not on the ones it lists.** `{client: …}` shipped outside this one and was
unguarded from day one.

⚠ **The DONE above holds only for the four `catalog.json` specs; on the two SIDECAR-LED ones it
is vacuous** — measured 2026-08-26 while editing Devourer's walks. `load_scenarios`
(`../../tools/wowkb/capart.py:750-751`) returns the **sidecar** as the comparison subject whenever
a spec has a sidecar and no `catalog.json`, so for **devourer** and **destruction** `check`
compares the sidecar against itself and the `.md` is never read at all. The failure it lets
through is the exact one this entry was written to close: edits to `scenarios.md` produced a
byte-identical preview and a green `check --all`, and only a hand-run `capart import scenarios
devourer` moved the page. So the prose gap is closed where a catalog exists and open where one
does not — which is the wrong way round, since a sidecar-led spec is precisely the one whose
`.md` is the only authored source. Migrating Devourer (`## Status`) removes half of it; the other
half is Destruction's until it migrates, and the durable fix is for `check` to scrape the doc
independently rather than re-using the loader's chosen subject.

### Teach `Catalog.OrderCheck` what it is actually checking

It compares the catalog against Blizzard's `layoutIndex` and reports as though that were the drawn
order. Since `Anchor.lua` shipped that is no longer true even on a stock setup — `GetItemFrames()`
sorts by `layoutIndex`, so every instrument cap owns is blind to a `SetPoint` re-anchor by
construction, and under a competing CDM skin the check is neither right nor wrong but blind, which
is the worse failure. At minimum its capture note should say which order it read.

### Target-aura latch — retarget is the only part that needs a flight

Aura secrecy is **combat-gated**, so cap mirrors aura truth out of combat and freezes it at
`PLAYER_REGEN_DISABLED`; edges maintain it from there. Cue G rests on a read, not an assumption.

**Two of the three risks are self-evident in play and are not tracked here.** Whether the seed
survives the transition, and whether `OnAuraApplied` arrives when Blade of Justice lands
Expurgation, both show up on the first pull — Blade of Justice is prio at the opener or it is not,
and Avenging Wrath releases or stays held all fight. Play it; do not build a flight for either.

- [ ] **Retarget only.** Does `PLAYER_TARGET_CHANGED` → `RefreshActiveFramesForTargetChange` raise
      aura alert edges (`knowledge/addon-dev/cooldown-manager.md` §5.1, :960)? If not, the latch
      describes the previous target. **Deferred until Affliction** — Retribution presses Avenging
      Wrath about once per opener, so a stale latch barely shows; multi-dotting is the whole of
      Affliction and it would be wrong constantly.

⚠ **No enablement detector, no setup warning, and `cdm-aura-edges-need-a-bound-row` is retired.**
This addon has one user, who knows to enable the Tracked Buff and knows what to blame if a row is
lit all fight. Should it ever want one, out-of-combat truth vs. the latch is a direct differential
and needs no item-frame enumeration.

### Split the Immolation Aura charge question in game

The 2026-08-15 flight's capture carried `immolation_capped` ×40 and `immolation_recharging` ×58 on a
loadout the player says had **no A Fire Inside** — a genuine contradiction that is still unexplained.

⚠ **State it accurately, because the first two explanations were both wrong.** `Sense.lua:105`'s
`maxCharges <= 1` guard is **pre-existing**, so on a one-charge build `capped` is **UNKNOWN**, not
`true` — the gold badge would have been *withheld*, not stuck on. So "the guard is not holding" is
not the hypothesis; either a different loadout was flown, or the client reported more than one
charge, or the badge came from somewhere else.

- [ ] `/reload` on the single-target loadout and read the `draw` capture. No charge cue means the
      flight was simply on the AoE build; anything else is a real bug. ⚠ The capture can no longer
      corroborate it from a `CHARGES` lane — the wire format is `id:scan` and carries no tier
      (2026-08-19), so the cue is the only term left that answers this.

Since then the gold badge has gained an explicit `talent` gate on A Fire Inside / Burning Wound,
which makes the behaviour deliberate rather than a side effect of a guard in another module — but it
does not explain the capture.

### Re-fly Havoc against the 12.1-sourced catalog

The row last flew on 2026-08-15 against a catalog that has since been re-sourced from the Tier-1
simc APL, gaining two predicates, four corrected holds, a row swap and a skip badge. Nothing about
the current row has been judged in play.

- [ ] One flight for the whole row, per `flight-reading.md` → *The Havoc row*: one player-experience
      question stated before playing, the player's judgment recorded in their own terms, captures
      read only afterwards to explain which route armed.
- [ ] It also carries the shipped-but-unflown style: the scan edge (Part 5 q2) and the cooldown
      hatch (q7), plus q1 and q5.

### ~~Consolidate the three Havoc docs into one `catalog.md`~~ — RETIRED 2026-08-19

**Do not re-raise this.** The one-`catalog.md`-per-spec rule it enforced has been reversed:
`catalog.md` / `scenarios.md` / `fact-classification.md` are a definition, its proof and its
safety case, and Havoc's three files are now the **model** rather than a debt
(`authoring.md` §0). Retribution was split to match on 2026-08-19.

The item's *other* half survives on its own, below.

### `rotation.md` is the sole home of the priority order

The gameplay KB carries the priority list with front matter and provenance; a catalog cites it and
must not restate it. Audit the per-spec catalogs for a second copy of the order — two copies drift,
which is the whole reason `simc-apl.md` exists as a generated artifact.

### Close out the migration artifacts

`simplification-plan.md`, `simplification-audit.md` and `rule-split-audit.md` are temporary and are
not product authorities. Delete or archive them, and remove the obsolete modules, fields and
vocabulary that were kept as compatibility scaffolding for an unreleased design.

### ~~Judge the two unflown Warlock surfaces~~ — ANSWERED ON PAPER 2026-08-19

**Do not re-raise as written.** Both questions were about the *pilot* surfaces, and the 2026-08-19
authoring pass answered both from the priority rather than from a flight — which is the cheaper
answer and the one that was available.

- **The independent Tyrant countdown bar is not authored**, so there is nothing to judge. The
  Demonology catalog declares no bar: the fact it would draw is Tyrant's own **sealed** cooldown
  remaining, and the row now carries the **readable** half of the same decision — a hold below
  five Soul Shards, which is an exact Lua comparison. `spec.md` §3.3 still owns the bar's
  semantics and the permission is unchanged; the duration-object recipe stays in
  `knowledge/addon-dev/` and under recipe `S6` in `authoring.md`'s index, with **no product code preserved for it**.
- **The sealed Backdraft marker has no consumer in the single-target rotation.** Its rungs ask
  whether Backdraft is *absent* (`buff.backdraft.stack<1`), which the readable aura latch answers;
  the sealed **count** is right for the AoE rung that asks for two stacks, and that rung is not
  authored. OBS-065 already carries the human verdict on the display itself.

⚠ **What is genuinely still unflown is everything**, and it is bigger than these two questions —
see the Status block. Neither Warlock spec has a catalog Lua of the current design.

### Two future Warlock catalogs, each with its reopening condition

Both are **separate catalogs authored later**, never overlays on the shipped ones — a
spec-and-hero pair is the unit (`authoring.md` §0).

- [ ] **Soul Harvester (Demonology).** `actions.soulharvest` is a genuinely different list: **no
      Ruination rung at all**, and Tyrant and Dreadstalkers cast plainly on cooldown with no
      Reign-of-Tyranny window — so two of the Diabolist catalog's cues would have to be deleted
      for it. **Reopening condition:** Season-2 logs or a regenerated `sims.md` putting Soul
      Harvester ahead in **M+**. Icy Veins already has it ~3 % ahead in *pure single target* at
      12.1 (Tier 3), which is not enough on its own —
      `knowledge/classes/warlock/demonology/builds.md` carries the argument.
- [ ] **Hellcaller (Destruction).** `actions.aoe_hc` is gated on `talent.wither`, and Wither has
      **no `CooldownSetSpell` row in any set** at 12.1.0.69214 — so the first thing that catalog
      must solve is which row the spec's whole DoT rides, exactly as Incinerate rides Shadow
      Bolt's. It also adds Malevolence, which the Diabolist catalog leaves unbound. **Reopening
      condition:** Season-2 logs or a re-sim putting Hellcaller ahead in M+. 12.1's Blackened Soul
      rework was an explicit Hellcaller priority-target buff and nobody has re-run the comparison,
      so this is a live possibility rather than a formality —
      `knowledge/classes/warlock/destruction/builds.md` carries it.

## Ideas

- **The empowered-cast (Demonsurge) cue — an optimisation over the baseline, not part of it.**
  Havoc's rung 3 has three holds and the catalog draws two. The third is
  `!action.death_sweep.demonsurge_available & !action.annihilation.demonsurge_available` — *don't
  recast Metamorphosis while empowered casts are still owed* — and nothing on the row says it.
  `proc` already exists in `Catalog.PREDICATES`, so **if** an owed empowered cast surfaces as a
  readable proc on the row, this is a marker and not a mechanism. That "if" is the whole of the
  work: measure first (`specs/havoc/catalog.md` → *Open facts* 6), then author. **Do not build it as
  part of the Havoc baseline** — the baseline ships without it and is coherent without it.
