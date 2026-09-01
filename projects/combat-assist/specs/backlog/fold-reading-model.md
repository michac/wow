# The folded row's reading model

**What this file is for:** the plan for one committed backlog item. `backlog.md` → `## Now`
carries the one-line entry that points here; this file holds the question, the steps and the
traps. It is deleted when the work lands and `notes.md` records the round.

**The author decision is MADE (2026-09-01) and only the mechanical half is left** — the gates,
step 3. This file is deleted when they land and `notes.md` records the round.

## The decision — MADE 2026-09-01

**A folded row reads like a book: the whole top line, then the whole bottom line.** One walk,
priority order continuing across the break. The author's call, from play, and it is recorded in
`render-shelf.md` Part 0.5 → *The fold*. The rejected alternative (bottom row is the scan, top row
a shelf you check) would have made Part 0.5 two procedures and re-opened every treatment under it.

**Both shipped catalogs that bet on this survive unedited** — Retribution's interleave badge still
walks past Divine Toll; Protection's absent `overcap` cue is still justified because the walk
still reaches the four generators after Shield of the Righteous. That second one was the reason to
decide rather than default: a missing cue is invisible, so nothing would have said it broke.

**The origin, now recorded in the shelf:** the break is a **width** fix. Several specs' CDM rows
were getting awkwardly wide, raised during the EllesmereUI anchoring work. The
top-cooldowns/bottom-rotation meaning came after and is binding on future breaks.

⚠ **What the decision does NOT dissolve.** The top line is walked first on every scan and its
icons are eliminated most of the time — the author's *"I'm always paying the scan tax when I
don't [need them]"*. That is not a reading-model defect; it lands on V11's hatch, and it is
`backlog.md` → *The hatch is paid on every scan*. Demoting the cooldowns was considered by the
author and rejected: it strands the rotational buttons instead.

⚠ **One residual, answerable only in play, not blocking:** the break sits directly in front of a
gold positive cue in two specs (Demonology's `implosion`, Havoc's `immolation_aura`). Pass 1 is
meant to make position irrelevant — does heading its own row help or hurt? Fold it into the next
session on either spec.

**Steps 2 and 3 below are now unblocked, and step 2 is DONE:** Part 0.5 carries the fold, Part 2.5
was checked and does not move (composition is per row), and `havoc/catalog.md:10` no longer says
"single-row". **What remains is step 3, the gates.**

## Step 2 — the shelf — DONE 2026-09-01

- **Part 0.5 gained the fold** — a *The fold* subsection carrying the decision, the width origin,
  and the two catalog bets it preserves; the two-pass block now says both passes read a folded row
  like a book.
- **The treatments below were re-judged** against it. None moves: the fold decides where a row
  sits and every treatment is per row.
- **Part 2.5 was checked and does not move**, and says so in one line so the check is not
  repeated.
- **`havoc/catalog.md:10`** no longer calls its walk "single-row".

## Step 3 — the gates (the expensive half)

⚠ **`break_before` appears in `capart.py` EXACTLY ONCE — line 1330, where it is copied into the
exported Lua — and no gate reads it.** Every preview renders one strip, so `capart check --all`
being green says nothing whatever about the fold. This is a live gap today, not a future one.

The row grammar is one-dimensional at its root:

- **`parse_row` (`capart.py:600`)** returns a flat `list[dict]` and discards its boundaries.
- ⚠ **Its `SEAM` is already spoken for and means something else.** A seam marks a **virtual
  row** — a cap-owned icon with no Cooldown Manager frame — and the parser accepts **exactly two
  seams or none**, dying on any other count because one seam cannot say which side cap owns. A
  fold is a *third* kind of boundary that this grammar refuses by construction. Do not try to
  express it as a seam.
- **`elimination_gate` (`:4788`)** walks the flat list, so it asserts "the leftmost entry that is
  neither swiped nor negative is the press" over a shape the client no longer draws.
- ⚠ **`density_gate` (`:4924`) takes a literal prefix slice, `sc["row"][:press]`** — **the one
  place a naive 2-D change breaks silently**, because a slice across a row boundary counts skips
  the eye never crossed.
- **`scenarios.json` is a second producer** that bypasses `parse_row`, so its schema is part of
  the change.
- ⚠ **The break does not travel.** `break_before` lives in `catalog.json` / `Catalog.lua`; the
  gates read `scenarios.json` / `scenarios.md`, and the two have no shared notion of it. Either
  the break travels into the scenario row, or it is re-authored in the scenario grammar.

The funnel is narrow — `_check_one` → `reading_gate` → the three sub-gates, about **5–6 call
sites** — so the work is bounded. What makes it expensive is that each gate has to be told which
reading model it is enforcing, which is why it waits on step 1.

## Done when

- ~~The decision is recorded in `render-shelf.md` Part 0.5 and the question is deleted from
  `discussion.md`.~~ **DONE 2026-09-01.**
- ~~The treatments under Part 0.5 have been re-judged, and the shelf has an entry for the break.~~
  **DONE 2026-09-01.**
- ~~Under SHELF only: Retribution's interleave badge and Protection's absent `overcap` re-argued.~~
  **MOOT** — the answer was the book read and both survive unedited.
- [ ] A gate reads `break_before` and fails a scenario whose press is not what the book read
      reaches first.
- ~~`havoc/catalog.md:10` no longer says "single-row".~~ **DONE 2026-09-01.**
