---
title: Addon-dev KB — entry point
patch: 12.0.7
fetched: 2026-07-23
reviewed: 2026-07-23
sources:
  - ./sources.md
  - https://github.com/Gethe/wow-ui-source (live, version.txt 12.0.7.68887, commit 4383ced30106d51b27e3e86d1987f1552f0d259d)
  - https://warcraft.wiki.gg/
  - https://github.com/Stanzilla/WoWUIBugs
confidence: high
---

# World of Warcraft addon development — Retail, Midnight 12.0.x

## 0. This is development guidance, not game data

**Everything under `knowledge/addon-dev/` is about writing code. Nothing in it is
about playing the game.** The rest of `knowledge/` is a Retail/Midnight *game*
knowledge base — rotations, gearing, weeklies, raids, professions — governed by
this repo's staleness doctrine and answered with in-game facts. This subtree
answers a different kind of question: *"how does `SetAttribute` interact with
taint"*, not *"what should I press next"*.

The two must not be blended:

- **A question about the game** (`what ilvl does a +10 vault slot give?`) is
  answered from `knowledge/endgame/`, `knowledge/classes/`, or live tools. Never
  from here.
- **A question about addon code** (`why is my frame blocked in combat?`) is
  answered from here, from Blizzard's shipped UI source, and never from the game
  KB.
- The **tiering vocabulary is also different.** The game KB's tiers (`_meta/sources.md`:
  Blizzard API / wago.tools / logs / Icy Veins / Reddit) are about *game* sources.
  This subtree defines its own tiers in [`sources.md`](./sources.md) §0, about
  *engineering* sources. `Tier 1` does not mean the same thing in the two places.

What the two subtrees *do* share is the front-matter convention (`patch`,
`fetched`, `reviewed`, `sources`, `confidence`) and the `@verify-ingame` marker.
**Nothing in this subtree has been executed in the client** — every claim is a
read of source, generated documentation, shipped artefacts on disk, or a dated
community page. Items where running the code would change the answer are marked
`@verify-ingame` throughout.

**Scope**: Retail, patch **12.0.7** (Midnight), build **12.0.7.68887**. Classic
flavours appear only where a `.toc` mechanism forces them into view. Anything
describing `Interface/FrameXML/` as a top-level directory, or discussing taint
without mentioning secret values, is describing a dead version of the client.

---

## 1. Topic map

Seven files, partitioned so that **any addon-dev question lands in exactly one**.
Each ends with a **"Rules we could audit against"** section (see §4).

| File | Owns | Ask it when |
|---|---|---|
| [**anatomy-and-runtime**](./anatomy-and-runtime.md) | What an addon physically *is*: the folder + `.toc` manifest, the directive set (and which directives are Blizzard-only), load order, dependencies, load-on-demand, the shared Lua 5.1 sandbox, the login/logout/`/reload` lifecycle, error handling, `C_AddOns`/`C_AddOnProfiler`. | "Why isn't my file loading?" · "When can I read my SavedVariables?" · "Is `os.time` available?" · "What fires at login, in what order?" |
| [**api-events-and-discovery**](./api-events-and-discovery.md) | The programming model: the four ways code gets called (script handlers, game events, callback registries, timers), event registration and its Midnight callback API, the combat-log change, `OnUpdate` vs `C_Timer` vs dirty flags, the shape of the 6144-function API surface — **and how to find things out yourself** (`/api`, `/eventtrace`, `wowkb.uiapi`, the wiki's blue-post archive). | "What's the payload of this event?" · "Should this be an `OnUpdate` or a ticker?" · "Does this function exist?" · "How do I look this up next time?" |
| [**frames-textures-animation**](./frames-textures-animation.md) | Everything drawable: the widget type graph, `CreateFrame` vs XML vs templates vs mixins vs intrinsics, anchoring and size, the three z-orderings (strata / level / draw layer), textures and their **four independent channels**, fonts and media, the animation system, object pooling, attaching to Blizzard's frames. | "Why is my texture behind that one?" · "Does `SetVertexColor` clobber `SetGradient`?" · "What does a pool resetter have to clear?" |
| [**security-taint-and-restricted-data**](./security-taint-and-restricted-data.md) | **Three separate systems**: protected actions / combat lockdown (patch 2.0), taint (patch 2.0), and secret values (**new in 12.0**). Secure templates, handler snippets, state drivers; the `SecretArguments` three-way; aspects, predicates, curves and duration objects. | "Why is this blocked in combat?" · "Why is Blizzard's file erroring?" · "Can I do arithmetic on `UnitHealth`?" · "How do I show a cooldown I'm not allowed to read?" |
| [**module-architecture**](./module-architecture.md) | How to split an addon across files and objects — and which of those choices the *game* constrains rather than taste. The `ns` namespace table, four module-registration patterns, the data/display seam, and the three platform-specific pressures (taint boundary, pooling, the SavedVariables format). | "How should I lay this addon out?" · "Do I need Ace3's addon object?" · "Where does my state live?" |
| [**state-persistence-and-communication**](./state-persistence-and-communication.md) | Data that outlives a frame or leaves the client: the three SavedVariables scopes, **when the file actually hits disk**, schema migration, settings/profiles, serialization + compression (including Blizzard's new `C_EncodingUtil`), addon messaging, and Midnight's chat-messaging lockdown. | "Why is my capture stale?" · "How do I migrate saved data?" · "Why did my addon message fail?" |
| [**libraries-and-ecosystem**](./libraries-and-ecosystem.md) | The shared infrastructure: what a "library" physically is, LibStub and its failure modes, embedding vs externals (`.pkgmeta`), Ace3 component by component, **what Blizzard now ships that used to need a library**, a maintenance-status register, and what each mature addon is worth reading *for*. | "Do I need this library?" · "Is this library dead?" · "Why doesn't the repo contain its own libs?" |

**Boundary calls worth knowing**, because they're the ones that look ambiguous:

- *Widget methods being `IsProtectedFunction`* — the **flag** is documented in
  `frames`; what it **means at runtime** is `security`'s claim. `frames` is
  deliberately restrained here and points across.
- *Hooking* — the mechanics and its use as a discovery instrument are in
  `api-events`; the taint consequences are in `security`.
- *Object pools* — the widget-lifecycle view (resetters, proxies, what leaks) is
  in `frames`; the "this shapes your architecture" view is in `module-architecture`;
  the "a secret in a pool poisons every later acquire" view is in `security`.
  All three cite the same `Pools.lua` and agree.
- *`.toc` directives* — the catalogue is in `anatomy`; `module-architecture`
  covers only the ones that change **code structure** (`LoadSavedVariablesFirst`,
  `AllowAddOnTableAccess`, LoD partitioning).
- *SavedVariables* — the load-order fact is in `anatomy`, the format and flush
  semantics are in `state-persistence`, the "your model must be a plain-data tree"
  consequence is in `module-architecture`.

[**sources.md**](./sources.md) is the eighth file and is not a topic: it is the
source registry — what is on disk, at which commit, what each source is good and
bad for, and where the holes are. **Read its §0 (tiers) and §7 (per-topic
routing) before adding to any topic file.**

---

## 2. Deliberate omissions

These were **cut from scope on purpose.** They are not oversights, and nobody
should assume the KB "just hasn't got to them yet".

### 2.1 Packaging and distribution — cut

The BigWigs packager (`release.sh`, `.pkgmeta`, `@build-type@` keyword
substitution, multi-flavour toc splitting, GitHub Actions release workflows,
CurseForge / WoWInterface / Wago upload) has **no topic file**.

*Why:* this workspace does not distribute addons through that pipeline. The three
addons here (`BucketBinds`, `CDMProbe`, `PlannerState`) ship via
`wowkb.addon release` → a GitHub release → `ghaddons` into the local install,
which is documented in the repo root `CLAUDE.md` and `addon-manager/README.md`.
A packaging topic would have been research with no consumer.

*What survived anyway, because other topics need it:* `.pkgmeta` **externals** are
covered in `libraries-and-ecosystem` §3.3 (they are why grepping a clone for
`LibStub` finds nothing) and `.pkgmeta` **`move-folders`** in `module-architecture`
§5.4 (one git repo ≠ one shipped addon). The packager clone is registered in
`sources.md` §3.5 if the topic is ever wanted.

### 2.2 The everyday dev loop and tooling — cut

An eighth topic on the edit→`/reload`→read-the-error cycle — luacheck/luaparser
config, EmmyLua/LuaLS annotations in an editor, `/console scriptErrors`, BugSack,
symlinking an addon folder into the install, in-game print/debug discipline — was
**dropped before research started**.

*Why:* it is the topic most specific to one developer's machine and least
transferable, and the parts of it that are load-bearing are already owned
elsewhere: `/reload` semantics are `anatomy` §7, the in-client discovery tools
(`/api`, `/eventtrace`, `/dump`, `/fstack`, `/tinspect` — including the gates
that make them silently produce nothing) are `api-events` §5.1, taint diagnosis
(`taintLog`, `ADDON_ACTION_BLOCKED`, `issecurevariable`) is `security` §2.3, and
error handling is `anatomy` §5.4. This repo's own dev loop lives in
`projects/*/CLAUDE.md` and the addon sub-repos.

*The honest cost of the cut:* there is **no** single place here that says "here is
how to set up to write an addon", and `sources.md` §6 already records that no
Blizzard-authored tutorial exists at any tier. If someone new joins, that gap is
the first thing they will hit.

### 2.3 Also out of scope, for the record

- **Classic / Cata / MoP flavours.** Retail Midnight only, per the repo's scope.
  Flavour mechanics appear only as `.toc` machinery.
- **Anything requiring the client to be running.** No claim here was tested
  in-game; see §3.
- **Addon *product* design** — UX, what makes a good addon — as opposed to how
  the platform works.

---

## 3. How this KB was built, and what that means for trusting it

Three phases, deliberately in this order.

**Phase 1 — source registry first.** Before any topic was written,
[`sources.md`](./sources.md) was produced: clone Blizzard's shipped UI source at
the live build, inventory the live game install, test which community sources are
actually *fetchable* from this machine, define the tier ladder, and write down the
holes. Two tools were built because the sources resisted ad-hoc use —
`wowkb.uiapi` (indexes Blizzard's 592-file generated API spec and emits results
already in `file:line` form) and `wowkb.wiki` (raw wikitext with revision ids and
timestamps, instead of WebFetch's undated paraphrase). The registry also names the
sources to **avoid**, with a worked falsification of the most plausible-looking one
(an AI-generated "WoW Addon Development Guide" that is wrong on checkable points).

**Phase 2 — per-topic research, each against the registry.** Seven topics,
each routed to a starred primary source by `sources.md` §7. Standing rules: cite
Blizzard source as `file:line` against a named build; stamp every wiki citation
with its revision id **and** last-edit date, because wiki pages rot silently;
never promote a Tier-3 observation ("WeakAuras does X") to a rule; never
generalise from one addon; and where something could not be established, write an
explicit **`[gap]`** saying what was looked for and where.

**Phase 3 — adversarial verification.** Every file was then re-checked by a pass
whose brief was to *refute* it: re-open every locator, independently re-derive
every corpus count, re-fetch every wiki revision. This was not a formality —
**124 of 438 checked claims (28%) did not survive**:

| File | Claims checked | Refuted |
|---|---:|---:|
| frames-textures-animation | 63 | **28** |
| module-architecture | 64 | 19 |
| security-taint-and-restricted-data | 62 | 17 |
| anatomy-and-runtime | 63 | 16 |
| state-persistence-and-communication | 63 | 16 |
| libraries-and-ecosystem | 52 | 16 |
| api-events-and-discovery | 71 | 12 |
| **total** | **438** | **124** |

**What that number means, and what it does not.** It is not a defect rate in the
finished text — every one of the 124 was corrected before publication. It is a
measure of *how wrong a careful first pass is on this material*, and it is the
single most important thing to know about this KB. The refutations were not
typos; they were the kind of error that reads as authoritative:

- **Direction reversed.** The bare `acos/asin/atan/atan2` globals were described
  as taking degrees. They take a plain ratio and *return* degrees, while
  `sin/cos/tan` take degrees. Code written to the wrong version is silently wrong.
- **Inferred mechanism stated as fact.** "The frame-attribute store here is a
  taint barrier" — the code is a plain refcount with no comment saying so. Cut,
  not softened.
- **A conclusion that contradicted its own citation.** The claim that four
  `Cooldown` setters "do accept secret arguments" rested on the absence of
  `NotAllowed` while ignoring that `AllowedWhenUntainted` excludes all addon code.
- **Counts that were artefacts of the grep**, not of the corpus — see §5.
- **"Blizzard always does X"** where Blizzard's own tree contains a counterexample
  (`GridLayoutFrameMixin:Layout` returns early without `MarkClean`).

Because of this, the files carry an unusual amount of **visible self-correction**:
inline `[corrected 2026-07-23]` notes saying what the earlier draft claimed and
what the source actually says. That apparatus is deliberate. Do not clean it up —
it is how a reader who saw an earlier version knows what to un-learn, and it is
the record that a claim was *checked* rather than merely *written*.

**How to read a claim here.** Every claim states the tier of its strongest
evidence. `[T1 src]`/`[T1 docs]` = Blizzard's shipped source or generated spec at
build 12.0.7.68887, verifiable by `file:line`. `[T1 obs]` = observed on the live
install (an artefact, not a spec). `[T2 wiki]` = warcraft.wiki.gg with a revid and
date — **check the date**, several load-bearing pages are years stale.
`[T2 bug]` = a WoWUIBugs issue, which is evidence of *observed behaviour* and,
where labelled `Acknowledged by Blizzard`, evidence Blizzard agrees it is a bug —
**never** evidence of intended design. `[T3]` = one named addon at one named
commit: a data point, never a rule.

**The strongest and weakest ground.** The security topic has the best Tier-1
evidence in the set — Blizzard's generated docs machine-annotate the entire
restriction surface, so counts like "59 protected widget methods", "120 functions
accept secrets from tainted code" are exact and reproducible. The weakest is
anything about *behaviour over time*: what an annotation means, what error text
you get, what happens when two systems interact. Blizzard documents **shape**, not
semantics — only 858 of 9521 doc entries carry any prose at all, and several
annotations that rules would love to lean on (`SynchronousEvent`, `UniqueEvent`,
`SecureHooksAllowed`, `HasRestrictions`) are **defined nowhere**. Where a file
leans on one of those, it says `[inference]` and the rule is advisory.

---

## 4. The intended next use: audit this workspace's three addons

Every topic file ends with **"Rules we could audit against"** — **204** numbered,
individually-cited statements (anatomy 25 · api-events 30 · frames 40 · security
31 · module 25 · state-persistence 25 · libraries 28), written to be decidable by
grep or by reading a call site rather than by taste. That section is the point of
the KB, not an appendix.

The intended consumer is this workspace's own addon code:

- `projects/cooldown-hud/addon/` — **CDMProbe**. The highest-value target: it
  skins Blizzard's Cooldown Manager and reads cooldown/aura state, so it sits
  directly on the Midnight secret-value seam. `security` §4.5/§4.8 (secret
  arguments; the curve/duration route for cooldown timing), `frames` §5 (texture
  channels, pooling) and `state-persistence` §2 (its capture protocol depends on
  "SavedVariables only flush on `/reload`", which that file independently
  confirms) all bear on it.
- `projects/keybinder/addon/` — **BucketBinds**. Sets keybinds and action-bar
  slots in bulk, i.e. it lives on the *protected action* seam rather than the
  secret one: `security` §1 and §3, and `anatomy`'s `.toc`/lifecycle rules.
- `planner-state/PlannerState/` — **PlannerState**. A dump-and-persist addon:
  `state-persistence` in full (scopes, flush points, schema versioning,
  `PLAYER_LOGOUT` hazards — including WoWUIBugs #748, which is precisely "API
  calls that silently return nothing during a *real* logout but work in
  `/reload`", a failure mode that addon is exposed to).

**How to run an audit, given §3.** Rules are not equal and must not be applied as
if they were:

1. **Tier-1 rules are pass/fail.** ("`Frame:CreateFontString` takes three
   documented parameters, not four.")
2. **Tier-2 rules are flag-don't-fail.** A dated wiki page is a plausible source,
   not a fact about the client.
3. **Rules marked `[inference]` or resting on an undefined annotation are
   advisory only** — flag for a human, never auto-fix.
4. **Tier-3 rules are "your code is consistent with N of the surveyed addons"**,
   which is a conversation, not a finding.
5. **A rule that fires should be re-derived against the source before acting on
   it.** Phase 3 refuted 28% of a careful first pass; the rules are better than
   that now, but the discipline is the point.

A second use, lower effort and immediate: the **`@verify-ingame` markers**. They
are real, testable, one-line questions (`/dump type(require), type(os), type(io)`
settles the Lua-surface gap; `C_AddOns.DoesAddOnExist("LibStub")` settles the
nested-`.toc` question). Someone logged in could close a dozen of them in a
session, and each closure upgrades a `[gap]` to a fact.

---

## 5. Cross-file reconciliation — disagreements found and what was done

The seven topics were researched independently, so they were cross-checked
against each other on 2026-07-23. Findings, all resolved rather than papered over:

**Resolved by re-deriving the number.**

- **Load-on-demand counts.** `anatomy` §4.3 said "167 of 346 shipped tocs" are
  LoD; `module` §5.4 said 125. Both greps reproduce — **but 42 shipped tocs
  declare `## LoadOnDemand: 0`**, the explicit opposite. 167 is a line count,
  125 is the semantic count. `anatomy` §4.3 and its rule 20 were **corrected to
  125/346 and 45/147**; `sources.md` §1.1 now flags its own 167 as a line
  frequency.
- **`sources.md` annotation counts.** Its §1.2 table mixes function-only counts
  with corpus totals, which is why `HasRestrictions` reads 231 there and 236 in
  `security`. Both are right for what they count (231 functions + 5 events).
  One entry — `SecretWhenUnitIdentityRestricted` **12** — was simply **wrong**
  (15). `sources.md` now carries the re-derived table and a note that the topic
  files' numbers win.
- **"51 secret predicates."** Only 19 are `Type = "Secret"`; 32 are
  `Type = "Precondition"`, and the two kinds behave differently (value vs call).
  `sources.md` relabelled.
- **Doc-file count.** 592 `.lua` + 1 `.toc` = 593 entries. `sources.md` said
  "593 Lua files"; corrected.
- **oUF's size.** 784 K in `sources.md` includes `.git`; 504 K in `libraries`
  does not. Both now shown.

**Resolved as a measurement artefact — the most instructive one.**

- **Addon-namespace adoption.** `anatomy` §5.2 reported Details **111** files
  binding the `...` vararg and WeakAuras2 **7**; `module` §2.3 reported Details
  **8** and WeakAuras2 **128**. Nearly inverted, and both greps reproduce exactly.
  Cause: `module`'s regex (`^local [A-Za-z_, ]+= *\.\.\.`) has **no digits in its
  character class**, and Details' namespace local is spelled `Details222` — so it
  missed 103 files. `anatomy`'s regex requires **two** identifiers, and WeakAuras
  writes `local AddonName = ...` — so it missed 121. **Details = 8 was corrected
  to 111**; the WeakAuras divergence is left standing in both files with a
  cross-reference, because it is a genuine difference in what is being counted.
  The lesson, now stated in both files: *a corpus count is only as good as its
  regex — cite the regex with the count.*

**Resolved by correcting an over-read.**

- **The Cooldown-setter falsification** in `sources.md` §4 concluded those four
  setters "do accept secret arguments" from the absence of `NotAllowed`. They are
  `AllowedWhenUntainted`, and **all addon code is tainted** — so from an addon
  they do not. `security` §4.5 caught this; `sources.md` now carries the
  correction. (The verdict on the AI-generated guide is unchanged: do not cite it.
  But this particular refutation should not be reused as written.)
- **"Wiki-only globals."** `sources.md` listed `issecretvalue`,
  `hasanysecretvalues` and `scrub` as Tier-2-only. All three are **Tier 1**,
  documented in `FrameScriptDocumentation.lua`, along with the whole
  secret-testing family. `security` §4.4 caught it; `sources.md` §1.2 and §7 are
  fixed.
- **`## Secure`.** `sources.md` called it Blizzard-internal alongside the
  documented-restricted directives. It is **undocumented**, not
  *documented-as-restricted* — a distinction both `anatomy` §2.3 and `module`
  §5.1/rule 17 insist on. `sources.md` now makes it too.

**Left standing as a real divergence, with the reason recorded.**

- **"The seven clones" is not the same seven.** `anatomy`, `frames`, `security`
  and `module` survey WeakAuras2 · BigWigs · Details · Plater · ElvUI · oUF ·
  **Ace3**; `libraries` substitutes **Bagnon** for Ace3 (Ace3 being its subject,
  not its sample). So "4 of 7" in one file is not over the same population as
  "4 of 7" in another. Noted in `sources.md` §3.1. Independence is worse than
  n=7 in both sets — Details and Plater share an author and a framework, and
  ElvUI vendors oUF — so treat effective n as ~5.
- **ElvUI's secure-template footprint** is 21 files in `security` §3.4 and 16 in
  `libraries` §11. Different greps (`security` also matches `RegisterStateDriver`
  and `SecureGroupHeader`, and searches `.xml`). Both publish their command; no
  correction needed.
- **BigWigs `IsSecret` line numbers** differ between `sources.md` §3.1 and
  `security` §5 because they cite *different call sites* (guard sites vs the
  compat-shim aliases), not the same one twice.

**Registry additions.** `sources.md` gained a §3.8 recording sources the topic
agents used that predated no entry: the **Bagnon** clone, **`gh api`** repository
metadata, **WoWInterface's `api.mmoui.com` file list**, `wago.tools/api/builds`,
raw-wikitext line numbering, the specific WoWUIBugs issues relied on, and the
live `WTF/` tree used as a persistence-format corpus.

---

## 6. Known weaknesses of this KB

Stated plainly so nobody has to rediscover them.

- **Nothing has been run in the client.** This is the single biggest limitation.
  Every `@verify-ingame` marker is a real open question.
- **This subtree's markers are deliberately invisible to `wowkb.gen_verify`, and
  that is a decision, not a bug** (recorded 2026-07-23 during the W1 design).
  `gen_verify` treats a marker written inside `` `backticks` `` as prose
  (`gen_verify.py` `_strip_code`), and **64 of this subtree's 68 markers are
  backticked**, so `_meta/verify-in-game.md` lists **zero** addon-dev items.
  *Left that way on purpose*: §0 above sets a hard firewall between game data and
  engineering guidance, and pouring ~45 engineering questions into a game-side
  checklist of 29 would break it — you would be asked to test `table.freeze`
  while standing at an obelisk. The registry for this subtree is instead
  `projects/addon-lab/questions.json`, keyed by a **stable id** rather than by
  marker text, so an id survives the line moving. `grep -rn '@verify-ingame'
  knowledge/addon-dev/` remains the raw view.
- **Blizzard's actual developer channel is unreadable.** Its technical addon-API
  posts go to the **WoWUIDev Discord**, which is not publicly fetchable. Every
  Blizzard *statement* quoted in this KB reaches us through warcraft.wiki.gg's
  verbatim blockquote archive of those posts — Tier-1 content through a Tier-2
  channel. There is no official tutorial, no error-semantics reference, and no
  migration guide at any tier (`sources.md` §6).
- **Three build numbers are in play.** `wow-ui-source` = 12.0.7.**68887**,
  `BlizzardInterfaceResources` = 12.0.7.**68256**, and this repo's
  `_meta/game-version.md` records live as 12.0.7.**68453**. Same patch, three
  builds; the local checkout wins on conflict. The wiki's API index is stamped for
  **12.1.0 (68301) PTR**, i.e. a build ahead of live, so a wiki page may describe
  something that is not deployed.
- **Semantics are thinner than shape.** See §3. Where a rule leans on an
  undocumented annotation it says `[inference]`.
- **`frames-textures-animation` carries the most unresolved gaps** (16 listed),
  and the most consequential is §5.3: whether `SetVertexColor` and `SetGradient`
  write the same storage is **not established at any tier**, with a concrete
  in-game test written out. It is also the file the adversarial pass hit hardest
  (28 of 63), which is consistent — it is the broadest surface with the most
  Tier-1 detail to get subtly wrong.
- **No topic came back thin**, but two are structurally softer than the rest and
  say so in their own front matter: **`module-architecture`** (`confidence:
  medium`) because the platform genuinely mandates almost nothing above "an
  ordered list of files and one private table" — most of it is necessarily
  Tier-3 pattern-reporting; and **`libraries-and-ecosystem`** (`confidence:
  medium`) because adoption evidence is unobtainable from this machine
  (CurseForge 403, wago.io 401), so every "widely used" is a count of copies on
  **one** install. Both are honest about it; neither needs re-running, but both
  would improve most from evidence this box cannot reach.
