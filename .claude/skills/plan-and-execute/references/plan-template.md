# Plan template

Copy the shape, not the words. Delete sections that do not apply — an empty section is noise.

---

```markdown
# Plan — <work item> (rev N)

Rev N follows <what changed and why>. Earlier revisions are superseded; do not carry
anything forward from memory of them.

## ⚠ HOW TO READ THIS PLAN

**Every ⚠ here is guidance to YOU, the executor. None of it is text to transcribe into the
output.** Some ⚠ notes are phrased as assertions ("⚠ Do not write X") — they are instructions
about what to avoid, not content.

## The defect / the goal

What is wrong or missing, stated precisely enough to be falsifiable. Quote the offending
text or name the exact symbol. If the change rests on a fact, cite its source here.

## Scope

What is in. What is deliberately out, including the adjacent things a reasonable executor
would be tempted to fix. If a scope boundary was *established* by a search, say what was
searched — a future reader needs to know how much the boundary is worth.

## The change

Numbered, per file. For each:
- exactly what to add, change or delete
- ⚠ anything that can go wrong SILENTLY here, and the assertion that proves it did not
- ⚠ where a naive edit lands wrong (sibling keys with the same name, duplicate ids,
  generated files that must be regenerated)

## ⚠ Re-verify these yourself

The claims the change rests on, with the command or file that establishes each. **Do not
take this plan's word for them.** Plans are wrong; this one may be.

## Verification — run these and report FULL OUTPUT

    <exact commands>

Baseline: <what a pass looks like today>. It must still be that.

⚠ If a check fails, fix your own work. Do not weaken the check, do not special-case the
subject, do not edit the tool to make it pass.

## Report back

1. Diff per file.
2. Full output of each command.
3. <the specific assertion(s) that prove the silent failures did not happen>
4. Judgment calls you made.
5. Anything in this plan you found wrong or ambiguous.
```

---

## Executor prompt

Pass the plan **by path**. Restate only the traps:

```
Execute a written plan exactly as specified. Repo root: <path>
THE PLAN: <absolute path>

Read the ENTIRE plan first, including the "HOW TO READ THIS PLAN" block — every ⚠ is
guidance to you and must NOT appear in the output.

<Restate the 1-3 silent-failure traps here. Do not assume the plan is read carefully.>

Match the existing voice and density of each file you touch.

Run and report FULL OUTPUT of: <commands>
If a check fails, fix your own work — do not weaken it.

Report: diff per file · full command output · <the proving assertion> · judgment calls ·
anything in the plan that was wrong.

Do not commit. <Other hard limits.>
```

## Reviewer prompt

```
Adversarially review a plan against the repo. DO NOT EDIT ANY FILE. Report findings only.
THE PLAN: <absolute path>

The author has been wrong on this before — verify, do not assume.

SIMULATE IT. Copy what you need to a throwaway tree, apply the change, and RUN the real
checks. "Looks consistent" is not the product; "I applied it and gate X fails with <message>"
is.

Check: <the specific claims>, whether any check will fail that the plan does not mention,
whether a fresh agent could execute it unambiguously, and anything the plan asserts that is
simply wrong.

End with a prioritized list of required changes and a verdict: READY FOR HAND-OFF, or NOT
with the specific blocker.
```
