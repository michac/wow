# Plan — `frames-textures-animation.md`

**Read `00-brief.md` first.** You own **this file only**.

**Verdict: mechanical strip pass. Do NOT regenerate.** The prose is good and the
provenance is dense — §5.3's gap analysis (`:762-775`) is among the best work in the
corpus. This file is wearing barnacles, not rotting.

Size: ~99 KB, 1747 lines. **The worst Gate-1 offender in the corpus.**

| Gate | Now | Target |
|---|---|---|
| 1 — retrospective prose | **32** | 0 |
| 2 — dates in prose | **49** | 0 |
| 3 — self-correcting sections | 0 | 0 |

---

## 1. The contradiction you must resolve — you are the losing side

### `SetTexture` and a secret string — `:656-659`

Current text:

> `SetTexture`, `SetAtlas` and `SetColorTexture` all carry
> `SecretArguments = "AllowedWhenTainted"` and **no** `SecretArgumentsAddAspect`
> `[T1 docs, same file]` — i.e. they accept secret arguments and, having no
> connected aspect, that marks the *whole object* as having secret values (§3.3).

**This is wrong and it was measured wrong.** `security-taint-and-restricted-data.md:1385-1389`
records, `[client 2026-08-04]`:

> `SetTexture` **refuses a secret string outright** despite carrying
> `SecretArguments = "AllowedWhenTainted"` (`SimpleTextureBaseAPIDocumentation.lua:441`).
> The annotation is necessary, not sufficient — the client's own message is *"Cannot set
> texture to a secret string value."* `SetAtlas`, on the identical annotation, accepts it
> silently.

**Security wins**: it ran the code, this file read the docs. Rewrite `:656-659` so that:

- the three setters are no longer lumped together — `SetTexture` behaves differently from
  `SetAtlas` on the *identical* annotation;
- the general lesson is stated, because it is the most transferable thing in the file:
  **a `SecretArguments` annotation is necessary, not sufficient. It says the API will not
  reject the call at the annotation layer; it does not say the implementation accepts the
  value.**
- it points at `security` §4.8.1 for the measured table rather than restating it (that
  section is frozen — cite, do not copy).

Keep the whole-object-secrecy claim for the setters where it still holds.

---

## 2. The known sediment

**29+ `[corrected 2026-07-23]` blocks**, ~11.8 KB, plus a **1.2 KB header block at
`:29-45`** that is pure process narrative. Delete the header block outright.

Worked examples (find the rest with Gate 1):

**`:1409-1421` — pools, eight vs nine.** The base sentence still says "eight"; a
`[corrected]` note below says nine. **Nine is right** (`GetTemplate` bolted on at
`Pools.lua:539`). Rewrite as shown in the brief's worked example. ⚠ **This same fact is
duplicated at `:1717-1729` (rule 37) with its own separate `[corrected]` footnote.**
Fix both, and make them agree. `module-architecture.md` also carries the wrong number —
another agent is fixing that; do not touch it.

**`:634-650` — sediment two layers deep.** A 2026-07-30 measurement nested inside a
2026-07-23 correction of a table row that no longer exists. Three timestamps, one fact.
The surviving claims: `SetMask` is orthogonal to the three base-image writers and lives in
§5.7; **it does not clip a `SetColorTexture` fill** `[client 2026-07-30]`; whether the
three base-image writers are mutually exclusive is uncited and stays `@verify-ingame`.

---

## 3. The duplication problem

**"Rules we could audit against" is ~16% of this file and is a second copy of the body.**
Corrections have been applied to the two copies independently, which is how `:1409` and
`:1717` drifted apart.

**Do not delete the rules section** — it is the file's audit surface and §4 of the README
depends on it. **Do** make each rule a one-line assertion that cites the body section
rather than re-arguing it. A rule should not carry its own `[corrected]` footnote; if it
does, the fix belongs in the body and the rule shrinks to a pointer.

---

## 4. Structural note — do not act, just report

This file documents **no `StatusBar`, no `Cooldown` widget, and no ScrollBox/ScrollUtil** —
the widget types this workspace's own addons drive. Several pure widget-lifecycle facts
about them currently live inside `security` §4.8 (frozen) because that is where they were
discovered. That relocation is planned but **blocked**; note it in Escalations and move on.

Separately, `knowledge/addon-dev/observations.md` OBS-002 and OBS-003 record that this file
documents no `EditBox` behaviour at all, and that the copy-out mechanism (multiline EditBox
+ `HighlightText()`) is undocumented. **Do not write that section now** — those entries
drain later, deliberately, so the section is written once against settled limits.

---

## 5. Front matter

`:9` cites "593 files" in the source line. The corpus is **592 `.lua` + 1 `.toc` = 593
entries**, i.e. **592 Lua files**. Fix to whichever is accurate for what the line claims,
and flag in Escalations that `sources.md` carries the same drift (held centrally).
