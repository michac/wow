---
title: How a claim is written in this KB — the current-state rule
patch: 12.1
fetched: 2026-08-17
reviewed: 2026-08-17
sources:
  - knowledge/addon-dev/README.md   # §7, where this rule was written and proven first
confidence: high
---

# How a claim is written here — the current-state rule

**A knowledge file states what is true now. It never states what it used to say.**

This is doctrine for **all of `knowledge/**`**. It was written for
`knowledge/addon-dev/` and enforced there by `wowkb.kblint` for months before it was
promoted; that subtree keeps two extra rules of its own (§8 below).

## Why this exists

An agent reading a file top-down, or grepping one line out of it, must get the **current**
answer. A correction written as an *append* — the old claim left standing, a ⚠ note added
below saying it is wrong — defeats both. The reader who stops early, or who greps the
line the stale number lives on, gets the wrong answer with no signal that a correction
exists 20 lines further down. This is the single most common way this KB has misled its
own tooling, and it is entirely self-inflicted: the correct value was known at the moment
the wrong one was left in place.

Measured 2026-08-17, before the first sweep: **69 of 356** knowledge files carried
retrospective prose, across 26 directories.

## The rules

1. **Correcting a claim means rewriting the claim.** Edit the sentence, the table cell,
   the number, in place. Do **not** leave the old text standing under a correction note.
   If a reader can get the wrong answer by reading top-down or by grepping a single line,
   the edit is not finished.
2. **History goes in one place or nowhere.** If the *fact that we were wrong* is itself
   worth keeping — because it would otherwise be re-derived, or because it cost real work
   — it is **one line** in a `## Changelog` at the bottom of the file:
   `2026-08-17 — rank-9 helm is Veteran (279), not Champion/246, and re-issues per season.`
   Cap: 20 entries or 2 KB, whichever comes first; drop entries older than two patches.
   Anything longer belongs in `_meta/changelog-<patch>.md`.
3. **The lede is the current answer.** Everything between the front matter and the first
   `##` heading states what is true, flatly. No hedges, no correction notes, no "but see
   below". A reader who quits after the first screen must not be wrong — only incomplete.
4. **Dates belong to provenance, not to prose about ourselves.** `fetched:`/`reviewed:`,
   a citation stamp, an evidence tag, the `## Changelog`, and **the game's own calendar**
   (a patch's live date, a season's start, an event window) all carry dates legitimately.
   *"We said X on 2026-08-11 and corrected it on 2026-08-17"* does not — that is rule 2's
   one line, or nothing.
5. **No numbered "findings" list in a reference body.** A finding is merged into the
   section it amends. Out-of-order ordinals are the signature of a file being appended to
   instead of edited.
6. **Unsettled findings do not go in a knowledge file at all.** They go in a queue. A
   knowledge file asserts; a queue file asks. The queues are `_meta/kb-inbox.md` (the
   free-form parking lot), `@verify-ingame` markers (drained by `wowkb.gen_verify`),
   `discovered-weeklies.json`, and `addon-dev`'s own three.
7. **A temporal correction is not a source conflict.** CLAUDE.md's *provenance precedence*
   rule — keep the Tier-1 value, flag the disagreement — governs **two live sources
   disagreeing now**. When *we* were simply wrong and now know better, there is no
   disagreement to preserve: delete the old claim and write the new one. Confusing these
   two is the specific mistake that produces append-style corrections.

## §8 — the two extra rules `knowledge/addon-dev/` keeps

They are domain rules, not general ones, and they stay in that subtree's README §7:

- **A measurement is a claim plus a tag, not a story** — present tense, `[client YYYY-MM-DD]`,
  one sentence of method only if the method is load-bearing.
- **A claim is scoped to the API, not the call site** — if a fact is only true of one addon,
  one spec or one build, it is not a KB fact.

`addon-dev` also runs three gates the rest of the KB does not (dates in prose, unqualified
negatives, citation circles), because its evidence classes are stricter.

## The gates

`wowkb.kblint` enforces what is mechanically checkable. Rules 1 and 5 are **gate 1**
(retrospective prose outside a Changelog), rule 3 is **gate 6** (a hedged lede), and a
section corrected by a later part of the same file is **gate 3**. Gates 1, 3 and 6 run
over **all of `knowledge/**`**; gates 2, 4 and 5 remain `addon-dev`-only.

```bash
uv run python -m wowkb.kblint                 # addon-dev, all 6 gates, exit 1 on any hit
uv run python -m wowkb.kblint --all           # the whole KB
uv run python -m wowkb.kblint --all --warn    # report the backlog without failing
uv run python -m wowkb.kblint --all --counts  # per-file table only
```

⚠ **`--warn` is scaffolding, not a setting.** It exists so the 69-file backlog can be
burned down without a permanently red gate. When the count reaches zero, the flag should
stop being passed — a gate that never fails is not a gate.

## Changelog

2026-08-17 — promoted from `addon-dev/README.md` §7 to KB-wide doctrine; added rules 3
(lede), 4 (game dates are legitimate) and 7 (temporal correction ≠ source conflict).
