# The folded row's reading model

**What this file is for:** the plan for one committed backlog item. `backlog.md` → `## Now`
carries the one-line entry that points here; this file holds the question, the steps and the
traps. It is deleted when the work lands and `notes.md` records the round.

**It is blocked on ONE author decision** that cannot be made from the code, and everything
after that decision is mechanical. Do not start the mechanical half first — the gate work
*encodes* the answer.

## The question

`render-shelf.md` Part 0.5 defines the whole interaction as a two-pass walk:

```
pass 1 — scan left to right for a POSITIVE cue. If one is present, press it.
pass 2 — scan left to right, skipping swiped / red-cued / hatched items.
         press the first item that survives.
```

It says **left to right**. Since 2026-09-01 the row folds — four catalogs author a break, and
Retribution, Protection, Havoc and Demonology all draw two lines in a real client. The procedure
does not say what a second line means.

**What is already settled and is not up for discussion:** the fold's *meaning*. The top row is
the cooldowns, the bottom row is the rotation presses. That is a constraint on future breaks,
not a description — `backlog.md` → `## Status` carries how it was arrived at.

**What is open is what the eye does:**

- **WRAP** — the fold is a line break. One walk, top-left to bottom-right, priority continuing
  across it. Part 0.5 gains a sentence; the gates learn a seam.
- **SHELF** — the bottom row *is* the scan; the top row is a thing you check rather than walk.
  Two reads, not one wrap, which makes Part 0.5 two procedures and re-opens every treatment
  underneath it.

## Why this is not cosmetic — two shipped catalogs already bet on the answer

⚠ **Both bets were made while the row was one line, and neither author knew they were betting.**

**Retribution buys its whole interleave with one badge.** `retribution/catalog.md:194-196`:
*"elimination walks past Divine Toll and lands on the spender."* Divine Toll is now the **last
icon of the top row** and Templar's Verdict the **first of the bottom**. Under WRAP the argument
stands exactly as written. Under SHELF you never walk past Divine Toll — you start at the
spender — so the badge buys nothing and the interleave is correct *by accident*, which stops
being correct the next time the order moves.

⚠ **Protection justifies an ABSENT cue, and that is the dangerous one.**
`protection/catalog.md:526-528`: *"every generator in this catalog … sits below Shield of the
Righteous at position 3, so at cap the walk stops on the spender and never reaches them."* All
four generators are on the bottom row; SotR is on the top. Under SHELF the walk **starts** among
those generators and reaches them *before* SotR — the ordering that made the cue unnecessary is
inverted. **A missing cue is invisible.** Nothing on screen will say the argument stopped
holding, and no gate will either.

**And one more the same session answers.** The break sits directly in front of a gold positive
cue in two specs — Demonology's `implosion`, Havoc's `immolation_aura`. Pass 1 exists to make
position irrelevant when a positive cue is up. Does putting that cue at the head of its own row
help it or hurt it?

## Step 1 — the decision (the author's, in a client)

Three falsifiable observations, one session. What is wanted back is **which way the eye actually
went**, not a verdict on the design.

| Spec | State | The question |
| --- | --- | --- |
| Protection | 5 Holy Power, in a pull | SotR is lit on the top row; four unbadged generators sit on the bottom. **Which do you reach for?** A hand that goes to a generator says the absent `overcap` cue is a real defect, and says SHELF |
| Retribution | 5 Holy Power | Divine Toll wears `overcap` as the last icon of the top row; the spender is first on the bottom. **Do you experience skipping past it, or do the rows read as unrelated lists?** |
| Demonology *or* Havoc | the gold cue up | The positive cue is the first icon of the bottom row. **Does the fold make it easier or harder to see before you start eliminating?** |

⚠ **WRAP-and-change-nothing is a legitimate outcome and probably the likeliest.** If the eye
wraps, both catalog arguments survive untouched and this item collapses to a Part 0.5 sentence
plus the gate work below. The three presses are worth running anyway, because the two arguments
above are the ones that would break *quietly* if the guess went the other way.

## Step 2 — the shelf (only after step 1)

`render-shelf.md` Part 0.5 owns the procedure and names itself as the thing to edit when a
flight says the scan is wrong. It is the one file that may hold a visual opinion.

- **Part 0.5 gains the fold.** It is single-line about direction today and does not admit a
  second row exists.
- **Re-judge the treatments below it against the new version**, which is what Part 0.5 says to
  do rather than tweaking each treatment on its own.
- **Part 2.5's z-stack cites the reading model by name** and is composed per row; check whether
  a fold changes anything about composition (it probably does not — this is a check, not a
  predicted edit).
- ⚠ **`render-shelf.md` has no entry for the row break AT ALL.** The file that owns every visual
  opinion is silent about a visual change that shipped in four specs.
- ⚠ **`havoc/catalog.md:10` still calls its scenarios a *"single-row … elimination walk"***.
  Havoc draws two rows. Fix as this passes.

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

- The decision is recorded in `render-shelf.md` Part 0.5 and the question is **deleted** from
  `discussion.md` (its charter: a decided question leaves, it does not get a resolved section).
- The treatments under Part 0.5 have been re-judged against it, and the shelf has an entry for
  the break.
- Under SHELF only: Retribution's interleave badge and Protection's absent `overcap` are
  re-argued or re-authored, because both currently rest on WRAP.
- A gate reads `break_before` and fails a scenario whose press is not what the declared reading
  model reaches first.
- `havoc/catalog.md:10` no longer says "single-row".
