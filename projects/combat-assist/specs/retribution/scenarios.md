---
title: Retribution Paladin — the scenario catalog
spec: Retribution Paladin (Templar) — specID 70, Midnight 12.1
---

# Retribution Paladin (Templar) — the scenario catalog

**What this file is for.** `catalog.md` maps every ability to a role lane and the cues. This file is the **proof** that lane + cues actually reproduce the priority order — state by state, naming the press and, for every button that is available and skipped, the reason. It is what `capart check`'s reading gate mechanises, and it is where this design gets falsified.

**Cross-links.** `catalog.md` (beside this file) is the definition — roster, lanes, markers,
contract boundary. `../spec.md` §3.1 owns the tier model and §3.6 the readable/sealed boundary;
`../authoring.md`'s recipe index owns the recipe IDs and their evidence anchors; `../render-shelf.md` owns every pixel and this file
describes none. Priority source: `knowledge/classes/paladin/retribution/simc-apl.md` (Tier 1,
generated), explained by that spec's `rotation.md`; neither is restated here.

**Three files per spec, and Havoc is the model** (`../authoring.md` §0): a definition, its proof,
and its safety case.

---

## The state walk

Fifteen states, each naming the press, and for **every button that is available and skipped**,
the reason. Buttons the Cooldown Manager has already swiped need no explanation. The walk reads
the authored row order left to right and must satisfy the shape `capart check`'s **elimination
gate** enforces: *the leftmost entry that is neither swiped nor wearing a negative badge is the
press.* Row numbers are the authored order above.

Shorthand: `HP` = Holy Power. "AW", "ES", "WoA", "DT", "TV", "DS", "BoJ" are the rows.

### The rows are `scenarios.json`; this file is the walk

**The CDM row for every scenario below lives in `scenarios.json` beside this file, which is
canonical and hand-edited** — nine entries in authored order, each a `{name, verdict}` record
with optional `cues` / `sealed` / `client`. This document carries the *walk*, keyed by the same
ids, and it no longer restates the row. Until this split the row was a ` · `-separated bullet
here that a regex scraped into a cache under `previews/data/`; the doc led and the JSON followed,
and that direction is what the split reversed.

`capart check retribution` cross-references the two halves **by id in both directions** and
matches every state a row draws against the per-ability `states` table in `catalog.json`, so a
walk cannot draw a combination no catalog can produce. To see the rows drawn, open
`previews/retribution-stepper.html`.

The ability name in a row is whatever the Cooldown Manager would *display* in that state —
`Hammer of Light`, not `Wake of Ashes`, while row 3 is transformed — because that is the identity
the client draws and the swipe follows (*Open facts* 1).

A verdict says what cap concluded, never what the button looks like: **the pixels belong to
`../render-shelf.md`**. `cd` = swiped by Blizzard, no cap opinion. `open` = shown, in the
scan, with every badge it wears named explicitly in `{cues: …}` — `blocked` from a readable Lua
term or from a sealed band the client paints, `starved` the red affordability badge, `overcap`
the red waste badge. `press` = the button an unobstructed scan reaches. ⚠ `press` and `open`
render identically, by design — the press is not something cap draws.

⚠ **One entry wears a positive cue** — Blade of Justice's `priority` at the opener (cue **H**,
worn by two markers, `boj_opener` and `boj_opener_woa`, whose union spells the rung's reachability
OR) — so RET-1 is judged by pass 1 of `../render-shelf.md` Part 0.5 and **every other
scenario here is judged by pass 2, elimination**. Why this catalog declines the vocabulary's
*other* positive cue, `capped`, is argued in `catalog.md` (*Why this catalog does not spend
`capped`*). *(Until 2026-08-25 this line read "no entry in this catalog wears a positive cue",
which stopped being true when cue H was authored.)*

### RET-1 · Opener, everything ready, HP 0

- **State.** Pull timer at zero, every cooldown up, **Holy Power 0**, single-target mode, no
  procs. **Holy Flames talented, Expurgation not yet on the target** — the state the opener exists
  to end.
- **Walk.** ⚠ **This scenario is read by pass 1, not by elimination** — the only one in the
  catalog that is.
  1. **Blade of Justice** wears `priority` (cue **H**) → **press.** `generators` 2, the rung that
     puts Expurgation up. The condition is that rung: Holy Flames talented, the DoT absent, the
     button ready — and the rung is REACHED, which at Holy Power 0 with Wake of Ashes up is true
     down both branches, so **both** markers fire (state `boj_opener_both`) onto the one badge.
     ⚠ At **five** Holy Power with Wake of Ashes on cooldown neither fires and the row is clean,
     because `generators` 1 diverts to `finishers` and rung 2 is never reached — which is what the
     two reachability terms are for.
  2. Everything else is read only if the eye goes looking. Execution Sentence and Avenging Wrath
     are genuinely held — Execution Sentence by **two** markers at once (`es_awaits_wrath_ready`
     and `es_awaits_expurgation`, state `es_expurgation_and_wrath_ready`), Avenging Wrath by
     `aw_awaits_expurgation` — and the two spenders are unaffordable at 0 Holy Power. None of that
     has to be interpreted to find the press. ⚠ Row 1 and row 2 are held by the **same clause**
     here, `(!talent.holy_flames|dot.expurgation.ticking)`, on two different rungs; the badge does
     not distinguish them and does not need to.
- **Eye-direction.** ⚠ **This is the catalog's worked example of the density rule.** Said by
  elimination, the opener needs **four** holds — Execution Sentence, Avenging Wrath, Wake of Ashes
  and Divine Toll all standing down so a left-to-right scan can reach position 7. That is over
  budget (`../render-shelf.md` Part 0.5) and it reads as "something is wrong" rather than "press
  the clean one". Promoting the press costs one badge and says the same thing.

  **Two markers were deleted outright** when this was authored — `woa_awaits_wrath_ready` and
  `dt_awaits_wrath_ready` — because they existed for no reason other than steering the scan past
  their own rows. That is the test of a promotion worth making: it should *remove* authored
  vocabulary, not add to it.
- **Cue set.** Priority (H) → **have**. Readable hold (C) → **have**, on rows 1 and 2.
  Affordability (A) → **have**.

### RET-2 · HP 5, Wake of Ashes on cooldown — the interleave, resolved

- **State.** Single target, no procs, **Holy Power 5**. Execution Sentence, Avenging Wrath and
  Wake of Ashes are all on cooldown. Divine Toll is ready.
- **Walk.**
  1. **Execution Sentence … Wake of Ashes** — on cooldown → skip.
  2. **Divine Toll** — available, and the `overcap` badge lights on the exact readable predicate
     `resource >= 5`: pressing it here throws away its whole Holy Power injection → skip.
  3. **Final Verdict** — affordable, nothing rules it out → **press.** `finishers` 4, reached
     through the early `finishers` call at `generators` 1.
- **Eye-direction.** ⚠ **This is the scenario the whole row order is built for.** `finishers` is
  called from *inside* `generators`, so the spenders outrank Divine Toll **only at 5 Holy Power** —
  a thing a fixed row order cannot say. One badge on one row says it instead, and it is readable,
  not sealed, because Holy Power is `NeverSecret`.
- **Cue set.** Overcap (B) → **have**, and readable — the difference from Havoc, whose equivalent
  is a sealed Fury readout.

### RET-3 · HP 5, Wake of Ashes READY — and deliberately unbadged

- **State.** As RET-2, but **Wake of Ashes is ready**. Holy Power is still 5.
- **Walk.**
  1. **Execution Sentence / Avenging Wrath** — on cooldown → skip.
  2. **Wake of Ashes** — available, carries **no** `overcap` badge by design, and neither sealed
     band is in range → **press.** `generators` 3.
  3. **Divine Toll** — still badged; it never gets the chance to compete.
- **Eye-direction.** ⚠ **The badge that would be honest about generation would be wrong about the
  press.** The APL's early `finishers` call is gated on `cooldown.wake_of_ashes.remains` — Wake of
  Ashes *on cooldown* — so at 5 Holy Power with it **ready** the APL presses it and accepts the
  waste, because what the button is worth is the Hammer of Light window. `overcap` is worn by
  exactly one row in this catalog, and this is the row it is kept off.
- **Cue set.** Nothing fires. The press is pure elimination.

### RET-4 · Hammer of Light window open, HP 4

- **State.** Wake of Ashes has been cast; **row 3 is displaying Hammer of Light**. Holy Power 4.
  Execution Sentence and Avenging Wrath are on cooldown.
- **Walk.**
  1. **Execution Sentence / Avenging Wrath** — on cooldown → skip.
  2. **Hammer of Light** — row 3 reads `identity == transformed`, so band 1 gives it **ROTATION**
     instead of COOLDOWN; both of its sealed holds are gated off by that same identity term, and
     `woa_starved` is dark at 4 Holy Power → **press.** `finishers` 2.
- **Eye-direction.** ⚠ **This row *was* the catalog's single point of failure until 2026-08-18.**
  Had the Cooldown Manager kept swiping it for Wake of Ashes's own running cooldown, the walk
  would skip straight past the free press and land on Divine Toll or a spender. It does not — the
  swipe follows the **displayed** spell (*Open facts* 1, and `knowledge/addon-dev/cooldown-manager.md`
  §3.1.1). The two-band identity design stands on that fact.
- **Cue set.** Identity (R7) → **have**. Nothing else fires.

### RET-5 · Hammer of Light window open, HP 2 — the window you cannot afford

- **State.** As RET-4, but **Holy Power 2**. Divine Toll is ready and Avenging Wrath is far away.
- **Walk.**
  1. **Execution Sentence / Avenging Wrath** — on cooldown → skip.
  2. **Hammer of Light** — available, but `starved` lights: `affordable` is read on the **live**
     id, which is Hammer of Light's 3 Holy Power, not Wake of Ashes's zero → skip.
  3. **Divine Toll** — no `overcap` at 2 Holy Power, and `dt_awaits_wrath`'s band is out of range
     → **press.** `generators` 4, and the Holy Power it injects is what re-arms the window.
- **Eye-direction.** Affordability read on the live identity is what makes this row honest. Read
  on the base id it would be free, the badge would stay dark, and the walk would stop on a button
  the player cannot press.
- **Cue set.** Affordability (A) on the live id (R1 + R7) → **have**.

### RET-6 · HP 4, Art of War proc — a free Blade of Justice outranks spending

- **State.** Single target, **Art of War (or Righteous Cause) is up**, Holy Power 4, every
  cooldown down, Blade of Justice ready.
- **Walk.**
  1. **Execution Sentence … Divine Toll** — on cooldown → skip.
  2. **Final Verdict** — affordable, but `blocked` lights from `tv_awaits_blade`: a proc is up,
     Blade of Justice is ready, and Holy Power is ≤ 4 → skip.
  3. **Divine Storm** — the same badge, from `ds_awaits_blade` → skip.
  4. **Blade of Justice** — **press.** `generators` 5, which sits above `generators` 6.
- **Eye-direction.** ⚠ **This is why `ds_awaits_blade` exists as a second marker.** Badging only
  row 5 would hand the walk to row 6 and the player would press Divine Storm — the correct answer
  to "not Templar's Verdict" and the wrong answer to the question actually being asked.
- **Cue set.** Readable hold (D) → **have**, on both spenders. Both proc buffs are registered
  spell-activation overlays and both point at Blade of Justice `184575`, so the APL's OR authors
  itself as one `proc` term.

### RET-7 · HP 5, Art of War proc — the proc loses

- **State.** As RET-6, but **Holy Power 5**.
- **Walk.**
  1. **Execution Sentence … Divine Toll** — on cooldown → skip.
  2. **Final Verdict** — row 5's proc-defer marker requires `resource <= 4`, which is false here,
     so the badge stays dark → **press.**
- **Eye-direction.** The `resource <= 4` term on the marker is doing the same job the `overcap`
  badge does in RET-2, from the other side: at 5 Holy Power the early `finishers` call outranks
  `generators` 5, so the proc'd Blade of Justice correctly loses to the spender sitting left of it.
- **Cue set.** Nothing fires. Elimination, with a readable term keeping the badge off.

### RET-8 · AoE mode on, 4 targets, HP 4

- **State.** The player has flipped cap's AoE toggle; four targets, no Empyrean Legacy proc,
  Holy Power 4, cooldowns down.
- **Walk.**
  1. **Execution Sentence … Divine Toll** — on cooldown → skip.
  2. **Final Verdict** — the `st_only` pawn from `tv_divine_storm_aoe`: the toggle is on, no
     Empyrean Legacy proc is live, and the spend is affordable → skip. ⚠ **Not `blocked`** —
     nothing is held here and nothing would be wasted, it is simply the other spender's turn.
  3. **Divine Storm** — **press.** `finishers` 3, via `ds_castable`'s target clause.
- ⚠ **The 2-vs-3 target threshold is the player's, not cap's.** Tempest of the Lightbringer
  without Jurisdiction moves it, and **cap models no enemy count** — the toggle is the whole
  interface. This scenario says what the badge does once the toggle is on, not when to flip it.
- **Cue set.** Mode (E) → **have**, gated on the `aoe` predicate. Its mirror `aoe_only` rides
  Divine Storm in single target, and the pair is what lets the two spenders be told apart at all.

### RET-9 · Single target, Empyrean Power proc, HP 4

- **State.** Single target, **Empyrean Power is up**, Holy Power 4, cooldowns down. The AoE
  toggle is **off**.
- **Walk.**
  1. **Execution Sentence … Divine Toll** — on cooldown → skip.
  2. **Final Verdict** — `blocked` from `tv_empyrean_power` → skip. ⚠ **`blocked`, not the
     `st_only` pawn RET-8 wears.** The mode is right here; what rules Final Verdict out is a free
     Divine Storm waiting, which is precisely "a readable dependency says the press would be
     wasted". A pawn here would tell the player their mode was wrong when it was not.
  3. **Divine Storm** — **press.** A free Divine Storm satisfies `ds_castable` with **no target
     term at all**, which is why this row looks identical to RET-8 and is a different marker.
- **Eye-direction.** ⚠ **This scenario and RET-8 used to look identical, and stopped on
  2026-08-19.** Both put a badge on Final Verdict, and while the vocabulary had one negative key
  for both, the argument here was that the player does not need to know *which* clause of
  `ds_castable` fired. That was a concession to the vocabulary rather than a finding: the two
  reasons are a **mode** and a **proc**, they are acted on differently — one is fixed by the
  toggle, the other passes on its own — and the badge's job is to carry the reason. Now they
  differ.
- **Cue set.** Proc-defer (D) → **have**, gated on `proc` rather than on `aoe`.

### RET-10 · AoE mode on, Empyrean Legacy proc, HP 4 — the exception to the exception

- **State.** AoE toggle on, **Empyrean Legacy is up**, Holy Power 4.
- **Walk.**
  1. **Execution Sentence … Divine Toll** — on cooldown → skip.
  2. **Final Verdict** — both E markers carry `!proc(templars_verdict)`, which is now false, so
     row 5 is clear even in AoE → **press.**
- **Eye-direction.** ⚠ **This state is why `!proc(templars_verdict)` is a term on *both* markers
  rather than a third marker of its own.** It is `ds_castable`'s `&!buff.empyrean_legacy.up`
  clause: an empowered Templar's Verdict beats Divine Storm at four targets. Expressed as a
  separate rule it would have had to *un-badge* a row, and the marker grammar is AND-only — there
  is no un-badging, only a term that keeps the badge dark.
- **Cue set.** Nothing fires; the negation is what keeps it that way.

### RET-11 · HP 2, no procs, Blade of Justice on cooldown

- **State.** Holy Power 2, no procs, every cooldown and Blade of Justice on cooldown.
- **Walk.**
  1. **Execution Sentence … Divine Toll** — on cooldown → skip.
  2. **Final Verdict / Divine Storm** — available and `starved`: 2 Holy Power will not pay for a
     3-cost spend → skip.
  3. **Blade of Justice** — on cooldown → skip.
  4. **Judgment** — **press.** `generators` 10 — or **Hammer of Wrath** (`generators` 9), if that
     is what row 8 is currently displaying; the row is one button and the client picks which.
- **Eye-direction.** The generator is reached by **subtraction**, exactly as Havoc's Felblade is:
  nothing promotes it, the two spenders above it demote themselves.
- **Cue set.** Affordability (A) → **have**.

### RET-12 · Execution Sentence ready, Avenging Wrath ~10s out, HP 2

- **State.** Execution Sentence is up. **Avenging Wrath is ~10s from ready**, Wake of Ashes is far
  away, Divine Toll is up, Holy Power 2, Blade of Justice ready.
- **Walk.**
  1. **Execution Sentence** — available, and `blocked` lights from **two markers at once**
     (`es_awaits_wrath` at `within = 15`, `es_awaits_wake` at `beyond = 1.5`). One badge, because
     naming the same cue twice unions into one badge — and that union **is** the OR → skip.
  2. **Avenging Wrath / Wake of Ashes** — on cooldown → skip.
  3. **Divine Toll** — `blocked` from `dt_awaits_wrath`, the same 15s band → skip.
  4. **Final Verdict / Divine Storm** — `starved` at 2 Holy Power → skip.
  5. **Blade of Justice** — **press.** `generators` 8.
- **Eye-direction.** Hold Execution Sentence: Avenging Wrath is close and Wake of Ashes is not, so
  the placed cooldown is worth a few seconds of patience. Divine Toll is held for the same window.
  ⚠ Both are **sealed** — cap hands over a band and never learns where inside it the value fell,
  so this is confirmed by eye in game, not by a capture.
- **Cue set.** Sealed hold (C) → **sealed**, on rows 1 and 4. Affordability (A) → **have**.

### RET-13 · Execution Sentence, Avenging Wrath and Wake of Ashes all ready, HP 3

- **State.** The state the sealed band cannot cover: **Avenging Wrath is ready**, i.e. zero
  remaining. Execution Sentence and Wake of Ashes are up too. Holy Power 3. Mid-fight, so
  **Expurgation is ticking** and `aw_awaits_expurgation` is dark — the difference from RET-1.
- **Walk.**
  1. **Execution Sentence** — `blocked` from `es_awaits_wrath_ready`, the **readable** half of the
     hold: `cooldown.avenging_wrath.remains>15` is false at zero → skip. `es_awaits_expurgation` is
     dark, because the DoT is up.
  2. **Avenging Wrath** — **press**, and its bottom edge carries the **Expurgation clock** (V20):
     the DoT that released this hold, draining. Nothing cap read — the slot filters to `383346`
     and the client owns the fill.
- **Eye-direction.** ⚠ **A sealed band deliberately reads nothing at zero remaining**, so RET-12's
  band goes dark in exactly the state where the hold matters most. Row 1 is the only row in this
  catalog carrying a readable companion to a sealed hold, and the reason is **position**: it sits
  left of everything it waits on, so a quiet row 1 would be pressed before the eye ever reached
  Avenging Wrath. Rows sitting to the *right* of what they wait on need only the band —
  elimination covers their zero case. **Position in the row decides which halves a hold needs.**
  ⚠ **RET-1 tested that rule and it held, but only just.** There, cue G holds a *ready* Avenging
  Wrath, so the walk does not stop at row 2 and rows 3 and 4 briefly needed companions of their
  own. Promoting the opener (cue H) removed the need and both were deleted. The rule survives
  because a promoted scenario is never read by elimination at all.
- **Cue set.** Readable hold (C) → **have**, the counter to RET-12's sealed one. The Expurgation
  clock carries **no cue** — a bar is not a verdict.
  ⚠ **The clock is here for the state this walk is NOT in.** Cue G's latch is seeded out of
  combat and mutated by alert edges afterwards, so on a setup where the Expurgation row was never
  added to Tracked Buffs no edge ever arrives, the seed stays "absent", and cap holds Avenging
  Wrath for the whole fight while looking confident (`catalog.json`'s `aw_stale_latch`). The
  container needs no such row: it is cap's own frame, `includeSpellIDs`-filtered and pointed with
  `SetUnit`. So in that state the hold badge and the draining bar sit on one row saying opposite
  things — which is the tell. It does not fix the branch; the enablement detector still has to.

### RET-14 · Light's Deliverance at 60 — RET-3 with one fact added

- **State.** Single target, mid-fight, no procs, **Holy Power 5**. Execution Sentence and Avenging
  Wrath are on cooldown, **Wake of Ashes is ready**, Divine Toll is up. **Light's Deliverance is at
  60 stacks.** Holy Flames is not talented on this build, so neither the Expurgation hold nor its
  clock exists and row 2 is an ordinary swiped row.
- **Walk.**
  1. **Execution Sentence / Avenging Wrath** — on cooldown → skip.
  2. **Wake of Ashes** — available, nothing rules it out → **press.** `generators` 3, exactly as in
     RET-3: at 5 Holy Power with Wake of Ashes *ready* the early `finishers` call at `generators` 1
     does not fire, because its condition is `holy_power=5&cooldown.wake_of_ashes.remains`.
     The row additionally carries one **positive mark** in its corner — the Light's Deliverance
     band at its upper threshold (V16).
- **Eye-direction.** ⚠ **This scenario is deliberately RET-3 with one fact changed**, and the
  isolation is the point: same build, same cooldowns, same press, one extra thing on screen. What
  the mark means is *a free Hammer of Light is banked and waiting for you*, on the row that will
  display it — and on a button you still have to press, because nothing auto-casts it. It is not a
  promotion and it does not move the press — the press was already this row.
  ⚠ **The mark is silent below the threshold.** The lower band draws `none`, so at 0–59 stacks the
  row is byte-identical to RET-3. That is the trade V16 buys over a bar: a bar has no blank state.
  ⚠ **The 60 is a RESTING state, not a threshold the counter crosses and leaves.** The spell text
  conditions the consumption on Wake of Ashes and Hammer of Light **both** being unavailable, so
  with Wake of Ashes ready the stack sits at 60 and stays there — the mark is steady, not a
  flicker, and it says "banked and waiting", never "press this now".
- **Cue set.** No cue at all. The band is a client-evaluated display, not a badge: cap authored the
  number 60 and never learns which side of it the count fell on.

### RET-15 · Target swap — Execution Sentence held, and the row beneath it is NOT the press

- **State.** Single target, mid-fight, fresh target. **Holy Flames and Execution Sentence are
  talented; Radiant Glory is not.** **Expurgation is not yet on this target.** Holy Power 2, no
  procs. **Execution Sentence is ready**, **Wake of Ashes is ready**, Divine Toll is up, **Blade of
  Justice is on cooldown**, and Avenging Wrath is ~40s out — far outside every band that names it.
- **Walk.**
  1. **Execution Sentence** — available, and `blocked` from `es_awaits_expurgation` alone: at 40s
     out neither Avenging Wrath marker fires, and Wake of Ashes is ready so `es_awaits_wake` is
     dark too. `cooldowns` 10's last term, `(!talent.holy_flames|dot.expurgation.ticking)`, is
     false → skip.
  2. **Avenging Wrath** — on cooldown → skip.
  3. **Wake of Ashes** — available, and `blocked` from **`woa_awaits_sentence_ready`**.
     `generators` 3's second clause is
     `(!talent.execution_sentence|cooldown.execution_sentence.remains>4|target.time_to_die<10)`:
     Execution Sentence is talented and its cooldown remaining is **zero**, so the first two
     disjuncts are false and the APL does not press this → skip.
  4. **Divine Toll** — available, nothing rules it out → **press.** `generators` 4, whose only
     non-simulation term is `cooldown.avenging_wrath.remains>15`, true at 40s. `dt_awaits_wrath`
     is dark for the same reason and `dt_overcap` needs 5 Holy Power.
  5. Everything to the right is read only if the eye goes looking: the two spenders are `starved`
     at 2 Holy Power and Blade of Justice is swiped, which is why cue **H** does not promote here.
- **Eye-direction.** ⚠ **This scenario is the reason `woa_awaits_sentence_ready` exists, and it is
  the defect `es_awaits_expurgation` closed, relocated one row.** Row 3 used to carry only the
  **sealed** `within = 4` band on Execution Sentence, justified by *"a ready Execution Sentence
  stops the elimination walk before it arrives."* That was true while row 1 was quiet when ready.
  It is not true now: **a held row does not eliminate the row beneath it** — the walk steps over
  row 1's badge and lands on row 3, and a sealed band reads nothing at zero remaining. Without the
  readable term Wake of Ashes drew **clear and leftmost for a press `generators` 3 forbids**.
  **Position in the row decides which halves a hold needs — and so does what the rows to your left
  are wearing.** That is the general form RET-13's note only had half of.
  ⚠ **Two holds stand before the press, which is exactly Part 0.5's budget and not over it.** The
  alternative — promoting Divine Toll — would spend a positive cue on a rank claim, which the
  shelf excludes.
  ⚠ **The `talent` term on the new marker is load-bearing.** On a build *without* Execution
  Sentence the rung's first disjunct is true and Wake of Ashes is unconditional there; an ungated
  hold would badge a press the APL makes freely.
  ⚠ **One honest over-hold, stated rather than left silent.** `target.time_to_die<10` also
  satisfies the clause, and cap does not model the encounter — no `fight_remains`, by product
  rule. So in the last ten seconds of a fight this holds a Wake of Ashes the APL presses. That is
  a **missed press, not a wrong one**, which is the direction this project accepts everywhere else.
- **Cue set.** Readable hold (C) → **have**, on rows 1 and 3, and both are readable halves of
  conditions whose sealed bands go dark at zero. Affordability (A) → **have**.

**What the walk did not have to explain.** No state in it required cap to **know** a target count,
a buff duration, an aura's remaining time or a stack count. Every *skip* above is a readable Lua
term, a sealed band on a *cooldown*, a readable readiness where the band would go dark, or — at
RET-1, RET-13 and RET-15 — the readable up/down latch on a target aura that cues **G** and **H**
are both built from. Two things are now **drawn** without
being known: the Expurgation clock on row 2 (RET-13) and the Light's Deliverance band on row 3
(RET-14). Neither eliminates a row and neither enters a Lua condition — which is why they change no
walk above. ⚠ Which of two Hammer of Light states is live is still not answerable, and
`catalog.md`'s *Open facts* 3 still owns it.

**One scenario in fifteen is read by pass 1.** RET-1 is the catalog's only promotion, and the
ratio is the point: a vocabulary where the positive cue is reached often has stopped being a
reading model and become a pointer (`../render-shelf.md` Part 0.5).

⚠ **Row 9 renders only on a Templar Strikes build.** Crusader Strike binds nothing otherwise, so
on any other build the row simply is not there and the walk is eight entries wide. It is drawn in
every scenario above because a row that exists on *some* build has to be shown reaching the end of
the walk somewhere.
