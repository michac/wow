# Plan — `libraries-and-ecosystem.md`

**Read `00-brief.md` first.** You own **this file only**.

**Verdict: strip pass, plus one section deleted outright.**

Size: ~72 KB, 1065 lines. `confidence: medium`, and that rating is **correct and
justified** (README explains why: adoption evidence is unobtainable from this machine —
CurseForge 403, wago.io 401). Leave it at medium.

| Gate | Now | Target |
|---|---|---|
| 1 — retrospective prose | **19** | 0 |
| 2 — dates in prose | **67** — the highest in the corpus | see §3 |
| 3 — self-correcting sections | 0 | 0 |

---

## 1. Delete outright: the "Adversarial verification pass" section, `:51-94`

**3.4 KB, at the very top of the file, before any claim**, whose entire content is an
11-row **Was / Is** table of what a deleted draft said.

This is the single clearest instance of the pathology in the corpus: a reader's first
encounter with the file is a list of things that are not true.

**Delete it.** If the provenance is worth keeping it is one front-matter line:

```yaml
verification: adversarial re-read 2026-07-23, 11 of ~50 claims corrected
```

⚠ **Before deleting, check every row.** Some Was/Is rows may carry the *only* statement of
the corrected value. Any such value must already exist in the body — put it there first if
it does not. This is the brief's "never delete a fact" rule at its sharpest.

---

## 2. The remaining sediment

**~20 "an earlier draft…" asides, ~5.6 KB.** Standard treatment: fold the corrected value
into the claim, delete the framing.

**The rules section is 24% of this file — the worst duplication ratio in the corpus.**
Same instruction as elsewhere: keep the section, but each rule becomes a one-line assertion
citing its body section rather than re-arguing it. This is where the biggest byte win in
your file is, and it is low-risk because the body is the authority.

---

## 3. Gate 2 — read this before you start deleting dates

**67 hits, and many are legitimate.** This file's subject is *the maintenance status of
third-party libraries*, so a date is often the claim: `pushed_at 2015-09-02` is not
narrative, it is the evidence that a library is frozen.

**Do not strip those.** The correct treatment:

- A date that is **evidence about a library** stays, in a consistent citable form —
  prefer `[gh: pushed_at 2015-09-02]` or similar over bare prose.
- A date that is **narrative about our own process** ("we checked this on…", "an earlier
  pass on 2026-07-23 said…") goes.

Report the final count with a one-line note on how many are load-bearing. **A gate that
cannot reach zero honestly should be reported, not gamed.**

---

## 4. Known factual drift to fix

**LibDataBroker's size.** This file says LDB is **90 lines** (`:598`, `:666`), and
`state-persistence-and-communication.md:872` agrees. `sources.md:464` says **40 lines**.
**You are right — 90 wins**; the 40 is the outlier and `sources.md` is held centrally, so
just flag it in Escalations.

The same `sources.md:464` dates the LDB repo 2008-07-31 against this file's
`pushed_at 2015-09-02` (`:666`). Both can be true (created vs last pushed) — if your text
makes that distinction clear, say so in Escalations so the central fix can match it.

---

## 5. Structural note — do not act, just report

§7 ("What Blizzard now ships that used to need a library", `:512-527`) is a useful table
whose every row's subject is **owned by another file** — `C_Timer` → api-events,
pools/mixins/CallbackRegistry → frames + module, Settings API → state-persistence, addon
compartment → anatomy.

It should become an **index that links** rather than a table that restates, or it becomes
a fifth place for the pool method count to drift. **You may do this if it is a
straightforward edit within your file** (replacing restated detail with a pointer). Do not
edit the files it points at.

Also: §8.2 already covers LibDataBroker + LibDBIcon, and
`state-persistence-and-communication.md` §9 covers it again. README's boundary-calls list
does not name this split, so it looks accidental rather than deliberate. **Report it; do
not act** — the other file has its own owner.
