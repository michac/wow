---
title: Retribution Paladin — the scenario catalog
spec: Retribution Paladin (Templar) — specID 70, Midnight 12.1
---

# Retribution Paladin (Templar) — the scenario catalog

**What this file is for.** `catalog.md` maps every ability to a role lane and the cues. This file is the **proof** that lane + cues actually reproduce the priority order — state by state, naming the press and, for every button that is available and skipped, the reason. It is what `capart check`'s reading gate mechanises, and it is where this design gets falsified.

**Cross-links.** `catalog.md` (beside this file) is the definition — roster, lanes, markers,
contract boundary. `../spec.md` §3.1 owns the tier model and §3.6 the readable/sealed boundary;
`../pattern-shelf.md` owns the recipes; `../render-shelf.md` owns every pixel and this file
describes none. Priority source: `knowledge/classes/paladin/retribution/simc-apl.md` (Tier 1,
generated), explained by that spec's `rotation.md`; neither is restated here.

**Three files per spec, and Havoc is the model** (`../authoring.md` §0): a definition, its proof,
and its safety case.

---

## The state walk

Thirteen states, each naming the press, and for **every button that is available and skipped**,
the reason. Buttons the Cooldown Manager has already swiped need no explanation. The walk reads
the authored row order left to right and must satisfy the shape `capart check`'s **elimination
gate** enforces: *the leftmost entry that is neither swiped nor wearing a negative badge is the
press.* Row numbers are the authored order above.

Shorthand: `HP` = Holy Power. "AW", "ES", "WoA", "DT", "TV", "DS", "BoJ" are the rows.

### The **CDM row** bullet is machine-read

Every scenario below carries a `- **CDM row.**` bullet in a fixed grammar — nine entries in
authored order, separated by ` · `, each `<Ability> \`<verdict>\``. `wowkb.capart import scenarios
retribution` scrapes it into the preview's sidecar and `wowkb.capart check retribution` re-scrapes
it and fails if the two disagree, so **this document leads and the preview follows**. The ability
name is whatever the Cooldown Manager would *display* in that state — `Hammer of Light`, not
`Wake of Ashes`, while row 3 is transformed — because that is the identity the client draws and
the swipe follows (*Open facts* 1).

A verdict says what cap concluded, never what the button looks like: **the pixels belong to
`../render-shelf.md`**. `cd` = swiped by Blizzard, no cap opinion. `hold-readable` / `hold-sealed`
= the red `blocked` badge, from a readable Lua term or from a sealed band the client paints.
`starved` = the red affordability badge. `overcap` = the red waste badge. `press` = the button an
unobstructed scan reaches. `below` = shown, but the walk never got there. ⚠ `press` and `below`
render identically, by design — the press is not something cap draws.

⚠ **No entry in this catalog wears a positive cue**, so every scenario here is judged by pass 2
of `../render-shelf.md` Part 0.5, elimination. Why Retribution declines the one positive cue in
the vocabulary is argued above (*Why this catalog does not spend the positive cue*).

### RET-1 · Opener, everything ready, HP 0

- **State.** Pull timer at zero, every cooldown up, **Holy Power 0**, single-target mode, no
  procs. **Holy Flames talented, Expurgation not yet on the target** — the state the opener exists
  to end.
- **CDM row.** Execution Sentence `hold-readable` · Avenging Wrath `hold-readable` · Wake of Ashes
  `below` · Divine Toll `below` · Final Verdict `starved` {client: not-enough-power} · Divine Storm `starved` {client: not-enough-power} · Blade of Justice `press-promoted` {cues: priority} ·
  Judgment `below` · Crusader Strike `below`
- **Walk.** ⚠ **This scenario is read by pass 1, not by elimination** — the only one in the
  catalog that is.
  1. **Blade of Justice** wears `priority` (cue **H**, `boj_opener`) → **press.** `generators` 2,
     the rung that puts Expurgation up. The condition is that rung: Holy Flames talented, the DoT
     absent, the button ready.
  2. Everything else is read only if the eye goes looking. Execution Sentence and Avenging Wrath
     are genuinely held — `es_awaits_wrath_ready` and `aw_awaits_expurgation` — and the two
     spenders are unaffordable at 0 Holy Power. None of that has to be interpreted to find the
     press.
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
- **CDM row.** Execution Sentence `cd` · Avenging Wrath `cd` · Wake of Ashes `cd` ·
  Divine Toll `overcap` · Final Verdict `press` · Divine Storm `off-mode` {cues: aoe_only} · Blade of Justice `below` ·
  Judgment `below` · Crusader Strike `below`
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
- **CDM row.** Execution Sentence `cd` · Avenging Wrath `cd` · Wake of Ashes `press` ·
  Divine Toll `overcap` · Final Verdict `below` · Divine Storm `off-mode` {cues: aoe_only} · Blade of Justice `below` ·
  Judgment `below` · Crusader Strike `below`
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
- **CDM row.** Execution Sentence `cd` · Avenging Wrath `cd` · Hammer of Light `press` ·
  Divine Toll `below` · Final Verdict `below` · Divine Storm `off-mode` {cues: aoe_only} · Blade of Justice `below` ·
  Judgment `below` · Crusader Strike `below`
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
- **CDM row.** Execution Sentence `cd` · Avenging Wrath `cd` · Hammer of Light `starved` {client: not-enough-power} ·
  Divine Toll `press` · Final Verdict `starved` {client: not-enough-power} · Divine Storm `starved` {client: not-enough-power} ·
  Blade of Justice `below` · Judgment `below` · Crusader Strike `below`
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
- **CDM row.** Execution Sentence `cd` · Avenging Wrath `cd` · Wake of Ashes `cd` ·
  Divine Toll `cd` · Final Verdict `hold-readable` · Divine Storm `hold-readable` {cues: aoe_only} ·
  Blade of Justice `press` · Judgment `below` · Crusader Strike `below`
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
- **CDM row.** Execution Sentence `cd` · Avenging Wrath `cd` · Wake of Ashes `cd` ·
  Divine Toll `cd` · Final Verdict `press` · Divine Storm `off-mode` {cues: aoe_only} · Blade of Justice `below` ·
  Judgment `below` · Crusader Strike `below`
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
- **CDM row.** Execution Sentence `cd` · Avenging Wrath `cd` · Wake of Ashes `cd` ·
  Divine Toll `cd` · Final Verdict `off-mode` {cues: st_only} · Divine Storm `press` ·
  Blade of Justice `below` · Judgment `below` · Crusader Strike `below`
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
- **CDM row.** Execution Sentence `cd` · Avenging Wrath `cd` · Wake of Ashes `cd` ·
  Divine Toll `cd` · Final Verdict `hold-readable` · Divine Storm `press` ·
  Blade of Justice `below` · Judgment `below` · Crusader Strike `below`
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
- **CDM row.** Execution Sentence `cd` · Avenging Wrath `cd` · Wake of Ashes `cd` ·
  Divine Toll `cd` · Final Verdict `press` · Divine Storm `below` · Blade of Justice `below` ·
  Judgment `below` · Crusader Strike `below`
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
- **CDM row.** Execution Sentence `cd` · Avenging Wrath `cd` · Wake of Ashes `cd` ·
  Divine Toll `cd` · Final Verdict `starved` {client: not-enough-power} · Divine Storm `starved` {client: not-enough-power} · Blade of Justice `cd` ·
  Judgment `press` · Crusader Strike `below`
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
- **CDM row.** Execution Sentence `hold-sealed` · Avenging Wrath `cd` · Wake of Ashes `cd` ·
  Divine Toll `hold-sealed` · Final Verdict `starved` {client: not-enough-power} · Divine Storm `starved` {client: not-enough-power} ·
  Blade of Justice `press` · Judgment `below` · Crusader Strike `below`
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
- **CDM row.** Execution Sentence `hold-readable` · Avenging Wrath `press` · Wake of Ashes `below` ·
  Divine Toll `below` · Final Verdict `below` · Divine Storm `off-mode` {cues: aoe_only} · Blade of Justice `below` ·
  Judgment `below` · Crusader Strike `below`
- **Walk.**
  1. **Execution Sentence** — `blocked` from `es_awaits_wrath_ready`, the **readable** half of the
     hold: `cooldown.avenging_wrath.remains>15` is false at zero → skip.
  2. **Avenging Wrath** — **press.**
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
- **Cue set.** Readable hold (C) → **have**, the counter to RET-12's sealed one.

**What the walk did not have to explain.** No state in it required cap to know a target count, a
buff duration, or which of two Hammer of Light states was live. Every skip above is a readable Lua
term, a sealed band on a *cooldown*, or — at RET-1 only — the readable up/down latch on a target
aura that cues **G** and **H** are both built from.

**One scenario in thirteen is read by pass 1.** RET-1 is the catalog's only promotion, and the
ratio is the point: a vocabulary where the positive cue is reached often has stopped being a
reading model and become a pointer (`../render-shelf.md` Part 0.5).

⚠ **Row 9 renders only on a Templar Strikes build.** Crusader Strike binds nothing otherwise, so
on any other build the row simply is not there and the walk is eight entries wide. It is drawn in
every scenario above because a row that exists on *some* build has to be shown reaching the end of
the walk somewhere.
