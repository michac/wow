# Plan — `anatomy-and-runtime.md`

**Read `00-brief.md` first.** You own **this file only**.

**Verdict: light in-place pass — the smallest job in the fan-out.** Two real defects, both
introduced by a mining run on 2026-08-05, plus a modest date sweep.

Size: ~71 KB, 1230 lines.

| Gate | Now | Target |
|---|---|---|
| 1 — retrospective prose | **2** | 0 |
| 2 — dates in prose | **19** | 0 |
| 3 — self-correcting sections | **3** | 0 |

---

## 1. The `## Category:` note is wrong on both halves — `:283-293`

Current text:

> ⚠ **`## Category:` is a real, addon-facing field this file did not carry** (added
> 2026-08-05).

**Both claims in that sentence are false, and it is filed in the wrong section.**

1. **"this file did not carry it"** — it does. `:221` has had a table row all along:
   `| Category | 21 | Collapsible header in the AddOns list. Localisable. |`
2. **The related claim at `:291`** — *"`## Category:` does not appear in the Blizzard
   corpus … so this is a third-party-only field in practice"* — is contradicted by
   `sources.md:96`, which counts shipped-toc directive frequencies and lists
   **`Category` 1**. So it appears exactly once in the shipped corpus. Soften the claim to
   match the count: near-absent from Blizzard's own addons, not absent.
3. **It is filed under §2.3 "Restricted directives — do not use them"** — the exact
   opposite of what it says. Its own first sentence calls the field *addon-facing*.

**Fix:** merge the useful content (what the field does, that it does not affect loading /
dependencies / environment, that it is localisable) into **§2.2's addon-facing directive
table at `:221`**, correct the corpus claim against `sources.md`'s count, and delete the
§2.3 note entirely. This is a mined Tier-3 claim that was asserted into a
`confidence: high` file without checking two Tier-1 counts already in the KB — say so in
your report.

---

## 2. LoadOnDemand — two numbers, both correct, and a trap

`:526-541` and `:1196` give LoadOnDemand as **125/346**; `sources.md:91` and `:97` give
**167/346**. Both are right: 125 is a semantic count, 167 a line-frequency count. The
corpus currently reconciles this with ~10 lines of explanation at each site.

**Fold it to one sentence** at the primary site, roughly:

> 125 of 346 shipped addons are LoadOnDemand by semantics; `sources.md`'s 167 is a raw
> line frequency and counts differently.

Then delete the second explanation at `:1104-1105` / `:1196`, leaving the bare number with
a pointer. A grep for "LoadOnDemand" should stop returning twenty lines of reconciliation.

---

## 3. Gate 3 — three self-correcting sections

Three hits. For each: **edit the section being corrected**, then delete the pointer. If the
correction turns out to be wrong (as in §1 above — the 08-05 mining run got two things
wrong), fix the correction, not the base text.

---

## 4. Front matter

Front matter now leads with a **Tier-3 deleted-clone source** (EllesmereUI) ahead of
`wow-ui-source`. Reorder so the Tier-1 source leads. Do not remove the EllesmereUI
citation — flag in Escalations that `sources.md` has no registry entry for it and no
evidence class for a source whose clone has been deleted (held centrally).

Note also: `reviewed: 2026-08-05` currently post-dates the mining run that **introduced**
the §1 defect. A `reviewed` stamp that post-dates a regression is worse than none. Set
`reviewed: 2026-08-05` again when you finish — this time it will be true.

---

## 5. Report, do not act

`sources.md:230` calls EllesmereUI a **20-module** suite; this file (`:290`) and
`module-architecture.md:129` both call it an **18-addon** suite, and both were written by
the same 2026-08-05 mining run. The clone has been deleted, so **this is not resolvable
from the tree.** Do not guess a number. Put it in Escalations; it needs a re-clone or the
claim needs to lose its count.
