# Combat Assist Plus — project root

`/cap` is a Retail / Midnight combat-assistance addon that extends Blizzard's Cooldown
Manager. It is a standalone companion app, not part of the gameplay KB.

Read `specs/spec.md` before changing behavior. One rule there outranks the rest, and it is a
platform fact rather than a stance: **cap never branches on sealed data** (§3.6). `Catalog.lua`
and `Channel.lua` hold that line in code.

The boundary constrains what cap *compares*, never what it *shows* — be optimistic about carrying
APL logic (`spec.md` §3.6's ladder). A claim of impossibility in any `specs/**` file follows
`authoring.md`'s "How to write a defeat": scenario, failing rung, reopening condition — never a
bare "cannot".

The addon source is `addon/`, a separate gitignored repository with its own `CLAUDE.md`.

## Project documents

Eight permanent files have eight jobs:

| File | Owns |
| --- | --- |
| `specs/spec.md` | Approved player-visible behavior and product boundaries. |
| `specs/backlog.md` | The only implementation-status block and the ordered work list. |
| `specs/authoring.md` | The process: the stages a new spec walks, with entry/exit criteria. |
| `specs/render-shelf.md` | Every visual opinion: surfaces, primitives, colors, motion, placement. |
| `specs/render-rationale.md` | Why the shelf says what it says: alternatives, reasoning, rejects. |
| `specs/notes.md` | Short dated records of completed rounds. |
| `specs/discussion.md` | Only unresolved product questions requiring an author decision. |
| `specs/flight-reading.md` | How to interpret the capture format the current source emits. |

`specs/pattern-shelf.md` is the recipe reference `authoring.md` stage 3 classifies against.

**The two shelves.** `pattern-shelf.md` = which facts you may use. `render-shelf.md` = how you may
show them. **Visual opinions belong in the render shelf and nowhere else** — `spec.md` fixes the
*model* (role lanes, readable-vs-sealed) and says nothing about pixels. Trying a
new look is an edit to the shelf, not a spec amendment; regenerate the preview from it and look.

**The shelf declares, the rationale explains.** `render-shelf.md` states exactly **one** style —
one treatment per primitive, present tense, no alternative beside it — and every number it draws
with lives in its Part 6 `render-tokens` JSON block, cited from prose by path and never restated.
Alternatives, reasoning and rejects go to `render-rationale.md`, which has no authority. Regenerate
with `uv run python -m wowkb.capart build <spec>`; never hand-edit the preview. **Every spec's
preview is a uniquely named file in the one `previews/` directory, served by one `wowkb.serve` on
one port** — a new spec needs no new server. Serving details: `previews/CLAUDE.md`.

**…and Part 7 is the lab, which decides nothing.** Everything above Part 7 is the style; nothing
below it is. The lab exists because the one-style rule made *trying* something expensive — the only
way to see an idea was to overwrite the declared style and remember to put it back. A lab entry
renders in its own section of the preview and may be drawn by the in-game `/cap style` gallery
(cap-owned frames, not a live row — you cannot judge a treatment without watching the client draw
it), but **never in a CDM row**: it reaches the addon only as `ns.LabStyle` in the generated
`Lab.lua`, and `capart check`'s reach gate fails if anything but the gallery names it. And
**nothing in `verdicts` or
`cues` may reference it** (`capart build` errors if it does, which is what keeps an experiment from
quietly becoming load-bearing). A treatment leaves the lab by being **moved** into Parts 1–6, never
by being cited from there. Each entry carries an `asks` — the question it exists to answer.

**The lab's contents change constantly and are not listed here** — run
`uv run python -m wowkb.capart export lab`, which prints every entry, or read Part 7. A count in
this file goes stale the first time anyone tries an idea, and a stale inventory of an
explicitly-provisional thing is worse than none. The families as of 2026-08-19 are `hotkey-*` (V15 font
candidates), `arrival-*`, `ready-*`, `blaze-*` (badge-scale promotion candidates) and
`procglow-*` (icon-scale ones).

⚠ **A lab entry can leave without emptying its family:** V13's scan edge was promoted out of the
`ready-*` set on 2026-08-19 and the other three stayed, because they are the alternatives it was
picked over and Part 5 question 2 is what settles that choice in the client. The same happened to
the `blaze-*` family when V14 was promoted out of it.

**Promotion has gone the other way too, and twice it took a whole family with it.** The stripe
family's `stripes-l4-cooldown` became **V11** on 2026-08-16 and *took the shared stripe sheet with
it* — the sheet is now `tokens.hatch` and ships to `Media/stripes.tga`. Then on **2026-08-19 V11
was generalised from "on cooldown" to "ruled out"**: a row wearing **any** cue whose polarity is
negative stripes, in cap's own red, which is Part 0.5's pass 2 drawn rather than merely stated.
That one rule answered both surviving stripe entries at once, so `stripes-l3-hold` and
`stripes-l5-starved` were promoted and deleted together and the family is now empty.

**V14 · Promotion ring** left the same day: a ring around the badge of a row wearing a positive
cue, generated by `wowkb.procring` against four properties MEASURED off Blizzard's own proc glow
(it does not pulse; it never covers the icon; its falloff is asymmetric; the band sits at a
measured radius). Its sheet moved to `Media/procring.tga` on promotion, exactly as V11's did. The
four `blaze-*`/`procglow-*` candidates it beat stay in the lab as the alternatives.

The lab's first two entries were promoted on 2026-08-13 and deleted from it
(`backlog.md` → `## Status`); an empty lab is its correct resting state, not a defect. A new idea
gets a `lab` key, an `asks`, and a section in Part 7.

`specs/simplification-plan.md`, `specs/simplification-audit.md` and `specs/rule-split-audit.md`
are temporary migration artifacts. They are not additional product authorities.

The live addon version comes from `wowkb.addon list`. What is built or flown comes only from
`specs/backlog.md` → `## Status`.

If behavior is not in `spec.md`, put it in `backlog.md` → `Ideas` or ask before building it.
A question leaves `discussion.md` when decided. Record completed work briefly in `notes.md`.

## Working on addon code

Read the workspace `wow-developer` skill and its `references/house-rules.md` before editing
Lua, XML or the `.toc`.

Client facts belong in `knowledge/addon-dev/`, not in product docs or source comments. A
marked unknown that would be load-bearing is a stop-and-ask under that skill.

Before touching the gitignored addon checkout, run `wowkb.addon pull --all`. Captures leave
the addon only through `wowkb.capture cap <stream>`; SavedVariables flush on `/reload` or
logout. `specs/flight-reading.md` describes what each current stream can and cannot prove.

Tests protect mechanical and platform guarantees.

## Authoring another spec

**`specs/authoring.md` owns the process** — eight stages with entry/exit criteria, from grounding
the rotation KB through transcription, tests and the flight. Read it before starting a spec; do
not re-derive the route here or restate it in a backlog phase header.

The two rules it is easiest to violate on day one: **a spec-and-hero pair is the unit** (a second
hero tree is a separate catalog, not an overlay), and **three files per spec directory** —
`catalog.md` (the definition), `scenarios.md` (the walk that proves it), `fact-classification.md`
(the readable/sealed/open safety case). Havoc is the model; `authoring.md` §0 owns the split.

Gameplay choices remain in `Catalogs/<Spec>.lua` and the matching `specs/<spec>/catalog.md`;
unknown-safe evaluation remains in `Signal`, and pixels remain in shared treatment/overlay
code. Fly the player judgment before reading captures.

## Releasing

Releasing is always ask-first. A push alone does not reach the game; deployment installs the
latest GitHub release.

```bash
cd ~/code/fun/wow/tools
uv run python -m wowkb.addon release cap [--patch|--minor|--major]
```

After a release is cut and deployed, `wowkb.addon` prints a reminder to run the `cap-conscience`
review (`.claude/agents/cap-conscience.md`). It is read-only, blocks nothing, and its output is
questions for the author. Do not run it mid-authoring — it reviews a shipped catalog, and running
it against work in progress is what the split it came from was written to prevent.
