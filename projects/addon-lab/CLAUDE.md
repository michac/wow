# ClientLab — the client lab addon (`/clab`)

A long-lived **scratch** addon whose only job is to answer questions about the WoW
client by running one line of Lua in it. It is the home for experimental
API-poking that would otherwise keep accreting inside product addons (it was
accreting inside CDMProbe). Parent program: `todo/addon-engineering.md` (W1); the
durable project doc is `docs/w1-plan.md`.

## The one invariant

**Nothing in a product addon may ever depend on ClientLab.** Not CDMProbe, not
BucketBinds, not PlannerState. ClientLab *reads* the client; it never becomes a
dependency of anything shipped. This is the rule that makes it safe to let junk
accumulate here — a dead test, a wrong guess, a half-built probe costs nothing
because nothing downstream can break. Stated again at the top of `ClientLab/Core.lua`.

## What it is NOT

- **Not a product.** No GitHub repo, no releases, no `ghaddons`, **not** in the
  `wowkb.addon` registry (that registry is the three product addons only).
- No version discipline, no release checklist. `## Version:` in the `.toc` is
  cosmetic — nothing tracks it.
- Tracked in **this** repo at `projects/addon-lab/` (not a gitignored sub-repo).

## Deploy = a directory copy

The whole point of the housing choice: adding a test costs a **copy**, not a
release cut.

```bash
cd ~/code/fun/wow/tools
uv run python -m wowkb.lab deploy          # cross-check the registry, then copy
uv run python -m wowkb.lab deploy --check   # cross-check only, don't copy
```

`deploy` mirrors `projects/addon-lab/ClientLab/` into
`<WoW>/Interface/AddOns/ClientLab/` (deletions included) and, **before copying**,
runs the registry cross-check (below). It reuses `charstate.DEFAULT_WOW` for the
install path, so the `/mnt/c/...` path lives in exactly one place.

## The registry: `questions.json`

`questions.json` is the single source of truth for what the lab tests. Every entry
is `{id, anchor, bucket, question, expect, status}` keyed by a **stable id** — the
join column between the JSON, the `ns.Test{}` records in `ClientLab/T_*.lua`, and
each row of the `runs` capture stream. It is the registry *instead of*
`_meta/verify-in-game.md`: `knowledge/addon-dev/` is firewalled from the game KB, so
its `@verify-ingame` markers are written inside backticks and `wowkb.gen_verify`
ignores them — a documented decision, not a bug (`addon-dev/README.md` §6, which
indexes this file as the fourth queue in §1.2).

⚠ **This is the registry of TESTS, not the record of unknowns.** An unknown lives as a
**marker on the claim** in the topic file — `grep -rn '@verify-ingame' knowledge/addon-dev/`
for the raw count. A question earns a row here when somebody decides to **test** it.

### The unknowns loop — five lines

Full process doc: [`docs/lab-process.md`](docs/lab-process.md).

1. **A marked claim you are about to build on is a STOP** — ask the user. Three answers:
   *assume it* (proceed, and say so in the code), *park it* (leave the marker), *test it*.
2. **"Test it"** = write `ns.Test{}` into `T_<Topic>.lua`, add/flip the row here to
   `built`, promote the marker on the claim to `` `@pending-test: <id>` ``, `lab deploy`.
3. **Nothing is scheduled.** `Autorun` flies every `built` test on the next login/pull —
   writing the test *is* queuing it.
4. **`wowkb.lab show` → `drain <id>`** clears it: `drain` mints the `OBS-nnn` and **REMOVES
   the row from questions.json** (the OBS + git are the archive — no `answered` status is
   kept), then you rewrite the claim, drop `@pending-test`, tag `[client YYYY-MM-DD]`, **and
   delete the test** (house rule 2 — probe code dies in the edit that writes its claim;
   `deploy --check` fails by name until it does). Delete the file and its `.toc` line too if
   that was its last test. **The suite AND the registry shrink as the KB grows.**
5. **Three statuses only:** `built` · `parked` · `not-answerable` (`deploy --check` refuses a
   fourth). A drained question is **removed**, not restatused. Nothing ages an open marker —
   the trigger is **use**, not age. `wowkb.lab blocked` groups the untested rows by the
   capability each waits on.

**`expect` lives only in the JSON and is never compared in-game.** The lab
*discovers* an unknown answer; it does not *assert* a known one (that is what
`wowkb.cdmp` does for CDMProbe). So a test's `run` returns a value and nothing
more, and a **human** reads result-beside-expectation later. An automatic
PASS/FAIL would be the instrument grading its own subject.

**Registry cross-check (both directions).** `deploy` refuses to copy unless every
`status: "built"` question has a matching `ns.Test{}` and every `ns.Test{}` id is a
built question. An unmatched id is a loud error, never a silent skip. A **drained** id
whose test is still in the Lua now shows up as an **orphan** (a Lua id with no `built`
row) and fails **by name** — that is the direction the suite grows back in.

## Test-authoring rules (learned, not optional)

- **Split test files by KB topic file, not by bucket** (`T_Anatomy` ↔
  `anatomy-and-runtime.md`, …). W2's job is "go back to `file:line` and edit the
  claim", so locality to the anchor is what matters.
- **Probe a global by string, never by identifier.** Use `ns.GlobalType(name)`
  (type via `_G` *and* via the addon environment — the two can differ, and the
  difference is sometimes the answer) or `ns.G(name)` (resolve to the value, to
  call it). Bare identifiers would make `luacheck` scream at exactly the code whose
  job is to touch maybe-missing globals.
- **`skipped` is never a pass.** A test whose precondition is unmet records
  `status="skipped"` with a reason and never a value. A test that errors records
  the error *as its answer* (for many questions, "it errors" is the claim). One
  test can never break the run — each is individually `pcall`ed.
- **Never record a value you did not measure.** If the right secret type isn't
  available (row 8 needs a boolean secret; the cooldown source gives a number), the
  test records `measured=false` + why, not a fabricated verdict. This is *the*
  done-criterion — the program doc records two incidents of an instrument emitting
  a confident number it could not observe.
- **…and never record one that two different worlds could have produced.** This is
  the stricter half, and the one that has actually cost flights. `measured = true`
  ends the test for that pull — `Autorun` retries only what declines — so an early
  sample that is merely *ambiguous* is filed as an answer and never revisited. A
  `nil` from an aura nobody applied and a `nil` from a sealed one are the same four
  letters. Before writing `measured = true`, name the other world that produces the
  same bytes; if you can, you are declining. Full rule and the worked case:
  `docs/lab-process.md` §3.1.

## The run loop (in game)

The §4.2 secret table is combat-gated: a genuine Secret Value only exists in
combat (a GCD cooldown read, per CDMProbe's `cooldown-read-combat-seam`).

**The lab runs itself. There is nothing to type.** This addon is only enabled when
someone is deliberately gathering values, so gathering must not cost keystrokes —
and the one window in which the §4.2 secret rows can execute at all is *during a
pull*, which is the worst possible moment to ask a human to type. `Autorun.lua`
watches for the state instead:

```
login          -> settles ~6 s, then runs out of combat
combat starts  -> runs ~2 s in, once cooldowns are actually rolling
during a pull  -> retries ONLY the rows still unanswered, every 3 s, while it lasts
spec/hero swap -> re-runs out of combat (the old rows' stamp no longer describes you)
```

So the whole in-game procedure is: **enable the addon, `/reload`, and go pull
something.** Chat says when coverage is complete.

`/clab` opens the **panel** — the only interface, and the only slash command. Its
buttons are for a moment only the player can recognise (re-run *now*, at this point
in the pull), never for the routine gathering the driver already does.

Runs land in the **`runs` capture stream** (`ClientLabDB.captures.runs`, the house
standard — `references/capture-and-dump-standard.md`), a **ring of 8 sessions**. A
session is one addon load and holds **every** run in it, so an in-combat run no
longer clobbers the out-of-combat one, and each row is stamped with `combat` /
`spec` / `hero` / `instance` at the moment it was taken.

```bash
uv run python -m wowkb.capture clab runs   # → raw/clab-runs.log, one line per row
uv run python -m wowkb.lab show            # result beside expect (no verdict)
```

⚠ `/reload` is still what flushes SavedVariables — but `[copy]` off the dump panel
reads the live ring, so you only reload when you actually want the file on disk.

The pre-standard `ClientLabDB.runs` two-slot store is **gone** (purged on load). Its
last run is archived at `runs/2026-07-24-v0.1.0-legacy.json`, and `wowkb.lab show`
keeps a reader for the old shape.

## Checks

```bash
export PATH="$HOME/.luarocks/bin:$PATH"
cd ~/code/fun/wow/projects/addon-lab && luacheck ClientLab/
```

`luacheck` must be clean with **zero inline suppressions** — fix the code or curate
the `read_globals` std in `.luacheckrc` (the CDMProbe doctrine). The std is kept
short *because* maybe-missing globals are probed by string, not named as
identifiers.

## What is here now

**A `T_*.lua` file holds only what is still OPEN**, so the set of them is a live measure of
what the KB does not yet know — it shrinks with every drain, and a file disappears when its
last question is settled. **As of 2026-08-21 the suite is EMPTY** — the last five files
(`T_CooldownManager` / `T_TargetAuras` / `T_AuraEdges` / `T_AuraFormatter` / `T_AuraPandemic`)
were drained and deleted — which is its correct resting state, not a defect: every question
they held has an answer in `knowledge/addon-dev/` and a `git log` entry. A refilled lab is the
system working. The current set is always `wowkb.lab deploy --check`, never a list here.
```
projects/addon-lab/
  CLAUDE.md            this file
  docs/lab-process.md  THE PROCESS — how an unknown becomes a KB claim
  docs/w1-plan.md      the harness design
  questions.json       THE REGISTRY (open questions only — built/parked/not-answerable)
  .luacheckrc          read_globals curated for the lab
  runs/                archived pre-standard runs (provenance for drained claims)
  ClientLab/
    ClientLab.toc
    Core.lua           namespace, SavedVariables, chat helpers, GlobalType/G, registry
    Capture.lua        VENDORED from CDMProbe — the `<DB>.captures.<stream>` ring
    Lab.lua            ns.Test / stash / ns.Stamp / the runner + the `runs` stream
    Secret.lua         obtain ONE genuine Secret Value; gate needs="secret" tests
    Ask.lua            the eyeball channel — a stimulus and a human verdict
    Report.lua         chat rendering of the last run + the coverage goals
    Dumps.lua          the DUMP PANEL — /clab, [print] and [copy]
    Autorun.lua        the driver: the lab runs itself, nothing to type
    T_<Topic>.lua      one file per KB topic file — NONE open right now (see above)
```

## The panel — `/clab`

**A human-triggered capture is a button, never a slash subcommand** (capture standard
§4, §6). So there is no `/clab run`, no `/clab guide`, no `/clab list` — the driver
covers all of that unprompted, and what remains is three buttons plus `[copy]`.

`[copy]` **reads the in-memory ring**, so an answer leaves the client with **no
`/reload`**. That is the point: a reload ends the pull that made the value secret.

- **`run all tests`** — a re-run *now*, at this instant in the pull. Goes through the
  normal `ns.RunAll()`, so rows land on the `runs` stream too: the bytes a human
  copies and the bytes the extractor reads describe **one** run.
- **`secret probe`** — `ns.GetSecret()` plus its `source`/`why`. When the gate fails
  this is the difference between "14 rows skipped" and knowing why in five seconds.
- **`coverage`** — what evidence is still missing. Every unmet goal names a **game
  situation to get into**, never a command to type.

The panel **refuses to build in combat** (open it once beforehand; it stays usable
mid-pull), its copy EditBox is never a secure frame, and `SetMaxLetters(0)` /
`SetMaxBytes(0)` are called unconditionally. Copy pages at **30,000 chars — a guess
that `OBS-003` owns measuring.** If a payload ever stalls the client here, that is a
measurement: record it in `knowledge/addon-dev/observations.md`.
