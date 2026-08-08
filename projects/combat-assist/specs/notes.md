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
