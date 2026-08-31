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
      assertions). **What has not:** the modal, the positional test against a live rider, and the
      depth guard — all three are client behaviour and are the acceptance set for the next flight.
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
      the grid arithmetic (`anchor_spec`, 6). **What has not:** the drag itself, the seed from a
      live viewer, and whether the panel holds across a spec swap and an Edit Mode icon-size
      change — the acceptance set for the flight.
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
      **What has not:** that the overlay actually goes dark in the client on `/cap anchor off`
      and comes back on `/cap anchor on` — the acceptance set for the flight.
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
      table and that two characters do not see each other's). **What has not:** that a second
      character actually seeds its own row — which needs two characters with the Cooldown
      Manager in different places, and is the acceptance set for the flight.
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
      - **Not yet flown.** What the tests cannot reach: that a real CDM item frame accepts the
        `SetScale`, that a re-pool is actually caught by the re-assert, and that `disarm`
        restores a size the player can see. `scalefail=<n>` reaches the anchor capture and
        should never appear.
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
  two-entry proof and **not** what `specs/**` now says.
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
- **Devourer is transcribed and has never been flown.** `Catalogs/Devourer.lua` is generated from
  `catalog.json` and loads, so everything on the page draws in the client — but nothing on it has
  been SEEN. It is the first spec whose definition needed **V12's virtual row**, and after
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
- [ ] **Fly the park.** Get a row to drop out of the plan without a pool release (a
      `GetCooldownID()` identity change is the reachable one) and confirm `# parked n=1`, the icon
      leaving the row, `A{parked:1}` standing in the readout, and `/cap anchor off` bringing it
      back with `# restored n=<all>` and `orphans=0`. ⚠ **The failure to watch for is the
      opposite one:** a park that survives a destructive stomp would hide a live ability, so
      confirm `A{parked:0}` after every `# stomp … destructive=1`.
- [ ] **Fly the recovery.** Force a re-pool (spec swap, or a settings change that alters the row
      count) and confirm `# stale` → `# rearmed` → `X{ok}`, rather than a silently scrambled row.
      Then answer the dialog both ways and confirm `# restored` / `# armed` follow.
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

### THE OWED FLIGHT — v0.13.2 is deployed and nothing in it has been SEEN

Cut and deployed 2026-08-27, 21 commits, the largest catalog change the project has had. Every
gate is green and no gate can see a pixel. cap reports `offered` / `armed` / `refused` and never
learns whether a sealed band actually painted, so all of the below needs an eye.

⚠ **v0.13.1 shipped a cue that eliminated a correct press and was replaced within the hour.** The
post-release conscience review found cue H holding Collapsing Star on `ready(void_ray)` alone,
where rung 8 fires on `!eradicate|!moment_of_craving|4pc` — so with both procs banked the APL skips
Void Ray, rung 9 is the press, and cap badged it `blocked`. v0.13.2 gates the hold on `!proc(reap)`
as well. **Fly v0.13.2, not v0.13.1**, and add one thing to the list below:

- [ ] In AoE, in the form, with Void Ray **ready** and a Star granted: does Collapsing Star wear
      `blocked`? It should ONLY when neither Reap-family proc is banked. ⚠ **No scenario in the
      walk exercises cue H at all** — every scenario reaching Collapsing Star has Void Ray on
      cooldown — so this state has never been reasoned about by a gate, only by hand.

**On a Devourer Demon Hunter** — the spec that has never been flown at all:

- [ ] The **standing virtual row** (Consume) draws at all, on cap's own strip, at the right end.
- [ ] It shows **Devour** inside Void Metamorphosis. This is `Panel.Face` resolving
      `C_Spell.GetOverrideSpell` on the draw, and it is the one thing in V12 that no test covers
      end-to-end — the catalog is silent about the transform by construction, because
      `Catalog.Check` refuses a subject predicate naming a virtual ability.
- [ ] Inside the form, the **Void Metamorphosis row draws Collapsing Star** with its count band.
      This is the 2026-08-27 measurement's whole consequence: an override borrowing the row of the
      spell it replaces. If it does NOT, the override premise is wrong and Devourer's catalog needs
      re-authoring, not patching.
- [ ] Out of form, the bank band draws the **right threshold for the build** — 35 with *Soul
      Glutton*, else 50. Two markers, mutually exclusive on `talent(soul_glutton)`.
- [ ] The **three ceded corner steps** on that row, two of them permanently blank. Expected and
      recorded; the question is only whether it reads as a fault.

⚠ **V12's `gated` kind CANNOT be flown — it has no consumer anywhere.** It was built for Collapsing
Star, which turned out not to need it. Record it as unexercised, never as passed.

**On Protection and Retribution** — the failure mode `backlog.md` already records for Destruction
is a display with no subject, which draws nothing and says nothing about why:

- [ ] Protection's **Sacred Weapon (V19)** and the **Consecration presence band** have a subject
      and actually draw.
- [ ] Retribution's **Expurgation (V20)** proc bar has a subject and actually draws. ⚠ It binds
      only if the player has added Expurgation to Tracked Buffs; if not, `aura:expurgation` reads
      UNKNOWN and the marker stays DARK, which is correct behaviour and looks identical to a
      broken one.

**Then, and only then:** delete `render-shelf.md`'s **"Not flown."** under V12 (currently `:787`).
It is the honest marker until an eye has been on it.

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
exists as the precise form when an author wants to name the exact rung — the residual question is
whether it should be *required* wherever the bare-mention path is what resolved, which would make
the loose case visible instead of silent. Not done: it would re-open every resolving display at
once, and the gate has not yet been argued with by anyone but its author.

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

- **`render-shelf.md`'s V12 section still argues from Collapsing Star, and that premise was
  measured false.** Recorded 2026-08-27, from the catalog-review residue. V12's *Why it exists*
  paragraph says Collapsing Star *"is a real press … and has no frame anywhere in the CDM pool"*,
  and its `gated` kind is defined with Collapsing Star as the worked example. Collapsing Star was
  then measured in game to be a spell **override on the Void Metamorphosis row**, so R7 draws it,
  it is not cap-owned, and it is not a virtual row at all — which is also why **V12's `gated` kind
  has no consumer anywhere** (the Devourer status entry above already says so). The one live
  virtual row is Consume, `standing`. So the shelf's justification for the primitive rests on a
  case that no longer holds, while the primitive itself is still right — Consume has no frame
  either. **This is the shelf's call and was deliberately not edited here**: rewriting V12's
  motivating example is a visual-opinion edit, and `render-shelf.md` is the one document that owns
  those. What it needs is the standing example swapped in and `gated` re-justified or retired.
  ⚠ The *other* half of the same finding is already fixed: the shelf's claim that a virtual row
  wears the hatch *"and nothing else — no scan edge, no badge"* is gone, and V12 now says plainly
  that a virtual row takes V13's scan edge, which is what the code always did.

- **Destruction has never been catalog-reviewed.** The 2026-08-25 pass reviewed five specs —
  Demonology, Havoc, Protection, Retribution, Devourer — and skipped Destruction because this file
  records it shelved. Every other spec's review found something no gate looks at, including two
  cross-cutting patterns (a hold naming a row it never checks is available; a recorded defeat that
  went stale under a later primitive) that are now a **gate** and a **habit** respectively. Neither
  has ever been run against Destruction's documents. It is cheap and it is read-only. ⚠ Do it
  **before** stage 6 authors `specs/destruction/catalog.json`, not after: the patterns are about
  the documents, and transcribing a document that carries them transcribes them too.

- **Check a SETTLED claim as hard as a hedged one — the lesson of the Light's Deliverance
  reversal, kept because it is about process rather than about Retribution.** Recorded 2026-08-27.
  A review recommended a `sealed-count-bands` on Light's Deliverance; it was authored, and then
  deleted, and both the band and the mechanic it rested on were wrong (`retribution/catalog.md`
  holds the full account). The part worth generalising is the **provenance of the mistake**: an
  agent had put an `@verify-ingame` on the threshold, and a later "settled" decision removed it,
  having closed the question by reading spell text — a source that could not answer it. The hedge
  was warranted and the settlement was not. **So a claim marked settled deserves the same scrutiny
  as one marked open, and more when what settled it was prose rather than measurement.** The
  practical form: when a marker or a defeat is removed *because a question was closed*, record what
  closed it, and treat "the tooltip says so" as evidence about wording rather than about mechanics.

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
  ⚠ **Protection's Defeats 4 and 5 both rested on this false premise and are rewritten.** The
  sweep this implies has not been done: **any catalog that declines `capped` should have its
  stated reason re-read against `Sense.readCapped`**, Retribution's first — its reason may be
  sound on other grounds, but if it cites a missing charge count it is citing something that was
  never required.

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
