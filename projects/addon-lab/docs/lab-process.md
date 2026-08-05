# The lab process — how an unknown becomes a KB claim

> The durable one-pager. `docs/w1-plan.md` owns the harness design and `docs/w2-answer-pass.md`
> records the pass that proved the machinery works; neither is restated here. This is the
> **process**, which is the part that was missing once the machinery worked.

## 0. The reframe

The registry is **not** "understand everything possible about the client" — that is
unbounded by construction. It is **"understand how to implement our addon."**

So the trigger for testing an unknown is **use, not time**. Someone needs the answer to
write code; until then the question sits in the topic file as a marker and costs nothing.
It must be cheap and blameless to write down *"not sure, haven't needed this"* — and
impossible to build on that claim later without noticing.

**Only two things may never accumulate:**

| Never | Why | What stops it |
|---|---|---|
| a **measured answer** that has not reached the KB | the answer exists and nobody can find it — this once stranded 15 answers for 12 days | `wowkb.obs check` (14 days / 12 open) |
| an **unverified claim silently relied upon** | code written on a hypothesis that reads like a fact | the marker sits **on the claim**; the rule is **ask** |

Everything else — open markers, `[gap]` annotations, untested rows — may pile up
harmlessly. They are a **catalogue**, not a backlog. There is deliberately **no clock, no
cap and no release gate** on an open question; adding one would recreate the guilt-backlog
this process exists to remove.

## 1. The marker is the mechanism

**An unknown is recorded on the claim, in the topic file. Not in a tool.** An agent reading
`cooldown-manager.md` meets the marker in the prose it is already reading, at exactly the
moment it matters. A tool that re-derives that list is a step somebody has to remember —
and a step somebody has to remember is a gate that fails silently.

Three states, and they are the whole lifecycle:

| Marker | State |
|---|---|
| `` `[gap]` `` · `` `[unverified]` `` · `` `@verify-ingame` `` | **open** — nobody is on it |
| `` `@pending-test: <id>` `` | **in flight** — a `ns.Test{}` with that id is in ClientLab and flies on the next login/pull |
| `[client YYYY-MM-DD]` | **measured** — drained, marker gone, claim rewritten |

Markers here are written **inside backticks** so `wowkb.gen_verify` leaves them out of the
game KB's checklist (`addon-dev/README.md` §6 — a firewall, not a bug). Nothing harvests
them and nothing needs to.

## 2. Meeting one

**A marked claim you are about to BUILD ON is a STOP.** Not one merely nearby — one your
code would rest on. Surface it: name the claim, say what is unverified, and let the user
pick.

| They say | You do |
|---|---|
| **assume it / guess** | proceed — and say so **in the answer and in the code**, so the assumption is visible where it will bite |
| **park it** | leave the marker (add one if the hole has none) and move on |
| **test it** | §3 |

**Never assume silently, and never quietly go build a test instead of asking.** Both
substitute your judgement for a call that is the user's, and the second one is the sneakier
failure: it looks like diligence and it spends a play session.

## 3. "Test it" — four steps, no ceremony

1. Write `ns.Test{ id = … }` into `ClientLab/T_<Topic>.lua` — the file named for the KB
   topic file the claim lives in. (Split by topic file, not by bucket: the eventual job is
   "go back to `file:line` and edit the claim", so locality to the anchor is what matters.)
2. Add its row to `questions.json` as `built`, or flip an existing `parked` row. Not
   bureaucracy — `deploy --check` refuses to copy unless **every test has a row and every
   row has a test, both directions**. An id with no row would emit a value nobody expects;
   a row with no test is a silent hole in coverage.
3. **Promote the marker** on the claim to `` `@pending-test: <id>` ``.
4. `uv run python -m wowkb.lab deploy`.

**There is nothing to schedule.** `Autorun.lua` runs every built test on the next login,
again ~2 s into combat, and retries the still-unanswered ones every 3 s while the pull
lasts. **Writing the test is queuing it.** The whole in-game procedure remains: enable the
addon, `/reload`, go pull something.

## 4. Clearing one

```bash
cd ~/code/fun/wow/tools
uv run python -m wowkb.lab show            # result BESIDE expect — no verdict, by design
uv run python -m wowkb.lab drain <id>      # mints OBS-nnn, sets `answered`
uv run python -m wowkb.obs drain OBS-nnn   # after the topic file is edited
```

`show` never prints a PASS/FAIL: that would be the instrument grading its own subject. A
human reads result beside `expect` and decides. `drain` then prints the edits it cannot
make for you — rewrite the claim in place, **drop `@pending-test`**, tag
`[client YYYY-MM-DD]` (the date of the *run*, not today), **delete the test**, then close
the observation.

A test that flew and could not answer (`skipped`, `measured = false`) **keeps its marker**
and flies again next pull. `drain` refuses those loudly — skipped is never a pass, and
declined is never a pass either.

### The suite shrinks as the KB grows

**Deleting the test is a required step, not tidying.** It is house rule 2 — *probe code is
deleted in the commit that writes the KB claim it produced* — applied to the lab, and
`deploy --check` fails by name until it is done. Delete every declaration of that id, and
the file plus its `.toc` line if it was the last test in it.

The rule this replaced kept an answered test *"to re-check the answer on a later patch"*.
Nothing ever re-checked one: `show` refuses to print a verdict by design and `drain`
refuses an answered question, so a regression could not have been noticed — it was a
capability with no mechanism, costing run time during every pull and burying the open
questions in `show` output. **Patch-day re-verification is owned elsewhere**, by
`<version>-ptr-heads-up.md` and the `/update` sweep, which name the exact lines that go
false.

What survives is the `answered` row: the question, the `expect`, the method, the run, and
the `OBS-nnn`. That is the recipe if a patch ever makes the question worth re-asking, and
it is cheaper to keep than the code.

Adopting the rule swept **32 answered questions** out at once — 57 registered ids down to
**25**, with `T_Module.lua` and `T_CooldownManager.lua` deleted entirely because every
question they held was settled.

## 5. The four statuses

| status | means | test required | gated |
|---|---|---|---|
| `answered` | measured, drained, KB rewritten | **no — the test is deleted with the claim** | `deploy --check` fails if one lingers |
| `built` | a `ns.Test{}` exists; flies next pull | yes | reported by `deploy --check` |
| `parked` | written out, nobody is testing it | no | **never** |
| `not-answerable` | no instrument can settle it; the reason is in `expect` | no | no |

`deploy --check` refuses a status outside these four — the collapse from six only holds if
nothing can re-introduce a seventh.

⚠ **A `parked` row is not required for an unknown to be recorded.** A bare marker on a
claim is a perfectly good parked question. Rows exist where the reasoning was worth keeping
— what would settle it, what it is waiting on.

**`blocked_on`** names what a question waits on, as a **capability** rather than a task,
because many rows share one blocker:

```bash
uv run python -m wowkb.lab blocked
```

reads the residue as *~7 missing capabilities* (a sibling-addon generator, XML authoring in
the lab, a desktop file read, a second client, a boolean-valued secret, LibStub, a secret
that is a valid atlas name) rather than *20 stuck questions*. `null` means nothing is
missing — it simply has not come up.

## 6. What is enforced, and what deliberately is not

**Enforced**

- `wowkb.obs check` — a measured answer must reach the KB.
- `wowkb.lab deploy --check` — registry ⇄ Lua, both directions, plus the status vocabulary.
- `wowkb.kblint` · `luacheck` with **zero inline suppressions**.

**Deliberately not**

- **Any count or age of open markers.** No clock, no cap, no release gate.
- **Any tool you must run before writing code.** The marker is in the prose; requiring a
  command to re-derive it adds a step and a thing to forget.
- Anything that would make writing down an unknown feel like incurring a debt.

## 7. Known residue

- **Anchors drift.** A row's `<file>:<line>` moves under an edit and nothing validates it.
  The `id` is the durable key; treat a stale anchor as a lint finding, not as evidence the
  question is gone. An anchor validator in `deploy --check` is the fix (`_meta.anchor_drift`
  records the same).
- **Most markers in the topic files have no registry row**, and that is correct rather than
  a leak: a question earns a row when somebody decides to test it. Two different things
  wear a `[gap]` — *"I looked and it isn't there"* (a real question) and an epistemics
  warning against a tempting inference (*"that absence is weak evidence, not proof"*, which
  is prose doing its job). Only the first is ever worth a row.
