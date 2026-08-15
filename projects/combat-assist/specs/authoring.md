# Combat Assist Plus — authoring a spec

**What this file is for:** the pipeline a new spec walks, from "we want to support X" to a flown
catalog — as stages with **entry** and **exit** criteria. It is the single home of the *process*.
It owns no gameplay opinion, no player-visible behavior and no status.

Everything here is downstream of `spec.md` §1. Where a stage restates a rule, the cited section
is the authority and this file is the reminder of *when* it applies.

**Who owns what.** `spec.md` owns approved behavior. `pattern-shelf.md` owns the recipes
(`R1`…`R10`, `S1`…`S6`, the Part-3 seams) and their `knowledge/addon-dev/` evidence.
`backlog.md` → `## Status` owns what is built and what has flown. `notes.md` owns dated history.
`discussion.md` owns undecided product questions. This file owns the order the work happens in.

---

## 0. The unit, and the file layout

**A spec-and-hero pair is the unit cap authors.** Havoc / Fel-Scarred is one catalog; Havoc /
Aldrachi Reaver is a *separate catalog authored later*, not a second overlay bolted onto the
first. Two hero trees that genuinely share a roster can share one document; the moment a row
needs "…unless Aldrachi Reaver", it is two catalogs.

**One `catalog.md` per spec directory.** `specs/<spec>/catalog.md` is the normative document —
the thing `Catalogs/<Spec>.lua` transcribes. A spec that grows a second or third design file has
grown a consolidation debt, not a richer design. (Havoc did exactly this: `catalog.md` +
`fact-classification.md` + `scenarios.md`, with a standing owed item to fold them back.) If a
section genuinely needs to be drafted separately while thinking, fold it in before the stage
exits.

**The priority order lives in the gameplay KB**, `knowledge/classes/<class>/<spec>/rotation.md` —
not in the catalog. The catalog cites it. Two copies of a priority list drift, and the KB copy is
the one with front matter and provenance.

**Docs lead artifacts, always.** A published artifact (concept overview, scenario stepper) is a
*rendering* of a doc, never a source. Edit the doc first, then regenerate the artifact from it.
Never let an artifact drift ahead of the document it renders — a reader who trusts the artifact
then has no way to find out they are wrong.

---

## 1. Ground the rotation (entry stage)

**Entry:** a spec has been chosen and there is a reason to author it.

Bring `knowledge/classes/<class>/<spec>/rotation.md` and `builds.md` up to the live patch first,
from the authoritative APL — simc default (`wowkb.simc`, Tier 1) plus the live class-guide
priority, re-verified with a date. Author against a *current* priority or the whole design
inherits the error.

**Exit:** `rotation.md` + `builds.md` carry the live patch, a `reviewed:` date, and the priority
order has been re-checked against a named source on a named day.

---

## 2. Name the player problems

**Entry:** stage 1 exit.

Walk the priority and, for each ability, name **the player problem a hint would solve** — the
thing the player gets wrong or has to hold in their head. An ability with no named problem gets
no row. This is the filter that keeps a catalog from becoming a roster dump.

Then walk the priority as a **dependency graph**, not a flat power list: each press's rank is set
by *why* it belongs there — a reset it grants, a window it opens, a buff it maintains, a resource
it needs — and that reason often rests on the readable state of a *different* ability
(`spec.md` §3.1, the readable-relationship rule). The walk is what surfaces the complete cue set
and the honest gaps.

**Exit:** a problem-per-row list, and for each row the ordering-reason behind its rank.

---

## 3. Classify every fact

**Entry:** stage 2 exit.

Enumerate only the facts those rules require, and tag each one against `pattern-shelf.md`
Parts 1–2 (`spec.md` §3.6 is the boundary):

- **readable** — Lua may compare, index, add or truth-test it. Drives emphasis tiers and readable
  markers.
- **sealed-display** — forwarded to a client-owned sink only. Never compared, indexed, added or
  truth-tested. cap reports `offered` / `armed` / `refused` and never reads back.
- **open** — unmeasured, or no API. Produces **no hint**.

Every tagged fact points at its recipe and that recipe's `knowledge/addon-dev/` evidence. A fact
with no recipe is either a new Part-3 seam (stage 6) or an open fact (stage 5).

**A threshold on a secret is expressible**, in either polarity, as an authored curve the client
evaluates (`spec.md` §3.6) — the platform seals the *value*, not a break point authored against it.

**Exit:** every fact the catalog consumes carries a lane, a recipe and its evidence. No sealed
fact appears in a proposed Lua condition.

---

## 4. Map facts to treatment

**Entry:** stage 3 exit.

Author readable facts into the role lanes (COOLDOWN / ROTATION / FALLBACK, `spec.md` §3.1) and
readable markers. Author sealed facts as independent **cues** into an existing client-owned sink.
Open facts produce nothing.

**Name cues, do not draw them.** A catalog says *which* cue a row carries; `render-shelf.md` says
what that cue looks like. If the cue needs a primitive the shelf does not have, add the primitive
*there* (status `candidate`) rather than describing pixels in the catalog — otherwise the
vocabulary forks again.

Then prove the design reproduces the priority: walk realistic game states and, for each, name why
the eye lands on the one press the rotation would choose — including, for **every button that is
available and skipped**, the reason it is skipped. Buttons the CDM already rules out natively
(the swipe) need no explanation; the available-but-skipped ones are exactly where the cues earn
their place or the gaps show.

**Exit:** a normative `catalog.md`: roster → lane, the cue set, the recipes each row consumes,
and a state walk that reproduces the order.

---

## 5. Route the open facts

**Entry:** stage 4 exit, which has named them.

Each open fact becomes an `@verify-ingame` marker on the claim, or a ClientLab
`@pending-test: <id>` once a test exists (`projects/addon-lab/docs/lab-process.md`). An unknown
is recorded **as a marker on the claim**, never as a line in a tool or a TODO in the catalog.

**A load-bearing open fact is a stop-and-ask** (`spec.md` §3.6). Rows that do not depend on it
proceed; the row that does ships without that hint until the marker drains.

**Exit:** every open fact carries a marker; the catalog states, per row, what ships now and what
waits.

---

## 6. Transcribe

**Entry:** stages 4–5 exit, and the addon checkout is current (`wowkb.addon pull --all`, and
check `wowkb.addon list` → `drift`; a stale worktree transcribes against dead vocabulary).

Transcribe `catalog.md` into `Catalogs/<Spec>.lua` against the *real* current source vocabulary,
add it to the `.toc` and register it. Resolve override spell IDs via `overrideSpellID` at bind
(R7); never hardcode a transform's ids.

**Gameplay choices stay in the catalog. Unknown-safe evaluation stays in `Signal`. Pixels stay in
shared treatment/overlay code.**

**The renderer test** (`pattern-shelf.md` Part 3, the marker seam — the definition-of-done for
`backlog.md` → Phase 9.4)**:** a spec that reuses an existing tier
and an existing marker/channel shape **edits nothing** in `Treatment.lua` / `Overlay.lua` — it is
authored purely as catalog data. A renderer edit means the slice introduced a new marker shape or
channel pairing. Write a shared helper when this slice needs one.

**Exit:** the catalog loads, binds and fails inert with no catalog, no matching build, an unsafe
read or an unsupported binding.

---

## 7. Test what tests can know

**Entry:** stage 6 exit.

Extend the `busted` suite for the *mechanisms* the slice added: provider seeding and re-seed on
transform flip, curve guards, marker union across the readable and sealed lanes, unknown-safe
propagation. Keep spec examples in an explicitly provisional characterization group, separate
from engine guarantees.

**Exit:** the release runner's suite passes.

---

## 8. Fly it

**Entry:** stage 7 exit, plus **release approval** — releasing is always ask-first, per the
project `CLAUDE.md`. A push alone does not reach the game.

`spec.md` §6 owns this: state **one** player-experience question before the flight, play first,
record the player's report in their own terms. Read captures **afterward**, only to explain which
route armed and why the observed result may have happened.

Captures never overrule the player's visual judgment: **accepted is not drawn**
(`pattern-shelf.md` Part 2). Occupancy and refusal rates are diagnostics, not acceptance quotas.
`flight-reading.md` says what each stream can and cannot prove. SavedVariables flush only on
`/reload` or logout.

Change one conceptual variable at a time, and ask at every product judgment.

**Exit:** a player judgment recorded, `backlog.md` → `## Status` updated to say what flew, and a
dated entry in `notes.md`. After the release is cut, the `cap-conscience` review runs and reports
to the author; it holds no write tools, blocks nothing, and its output is questions.

---

## Standing rules (not stage-bound)

- **Status lives in one place.** `backlog.md` → `## Status`. Never assert in prose what is built,
  flown or released; never hardcode an addon version — run `wowkb.addon list`.
- **Client facts live in `knowledge/addon-dev/`**, not in product docs and not in source comments.
- **An open fact is a marker on the claim**, and a load-bearing marked claim you are about to
  build on is a stop-and-ask.
- **Docs lead artifacts** (§0). Regenerate; never hand-edit an artifact ahead of its doc.
- **Visual opinions live in `render-shelf.md`**, never in `spec.md`, a catalog, or the renderer's
  source. A look you want to try is a shelf edit — no permission needed, no spec amendment.
- **The shelf declares, the rationale explains.** `render-shelf.md` states one treatment per
  primitive, with every number in its Part 6 token block and prose citing paths into it.
  Alternatives, the reasoning behind a choice, and what was tried and rejected go to
  `render-rationale.md`, which is authoritative over nothing. A second option written into the
  shelf is a bug: the artifact generator renders a style, and cannot render a debate.
- **Ask before building behavior that is not in `spec.md`** — it goes to `backlog.md` → `Ideas`
  or to `discussion.md`, not into the source.
- **Do not prebuild vocabulary.** No aura/totem duration, target-aura, APL-DSL or
  capability-registry work until a spec that needs it is being authored.
- **Releasing is ask-first**, every time.

## Where a thing gets written

| The thing | Its home |
| --- | --- |
| Priority order, talents, gearing | `knowledge/classes/<class>/<spec>/` |
| A measured client fact | `knowledge/addon-dev/` |
| A recipe and its evidence | `specs/pattern-shelf.md` |
| What a cue looks like — art, color, motion, placement | `specs/render-shelf.md` |
| Why it looks that way — alternatives, reasoning, rejects | `specs/render-rationale.md` |
| A spec's roster, lanes, cues, state walk | `specs/<spec>/catalog.md` |
| Approved player-visible behavior | `specs/spec.md` |
| What is built / flown, and the work list | `specs/backlog.md` |
| An undecided product question | `specs/discussion.md` |
| What we did, dated | `specs/notes.md` |
| How to read a capture | `specs/flight-reading.md` |
| The order the work happens in | this file |
