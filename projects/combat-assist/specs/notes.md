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
  quotation of our own prose is the one thing it cannot afford. (A real defect, twice — see
  the 2026-08-10 §3.1 cull entry.) If the text was only ever in a working tree, describe the
  edit instead. ⚠ **This does not cover primary sources** — what a player said in play, a
  flight report, an observation. Those are evidence, they were never in git and never should
  be, and quoting them verbatim is the point: paraphrasing a player's words into our own
  vocabulary is how a report becomes a conclusion.
- **Status does not live here.** Where the code is, what has flown, what the live version is:
  `backlog.md` → `## Status`, and nowhere else.
- ⚠ **A fact about how the game or the API behaves does not stop here.** That goes to
  `knowledge/addon-dev/` (see the wow-developer skill) — this file records *our* work, not
  the client's behaviour.
- No busted/luacheck counts, no mutation lists, no comment:code ratios, no "considered and
  declined". Cut the argument that `spec.md` and `discussion.md` already carry.

**The standing order is `simplify → draw → add detail from play`.**

---

## 2026-08-11 — the small pilot replaced the tier engine

**What changed.** The approved Phase 3–5 migration replaced the ten-entry tier/cue catalog
with two enhanced entries and two readable dependencies. The source moved to unknown-safe
signals, a static border, two fixed Tyrant context dots, stock-glow coexistence and one
independent Tyrant bar. Tests split into engine guarantees and provisional Demonology
characterization, and the capture guide was reduced to the fields the new source emits.
`Catalog.lua`, `Catalogs/Demonology.lua`, `Signal.lua`, `Track.lua`, `Treatment.lua`,
`Sense.lua`, `Overlay.lua`, `Bars.lua`, tests, `demonology/catalog.md`, `flight-reading.md`.

**Why it still binds.** The implementation enforced the safety line from `spec.md` §3.5
without enforcing the removed tier, silence, cue, sequence or visual-policy doctrine. A
readable-only marker became a first-class output and mutable gameplay examples stopped
masquerading as universal engine guarantees.

**Caveat.** The new pixels had not been installed or flown. Their colors, geometry,
stock-glow coexistence, marker usefulness and the bar's value remained Phase 5 judgments.

## 2026-08-11 — the product returned to §1

**What changed.** The simplification audit completed and the author approved its recommended
A1–G1 direction. `spec.md` was rewritten after §1 around one static emphasis, readable-first
context markers, an optional sealed display path, no automatic sequences, one independent
Tyrant-bar experiment and a Demonbolt/Tyrant pilot. The backlog and discussion were reduced
to the migration work and genuinely open play questions; both repository instructions now
point to the backlog instead of restating status. `spec.md`, `backlog.md`, `discussion.md`,
both `CLAUDE.md` files, `demonology/catalog.md`, `simplification-audit.md`.

**Why it still binds.** Existing code and tests were no longer accepted as justification for
product rules. The surviving enforceable boundary was readable facts may drive Lua while
sealed facts may only feed client-owned display sinks; gameplay and visual choices returned
to provisional hypotheses judged through play.

**Caveat.** This round changed documentation only. The addon still implemented the old model
until the rewritten spec passed its checkpoint and Phase 3 migrated source.

## 2026-08-11 — the capture read: the tier signal is saturated

**What changed.** The v0.2.4 `draw` capture was interpreted — one Demonology pull, a 700.7 s
combat window, 169 in-combat change-lines, read **time-weighted** rather than by line count.
No code was touched. Five findings came out and each went where it bears: `discussion.md`
D14, D7, D12, D15 and D17, plus three new items at the top of `backlog.md` → `Now`.

**Why it still binds.**

- **The pull was saturated, and that is what *"too flickery"* was describing.** Two or more
  entries were HIGH for **74.8 %** of it against M3b's 16 %, something was HIGH **87.4 %** of
  the time, and five of the eight entries held one tier unbroken for **500–545 s** of 700.
  Nothing receded; the only moving part on screen was the pulse, on everything, at once. D14's
  candidate faults — the trough, the rate, the `ADD` blend, the base alpha — all sit
  downstream of that, because what the reading found was the catalog's bands being satisfied
  near-permanently. ⚠ It did not clear any of them; it said fixing them alone could not have
  fixed the complaint, and that a brighter ring on that screen would have made it worse.
- **A change-line log is not a duty cycle, and three documents had been reading it as one.**
  The raw counts these files carried — 82/29 on E8's cue, 106/79/13 on E3, 198 of 199 — are
  lines of a deduped stream, so a state that changed twice and lasted ten minutes counted the
  same as one that flickered twice in a second. Time-weighting moves them a long way: E8's cue
  read 82/29 by line and **81.9 %** of the pull by time. That is why the rule about
  interpreting a capture once now sits in `flight-reading.md` rather than being remembered.
- **The graded register was nearly inert, and the cause sat in the catalog rather than in the
  treatment.** HIGH sat at exactly its ungraded midpoint for about **95 %** of its occupancy,
  because E3 declares no grade and E1's and E2's name `cooldownRemaining(this)` — a channel,
  which cap by construction cannot read, so nothing it says could ever reach an alpha cap
  writes. MEDIUM did vary, on the two entries grading on `shards`. D7 predicted exactly this
  from the code on 2026-08-08; the pull measured it rather than argued it.

**Caveat.** ⚠ Two halves of this are answerable by no capture, and were written as such:
whether E8's **marker** appeared is the client's half of D12, decided from a count cap never
learns; and `glow:` counts the frames it hooked rather than the dim it performed, so D17's two
surviving causes cannot be separated by another flight — what is owed there is a counter on
the dim itself, which is the `nosize:` defect a second time.

## 2026-08-10 — FIRST PIXELS: v0.2.4 flown, and four things play said that the desk could not

**What changed.** cap drew on screen for the first time: v0.2.4 released and deployed, one
Demonology pull. Everything from M3c onward — the graded register, the cues, the proc-glow
dim and the bars — had been built, reviewed four times and never executed in the client. It
works; the player's verdict was *"hey it works!"* before any of the detail. Four things play
reported, all filed as `discussion.md` **D14–D17**: the tier glows read as candles (too
flickery, wanted brighter); a transformed row (Grimoire: Imp → Consume Magic) stays
emphasised for its whole cooldown because `ready(this)` reads true; Tyrant's HIGH promotion
is wrong and should be MEDIUM with markers; and the stock proc glow was **not** suppressed.

**Why it still binds.** Three things, and they outlast the build they were learned on.

- **A flight that measures a rule firing correctly says nothing about whether the rule is
  right.** E1's HIGH promotion (`ready(this) and not ready(E2)`) was a desk decision; the M3b
  flight measured it landing within 2 s of the Dreadstalkers cast and recorded it as working
  — and it *was* working, in the only sense that instrument could test. Play reversed it
  anyway. **No instrument in this project can close that gap**: `busted` tests the arithmetic,
  the capture tests that the arithmetic reached a pixel, and neither has an opinion about
  what the arithmetic should be.
- **The restraint on the KB paid.** The proc-glow dim recipe was filed as blocked on the
  flight rather than drained into `cooldown-manager.md`, because it was read off CDMProbe's
  source and never measured by us. The flight then showed the dim does not work here. Had it
  been written as a `[client]` claim on faith, the KB would now carry a broken mechanism and
  the next project would inherit it.
- **The flush rule earned its place in the procedure.** A capture only reaches disk on
  `/reload`, so a flight ending without one leaves the log describing the *previous* build —
  a reading that would then have been taken as a null result. This pull did end in one; what
  came out of it was that the ordering was worth writing down rather than remembering, and it
  now lives in `flight-reading.md` and the skill's `capture-and-dump-standard.md`.

**Caveat.** ⚠ **This entry is the player's report, not the measurement.** The pull was also
captured, with a complete `# combat start` → `# combat end` window, and every word above was
written before anyone opened it; it was read the next day and the entry above it carries what
it said. Nothing was decided here: all four went to `discussion.md` with the case both ways,
because three have a genuinely open *how* even though the *what* is settled.

## 2026-08-10 — the cooldown bars (M4a)

**What changed.** §3.4's bars, built in the panel that already existed: one duration bar per
catalog roster entry, the remaining time drawn by the client off a duration object and never
entering Lua, §3.1's tier signal on the fill. The roster was overturned on the merits — E4
Summon Doomguard out (it binds to no row, so its bar would draw nothing), E8 Implosion in
(once the rotation is rolling the imp count saturates and the 15 s cooldown is what gates the
press). `Bars.lua`, `Treatment.lua`, `Catalog.lua`, `Catalogs/Demonology.lua`, `Sense.lua`,
`Overlay.lua`, `spec.md` §3.4, `catalog.md` §1/§4, `discussion.md` D12/D13,
`tools/wowkb/addon.py`.

**Why it still binds.**

- **A bar's tier is nil for exactly the stretch the bar is useful.** Every band on E1/E2/E3
  requires `ready(this)`, so an ability on cooldown has no tier — and that is precisely when
  its bar has something to show. The bar is therefore a surface in its own right: it counts
  down regardless, and the tier colours it when there is one.
- **A picked number went in dressed as a derivation, and that is what this round cost.**
  `BAR.rest`'s first value was justified by an analogy to the *none* veil — two different
  composites — was promoted into `spec.md` as a normative number, and was then pinned by a
  test that made the analogy the only thing holding it. It also collided with LOW's own alpha
  band. What actually followed from a surviving property was only an **ordering**: a bar has
  no ring, so the fill is the only carrier of the LOW → *none* step, and the resting fill
  therefore had to read under LOW's dimmest. The value inside that bound was relabelled a
  **pick**, and `spec.md` §3.4 now states the property and carries no numbers — which is where
  the rule about picked-versus-derived lives, not here.
- **Two declarations of one fact drift.** The roster was declared three times — `catalog.bars`,
  a per-entry `bar = true` flag the loader actually *refuses*, and a column in `catalog.md`
  §1 — and they already disagreed. Reduced to one: §4's ordered list, because order is part
  of the declaration and a flag carries no order. Two load-time checks now refuse both halves
  of the drift.

**Caveat.** The hold cue on a bar was deferred rather than half-built; D12 (is E8's cue lit
nearly all the time?) and D13 (the resting fill and track colour) are open on a look.

## 2026-08-10 — the §3.1 cull

**What changed.** A targeted cull of §3.1's normative surface assertions, with one test
applied to every one: *which principle is this downstream of?* Three struck outright, two
narrowed to the half that traces to a principle, and LOW's ring returned to the lab-measured
`0.50` (band `0.36 – 0.50`) once the rule that had pushed it down was gone. `Treatment.Rank`
was added at the same time. `spec.md` §3.1/§6, `Treatment.lua`, `Overlay.lua`,
`treatment_spec.lua`, `discussion.md` (D10 updated, D11 opened).

⚠ **Struck vocabulary — none of it is current, and it is named here only as the record of
its removal:** the ladder being *monotone* in brightness and in pulse rate, each tier owning
a *disjoint* brightness band, a marker having a *fixed place* with two of them, *a positive
cue is not a second visual language*, the shared-row pick taking the *brighter of the two*,
and the greyscale / colour-blind defence. Do not carry any of it forward.

**Why it still binds.**

- **Each replacement names its root.** The ladder is *ordered* (§3.1's own first sentence:
  three emphasis levels are levels or they are three colours); a grade moves an entry only
  inside its own tier's range (§3.0's Grade); cap's emphasis must be **distinguishable** from
  the stock proc glow (§1's move 2) — strictly weaker than forbidding Blizzard's art, which is
  why the ring's atlas was left alone and the question went to D10.
- **The one thing the cull broke, and the four lines that fixed it.** "Brighter" and "higher
  tier" were the same sentence only because of the struck band rule; with it gone a graded LOW
  can out-brighten a dim MEDIUM, so the shared-row pick could draw the lower tier.
  `Treatment.Rank` makes the comparison tier order first, emphasis only inside one tier.
- **LOW's 0.50 is the only LOW alpha anybody has ever looked at**, chosen on a real spell icon
  at true CDM size; the number that displaced it came out of the struck rule's own arithmetic.
  Restoring it puts the measured number back and moves the unmeasured question to a look (D11).

**Caveat.** ⚠ This entry, as first written, was wrong twice. It claimed two deleted tests still
passed; one was **red**. And it quoted struck `spec.md` text that `git` cannot show — §3.1's
treatment subsection had never been committed. Both corrected in place; the deletions were still
right, and the reason matters: **the tests went because the rule they assert is gone, not to
make the suite green.**

## 2026-08-10 — the measured restyle

⚠ **SUPERSEDED:** LOW's band was set to `0.22 – 0.36` here; the §3.1 cull put it back to
`0.36 – 0.50` the same day. Everything else in this entry stands.

**What changed.** A ClientLab picker put candidate treatments on real spell icons at true CDM
size and a person chose. The ring is Blizzard's own `UI-HUD-ActionBar-Proc-Loop-Flipbook`
played as a flipbook, `ADD`, at 1.4× the icon; all three tiers wear it and are separated by
hue, alpha and pulse rate (2.5 / 1.2 / 0.5 Hz); *none* keeps the only veil. LOW lost its veil
and gained a ring, which is the substantive change. `Treatment.lua`, `Overlay.lua`, `spec.md`
§3.1/§6.

**Why it still binds.**

- **The pulse and the tier alpha are one channel**, so the tier's alpha is baked into the
  animation endpoints rather than wrapped in a second frame — which means the pulse re-arms
  whenever tier or grade moves, and **one function owns the write**: `Stop()` restores whatever
  the group last captured, so an alpha written outside `armPulse` is clobbered a line later.
  The ring also needs its **own host frame** one level below the overlay, because a frame alpha
  multiplies its children and would otherwise pulse the veil and both markers too.
- **A `D{}` counter exists so a flight does not need the eyeball; a paragraph telling the
  pilot to go and look is the counter's absence with extra steps.** The review fix pass found
  that a refused `GetWidth` left the ring unsized and unshown while every number in the log
  read healthy — a totally blank pull byte-identical to a working one. That is now `nosize:`,
  not prose. Same round: the per-row phase offset became a fraction of the row's own cycle,
  because a flat offset aliased rows back into alignment on the fastest tier.
- **The pick collided with a rule and the rule lost.** §3.1 forbade reusing Blizzard's
  proc-glow art and the chosen ring **is** that sheet. The rule was rewritten to require
  distinguishability instead — but at a desk against no pixels, so the argument is held open as
  `discussion.md` **D10**. If they read as one thing the fix is one string.

**Caveat.** The FlipBook setter names turned out to be Tier 1 in the generated docs, but an
XML attribute name is not a Lua setter name, so all three are probed by name and a miss falls
back to the four-quad ring and reports which method was absent.

## 2026-08-10 — the proc-glow suppression

⚠ **SUPERSEDED in effect: the dim does not work.** The first flight found a proc'd icon still
at full volume (`discussion.md` **D17**), so the mechanism below is the one that was built and
not one that is known to function. The reasoning about *why* it was shaped this way still
binds; the claim that it suppresses anything does not.

**What changed.** `Glow.lua`: a per-instance post-hook on each CDM item frame's
`RefreshOverlayGlow` that sets `item.SpellActivationAlert:SetAlpha(0.5)`. That is the whole
mechanism, and it closes the *replaces the stock proc treatment rather than adding to it* half
of `spec.md` §3.2. Plus `Glow.Restore()`, which puts every hooked alert back to full alpha
when cap goes dark. Two lines in `Sense.lua`, one `draw` field in `Overlay.lua`, one `.toc`
line.

**Why it still binds.**

- **The four shape decisions, three of which are constraints rather than choices.** The alpha
  goes on the alert *frame*, never its child textures (the proc animation drives the
  children's alpha, so a write there loses every frame). A per-instance hook, not one on the
  shared mixin table (the methods are `Mixin()`-copied per frame, so a table hook misses every
  frame that already exists — which at bind time is all of them). A dim, not a hide (hiding is
  protected and blocked in combat). And it rides `Sense`'s existing frame walk, which already
  owns the weak-keyed hook-once-per-frame-object-ever table this needs.
- **An idempotent write is not a free one when the surface is shared and the clock is 10 Hz.**
  `Restore` shipped without the liveness guard `light()` had, so while cap was dark it wrote
  `SetAlpha(1)` onto every hooked alert ten times a second, indefinitely — which contradicts
  §3.5's *no catalog, nothing at all* and stomps any other addon's suppression precisely while
  cap is doing nothing.
- **The three "why" claims above are read off CDMProbe's source and are measured nowhere.**
  They were written as provenance in the comments rather than asserted as facts, and the KB
  drain was filed as blocked on a flight rather than done on faith. ⚠ **That is the whole
  reason the negative result cost nothing.** Note the trap it creates: forbidden from filing
  a claim, the natural move is to assert it in a comment instead, where nothing lints it.

**Caveat.** ⚠ The `.toc` order turned out to be load-bearing and nothing tests it. `Glow.lua`
was placed before `Overlay.lua` so its verdict listener registers first; the other order made
`glow:` report the liveness of the pass before it. The invariant itself sits on the `.toc`
line in the addon, which is the only place that can enforce it.

## 2026-08-08 — M3c and M3d: the graded register, then the half cap is not allowed to compute

**What changed.** M3c: `Treatment.lua` (pure — tier → look, and the only place the visual
numbers exist), `Overlay.lua` (impure — cap's own frames), `Sense.OnVerdicts`, and the `draw`
capture stream. M3d: `Channel.lua` — the two sealed comparisons, a three-way stack quantiser
and a `Step` curve evaluated by a duration object — plus `Treatment.Ink`, two marker slots per
row and `C{}` on the `draw` stream. And the **polarity rule was struck** from `spec.md` §3.1
and from two module headers, reopening `discussion.md` **D8**.

**Why it still binds.**

- **cap draws its own frames, parented to `UIParent` and only ever *anchored* to the item
  frame.** The CDM rewrites a tracked icon's colour constantly, so anything cap writes onto
  Blizzard's texture is stomped within a frame or two; an addon frame parented to `UIParent`
  reads unprotected even when anchored to a protected one, which is what makes
  `SetPoint`/`Show`/`Hide` legal in combat. The paint path writes only those plus
  `SetVertexColor`/`SetAlpha`, so everything geometric happens at construction.
- **Ungraded is the *midpoint* of a band, not its top.** The alternative makes every ungraded
  entry outshine every graded one at the same tier, which reads as "no grade means maximum
  urgency". Six of Demonology's ten entries are ungraded, so this is most of what is on screen.
- **A cue is a two-part statement and neither channel has a readback.** cap decides whether one
  is *offered*, the client decides whether it *appears*, and `SetText`/`SetAlpha` hand nothing
  back. So a log can prove the mechanism is wired and can never prove a marker appeared — and a
  threshold that fires at the wrong moment reads exactly like one that fires correctly in every
  instrument cap owns. M3c therefore drew **no** cue rather than painting one from the offer.
- **A cull can *add* a rule, and anything a cull introduces deserves the same test it applies
  to what it removes.** *"Polarity is carried by shape — press and hold may never differ only
  in hue"* entered in the **rule cull**, whose entire purpose was cutting rules back to §1's
  three principles. M3c then implemented it, wrote it into §3.1's treatment table and restated
  it in two module headers, so within a week an unargued visual preference had three
  independent-looking sources and read as settled.

**Caveat.** M3d's two-viewer tie-break (lowest cooldownID among the aura rows) is a read-side
rule only and deliberately stays out of `spec.md` — the *draw* is on the entry that owns the
cue, so the ambiguity cannot reach a pixel.

## 2026-08-08 — the window migration: the code caught up to the spec

**What changed.** `spec.md` deleted the window catalog mechanic on 2026-08-07 and the code
kept speaking it for a day. Gone: the window vocabulary and its cap, the `window` gate, the
`remaining` term, `Track`'s window machinery, and `catalog.md` §2 in full. Arrived: subjects
on every gate term, negation in a band, `combat` promoted into the gate set, `e.cues` as a
list with polarity and a channel, and **check 3 (declared subjects)**. `Catalog.lua`,
`Track.lua`, `Sense.lua`, `Catalogs/Demonology.lua`, `catalog.md`.

**Why it still binds.**

- **It added no capability and that was the point.** Every fact the old catalog knew, the
  migrated one knows; what it bought is that whatever goes on screen next is the model we are
  keeping. Two exact reads replaced one estimate: E1's band became
  `ready(this) and not ready(E2)`, which reads *long*, and a negative cue at
  `cooldownRemaining(E2) ≤ 8` trims exactly that tail — arithmetic the client does.
- **`not ready(E1)` in E2's cue precondition is load-bearing.** A ready Tyrant has a
  zero-remaining cooldown, which clears any `≤ t` threshold, so without it the hold marker
  would be pinned on through the entire setup — precisely the stretch where Dreadstalkers
  should be pressed. ⚠ `t = 20` is imprecise and is filed as `catalog.md` **O8**, not glossed:
  the real hold zone is `12 < remaining < 20` and the channel table offers one upper threshold.
- **Narrowing applies-to is worse than losing a band.** Adding the apex talent to E5's
  applies-to would make cap draw *nothing at all* on a build without it (§3.5, "no catalog,
  nothing at all"), so the band went instead; what it cost is `catalog.md` **O1**.
- **Check 3 polices the *form* of a subject per term, not merely its membership.** A term read
  off a bound row names an **entry**; a term about an aura names an **aura spell id**. A
  wrong-form subject is not a stricter spelling of the right one — it type-checks, passes all
  five checks, is then permanently *unknown* for the life of the build, and gate health reports
  "nothing refused" because the read was never asked for at all. Related and easy to miss:
  `Catalog.Reads` keys reads by **subject**, because `not ready(E2)` inside E1's band is a read
  of E2 and tallying it against E1 reports a working catalog as blind.

**Caveat.** One correctness bug rode along because it was in the same function: `Resolve`'s
`match()` keyed on `e.spell` alone, so E3 dropped silently on half of all builds.

---

**Before 2026-08-08, nothing is recorded here.** The scaffold through M3b, the rule cull and
the deletion of the window catalog mechanic all argued in a vocabulary the window migration
above removed, and re-carrying it is how a deleted mechanic comes back.

Anything from that period that still binds is already in `spec.md`, `discussion.md` or the
entries above. If you need the original 18 entries:
`git show a33e152:projects/combat-assist/specs/notes.md`.
