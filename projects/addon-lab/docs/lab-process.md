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
lasts. **Writing the test is queuing it.** ⚠ But *"still unanswered"* is decided by the
test itself, and getting that wrong is the one way to waste a flight — **§3.1**. The whole in-game procedure remains: enable the
addon, `/reload`, go pull something.

### 3.1 The one rule that decides whether a flight is wasted

**`measured` is not a description of the run. It is the scheduler.**

`Autorun` re-runs a test only while it declines. `runOne` sets `declined` from
`value.measured == false`, `ns.Unanswered` collects the declined, and the 3 s ticker
re-runs exactly those. So the moment a test returns `measured = true` it **leaves the
unanswered set and is never sampled again for that pull**. There is no second chance and
no warning; the log simply contains one early sample, rendered as an answer.

The trap is that an author writes `measured` meaning *"did I get data?"* while it means
*"is this run over?"*, and those come apart precisely when a test fires before the game
reached the state it was written for.

> **The rule: return `measured = true` only when the observation could not have been
> produced by the world where nothing has happened yet.**

The worked example, and the reason this section exists — twice:

```
C_UnitAuras.GetUnitAuraBySpellID("target", 383344)  -->  nil
```

Two worlds produce that. **The DoT is not on the target yet** — sample again in three
seconds. **The seal hides it** — the finding we flew for. Same four letters. A test that
calls the first one an answer records "unreadable" for an aura nobody had applied, and it
will never look again.

So before writing `measured = true`, name the other world that produces the same bytes. If
you can name one, you are declining:

```lua
return { measured = false, why = "every candidate returned a bare nil — indistinguishable "
  .. "from 'no DoT applied yet'. Cast Blade of Justice and stay in combat." }
```

⚠ **A refusal IS an answer.** An error, a `SecretArguments` rejection, a Precondition
firing — those distinguish the worlds and should be recorded as measured, not retried. The
rule is about ambiguity, not about failure.

⚠ **`why` is read by a human deciding whether to re-fly**, so it names the state that was
missing and how to reach it. "no target" is a status; "target a dummy and stay in combat"
is a next action.

### 3.2 The traps this lab has actually hit

Not general Lua advice — these each cost a flight or a wrong claim, and they recur.

- **`x and y or z` returns `z` when `y` is legitimately `false` or `nil`.** Every guarded
  read in a test is exactly this shape, and `false` is exactly what half of these tests are
  trying to observe. **Write the branch out long.** Hit twice, most recently reporting a
  colour as *readable* — the leak result — because the method was absent and
  `not IsSecret(nil)` is `true`.
- **Do not sample `list[1]` and report on it.** A permanent override, a first aura, a first
  frame: whatever sorts first will win every run, and the test silently answers a narrower
  question than its `id` claims. Report every element, keyed by name.
- **A control that can only return one value is not a control.** Probing a *target* debuff
  against the *player* returns `nil` forever and proves nothing. Discover a subject at
  runtime that the control can actually succeed on, and record "inconclusive" when you
  cannot — never a nil dressed as a comparison.
- **Read the code that emitted a log before believing the log.** An absent record proves
  nothing until you know the emitter could have written it. A capture stream whose writer
  only runs out of combat cannot evidence anything about combat, and its silence is not
  data.

### 3.3 `phase` — two fields, one name, and most values inert

⚠ There are **two** unrelated `phase` fields and neither does what its name suggests.

| Where | The only value that does anything | What it does |
|---|---|---|
| `ns.Test{ phase = … }` (the record) | `"roundtrip"` | `Report.lua` flags a round-trip whose read-back never landed. |
| the **returned table**'s `value.phase` | `"read-back"` | `runOne` marks this run as the one that recovered a payload. |

Every other value of either is **inert**. `phase = "combat"` looks like scheduling and is
not — scheduling comes from `measured` alone (§3.1). Leave `phase` unset unless you mean
one of the two values above.

## 4. Clearing one

```bash
cd ~/code/fun/wow/tools
uv run python -m wowkb.lab show            # result BESIDE expect — no verdict, by design
uv run python -m wowkb.lab drain <id>      # mints OBS-nnn, REMOVES the row from questions.json
uv run python -m wowkb.obs drain OBS-nnn   # after the topic file is edited
```

`show` never prints a PASS/FAIL: that would be the instrument grading its own subject. A
human reads result beside `expect` and decides. `drain` then prints the edits it cannot
make for you — rewrite the claim in place, **drop `@pending-test`**, tag
`[client YYYY-MM-DD]` (the date of the *run*, not today), **delete the test**, then close
the observation.

**Drain REMOVES the row; it does not restatus it to `answered`.** questions.json is a live
worklist of OPEN questions only — it shrinks on drain exactly like the `T_*.lua` files do.
The `OBS-nnn` the drain minted (observations.md) plus git together hold the question, its
`expect`, the run and the verdict, so a retained row would only duplicate them. There is no
`answered` status.

A test that flew and could not answer (`skipped`, `measured = false`) **keeps its marker**
and flies again next pull. `drain` refuses those loudly — skipped is never a pass, and
declined is never a pass either.

**A visual question is closed by a HUMAN — through either channel.** The recorded panel
click (`/clab` → visual checks) is one; `drain <id> --verdict '<what you saw>'` is the
other, for a verdict the author states in prose. Both mint the same eyeball evidence class;
a recorded click wins over `--verdict` when both exist, because the click is bound to the
exact stimulus text and prose is not. The click-only rule was dropped 2026-08-24, when the
author had stated a verdict — with a screenshot — and the tool was refusing it over which
surface the words arrived on. What never changed: no programmatic run closes a visual
question, and `--verdict` on a non-visual question is ignored.

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

What survives is the **`OBS-nnn` entry** (plus git): the question, the `expect`, the method,
the run and the verdict, with its drains-to anchors. That is the recipe if a patch ever makes
the question worth re-asking — a richer record than a kept questions.json row, which merely
duplicated it. So the row is **removed** on drain, not retained; the OBS is the archive.

Adopting the rule swept **32 answered questions** out at once — 57 registered ids down to
**25**, with `T_Module.lua` and `T_CooldownManager.lua` deleted entirely because every
question they held was settled.

## 5. The three statuses

| status | means | test required | gated |
|---|---|---|---|
| `built` | a `ns.Test{}` exists; flies next pull | yes | reported by `deploy --check` |
| `parked` | written out, nobody is testing it | no | **never** |
| `not-answerable` | no instrument can settle it; the reason is in `expect` | no | no |

There is no `answered` status: a drained question's row is **removed** (its OBS + git are the
archive), and its test is deleted with the claim it produced — so a test left behind shows up
as an orphan in `deploy --check` (a Lua id with no `built` row) and fails by name, which is the
direction the suite grows back. `deploy --check` refuses a status outside these three.

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
