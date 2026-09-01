# Combat Assist Plus — open questions

**What this file is for:** product questions that still require an author decision. It holds
the smallest live options and what would decide between them. Approved behavior belongs in
`spec.md`; agreed work in `backlog.md`; completed reasoning in `notes.md`.

**A question leaves this file when it is decided.** It does not get a strikethrough, a "resolved"
section, or a note saying what it used to be — the decision goes to whichever file owns it and the
question is deleted. A file of closed questions is a file nobody reads, which is how three settled
questions came to sit here asserting rules the code no longer followed.

> **Numbering restarted at D1 on 2026-08-17.** The previous series ran to D26 and is fully closed.
> `notes.md`, `backlog.md` and `flight-reading.md` still cite numbers from it — **those references
> mean the pre-reset series**, not anything below.

---

## Closed questions

The Havoc pass of 2026-08-17 closed the last three, all of them against the 12.1 simc APL that
arrived that day:

- **The Hunt's hold** was inverted, not merely too broad — the APL *casts* The Hunt when
  Metamorphosis is ready. It is now two sealed bands (Eye Beam far, Metamorphosis near), gated on
  Eternal Hunt. The separate suspicion that readiness was stuck `true` is gone too: readiness
  stopped being a latch on 2026-08-16 and became a read.
- **The uncountable charge spell** resolved to positive-only. The below-max `blocked` badge is
  deleted; the gold badge stays, gated on the talents that create a charge worth losing.
- **Immolation Aura's rank against Chaos Strike** was waiting on exactly one thing — a 12.1 APL —
  and got it. Immolation Aura sits above Chaos Strike at rung 20, with a skip badge carrying the
  single-target case.

**2026-08-28 — V21 occluded by the cue that made it necessary.** Cue K's condition
(`identity(grimoire, "transformed")`) and V21's gate (`baseoncd(grimoire)`) are the same window,
so the red disc covered the countdown for the whole of it. The four options written down were all
about *which of the two wins*. The answer was a fifth: **neither — they are one statement**, so
`blocked` draws the cooldown it is held on and the frozen clock glyph is not drawn at all. See
`render-shelf.md` V5.1 and V21, and `demonology/catalog.md`'s changelog for the same date.

An empty file is this file's correct resting state, not a defect — but it is not empty now:
the question below is open.

## A folded row — does the scan wrap, or does the bottom row own it?

*Raised 2026-09-01, by four catalogs authoring a break and the row flying two-high.*

Part 0.5's procedure says **scan left to right**. A folded row is two lines, and the procedure
does not say what that means. Correction 10 settled what the fold *means* — top row the
cooldowns, bottom row the rotation presses — and that is a constraint now. It does not answer
what the eye *does*.

**The two answers, and they are not cosmetic:**

- **WRAP.** The fold is a line break. One walk, top-left to bottom-right, priority order
  continuing across it. Part 0.5 barely changes; the gates learn a seam.
- **SHELF.** The bottom row is the scan; the top row is a thing you check, not walk. Two reads,
  not one wrap — which makes Part 0.5 two procedures and re-opens every treatment under it.

**What decides it is not taste — two shipped catalogs already bet on the answer:**

- **`retribution/catalog.md:194-196` buys its whole interleave with one badge**: *"elimination
  walks past Divine Toll and lands on the spender."* Divine Toll is now the **last icon of the
  top row** and Templar's Verdict the **first of the bottom**. Under WRAP the argument stands.
  Under SHELF you never walk past Divine Toll — you start at the spender — so the badge buys
  nothing and the interleave is right by accident, which is the kind of right that stops being
  right the next time the order moves.
- ⚠ **`protection/catalog.md:526-528` justifies an ABSENT cue** with *"every generator sits below
  Shield of the Righteous… at cap the walk stops on the spender and never reaches them."* All
  four generators are on the bottom row; SotR is at position 3 on the top. Under SHELF the walk
  **starts** among those generators and reaches them *before* SotR — the ordering is inverted and
  the reason the cue was never authored is gone. **A missing cue is invisible**: nothing on screen
  will say the argument stopped holding.

**And one more the same session answers.** The break sits directly in front of a gold positive cue
in two specs — Demonology's `implosion`, Havoc's `immolation_aura`. Pass 1 is meant to make
position irrelevant when a positive cue is up. Does putting it at the head of its own row help
that, or hurt it?

⚠ **No gate models the fold, so `capart check --all` says nothing about any of this.**
`break_before` appears in `capart.py` exactly once — line 1330, emission — and no gate reads it;
`parse_row` returns a flat list and discards its seams, and every preview renders one strip. The
gate work is real (~5–6 call sites, plus `scenarios.json` as a second producer, plus making the
break travel from `catalog.json` into the scenario grammar) and it **encodes the answer**, so it
waits on the decision rather than the other way round.

## Devourer — is Vengeful Retreat worth binding at all?

*Raised 2026-08-19, by the shelf's V13 collapse.*

`devourer/catalog.md` §6 binds Vengeful Retreat with **no cue**, and the reason it gave was that
the lane border said *"this is a cooldown-class button"* in cap's own vocabulary. The scan edge
does not say that — it is one bit and carries no category, and since 2026-08-25 the model
holds no category either — so that argument is gone.

Two things make the question sharper rather than academic:

- Vengeful Retreat is in the **Utility** category. `Anchor.lua` orders the **Essential** viewer
  only and the reading model walks only that, so a scan edge on this row marks membership in a
  scan that never happens. It is the one place in cap where the edge is drawn and means nothing.
- The only real signal the binding still buys is **V11's cooldown hatch**, which does say *not
  now* and says it without the walk reaching the row. Whether that alone is worth binding a row
  outside the scanned line is a product call.

**The two answers, either of which is fine:** bind it for the hatch and say that is why; or
unbind it and let Blizzard's own swipe carry the row, which is what it does on every other Utility
button today.

⚠ **Half of this question was settled on 2026-08-31 and the other half was not.** `spec.md` §1's
principle (c) — the order and the augments are one product, so cap draws nothing on a row it did
not order — answers the sub-question this used to carry: **yes, the scan edge should be suppressed
outside the scanned viewer**, for exactly the reason given above, that it marks membership in a
scan that never happens. That is now a general rule and not a Devourer decision.

What is still open is the top-level call, and principle (c) narrows rather than answers it: with
the edge suppressed, binding Vengeful Retreat buys **only** V11's cooldown hatch. So the question
is now the cleaner one — *is the hatch alone worth binding a row outside the scanned line?* —
with no scan-edge confound in it.

⚠ **Not yet implemented.** The engine enforces principle (c) at `Sense.Verdicts` for the whole
overlay (ordering off, or stood down), which is the state that made cap's reading a lie
everywhere at once. Per-viewer suppression is the same principle applied one row at a time and is
NOT built: today a bound Utility row still draws its edge. It is deliberately left until the
question above is answered, because unbinding the row would make the suppression moot.
