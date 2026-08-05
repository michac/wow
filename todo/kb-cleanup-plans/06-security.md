# Plan — `security-taint-and-restricted-data.md` (§0–§4.7 and §5–§7 only)

**Read `00-brief.md` first.** You own **this file only**, and **not all of it**.

## ⚠ FROZEN REGION — §4.8 through §4.12

**Do not edit anything from §4.8 to the end of §4.12.** That subtree (~24 KB) is the only
run-in-client evidence in the file, it is structurally broken in ways that need a rewrite
rather than a strip, and **its resolution is gated behind an in-game flight the
cooldown-hud project already owes.** A separate pass handles it after that flight.

You may **cite into** the frozen region. You may not move text into or out of it, renumber
it, or fix its internal contradictions. If you spot something there, put it in Escalations.

Known-broken inside the frozen region, already catalogued — **do not fix**:
its findings are numbered 1, 9, 10, 11, 12, 13, 14, 2, 3, 4, 5, 6, 7 (no finding 8); a
table row at `:1230` reads ✅ under a correction saying that reading shipped a 0%-width bar
for four builds; `:1241` cites a §4.9 sentence that does not exist; `:1315` has §4.8.1
correcting itself.

---

Size: ~122 KB, 2082 lines — the largest file in the corpus.

| Gate | Now | Target (your region only) |
|---|---|---|
| 1 — retrospective prose | **17** | 0 outside the frozen region |
| 2 — dates in prose | **28** | 0 outside the frozen region |
| 3 — self-correcting sections | **4** | 0 outside the frozen region |

Report your counts as "in-scope" vs "frozen" so the numbers stay readable.

---

## 1. The contradiction you must resolve — it is inside your region

### `table` in the secure-snippet environment — §3.2 at `:631-635` vs rule 7 at `:1892-1904`

§3.2 says:

> The environment handed to snippets is an explicit allow-list … **`table` is deliberately
> excluded** — the comment says *"table is provided elsewhere, as direct tables are not
> allowed"* (`:27`).

Rule 7 says, corrected 2026-08-05:

> ⚠ **`table` IS available, and this rule said the opposite.** `RestrictedExecution.lua:324-334`
> injects a `table` namespace — `maxn`, `insert`, `remove`, `sort`, `concat`, `wipe`, and
> **`new`** … So **`table.new()` / `newtable()` is the sanctioned substitute for the `{}`
> constructor**, which `BuildRestrictedClosure` rejects at build time — snippet-local storage
> is entirely possible, where this rule previously implied it was not.

**Rule 7 is right.** It cites the second Tier-1 file (`RestrictedExecution.lua:276-294,
:324-335`) that §3.2 stopped short of.

**The correction was applied to the rule and never to the prose body it came from** — and
§3.2 is exactly where a "how do I write a secure snippet" question lands. A reader of §3.2
today concludes snippet-local storage is impossible and designs around a limit that does
not exist.

**Fix §3.2's body**, then reduce rule 7 to a one-line assertion citing it (drop the
"this rule said the opposite" framing entirely).

⚠ `mined-pending-verification.md:212-214` records this as *"Applied already — do NOT
re-mine"*, which is false: it was half-applied. **That file has no agent. Note it in
Escalations** — the central pass will fix the record.

---

## 2. §4.6 needs a fix even though §4.8 is frozen — `:923-961`

§4.6 declares:

> Passing a secret into a widget setter *marks the object*. **Three distinct outcomes:**

…and presents (a) aspect / (b) whole-object secrecy / (c) const accessor as **alternatives**,
then picks **`FontString:SetText`** as its worked example for (a) at `:947-951`.

A measured finding in the frozen region (`:1374-1383`, `[client 2026-08-04]`) proves
`SetText` is precisely the case that does **(a) and (b) simultaneously** — it applies the
`Text` aspect **and** marks anchoring secret, propagating down the anchor chain.

**So §4.6's own worked example is the case that breaks §4.6's framing**, and a reader who
follows it anchors a tooltip to that FontString and it breaks.

**This is in your region — fix it.** Rewrite §4.6 so that:

- the three outcomes are **not** mutually exclusive — (a) and (b) can co-occur;
- `SetText` is presented as the case that does both;
- the practical rule is stated: **a FontString fed a secret must be a leaf** — anchor it to
  things, never anchor things to it;
- it **cites** `:1374-1383` for the measurement rather than restating it (frozen region —
  cite, do not copy).

---

## 3. §4.7 — the missing predicate

§4.7 is the predicate census (*"51 predicates … 32 Precondition, 19 Secret"*), and README
routes all predicate questions here. It **does not mention `RequiresNonSecretAura`**, a
12.0.7-live Tier-1 `Precondition` on three `C_UnitAuras` getters — while §4.5 (`:896-898`)
lists those same three getters as plain `AllowedWhenTainted` with **no** precondition.

The predicate is documented in `cooldown-manager.md:525`, `12.1.0-ptr-heads-up.md:47` and
`mined-pending-verification.md:183` — i.e. everywhere except the file that owns predicates.

**Add it to §4.7 and correct §4.5's three rows.** Verify the annotation against
`raw/addon-research/wow-ui-source` before writing it — do not transcribe from the other
files. If the count in §4.7's header changes as a result, update it.

---

## 4. The remaining sediment (in-scope only)

**~14 "an earlier draft" asides**, plus the process-narrative header block at `:45-53` —
delete that block.

**`:695` — oUF's size.** Reads a bare **784 K**. That figure includes `.git`; the code size
is **504 K**. README recorded this reconciliation and it was applied to `sources.md` and
`libraries-and-ecosystem.md` but not here. Fix to 504 K (or state both with the
distinction).

---

## 5. Structural note — do not act, just report

This file is **122 KB doing three jobs** with different half-lives, different evidence
tiers and different readers:

- **§0–§3** — the patch-2.0 protection/taint model. Settled, source-read, stable.
- **§4.1–§4.7** — the secret-values *reference*: annotation vocabulary, counts, predicates.
  A lookup surface, re-derived per build.
- **§4.8–§4.12** — a *measured cookbook*: how to put a value you cannot read on screen. The
  only run-in-client evidence, the fastest-growing part, and what CDMProbe actually consumes.

The proposed split lifts the third into its own `displaying-secret-values.md` that declares
itself run-in-client at the top. **That is the frozen region, so it is not your job** — but
if your work surfaces anything that makes the seam cleaner or harder, say so in Escalations.
That decision is pending and your read of the file is the best evidence available for it.
