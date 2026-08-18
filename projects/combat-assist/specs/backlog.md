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
  row as **lane + badges**, leaves Blizzard's proc glow intact, and owns one independent Tyrant
  bar. Sealed facts reach client-owned display sinks only, never a Lua branch.
- A catalog's tier names *are* the shelf's lane names — **COOLDOWN / ROTATION / FALLBACK** — with
  no mapping table between them (`Treatment.LANE` was deleted rather than made an identity map).
- Engine guarantees and provisional per-spec examples are separate test groups.

### The style

- **The style is lane borders + corner badges, over Blizzard's own swipe and desaturation.** The
  veil is deleted; the addon carries zero occurrences of `veil` (2026-08-16). `render-shelf.md`
  declares it, `capart export` generates `Style.lua` and the badge / ring / hatch art from Part 6,
  and `capart check` fails on a committed asset that disagrees with the shelf. `Paint.lua` holds
  one builder per primitive and both the live overlay and `/cap style` draw through it.
- **V2's lane border is a ring flipbook** (2026-08-16): one generated white-alpha sheet, 16 frames
  in a 4×4 grid, tinted per lane and stepped in place on the shared ticker so the arrival lasts
  `tokens.arrival.duration_s`. Every lane draws the same band; lanes differ by hue alone. Nothing
  scales, so a border cannot reach a neighbouring row. **Not flown** — Part 5 question 8.
- **V11's cooldown hatch is shipped** (2026-08-16), on every row the CDM says is down.
  `verdicts.cd` is the only verdict carrying `hatch: true`, and **only `false` draws** — an
  `UNKNOWN` or absent readiness draws bare, so absence of a hatch never asserts a button is up.
  ⚠ A **charged** ability and a row whose first readiness edge has not landed will not wear it, so
  the hatch is not a complete census of what is down. **Not flown** — Part 5 question 9.
- **The cue vocabulary is negative by default with one positive cue** (`capped`, gold, badge
  slot 3). The three negatives — `blocked`, `starved`, `overcap` — share one red and are told apart
  by shape. `press`, `press-promoted` and `below` render identically: the press is not a thing cap
  draws. ⚠ The one-positive rule is **under review** — see *There is no positive-cue budget*.
- The reading model is mechanised rather than minuted. `capart check`'s `reading_gate` is an
  ordered chain: a scenario wearing a positive cue is judged by pass 1, every other scenario by
  pass 2 — the leftmost entry that is neither swiped nor wearing a negative badge must be the
  press. A scenario that stops leading the eye to its press fails **by name**.
- The two Warlock context dots (`dreadstalkers`, `grimoire`) are still evaluated and still reported
  in the `draw` capture's `M{}`, but **draw nothing**: the cue set is closed and they have no key.
- Part 7's lab holds two diagonal-stripe entries (`stripes-l3-hold`, `stripes-l5-starved`), drawn
  and deciding nothing. They borrow V11's shipped stripe sheet rather than keeping a second copy.

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
  2 Hz, and **backs off after one warning** when another addon contends for the same frames.
  `/cap anchor [on|off|rows]`; the setting persists at `ns.db.anchor`.
  - **Flown 2026-08-16** (cap v0.7.0, Havoc / Fel-Scarred, nine Essential rows): the drawn order
    read back byte-identical to the authored order right after the apply and again at both edges of
    a 138 s fight, `disp:0 cont:0 stomp:0`. ⚠ `RefreshLayout` never fired, so the in-combat
    pool-release path that would break it is **untested** — persistence is supported, not proven.
  - ⚠ **Not built:** the always-show / un-hide half. `SetCooldownToCategory` writes the player's
    saved CDM layout, which the ordering design deliberately avoided, and it needs an author call.
  - `Anchor.lua`'s `InCombatLockdown()` guard on `apply()` is **caution, not a restriction**:
    `IsProtected()` returned `false, false` on 9 of 9 Havoc rows, in and out of combat
    (`knowledge/addon-dev/cooldown-manager.md` §4.1).

### The specs

- **Havoc / Fel-Scarred is the live spec.** `Catalogs/Havoc.lua` carries twelve entries in authored
  priority order; Aldrachi Reaver is a separate future catalog and correctly gets nothing. What
  draws: twelve lane borders (three purple `CHARGES`), the holds on Metamorphosis / The Hunt /
  Essence Break / Vengeful Retreat, `starved` on the two Fury spenders, Immolation Aura's gold
  `capped` and its single-target skip badge, the arrival snap, the cooldown hatch, and the
  generators' graded overcap readout.
  - **The composition seam held.** Adding the holds and the graded curves edited neither
    `Treatment.lua` nor `Overlay.lua`'s cue vocabulary — `authoring.md` stage 6's renderer test,
    passed repeatedly.
  - **Re-sourced from the Tier-1 simc APL on 2026-08-17**, which corrected several rules and
    reversed one. `specs/havoc/catalog.md` → `## Changelog` is the record, and its *Open facts*
    section owns every unmeasured Havoc fact. **The row has not flown since.**
  - The Havoc design lives in three files — `catalog.md` (normative), `fact-classification.md`,
    `scenarios.md` — which is the standing violation of `authoring.md` §0's one-catalog rule.
- **The Havoc row flew once, 2026-08-15** (cap v0.4.0, Fel-Scarred, on EllesmereUI), against the
  pre-APL catalog. Its structural finding — the reading model assumes the CDM's row order matches
  the authored priority — is what `Anchor.lua` was built to answer.
- Demonology remains the small pilot: Tyrant and Demonbolt are its only enhanced entries,
  Dreadstalkers and Grimoire are readable Tyrant dependencies. Destruction / Diabolist is the
  minimal sealed proof — Conflagrate tiering plus an independent sealed Backdraft count through
  Blizzard's 12.1 AuraContainer path. **Neither has ever flown as a cap build.**
- **Cue D (demon-form promotion) and cue B's positive "banked" half are authored and not drawn.**
  A promotion is a positive cue and `press-promoted` renders identically to `press`. The permission
  is unchanged; what is missing is pixels, not authority.

### Tooling

- `wowkb.capart` renders the artifact and the addon's `Style.lua` from the docs, and `wowkb.serve`
  closes the *edit the shelf → look* loop. ⚠ **The scenario sidecar is on the build path**: `build`
  renders scenario prose *from* the sidecar while `check` compares doc against sidecar on
  `(name, verdict, cues)` only, so **prose edits to `scenarios.md` do not reach the artifact and no
  gate notices**. Run `capart import scenarios havoc` after editing prose, not only after editing a
  row. Closing that gap is a work item below.

## Now

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
      addon winning the frame, and cap stops re-applying after the first one — so a contended row
      keeps the *other* addon's order and must not be read as a priority. (It can also mean a
      layout path `Anchor.lua` does not hook, e.g. the `BottomManagedFrame` container.)
      ⚠ **A frozen sample is not evidence of a failed apply.** A competitor that wins
      deterministically every round produces a byte-identical `D{}` across every sample, because
      each sample catches the frames in *its* layout. `stomp:0` is what separates the two.
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
is the inventory of what cap gets for free and must not restate or fight, and the artifact reads it
to draw a faithful row. Client facts drain to `knowledge/addon-dev/cooldown-manager.md`; the shelf
section is the *rendering* view of them.

### Close the sidecar prose gap in `capart check`

`check` compares doc against sidecar on `(name, verdict, cues)`, so scenario **prose** can drift
ahead of the rendered artifact with no signal — measured twice, once on a citation fix and again
during the veil retirement, when the walk still said "veiled" and `check` passed. Either compare the
rendered extras too, or have `build` read prose from the doc rather than the sidecar.

### Teach `Catalog.OrderCheck` what it is actually checking

It compares the catalog against Blizzard's `layoutIndex` and reports as though that were the drawn
order. Since `Anchor.lua` shipped that is no longer true even on a stock setup — `GetItemFrames()`
sorts by `layoutIndex`, so every instrument cap owns is blind to a `SetPoint` re-anchor by
construction, and under a competing CDM skin the check is neither right nor wrong but blind, which
is the worse failure. At minimum its capture note should say which order it read.

### Split the Immolation Aura charge question in game

The 2026-08-15 flight's capture carried `immolation_capped` ×40 and `immolation_recharging` ×58 on a
loadout the player says had **no A Fire Inside** — a genuine contradiction that is still unexplained.

⚠ **State it accurately, because the first two explanations were both wrong.** `Sense.lua:105`'s
`maxCharges <= 1` guard is **pre-existing**, so on a one-charge build `capped` is **UNKNOWN**, not
`true` — the gold badge would have been *withheld*, not stuck on. So "the guard is not holding" is
not the hypothesis; either a different loadout was flown, or the client reported more than one
charge, or the badge came from somewhere else.

- [ ] `/reload` on the single-target loadout and read the `draw` capture. No `CHARGES` lane and no
      charge cue means the flight was simply on the AoE build; anything else is a real bug.

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
- [ ] It also carries the shipped-but-unflown style: the ring flipbook (Part 5 q8) and the cooldown
      hatch (q9), plus q1, q3 and q6.

### Consolidate the three Havoc docs into one `catalog.md`

The one-`catalog.md`-per-spec rule is `authoring.md` §0 and Havoc is the standing violation of it.
Fold `scenarios.md` + `fact-classification.md` back into `catalog.md` and make `rotation.md` the
sole home of the priority order. The scenario-stepper artifact renders whatever the consolidated doc
says.

### Close out the migration artifacts

`simplification-plan.md`, `simplification-audit.md` and `rule-split-audit.md` are temporary and are
not product authorities. Delete or archive them, and remove the obsolete modules, fields and
vocabulary that were kept as compatibility scaffolding for an unreleased design.

### Judge the two unflown Warlock surfaces

Neither Demonology nor Destruction has ever flown as a cap build, and two questions are waiting on
that rather than on any code.

- [ ] **Does the independent Tyrant countdown bar earn its screen space?** If it does, it is the
      canonical *spell duration object → client-owned countdown* example. If it does not, keep the
      duration-object recipe in `knowledge/addon-dev/` rather than preserving dead product code.
- [ ] **Fly the sealed Backdraft marker in restricted combat.** Record the player's visual judgment
      first and use the capture only to prove which route armed — an accepted secret sink is not
      evidence that a pixel appeared.

## Ideas

- **The empowered-cast (Demonsurge) cue — an optimisation over the baseline, not part of it.**
  Havoc's rung 3 has three holds and the catalog draws two. The third is
  `!action.death_sweep.demonsurge_available & !action.annihilation.demonsurge_available` — *don't
  recast Metamorphosis while empowered casts are still owed* — and nothing on the row says it.
  `proc` already exists in `Catalog.PREDICATES`, so **if** an owed empowered cast surfaces as a
  readable proc on the row, this is a marker and not a mechanism. That "if" is the whole of the
  work: measure first (`specs/havoc/catalog.md` → *Open facts* 6), then author. **Do not build it as
  part of the Havoc baseline** — the baseline ships without it and is coherent without it.
