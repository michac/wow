# Combat Assist Plus — notes

**What this file is for:** the running record of what we did — session logs,
decisions and why they went that way, things we tried that didn't work, in-game
observations. Append-only in spirit: this is the file you read to find out how the
project got where it is.

It is deliberately the *loose* one. `spec.md` says what the addon should do and
`backlog.md` says what's left; anything that doesn't fit either — a measurement, a
dead end, a rationale, a "next session, start here" — lands here rather than
getting lost or being forced into a spec line.

Newest session at the top. Date each entry.

⚠ **A fact about how the game or the API behaves does not stop here.** That goes to
`knowledge/addon-dev/` (see the wow-developer skill's "Improve the KB as you go") —
this file records *our* work, not the client's behaviour.

---

## 2026-08-10 (FIRST PIXELS) — v0.2.4 flown, and four things play said that the desk could not

**cap drew on screen for the first time.** v0.2.4 released and deployed, one Demonology pull.
Everything from M3c onward — the graded register, the cues, the proc-glow dim and §3.4's bars —
had been built, reviewed four times and never executed in the client. **It works**: the surfaces
render, the binding holds, and the player's verdict was *"hey it works!"* before any of the
detail below.

⚠ **This entry is the player's report, not a measurement.** No capture backs any of it: the
`draw` ring on disk at time of writing is **entirely v0.2.3** across all 8 sessions and carries
no `glow:`, `nosize:` or `B{}` field at all, because SavedVariables only flush on `/reload` and
the pull had not been followed by one. Every number named below is a number from the source, not
from the flight. The four items are filed as **D14–D17**.

### What play said

1. **The tier glows read as candles.** *"Way too flickery … needs to be brighter across the
   board."* → **D14**. The tier alphas were measured by a person on real icon art; the **pulse
   trough (0.68) was picked at a desk**, and it is the number that decides how far a ring dips.
   The one thing nobody looked at is the leading suspect.
2. **A transformed row lights for its whole cooldown.** Grimoire: Imp becomes **Consume Magic**
   when on cooldown — a real, castable, off-cooldown utility — so `ready(this)` reads true and
   E3 sits emphasised through the entire downtime. → **D15**. cap is not misreading anything;
   the catalog never said which identity it meant.
3. **Tyrant's HIGH promotion is wrong.** It should be MEDIUM whenever off cooldown, with
   **markers** for the setup pieces (dogs out, grimoire out) rather than a tier bump. → **D16**.
4. **The proc glow was NOT suppressed.** A proc'd Demonbolt still dominates the screen; same on
   Infernal Bolt. → **D17**. This is `Glow.lua`'s first measured result and it is a negative one.

### The three things this flight is worth more than the code it tested

**E1's HIGH promotion was a desk decision, measured firing correctly, and play reversed it.**
The rule is `ready(this) and not ready(E2)` → HIGH: Tyrant is urgent once Dreadstalkers is on
cooldown, i.e. once the pets are out. The **M3b flight measured it landing within 2 s of the
Dreadstalkers cast** and recorded it as working — and it *was* working, in the only sense that
flight could test. It is still the wrong behaviour. **A flight that measures a rule firing
correctly says nothing about whether the rule is right**, and nothing in this project's
instrument set can close that gap: `busted` tests the arithmetic, the capture tests that the
arithmetic reached a pixel, and neither has an opinion about what the arithmetic should be.
That is the clearest case yet for `simplify → draw → add detail from play`, and it is worth
remembering the next time a tier rule looks obviously right on paper.

⚠ **Do not call this rule `dogs_out`.** That was the *window* it replaced, and the window
migration deleted the vocabulary along with the mechanic — the term survives only in
pre-migration history (`notes.md` 2026-08-07/08 and `backlog.md`'s `## Reference`). The
pre-migration flight record also called it *"the catalog's centrepiece"*, which described
**windows as the catalog's cross-ability reasoning mechanism** — true at the time and false
since they were removed. Quoting either forward is the "a rule surviving in a header is how it
comes back" failure one file over; both were caught in review of this very entry.

**A negative result on `Glow.lua` is exactly why its claim was never written to the KB.**
`backlog.md` filed the proc-glow dim recipe as **blocked on the flight** rather than draining it
into `cooldown-manager.md`, on the grounds that it was read off CDMProbe's source and never
measured by us. Had that been written as a `[client]` claim on faith, the KB would now carry a
mechanism that demonstrably does not work here, and the next project would inherit it. The
restraint paid.

**The instrument was not there when it was needed, and the reason is procedural.** `glow:` would
have separated *"nothing was hooked"* from *"hooked and the pixel did not move"* in one glance,
and it exists precisely for that — but a capture only reaches disk on `/reload`, and a flight
that ends without one leaves the log describing the *previous* build. Worth making the
`/reload` part of the flight, not a step after it.

### What was NOT decided here

Nothing. All four went to `discussion.md` with the case on both sides, because three of them
have a genuinely open **how** even though the **what** is settled: D15's fix could be four lines
in one catalog entry or one invariant in `Tier`; D16 needs a marker driven by a gate, which the
§3.0 vocabulary does not currently admit; D17 has four candidate causes that a single capture
field would separate. Only D14's direction ("brighter, less flickery") is unambiguous, and even
there the fault could be the trough, the rate or the ADD blend.

## 2026-08-10 (the bars fix pass) — a picked number wearing a derivation's clothes, and three declarations of one roster

**Done, static only. `Bars.lua`, `Treatment.lua`, `Sense.lua`, `treatment_spec.lua`,
`bars_spec.lua`; `spec.md` §3.4, `catalog.md` §1/§2/§4, `discussion.md` **D13**, `backlog.md`.
busted 163 → 164, luacheck 0/0 in 23 files, 11 mutations run and 10 caught (the eleventh could
not be written after the seam narrowed — below). ⚠ **Nothing here has run in the client** —
the round below never drew a pixel and neither does this one. `armed` is still the strongest
word in the log and it means cap handed the client a duration object.**

A review of the bars round below. Its headline finding is the same failure mode as the
2026-08-08 (polarity) entry, one surface over.

### The one that mattered: `BAR.rest` was a picked number dressed as a derivation, promoted to `spec.md`, and pinned by a test — inside LOW's own band

Four separate faults, and they compound in that order:

- **The value collided with the tier it sits under.** LOW is the slate `0.80 0.82 0.88` over
  the alpha band `0.36 – 0.50`; the resting fill was **the same hue at alpha `0.40`**, inside
  that band. A LOW bar at grade ≈`0.286` rendered the resting fill exactly. On an icon
  §3.1 makes the LOW → *none* step **the presence of a ring** — and a bar has no ring, so on
  this surface the step had no carrier at all while §3.4's new table normatively specified two
  states that draw the same pixels. It is the collision §3.1 already forbids for markers
  (*"LOW's hue is the hold slate… a positive cue therefore stands for HIGH or MEDIUM"*).
- **The justification was an analogy.** *"The bar carries no artwork to veil, so it takes the
  veil's own fraction instead"* — a veil at `0.60` multiplies an **icon's own light** by 0.40;
  a slate at alpha `0.40` over a dark track over the panel is a different quantity in a
  different composite. The test comment said the mechanism does not apply and then used the
  number anyway.
- **A test ratcheted the analogy into an invariant.** `assert.equal(1 - T.Tier("none").veil,
  T.BAR.rest.a)` made the analogy the **only** thing pinning `0.40` — a rung stronger than the
  struck polarity rule ever got.
- **`BAR.track`'s four values went normative into `spec.md` with no argument at all**, sitting
  in one table beside §3.1's measured numbers with nothing separating measured from picked.

**The derivation this lands on, and it is only an ordering.** The claim that survived the
§3.1 cull is *"the ladder is ordered"*, and *none* is its bottom rung. A bar has no ring, so
the fill is the only thing that can carry the LOW → *none* step — therefore **the resting fill
must read under LOW's dimmest**. The resting slate is LOW's own hue, so on the shared hue that
reduces to an alpha strictly under LOW's dim end of `0.36`. That much follows from a surviving
property and from nothing else.

**The number inside that bound is PICKED, and it is stated as picked.** `rest.a = 0.24`. The
resulting gap to LOW's dim end is `0.12`, about the width of LOW's own band — offered so a
reader can judge the pick, **not** as its derivation. Nobody has seen it. `BAR.track` is
picked outright and is now labelled so. `spec.md` §3.4 states the three **properties** and
carries no numbers; `Treatment.BAR` holds the values with a ⚠ that only the ordering is
derived; and `discussion.md` **D13** is the open question, filed the way D10/D11 were: what
should these two actually be, decided by looking, since `B{}` reports `armed` and can never
report a colour. `backlog.md`'s *Judge the bars on screen* now names them alongside the three
legibility questions it already had.

**The test asserts the property, not the arithmetic.** *"rests under every reachable LOW
fill"* checks the resting hue **is** LOW's (so an alpha comparison is a legitimate brightness
comparison) and then that the resting alpha is strictly under LOW at 21 grades across `0..1`.
Beside it, *"orders the four fills, none lowest"* walks the bar ladder on one scalar —
`Treatment.FillBrightness`, added because `Brightness`'s negative-veil branch says nothing
about a surface with no veil. The old identity assertion is gone.

⚠ **Unreachable on Demonology, and that is not a defence.** No entry on the roster bands LOW
(E1/E2/E3 are HIGH/MEDIUM, E8 MEDIUM), so nothing on this catalog could have hit the
collision. It is a property of `Treatment.Fill`, the **shared engine** every future spec draws
through, and it was written into `spec.md` as a normative table before any spec could reach it.

### `catalog.md` declared the roster three times, one of them in a field the code refuses at load

Five `- **bar:** …` bullets sat in the same field list as `- **grade:**` and `- **cue:**`
while `Catalog.Check` **fails** any entry carrying `bar` — so a transcriber following the
document produced a catalog that dies at load, in a section whose own new text says *"a
catalog shipping both is a load-time finding"*. §1's roster table carried a third declaration,
a `Bar` column, in a round whose whole argument was that two declarations of one fact drift.

**Reduced to one: §4's ordered list.** The bullets and the column are gone; §1 points at §4,
and §4 says in as many words that it is the only declaration and that the addon refuses both
halves of the drift (an entry declaring `bar`, and a `bars` id that is not an entry). Nothing
about *which* abilities get bars changed. One adjacent tidy while in the file: §4's Power
Siphon ⚠ opened *"for the reason this section used to give for both"* — a history marker in a
present-tense document.

### The five smaller ones

- **`relayout` detached without resetting the show flags** — finding 5's exact failure.
  `Frame.Detach` hid the row's frame but left `barShown` and `snapped` set, so a pooled row
  brought back by a roster change was `Show`n with `snapped == true`, skipped
  `SetToTargetValue` and interpolated out of a stale value — which is precisely what §4.8.1
  finding 5 exists to prevent. `dark()` had it right via `showBar(r, false)`; the detach loop
  did not. Both now go through one `release(r)`. ⚠ **No desk test:** the surface needs a
  client, and a fake of `CreateFrame` would be a model of our belief (house rule 6).
- **`refused` covered two different failures** — "the read was absent or threw" and "the sinks
  raised" both reported `refused`, so a flight could not tell which. Split into `refused` (the
  read) and `unarmed` (the sinks). ⚠ **Two cells, one set of pixels**: both still draw an
  empty track carrying `--`, so the three-sets-of-pixels claim below is unchanged. The `B{}`
  table in `backlog.md` carries both rows and says so.
- **The `SetStatusBarTexture` justification asserted a client fact the KB does not carry** —
  *"an older arity returning nothing would read the same as a refusal"*. The KB records the
  bool for 12.0.7 and there is no older arity on the target client. **The decision is right
  for a stronger reason:** standing down on `notex` leaves the player nothing, where carrying
  on still leaves them a track and a number. Behaviour unchanged, reason rewritten, in the
  code and in `backlog.md`'s `bar:` table. (House rule 1: a fact about the game does not live
  in a comment — and this one was not a fact.)
- **Two descriptor fields were produced and never consumed** — `cooldownID` and `grade`, with
  `bars_spec` pinning output nothing reads. Dropped rather than kept for a rung that has not
  been written; the hold-cue rung can add what it actually needs.
- **`Sense.Catalog()` was the widest accessor for the narrowest need** — it handed every
  surface the live mutable catalog so that one caller could read one field. Replaced by
  **`Sense.Roster()`**, returning the ordered id list and nothing else, and `Bars.Plan` now
  takes `(roster, out)`. A surface that draws bars cannot reach bands or cues through it.
- **`backlog.md` cited `catalog.md` §4 for a sentence the same round wrote** — the hold-cue
  rung quoted *"the bar is the roomier surface…"* as pre-existing support, and `git log -S`
  finds it nowhere in history. True as of the commit, so not a reconstruction violation, but
  it read as an inherited argument. Attribution fixed in place.
- **`Bars.Report()` can return probe `"-"`** (no row ever built) and the `bar:` table did not
  list that cell. Added.

### The mutations, and the one that could not be written

Ten caught. On `Treatment`: `rest.a` back to `0.40` (the struck value) · `rest.a` to `0.36`
(equal, not strictly under) · the resting hue off LOW's slate — each caught by *rests under
every reachable LOW fill*; and MEDIUM's band sunk under LOW, caught by the new bar-ladder test
**and** by §3.1's icon ladder. On `Bars.Plan`: sorting the roster · inventing a default roster
for a nil one · asking about the row's `cooldownID` instead of its spell · giving an unbound
entry a spell anyway · taking the resting treatment for every bar · never looking the verdict
up (four tests).

⚠ **The eleventh is not writable and that is the point.** *"carries the BOUND row's spell,
not the authored one"* used to be mutable by reaching for the catalog's authored id — and
after the `Sense.Roster()` narrowing `Bars.Plan` **cannot see the catalog at all**, so the
fault the assertion guards against is now unreachable by construction. Substituting `row.base`
for `row.primary` survives the suite, because the fixture's rebound row legitimately has both
equal: a Fel Ravager build's row *is* based on Fel Ravager, and it is E3's `alt` that binds it.

### Considered and declined

**The comment-ratio ratchet (review finding 9).** Declined as instructed, and the numbers are
sub-noise: `Catalog.lua` 0.3639 → 0.3642, `Sense.lua` 0.2346 → 0.2371, `Catalogs/Demonology.lua`
0.119 → 0.133. What this round did do is hold its own line rather than add to the creep: the
new comments were trimmed until each touched file came out at or under where it started —
`Bars.lua` **0.3317** (0.330 before, and under the 0.35 new-file bar), `Treatment.lua`
**0.3423** (0.3472 before), `Sense.lua` unchanged at 0.2394 by line count.

### What was deliberately not done

- **No release, no deploy, no flight, no commit, no push.** This round ends at the desk.
- **No `knowledge/addon-dev/` write.** Nothing here is a fact about the client — the one
  claim that pretended to be (the `SetStatusBarTexture` arity) was deleted, not promoted.
- **The behaviour the round below found is untouched and it is right**: a bar counts down
  whether or not cap has an opinion, because every band on E1/E2/E3 requires `ready(this)`.
  Only the number, its justification, its spec status and its test moved.
- **D12 not settled**, and E8's cue not redesigned off it.

## 2026-08-10 (the cooldown bars, first pass) — the roster overturned on the merits, and a bar that counts down without an opinion

**Done, static only. New `Bars.lua`; `Treatment.lua`, `Catalog.lua`, `Catalogs/Demonology.lua`,
`Sense.lua`, `Overlay.lua`, the `.toc` and `.luacheckrc`; `tools/wowkb/addon.py`; `spec.md` §3.4,
`catalog.md` §1/§4, `discussion.md` D12, `backlog.md`. busted 147 → 163, luacheck 0/0 in 23
files, 12 mutations run and caught. ⚠ Nothing here has run in the client** — no bar has drawn,
no timer has ticked and no number has appeared. `armed` is the strongest word in the log and
it means cap handed the client a duration object.

**The roster changed, and the document was edited rather than diverged from.** `catalog.md` §4
listed **E4 Summon Doomguard** as the fourth bar and carried a ⚠ excluding Implosion and Power
Siphon because *"a 15 s bar is noise, and neither ability's decision is about time remaining —
it is about a count cap cannot see."* Both halves fail, and for different reasons:

- **"Not about time remaining" is wrong for Implosion in steady state.** Once the rotation is
  rolling you almost always have 6+ Wild Imps up, so the count is **saturated** and stops
  discriminating; what gates the press is the **15 s cooldown**. The count is the limiting
  factor at the start of a pull and the cooldown is the limiting factor for the rest of it,
  and the rest of it is most of it. (Player judgement, recorded because it contradicts a
  written catalog claim.)
- **E4 does not bind.** O3 settled it on 2026-08-06 — `1276672` is in no row of the 21-row
  capture — so a Doomguard bar draws nothing at all. The **entry** stays authored; the bar
  goes. A bar that never binds is a hole in the panel rather than a spare.
- **Power Siphon still gets no bar**, and the old ⚠'s reasoning is exactly right about it: the
  gate is "Demonic Core stacks ≤ 1", not the 30 s cooldown.

⚠ **The same argument bears on E8's own cue and this round did NOT act on it.** E8 says the
imp count *"crosses 6 in bursts, so the HIGH-styled number arrives and leaves with the actual
opportunity"* — which is the opposite of saturated. If the bar argument is right the cue is
close to permanently lit, which is the exact failure the entry's ⚠ says it stopped its **band**
at MEDIUM to avoid. Filed as `discussion.md` **D12** with what would decide it: the duty cycle
of `armed` on E8's `C{}` cell across a flown pull, which needs no new instrument.

**Two declarations of the roster existed and neither was validated.** `catalog.bars` and a
per-entry `bar = true` both shipped, `Catalog.lua` checked neither, and they already disagreed
(the flags said E1–E4, the list said E1–E4, and the document's §1 table said something a
reader had to reconcile by hand). `bars` wins because **order is part of the declaration** — a
panel stacks and a flag carries no order. The flags are deleted, and two load-time checks now
refuse an entry that declares one and a `bars` id that is not a declared entry.

**The finding that shaped the design: a bar's tier is nil for exactly the stretch the bar is
useful.** Every one of E1/E2/E3's bands requires `ready(this)`, so an ability on cooldown has
no tier at all — and that is precisely when its bar has something to show. A bar hidden or
blank without a tier would have been invisible through most of a pull. So the bar is a surface
in its own right: it counts down regardless, and the tier colours it when there is one. That
needed one new number (`Treatment.BAR.rest`, the slate at alpha `0.40`) and one clause in
`spec.md` §3.4 — the resting fill takes **the light §3.1's veil leaves**, because a bar carries
no artwork to veil and recedes by the same fraction instead. This is also the same fact
`discussion.md` **D7** parked on M4's drawn bars, and the backlog line now says so.

**Ready is a different widget, not a re-armed one.** A ready spell has no remaining cooldown,
so `ignoreGCD = true` hands back nothing — and releasing a timer bar (`SetMinMaxValues(0, 0)`)
and re-arming it is a sequence nothing has measured. So `ready` draws a plain full-width
texture and the timer bar is hidden, which also makes `SetToTargetValue`'s *first show only*
rule (§4.8.1 finding 5) fall out of Show/Hide rather than out of a flag someone has to
maintain.

**Three states, three sets of pixels — and only two of them are cap's to tell apart.** The
brief asked that zero, expired and broken be visibly distinct. The formatted string is
**secret**, so cap cannot read it back and cannot know whether the client drew a number or
nothing; what separates the three is the *fill*. `ready` is full and unnumbered, `armed` is the
client's fill and the client's string, `refused` is an empty track carrying cap's own `--`.
**`--` never stands for zero** — that answer belongs to the client and does not come back.

**Deferred, and filed rather than half-built:** the **hold cue on a bar**, which is §4's
headline value and the riskiest part of it. It gets its own rung once pass 1 has been seen.
Also deferred: judging the four rows on screen, and D7's grade question.

**One tooling fix, one line.** cap's `wowkb.addon` registry entry had no `test_dir`, so
`wowkb.addon release cap` never ran `busted` as a release gate even though `.busted` has
pointed at the suite since M3a. `luaparser` proves the Lua parses; only `busted` proves it
still decides correctly.

---

## 2026-08-10 (the record fix pass) — a false claim about a red test, quotes from a tree `git` never saw, and a flight that cannot answer its own question

**Done, static only. `Overlay.lua`, `treatment_spec.lua`, `notes.md` (two earlier entries
corrected in place), `backlog.md`, `discussion.md` D11. busted 147 → 147, luacheck 0/0 in
21 files, 2 mutations run and caught. ⚠ Nothing here has run in the client** — every fault
below was found by reading and arithmetic, and none of the fixes has drawn a pixel either.

A review of the two rounds below. Three of its findings are about **this file** rather than
the code, which is the reason the round exists: `notes.md` is the only record of an argument
whose `spec.md` side was never committed, so a wrong sentence here is not recoverable from
anywhere.

**The one that mattered: this file said a red test was green.** The §3.1-cull entry claimed
both deleted disjointness tests *"still passed after LOW moved, which is precisely why they
had to go with the rule"*. Run against the bands as they stand, one passed and one was
**red**: a fully graded MEDIUM reads `0.518622` against the dimmest HIGH's `0.746441`
(passes), but LOW's bright end reads `0.410040` against MEDIUM's dim end `0.319152`, so
*"gives every tier a band disjoint from the next one down"* was failing when it was deleted.
The same entry had the arithmetic **right** forty lines later, in the paragraph arguing LOW
back to 0.50 — so it contradicted itself, and the half a reader meets first was the wrong
half. Corrected in place. ⚠ **The deletion was still right and the reason is worth stating
plainly: both went because the rule they assert is gone, not to make the suite green.** A
round that deletes a red test *and* misreports it as green is indistinguishable from one that
deleted it to get to zero failures, which is why the record mattered more than the outcome.

**The misquote defect the fix-pass entry named is worse in the entry below it.** That entry
repaired one fabricated quote and set the standard — *a quoted string absent from the history
is the one thing `notes.md` cannot afford*. By it, the cull entry fails repeatedly:
`git show HEAD:projects/combat-assist/specs/spec.md` contains **none** of *monotone*,
*disjoint*, *fixed place*, *proc-glow art*, *brighter of the two*, *colour-blind*,
*greyscale* or *Hue is the accent*. §3.1's whole `#### What a treatment looks like`
subsection is an all-`+` block in `git diff` — **it has never been committed**, so the rules
the cull struck existed only in a working tree, and the entry that argues about them is the
one artifact of them. Only *"A positive cue is not a second visual language"* survives the
check (`HEAD`'s `spec.md:165`). Same in the addon repo: three of the five quoted test names
are in commit `f711956`, and *"tracks the grade, so the pulse never lifts an entry out of its
band"* is in none — `git log -S` finds it nowhere, because the restyle that created it is
also uncommitted.

⚠ **The repair available at a desk that may not commit is a label, not a citation.** The
quotes stay — the argument is unreadable without them — marked as **reconstructions of an
uncommitted tree** rather than as quotations, so a future reader knows the struck text is not
recoverable from `git` and stops looking. Three warnings were added: one on the cull's *What
was struck*, one on its test-count list, one on the fix-pass entry's *monotone in pulse rate*.

**A flight cannot answer D11, and would have come back "looks fine" for the wrong reason.**
D11 defers to *"a pull where E7 Demonbolt is graded down at LOW while something else sits at a
dim MEDIUM"*. The **bands** overlap — LOW's bright end 0.4100 against MEDIUM's dim end 0.3192
— but **the Demonology catalog never reaches the overlap**, and every step of that is forced
by the catalog rather than by the treatment table. E7 enters MEDIUM only at `shards ≤ 3` while
grading `resource` *falling*, which pins the grade at `≥ 0.4`; E5's needs `affordable`, and
Hand of Gul'dan's 3-shard cost pins it at `≥ 0.6`. Going the other way, E7's LOW band needs
`shards ≥ 4` on that same falling grade, so a graded LOW is pinned at `≤ 0.2`. **Brightest
reachable LOW `0.3526` (an *ungraded* E9/E10), dimmest reachable MEDIUM `0.3989` — a gap of
0.046.** Measured by sweeping every gate combination the catalog admits with affordability
tied to the DB2 cost, not by reading the table. Recorded **in D11 itself**, with what
observing the real adjacency would take (a LOW band reachable at a high grade — nothing on
Demonology grades that way — a second spec, or a deliberate lab mock), and the `backlog.md`
line that pointed at the flight now says so too.

**One culled-rule orphan survived the cull, in the worst place.** `backlog.md`'s M3c
flight-reading table still read *"that entry LOST its row to a brighter sibling"*.
`Overlay.lua`, its `draw`-pass comment and `spec.md`'s *"Two entries may bind one row"* were
all moved to **higher tier** when `Treatment.Rank` landed; the table a pilot reads while
diagnosing was not, so it described a comparison the code stopped making. Fixed, and it now
says the part that is easy to get wrong out loud: a **dimmer** cell can be the one carrying
the `*`. A sweep of `specs/` and the addon for the rest of the culled vocabulary
(*brighter* / *disjoint* / *monotone* / *fixed place* / *second visual language*) found no
other survivor — the remaining hits are records of the cull, `discussion.md` arguments, or
unrelated (`catalog.md`'s *four shards reads brighter than three* is a grade **inside** one
tier, which is exactly what survived).

**Four code findings, and only one of them changes behaviour.**

- ⚠ **`SetStartDelay` under `SetLooping("BOUNCE")` is unverified, and `P{}` asserts a rate
  that may be untrue.** `frames-textures-animation.md` §7.3 records the setter as
  `AllowedWhenUntainted` and records **nothing** about whether the delay re-applies on each
  loop iteration. If it does, a row's period is `cycle + delay`, so `cell()`'s `p2.5`/`p1.2`/
  `p0.5` names a rate nothing runs at, and rows *in the same tier* pulse at different rates —
  which is not the claim §3.1's desync safety property makes (unequal rates **between** tiers
  plus a per-row offset). Marked `--@unverified` on `armPulse` and added to the flight
  acceptance set, per house rule 5. Second-order and true either way: a re-arm re-pays the
  delay, so a row whose treatment changes faster than its own delay never reaches a first
  pulse — **LOW's worst case is ~1.98 s**.
- **The justification calls were unreachable on one path**, which is the only behaviour
  change in the round. `SetJustifyH`/`SetJustifyV` sat **after** `buildCountPulse`'s early
  return, so on `mark:…/nopulse` — the one path where an inherited non-centre justification
  still matters, because the glyph is static — they never ran. Moved above the return.
- **Two animation groups play with nothing to draw**, and neither is a bug. `buildFlip`
  plays at build, so every pooled overlay's flipbook runs all session whatever the tier; and
  `paint` arms the pulse before the line that may hide an unsized ring host. A line each,
  because the next reader will otherwise "fix" one of them.
- **`layer()`'s combat early-out guards more than it used to.** It now also gates
  `ringHost:SetFrameLevel(LEVEL - 1)`, and a default child level is parent+1 — so a frame
  first acquired in combat would draw its ring **over** the count and hold markers. The
  doctrine that prevents it (everything acquired out of combat) holds and is stated at
  `layer`; what was wrong was `buildRingHost`'s comment asserting the ordering as a flat
  fact. Both comments now say which one establishes it. **Not** established unconditionally
  on purpose: the only way to do that is to call a protected, in-combat-unmeasured setter on
  the hot path, which trades a comment defect for a real one.

**And one surviving cross-tier `Brightness` assertion, by this round's own standard.**
`treatment_spec.lua`'s *"lights Dreadstalkers brighter than a demoted Demonbolt"* compared a
graded HIGH against a graded LOW on one scalar — the exact comparison shape the cull removed
the rule for. It holds by a wide margin, which is what makes it the quiet kind. **Re-expressed
rather than deleted**, because the claim underneath it is real and `Rank` is what now carries
it: it asserts the two tiers (`HIGH`, `LOW`) and then `Rank(E2) > Rank(E7)`, which is what
`outranks` actually does. Test count unchanged at **147**.

**Two findings considered and declined.**

- **A transient shared pulse phase after a bound-set change.** `rebuild` re-derives
  `phaseOf` off the sorted order, so rows can briefly share an offset while the new order
  settles. It is out-of-combat only (a settle never happens in a pull), and the seizure
  floor the offsets exist for is about a screenful flashing together *sustained*, not a
  frame of it during a spec swap. Declined.
- **`Treatment.lua`'s ratchet at 0.3333.** House rule 1's comment:code ≤ 0.35 applies to a
  file created or substantially rewritten; the restyle was neither, and every block there is
  a fact an editor would break. Declined on rule 1's own substantial-rewrite clause.

⚠ **One ratchet was moved and it should be said rather than buried.** `Overlay.lua` went
**0.284 → 0.306** comment:code, which is an increase on a file that was touched, against rule
1's "may not increase". It stays under the 0.35 target, and the additions are the two things
rule 1 names as earning prose — a `--@unverified` (rule 5) and invariants an editor would
silently break. Three existing blocks were tightened to pay part of it back; the rest is
accepted knowingly, not overlooked.

**What was deliberately not done.** No release, no deploy, no flight, no commit, no push, no
`knowledge/addon-dev/` write. `Treatment.RING.atlas` untouched — D10 settles on a flight.
The `SetStartDelay` question was **not** answered by reading Blizzard's XML or by reasoning
about what a loop "should" do — it is a client behaviour and it stays a marker until someone
looks.

## 2026-08-10 (the restyle fix pass) — the blank screen that read as a healthy pull, and three quieter ones

**Done, static only. `Treatment.lua`, `Overlay.lua`, `treatment_spec.lua`, `spec.md` §6,
`backlog.md`. busted 145 → 147, luacheck 0/0 in 21 files, 4 mutations run and caught.
⚠ Nothing here has run in the client** — every fault below was found by reading, and none of
the fixes has drawn a pixel either.

The WP2 review, applied after the §3.1 cull had already rewritten the same files. Two of its
findings changed meaning under the cull and are recorded as such rather than actioned.

**The one that mattered: a refused `GetWidth` drew nothing and the log said everything was
fine.** The ring is sized off `item:GetWidth()`, which is `ConstSecretAccessor` +
`SecretWhenAnchoringSecret`; `sizeRing` correctly refuses to guess and `paint` correctly
hides an unsized ring — and **nothing counted it**. A tiered row draws no veil either (the
veil is 0 wherever a ring exists) and `f:Show()` still ran, so a pull in which every width
read refused would print `anch:21 conf:21 nf:0 off:0` with full `P{}` cells: byte-identical
to a working pull. That is the failure `Overlay.lua`'s own doctrine forbids three functions
higher up — *"`hidden` and `noframe` are different failures and are counted apart… Conflated,
a total anchoring failure reads as a pass."* Fixed with a `nosize:` counter in `D{}`, beside
the two it belongs with, and a reading table in `backlog.md`. ⚠ The prose warning that was
there instead is what makes this worth writing down: **a `D{}` counter exists so a flight
does not need the eyeball; a paragraph telling the pilot to go and look is the counter's
absence with extra steps.**

**The alpha write was reverted one line after it was made.** `paint` wrote
`ringHost:SetAlpha(ring.a)` and then called `armPulse`, whose first act is `group:Stop()` —
which restores the alpha the group captured when it last played, clobbering the fresh write;
and the following `Play()` then captured the *clobbered* value as what the next `Stop()` will
restore to. Both halves are wrong and neither shows while every tier pulses, which
`Treatment.Pulse` explicitly does not promise. The write moved **inside** `armPulse`, between
the stop and the play — not after the call, which would leave the restore target stale. One
function owns the channel now, and the ordering has a comment naming why an editor must not
reorder it.

**The phase offset was period-independent, which quietly weakened the safety property.**
`PULSE.phase` was a flat `0.07 s` whatever the tier, so on HIGH — the shortest cycle — the
offsets wrapped and rows came back into alignment around the twelfth of that tier. Since the
whole reason offsets exist is the flash threshold, "mostly staggered" is not the claim being
made. `Treatment.Phase` now returns a **fraction of the row's own cycle**, stepped by the
golden ratio, and the surface multiplies it by the live tier's period (`Pulse.cycle`, the
bounce round trip). Two rows never share a phase and the property no longer depends on how
many rows a spec has. The test that pinned the old behaviour was replaced by two that pin
this one, both mutation-checked.

**Three smaller ones.** The ring size is now re-read every pass, not only when the item frame
object changes — a UI-scale change re-lays the frame without handing cap a different one, and
`sizeRing` is a no-op once the answer is unchanged, so the cost is one guarded read per drawn
row per tick, which is what `itemShown` already spends. `SetJustifyH`/`SetJustifyV` are
**called** rather than inherited. ⚠ **The framing first written here was half wrong and is
corrected in place:** `CENTER` and `MIDDLE` are the XSD **defaults**
(`frames-textures-animation.md` §6.2 — `justifyH` `CENTER`, `justifyV` `MIDDLE`,
`scaleAnimationMode` `FontSize`), so calling them is defence against a template that
overrode them, not the repair of a hole. What actually *was* unbacked is the sentence the
comment used to justify them — that `Vertex` scaling "grows the way justification points",
which appears nowhere in `knowledge/` — and a claim about how the client behaves belongs in
the KB or nowhere, never in a comment (house rule 1). And `P{}` prints the
fallback ring's `t<thickness>` **only when the fallback is live**, because with the flipbook
on screen it describes nothing drawn.

**One documentation fault, and it is the one worth being embarrassed about.** The restyle
entry below quoted a §6 sentence — *"answers the floor with a veil"* — that appears in no
commit. It existed only in the uncommitted working tree at the moment it was edited, so
`git log -S` finds nothing and a reader cannot check it. `notes.md` is the historical record;
a quoted string absent from the history is the one thing it cannot afford. Quote dropped, the
edit described instead.

**Two findings the cull made moot, checked rather than assumed.**

- **Pulse-rate monotonicity** was to be pinned with a loop over `ORDER`. The cull deleted
  *"monotone in pulse rate"* as a normative claim — ⚠ **that phrase, and §3.1's *unequal
  rates plus a per-row offset* below it, are both from the uncommitted tree**; §3.1's
  treatment subsection is in no commit, so neither is quotable from `git` (see the same
  warning on the cull entry). So there is nothing to pin — a test
  asserting it would be re-legislating a rule that was just struck. What survives is
  §3.1's *unequal rates plus a per-row offset*, and the **pairwise-distinct** test already
  pins exactly that. Not added, deliberately.
- **The §6 hedge.** The review said the §6 edit closed more than the evidence supported, and
  it was written when LOW sat at 0.29; the cull put LOW back to 0.43. The direction of the
  worry changes with it — a brighter floor is *less* likely to vanish and *more* likely to
  read as MEDIUM — so §6 now names what the floor is drawn as, says that is a shape for the
  answer rather than the answer, hedges **both** directions, and keeps its original closing
  line. That matches the hedge `backlog.md` and `discussion.md` **D11** already carry.

**What was deliberately not done.** No release, no deploy, no flight, no commit, no
`knowledge/addon-dev/` write. `Treatment.RING.atlas` untouched — D10 settles on a flight.
And **`nosize:` cannot be mutation-checked**: it lives in `Overlay.lua`, which has no harness
by design, so the only thing standing behind it is a reading of the code.

## 2026-08-10 (the §3.1 cull) — three surface rules struck, two narrowed, and LOW gets its measured number back

**Done, static only. `spec.md` §3.1 and §6, `Treatment.lua`, `Overlay.lua`,
`treatment_spec.lua`, `discussion.md` (D10 updated, **D11** opened), `backlog.md`. busted
147 → 145, luacheck 0/0 in 21 files, 2 mutations run and caught. ⚠ Nothing here has run in
the client** — the surface this argues about has still never drawn a pixel.

A targeted cull of §3.1's normative assertions, run between WP2 and its fix pass, with one
test applied to every one of them: **which principle is this downstream of?** The 2026-08-08
(polarity) entry below is why it exists — a cull that *added* a rule, which then acquired
three independent-looking sources inside a week.

### What was struck

⚠ **The struck §3.1 text quoted below is RECONSTRUCTED from an uncommitted working tree, not
quoted from history — `git` cannot show you any of it.** §3.1's whole
`#### What a treatment looks like` subsection has never been committed: it is an all-`+`
block in `git diff`, and `git show HEAD:projects/combat-assist/specs/spec.md` contains none
of *monotone*, *disjoint*, *fixed place*, *proc-glow art*, *brighter of the two*,
*colour-blind*, *greyscale* or *Hue is the accent*. **The one exception is
"A positive cue is not a second visual language"**, which is real and checkable at
`spec.md:165` of `HEAD`. Everything else below existed only in the tree at the moment it was
edited, so the **replacements** can be checked against the file on disk and the **originals**
against nothing. They stay, because the argument is unreadable without them — labelled as
what they are. This is the standard the fix-pass entry above sets (*a quoted string absent
from the history is the one thing `notes.md` cannot afford*) applied to its own predecessor.

- **"The ladder is monotone in brightness … and monotone in pulse rate too. It survives a
  colour-blind read and a small icon. Hue is the accent, not the signal."** Not downstream of
  (a), (b) or (c). It is the same shape as the polarity rule struck two days earlier and with
  the same defence — *survives a colour-blind read and a small icon* — a visual preference
  asserted as a constraint, and one which additionally **names the channel**: it forbids a
  design that carries the ladder in hue, for no reason a principle supplies. **Narrowed, not
  deleted outright** (below).
- **"A marker has a fixed place, and there are two of them."** A description of the built
  renderer promoted to a rule: top-centre count, bottom-centre hold, one slot of each. Not
  downstream of anything, and it forecloses two live questions — `discussion.md` **D8**'s
  single marker that turns from *hold* into *press*, and the three §3.5 channel forms that
  have no marker yet. **What survives is the half that is traceable**: no part of a marker
  carries a backing that outlives it, because a backing that does announces that a cue was
  *offered*, which is cap's half where *appears* is the client's — §3.0's own definition of a
  cue, and (a) in the same breath.
- **"A positive cue is not a second visual language"** (both statements of it). The substance
  — a positive cue is drawn in the treatment of the tier it stands for — is **definitional**
  and is stated in §3.5's cue declaration and enforced by check 4; the slogan is a second,
  broader claim that had already been used to justify a different decision (M3d's refusal to
  invent a LOW hue). That refusal stands on its own: LOW's hue *is* the hold slate, so a
  LOW-styled marker and a hold marker would be one colour. The slogan bought nothing the
  mechanics did not already carry.
- **⚠ "Each tier owns a disjoint brightness band … a fully-graded MEDIUM never reaches the
  dimmest ungraded HIGH."** The one this round was least sure of, and it does not survive.
  §3.0 defines Grade as *continuous emphasis within a tier, never changes the tier* — a claim
  about **computation**, and one that is **true by construction**: the bands settle the tier,
  a grade is computed only afterwards, and it only lerps inside that tier's own range.
  Nothing about two tiers' ranges overlapping can make it false. So §3.1's rendering of it in
  **pixels** is a second, separate claim wearing the first one's argument. Worse, §3.1
  already conceded that the screen does not obey it — the pulse is a second channel and
  HIGH's trough dips under MEDIUM's peak deliberately — so the invariant bound an internal
  number the renderer then violated anyway. Its exemption clause went with it.

### What was narrowed, and what each replacement is downstream of

- **The ladder** → *"The ladder is ordered. HIGH reads as more emphasis than MEDIUM, MEDIUM
  more than LOW, LOW more than* none*."* Downstream of **§3.1's own first sentence** (a tier
  is one of three *emphasis levels* — levels are ordered or they are categories) and of §1's
  **move 2**, which names dim-versus-bright as the grading channel in as many words. It says
  nothing about which channel carries the order.
- **The disjointness bullet** → *"A grade moves an entry only inside its own tier's range."*
  Downstream of **§3.0's Grade**, restated where §3.1 needs it. The midpoint convention rides
  along unchanged; it was never the contested half.
- **The proc-glow rule** → *"cap's emphasis must be distinguishable from the stock proc
  glow."* Downstream of **§1's move 2** — *Blizzard's proc glow says "this is available." cap
  says "this is available, and right now it's worth about this much."* Making those two
  distinguishable **is** the product, so the root is real. What does not follow from it is the
  stronger *"cap does not reuse Blizzard's proc-glow art"*: the same sheet in a different
  colour can satisfy the root and a different sheet in the same gold can violate it. §3.1 now
  states the requirement and says the separation cannot come from the art; whether the shipped
  treatment achieves it is `discussion.md` **D10**, which an eyeball settles. ⚠ **The rule was
  narrowed; the code was not changed.** `Treatment.RING.atlas` is untouched.
- **"The row takes the brighter of the two treatments"** → *"the row is drawn in the higher of
  the two tiers"*, which is what the sentence's own next clause already claimed. See below —
  this one has teeth.

### What survived, tested rather than assumed

Two entries binding one row take one treatment (an icon can only be drawn one way);
*veiled* ≠ *bare* (`none` versus a silence — §3.0); the two registers (a fact about the
client, and the section says so); *tiers describe value, not order* and *cap never ranks
within a tier* (principle (c), near-verbatim). None of these needed touching.

### The one thing the cull broke, and the four lines that fix it

**"Brighter" and "higher tier" were the same sentence only because of disjointness.** With
the invariant gone, a graded LOW can out-brighten a dim MEDIUM — so `Overlay`'s
`Brightness`-ordered pick of which of two entries a shared row draws could, in principle,
draw the **lower** tier. It cannot happen on Demonology (E5/E6 are the only pair sharing a
row and neither has a LOW band), which is exactly what makes it the silent kind. So
`Treatment.Rank` was added and `Overlay` now compares **tier order first, emphasis only
inside one tier**. That is not a new rule: it is the code catching up to the half of the
sentence that was always the meaning.

### LOW returns to 0.50, and this is the argued item

**The disjointness invariant is the rule that moved LOW's ring off the lab's number**, and
it is the entire reason it moved: the slate's luma (0.820) sits near gold's, so a LOW ring at
0.50 reads brighter than a fully-dimmed MEDIUM. With the rule culled there is nothing left
objecting to the measured value, so LOW's band is **`0.36 – 0.50`** — the measured 0.50 read
as the band's *bright* end, which is the same reading applied to MEDIUM in the restyle, and
the band's existing width kept so that exactly one number changes. The ungraded midpoint
moves 0.29 → **0.43**.

The reason to prefer 0.50 is not that it is prettier. **It is the only LOW alpha anybody has
ever looked at**, chosen by a person on a real spell icon at true CDM size; 0.36 was derived
from an arithmetic ceiling (`0.3192 / 0.820 = 0.389`, minus a margin) to satisfy the rule now
struck. Restoring it puts the *measured* number back and moves the *unmeasured* question —
does a bright LOW beside a dim MEDIUM read wrong? — to the flight, as **`discussion.md` D11**,
where it can be answered by looking instead of by arithmetic.

### The count, and which tests went

**busted 147 → 145.** Three deleted, one added, two shortened or relabelled. ⚠ **Three of
the five test names quoted below are checkable and two are not**: *monotone in ring
thickness*, *DIMMEST HIGH* and *disjoint from the next one down* are all in commit
`f711956` (`git log -S` finds each); *"tracks the grade, so the pulse never lifts an entry
out of its band"* is in **no** commit — it was created by the uncommitted restyle, so like
the §3.1 quotes above it is a reconstruction. *"ranks the tiers with none lowest"* is new
and readable in the working tree.

- deleted **"is monotone in ring thickness too, so the ladder survives in greyscale"** — the
  greyscale defence is culled, and the shipped ring is one flipbook shape so thickness is
  fallback-only geometry that separates nothing a player sees;
- deleted **"keeps a fully-graded MEDIUM below the DIMMEST HIGH, graded or not"** and
  **"gives every tier a band disjoint from the next one down"** — both assert the culled
  invariant. ⚠ **This bullet first claimed both still passed; that is false, and the
  correction is in place rather than under it.** Run against the bands as they stand, the
  first **passed** (a fully graded MEDIUM reads `0.518622`, the dimmest HIGH `0.746441`) and
  the second was **RED** (LOW's bright end reads `0.410040`, MEDIUM's dim end `0.319152`, so
  LOW reached into MEDIUM). The paragraph forty lines below — *"a LOW ring at 0.50 reads
  brighter than a fully-dimmed MEDIUM"* — had the arithmetic right, so the entry
  contradicted itself. **Both were deleted because the rule they assert is gone, not to make
  the suite green**, which is why one of them being red changes the record and not the
  decision;
- **"tracks the grade, so the pulse never lifts an entry out of its band"** lost its
  disjointness half and kept the half about the grade;
- added **"ranks the tiers with *none* lowest"**, for `Treatment.Rank`.

Both new mutations are caught: raising LOW's band until it passes MEDIUM breaks the ordered
ladder, and inverting `RANK` breaks the shared-row pick.

### What was deliberately not done

- **No release, no deploy, no flight, no commit.** This round ends at the desk.
- **No `knowledge/addon-dev/` write.** Nothing here is a fact about the client.
- **Nothing was added to §3.1.** Every edit removes a claim or replaces one with a strictly
  weaker claim, and each replacement names its principle above — which is the thing the
  2026-08-08 (polarity) entry says a cull owes.
- **§3.0's glossary and §3.5's five checks untouched**, out of scope by instruction; and
  **`Treatment.RING.atlas` untouched**, because D10 is about pixels and this round had none.

## 2026-08-10 (the measured restyle) — the lab's numbers meet the ladder, and one of them loses

**Done, static only. `Treatment.lua` (+60 lines), `Overlay.lua` (+125), `treatment_spec.lua`
(+49), one comment line in `.luacheckrc`; `spec.md` §3.1 and §6 amended, `backlog.md`
struck and re-filed. busted 141 → 147, luacheck 0/0 in 21 files, 12 mutations run and
caught. ⚠ Nothing here has run in the client** — no ring has been drawn, no pulse has
played, and `ring:`/`mark:` have never printed a value. The reading a flight should take is
in `backlog.md` → `## Reference` → *The measured restyle*.

**What arrived.** A ClientLab picker put candidate treatments on real spell icons at true
CDM size and a person chose: the ring is Blizzard's own `UI-HUD-ActionBar-Proc-Loop-Flipbook`
played as a flipbook, `ADD`, at 1.4× the icon; all three tiers wear it; they are separated
by hue, alpha and a **pulse rate** (2.5 / 1.2 / 0.5 Hz); *none* keeps the only veil. LOW
loses its veil and gains a ring, which is the substantive change — the LOW → none step
becomes *the presence of a ring* rather than two veil depths to compare.

**The one measured number that did not survive, and why it is LOW's.** `Brightness` is
`alpha × luma(hue)`, and the slate's luma is **0.820** — near gold's 0.909 and far above
blue's 0.665. So LOW at the measured **0.50** reads **0.410**, while MEDIUM's floor reads
**0.319** (0.48 × 0.665): LOW out-brightens a dim MEDIUM and the disjoint-band invariant
breaks. The test caught it, which is the whole reason it exists.

It was resolved by moving numbers, never by relaxing the test, and the number that moved is
LOW's: **`0.22 – 0.36`**. Three reasons, in order of weight.

- **The lab compared LOW's ring against *none*, never against a dim MEDIUM.** The 0.50 is
  evidence that a slate ring reads as *present*; it is no evidence at all about where it
  sits relative to a graded MEDIUM. It is the weakest claim on the table.
- **Narrowing MEDIUM instead would cost a feature that is not built yet.** MEDIUM's band is
  what §3.2's Demonbolt demotion rides — *a fade, not a flip*. Raising MEDIUM's floor to
  0.62 to make room for a LOW at 0.50 would halve that fade's range to buy back an alpha
  nobody has judged on screen.
- **The ceiling is arithmetic, not taste.** `0.3192 / 0.820 = 0.389` is the highest slate
  alpha that stays disjoint at all; 0.36 is that with a margin. LOW's width is MEDIUM's
  *proportional* width (0.385 of the bright end), because LOW's old 0.22 band width was in
  the veil channel and does not transfer to ring alpha.

⚠ **This is filed as open, not settled** (`backlog.md` → *The measured treatment*): 0.36 has
been seen by nobody. If LOW is unreadable in play the fix is a lower MEDIUM ceiling or a
narrower MEDIUM band — never a LOW that reaches into it.

**MEDIUM moved too, and that one is mechanical.** The lab measured each tier at full
strength, so the measured value is the band's **bright** end, not its midpoint. MEDIUM's
bright drops `0.86 → 0.78` and the existing width is kept, giving `0.48 – 0.78`. HIGH was
already exactly `0.82 – 1.00` and needed nothing — a band whose midpoint is 1.00 is not
representable, which is why "bright end" is the only reading that works.

**The pulse and the tier alpha are one channel, and that shapes the code.** An `Alpha`
animation drives the same channel `SetAlpha` writes, so rather than wrap the ring in a
second frame the tier's alpha is **baked into the animation endpoints** — `from` is 0.68 of
it, `to` is it. The consequence is that the pulse must be **re-armed whenever the tier or
grade moves**, which is exactly when the paint path runs, so it rides the existing
`f.painted ~= key` dedup and costs nothing extra. The paint path also writes the alpha
itself rather than trusting a stopped group to have restored it.

The ring got its **own host frame** for the same reason: the pulse is a frame alpha, and a
frame alpha multiplies its children — on the overlay frame itself it would have pulsed the
veil, the hold marker and the count along with the ring. The host sits one frame level
*below* the overlay so both markers draw over the ring; a ring and a veil never coexist, so
nothing is lost by the veil being above it too.

**`spec.md` §3.1 owed two amendments and both landed with the code.** The disjointness
invariant now binds **the band** — what `Treatment.Tier()` returns — and not the
instantaneous rendered alpha under an animation: HIGH's trough (0.68 × its alpha) dips under
MEDIUM's peak deliberately, because **rate** separates those two and holding disjointness
through the pulse would need a trough too shallow to read. And *none* is now stated as a
state with its own treatment, with the LOW → none step being the ring. The table was
re-transcribed, the "monotone in ring thickness" clause became **monotone in pulse rate**
(the ring is one shape now, so thickness no longer separates anything a player sees), and
§6's *how much does a demoted ability show?* was edited to name what the floor is now drawn
as. ⚠ That §6 edit over-closed the question and was hedged back in the fix pass above; the
edit it replaced was itself uncommitted, so `git log` cannot show you either side of it.

**`Treatment.Ink` still refuses LOW, and it now has to say so out loud.** LOW's hue *is* the
hold slate, so a LOW-styled marker and a hold marker would be one colour — the second visual
language §3.1 exists to forbid. Before this round the refusal was free, because LOW had no
ring to take a colour from; now it is an explicit `ink = false` on the tier, and a test
pins both halves (the hue really is HOLD's, and `Ink` really returns nil).

**H4 resolved at the desk, and better than expected.** The FlipBook Lua setter names were
recorded as established nowhere. They are in fact **Tier 1** — `SetFlipBookRows` /
`SetFlipBookColumns` / `SetFlipBookFrames` (+ `FrameWidth`/`FrameHeight`), all
`SecretArguments = "AllowedWhenUntainted"`, in the generated docs' own
`SimpleAnimFlipBookAPIDocumentation.lua`. Blizzard's `ActionButtonSpellAlerts.xml:25`
declares `flipBookFrameWidth="0" flipBookFrameHeight="0"`, i.e. the XSD defaults, so cap
sets only the three. **The probe was built anyway**: the three names are still probed by
name, a miss falls back to the four-quad ring and reports which method was absent on
`ring:`, and that path carries the round's one `--@unverified`. An XML attribute name is not
a Lua setter name and getting it wrong is silent — the probe is what makes it loud.

**One rule collided with the pick, and this round did not settle it.** §3.1's last surface
rule read *"cap does not reuse Blizzard's proc-glow art"* — and the ring a person picked in
the lab **is** Blizzard's proc-loop sheet. Leaving the rule standing would have left
`spec.md` asserting something the code contradicts, so it was rewritten to say what actually
separates the two (the §3.2 suppression, the tier hue and alpha, the pulse) — but that
rewrite is a transcription made at a desk against no pixels, so the argument is held open as
`discussion.md` **D10** and resolves on the first flight, at a Demonic Core proc. If they
read as one thing, the fix is one string: `Treatment.RING.atlas`, with
`glow-palette.md`'s candidate run already carrying the alternatives and their grids.

**What was deliberately not done.**

- **No release, no deploy, no flight.** This round ends at the desk.
- **No `knowledge/addon-dev/` write.** The FlipBook setter names belong in
  `frames-textures-animation.md` §7.1's setter table and are parked in
  `_meta/kb-inbox.md` instead — they are a documentation read, not a measurement, and this
  round had no mandate to edit that KB.
- **`Brightness` was not redefined to weight ring thickness.** It would have made the H1
  conflict disappear arithmetically, and it would have been changing the metric to pass the
  test — and it would describe the *fallback* geometry, not the shipped one.
- **The `--@unverified`-for-everything decision stays open.** One marker now exists and its
  claim is narrower than that decision; the backlog line says so rather than letting the
  marker imply the rest of the surface is verified.

## 2026-08-10 (the proc glow) — cap stops competing with a gold overlay it cannot outshine

**Done, static only. `Glow.lua` (57 lines), a 2-line touch to `Sense.lua`, one `draw` field
in `Overlay.lua`, one `.toc` line. busted 141/141 unchanged, luacheck 0/0 in 21 files.
⚠ Nothing here has run in the client** — not one frame has been hooked, not one alpha
written. The work list and the `glow:` reading are in `backlog.md` → `## Reference` →
*The proc-glow suppression*.

**What it is.** A per-instance post-hook on each CDM item frame's `RefreshOverlayGlow` that
sets `item.SpellActivationAlert:SetAlpha(0.5)`. That is the whole mechanism. It closes the
*replaces the stock proc treatment rather than adding to it* half of `spec.md` §3.2; the
Demonbolt demotion — the other half, and the one that needs a catalog rule — is untouched
and stays on M3e.

**Four decisions, and three of them are constraints rather than choices.**

- **The alpha goes on the alert FRAME, never on its child textures.** The proc animation
  drives the children's alpha, so a write there is in a fight it loses every frame; the
  frame's alpha multiplies the whole thing and is not animated.
- **Per-instance hook, not on the shared mixin table.** The methods are `Mixin()`-copied per
  frame, so a hook on the table misses every frame that already exists — which, at the point
  cap binds, is all of them.
- **A dim, not a hide.** Hiding is protected and blocked in combat.
- **It rides `Sense`'s existing frame walk** rather than opening its own. That was a choice,
  and the reason is that `Sense.lua:185` already enumerates exactly these rows and already
  owns the weak-keyed hook-once-per-frame-object-ever table this needs; a second walk would
  have been a second copy of a rule (`hooksecurefunc` can never be removed, and item frames
  are pooled) that is expensive to learn twice.

**`Glow.Restore()` and why cap owes it.** When cap goes dark — no catalog for the build, or
unsettled at combat entry — it puts every hooked frame's alert back to full alpha. cap
degrading Blizzard's UI while providing nothing in its place is strictly worse than cap not
being installed. The hooks cannot be uninstalled, so a liveness flag is what makes the
callback inert, and `Glow` learns the transition from `Sense.OnVerdicts` like every other
surface — one clock, and no second set of combat events.

⚠ **`Restore` shipped without a liveness guard and review caught it.** `light()` had the
early-out; `Restore` did not — so while cap was dark it wrote `SetAlpha(1)` onto every hooked
alert frame **ten times a second, indefinitely**, because `OnVerdicts` fires from the 10 Hz
tick on the early-return path too. Two things that costs: it contradicts `spec.md` §3.5's
*no catalog, nothing at all* — "cap draws nothing, **alters no CDM pixel**" — and that
section's check that cap is *completely inert* on a spec with no catalog, worst
in the dark-for-the-fight case where cap sits dark for a whole pull with frames already
armed; and it stomps any other addon's proc-glow suppression continuously, **precisely while
cap is doing nothing**. The lesson is narrow and worth having: an idempotent write is not a
free one when the surface is shared and the clock is 10 Hz. Guard added; it can skip nothing,
because `Arm` only dims while `live`.

⚠ **The `.toc` order is load-bearing and nothing tests it.** `Glow.lua` sits *before*
`Overlay.lua` so its verdict listener registers first; otherwise the `glow:` token on a dark
pass reports the liveness of the pass before it. One line of comment sits on it.

**What `glow:` can and cannot say.** `<frames>/live` or `<frames>/off`. It separates "cap
never found a frame to hook" from "the frames are hooked and cap is deliberately dark" —
which is worth the token, because without it a flight cannot tell *dimmed* from *never ran*.
It does **not** say the glow got dimmer and it never can: `SetAlpha` hands nothing back. Same
ceiling as `C{}`'s `armed`, for the same reason.

⚠ **Three of the four "why" claims in the file header were bald assertions with no anchor,
and one was wrong.** That the proc animation drives the *children's* alpha, that hiding is
protected and blocked in combat, and that the mixin methods are `Mixin()`-copied per frame
are all **absent from `knowledge/addon-dev/`** — they are read off CDMProbe's source, not
measured. Worse, *"`RefreshOverlayGlow` fires only on a CHANGE"* is **softened by the KB**:
`cooldown-manager.md` lists the overlay glow inside `RefreshData()`'s full re-resolve chain,
so it is also called on any re-resolve. The decisions are unchanged and still right; the
comments now **name the provenance** instead of asserting the facts, and the immediate-pass
comment no longer claims a firing rule §6 does not state. This is the shape of the trap the
KB-write ban creates: forbidden from filing the claim, the natural move is to assert it in a
comment instead, where nothing lints it.

⚠ **House rule 1's comment ratio was missed, and the defence for it used a wrong number.**
The first cut landed at 0.66 and the trim at 0.51, and the round reported that as a modest
outlier against "cap's other files run 0.26–0.33". That comparison was wrong — `Tier.lua` is
**0.401** and `Catalog.lua` **0.363**, so two shipped files already exceed the 0.35 ratchet
and `Glow.lua` was the worst in the addon by a wide margin. Cutting the prose that restated
the unanchored facts above fixed both defects at once and landed it at **0.333**. What
survives is the two blocks rule 1(a) actually earns: the `.toc` ordering invariant, and
`Restore`'s early-out.

**Two findings declined on purpose, and filed rather than fixed.**

- **No `--@unverified` on `Glow.lua`,** though house rule 5 asks for one. `Overlay.lua`,
  `Channel.lua` and `Treatment.lua` have equally never executed in the client and carry
  none — marking Glow alone would imply the other three are verified, which is the opposite
  of true. It is a **project-wide** decision and it is filed in `backlog.md` as one.
- **Tab-2 rows get armed** even though `cooldown-manager.md` §6 says only tab-1 viewers ever
  hear the glow event. A tab-2 frame is either skipped for want of the method or hooked
  inertly, so the only cost is an inflated `glow:` count — and a tab-1 filter would copy
  viewer knowledge into `Glow` that `Bind` owns. Noted in the `## Reference` block instead.

**Deferred, deliberately.** No `spec.md` edit — §3.2 already says cap *replaces* the stock
proc treatment and §3.1's third surface rule already says why; this implements text that was
already normative rather than changing what cap should do. No tests: `Glow.lua` is hooks and
frames end to end, with no pure seam worth extracting, and inventing a harness for it would
mean asserting against a fake of an API nobody here has called (house rule 6). No command,
because nothing about it is a thing to ask for. And no release — this project has no standing
auto-deploy exception.

⚠ **One thing is owed and it is owed to the KB, not to cap.** The dim recipe — alert frame
not child textures, per-instance not shared-table — currently exists **only in CDMProbe's
source**, which the 2026-08-06 entry already flagged as exactly the failure house rule 1
exists to prevent. It goes to `knowledge/addon-dev/cooldown-manager.md` §6 as a
`[client YYYY-MM-DD]` claim **after** it has run here, and not before: written now it would
be a claim sourced from another addon's code rather than from a measurement, which is a
worse defect than the gap it fills. Filed in `backlog.md` as blocked on the flight.

## 2026-08-08 (polarity) — a rule the cull ADDED, struck; and the lesson is about culls

**"Polarity is carried by shape — *press* and *hold* may never differ only in hue" is gone**
from `spec.md` §3.1 (both statements of it), from `backlog.md`'s channel-coverage note, and
from `Treatment.lua` and `Overlay.lua`'s comments. One `busted` describe label named it and
was renamed; no test asserted it. Nothing replaced it. 141 tests, luacheck 0/0.

**Where it came from, which is the part worth keeping.** `git log -S` puts it in commit
`e7b8b1c` — **the rule cull**. The pass whose entire purpose was cutting rules back to §1's
three principles *introduced* one. M3c then implemented it, wrote it into §3.1's new
treatment table as one of the four properties holding that table together, and restated it in
two module headers — so by the time anyone looked, an unargued assertion had three
independent-looking sources and read as settled.

**Why it does not survive scrutiny.** It is not downstream of (a), (b) or (c). It is a visual
preference, and a defensible one — shape survives a colour-blind read and a small icon — but
a preference asserted as a constraint. What it cost was concrete: it forbids a single marker
whose visibility and colour both ride the same duration, turning from *hold* into *press* as
a burst window arrives. That is simpler than the two-marker alternative the rule forces, and
it fixes `catalog.md` O8 by saying something useful in the stretch where the current hold
marker is merely wrong.

⚠ **The lesson is not "that rule was bad", it is that a cull can add.** A pass that removes
nine rules and adds one reads — in its own commit message and its own session log — as a pure
simplification, and the added rule inherits the credibility of the cleanup around it.
Anything a cull *introduces* deserves the same "which principle is this downstream of?" test
the cull applies to what it removes, and the answer belongs in the commit.

Now open again: `discussion.md` **D8**, how polarity is drawn. §6's original question was
struck when M3c answered it; removing the answer reopens it rather than leaving the design
unstated.

## 2026-08-08 (M3d) — the cues, and the half cap is not allowed to compute

**Done, static only. busted 138 → 141, luacheck 0/0 in 20 files, nothing flown, no release
cut.** The work list and the `C{}` reading: `backlog.md` → `## Reference` → *M3d*. What it
made normative is in `spec.md` §3.1 (*What a treatment looks like*, the marker-placement
bullet) and §6 (half of the cue budget, answered by construction). This entry is the *why*,
and the last section is the one that matters most.

### What arrived

`Channel.lua` — new, impure, and the only place either sealed mechanism lives. Two
functions, one guard doctrine, and both mechanisms are the KB's rather than ours:
`GetAuraApplicationDisplayCount`'s three-way quantiser and a `Step` curve evaluated by a
duration object. `Treatment.Ink` (the one field the renderer lacked), `Overlay`'s two
marker slots, and `C{}` on the `draw` stream.

### Four decisions

**1. The threshold's "on" value comes out of the curve, not out of Lua arithmetic.** The
hold glyph should sit at `HOLD.alpha = 0.95` when the client says *now*, which is a
multiplication — and arithmetic on a secret is refused outright. So `Channel.Threshold`
takes the on-value as a parameter and the curve is built `(0, on) … (t, 0)`: the client
returns 0.95 or 0 and Lua does nothing to it. The `0` end is *not* a parameter, deliberately
— "the marker is invisible outside the window" is structural, not a caller's choice.

**2. The count mark carries no plate, and that is a leak, not a style choice.** Below the
threshold the quantiser returns an empty string, which renders nothing — the *absence of
the text is the cue*. A dark plate behind it would still be drawn, so an icon would grow a
permanent box for as long as the cue was offered, and the box would be cap announcing that
it *offered* a cue. That is precisely the half the player is not supposed to be told. An
outlined font replaces it. The hold glyph keeps its plate because every part of it takes
the same secret alpha, so the plate vanishes with the bars.

**3. A positive cue whose tier is drawn as a veil is refused, not improvised.** `LOW` and
*none* put no light on the icon, so `Treatment.Ink` returns nil for them and the marker is
not drawn. The alternative was inventing a hue for LOW, which would have made a marker
readable in a colour no tier owns — a second visual language, which `spec.md` §3.1 exists
to forbid. Check 4 permits a positive LOW cue and nothing in the catalog authors one; if
one ever is, it reads `refused` in `C{}` rather than appearing in a made-up colour.

**4. The tie-break is a read-side rule and stays out of `spec.md`.** One aura can be
tracked on two viewers at once, so "the row carrying this aura" needs a deterministic
answer or it flip-flops between logins. Lowest cooldownID wins **among the `auras` rows**:
§4.8.2's precondition is a live bound aura, and only an aura row carries one. Check 3's
aura set contains every entry's own spell id, so `stacks(<a castable ability>) ≥ n` passes
the load checks — and where that ability is also a press, its `spells` row can hold the
lower cooldownID and answer nothing, pinning the cue at `refused` for the whole build.
None of this is a product rule, because it cannot reach a pixel: the *draw* is on the
entry that owns the cue — E7's on Demonbolt, E8's on Implosion — which is what the player
is being told to press, and which sidesteps the ambiguity for everything the player can
see.

### What a flight can and cannot verify, which is the whole point

**Neither channel has a readback, by construction.** `SetText` and `SetAlpha` both accept
a secret and neither hands one back; `GetEffectiveAlpha` on a secret alpha *throws*, so
there is not even a dishonest way to ask. So:

- **A log can prove the mechanism is wired.** `arm: = cue:` means cap resolved a live
  `auraInstanceID` / obtained a duration, built a curve, and handed the comparison over.
  `arm:` short of `cue:` with `C{}` naming the refusal means cap never reached the client,
  and `C{}` says which of the four ways.
- **A log can never prove a marker appeared.** cap offered; the client decided; nothing
  reports back. `wowkb.capture cap draw` showing `E8:+stacks:armed` for a whole pull is
  fully consistent with a screen on which no number ever appeared — because that is also
  what "the imps never crossed six" looks like from cap's side.
- **So the eyeball is not a nicety here, it is the only oracle**, and it has two jobs the
  log cannot do: (a) does the number appear when the imps cross six and vanish when they
  fall below, and (b) does the hold glyph appear only in the last stretch before a Tyrant
  window. Both are *threshold* questions, and a threshold that fires at the wrong moment
  reads exactly like one that fires correctly in every instrument cap owns.

⚠ **And one thing a flight must not conclude.** E8's cue flapping `armed` ↔ `refused` is
the Wild Imp row binding and unbinding its aura, which is imps arriving and expiring — the
PASS case, not an instability. The failure that looks similar is `refused` for a whole pull
with imps visibly out, which would mean the row lookup or the tie-break is wrong.

⚠ **Out of combat the quantiser returns a PLAIN string**, so a desk check in a city reads
the count as ordinary text and proves nothing about the sealed path. Only mid-pull is the
quantiser doing any work at all.

### The cue budget, left open on purpose

`spec.md` §6 asked for it to be decided against a drawn catalog. Half of it is now answered
by construction — an icon has one count slot and one hold slot, so **two** is the physical
budget and a third is not drawn — but the interesting half is not. Demonology authors at
most one cue per entry, so no icon has ever carried two; and the alternative surface the
question turns on, §3.4's bars, does not exist. Deciding "cross-ability cues live on the
bars" against a surface nobody has built would be authoring in advance against no evidence,
which is the thing the drawing rungs were reordered to stop. Left open, with the drawn
geometry recorded in the bullet so the next reader has evidence rather than a memory.

## 2026-08-08 (M3c) — the graded register: cap's own frames, and the numbers on them

**Done, static only. busted 113 → 138, luacheck 0/0 in 19 files, nothing flown, no release
cut.** The work list and what a flight has to read: `backlog.md` → `## Reference` → *M3c*.
The vocabulary it settled is normative in `spec.md` §3.1 → *What a treatment looks like*.
This entry is the *why*.

### What arrived

`Treatment.lua` (pure — tier → look, and the only place the numbers exist), `Overlay.lua`
(impure — frames, anchoring, paint), `Sense.OnVerdicts` (the listener registry plus the
call at the end of `evaluate()`), a third capture stream `draw`, and 25 tests. `spec.md`
§6's *"How is polarity drawn?"* is struck, because this rung answers it.

### Why the numbers are what they are

The plan fixed the *structure* — a monotone brightness ladder, hue as accent, shape
carrying polarity — and left the values. Four decisions produced them.

**1. Brightness is one number, so the ladder can be tested.** `Treatment.Brightness` is
`ring alpha × Rec.709 luma` for a ring, and `−veil` for a veil. That single scalar is what
"monotone" is asserted against; without it "the ladder is monotone" is prose. Reading
across HIGH → MEDIUM → LOW → none it goes `0.83 · 0.47 · −0.31 · −0.62`.

**2. Each tier owns a DISJOINT band, and the grade moves inside it.** HIGH alpha
`0.82–1.00`, MEDIUM `0.56–0.86`. Against their hues (luma `0.910` and `0.665`) that is a
brightness band of `0.746–0.910` against `0.372–0.572` — a fully-graded MEDIUM lands `0.17`
below the *dimmest* HIGH. The test pins that bound rather than the trivial "ungraded
MEDIUM < ungraded HIGH", because the overlapping-band bug is silent: every individual
treatment still looks right and only the ladder is wrong.

**3. Ungraded is the MIDPOINT of a band, not its top.** The alternative — ungraded = the
tier's brightest — makes every ungraded entry outshine every graded one at the same tier,
which reads as "no grade means maximum urgency". Midpoint says the honest thing: an entry
with no grade is neither the most nor the least urgent thing its tier can be. Six of
Demonology's ten entries are ungraded, so this choice is most of what is on screen.

**4. LOW's grade moves the veil, not a ring.** LOW has no ring, so a graded LOW (E7
Demonbolt, `shards` inverted — the demotion the whole §3.2 feature exists for) had nowhere
to go. Its veil bands `0.42–0.20`: dimmest-LOW is still lighter than *none*'s `0.62`, so
the ladder stays monotone and §6's *"a demoted ability must not become invisible"* is
answered by construction rather than by taste.

Hue: warm gold `1.00 0.92 0.55` against cool blue `0.45 0.70 0.95`. Gold/blue is the safe
pair, but the point is that **it does not matter** — the brightness and thickness ladders
carry the signal on their own, and the hue is what makes the two rings pleasant to tell
apart at speed. ⚠ Deliberately **not** Blizzard's proc-glow art: §3.2 replaces the stock
treatment, and a ring that looks like the stock glow makes the two indistinguishable.

### Why its own frames, and why it is legal

`SPELL_UPDATE_USABLE` rewrites a tab-1 icon's colour and *"fires constantly in a city"*
(`knowledge/addon-dev/cooldown-manager.md` §5), so anything cap writes onto Blizzard's
texture is stomped within a frame or two. So: cap's own frames, **parented to `UIParent`
and only ever anchored to the item frame** — measured, an addon frame parented to
`UIParent` reads `IsProtected() == false` and re-anchoring it to a protected frame does not
change that, with `SetPoint`/`Show`/`Hide` working in combat
(`security-taint-and-restricted-data.md` §1.1, `[client 2026-08-06]`).

**The paint path writes only `Show`/`Hide`/`SetVertexColor`/`SetAlpha`, and that is a
design constraint rather than an accident.** Those are the measured-safe combat calls.
Everything geometric happens at frame construction — including the *ring thickness*, which
is why there is one ring built per distinct thickness in the treatment table and the paint
shows one and hides the other, rather than resizing a single ring. `SetFrameStrata` is
protected and has **not** been measured in combat, so the layer is applied out of combat
only and an overlay first created mid-pull draws at `UIParent`'s default until the pull
ends. That hole is now marked in the KB (`security-taint-and-restricted-data.md` §1.1).

`SetColorTexture` is fed literals and only literals — it **poisons the anchor chain** on a
secret (§4.8.1 finding 12), and it is the one call in this file that would.

### Two decisions the code forced, which the spec now carries

- **Two entries can bind one row** (E5/E6 are both spell `105174`), and an icon can only be
  drawn one way. The row takes the **brighter** treatment. That is one icon carrying the
  higher of two tiers, not a ranking within one — but it is a new normative statement, so
  it is written into `spec.md` §3.1 rather than left in `Overlay.lua`.
- **A veiled row and a bare row mean different things.** An entry that matched no band gets
  the *none* veil; a **silence** gets no overlay at all. "cap has no opinion right now" and
  "cap has no opinion ever" are different claims and now look different.

### What is deliberately NOT drawn

**No cue of either polarity.** The hold treatment is defined in `Treatment.lua` and tested
there — it is part of the vocabulary this rung settles — and `Overlay.lua` paints none of
it. A cue is a two-part statement: cap decides whether it is *offered*, the **client**
decides whether it *appears*. Painting the glyph from the offer alone inverts that: E2's
hold would light for the whole ~48 s Tyrant is on cooldown instead of the last 20, which is
worse than no marker and would poison the only oracle this rung has. The `draw` stream
therefore reports **no cue field at all** — a log naming an offer would read as a pixel
that is not there. M3d builds the client half.

### The instrument, and why it exists

*"On any aspect-less channel, the only oracle is an eyeball"* — true of the pixel, but
**"did the paint path run, and did it find a frame to anchor to"** is exactly what a log
can answer, and without it a flight that sees nothing cannot tell a treatment bug from an
anchoring bug. Hence `wowkb.capture cap draw`: `D{n: rows: anch: conf: off:}` plus a
per-entry `P{}` cell, one deduped line per change of the drawn set. The reader registers
*addons*, not streams, and `cap` is already in its map, so no Python changed.

### Reported, not fixed

**E1's and E2's `grade = cooldownRemaining(this)` cannot fire, and `catalog.md` claims it
does.** `Tier.Evaluate` computes a grade only when a band held; both entries' bands require
`ready(this)`, so the grade only ever resolves when the cooldown is at zero — every moment
it would say something, there is no tier and no grade. `catalog.md`'s *"the icon warms as
the window approaches"* describes something the current model cannot produce. Not M3c's to
settle: it is either a §3.4 bars question or a spec question about whether a grade may
exist without a tier. Written up cold as **`discussion.md` D7**, with the case both ways
and a lean toward the bars.

**One thing a flight will want and cannot get.** There is no readback for the pixel. The
`draw` stream can prove the paint ran on a confirmed frame and still not prove anything
appeared, so *"anch: == rows:, conf: == rows:, screen blank"* is a real and expected
reading, and it means **treatment**, not anchoring. That row is in the acceptance table for
exactly that reason.

## 2026-08-08 (migration) — the window migration: the code caught up to the spec

**Done, static only. busted 92 → 113, luacheck 0/0, nothing flown, no release cut.** The
work list and what each decision was: `backlog.md` → `## Reference` → *The window
migration*. This entry is the *why*.

### What moved

`spec.md` deleted windows on 2026-08-07 and the code kept speaking them for a day. Gone
now: `Catalog.WINDOW_TERMS`, `MAX_WINDOWS`, the `window` gate, the `remaining` term,
`Track`'s `windowHolds` / `evalWindowTerm` / `SeedCooldown` / `cd` field / `health.windows`,
and `catalog.md` §2 in full (the document renumbered; O-numbers left alone). Arrived:
subjects on every gate term, negation in a band, `combat` promoted into the gate set,
`e.cues` as a **list** with polarity and a channel term, and check 3 (declared subjects),
which is genuinely new work rather than a rename.

### The four shape decisions, and why they went that way

**1. `dogs_out` became a band, not a cue.** E1's band 1 is `ready(this) and not ready(E2)`.
The reason to prefer it over a cue off cid 760 is that the cue was never available: 13
in-combat samples had `auraDataUnit` nil, because a summon binds no aura at all. What makes
the band honest is that it reads **long** where the old window read short — Dreadstalkers'
cooldown is 20 s against a ~12 s pet lifetime — and the negative cue at
`cooldownRemaining(E2) ≤ 8` trims exactly that tail: `cooldownRemaining(E2) ≤ 8` ⟺ the
pets have expired, arithmetic the client does. So the pair replaces one estimate with two exact
reads, which is the whole point of the migration and not a side effect of it.

**2. E2 keeps one HIGH band and the hold became a cue.** The backlog was emphatic that
converting the HIGH bands into cues would cost E2 and E3 their HIGH outright for no gain,
and that is right: a *negative* cue declares no tier. So bands 1 and 2 (setup / far)
collapse into `ready(this) and affordable(this)` → HIGH, and old band 3's MEDIUM — which
was the hold — becomes a negative cue. `spec.md` §3.4 says this in as many words: a ready
cooldown you should pool *is* ready, so the bar keeps its tier and the cue says wait.

⚠ **`not ready(E1)` in that cue's precondition is the non-obvious half.** A ready Tyrant
has a zero-remaining cooldown, which clears any `≤ t` threshold — so without it the hold
marker would be pinned on through the entire setup, which is precisely the stretch where
Dreadstalkers should be pressed. The precondition and the channel are load-bearing
together.

⚠ **`t = 20` is imprecise and is filed as `catalog.md` O8 rather than glossed.** The
rotation's real hold zone is `12 < cooldownRemaining(E1) < 20`: below 12 s the dogs pressed now are
still out when Tyrant lands and get extended, so pressing is right and the marker is wrong
there. `spec.md` §3.5's channel table offers a single upper threshold and cannot express a
band. The candidate fix is real and measured — a multi-point `Step` curve thresholds a
secret duration into a band entirely C-side
(`knowledge/addon-dev/security-taint-and-restricted-data.md` §4.8.1 finding 4) — but it
would be a new channel form and therefore a spec change, which this pass deliberately did
not make.

**3. E5's `tyrant_active` band is deleted and applies-to is NOT narrowed.** The backlog
offered both: add the apex talent to applies-to and delete band 2, or keep band 2 for the
un-apexed build. Neither, in fact — **narrowing applies-to makes cap draw nothing at all**
on a build without the talent (`spec.md` §3.5, "no catalog, nothing at all"), which is a far
worse failure than one entry losing one band. Band 2 could not be kept either: it rested on
`elapsed(E1)`, which is now illegal on another entry, over a fixed duration `catalog.md`
itself rated low confidence. So it goes, and on an un-apexed build band 1 simply never holds
and E5 degrades to shards/affordable, which is correct.

**4. E9's band 1 is `ready(this) and not proc(E7)`.** Verbatim from the backlog, and the
argument for it is that the alternative — inverting into a positive cue on E7 — says
nothing: both of E7's bands already require `proc(this)`, so there is no band left for the
inverse to decorate, and E9 would collapse to an unconditional LOW.

### What the migration cost

**One band, and it is named.** E5 has no way to say "spend the Tyrant window on Hand of
Gul'dan": nothing in the tracked set carries the Tyrant buff, so there is neither an
`auraUp` gate nor an `auraRemaining` channel for it. `catalog.md` O1 is rewritten to say
that, and to say that the route back is **enabling cid `84224`** (the `HideByDefault`
Tyrant bar, already a backlog item) — a read, not a re-derived fixed duration. Writing the
estimate back in would undo the thing this pass was for.

Struck as moot: O2, which worried that cooldown reduction would silently break cap's
count-down from a declared base cooldown. cap no longer counts anything down.

### Two things fixed on the way, neither of them a window

- **`Catalog.Resolve`'s `alt` defect.** `match()` keyed on `e.spell` alone, so E3 bound Imp
  Lord and not Fel Ravager and dropped silently on half of all builds, losing a real HIGH.
  It now tries `alt` after `spell`. Filed as an M3b leftover; it is a correctness bug in
  the same function the migration was already editing, so it rode along.
- **`Catalog.Reads` keys `byEntry` by SUBJECT, not by the entry that named it.** This is
  forced by subjects being legal in bands and is easy to miss: `not ready(E2)` inside E1's
  band is a read of *E2*. Keyed the old way, `Track`'s gate-health tally reports E2 as
  never-asked and E1 as blind twice over — a working catalog reading blind, which is the
  exact failure that measurement exists to detect.

### Decisions inside the pass that were mine rather than the plan's

- **A cue's channel is a term list**, the same literal shape as a band term:
  `{"cooldownRemaining", "E2", "<=", 8}`, `{"stacks", 296553, ">=", 6}`. One grammar for
  both columns, so the checker walks them the same way and an author has one thing to learn.
  `Catalog.CHANNELS` names, per channel, which of the two forms exist — bare, thresholded,
  or both — because §3.5 says they answer different questions and are not each other's
  fallback.
- **Check 5 is a second return value from `Catalog.Check`**, not a finding in the list. It
  cannot fail, and a finding that cannot fail sitting in the failure list is how it
  eventually gets treated as one.
- **Check 3 polices the FORM of a subject per term, not merely its membership.** Each term
  takes one kind of subject and only that kind can ever be answered: `ready` / `affordable`
  / `proc` / `identity` / `elapsed` and the `cooldownRemaining` / `active` channels name an
  **entry** — `this` or an entry id — because they are read off a bound CDM row and only
  entries resolve to rows; `auraUp` and the `auraRemaining` / `stacks` channels name an
  **aura spell id** an entry or a silence declares, because the aura latch is keyed by
  spell id. The form lives in `Catalog.GATES` / `Catalog.CHANNELS` (`subject = "entry"` |
  `"aura"`) so the table stays the one place the vocabulary is described. The exemption
  list is still exactly the three `spec.md` names.

  ⚠ **The looser rule shipped first, and it was a trap the review caught (2026-08-08).**
  The pass originally accepted *either* form on *any* subject term, on the reasoning that a
  spell id a silence declares is a declared ability. It is — and it is also unanswerable:
  `{"proc", 264173}` is semantically `{"proc", "E7"}`, type-checks, passes all five checks,
  and is then permanently UNKNOWN for the life of the build, while gate health reads
  `proc:1/1` — "nothing refused" — because the read was never asked for at all. The mirror
  case is worse still: `auraUp("this")` resolved to an entry id, `Track.Binding` filtered it
  out of `auraIDs` entirely, and the band was dead with no latch and no tally. A wrong-form
  subject is not a stricter spelling of the right one; it is a silent hole, which is
  precisely the failure the three-valued gate exists to make visible.
- **`Track.New()` lost its catalog argument.** Nothing read it once the windows went, and a
  stored-but-unread field with a comment explaining its purpose is the shape of the thing
  house rule 2's receipt describes.

---

## 2026-08-08 (the reorder) — the draw-first directive revised: simplify, then draw, then detail

**The order changed again, one day after it changed.** 2026-08-07 (later) put drawing ahead
of everything on the grounds that §3.5's apparatus had been authored in full against no
evidence, and that only playing could settle it. **That diagnosis stands and is not being
walked back.** What is revised is the sequence.

**The directive is now: simplify → draw → add detail as play tells us to.** The window
migration goes first; M3c/M3d/M3e follow it.

### Why the reorder was half right

Drawing before the migration means drawing whatever `Tier.lua` computes today, and that is
still the **window-era** model — six named windows, `remaining` counted off a declared base
cooldown, negation legal only inside a window. `spec.md` deleted all of that on 2026-08-07;
the code and `catalog.md` §2 never followed.

The 2026-08-07 entry conceded the cost in its own words — *"any refinement made while
playing gets re-expressed once that migration lands, and that is real rework"* — and
defended it on the grounds that feedback of the form "Dreadstalkers feels wrong here" is
vocabulary-independent. **That defence covers the feeling and not the fix.** The feeling is
indeed vocabulary-independent; the tuning you do in response to it is not, and the migration
carries four shape decisions that are still open (the hold-cue threshold `t`, whether E5
band 2 survives on an un-apexed build, whether `dogs_out` becomes a band or a cue, and E9's
negation). Tuning against a model with four unsettled joints, then re-expressing it, is the
rework the reorder named and then accepted too cheaply.

Put plainly: **drawing an outdated model teaches you about the outdated model.**

### What "simplify" does and does not mean

**It does not re-open `spec.md` §3.** The rule cull earlier the same day *was* the
simplification pass — three principles in §1, five checks in §3.5, the priority-ladder
apparatus gone. Re-arguing §3.1/§3.5 now would be the fifth re-run of the argument
`discussion.md` already carries, and it would be the exact failure mode the 2026-08-07
reorder correctly identified: authoring rules against no evidence.

**It means the code catching up to the spec that already exists.** The migration adds no
capability — every fact the window-era catalog knows, the migrated one knows, only spelled
differently. What it buys is that the thing we put on screen and then tune is the model we
are keeping.

**And the detail added afterwards comes from playing, not from authoring.** That half of the
2026-08-07 plan is untouched and is still the point: refine until it feels good, then
reverse-engineer the rules from that for the second spec.

### Cost, stated rather than glossed

Nothing is on screen for one more work item than yesterday's plan implied. Accepted — the
migration is a bounded pass over four files plus `catalog.md` §2, not a design round, and
`Catalog.Resolve`'s `alt` defect (E3 silently dropping on a Fel Ravager build) is a
correctness bug that rides in the same function and gets fixed on the way.

Work: `backlog.md` → **The window migration**, now first in `Now`.

---

## 2026-08-08 (later) — the backlog restructured, and four residuals closed

`backlog.md` → `Now` had drifted into 290 lines of mostly-done history, with the queue order
described in a ⚠ note that the file itself then contradicted. `Now` is now the queue **in
queue order** and holds **only open work**: the drawing rungs (M3c/M3d/M3e) · the M3b
leftovers · the window migration · the hidden-row surface · the stale artifacts · loose
decisions carried out of M2. The done ladders moved to a new **`## Reference` — done, and
the reasoning still binds** at the end of the file; that section exists for the reason the
old M2-ladder blurb already gave, which is why the blurb became its preamble rather than
being paraphrased away.

**Five open items were recovered from sections that read as finished** — the thing the
restructure was actually for. Three came out of `M3b–M3e` (the `refused:` criterion, the
three never-exercised flight criteria, and the `alt`/Fel Ravager defect, which had been
marooned *below* an acceptance table) into **The M3b leftovers**; two came out of M2b and
M2c, both headed ✅ DONE (the
no-catalog player-facing line; `Log.Render`'s missing busted suite) into **Loose decisions
carried out of M2**, with a one-line "not fully closed" note left behind in each rung so the
DONE record does not read as complete. Open-item count was **29 before and 29 after**; `[x]`
56, `[code]` 4, both unchanged.

The four residuals left by the cull, one line each:

- `backlog.md`'s two "see the rule cull" pointers (the breadth-count arithmetic in the
  window migration; the "don't count it toward breadth" half of E4's drop) now say plainly
  that check 2 was deleted on 2026-08-08, instead of pointing at a section that no longer
  exists.
- `Catalog.lua`'s cue-honesty failure message no longer cites "fails §3.1 like a bare HIGH
  band" — a rule the cull deleted — and instead states what check 4 requires. **Finding key
  `"cue-honesty"` untouched**: it is a log-format token the busted suite asserts on. 92
  successes / 0 failures, luacheck 0/0 in 16 files.
- `spec.md` §3.5's cue definition said "a marker drawn beside the icon", contradicting
  §3.0's glossary row (rewritten on 2026-08-08 to "on an icon or on a §3.4 bar"). Brought
  into line.
- M3a's `Catalog.lua` line kept its "coverage **and breadth re-run**" wording — M3a did
  build both — with the note that the breadth re-run was deleted on 2026-08-08. `## Done`'s
  banner claiming the `[code]` items are "not flown" is replaced: M2 **was** flown at M2d,
  and `/cap status` was subsequently removed by M2b.

**And one the review of the restructure caught, which is the only one with teeth.** The
window migration's *E10's Infernal Bolt bands* item still quoted the band as
`identity(Infernal Bolt) and shards ≤ 2` — the grammar **F3 had corrected that same day**,
because `identity`'s first argument is the subject and not the tested state. The item is
what a future session transcribes E10 from, so it would have re-introduced the exact defect
F3 existed to remove, in the addon table rather than the document. Now quoted as
`identity(this) ≠ base and shards ≤ 2`, with the reason attached. ⚠ **The lesson is about
where a corrected claim is repeated:** F3 fixed `catalog.md`, and nothing checked whether
`backlog.md` was quoting it. The two remaining "see the rule cull" phrases (M3e's item, the
acceptance-table item) were re-pointed at the dated `## Done` entry in the same pass.

Housekeeping only — nothing here decides anything about the addon.

## 2026-08-08 — the rule cull applied, and the surviving document defects closed

Both `Now` clusters executed in one pass. The reasoning is not re-argued here — it is the
2026-08-07 (later) entry above; this records what actually moved.

### What changed, by file

- **`spec.md`.** §1 gains the **three principles** as the mission statement, with the three
  moves (re-present / grade / contextualise) kept underneath them; "narrows decisions
  instead of making them" is gone from §1 in both places it appeared. §3.1's third rule
  ("if exactly one thing is ever HIGH, the tiering is wrong") is replaced by (c), the first
  two rules survive verbatim as a statement about the vocabulary, and the §3.1 Check drops
  its "more than one ability is emphasised" clause. §3.5's **nine checks become five** —
  coverage, register legality, declared subjects, cue schema, estimate disclosure — with 2
  (breadth), 3 (no verdicts as inputs), 8 (negation disclosure) and 9 (a named floor)
  deleted and nothing added in their place. The HIGH-at-once distribution stays as a
  reported statistic with the "has failed §3.1" verdict removed. §4's second bullet is
  restated to *cap does not reduce to a bare flag on the next button*, §4's Assisted Combat
  bullet to *cap did not author it and cannot grade it*, §5's Legitimacy to principle (a)
  with no "defeats the intent" test, and §6 loses the "does the tier signal stay honest
  under pressure?" question. Two ⚠ priority-ladder paragraphs in §3.5 collapse to one plain
  statement that the vocabulary has no term for another entry's verdict.
- **`Catalog.lua`.** `MIN_HIGH_CAPABLE`, the local `highCapable`, the `Catalog.HighCapable`
  export, the breadth finding in `Check`, the breadth re-run in `CheckBound` and the floor
  finding all deleted. `cat.floor` is untouched catalog data and `Demonology.lua`'s
  `floor = SHADOW_BOLT` stays. The inline comments now cite **`spec.md`'s new 1–5**, which
  is the first time the two files have agreed on a numbering. The module header no longer
  justifies `CheckBound` by breadth-over-the-authored-table; it exists for coverage, which
  genuinely needs the live rows.
- **`catalog_spec.lua`.** Three tests deleted (breadth-can-fail, floor-can-fail, and the
  post-drop breadth re-run). `it("names Shadow Bolt as the floor")` **kept** — it asserts
  `cat.floor == 686`, which is a transcription check on catalog data, not on a check.
- **`specs/demonology/catalog.md`.** O7 loses the breadth bookkeeping and is retitled;
  O3 loses its "must not be counted toward breadth" clause; E10's floor note no longer
  cites check 9 and no longer asserts the floor is graded at LOW *as a rule* (band 3's
  unconditional LOW stays as an authored choice with its own ⚠). **F3**: E10 bands 1–2
  become `identity(this) ≠ base [and shards ≤ 2]`, and the "written with the name for
  readability" hedge goes with the name. **F7**: E6's stale `@pending-test:
  cdm-identity-readable-in-combat` replaced by the positive statement and
  `[client 2026-08-06]`. **F8**: E2's note now says the release is `ready(E1)`, matching §2.
- **Three `CLAUDE.md` files** repointed from §3.1's three rules to §1's three principles —
  the project root, the workspace root, and **`addon/CLAUDE.md`**, which the backlog item
  did not list but which carried the same dangling pointer.

### F6 was verified against the Tier-1 source, not re-asserted

`knowledge/addon-dev/cooldown-manager.md` §1.2 routed the two aura alert edges through
`auraInstanceIDToItemFramesMap [:1641, :1652]`. Read directly in
`raw/addon-research/wow-ui-source/Interface/AddOns/Blizzard_CooldownViewer/CooldownViewer.lua`:
`:1641` and `:1652` are inside `CooldownViewerMixin:OnUnitAura` (`:1629`) and call
`OnUnitAuraRemovedEvent` / `OnUnitAuraUpdatedEvent` — display refreshes, not alert
triggers. The alert path is `CheckAuraRemovedAlertTriggers` (`:1672-1680`) and
`CheckAuraAddedAlertTriggers` (`:1682-1690`), called from `OnUnitAura` at `:1636` and
`:1669`, **both of which enumerate `self.itemFramePool:EnumerateActive()`** at `:1675` and
`:1685`. So the section's conclusion gets *stronger*: all six alerts reach an item-frame
method through the pool, with no exception for the aura pair. ⚠ The file's `reviewed:`
date was deliberately **not** bumped — only §1.2's citation was re-read.

⚠ The plan named the enclosing function `OnUnitAuraUpdate`; in the 12.0.7.68887 source it
is `OnUnitAura`. Corrected in the edit.

### Numbers

`busted` **95 → 92** (the three deleted tests, nothing else); `luacheck` 0/0 across 16
files, unchanged; `kblint` 17 findings before and after, none of them in
`cooldown-manager.md`.

### What the plan did not anticipate

- **`Tier.lua:180`'s comment cited "§3.1's breadth measurement"** — a dangling reference to
  a deleted rule in a file the plan put out of scope. Fixed as a comment-only edit to cite
  §3.5's HIGH-at-once distribution instead; no behaviour touched.
- **`Catalog.lua` still emits the finding key `"cue-honesty"`** where `spec.md` now calls
  the check **cue schema**. Left alone deliberately: renaming a finding key is a log-format
  change, and the window migration rewrites this check anyway. It is the one place the code
  and the document still use different words for the same check.
- **B8 needed no code change, confirmed by reading rather than assumed.** `Tier.lua`'s
  `cueOf` (`:162-169`) builds `{ when = cue.gate }` and runs it through `bandHolds`, which
  returns `false` on an unknown — so a cue whose precondition reads unknown is already
  withheld. `spec.md` now says so.
- **`spec.md`'s milestone table still labels M3e "§3.2 procs, and the honesty
  measurement".** Left as-is — the measurement survives, only its pass/fail did — but the
  phrase reads like the deleted gate and is worth rewording when M3e is actually planned.

## 2026-08-07 (later) — the rules are cut back to three principles, and drawing jumps the queue

`discussion.md` D3–D6 worked and struck, all four together. The four items were written as
separate questions about separate rules; they were answered as one, because they shared a
diagnosis none of them had stated.

### The diagnosis

**The rules had multiplied past what they were protecting.** Each was individually
defensible. The set was a governance apparatus written before a single pixel was drawn, and
a fair amount of it existed to keep cap visibly *distinct from CDMProbe* rather than to make
cap good. That is the wrong reason for a rule to exist, and it is why the same argument kept
getting re-litigated from a new angle every session — D3, D4, D5 and D6 are four re-runs of
one unresolved question.

### The three principles

cap's mission, and everything else is downstream of it:

- **a)** cap does not fight the secret restrictions. The **gate/channel split already
  expresses this** and is the one line worth enforcing in code.
- **b)** cap freely uses non-secret information to give good hints.
- **c)** cap does not try to *always* present a single best decision. **This is distinct
  from "never present a single decision" and from "always present several options of equal
  status".** Sometimes one option genuinely is best and the game hands us the data to say
  so — show it, and don't stress. Same for the inverse: sometimes everything is on cooldown
  and nothing is good, and that is also a thing worth showing.

(c) is the load-bearing correction. Every version of the anti-rotation-engine rule so far —
§3.1's third rule, check 2, the HIGH-at-once threshold D5 was hunting — encoded *"the output
must be a field"*. That is (c) overstated into a requirement, and it makes cap lie whenever
the game's own data says one thing is right.

### What each item resolved to

- **D3.** The broad reading was already dead on arrival: §3.3's primary/secondary step hints
  are a literal next-action answer, so adopting broad meant deleting a specced feature and
  nobody was proposing that. But the item's *narrow* option — "cap's output is a field" —
  was itself the thing to drop. §3.1's third rule is replaced by (c). §4's bullet is
  restated to the real anti-goal: **cap does not reduce to a bare flag on the next button
  with no *why* and no *what else*.** That is what the rule was always meant to prevent, and
  it is much narrower than what got written.
- **The Assisted Combat justification changes.** From "it is one answer where cap is a
  field" — which stops working the moment (c) lands — to **cap did not author it and cannot
  grade it**. It is an opaque verdict from rules cap didn't write, so §1's moves 2 and 3
  (grade, contextualise) are unavailable on it; re-presenting it means shipping someone
  else's opinion as ours. Same conclusion, honest reason.
- **D4 is dropped as hair-splitting.** Its hypothetical — a hundred client-evaluated
  comparisons whose composite tells you exactly what to press — is a strawman. If displaying
  available data clearly ends up reading as an instruction, **the UI has been fixed**, which
  is (b) working. No test for "defeats the intent" is sought, because the thing the test was
  hunting is not a failure mode. Legitimacy shrinks to (a) and stops being a veto.
- **D5 is moot.** It asked for a threshold on the HIGH-at-once distribution. Under (c) there
  is nothing for a threshold to enforce. The distribution **survives as a reported statistic
  with no pass/fail** — worth having as the instrument for saying *why* something felt wrong
  in play, worthless as a gate.
- **D6 culls further than the item proposed.** It suggested demoting 2, 6 and 9 to
  disclosures. Instead **2, 3, 8 and 9 are deleted outright.**

### The five checks that survive, and the rule for what may be one

A check earns its place only if it is **schema integrity** or **principle (a)**:

| # | Check | Why it stays |
| --- | --- | --- |
| 1 | Coverage | Schema. Every bound row is an entry or a silence; a row in neither is a defect, not an opinion. |
| 4 | Register legality | **This is (a) in code.** No channel in a band, no gate driving a cue's channel. The most important line in the file. |
| 5 | Declared subjects | Schema. A term naming an ability nothing declares is a reference error. |
| 6 | Cue schema *(mechanical half only)* | The renderer cannot draw a cue without polarity, its tier, and a precondition. The **"strict enough to not be permanently lit" judgement half goes to prose.** |
| 7 | Estimate disclosure | (a)'s own to-do list — it names every place cap guesses at a number the client would state exactly. Cannot fail, and that is fine. |

Deleted: **2** (breadth ≥3 HIGH-capable — an arbitrary number measuring capability when the
concern was co-occurrence), **3** (a no-op; the vocabulary has no term for another entry's
verdict, so it goes to prose as a statement about the vocabulary), **8** (negation
disclosure — it existed *only* to police the priority-ladder worry, and that worry is
deflated), **9** (a named floor — DPS-shaped, trivially satisfiable, and its LOW clause was
already falsified by E10's Infernal Bolt band, `backlog.md` F2).

### The process change, which matters more than the cull

**The rules were reverse-engineered from nothing.** §3.5's apparatus was authored in full
before anything was on screen, and D3–D6 are what happens when you argue a governance model
against no evidence.

Inverting it: **ship the tier/cue system, play with it, refine until it feels good, then
reverse-engineer the rules from that — for the second spec.** Demonology is the instrument,
not the proof. So **drawing jumps the queue** ahead of the window migration.

⚠ **The honest cost of that reorder, stated rather than glossed:** M3c/M3d will draw
whatever `Tier.lua` currently computes, and that is still the **window-era** catalog. What
the window migration changes is how the catalog *expresses* cross-ability facts, not which
facts it knows, so the tiers coming out are largely the same — but any refinement made while
playing gets re-expressed once that migration lands, and that is real rework. Accepted:
feedback of the form "Dreadstalkers feels wrong here" is vocabulary-independent, and it is
the feedback that cannot be obtained any other way.

### What evaporates rather than being fixed

Three queued items were fixing rules that no longer exist. Struck, not done:

- **F1** — the bound breadth count being seven vs eight. There is no breadth check.
- **F2** — E10's HIGH band colliding with check 9's LOW clause. There is no check 9.
- **The `backlog.md` item "D5 undersells its own case"** — there is no D5.

Work: `backlog.md` → **the rule cull**.

---

## 2026-08-07 — windows are deleted, cues carry the nuance

The largest design change since §3 was written. **`spec.md` §3.1 and §3.5 are rewritten**;
`discussion.md` D1 and D2 are struck. The Demonology catalog has **not** been migrated yet
and is now inconsistent with the spec — that is the top backlog item.

### What changed

Cross-ability reasoning used to live in a capped list of six named **windows**, and cues
were restricted to aura stack counts. Now:

- **A band may name any declared ability**, through the gate vocabulary. Windows are gone
  as a concept, along with `window(x)` and `remaining(x)`.
- **Negation is legal in a band**, on any subject — decided later the same day, see below.
- **Cues carry polarity** — positive (a reason to press, drawn in a tier's treatment) or
  **negative** (a reason to wait, drawn in a hold treatment belonging to no tier).
- **A cue's channel may name another ability**, and may be a countdown, a thresholded
  countdown, a count or a sealed boolean rather than only a stack count.
- **`casts` is not a gate any more** — it survives only as sequence-trigger vocabulary —
  and `elapsed` is restricted to `this`.
- **The guard moved from syntax to measurement.** The breadth check and the HIGH-at-once
  distribution are now the whole enforcement against a rotation engine.

### Why — three arguments, and the third is the one that decided it

**1. The window cap was governance, not capability.** Every window in the Demonology
catalog read something cap could already see. `cores_dry` is the clearest case — and it is
worth restating precisely, because the first version of this paragraph overstated it two
ways (a third overstatement, about how to replace it, is under *the negation assumption*
below).

It needed a window for **two** reasons, not one: E9 was not allowed to name E7, **and a
window was the only place negation was legal.** So subject freedom on its own would not
have freed it; both restrictions had to go. What it never needed was a new data source, and
there are **two** readable routes to the fact, not three — `proc(E7)` and `auraUp(Demonic
Core)` cid 777. The sealed Core stack count is a *channel*: it is a third way to put the
fact on the screen and is **not** a way for a band to read it, so counting it as a readable
route was a category error. Confusing "needs a window" with "has no data source" is still
what kept the mechanism looking load-bearing; the point survives its own overstatement.

**2. The restriction pushed authors toward cap's own arithmetic.** Because a band couldn't
read another ability, the catalog reached for `elapsed`/`remaining` counted against a
hand-declared base cooldown — an estimate — in exactly the places where the client would
have evaluated the real number exactly. Every low-confidence row in the catalog
(`tyrant_active`, `tyrant_far`, O1, O2) was cap counting. **O2 is retired outright**:
nothing counts down from a declared base cooldown any more.

**3. It had the platform's intent backwards.** The 12.0 architecture draws one line — you
may *display*, you may not *compute*. The old design treated "cap branches on it" as the
safe path and "the client renders it" as suspicious, which is inverted. A cue pipes a
sealed value through and does no arithmetic; that is the most aligned thing cap can build,
not a loophole. §1's "narrow decisions, don't make them" was being read as a limit on how
much cap may *show*, when it is a limit on how much cap may *decide*.

### The cost, accepted explicitly

- **The player must read tier and cue together.** §3.1's "never AND two signals" rule is
  **narrowed to positive cues** rather than deleted — a positive cue is drawn in its tier's
  treatment and genuinely is not a second language; a negative cue is the deliberate
  exception. Accepted: a lit button with a red countdown is a clearer statement than a
  button that silently went dark, and absence is ambiguous (on cooldown? untalented? cap
  blind?) in a way a drawn countdown is not.
- **cap cannot verify what a cue drew.** No readback exists — `GetEffectiveAlpha` throws
  once alpha carries a secret, and this is permanent, not merely unsolved. Accepted,
  because the verification target is *did the hint point me right*, answered by playing
  and by comparing parses against optimal — not by asserting on Blizzard's renderer. cap
  logs that a cue was **offered**, which is the part that is ours.
- **Nothing structural now prevents a priority ladder.** The HIGH-at-once distribution has
  to be measured continuously and acted on, and `spec.md` §6 says so.

### What the screenshot and the DB2 settled, at no cost

A capture of the in-game Cooldown Settings panel plus `raw/wago/CooldownSetSpell.csv`
answered three things that were being treated as unknowns. The client facts are written to
`knowledge/addon-dev/cooldown-manager.md`; what belongs here is what they mean for cap:

- **Call Dreadstalkers binds a TrackedBar row (cid 760)** alongside its Essential icon
  (cid 671), which nobody here had noticed. ⚠ **This overturns nothing.** No project
  document ever claimed "a summon has no duration to draw"; the standing claim is *a summon
  has no **aura** to read*, that is exactly what the 13 in-combat `auraDataUnit = nil`
  samples measured, and it is untouched. What the bar row establishes is that **a row
  exists** — it does **not** establish a reachable duration, because the field a duration
  would arrive through was nil on every one of those samples. The KB block carries that
  hedge; the first version of this bullet dropped it, and the hedge is the entire distance
  between "there is a bar" and "we can draw the pets' timer".
- **O1 is answered, and not by a new capability.** `tyrant_active` claimed to have no
  observable source. **Dominion of Argus** is a Tyrant-triggered 25 s buff, is a tracked
  bar (cid 169561), and binds a real aura — and E5 band 1 *already reads it*. Band 2's
  window could only ever have fired on a build without the talent. ⚠ **The 25 s is off the
  live in-game tooltip and the game KB disagrees with it** — see *one reviewer finding
  rejected*, below.
- **A spec's candidate row list is offline-derivable**, so "does a row exist for X" is a
  DB2 query, not an in-game hunt. ⚠ **But "the full row list" is three different numbers
  and they must not be run together.** On this build and spec: DB2 `CooldownSetID 60` =
  **65** rows; the client's `GetCooldownViewerCategorySet` = **44**; rows actually laid out
  and walked by cap = **21**. **Coverage check 1 is measured against the 21** — every row
  cap binds is an entry or a silence — and the DB2 65 is the superset that answers "could a
  row exist for X", which is a different question. Summon Demonic Tyrant has a bar row at
  cid 84224 carrying `HideByDefault`. ⚠ **That the player can enable it is an inference,
  not a measurement**: it follows from the saved-layout override path in Blizzard's Lua
  (`knowledge/addon-dev/cooldown-manager.md` §1.2) and has not been tried on the reference
  character. Two coverage defects fell out regardless: **E4 Summon Doomguard binds nothing**
  and is inert, and **Summon Vilefiend** (cid 763, spell `1251781`) is neither an entry nor
  a silence.

That last one produced a new spec requirement: **"in the data but not displayed" is a
distinct state from "not in the data"**, and the capture log must say which. A cue resting
on a hidden row fails silently with no other symptom.

### The negation assumption, raised in the morning and resolved in the afternoon

It was first written down as an assumption to revisit later: bands stay **positive**, no
negation, on the grounds that the anti-ordering rationale survived the window deletion and
that `cores_dry`'s consumer would invert cleanly. **Both halves were wrong, and the second
was checkable at the time.**

The proposed inversion was: instead of Power Siphon reading "no core is lit", Demonbolt
carries a *positive* cue when a core is up. But **E7's two bands already both require
`proc(this)`** — so a "a core is up" cue on Demonbolt says exactly what the entry lighting
at all already says, and is redundant with its own visibility. Worse, it moves the signal
to the wrong ability: E9 loses its only distinguishing band and collapses to an
unconditional LOW. That is not a demotion, it is silence.

**So negation is legal** (`spec.md` §3.5). E9 band 1 becomes `ready(this) and not
proc(E7)`, which is the fact it always meant. The rationale: a proc is a self-contained
readable signal, so "no core is lit" is a statement about the fight rather than an ordering
trick and can legitimately refine a tier; and the rule's original justification was tied to
windows being the sanctioned negation site, which no longer exist.

⚠ **The cost is stated plainly rather than softened.** `not ready(X)` is the literal atom
of a priority list. With negation legal there is **no syntactic guard left at all**, and
the HIGH-at-once measurement is the only thing standing between a catalog and a rotation
engine. What we added is visibility rather than a new restriction: `spec.md` §3.5's new
**check 8** lists every band negating a term on a subject other than `this` in the load
report — a standing list, not a failure, the same shape as the estimate-disclosure check.

### The fix pass, and what an adversarial review of the rewrite turned up

The same day, the rewrite above was reviewed against itself and against the client, and 14
defects were confirmed. Most were mechanical (a renumbered check citation, five dated
asides left in `spec.md` where the project's own rule says history is this file). Six were
substantive and are worth keeping:

- **§3.1 contradicted itself about visual languages.** The old rule — *never ask the player
  to AND together two differently-styled signals* — sat five paragraphs above the new text
  saying exactly that and defending it. Resolved by narrowing the old rule to **positive**
  cues, which are drawn in their tier's treatment and genuinely are not a second language;
  a negative cue is the deliberate exception and always was.
- **§3.5 contradicted itself about what prevents a priority ladder.** *"A verdict is never
  an input … this is the restriction that actually prevents a priority ladder"* against
  *"the guard is measurement, not syntax"*. The second is correct and now owns the claim;
  the first is demoted to preventing the *cheapest* form — an entry demoting itself because
  another came out HIGH — which is real but small.
- **The negative-cue worked example was backwards.** `cooldownRemaining(Summon Demonic
  Tyrant)` with no threshold draws *hold* at 45 s remaining, which is precisely when
  Dreadstalkers should be pressed. That produced **thresholded channel terms**:
  `cooldownRemaining(x) ≤ t` and `auraRemaining(x) ≤ t`, backed by the curve measurement
  from this session (a `Step` curve is a previous-point floor, so two points put the edge
  exactly on *t*, and every `Evaluate*` result is secret even with a non-secret curve). The
  un-thresholded forms stay — §3.4's bars want the number, not the edge.
- **`casts == n` is deleted from the gate table.** It let an author write `casts == 0 →
  HIGH` on ability A and `casts == 1 → HIGH` on B: a literal ordered opener written in
  bands, duplicating §3.3 and breaching §4. It survives as **sequence-trigger vocabulary
  only**, where being an ordered list is the point. `elapsed` was reverted to `this` at the
  same time — an entry may estimate about itself and about nothing else — and `combat`
  stays a gate.
- **"Every term below takes one subject" was false**, and the falsehood had teeth: `mode`'s
  argument is the literal `single`/`aoe`, so the new declared-subjects check would have
  flagged **every AoE band** in every catalog as a defect. `resource` and `combat` take no
  subject either. `talent(x)` is exempted for a different reason — a talent may be a
  passive with no CDM row, so it can be neither an entry nor a silence, and checking it
  would make the one gate whose whole purpose is talents an authoring defect.
- **A band naming a dropped or hidden subject had no defined semantics**, which is new
  surface: before the change a band could only name `this`. It reads **unknown**, so the
  band fails and the entry demotes — never *false*, because "the situation is absent" and
  "cap cannot see the situation" are different statements. The "available, not displayed"
  log line now covers band subjects, not only cue subjects. This is live on the reference
  build, where E4 and E9 both drop.

**Windows are also now defined for sequences**, which was dangling: `catalog.md` §6 still
has `enter: window(tyrant_setup)` and `enter: window(opener)` naming a mechanism that no
longer exists. A sequence trigger is **a band-legal condition plus `casts == n`**.

### INFERNAL BOLT — a real catalog defect, found by the same pass

`catalog.md` E10 said Infernal Bolt *"is strictly better and equally unconditional, so the
tier does not move"*. **It grants 3 shards.** Against a 5-shard cap, pressing it at 3+
shards wastes them — structurally the same case E7 documents for Demonbolt, in the entry
that sits directly below E7 in the same document. E10 now has three bands: HIGH at
`identity(Infernal Bolt) and shards ≤ 2`, LOW transformed, LOW unconditional.

Two consequences. **E10 becomes HIGH-capable**, taking the bound catalog's breadth count
from six to seven — and its HIGH is the only one that fires in *steady state*, which
partially answers O7's "long no-HIGH stretches" worry with something other than a shrug.
And **the aura route was never available**: Infernal Bolt has its own tracked-buff row
(cid `172289`, aura `433891`, `flags = 2` = `HideByDefault`), it is hidden, it binds
nothing, so `auraUp` cannot see it and `identity` on the Shadow Bolt row is the route that
works.

### One reviewer finding REJECTED, and it became a KB-staleness item

The review said Dominion of Argus is 15 s, not the 25 s recorded above. **The 25 s stands.**
The live in-game tooltip read on 2026-08-07 says *"leaves open a portal to Argus for 25
sec"*, and the running game outranks DB2 and the KB — the same rule that settled the
`1276166` id conflict in the opposite direction.

What the finding *is*, correctly routed, is that **the game KB is stale**:
`knowledge/classes/warlock/demonology/` carries 15 s in several places and the wago extract
agrees with it, which means a hotfix has not been ingested. Parked in
`knowledge/_meta/kb-inbox.md`.

### And six client facts went to the KB, where they belong

Everything measured this session about hidden CDM rows — that a `HideByDefault` row is
filtered out in Blizzard's *Lua* at data-set construction and therefore never gets a frame,
that no alert edge can fire for one (which **scopes** the KB's own
`hooksecurefunc(item, "TriggerAlertEvent")` completeness guarantee to bound rows), that the
API still returns hidden rows and that the struct's `category` is the raw DB2 value rather
than the player's effective placement, and that a saved layout can un-hide one — is in
`knowledge/addon-dev/cooldown-manager.md` §1.2, not here. `C_Spell.GetSpellCooldownDuration`
carrying no `SecretWhenCooldownsRestricted` went to §7 Tier 3, marked as a **doc-annotation
inference rather than a measurement**.

---

## 2026-08-07 — two reference artifacts, and a fourth spec file

**Published, and both are current as of v0.2.1.** They are *derived* documents — every
number in them was read out of the code or the capture, not typed from memory — so treat
them as a view, and the source files as the truth:

- **Architecture — how cap is wired and where the signal stops**
  <https://claude.ai/code/artifact/2de40ee9-5457-4ca3-b46e-77178e021207>
  The pure/impure split, the gate-vs-channel constraint, and the dead end between the
  computed verdicts and the screen. Written to answer *"are we actually showing anything
  yet?"* — the answer being one text label.
- **Demonology reference — every tracked row, what lights it, what is drawn on it**
  <https://claude.ai/code/artifact/46bb78b6-7c41-4210-a9b0-3b1707678569>
  The three channels, all 21 CDM rows with their bands and cues, the thirteen silences,
  and the crossing diagram showing that both threshold cues are **read off a buff row and
  drawn on an Essential icon**. Transcribed by running the real catalog through
  `Catalog.Resolve` against the client fixture.

⚠ **Building the second one found a live defect**: E3 declares `alt = {1276467}` for
Grimoire: Fel Ravager and **nothing reads that field**, so E3 drops silently on a Fel
Ravager build. Filed in `backlog.md`, not yet fixed. Transcribing a table by hand is a
worse instrument than running the code — and it found something 95 tests did not, because
no test covers a build cap has never run on.

**`specs/discussion.md` is new** — a fourth file, for topics raised and not yet decided.
The three-file process had no home for *"here is a question that would change the design,
and here is the case on both sides"*, so such questions were getting decided in passing or
lost. It is registered in the project `CLAUDE.md`.

---

## 2026-08-07 — M3b FLOWN. The tier signal computes correctly in a real pull.

v0.2.1, 76 s on a dummy, Demonology/Diabolist. 53 tier lines, 58 edge lines, 50 in-combat
samples. **Every gate answered, every pull, without a single refusal.** The acceptance
table with its measured column is in `backlog.md`; what is worth recording here is what
the flight taught rather than what it confirmed.

### The three results that matter

**The alert channel IS the readiness route.** `hooks:21` — one hook on every CDM row —
and `Available` / `OnCooldown` landed on exactly the four entries that have cooldowns and
on nothing else. M3a's whole design rests on this and it had never executed. The
`--@unverified` marker on `installHooks` is discharged.

**E6 Ruination fired.** Six samples at `E6:HIGH/1`. Before the lab answered
`cdm-identity-readable-in-combat` this entry was dead code that would have passed every
unit test and never lit once — the transform arms mid-pull and `Bind` refuses to resolve
in combat, so the identity had to come from an independent in-combat struct read. It does.

**`dogs_out` promoted Tyrant within 2 s of the Dreadstalkers cast**, and E5 hit **all
four** of its bands across the pull — the apex buff, `tyrant_active`, 5 shards, and plain
affordable. The catalog's centrepiece works, and the most complex entry in it exercised
every branch.

⚠ Gate health went `blind:3 → blind:0` and windows `4/6 → 6/6` within six seconds, both
for the same reason: `elapsed` is unknown until a cast is observed. That is the
three-state design behaving correctly — unknown, not false — and it is visible in the log
rather than inferred.

### The criterion that was wrong, which is the useful part

`refused:33` against `edges:19` reads alarming and is almost certainly correct: the hook
sits on all 21 rows and 13 of them are silences, so refusal is the *expected* case for
most of the roster. But I had written the criterion as *"small ⇒ good, large ⇒ the cid is
wrong"*, and **the count cannot distinguish those two at all.**

Worse, the instrument could not settle it either: refusals were counted and never logged
with their cid. That is the exact failure mode the KB warns about — *an instrument that
cannot observe its subject must say so, not emit a number* — committed by me, in a
criterion I wrote specifically to catch a cid-resolution bug. Fixed: a refused cid is now
logged once and counted thereafter, and the criterion is restated as **every refused cid
is a declared silence**, which is mechanically checkable.

### Three things the flight did not exercise, recorded as such

The settle fired `by:quiet`, which is **correct for a login** — the generation never moves
past its initial value, so the event arm cannot fire and the quiet fallback is the only
one available. It is not evidence the event arm works. Likewise the dark-for-the-fight
rule (cap settled 19 s before the pull) and `/cap aoe` (`mode:single` on all 50 samples).
None of these failed; none of them ran. A criterion nobody exercised must not read as a
pass, so they are open items rather than ticks.

### The HIGH distribution, which is NOT the M3e measurement

For the record and flagged as premature: 0 HIGH on 54 % of samples, exactly one on 30 %,
two or more on 16 %. `spec.md` §3.1's third rule is not violated. But this was 76 s of
mostly steady state with one Tyrant window, and neither the Implosion cue nor the proc
demotion exists yet — exactly the reason the measurement was moved to M3e. Reading a
breadth verdict off it now would retire a catalog that is behaving as designed.

### And the curve subsystem closed out

Two lab cells answered in the same session, both favourably, and both were built on the
back of a question that started as *"can a highlight change colour at 20 s left?"*:

- **`Step` is a previous-point floor.** With points at 0 and 20 the value changes at
  x = 20, not at the midpoint. So a threshold at *t* is two points, and the four-point
  padded `Linear` workaround I had proposed is unnecessary.
- **Both curve types clamp** outside their range, on both ends — the inference from
  `EncounterTimelineTrailAlphaCurve` was right.
- **Every `Evaluate*` result is secret even with a non-secret curve.**
  `SecretWhenCurveSecret` names a sufficient condition, not a necessary one. There is no
  binary-search leak, and no legitimacy problem with the graded register: cap hands the
  result to a sink and never sees it.

---

## 2026-08-07 — M3a closed and M3b built: the catalog had windows it could not evaluate

M3a is done and M3b's code is written. Nothing released, nothing flown. 95 busted tests,
0 luacheck, and 15 mutations checked across the new code.

### The gap nobody had noticed

`Track` was specified to emit "window truth", and the catalog document defines all six
windows precisely — but **the addon's table declared them as `{ name = true }`**. There
was no form in which a window could be *evaluated*, only asserted to exist. Every band
naming one would have read unknown forever, which is three of ten entries.

So the window rule form is a **spec change made deliberately**, not an implementation
detail: `spec.md` §3.5 gains a window vocabulary and `catalog.md` §2 gains a Rule column
transcribing what its prose already said. The shape follows what the format was already
built for — `Catalog.Check` **already refused `term.negate` in a band**, which is only
meaningful if negation is legal somewhere, and windows are that somewhere.

Three terms exist only in a window, and each earns its place by not being a gate:
`remaining` needs a *declared base cooldown*, i.e. an assumption about the build rather
than an observation; `combat` and `casts` describe the pull rather than an ability.

⚠ **`remaining` is where O2 now bites, and it bites in one place.** `tyrant_far`'s
">20s out" counts down from the entry's declared `cd`, corrected from the client whenever
it will say — which is out of combat only. Anything shortening Tyrant's cooldown makes
that window late, and it is late at one number instead of smeared across two bands.

### The health measurement had to be told what to count

`Catalog.Reads` exists because the first cut of the gate tally counted every gate against
every entry. On the bound Demonology catalog that reports `identity: 0/8` — seven
refusals that were never asked for — and a **working catalog reads as blind**, which is
precisely the confusion the tally was built to remove. It now counts only the gates an
entry's own bands, its cue gate, or a window naming it actually ask for.

The same map tells Sense which reads to make, so the expensive half fell out of the
honest half rather than being optimised in separately.

### Five things the build got right by being told to, and one it did not

Carried in from the handoff and all live: the weak-keyed hook table, the cooldownID
resolved *inside* the callback, the GCD floor on the baseline, three-state readiness with
a per-evaluation count, and the charge guard (which does nothing on Demonology and is
structural).

**The one defect the review caught:** the quiet-settle arm was driven only from a `Bind`
evaluation. On a quiet login nothing resolves again after the login grace, so a settle
waiting on the next resolve never comes — and cap would be **dark for the first pull of
every session**. It is driven from the tick now, and only while unsettled.

### `secretDuration()` was promoted, not deleted

House rule 2 says the probe dies with the claim, and the duration-predicate test died.
But its source-finder is exactly what §4.2 row 8 had been **blocked** on for the life of
the registry — *"every secret this client hands an addon is a cooldown number"*, now
false. So the helper was promoted out of the dying test into row 8's own, which is the
rule's own "promote the reader out first" precedent rather than an exception to it.

⚠ The five in-combat identity runs say something **weaker** than the single run recorded
last session. `overrideSpellID` is plain on 21/21 in every run — that part is stronger,
and it was observed *moving* mid-pull on two rows, which is what clears §4.11's
discriminate test. But `GetSpellID()`'s secret set **moved between runs seconds apart and
did not track `auraDataUnit`**: a row with no bound aura read secret in 3 of 5, a row
with one read plain in 3 of 5. The clean correlation was one sample's coincidence. The KB
says the volatile version.

---

## 2026-08-06 — M3a flown: two answers, and the CDM was announcing what I was polling for

### The two questions that answered

**Duration predicates are SECRET BOOLEANS.** `HasExpired` / `IsActive` / `HasStarted` /
`IsZero` all read `<secret boolean>` in combat, control (`GetRemainingDuration`) also
secret, `HasSecretValues() == true`. Measured twice. So `ready(this)` can never be a
direct read. Two consequences beyond that:

- a secret boolean still drives `SetAlphaFromBoolean` / `SetVertexColorFromBoolean`, so
  readiness **emphasis** is drawable leak-free even though readiness is not branchable;
- it is the **first boolean secret this workspace has ever obtained**. §4.2 row 8
  (`secret-op-bool-test-boolean`) is registered `blocked` on the grounds that *"every
  secret this client hands an addon is a cooldown number"*. That is now false, and the
  row is unblocked. ⚠ Not yet actioned.

**A row's display identity IS readable in combat, and E6 is saved.**
`GetCooldownViewerCooldownInfo(cid).overrideSpellID` read **plain on 21 of 21 rows**.
`item:GetSpellID()` was secret on exactly 3 — the 3 with `auraDataUnit` non-nil — so the
existing "secret on aura-bound rows" claim upgrades from *8 of 51, and those 8 were
aura-bound* to a clean correlation, 18/18 plain and 3/3 secret. Bonus, caught live: cid
135056 read `override=132411` against `base=1276452` mid-pull where the out-of-combat
bind had them equal, i.e. a transform observed moving. (`132411` does not resolve in the
static Game Data namespace — the second such id in two days.)

### The correction that matters more than either

**The CDM announces both readiness and aura presence as EVENTS, and I was polling.**
`CooldownViewerItemMixin:TriggerAlertEvent` carries six types. `Available` /`OnCooldown`
fire for cooldowns; `OnAuraApplied` / `OnAuraRemoved` fire from the viewer's `UNIT_AURA`
handling, matched purely by `auraInstanceID == self:GetAuraSpellInstanceID()` — **no tick,
no window, no settings gate**. And the player's alert configuration cannot hide them from
us: the `alertsByEvent` check lives *inside* `TriggerAlertEvent`, so a `hooksecurefunc`
post-hook fires whether or not an alert was configured.

So one hook per item frame supplies `ready` **and** aura presence. Rule 6 already said to
hook it; I had written that down and then built pollers anyway.

### Three instrument defects, one root cause

The Dreadstalkers cell burned two flights and never answered. In order: it reported a
full result when *other* rows bound, which took it out of the driver's retry set; its
discriminator was `wasSetFrom*`, a **tab-1** field aimed at a **tab-2** row, so
`sources:none-seen` meant nothing; and even repaired it rode the driver's cadence, which
stops after ~36 s and cannot cover a 12 s window it does not know about.

All three are the same rule — *an instrument that cannot observe its subject must say so,
not emit a number*. The cell is **deleted**, not re-flown, because the question was
malformed: **a summon binds no aura.** Pets are units in the world; there is nothing for a
row to bind, and 13 in-combat samples against 5 genuine aura rows binding normally in the
same samples is the corroboration rather than the finding.

⚠ The failed run did produce a real positive: **Dominion of Argus (BB/169561), Demonic
Core (BB/777), Wild Imp (BI/143038) and both Diabolic Ritual rows all bound**
`auraDataUnit`. So E5 band 1's read is confirmed working, and E8's cue has its live
`auraInstanceID`.

### Five design decisions

1. **Demonic Core gets a threshold cue** — gate `proc(this)` → `stacks(Demonic Core) ≥ 4`
   → drawn HIGH. The sealed count was the reason the catalog had written off overcap
   detection as *"a known, accepted hole"*; it is the same device as E8's pointed at a
   different count, and the hole is closed without any band seeing a number.
2. **`dogs_out` becomes the sixth window** — cross-ability reasoning is legal only in a
   window, and with no aura to read this is the only shape available. The catalog is now
   **at** the six-window cap.
3. **cap does not anticipate.** `tyrant_setup` drops "≤3s out" and becomes simply *ready*,
   which is exact off the `Available` edge — confidence medium → high, one estimate gone.
   Sequences may rely on abilities being fully ready.
4. **AoE is a manual toggle**, following CDMProbe: `/cap aoe`, macroable, mode shown on
   the panel. `spec.md` §6's target-count question is **struck** — answered by design, and
   `mode(x)` joins the gate vocabulary as cap's own state. Every AoE opinion in the
   catalog becomes sayable.
5. **Fury is a second-spec note, not a Havoc verdict.** *"The bar is unreadable"* and
   *"the bar rarely matters"* are different facts; only the second is spec-specific.

### The process fix, which is the durable part

Three sessions in a row re-litigated the same subsystem, so the KB gained
**§4.8.4** — `LuaDurationObject`, one row per method, verdict column, including the rows
nobody has measured marked as such rather than silently implied covered. Prose cannot
distinguish *"measured, the answer is no"* from *"nobody asked"*; a table can. The rule
went into the wow-developer skill: **before testing an API you have already touched, fill
in its verdict table and test only a blank cell.** §4.8.1's channel table is the proof it
works — nobody has ever re-asked whether `SetVertexColor` carries a secret.

⚠ Also recorded as a `[gap]`, not built on: `CooldownViewerBuffBarItemMixin` parks the
result of a secret comparison in **widget state** (`pipTexture:SetShown(currentTime > 0)`),
so `pip:IsShown()` is a candidate live/dead boolean for any bar row — the `PandemicIcon`
mould. It must clear §4.11's discriminate test first; `IsActive()` is the standing example
of a widget read that looks like a signal and is a constant.

---

## 2026-08-06 — M3 planned, and the capture on disk broke three assumptions

M3's plan is written and approved; the ladder is M3a…M3e. What is worth recording is
**how the plan changed**, because the mechanism is reusable.

### The capture is a fixture, and reading it is cheaper than flying

An adversarial review of the first draft was pointed at `wowkb.capture cap bind`
rather than at the docs, and the 21 live Demonology rows (generation 4) settled five
open questions and found three defects **before any M3 code existed**. Each was
re-verified against the rows by hand before being accepted:

- **Shadow Bolt `686` IS a CDM row** — Essential, slot 7, cid `34990`, `isKnown=true`.
  The catalog, `spec.md` §6 and a `backlog.md` work item all asserted the opposite. The
  named floor has an icon, so it is now **E10 at an unconditional LOW** and the "cap
  draws its own icons / a different addon" fork does not need taking on this spec.
- **Call Dreadstalkers occupies two rows** — cid `671` Essential (E2's press) and cid
  `760` BuffBar (`pool=193332`, E1's `auraUp` source). A roster keyed by spellID picks
  whichever it walks first and is wrong for one of the two gates, so binding is keyed by
  `{spellID, family}`. The BuffBar row was in neither the entries nor the silences —
  a real coverage defect, found by running check 1 by hand.
- **Dominion of Argus is `1276166`**, not `1276163`. ⚠ **I got this backwards first.**
  The Blizzard Game Data API resolves `1276163` to a spell of that name and errors on
  `1276166`, so the API said the silence list was right and the roster wrong. The live
  CDM row carries `1276166`. The client wins over the static namespace, and the general
  rule holds: resolve an id conflict against what the game is actually running.
- **Summon Doomguard is absent and Power Siphon is absent** (Implosion is the talented
  half). O3 and the choice node are settled: the authored catalog has ten entries and
  **this build runs eight**.
- **E5 and E6 share cid `34991`.** So `Tier.Evaluate` returns keyed by **entry**, not by
  cooldownID — keying by row would force a silent arbitrary winner between "MEDIUM,
  affordable" and "HIGH, transformed", which is a decision made in a return type.

### Three design corrections that the review earned

- **E6 Ruination is dead code as designed.** `Bind.lua:222` refuses to resolve in
  combat, so every identity field is frozen at the last out-of-combat read — and the
  transform arms *mid-pull*. It would pass every unit test and never light once. Now a
  lab question. Its band also lost its id: `identity(this) ≠ base` needs no literal and
  makes O4's disagreement irrelevant.
- **The seam was in the wrong place.** The first draft made `Tier` pure and put
  everything else behind one impure module — but `Tier` is a first-match band walker
  that does almost no work, while the readiness latch, the cast tape, the `elapsed`
  arithmetic and the windows (every piece the catalog itself rates medium or low
  confidence) all landed where nothing could test them. Hence **`Track.lua`**, pure, as
  the state machine.
- **The honesty measurement moved from M3b to M3e.** Taken before the cue and E6 exist
  it would report "usually exactly one HIGH" — which `spec.md` §3.1 reads as *the
  tiering is wrong* — from unbuilt gates rather than from the catalog. M3b measures
  **gate health** instead, which nothing else in the ladder covers.

### The two carried-forward blockers, decided

- **Health: assume healthy, log problems.** No `CVAR_UPDATE` work, no chat line. §3.5's
  deferred "says so plainly once" is now **log-only**, and `spec.md` §3.5 and its Check
  are edited in place rather than left asserting behaviour the code will not have. The
  reasoning is in the spec: the one state a player could act on raises none of cap's
  events, and a permanent property of the build repeated every login is noise.
- **Hero swap: an event-driven settle.** Commit on the first complete, out-of-combat
  resolve whose reason is `SPELLS_CHANGED` **and** whose generation moved. ⚠ The
  quiet-timer version I drafted first commits at precisely the wrong moment — during the
  first seconds the generation is quiet *because the rebuild has not started*, which is
  the state the settle exists to survive. A quiet-window fallback survives only for the
  identical-row-set case, and both arms are logged so a flight can delete one.

### Two research pointers, both followed

- **The stock proc glow can be dimmed, and we already knew how.** CDMProbe's
  `HudProcGlow.lua` post-hooks each item instance's `RefreshOverlayGlow` and sets
  `item.SpellActivationAlert:SetAlpha(0.5)` — alpha on the *alert frame* multiplies the
  glow without fighting the proc animation, which drives the child textures' alpha. So
  §3.2's "replaces" is achievable as a dim (hiding is protected and blocked in combat)
  and the spec needs no change. ⚠ That mechanism lives **only in CDMProbe's source**,
  which is exactly the failure house rule 1 exists to prevent — it goes to
  `knowledge/addon-dev/cooldown-manager.md` first, and cap implements from the KB.
- **LibOrbitGlow** (`MoONSHO7/LibOrbitGlow`, MIT, LibStub, 12.0+) is cloned to
  `raw/addon-research/`. Honest read: a glow library, not a graded-emphasis engine — a
  glow on every MEDIUM icon is the opposite of a quiet field. It earns a place for
  **HIGH only**, as an accent visibly unlike the proc glow cap is dimming.

### And the treatment question answered itself

`SPELL_UPDATE_USABLE` is registered by tab-1 viewers and rewrites *icon colour only*,
"constantly in a city". So anything cap writes to a CDM icon via `SetVertexColor` /
`SetDesaturation` is stomped unpredictably. **cap draws its own overlay and never writes
a Blizzard region** — which was one of three options offered, and is now the only one
that works. It also makes "one shared treatment table" achievable rather than
aspirational, since the cue text and the icon emphasis end up on the same surface.

---

## 2026-08-06 — M2d: flown, and the binding works

v0.2.0 released and deployed, one pass flown. **M2 is done.** 4 sessions, 224 entries,
accounting exact (12 lines + 12 state rows + 200 identity rows), `samples:` matching the
line count everywhere — nothing trimmed.

**The binding is CORRECT, which is more than "it bound".** 200 identity rows across three
specs and two classes, and cap resolved five display overrides — 686 Shadow Bolt → 29722
Incinerate, 348 Immolate → 445468 Wither (Hellcaller), 85256 Templar's Verdict → 383328
Final Verdict, 35395 Crusader Strike → 404542 Crusading Strikes, 31884 Avenging Wrath →
462048. Those are the exact cases CDMProbe recorded as the hard ones: abilities with no
icon of their own, riding a tracked frame. It got them right on **Retribution Paladin**,
a class cap was never designed against — the first non-Warlock evidence this project has.
⚠ The `rec=bind` digest is the only reason any of that is knowable; without it the log
proves a count and nothing else, and it was added *hours* before the flight because a
capture line is pre-rendered and wanting it afterwards is a re-fly.

**Every other criterion passed.** Row set byte-identical across a 183 s pull. Generation
moved exactly once per real change (1→5 for four changes). **No `PARTIAL` and `u:0` on all
12 samples** — the "a PARTIAL out of combat is a KB finding" trapdoor never opened; the
reads are clean. Frame position survived the reload (`0,-160,false` → `-927,-158,true`).

**Two acceptance criteria were wrong, and they were mine.**

`n:` against `set:` was published as "they must agree". They never do — 26/45, 25/42,
21/44, 25/38. `GetCooldownViewerCategorySet` is the spec's full candidate set even with
`allowUnlearned = false`, so the real invariant is `rows ≤ set`. Written to
`cooldown-manager.md` §7 so nobody rebuilds the check.

And **the `hidden` scope cut was right in outcome but wrong in mechanism.** M2c cut it as
"unreachable — an Edit Mode hide moves no row and fires no event cap registers". The
flight disabled the CDM through the **Options checkbox**, and the truth is worse and more
useful: the verdict was **fully computable** at the time (§4 already records that a hidden
viewer still returns every item frame, so a poll reads rows unchanged with `IsShown()`
false) and was simply **never asked for**. Across 5.7 minutes, off and back on, **not one
sample** — none of the nine CDM/talent events fires on that toggle. ⚠ **It is a sampling
failure, not a detection failure**, and that changes the fix: cap's health channel is
*passive*, sampling only when the CDM's own data moves, so no amount of better verdicts
helps without a trigger. `CVAR_UPDATE` is the obvious untested candidate.

That is an **M3 input, not an M2 bug** — cap does nothing when the CDM is off, which is
still correct. But §3.5's deferred "cap says so plainly once" would be silent exactly when
the player needs it, and `cooldownViewerEnabled` is itself unverified (it appears nowhere
in `knowledge/addon-dev/`), so the `disabled` arm may be doubly dead.

**Four facts drained to `knowledge/addon-dev/cooldown-manager.md`**: `overrideSpellID` is
**always populated** (200/200 rows — so `~= nil` never means "overridden", and rung 5 of
`GetSpellID()` is unreachable); the category set is a superset; `TRAIT_CONFIG_UPDATED`
precedes the CDM rebuild by ~5 s, so a hero swap settles over two events; and the
disabled-in-Options silence above. The `--@unverified` on `GetActiveHeroTalentSpec` is
**discharged** — the Paladin logged `hero:-`, a genuine nil through `pcall`, not a refusal
— and the marker is out of `Log.lua`.

---

## 2026-08-06 — M2c: cap gets an output path

Same day as M2a and M2b, and **still nothing flyable** — no release was cut, which is M2d's
ask-first step. Before this, cap bound the CDM into rows, held a health verdict, and told
nobody: M2b stripped the diagnostic surface and M2c owed it the one output path it is
allowed. It now writes `CombatAssistPlusDB.captures.bind`, read with `wowkb.capture cap
bind`. Five files touched, three created (`Capture.lua`, `Log.lua`, `.luacheckrc`).

**The scope decision, and it is the session's main one.** An adversarial review of the plan
found that cap's **health verdict is not provable**: an Edit Mode hide moves no row and
fires no event cap registers, so `hidden` is effectively unreachable at runtime even after
M2b fixed how it is *computed*. We did not fix that. **If the CDM is off, cap does nothing,
which is correct and does not need proving** — health is logged as whatever it says, and
M2d judges the log rather than the verdict. Cut on that basis: a heartbeat ticker, a
viewers-unreadable counter, refusing `hidden` on an unreadable read, splitting `empty` into
`empty`/`no-rows`, moving visibility sampling to evaluate-time, per-cause `unreadable`
counters, and a CDM-data-loaded flag. What was kept is everything about *cap working at
all* or about the *binding*. ⚠ This means M2d's `hidden` criterion (backlog: "judged against
a CDM actually hidden in Edit Mode") is **expected to come back unexercised**, and that is
the designed outcome, not a gap in the flight.

**Two things the plan did not anticipate and M2c had to fix anyway.**

`health.kind` was **nil on the healthy path**. `evaluate()` assigned it in five arms and
none matched when everything worked, so the first healthy sample would have hit
`string.format("%s", nil)` — an error inside an event handler, on the very first line the
log ever tried to write. Now `"ok"` falls through, and `"unknown"` (never evaluated),
`"ok"` (evaluated, healthy) and an absent value are three visibly different things.

**A clean pull produced no resolve at either combat edge**, which would have made M2d's
headline criterion vacuous. Every in-combat resolve returns early, so a pull that queued
nothing left the row count untouched across the whole fight — and a genuine PASS and "the
log was never writing" produce *identical* evidence. `PLAYER_REGEN_ENABLED` now schedules
unconditionally. ⚠ **That is a behaviour change, not a refactor**, and it exists to make the
post-combat number a measurement rather than a tautology.

**Three properties of the vendored `Capture.lua` shaped the build.** It needs `ns.db` and
`ns.version` and cap had neither — `Stream:_session()` returns nil when `ns.db` is unset and
**every write is dropped silently**, so a full flight would have read back `(no captures)`.
`ns.db` is now assigned in `ADDON_LOADED` *before* `applyDefaults`, so a load-time throw
still leaves the log able to write, and `Frame.lua` stopped owning the root table (two
identities for one root is how a capture lands in an orphan). And **`Stream:Mark` neither
reads nor writes the stream's own `last`**, so with the stream's dedup on,
`Line(x) → Mark(edge) → Line(x)` swallows the second line — the state *after* an edge,
which is exactly what a combat marker exists to record. So the stream runs `dedup = false`
and cap owns the dedup, where a Mark can move the baseline.

**The log's shape follows from lines being pre-rendered strings.** `Log.Render(snapshot)` is
pure and **is** the dedup key; `why`/`d`/`age` sit outside it, because a monotonic field
inside the key makes every line unique and floods the ring. Fields are grouped by
*freshness* — `B{}` is what the last resolve produced, `H{}` the verdict, `C{}` spec and
hero — so a reader never has to wonder whether a number is live or stale. Both combat marks
carry the **full body**, because a bare marker against an unchanged state emits no numbers
and *unchanged is the PASS case*. Combat comes from the **event name**, never
`InCombatLockdown()`. There is no `# config` mark: spec and hero ride inside the dedup key,
so a swap always moves the body and cannot be swallowed. `set:?` rather than `set:0` when no
viewer answered — a coerced zero reading as "nothing configured" is the sin the HUD's
decision log records costing 2,380 corroborating-wrong-answer lines.

**`Capture.Safe()` turned out to be necessary but not sufficient.** It strips colour
escapes, quotes and newlines, but leaves internal whitespace ("Beast Mastery") and braces —
which in a space-delimited line split a field or forge a group boundary. `Log.lua` adds a
local `token()` over it, and passes one **pre-built string** with no varargs so a `%` in a
localised spec name cannot reach `string.format`.

**`/addon-review` caught one real defect.** The `:Row` mirror put `health.detail` — the only
game-authored string in the payload — onto disk **raw**, while the `:Line` path tokenised
it. Rows flatten into the same `.log`, so that was one Blizzard localised reason string away
from a broken capture. Also fixed: a client fact ("`type()` reports a secret's true type")
living only in a comment when it is already KB, and `Log.lua` landing at 0.36 against the
0.35 comment ratio ceiling.

**The gate is live now.** `.luacheckrc` at the addon repo root means
`wowkb.addon release cap` runs luacheck and **aborts the cut on a hit** — its absence is
what silently switched the gate off. Green across all five files, as is luaparser.
`wowkb.capture cap --list` resolves and reports no captures yet, which is the point of doing
the registry edit before the flight rather than after it.

**The log could count but not identify, and that was caught by asking how M2d would
actually be performed.** The summary line carries `n:12 E:5 U:4 …` and nothing else — so
cap could bind twelve rows, have every identity wrong, and produce a byte-identical log to
a perfect run. Aggregate-only was what M2c's backlog item specified, and per-row detail was
always meant to be a `/cap dump` panel button (house rule 4) that does not exist. But
identity is exactly what M3's catalog keys on, so a wrong binding would not surface at the
flight — it would surface later as inexplicable tier behaviour, with a PASS sitting in the
record. `Bind.RowDigest()` + a `rec=bind` row per bound ability closes it. ⚠ It went in
**before** the flight for the reason this whole milestone exists: lines are pre-rendered,
so wanting it afterwards is a re-fly.

**The whole path was driven end-to-end outside the client**, which is as far as static
verification goes: a throwaway harness (scratchpad, deliberately **not** added to the repo)
loads the real `Capture.lua` / `Bind.lua` / `Log.lua` against a faked client, fires
`PLAYER_ENTERING_WORLD` → a pull → a talent change, serialises `CombatAssistPlusDB` in
SavedVariables form, and feeds it to the **real** `wowkb.capture` reader. It renders: four
lines, two of them combat marks, 19 rows, `samples:4` agreeing with the line count, the
digest emitted at `g:1` and re-emitted at `g:2` and **not** at either combat mark. What it
does **not** prove is anything about the client — every API in it is our own fake. It
proves the wiring, the dedup, the generation gate and the reader contract, and nothing more.

**Deliberately not built: a busted suite.** `Log.Render` is written pure so one *can* exist,
but a suite written against a format the first flight is about to change is a
change-detector. It waits for M2d.

**One `--@unverified` is now outstanding** and house rule 5 requires it to be in the current
flight's acceptance set, so it is on M2d: a nil `GetActiveHeroTalentSpec` meaning "no hero
tree chosen" has never been observed here. The log's four-way hero render (`name` · `#id` ·
`-` · `?`) is itself the instrument that settles it. Parked alongside it, not blocking:
`Frame.lua`'s `store()` falls back to a module-local scratch when `ns.db` is unset, which
would silently discard a saved position — unreachable today (every caller is
post-`ADDON_LOADED`) but it fails quiet rather than loud if a call site ever moves.

---

## 2026-08-06 — M2b: the diagnostic surface comes out

Straight after M2a, and **nothing here is flyable** — the changed code still cannot run
without a release, and that is M2d's ask-first step. The payoff is entirely that M2d has
less to judge. cap now has a read API, a movable frame, and no opinions about its own state
that it prints to anybody.

**`/cap status` is gone entirely**, not slimmed: the command, `cmdStatus`, the
`ns.RegisterStatus` registry in `Core.lua`, and both reporters (Bind's dense one, Frame's
one-liner). Bare `/cap` is now help. The registry lasted one day — it was landed on
2026-08-05 precisely so three parallel tracks could each contribute a status line without
touching `Core.lua`, and the thing it coordinated access to turned out not to be worth
having. ⚠ The mechanism was fine; the *surface* was the mistake, and a good mechanism is
not a reason to keep the surface.

**The chat-announcement mechanism went with it** — `MESSAGES`, `announce()`, the
3-per-session cap, the login-grace arming, `state.armed`. That is a wider call than the
reporters: **user-facing warnings are out of scope for the first pass**, and developer
output goes to the decision log (M2c). The five missing-CDM state names were never in
`spec.md` (grepped — zero hits) and now stay internal, so nothing about health messaging is
written into the spec. **The verdict survives as internal state**: M2c logs it, M2d judges
it. Which is exactly why the `hidden` fix still earns its keep — a wrong verdict in the
decision log is worse than no verdict.

**`hidden` is fixed, not collapsed.** `evaluate()` inferred it from `state.frames == 0`,
which M2a proved unreachable-by-construction: a hidden viewer hands back every item frame.
It now reads the **viewer's own `IsShown()`**, counted through `readField` so a non-plain
answer is classed like every other read, stored as `state.viewersShown`, with
`health.viewersShown` carrying the evidence forward into the log. ⚠ Not the *item* frame's
`IsShown`, which is constant-true when hide-when-inactive is off. Row count now means
**configured** — which is what the `#state.order == 0 → empty` arm already meant.

**A correction to the backlog, found by reading the code rather than the item.** The M2b
line claimed the `unreadable` counters "only feed" the stale-retention branch and should go
with it. **They don't.** `complete = false` is set independently at two sites, and the
counters' only reader was the status text. M2c wants "complete vs PARTIAL, unreadable
counts" in the log and M2d treats a PARTIAL out of combat as a **KB finding**, so
`state.unreadable` and `state.complete` are **kept — deliberately written-but-unread for one
milestone**. Only the retention branch and `row.stale` went. ⚠ cap has no `.luacheckrc`, so
nothing will complain about them meanwhile; that is a trade accepted, not an oversight.

**The spec consequence.** §3.5 named `/cap status` four times as the surface reporting
catalog authoring defects, dropped entries and the six load-time checks. All four now name
the capture log (`wowkb.capture cap <stream>`) — the correct destination under house rule 4,
because these are **developer artifacts, not player warnings**. §2's "checking status" setup
affordance is dropped, leaving "moving frames", which is what §4 already said.

**⚠ One tension left standing on purpose, as an M3 decision.** §3.5 still says that when no
catalog claims the spec, cap "says so plainly once" — the same class of user-facing chat
announcement just deferred out of `Bind.lua`. It is M3 surface and does not contradict
today's code, so the text stays. **M3 decides it**: either the first pass gets exactly one
player-facing line, at load, for a state the player can actually fix — or it goes to the log
with everything else and cap is silently inert on an unclaimed spec. The thing to avoid is
it getting built by default because nobody re-read the sentence.

**Untouched, because it is M3's input rather than a diagnostic:** the whole `ns.Bind.*` read
API, `notify()`/`listeners`, and the readability class-check on read. What M2a killed is the
retain-the-old-id path, not the check — `item.cooldownID` carries no `Secret*` annotation,
so it is class-checked like everything else.

**Verification was static, and honestly so.** luaparser over the three files (the same gate
`wowkb.addon release` runs), a symbol-by-symbol grep for every removed name, and a by-hand
orphan audit — because cap has **no test suite and no `.luacheckrc`**, so nothing would
catch a local whose only reader was deleted. `/addon-review` is clean; its rule-1 ratio
ratchet trips on all three files, which is a deletion-diff artifact (comment lines fell in
every file, code fell faster). Three agents, disjoint files, reviewed together before
anything landed — `Core.lua` deletes `ns.RegisterStatus` and `Bind.lua`/`Frame.lua` delete
its only callers, and **a half-landed pair is a call to a nil global that luaparser will not
catch**. **No release was cut.**

---

## 2026-08-06 — M2a: the four client claims, measured

M2a is done. The four assumptions M2's code was written against went to **ClientLab**,
not to cap, because none of them is a cap question — they are `knowledge/addon-dev/`
questions, and cap growing chat dumps to answer them was the lab-inside-a-product mistake
this milestone exists to correct. One session, one pull, one UI-scale change; all four
drained (OBS-056…059) and all four tests deleted, so the lab is back to 7 built ids.

**Three of the four confirmed the code. One killed a branch.**

- **`item.cooldownID` is never secret.** 26 rows across all four viewers, zero secret
  reads on the field *or* on `item:GetCooldownID()`, across 4 out-of-combat runs and 13
  samples spread through a pull, with the two expressions never disagreeing. The KB row
  said *"can read secret"* and that was inherited, not measured.
  → **`Bind.lua`'s stale-retention branch guards a case that has never been observed.**
  That is a result to act on in M2b, not machinery to keep because it was expensive to
  write. ⚠ It is not *annotated* non-secret, so the class-check on read stays; what goes
  is the retain-the-old-id-because-the-new-one-is-unreadable path and the `unreadable`
  counters that feed it.
- **A hidden viewer still hands back its item frames** — `#GetItemFrames()` equalled the
  pool's active count on all four viewers with all four hidden. And the two aura viewers
  proved the mechanism rather than merely surviving it: their item frames are individually
  *not* shown (1 of 9, 0 of 4) and come back anyway, because every item template sets
  `includeAsLayoutChildWhenHidden`, so the `IsShown` leg of the layout filter never binds
  on a CDM row at all.
  → **`hidden` and `empty` cannot both be read off the row count.** `evaluate()`'s
  `state.frames == 0 → hidden` branch is unreachable-by-construction for the reason it
  thinks: zero rows means the pool is empty, nothing else. Read the viewer's own
  `IsShown()` for hidden, and let the row count mean *configured*. M2b's job.
- **An addon frame under UIParent is unprotected, and stays so.** `false, false` while
  UIParent itself reads `true, true`; re-anchoring it to `ActionButton1` (`true, true`)
  left it `false, false`; and in combat `SetPoint` / `SetScale` / `Show` / `Hide` all
  succeeded. So §1.2's propagation runs *outward from* the protected frame, not inward to
  whatever anchors onto one. `Frame.lua`'s unguarded `SetPoint` in the `UI_SCALE_CHANGED`
  branch is fine.
- **`SetClampedToScreen` is continuous, and applied inline.** A frame parked 120 past the
  top-left corner read `left = 0.0` on the *same frame* as the `SetPoint`, and held `0.0`
  through its own `SetScale(2)` and two UI-scale changes.
  → **`Frame.lua:317-320`'s `--@unverified` comment can go, but so can most of its
  reason for existing**: the engine had already re-clamped before the handler ran, so the
  re-`SetPoint` is re-asserting a position, not rescuing one. Keep it for the *saved*
  position's sake; drop the claim that it is what keeps the panel on screen.

**Process notes, for the next time this shape comes up.**

- **Marking a claim must be line-neutral.** Q1's and Q3's markers went *inside* the
  existing table cell and sentence — nothing validates `questions.json` anchors, and Q3's
  edit sat above 17 of them, two on live `built` rows. Q2 and Q4 needed lines that did not
  exist yet, so the stub came first and the anchors were re-stamped in the same commit.
- **Do not re-stamp anchors by matching text.** Tried it; several §4.2 anchors point at
  *blank* lines, so three of them collapsed onto one. The correct instrument is a
  positional `difflib` line map from the pre-edit file, rebuilt from `HEAD` — and the
  check that it worked is that every anchor still lands on byte-identical text.
- **`needs = "secret"` would have destroyed Q1.** That gate records `skipped` out of
  combat and `skipped` never drains, so the out-of-combat half — which is half the claim —
  would have been unrecordable by construction.
- **One test file per KB topic file, and `T_Frames.lua` had one tenant**, so it and its
  `.toc` line were deleted with the claim. ⚠ `lab.py`'s `lua_ids()` globs `T_*.lua` off
  disk and never reads the `.toc`, so a test file missing from the `.toc` passes
  `deploy --check`, deploys, and never loads. Add and remove the `.toc` line in the same
  edit as the file, every time.

---

## 2026-08-05 — M2 and the catalog, built in parallel

Four tracks run concurrently — three subagents plus the integrator — after checking that
the backlog's apparent M2→M3→M4→M5 line is not the real dependency graph. It isn't: the
**catalog** blocks M3/M4/M5 and needs no addon code at all, and the **movable frame** has no
CDM dependency, so only the CDM binding was ever on the critical path.

**The constraint that shaped the split was the repo, not the work.** Two tracks write Lua
into `addon/`, a separate gitignored git repo, and they share two surfaces no matter how
cleanly the modules divide: the `.toc` file list and `ns.Commands`. So the shared surface
was landed first — `Core.lua` gained **`ns.RegisterCommand{...}`** (replacing the array
literal) and **`ns.RegisterStatus(order, fn)`** (replacing the hardcoded `cmdStatus` body),
after which each module registers its commands and its own `/cap status` line from its own
file and never touches Core. `Bind.lua` and `Frame.lua` were stubbed and `.toc`-listed by
the integrator. ⚠ Worktree isolation would have been **wrong** here — a worktree of the wow
repo does not carry the gitignored addon clone.

**⚠ Nothing built this session has run in the client.** cap **is** released and deployed —
but at **v0.1.1, the scaffold**: the game folder holds `.toc` + `Core.lua` only. `Bind.lua`
and `Frame.lua` exist solely in the working tree, and `ghaddons` installs from the latest
GitHub *release*, so a new cut is what puts them in the game. Every acceptance item below is
unflown, and the gate used was parse (luaparser) plus inspection against
`knowledge/addon-dev/`. *(The project `CLAUDE.md` said "no release has been cut" — stale
since v0.1.1; corrected the same day.)*

**Track A — the catalog gets a shape, and Demonology gets one.** `spec.md` §3.5 now defines
what a spec declares: applies-to, roster, windows, entries, silence, sequences — **data in a
closed vocabulary, not code**. Three devices do the load-bearing work, all aimed at §3.1's
third rule. **Entries cannot see each other** (a condition may name only its own ability,
resources/player buffs and windows — there is no syntax for another entry's tier or
readiness, so mutual exclusion, which is what a priority list is made of, is inexpressible).
**Band conditions are positive** — no negation; a held ability is *promoted* where pressing
it is right and demotes by falling through, forcing the author to name a fight situation
rather than an order. **Cross-ability reasoning happens only in a window**, capped at six and
named after situations. The vocabulary splits into **gates** (branchable) and **channels**
(display-only), which is how Secret Values became structural rather than a discipline:
`impCount >= 6` is not writable as a band condition because the only stack-count term is a
*cue* term. Two things are now checkable rather than hoped-for — **coverage** (every
CDM-tracked row must be an entry or a declared silence with a reason) and the **breadth
measure** (how many entries are HIGH at once).

`specs/demonology/catalog.md` is the first catalog: 9 entries, 5 windows, 4 bars, 11 declared
silences. The APL→tier-field translation is not mechanical and two places show it.
**Implosion can never be HIGH** — its true gate is the sealed Wild Imp count, so the tier says
"the button is up", a threshold cue says "the imps are there", and the player does the AND.
**Dreadstalkers' hold** is two positive windows (`tyrant_setup`, `tyrant_far`) with a
deliberate gap between them, so the hold zone is where neither is true and no band says "not".

**Track B — bound to the Cooldown Manager.** `Bind.lua` resolves the four CDM viewers into
rows keyed by `cooldownID`, each carrying the rule-15 spellID union (base ∪ `overrideSpellID`
∪ `overrideTooltipSpellID` ∪ resolved live id) with the linked pool kept separate, exposed on
`ns.Bind` (`Rows`, `Row`, `RowsForSpell`, `ItemFrame`, `Health`, `Generation`, `OnChanged`).
Rebinds fire on spec, talent, hero-tree, `SPELLS_CHANGED` and the three CDM events, coalesced
through a 0.2 s timer and **refused in combat** — a rebind under lockdown queues and drains on
`PLAYER_REGEN_ENABLED`. The decision that shaped everything else: **a read is three-way, not
two-way.** An *empty* item frame is a real "nothing here" (viewers pad to a minimum of two); a
*secret or throwing* read is "no answer", and a pass containing one is marked incomplete,
retaining the previous rows flagged `stale` rather than dropping them — so a CDM that goes
unreadable leaves cap holding a stale-but-correct binding instead of an empty one. Missing-CDM
states (`no-addon` / `unavailable` / `disabled` / `empty` / `hidden`) announce **once on
transition**, re-arm when the state clears, cap at three per session, and defer five seconds
past login so the async CDM data load cannot raise a false alarm.

**Track C — the movable panel.** `Frame.lua` builds `CombatAssistPlusPanel`, anchored to
UIParent and explicitly *not* to the CDM. `/cap move` toggles placement (out of combat only,
auto-locked on `PLAYER_REGEN_DISABLED` with an in-flight drag stopped and saved cleanly);
`/cap move reset` recentres. Unlocked it shows backdrop, border and label; locked and empty it
has no regions and no mouse, so it is invisible and inert while still present for M4's bars.
Position persists as the panel's centre offset from UIParent's centre **in UIParent units
normalised to scale 1.0** — Blizzard's own Edit Mode form (`EditModeManager.lua:295-320`,
restore at `EditModeSystemTemplates.lua:375`) — resolution-independent because the UI's root
space is a fixed 768 units tall, scale-independent because restore divides by current scale.
Every geometry read is guarded and **refuses to save rather than write an unmeasured number**
(OBS-049: a secret stored in SavedVariables comes back `nil` after `/reload`, so an unguarded
save would silently blank the position). **The frame is deliberately non-secure** — cap never
takes a protected action, protection is one-way and contagious to parents and anchor targets,
and staying unprotected is precisely what will let M4 relayout bars mid-pull. M4's seam is
`ns.Frame.Attach(region, height)` / `Detach` / `Relayout`, with the row height passed in as a
plain number so no bar's secret geometry can reach the container's own size.

**Track D — Cooldown HUD marked superseded.** Banners on `projects/cooldown-hud/CLAUDE.md`,
`docs/status.md` and `docs/multi-class-rollout.md`, and both root-`CLAUDE.md` side-project
entries rewritten. `status.md`'s routing rule ("plan the next cooldown-HUD thing starts
HERE") is **revoked** and its backlog is explicitly no longer a queue; the auto-deploy
exception is dead with the project. The root entry for cap no longer says "what it's for is
deliberately undefined", which was the stalest line in that file.

**Two corrections to our own spec, both found by building against it.**

1. **§3.1's own HIGH example was unimplementable.** "Implosion off cooldown **and** at 6+
   imps" requires branching on a sealed stack count — asserted two paragraphs above the
   section explaining why that cannot be done. Fixed in place, and §3.1 now states the
   tier/cue division explicitly.
2. **§4's Assisted-Combat rationale was factually wrong**, and so is the 2026-08-05 entry
   below that argued it. **Demonic Strength, Bilescourge Bombers and Guillotine are not on
   the Midnight Demonology tree at all** (no row in `all-talents.tsv` @ 12.0.7.67808 — for
   any spec), and **Doom is a PASSIVE** (talent 460551, applied by Demonbolt). So four of the
   five abilities we cited as damning omissions were *correctly* omitted; the list's only real
   omission is Implosion. **The decision to drop the assist stands unchanged** — the shape
   objection (one answer where cap is a field) was always the strong argument and is now the
   stated one. Verified independently by the integrator against `all-talents.tsv`; Implosion
   and Power Siphon are confirmed a CHOICE pair on node 101893, so exactly one exists per build.

⚠ **That correction rests on a claim the KB itself marks unresolved.**
`knowledge/classes/warlock/demonology/abilities.md:89-91` carries the same "not on the current
Midnight Demo spec tree" statement with an **`@verify-ingame`** marker still open. Two
independent sources agree (the DB2-derived talent table and that file), but by the workspace's
own rule a marked claim you are about to build on is a **STOP: ask**. The catalog's three
"not on the spec" silences inherit it.

**Decision, taken the same session and against the catalog as authored: a threshold cue
is drawn in the tier it stands for.** The catalog pass had Implosion's imp count as a
neutral marker beside a MEDIUM icon, with the player expected to AND "the button is up"
against "the imps are there". The author's call: **draw the number in the HIGH treatment**
— the same colour and styling as a HIGH icon — so Implosion simply *reads* HIGH.

This does not relax §5 and does not touch what cap may branch on. The composition is
`ready(this)` (cap's gate, band-legal) → `stacks(Wild Imp) ≥ 6` (the client's threshold,
never seen by us) → drawn HIGH. cap still never learns the count; what changed is that the
**presentation** carries the meaning cap is not allowed to compute, which is move 2 of §1
applied to the register that had been treated as second-class. §3.1 now states it as a
rule: *the two registers differ in resolution, never in vocabulary* — an emphasis that
means HIGH looks like HIGH, whoever did the arithmetic, and the player is never asked to
learn a second visual language.

It also fixes something the catalog had backwards. Implosion's entry justified having no
HIGH partly because a 15s cooldown would leave a HIGH band permanently lit — true of a
*band*, but not of the cue: the imp count crosses 6 in bursts, so a HIGH-styled number
arrives and leaves with the actual opportunity. The cue is the *better* signal here, not
the consolation prize. Two consequences elsewhere: §3.5 gained a **cue honesty** check (a
HIGH cue must carry a gate precondition, or it is permanently lit and reads as "always
press this"), and the breadth check now counts HIGH-declaring cues as HIGH-capable
entries, which takes the Demonology catalog from six to seven.

**Open, and escalated rather than decided:** the **dark field** (Demonology's filler is not
CDM-tracked, so LOW has nothing to draw on and a common state has nothing lit — teach "nothing
lit means go build", or have cap draw its own icons, which is a different addon from one that
rides the CDM); and **target count** (no vocabulary term supplies it, no KB fact establishes
whether it is readable, so every AoE opinion on Demonology is currently unsayable). Both are
now `spec.md` §6. The sequence work is the weakest part of the catalog — the opener was
**deliberately not authored**, because the sources describe it starting with Power Siphon,
which needs Wild Imps you do not have at a pull.

## 2026-08-05 — the tier model replaces the assist, on evidence

§3.1 was rewritten the same day it was written. The verbatim-Assisted-Combat design
lasted exactly as long as it took to read Blizzard's actual Demonology list.

**What killed it.** `raw/addon-research/simc/ActionPriorityLists/assisted_combat/warlock_demonology.simc`
— the in-client Assisted Combat priority list, from the `AssistedCombat*` DB2 tables:

```
summon_felguard (×2) · call_dreadstalkers · ruination · hand_of_guldan
infernal_bolt if buff · shadow_bolt if buff
# "for Blizzard automation, not included in the game's Assisted Combat system":
summon_demonic_tyrant · demonbolt if demonic_core · power_siphon · …
```

The author's worry was that the assist would recommend **Implosion** below 6 imps and
stick there. It cannot: **Implosion is not in the list at all.** Neither are Demonic
Strength, Bilescourge Bombers, Guillotine or Doom. And `hand_of_guldan` carries **no
shard condition**, so a hand-written "MEDIUM when you have the shards" rule is strictly
*more* informative than Blizzard's own line. Under the stricter reading of that comment
(which the destruction and fire files support, though retribution's placement of the
same comment at the top of its list muddies it) the assist also omits **Demonbolt-on-Core
and Tyrant** — which would have shipped a HUD that never highlights Demonbolt on proc,
while §3.2 is a feature entirely about Demonbolt procs. Incoherent either way.

So §3.1 had to change regardless of what replaced it. `[T1: DB2-derived]`

**What replaced it.** The author's own proposal: a **tier signal** — HIGH / MEDIUM /
LOW emphasis across the tracked set, with sequence hints layered on top. Adopted
wholesale, and the assist dropped **entirely** rather than kept as a fallback (the
offered middle option). §6's first open question is therefore answered at M1 instead of
M7, which is what it was written to allow.

The argument that made it more than a preference: **tiers unify §3.1, §3.2 and §3.4 into
one engine at three surfaces.** Smart procs stop being a feature and become an *input*
to the tier; the cooldown bars' urgency treatment is the same signal on a second
surface. That is a real simplification, not a rationalisation of a change already made.

⚠ **The risk it introduces, written into §3.1 as an enforceable rule and into §6 as the
thing to measure:** tiers are a priority list with extra steps *if in practice exactly
one thing is ever HIGH*. Hence the three rules — tiers describe value not order, cap
never ranks within a tier, and a tiering that collapses to one answer per GCD is
mis-designed rather than shippable. M3 carries an item to instrument this.

**The visual vocabulary, and why it has two registers.** Checking the tier inputs
against what the platform allows produced a sharper split than expected:

| Input | Continuous emphasis? | Threshold? |
|---|---|---|
| Soul Shards | ✅ readable *and branchable* — no indirection needed | ✅ |
| Cooldown remaining | ✅ duration object is itself a curve evaluator (§4.8.1 finding 4) | ✅ |
| Proc presence | ✅ presence is readable; only the stack *count* is sealed | ✅ |
| **Wild Imp count** | ❌ **no curve sink exists at all** | ⚠ text only |

So the imp count is the single odd input out. §4.8.2's shipped technique —
`GetAuraApplicationDisplayCount(unit, id, min, max)` quantising in C, empty string below
the threshold — is text-shaped and cannot reach alpha, colour or a bar. Offered
text-as-glyph / napkin-the-count-in-Lua / accept-binary, the author's call was
**glowing text, and "that's plenty signal"**. §3.1 now states both registers and
explicitly forbids contorting the design to make a stack count fade. The napkin-count
idea is parked in the backlog rather than discarded.

**A distinction worth not re-litigating:** `projects/cooldown-hud/specs/demonology/observability-map.md`
calls the imp count *"provably unreadable"* (`imp-side-channel-closed`). That is **not**
in conflict with §4.8.2. It is scoped to reading the count *into Lua to feed a priority
engine*, which remains true. Showing a threshold was never the same question, and the
distinction is the entire basis of this design.

## 2026-08-05 — the spec, and cap supersedes the Cooldown HUD

`spec.md` §1–§5 written from a design conversation. The shape of it, and why each
call went the way it did:

**The origin is a retreat, and that's the point.** CDMProbe started as "what can I
do with the CDM" and evolved into a next-action HUD — a decision engine. Two things
made that untenable rather than merely unfashionable: it runs against Blizzard's
stated position on combat addons, and the 12.0 restrictions had already started
capping what it could calculate. cap is the same premise re-aimed at what the
platform actually invites: **re-present, grade, contextualise** — narrow the
decision, don't make it. The restrictions stop being a wall to route around and
become the design brief.

**Decisions taken (all the author's):**

- **cap supersedes Cooldown HUD.** Not a sibling, not a handoff after the Havoc
  flight — a replacement. CDMProbe's *code* is not carried over; its measured
  client facts are already in `knowledge/addon-dev/` and stay authoritative, and
  its per-spec rotation research is worth harvesting into catalogs. ⚠ The
  cooldown-hud docs and the root `CLAUDE.md` still read as if it's the live CDM
  addon — backlogged, not yet done. **Its outstanding Havoc flight is now moot as a
  CDMProbe deliverable.**
- **Fully fresh code.** No pipeline port. The Coach/Binder/Renderer architecture was
  shaped around authoring a priority answer, which is the one thing cap doesn't do;
  inheriting it would smuggle the premise back in.
- **The assist line is deliberately provisional.** v1 surfaces
  `C_AssistedCombat`'s pick verbatim and cap authors no priority list of its own.
  The author's framing: *play it by ear — start with verbatim, re-approach if that
  plus the other three features still leave me information-starved.* Written into
  the spec as §6's first open question and M7, so it's a scheduled revisit rather
  than a boundary someone has to argue their way past later.
- **Demonology first**, one spec at a time, per-spec catalogs.
- **Procs: replace, don't annotate.** Blizzard's glow gets suppressed and redrawn
  graded, rather than overlaid with a veto mark. One signal, ours, with a fade
  rather than a flip wherever the deciding quantity is continuous.
- **Sequences: auto-detect only.** A manual arm was offered and declined — being
  asked to declare "I am now opening" at the moment you're opening defeats the
  purpose. The cost is accepted false positives, so the spec makes *losing the
  thread silently* a first-class requirement.
- **Cooldown bars: free-floating**, not anchored to the CDM. Place them where your
  eyes already are.
- **Audience: me first, public later.** No settings panel in v1; nothing hardcoded
  so hard that publishing becomes a rewrite.

**The technical ground was checked before writing, and it holds.** The author's
instinct that this would be built on "curves based on secret values" is exactly
right: `security-taint-and-restricted-data.md` §4.8/§4.8.1 records the measured
channels that carry a secret (alpha, vertex colour, desaturation, bar value,
rotation, duration objects), and §4.8.1 finding 3 has a **live in-combat cooldown
bar drawing off a secret duration** already proven on Demonology's Summon Demonic
Tyrant. So §3.4 rests on a measured mechanism, not a hope, and §3.2's graded
fade has a sanctioned route even when the deciding quantity is unreadable.
`C_AssistedCombat.GetNextCastSpell` is measured readable in combat
(`cooldown-manager.md` §7) — with the caveat that its *usefulness* was never
sampled, only its readability.

⚠ **Open risk carried into M3:** the one capture that sampled `GetNextCastSpell`
recorded a constant `691` at every sample and the recorder dedups by readability
class, so nothing yet shows the value tracks the rotation at all. §3.1 assumes it
does. **A value-sampling pass is the first thing M3 should do** — if the oracle
doesn't move, §3.1 has no content and §6's first question gets asked immediately
instead of at M7.

## 2026-08-05 — scaffold

Created the project and the addon repo `michac/cap` from scratch.

- `projects/combat-assist/addon/` — own git repo, gitignored by the wow repo, same
  arrangement as CDMProbe / BucketBinds / PlannerState. Pushed, public, MIT.
- `CombatAssistPlus/` — `.toc` (Interface 120007, v0.1.0,
  SavedVariables `CombatAssistPlusDB`) + `Core.lua`: namespace, a defaults merge on
  `ADDON_LOADED` that fills new keys without clobbering saved ones, and the `/cap`
  router built off an `ns.Commands` schema table with exact-match dispatch and a
  prefix-only "did you mean" (house rule 7 — no substring dispatch). `status`,
  `toggle`, `help`. No combat code, no frames.
- Registered as `cap` in `wowkb.addon` (→ `michac/cap` →
  `projects/combat-assist/addon`, confirm hint `/cap status`) and added to
  `addon-manager/config.json`. `release cap --dry-run` runs clean end to end.
- **No release cut**, so `ghaddons` has nothing to install — the addon is not in the
  game folder yet.

Decision: what the addon *does* was left undefined on purpose rather than guessed
at. `spec.md` §6 carries the open questions.
