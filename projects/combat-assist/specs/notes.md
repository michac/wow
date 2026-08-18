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

## No entries yet

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
