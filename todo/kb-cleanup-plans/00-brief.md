# Shared brief — addon-dev KB cleanup fan-out

**Every agent reads this first, then its own plan file.** Findings behind it:
`todo/addon-dev-overhaul.md`.

---

## What you are doing

`knowledge/addon-dev/` has been maintained **additively**: claims were corrected by
appending a dated note underneath, rather than by rewriting the claim. The result is a
corpus where roughly a quarter of the bytes are not claims, and — worse — where **13
places give a wrong answer to anyone who reads top-down or greps a single line**, because
the base text is stale and only a buried note corrects it.

You are converting one file from *sedimentary* to *current-state*.

The rule you are applying is now `knowledge/addon-dev/README.md` **§7**. Read it. It is
the contract; this brief is the operating procedure.

---

## Hard scope rules

1. **You own exactly the file(s) your plan names. Do not edit any other file.**
   Six agents are running in parallel on sibling files. If your work implies a change
   elsewhere, **write it in your report** — do not make it.
2. **Do not touch `README.md` or `sources.md`.** Those are held centrally.
3. **`security-taint-and-restricted-data.md` §4.8–§4.12 is frozen** for everyone. Its
   resolution is gated behind an in-game flight the cooldown-hud project already owes.
   Do not edit it, cite into it freely, or move anything into or out of it.
4. **Never delete a fact.** The transformation is *rewrite* and *relocate*, never *drop*.
   If a correction note contains a claim the base text lacks, the claim survives — in the
   base text.
5. **When unsure, park it.** Add an entry to your report's "Escalations" section rather
   than guessing. A wrong confident edit here is exactly the failure being cleaned up.

---

## The transformation

### The core move

Find every place where a claim is followed by a correction, and **fold the correction into
the claim**:

> **Before**
> ```
> The `ObjectPoolProxyMixin` surface is eight methods: `Acquire, ReleaseAll, …`
> `[corrected 2026-07-23]` "Exactly eight" is true only of a plain object pool. Every
> *region* pool bolts a ninth method … So a frame-pool proxy has **nine**.
> ```
>
> **After**
> ```
> A secure pool handed to addon code is a **proxy**. A plain object pool exposes eight
> methods `[Pools.lua:282-297]`; every region pool (frame/texture/fontstring/masktexture/
> actor) exposes **nine** — `GetTemplate` is bolted on at `[:539]`.
> ```

Note what happened: the reader can no longer reach the wrong answer, the citation
survived, and 4 lines became 3.

### What to delete outright

- **"An earlier draft said…" / "previously we claimed…" / `[corrected <date>]` framing**,
  once the corrected value is in the claim.
- **Whole "Adversarial verification pass" / Was-Is table sections.** These document a
  *process*, not the subject. If the fact that a pass happened matters, it is one
  front-matter line or one Changelog line.
- **Claims removed rather than transplanted** — text whose content is "we used to assert
  X and no longer do". Delete the paragraph; the surrounding claim is already correct.
- **Struck-through (`~~…~~`) closed gaps.** A closed gap is not pending work. If the
  answer is not already in the body, put it there, then delete the strike-through.
- **Session narrative:** which spec, which character, which build, what we tried first,
  how many builds it cost. That belongs in `projects/<addon>/docs/`.

### What to keep, always

- Every **`file:line` citation** and every **`[T1 …]` / `[T2 …]` / `[client …]` tag**.
  These are the KB's whole value. If you fold two sentences into one, the citations from
  both come with it.
- Every **`@verify-ingame`** and **`[gap]`** marker whose question is still open.
  ⚠ **Preserve backticking exactly as you find it.** A backticked `` `@verify-ingame` ``
  is deliberately invisible to `wowkb.gen_verify`; changing that quietly adds items to a
  player-facing in-game checklist.
- The **measured content** of anything tagged `[client]`. Rewrite its framing, never its
  finding.

### What to add

- A **`## Changelog`** at the very bottom of the file, if — and only if — a correction is
  worth remembering because it would otherwise be re-derived or because it burned a
  release. One line each, newest first:
  ```markdown
  ## Changelog

  - 2026-07-23 — §9 pool proxy: a region pool exposes nine methods, not eight.
  ```
  Cap 20 entries / 2 KB. **Most corrections do not earn a line.** If in doubt, leave it out.

---

## Your gates

Your plan names your file's current counts. Drive them toward zero — **except where a hit
is a false positive, which you should report rather than contort the text to satisfy.**

```bash
cd /home/mchristiansen/code/fun/wow

# GATE 1 — retrospective prose outside a Changelog
awk '/^## Changelog/{skip=1} skip{next} 1' knowledge/addon-dev/<YOUR FILE> \
| grep -nEi 'an earlier (draft|version|pass|run|note)|previously (said|read|cited|written|showed|gave|asserted)|\[corrected|used to (be|read|say|assert|show)|GRADE CORRECTION|\*\*Correction|Adversarial verification pass'

# GATE 2 — a date in prose is a defect
grep -nE '20[0-9]{2}-[0-9]{2}-[0-9]{2}' knowledge/addon-dev/<YOUR FILE> \
| grep -vE 'revid [0-9]+, 20|\[client 20|^[0-9]+:(patch|fetched|reviewed|title|sources|  -)|## Changelog'

# GATE 3 — no section corrected by a later part of the same file
grep -nE '(⚠⚠?|❌).{0,120}§[0-9]' knowledge/addon-dev/<YOUR FILE>
```

**Gate 2 subtlety:** a date attached to a *measurement* is legitimate — it just has to be
in `[client YYYY-MM-DD]` form. Converting `**MEASURED 2026-07-30:**` to `[client 2026-07-30]`
is the correct fix, not deleting the date.

---

## Front matter

When you finish, set `reviewed:` to **2026-08-05**. Leave `fetched:` alone unless you
changed what the file *claims* (folding a correction into a claim does change it — use
your judgement; if a claim's value changed, bump `fetched:` too).

Do not change `confidence:` — that is a central call being made separately.

---

## Deliverable

Do the edits, then report:

1. **Gate counts before → after**, all three.
2. **Contradictions resolved** — for each one your plan assigned you, the old text, the
   new text, and confirmation the winning side is now what the file says.
3. **Anything you deleted that was more than framing** — if you removed a sentence
   carrying a claim, say which and why.
4. **Changelog entries added** (there should be few).
5. **Escalations** — cross-file implications you did NOT act on, false-positive gate hits,
   and anything where you were unsure. Be liberal here; this section is the point.

Do not commit. Do not run `git` at all.
