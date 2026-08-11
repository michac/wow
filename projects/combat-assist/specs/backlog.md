# Combat Assist Plus — backlog

**What this file is for:** the list of work items, plus the one **Status** block that says
where the code is. One line per item, newest thinking at the top of its section. An item
here is *agreed work not yet done* — if it's speculative it goes under **Ideas**; if it's
done it collapses to one line under **Done** and the reasoning goes to `notes.md`.

Keep items small enough to finish in a session. An item that needs a paragraph to explain is
a sign the answer belongs in `spec.md` first.

Items carry the `spec.md` section they implement, as a bare `§n.n` at the end of the line.

**Naming: there is exactly one code, and it is the milestone.** `M0`…`M5` and their lettered
rungs (`M3a`…`M3e`) come from `spec.md`'s milestone table — they are an *ordered ladder*,
which is what earns them a code. **Everything else is a section named in plain words** ("the
rule cull", "the window migration"). ⚠ **This is a rule because it already went wrong once:**
work clusters were being labelled `M3-F` / `M3-W` / `M3-C` / `M3-R` / `M3-S`, which look like
siblings of `M3a` but are not ordered, not milestones, and whose letters were private
mnemonics nobody could decode a week later. If a new cluster needs a name, describe it —
don't mint a code.

## Status

**This block is the only place in the project that asserts where the code is.** Every other
file — both `CLAUDE.md`s, `notes.md`, `discussion.md`, `flight-reading.md` — points here and
asserts nothing. **The live addon version is read off `wowkb.addon list`, never hardcoded in
prose.**

⚠ **One sanctioned exception: `spec.md`'s Milestones table**, which carries a per-rung status
column because it is the ladder those rungs are ordered on. It **mirrors** this block and must
stay consistent with it — if the two disagree, this one is right and the table is the thing to
fix. It is not a second source, and nothing else may grow one.

| Milestone | State |
| --- | --- |
| M0 · M1 · MC · M2 (M2a–M2d) | done; M2 flown 2026-08-06 |
| M3a · M3b | done; M3b flown 2026-08-07 |
| the window migration | done 2026-08-08 |
| M3c · M3d · the §3.1 cull · the proc-glow suppression · the measured restyle · M4a's bars | released as **v0.2.4** and **flown 2026-08-10** |
| M3e · M4's remaining rungs · M5 | not started |

**cap has drawn on screen.** One Demonology pull on 2026-08-10 put every built surface in front
of a player at once, and it works — the surfaces render, the binding holds, the ring is the
flipbook, every bar armed and no row went unsized. What play said, and what the capture then
measured, are the first section of `Now`; one of the four things play said is that the
proc-glow dim does not work.

**That flight was captured, and the capture has been read** — interpreted 2026-08-11 over a
**700.7 s** combat window and 169 in-combat change-lines, time-weighted. ⚠ **The headline is
that the tier signal is saturated**: two or more entries were HIGH for **74.8 %** of the pull
against M3b's 16 %, and five of the eight entries held one tier unbroken for 500–545 s. What
else it said is in `notes.md` (2026-08-11) and in `discussion.md` **D7 · D12 · D14 · D15 ·
D17**; the work it generated is the first section of `Now`. **It is interpreted, so cite those
findings rather than re-reading the log** (`flight-reading.md` carries the rule).

## Now

⚠ **The order is `simplify → draw → add detail as play tells us to`.** The detail that gets
added from here comes from **playing**, not from authoring: `spec.md` §3 is not re-opened.
The sections below are in queue order and `Now` holds only open work.

### What the first flight said — v0.2.4, flown and measured

⚠ **This section goes first because it is the only work here informed by pixels**; everything
below it was authored. Every item has its open half in `discussion.md`. **The capture behind it
is digested** — these items and those `discussion.md` entries carry what it said, and re-opening
the log is not a step in any of them.

- [ ] **Re-cut the catalog's bands so the tiers recede.** ⚠ **The biggest thing the flight said,
      and bigger than the four things play reported, which are downstream of it.** Measured: two
      or more entries HIGH for **74.8 %** of the pull against M3b's **16 %**, something HIGH
      **87.4 %** of the time, and five of the eight entries at one tier **unbroken for
      500–545 s** of 700.7 s. Nothing recedes, so the ladder carries no information — and the
      standing argument for why that costs rather than merely looks busy: **highlighting at 50 %
      validity measures as no better than none**, and unreliable cueing makes *uncued* targets
      missed more often than no cueing at all. If HIGH fires most GCDs it is a label, not an
      alarm. The fix is in the bands, not the treatment. Worst occupancies: E3 emphasised 98 %
      (HIGH 74 / MEDIUM 24) · E8 MEDIUM 84.7 % · E5 MEDIUM 83 % · E2 HIGH 77 % · E1 MEDIUM 73 %.
      §3.1.
- [ ] **A transformed row lights for its whole cooldown** — Grimoire: Imp becomes Consume Magic
      when on cooldown, so `ready(this)` reads true and E3 sits emphasised throughout.
      **Measured at 98 % of the pull, one unbroken stretch of 503.9 s** — the largest single
      contributor to the re-cut above, which is why it goes first among the four. The behaviour
      is decided (**that state is *none***); where the fix belongs is not. **`discussion.md`
      D15.** ⚠ Before choosing, count how many other rows on this spec transform into an
      unrelated ability while on cooldown — nobody has looked.
- [ ] **E1's and E2's grades are a register error, not a tuning question** — they name
      `cooldownRemaining(this)`, a **channel**, so a grade written on cap's own frame alpha can
      never fire from one; E3 declares no grade at all. Measured: HIGH sat at its ungraded
      midpoint `a91` for ~**95 %** of its occupancy, while MEDIUM varied on the two entries
      grading on `shards`. §3.1's continuous emphasis is running on **two of eight entries**.
      ⚠ This is a `catalog.md` edit and the choice is D7's — the grades move to the §3.4 bar or
      come out — so it does not get made here. **`discussion.md` D7.** §3.1.
- [ ] **The tier glows read as candles** — too flickery, and wanted brighter across the board.
      ⚠ **Now downstream of the re-cut above**: the measurement puts the root upstream of all of
      the trough, the rate, the `ADD` blend and the base alpha, and a brighter ring on a
      saturated screen is worse. It does **not** clear those four — fixing them alone cannot fix
      the complaint. **`discussion.md` D14.** ⚠ **The per-row phase offset may not be quietly
      dropped** — it is a seizure-floor property, not tidiness.
- [ ] **The proc glow is not suppressed** — a proc'd Demonbolt still dominates, same on
      Infernal Bolt. `Glow.lua`'s first measured result, and it is negative. **Two of the four
      candidate causes are dead** — the frames were hooked and the dim was armed — leaving a
      wrong field name on a CDM item and a setter that lands on nothing: **`discussion.md`
      D17**. ⚠ **This blocks D10** — "does cap's ring read as distinct from the stock glow" is
      not answerable while the stock glow is at full strength.
- [ ] **Put a counter on the dim itself** — `glow:` counts frames whose `RefreshOverlayGlow` was
      hooked, which is the step *before* the one that can fail: `dim()` separately needs
      `SpellActivationAlert` to resolve and discards its `pcall` result, so both surviving causes
      report `live`. ⚠ **This is the `nosize:` defect again** and the fix is the same shape —
      count whether the alert field resolved and whether the setter ran. **Not another flight:**
      no flight can separate the two while the instrument stops where it does. §3.2.
- [ ] **Tyrant should be MEDIUM with markers, not promoted to HIGH** — E1 collapses to one
      MEDIUM band on `ready(this)` and the staging information moves to markers. ⚠ The tier half
      is a catalog edit and is decided; **the marker half has no vocabulary**, because
      *"Dreadstalkers are out"* is a gate with no sealed half. **`discussion.md` D16** — and it
      is the *"a catalog entry that needs one"* trigger the coverage table below waited for.
      ⚠ It is also a band change and belongs with the re-cut above rather than beside it.
⚠ **A caution rather than an item, so it carries no box: E1's HIGH promotion was measured
firing correctly by the M3b flight and play still reversed it.** **A flight that measures a
rule firing correctly says nothing about whether the rule is right**, and no instrument in
this project can close that gap. Read it before writing the next tier rule (`notes.md`,
FIRST PIXELS).

### The drawing rungs — M3c, M3d, M3e

**M3 is the tier signal, and its ladder is M3a…M3e, each rung flyable.** `--patch` release +
deploy is **pre-authorised for M3 flights and nothing else** — ⚠ a cut carrying work from any
other milestone is **ask-first**, and the build has carried M4a since v0.2.4.

- [ ] **Give the unmarked channel forms markers, driven by a catalog that wants one** — the
      table below is the current coverage. Nothing authors `auraRemaining(x) ≤ t` or
      `active(x)` today, so building their markers now would be inventing a visual language
      against no evidence; the trigger is a catalog entry that needs one, and **D16 is the
      first one to arrive**.
- [ ] **Decide `--@unverified` across the drawing surface, or for none of it.** House rule 5
      wants the marker on any path whose *game behaviour* has never been observed — which was
      `Overlay.lua`, `Channel.lua`, `Treatment.lua`, `Glow.lua` and `Bars.lua`, all five.
      Marking one implies the rest are verified, so nothing is marked and the decision is here
      rather than made by omission. ⚠ The rule also says every `--@unverified` must appear in
      the **current flight's acceptance set**, and the v0.2.4 flight discharged one of the two:
      **`buildFlip` is verified** — the FlipBook setter names were established nowhere but the
      generated docs, and `ring:flip` held for the whole pull, so the atlas resolved, all three
      setters took and the flipbook was the live geometry. ⚠ The marker itself still has to come
      off the source. **One marker stands: `armPulse`** — does `SetStartDelay` re-pay on every
      iteration of a `BOUNCE` loop? `frames-textures-animation.md` §7.3 records nothing about the
      loop, and only an eyeball can answer. ⚠ Do not read a discharged marker as a claim that the
      rest of the surface is verified.
- [ ] **M3e** — the Demonbolt demotion, the other half of §3.2. Its acceptance is **playing
      with it**: the point of drawing early is that the next spec's rules get
      reverse-engineered from a thing that felt good rather than authored against no evidence.
- [ ] **Drain the dim recipe into `knowledge/addon-dev/cooldown-manager.md` §6** — ⚠ **and the
      first flight says do not.** The alert-frame-not-child-textures lever and the
      per-instance-hook requirement exist only in CDMProbe's source, were never measured by us,
      and the flight showed the dim **does not work here**. Writing it now would file a broken
      mechanism as a `[client]` claim. Blocked until the mechanism works and a flight has
      measured it — see D17.

**Which of `spec.md` §3.5's channel forms are actually drawn.** `Overlay.lua`'s `slotFor`
owns this and implements **two** of the six that table's `Draws` column promises. A form with
no marker is still **legal** — it loads, passes every check, and reports `nodraw` in `C{}` —
so an author reading only `spec.md` gets silence rather than an error. This is milestone
scoping, not a spec change; `spec.md` §3.5 points here for it.

| §3.5 form | `Draws` | Today |
| --- | --- | --- |
| `stacks(x) ≥ n` | count | ✅ **drawn**, on a **positive** cue — the `count` slot |
| `cooldownRemaining(x) ≤ t` | marker | ✅ **drawn**, on a **negative** cue — the `hold` slot |
| `auraRemaining(x) ≤ t` | marker | ❌ not yet. ⚠ **check 4 admits it as a negative cue's channel**, so it is the form a catalog author is likeliest to write and get nothing from |
| `cooldownRemaining(x)` · `auraRemaining(x)` | countdown | ❌ not yet. The bars draw a countdown, but off the bound row directly — a *declared* bare channel on a grade or a cue still reaches no marker |
| `active(x)` | pip | ❌ not yet |

⚠ **A slot is claimed by a (polarity, channel) pair, not by a channel alone.** A *positive*
`cooldownRemaining ≤ t` and a *negative* `stacks ≥ n` both read `nodraw` today even though
both channels sit in the drawn rows above. Which marker a future pairing should get is open
(`discussion.md` **D8**).

### The measured treatment — judged once, and what that left open

- [ ] **Judge LOW's ring on screen — it is at the lab-measured 0.50**, band `0.36 – 0.50` with
      the measured value as its bright end. The narrow question here is whether a 0.50 slate
      ring is readable as LOW at all. ⚠ The broader one — a graded LOW can now reach a dim
      MEDIUM — is `discussion.md` **D11**, and **a Demonology flight does NOT answer it**. §3.1.
- [ ] **Judge the ring's size and bleed on screen.** It is 1.4× the *item frame*, read off
      `item:GetWidth()`, because that is what Blizzard's own alert frame does. ⚠ A refused or
      secret read leaves the ring **unsized and unshown** — deliberately, rather than inventing
      an icon size — so a pull that draws no ring with `ring:flip` in `D{}` is that state, not
      a treatment bug. §3.1.
- [ ] **Both routes render zero identically to broken.** Set `SetExpiredText` and
      `SetZeroDurationText` to distinct visible strings (§4.8.1 findings 14–15), and read the
      remaining duration with `ignoreGCD = false` so a ready spell shows the GCD rather than
      `0` — ⚠ that second half is a design choice here, not something those findings state.

⚠ **"Cap the HIGH tier's population" is no longer an item here, so it carries no box** — it was
the generic worry and it now has a measured instance, so it lives in *Re-cut the catalog's
bands* above. What that move carries with it: the M3b baseline it was written against (50
in-combat samples over 76 s of mostly steady state, one Tyrant window, neither the Implosion cue
nor the proc demotion in the build — **0 HIGH on 54 %, exactly one on 30 %, two or more on
16 %**), and the v0.2.4 pull it is now read against (time-weighted: **0 HIGH 12.6 %, one
12.6 %, two 71.3 %, three 3.5 %**). ⚠ The two instruments differ — 50 samples against a
time-weighted change log — and the gap is far wider than that difference can account for.

⚠ **A standing constraint rather than an item, so it carries no box: a secret-fed FontString
must be a layout leaf.** `SetText(secret)` marks the string *and its dependent*
anchoring-secret (§4.8.1 finding 10). Anchor it *to* things; never anchor anything *to* it.
`DurationTextBinding` is recorded as the anchor-safe route; whether that still holds is
**reopened** (§4.8.1's `[gap]`) and the lab is isolating it — do not build on the binding
route until that resolves. §4.

### The M3b leftovers — what that flight did not settle

- [ ] ⚠ **The `refused:` criterion is mis-specified and is not checkable.** Refusals are the
      expected case (the hook is on every row and most rows are silences), but **refused edges
      are counted and never logged with their cid**, so the instrument cannot tell "correctly
      ignoring silences" from "resolving the wrong cid" — the exact failure the criterion
      exists to catch. Log the cid on refusal, and restate the criterion as *every refused cid
      is a declared silence*.
- [ ] ⚠ **Three things no flight has exercised, and a criterion nobody exercised must not read
      as a pass.** (a) the **event-driven settle arm** — needs a real spec or hero swap;
      (b) the **dark-for-the-fight rule** — needs a `/reload` mid-combat or a swap immediately
      before a pull; (c) **`/cap aoe`** — never toggled in a flight.

### The hidden-row surface — rows that exist but are switched off

⚠ Coverage check 1 is measured against the rows cap actually **binds**, so a row that is not
bound is not a coverage failure. What is missing is the reporting around it.

- [ ] **E4 Summon Doomguard drops at bind, and that is the designed behaviour** (`catalog.md`
      O3: `1276672` appears in no row of the 21-row capture). What is owed is only that the
      drop be **visible** — the item below.
- [ ] **Summon Vilefiend (cid 763, spell `1251781`) is not a tracked row on this build** — it
      carries `HideByDefault` in DB2's `CooldownSetID 60` and is not in the live bind, so it
      needs **no** silence today. ⚠ It would need one on a build that un-hides it.
- [ ] **"Available, not displayed"** — implement `spec.md` §3.5's state. A row that exists but
      is switched off must be named in the capture log rather than dropped silently, **for a
      band's subject as well as a cue's**.
- [ ] **Enable cid 84224** (the `HideByDefault` Summon Demonic Tyrant bar) on the reference
      character and confirm it binds — an exact Tyrant-active duration, currently unused. ⚠
      That it *can* be enabled is an inference off Blizzard's saved-layout path
      (`cooldown-manager.md` §1.2), not a measurement; this item is the measurement.

### The stale artifacts — re-derive the two published references

- [ ] **Re-derive both artifacts** — [Architecture](https://claude.ai/code/artifact/2de40ee9-5457-4ca3-b46e-77178e021207)
      and the [Demonology reference](https://claude.ai/code/artifact/46bb78b6-7c41-4210-a9b0-3b1707678569).
      Both are **STALE**: they describe a catalog mechanic and a cue vocabulary that no longer
      exist. The project `CLAUDE.md` carries the standing warning and points back here; drop
      it when they are re-derived. ⚠ Derive them by *running the code against the capture*, as
      the originals were — that is what found the `alt` defect.

### Loose decisions carried out of M2

- [ ] ⚠ **M3 decision, deferred not dropped:** `spec.md` §3.5 still says cap "says so plainly
      once" when no catalog claims the spec. Either M3 gives it exactly one player-facing line
      at load for a state the player can fix, or it goes to the log and cap is silently inert.
      Don't let it ship by default.
- [ ] ⚠ **No busted suite for `Log.Render`.** It is written pure so one *can* exist, but a
      suite written against a format the next flight is about to change is a change-detector.
      Revisit once the format has survived a flight.

## Next

### The claim-reliability revision — KB process, not cap code

**Plan: [`todo/kb-claim-reliability.md`](../../../todo/kb-claim-reliability.md). Execute it in
a fresh context; it is written to be self-contained.** Tracked here because cap is the consumer
that gets hurt — cap's catalogs are authored straight off `knowledge/addon-dev/`. The problem:
a negative result is recorded with a positive's evidence class, so the KB reinforces its own
wrong answers. The fix splits `[client]` from `[searched: <instruments>]`, gates both in
`wowkb.kblint`, strips claim→`OBS-nnn`/`projects/**` pointers, and makes a claim whose capture
has rolled off say so. ⚠ **Not the sourcing ban** floated 2026-08-09 and rejected.

**Four invariants the M3 code already implements — recorded because they are easy to regress:**
the readiness latch hooks **once per frame object ever** through a weak-keyed table and
resolves the cooldownID *inside* the callback (`hooksecurefunc` cannot be removed and item
frames are pooled); the out-of-combat baseline uses `ignoreGCD = true` or discards durations
≤ 1.5, or a read taken just after a cast records the whole roster as on cooldown; readiness is
**three-state** with the refusal count logged; and `maxCharges` is seeded out of combat with a
refusal to latch > 1. ⚠ **"Unknown fails the band" is a rule about the *band*, not about the
term** — `not ready(X)` on an unknown `ready(X)` must also fail. Get this wrong and a blind cap
reads confident.

**M4 — §3.4 smart cooldowns.**

- [ ] **The hold cue on a bar** — §3.4's headline value, held out of pass 1 deliberately so the
      bars can be seen before a second thing is drawn on them. The mechanism already exists and
      is the icon's: `Channel.Threshold` + `Treatment.Ink(Treatment.Mark(cue))`, in the hold
      treatment. ⚠ **A ready cooldown carrying a hold keeps its tier** (`spec.md` §3.4).
- [ ] **Judge the bars on screen** — four rows, ~18 px each, in a 220 px panel. Is the countdown
      legible in combat, does the label survive a tier fill, and does a ready bar read as *ready*
      rather than as *stuck*? ⚠ Nothing in the log can answer any of the three. ⚠ **Two numbers
      nobody has seen ride on the same look** — the resting fill and the track colour, both
      `Treatment.BAR`, both expected to move (`discussion.md` **D13**).
- [ ] **Decide what a bar does with a grade** — `discussion.md` **D7** parked "may a grade exist
      without a tier" on M4's drawn bars, and the bars now exist. E1's and E2's
      `cooldownRemaining` grades are inert: a grade is only computed when a band held, and their
      bands need `ready(this)`. Either the bar carries the warming or the grade lines come out
      of `catalog.md`. ⚠ **The inertness is now measured, not inferred** — HIGH sat at its
      ungraded midpoint ~95 % of its occupancy — so this decision is what unblocks
      *E1's and E2's grades are a register error* in `Now`.

**M5 — §3.3 sequences.**

- [ ] **Author the Demonology opener** — deliberately left unwritten rather than transcribed,
      because the sources describe it starting with Power Siphon, which needs Wild Imps you
      don't have at a pull. Needs a real answer, not a copied one. (The Tyrant burst window IS
      drafted, at medium confidence.)
- [ ] The detector — recognise a sequence from combat entry and your own casts, with no input
      from you.
- [ ] Primary + secondary hints on the CDM, layered over the tier signal and visually distinct
      from it.
- [ ] Drop the sequence silently and instantly when you cast off-script. No nagging, no
      correction, no resume.
- [ ] ⚠ **Sequence triggers are not checked at all.** `Catalog.Check` never inspects
      `cat.sequences`, so `spec.md` §3.5's *"a trigger naming a channel, or naming a term
      outside this set, does not load"* is unenforced. That matters because the trigger is the
      **one** place `casts` is legal, so it is exactly where new trigger vocabulary gets
      written. Check it as a band-legal condition plus `casts == n` when the machinery lands.

**Cross-cutting.**

- [ ] Decide the fate of the `assisted-combat-next-cast-varies` lab test now that §3.1 no
      longer consumes the oracle. It is built and deployed, so it costs nothing to let it
      answer — and a working oracle would be a useful *development-time* falsification check
      against our own tiers. Park it or keep it, but don't leave it undecided.
- [ ] ⚠ **`talent(x)` is in the spec's gate table and nothing answers it.** `Sense.buildReads`
      never returns it and it is not in `GATE_ORDER`, so a band using it reads **unknown for
      the life of the build** with nothing tallying the refusal. **Either wire it or delete the
      gate from `spec.md` §3.5** — decide when something needs it, not before.
- [ ] `/mine-addon` pass for prior art on graded emphasis under 12.0 restrictions.
- [ ] Route the KB findings parked in `knowledge/_meta/kb-inbox.md` (four on
      `cooldown-manager.md`, two on `frames-textures-animation.md`, plus a Demonology transform
      spell-ID conflict). None blocks cap.

## Ideas

*(unfiltered — no commitment implied)*

- Napkin the Wild-Imp count from your own casts (readable in combat; Hand of Gul'dan makes
  three) to get a *smooth* Implosion signal, with the C-side quantiser underneath as the
  ground-truth gate. Deferred: §3.1 accepts a binary threshold cue as sufficient signal, and
  this drifts (imps expire, Tyrant extends, Implosion consumes).
- Sound on an ability crossing into HIGH — the moment it *becomes* right is the one easiest to
  miss visually.
- A practice/verify mode: replay a recorded pull against the sequence detector to see where it
  lost the thread, instead of eyeballing it mid-fight.
- Sequence catalogs drafted from the in-client Assisted Combat priority lists rather than
  hand-authored from guides. ⚠ On Demonology that list is thin.

## Done

*(one line each. `notes.md` carries the story from 2026-08-08 on; for anything earlier, the
original entries are at `git show a33e152:projects/combat-assist/specs/notes.md`)*

- [x] **The v0.2.4 `draw` capture read** — five findings, to `discussion.md` D7/D12/D14/D15/D17
      and to the top of `Now`; the headline is saturation — 2026-08-11
- [x] **The first pixels flight** — v0.2.4 released, deployed and flown — 2026-08-10
- [x] **M4a, the cooldown bars** — `Bars.lua`, `Treatment.Fill`, `test_dir` on the registry
      entry — 2026-08-10
- [x] **The measured restyle** — the flipbook ring, the per-tier pulse and its per-row phase
      offset, LOW as a ring, `nosize:` — 2026-08-10
- [x] **The §3.1 cull** — three surface rules struck, two narrowed, `Treatment.Rank` added,
      LOW back to 0.50 — 2026-08-10
- [x] **The proc-glow suppression** — `Glow.lua` + `Glow.Restore()` — 2026-08-10
- [x] **M3d, the cues** — `Channel.lua`, `Treatment.Ink`, two marker slots, `C{}` — 2026-08-08
- [x] **M3c, the graded register** — `Treatment.lua`, `Overlay.lua`, `Sense.OnVerdicts`, the
      `draw` stream — 2026-08-08
- [x] **The polarity rule struck** — a rule the rule cull had *added*; D8 reopened — 2026-08-08
- [x] **The window migration** — the catalog mechanic deleted from the code and `catalog.md`;
      subjects, negation, cue polarity, check 3 — 2026-08-08
- [x] **The rule cull** — `spec.md` §1 gains the three principles; nine rules cut back to them
      — 2026-08-08
- [x] **The document defects** — F3–F9, the unknown-cue-gate rule, §3.0's `Cue` row — 2026-08-08
- [x] **M3b** — the gates read and the tiers computed, nothing drawn; flown as v0.2.1 — 2026-08-07
- [x] **M3a** — the lab claims drained; `Catalog.lua`, `Tier.lua`, `Track.lua`, the Demonology
      catalog, `/cap aoe`, the busted harness — 2026-08-07
- [x] **Target count: struck, answered by design** — AoE is a manual toggle — 2026-08-07
- [x] **M2d** — flown as v0.2.0: the binding is **correct**, not merely populous; four facts
      drained to `cooldown-manager.md` — 2026-08-06
- [x] **M2c** — the standard capture log: `Capture.lua`, `Log.lua`, `.luacheckrc` as a release
      gate — 2026-08-06
- [x] **M2b** — cap's diagnostic surface stripped; client behaviour is a lab question — 2026-08-06
- [x] **M2a** — the four client claims M2 rests on labbed and drained (OBS-056…059) — 2026-08-06
- [x] **The floor is drawable on Demonology** — Shadow Bolt `686` is an Essential CDM row —
      2026-08-06
- [x] **M2** — `Bind.lua`, `Frame.lua`, the CDM off/unconfigured detection — 2026-08-05
- [x] **MC** — §3.5's catalog format and the Demonology catalog — 2026-08-05
- [x] **M1** — `spec.md` §1–§5 written — 2026-08-05
- [x] **Cooldown HUD marked superseded** — banners, both root `CLAUDE.md` entries, its
      auto-deploy exception declared dead — 2026-08-05
- [x] **Scope boundary** decided against Cooldown HUD and BucketBinds — 2026-08-05
- [x] **M0** — scaffold: repo `michac/cap`, `.toc`, `/cap` router, `wowkb.addon` + `ghaddons`
      — 2026-08-05
