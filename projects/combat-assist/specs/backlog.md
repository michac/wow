# Combat Assist Plus — backlog

**What this file is for:** the current implementation status and the ordered work list.
`spec.md` owns intended behavior; `notes.md` owns completed history; `discussion.md` owns only
questions that still require an author decision.

The live addon version comes from `wowkb.addon list`, never from prose here.

**A committed item may carry a plan file in `backlog/`.** The one-line entry stays here, in
order, and the steps live beside it — `backlog/<slug>.md`, deleted when the work lands and
`notes.md` records the round. That is the only thing the folder is for: it is not a second work
list, and an item with no plan file is not lesser.

**An item here has to keep earning its place.** Completed phases, migration checkpoints and
corrective passes are history and belong in `notes.md`; the measurement behind a status line
belongs in `notes.md` or `knowledge/addon-dev/`. If an item's premise stopped being true, rewrite
it or delete it — never leave it standing with a note underneath.

## Status

This is the project's only implementation-status source. **It records what is BUILT.** Per-fact
uncertainty is not a status field here — it lives as a marker on the fact itself, where it names
what would be wrong and is read at the point of use: `@verify-ingame` on a claim, `--@unverified`
beside the call it doubts. A blanket "unflown" stamp on a paragraph had no owner, no removal
criterion and no reader, and went stale the moment anyone logged in; it was retired 2026-08-28.

### The engine

- The engine supports the readable predicates its catalogs use — `ready` · `proc` · `identity` ·
  `capped` · `affordable` · `aura` · `baseoncd` · `resource` · `talent` · `aoe` — propagates
  unknown safely, composes a
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
  It carries the uniform blind rule (no ON alternative + any BLIND alternative ⇒ withheld) and
  two accepted behavior changes: Demonology Shadow Bolt and Destruction Incinerate/Conflagrate
  stay lit under blindness where their deleted two-band flips darkened them.
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
  `arrival-*` entries, which had been deleted six days earlier. Part 5 question 2 asks whether a
  static line is loud enough in a pull.
- **V11's cooldown hatch is shipped** (2026-08-16), on every row the CDM says is down.
  `verdicts.cd` is the only verdict carrying `hatch: true`, and **only `false` draws** — an
  `UNKNOWN` or absent readiness draws bare, so absence of a hatch never asserts a button is up.
  ⚠ A **charged** ability and a row whose first readiness edge has not landed will not wear it, so
  the hatch is not a complete census of what is down. Part 5 question 9 is the readability ask.
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
  ⚠ FlipBook semantics are a **source read** and the doubt is marked where it belongs:
  `--@unverified` on `Paint.FlipBook`.
- **V18 is the segmented bar, red at full** (2026-08-24, replacing the radial). The sealed
  count draws as a left-to-right bar on the row's BOTTOM edge over a segment grid (cap's own
  track art), and at `max` the **whole bar flips to the negative red** — a second slot's count
  band (`Channel.BarFlipRules` → the pre-tinted `bar_full` crop) at threshold = max,
  client-decided. First consumer: Demonic Core (full stacks = procs about to be wasted). The
  move off the corner also ends the DEM-8 geometry conflict with V19's badge (Part 5 #10 is now
  a readability question). Radial render mode retired from the style.
- **Badge geometry is a ratio of the row's MEASURED width, not of the shelf's nominal icon.**
  `Paint.Ratios(width)` is the arithmetic, `Paint.Geometry(host)` is it with the width read off
  a host, and every badge, plate, glyph, halo and promotion ring is sized through one of them.
  The three frozen escape sizes are gone from `render-tokens.json` — `count.hatch_px`,
  `plate_px` and `mark_px` were `Geometry()` outputs computed once against a 56 px icon, so on
  any other icon size every badge on every row was mis-sized and mis-placed. `Channel.CountGeometry`
  derives them at arm time; `capart` derives the preview's from the same ratios.
  ⚠ **Which makes PINNING ORDER load-bearing.** `Overlay.acquire` anchors onto the CDM item
  before it builds a single primitive, `rebuild` re-anchors before `configure`, and
  `Channel.Arm` returns **`deferred`** on a host with no valid rect so the per-draw retry picks
  it up. An escape's size is a literal baked into the band string when the sink is armed and
  never revisited, so arming against a 0x0 host froze the whole row at the nominal.
  `/cap band` has lost its size argument for the same reason — the offset is still nudgeable,
  the size is now read-only, and the no-argument readout prints measured width beside drawn
  diameter as the assertion.
- ⚠ **A band is still sized ONCE, at arm time** — and since 2026-08-31 that is **no longer a
  live defect**, because its cause is gone rather than fixed. The stale case was an Edit Mode
  icon-size change under a live row; cap now owns the icon size (`spec.md` §3.9), so that
  setting cannot resize the rect a band was sized against, and cap's own `icon_px` is a token
  baked into `Style.lua` at load, which cannot change without a `/reload` re-arming everything
  anyway. **What remains open is the client question, not the defect**: whether
  `SetApplicationCount` can be called a second time on a live button
  (`@pending-test: aura-sink-recall`, `security-taint-and-restricted-data.md` §3.5.3) — the
  source reads as a plain setter but nothing in the 12.1 UI calls one twice. Still **not built**;
  it is now a resize path with no known caller rather than a gap with a symptom.
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
  measured in the preview. ⚠ The `AddPandemicRegion` + `SetDurationBar` **one-button pair has
  only ever been measured a half at a time** — Part 5 #11 asks it as a readability question.
  Count bands: the hatch is legal on **negative** bands only (`Channel.CountRules` refuses a positive hatch), and the
  numeral rides ON the badge plate as its own `plate` element/slot (`Channel.CountElements` is
  now hatch → plate → mark → count). No catalog declares `outside_s` yet.
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
  RULE, whose *static by declaration* half still stands and whose geometry has since been
  replaced by the z-stack below; DEM-8's Demonbolt — two stacked bars plus the window badge —
  is the densest row in any catalog. Demonology also grew the ramp holds (cue I, `building`, authored PAST the
  unconditional APL rungs — playtest-gated), re-badged Demonbolt's core hold to `noproc`, and
  its scenarios now wear the Implosion imp band everywhere imps are out (the "no markup on
  Implosion" gap), with DEM-13's Tyrant-ready/Tyrant-far contradiction fixed in passing.
  All of it is built: the dial pair, the three-point band, and the cession geometry.
- **The badge corner is a Z-STACK, and V21 is the first primitive that needed it.** Every badge
  on a row — cue badges, graded badges, corner sealed displays — draws at the SAME place and is
  separated by frame level (`Paint.Z` / `CueLevel` / `CornerLevel`), so exactly one is visible.
  The order is Part 0.5's reading model rather than the cue rank — **negatives occlude positives,
  rank decides inside a polarity, sealed corner displays lose to every negative** — because the
  two failure directions are not the same size: a skip hidden under a promotion makes a held row
  look pressable. `Treatment.Stack` resolves it, answers for EVERY key in the vocabulary so a
  loser is HIDDEN rather than merely covered, and `presentation_spec` asserts that. It replaced
  the flowing stack, whose measured defect was arithmetic: at 40 % on a 56 px icon a 3-deep stack
  overflowed the icon by 15.2 px and a 4-deep one by 40.6 px, across 13 states in two catalogs,
  and no gate could see it — the elimination gate asks whether a row CARRIES a negative, never
  where the badge lands. With one badge to draw, `badges.diameter_pct` went 40 → 48.
- **V21 is the live cooldown dial, and it IS the `blocked` badge** (2026-08-28). A row held
  because a cooldown is running draws that cooldown — a red radial on the real remaining with a
  white countdown in it — where `timer_CW_50`, a picture of a clock frozen at 50 %, used to sit.
  Same cue, same polarity, same rank, same red hatch beside it. Two catalog displays reach one
  widget: `sealed-base-cooldown` (this row's own base spell, gated on the readable `baseoncd`
  predicate — `C_Spell.GetSpellCooldown(baseID).isActive`, NeverSecret and plain in restricted
  combat) and `sealed-cooldown-range` (another ability's, with the band's Step curve writing the
  frame's alpha exactly as it used to write a badge's). Either way the duration object goes to
  `SetTimerDuration` and `FormatRemainingDuration` and cap never reads it. Not an AuraContainer —
  there is no aura behind a cooldown — so it is cap's own frame with its own teardown. A marker
  declaring both a dial display and a `cue` draws that cue AS the dial and the sprite for it is
  not drawn; one declaring no cue keeps its corner claim and asserts nothing.
  **Consumers:** Demonology's Grimoire (its own 120 s, on a row wearing the dispel it becomes,
  plus a new `(3, 10)` Tyrant band authored past the APL on 2467 logged casts) and cue J on Call
  Dreadstalkers, which inherited the dial with no change to its marker; Havoc's Essence Break
  reading Eye Beam is the third. Devourer's **Voidblade** can inherit it with a marker and no
  code. ⚠ **This reopened the 2026-08-23 ruling that retired animated negatives.** What that
  flight rejected was a five-frame flipbook of a *fake* clock; a real radial terminates and
  carries information. `capart check` gate **0e** — a negative may declare only one frame — was
  **deleted** rather than widened, having been measured inert first, so the rule now lives in
  `render-shelf.md` V5.1 with nothing enforcing it: `Paint.Badge` still builds a FlipBook for any
  multi-frame cue.
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
  - **Ordering holds in combat.** Nothing on the anchor path is gated on `InCombatLockdown()`:
    the CDM's item frames are unprotected (`IsProtected()` returned `false, false` on 9 of 9
    Havoc rows, in and out of combat — `knowledge/addon-dev/cooldown-manager.md` §4.1) and a
    bind resolve is pure reads. `Anchor.Judge` reads no combat flag, so a re-assert is the same
    verdict in a pull as out of one. The accepted cost is that icons may move mid-fight, which
    is the trade for a row that never silently reverts to Blizzard's order.
  - **The re-assert is per frame and synchronous.** `Anchor.lua` hooks each tracked item
    frame's own `SetPoint` and puts it back inside the call that moved it, discriminating cap's
    own writes by whether the point is relative to cap's anchor frame. The 0.5 s sampler is an
    **auditor**: it measures drift, drives `Judge`/contention and re-places as a backstop, but
    the repair no longer waits for it. `S{reassert:<n>}` counts the corrections.
    ⚠ **A layout pass may still move the row; a displacement may not.** Correcting inside
    Blizzard's own `SetPoint` destroys the evidence of where it was moving the row TO, so the
    hook reads the position first and `apply` adopts it as the new origin — but only when the
    apply came from an event rather than from a judged displacement, or a competitor could drag
    the row simply by losing to cap repeatedly.
  - ⚠ **The classifier has unit coverage; the dialog, the rebuild, the stale detector and the
    per-frame re-assert do not.** They have been reasoned about, not exercised — so the counts
    those four produce are the numbers to distrust first.
  - ⚠ **The unattributed case is unresolved but should now be attributable.** The capture showed
    displacement with neither `Layout` nor `RefreshLayout` firing. A mover that goes through
    `SetPoint` is now caught whether or not it exposes a hook; one that survives to the sampler
    reached the frame by another route (a scale or parent change) and reads as `# contended`.
    The flight is what tells the two apart.
  - ⚠ **Not built:** the always-show / un-hide half. `SetCooldownToCategory` writes the player's
    saved CDM layout, which the ordering design deliberately avoided, and it needs an author call.
  - **A claimed frame the plan loses is PARKED, not abandoned.** `Anchor` tracks every item
    frame it has moved (`claimed`), and one that drops out of a rebuilt plan is held offscreen
    instead of left sitting in the row in nobody's order — `spec.md` §3.9's fifth property,
    amended for it. The commonest way in is a live `GetCooldownID()` that stopped matching,
    which takes a row out of `Bind`'s list without taking the icon off the screen. `disarm`
    restores `claimed` rather than `tracked`, so turning ordering off returns parked icons too,
    and a destructive stomp drops every claim — the pool re-issues those frames against new
    rows, and a stale park would make a live ability silently invisible. `A{parked:<n>}` is how
    many are off the row now, `S{park:<n>}` how many have been across the session, and the
    `# parked` mark is emitted by the apply that MOVED them, never by the plan rebuild that
    decided to.
  - **cap stands down beside another CDM rider** (2026-08-31), which is `spec.md` §3.9's sixth
    property. Two addons that each hook an item frame's own `SetPoint` and force it back to
    their own anchor recurse without bound inside one call stack — a client crash, not a
    flicker (`knowledge/addon-dev/cdm-rider-patterns.md` §4.6.1, which also records the
    shipping rider that carries a hardcoded early-bail for the same reason). `Riders.lua` holds
    the known-rider table (`EllesmereUICooldownManager` plus the five named in EllesmereUI's own
    conflict list) and every word the player reads; `Anchor.lua` decides in two stages **before**
    `adopt` installs the first hook. `C_AddOns.IsAddOnLoaded` on the folder name says WHO to
    name; an Essential item frame whose points name neither the viewer's subtree nor cap's own
    anchor says whether that addon is actually holding the row. Both must agree, so a module that
    is installed but switched off never nags. On a hit cap refuses to arm, says it once in chat,
    and raises a **single-OK** modal — its own `StaticPopupDialogs` entry, because
    `GENERIC_CONFIRMATION` is two-button by construction
    (`knowledge/addon-dev/frames-textures-animation.md` §2.6). The acknowledgement is
    deliberately **not** persisted: it returns on every login and `/reload` while both are
    enabled. It fires only where cap would otherwise have ordered — `/cap anchor off` is never
    nagged — and defers out of combat exactly as the contention question does. The decision is
    re-taken on every arm attempt, so disabling the rider releases cap on the next event.
    - `_G._CAP_IsOrderingEnabled` is published so another addon's conflict table can gate its own
      popup on cap actually ordering, following the `_ERF_IsHoverCastEnabled` precedent
      EllesmereUI's Clique entry already uses. It reads the setting AND the stand-down.
    - **`onFramePoint` carries a re-entry depth guard** for the rider that claims the row *after*
      cap has armed, which the arm-time test cannot see. Exceeding it stands cap down instead of
      recursing; the teardown is deferred because the guard fires inside somebody else's
      `SetPoint`. It latches for the session, and `/cap anchor retry` releases it.
    - **What has been exercised:** the two-stage decision and the wording, by `riders_spec` (12
      assertions), and — **in the 2026-08-31 flight** — the modal, the positional test against a
      live rider and the depth guard, the three client behaviours the suite cannot reach. All
      held.
  - **The row is a named 6x2 panel the player places** (2026-08-31), which is `spec.md` §3.9's
    seventh property and the first half of making the row anchorable by other UI. `P.anchor` was
    a nameless 1x1 `UIParent` child whose position was re-derived from Blizzard's measured
    geometry on every pass, so the row had no position of its own and nothing could be anchored
    to it. It is now `CombatAssistPlusRow`, sized `tokens.row` (6 across, 2 down, 50 cell,
    1 gap) and placed from a saved position.
    - **`Place.lua` is Frame.lua's placement machinery, parameterised rather than copied.**
      `Frame.lua` was single-panel throughout — one hardcoded store key and ten functions over
      one file-local `panel` — so it was lifted into a keyed module that both frames register
      with, taking `Window.lua`'s keying and `Frame.lua`'s scale arithmetic. (`Window.lua`'s own
      maths is not reusable here: it may skip normalisation because a window is never scaled,
      and the row panel is scaled on every apply.) `db.frame` migrates once into
      `db.places.frame`, and the old key is left rather than moved so a rollback still finds the
      panel where the player left it.
    - **`/cap move` now unlocks both frames at once.** `/cap <verb> [<arg>]` is the whole command
      budget and `reset` already holds the argument slot, so a per-frame verb has nowhere to go;
      one gesture for all of cap's furniture also reads better than two. Every chat line grew a
      subject, since "frame locked at …" no longer identifies anything.
    - **Two things were deleted rather than repaired.** `metrics()`'s gap derivation is gone —
      the grid is cap's now, and for the record its `DEFAULT_GAP = 4` fallback was wrong:
      Blizzard's layout padding is `iconPadding + GetAdditionalPaddingOffset()` = 5 + (-4) = 1.
      And the whole `P.foreign` origin-adoption path is gone, because following the Cooldown
      Manager's placement is precisely what a row with a saved position must not do. That is a
      **behaviour change**, recorded in `spec.md` §3.9: an Edit Mode move of the viewer no longer
      drags cap's row with it.
    - ⚠ **The one trap, and it is a double-count.** Every length in `tokens.row` is in the
      panel's OWN coordinate space. The panel wears a scale matching the item frames, so Edit
      Mode's icon-size setting arrives as that scale — `GetWidth` on an item frame reads 50
      whatever `SetScale` did to it. The plan's `50 x iconScale` cell would have counted the
      setting twice; the floor is 50 flat, and `anchor_spec` asserts the grid does not vary with
      `iconScale` so the mistake cannot come back quietly.
    - **What has been exercised:** the store and its migration (`place_spec`, 7 assertions) and
      the grid arithmetic (`anchor_spec`, 6), and — **in the 2026-08-31 flight** — the drag, the
      seed from a live viewer, and the panel holding across a spec swap. All held. ⚠ The Edit Mode
      icon-size half of that last step no longer asks anything: cap owns the icon size, so the
      slider cannot reach the panel. The flight turned `row.icon_px` instead.
  - **cap draws nothing when it cannot order the row** (2026-08-31) — `spec.md` §1's new
    **principle (c)**, which is a line in the sand rather than a feature. Ordering and the
    augments were separable and should not have been: §3.1's reading is a claim about POSITION,
    so an overlay on a row cap did not order points at the wrong icon. Measured before changing
    anything: **nothing outside `Anchor.lua` consulted ordering at all**, so `/cap anchor off`
    and the rider stand-down both drew the full overlay — scan edge, badges, elimination — onto
    a row in Blizzard's arbitrary saved order.
    - The stand-down was the sharp version of it: its modal said *"the row's left-to-right order
      is not cap's and should not be read as a priority"* and then cap drew the thing whose
      entire meaning is "read this as a priority". The message now says cap is drawing nothing,
      and `riders_spec` asserts the old sentence is **gone** rather than merely present.
    - **Enforced in ONE place**, `Sense.Verdicts` — which already described itself as the one
      place the settle and dark-for-the-fight rules live rather than being re-derived per
      surface. There are two subscribers today (`Overlay`, `Panel`) and a third inherits it for
      free; returning nil is also what makes them HIDE, since nil is the draw-nothing path every
      surface already handles.
    - `/cap status` gains a **DARK — NOT ORDERING** term directly under `OFF` and above every
      finer diagnosis, because while it holds none of them is worth reporting. `Anchor.NotOrdering`
      returns `"off"` / `"rider"` / nil, passed INTO `Status.Verdict` rather than read off the
      namespace so the classifier stays pure. The two causes get different advice: one is a
      setting to flip, the other an addon to disable.
    - ⚠ **It settles half of `discussion.md`'s open Vengeful Retreat question and not the other
      half.** The sub-question — should the scan edge be suppressed outside the scanned viewer —
      is answered yes, by the same argument, and is now a general rule. The top-level call
      (bind for the hatch, or unbind) is still the author's, and is cleaner for it. **Per-viewer
      suppression is NOT built**: a bound Utility row still draws its edge, deliberately left
      until that question is answered, since unbinding would make the suppression moot.
    - **What has been exercised:** the ordering term's place in the status order and its two
      reasons (`status_spec`, 5 assertions) and the rewritten stand-down message (`riders_spec`).
      and — **in the 2026-08-31 flight** — that the overlay does go dark in the client on
      `/cap anchor off` and comes back on `/cap anchor on`.
  - **Placement is per character; opinions stay per account** (2026-08-31). `CombatAssistPlusDB`
    keeps `enabled` and `anchor`; a new `CombatAssistPlusCharDB` keeps `places`. ⚠ **This closes
    a regression the panel work introduced hours earlier and did not survive one question.**
    `placed` is a single boolean, so an account-wide store is seeded **once**, by whichever
    character logs in first — every character after that inherits a position measured from
    somebody else's Cooldown Manager and never seeds its own, with nothing on screen to say why.
    Before the panel existed the row was re-derived from measured geometry every pass and could
    not be wrong this way; the movable panel traded that away without noticing.
    - **A seeded position does not cross characters and a dragged one does.** `Place` records
      `by = "seed" | "move"`, and the migration reads it: position carries over as a starting
      point either way, but `placed` is dropped when the only reason it sat there was a seed
      taken elsewhere. Copying the flag unconditionally would reinstate the bug in the very
      migration written to fix it. The pre-keyed `db.frame` era is read as `"move"`, correctly
      — the row did not exist then, so nothing in it was ever seeded.
    - Both account-wide shapes (`db.frame`, and `db.places` from the two builds released
      earlier today) are read and **left in place**, so a rollback still finds them.
    - **What has been exercised:** the split, the two migrations and the seed rule
      (`place_spec`, 12 assertions, including that nothing writes placement into the account
      table and that two characters do not see each other's), and — **in the 2026-08-31 flight**
      — that a second character seeds its own row, flown on two characters with the Cooldown
      Manager in different places.
    - ⚠ **One bug found by writing the test procedure down** (2026-08-31): `resizeAnchor` set
      the panel's scale without re-applying its position. The saved offset is stored in UIParent
      units at scale 1.0 and written back DIVIDED by the panel's own scale, so the number
      already in the panel's `SetPoint` was computed against the OLD scale and means a
      different screen position under the new one. The armed path re-applies a line later and
      hid it entirely; the Edit Mode settings callback fires whether or not cap is ordering, and
      **there the panel jumped**. It re-applies on rescale now. Found by asking what an icon-size
      change is supposed to LOOK like, not by a test — which is the argument for writing a
      flight procedure as steps and expectations rather than as a phrase.
    - ⚠ **And that bug was a symptom — the premise under it was never decided** (2026-08-31).
      Following Edit Mode's icon-size setting was an implementation default that arrived inside
      the Phase 1 commit and hardened into a requirement; `spec.md` never stated it. **Authority
      is now inverted: cap owns the icon size** (`spec.md` §3.9, eighth property). `row.icon_px`
      in `render-tokens.json` is the one authored knob, the panel wears `icon_px / 50`, and cap
      re-asserts that same effective scale onto every frame it claims — from inside `place`,
      the single door every write goes through, because Blizzard re-applies `iconScale` at
      **pool acquire** and a one-shot would silently revert on the first spec swap. `disarm`
      gives the slider's value back. `icon_px` defaults to 50, the template's own size, so the
      landing is pixel-identical for anyone who has not authored a size.
      - The rescale re-apply above is **kept as a guard and is no longer load-bearing**: the
        panel's scale is now a constant read from a token, so nothing at runtime can change it.
      - ⚠ `Anchor.Scale` / `Anchor.ItemScale` are exported for the same reason `Grid` is —
        the correction for a claimed frame's parent is arithmetic that is checkable without a
        client, and getting it wrong reintroduces the v0.18.1 bug one level down, invisibly,
        because it is the identity whenever the viewer sits at UIParent's scale.
      - **Flown 2026-08-31**, on v0.19.0 and again on v0.19.1, `/cap band`'s readout included.
        The three things the tests could not reach all held: a real CDM item frame takes the
        `SetScale`, the re-pool is caught by the re-assert on the next `place`, and `disarm`
        gives back a size the player can see. `scalefail=<n>` did not appear in the capture —
        it is the standing signal, so its absence is the result, not the lack of a look.
    - **Two knock-on geometry decisions, both raised by the post-release review and both taken
      the same day.** Neither was a regression; the inversion is what made them indefensible.
      - **The client's fallback icon size split from the preview's.** `Paint.Extent` and
        `Channel.CountGeometry` fell back to `surfaces.icon_px` = **56** — the PREVIEW's
        authoring nominal — while the frame they stand in for is **50** in its own space at
        every setting. Every escape sized on that degraded path was 12% over, which `Paint.lua`
        already recorded measured in flight: *"a 56px escape on a 42px icon is where the
        overhang came from"*. `surfaces.host_nominal_px` = 50 is now the client's, `icon_px`
        stays the preview's, and `/cap band` prints `host nominal` instead of a 56 that read as
        a discrepancy. ⚠ `/cap style`'s gallery still reads `icon_px` **deliberately** — it
        shows the shelf as authored rather than decorating a real frame.
      - **The virtual row lost its own icon size.** `panel.icon_px` was authored beside
        `row.icon_px`; both read 50, so nothing showed. But a V12 row is a PEER in the same
        scan (Devourer's Consume), and `row.icon_px` is now the one knob a player turns — so
        the first authored size would have left Consume the only entry in its scan at the old
        one. The token is **deleted**, not synchronised: `Panel.lua` derives from
        `ns.Style.row.icon_px`. `render-shelf.md` V12 says so.
      - ⚠ Both were invisible because the numbers agreed by coincidence. That is the shape to
        watch for elsewhere: a duplicated constant is not caught by a test that only ever runs
        at the value where the duplicates match.
  - **The panel's second row is real** (2026-08-31). The panel has been `6x2` since it was
    named, but placement laid every icon out on one axis and ignored the second row of cells, so
    a roster longer than six ran off the right-hand edge of a panel that claimed to hold it.
    Three pure functions carry it: `Anchor.Cells` (offsets for `n` icons), `Anchor.ReadOrder`
    (the drawn order), and `Anchor.Plan` gaining a `breakAt`.
    - **A catalog may name ONE break, `break_before = "<entry id>"`,** and a break entry that is
      not talented **falls through to the next present entry** — the alternative is a hole in
      the row every time a talent moves. It is resolved in PLAN space, not in `Catalog.Resolve`:
      Resolve's `byEntry` does not know about the dedup that drops the second of two entries
      naming one row, nor about the unnamed rows appended after the named ones, and both change
      which item is first past the break. `Catalog.Check` refuses an undeclared id, the first
      entry, a non-string, and a **virtual** entry — the last because a virtual entry never
      reaches `byEntry`, so the key would be a permanent no-op with no error behind it.
    - **The break is a MINIMUM wrap point, not the only one.** A row also ends when it runs out
      of columns. ⚠ **That is a visible change for FOUR of the six specs**, measured rather than
      assumed, at the token's six columns: Havoc 12 placed entries → 6 + 6, and Demonology,
      Protection and Retribution 9 each → 6 + 3. (Havoc has declared `cols = 7` since
      2026-09-01, so its own clamp is 7 + 5.) Devourer is 6 placed plus 1 virtual and Destruction 1, so both still fit one
      row. (An earlier note here said Havoc was the only spec long enough; it counted authored
      entries against two rows instead of against one row's six columns.) **All four now author
      one** (2026-09-01) — see *The four breaks are authored* below.
    - ⚠ **The row split is part of the VERDICT, and that was nearly missed.** `Anchor.Drawn`
      returned an id sequence and `match` compared it elementwise, so a pass that collapsed all
      twelve icons onto one row would produce the *identical* sequence to the correct two-row
      draw and read `X{ok}` forever — the phase would have shipped with no instrument for the
      only thing it added. `Drawn` now measures how many landed on the first row and `match`
      requires it to equal what `apply` placed. The wire carries it as a `|` in **both** `P{}`
      and `D{}`, so the two are read beside each other; a count in `A{}` would have restated the
      plan's own number and could never have disagreed with itself.
    - ⚠ **Two things that look like details and are not.** The y axis points **up**, so
      descending a row is negative — and a positive `y` would draw the second row above the
      first with the drift auditor reporting **zero drift**, because `want.top` would be wrong
      in the same direction. Nothing already in the addon catches that, so the sign is asserted
      by a test. And the reading sort is **top descending, left ascending**: a higher `GetTop()`
      is higher on screen, so an all-ascending comparator passes every same-row assertion and
      silently reverses the rows.
    - ⚠ **The row comparator uses an integer bucket, not a tolerance, deliberately.** A
      comparator of the form `abs(a.top - b.top) > TOL` is not transitive and Lua's `table.sort`
      raises `invalid order function for sorting` on a large enough shuffled input — a hard
      error, on a capture path, at a frame count nobody tested. Rounding to a whole unit is
      transitive by construction, and row pitch is at least 51 panel units at any size cap draws.
    - **`Catalog.Check` now refuses a roster the panel cannot hold**, counting **non-virtual**
      entries and validating the **partition** rather than the total — a break authored late runs
      the first row past the edge even when the roster fits. It reads `cols`/`rows` from the
      tokens and never a literal, so widening the row stays a `render-tokens.json` edit.
      ⚠ **It is an authoring tripwire, not a safety net:** `Anchor.Plan` appends every viewer row
      the catalog does not name, so a player enabling one extra ability in the Essential viewer
      can overflow a catalog that passes — from outside the catalog's control. The column clamp
      is what holds at runtime.
    - **Havoc DECLARES twelve entries against twelve cells.** That is the authoring bound, not a
      statement about what a given player's row draws — what they draw is their Essential-viewer
      layout, clamped at runtime and reported as `over:<n>`. One more authored entry needs a wider
      panel (`cols` is a catalog key or a token, so 7x2 is a data edit and shrinking `icon_px`
      holds the screen width), not a code change.
    - **FLOWN — both halves, twice.** What the tests could not reach was that the second row
      draws where the arithmetic says, and that parked frames stay out of the reading sort.
      A reported week of play on Havoc (2026-08-31) covered the first: at twelve entries against
      six columns the column clamp wrapped the row, so the second line was on screen throughout.
      The v0.23.1 flights (2026-09-01) then measured both — `X{ok}` with `P{}` and `D{}` agreeing
      **including the `|` in the same place** on three specs, and `parked:3` with `D{}` carrying
      exactly the eight planned ids. Parked frames sit `+10000` ABOVE the panel and the sort is
      top-descending, so a leak would have put them **first**; they are absent instead.
      `X{MISMATCH}` with matching ids either side of a differing `|` remains the standing signal,
      so the check keeps its subject. Details in *What the second flight settled* below.
  - **The panel's grid resolves in three tiers — player, catalog, token** (2026-08-31), which is
    `spec.md` §3.9's ninth property. `cols`, `rows` and `icon_px` are ONE setting with three
    fields; `/cap grid` reads it back, says which tier each number came from, and sets the
    player's; `/cap grid reset` drops that tier back to whatever the catalog proposes.
    - ⚠ **This closed a defect Phase 2 shipped with, found by asking what happens when a break
      puts more than six on a row.** The answer was: cap drew a **third row, outside the
      panel** — `Anchor.Cells` wrapped at `cols` but never saw `rows`, so it structurally could
      not clamp, and a test written the same day asserted the third row as expected behaviour.
      It was not a regression: before Phase 2 an over-long roster ran off the RIGHT edge, so
      overflow-outside-the-rect is as old as the panel. Phase 2 rotated it and made it rarer.
      **The reason it matters more now is Phase 3:** the panel's rect is what other UI anchors
      to, and icons outside it make that rect a lie.
    - **An icon with no cell is held off the row**, counted as `over:<n>` in the anchor capture,
      beside `parked:<n>` and deliberately not merged with it. The two have different causes and
      different fixes: a parked icon is one cap can no longer place in the order, an overflowed
      one is still in the order and merely has nowhere to go — and the fix for it belongs to the
      player. Merging them would repeat what `norow` does wrong (`Bind.lua:242`).
    - ⚠ **Overflowed frames stay in `P.tracked` and had to be kept out of the reading sort.**
      They sit at the park offset, `+10000` above the panel, and `ReadOrder` sorts on top
      descending — so ONE overflowed frame would have sorted ahead of everything and been read
      as the entire first row. `Drawn` judges position over the placed frames only and identity
      over all of them. This is the same trap the parked frames are exposed to, arrived at from
      the other direction.
    - **Keyed on spec AND hero tree, not on the character**, because what the grid has to fit is
      a roster and a roster is chosen by the catalog — Fel-Scarred and Aldrachi Reaver are two
      different lengths on one character. Per-character would size every spec for the longest
      one; per-account would do it across every character. It lives in `ns.cdb` beside
      placement, on Place.lua's reasoning.
    - **Validated on READ, not only on write.** Saved variables are a file a player can edit and
      a build can roll back into, so a stored string or an out-of-range number falls back to the
      token rather than propagating into geometry. `cell_px` and `gap_px` are deliberately NOT
      settable: `cell_px` is floored at the item template's own 50 and a narrower cell overlaps
      its neighbour in panel units — shrinking icons is `icon_px`'s job, and exposing both would
      be two knobs for one outcome, one of which silently draws icons on top of each other.
    - **A CATALOG MAY DECLARE ITS OWN GRID**, `grid = { cols = <n>, rows = <n> }`, validated in
      `Catalog.Check` and emitted by `capart export catalog`. It sits between the player and the
      token: the catalog knows how long its roster is, so a spec needing seven columns ships that
      way and a fresh install draws it; the player still wins, because they set theirs
      deliberately and a catalog update must not silently move a row they placed.
      - ⚠ **`icon_px` is refused BY NAME, with a message pointing at `/cap grid`.** The line is
        *fit* against *taste*: cell counts fit a roster and are the author's; icon size is a
        preference and is the player's. An author-settable icon size would re-open one level up
        the authority inversion the icon-size bullet below closes.
      - ⚠ **The bounds are ONE list.** `Catalog.GridLimits` is the only copy and `Anchor.Limits`
        aliases it, so the author's numbers and the player's are judged the same. It lives in
        `Catalog.lua` because `tests/check_catalog.lua` loads that file without `Anchor.lua`,
        which builds a frame at file scope. Two lists that agreed today would drift the first
        time a ceiling moved.
      - **Validated on read in `Anchor.lua` too**, on the same reasoning the player's store is:
        `Catalog.Register` asserts only the spec id, so a shape the validator would have refused
        must fall back to the token rather than reach the geometry.
    - **`Catalog.Check` measures against the panel the catalog SHIPS.** Its capacity and split
      checks read `cat.grid` where the catalog declares one and the token where it does not —
      the same order `Anchor.Grid` resolves in, minus the player tier a static check cannot see.
      So it answers "does this catalog fit the panel it ships with", which is the authoring
      question and the right one at author time. The runtime clamp is what holds for a player.
    - **Not yet flown.** What the tests cannot reach: that `/cap grid` re-draws without a
      re-arm, that a spec swap picks up that spec's own grid, and that overflowed icons actually
      leave the row rather than stacking at its corner. `over:<n>` in the capture should be 0
      unless the grid is genuinely too small.
    - **@pending Phase 3** — a grid change resizes the panel without a `SetSize` any mover has
      hooked, which is exactly the case `EllesmereUI.NotifyElementResized` exists for (step 25).
      `regrid` is where that call goes.
    - ⚠ **A `viewer` FIELD MUST NOT BE BUILT, and the capacity count is not an over-count**
      (settled 2026-09-01, reversing what this entry said on 2026-08-31). Essential vs Utility is
      **the player's layout, not a property of the spell**: the two viewer mixins are the same
      code twice, the two item mixins are bare aliases, the two item templates differ in four
      cosmetic values, and the drag table permits Essential ⇄ Utility ⇄ HiddenActive freely while
      `GetCooldownCategoryChangeStatus` declines to police it at all — four Tier-1 12.1.0 facts
      now written up under `knowledge/addon-dev/cooldown-manager.md` §1.1, which already said
      *classify on family, not on category*. A `viewer` field would encode a user setting as
      authored data and be wrong the moment the player dragged the row. So `Catalog.Check`
      counting every declared non-virtual entry is **correct**: it is an authoring-time upper
      bound against the panel the catalog ships, and what holds for a real player is
      `Anchor.Cells`' clamp and `over:<n>`. Devourer's `vengeful_retreat` in the Utility viewer is
      a **setup instruction** — the drag into Essential is legal and is the player's to make — so
      it is a line in the docs, not a field. `Catalog.lua`'s comment has been rewritten to say so.
      ⚠ Do not re-derive placement from `wowkb.spec_inventory`'s `Blizz cat` column either: it is
      the DB2 default and reads convincingly like an answer.
    - **Havoc's break is a choice again, because the grid is authorable.** At 6 columns the
      partition rule admits exactly one index for a 12-entry roster — 7, `immolation_aura` — so
      the break was arithmetic rather than a decision. A catalog declaring `cols = 7` makes
      `blade_dance` (5 + 7) legal too, and a 13th entry costs a cell rather than costing Havoc
      the ability to carry a break at all. Which of the two reads better is a question for the
      panel on screen, not for the partition rule.

  - **The four breaks are authored** (2026-09-01) — the mechanism has existed since v0.20.0 and
    no catalog used it, which meant the one thing three releases have been waiting to fly, *does
    the break hold across a talent change that removes the break entry*, could not be exercised
    by any build. One key per catalog closed it. All four are **clean cuts** — no
    reordering, no cue changes, no scenario churn, and reverting one is the same edit backwards:

    | Spec | Placed | `break_before` | Split |
    | --- | --- | --- | --- |
    | Retribution | 9 | `templars_verdict` | 4 + 5 |
    | Demonology | 9 | `implosion` | 5 + 4 |
    | Protection | 9 | `avengers_shield` | 4 + 5 |
    | Havoc | 12 | `blade_dance` | 5 + 7, on an authored `grid = { cols = 7 }` |

    A cut is legal by construction — it preserves whatever order the catalog already authored, so
    it cannot introduce a contradiction with the APL that was not already there. ⚠ **That is
    weaker than "the entry order IS the flattened `actions.default`", which is what this entry
    claimed on the day and is FALSE for at least two specs**: Havoc's `vengeful_retreat` is entry 1
    at rung 5 and Retribution puts `templars_verdict` (rung 54) above `divine_storm` (rung 53).
    The flatten is the starting point a catalog is authored from, not an invariant it holds.
    Devourer (6 placed + 1 virtual) and Destruction (1 shipped entry) still fit one row and get no
    break.
    - ⚠ **HAVOC IS THE SPEC THAT NEEDED A WIDER PANEL, and shipping it at six cost a day.**
      `cap-conscience` over v0.22.0 caught it and it verifies against the APL: at six columns a
      12-entry roster admits **exactly one** break index, and that index put **`blade_dance` —
      `actions.default` rung 19, a 9-second rotational press — on the TOP row**, while
      **`immolation_aura`, whose highest rung is 2, above Metamorphosis**
      (`knowledge/classes/demon-hunter/havoc/simc-apl.md:40-41`), headed the bottom one. Backwards
      on both sides. The cut was **forced by arithmetic and then described as though it had been
      chosen**, and the description is what was wrong — the mechanism did what it was asked.
      Corrected 2026-09-01 to `grid = { cols = 7 }` + `break_before = blade_dance` (5 + 7), which
      is clean: five cooldowns over seven rotation presses.
      ⚠ **The general lesson is that a forced choice is not a validated one.** Havoc was the only
      spec where the partition rule left no freedom, and that is precisely why it was the one
      nobody checked — there was nothing to deliberate, so the result went unexamined. When an
      authoring decision has exactly one legal answer, that is the moment to ask whether the
      CONSTRAINT is right, not to record the answer as a choice.
    - ⚠ **Protection's `shield_of_the_righteous` rides the TOP row and that is correct.** It sits
      at index 3, between two cooldowns, and an earlier pass called that a wart to fix by
      reordering. SotR is **rung 9** of the Tier-1 APL, above `avengers_shield` (13/18),
      `consecration` (15/19/24/29) and `judgment` (16/17/22) — the catalog's order matches
      `actions.default` exactly, and moving it down would put a rung-9 action beneath rung-13
      ones. **So the top row means "outranks the rotation", not "on a timer"**, and Protection is
      the spec that makes the distinction visible: SotR is a charged, held, active-mitigation
      press that genuinely outranks the filler. The three further costs of a reorder are in
      `specs/archive/ellesmere-mover-plan-2026-09-01.md` §2.5c.
    - **Havoc's index was forced, not chosen.** At 6 columns a 12-entry roster admits exactly one
      break index. `grid = { cols = 7 }` + `blade_dance` (5 + 7) is now legal and may read better;
      that is a question for the panel on screen, per the bullet above.
    - **Authored through the JSON, never the Lua.** `specs/<spec>/catalog.json` →
      `capart export catalog <spec>` → `capart build --all` → `capart check --all`; the
      `catalog_gate_lua` byte-compare is what makes hand-editing `Catalogs/<Spec>.lua` fail.
    - **Released as v0.22.0** (2026-09-01) to be flown. Its notes carry the CONSOLIDATED
      acceptance set — three releases' worth of unread questions in one list, item 3 of which
      is the break fallthrough. **Not yet flown:** no client has drawn any of them.

  - **The row is registered with EllesmereUI's mover** (2026-09-01) — the thing eight phases of
    panel work existed to make possible, and the first time anything outside cap can anchor to
    `CombatAssistPlusRow`. `Ellesmere.lua` registers one element, `CAP_ROW`, entirely behind
    `_G.EllesmereUI` plus `## OptionalDeps: EllesmereUI`; with the host absent the file loads and
    does nothing. It declares `noResize` and **nothing else** — `noAnchorTarget` and
    `noAnchorTo` are what would remove the point, so `ellesmere_spec` asserts their absence.
    The foreign surface it speaks to is `knowledge/addon-dev/cdm-rider-patterns.md` §4.8, read
    off a 9.1.3 live install.
    - **One store, two doors.** `savePos`/`loadPos`/`clearPos`/`applyPos` delegate to the same
      `Place` handle `/cap move` drags, so a mover drop and a cap drag write the same number and
      neither can be stale against the other. The host normalises to CENTER/CENTER before it
      delegates, which is already `Place`'s persisted shape, so nothing converts anything.
      ⚠ Omitting the delegates was the silent failure available here: the host's fallback is the
      EllesmereUIActionBars profile table, so every drag would have been written somewhere cap
      never reads.
    - ⚠ **`getSize` is read in UIParent's units and `Anchor.GridSize` is in the panel's.** The
      panel wears `icon_px / 50` as its scale, so the unscaled number would size the mover — and
      every geometry the host derives from it — wrongly at every icon size but one. Asserted.
    - ⚠ **`SetScale` is why `Anchor` notifies at all.** The registration installs its own
      `OnSizeChanged` and `SetPoint` hooks, so an ordinary resize or move already cascades to
      anchored children with no help; what it cannot see is a panel that kept its width in its
      own units and now covers more screen. `resizeAnchor` and `regrid` call
      `EllesmereUI.NotifyElementResized`, and `regrid` calls it **unarmed too** — `/cap grid` is
      legal with cap drawing nothing, and a mover anchored to an unarmed panel is anchored to a
      rect that just moved.
    - ⚠ **Registration is at `PLAYER_LOGIN` with a deferred re-drive, because the host's login
      timing is CONDITIONAL.** Its `PLAYER_ENTERING_WORLD + 1 s` listener exists only when
      EllesmereUIActionBars is *absent*; with it installed the apply runs from that addon's own
      hooks instead. Rather than pick a branch, the bridge re-drives `ReapplyOwnAnchor` and
      `ReapplyAllUnlockAnchors` a second after registering, which makes the branch moot — a
      child whose target could not be resolved when the pass ran was skipped and nothing
      re-drives it on its own.
    - **FLOWN TWICE 2026-09-01. The first flight found a defect the registration created; the
      second reached the goal.** ⚠ **The bars hold against the row across a reload, a spec swap
      and a `/cap grid` change** — which is the thing eight phases of panel work existed to
      make possible, and it is now done. The defect is the entry below; what the second flight
      settled is the entry after it.

  - **The auditor measures the icons against the panel, not against the screen** (2026-09-01,
    v0.23.1) — the fix for what the first flight of the mover element found. **v0.23.0 opened
    the contention dialog against nobody and re-applied the row twice a second for as long as
    it was armed.**
    - **What the capture said**, and it is the whole diagnosis: `stomp:0` (Blizzard's layout
      never ran), `reassert:0` (nothing called `SetPoint` on an icon — not Blizzard, not the
      host), `contended:9` with `# displaced n=11` at every 0.5 s sample, and **`X{ok}`
      throughout**. Right order, wrong frame of reference: the icons were correct *relative to
      the panel* and wrong *relative to the screen*, and the only thing those two share is the
      panel.
    - **The mechanism.** `want` carried an ABSOLUTE coordinate, `anchor:GetLeft() + c.x`, read
      one line after `Place:Apply()` may have moved the panel — and a `SetPoint` does not
      update the rect, so the read could answer with where the panel *was*. Idempotent while
      cap was the only writer, which is why it survived to here; **registering with a mover is
      what gave the frame a second writer**, and the stale read then locked the delta in
      permanently, because every "re-apply" recomputed the same wrong number.
    - ⚠ **The fix does not depend on which sub-cause it was.** Whether the panel disagreed
      because of the stale rect or because the host was re-placing it, the answer is the same
      and it removes the class: `want` carries the panel-relative offset only, and the sampler
      reads the panel's origin **at the moment it looks**. A panel that moves is no longer
      displacement, which is correct — the icons are anchored to it and are supposed to travel
      with it. The row's `onPlaced` reschedule went with it: a drag now invalidates nothing.
    - ⚠ **The client fact underneath is NOT measured.** `knowledge/addon-dev/`
      `frames-textures-animation.md` §3.7 carries it hedged and `@verify-ingame`, corroborated
      by a shipping addon's own source comment rather than by us. Nothing in cap depends on it
      any more — the read was deleted, not worked around.
    - ⚠ **The instrument could not have told you.** The auditor records every icon's absolute
      position and never the panel's, so a panel move and eleven icon moves are the same line.
      That is why `# contended` named a stranger that did not exist.

  - **Protection ships `grid = { cols = 7, rows = 2 }`** (2026-09-01) — because **its own fold
    cost it an icon on a real character.** Folding before the fifth entry ends the first row
    *there*, so the two cells past it cannot be reached: at six columns the panel held **ten**,
    and a measured roster of **eleven** — nine authored plus two the player had enabled in the
    Essential viewer — dropped one off the row. On v0.21.0, before any break existed, the same
    eleven fit as 6&nbsp;+&nbsp;5 with `over:0`.
    - ⚠ **A FOLD AND A PANEL WIDTH ARE ONE DECISION, and `Catalog.Check` cannot see the whole
      of it.** It measures the catalog's own roster against the catalog's own grid, which is an
      authoring-time upper bound and correct as far as it goes — but a player's roster is the
      authored entries **plus every extra they enabled**, extras land in the tail, and the
      authoring gate has no way to know. Havoc bought seven columns for a twelve-entry roster;
      Protection needed them for a nine-entry one, and the difference is entirely the fold.
    - **`/cap grid` was reporting `cols × rows` as capacity, which a fold makes false.** It told
      the player the row holds twelve while cap held an icon off it for want of a cell. It now
      names the fold and reports what can be reached, asked of `Anchor.Cells` — the same
      function that lays the row out, so the two cannot drift. Four tests pin the arithmetic.

  - **What the second flight settled** (2026-09-01, v0.23.1, four sessions across Retribution,
    Protection and Havoc). Read `raw/cap-anchor.log`; every header says `contended:0`.
    - **The loop is gone and the healthy signature is there instead.** `disp:0 cont:0` in every
      session, while `reassert` climbs to 11 and 12 — Blizzard's layout moved the frames and cap
      answered inside the same call, which is what a working rider looks like. Not the absence
      of a symptom: the presence of the right one.
    - **The reading sort is proven** — every `# reapply` reads `X{ok}` with `P{}` and `D{}`
      agreeing **including the `|` in the same place**, on three different specs. (`# armed`
      reads `X{MISMATCH}` before placing, which is Blizzard's own order and expected.)
    - **`/cap grid` re-draws without a re-arm** — three consecutive `# reapply why=grid` with no
      `# armed` between them.
    - **A spec swap picks up that spec's own grid AND its own break**, live and mid-session:
      Retribution folded 4+4, Protection 4+7, Havoc 5+4, each through
      `# stale` → `# rearmed why=RefreshLayout` → `X{ok}`.
    - **The catalog tier reached a real client for the first time.** Protection drew **4+7**,
      which is only possible on the seven columns its catalog declares. **That closes the tier
      question**: Havoc's own `7 (catalog)` readback is another instance of a shape already
      proven, and a manual flight tests the shape, not every instance of it.
    - **Protection's `over:` is 0** where the same character read `over:1` an hour earlier. The
      wider panel did what it was widened for.
    - **Parked frames stay out of the reading sort** — `parked:3` with `D{}` carrying exactly
      the eight planned ids. They sit `+10000` ABOVE the panel, so under a top-descending sort
      a leak would have put them **first**; they are absent instead.
    - ➖ Not exercised: the forced overflow case (`/cap grid 3 1` → `over:6`). The ordinary-play
      half of it is answered.

  - ⚠ **"Does the break hold across a talent change that removes the break entry" WAS NEVER A
    FLIGHT ITEM, and calling it *the oldest debt in the project* was wrong** (retired
    2026-09-01). `Anchor.Plan` is pure and `anchor_spec` has covered the fallthrough since
    Phase 2 — *"the nominal talent change: the break entry is not talented this build"*, plus
    the case where nothing from the break onward survives. The item was carried across three
    releases because a plan document kept restating it, and nobody re-read the tests.
    - **What the client half would have added is already proven.** A talent change and a spec
      swap reach the same handler by different events, and flight 2 exercised the
      roster-changed path three times: `# stale` → `# rearmed why=RefreshLayout` → `X{ok}`.
    - ⚠ **AND THE PREDICTION IN THE FLIGHT NOTES WAS WRONG, which is the actual lesson.** It
      said a removed break entry drops the fold back to the column clamp — Demonology folding
      6&nbsp;+&nbsp;2. It does not: `Anchor.lua`'s resolution walks the plan for the first entry
      whose AUTHORED position is at or after the break, so **the break slides to the next
      surviving entry** and Demonology folds 5&nbsp;+&nbsp;3. Reading the code answered in a
      minute what the flight was being held open for, and answered it correctly.
    - **A test now pins the case the other two missed**: the break entry absent on a roster long
      enough that the column clamp is a plausible outcome, which is the shape that made the
      wrong prediction sound reasonable.
    - **The rule this leaves:** an item belongs on a flight card when the CLIENT is the only
      thing that can answer it. A pure function's behaviour under a roster change is not that,
      whoever wrote it down.

  - ⚠ **`wowkb.capture` was reading the wrong file, and had been since cap gained a
    per-character store** (fixed 2026-09-01). cap declares both `## SavedVariables` and
    `## SavedVariablesPerCharacter`, so `CombatAssistPlus.lua` exists in two layouts and only
    the account-wide one holds `CombatAssistPlusDB`. The reader took the newest by mtime, both
    flush on the same `/reload`, and the tie went to the file with no captures in it — **a
    92-line session read as "no captures on disk."** It now takes the newest file that actually
    carries the global. The same trap is live for any addon that declares both.

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
    section owns every unmeasured Havoc fact.
  - The Havoc design lives in three files — `catalog.md` (the definition),
    `scenarios.md` (the walk), `fact-classification.md` (the safety case) — which is the
    **model every spec follows** (`authoring.md` §0, revised 2026-08-19).
- **The Havoc row flew once, 2026-08-15** (cap v0.4.0, Fel-Scarred, on EllesmereUI), against the
  pre-APL catalog. Its structural finding — the reading model assumes the CDM's row order matches
  the authored priority — is what `Anchor.lua` was built to answer.
- **Demonology / Diabolist is BUILT** (2026-08-22). `Catalogs/Demonology.lua`
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
  **one-entry** proof and **not** what `specs/**` now says. ⚠ It was called a *"two-entry proof"*
  here until 2026-09-01 and it never was one: the pilot declares **two abilities** (`conflagrate`,
  `backdraft`) and **one entry** (`conflagrate`, carrying the Backdraft count band). Backdraft is an
  aura dependency that never enters `Signal`, which is exactly why it is not an entry.
  ⚠ **That is the one place left in the project where a shipped catalog and its document
  disagree**, and it is deliberate — `authoring.md` stage 6 has not run for it. Do not read the
  `.lua` as the design. It wants the same count primitive for Backdraft that Demonology now uses,
  which is now a transcription rather than a promotion.
  - ⚠ **It is now the ONE authored spec with no `catalog.json`, and that is a finding rather
    than a not-yet** (2026-08-25; recounted 2026-08-27). Devourer was the other one until it was
    transcribed on 2026-08-27 — its blocker was V12, and V12 is built — so the contrast this
    bullet used to draw is gone and Destruction stands alone. **Destruction** was attempted, and
    the scenario↔state gate refused it — **five scenarios, three cues**. `DES-1` draws Conflagrate
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
  - `authoring.md` stage 8 has not run on it, in either form.
- **Retribution / Templar is authored and transcribed.** Three files
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
- **Protection / Lightsmith is authored and transcribed.** Three files
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
- **Devourer is transcribed, and the one attempt to fly it saw nothing.** `Catalogs/Devourer.lua`
  is generated from `catalog.json` and loads. ⚠ **That is NOT the same as drawing**, and the
  2026-08-31 report is the correction: the author was on the spec and *"it didn't show up at all."*
  Whether the catalog failed to bind, the panel drew empty, or no row was ever in a drawable state
  is unestablished, and the thread is parked at the author's direction (`## Now`). It is the first spec whose definition needed **V12's virtual row**, and after
  2026-08-27 it needs exactly **one**: Consume, `standing`. Collapsing Star was measured in game to
  be a spell **override** on the Void Metamorphosis row, so R7 draws it and it is not cap-owned at
  all — which means V12's **`gated` kind has no consumer anywhere**, built and tested and
  unexercised. **The preview** was registered in `SPECS_BUILT` on 2026-08-19 and now carries
  **11** scenarios (B-1…B-5 build phase, M-1…M-5 window phase, DEV-11 the Utility row), and is the
  first page any spec has drawn a virtual row on. Two things about it are deliberate and should not be read as settled work:
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

- **~~A DEFEAT is invisible on the preview~~ — SHIPPED 2026-08-27.** Numbered items under
  `## Defeats` are parsed from `catalog.md`, rendered on every spec page that has a section, and
  referenced per-entry by `catalog.json`'s `defeat`, so a reader of a row sees that this row is
  where cap gives up. Gated both ways by `catalog_gate_defeats`, with a declared
  `defeats_unreferenced` escape whose `why` is required — a bare number list would be a category
  exemption. `defeat` does **not** travel to the addon (it cites a rung the client is never told
  about), and `check_capart_catalog_lua` asserts that non-travel so the obvious wrong move fails a
  test. Rendering keys off `catalog.md`, so **Destruction gets its five despite having no
  `catalog.json`**. Now reaching the page: Protection 8/8, Demonology 5/5, Destruction 5/5.
  ⚠ **The counts this entry originally carried — Protection 47, Demonology 15, Destruction 10 —
  were `grep` mentions of "Defeats, item N" across each spec's tree, not authored items.** The
  numbered items are 8, 5 and 5. The invisibility was real and the measurement of it was not.

- **Havoc and Retribution have no numbered `## Defeats` section at all**, and argue their defeats
  in running prose instead — so they are structurally unable to carry any of the above, and their
  pages render no defeats block. Recorded 2026-08-27, when the machinery landed and made the
  asymmetry visible rather than merely present. Converting the prose to numbered items is a real
  and small slice; what it buys is that the two specs closest to shipping stop being the two whose
  giving-up is invisible.

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
    was not migrated**: Destruction was attempted and refused by the scenario↔state gate (measured
    above). Devourer **is migrated** as of 2026-08-27 — V12 became a `primitive` when it was built,
    which is what `drawn_by` needs, and the second of the two rows the blocker named turned out to
    be an override rather than a virtual row at all.
  - **Seven catalog gates**, applied to any spec that has a `catalog.json` and skipped by absence,
    so the remaining rollout needs no second list: Lua byte-compare, marker↔state,
    closed vocabulary, scenario↔state, co-occurrence, **outranker readiness**, and validator
    parity (`Catalog.Check` run outside the client by `tests/check_catalog.lua`). **Every one has
    been seen to fail by name** on every migrated spec — a gate never watched failing is not known
    to work.
  - **The outranker gate shipped HARD, not as a warning** (2026-08-26,
    `capart.catalog_gate_outranker`). It exists for the four Pattern-A defects fixed that day: a
    hold names the row it yields to and never checks that row is AVAILABLE, so it ELIMINATES the
    correct press whenever the outranker cannot go. ⚠ **It was authored to parse the marker's
    prose and does not** — prose was the wrong subject and would have made it a noisy gate, which
    is worse than none, because a gate people bypass trains them to bypass gates. It judges
    against Tier-1 data instead: the hold state's `apl` citation → the upstream rung's action
    (`apl_line`) → `catalog.md`'s own *Bound abilities* table → a roster row. If that row is not
    the entry's own, some term across the state's markers must name it. **Measured before it was
    wired in: zero findings on all four migrated catalogs, and exactly the three pre-fix
    Protection states when the two fixes were reverted.** It abstains in four places rather than
    guess — an `exception` state, an unresolvable citation, a directive rung, an action with no
    roster row — and each abstention is a thing it cannot catch rather than a thing it approves.
    ⚠ It is scoped to holds that yield to a **different** row, so it does not catch the other two
    Pattern-A shapes: a hold that is derived from one rung of a **two-life** row and does not say
    which life (Demonology's two window holds, fixed with `identity(hand_of_guldan, "base")`),
    and a promotion that carries its rung's condition but not its rung's **reachability**
    (Retribution's `boj_opener`, split into two markers). Both cite the entry's own rung, so the
    gate abstains by design.
  - ⚠ **The scenario↔state gate matches on a `(verdict, cues, sealed)` TRIPLE, and two states on
    one entry can share one.** Since 2026-08-26 Demonology's `hand_of_guldan` carries both
    `hog_ruination` (rung 10, Ruination armed) and `hog_press` (rung 11, the ordinary spend), and
    both are `(open, {}, {})` — the first place in any catalog where the gate cannot tell two
    states of one entry apart. **This is structural, not a break, and the next person to hit it
    should not go looking for what they did wrong.** The gate's question is *"does anything on
    this entry draw what the walk drew"*, and two states that draw identically are by construction
    one answer. **What it costs:** DEM-16 proves that *a* state on that entry renders as a clean
    open row; it does not prove the state the walk is arguing about, which is the transformed
    life. The rung citation, the walk prose and the outranker gate carry that, and the triple does
    not. This is the sharp form of `cap-review-todo.md` §3's standing note that a scenario proves
    a rendering rather than a rule. **No fix attempted**: making the gate match on state ID would
    mean every scenario row naming a state, which is a scenario-format change with a much larger
    blast radius than the thing it would catch.
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

- **A sealed display may draw a fact its own rung citation does not contain, and nothing checks.**
  Measured 2026-08-27, out of Retribution's Light's Deliverance band. Every state must already say
  where it comes from — an `apl` citation or an `exception` — and the states gate confirms the
  citation **resolves**. It does not confirm the cited rung is *about* the fact being drawn.
  `woa_ld_armed` cited `generators 3`, which resolves cleanly; `generators 3` is the Wake of Ashes
  rung and `lights_deliverance` appears **zero times in the whole priority list**. The band drew a
  fact its own provenance did not contain, and was deleted for exactly that reason (2026-08-27) —
  the APL reads only the *result*, `buff.hammer_of_light_free.up` at `finishers` 2.
  **The gate:** for a marker carrying a `display`, the display's subject must appear in a rung the
  entry cites, or the marker must declare why not.
  ⚠ **Dry-run measured before writing this, and it is MEDIUM, not the one-liner it looks like.**
  Across the four migrated catalogs **27 of 32 display markers resolve**. Of the five that do not:
  **one is a real find** — `demonology/ib_art_clock` draws `art_mother_of_chaos`, which occurs **0
  times** in the Demonology APL, off rungs `diabolist 15`/`16` that are bare actions with no
  conditions. That is the Light's Deliverance shape exactly, though it is a V20 clock rather than a
  positive count and so makes no press claim — it needs a ruling, not an assumption.
  **One needs a human** — `protection/cons_awaits_hammer` draws `divine_guidance`, which IS in the
  Protection APL but not in any of the three rungs that entry cites.
  **Three are the gate's own problem** — `protection/cons_field_up` fails only because the catalog
  id is `consecration_up` where the APL token is `consecration`, and Havoc's `felblade_overcap` /
  `demons_bite_overcap` carry **no aura subject at all** (they read `UnitPower`, not an application
  count).
  So it needs two things it does not have: skip subject-less displays, and a **catalog-id → APL-token
  map**. `catalog_gate_outranker` already builds a map like that from `catalog.md`'s *Bound
  abilities* table — but that table maps ACTIONS, and these subjects are AURAS (`buff.X` / `dot.X`),
  so it likely does not cover them. Budget a mapping table, not a predicate.

## Batches

**The scarce resource in this project is trips into the game client, not gates.** `capart check
--all` runs over every spec in seconds, a `cap` release is pre-authorized (`CLAUDE.md` §
Releasing), and a doc edit costs nothing but the writing. **A flight costs a week of play.** So the
work below carves into six batches by *what each item needs*, and an item's batch is decided by
its most expensive requirement — not by its subject. Two items about the same cue can land in
different batches; two items about nothing in common can share one.

- **Batch A — paper.** No catalog data, no addon Lua, no release, no flight, no lab deploy. Doc
  edits, sweeps, archive moves and recorded decisions. Costs one `capart check --all` and one
  commit, so the items are batched purely to save the *ceremony*, not any real resource.
- **Batch B — gates and tooling.** Changes to `wowkb.capart` itself: new or loosened `check`
  assertions, the doc↔sidecar comparison, the preview builder. Needs a green `check --all` over
  every spec and nothing else. ⚠ **This is also where tooling-only work goes that the other five
  constraints have no name for** — the carve-up is by data / Lua / release / flight / lab, and a
  `capart.py` change is none of those. It is B by default.
- **Batch C — catalog data.** `catalog.md` + `scenarios.md` + `catalog.json` + `Catalogs/<Spec>.lua`
  moving together, because a re-rank or a new marker is not a document edit — the row order is the
  APL's rung order and `Anchor.lua` draws it. Ends in a build and a `check`.
- **Batch D — addon Lua.** Engine-side changes: predicates, `Sense`/`Signal`/`Treatment`/`Paint`,
  capture strings, module removals. C and D share **one release cut** because a release is per
  addon, not per change.
- **Batch E — ClientLab.** Anything that needs an unknown measured in a live client through the
  scratch lab: one `projects/addon-lab/` deploy carries every open test at once, so an item that
  needs a measurement waits for the next deploy rather than earning its own.
- **Batch F — flights.** Per spec, and **not** batchable across specs the way the others are: a
  flight is a week of playing *one* spec, and questions about a spec you are not playing get no
  answer from it.

⚠ **The attribution rule for a batched flight, which is the one thing batching can genuinely get
wrong.** When a release carries several changes into one week of play, **a week of no complaint is
not a positive report on any of them.** It is one report on the whole build, and it says only that
nothing was bad enough to mention. The square-dial defect flew for a week under exactly that
reading. So a flight settles a question only where the report *names* the thing — a question no
observation names comes back **unexercised**, not passed, and stays in its batch.

## Now

### The folded row's fold gates → `backlog/fold-reading-model.md`

**The reading model is DECIDED and the decision is in `render-shelf.md` Part 0.5: a folded row
reads like a book** — the whole top line, then the whole bottom line, one walk, priority order
continuing across the break. Author's call, 2026-09-01, from play. The rejected alternative was
the bottom row being *the* scan with the top as a shelf, which would have made Part 0.5 two
procedures. `discussion.md`'s question is deleted per its charter.

**Both shipped bets survive unedited**, which is why the call was worth taking deliberately:
Retribution's interleave badge still walks past Divine Toll, and Protection's **absent** `overcap`
cue is still justified because the walk still reaches the four generators after Shield of the
Righteous. A missing cue is invisible, so the other answer would have broken that one quietly.

⚠ **The origin of the break is now recorded, and it was nowhere before**: several specs' CDM rows
were getting awkwardly wide, raised during the EllesmereUI anchoring work. It is a width fix
first; the top-cooldowns/bottom-rotation meaning came after and is binding on future breaks.

**What is left is the expensive half — no gate models the fold.** `break_before` appears in
`capart.py` exactly once (line 1330, emission) and nothing reads it, so `capart check --all` green
says nothing about the fold. The plan file holds the call sites; the trap worth repeating here is
`density_gate`'s literal prefix slice `sc["row"][:press]`, which counts skips across a row
boundary that the eye now crosses in a defined way. `scenarios.json` is a second producer, and the
break has to travel from `catalog.json` into the scenario grammar or be re-authored there.

⚠ **One residual the decision did not answer**, and it only shows up in play: the break sits
directly in front of a gold positive cue in two specs (Demonology's `implosion`, Havoc's
`immolation_aura`). Pass 1 is meant to make position irrelevant — does heading its own row help
that cue or hurt it? Not blocking; fold it into the next Demonology or Havoc session.

### The hatch is paid on every scan — promoted out of the Protection flight

**This is Protection flight finding 4 raised to its real scope, not a new item.** It was recorded
as one bright icon — *"Sentinel is such a bright icon that even dimmed a bit with a hatch it's
still sort of asking to be clicked"* — which reads as a treatment tweak for a rare case. It is
not.

**The author's second report, 2026-09-01, is structural.** *"the cap spec implementations I use so
far seem to have the property of having some long running cooldowns at the start, because they're
high priority, that sit at the far left on cooldown or red much of the time. They're easy to see
when I need them, but I'm always paying the scan tax when I don't."* Under the fold decision above
the top line is walked **first, on every scan**, and by the fold's own meaning it is the cooldowns
— the icons that are eliminated most of the time. So V11's hatch is no longer occasionally tested
by a bright icon; it is the thing standing between the reader and the press on every single read,
on all four specs that fold.

**Demoting the cooldowns is not the fix and the author already ruled it out**: *"Trying to put
them on the first row means suddenly rotational, lower priority items outside of cooldown windows
don't exist way off in no man's land."* Both orders strand something; the hatch has to carry it.

- [ ] **Part 5 question 7 has now answered in the direction the shelf feared** and the shelf owns
      the fix. Black at `0.50` reads as *dimmed*, not as *ruled out*, on high-value art.
- [ ] ⚠ **Not a hue.** The retired veil died of exactly that, and the blend has no headroom left.
      The shelf's own guidance is **area or a different treatment** — L4's black stripes were
      promoted to V11 for this reason and are the nearest existing move.
- [ ] Judge it against the fold: the question is no longer *"is this icon legible when hatched"*
      but *"can a reader cross a fully-hatched top line without stopping"*. Those are different
      thresholds and the second is the one that matters now.

⚠ **`backlog/protection-next.md` → *Deliberately NOT in this round* still defers it and now
points here.** Keeping the argument in two places is the drift this file complains about
elsewhere; this entry is the one home.

### Shard projection — anticipate the post-cast count → `backlog/shard-projection.md`

Demonology, three abilities, one number: while Shadow Bolt, Infernal Bolt or Hand of Gul'dan is in
flight, `world.resource` reads the count the cast will leave you at, so every shard cue already in
the catalog becomes anticipatory with no catalog edit. Nothing is sealed — Soul Shards are
never-secret — and the plan file holds the five steps, the CDMProbe traps and the
`cdm-rider-patterns.md` §9.2 correction it rests on.

### Anchor's un-hide half needs an author call

`/cap anchor rows` reports which catalog entries have no pooled frame. Making one appear means
`SetCooldownToCategory`, a write to the player's saved CDM layout, which sits against `spec.md`
§4's "does not replace or configure the Cooldown Manager" and carries an open `[gap]
@verify-ingame` for whether an un-hidden row lands in a viewer end to end. Nothing is built and
nothing should be until the boundary question is answered.

⚠ **The read-only half is flown and holds** (2026-08-31, a week of play on Havoc and
Retribution): the re-apply edges, the park, the recovery and the `# contended` counter all
behaved. What that week did NOT reach is the mid-combat destructive teardown — `UNIT_AURA` is
unfiltered by unit, so a full aura update on your target can rebuild the whole layout
(`knowledge/addon-dev/cooldown-manager.md` §4.1). It did not visibly happen; the capture is the
only thing that would say it did not happen *quietly*. Grep `# stomp RefreshLayout destructive=1
combat=1` when a capture is next read, and confirm `A{parked:0}` follows any hit — a park that
survived a destructive stomp would hide a live ability.

### The swipe says two different things and cap could make it say which

**The author's report, 2026-08-16, after hours of play and independent of cap:** *"the distinction
between I have two seconds left on Tyrant, and I have 2 seconds left until it's off cooldown is
constantly mixing me up in the chaos of combat."* This is a Cooldown Manager problem cap happens to
be able to fix, not a cap problem.

Blizzard already distinguishes them, too weakly: `ITEM_AURA_COLOR = (1, 0.95, 0.57, 0.7)` — pale
cream — versus `ITEM_COOLDOWN_COLOR = (0, 0, 0, 0.7)` — black
`[T1 src @12.1.0: CooldownViewer.lua:20-21]`. Same shape, same direction, same alpha, and the pale
one sits over bright icon art that fights it. Hue alone is losing in combat.

⚠ **The shelf amendment this needs was deliberately NOT taken in the 2026-09-01 paper round, and
that is the right call rather than an oversight.** It is a paper edit and would have batched
cleanly, but it is the **precondition of a build** — describing a reversed swipe in `render-shelf.md`
while nothing draws one puts a treatment on the shelf that no preview can render, which is exactly
what the shelf's "one treatment per primitive, no debates" rule exists to prevent. It travels with
the build, in batch C/D.

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

### `devourer`'s `voidblade_on_cd` is the same defect class, unexamined

DEM-S2's shape — a `cd` verdict on a row that will be displaying a non-swiping replacement — has
a live candidate inside the built set. Voidblade is replaced by **Hungering Slash `1239123`** for
6 s with Voidblade's own cooldown running underneath, and `voidblade_on_cd` carries the identical
boilerplate exception while gating nothing on `identity`.

- [ ] Check what the row actually draws for those 6 s, and whether the scenarios that call it
      swiped are describing a state that happens.

Retribution's Wake of Ashes row already carries identity branches and is lower risk. ⚠ The
Grimoire pair are the only abilities in the corpus whose transform driver is *the base spell's own
cooldown*; this one's driver is the post-cast window, so it is a different driver reaching the
same wrong verdict.

### Roll `shows` out to the other three catalogs' transformed states

Shipped on demonology 2026-08-28: a state may carry `"shows": "<roster name>"` so its state card
draws the face the row is actually displaying, instead of the entry's base face. The other
catalogs still draw the base face on every state, which is the same defect DEM-S2 had.

- [ ] **devourer**, 9 states — `star_short`, `star_granted_st`, `star_granted_aoe`,
      `star_yields`, `star_short_and_yields` → Collapsing Star; `cull_open` → Cull;
      `voidblade_pierce_the_veil` → Pierce the Veil; `voidblade_reapers_toll` → Reaper's Toll;
      `devour_standing` → Devour.
- [ ] **protection**, 3 — `ha_weapon_absent`, `ha_weapon_window`, `ha_weapon_healthy` →
      Sacred Weapon.
- [ ] **retribution**, 1 — `woa_starved` → Hammer of Light.

⚠ **KNOWN LIMITATION — `shows` is single-valued and cannot express a DUAL-LIFE state.**
`reap_open` (*"Reap, **or** Eradicate once banked"*), `voidblade_open`, `woa_clear` and
`judgment_clear` each describe a row that may be wearing either face. Leave them alone; forcing
one is the same class of error as drawing the base face on a transformed state.

### ~~There is no positive-cue budget — say so in the docs~~ — DONE 2026-09-01

Author's correction, 2026-08-16: **the single-positive-cue rule was being read as a budget, and it
was not one.** The docs presented it as a scarce resource, so a reader reasoned about *spending* the
positive and declined to propose one that was justified — measured twice in one session.

**The gate was the half that got fixed first** (2026-08-17/19) and the prose lagged it by two weeks.
`reading_gate` became an ordered chain, and the shipped assertion is `one_positive_per_entry` —
**per ENTRY**, not per vocabulary and not per row. `positive_gate` resolves two positives on two
different buttons the way the scan does: **leftmost wins**, failing only when the leftmost positive
is not the press.

**Five passages were rewritten on 2026-09-01, and one of them was load-bearing.**
`render-shelf.md:248` still said a second positive cue fails `check` because *"two of them in one
row makes pass 1 ambiguous"* — **false as written**, and it is the passage a reader reaches from the
gate list, so it taught the budget the paragraph six lines above it had already retired. Also fixed:
`:222`'s *row* where the gate says *entry* (row ≠ entry), `:453`, `:475`, `:647`, and `spec.md`'s
*"the one positive cue"*.

**Then the fourth checkbox — re-examine what the rule CAUSED — and it did not end in no change.**
The four positive halves parked as "pixels, not authority" were re-read against Part 0.5's new
*Rank first* rule instead of against the budget. **None of the four is still parked**, and two of
them had been decided in the catalog while `spec.md` §3.6 and the shelf went on calling them parked:

- **The "banked" Fury light — DELETED**, and for the strongest reason available: `havoc/catalog.md`
  cue B records that *"the APL puts no Fury term on Essence Break"*, so there is no rung to cite and
  nothing for a cue of **either** polarity to draw. ⚠ Not a *Rank first* outcome — banked Fury
  varies within a state and could never have been rank. The rule is silent here; the APL is not.
- **The demon-form promotion — RETIRED on content.** Its whole claim is that Annihilation outranks
  Felblade, and the anchored row order already puts them at positions 8 and 9 in both forms, so it
  would move no button. That IS *Rank first*, applied and found sufficient.
- **The green dependency dot — refuted**, and by *Rank first* exactly: a satisfied dependency is a
  statement about rank, which is why V6 was retired on 2026-08-13.
- **The weave chevron — refuted.** Off-the-GCD is a constant property of the ability, already
  carried by the `weave` verdict that the elimination gate steps over.

⚠ **The lesson is not about positives.** A parked item is a decision waiting to be taken, and two of
these had been taken elsewhere with nothing propagating the answer back. **The catalog decided and
the constitution kept describing the old state** — which is the same failure mode as a stale claim
with a correction appended under it, one file removed.

### ~~Ordering versus conditionals — ordering is cheaper to read~~ — LANDED 2026-09-01, and the Havoc audit found nothing

Author's position, 2026-08-16, correcting an equivalence stated in review: *"conditionals require
more mental energy than ordering, especially for items already mostly on the far left."*

**The rule is now `render-shelf.md` Part 0.5 → *Rank first***: *when a fact is stable enough to
express as rank, express it as rank and spend no cue on it; reserve a cue for what genuinely varies
within a state.* ⚠ **It went to Part 0.5 rather than to `spec.md` §3.1, which is where this entry
originally sent it, and that turned out to matter for a reason nobody had noticed: TWO LIVE
CITATIONS ALREADY POINTED AT PART 0.5 FOR IT.** `render-shelf.md`'s own V12 section
(*"which is Part 0.5's rule in its plainest form"*) and `devourer/catalog.md` (*"which is what
`../render-shelf.md` Part 0.5 asks for"*) both cited a rule Part 0.5 did not contain. Writing it
into `spec.md` would have left both broken and added a third home for the same idea. §3.1 now
carries **one clause citing it**, per its own *"a procedure written down twice is a procedure that
will disagree with itself."*

⚠ **The rule was written to cut both ways, which the one-line version does not.** A fact that
genuinely changes within a state *cannot* be rank — a fixed position cannot say "right now" — so
ranking it produces a row that is silently wrong half the time. Two failures, one rule: a cue doing
a rank's job costs attention on every scan; a rank doing a cue's job costs correctness. The
re-examination of the parked positives (above) turned on exactly that distinction.

**The Havoc audit ran, and it is a clean negative — no re-rank, nothing for batch C.** Counted over
the 16 authored scenarios in `havoc/scenarios.json`, the most-lit marker in the spec is Chaos
Strike's `starved` at **3 of 15 appearances (20 %)**; every other marker is at or below 18 %, and
five are single-digit. Nothing is anywhere near "lit in most states". ⚠ **State the limit with the
result:** the 16 scenarios are *authored* states chosen to exercise the catalog, not a sample of
play, so this is evidence about what the catalog claims and not about frequency in a real fight.
What it does establish is that no marker is lit in most of the states the catalog itself thinks are
worth writing down — which is the shape the rule looks for. **Reopening condition:** a flight
report naming a row that reads as permanently badged. Retribution already produced one of those
(*Say WHY a row is hatched* in `## Ideas`), and it was three rows reading permanently red — the
same complaint from the other end.

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

### Devourer drew nothing

**The flight ran** — a week of play on **Havoc and Retribution**, reported 2026-08-31, and the
shipped style held: the scan edge, the cooldown hatch, the keybind hint, V20's edge bar on
`sealed-proc-bar`, and the nine-slice ruled-out outline.
⚠ **V21's dial on `sealed-cooldown-range` is NO LONGER covered by that week.** Protection reported
it drawing as a **square** on 2026-08-31 (*THE FIRST PROTECTION FLIGHT*, finding 1) and both Havoc
and Retribution carry the same display — so either it was square there too and went unremarked, or
the failure is supplier-specific. **A week of no complaint is not a positive report**, and this is
the one place that distinction has now cost something. Treat the dial as unverified on all three. Retribution's Expurgation proc bar has a subject and draws. What that week could not
reach are the two specs below, because the author was not on them.

**Devourer showed nothing at all.** The author's report: *"I think it didn't show up at all for
that spec."* ⚠ **The thread is PARKED at the author's direction, not closed** — nobody has
established whether the catalog failed to bind, the panel drew empty, or the spec was simply
never in a state that produced a row. Do not read the parking as a verdict, and do not read a
later green gate as having answered it: no gate can see a pixel. The four things a Devourer
flight was going to settle are still unsettled, and the third is the load-bearing one:

- [ ] The **standing virtual row** (Consume) draws at all, on cap's own strip, at the right end.
      This is the only live consumer of V12, so V12 is unflown until it does.
- [ ] It shows **Devour** inside Void Metamorphosis — `Panel.Face` resolving
      `C_Spell.GetOverrideSpell` on the draw, the one thing in V12 no test covers end to end.
- [ ] Inside the form, the **Void Metamorphosis row draws Collapsing Star** with its count band —
      an override borrowing the row of the spell it replaces. If it does NOT, the override premise
      is wrong and Devourer's catalog needs re-authoring, not patching.
- [ ] Out of form, the bank band draws the **right threshold for the build** — 35 with *Soul
      Glutton*, else 50 — and the three ceded corner steps, two permanently blank, do not read as
      a fault.
- [ ] In AoE, in the form, with Void Ray **ready** and a Star granted: does Collapsing Star wear
      `blocked`? It should ONLY when neither Reap-family proc is banked. ⚠ **No scenario in the
      walk exercises cue H at all** — every scenario reaching Collapsing Star has Void Ray on
      cooldown — so this state has never been reasoned about by a gate, only by hand.

⚠ **SENTINEL IS AN UNMODELLED THIRD TRANSFORM ON POSITION 1, and the existing cue MISLEADS on
that build.** Found 2026-08-31 from an in-client tooltip the author screenshotted, before anything
flew. The Avenging Wrath talent tooltip reads **"Replaced by Sentinel"** *[T1: live 12.1 client]*,
and **Sentinel carries no `CooldownSetSpell` row** in the spec inventory — so, exactly like Sacred
Weapon riding Holy Bulwark and Hammer of Wrath riding Judgment, **Sentinel can only reach the
Cooldown Manager as an override on Avenging Wrath's row**. Protection therefore has *three*
transforms and the catalog models two.

- **The catalog authors no `identity` on entry 1** and binds `avenging_wrath` `31884` flat.
- **Cue A is not merely absent on a Sentinel build — it is WRONG.** It says *hold Avenging Wrath
  for Divine Toll*, an offensive-window argument, while the row is displaying **Sentinel**, a
  defensive cooldown with entirely different usage. A missing cue fails dark; this one fails lit.
- **Upstream cannot help.** The simc APL never mentions Sentinel, so the Tier-1 priority list
  models only the non-Sentinel build and there is no rung to transcribe.
- ⚠ **The absence is one tier weaker than Sacred Weapon's.** That claim rested on an exhaustive
  DB2 sweep of every set in the file; this rests on Protection's own `ability-inventory.tsv`.
  **Do the exhaustive check before authoring `identity` on it.**
- ⚠ **`knowledge/classes/paladin/protection/builds.md` asserted the opposite until today** — that
  the two are "separate nodes, not a choice pair", which is topologically true and was read as
  *you keep both buttons*. It has been rewritten and its changelog carries the correction. This is
  the second time a catalog premise came from that file's talent prose rather than from the
  client, and it is the same shape as the Light's Deliverance reversal: **a settled-looking claim,
  settled by prose.**

**Protection HAS now been seen** (2026-08-31) — see *THE FIRST PROTECTION FLIGHT* below, which
owns what it found. One thing that flight did **not** reach stays here, because the build carried
Divine Guidance and the band is the other half of the choice node:

- [ ] Protection's **Consecration presence band** (`cons_field_up`, Blessed Assurance builds only)
      has a subject and actually draws — it is the failure mode this file records for
      Destruction, a display with no subject, which draws nothing and says nothing about why.
      ⚠ **Not covered by the 2026-08-31 flight**, which ran Divine Guidance, and not by the
      Havoc/Retribution week: `sealed-pandemic` and the presence band are Demonology's and
      Protection's, and V19 has still never been confirmed drawing.

⚠ **V12's `gated` kind CANNOT be flown — it has no consumer anywhere.** It was built for Collapsing
Star, which turned out not to need it. Record it as unexercised, never as passed.

**`render-shelf.md`'s "Not flown." under V12 STAYS.** It was the one line the old entry promised to
delete once the flight landed, and the flight landed on the two specs that have no virtual row.
Consume is Devourer's and Devourer drew nothing, so the marker is still the honest one.

### THE FIRST PROTECTION FLIGHT — eight observations, six findings, 2026-08-31 → `backlog/protection-next.md`

**The ordered work list is `backlog/protection-next.md`** — what to add, then what to test, plus
what was deliberately left out of that round. This entry owns the findings and the evidence; that
file owns the response.

The spec's first time on a screen, on a **Lightsmith / Divine Guidance / Sentinel** build. The
author's verdict was *"it's kind of a mess as is"*, and the eight findings below are in their
words with the diagnosis under each. **Nothing here was found by a gate**, which is the point.

**1 — The `sealed-cooldown-range` dial DRAWS AS A SQUARE.** *"Sentinel has its badge drawn wrong,
as a square… Same with Holy Bulwark."* Both rows carry that display and nothing else does, so the
subject is V21's dial. `buildDial` (`Channel.lua`) asks for a radial bar through
`pcall(bar.SetRenderMode, bar, Enum.StatusBarRenderMode and …Radial or 1)`, and a **linear
StatusBar is a rectangle** — so a refusal degrades to exactly the reported shape.
⚠ **Exactly ONE of the two pcalls on this bar is silent, and it is the SHAPE one.**
`baseCooldownSink`'s `SetTimerDuration` refusal **is** logged, so the drive is instrumented; the
`SetRenderMode` call inside `buildDial` is not, and that is the one that decides square-vs-arc.
**Fix that instrumentation first**, and check the `Enum.StatusBarRenderMode and … or 1` fallback on
the same pass — a nil enum silently posts a literal `1`.

⚠ **The gallery cannot clear this and that is the finding under the finding.** `/cap style` builds
its dial with the **same** `SetRenderMode` pcall (`StylePanel.lua`), so the known
`buildSealed` duplication is NOT the blind spot here. The difference is one line later: the gallery
drives its bar with a static `SetValue(0.75)`, while the live row hands the bar to the client via
`SetTimerDuration`. **So the gallery proves the render mode was accepted at BUILD time and never
that it survives the client taking the bar over** — which is the only state the live row is ever
in. If the client resets render mode when it attaches a timer, every existing instrument shows a
perfect arc and the row shows a rectangle. **Read `GetRenderMode` back AFTER `SetTimerDuration`,
not at build.**

⚠ The comment in `buildDial` cites *"Radial is measured on a SetTimerDuration-driven bar
[client 2026-08-21]"*. If that measurement was taken on `windowSink` (V19's pandemic dial) it does
**not** transfer to `baseCooldownSink` — different supplier, different spell resolution — and a
one-sink measurement generalised to all four is its own defect. Establish which sink was measured
before trusting the line.
⚠ Not yet explained: Havoc and Retribution both carry `sealed-cooldown-range` and flew a week
without this being reported. Either it was there and unnoticed, or something differs per supplier.
Do not close it on the Protection evidence alone.

**2 — Blizzard's own text collides with cap's chrome, and the row cannot hold both.**
*"the count is overlapping the keybind"*, plus *"the last item in the CDM that has `1:36` in giant
text overlaying it"*, plus rows reading `57 S…nds` and `40 S…onds` — the client's countdown
spelled out and overflowing the icon. cap's hotkey is a `TOPLEFT` FontString at `+2,-2`
(`tokens.hotkey`) drawn **five frame levels above everything**, so it wins the collision it should
never have entered. **This is the entry below — *Add a shelf section for what Blizzard already
draws on a CDM icon* — being cashed in.** That item was speculative; it is now load-bearing, and
`ChargeCount`'s anchor is not recorded anywhere in `knowledge/addon-dev/`.

**3 — Two bound abilities wear no hint.** *"two of the abilities are definitely keybound without
any fancy macro shenanigans, but aren't being marked with their keybinding."* V15's two-stage
lookup reads `frame.action` off the real button frames; a bare miss on a plainly-bound key is a
`Binds.lua` defect, not the documented macro blank. Needs the two ability names to diagnose.

**4 — The hatch loses to bright icon art.** *"Sentinel is such a bright icon that even dimmed a
bit with a hatch it's still sort of asking to be clicked."* This is **Part 5 question 7 answering
in the direction the shelf feared**: black at `0.50` reads as *dimmed*, not as *ruled out*, on
high-value art. ⚠ It is NOT a licence to add a hue — the retired veil died of exactly that. The
shelf's own guidance is area or a different treatment.
⚠ **PROMOTED 2026-09-01** — this finding now has its own entry, *The hatch is paid on every scan*,
because the fold decision makes it a cost on every read of four specs rather than one bright icon
on one. The finding and its evidence stay here; the response lives there.

**5 — A duration-shaped swipe is read as a cooldown.** *"it has no cooldown red icon, which it
should since it's one of those annoying abilities that shows me the duration instead of the
cooldown, like tyrant."* **This is the standing entry *The swipe says two different things* getting
its second independent witness, on a different class.** It was recorded from Demonology; it
reproduces on Protection's Sentinel. That raises it from a nice-to-have to the highest-value
unbuilt item in this file, and the `SetReverse` option — a dial that FILLS versus one that
EMPTIES — is the one the report is asking for.

**6 — Charges should be a bar, not a small number.** *"For Demonic Core we have the marked
progress bar on the bottom to indicate how many stacks. I wonder if we could do that for abilities
with charges instead of the small number."* An author request to point **V18's segmented bar**
(`sealed-count-bar`, today an aura's application count) at a **charge** count. ⚠ Charges are
**readable** — `Sense.readCapped` already calls `C_Spell.GetSpellCharges` every tick — so unlike
Fury this needs no sealed sink and no lab question. It is a shelf primitive plus a catalog key.
It also **subsumes finding 2's count half** by moving the number off the icon face entirely.

---

### `1:36` is Blizzard's number, and on a held row cap draws the same number twice

Raised 2026-09-01, out of the first Protection flight's finding 2. The author saw *"the last item
in the CDM that has `1:36` in giant text overlaying it"*. That text is the `Cooldown` widget's own
C-side countdown, centred on the whole icon at `GameFontHighlightHugeOutline` — huge on a 50 px
Essential item by Blizzard's choice, with **no region to reparent, no anchor to move and no
parentKey to reach** (`knowledge/addon-dev/cooldown-manager.md` §1.5, point 3).

⚠ **It was first written up here as "cap cannot touch it", and that was wrong.** There is no
region, but there is a **setter**: `SetHideCountdownNumbers(not shown)`, reached through
`CooldownViewerItemMixin:SetTimerShown`, and it is applied from `OnAcquireItemFrame` and from the
viewer's own Edit Mode toggle — **not** from any per-refresh path
`[T1 src @12.1.0: CooldownViewer.lua — CooldownViewerItemMixin:SetTimerShown,
CooldownViewerMixin:OnAcquireItemFrame, CooldownViewerMixin:SetTimerShown]`. So it is the same
shape `Glow.lua` already uses on the proc glow: hook per instance, write when cap is live, restore
when cap goes dark. **`spec.md` §4 does not forbid it** — the promise is that cap never writes the
player's *saved* Cooldown Manager configuration, and this is a runtime display write on a frame,
strictly smaller than the row re-anchoring §4 already permits.

**What makes it worth raising is not the size of the font. It is the duplication.** On a row
wearing a `sealed-cooldown-range` hold, cap's V21 badge already draws a countdown — and the
client draws a *different* countdown, of a *different* clock, in the middle of the same icon.
Protection's row 1 is the case: Blizzard's centred number is that row's own cooldown, cap's badge
numeral is Divine Toll's. Two numbers, one icon, neither labelled.

**Three answers and they are not the same decision:**

- **Leave it.** Blizzard's number is information the player uses on every row, and cap's badge is
  present on a minority of them. The noise is the price of not deciding for the player.
- **Suppress it only where cap draws a dial.** The narrow one: the duplication is the defect, so
  remove it exactly where it occurs and nowhere else. ⚠ It makes the row's OWN remaining time
  disappear on precisely the rows that are held — which may be the moment it is most wanted.
- **Suppress it on every row cap has claimed**, and let cap's chrome be the only numbers on the
  strip. The strongest and the most presumptuous.

⚠ **The player's own *Show Timer* toggle already does the third**, per viewer, without cap. That
is the argument for doing nothing: an option that exists and is one click away is not a gap.
⚠ **This is a `spec.md` §3 change before it is a shelf change** — it is player-visible behaviour
on Blizzard's own surface, not a treatment of cap's, so it needs a spec line and not just a token.

### An OFF-GCD press is not a rung, and the scan has no word for it

Found 2026-09-01 in play, from the author asking why cap says nothing at Holy Power cap. The
answer turned out not to be a missing badge.

**Shield of the Righteous is off the global cooldown and has no cooldown of its own**
*[`knowledge/classes/paladin/protection/abilities.md` — Shield of the Righteous]*. Two things
follow that the catalog reasoned around without naming:

- **It is why Protection's APL carries no `holy_power` term anywhere.** With a free spender there
  is no spend-or-generate decision to arbitrate: you dump and continue in the same window. The
  `## Why no row wears overcap` section reaches the right conclusion from a weaker premise —
  *"there is no number to author it from"* — when the stronger one is that there is no **tension**
  to author about.
- **It breaks the walk's central assumption.** Part 0.5 says *scan left to right, press the first
  thing not ruled out*, which silently assumes every entry costs the same thing: a global. In
  simc, reaching rung 9 does not end the turn — the action fires off-GCD and evaluation continues
  down the list in the same instant. In cap, reaching an un-eliminated icon **does** end the walk.

**So SotR is not really in the queue.** At cap the player should press it wherever the scan lands,
and then carry on from where they were. The row's `scan_when = affordable` makes it a *conditional
member* of the scan, which is not wrong and is not enough: a walk that stops there reads as *press
this INSTEAD of what is below*, when the truth is *press this AS WELL*.

⚠ **This is a Part 0.5 question before it is a treatment, and it is not Protection's alone.**
Every spec with an off-GCD press has it. What is missing is a way for an entry to say *I cost no
global* — plausibly a `free` flag on the entry, which the walk steps **over** rather than stopping
on, with a treatment that reads as "take this in passing" rather than as a verdict. Do not author
it as a cue: a cue is a statement about whether to press, and this is a statement about what
pressing COSTS.

⚠ **Do not reach for `overcap` as the substitute.** It was considered and it is the wrong shape:
it would fire on the generators, which are not the thing to change, and Protection has no Tier-1
threshold to author it from. The complaint was never "tell me I am at cap" — it was "the row does
not lead me to the spender", and the spender's problem is its COST, not its rank.

### The client's unusable tint is a FOURTH eliminating signal and the model does not admit it

Part 0.5 counts three: Blizzard's swipe, cap's own negative badge, and — since 2026-08-22 — a
sealed band the client hatched by evaluating a rule cap authored. There is a fourth and cap has
never admitted it. When a spell's only bar is an access gate rather than a cooldown, the Cooldown
Manager paints the row with `ITEM_NOT_USABLE_COLOR` (`knowledge/addon-dev/cooldown-manager.md`
§3.4). A human reading the strip skips that row. The reading model does not, so the walk and the
eye disagree, and the walk is the thing the elimination gate checks.

**Two consumers, both live, found independently:**

- **Destruction · Shadowburn** — out of execute without the proc, the row is tinted and the
  catalog's own hold is undrawn because the gate is an unmeasured `IsSpellUsable` first return
  (`destruction/catalog.md` → Defeats item 3).
- **Devourer · in-form position 1** — Collapsing Star is granted every 30 fragments harvested
  inside the window, so for most of that window the row draws tinted-but-reachable at the head of
  the scan (`devourer/catalog.md` §3).

⚠ **Not admitting it is the current decision, and it is deliberate.** Admitting a signal is a
Part 0.5 change, Part 0.5 is the authority every treatment is judged against, and the minimal move
while two specs have just been authored against the three-signal model is to leave the model
alone. What this entry buys is that the next spec to hit it finds a recorded question instead of
re-deriving it a third time.

**What would settle it:** whether the tint is legible enough to carry an elimination on its own —
which is an eye question, not a measurement — and, if it is, whether the model admits a signal cap
neither reads nor decides. The `IsSpellUsable` measurement is a *different* question and does not
answer this one: reading the gate in Lua would let cap draw its own badge, which is signal two.

### The display-provenance gate resolves by SUBSTRING, over the row's whole rung set

Shipped 2026-08-27 and working — 29 of 36 sealed displays resolve, 4 argue themselves in a
declared sentence, 3 are skipped by kind because a `sealed-power-percent` display has no aura
subject to check. What is worth writing down is the **shape of its remaining looseness**, so
nobody later reads a green tally as a stronger claim than it is.

**It matches the subject's APL token as a substring of the rungs the ENTRY cites**, not the
wearing state's, and not against the rung's *condition*. Both halves are deliberate and both cost
something:

- **Per-row, not per-state.** A hold state cites the rung it yields *to*, which is another
  button's line, so a per-state check fails every honest hold that carries a display. Per-row is
  the claim actually worth making, and it is the same line the state gate already draws:
  authoring discipline, not an APL correctness engine.
- **Substring, so a subject can resolve against a rung that merely MENTIONS it.** The live
  instance is Protection's `cons_field_up`: it resolves through rung 29's bare `consecration`,
  while the fact it draws — the ground effect being up — actually lives in rungs 19 and 24's
  `!consecration.up`. The gate is satisfied by a weaker thing than the one that would justify the
  display.

Tightening it means per-state condition matching, which fails the holds. `display_apl` already
exists as the precise form when an author wants to name the exact rung.

**DECIDED 2026-09-01 — document the looseness, require nothing. No change to the gate.** The
residual question was whether `display_apl` should be *required* wherever the bare-mention path is
what resolved, making the loose case visible instead of silent. It is not, for two reasons: it
re-opens every currently-resolving display at once on a gate nobody but its author has argued with,
and the tighter check it gestures at — per-state condition matching — is not available at all, so
requiring the precise citation is ceremony with no correctness argument behind it yet. **The shape
now lives in the gate's own docstring** (`_display_provenance_gate`), which is where a reader meets
it, rather than only here. **Reopening condition:** one display found by hand to be drawing a fact
its row's rungs do not read — the Light's Deliverance failure slipping through — which is what
would make the extra ceremony worth its price.

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

### Teach `Catalog.OrderCheck` what it is actually checking — WORDING SETTLED 2026-09-01, the edit is batch D

It compares the catalog against Blizzard's `layoutIndex` and reports as though that were the drawn
order. Since `Anchor.lua` shipped that is no longer true even on a stock setup — `GetItemFrames()`
sorts by `layoutIndex`, so every instrument cap owns is blind to a `SetPoint` re-anchor **by
construction**, and under a competing CDM skin the check is neither right nor wrong but **blind**,
which is the worse failure. `Anchor.lua:9` already records the invariant from the other side:
*"position is read with GetLeft/GetTop, never through Bind or Catalog.OrderCheck, which sort by
layoutIndex and cannot see a SetPoint."*

⚠ **The fix is two strings in `Sense.lua`, so it is addon Lua and rides the next cut, not this
round.** The check itself is correct at what it does and must not be changed — `OrderCheck`
(`Catalog.lua:793`) takes the row list it is given and reports the first pair out of order, which
is exactly right. What is wrong is that its two outputs claim more than it read. Both are in the
`told ~= state.orderTold` block:

- **`Log.Note`, today:** *"row-order %s is laid out after %s; this catalog reads left-to-right in
  priority order"*.
  **Replace with:** `"row-order %s is laid out after %s in the Cooldown Manager's own layoutIndex, "
  .. "which is what this check reads — not the drawn position, which another addon may have
  re-anchored; this catalog reads left-to-right in priority order"`.
- **`Emit`, today:** *"your Cooldown Manager orders X before Y, which is not this catalog's
  priority order — read the row with that in mind."*
  **Replace with:** `"your Cooldown Manager's saved layout orders X before Y, which is not this
  catalog's priority order — read the row with that in mind. (This reads the saved layout, not
  where the icons are actually drawn.)"`

**Why the wording and not a real fix.** Reading drawn position means `GetLeft`/`GetTop`, which is
what `Anchor.lua` already does and which needs a frame that has been laid out — a different
lifecycle from the one `Sense.lua` runs this in. Making the check *see* a re-anchor is a genuine
piece of work; making it stop **claiming** to see one is two strings. ⚠ **Do not let a later pass
record this entry as fixed when only the wording has landed** — the blindness is unchanged and this
is a truthfulness fix, nothing more.

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

### ~~Consolidate the three Havoc docs into one `catalog.md`~~ — RETIRED 2026-08-19

**Do not re-raise this.** The one-`catalog.md`-per-spec rule it enforced has been reversed:
`catalog.md` / `scenarios.md` / `fact-classification.md` are a definition, its proof and its
safety case, and Havoc's three files are now the **model** rather than a debt
(`authoring.md` §0). Retribution was split to match on 2026-08-19.

The item's *other* half survives on its own, below.

### ~~`rotation.md` is the sole home of the priority order~~ — SWEPT 2026-09-01; no second copy found, two files gained the missing sentence

The gameplay KB carries the priority list with front matter and provenance; a catalog cites it and
must not restate it. All six `*/catalog.md` were read end to end for a **reader-facing restated
ordered list** — a numbered list, table or prose run reproducing the priority as something to read
*instead of* the APL. Per-entry rung citations are required by the state-provenance gate and were
not the target.

**Nothing found, and the near-misses are the useful part.** Three constructs came close and all
three survive on examination:

- **`## The authored row order`** (five files, a `# | Entry | rung` table). Its subject is
  `Catalogs/<Spec>.lua`'s `entries` array — an addon artifact that has to be documented — and each
  instance is followed by prose explaining exactly where row order and rung order **diverge**
  (Havoc's Vengeful Retreat 5→1, Retribution's `finishers` interleave, Demonology's Demonbolt swap).
  A document of the divergences is not a copy of the order.
- **Havoc's four-rung Immolation Aura table.** Rung-ordered with verbatim conditions, but it is one
  **entry's** placement being argued across the four rungs that set it — provenance of unusual
  breadth, not a mini-priority-list.
- **Devourer's *"13 distinct presses in first-occurrence order"***. A census sizing the roster; raw
  simc tokens, no conditions.

**What the sweep actually found: `havoc` and `devourer` were the two files WITHOUT the *"Neither is
restated here"* header sentence the other four carry — and they are the two that produced the near
misses.** Both now carry it, each naming its own near-miss so the next reader does not re-raise it.
That is the durable half: the rule was already being followed and was the only one of the header's
promises left unwritten in two files.

⚠ **Rung-mention counts are not a defect signal and should not be read as one** — protection 130,
havoc 98, demonology 54, destruction 38, devourer 36, retribution 7 bare (plus 34 list-qualified).
A high count is what per-entry provenance looks like.

### ~~Close out the migration artifacts~~ — the `specs/` half is DONE 2026-09-01; the Lua half is batch D

**Four artifacts went to `specs/archive/` under the existing `-YYYY-MM-DD` convention** — the
simplification plan and audit, the rule-split audit, and the Devourer preview plan, which named
*this entry* as its own release condition. Archived rather than deleted: their arguments are the
record of why the current design is shaped as it is, and `archive/` exists for that. ⚠ **Nothing in
`archive/` may be cited as a reason to do anything, and nothing there is to be read in the present
tense** — `projects/combat-assist/CLAUDE.md` now says so once, for the folder, instead of naming
three files by hand.

⚠ **The simplification plan was already contradicted by the constitution when it was archived**, so
it was a live document telling a reader the wrong thing: its corrected target is the three discrete
tiers `ASAP` / `SOON` / `FALLBACK`, and `spec.md` §3.1 retired those on 2026-08-25. The archived
copy's header now says so.

**`ellesmere-mover-plan.md` was deleted**, not archived — its history is already at
`archive/ellesmere-mover-plan-2026-09-01.md`, its goal was reached (Phase 3 flew, v0.23.1), and its
outcomes are in `## Status`. Its own header said it was kept only because deleting an *untracked*
file is not undoable by git; it was in fact tracked, so that reason was false and the deletion is a
`git revert` away. The archived copy is now flagged as the whole record.

- [ ] **What is left is the addon-side half, and it is batch D.** The audits name **only Lua and
      tests** for *"remove the obsolete modules, fields and vocabulary kept as compatibility
      scaffolding for an unreleased design"* — there was never a `specs/` half of that checkbox, and
      reading one into it is what kept this entry looking half-done. It rides the next C/D release.

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

⚠ **Neither Warlock spec has a catalog Lua of the current design**, so neither has flown and
neither can — see the Status block. The 2026-08-31 week of play was Havoc and Retribution; it says
nothing about Demonology or Destruction.

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

- **Five parked items, none blocking anything → `backlog/parked-work.md`.** Written down so they
  stop being rediscovered and re-argued. **Destruction** — the shipped 47-line pilot and its
  10-entry document disagree; blocked behind `authoring.md` stage 6, a first catalog review, and
  the absence of a `catalog.json`, and its press-on-sight abilities are scattered so no cut
  separates cooldowns from rotation. **Devourer's Vengeful Retreat** — a line in the setup docs,
  ⚠ never a `viewer` field. **Mover-driven resize** — ⚠ explicitly not the fix for overflow, since
  a roster-derived grid destroys *"the rect is known at login"*, which the EllesmereUI anchoring
  depends on. **`RegisterSkin`** for cap's own windows — cosmetics, touches no CDM frame.
  **`norow` conflates three causes** in `Bind.lua:242` — a diagnostic sharpening, not a fix.
  ⚠ ~~The Destruction entry carries one correction to make while passing.~~ **Made 2026-09-01** —
  the `## Status` Destruction bullet now reads *one-entry proof* and says why. ⚠ The line number
  this pointed at (`backlog.md:619`) had already drifted onto a different paragraph, which is the
  second thing it got wrong: **cite a heading, not a line number, in a file edited every session.**

- **Say WHY a row is hatched, on hover.** Asked for 2026-08-29, from playing Retribution: three
  rows (Execution Sentence, Wake of Ashes, Divine Toll) read as permanently red with no way to tell
  which of four holds is doing it. **cap already computes the answer and drops it at the screen** —
  `Signal.markersOf` records `{id, state, terms}` per readable marker, where `terms` are already
  formatted (`ready(execution_sentence)=T`, `talent(radiant_glory)=F`), and `Sense.lua` serialises
  the lot into captures as `W{}`. Nothing needs computing; it needs a surface.
  - **`/cap why` first**, and it may be enough: print the current reasons per row, or for one named
    row. No mouse, no taint, no client unknowns, all existing machinery.
  - **The hover tooltip is the real ask, and it has ONE thing to measure first.** The mechanism has
    to be *hook the CDM item's `OnEnter` and append to `GameTooltip`* — **not** `EnableMouse` on
    cap's row overlay, which takes no mouse today and would swallow the hover and kill Blizzard's
    own spell tooltip. ⚠ **`knowledge/addon-dev/cooldown-manager.md` says nothing about whether
    those items are mouse-enabled, fire `OnEnter`, or are safe to hook** — they are pooled, re-bound
    on `OnCooldownIDSet`, and since 12.1 participate in secure aura plumbing. That is a ClientLab
    question and it gates the work: `projects/addon-lab/`, one test.
  - ⚠ **What it can and cannot say, which is a DESIGN limit and not an effort one.** A readable
    marker can be quoted term by term. A **sealed band cannot**: cap never learns whether the client
    painted it or what the remaining is — and on the three rows that prompted this, the Avenging
    Wrath holds are all sealed bands. So the tooltip names the RULE (*held while Avenging Wrath is
    within 15s — client-decided*) and never the value. That is still the fix for the complaint,
    which was that the reason was unreadable, not that the number was missing; V21's dial supplies
    the number on the badge face.
  - Player-visible behaviour, so it needs a `spec.md` line before it is built, not just this entry.

- **V12's `gated` kind is built, unexercised, and its retirement is a Lua change — batch C/D.**
  The *documentation* half of this finding is closed: `render-shelf.md` V12 argues from **Consume**
  (`standing`) and carries the dated correction that Collapsing Star is a spell **override** on the
  Void Metamorphosis row, so R7 draws it and it was never a virtual row. Verified 2026-09-01 —
  nothing in `specs/**` still argues V12 from Collapsing Star.
  **What is left is the kind itself.** `gated` has **no consumer anywhere**, has never had one, and
  must be recorded as *unexercised* rather than as passed. Retiring it is a live option and the
  cheaper one — but it is `Catalog.lua`'s `VIRTUAL` kinds, `Catalog.Check`'s refusal of a subject
  predicate naming a virtual ability, and `Overlay.lua`, so it is **addon Lua and not available on
  paper**. ⚠ **Keeping it is the current decision and it has a reason**: the inverted-unknown rule
  it carries is the thing that makes a gated row hard, and the shelf says the next spec that wants
  one meets that rule before authoring rather than after. Deleting the kind deletes the place that
  argument is attached to.

- **~~Destruction has never been catalog-reviewed.~~ — REVIEWED 2026-09-01. Six findings, four of
  them stale defeats, and one of them is a transcription trap for stage 6.** The 2026-08-25 pass
  reviewed five specs and skipped Destruction because this file recorded it shelved. ⚠ **Both
  cross-cutting patterns had to be run by hand** — the hold-availability gate iterates
  `catalog.json` states and Destruction has none — which is exactly why doing it before stage 6
  authors that file was the right order.

  **Pattern 1 — a hold naming a row it never checks is available: CHECKED, NOTHING FOUND**, and it
  is a clean negative rather than a "could not tell". All ten markers were read against the
  ten-entry roster: **there is not one cross-row term in this catalog**, which the file states
  itself (*"not one rung in `actions.default` reads another ability's `cooldown.X.remains`"*) and
  which it acts on, explicitly declining the one companion marker it could have written. Every
  hold's stated reason is its own rung's own conjunct. Protection's Defeat 4 has no instance here
  and nothing would transcribe one.

  **Pattern 2 — a recorded defeat gone stale under a later primitive: FOUR of five are stale.**
  Fixed in place on 2026-09-01, since a defeat resting on a false premise is a stale claim:
  - **Defeat 1 (the DoT pandemic window) — reopened, and the reopening is CHEAPER than the file
    thinks.** It says the fix is a `pandemic` predicate in `Catalog.PREDICATES` plus a
    `readPandemic`. **V19 needs neither** — promoted 2026-08-22, it drives a client-owned region
    off the client's own refresh arithmetic and authors no threshold, it is recipe `S9`, and it has
    two shipped consumers. Its two-sided pair *is* cue E's job. Immolate's DoT is already
    established here as the Category-2 row V19 needs. ⚠ **This is the transcription trap:**
    authoring `immolate_up` as a whole-DoT `blocked` from today's text ships a defeat that is
    expressible. **Resolve before `catalog.json` — batch C.**
  - **Defeat 2 (the ritual clock) — its central claim is false and it is re-scoped.** *"There is no
    aura-remaining band"* was true when written; V19's outside hatch is literally a band on an
    aura's remaining seconds (Protection ships one), and V20 drains an aura's remaining into a
    client-owned bar with the *armed Demonic Art* as a declared consumer — the same mechanism.
    What survives is the **sum** of three stage remainings and the Tier-2 "exactly one stage is
    live" equivalence, which is what its `@verify-ingame` is really about.
  - **Defeat 5 / §5.3 (which Diabolic Ritual row is the armed Art) — partly stale.** Demonology has
    since named the aura and armed a display over it (`art_mother_of_chaos`, aura `432794`,
    flagged there as Tier-3-sourced and dying silent). *"One measurement serves both Warlock
    catalogs"* still holds; Destruction is now the one that has not taken the available hedged
    route, and its docs do not know the id exists.
  - **Defeat 4 (`target_if`) — WORDING ONLY, and worth fixing precisely because it is not a real
    reopening.** *"What would reopen it: a surface that is not a CDM row"* is now satisfied as
    written by V12's virtual row, which reopens nothing — a virtual row is still a button and the
    unsaid thing is *which enemy*. Re-phrased to *"a surface that can address a unit"*. ⚠ A
    reopening condition that a later build satisfies by accident is worse than none: the next pass
    trips on it.
  - **Defeat 3 (Shadowburn in execute range) — NOT stale**, checked against all eleven primitives.
    Every one needs an aura or cooldown subject that does not exist here, and `spec.md`'s
    presence-not-absence limit is not even engaged because there is no display at all. It stands
    exactly as written.

  **Two vocabulary claims were stale and would have been transcribed verbatim** — both fixed:
  `catalog.md` measured its design against a `Catalog.DISPLAYS` list that still named the retired
  `player-aura-stacks`, and `fact-classification.md` cited its `min = 2` guard as live. ⚠ **That is
  what made Defeats 1 and 2 look closed** — both argue from *"no display kind exists"*, against a
  list two primitives out of date. And `scenarios.md` called the client's unusable tint *"a third"*
  eliminating signal where `catalog.md` correctly says three exist already, making it a fourth: the
  two documents disagreed with each other.

  ⚠ **The "empty sealed lane" claim is a CONSEQUENCE of two stale defeats, not a finding about the
  spec.** *"The first catalog with an empty sealed lane"*, *"this catalog authors zero sealed
  cues"* and the whole of `fact-classification.md` §4 are currently written as an observation about
  Destruction. Acting on Defeat 1 puts a `sealed-pandemic` in the lane and falsifies all of them.
  **Left standing deliberately** — rewriting them before the catalog edit lands would be asserting
  a design decision nobody has taken; they move together, in batch C.

  **The known live Shadowburn finding is cross-referenced, not re-derived, and the docs already
  carry it fully** in four places, independently of this file, including the two-consumer count and
  the 2026-08-27 narrowing that the `IsSpellUsable` measurement is now Destruction's alone since
  Collapsing Star turned out to be an R7 override. The only gap was the signal count above.

  **Low confidence, recorded not acted on:** if the author's request to point V18's segmented bar at
  a **charge** count ships, Conflagrate is its first candidate — Destruction is the only catalog
  where the charge state does ordering work. It reopens nothing today; V18 is a shape, not a
  numeral, and the argument that no rung wants the number survives.

- **~~Check a SETTLED claim as hard as a hedged one~~ — LANDED in `authoring.md` 2026-09-01.** It
  was a process lesson with no home; the process file is `authoring.md`, and it is now a standing
  rule beside *How to write a defeat*, keeping the Light's Deliverance provenance — the hedge was
  warranted, the settlement was not, and what closed the question was **spell text**, which could
  not answer it. A second standing rule went in beside it out of the Destruction review: **a defeat
  goes stale and nothing notices**, so a promoted primitive means grepping the corpus for the
  defeats that named its absence, and a reopening condition must name the thing you need rather
  than the negation of what you have.

- **An OR in the marker `when` grammar — wanted by a defeat that has no other exit.**
  Recorded 2026-08-26 out of Protection's Defeat 4. `when` is AND-only (`Signal.lua`), and the
  project's one workaround is **two markers wearing the same cue**, whose union is the disjunction
  (Retribution's `boj_opener`/`boj_opener_woa`, Havoc's rung-2 merge). That works when each
  disjunct is a *positive* statement. It does **not** work for Defeat 4, whose statement is
  *"every rung above mine is unavailable"* — a conjunction of negations over OTHER rows, which is
  not a disjunction and does not decompose into markers.
  ⚠ **And on Protection it is not merely awkward, it is UNSOUND — do not author it as a
  many-term marker.** Rung 16 is a bare `hammer_of_wrath`, it outranks rung 23, and **Hammer of
  Wrath has no roster row at all** (`specs/protection/catalog.json` → `abilities`). So a marker
  spelling out `!ready(avengers_shield) ∧ !ready(judgment) ∧ !ready(consecration) ∧
  !aura(blessed_assurance)` would still be blind to one of the rungs it claims to have cleared,
  and would fire when Hammer of Wrath is the press. **A hold that enumerates its outrankers is
  only as sound as the roster is complete**, which is a property no gate checks and no author can
  see from the marker.
  The real shapes worth considering, in order of appetite: a **per-marker rank** so a row can say
  *"I am ranked below the rows to my right"* directly; or alternatives inside `when`; or binding
  the missing rows so enumeration becomes sound. The first says the actual thing — the other two
  make the workaround safer without making it honest.

- **`capped` needs no `charged` declaration — a project-wide correction, not a Protection one.**
  Measured 2026-08-26. `Sense.lua:96-106` `readCapped` calls `C_Spell.GetSpellCharges` on the
  **live** id every tick, reads `maxCharges` off the client, returns UNKNOWN (never `false`) at
  `maxCharges <= 1`, and **never consults `ability.charged`** — `Track.lua:190-199` says it
  deliberately bypasses the charge ledger, and `Catalog.lua:17` gives `capped` `arity = 1,
  subject = true` with no `charged` requirement. So the self-withholding at one charge **is** the
  talent-conditional behaviour that two separate defeats asked someone to build.
  ⚠ **Protection's Defeats 4 and 5 both rested on this false premise and are rewritten.**
  ⚠ **THE SWEEP RAN 2026-09-01 AND FOUND NOTHING — no catalog declines `capped` for the wrong
  reason.** Every catalog that does not spend it was re-read against `Sense.readCapped`:
  - **Retribution** argues it at length under *Why this catalog does not spend `capped`*, in three
    independent parts — five Holy Power is loss *conditional on a press* rather than loss in
    progress; the negative phrasing exists and is already authored as `overcap` on Divine Toll;
    and "spend now" is a rank claim the scan already carries. **Not one of the three touches a
    charge declaration.** Sound on merits, unchanged.
  - **Demonology** declines it because **nothing in its Essential set is a charge spell at all** at
    12.1, measured off `ability-inventory.tsv`. There is no subject, so the question does not
    arise.
  - **Protection** already carries the correction in full.
  - **Havoc** and **Destruction** spend it (Immolation Aura, Conflagrate), so neither declines it.
  - ⚠ **Devourer neither spends nor declines it** — `capped` appears nowhere in its catalog. That is
    a silence rather than a wrong reason, so it is not what this sweep was looking for, but a
    catalog that never considered a cue is not the same as one that considered and refused it. Left
    as a note; it wants a sentence the next time that file is opened.

  **So the false premise cost two of Protection's defeats and nothing else.** Recorded because the
  sweep ending in nothing is the outcome worth writing down — an unrecorded no-change gets
  re-swept.

- **~~The Protection preview is 1 KB over budget.~~ — RESOLVED 2026-08-27, and the budget was
  the thing that was wrong.** The warning was real but it was not about Protection: `build`
  measured `len(page)` — the whole HTML — against `tokens.budget.max_base64_kb`, a ceiling whose
  own `_comment` says it exists for **asset** bloat. So the number had been moved twice (300 → 350,
  and earlier 512 → 600 in a different unit) to accommodate pages that had grown more **markup**,
  which is a ceiling being re-aimed at a quantity it does not name. Now split in two: the asset
  payload is judged against `max_base64_kb` (**80**, against a worst case of 55 KB on Havoc) and
  total page weight against a new `max_page_kb` (**400**, against a worst case of 359 KB, also
  Havoc). No page warns today, and both warnings were proven able to fire. ⚠ `max_base64_kb` moves
  for more **art** and never to quiet a page that has grown more HTML — that reflex is what this
  entry records.

- **A sealed sink for a secret POWER COUNT — the gap V16-V18 cannot cover, and Havoc is the
  proof.** Recorded 2026-08-26 as a clean NEGATIVE answer, because nothing anywhere said it:
  **V16/V17/V18 cannot state Fury.** All three ride an aura's *application count*
  (`SetApplicationCount` / `SetApplicationBar`), and Fury is `UnitPower` — a different thing
  entirely. The only sealed sink that takes a power value at all is `sealed-power-percent`, whose
  channel is a **colour curve**: it can say *"you are near a break point"* by hue, and cannot say
  *how much* by any means. So there is no form in which a number derived from a secret power
  reaches the screen.
  ⚠ **The consequence is that Havoc using none of V16-V20 is not an oversight**, which is how it
  reads if you only count adoptions. Havoc has **no stacking aura and no DoT of its own** — the
  two things those primitives are built on — so the absence is structural. Its one sealed-count
  question is Fury, and Fury has nowhere to go.
  **This is a missing SINK, not a missing catalog edit**, and it is the honest form of the
  question *"why does the spec with the most sealed facts adopt the fewest sealed displays?"*.
  If a Fury bar is ever wanted it is a lab question first — whether a `UnitPower` value can reach
  a client-owned bar without Lua ever comparing it — and only then a shelf primitive. **Do not
  author it as a catalog edit; there is nothing to author it with.**

- **The empowered-cast (Demonsurge) cue — an optimisation over the baseline, not part of it.**
  Havoc's rung 3 has three holds and the catalog draws two. The third is
  `!action.death_sweep.demonsurge_available & !action.annihilation.demonsurge_available` — *don't
  recast Metamorphosis while empowered casts are still owed* — and nothing on the row says it.
  `proc` already exists in `Catalog.PREDICATES`, so **if** an owed empowered cast surfaces as a
  readable proc on the row, this is a marker and not a mechanism. That "if" is the whole of the
  work: measure first (`specs/havoc/catalog.md` → *Open facts* 6), then author. **Do not build it as
  part of the Havoc baseline** — the baseline ships without it and is coherent without it.

- **Trinkets are in the Cooldown Manager since 12.1, they are in the APLs, and cap ignores them.**
  Raised 2026-08-27. On-use trinkets are part of a rotation and are gated on **possession and
  equipped slot**, not on spec or talent — so a catalog cannot enumerate them the way it enumerates
  abilities, and declaring `item: <id>` would tie spec knowledge to a season's loot table.
  **The unlock is that the player's own act of adding the trinket to Essential Cooldowns IS the
  declaration.** 12.1 made that a first-class category rather than something to infer:
  `EquipSlotEssential` (**7**) and `EquipSlotTracked` (**8**) join `SpecAgnostic*` for racials
  (`knowledge/addon-dev/cooldown-manager.md:85-100`). Two equip trinkets, or two on-use ones the
  player macros, means category 7 is empty and cap binds nothing — the fail-dark behaviour wanted,
  for free. Motivating case: a **channeled** trinket cannot be macro'd, so it needs a visual.
  **Bind by SLOT, not by item, because that is how the APL addresses it** — `use_item,slot=trinket1`,
  and the CDM row carries `equipSlot`, read via `GetInventoryItemCooldown("player", equipSlot)`
  (`cooldown-manager.md:325-340`). Both sides already key on the same thing. **36 of 40 specs' APLs
  carry `use_item`**, so this is a project-wide primitive, not one spec's nicety.
  Upstream already agrees with the hand-rolled ordering: Demonology's `actions.items` rung 1 branches
  on `(!pet.demonic_tyrant.active&trinket.1.cast_time>0|!trinket.1.cast_time>0)` — a trinket with a
  cast time goes BEFORE Tyrant, an instant one does not care.
  ⚠ **One measurement blocks it, and it is a ClientLab question, not a design one.** An `EquipSlot*`
  row's value does **not** come from `C_Spell.GetSpellCooldown` — it comes from
  `GetInventoryItemCooldown`, a different API on a different key, and **the value cascade was derived
  on spell-backed rows only and was never re-derived for the item path**
  (`cooldown-manager.md:340-347`, `@verify-ingame`). cap's `ready()` rests on that cascade, and
  `ready()` is what every hold and the default `scan_when` alternative are built on — so today cap
  cannot establish that a trinket row is even IN the scan. Blizzard's own
  `-- TODO: Support potions as well, this won't just be equipslot` (`CooldownViewer.lua:1018`) says
  the item path is unfinished upstream. Nothing in §1.3 has been seen in a client.
  ⚠ **What cap CANNOT do here, and it is already a recorded gap:** it never writes to or rearranges
  the Cooldown Manager (`spec.md` §4), so the player drags the row and cap annotates it. Saying
  *"this row is ranked below the rows to my right"* is the same grammar gap Protection's Defeat 4
  records above. The deliverable is the overlay, not the ordering.
  ⚠ **And the APL region is the known-weak one** — `wowkb.sim`'s `apl_append` exception exists
  precisely because upstream deadlocks on two on-use trinkets, its default profile shipping only one.
