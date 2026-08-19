# House rules for addon code

Read this before writing addon Lua. `SKILL.md` carries these as one-liners; this is the
full text and the reasoning. `/addon-review` checks them mechanically.

Every rule here exists because its absence cost this workspace something specific. Where
that is true the receipt is named, so you can judge the rule rather than obey it.

---

## 1. Comments say what the code does now

**The test that decides it:** *if a comment would still be true after you deleted the code
it sits on, it is KB material, not a comment. If it says what the code used to do, it is
git history, not a comment.*

- **≤ 6 lines per block. ≤ 10 for a file header.** Longer means you are writing a doc —
  write the doc.
- **Banned in comments, no exceptions:** dates, version numbers, `Phase N`, "used to",
  "was wrong", "corrected", "this replaced", "until X this said". That is a changelog, and
  `git log -p` already has it, indexed and never stale.
- **A fact about how the game behaves does not go in a comment.** It goes in
  `knowledge/addon-dev/observations.md` in the same edit. Leave at most a one-line pointer:
  `-- readability rules: see api-events-and-discovery.md §2.8`.
- **Two things earn a comment that reads like prose**, and only these:
  (a) an ordering or invariant an editor would silently break — one line, plus the name of
  the test that pins it; (b) a `--@unverified` marker (rule 5).
- **Ratio:** a file you create or substantially rewrite lands at **comment:code ≤ 0.35**.
  A file you touch may not *increase* its ratio. This is a ratchet, not a gate — no
  CDMProbe file passes 0.35 today and a hard gate would block every commit.
- **Deleting a comment that contains a fact is a bug.** The fix is always *move it*.

**The receipt.** CDMProbe ships 7,911 code lines and 8,321 comment lines. 263 blocks carry
a history marker and, being the long ones, account for 52% of all comment lines. One
measured in-client fact — that `ChargeGained` fires on any upward move of the cached count,
not once per charge — lived *only* in `State.lua:377` and would have died with the file.

---

## 2. Probe code has an expiry date

A **probe** is code whose purpose is to answer a question, not to serve the user. Every
probe is born with three things:

1. **It lives in `<Addon>/probes/`.** A folder, not a naming convention — `ls probes/` is
   the inventory and cannot drift.
2. **A machine-readable header:**
   ```lua
   --@probe
   -- question:  does C_AssistedCombat.GetNextCastSpell() return a readable spellID in combat?
   -- opened:    2026-07-31
   -- expires:   2026-08-14
   -- lands-in:  knowledge/addon-dev/api-events-and-discovery.md §2
   --@endprobe
   ```
   `expires` defaults to opened + 14 days, and is the only date allowed anywhere in addon
   source.
3. **Its `.toc` lines sit under `# --- probes (delete on close) ---`,** last, so the diff
   that removes them is obvious.

**Answering the question obligates deletion in the same commit.** You may not write the KB
claim without deleting the probe that produced it — the reward is coupled to the cost.

**Deletion is five items**, and skipping them is how 4,070 dead lines accumulated:

- [ ] the `.lua` file
- [ ] its `.toc` line
- [ ] its capture stream **and** its `DEFAULTS` entry
- [ ] its spec under `tests/probes/`
- [ ] its Python extractor / grader subcommand

**Who removes it:** the agent that reads the answer out of the capture. Not "someone later".

**Probes get no baggage.** A probe may not be built on another probe, may not add a field
to a shipped data structure, and may not add a subcommand to a shipped command. If a probe
discovers a reader a permanent consumer will want, **promote the reader out first** —
CDMProbe did this correctly three times (`ns.ReadValidAlertTypes`, `ns.ClassOf`,
`ns.ReadCooldownDuration`), and that precedent is the rule.

**The receipt.** `Core.lua:50` still describes a SavedVariables key as *"Read by
`wowkb.cdmp rtfx`"*. That reader was deleted 2026-08-02. The key is still seeded on every
login, nothing writes it, nothing reads it, and the comment is the only thing keeping it
alive.

---

## 3. One capture path

Every recorder writes to `<DB>.captures.<stream>`; every extractor is
`wowkb.capture <addon> <stream>`. Full contract: **`capture-and-dump-standard.md`**.

- `ns.Capture.Open(name, {sessions, cap, dedup})` — `sessions` and `cap` are required.
  **Nothing is unbounded.**
- `:Line` for a greppable trace, `:Row` for a grader, `:Mark` for an edge.
- **Lines are pre-rendered strings and that is a one-way door.** Anything you might later
  want to slice by — combat state, spec, hero tree — must be a `:Mark` **now**. No
  extractor change can add it to a capture already on disk.
- **`:Mark` sits above the dedup.** A transition the log exists to record must not be
  conditional on something else changing.
- **No game value reaches a line except through `Capture.Safe()`**, which returns a
  readability class, never a raw secret.
- **No colour escapes inside a line.**

**The receipt.** Before the standard: 7 top-level stores, 4 retention policies, 3 output
destinations, and four near-identical loaders in `cdmp.py`. A missing combat marker made a
21,048-line capture unreadable for its own acceptance question and cost a re-fly.

---

## 4. Dumps are buttons, not commands

Any "give me a dump at this moment" is `ns.Dumps.Register{id, label, blurb, capture}` on
the `/<addon> dump` panel. Press it mid-pull — no typing, no macro.

- The panel's list view shows each capture with a distinguishing blurb and a `[copy]`.
- **`[copy]` reads the in-memory ring**, so no `/reload` and no hunting through
  SavedVariables for the right entry.
- It rides the **same stream shape as rule 3**, so `wowkb.capture <addon> dump` still works
  and the agent path is untouched.
- **WoW has no clipboard API.** Copy-out is a multiline `EditBox` → `SetText` →
  `HighlightText()` → `SetFocus()`, leaving the text selected for Ctrl+C. Call
  `SetMaxLetters(0)` and `SetMaxBytes(0)`; page large payloads.
- The panel **must refuse to create in combat**, and its EditBox must never be a secure
  frame.

**The receipt.** `AlertTape.lua:220-224`: *"an earlier cut printed it to chat only, which
was useless: WoW's default chat frame has no copy/paste, so the one output that has to
reach the analysis machine was the one output that could not leave the client."*

---

## 5. Shipped, probe, archived — location is the marker

**Do not build a verified/experimental annotation system.** Per-function markers are prose,
prose drifts, and rule 2's receipt is what drift looks like. `ls` cannot lie:

| Location | Means |
|---|---|
| `<Addon>/` | shipped — load-bearing for a user |
| `<Addon>/probes/` | experimental, dated, expires, deleted on answer |
| `<Addon>/archive/` | retired, out of the `.toc`, out of luacheck, out of your greps |

**The one exception**, because it is per-claim rather than per-file:

```lua
--@unverified napkin fallback fires when base cooldown reads a LIE (Havoc, 3 buttons)
```

`--@unverified` is the code-side twin of the KB's `@verify-ingame`: a path whose *game
behaviour* has never been observed. **Every one must appear in the current flight's
acceptance set.** An unverified path nobody is going to fly is either dead code or a lie
you have not caught yet.

Explicitly rejected: a `VERIFIED = {…}` manifest, confidence levels in comments,
per-function decorators.

---

## 6. Test pure logic; do not test the client

**The rule, stated so it is decidable:** *if the assertion's truth depends on a fake you
wrote of an API you have never called, delete the test.* It is a model of your belief. It
will stay green while the belief is wrong, and its greenness is worse than nothing, because
it will be cited as evidence.

**Test:** pure functions of plain data — the Coach, priority lists, State's roster seams,
the Binder's resolution, the napkin's arithmetic, a log's record/render split.

**Do not test:** anything whose answer is "what does the client do".

Two patterns already right in this workspace, and doctrine everywhere:

- **A contract suite is authored from the KB, never from the module under test.**
  `fixtures/cdm-cases.lua` is authored from `cooldown-manager.md`, and a meta-test *forbids*
  a case's `ref` pointing at `State.lua`. A suite transcribed from the source is a
  change-detector wearing a contract's clothes.
- **A suite 100% green against current code is by construction a snapshot.**
  `status = "pinned-defect"` cases assert the contract answer and **fail on purpose**, so
  the fix flips its own case green in the same diff.

**Probes get honesty tests only** — that *our* code degrades correctly when the namespace
is absent, the call throws, or the return is secret. That is about our behaviour under
refusal, not about the API. **Cap: 8 tests, in `tests/probes/`, deleted with the probe.**

---

## 7. Commands come from a schema table

The model is BucketBinds `Core.lua:210`: one table of `{name, args, desc, handler,
complete}` that drives help, did-you-mean, tab-complete and the console dropdown for free.

- **Never hand-roll argument parsing.**
- **Max depth `/<addon> <verb> [<arg>]`.** `/cdmp curve stack dur test 30` is the failure
  mode: 19 invocations, 4 tokens deep, behind a recursive-descent parser whose ordering
  hazards are documented in-code *because they were bugs*.
- **No substring dispatch.** `rest:find("on")` also matches `"sound on"` —
  `HudDriver.lua:512` documents that exact collision, and the same pattern is live in five
  commands.

---

## 8. A discarded error is a fabricated result

`pcall` is unavoidable here — the client refuses calls, and a refusal must not take the
addon down. But `pcall` converts *"the game said no"* into *"nothing happened"*, and those
two are the same shape in every downstream reader. Every rule below is one incident.

**8.1 One `pcall` per call you want to distinguish.** Wrapping a sequence in a single
`pcall` and discarding `err` means any member failing looks like all of them silently doing
nothing:

```lua
-- WRONG: a rejected filter and an empty target are now indistinguishable
pcall(function()
    container:AddAuraGroup("row", "HARMFUL", options)
    container:SetUnit("target")
    container:UpdateAllAuras()
end)
```

Each call gets its own `pcall`, and the first failure is **kept and surfaced** — into the
panel, the capture, or the return value. Group calls only when you genuinely do not care
which one failed, and say so in a comment.

**8.2 `x and y or z` is not a guard.** It returns `z` whenever `y` is `false` or `nil` — and
`false` is exactly what a readable-vs-secret probe is usually trying to observe:

```lua
-- WRONG: reports "readable" for a value it never read, because
-- `obj.Get and obj:Get()` is nil when the method is ABSENT, and `not IsSecret(nil)` is true
local readable = obj.Get and not IsSecret(obj:Get())
```

Absent, refused and present are three answers. Write the branches out; give each its own
word.

**8.3 A `nil` return is two worlds until you prove otherwise.** At 12.1 a Precondition with
`FailureMode = "ReturnNothing"` returns *no values*, which is byte-identical to "the thing
you asked about does not exist" (`security-taint-and-restricted-data.md` §4.7). Before
recording a `nil` as a finding, name the other world that produces it and rule it out with a
second instrument — the one that *errors* rather than the one that goes quiet.

**8.4 `type()` does not screen out a secret.** It returns the **real** type, so
`type(v) == "table"` passes for a secret table and the next index raises, discarding whatever
you had already collected. Class-check first (`issecretvalue` / `issecrettable`), then branch.

**8.5 A UI that can render nothing must render why.** An empty panel is a bug report with no
information in it. If a region can legitimately be empty, it says which — *"built ok, nothing
matched"* versus the refusal text, in different colours. Blank is never an outcome.
