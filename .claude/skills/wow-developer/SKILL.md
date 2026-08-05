---
name: wow-developer
description: >-
  Developing World of Warcraft addons (Retail / Midnight 12.0) — writing, debugging, or
  reviewing Lua / XML / .toc code that runs inside the WoW client. Use this whenever the
  work is addon code: CreateFrame and widgets, taint or "blocked in combat", secret
  values, SetAttribute and secure templates, event registration and payloads,
  SavedVariables, animation and textures (e.g. SetVertexColor vs SetGradient), or how to
  lay an addon out — even when none of those exact words appear but the code clearly runs
  in the client. This workspace keeps TWO knowledge bases and this skill routes between
  them: addon-code questions are answered from knowledge/addon-dev/; gameplay questions
  (rotations, gearing, weeklies, ilvl, "what should I do this session") are NOT — they
  belong to the game KB and its live tools. Do not trigger for gameplay or strategy
  questions.
---

# WoW addon development

Write, debug and review addon code well, and leave the knowledge base more correct than
you found it. Two facts drive everything below:

1. **There is no headless WoW.** The only place code truly runs is a slow, stateful,
   security-restricted client you cannot script. So the discipline is to *not need* the
   client — push logic and rendering into shapes you can test without it.
2. **Most of the internet describes a dead client.** The layout, the API and the security
   model all changed in Midnight (12.0). Answer from the pinned KB first; treat undated or
   pre-12.0 material as suspect.

## Two knowledge bases — route before you answer

| The question is about… | Answer from | Never from |
|---|---|---|
| **Addon code** — "why is my frame blocked in combat?", "does `SetVertexColor` clobber `SetGradient`?", "what's this event's payload?" | `knowledge/addon-dev/` + Blizzard's shipped UI source | the game KB |
| **The game** — ilvl, rotations, gearing, weeklies, "what should I do this session?" | `knowledge/` (endgame, classes, systems) + live tools | `knowledge/addon-dev/` |

Litmus: *would running the code change the answer?* If yes it's a dev question. If it
depends on this reset's game state it's a game question, and not yours.

**The "Tier 1" trap.** Both subtrees rank sources into tiers and **the tiers mean different
things**. The game KB's (`knowledge/_meta/sources.md`) are about game sources; addon-dev's
(`knowledge/addon-dev/sources.md` §0) are about *engineering* sources — Blizzard's shipped
UI source, its generated API docs, `UI.xsd`. Never carry a tier judgment across.

## Consulting the addon-dev KB

**Start at `knowledge/addon-dev/README.md`.** Its §1 topic map is the router; `sources.md`
§7 routes per-topic to the underlying source. Read those two rather than re-deriving the map.

Beyond the topic files, four files are queues rather than claims — a topic file asserts,
a queue file asks:

- **`observations.md`** — facts our own running code discovered, parked until drained into
  the topic file that owns them.
- **`mined-pending-verification.md`** — findings from reading third-party addons, not yet
  corroborated.
- **`12.1.0-ptr-heads-up.md`** — what goes wrong on patch day. `patch:` ahead of live.
- **`projects/addon-lab/questions.json`** — the **test registry**, outside `knowledge/`
  because it has an addon behind it (**ClientLab**, `/clab`). One row per question the lab
  tests or could test, keyed by a stable `id` and anchored `<file>:<line>` back into the
  topic files. It is *not* where an unknown is first written down — the marker on the claim
  is. See **Unknowns** below.

Respect the provenance markers — they are what keep you off stale answers:

- **Front-matter:** `patch`, `fetched`, `reviewed`, `confidence`. A file can read current
  (`patch: 12.0.7`) yet be weeks stale on `reviewed:`.
- **`[client YYYY-MM-DD]`** — this claim was measured by running code in the client. It is
  the strongest evidence class in the subtree. An **unmarked** claim is a source read:
  correct about *shape*, but the generated docs' annotations are necessary and not
  sufficient, and only a measurement knows the difference.
- **`[T1 obs]` is NOT `[client]`.** It means someone counted something in an on-disk
  artefact — occurrences in the shipped corpus, rows in a generated doc. Tier 1, real
  evidence, and **nothing ran in the game**. The two read alike at a glance and rank
  nowhere near each other.
- **`@verify-ingame`** — running the code would settle this. Treat it as a hypothesis.
- **`@pending-test: <id>`** — a ClientLab test with that id already exists and flies on the
  next pull. In flight, not open: don't write a second test for it, and don't treat it as
  measured either.
- **`[gap]`** — an honest hole. **Close it, leave it, or leave it and add one where a hole
  has none — all three are fine.** Leaving one is the common case and costs nothing; a
  `[gap]` that warns you off a tempting inference (*"that absence is weak evidence, not
  proof"*) is prose doing its job and is not a question at all. What you may never do is
  build on one silently — see **Unknowns**.
- **Build-pinned to 12.0.7.68887.** `file:line` anchors are only valid for that build.

## Look it up before you guess

- Blizzard UI source + reference clones: `raw/addon-research/` (gitignored). Cite `file:line`.
- `wowkb.uiapi` queries the generated API spec; `wowkb.wiki` pulls warcraft.wiki.gg.
- In client: `/api` and `/eventtrace` are the shipped discovery tools.

## Verify before you assert

**28% of the addon-dev KB's initial claims were refuted on careful verification.**

- **Check claims against `file:line` before relaying them** — yours, another agent's, or a
  web page's. Confident and wrong is the default failure mode here.
- **Never assert a mechanism from a screenshot, or from an instrument you have not
  validated.** Both have cost releases.
- **An instrument that cannot observe its subject must say so, not emit a number.**

## Unknowns — the protocol

**The marker on the claim is the whole mechanism.** You meet it in the prose you are
already reading; there is no list to generate and no command to run first. Its three
states are the lifecycle:

```
`[gap]` · `[unverified]` · `@verify-ingame`    open — nobody is on it
`@pending-test: <id>`                          a ClientLab test exists; flies next pull
`[client YYYY-MM-DD]`                          measured and drained; marker gone
```

**When a marked claim is load-bearing for what you are about to write: STOP and ASK.**
Name the claim, say what is unverified, and let the user pick. Three answers, all fine:

| They say | You do |
|---|---|
| **assume it / guess** | proceed — and say so **in the answer and in the code**, so the assumption is visible where it will bite |
| **park it** | leave the marker (add one if the hole has none) and move on. Parking is free and blameless — *"not sure, haven't needed this"* is a complete answer |
| **test it** | write the test now, four steps below |

**Never assume silently, and never quietly go build a test instead of asking.** A marker
merely *near* your work is not a stop — only one you would be building on.

**"Test it" — four steps, no ceremony:**

1. Write `ns.Test{ id = … }` into `projects/addon-lab/ClientLab/T_<Topic>.lua` — the file
   named for the KB topic file the claim lives in.
2. Add its row to `projects/addon-lab/questions.json` as `built` (or flip an existing
   `parked` row). Not bureaucracy: `deploy --check` refuses to copy unless every test has
   a row and every row has a test, **both directions**.
3. **Promote the marker** on the claim to `` `@pending-test: <id>` ``, so the next reader
   sees it is in flight rather than open.
4. `uv run python -m wowkb.lab deploy` — a directory copy, not a release.

**There is nothing to schedule.** `Autorun.lua` runs every built test on the next login,
again on combat entry, and retries the unanswered ones through the pull. Writing the test
*is* queuing it.

**Clearing one.** Next session: `wowkb.lab show` (result beside `expect` — no verdict is
printed, a human decides) → `wowkb.lab drain <id>` mints the observation → rewrite the
claim, **drop `@pending-test`**, tag `[client YYYY-MM-DD]` → **delete the test** →
`wowkb.obs drain OBS-nnn`. A test that flew and could not answer keeps its marker: it will
fly again next pull.

⚠ **Deleting the test is not optional, and it is house rule 2 applied to the lab.** The
claim in the topic file is the durable artefact; the test that produced it is probe code
and dies in the same edit. Delete the file and its `.toc` line too if it was the last test
in it. Nothing re-checks a drained test — `show` refuses to print a verdict and `drain`
refuses an answered question — so a retained one only costs run time on every pull, and
`deploy --check` now fails by name until it is gone. **The suite shrinks as the KB grows.**

Two more rules, both about honesty:

- **A fact your own code discovered is not an unknown** — it is an answer looking for a
  home. That goes to `observations.md` (below).
- **Never record a value you did not measure.** A test that could not observe its subject
  records `measured = false` + why. `skipped` is never a pass.

Only two things may never accumulate: **a measured answer that has not reached the KB**
(gated by `wowkb.obs check`) and **an unverified claim silently built on** (gated by you
asking). Everything else piles up harmlessly — **no clock, no cap, no gate on an open
marker**, and the trigger for testing one is *use*, never age.

## Architectural discipline

**Design so the client isn't required to test.**

- **Separate pure logic from the game.** A rotation, a scoring pass, a state reduction
  takes plain data in and returns plain data out, touching no API — unit-testable under
  `busted` with no client. When logic is smeared through frame handlers, the only harness
  is a live pull.
- **Keep the display data-driven and decision-free.** A render layer turns a data structure
  into pixels and makes no choices, so you can feed it dummy values.

Blizzard's own code models this; `module-architecture.md` documents it at
`confidence: medium` — corroboration, not a mandate.

## House rules — all seven are checkable

Full text and the receipt for each: **`references/house-rules.md`** — read it before
writing code. Capture/dump contract: **`references/capture-and-dump-standard.md`**.
Mechanical enforcement: **`/addon-review`**.

1. **Comments say what the code does now.** ≤6 lines a block, ≤10 a header, and **no dates,
   versions, `Phase N`, or "used to"** — that's `git log`. A fact about how the game behaves
   goes to `observations.md`, not a comment. New files land at comment:code ≤0.35; a file
   you touch may not increase its ratio.
2. **Probe code lives in `<Addon>/probes/`**, carries a `--@probe` header with an `expires`
   date, and is **deleted in the commit that writes the KB claim it produced**. Deletion is
   five items: file, `.toc` line, capture stream + `DEFAULTS` entry, spec, extractor.
3. **One capture path.** `ns.Capture.Open(stream, {sessions, cap})` → `<DB>.captures.<stream>`
   → `wowkb.capture <addon> <stream>`. Lines are pre-rendered, so **anything you'd slice by
   later must be a `:Mark` now**; no game value reaches a line except through `Capture.Safe()`.
4. **Dumps are buttons, not commands.** `ns.Dumps.Register{…}` on the `/<addon> dump` panel,
   with a blurb and a `[copy]` (**WoW has no clipboard API** — multiline EditBox +
   `HighlightText()`). Rides the same stream shape as rule 3.
5. **Location is the marker**, not an annotation: `<Addon>/` shipped · `probes/`
   experimental · `archive/` retired. The one exception is `--@unverified` on a path whose
   game behaviour has never been observed, and every one must be in the current flight's
   acceptance set.
6. **Test pure logic; don't test the client.** If the assertion's truth depends on a fake
   you wrote of an API you have never called, delete the test. Author contract suites from
   the KB, never from the module under test.
7. **Commands come from a schema table** (BucketBinds `Core.lua:210`), never a hand-rolled
   parser. Max depth `/<addon> <verb> [<arg>]`. **No substring dispatch** — `rest:find("on")`
   also matches "sound on", and that has been a real bug three times.

## Improve the KB as you go

The KB grows through use. When your work teaches you something the KB doesn't have, or
proves something in it wrong, **write it back in the same session** — and when it teaches
you only that there is a **hole**, record the hole, in the same session, just as cheaply.

**How a claim is written — the current-state rule.** A topic file states what is true now.
It never states what it used to say.

- **Correcting a claim means rewriting the claim**, in place. Do not leave the old text
  standing under a correction note. If a reader can get the wrong answer by reading
  top-down or grepping one line, the edit is not finished.
- **History goes in one line in the file's `## Changelog`, or nowhere.** Anything longer
  belongs in `projects/<addon>/docs/`.
- **A measurement is a claim plus a `[client YYYY-MM-DD]` tag, not a story.** The spec, the
  build, what you tried first and how many builds it cost are session facts — project docs,
  never a reference file.
- **A date in prose is a defect.** Dates live in front matter, a citation stamp, a
  `[client]` tag, or the Changelog.

**Where it goes.** Each destination has a mechanical admission test, so the choice needs
no judgement — and note that the first four all key on having *learned* something. The
fifth is the one for a hole you did **not** fill, and it is the one that used to have
nowhere to go:

| It is… | The test | Goes to |
|---|---|---|
| **measured by running our code** | can you write *"Observed:"* and then say what ran? | `observations.md`, with a required `Drains to: <file> §<section>` |
| **read in a third-party addon** | can you name the addon **and** the version/commit you read? | `mined-pending-verification.md` |
| **a verified `@verify-ingame` claim** | do you have a `[client YYYY-MM-DD]`-worthy measurement? | edit the claim in place, drop the marker, tag it |
| **a game-KB thing, not addon-dev** | would running the code change the answer? if **no**, it is not ours | `knowledge/_meta/kb-inbox.md` |
| **a hole — you looked and the KB does not answer it** | none of the above; you know the *question*, not the answer | a **marker on the claim**, in the topic file — nothing else. See **Unknowns** |

Drain what you can while you are there: **a session that reads a capture drains every
entry that capture settles.**

`wowkb.obs check` fails a `--minor`/`--major` release on anything open past 14 days —
**that gate is on answers, not on questions.** Nothing ages an open marker, deliberately.
If a correction is uncertain, say so (`confidence:`, `@verify-ingame`) rather than
overstating it.
