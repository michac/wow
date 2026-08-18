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

## No open questions

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

An empty file is this file's correct resting state, not a defect.
