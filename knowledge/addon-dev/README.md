---
title: Addon-dev KB — entry point
patch: 12.0.7
fetched: 2026-07-31
reviewed: 2026-07-31
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

**Evidence classes, and how to read one.** A claim here carries a marker saying how it
is known, and the marker outranks the file's `confidence:` scalar:

- **`[client YYYY-MM-DD]`** — measured by running our own code in the client. The
  strongest class in the subtree, and the only one that knows what the docs cannot say.
  Concentrated in **`cooldown-manager.md`** (which owns the Cooldown-Manager
  measurements) and **`security-taint-and-restricted-data.md`** §4.8 onward, with a few
  in `frames-textures-animation.md` §5.1/§5.7. `grep -rl '\[client 20'` is the live list —
  do not maintain a copy of it here.
- **unmarked** — a read of Blizzard's shipped source, its generated documentation, an
  on-disk artefact, or a dated community page. Correct about *shape*. Not sufficient about
  *behaviour*: a generated-docs annotation is necessary and not sufficient, and the gap
  between the two is exactly what a measurement closes. (`SetTexture` carries
  `SecretArguments = "AllowedWhenTainted"` and the client still refuses a secret string.)
- **`@verify-ingame`** — running the code would settle this. A hypothesis.
- **`@pending-test: <id>`** — a ClientLab test with that `id` exists and flies on the next
  login/pull. **In flight, not open**, and not measured either. It becomes
  `[client YYYY-MM-DD]` when the run is drained (§1.2).
- **`[gap]`** — an honest hole.

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

### 1.1 System studies

A **system study** is organised around one Blizzard system rather than one
mechanism, for cases where this workspace has an addon built on top of it and the
model does not survive being cut across the seven-way partition. A system study
**defers to the topic files for general mechanism** and claims only what is
specific to its subject.

| File | Subject | Ask it when |
|---|---|---|
| [**cooldown-manager**](./cooldown-manager.md) | `Blizzard_CooldownViewer` — the two row families, the five-rung identity ladder, the value cascade, refresh cadence, per-family event sets, and the readable surface under secret values. Backs `CDMProbe`. | "What spellID is this CDM row *actually*?" · "Why did my cooldown read come back ready?" · "Which events does a TrackedBuff row get?" · "Why does that icon glow?" |

⚠ **`cooldown-manager.md` carries the densest run of client-confirmed claims**
(marked `[client]`), but it is no longer the only file that has any — see §0's
evidence classes for where else measurements live.

### 1.2 Queues — files that ask rather than assert

Four queues are **not** claims and must never be cited as one. A topic file asserts;
a queue file asks. Each says in its own header what would settle an entry.

| File | Holds | Drains to |
|---|---|---|
| [**observations.md**](./observations.md) | Facts **our own running code** discovered — the class that used to end up in a source comment and die with the file. Every entry carries a required `Drains to:`. | the topic file it names. `wowkb.obs check` gates a release. |
| [**mined-pending-verification.md**](./mined-pending-verification.md) | Findings from reading **third-party addons**, with clone provenance, not yet corroborated against Tier 1. | a topic file, once corroborated |
| [**12.1.0-ptr-heads-up.md**](./12.1.0-ptr-heads-up.md) | What goes wrong **on patch day** — the lines that become false. `patch:` is deliberately ahead of live. | applied at the patch, by `/update` |
| **`projects/addon-lab/questions.json`** — outside this tree | **The TEST registry**: one row per question the lab tests or could test, keyed by a stable `id`, anchored `<file>:<line>` back into these topic files. It binds a question to the Lua that tests it and the run row that answers it — the half a marker cannot do. Run by the **ClientLab** addon (`/clab`); deploy is a directory copy, not a release. | a topic file, once the question is answered |

**Put an unsettled finding in a queue, not in a topic file.** That is the rule §7.7
states, and these are where it points.

⚠ The fourth lives outside `knowledge/` on purpose — it is a **test registry with an
addon behind it**, not prose. It is indexed here anyway, because a queue an agent cannot
reach from the topic map is a queue nobody drains. **If you add a fifth queue anywhere,
index it here.** (There is deliberately no fifth. In particular the game KB's per-doc
`## TODO` section is **not** a convention here — no file in this subtree has one, and
`_meta/kb-inbox.md` is the game KB's parking lot, not this one's.)

**A *don't-know* is not filed in any of the four.** It is written **on the claim**, as a
marker in the topic file — and that is deliberate, because the other three queues each
need you to have **learned** something (our code observed it, an addon demonstrated it, a
patch will break it), and a hole you looked into and walked away from is none of those. A
marker needs no tool, no id and no row: whoever next reads the claim reads the marker, at
exactly the moment it matters.

**The marker carries the whole lifecycle:**

| Marker | State |
|---|---|
| `[gap]` · `[unverified]` · `@verify-ingame` | open — nobody is on it |
| `@pending-test: <id>` | a `ns.Test{}` with that id is in ClientLab and flies on the next login/pull; the row is `built` |
| `[client YYYY-MM-DD]` | measured and drained; the marker is gone and the claim is rewritten |

⚠ **A marked claim you are about to BUILD ON is a STOP** — surface it and ask, never assume
silently. That is the one thing this subtree does not let accumulate, alongside a measured
answer that has not reached the KB (`wowkb.obs check`). **An open marker, by contrast, has
no clock, no cap and no gate**: the trigger for testing an unknown is *use*, not age, and
this file's `[gap]`s are a catalogue rather than a backlog. Do **not** sweep them into the
registry — many are epistemics warnings against a tempting inference, which is prose doing
its job, and a question earns a row when somebody decides to **test** it.
(`wowkb.lab blocked` shows the rows nobody is testing, grouped by the capability each
waits on.)

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

The lesson to carry forward is **re-derive before you act**, not "distrust everything".
The corrections themselves belong in a file's `## Changelog`, one line each — see §7 for
how a claim is written here.

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

Every topic file ends with **"Rules we could audit against"** — roughly two hundred
numbered, individually-cited statements, written to be decidable by grep or by reading
a call site rather than by taste. `cooldown-manager.md` carries its own set too. That
section is the point of the KB, not an appendix.

⚠ **No exact census is kept here, deliberately.** The files number rules differently
enough that any single grep miscounts several of them, so a precise total in this file
would be wrong within a patch and would be believed. Count the file you care about.

⚠ **A rule and the body section it audits must be edited together.** Every rule
restates a body claim, so a correction applied to one and not the other is invisible to
any single-file read — that is exactly how the pool-proxy count and the secure-snippet
`table` claim each stayed wrong for weeks. Prefer a rule that asserts and cites its
section over one that re-argues it.

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

## 6. Known weaknesses of this KB

Stated plainly so nobody has to rediscover them.

- **Most of this subtree has not been run in the client**, and that remains the
  single biggest limitation. The exceptions carry a `[client YYYY-MM-DD]` tag (§0);
  everything else is a source read, and every `@verify-ingame` marker is a real open
  question.
- **This subtree's markers are meant to be invisible to `wowkb.gen_verify`, and that
  is a decision, not a bug.** `gen_verify` treats a marker written inside
  `` `backticks` `` as prose (`gen_verify.py` `_strip_code`), so a backticked marker
  stays out of `_meta/verify-in-game.md`. *By design*: §0 sets a hard firewall between
  game data and engineering guidance, and pouring engineering questions into a
  game-side checklist would break it — you would be asked to test `table.freeze` while
  standing at an obelisk.
  The raw view, and the honest one, is
  `grep -rn '@verify-ingame' knowledge/addon-dev/`; the leaked count is whatever that
  reports with **no** surrounding backticks. Do not "correct" a backticked marker to a
  bare one — a bare marker here is a leak, not an open item.
  ⚠ **Backticking hides the marker from `gen_verify`, not from a reader.** Nothing
  harvests these into a checklist, and nothing needs to: the marker sits **on the claim**,
  so it is met at the point of use, by whoever is about to build on it (§1.2). What a
  backticked marker must never become is *silent* — do not delete one to tidy a paragraph,
  and do not soften the claim it sits on so the marker looks unnecessary.
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

---

## 7. How a claim is written here — the current-state rule

**A topic file states what is true now. It never states what it used to say.**

1. **Correcting a claim means rewriting the claim.** Edit the sentence, the table cell,
   the number, in place. Do **not** leave the old text standing under a correction note.
   If a reader can get the wrong answer by reading top-down or by grepping a single line,
   the edit is not finished.
2. **History goes in one place or nowhere.** If the *fact that we were wrong* is itself
   worth keeping — because it would otherwise be re-derived, or because it burned a
   release — it is **one line** in a `## Changelog` at the bottom of the file:
   `2026-08-04 — §4.8 duration sinks: "carries" ≠ "displays"; aspect-less, no readback.`
   Cap: 20 entries or 2 KB, whichever comes first; drop entries older than two patches.
   Anything longer belongs in `projects/<addon>/docs/`.
3. **A measurement is a claim plus a tag, not a story.** Write the claim in the present
   tense and tag it `[client YYYY-MM-DD]`. **One** sentence of method is allowed if the
   method is load-bearing. The spec, the character, the addon build, what we tried first
   and how many builds it cost are session facts — they go in the project docs.
4. **Dates appear in exactly four places:** front matter (`fetched`/`reviewed`), a citation
   stamp, a `[client YYYY-MM-DD]` provenance tag, and the `## Changelog`. **A date in prose
   is a defect.** A citation stamp is any bracketed tier tag carrying the date *inside* the
   brackets — `[T2 wiki: …, revid X, 2026-02-19]`, `[T2 bug: WoWUIBugs#414, closed 2025-03-07]`.
   An external event's date (a bug filed, an issue closed, a repo last pushed) **is**
   provenance and keeps its date — put it in the citation, not in the sentence.
5. **No numbered "findings" list in a reference body.** A finding is merged into the
   section it amends. Out-of-order ordinals are the signature of a file being appended to
   instead of edited.
6. **A claim is scoped to the API, not the call site.** "`SetText` with a secret marks
   anchoring secret" — not "our FontString broke because…". If a fact is only true of
   CDMProbe/Demonology/one build, it is not a KB fact; it belongs in the project.
7. **Unsettled findings do not go in a topic file at all.** They go in a queue (§1.2).
   A topic file asserts; a queue file asks.

### The gates

`wowkb.kblint` runs these in CI. Each must return zero.

```bash
# 1 — no retrospective prose outside a Changelog section
awk '/^## Changelog/{skip=1} skip{next} 1' knowledge/addon-dev/*.md \
| grep -nEi 'an earlier (draft|version|pass|run|note)|previously (said|read|cited|written|showed|gave|asserted)|\[corrected|used to (be|read|say|assert|show)|GRADE CORRECTION|\*\*Correction|Adversarial verification pass'

# 2 — every date sits in front matter, a citation, a [client] tag, or the Changelog.
# ⚠ The Changelog is skipped by CONTENT, not by its heading line — rule 2 mandates dated
# entries there, so a file that complies must not fail its own gate.
# The three QUEUES are exempt: a queue entry IS a dated event (§1.2). So is sources.md,
# a registry whose rows are "what was on disk, when".
for f in knowledge/addon-dev/*.md; do
  case "$f" in *observations.md|*mined-pending-verification.md|*12.1.0-ptr-heads-up.md|*sources.md) continue;; esac
  awk '/^## Changelog/{skip=1} skip{next} 1' "$f" \
  | grep -nE '20[0-9]{2}-[0-9]{2}-[0-9]{2}' \
  | grep -vE '\[(T[0-9][^]]*|client) 20|revid [0-9]+, 20|pushed_at 20|created_at 20|^[0-9]+:(patch|fetched|reviewed|title|sources|  -)' \
  | sed "s|^|$f:|"
done

# 3 — no section corrected by a later part of the same file
grep -nE '(⚠⚠?|❌).{0,120}§[0-9]' knowledge/addon-dev/*.md
```
