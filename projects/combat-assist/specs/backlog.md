# Combat Assist Plus — backlog

**What this file is for:** the current implementation status and the ordered work list.
`spec.md` owns intended behavior; `notes.md` owns completed history; `discussion.md` owns only
questions that still require an author decision.

The live addon version comes from `wowkb.addon list`, never from prose here.

## Status

This is the project's only implementation-status source.

- **Readiness stopped being a latch (2026-08-16, after the v0.11.0 flight).** The cooldown hatch
  stuck on for a whole pull, and the cause was not the hatch — it was the readiness model
  underneath it, which the lane border has been using all along. cap latched `ready = false` on the
  CDM's `OnCooldown` alert and waited for `Available` to clear it. **`Available` is raised from the
  viewer's `OnUpdate`, and the viewer only ticks rows the PLAYER configured an alert on**
  (`NeedsOnUpdateRegistration`), so on a stock setup it never comes. Measured in the flight:
  **320 `OnCooldown` across 8 rows, 35 `Available` on the one row with an alert**, and zero
  `ChargeGained` — the same gate a second time. Before V11 this showed up as rows silently missing
  a lane border, which reads as "cap has no opinion"; the hatch turned a quiet wrong answer loud.
  - **The fix is a READ, not a better latch.** `Sense.readRowCooldown` asks the item's own Cooldown
    widget whether it is shown and `wasSetFromCooldown` whether the dial means a cooldown — two
    plain booleans, both Blizzard's verdict mirrored into widget state. `Track:World` prefers it
    over the latch; a read has no memory and so cannot stick.
  - **The symmetric edge was never in the alert channel.** `OnCooldownDone` is a widget script the
    engine fires when a swipe completes (`CooldownViewer.lua:725`), wired on every item at
    `OnLoad`, needing no configuration. `Sense` now `HookScript`s it as the ready edge, additively.
  - ⚠ **One inferred link, now in the lab:** the Cooldown widget's `IsShown()` is not yet measured
    plain in combat — its tab-2 sibling `Bar.Pip:IsShown()` is. `@pending-test:
    cdm-cooldown-widget-shown-in-combat`. Until it drains the edge latch still runs underneath.
  - **Six ClientLab tests went in with it**, covering the widget read, `OnCooldownDone`'s firing,
    the `isOnActualCooldown`/`IsOnCooldown()` field secrecy, the never-measured scratch-frame
    pattern, forced `OnUpdate` registration (the route NOT taken), and — finally —
    `IsProtected()` on a live item frame, which the anchor work has been waiting on.

- **The cooldown hatch is shipped — V11, on every row the CDM says is down (2026-08-16).** L4 was
  promoted out of the lab per Part 7 rule 4 and took the shared stripe sheet with it: the geometry
  and V11's colour and phase are `tokens.hatch`, the sheet ships to `Media/stripes.tga` under the
  tint guard, and Part 7's two remaining stripe entries borrow that one file rather than keeping a
  second copy. `verdicts.cd` gains `hatch: true` and is the only verdict that does. In the addon:
  `Signal.Evaluate` puts `oncd` on the verdict, `Treatment.For` returns `hatch`, `Paint.Hatch`
  builds it, and `Overlay.paint` shows it — under the lane border and the badges, over the icon and
  the swipe. `/cap style` gained a V11 section drawing swipe-only / hatch-only / as-it-ships /
  untreated side by side, which is the comparison the entry always asked for.
  - **The fact is the CDM's.** Readiness is the viewer's own alert edges (`Available` /
    `OnCooldown`), already latched by `Track` — cap computes no timer. **Only `false` draws**: an
    `UNKNOWN` or absent readiness draws bare, so absence of a hatch never asserts a button is up.
  - ⚠ **Two kinds of row on cooldown will not wear it**, and this is the unknown-safe direction
    rather than a bug: a **charged** ability's readiness is deliberately not latched
    (`Track:setReady` skips `charged`), and a row whose first edge has not landed yet is `UNKNOWN`.
    The hatch is not a complete census of what is down. Whether that reads as inconsistent in play
    is a flight question — Part 5.
  - **This deliberately restates Blizzard's swipe**, which V7 said cap had no reason to do. That
    was true while the swipe sat on an otherwise unmarked row; it stopped being true once
    everything around it grew a border, a badge and an arrival, at which point a stock swipe read
    as *less* marked than its neighbours. Whether the restatement earns its place is the flight.
  - **`Overlay.cell` gained a trailing `~`** for the hatch, so `id:off~` is a real state and a bare
    `off` can no longer be read as "this row drew nothing".
  - Two new `check` gates: `Media/stripes.tga` byte-matches `tokens.hatch`, and a leftover
    `Media/lab/stripes.tga` from before the promotion is a failure rather than a silent second copy.

- **Authored ordering is shipped behaviour, on by default (2026-08-16).** `probes/AnchorOrder.lua`
  was promoted to `Anchor.lua`: cap arms itself a second after `PLAYER_ENTERING_WORLD`, re-anchors
  the Essential viewer's item frames into the catalog's authored order, re-applies out of combat on
  every layout stomp and on the spec/talent/settings edges, and samples at 2 Hz. `/cap anchor
  [on|off|rows]` replaces `/capanchor`; the setting persists at `ns.db.anchor`. Demo mode is gone.
  The `anchor` capture stream is unchanged, so `wowkb.capture cap anchor` still reads it.
  **Contention now backs off rather than re-asserting** — one warning, then cap leaves the row
  alone, because two riders trading positions at 2 Hz is worse for the player than losing quietly.
  ⚠ Still **not** built: D22's always-show / un-hide half, which needs a settings write and an
  author call. And the mid-combat `RefreshLayout` teardown remains unexercised — see the section
  below for why that stopped being a blocker.
  - **The author's call, 2026-08-16:** *"we know it's possible"* — EllesmereUI repositions these
    same frames and has run for months across dungeons, delves and raids without ever falling back
    to Blizzard's layout. That is an existence proof that a tainted addon can hold a CDM re-anchor
    in combat, which retires the "unfixable" branch. Ship it; fix it if it breaks. **If it does
    break, the first thing to try is re-applying *in* combat** — `apply()`'s `InCombatLockdown()`
    guard is caution, not measurement, and the item templates declare no `protected` attribute.

- **V2's lane border is a ring flipbook, and the lanes lost their thicknesses (2026-08-16).**
  Promoted out of the lab per Part 7 rule 4: the border is one generated white-alpha sheet — 16
  frames, 4×4 grid of 64 px cells — tinted per lane with one `SetVertexColor` and stepped in place
  on the addon's single shared ticker (`tokens.motion.tick_s` 0.025 s, so the arrival lasts
  `tokens.arrival.duration_s` 0.40 s and `capart check` gates the three against each other). The
  `Scale` snap is gone from the shipped path, and with it any way for a border to draw outside its
  own row; `Paint.Arrival` survives only because Part 7's `arrival-*` entries are *about* a `Scale`.
  Every lane draws the same band (`tokens.ring.thickness_px`) and they differ by hue alone. Art
  ships to `Media/ring.tga` under the tint guard, byte-gated by `check`. **Not flown** — the three
  open questions are Part 5 question 8.

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
- **D22's positioning claim is supported by flight (2026-08-16).** cap re-anchored the Essential
  viewer's nine rows into the authored order out of combat and held it through 138 s of combat,
  `X{ok}` at both combat edges, zero displacement. ⚠ Two gaps: `RefreshLayout` never fired, so the
  in-combat pool-release path that would break it is **untested**; and a first session failed
  outright with the apply apparently never landing. Arm-time reliability, not persistence, is the
  open question. Details under `Now`.
- **The D22 instrument exists (2026-08-16).** `probes/AnchorOrder.lua` re-anchors
  the Essential viewer's frames into the authored order out of combat, hooks `Layout` /
  `RefreshLayout` / `CooldownViewerSettings.OnDataChanged`, samples drawn position at 2 Hz from
  `GetLeft()`, and records to a new `anchor` capture stream. It classifies a displacement as
  `# displaced` (a layout call cap saw) or `# contended` (no observed cause), which is what keeps a
  flight on a re-anchoring CDM skin from reading as a persistence failure. It restores on
  `/capanchor off` per §3.6's one discipline. **Nothing about D22 is answered until it is flown**;
  the probe only makes the question askable.
- **The lab is not empty (2026-08-16).** Three diagonal-stripe entries are drawn on the Havoc
  artifact, from a generated tileable white-alpha sheet. They decide nothing — Part 7 rule 3 —
  and are deliberately off the addon ship path.
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

**The probe is closed and promoted (2026-08-16).** `probes/AnchorOrder.lua` is deleted and its
question answered as far as it is going to be answered before shipping; the code is now
`Anchor.lua`, on by default, with `/cap anchor` as its verb and `tests/spec/engine/anchor_spec.lua`
under the release gate. `probes/` and `tests/probes/` are gone. What remains open below is a list
of things to notice in play, not a gate in front of the feature.

*What reading the source settled before flying, so the flight does not re-discover it:*

- **`layoutIndex` cannot be used to reorder.** `RefreshData` indexes `cooldownIDs[layoutIndex]`,
  so the sort key and the data index are the same field — swap two frames' indices and their
  cooldownIDs swap to match, so they trade identities and nothing appears to move. `SetPoint` is
  the only route, which is what this item always said.
- ⚠ **cap cannot see its own re-anchor through any existing instrument.** `GetItemFrames()` sorts
  by `layoutIndex`, and `Bind` derives row order from that index, so `Catalog.OrderCheck` and the
  `bind` stream's `# row-order` note keep reporting Blizzard's order after a successful re-anchor.
  The probe reads drawn position from `GetLeft()`/`GetTop()` instead. **Do not read the absence of
  that note as success here.**
- **The likely failure mode is named:** `alwaysUpdateLayout` is set once by `RefreshLayout` and
  never cleared, so no `Layout()` is ever a no-op, and `UNIT_AURA`'s `isFullUpdate` branch calls
  `RefreshLayout` — releasing the pool and clearing every anchor — **in combat**.
- **Always-show may not be needed for positional stability.** All four item templates set
  `includeAsLayoutChildWhenHidden`, so an inactive row keeps its grid slot and the row gaps rather
  than closing up. It is still needed so cap's overlay has something to paint on.

All four facts are in `knowledge/addon-dev/cooldown-manager.md` §4.1, source-read at 12.1.0.

- [x] **Out-of-combat re-anchoring holds.** `/capanchor on` out of combat. Confirm the row draws in
      the authored order **and** the CDM keeps rendering each frame normally (swipe, charges, glow)
      — i.e. cap moved the frames without breaking Blizzard's per-frame paint. The paint half is a
      player-eye judgment; the order half is `X{ok|MISMATCH}` in the `anchor` stream.
- [x] **Persistence through combat.** Enter combat and confirm the positions hold. `# stomp
      RefreshLayout destructive=1 combat=1` is the predicted failure and **is itself the finding** —
      after a destructive stomp the probe stops expecting anything until the next out-of-combat
      pass, so silence afterwards must not be read as "the order held".
**FLOWN 2026-08-16 (cap v0.7.0, Havoc / Fel-Scarred, Essential viewer, 9 rows). It works — with two
things unproven.** Session 2 armed at `t149057.0`: drawn order before the apply was scrambled, and
immediately after it read byte-identical to the authored order, `X{ok}`. `# combat start` at
`t149122.8` and `# combat end` at `t149261.4`, **both still `X{ok}`** — 138 s of combat, `disp:0`,
`cont:0`, `stomp:0`. Out-of-combat re-anchoring holds and it persists through a fight. **D22's
unproven claim is supported.**

⚠ **The predicted failure was never exercised.** `stomp:0` for the whole session — `RefreshLayout`
never ran, so `UNIT_AURA`'s `isFullUpdate` path (releases the pool, clears every anchor, *in
combat*) is still untested. Persistence is **supported, not proven against the named risk**. Zone
in, swap targets, or fight something aura-heavy, then grep `# stomp RefreshLayout destructive=1
combat=1`. Until that fires, treat persistence as provisional.

**Session 1 is explained, and it validates the contention detection.** The player had a third-party
Cooldown Manager **override enabled** for that session; they disabled it and session 2 is the clean
result above. Session 1 read `X{MISMATCH}` with `# contended n=5` every 0.5 s for 35 cycles,
`stomp:0` throughout — cap applied, the other addon immediately put the frames back, repeat.

⚠ **Note the signature, because it misleads.** `D{}` is **character-for-character identical across
all 35 samples**, which reads like "the apply never landed". It is not: a competitor that wins
deterministically every round produces a constant sample too, because every sample catches the
frames in *its* layout. **A failed apply and a lost fight are indistinguishable from the sampled
positions alone** — what separates them is `stomp:0` plus the fact that disabling the competitor
fixed it. Do not read a frozen `D{}` as a failed apply.

- [x] **Detect-and-warn works.** D22's standing constraint — *"a CDM re-skin that also re-anchors
      these frames fights cap for position; 'Requires no reordering CDM module' stands; cap detects
      and warns rather than silently mislead"* — is now **measured**, not asserted. The probe
      classified it correctly (no hooked layout call ⇒ not Blizzard), emitted its chat warning on
      the first occurrence, and the player acted on it. This is the behaviour a shipped version of
      this feature needs, and it exists.
- [ ] **The re-apply edges.** Spec / talent / hero swap, `PLAYER_ENTERING_WORLD`,
      `CooldownViewerSettings.OnDataChanged`. `Anchor.lua` hooks all of them and marks `# reapply
      why=<reason>`; confirm the order is restored after each.
- [ ] **The mid-combat teardown, watched rather than gated.** `UNIT_AURA` is the only layout
      teardown that reaches combat, and it is **unfiltered by unit** — `RegisterUnitEvent("UNIT_AURA",
      "player", "target")` with a handler whose first parameter is `_unit`, so a full aura update on
      your *target* rebuilds the whole layout (`knowledge/addon-dev/cooldown-manager.md` §4.1).
      What sets `isFullUpdate` is C-side and unreadable from Lua. If the order reverts mid-pull the
      capture says so: grep `# stomp RefreshLayout destructive=1 combat=1`. Not a blocker — see the
      author's call in `## Status`.
- [ ] **The missing-spell half — observation only.** `/cap anchor rows` reports which catalog
      entries have no pooled frame. ⚠ **The un-hide write was deliberately not built** and needs an
      author call: `SetCooldownToCategory` writes the player's saved CDM layout, which is the
      settings write D22 avoided ("ordering is solved by pure repositioning, with no settings write
      at all"), sits against §4's "does not replace or configure the Cooldown Manager", and carries
      an open `[gap] @verify-ingame` for whether an un-hidden row lands in a viewer end to end.
- [ ] ⚠ **Watch for `# contended`.** EllesmereUI's Cooldown Manager module re-anchors these same
      frames. A displacement with no hooked layout call behind it is marked `# contended`, not
      `# displaced`, and cap now **stops re-applying** after the first one and says so — so a
      contended row keeps the *other* addon's order and must not be read as a priority. (It can
      also mean a layout path `Anchor.lua` does not hook, e.g. the `BottomManagedFrame` container.)
- [ ] Record the player/behaviour result. If positioning cannot be made to persist, **D22 reopens**.
      Client facts (protection status, reflow triggers, un-hide route) drain to
      `knowledge/addon-dev/`, not here.
- [x] **Runtime protection: ANSWERED, and item frames are not protected.** `[client 2026-08-16]`
      `IsProtected()` returned `false, false` on 9 of 9 Havoc rows, in combat and out
      (`knowledge/addon-dev/cooldown-manager.md` §4.1). So `Anchor.lua`'s `InCombatLockdown()`
      guard on `apply()` is **caution, not a restriction**, and the mid-combat `RefreshLayout`
      teardown is recoverable in place rather than permanent until the pull ends.
- [ ] **Decide whether Anchor re-applies in combat now that it may.** Deliberately NOT changed
      with the measurement — it is a behaviour change on a feature that has flown once, and the
      teardown it would cover has still never been observed firing. The cheap version is to
      drop the guard in `apply()` and let the existing `# stomp` path re-anchor; the question is
      whether re-anchoring mid-pull is *desirable*, since a row that moves during combat is its
      own kind of wrong.

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

### Retire the veil — one condition, one surface

Author's direction, 2026-08-16: **remove the veil entirely.** Not tune it, not gate it — delete
the primitive and everything that reads it.

**The finding.** Every skip condition cap has expresses itself by dimming *the same texture*. A
readable hold, a sealed hold, `starved`, `overcap` and both graded curves all land on one veil, on
top of Blizzard's own desaturation and swipe, which dim that same icon for their own reasons. So in
flight a dark row is the sum of an unknown number of causes and you cannot see which one fired —
the surface has no capacity left to say anything. The first Havoc flight said the same thing from
two directions already: `withheld` was the weakest read in the row (Status, above), and cap's veil
is *louder* than Blizzard's swipe (**D25**).

**The fact that makes this cheap: the veil carries no information the badge doesn't.** Part 2.5
derives it — a row is veiled **iff** it wears a negative cue — so it is strictly redundant with the
badge that is already there saying *why*. Deleting it loses nothing from the reading model; Part
0.5's pass 2 simply becomes *"the leftmost entry that is neither swiped nor wearing a negative
badge is the press."*

**Nothing replaces it in this change.** Fly the row as lane border + badges over Blizzard's own
swipe and desaturation, and find out whether "skip" is still legible with the dim gone. The striped
overlays below are the candidate replacement, **not** a commitment — landing both at once means the
next flight cannot tell which change did what.

*The shelf.*

- [x] Delete **V4**. Rewrite Part 2.5: a row is a **lane and badges**; drop step 2 and the
      veiled-iff rule with it.
- [x] Delete `tokens.veil`, and **delete the `veil` key** from all nine `tokens.verdicts` entries —
      remove it, don't set it `false`, or the derivation grows back.
- [x] Rewrite the curve-driven veil (V9/V10, "one curve, two sinks") down to **one sink**, the
      badge alpha. The reason the second sink existed — a badge fading in over a veil that snapped
      on says two things about one moment — dies with the veil.
- [x] Part 0.5: rewrite pass 2 and the `withheld` paragraph so elimination reads off **the swipe
      and the negative badge**. Also `spec.md:128`, which states the same invariant.

*The tool.*

- [x] Delete `capart.py` gate **0c** (the veil-derivation reconciler) — its subject is gone.
- [x] Re-point `elimination_gate` to *swiped or negative-badged*. **Keep this one**: it is the
      reading model's invariant, not a style opinion.
- [x] `capart build havoc`, look at it, republish the existing artifact URL (`589b5eca-…`).

*The addon.*

- [x] Delete `Paint.Veil` (`Paint.lua:196-204`) and every `f.veil` site in `Overlay.lua`
      (`:23-24`, `:37`, `:156-165`), plus the graded path's veil sink (`:111-116`).
- [x] The `draw` capture's row string is `id:LANE[/veil][+cue,cue]` (`Overlay.lua:170-174`). Drop
      `/veil`, and update `flight-reading.md` — captures recorded before this read differently and
      the reader should say so rather than silently mean something else.
- [x] `capart export lua` to regenerate `Style.lua`; update the three specs that assert on the veil
      (`tests/spec/product/havoc_spec.lua`, `engine/style_spec.lua`, `engine/compose_spec.lua`).

*The decisions it closes.*

- [x] **D25 resolves by removal** — record it in `discussion.md` as *the subject was retired*, not
      as a veil weight that was chosen.
- [x] **D24 loses the stated cost of its middle option** ("keep both, drop the veil" cost the Part
      2.5 derivation, which no longer exists). Re-state the option; it does not decide itself.
- [x] Record the round in `notes.md`.

**Done 2026-08-16.** The addon carries **zero** occurrences of `veil`. The evidence the change was
safe is the elimination gate: it held on all 13 scenarios with the veil term removed, and was proved
non-vacuous by stripping a negative cue from one eliminated entry in memory, which produced exactly
one failure. Every scenario reaches the same press with only the swipe and the badge doing the work
— which is what "the veil carried no information the badge doesn't" means, mechanically.

Three things the checklist above did not name and which were load-bearing: `Treatment.lua` held the
**derivation itself**; `havoc/scenarios.md` states pass 2 and had two walk steps calling rows
*veiled*, and that prose **renders into the artifact**; `havoc/catalog.md` declared cue C2's second
sink rather than the shelf. ⚠ Also re-confirmed the sidecar gap already in Status: `build` renders
walk prose from the sidecar, so `capart import scenarios havoc` was required — `check` compares
`(name, verdict, cues)` only and passed while the walk still said "veiled".

*The flight question, stated before flying:* with no dim anywhere, can you still tell at a glance
which rows cap has ruled out — and is that read now attributable to a single cause?

### There is no positive-cue budget — say so in the docs

Author's correction, 2026-08-16: **the single-positive-cue rule is being read as a budget, and it
is not one.** The docs present it as a scarce resource — Status says the vocabulary is "negative BY
DEFAULT with exactly ONE positive cue", `capart check` gate 0b hard-fails a second
`polarity: "positive"`, and gate 0d fences positives to badge slot 3. The intent was a guardrail
against adding positives casually. The effect is that a reader reasons about *spending* the
positive, and declines to propose one that is justified. Measured: it happened in this session,
twice, in prose written to the author.

⚠ **And Part 0.5 contradicts itself on exactly this point.** Pass 1 is specified as
*"scan left to right for a POSITIVE cue. If one is present, press it."* — a **left-to-right scan
that presses the first hit**, which is an ordering rule, and ordering rules exist to resolve
multiplicity. The pass-1 `check` gate is written the same way: *"the leftmost entry wearing one must
be the press"*, a sentence that only means something if several entries can wear one. Yet the
second-positive gate forbids multiplicity on the grounds that *"two of them in one row makes pass 1
ambiguous about which to press"* — the ambiguity pass 1 already resolves by position. **The shelf
disambiguates by order in one paragraph and calls the same case ambiguous three paragraphs later.**

Only one of these can stand, and which one is an author decision:

- **Pass 1's ordering is real** ⇒ multiple positives are fine, leftmost wins, and the
  second-positive gate has no argument left. Pass 1 becomes a genuine scan.
- **Positives really are capped at one** ⇒ pass 1 is not a scan at all, it is *"is `capped`
  present"*, and the left-to-right language should go, along with "leftmost" in the gate — both are
  describing a procedure that never runs.

- [ ] **Resolve the pass-1 contradiction first** — the two branches above. Everything else here is
      downstream of it, and the branch chosen decides whether gate 0b survives at all.
- [ ] Rewrite the Status bullet and `render-shelf.md` Part 0.5 so the rule reads as **"a positive
      cue is an override of left-to-right ordering, so it carries a burden of proof"** — not as a
      count. The cost of a positive is that it breaks the reading model, and that is a per-cue
      argument, not a quota.
- [ ] Decide what happens to **gate 0b**. Options: delete it (the burden of proof is editorial, not
      mechanical); keep it as a *warning* that names the argument a second positive must make; or
      keep it hard and rename it so it stops reading as a cap — its current message is what teaches
      the budget. ⚠ Gates 0d (slot 3) and 1c (every cue is worn) are unaffected and should stay
      exactly as they are. **Gate 1b is affected** — its "leftmost" wording belongs to the
      multiplicity branch.
- [ ] Re-examine what the rule caused. `spec.md` §3.6 records a threshold as expressible in **either**
      polarity; the positive halves — cue B's "banked", the green dependency dot, the weave chevron,
      cue D's promotion — are all parked with "the permission is unchanged; what is missing is
      pixels, not authority". Check whether any of them was parked for the budget rather than on its
      merits.

### Ordering versus conditionals — ordering is cheaper to read

Author's position, 2026-08-16, and it corrects an equivalence stated in review: *"conditionals
require more mental energy than ordering, especially for items already mostly on the far left."*

Two encodings can produce **identical presses** and still not be equivalent to a player. Ranking A
above B with a condition that skips A, versus ranking B above A outright, are behaviourally the
same and cognitively are not: a badge must be seen, identified and interpreted before the eye moves
on, while a position costs nothing. The tax is worst on a **leftmost** entry, where the eye arrives
first and pays it on every scan — including the majority of scans where the condition is false.

This is a general authoring rule, not a Havoc detail, and it belongs in the model:

- [ ] State it in `spec.md` §3.1 beside eye-direction-by-elimination: **when a fact is stable enough
      to express as rank, express it as rank; reserve a cue for what genuinely varies within a
      state.** A cue that is nearly always lit is a mis-ranked row wearing a badge.
- [ ] Apply it to **Metamorphosis vs Eye Beam** (see below). Meta sits leftmost and wears
      `meta_wastes_eye_beam` / `meta_wastes_death_sweep` whenever either is ready — a badge on the
      first thing you look at, most of the time. Ranking Eye Beam above Meta says the same thing for
      free. ⚠ This changes the authored order, and the order is the argument, so it wants
      `catalog.md` + `scenarios.md` + `Catalogs/Havoc.lua` moving together — and D26's caution
      applies: decide it from the APL, not from a page whose order is a rendering artifact.
- [ ] Re-audit the rest of the Havoc row for the same shape — any marker that is lit in most states
      is a candidate for becoming rank instead.

### Diagonal stripes — cap hinting *against* an ability

Author's direction, 2026-08-15/16. **This is a new statement, not a veil replacement.** The veil
said *"skipped"* as a global consequence of the cue vocabulary; stripes say something narrower and
more specific — **cap is hinting against pressing this ability** — and they say it by stating a
condition across the icon rather than by subtracting light from it. The veil retirement above
stands on its own and lands first; if it turns out nothing needs to replace it, this work is still
worth doing on its own terms.

> ⚠ **Build this per-render. Do not build it the way the veil was built.** No `stripes` boolean on
> `tokens.verdicts`, no derivation from cue polarity, no shared "is this row striped" state that
> several conditions write to and something else reads back. **Each render that hints against its
> ability draws its own stripes, in its own render path, owning its own parameters.** That is the
> whole point: when a striped row shows up in flight, the stripes belong to exactly one condition
> and you can say which. A global that three conditions feed is the failure being removed above,
> re-created in a new colour.

**This is Part 7 lab work first** — nothing here may be named from `verdicts`/`cues` until it is
promoted by being *moved* into Parts 1–6 (shelf rule 4, enforced by `capart build`). Each entry
needs an `asks`.

**The three lab entries are drawn and on the page (2026-08-16):** `stripes-l3-hold`,
`stripes-l4-cooldown`, `stripes-l5-starved` in `render-shelf.md` Part 7, rendered into the Havoc
artifact. The sheet is generated by `capart.stripe_sheet` — 128 px tile, 16 px pitch, duty 0.5,
45° — and each entry supplies only its own colour and its own `mask-position`, which is the CSS
analogue of `SetVertexColor` + `SetTexCoord`. **The asset is the only shared thing**, as this
section requires. L4 sits half a period off L3, verified complementary: 0 px overlap and 0 px gap
across a 32 px span, so the both-at-once cell interleaves rather than fights.
⚠ Two things the drawing does **not** settle, both deliberate: it is **not on the ship path**
(no TGA, not in `export_badges`, not in `check`'s gate-3b list — the lab has no authority), and the
hold/starved cells are authored as verdict `below` plus explicit cues rather than the real verdict
names, because those still carry `veil: true` until the veil retirement lands. Moving them is a
one-line edit afterwards.
⚠ Finding worth keeping: **supersample-then-downsample does not tile.** Pillow's LANCZOS kernel
clamps at the image edge instead of wrapping, so the last row/column gets anti-aliased against
nothing and leaves a visible seam. The generator draws a one-pitch margin on every side and crops
it after the downsample. Measured: alpha depends only on `(x+y) mod pitch` across the whole tile.

- [ ] **L3 — red stripes on the sequencing hold.** A row held for a cooldown (`hold-readable` /
      `hold-sealed`) draws its corner badge **and** red diagonal stripes across the icon face.
      Drawn by the hold's own render, not by a rule about holds.
- [ ] **L4 — black stripes on a detected cooldown.** A `cd` row draws black diagonal stripes on the
      **complementary** phase of L3's, so a row that is *both* held and on cooldown reads as
      alternating red/black — two conditions visibly present at once, which is the thing a single
      shared surface could never show. Note this is cap drawing on a `cd` row for the first time
      (`tokens.verdicts.cd` draws nothing today, on the theory that Blizzard's swipe already ruled
      it out). **D25** closes with the veil, but its underlying question returns here in a new
      form — is cap restating the swipe, or adding to it? That is a flight question, not a
      paper one.
- [ ] **L5 — red stripes on `starved`.** A row lacking the resource to cast draws red stripes from
      *its own* render. It uses the same red as L3 because it is the same kind of statement — not
      because a rule says every negative thing is red. If after flying all three it turns out the
      three renders are drawing something identical, **that is an observation that may earn a shared
      recipe later**, not a rule to author up front.
- [x] **It is a texture, not drawn geometry.** Do not build stripes out of a pile of thin quads per
      icon — that is many frames per row, it costs per-icon anchoring, and axis-aligned
      `SetColorTexture` cannot make a diagonal anyway. **One tileable white-alpha stripe sheet**,
      and each render calls it.
      - **Blizzard has no such art — checked 2026-08-16.** `wowkb.uiart find` returns only
        `auctionhouse-rowstripe-1/2` (16×18 table row banding) for *stripe*, four Soulbinds tree
        connectors for *diagonal*, and nothing at all for *hazard* / *hatch* / *caution*. So this is
        ours to author, by Part 4's rule: **generate it from a script beside the shelf**, the way the
        badge disc and halo already are — regenerable rather than a binary mystery, saturation 0.000
        by construction, and it ships through the existing `capart export` path as TGA.
      - **The asset is the only shared thing, and it carries the coupling for free.** Red and black
        must agree on angle and pitch and take complementary phase or they will not interleave.
        One tiling sheet gives all of that: **each render passes its own colour (`SetVertexColor`
        multiplies white-alpha to anything, black included) and its own `SetTexCoord` offset —
        half a period apart is the complementary phase.** No shared state, no boolean, no
        derivation: one file on disk, and two renders that each ask it for something different.
- [ ] **No dim comes back with them.** Stripes state a condition without subtracting light. The
      generated HTML's job stays **CDM-like icons with CDM-like swipes and counts**, with cap's own
      marks on top.
- [ ] **Add a shelf section for the effects Blizzard already puts on CDM icons**, read off the
      Tier-1 source we already hold at
      `raw/addon-research/wow-ui-source-12.1.0/Interface/AddOns/Blizzard_CooldownViewer/`
      (`CooldownViewer.xml`, `CooldownViewerItemData.lua`, `CooldownViewerAlert.lua`,
      `PandemicAlertAnimation.xml`, `CooldownViewerVisualAlertTarget.lua`) — swipe, charge/count
      text, desaturation, the proc/visual alert overlay, pandemic alert, and their layers. It is
      the inventory of what cap gets for free and must not restate or fight, and the artifact reads
      it to draw a faithful row. Client facts drain to `knowledge/addon-dev/cooldown-manager.md`;
      the shelf section is the *rendering* view of them.

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
