# Combat Assist Plus — open discussion

**What this file is for:** topics raised and **not yet decided**. A discussion item is
not agreed work (that's `backlog.md`), not a product decision (that's `spec.md`), and not
a record of what we did (that's `notes.md`). It exists because those three have no home
for *"here is a question that would change the design, and here is the case on both
sides"* — which previously meant such questions either got decided in passing or lost.

**Lifecycle.** An item leaves this file when it is decided: the decision goes to
`spec.md` if it changes what cap should do, to `backlog.md` if it becomes work, and the
reasoning to `notes.md`. Strike it here with the date and where it went. Nothing here
ages, and nothing here is a commitment.

Each item is written to be read **cold**, with no conversation behind it.

---

## Open

*(nothing open)*

Candidates raised in passing and **not** yet written up as items — add them properly if
they start to matter:

- **What is a cue budget?** Tracked as a `spec.md` §6 open question rather than here,
  because it cannot be argued in the abstract — it needs a drawn catalog.

---

## Struck

### D3–D6 — the founding rules, re-read

**Raised:** 2026-08-07 · **Struck:** 2026-08-07 — **decided together, and the answer was
smaller than any of the four items assumed.**

The four were written as separate questions about separate rules. They were answered as
one, because the diagnosis underneath them was the same: **the rules had multiplied past
what they were protecting.** Each was individually defensible and the set had become a
governance apparatus written before a single pixel was drawn — much of it there to keep cap
visibly distinct from CDMProbe rather than to make cap good.

**The decision: cap's mission is three statements, and everything else is downstream.**

- **a)** cap does not fight the secret restrictions. The gate/channel split already
  expresses this and is the one line worth enforcing in code.
- **b)** cap freely uses non-secret information to give good hints.
- **c)** cap does not try to *always* present a single best decision. That is distinct from
  "never present a single decision" and from "always present several options of equal
  status". Sometimes one option genuinely is best and the game hands us the data to say so
  — show it, without stress. Same for the inverse: sometimes nothing is good, and that is
  also a thing to show.

**What each item resolved to:**

- **D3 — narrow, and narrower than the item's own "narrow".** The broad reading was already
  dead: §3.3's primary/secondary step hints are a literal next-action answer. But the narrow
  reading's *"cap's output is a field"* framing was itself part of the problem — it is (c)
  overstated into a requirement. §3.1's third rule ("if exactly one thing is ever HIGH the
  tiering is wrong") is replaced by (c). §4's bullet is restated to the real anti-goal: cap
  does not reduce to a bare flag on the next button with no *why* and no *what else*. The
  Assisted Combat justification changes from "one answer where cap is a field" to **cap did
  not author it and cannot grade it** — which is the honest reason and survives the
  reframing.
- **D4 — the debate was hair-splitting and is dropped.** Its hypothetical (a hundred
  client-evaluated comparisons whose composite tells you what to press) is a strawman: if
  displaying available data clearly reads as an instruction, the UI has been fixed, which is
  (b). Legitimacy shrinks to (a) and stops being a veto with a test. No test for "defeats
  the intent" is sought, because the thing it was hunting is not a failure mode.
- **D5 — moot.** It asked for a threshold on the HIGH-at-once distribution. Under (c) there
  is nothing for a threshold to enforce. The distribution survives as a **reported
  statistic with no pass/fail** — the instrument for saying *why* something felt wrong in
  play, not a gate.
- **D6 — the cull went further than the item proposed.** Checks 2, 3, 8 and 9 are deleted
  outright rather than demoted to disclosures. Five survive, and every one is either schema
  integrity or principle (a): 1 coverage, 4 register legality, 5 declared subjects, 6's
  mechanical half (a cue declares polarity / its tier / a precondition — fields the renderer
  needs filled in; the "strict enough" judgement half goes), 7 estimate disclosure (it names
  the places cap guesses at a number the client would state exactly, which is (a)'s own
  to-do list).

**And the process change that came with it, which matters more than the cull.** The rules
were reverse-engineered from nothing. **Ship the tier/cue system, play with it, refine until
it feels good, then reverse-engineer the rules from that for the second spec.** Drawing
jumps the queue ahead of the documentation migration.

Reasoning: `notes.md` 2026-08-07 (second entry). Work: `backlog.md` → **the rule cull**.

### D1 — Can a channel select between BANDS, by driving alpha on two rendered treatments?

**Raised:** 2026-08-07 · **Struck:** 2026-08-07 — **decided, and then overtaken.**

**Decision:** *no* to the literal proposal — a channel may not select a band, and
channels stay out of band conditions entirely. Landed as `spec.md` §3.5's register
legality check.

But the item's real content was *"cross-ability facts should reach the player through
the client rather than through cap's arithmetic"*, and that **was** adopted, in a larger
form than D1 proposed: cues gained polarity, gained arbitrary subjects, and took over the
job windows were doing (D2). So D1's mechanism was rejected and its argument won.

Three things worth keeping from the analysis:

- **The route it proposed was a detour.** `Region:SetAlphaFromBoolean(v, aTrue, aFalse)`
  and `SetVertexColorFromBoolean` do the job in one call with less surface than the
  `C_CurveUtil.EvaluateColorValueFromBoolean` pair it sketched, and `SetVertexColorFromBoolean`
  needs one region rather than two stacked, which removes the combinatorial objection.
- **Its cost #2 was the decisive one and it is permanent.** A secret-driven rendering has
  no readback, so cap can never learn what appeared. Accepted rather than solved — see
  `notes.md` 2026-08-07 for why that is the right call.
- **Its claim to retire O2 was overstated at the time and then came true anyway.** O2
  needed the *window* to use an exact cooldown, which a channel could never do. Deleting
  windows retired it instead.

Reasoning: `notes.md` 2026-08-07. Spec: §3.1's two registers, §3.5's cue declaration.

### D2 — What problem does the window mechanic solve?

**Raised:** 2026-08-07 · **Struck:** 2026-08-07 — **answered, and the answer was that it
does not solve one.**

The item's own answer — *"a window is a budget for cross-ability reasoning"* — was
correct about what the mechanism **did** and wrong about whether it was needed. Its two
live sub-questions ("is six right?", "`opener` spends a slot on nothing") were both
symptoms of a mechanism nobody could size, and both dissolved with it.

What the analysis missed, and what decided it: **every window read something cap could
already see.** The budget therefore constrained *expression*, not capability, while
pushing authors toward cap's own arithmetic in exactly the places the client would have
answered exactly. `cores_dry` is the worked example — it needed a window because one
entry may not name another, not because the proc was unreadable.

**Decision:** windows deleted. Bands may name any declared ability through the gate
vocabulary; the guard against a priority ladder moves from syntax to the HIGH-at-once
measurement.

Reasoning: `notes.md` 2026-08-07. Spec: §3.5 "Entries, bands and cues". Work: the
Demonology catalog migration, `backlog.md` → `Now`.
