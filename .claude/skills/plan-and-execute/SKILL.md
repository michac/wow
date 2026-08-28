---
name: plan-and-execute
description: >-
  Write a plan good enough that another agent could execute it, have it reviewed once, then
  decide whether to hand it off or do it yourself. INVOKE DELIBERATELY — this repo's
  CLAUDE.md points here — for substantial multi-step work: a change spanning several
  documents that must agree, work that asserts facts which will later be cited or built on,
  or a task where being wrong is expensive to discover later. Also invoke mid-change on
  discovering the work is much bigger than it looked. Do NOT invoke for questions, ordinary
  single-file edits, or anything an existing test or gate fully covers — most work does not
  need this, and running it on small changes is the failure mode to avoid.
---

# Plan and execute

> **A good plan is one that another agent could execute for you.**

That is the standard, and it applies **whether or not you actually delegate**. A plan you
could not hand off is a plan still half-living in your head — which is exactly the part that
gets lost when you are wrong.

## The sequence

1. **Write the plan by hand.** Not a subagent's job. This is the judgment.
2. **One adversarial review.** One. See §3 for the cap and its one escape hatch.
3. **Revise.**
4. **Now decide: delegate or execute yourself.** Not before — you cannot size the work
   honestly until it is planned.
5. **Accept from the diff, never the summary.**

## 1. Before you start: is this actually plan-shaped?

If a single gate, test, or typecheck fully covers the change and it touches one file, **stop
and just do it**. Invoking this skill for a typo or an icon registration is the failure mode.

Say the verdict in one line and move on: `Plan-shaped: three docs must agree and the gates
cannot see a wrong claim.`

## 2. Writing the plan

Template: `references/plan-template.md`. The test for every section is the motto — *could
another agent act on this without asking me a question?* Non-optional:

- **A "how to read this plan" header** saying guidance markers (⚠, notes to the executor) are
  instructions and **must never be transcribed into the output**. Without it, executors paste
  your warnings into the deliverable.
- **Name the silent failures** — anything that can go wrong while every check still passes: a
  duplicate id shared by two sibling keys, an edit landing on the wrong one, a generated file
  not regenerated. Give the **assertion that proves it went right**, not just the instruction.
  Loud failures need no warning; silent ones are the whole risk.
- **Exact verification commands**, copy-pasteable, with the baseline: *"currently 0 failures,
  must stay 0."* An executor cannot recognise a pass without it.
- **Explicit out-of-scope**, including the adjacent things a reasonable agent would be tempted
  to fix.
- **"Re-verify this yourself"** on every load-bearing claim, naming the source. Tell the
  executor not to trust the plan. **Plans are wrong** — this repo has the receipts.
- **Line numbers are pre-change hints.** Say so; require a re-grep.

Write plans as files in the scratchpad, one per work item. Revise in place, mark the revision,
and state that earlier revisions are superseded.

## 3. The single adversarial review

**Reviewers must RUN things, not reason about them.** Ask for a simulation: copy what is
needed to a throwaway tree, apply the change, run the real gates. *"This looks consistent"* is
worth almost nothing; *"I applied it and gate X fails with this message"* is the product.

Require a verdict with acceptance criteria — **READY FOR HAND-OFF, or NOT with the specific
blocker** — or the loop has no terminator.

**One review. The only escape hatch:** if you *dispute* a blocking finding, verify it yourself
with fresh evidence — re-run the query, read the source, check the data — and say plainly
whether you overturned it or it stood. Do not spend a second review round on a disagreement.
⚠ And re-check your own rebuttal: being right once does not make you right.

## 4. Delegate or execute yourself

Now that the plan exists, decide on what it turned out to be:

**Delegate** when execution means reading many files (context you do not need to keep), when
it is mechanical once planned, or when it is long. Pass the plan **by path, never pasted** —
the subagent reads it fresh and your context does not carry it twice. Restate only the
silent-failure traps in the prompt; do not assume the plan is read carefully.

**Execute yourself** when it is short, when it needs a voice or taste you would have to
over-specify, or when you expect to iterate as you go.

## 5. Accept from the diff

A summary states intent; the diff is the effect. **Run the gates yourself** rather than
trusting reported output, and read the inserted text for the exact failure modes the plan
warned about. This step is cheap and it has caught something nearly every time.

Report what shipped, what the gates say, which judgment calls the executor made, and what it
found that the plan got wrong. If a reviewer or executor corrected you on something
substantive, say so once — it tells the reader how much to trust the result.
