# W1 — ClientLab, the lab addon

> **STATUS: PLANNED (2026-07-23).** Nothing built. Parent program:
> `todo/addon-engineering.md`. This doc owns W1 only; W2 (run it, read it, update
> the KB) and W3/W4 stay in the program doc.

## Context

`knowledge/addon-dev/` was built entirely from source-reading and documentation.
Its own README §6 leads with the limitation: **nothing in it has been run in the
client.** The subtree carries **137 `[gap]` markers** and **68 `@verify-ingame`
markers**, and the answer to a large fraction of those is one line of Lua executed
in a live client.

Separately, experimental API-poking has been accreting inside CDMProbe — a product
addon — because there was nowhere else to put it. ClientLab is that place.

W1 builds the instrument. It does **not** answer the questions (that is W2), and it
deliberately builds only the cheapest third of them first, because the record format
is the thing most likely to be wrong and the cheapest way to find out is one in-game
run.

## What exploration established (read before designing anything)

Three findings that the program doc gets wrong or does not mention:

1. **The addon-dev marker backlog is invisible to `wowkb.gen_verify`.** That tool
   deliberately ignores a marker written inside `` `backticks` `` (prose vs. live
   marker — `gen_verify.py:43` `_strip_code`). **64 of 68** addon-dev markers are
   backticked, so `_meta/verify-in-game.md` lists **zero** addon-dev items.
   *Decision: leave it that way.* `README.md:33-37` sets a hard firewall between
   the game KB and the addon-dev subtree, and dumping 45 engineering questions into
   the game-side verify checklist (currently 29 items) breaks it. `grep -rn
   '@verify-ingame' knowledge/addon-dev/` still works. The registry becomes
   `questions.json` (below), keyed by a stable id rather than by marker text.
   **Deliverable: record this as a decision** in `knowledge/addon-dev/README.md`
   and in `gen_verify.py`'s docstring, so the gap is documented rather than silent.

2. **The program doc's "three competing `reset` registrations … two are dead by load
   order" is wrong.** The line numbers are right; the reading is not. It is a
   deliberate decorator chain — `Probe.lua:664` defines the base, `Resource.lua:282`
   and `HudCore.lua:690` each capture `ns.commands.reset.fn` as `prevReset` and call
   it, and `.toc` load order *is* the composition order. `ns.RegisterCommand`
   (`Core.lua:76-79`) only appends to `commandOrder` on first registration, so one
   help entry results. Nothing is dead. Of the "458 retired lines", only
   **`HudTint.lua` (72 lines)** is genuinely dormant; `Skin.lua` (90) and
   `Resource.lua` (296) are retired *directions* but are loaded, referenced from
   four call sites, and reachable. **Deliverable: correct that paragraph in
   `todo/addon-engineering.md`** — W4a is scoped from it.

3. **The marker set undercounts the work.** Beyond the 45 distinct marker
   questions, `security-taint-and-restricted-data.md:717-742` is a **14-row
   secret-value operation table** where every row is a one-line pass/fail test, and
   roughly **12 more addon-testable questions** sit under `[gap]` with no marker
   (SavedVariables writer precision / NaN / cycles / key ordering, the 16-char
   prefix + 255-byte + throttle addon-message limits, event dispatch order between
   frames, `.toc` parser case-sensitivity).

Bucket totals of the 45 distinct marker questions:

| Bucket | n | Pass |
|---|---|---|
| call-and-record | 15 | **1** |
| scratch-frame behaviour | 8 | 2 |
| XML surface | 4 | 2 |
| animation semantics | 1 | 2 |
| event mechanics | 4 | 3 |
| lifecycle observation | 3 | 3 |
| container / TOC — needs generated sibling addons | 7 | deferred (W1d) |
| not answerable by any addon | 3 | never |

Plus the 14-row secret table in **pass 1**, and the ~12 unmarked `[gap]`s recorded
in the registry as candidates.

## Design

### Shape

Tracked in **this** repo, not a sub-repo. No GitHub repo, no releases, no
`ghaddons`, **not** in the `wowkb.addon` registry. Deploy is a directory copy into
`Interface/AddOns/`. This is what the program doc specifies, and it is what makes
iteration cheap: adding a test costs a copy, not a release cut.

```
projects/addon-lab/
  CLAUDE.md              deploy recipe + the invariants (esp. "nothing may depend on it")
  docs/w1-plan.md        this file
  questions.json         THE REGISTRY — id / anchor / bucket / expect / status
  .luacheckrc            copied from CDMProbe's, read_globals curated for the lab
  ClientLab/             <- copied verbatim into Interface/AddOns/ClientLab/
    ClientLab.toc
    Core.lua             namespace, SavedVariables, chat helpers, command registry
    Lab.lua              the test registry + runner + stash()
    Report.lua           chat rendering + `/clab guide`
    Secret.lua           obtain a genuine Secret Value; gate the tests that need one
    T_Anatomy.lua        tests, ONE FILE PER KB TOPIC FILE
    T_ApiEvents.lua
    T_Libraries.lua
    T_Module.lua
    T_Security.lua       the §4.2 14-row operation table
```

Test files are split **by KB topic file, not by bucket** — W2's job is "go back to
`file:line` and edit the claim", so locality to the anchor is what matters.

### The invariant that makes this safe

**Nothing in a product addon may ever depend on ClientLab.** This is what permits
junk to accumulate here. State it in `CLAUDE.md` and in `Core.lua`'s header.

### The test record

Declarative, registered by each `T_*.lua` file:

```lua
ns.Test{
  id       = "sandbox-require",              -- stable key; the reader's join column
  anchor   = "anatomy-and-runtime.md:677",   -- where the answer goes in the KB
  bucket   = "call",                         -- call|frame|anim|event|life|xml
  phase    = "manual",                       -- manual|load|login|world|logout|post
  needs    = nil,                            -- nil | "combat" | "secret"
  question = "Does the sandbox expose require / os / io?",
  run      = function() return {
                 require = ns.GlobalType("require"),
                 os      = ns.GlobalType("os"),
                 io      = ns.GlobalType("io"),
               } end,
}
```

**`expect` is deliberately NOT in the Lua.** It lives in `questions.json` and is
never compared in-game. This is the collect/assert split from
`m4.5-t3-plan.md`, and it is the one place the inherited doctrine needs restating,
because the lab is not `wowkb.cdmp`: **cdmp asserts a known answer against
regression; the lab discovers an unknown answer.** So the reader renders
`result` beside `expect` and a **human** decides — an automatic PASS/FAIL here
would be the instrument grading its own subject.

`phase` and `needs` are unused by pass 1 (everything is `manual`, `needs` only
`"secret"`) but exist from day one, because validating the record format on a cheap
pass is the entire reason pass 1 exists.

### The result envelope

Every test yields exactly one of three statuses — and **`skipped` is never a pass**,
the same rule `cdmp.py:180-190` enforces for SKIP:

```lua
{ id=, anchor=, bucket=, question=,
  status = "ok" | "error" | "skipped",
  value  = <stashed>,   -- on ok
  err    = <string>,    -- on error  -- for many of these, "it errors" IS the answer
  why    = <string>,    -- on skipped: "needs combat", "no secret value obtainable"
}
```

Wrapped in a run header carrying `at`, `version`, `interface`, `combat`,
`instance` — the fields `cdmp.py:414-443` uses for patch-drift and mixed-capture
detection, which the lab's reader will want for the same reasons.

Every test is `pcall`ed individually (the `Core.lua:99` dispatch idiom). A test that
errors records the error **as its answer**. One test cannot break the run.

`stash()` is CDMProbe's (`Probe.lua:128-133`), extended to recurse one level into a
flat table: Secret Values → `"<secret>"`, functions → `"<function>"`, live
frames/tables → dropped. Nothing non-scalar ever reaches SavedVariables.

### `ns.GlobalType(name)` — a design constraint that falls out of lint

Many pass-1 tests probe whether a global *exists* (`require`, `os`, `io`,
`table.freeze`, `strsplittable`, `string.rtgsub`, the six `C_CombatLog.*` names, the
`UIDropDownMenu_*` set). Referencing those as bare identifiers would make `luacheck`
scream at the very code whose purpose is to touch them.

**Rule: a test probing a global's existence must look it up by string, never by
identifier.** `ns.GlobalType(name)` returns `{ g = <type via rawget(_G, name)>, env
= <type via a pcall'd lookup in the addon's own environment> }`. This is not just
lint hygiene — the two lookups can *differ*, and that difference is itself the
answer to `libraries-and-ecosystem.md:552` (`UIDropDownMenu_*` resolves through
`GetCurrentEnvironment()` rather than `_G`, per `UIDropDownMenu.lua:1`).

### `Secret.lua` — the gate on the §4.2 table

The 14-row operation table needs one genuine Secret Value. CDMProbe already
established where one comes from: cooldown reads are secret **in combat** and
readable out of it (`probe-baseline.json`, `cooldown-read-combat-seam`).

`ns.GetSecret()` returns `value, source` or `nil, why`. All 14 operation tests
declare `needs = "secret"`; out of combat they record `status = "skipped"`, `why =
"no secret value obtainable in this context"` — never a value. Each operation is
separately `pcall`ed, because **most are expected to error** and the error is the
claim being tested.

This makes the run loop combat-gated, in the same shape as CDMProbe's known-working
loop:

```
/clab run            (out of combat)
pull a target dummy
/clab run            (in combat)
/reload              <- NOT optional; SavedVariables only flush on reload/logout
```

### `/clab guide` — coverage

The `probe guide` pattern (`Probe.lua:472-564`): a flat `{label, nudge, met}` list,
**pull-based**, no ticker. Its value is timing — you learn the capture is incomplete
while still standing at the dummy. Pass-1 goals, deliberately few (per that file's
own note about not outgrowing a handful): an OOC run captured · a secret value
obtained · the secret-op table run · an in-combat run captured.

Heed `Probe.lua:522-526`: never write a goal that can never go green. Ask whether
the channel was **exercised**, not whether it returned data.

### SavedVariables

`## SavedVariables: ClientLabDB`, account-wide.

```
ClientLabDB
  runs = { ooc = <run>, combat = <run> }   -- keyed by combat state, like CDMProbeDB.probe
  journal = {}                             -- pass 3: the lifecycle event log
```

`Core.lua` copies CDMProbe's non-destructive `CopyTable` defaults merge
(`Core.lua:112-119`) and its capture-buffer / secret-safe `ns.Print`
(`Core.lua:42-71`) essentially verbatim. Each run carries `version` + `interface`;
no schema field and no migration, matching CDMProbe's stated reasoning
(`Core.lua:12-14`).

### `tools/wowkb/lab.py`

W1 builds only `deploy`; W2 builds `show` / `report`. One module, incremental.

- `deploy` — copy `projects/addon-lab/ClientLab/` → `<DEFAULT_WOW>/Interface/AddOns/ClientLab/`,
  mirroring deletions. Reuses `charstate.DEFAULT_WOW` rather than repeating the
  `/mnt/c/Program Files (x86)/…` path in prose, where it would rot.
- **Registry cross-check (W1, cheap and worth having now):** every `id` in the Lua
  must exist in `questions.json` and vice versa. An unmatched id is a loud error,
  not a silent skip — the `cdmp.py:360-369` "no check function for this id" rule.

## Scope — what pass 1 does NOT include

Stated explicitly so a later session does not assume it was missed:

- The 7 **container/TOC** questions. They test the addon *container*, so the lab
  cannot test them in its own `.toc` without breaking itself. They need a generator
  writing small sibling addons into `AddOns/` per test — **W1d**, a separate design.
- The 3 **not-answerable** questions, recorded in `questions.json` with
  `status: "not-answerable"` and the reason, never built:
  `api-events-and-discovery.md:174` (unfalsifiable from Lua — both readings produce
  identical observable behaviour), `security-…:470` (needs a CVar + client restart +
  reading `Logs/taint.log` off disk), `state-…:355` half (needs reading the written
  SavedVariables file off disk — though its "secrets become nil" half **is**
  addon-testable via a two-session round trip, and is recorded as a pass-3
  candidate).
- Buckets 2 and 3 (scratch-frame, XML, animation, event, lifecycle — 20 tests).
- The ~12 unmarked `[gap]` questions — harvested into `questions.json` as
  `status: "candidate"`, not built.

## Build order

1. **KB hygiene** (do first, ~20 min): correct the `reset` paragraph in
   `todo/addon-engineering.md`; record the backticked-marker decision in
   `knowledge/addon-dev/README.md` + `gen_verify.py`'s docstring.
2. **`questions.json`** — the full registry: 45 marker questions + 14 secret-table
   rows + ~12 `[gap]` candidates + the 3 not-answerable, each with `id`, `anchor`,
   `bucket`, `question`, `expect`, `status`. Authored from the exploration output;
   this is the single list and everything else keys off it.
3. **Skeleton** — `.toc`, `Core.lua`, `Lab.lua`, `Report.lua`, `.luacheckrc`,
   `CLAUDE.md`, plus **one** trivial test, and `wowkb.lab deploy`. Deploy, `/clab
   run`, `/reload`, confirm the file on disk has the shape intended.
4. **`Secret.lua`** + the 14-row §4.2 table.
5. **The 15 call-and-record tests** across `T_Anatomy` / `T_ApiEvents` /
   `T_Libraries` / `T_Module`.
6. **`/clab guide`**, then `luacheck ClientLab/` clean.

Step 3 stopping to verify on disk before step 4 is the point of the phasing — it is
the program doc's own lesson (*"do not assert from an instrument you have not
validated"*) applied to the instrument itself.

## Verification

```bash
export PATH="$HOME/.luarocks/bin:$PATH"
cd ~/code/fun/wow/projects/addon-lab && luacheck ClientLab/
cd ~/code/fun/wow/tools && uv run python -m wowkb.lab deploy      # + registry cross-check
```

In game: `/clab` (help) → `/clab run` out of combat → `/clab guide` (names what is
missing) → pull a dummy → `/clab run` in combat → `/reload`. Then the run is at
`…/WTF/Account/<ACCT>/SavedVariables/ClientLab.lua` under `ClientLabDB.runs`.

**W1 is done when:**

- every registered test reports `ok`, `error`, or `skipped` **with a reason** — and
  **no test reports a value it did not measure**. That is the single criterion; the
  program doc records two separate incidents of an instrument emitting a confident
  number it could not observe.
- the ~29 pass-1 tests are all present in the on-disk run, and the registry
  cross-check passes in both directions.
- `luacheck` is clean with **zero inline suppressions** — a real catch gets fixed, a
  legitimate API name goes in the `read_globals` std (`.luacheckrc:11-15` doctrine).

Answering the questions and editing the KB is **W2** and explicitly not part of this.
