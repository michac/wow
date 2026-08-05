---
name: mine-addon
description: >-
  Mine a third-party WoW addon for API FACTS and write them into knowledge/addon-dev/,
  then delete the source. Use when the user wants to learn from a reference addon —
  "how does <addon> do X", "clone <addon> and see how they...", "mine ElvUI /
  EllesmereUI / oUF / WeakAuras for working examples", "another addon can do it so we
  can too" — or when a KB claim needs checking against a shipping implementation.
  The output is facts + our own minimal illustrations + file:line provenance, NEVER
  copied code. Do not use for our own addons (CDMProbe, BucketBinds, PlannerState) or
  for Blizzard's UI source, which is Tier 1 and read directly.
---

# Mining a reference addon for API facts

A shipping addon is the only evidence source in this workspace that proves an API
sequence **actually works in the live client**. The generated docs say what an
argument is typed as; a working addon says what order you have to call things in. That
gap is where this skill earns its keep — the 2026-08-04 `SetMinMaxValues(0, 1)` →
`SetTimerDuration` finding cost four builds of inference and was settled in one grep of
an installed addon.

It is also the evidence source with the sharpest legal edge and the worst
signal-to-noise. Both are handled below, and neither is optional.

---

## 1. The line you may not cross

**Assume every addon is All Rights Reserved unless its license says otherwise.** Most
are. EllesmereUI's `license.txt` is literally *"copyrighted to their authors with all
rights reserved"*; EnhancedCooldownManager is GPL-3.0, which is *worse* for us, not
better — copying from it would infect our MIT addon.

So the deal is the same either way, and this workspace already set it (CDMProbe
`CLAUDE.md`, licensing note): **read for API discovery only; copy nothing.**

| ✅ Mine this | ❌ Never take this |
|---|---|
| Required **call order** (`SetMinMaxValues` before `SetTimerDuration`) | Their function bodies, verbatim or reworded |
| **Argument shape** — which arg is the enum, which is nilable in practice | Their file/module structure as a template |
| **Which return values matter** (`SetStatusBarTexture` returns `success`) | Their comments, renamed variables, "inspired by" transcription |
| **Enum members** and API names they call | Their algorithms, tuning constants, or data tables |
| **That a thing is possible at all** — the existence proof | Their art, media, locale strings, or saved-variable schemas |

The test: **could you have written this sentence after being told the fact over the
phone, without ever seeing the file?** If yes it is a fact. If you had to look at the
code to reproduce the shape, it is expression — restate the fact and write your own
illustration from scratch.

⚠ **"Working example" does NOT mean "their example."** It means *our* minimal snippet,
written from the fact, that we can test. Cite their `file:line` as **provenance for the
claim**, the way a footnote cites a source it does not reproduce.

---

## 2. An addon is Tier 3 evidence — corroborate before you believe it

`knowledge/_meta/sources.md` puts Blizzard's API/source at Tier 1 and third-party
addons well below. A shipping addon proves *something worked at some point*. It does
not prove the thing is necessary, current, or correct.

⚠ **Real example, from the run this skill was written out of:** EllesmereUI calls
`Enum.StatusBarInterpolation.None` — a member that **does not exist** in the generated
enum (only `Immediate = 0` and `ExponentialEaseOut = 1`,
`SimpleStatusBarConstantsDocumentation.lua:25-28`). Their guard makes it harmless. Copy
it as gospel and you ship a nil.

So **every mined fact gets checked against Tier 1 before it is written**:

1. **Does the generated doc agree?**
   `raw/addon-research/wow-ui-source/Interface/AddOns/Blizzard_APIDocumentationGenerated/`
   — signatures, enums, `Nilable`, `SecretArguments`, `MayReturnNothing`.
2. **Does Blizzard's own UI source do the same thing?** A Blizzard caller doing it too
   promotes the fact to near-Tier-1 and it should be cited *instead*.
3. **Is it superstition?** Defensive `if x and x.y then` guards, workarounds for bugs
   long fixed, and legacy paths for old clients are the common false positives. If you
   cannot say *why* a step is required, record it as **unverified**, not as a rule.
4. **Strip the comments — does the fact survive?**

### 2.2 The strip-the-comments test

⚠ This is **not** the generic "comments can be stale" warning; that one is obvious and
you already apply it. The failure here is the **inverse**, and it is specific to a class
of codebase that is becoming common: one with a house rule mandating rationale comments
(look for a `CLAUDE.md` / `AGENTS.md`, uniform comment density, and comments that
*argue* rather than *describe*). Their comments are abundant, confident and narratively
detailed — and confidence-rating instinctively keys on richness of detail, so a
well-argued paragraph reads exactly like a field report:

> *"We bisected nine gates; parenting, existence and strata were each individually
> exonerated."*

That may be a measured result. It may equally be a hypothesis written down at authoring
time and never falsified. **The prose cannot tell you which**, and its quality is not
evidence either way.

So ask, per fact:

> **If every comment in this file were stripped, would the fact still be derivable from
> the code?**
>
> - **Yes** — the code *demonstrates* it (a call order you can read, an argument shape,
>   a guard that must exist for the following line to work). Grade normally.
> - **No** — the comment *asserts* it and the code is merely **consistent** with it.
>   **Cap at `confidence: low`**, however convincing the prose. Say in the finding that
>   the source is a comment.

⚠ **A comment naming a build number, an error string or an exonerated hypothesis raises
specificity, not tier.** It is still one Tier-3 source, and specificity is exactly what
makes it read as measured.

Calibration from the run that produced this rule: of ~51 facts, **2** were purely
comment-sourced — an addon-reported taint edge and a claim about init timing. Both were
graded medium on the strength of their prose; both belong at low. Expect this to move a
handful of facts per run, not most of them.

### 2.1 Find the version gate BEFORE you read a line — a fact's PATCH is part of the fact

⚠ **Do not try to solve this by checking out an old tag.** Live addons dual-target: one
codebase declares every interface it supports and branches at **runtime**. EllesmereUI
is the worked example — 374 tags, **one branch**, and *every* tag from v8.5.6 to v8.7.5
declares the identical `## Interface: 120000, 120001, 120005, 120007, 120100`. There is
no 12.0.7-only version to check out. An older tag gives you less material and the same
dual-target design.

The split lives in the source, and it is greppable:

```bash
grep -rn "GetBuildInfo\|WOW_PROJECT\|Is[A-Za-z]*PTR\|tocversion" --include=*.lua <root> | grep -v /Libs/
ls <root>/*/*_1[0-9][0-9].lua        # per-patch file variants
```

For EllesmereUI that is one line — `EllesmereUI.IS_121 = (select(4, GetBuildInfo()) or
0) >= 120100` (`EllesmereUI_Lite.lua:15`) — used **103 times**, plus two `*_121.lua`
files. Find the equivalent flag first and write it into your notes, because:

**A fact reached through a next-patch gate is a NEXT-PATCH fact.** It may not be written
into a `patch: 12.0.7` body. It goes to the PTR/next-patch parking doc
(`knowledge/addon-dev/<version>-ptr-heads-up.md`), which exists precisely to hold
patch-day edits that are not yet true. Getting this wrong is how a KB claim becomes a
live bug: the code demonstrably works — next patch.

Three outcomes, all worth writing:

- **Confirms** an existing KB claim → add the citation, don't restate the claim.
- **Corrects** one → that is the highest-value result. Fix the claim, and say plainly
  what the old reasoning got wrong (see §4.8.1 finding 10 for the shape).
- **New fact** → new subsection, with confidence set by how well Tier 1 corroborates.

---

## 3. Procedure

**Step 0 — locate, don't duplicate.** If the addon is installed
(`…/_retail_/Interface/AddOns/<Name>/`) read it there; that copy is transient and gets
replaced on update. Clone only if it is not installed or you need history. Clone into
`raw/addon-research/` — **`raw/*` is gitignored**, so it can never enter the repo.
Record the version (`.toc` `## Version:`) and the license verbatim before anything else.

**Step 1 — survey, and pick targets by question.** Do not read an addon end to end;
most of it is UI chrome that asserts nothing. Start from what the KB wants to know:

```bash
# The high-value surfaces, in rough order of payoff for this workspace:
grep -rln "issecretvalue\|SecretAspect\|HasSecretAspect\|canaccess" <root> --include=*.lua
grep -rln "SetTimerDuration\|DurationObject\|C_DurationUtil\|C_CurveUtil" <root> --include=*.lua
grep -rln "SetAttribute\|SecureHandler\|RegisterUnitWatch\|taint" <root> --include=*.lua
grep -rln "C_CooldownViewer\|CooldownViewer" <root> --include=*.lua
grep -rln "AuraContainer\|AuraButton\|ForbiddenAspect" <root> --include=*.lua   # 12.1.0
```
Exclude `Libs/` — third-party libraries are separately licensed and separately known.

**Step 2 — fan out.** Give each subagent ONE surface and the §1 + §2 rules in full.
Require each to return **facts only** — a list of `{claim, why it is load-bearing,
file:line, Tier-1 corroboration, confidence}` — and to state explicitly when it found
nothing, because "this surface had no findings" is a result that stops the next person
re-reading it. ⚠ A subagent that returns code snippets has failed the task; re-prompt it.

**Step 3 — corroborate centrally.** Do §2 yourself on the merged list. Subagents are
optimistic; a fact nobody checked against the generated docs is a rumour.

**Step 4 — write.** A mined fact that survived §2 lands in **one of two places**, and the
split is this skill's whole output contract:

- **Corroborated against Tier 1** → the right `knowledge/addon-dev/` topic file
  (`security-…`, `frames-textures-animation`, `api-events-and-discovery`,
  `cooldown-manager`, `module-architecture`, `anatomy-and-runtime`).
- **Not corroborated** — Tier 3 alone, or it needs a client — →
  **`knowledge/addon-dev/mined-pending-verification.md`**, this skill's own queue, with
  the clone provenance on every entry. It is a queue, not a claim: nothing in it may be
  cited as fact until a topic file adopts it (`README.md` §1.2). ⚠ Putting an
  uncorroborated fact straight into a topic file is the failure this file exists to
  prevent — a Tier-3 rumour reading as settled because of where it sits.

Either way, update front matter: bump `reviewed:`, and **add the addon to `sources:` with
its version and a "read for API discovery only, no code copied" note.** That line is the
audit trail; it is not decoration.

⚠ **What you could not find out is also a result.** A surface you read that did *not*
answer the question is an unknown, and it is recorded the cheapest way there is: a
`` `[gap]` `` marker **on the claim** in the topic file, saying what is not known. No tool,
no ticket. A hole nobody wrote down gets re-searched by the next run.

**Step 5 — delete the clone.** `rm -rf raw/addon-research/<Name>`. The KB now carries
the facts; the source is a liability, not an asset. Skip only if the user says to keep
it. Say that you deleted it.

---

## 4. The output contract

Every mined claim lands in this shape:

> **`StatusBar:SetTimerDuration` needs a range — `SetMinMaxValues(0, 1)` first.** A
> timer *drives the value within* a range; it does not bring one. Without one the bar
> holds a valid duration object and draws 0 %.
> *Tier 1:* `SimpleStatusBarAPIDocumentation.lua:216-228, 308-320`.
> *Seen working in:* EllesmereUICooldownManager 8.5.6,
> `EllesmereUICdmBuffBars.lua:4499-4517` — read for API discovery only.
> *Confidence:* high.

Four parts, none skippable: **the fact**, **why it is load-bearing**, **Tier-1
corroboration**, **provenance + version**. If you cannot fill the third, mark it
`confidence: low` and `@verify-ingame` rather than dropping it.

---

## 5. What not to mine

- **`Libs/`** — separately licensed, and LibStub/Ace/LibSharedMedia are already known.
- **Tuning constants, colours, layout numbers** — expression, and worthless to us.
- **Anything Blizzard's own source already demonstrates.** Cite Blizzard instead; it is
  a tier higher and carries no licensing question at all.
- **Gameplay data** (rotations, spell IDs as game facts). Wrong KB entirely — that is
  the game KB, and it has its own sourcing rules.
