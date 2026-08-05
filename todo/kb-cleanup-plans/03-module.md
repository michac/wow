# Plan — `module-architecture.md`

**Read `00-brief.md` first.** You own **this file only**.

**Verdict: strip pass.**

Size: ~71 KB, 1289 lines. `confidence: medium` — **correct, keep it**. README explains
why: the platform genuinely mandates almost nothing above "an ordered list of files and one
private table", so most of this file is necessarily Tier-3 pattern-reporting rather than
Tier-1 fact. That honesty is a feature.

| Gate | Now | Target |
|---|---|---|
| 1 — retrospective prose | **12** | 0 |
| 2 — dates in prose | **12** | 0 |
| 3 — self-correcting sections | **1** | 0 |

---

## 1. The contradiction you must resolve — you are the losing side

### Secure pool proxy surface — `:938-942`, repeated in rule 11 at `:1146-1150`

Current text:

> Secure pools are additionally exposed only through a **proxy** with a fixed method
> whitelist — `Acquire`, `ReleaseAll`, `Release`, `EnumerateActive`, `GetNextActive`,
> `IsActive`, `GetNumActive`, `DoesObjectBelongToPool` `[T1 src: Pools.lua:282-297]` — so
> you cannot reach the pool's internals at all. Design against those **eight** methods.

**Eight is right only for a plain object pool.** Every *region* pool (frame / texture /
fontstring / masktexture / actor) goes through `CreateSecureRegionPoolInstance`, which
bolts a **ninth** method onto the proxy — `proxy.GetTemplate`, assigned at
`Pools.lua:539` (`[T1 src: Pools.lua:536-544]`).

`frames-textures-animation.md` has the correct version and names the assignment line;
this file carried the pre-correction number through its own 2026-08-05 review.

**Fix both locations and make them agree.** Since a frame pool is overwhelmingly the case
a reader of *this* file cares about, lead with nine and note that a plain object pool is
the eight-method case — not the other way round.

⚠ `frames-textures-animation.md` has its own agent fixing its own duplicate of this. Do
not edit it.

---

## 2. The known sediment

**~13 "an earlier draft" asides, ~3.9 KB.**

**`:670-689` is the worst — 20 lines correcting a claim that no longer exists:**

> ⚠ **Corrected.** An earlier draft claimed the abstract-method idiom "appears at exactly
> 7 sites … it is rare, not a house style." That was an artefact of grepping two literal
> phrases … and it is wrong in both directions:

The three bullets underneath **are the real claim** and they are good. They are merely
formatted as evidence against a ghost. Rewrite as a forward assertion, roughly:

> **Declaring abstracts is common; enforcing them at runtime is rare.** 137 lines in the
> shipped source are a bare comment telling a derived mixin to override; only 7 sites
> enforce at runtime, and those 7 use three different idioms (`error`, `assert(false)`,
> `assertsafe(false)`).

`:487-495` has the same shape — treat it the same way.

---

## 3. Gate 3 — the self-correcting section

One hit. Find it (`grep -nE '(⚠⚠?|❌).{0,120}§[0-9]'`) and resolve it by **editing the
section it points at**, then deleting the pointer. A section corrected by a later part of
the same file is a defect ticket, not documentation.

---

## 4. Scope creep to remove — §1.1a, `:117-143`

This section mixes a Tier-1 constraint with Tier-3 style advice, in a file whose own
headline (`:37-42`) promises *"Where this file states a rule, the rule is anchored in
Tier 1."*

- **Keep:** the `.toc`-ordering constraint (the first file in the `.toc`) and the
  dual-client version flag. Those are platform facts.
- **Remove:** "compute the flag once", "pair it with a demolition plan in the comment",
  "a version gate with no stated expiry becomes permanent". That is engineering culture
  derived from reading **one** Tier-3 addon, and it is not what this file promises.

Where it should go instead is a judgement call — put it in Escalations with your
recommendation (`12.1.0-ptr-heads-up.md` and a project doc are both candidates). **Do not
write it into another file yourself.**

---

## 5. Structural note — do not act, just report

README §1 says pools are deliberately split three ways across `frames`, `module` and
`security`, and that *"All three cite the same `Pools.lua` and agree."* They did not — that
is the contradiction in §1 above.

The durable fix is for **this** file to hold the architectural view ("pooling forces
ownership discipline") and **cite** `frames` for the method surface, rather than restating
a count it cannot keep current. §5.2 (`:900-942`) is where that applies. **You may make
that edit** — it is within your file and it is the change that prevents the drift
recurring. Note it in your report.
