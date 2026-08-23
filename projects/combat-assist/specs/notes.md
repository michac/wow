# Combat Assist Plus — notes

**What this file is for:** the record of what we did — one short entry per round of work,
newest first, dated. It exists so a future reader can find out *why* something is the way it
is without re-deriving the argument. It is **not** a second spec and it is **not** a status
board.

**The fixed form. Every entry uses it, ~25–35 lines, hard ceiling 40:**

```
## YYYY-MM-DD — <short headline>

**What changed.** One or two sentences, plus the files touched as a bare list.
**Why it still binds.** The one argument a future reader must not re-derive — or, if
nothing survives, "nothing; superseded by <X>" and stop.
**Caveat.** Optional single line: what is unmeasured, what was deliberately not done.
```

**The rules that keep it flat:**

- **Past tense only. A notes entry never states a rule in normative form.** A rule lives in
  `spec.md` or the catalog; notes **cites** it. This is the rule that stops notes becoming a
  second spec, and it is the one that erodes first.
- **A reversed decision gets a one-line `⚠ SUPERSEDED:` pointer at the head of its entry**,
  not a correction buried in the prose.
- **Never quote DOCUMENT TEXT that is not in git history** — a line of `spec.md`, a catalog
  rule, a test name, a comment. This file is the historical record and an unverifiable
  quotation of our own prose is the one thing it cannot afford. If the text was only ever in a
  working tree, describe the edit instead. ⚠ **This does not cover primary sources** — what a
  player said in play, a flight report, an observation. Those are evidence, they were never in
  git and never should be, and quoting them verbatim is the point: paraphrasing a player's
  words into our own vocabulary is how a report becomes a conclusion.
- **Status does not live here.** Where the code is, what has flown, what the live version is:
  `backlog.md` → `## Status`, and nowhere else.
- ⚠ **A fact about how the game or the API behaves does not stop here.** That goes to
  `knowledge/addon-dev/` (see the wow-developer skill) — this file records *our* work, not
  the client's behaviour.
- No busted/luacheck counts, no mutation lists, no comment:code ratios, no "considered and
  declined". Cut the argument that `spec.md` and `discussion.md` already carry.
- **An entry is not permanent.** This is a log, and a log gets reset. When an entry's argument
  has landed in the file that owns it — `spec.md`, a catalog, `render-rationale.md`,
  `flight-reading.md`, `knowledge/addon-dev/` — the entry has done its job and goes. Mine
  before you delete; the deletion is the cheap half.

**The standing order is `simplify → draw → add detail from play`.**

---

## 2026-08-19 — both Warlock pilots replaced by comprehensive catalogs

**What changed.** Demonology / Diabolist and Destruction / Diabolist were re-authored from the
Tier-1 12.1 simc APLs through `authoring.md` stages 1–5, each as three files, twelve scenarios and
a registered preview. Stage 1 came first: both `rotation.md` files were still citing dead pre-12.1
profile URLs, and the Destruction APL turned out to have moved (`8ec56ea`, 2026-08-18) — the
regeneration deleted a Chaotic-Inferno Incinerate rung an earlier reading carried, and widened two
AoE gates. Files touched:

- `knowledge/classes/warlock/{demonology,destruction}/{rotation,builds,simc-apl}.md`
- `specs/demonology/{catalog,scenarios,fact-classification}.md`
- `specs/destruction/{catalog,scenarios,fact-classification}.md`
- `specs/{spec,backlog}.md`, `tools/wowkb/capart.py`

**Why it still binds.** Three findings a future reader must not re-derive.

**One unwritten S-form covers four sealed facts.** Demonic Core's stack count, Wild Imps', and
Backdraft's two-stack rung all want the same thing: a step curve on an aura **application count**,
the way S4 already runs one on a cooldown-remaining duration. cap's only aura-stack form paints a
number and is hard-limited to `min = 2`. None of these is a platform limit — the secret is a
number and §3.6 says a threshold on a secret is expressible — so the shape is named in both
catalogs' *Defeats* and deliberately not prebuilt.

**Position decides whether a transform costs a marker.** Both specs carry Infernal Bolt as an
override, from one spec-conditional Tier-1 string. On Demonology it rides the rightmost row and
outranks its left-hand neighbour, so Demonbolt needs a cross-row `identity` hold — the first
marker in any catalog to read another row's identity. On Destruction the same transform rides the
last row and its two rungs are adjacent, so it costs nothing.

**Destruction's sealed lane came out empty**, and that is a consequence rather than a virtue: no
rung reads another ability's cooldown remaining, Soul Shards are readable, and the single-target
Backdraft rungs ask whether the aura is absent rather than how many stacks. Every marker in that
catalog is a readable Lua condition — a first.

**Caveat.** Stages 6–8 did not run: no catalog Lua of the current design, no tests, no flight. Two
questions were carried back to the author rather than decided — an execute-range predicate for
Shadowburn (the same unmeasured `isUsable` read Devourer waits on), and whether Blizzard's own
`unusable` tint should count as a third eliminating signal in the reading model.


---

## 2026-08-19 — Devourer got a preview, and the virtual row got drawn

**What changed.** Devourer was registered in `capart`'s `SPECS_BUILT` and its ten scenarios
(B-1…B-5, M-1…M-5) were transcribed out of the older prose grammar into the one the scraper reads,
so `devourer-stepper.html` renders. Three mechanical things had to move for it: a *Bound abilities*
table was added to `devourer/catalog.md` (the parser reads exactly one table shape and the spec had
none), `parse_row` learned `‖` as a seam marking a **virtual row**, and the scenario-id pattern
widened to accept a one-letter prefix, which `B-n` / `M-n` needed. Files: `tools/wowkb/capart.py`,
`specs/devourer/catalog.md`, `specs/devourer/scenarios.md`, `specs/render-shelf.md` (V12 prose plus
two `preview` token groups), `previews/template/stepper.js`, `previews/template/shelf.css`.

**Why it still binds.** The preview draws a virtual row **inline in the row**, which the client does
not do — in game the panel is a separate surface and that separation is what says *cap owns this
frame*. A flat page loses the separation, so the tick carries the bit instead. That is why the tick
lives in `tokens.preview` and not in the style: `NOT_THE_STYLE` excludes the key, so the addon
cannot draw it. The seam grammar is deliberately narrow — two seams or none, panel bracketing the
Essential line — because one seam cannot say which side cap owns.

**Caveat.** The page is for **review, not record**: nothing on it has flown, and the gates prove
only self-consistency. **M-3's row was derived, not authored** — the doc had it as a prose delta on
M-2 — and every place the authoring docs doubt themselves now carries a loud `⚠ UNSURE` block on
the page rather than a footnote in the markdown. No `Catalogs/Devourer.lua` was written and no
release was cut.

---

## Before that: no entries

**Reset 2026-08-17.** The previous 28 entries, dated 2026-08-08 → 2026-08-16, were mined and
removed: their durable arguments now sit in `render-rationale.md`, `backlog.md` → `## Status`,
`flight-reading.md` and `knowledge/addon-dev/`. An empty log is this file's correct resting state
after a reset, not a defect.

The full pre-reset text, and the 18 entries before *that* which the 2026-08-08 window migration
already superseded:

```
git show 671fb68:projects/combat-assist/specs/notes.md
git show a33e152:projects/combat-assist/specs/notes.md
```

## 2026-08-22 — Demonology built, and three sealed-display primitives promoted

`Catalogs/Demonology.lua` of the current design ships: nine entries in the authored priority
order, transcribed from `demonology/catalog.md`, with fourteen scenarios in `scenarios.md`.
`authoring.md` stages 6 and 7 have run; stage 8 has not. The pilot is gone from the addon, and the
engine specs that had been riding it now ride `tests/fixtures/engine_catalog.lua` instead — an
engine guarantee that rests on a shipped roster breaks the day that roster is authored.

Four treatments left `render-shelf.md` Part 7 to make it possible, as **V16** (the banded count
and its mark), **V17** (the complement), **V18** (the sealed radial) and **V19** (the refresh
window). `composites` was deleted rather than promoted: it was the argument that those four
compose on one row, and its subject is now a real spec's walk. `duration_band` stays.

Three things worth remembering:

- **Nothing new was learned about the client.** Every measurement was in hand on 2026-08-21. What
  was in the way was that a catalog may not cite a lab entry, so the fact was expressible and
  unusable at the same time. Promotion is a pipeline step and it was the whole cost.
- **A sealed fact can now eliminate a row.** The reading model has three eliminating signals
  instead of two, and `capart check`'s elimination gate knows about the third explicitly. That
  closed `demonology/catalog.md`'s second defeat and made DEM-13 and DEM-14 writable.
- **`player-aura-stacks`'s `min = 2` was never a platform limit** — it is what the client does
  when no formatter is passed. The kind is retired; Destruction's Backdraft migrated mechanically
  and draws exactly what it did.

Two defects the work surfaced and fixed, neither of which had a symptom: a container display
carrying a readable gate armed **nothing at all** (`Overlay.configure` tested `not marker.when`,
and only the graded path consumed `verdict.gates`), and V14's `tint: "lane"` meant the one
primitive whose whole advantage is being neutral was the one going unguarded by the tint guard.

## 2026-08-22 — v0.12.0 drew nothing, and a pure suite could not have caught it

The Demonology flight got no flight: cap loaded, Anchor re-ordered the viewer, and **not one
pixel drew** — no badges, no scan edges, no hatches, no keybind labels.

`wowkb.capture cap tier` named it in one line:
`# listener-error i:3 Overlay.lua:232 attempt to call a nil value`. `badge:SetPoint` does not
exist. `Paint.Badge` returns a plain TABLE with `Show`, `Hide` and `Step`, and the flowing badge
stack (2026-08-19) started re-anchoring through a method nobody added.

**It shipped invisible for three days because the only catalog anyone ran declared no cues.** The
Demonology *pilot*'s two markers carried none, so `wanted` was always empty and the stack loop
only ever reached its `badge:Hide()` branch. The first catalog with cues took the whole of
`paint()` down on its first row — and `Sense.fireVerdicts` pcall-protects its listeners by
design, so the error reached the capture and nobody's screen. Havoc and Retribution would have
hit it identically; neither had flown since.

Three things worth keeping:

- **A pure suite is structurally blind to this.** `mock_ns.lua` is right that nothing needing a
  `CreateFrame` stub belongs in it, and the consequence is that no test here can ever construct a
  badge. So *cap calling a method its own constructor does not define* had no guard at all.
  `tests/spec/engine/surface_spec.lua` is that guard and it is deliberately **textual** — it
  checks the source, because there is nowhere else to check.
- **The protective pcall is correct and it is also what hid this.** A bare error on the 10 Hz
  tick re-throws forever, so the guard has to be there; what it costs is that a total draw
  failure looks like silence. The capture is the only thing that closed the gap between "nothing
  works" and a file and a line — which is the whole argument for the capture standard.
- **The reachability, not the code, was the risk.** The call was wrong the day it was written;
  what changed was a catalog declaring a cue. A branch no shipped data reaches is untested no
  matter how many tests pass.
