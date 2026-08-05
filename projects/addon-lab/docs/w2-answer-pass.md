# W2 — the answer pass: run the lab, drain what it says into the KB

> Parent program: `todo/addon-engineering.md` (W2). W1 built the instrument;
> this doc is about **pointing it at the registry and closing questions**.
> `docs/w1-plan.md` owns the harness design and is not restated here.

## 0. The one-paragraph summary

The lab can currently answer **29 of 75** registered questions, and every answer it
produces has to be dug out of SavedVariables after a `/reload`. Three things are in the
way, in this order: the lab **predates the capture standard**, so it cannot use the dump
panel that would let a human read an answer mid-pull; there is **no drain path**, so an
answered question is still a manual KB edit nobody is prompted to make; and the unbuilt
questions are **batched wrong** — they are grouped by KB topic file, which is right for
*editing*, and useless for deciding what one play session can cover.

Fix those three and the remaining ~35 answerable questions become four in-game sessions,
not forty.

---

## 1. What is actually open

75 registered questions. The status field already sorts them:

| Status | N | What it means for this pass |
|---|---:|---|
| `built` | 29 | Test exists. **Has it ever been run and drained?** §2.1 — this is the first thing to establish |
| `deferred` | 24 | Real, addon-answerable, unbuilt. **The main body of work** |
| `candidate` | 11 | Harvested from a bare `[gap]`, never triaged. Some are trivially buildable, one is not answerable at all |
| `deferred-w1d` | 8 | All eight are `.toc`/container questions. Blocked on one generator (§5) |
| `not-answerable` | 3 | Reason recorded. Do not re-attempt; two need a **file read**, not an addon |

By bucket: `call` 25 · `secret` 17 · `life` 9 · `frame` 7 · `toc` 7 · `event` 5 · `xml` 4 ·
`anim` 1.

⚠ **`toc-category-grouping` and `secret-aspectless-pixel-moved` are partly or wholly
visual.** No instrument closes them; only an eyeball does. They must never be marked
answered off a green run — the registry's own rule, and it has already cost this workspace
two incidents.

---

## 2. Phase A — make the instrument usable (no game session needed)

### 2.1 Establish what the existing 29 already told us

**Do this first, before writing a single new test.** Settled 2026-08-05 by reading the file
directly — and it is worse than "may hold answers":

⚠ **`wowkb.lab show` does not exist.** `tools/wowkb/lab.py` is 159 lines with
`choices=["deploy"]`. There is no reader, which is *why* nothing was drained: nobody
**could** drain it. Building the reader (§2.1a below, now the first shippable deliverable)
comes before everything else in this doc.

**What is actually on disk.** `…/WTF/Account/LLOYDCHRISTMAS/SavedVariables/ClientLab.lua`,
21,791 bytes, written **2026-07-24 07:54**, addon v0.1.0. Two slots, `ooc` (07:49:13) and
`combat` (07:51:04), each **ok 15 / error 0 / skipped 14**. **None were ever drained** —
they have sat there for 12 days. Spot-checks:

| id | result |
|---|---|
| `sandbox-require-os-io` | `require` / `os` / `io` all **nil**, in `_G` *and* the addon env |
| `addon-exists-nested-lib` | `LibStub=false`, `RaiderIO=true` |
| `string-rtgsub-callable` | `type="function"`, `calledOk=true`, `result="a-b-c"` |

Meanwhile `anatomy-and-runtime.md:677` still reads *"`@verify-ingame`: `/dump type(require),
type(os), type(io)` settles it in one line"*, and `string.rtgsub` is still an open `[gap]`
at `:972`. The answers existed the whole time.

**The 14 secret rows have never executed once.** Both slots skip all 14 — `ooc` for the
right reason, `combat` with *"cooldown fields read non-secret (out of combat?)"*, which is
the **v0.1.0 GCD-spell bug**. `Secret.lua` was fixed at **07:55**, one minute after the
07:54 capture, and has never been re-flown. §4 batch 3 is therefore not "re-run for
confirmation" — it is a first run.

So: 15 answers to drain, 14 rows to fly, and **no reader for either**. Build the reader,
drain the 15, then migrate — building more tests first reproduces the failure at scale.

### 2.1a Build the reader — `wowkb.lab show`

The first shippable deliverable, and all of it desk work.

- [ ] Load `questions.json` and the stored run, join on `id`.
- [ ] Print **result beside `expect`**, grouped by status. **Never a verdict** — `expect` is
      never compared programmatically; a human reads and decides (§7 rule 1).
- [ ] Flag `skipped` loudly with its `why`. **`skipped` is never a pass.**

### 2.2 Migrate ClientLab onto the capture standard

The lab writes `ClientLabDB.runs.{ooc,combat}` — a bespoke two-slot store. The house
standard (`references/capture-and-dump-standard.md` §2) is `<DB>.captures.<stream>`, and
`wowkb.capture` is the only sanctioned reader. The lab is the one addon in the workspace
still outside it.

This is not tidying. Three concrete defects fall out of the old shape:

1. **Two slots, not a ring.** A second combat run **clobbers** the first. A pass that
   respecs to test a hero swap destroys its own earlier evidence — §2 rule 3 exists
   because this already cost `decisionlog` a re-fly.
2. **No `/reload`-free readback.** Every answer costs a reload, which ends the pull you
   were measuring. This is the single biggest tax on the whole pass.
3. **Nothing is stamped.** `combat` is a boolean on the run header; spec, hero tree and
   instance type are not per-result. Any later "was this measured on Demo or Havoc?"
   is unanswerable, and §2 rule 4 says that is a **one-way door**.

**Work:**

- [ ] Vendor `Capture.lua` from CDMProbe into `ClientLab/` (soft contract — copy and adapt;
      keep §2 exact).
- [ ] Open one stream: `ns.Capture.Open("runs", { sessions = 8, cap = 2000 })`. Eight
      because a pass that swaps spec **and** hero tree burns 4–5 `/reload`s.
- [ ] Emit **`rows`**, not `lines` — the consumer is `wowkb.lab`, a reader that must be
      free to evolve. (§2 "choosing lines vs rows".) One row per test result:
      `{id, status, value, err, why, combat, spec, hero, instance}`.
- [ ] **Stamp spec + hero tree + combat as `:Meta` at run time**, per §2 rule 4. Anything
      you might later slice by must be recorded now.
- [ ] Register the lab in `wowkb.capture`'s addon registry (`clab`), so
      `uv run python -m wowkb.capture clab runs` works like every other addon.
- [ ] Keep `ns.stash()` exactly as it is. It already degrades a Secret Value to
      `"<secret>"`, which *is* the finding — that is `Capture.Safe()`'s contract reached
      independently, and it must not regress into formatting a secret.

### 2.3 Add the dump panel — the change that pays for the rest

`ns.Dumps.Register{}` + `/clab dump` (§4 of the standard). **`[copy]` reads the in-memory
ring, so there is no `/reload` and no hunting through SavedVariables.**

For this pass specifically, that converts the loop from *one answer per reload* to
*answer, adjust, re-answer, without leaving the dummy*. Register two buttons:

- **`run`** — run every test and copy the results out, mid-pull.
- **`secret`** — `ns.GetSecret()` plus its `source`/`why` string. When the secret gate
  fails, this is the difference between "14 rows skipped" and knowing *why* in five
  seconds.

⚠ Panel must refuse to build itself in combat, and the copy EditBox must never be a secure
frame. Call `SetMaxLetters(0)`/`SetMaxBytes(0)` unconditionally. Page at ~30k chars —
**and that cap is a guess; OBS-003 already owns measuring it**, so if this pass stalls the
client on a big payload, that is a measurement, and it goes to `observations.md`.

### 2.4 Teach `wowkb.lab deploy --check` to validate anchors

The KB cleanup silently drifted several `anchor` values (`taintlog-level-5` pointed at
:470 for a marker at :467). The registry's `id` is durable by design; the anchor is a
convenience nothing checks.

- [ ] `--check` verifies every `anchor`/`also` resolves to a line that still contains a
      `@verify-ingame` marker or a `[gap]`. Report drift; **do not auto-fix** — a moved
      anchor and a deleted claim look identical to a line-number check, and guessing
      between them is how a question gets silently retired.

---

## 3. Phase B — the drain path (this is the part that is missing entirely)

Answering a question changes nothing until the KB changes. Right now that step is
undocumented and unprompted, which is exactly how the last batch of answers rotted.

**The model is already decided elsewhere and should just be adopted here:** an answer is
an *observation*, and `observations.md` + `wowkb.obs` is the queue that carries one into a
topic file with a required `Drains to:`.

### The loop

```
/clab run                    in game — rows land in the `runs` stream
[copy] off the dump panel    (or /reload, then wowkb.capture clab runs)
uv run python -m wowkb.lab show      result BESIDE expect; a HUMAN reads it
uv run python -m wowkb.lab drain <id>    <- NEW: mints the observation
uv run python -m wowkb.obs drain OBS-nnn  existing: writes it into the topic file
```

### `wowkb.lab drain <id>` — the new piece

- [ ] Reads the stored result for `<id>` and the question's `expect`, and **appends an
      `observations.md` entry** with `Drains to:` pre-filled from the question's `anchor`.
- [ ] Refuses on a `skipped` result. **`skipped` is never a pass** — the lab's own rule.
- [ ] Refuses on any question whose `expect` says only an eyeball closes it
      (`toc-category-grouping`, `secret-aspectless-pixel-moved`). Those get a human-written
      observation or none.
- [ ] Flips the question's status to `answered` and records the run's `started`/`version`,
      so the registry stops offering it.
- [ ] Emits the exact edit the topic file needs: **rewrite the claim in place, drop the
      `@verify-ingame`, add `[client YYYY-MM-DD]`.** Never a correction note under
      standing wrong text — README §7 rule 1.

**Why route through `observations.md` rather than editing the topic file directly:** the
drain is a *judgment* (does this measurement actually settle the claim as written?), and
`wowkb.obs check` already gates a release on observations left open past 14 days. That
gate is the thing that makes an answered-but-unwritten question impossible to forget. A
direct edit has no such backstop.

---

## 4. Phase C — build the unbuilt tests, batched by session precondition

**Batch by what a single play session can cover, not by topic file.** Test *files* stay
split by KB topic file (locality to the anchor is what W2's edit step needs) — this is
purely the build and fly order.

### Batch 1 — OOC, no preconditions (~13 questions, 1 session)

Everything answerable standing in a city. The cheapest possible win, and it exercises the
new capture path before anything expensive rides on it.

- **Frame/z-order** (5): `frame-strata-parent`, `frame-level-arithmetic`,
  `draw-layer-z-order`, `fontstring-sublevel-arg`, `texture-source-exclusivity`
- **Colour storage** (3): `vertexcolor-vs-gradient`, `settextcolor-vs-getvertexcolor`,
  `xml-color-element-target`
- **Events** (3): `register-all-then-unregister`, `event-dispatch-order-between-frames`,
  `onupdate-blocked-by-hidden`
- **Encoding** (2): `encoding-util-error-semantics`, `savedvars-number-precision`

These are pure scratch-frame work. No combat, no secrets, no reload.

### Batch 2 — reload round-trips (~5 questions, 1 session + reloads)

Two-phase tests: write, `/reload`, read back. Needs a `phase` field the harness already
declares but does not use (`Lab.lua:15` — "exist from day one" — this is the pass that
uses it).

- `savedvars-secret-roundtrip` ⭐ (the addon-testable half of a `not-answerable`)
- `savedvars-table-cycles`, `savedvars-key-ordering`, `savedvars-bak-semantics`
- `reload-state-preserved`, `reload-addons-unloading-payload`, `logout-event-order`

⚠ `savedvars-bak-semantics` needs a **file read**, not Lua. Pair the in-game half with a
`wowkb` stat of the `.bak` — the same split already recorded on `savedvars-secret-comment`.

### Batch 3 — combat + secrets (~6 questions, 1 dummy session) — **highest value**

Combat-gated, so they need a dummy and a sustained pull. `Secret.lua` already obtains a
genuine Secret Value from a tracked Cooldown Manager spell.

- ⭐ **`cdm-auradatacached-plain-in-combat`** — *the* question. If `item.auraDataCached`
  is plain in combat, the in-combat DoT-remaining read that `cooldown-manager.md` §5.1
  **and** §7 both declare unanswerable is already on the frame. It also settles A1 in
  `mined-pending-verification.md` and unblocks any DoT assist.
- `secret-compare-to-nil-permitted` — must include a control (`s == 0`) that **is expected
  to throw**. A test where every branch passes has not measured anything.
- `serializer-secret` — a Secret Value into AceSerializer / LibSerialize / LibDeflate.
  None of the three guards for it, so this is a real exposure, not a curiosity.
- `secret-taint-isvisible-engine-subtree` (from `security:2057`) — parent an addon frame
  into an engine-owned subtree, read `IsVisible`.
- The `needs = "secret"` rows that `skipped` in any prior run.

**Do this on a class with a target DoT.** The pandemic question in `kb-inbox` is Affliction-
only for the same reason, and the two share a session — Agony on a dummy answers both.

### Batch 4 — build-dependent (~3 questions, rides on any session)

- `traitconfig-fires-on-hero-swap` — register all three events, log every firing beside
  `GetActiveHeroTalentSpec()`, swap hero tree without swapping spec. **The count matters as
  much as the fact.** Free to fly alongside batch 3 if the character has two hero trees.
- `synchronous-event-semantics`, `event-callback-nil-owner`.

### Not batched — needs a design first

`xml-onload-varargs`, `addon-declared-intrinsic`, `scoped-modifier-for-addons` need XML
files rather than Lua, and `addon-message-*` / `battlenet-senddata-limits` need a second
client or a party member. Leave them `deferred` with the reason recorded. **An honest
`deferred` beats a test that fakes its own precondition** — house rule 6.

---

## 5. Phase D — W1d, the sibling-addon generator (8 questions, one build)

All eight `deferred-w1d` questions are `.toc`/container questions, and all eight are
blocked on the same missing capability: **the lab cannot test the addon container from
inside its own container without breaking itself.**

One generator unblocks all eight at once, which makes it the best ratio of build-effort to
questions-answered in this whole plan — better than any individual test.

- [ ] `wowkb.lab siblings` writes N tiny addons into `AddOns/`, each a `.toc` variant
      (`## OptionalDeps` absent · a deliberate Lua error mid-file · a dependency chain
      A→B→C · `## LoadIntoEnvironment` · `## Secure` · lowercase directives · a known file
      order · differing `## Category:`), each doing nothing but setting a global.
- [ ] ClientLab reads which globals exist and in what order. **The generated addons are
      the experiment; ClientLab is only the reader.**
- [ ] Generated siblings are **deleted by the same command that made them.** They are
      probe code in the house-rule-2 sense — an `AddOns/` folder full of orphaned
      `ClientLabSibling_07` is exactly the accretion the lab exists to prevent.

⚠ Requires a full client restart, not a `/reload` — addon enumeration happens at login.
Budget it as its own session.

---

## 6. Sequencing, and why

```
A  instrument      2.1 read what exists  →  2.2 capture standard  →  2.3 dump panel  →  2.4 anchor check
B  drain path      wowkb.lab drain  →  observations.md  →  topic file
C  tests           batch 1 (OOC)  →  batch 2 (reload)  →  batch 3 (combat/secret)  →  batch 4
D  W1d             the generator, its own session
```

**A before C** because every test built before the capture migration has to be revisited,
and because 2.1 **does** reveal answers already sitting on disk — **15 of them**, undrained
since 2026-07-24 because no reader existed to drain them with.

**B before C** — and this is the one that is easy to get wrong. Building 20 tests and *then*
inventing the drain path produces 20 answers with nowhere to go, which is precisely how the
existing 29 ended up in an undrained state. **Prove the whole loop on one question first:**
build it, fly it, drain it, watch the topic file change. Then batch.

**Batch 3 is the highest-value and should not be reordered earlier.** It needs the dump
panel to be worth flying — without `[copy]`, each secret answer costs a reload, and a
reload ends the pull that made the value secret in the first place.

---

## 7. Rules this pass must not break

Restated because each has already cost something here:

1. **`expect` never ships to the client.** The lab discovers; it does not assert. A test's
   `run` returns a value, a human reads it beside the expectation. An automatic PASS/FAIL
   is the instrument grading its own subject.
2. **Never record a value you did not measure.** Wrong precondition → `measured=false` and
   why, never a fabricated verdict. This is *the* done-criterion; the program doc records
   two incidents.
3. **`skipped` is never a pass**, and a grader reports **UNREADABLE, never a number**, when
   a capture predates the mark it needs.
4. **Comments say what the code does now** — no dates, no versions, no "used to". A fact
   about the game goes to `observations.md`, not a comment. New files at comment:code
   ≤0.35. (`Secret.lua`'s header currently violates this; fix it when touched, not as a
   sweep.)
5. **Probe a global by string** — `ns.GlobalType(name)` / `ns.G(name)`, never a bare
   identifier. `luacheck` clean with **zero inline suppressions**.
6. **A visual question stays open until an eyeball closes it.** Two of these can never go
   green programmatically, and marking one answered off an INERT verdict would be the
   third instrument-overreach incident.

## 7a. Where this pass got to (2026-08-05)

**Desk work is complete; what remains is flying.** Registry: **14 answered · 40 built ·
6 deferred · 8 deferred-w1d · 4 candidate · 3 not-answerable**, up from 29 built / 0
answered. Every `built` entry that cannot be closed by a run carries a `note` saying why,
so "we looked and chose not to" is distinguishable from "nobody looked."

Shipped: `wowkb.lab show` + `wowkb.lab drain` (§2.1a, §3) · the capture migration (§2.2,
now `rows` with per-row `combat`/`spec`/`hero`/`instance` stamps) · the dump panel (§2.3) ·
25 new tests across batches 1, 2 and 3.

Three things were found that the plan did not anticipate:

1. **`issecure-in-addon-frame` was NOT drainable.** `T_Anatomy.lua` used
   `ok and (res and true or false) or ("errored: "..res)` — and a legitimate
   `issecure() == false` makes the middle term falsy, so Lua's `or` falls through to the
   ERROR branch. The one answer the test exists to record is the one it could not spell.
   The expression is fixed; the question needs a re-fly. **14 of 15, not 15 of 15.**
2. **`draw-layer-z-order` is a THIRD eyeball-only question**, alongside the two §3 names.
   Its `expect` asks for "two overlapping textures and a visual read", and no API returns
   composite draw order. `wowkb.lab drain` refuses all three.
3. **Three round-trip payloads are quarantined into a second SavedVariable**
   (`ClientLabScratchDB`). NaN/infinity may serialise to something the loader rejects, a
   self-referencing table may hang the client at logout, and a Secret Value reaching the
   writer is the question itself — any of which can take the whole file, and `ClientLabDB`
   holds the `runs` capture ring. One `.toc` line; the worst case now loses only the probe
   that caused it.

### The in-game recipe

**Enable the addon, `/reload`, and go pull something.** That is the whole procedure.

The first cut of this shipped a checklist of slash commands typed mid-pull, which is
both a **violation of the capture standard** (§4: a human-triggered capture is a
button, never a subcommand) and the exact failure `/cdmp flight` was built to end.
`Autorun.lua` replaced it: the lab runs OOC after login, again ~2 s into combat, and
then retries **only the rows still unanswered** every 3 s for as long as the pull
lasts. A secret can be unobtainable one instant and available the next, so a single
in-combat run was never evidence that a row could not answer.

⭐ Pull on **Affliction** so Agony rides along for `cdm-auradatacached-plain-in-combat`.
`/clab` opens the panel if you want to `[copy]` an answer out mid-pull.

Then, at the desk:

```bash
uv run python -m wowkb.capture clab runs   # if you reloaded
uv run python -m wowkb.lab show            # result beside expect
uv run python -m wowkb.lab drain <id>      # per question a human has decided
```

**Reload round-trips** (`savedvars-*`, `savedvariables-first-ordering`,
`logout-event-order`) are their own session: `run` → `/reload` → `run`. The three
quarantined ones do **not** auto-re-arm — run once more to re-arm them. `logout-event-order`
needs a full logout to produce a journal at all.

**`traitconfig-fires-on-hero-swap`** is free on any session with two hero trees: its
listener is always on, so just swap and re-run.

## 8. Done looks like

- `wowkb.capture clab runs` works; `ClientLabDB.runs` is gone.
- `/clab dump` copies an answer out mid-pull with no `/reload`.
- `wowkb.lab drain <id>` mints an observation; `wowkb.obs check` then *forces* the KB edit.
- Registry: 29 built → ~50 answered, with every remaining entry carrying a **reason** it is
  not answerable rather than a status nobody revisited.
- The `[gap]`/`@verify-ingame` counts in `knowledge/addon-dev/` go **down**, and each one
  that goes down leaves a `[client YYYY-MM-DD]` tag where it used to be.
