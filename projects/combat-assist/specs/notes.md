# Combat Assist Plus — notes

**What this file is for:** the record of what we did — one short entry per round of work,
newest first, dated. It exists so a future reader can find out *why* something is the way it
is without re-deriving the argument. It is **not** a second spec and it is **not** a status
board.

**The fixed form. Every entry uses it, ~25–35 lines, hard ceiling 40:**

```
## YYYY-MM-DD — <short headline>

**What changed.** One or two sentences, plus the files touched as a bare list.
**Why it still binds.** The one argument a future reader must not re-derive — or, if
nothing survives, "nothing; superseded by <X>" and stop.
**Caveat.** Optional single line: what is unmeasured, what was deliberately not done.
```

**The rules that keep it flat:**

- **Past tense only. A notes entry never states a rule in normative form.** A rule lives in
  `spec.md` or the catalog; notes **cites** it. This is the rule that stops notes becoming a
  second spec, and it is the one that erodes first.
- **A reversed decision gets a one-line `⚠ SUPERSEDED:` pointer at the head of its entry**,
  not a correction buried in the prose.
- **Never quote DOCUMENT TEXT that is not in git history** — a line of `spec.md`, a catalog
  rule, a test name, a comment. This file is the historical record and an unverifiable
  quotation of our own prose is the one thing it cannot afford. If the text was only ever in a
  working tree, describe the edit instead. ⚠ **This does not cover primary sources** — what a
  player said in play, a flight report, an observation. Those are evidence, they were never in
  git and never should be, and quoting them verbatim is the point: paraphrasing a player's
  words into our own vocabulary is how a report becomes a conclusion.
- **Status does not live here.** Where the code is, what has flown, what the live version is:
  `backlog.md` → `## Status`, and nowhere else.
- ⚠ **A fact about how the game or the API behaves does not stop here.** That goes to
  `knowledge/addon-dev/` (see the wow-developer skill) — this file records *our* work, not
  the client's behaviour.
- No busted/luacheck counts, no mutation lists, no comment:code ratios, no "considered and
  declined". Cut the argument that `spec.md` and `discussion.md` already carry.
- **An entry is not permanent.** This is a log, and a log gets reset. When an entry's argument
  has landed in the file that owns it — `spec.md`, a catalog, `render-rationale.md`,
  `flight-reading.md`, `knowledge/addon-dev/` — the entry has done its job and goes. Mine
  before you delete; the deletion is the cheap half.

**The standing order is `simplify → draw → add detail from play`.**

---

## 2026-08-19 — both Warlock pilots replaced by comprehensive catalogs

**What changed.** Demonology / Diabolist and Destruction / Diabolist were re-authored from the
Tier-1 12.1 simc APLs through `authoring.md` stages 1–5, each as three files, twelve scenarios and
a registered preview. Stage 1 came first: both `rotation.md` files were still citing dead pre-12.1
profile URLs, and the Destruction APL turned out to have moved (`8ec56ea`, 2026-08-18) — the
regeneration deleted a Chaotic-Inferno Incinerate rung an earlier reading carried, and widened two
AoE gates. Files touched:

- `knowledge/classes/warlock/{demonology,destruction}/{rotation,builds,simc-apl}.md`
- `specs/demonology/{catalog,scenarios,fact-classification}.md`
- `specs/destruction/{catalog,scenarios,fact-classification}.md`
- `specs/{spec,backlog}.md`, `tools/wowkb/capart.py`

**Why it still binds.** Three findings a future reader must not re-derive.

**One unwritten S-form covers four sealed facts.** Demonic Core's stack count, Wild Imps', and
Backdraft's two-stack rung all want the same thing: a step curve on an aura **application count**,
the way S4 already runs one on a cooldown-remaining duration. cap's only aura-stack form paints a
number and is hard-limited to `min = 2`. None of these is a platform limit — the secret is a
number and §3.6 says a threshold on a secret is expressible — so the shape is named in both
catalogs' *Defeats* and deliberately not prebuilt.

**Position decides whether a transform costs a marker.** Both specs carry Infernal Bolt as an
override, from one spec-conditional Tier-1 string. On Demonology it rides the rightmost row and
outranks its left-hand neighbour, so Demonbolt needs a cross-row `identity` hold — the first
marker in any catalog to read another row's identity. On Destruction the same transform rides the
last row and its two rungs are adjacent, so it costs nothing.

**Destruction's sealed lane came out empty**, and that is a consequence rather than a virtue: no
rung reads another ability's cooldown remaining, Soul Shards are readable, and the single-target
Backdraft rungs ask whether the aura is absent rather than how many stacks. Every marker in that
catalog is a readable Lua condition — a first.

**Caveat.** Stages 6–8 did not run: no catalog Lua of the current design, no tests, no flight. Two
questions were carried back to the author rather than decided — an execute-range predicate for
Shadowburn (the same unmeasured `isUsable` read Devourer waits on), and whether Blizzard's own
`unusable` tint should count as a third eliminating signal in the reading model.


---

## 2026-08-19 — Devourer got a preview, and the virtual row got drawn

**What changed.** Devourer was registered in `capart`'s `SPECS_BUILT` and its ten scenarios
(B-1…B-5, M-1…M-5) were transcribed out of the older prose grammar into the one the scraper reads,
so `devourer-stepper.html` renders. Three mechanical things had to move for it: a *Bound abilities*
table was added to `devourer/catalog.md` (the parser reads exactly one table shape and the spec had
none), `parse_row` learned `‖` as a seam marking a **virtual row**, and the scenario-id pattern
widened to accept a one-letter prefix, which `B-n` / `M-n` needed. Files: `tools/wowkb/capart.py`,
`specs/devourer/catalog.md`, `specs/devourer/scenarios.md`, `specs/render-shelf.md` (V12 prose plus
two `preview` token groups), `previews/template/stepper.js`, `previews/template/shelf.css`.

**Why it still binds.** The preview draws a virtual row **inline in the row**, which the client does
not do — in game the panel is a separate surface and that separation is what says *cap owns this
frame*. A flat page loses the separation, so the tick carries the bit instead. That is why the tick
lives in `tokens.preview` and not in the style: `NOT_THE_STYLE` excludes the key, so the addon
cannot draw it. The seam grammar is deliberately narrow — two seams or none, panel bracketing the
Essential line — because one seam cannot say which side cap owns.

**Caveat.** The page is for **review, not record**: nothing on it has flown, and the gates prove
only self-consistency. **M-3's row was derived, not authored** — the doc had it as a prose delta on
M-2 — and every place the authoring docs doubt themselves now carries a loud `⚠ UNSURE` block on
the page rather than a footnote in the markdown. No `Catalogs/Devourer.lua` was written and no
release was cut.

---

## Before that: no entries

**Reset 2026-08-17.** The previous 28 entries, dated 2026-08-08 → 2026-08-16, were mined and
removed: their durable arguments now sit in `render-rationale.md`, `backlog.md` → `## Status`,
`flight-reading.md` and `knowledge/addon-dev/`. An empty log is this file's correct resting state
after a reset, not a defect.

The full pre-reset text, and the 18 entries before *that* which the 2026-08-08 window migration
already superseded:

```
git show 671fb68:projects/combat-assist/specs/notes.md
git show a33e152:projects/combat-assist/specs/notes.md
```

## 2026-08-22 — Demonology built, and three sealed-display primitives promoted

`Catalogs/Demonology.lua` of the current design ships: nine entries in the authored priority
order, transcribed from `demonology/catalog.md`, with fourteen scenarios in `scenarios.md`.
`authoring.md` stages 6 and 7 have run; stage 8 has not. The pilot is gone from the addon, and the
engine specs that had been riding it now ride `tests/fixtures/engine_catalog.lua` instead — an
engine guarantee that rests on a shipped roster breaks the day that roster is authored.

Four treatments left `render-shelf.md` Part 7 to make it possible, as **V16** (the banded count
and its mark), **V17** (the complement), **V18** (the sealed radial) and **V19** (the refresh
window). `composites` was deleted rather than promoted: it was the argument that those four
compose on one row, and its subject is now a real spec's walk. `duration_band` stays.

Three things worth remembering:

- **Nothing new was learned about the client.** Every measurement was in hand on 2026-08-21. What
  was in the way was that a catalog may not cite a lab entry, so the fact was expressible and
  unusable at the same time. Promotion is a pipeline step and it was the whole cost.
- **A sealed fact can now eliminate a row.** The reading model has three eliminating signals
  instead of two, and `capart check`'s elimination gate knows about the third explicitly. That
  closed `demonology/catalog.md`'s second defeat and made DEM-13 and DEM-14 writable.
- **`player-aura-stacks`'s `min = 2` was never a platform limit** — it is what the client does
  when no formatter is passed. The kind is retired; Destruction's Backdraft migrated mechanically
  and draws exactly what it did.

Two defects the work surfaced and fixed, neither of which had a symptom: a container display
carrying a readable gate armed **nothing at all** (`Overlay.configure` tested `not marker.when`,
and only the graded path consumed `verdict.gates`), and V14's `tint: "lane"` meant the one
primitive whose whole advantage is being neutral was the one going unguarded by the tint guard.

## 2026-08-22 — v0.12.0 drew nothing, and a pure suite could not have caught it

The Demonology flight got no flight: cap loaded, Anchor re-ordered the viewer, and **not one
pixel drew** — no badges, no scan edges, no hatches, no keybind labels.

`wowkb.capture cap tier` named it in one line:
`# listener-error i:3 Overlay.lua:232 attempt to call a nil value`. `badge:SetPoint` does not
exist. `Paint.Badge` returns a plain TABLE with `Show`, `Hide` and `Step`, and the flowing badge
stack (2026-08-19) started re-anchoring through a method nobody added.

**It shipped invisible for three days because the only catalog anyone ran declared no cues.** The
Demonology *pilot*'s two markers carried none, so `wanted` was always empty and the stack loop
only ever reached its `badge:Hide()` branch. The first catalog with cues took the whole of
`paint()` down on its first row — and `Sense.fireVerdicts` pcall-protects its listeners by
design, so the error reached the capture and nobody's screen. Havoc and Retribution would have
hit it identically; neither had flown since.

Three things worth keeping:

- **A pure suite is structurally blind to this.** `mock_ns.lua` is right that nothing needing a
  `CreateFrame` stub belongs in it, and the consequence is that no test here can ever construct a
  badge. So *cap calling a method its own constructor does not define* had no guard at all.
  `tests/spec/engine/surface_spec.lua` is that guard and it is deliberately **textual** — it
  checks the source, because there is nowhere else to check.
- **The protective pcall is correct and it is also what hid this.** A bare error on the 10 Hz
  tick re-throws forever, so the guard has to be there; what it costs is that a total draw
  failure looks like silence. The capture is the only thing that closed the gap between "nothing
  works" and a file and a line — which is the whole argument for the capture standard.
- **The reachability, not the code, was the risk.** The call was wrong the day it was written;
  what changed was a catalog declaring a cue. A branch no shipped data reaches is untested no
  matter how many tests pass.

## 2026-08-24 · AnimationGroups everywhere, and the DoT gets two states

The drain pass's ruling — motion on a handed-over region survives only inside an AnimationGroup
armed before the handover — became the house rule for ALL motion: `Paint.FlipBook` wraps the
client's FlipBook animation, the promotion ring and the badge strips walk their sheets through
it, and the shared `C_Timer` stepper plus `Paint.FrameIndex` are gone. `capart export badges`
now bakes a `strip_<cue>` sheet for every multi-frame cue (one today: `capped`), and
`style_spec` textually asserts Paint re-acquires no ticker. FlipBook's setters are Tier-1
generated docs; its walk semantics are a source read, so the whole conversion is `--@unverified`
until a flight eyeballs the capped badge and the ring.

Review-driven shelf changes, three rounds in one day. V19 became a **two-state DoT pair**:
aura up but outside its refresh window draws a gold do-not-refresh hatch (`SetDurationText`
band tables on remaining seconds, threshold = an optional catalog `outside_s` — the seam
against the client's real window edge is documented, and L7's seconds-form inversion is thereby
promoted); inside the window, the badge at cue-badge brightness exactly — the `fire` glyph
(deliberately shared with `priority`: both say "act now", and the window badge is a
client-decided promotion; the old `timer_CW_75` glyph was a static clock whose baked wedge read
as a live radial attached to nothing, retired for lying) with the FULL positive-cue treatment
— V14's promotion ring plus the halo; the halo alone read as a faint gold mist beside a real
promotion, which a frozen-phase A/B in the preview made undeniable. Two things were drawn on it and removed the same
day: a flame flipbook (replaced by the halo, which carries the established light-behind-a-badge
grammar) and a client-seconds countdown (the window's presence IS the statement; removing it
also removed the unflown one-button sink-pair question — which the dial, below, brought back
in bar form). V16's positive direction lost its gold
hatch (a hatch means *ruled out*, and `Channel.CountRules` now refuses `hatch` on a
non-negative band); the numeral in both band directions sits on the badge plate, its own
`plate` element/slot, because a plate escape cannot sit under text within one string; V17's
gallery swatch states the count itself in red rather than a glyph. **V18 was re-formed** the
same day out of the one-round lab entry `segment_bar`: the radial became a segmented
left-to-right bar on the row's bottom edge, flipping the whole bar to the negative red at max
via `Channel.BarFlipRules` + the generated `bar_full` crop (the crop-revealed-tip variant was
rejected — a capped-stacks warning wants the whole bar), which also ended DEM-8's corner
collision. The gallery block moved out of the shared stepper.js into `template/gallery.js`,
embedded on primitives.html alone — its ~10 KB rode every spec page and havoc was over budget
(`bareItem` stayed shared: the lab's cell builders read it too, which the split briefly broke).

**2026-08-24, later: V19's badge glyph became the dial.** The static `fire` glyph said nothing
the ring and halo were not already saying; it is replaced by a **real radial countdown of the
DoT's remaining lifetime** — a `StatusBar` child of the pandemic wrapper handed to
`SetDurationBar`, whose whole apply path is `SetTimerDuration(auraDuration, interpolation,
options.direction)` with `direction = RemainingTime` (KB §3.5.2, written back first,
symbol-anchored). Cap reads nothing: the bar's value is sealed and the client drains it.
`SetMinMaxValues(0, 1)` is called FIRST (`ApplyDurationBar` never does — §4.8.1 finding 3),
the fill's `SetStatusBarTexture` success bool is checked (house rule 8), and Radial render
mode is pcall'd with linear fallback. This is the retired `timer_CW_75` wedge's claim made
TRUE — the wedge was static art pretending to be a timer; the dial is a value the client
drains — and it deliberately re-opens the one-button sink-pair question the countdown's
removal had closed: `AddPandemicRegion` + `SetDurationBar` on ONE button is unflown, each half
measured alone (Part 5 #11, `--@unverified` in `windowSink`). The widget lives INSIDE the
handed-over wrapper, which is what scopes it to the refresh window. `tokens.pandemic` lost
`frame`/`size_px` and gained `dial` (gold arc, dark track); the pandemic entry left
`BORROWED_FRAMES` (`fire` stays on the sheet as `priority`'s own frame); the preview draws the
dial as a JS-driven conic-gradient that counts down live over a nominal looping window,
because a static wedge in the swatch would be exactly the lie the wedge was retired for.

**2026-08-24, the stepper-feedback round.** The pilot played the demonology steppers and the
findings became vocabulary. (1) **The ramp reads as a hold now**: Grimoire, Doomguard,
Dreadstalkers, Tyrant and Hand of Gul'dan wear a new `building` card (Kenney
`card_outline_lift`) over the red hatch while Tyrant is ready below five shards — authored
PAST the unconditional APL rungs, the pilot's explicit relaxation of the earlier
"don't negative-cue half the row" stance, unbudgeted on the density rule's own
starved/overcap grounds, playtest-gated. (2) **`noproc`** (Kenney `card_outline`, the empty
card slot) replaces `blocked` on Demonbolt's core hold — "nothing to wait on" is not "wait".
(3) **The dogs' two-sided band** — `Channel.BandPoints`, `Catalog.Check` relaxed to accept
`beyond < within` — closes the catalog's Defeats item 1 by its own named recipe; DEM-15 is the
dead-zone scenario. (4) **V20, the proc dial**: V19's dial standing alone (plate + arc, no
promotion treatment) on a `sealed-proc-dial` slot; Demonic Core on Demonbolt is the consumer,
and the pilot's question "is DEM-8's dial the Core's duration?" had the answer NO — that one
is Doom's — which is exactly why the Core got a dial of its own. (5) **Part 2.5's cession
rule**: corner sealed displays claim stack slots 0..n−1 by declaration (static, because shown
is sealed) and cue badges start below; wired through Overlay/Channel (`cornerSlot`) and the
preview. (6) The scenarios now wear the **Implosion imp band** wherever imps are out — the
"no markup on Implosion like I'd expect" gap: every off-mode-only Implosion row had been
implicitly claiming six-plus imps — via a new `{count: N}` scenario-grammar group, and fixing
DEM-13's latent Tyrant-ready/Tyrant-far contradiction, which the new ramp cues made visible.
Nothing flown; the acceptance set grows by the dial pair, the three-point band, and the
cession geometry.

**2026-08-25, the second stepper round — the dial becomes a bar, and the counts get their
colors.** Four findings from playing the previous night's build. (1) The imp count drew GOLD
in the preview on held rows while the addon drew RED — the preview's hue rule keyed on the
verdict where the client keys on the BAND's polarity; the scenario grammar now states which
band fired (`{count: 3-}` / `{count: 6+}`) and the preview follows it. (2) The imp band
**recolors instead of clearing** at six: the empty upper band made a loaded Implosion
identical to an unremarkable one (DEM-12's report, "missing all the golden imp count"), so
the numeral now turns gold at the threshold — hue alone carries the verdict, and a positive
band still may not hatch. (3) **V20 re-formed from corner dial to proc bar after one day**:
gold in the badge column, where hue is polarity (V5.1), read as a verdict arguing with the
red hold on exactly the rows the countdown matters (DEM-10's "really muddy") — the pilot
picked the duration-bar option, so the proc's clock is now a thin client-drained bar directly
above V18's charge bar (static lift from declarations; the corner claim released, Demonbolt's
corner back to the window badge alone). `tokens.pandemic.dial` stays — V19's badge dial was
never the problem. (4) The same kind rides the Shadow Bolt row as `ib_art_clock`: the armed
Art's remaining lifetime under Infernal Bolt — the aura id (432794, Mother of Chaos) is
**Tier-3-sourced** and a wrong id dies silent, which makes it the flight's cheapest
falsification. Two stacked client-drained bars on one bottom edge are unflown, as is the 3 px
bar itself.

## 2026-08-25 — the lanes leave the model

**What changed.** The 2026-08-25 simplification review's verdicts, applied end to end. The
three role tiers (COOLDOWN / ROTATION / FALLBACK) left the model: membership is one boolean —
a row is in the scan when its `scan_when` alternatives (default: ready-self) read ON — and
`Catalog.TIERS`, `Signal`'s tier selection, `bands` as a required structure and the wire's
`id:ROTATION` bodies are gone (`id:scan` / `id:off` now; the capture stream keeps the name
`tier`). The 13-name scenario verdict vocabulary collapsed to five — `press`, `cd`, `weave`,
`ruled-sealed`, `open` — with every cue-flavored verdict rewritten as an explicit `{cues: …}`
group. Files: `spec.md` §1/§3.1/§3.7, `render-shelf.md` (Part 6 `tokens.verdicts`),
`authoring.md`, `flight-reading.md`, all six `<spec>/catalog.md` + `scenarios.md`,
`wowkb.capart`, the stepper/gallery templates, and in the addon `Catalog.lua`, `Signal.lua`,
`Treatment.lua`, `Sense.lua`, all five `Catalogs/*.lua` and the test suite.
**Why it still binds.** The shipped product had already reduced the ladder to one bit
(2026-08-19: `Treatment.For` read only `tier ~= nil`, and `presentation_spec` asserted the
tiers drew identically), and the pilot's stated usage model — positive cues first, then a
left-to-right scan of not-ruled-out rows — has no lane read in it. A structure the paint
cannot express and the reading model never consults is carried risk, not information: 34 of
37 authored bands were the single ready-self band, and the three genuine conditions survive
as `scan_when` (Wake of Ashes's identity pair; affordability on Shield of the Righteous,
Templar's Verdict, Divine Storm). Likewise the dead verdicts were cue names wearing a second
hat — capart already linted against declaring the cue the verdict implied. The audit
deliberately kept: the density rule and budgets, authored row order + the elimination gate,
Charges, readable/sealed classification, the whole shelf render vocabulary and `Channel`'s
sealed-display bands ("band" in that sense is a different concept and untouched).
**Caveat.** Two accepted behavior changes are authored, not flown: Demonology Shadow Bolt and
Destruction Incinerate/Conflagrate dropped their both-lit two-band flips to default
membership, so those filler rows now stay lit under an unknown identity/resource where the
old blind rule darkened them. The uniform blind rule (no ON alternative + any BLIND
alternative ⇒ withheld, `blind = true`) is likewise unflown.

---

## 2026-08-27 — the combat teardown, and badges that were the wrong size everywhere but 56

**What changed.** Every combat gate on the ordering path was deleted, a per-frame `SetPoint`
re-assert replaced the deferred repair, and badge geometry stopped being arithmetic on the
shelf's nominal icon. Files: `Anchor.lua`, `Bind.lua`, `Overlay.lua`, `Paint.lua`,
`Channel.lua`, `Panel.lua`, `Sense.lua`, `StylePanel.lua`, the anchor/style/channel specs,
`render-tokens.json`, `render-shelf.md`, `flight-reading.md`, `capart.py`, and
`security-taint-and-restricted-data.md` §3.5.3.

**Why it still binds.** Three arguments a future reader must not re-derive.

*The gates were never protecting anything.* The CDM's item templates declare no `protected`
attribute and no secure template, `IsProtected()` had already measured `false, false` on 9 of 9
Havoc rows in and out of combat, and a bind resolve is `pcall`'d getters end to end. What the
gates cost was concrete: `RefreshLayout` releases the whole item-frame pool from the viewer's
full-aura-update path, so a destructive stomp mid-pull left Blizzard's order on screen for the
rest of the fight while the row still read as a priority scan. `Anchor.Judge` no longer takes a
combat flag at all. The accepted trade — icons may move during a pull — is the author's
decision and is the reason the always-true alternative was not chosen.

*A deferred repair has a window; a synchronous one does not.* Correcting inside the mover's own
`SetPoint` call is what EllesmereUI does, and it catches a mover that exposes no hook of its
own, which is the shape of cap's standing unattributed case. The discriminator is the anchor
frame: everything cap writes is relative to it, so a point relative to anything else came from
outside. `P.expected` is stamped before the write that sets it, because the hook fires inside
that call.

*Three tokens were outputs, not decisions.* `count.hatch_px` 56, `plate_px` 25 and `mark_px` 15
were `Geometry()` evaluated once against a 56 px icon — `56×1.0`, `22.4×1.12`, `22.4×0.68` —
and the ratios they came from were already in the shelf. Worse, `Paint.Geometry()` took no host
at all, so on any other icon size every badge on every row was mis-sized. Making them
arithmetic on a measured width made pinning order load-bearing: an escape's size is a literal
baked into the band string at arm time, and a host with no rect measures nothing.

**Caveat.** None of it has flown. Re-applying a band's size when the icon rect changes was not
built: it depends on `SetApplicationCount` being callable twice on a live button, which is now an
open ClientLab question rather than an assumption.

---

## 2026-08-27 — a claimed frame the plan loses is parked, not abandoned

**What changed.** `spec.md` §3.9 gained a fifth property and §4 was widened to match, then
`Anchor.lua` grew a claim/park/release lifecycle. Files: `spec.md`, `Anchor.lua`,
`anchor_spec.lua`, `backlog.md`, `flight-reading.md`. `Lab.lua` was re-exported in passing — it
had been left behind by the commit that put L9 `ring_collision` in `render-lab.json`, and
`StylePanel` gained the `composition` drawer that entry declares, so the gallery can draw it.

**Why it still binds.** `adopt` rebuilt `tracked` wholesale and `disarm` restored only
`tracked`, so a frame cap had moved and then stopped tracking was left at cap's coordinates,
inside a row that still reads as a priority scan, in nobody's order — and turning ordering off
would not have restored it either. Making `Bind.ItemFrame` clear a stale frame earlier the same
day made that path reachable rather than theoretical. So `claimed` is now the set cap answers
for, `tracked` is the subset the plan places, and `parked` is the difference: held off the row
rather than drawn in the wrong place, which is the same choice `Overlay.quiet` and Sense's dark
latch already make one level up. Two riders are load-bearing. A park and a placement use the
**same anchor keyword**, because a same-keyword `SetPoint` replaces and a different one
accumulates a second conflicting anchor. And a destructive stomp drops every claim: the viewer
re-issues those frame objects against different rows, so a park that outlived the pool would
make a live ability silently invisible.

**Caveat.** Unflown. The `# parked` mark is emitted by the apply that moves the frames rather
than the adopt that decides to, so an adopt followed by a failed apply reports nothing — which
is correct but means a park can be decided and not yet done.
