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
the on-disk run under `ClientLabDB.runs`. It is the registry *instead of*
`_meta/verify-in-game.md`: `knowledge/addon-dev/` is firewalled from the game KB
and 64 of its 68 markers are backticked, so `wowkb.gen_verify` reports zero
addon-dev items — a documented decision, not a bug (see `addon-dev/README.md` §6).

**`expect` lives only in the JSON and is never compared in-game.** The lab
*discovers* an unknown answer; it does not *assert* a known one (that is what
`wowkb.cdmp` does for CDMProbe). So a test's `run` returns a value and nothing
more, and a **human** reads result-beside-expectation later. An automatic
PASS/FAIL would be the instrument grading its own subject.

**Registry cross-check (both directions).** `deploy` refuses to copy unless every
`status: "built"` question has a matching `ns.Test{}` and every `ns.Test{}` id is a
built question. An unmatched id is a loud error, never a silent skip.

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

## The run loop (in game)

The §4.2 secret table is combat-gated: a genuine Secret Value only exists in
combat (a GCD cooldown read, per CDMProbe's `cooldown-read-combat-seam`).

```
/clab run            (out of combat — secret rows record `skipped`)
/clab guide          (what coverage is still missing; pull-based, re-type to re-check)
pull a target dummy
/clab run            (in combat — the secret rows fire)
/reload              <- NOT optional; SavedVariables only flush on reload/logout
```

The run lands at `…/WTF/Account/<ACCT>/SavedVariables/ClientLab.lua` under
`ClientLabDB.runs.ooc` / `.combat`.

## Checks

```bash
export PATH="$HOME/.luarocks/bin:$PATH"
cd ~/code/fun/wow/projects/addon-lab && luacheck ClientLab/
```

`luacheck` must be clean with **zero inline suppressions** — fix the code or curate
the `read_globals` std in `.luacheckrc` (the CDMProbe doctrine). The std is kept
short *because* maybe-missing globals are probed by string, not named as
identifiers.

## Scope of pass 1 (this build)

Harness + record format + the 15 call-and-record questions + the 14-row §4.2 secret
table = ~29 tests. Everything else — the 7 container/TOC questions (need generated
sibling addons, **W1d**), the 3 not-answerable, buckets 2/3 (scratch-frame, XML,
animation, event, lifecycle), and the ~11 unmarked `[gap]` candidates — is recorded
in `questions.json` with the appropriate `status` and **not built**. See
`docs/w1-plan.md` for the full scope split.
```
projects/addon-lab/
  CLAUDE.md            this file
  docs/w1-plan.md      the durable project doc
  questions.json       THE REGISTRY
  .luacheckrc          read_globals curated for the lab
  ClientLab/
    ClientLab.toc
    Core.lua           namespace, SavedVariables, chat helpers, GlobalType/G, registry
    Lab.lua            ns.Test / stash / the runner + result envelope
    Secret.lua         obtain ONE genuine Secret Value; gate needs="secret" tests
    Report.lua         chat rendering of the last run + /clab guide
    T_Anatomy.lua      tests, ONE FILE PER KB TOPIC FILE
    T_ApiEvents.lua
    T_Libraries.lua
    T_Module.lua
    T_State.lua
    T_Security.lua     the §4.2 14-row secret-op table
```
