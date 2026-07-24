---
title: Addon-dev KB — source registry
patch: 12.0.7
fetched: 2026-07-23
reviewed: 2026-07-23
sources:
  - https://github.com/Gethe/wow-ui-source (live branch, 12.0.7.68887)
  - https://warcraft.wiki.gg/api.php
  - https://github.com/Stanzilla/WoWUIBugs
  - https://www.townlong-yak.com/framexml/
confidence: high
---

# Source registry for the addon-dev KB

This file is the **map every addon-dev topic file must be researched from**. It
records what is on disk, at which commit, what each source is good for, what it
is *not* good for, and where the honest holes are.

Read §0 (tiers) and §7 (per-topic routing) first. Everything else is reference.

---

## 0. Tier definitions used here

| Tier | Meaning | Confidence you may claim |
|---|---|---|
| **1** | Blizzard's own shipped artefacts — the UI source, its machine-generated API documentation, the `UI.xsd` schema, official Blizzard articles. Verifiable by file:line against a build number. | `high`. State the build. |
| **2** | warcraft.wiki.gg and Blizzard-monitored trackers (WoWUIBugs). Community-written but corrected by practitioners, and — critically — the **only accessible archive of Blizzard's addon-dev blue posts** (see §2.1). | `medium`–`high`. Always stamp the revision date. |
| **3** | Mature open-source addons and libraries. These show **what works in practice**, never **what the rules are**. | `medium` at best, and only as "addon X does Y at commit Z". |
| **4** | Blogs, Reddit, SEO sites, AI-generated guides. Corroborate against Tier 1–2 or omit. | `low`. Name the source and its weakness. |

**The rule that matters:** never promote a Tier 3 observation to a rule. "BigWigs
calls `issecretvalue` before `string.upper`" is a data point about BigWigs. It is
only a *rule* if Tier 1 or Tier 2 says the operation is forbidden.

**Do not generalise from one addon.** If exactly one clone does something, say
"one of the seven addons surveyed does X" — not "addons do X".

---

## 1. Tier 1 — Blizzard's own

All clones live under `/home/mchristiansen/code/fun/wow/raw/addon-research/`
(**gitignored** via `raw/*`, verified 2026-07-23 — nothing here reaches git).
Total 340 MB. All are `--depth 1`, so `git log` shows one commit; use the
recorded SHA as the citation anchor.

### 1.1 `wow-ui-source` — Blizzard's shipped UI source ★ the primary source

```
path   : raw/addon-research/wow-ui-source
repo   : https://github.com/Gethe/wow-ui-source   branch: live
commit : 4383ced30106d51b27e3e86d1987f1552f0d259d   (2026-07-23)
build  : version.txt == 12.0.7.68887   ← matches live patch 12.0.7. Current.
size   : 48 MB · 3685 files (2298 .lua, 1028 .xml, 346 .toc, 1 .xsd)
```

Everything is under `Interface/AddOns/` — **317 `Blizzard_*` addons**. The old
`Interface/FrameXML/` and `Interface/SharedXML/` top-level dirs no longer exist;
they are now `Blizzard_FrameXML/`, `Blizzard_FrameXMLBase/`, `Blizzard_SharedXML/`,
`Blizzard_SharedXMLBase/`, `Blizzard_SharedXMLGame/`. **Any web guide that tells
you to look in `Interface/FrameXML/` is describing a pre-Midnight layout** — that
alone is a useful staleness detector on Tier 3/4 sources.

Directories that carry the most weight per topic:

| Directory | Why it matters |
|---|---|
| `Blizzard_APIDocumentationGenerated/` (593 files) | The complete generated API spec. See §1.2 — query it with `wowkb.uiapi`, do not grep it by hand. |
| `Blizzard_APIDocumentation/` (8 files) | The **in-game `/api` browser** that reads the above. `Blizzard_APIDocumentation.lua:120-139` documents the `/api search`, `/api system list`, `/api <system> list` syntax. Tier-1 proof that in-game API discovery exists and how it is spelled. |
| `Blizzard_RestrictedAddOnEnvironment/` | **The security topic's home.** `RestrictedEnvironment.lua`, `RestrictedExecution.lua`, `RestrictedFrames.lua`, `RestrictedInfrastructure.lua`, `SecureHandlers.lua`, `SecureHandlerTemplates.xml`, `SecureGroupHeaders.lua`, `SecureStateDriver.lua`, `SecureHoverDriver.lua`. This folder is **new in the Midnight-era layout** — these files used to sit loose in FrameXML. |
| `Blizzard_FrameXML/SecureTemplates.lua` + `.xml` + `SecureTemplatesBase.xml` | Secure action-button templates; the canonical protected-action path. |
| `Blizzard_SharedXMLBase/` (40 files) | The runtime primitives: `Mixin.lua`, `Pools.lua`, `CallbackRegistry.lua`, `EnumUtil.lua`, `Flags.lua`, `TableUtil.lua`, `FrameUtil.lua`, `AnchorUtil.lua`, `Color.lua`, `ObjectUpdater.lua`, `SecureTypes.lua`, `ExportUtil.lua`, `ProxyUtil.lua`. Read this before writing anything about "the runtime environment" or "module architecture" — it is Blizzard's own answer to both. |
| `Blizzard_SharedXML/` (131 files) | Widget/rendering layer: `Backdrop.lua`, `NineSlice.lua`, `AnimationTemplates.lua/.xml`, `LayoutFrame.lua`, `ManagedLayoutFrame.lua`, `HybridScrollFrame.lua`, `Interpolator.lua`, `EasingUtil.lua`, `ModelScene*`, `PixelUtilSecure.lua`, `SecureScrollTemplates.lua`, `SecureUIPanelTemplates.lua`, `HelpTip.lua`, `DataProvider.lua`. |
| `Blizzard_SharedXML/UI.xsd` (1628 lines) | **The XML schema for the entire UI markup language.** Author-attributed to Blizzard in the header comment. This is the *only* Tier-1 spec for XML frame definitions — element names, attribute enums (`FRAMEPOINT`, `FRAMESTRATA`, …), nesting rules. Cite it as `Interface/AddOns/Blizzard_SharedXML/UI.xsd:<line>`. |
| `Blizzard_EventTrace/Blizzard_EventTrace.lua` (994 lines) | The shipped event sniffer. `:988-989` registers `SlashCmdList["EVENTTRACE"]`. Primary evidence for the "event discovery" half of the api-events topic. |
| `Blizzard_DebugTools/` | `Blizzard_TableInspector.lua`, `DebugObjectUtil.lua`, `Blizzard_TexelSnappingVisualizer.lua`, `Blizzard_TextureInfoGenerator.lua`. |
| `Blizzard_ScriptErrorsFrame/`, `Blizzard_AddOnPerformance/`, `Blizzard_AddOnList/` | Error surfacing, the CPU profiler UI (`C_AddOnProfiler`), and the addon list / load-on-demand UI. |
| `Blizzard_CooldownViewer/` (26 files) | The Midnight Cooldown Manager — directly relevant to this repo's `projects/cooldown-hud/`. |
| `Blizzard_Menu/` | The modern menu system; also the densest real usage of `securecall` in Blizzard's own code. |

**`.toc` gotcha (important, anatomy topic).** The 346 shipped `.toc` files use
directives that **addons may not use**. Observed frequencies across the shipped
tocs: `Title` 346, `Author` 214, `AllowLoad` 177, `Dependencies` 176,
`LoadOnDemand` 167, `AllowLoadGameType` 146, `DefaultState` 104, `Dep` 68,
`Version` 55, `Notes` 39, `RequiredDep` 30, `LoadFirst` 19,
**`UseSecureEnvironment` 13**, `SavedVariablesPerCharacter` 10,
`SavedVariables` 10, **`Secure` 5**, `OptionalDeps` 4, `Interface` 4,
`SavedVariablesMachine` 3, `EscalateErrorDuringLoad` 3, `LoadWith` 2,
`AllowAddOnTableAccess` 1, `IconTexture` 1, `Category` 1 …
⚠ These are **line frequencies, not semantics** — 167 tocs carry a
`## LoadOnDemand` line, but **42 of them declare `: 0`**, so only **125** are
actually load-on-demand. Two topic files disagreed on this until 2026-07-23; see
`anatomy-and-runtime.md` §4.3.

Several of those are **Blizzard-internal**, but on two different footings, and
both `anatomy-and-runtime.md` §2.3 and `module-architecture.md` §5.1 insist on
the distinction: the wiki's §Restricted list names exactly **five** —
`AllowLoad`, `EscalateErrorDuringLoad`, `LoadFirst`, `SavedVariablesMachine`,
`UseSecureEnvironment` — while **`Secure` is not on it and is not documented at
all**. `Secure` (5 shipped tocs, 0 third-party) is *undocumented*, not
*documented-as-restricted*. Do not present the shipped-toc directive list as the
addon-facing one. The addon-facing list is the wiki's `TOC format` page (§2.1),
cross-checked against real third-party `.toc` files in the live install (§3.5).

**How to read it fast:** `wowkb.uiapi grep '<regex>' --type lua` (§5.1) strips the
checkout prefix so output is already citation-shaped. There is **no `ripgrep` on
this box** — the tool falls back to GNU `grep -rnE` automatically; plain `grep -r`
over 48 MB takes a few seconds, which is fine.

### 1.2 `Blizzard_APIDocumentationGenerated` — the machine-readable API spec ★★

This deserves its own entry because it is the single highest-value artefact in
the whole registry and it is easy to miss inside the checkout.

```
path : raw/addon-research/wow-ui-source/Interface/AddOns/Blizzard_APIDocumentationGenerated/
```

**592** Lua files (the directory holds 593 entries; the 593rd is the `.toc`),
build-stamped 12.0.7.68887, indexed to:

```
308 systems   77 ScriptObject (widget) tables
6144 functions  (4068 namespaced C_* · 692 globals · 1384 widget methods)
1741 events    795 enumerations   735 structures   55 constants
 51 predicate declarations (32 Precondition + 19 Secret)
```

> ⚠ **Two labels here were wrong and are corrected (2026-07-23, from the topic
> files' verification passes).**
> - **"51 secret predicates" overstates by 2.7×.** Only the **19** `Type =
>   "Secret"` declarations are secret predicates; the other **32** are
>   `Type = "Precondition"` (`RequiresValidActionSlot`, …). Re-verified by grep.
>   See `api-events-and-discovery.md` §4.1 and
>   `security-taint-and-restricted-data.md` §4.7, which also establishes that the
>   two kinds behave differently: a `Secret` predicate changes what the call
>   *returns*, a `Precondition` changes whether the call *succeeds*.
> - **"735 structures" is `Structure` (715) + `CallbackType` (20) in one bucket.**
>   `wowkb.uiapi stats` merges them. Keep them apart.

Every function entry can carry security annotations. Full observed vocabulary and
counts (from the built index — this *is* the Midnight security surface map).

> ⚠ **Read the counts below as FUNCTION-entry counts, not corpus totals**
> (2026-07-23). The index this table was built from counts function entries;
> several of these annotations also appear on **events**, and one figure was
> simply wrong. Re-derived by direct grep over all 592 doc files:
>
> | Annotation | This table | Corpus total (`grep -rh '<name> = true'`) | Note |
> |---|---|---|---|
> | `HasRestrictions` | 231 | **236** | 231 functions + 5 events |
> | `SecretInChatMessagingLockdown` | 36 | **98** | 36 functions + 62 events |
> | `SecretWhenUnitIdentityRestricted` | 12 | **15** | ⚠ plain error, not a scoping difference |
> | `MayReturnNothing` 596 · `IsProtectedFunction` 59 · `ConstSecretAccessor` 37 · `SecretWhenUnitStatsRestricted` 50 · `SecretWhenUnitAuraRestricted` 20 · `SecretReturns` 18 · `SecureHooksAllowed` 24 | | **confirmed identical** | |
>
> When a topic file's number disagrees with this table, the topic file's number —
> which states its grep — wins.

```
3677 SecretArguments   (AllowedWhenUntainted 3473 · AllowedWhenTainted 120 · NotAllowed 84)
 596 MayReturnNothing        231 HasRestrictions        82 SecretReturnsForAspect
  59 IsProtectedFunction      52 SecretArgumentsAddAspect
  50 SecretWhenUnitStatsRestricted     37 ConstSecretAccessor
  36 SecretInChatMessagingLockdown     24 SecureHooksAllowed
  23 SecretWhenAnchoringSecret         20 SecretWhenUnitAuraRestricted
  18 SecretReturns            15 ReturnsNeverSecret     14 SecretWhenCooldownsRestricted
  12 SecretWhenUnitIdentityRestricted   8 SecretWhenCurveSecret
   6 SecretWhenUnitPowerRestricted      5 SecretWhenUnitSpellCastRestricted
   4 SecretWhenInCombat       3 SecretWhenNumericFormatterSecret
(plus ~20 Requires* preconditions: RequiresClubsInitialized 83, RequiresActiveCommentator 53,
 RequiresFriendList 30, RequiresValidActionSlot 24, RequiresDeclassifiedUnitIdentity 3, …)
```

Worked example of the evidence quality available (`wowkb.uiapi func '^UnitHealth$'`):

```
UnitHealth(unit: UnitTokenPvPRestrictedForAddOns, usePredicted: bool) -> result: number
    [SecretReturns=True]
    Interface/AddOns/.../UnitDocumentation.lua:1446
```

`SecretReturns = true` with **no** conditional predicate, on only 18 functions.
Contrast `C_Spell.GetSpellCooldown`, which is `SecretWhenCooldownsRestricted` —
conditional. That distinction is exactly the sort of thing a topic file must get
right and a blog post will not.

**Limits — state these when you cite it.**
- Shape, not behaviour. Only **858 of 9521** entries carry a `Documentation`
  field. There are no examples and no error semantics.
- Global coverage is **partial**. `UnitHealth` and `GetBuildInfo` are in;
  `CreateFrame`, `hooksecurefunc`, `issecure`, `issecurevariable`,
  `forceinsecure`, `securecall` are **not**.
  ⚠ **`scrub` was listed here in error and is removed (2026-07-23).** It *is*
  documented, at `FrameScriptDocumentation.lua:348-363`, with prose and a
  `SecureHooksAllowed = false` flag — as is the whole secret-testing family
  (`issecretvalue` :244, `hasanysecretvalues` :210, `issecrettable` :227,
  `canaccessvalue` :65, `canaccessallvalues` :20, `canaccesstable` :48,
  `canaccesssecrets` :37, `scrubsecretvalues` :331, `secretwrap` :383,
  `secretunwrap` :365, `dropsecretaccess` :131, `securecallmethod` :400,
  `SetTableSecurityOption` :429). See
  `security-taint-and-restricted-data.md` §4.4, which found this. Some of those
  (`issecurevariable`) do not appear anywhere in the shipped source either, so
  the wiki is the *only* source — say so and tier it 2.
  `wowkb.uiapi missing <name>` answers "docs / source / neither" in one call.
- Some structures are absent because Blizzard types them as bare `table`
  (e.g. there is no `AuraData` structure; `C_UnitAuras` returns `table`).
- **Data quirk:** `Enum.SecretAspect` reports `numValues=29 min=1 max=4194304`
  but the first seven members all report `EnumValue = 1`. That is what the file
  says; it is a bitfield whose generator mis-renders the low bits. Do not build a
  claim on those seven values.
- Three files use enum arithmetic and need metamethod stubs to load
  (`CharacterCustomizationShared`, `CurrencyConstants`, `PetConstants`);
  `wowkb.uiapi` handles this — a naive Lua loader will fail on them.

### 1.3 The live game install — real shipped addons + real SavedVariables

```
path : /mnt/c/Program Files (x86)/World of Warcraft/_retail_/
```

- `Interface/AddOns/` — **81 entries**, including Bartender4, BigWigs+LittleWigs,
  Details, MythicDungeonTools, OPie, RaiderIO, Syndicator, TellMeWhen, TomTom,
  TradeSkillMaster, Auctionator, Baganator, EllesmereUI (a 20-module suite),
  DandersFrames, plus this repo's own BucketBinds / CDMProbe / PlannerState.
  **WeakAuras is not installed** — use the clone.
- `WTF/Account/*/SavedVariables/*.lua` — ~50 live SV files. Real persisted-state
  shapes, real sizes (EllesmereUI 590 KB, DandersFrames 129 KB, CDMProbe 126 KB,
  BucketBinds 86 KB). Note the `.lua.bak` siblings: **the client keeps one backup
  per SV file** — a Tier-1-by-observation fact for the persistence topic.
- **This is the only place the CurseForge-only libraries exist in source form**
  (see §3.4). `LibSharedMedia-3.0`, `LibDBIcon-1.0`, `LibStub`,
  `CallbackHandler-1.0` are vendored inside BigWigs/, Bartender4/, etc.
- Caveat: these are **packaged release** copies. `@` build keywords have been
  substituted by the packager, so the code differs from the upstream repo. Cite
  as "as shipped in <Addon> <version> on this install", never as upstream source.

### 1.4 Official Blizzard articles

- `https://news.blizzard.com/en-us/article/24244638/how-midnights-upcoming-game-changes-will-impact-combat-addons`
  — Tier 1 but **player-facing and deliberately non-technical**. Checked
  2026-07-23: it names **zero** APIs, zero restricted maps, no comms rules, and
  explicitly says "we have been sharing detailed technical updates directly with
  addon developers" without linking them. Good for *philosophy* quotes
  ("addons should not automate combat decisions"), useless for mechanics.
- `worldofwarcraft.blizzard.com/en-us/news/...` content-update notes — linked
  from each wiki `Patch <ver>/API changes` page under `==Resources==`.

---

## 2. Tier 2 — community-maintained but authoritative

### 2.1 warcraft.wiki.gg ★ the indispensable complement to Tier 1

```
web  : https://warcraft.wiki.gg/
api  : https://warcraft.wiki.gg/api.php   (MediaWiki, open, no auth, works)
tool : uv run python -m wowkb.wiki ...    (§5.2 — USE THIS, not WebFetch)
```

**Fetchability.** WebFetch works on the wiki, but it renders through a
summarising model: you get a paraphrase with no revision id, which is the wrong
shape for a cite-everything KB. `api.php` returns raw wikitext plus a per-revision
`timestamp`. Both were verified working 2026-07-23. Use the tool.

**Maintenance state — read this carefully, it is nuanced.**
- There is a site notice on API pages: *"The API wiki is under maintenance. Since
  `2026-07-23T06:08:00Z`, ETA: at least multiple days"*. It is a **banner about
  the auto-generation pipeline, not an outage** — `api.php` served every page
  tested throughout.
- The wiki is **actively edited**. Sampled revision timestamps (2026-07-23/24):
  `World of Warcraft API` 2026-07-23, `API CreateFrame` 2026-07-23,
  `Widget API` 2026-07-23, `Events` 2026-07-23, `Patch 12.1.0/API changes`
  2026-07-24, `Secret Values` 2026-07-22, `TOC format` 2026-07-09.
- But **individual pages rot silently**: `Secure Execution and Tainting`
  2026-02-15, `API hooksecurefunc` 2026-01-03, `API issecurevariable` 2026-01-03,
  `Using the AddOn namespace` 2025-09-16, `SavedVariables` **2022-09-03** (18
  lines — effectively abandoned; the live page is the HOWTO
  *"Saving variables between game sessions"*).
- **Build skew:** the `World of Warcraft API` index page is stamped
  *"PTR Patch 12.1.0 (68301)"* — **ahead of live 12.0.7**, and this repo's
  `game-version.md` says there is no PTR right now. A wiki page may therefore
  describe an unreleased build. `wowkb.wiki info <title>` prints the stamp; put
  it in every wiki citation.

**★ The single most important thing on this wiki:** the
`Patch <ver>/API changes` pages **archive Blizzard's addon-dev blue posts
verbatim**, in `<blockquote>`s, with source links. Blizzard publishes those posts
**on the WoWUIDev Discord** (`discord.com/channels/327414731654692866/...`),
which we cannot read (§6). So these pages are the *only accessible archive of
Tier-1 Blizzard communication to addon authors*. Treat a blockquote there as
Tier 1 content delivered through a Tier 2 channel — quote it, and cite both the
wiki revision and the Discord permalink it names.

Confirmed present and sizeable:

| Page | Lines | Last edit |
|---|---|---|
| `Patch 12.0.0/Planned API changes` | 1419 | 2026-06-17 |
| `Patch 12.0.0/API changes` | 1262 | 2026-06-18 |
| `Patch 12.0.5/API changes` | 952 | 2026-06-19 |
| `Patch 12.0.7/API changes` | 514 | 2026-07-22 |
| `Patch 12.1.0/API changes` (unreleased) | 1523 | 2026-07-24 |

Structure of each: `==Resources==` (TOC number, official patch-notes link,
`wow-ui-source` and `BlizzardInterfaceResources` compare-URLs) ·
`==Undocumented changes==` · `==Blue posts==` (dated, quoted) ·
consolidated added/removed lists for Global API, ScriptObjects, Widgets, Events,
CVars, Enumerations, Structures, plus deprecations with migration paths.

**Navigation.** `Category:Interface customization` is the hub — 20 subcategories,
93 pages. The subcategories that matter:
`Category:API functions`, `Category:API events`, `Category:API namespaces`,
`Category:API types`, `Category:API systems`, `Category:API patch changes`,
`Category:Widgets`, `Category:XML elements`, `Category:UI technical details`,
`Category:FrameXML documentation`, `Category:Macro API`, `Category:HOWTOs`,
`Category:Console variables`, `Category:Function Libraries`.

`Category:HOWTOs` (45 pages) is where the prose lives — the topics agents will
want: *Getting started with writing addons · Create a WoW AddOn in 15 Minutes ·
Handling events · Hooking functions · Using function hooking libraries ·
Object security · Saving variables between game sessions · Creating defaults ·
Using the AddOn namespace · Creating a slash command · Creating key bindings ·
Making movable and resizable frames · Making scrollable frames ·
Creating a settings menu · Blizzard Menu implementation guide · Localizing an
addon · LibStub · Ace3 for Dummies · WelcomeHome: Your first Ace3 Addon ·
Using the BigWigs Packager with GitHub Actions · Viewing Blizzard's interface
code · Symlinking AddOn folders · Getting more useful errors · Porting addons to
Classic*.

Key single pages, verified to exist: `Secret Values` (215 lines, 2026-07-22 —
sections: Restrictions · Secret tables · API documentation changes · Secret
predicates · Secret aspects · Secret anchors · Constant accessors · Curves and
ColorCurves · Durations · Patch changes), `Secure Execution and Tainting`
(90 lines, 2026-02-15 — **describes the patch-2.0/3.0 model and does not cover
secret values**; it links out to `Secret Values`), `TOC format` (493 lines,
2026-07-09), `Widget API` (630 lines), `Events` (2207 lines), `XML/Frame`,
`UIOBJECT Frame`, `AddOn`, `Addon compartment`, `Interface AddOn Kit`.
Note `XML UI` **does not exist** — the namespace is `XML/<element>`.

### 2.2 WoWUIBugs — the Blizzard-monitored UI/API bug tracker

```
repo : https://github.com/Stanzilla/WoWUIBugs
state : NOT archived · 178 open issues · ~851+ issues filed
        issues updated and closed on 2026-07-23 (checked that day) — actively triaged
access: `gh api repos/Stanzilla/WoWUIBugs/issues?...` works (gh is authenticated here)
```

Labels prove Blizzard engagement: **`Acknowledged by Blizzard`**, `High Priority`,
`Regression`, `Wontfix`, `Mainline` / `Mainline PTR` / `Mainline Beta`,
`✔️ Verifiable Example`, `❌ Not A Blizzard Issue`.

Caveat: the repo's `pushed_at` is 2022 because there is no code — judge activity
by `updated_at` (2026-07-16) and issue timestamps, not commits. Blizzard staff do
not post in-thread; acknowledgement is expressed via the label. So an issue is
Tier 2 evidence of *observed behaviour*, and the label is Tier 2 evidence that
Blizzard agrees it is a bug. It is **never** evidence of intended design.

High-value queries already run:
- `secret value` → **13** issues (e.g. #804 `MathUtil.lua:28: attempt to compare
  local 'max' (a secret value)`, #801 `MoneyFrame.lua … arithmetic on a secret
  value`, #811 `Tooltip secret value error inside LayoutFrame.lua` (open),
  #834 `UnitChannelInfo/UnitChannelDuration return bogus info` (open)).
- `taint` → **86** issues (e.g. #453 `Map canvas overlays, click, and mouse
  action handlers taint the UI` — *Acknowledged by Blizzard*).
- #807 `SecureAuraHeaderTemplate and new APIs`, #748 `Certain API calls don't
  work correctly during PLAYER_LOGOUT` (open, *Acknowledged*) — the latter is
  directly relevant to the persistence topic.

### 2.3 townlong-yak.com — versioned FrameXML browser + build diffs

```
https://www.townlong-yak.com/framexml/    build 68887 (12.0.7, 2026-07-22) — current
https://www.townlong-yak.com/bad/         Blizzard API Documentation, rendered
https://www.townlong-yak.com/casc/  /dbc/ /globe/ /blp/  (CASC, DBC, globals, textures)
```

Fetches cleanly with WebFetch. Its real value over our local checkout is the
**per-file Compare link between builds** — "what changed in this file between
12.0.5 and 12.0.7" without cloning both. Permalink shape:
`/framexml/<build>/<AddOnName>/<File.lua>`. Run by Foxlit, a long-standing and
technically respected member of the addon community; it is nonetheless a
third-party mirror, so **cite the local checkout for file:line and use
townlong-yak for the diff narrative**.

### 2.4 Blizzard forums (Discourse) — Tier 1 *only* for staff posts

```
JSON API works, but you must follow redirects (-L):
  https://us.forums.blizzard.com/en/wow/search.json?q=<query>
  https://us.forums.blizzard.com/en/wow/t/<topic_id>.json
```

Verified: topic 2199207 *"Combat Philosophy and Addon Disarmament in Midnight"*
(2025-11-13) returns `"username": "BlizzardEntertainment", "staff": true` — so
the `staff` boolean is a reliable blue-post discriminator.

**But navigation is broken for our purposes.** There is no reachable
"UI and Macro" category in the current `categories.json`; the historical
`/c/community/ui-and-macro/174` URLs 301 to a class forum. Search returns mostly
player complaint threads. **Do not mine the forums for API facts** — go through
the wiki's blue-post archive (§2.1) and use the forums only to pull the full text
of a specific known thread by id. Tier 4 for everything else.

---

## 3. Tier 3 — community addons and libraries

All under `raw/addon-research/`, all `--depth 1`.

### 3.1 Reference addons

| Addon | Commit (2026) | Size | Read it for |
|---|---|---|---|
| **WeakAuras2** `WeakAuras/WeakAuras2` | `38d4bf1e6099` 07-20 | 64 M | The most complex live-data addon there is. `WeakAuras/` — `GenericTrigger.lua`, `BuffTrigger2.lua`, `Prototypes.lua`, `Conditions.lua`, `Animations.lua`, `AuraEnvironment.lua` (sandboxing user code!), `Transmission.lua` (import/export + comms), `Modernize.lua` (SV schema migration), `RegionTypes/` + `SubRegionTypes/` + `BaseRegions/`, `Profiling.lua`. |
| **BigWigs** `BigWigsMods/BigWigs` | `3fdc10f6cfd1` 07-21 | 50 M | Cleanest module architecture in the set. `Core/BossPrototype.lua` (~2300+ lines — the module base class), `Core/PluginPrototype.lua`, `Core/Core.lua`, `Loader.lua` (LoD orchestration), `Plugins/`, `Options/`, per-zone module packages. **Also the best real Midnight secret-value adaptation** — `self:IsSecret(...)` guards at `Core/BossPrototype.lua:1096,1122,2310`, `Plugins/Messages.lua:933`, `Plugins/Bars.lua:1873`, `Plugins/Pull.lua:393`, and `Tools/AutoInvite.lua:69` (`local issecretvalue = issecretvalue or function() end -- XXX 12.0 compat`). |
| **Details!** `Tercioo/Details-Damage-Meter` | `e14de53cc2e1` 07-21 | 43 M | Combat-log processing at scale, `classes/`, `core/`, `frames/`, `functions/`, and hand-written `API *.txt` docs. 30 files mention secret handling. Ships its own framework (`Libs/DF`). |
| **Plater** `Tercioo/Plater-Nameplates` | `2b2ff463cccd` 07-23 | 37 M | Nameplates: `Plater_Auras.lua`, `Plater_Animations.lua`, `Plater_Comms.lua`, `Plater_ImportExport.lua`, `Plater_API.lua`, `Plater_Docs.lua`. 11 files mention secret handling. |
| **ElvUI** `tukui-org/ElvUI` | `f60934a174d6` 07-23 | 16 M | The canonical *suite*: `ElvUI/` (modules) + `ElvUI_Options/` + `ElvUI_Libraries/`. **The densest secure-template user in the set** — 16 files touch `SecureHandler` / `RegisterStateDriver` / `SecureGroupHeader`; 32 files touch secret values. |
| **Bagnon** `Jaliborc/Bagnon` | `9f72bd96a756` 07-17 | 228 K | **Added to the registry 2026-07-23** — cloned and used by `libraries-and-ecosystem.md` (§11, rules) but not listed when this registry was written. The corpus's only example of the "split addon" pattern: **no `.pkgmeta` at all**, no `Libs/`, dependencies satisfied by a sibling addon via `## Dependencies: BagBrother`, plus cross-addon XML includes (`src/main.xml`). Uses `LibStub('C_Everywhere')` rather than Ace3. `## X-License: All Rights Reserved` — readable, not reusable. |
| **oUF** `oUF-wow/oUF` | `5672a3cb10e1` 07-20 | 504 K (784 K incl. `.git`) | Small and legible unit-frame framework built on `SecureUnitButtonTemplate` / secure group headers. Read `ouf.lua`, `factory.lua`, `units.lua`, `private.lua`, `elements/`. Best single worked example for the security + frames topics because you can read all of it. Also vendored inside ElvUI (`ElvUI/ElvUI_Libraries/Game/Shared/oUF/`). |

> ⚠ **"The seven clones" does not mean the same seven in every topic file**
> (noted 2026-07-23). `anatomy`, `frames`, `security` and `module` survey
> **WeakAuras2 · BigWigs · Details · Plater · ElvUI · oUF · Ace3**;
> `libraries-and-ecosystem` substitutes **Bagnon for Ace3** (Ace3 being its
> subject rather than a sample). So a "4 of 7" in one file and a "4 of 7" in
> another are not over the same population. Independence is worse than n=7 in
> both sets: **Details and Plater share an author (Tercioo) and the `DF`
> framework, and ElvUI vendors oUF.** Treat the effective n as ~5.

### 3.2 Ace3 and friends — the library baseline

```
path   : raw/addon-research/Ace3      commit 4475787f06f7 (2026-07-10)  1.5 MB
repo   : https://github.com/WoWUIDev/Ace3
```
Contains, each in its own dir: `AceAddon-3.0` (module/lifecycle), `AceEvent-3.0`,
`AceTimer-3.0`, `AceBucket-3.0` (event coalescing), `AceHook-3.0`,
`AceDB-3.0` + `AceDBOptions-3.0` (profiles/defaults — the persistence topic's
reference), `AceComm-3.0` (addon channel chunking), `AceSerializer-3.0`,
`AceConfig-3.0` + `AceGUI-3.0` (options UI), `AceConsole-3.0`, `AceLocale-3.0`,
`AceTab-3.0`, plus `LibStub/` and `CallbackHandler-1.0/` and a `tests/` dir.

Note the repo moved to the `WoWUIDev` org — old guides pointing at
`Ace3/ace3` on CurseForge SVN or `wowace.com` are describing the old home.

### 3.3 Standalone libraries cloned (`raw/addon-research/libs/`)

| Lib | Commit | Date | Note |
|---|---|---|---|
| `LibSerialize` (rossnichols) | `e89d5055c761` | 2026-07-16 | Active. Modern serializer; pairs with LibDeflate. |
| `LibDeflate` (SafeteeWoW) | `afc3b78d12fb` | **2021-05-05** | Pure-Lua DEFLATE. Old but *stable by design*, not abandoned — still the ecosystem default (referenced by WeakAuras, Details, Plater `.pkgmeta`). Say "unchanged since 2021", not "unmaintained". |
| `Chomp` (wow-rp-addons) | `0b2e0b067a0a` | 2026-04-20 | Addon-comms transport with throttling/queueing. |
| `LibSpecialization` (BigWigsMods) | `1151c4788bb4` | 2026-07-17 | Spec broadcast over comms. |
| `LibCustomGlow` (Stanzilla) | `4f8f5c2607d7` | 2026-07-17 | Glow/highlight effects — frames topic. |
| `libdatabroker-1-1` (tekkub) | `1a63ede0248c` | **2008-07-31** | The LDB spec itself. Frozen since 2008 — it is a 40-line spec, not rotting code. Still universally used (LibDBIcon consumes it). |
| `TaintLess` (townlong-yak) | `a4f3eda90db1` | **2025-02-26** | ⚠ **Tier down.** Single-file `TaintLess.xml`, self-versioned `[24-07-27]`. It monkey-patches known *Blizzard* taint bugs. It predates Midnight (12.0.0, 2026-01-20), so its fix set is pre-secret-values. It is still listed in WeakAuras' `.pkgmeta` as of 2026-07, which tells you it is *still shipped*, not that it is *still current*. Read it for the technique (`securecall`, `issecurevariable`, `purgeKey`), not for a list of live bugs. |

**Not clonable from GitHub:** `LibSharedMedia-3.0` and `LibDBIcon-1.0` live on
CurseForge SVN (`repos.curseforge.com/wow/...`), which needs an SVN client.
Read them from the live install instead — e.g.
`_retail_/Interface/AddOns/BigWigs/Libs/LibSharedMedia-3.0/` and
`.../BigWigs/Libs/LibDBIcon-1.0/`.

### 3.4 ★ `.pkgmeta` — libraries are NOT in the addon git repos

All seven addon clones carry a `.pkgmeta`. **Externals are resolved at package
time**, so a `git clone` of WeakAuras contains **no `WeakAuras/Libs/` at all**.
This trips people up: grepping the WeakAuras clone for `LibStub` finds nothing
and it looks like WeakAuras doesn't use it.

WeakAuras' `.pkgmeta` is the best single map of what a large 2026 addon depends
on — LibStub, CallbackHandler-1.0, AceTimer/AceSerializer/AceComm/AceConfig/AceGUI,
Chomp, LibSharedMedia-3.0, LibDataBroker-1.1, LibCompress, LibDeflate,
LibSpellRange-1.0, LibRangeCheck-3.0, LibCustomGlow-1.0, LibDBIcon-1.0,
LibGetFrame-1.0, Archivist (pinned `v1.0.8`), LibSerialize (pinned `v1.0.0`),
LibSpecialization, **TaintLess** (from `townlong-yak.com/addons.git/taintless`),
LibDispel, AceGUI-3.0-SharedMediaWidgets, LibUIDropDownMenu, LibAPIAutoComplete-1.0.

To read a lib's code: use the packaged copy in the live install (§1.3), or the
`libs/` clones (§3.3).

### 3.5 Packaging / distribution toolchain

```
path : raw/addon-research/packager   commit 36b4c3b7b7bd (2026-06-17)  388 KB
repo : https://github.com/BigWigsMods/packager
```
`release.sh` (3351 lines) + `action.yml` — the de-facto community standard, used
by essentially every addon in §3.1. `README.md` (417 lines) is the **reference
for `.pkgmeta`, the `@build-type@` keyword system in Lua/XML/TOC, multi-game-version
TOC splitting (`## Interface: 11502, 100207, 40400, 110000` vs separate
`_Mainline`/`_Cata`/`_Vanilla` toc files), string substitutions, and the
`X-Curse-Project-ID` / `X-WoWI-ID` / `X-Wago-ID` toc fields.**

Distribution hosts, fetchability checked 2026-07-23:

| Host | HTTP | Note |
|---|---|---|
| `wago.tools` | 200 | Build/DB2 browser. Already wrapped by `wowkb.wago`. |
| `addons.wago.io` | 200 | Addon + WeakAuras distribution. |
| `wowinterface.com` | 200 | Old-guard host; forums still carry historical threads. |
| `wowace.com` | 200 | Library home, redirects into CurseForge infra. |
| **`curseforge.com/wow/addons`** | **403** | ⚠ Cloudflare-blocked from this box. Do not plan research around it; use the GitHub repo or wago.io mirror. |

### 3.6 `Ketho/vscode-wow-api` — offline mirror of the wiki's API prose

```
path   : raw/addon-research/vscode-wow-api   commit d0b5b51fac4c (2026-06-24)  39 MB
```
EmmyLua/LuaLS annotations for the whole API. Structure:
`Annotations/Core/Blizzard_APIDocumentationGenerated/` (329 files),
`Annotations/Core/Widget/` (59), `Annotations/Core/FrameXML/` (49),
`Annotations/Core/Libraries/` (52 — Ace3, CallbackHandler, **ChatThrottleLib**,
HereBeDragons-2.0, LibDBIcon, LibDataBroker, LibDeflate, LibQTip, LibSharedMedia,
LibSink, LibStub, LibDualSpec, LibDialog, LibTextDump),
`Annotations/Core/Lua/` (7 — the Lua 5.1 stdlib as WoW exposes it, incl. `bit`
and `compat`), `Annotations/Core/Data/` (`Wiki.lua` 9095 lines, `Enum.lua` 10962,
`Event.lua` 1741, `CVar.lua` 1626).

**Why it earns a place:** `Annotations/Core/Data/Wiki.lua` is a machine-extracted
dump of the wiki's API pages, so it covers exactly the globals Tier 1 omits —
`hooksecurefunc` at `Wiki.lua:9041`, `issecurevariable` at `Wiki.lua:9059`, each
with a `---[Documentation](https://warcraft.wiki.gg/wiki/API_x)` backlink. It is
**greppable offline**, which matters while the wiki carries a maintenance banner.

⚠ **Tier 3, and it lags.** README badge says `mainline 12.0.1`; last commit
2026-06-24. Live is **12.0.7**. Use it to *find* things fast, then verify the
claim against `wowkb.uiapi` (Tier 1) or `wowkb.wiki` (Tier 2) before writing it.

### 3.7 `Ketho/BlizzardInterfaceResources` — flat per-build dumps

```
path   : raw/addon-research/BlizzardInterfaceResources   branch live
commit : 774b2c550366 "12.0.7 (68256)"  (2026-06-19)   28 MB
```
`Resources/GlobalAPI.lua`, `WidgetAPI.lua`, `ScriptObjectAPI.lua`, `Events.lua`,
`Frames.lua`, `Mixins.lua`, `Templates.lua`, `LuaEnum.lua`, `CVars.lua`,
`AtlasInfo.lua`, `FrameXML.lua`, `GlobalStrings/<locale>.lua` (11 locales),
`WidgetHierarchy.png`.

Best for **flat enumerations** where the structured index is overkill: "every
global frame name", "every template name", "every atlas", "every CVar", "every
GlobalString". The wiki's `Patch <ver>/API changes` pages link its
`compare/12.0.5..12.0.7` URL as the canonical build diff.

⚠ It is at build **68256**; our `wow-ui-source` is at **68887**. Same patch
(12.0.7), different build — do not treat the two as interchangeable at file level.

---

## 4. Tier 4 — named so you recognise and avoid them

- **`Amadeus-/WoWAddonDevGuide`** — "World of Warcraft Addon Development Guide
  designed for Claude AI use", **~1 MB of confident markdown**, 26 stars,
  **GitHub-archived (read-only)**, last push **2026-05-29** (i.e. pre-12.0.7).
  You *will* hit this searching for WoW addon docs, and it reads well. It is
  AI-generated and unreviewed. A spot-check against Tier 1 found it wrong on a
  specific, checkable point: `12a_Secret_Safe_APIs.md` claims *"12.0.1:
  `SetCooldownFromDurationObject` is now the ONLY `CooldownFrame` method that
  accepts secret values; `SetCooldown`, `SetCooldownFromExpirationTime`,
  `SetCooldownDuration`, `SetCooldownUNIX` are restricted."* At 12.0.7.68887 the
  generated docs give all four of those `SecretArgumentsAddAspect =
  {Enum.SecretAspect.Cooldown}` and **no** `SecretArguments = "NotAllowed"`.
  (`FrameAPICooldownDocumentation.lua:280,293,305,316,329`.)

  ⚠ **This entry over-read its own evidence and is corrected (2026-07-23).** It
  concluded "i.e. they *do* accept secret arguments". They carry
  `SecretArguments = "AllowedWhenUntainted"`, and **all addon code is tainted**,
  so *from an addon* those four still do not accept a secret — the guide's
  practical advice was closer to right than this refutation was. What is
  genuinely wrong in the guide is its *mechanism*: the four are not
  `NotAllowed`-restricted, they are untainted-only, and the sanctioned addon
  route for secret cooldown timing is a `LuaDurationObject`
  (`C_Spell.GetSpellCooldownDuration` → `Cooldown:SetCooldownFromDurationObject`),
  which works because a duration object *is not a secret value* — not because
  that sink accepts secrets (it is `AllowedWhenUntainted` too). Full working:
  `security-taint-and-restricted-data.md` §4.5 and §4.8, which caught this.
  **The verdict on the guide is unchanged** — do not cite it — but this
  particular falsification should not be reused as written.
  **Verdict: do not cite. Do not use as a starting outline.** If a phrasing from
  it seems useful, re-derive the claim from Tier 1 first.
- **`ssegold.com`, `kingboost.net`** — gold/boost-selling SEO sites publishing
  "Midnight addon changes explained" articles. Zero technical authority.
- **`kaylriene.com`** — a genuine, thoughtful player blog on the Midnight addon
  changes. Fine for *narrative and motive* ("why Blizzard did this"), never for
  API mechanics. Tier 4; corroborate.
- **`warcrafttavern.com`, `icy-veins.com` news posts** — usable only to *find*
  the primary blue post they are summarising; then go read that.
- Any page that tells you to look in `Interface/FrameXML/` or `Interface/SharedXML/`
  as top-level dirs, or that describes taint without mentioning secret values,
  is describing the pre-Midnight game. Down-tier on sight.

---

## 5. Tools built for this KB

Both are new, live in `tools/wowkb/`, and are stdlib-only apart from the existing
uv env. Run from `tools/`.

### 5.1 `wowkb.uiapi` — query the Tier-1 generated API docs

```bash
cd tools
uv run python -m wowkb.uiapi index                  # (re)build the JSON index — ~3 s
uv run python -m wowkb.uiapi stats                  # build id + counts
uv run python -m wowkb.uiapi func 'C_Spell.GetSpell' --full
uv run python -m wowkb.uiapi event 'UNIT_SPELLCAST'
uv run python -m wowkb.uiapi system Spell           # whole system: functions + events
uv run python -m wowkb.uiapi widget FrameAPICooldown
uv run python -m wowkb.uiapi enum '^SecretAspect$'
uv run python -m wowkb.uiapi struct Aura
uv run python -m wowkb.uiapi secure --protected     # the 59 IsProtectedFunction
uv run python -m wowkb.uiapi secure --restricted    # the 231 HasRestrictions
uv run python -m wowkb.uiapi secure --hookable      # the 24 SecureHooksAllowed
uv run python -m wowkb.uiapi secure --args-not-allowed
uv run python -m wowkb.uiapi predicates             # all 51 secret predicates + prose
uv run python -m wowkb.uiapi missing hooksecurefunc # docs? source? neither?
uv run python -m wowkb.uiapi grep 'SecureHandler' --type lua
```

It loads the 593 doc files through `lua5.1` with stubs for `APIDocumentation` and
proxy metatables for `Enum`/`Constants` (including arithmetic metamethods — three
files need them), then serialises to
`raw/addon-research/_index/uiapi.json` (gitignored). **Every line of output ends
with `<file>:<line>` relative to the checkout**, so results are already in
citation form. `--json` on any query for machine-readable output.
`grep`/`missing` auto-fall back to GNU `grep` (no `rg` on this box).

Re-run `index` if you `git pull` the checkout to a new build.

### 5.2 `wowkb.wiki` — raw wikitext from warcraft.wiki.gg

```bash
cd tools
uv run python -m wowkb.wiki info API_CreateFrame "Secret Values" TOC_format
uv run python -m wowkb.wiki page "Secret Values"
uv run python -m wowkb.wiki page API_issecurevariable API_hooksecurefunc
uv run python -m wowkb.wiki search "secret value" --limit 25
uv run python -m wowkb.wiki category HOWTOs
uv run python -m wowkb.wiki category "Interface customization" --subcats
uv run python -m wowkb.wiki changes 12.0.0 12.0.5 12.0.7    # Patch <v>/API changes
```

**Use this instead of WebFetch for the wiki.** It prints the page URL, `revid`
and `lastedit` timestamp above the raw wikitext, so a quote is exact and its age
is visible. Responses cache under `raw/wiki/` (gitignored); `--fresh` bypasses.
Missing pages are reported explicitly as `PAGE DOES NOT EXIST` with a `[gap]`
line, so a typo'd title never silently becomes "I found nothing, so it's false".

---

### 3.8 Sources the topic agents added beyond this registry

Recorded 2026-07-23 during reconciliation, so the registry stays an accurate map
of what the KB actually rests on.

| Source | Used by | Tier | Note |
|---|---|---|---|
| **`gh api repos/<owner>/<repo>`** (GitHub repo metadata) | `libraries-and-ecosystem.md` §9 | **2** | `pushed_at`, `stargazers_count`, `archived`, `created_at` for ~20 libraries. `gh` is authenticated on this box. ⚠ `pushed_at` is evidence about the *repository*, never about whether the code works — a frozen spec-shaped library (LibDataBroker, LibStub) has an old date by design. Also usable to prove a repo's **absence** (`Nevcairiel/LibDBIcon-1.0` → 404). |
| **`https://api.mmoui.com/v3/game/WOW/filelist.json`** (WoWInterface public file list) | `libraries-and-ecosystem.md` §9.1, rule 26 | **2** | 8134 entries, fetched 2026-07-23, no auth. The one *reachable* addon-host index (CurseForge is 403, `addons.wago.io` is 401). Its value here was negative evidence: it lists Ace3 as last updated **2017-09-04** against r1390/2026-02-03 upstream — i.e. **never take a library's version from WoWInterface**. |
| **`https://wago.tools/api/builds`** | `api-events-and-discovery.md` §5.5 | **1-ish** | Per-product build list; confirmed `wow` newest = `12.0.7.68887` on 2026-07-23, matching the checkout. Already wrapped by `wowkb.wago` for DB2 tables; the `builds` endpoint is the new use. |
| **Raw wikitext line numbers** via `api.php?action=query&prop=revisions&rvprop=content` | `state-persistence-and-communication.md` throughout | 2 | That file cites wiki **line numbers**, not just revids, so quotes are re-findable. Its own verification pass found every such number was uniformly 5 lines high in the first draft — if you adopt this convention, re-measure against `action=raw`, and never mix rendered-page line numbers with wikitext ones. |
| **WoWUIBugs issues by number** (`#107`, `#216`, `#241`, `#250`, `#414`, `#453`, `#474`, `#549`, `#573`, `#649`, `#748`, `#801`, `#804`, `#811`, `#826`, `#847`, `#848`) | frames, security, module, state | 2 | The tracker is registered in §2.2 but these specific issues are the ones the KB actually leans on. Labels and open/closed state were re-checked via `gh api repos/Stanzilla/WoWUIBugs/issues/<n>` on 2026-07-23. |
| **The live install's `WTF/` tree** as a persistence corpus | `state-persistence-and-communication.md` §1–2 | 1 by observation | §1.3 registered the install for *addon source* and SavedVariables *shapes*; the persistence topic went further and used it as evidence for on-disk **format** (no indentation, CRLF, `nil` written for declared-but-unset globals, one `.lua.bak` per file, `WTF/SavedVariables/` as the `SavedVariablesMachine` location — the last of which is **not documented on the wiki**, so it is our observation alone). |

**Not used by any topic file, despite being in this registry:** `townlong-yak`
build-diff links (§2.3) — cited as a technique, never actually exercised, because
we have only one checkout to compare; and the Blizzard Discourse forum JSON
(§2.4), which §6 already predicted would be useless.

---

## 6. Gaps — what we could NOT establish, and where we looked

- **`[gap]` Blizzard's primary addon-developer channel is unreachable.** Blizzard
  publishes its technical addon API notes on the **WoWUIDev Discord**
  (server `327414731654692866`, invite `discord.com/invite/txUg39Vhc6`, ~4.9 k
  members). Every `Patch <ver>/API changes` blue-post citation on the wiki points
  at `discord.com/channels/327414731654692866/<channel>/<message>`. We have no
  Discord access, and Discord permalinks are not publicly fetchable. **Mitigation:
  the wiki quotes them verbatim; always prefer that archive and cite the Discord
  permalink alongside as the unverifiable primary.** Looked at: news.blizzard.com
  (no links), us.forums.blizzard.com Discourse API (no UI&Macro category),
  WebSearch.
- **`[gap]` No Blizzard "UI and Macro" forum category exists any more.**
  `categories.json` on `us.forums.blizzard.com/en/wow` lists no such category, and
  the historical `/c/community/ui-and-macro/174` path 301s to a class forum.
  Old guides that name it are stale. Search + topic-id JSON still work.
- **`[gap]` No official Blizzard-authored addon *tutorial* or *guide* exists.**
  The generated docs are a spec, `/api` is a browser. The only prose is
  community-written (wiki HOWTOs, Tier 2).
- **`[gap]` Error/failure semantics are largely undocumented at Tier 1.** The
  generated docs say a function `HasRestrictions` or `MayReturnNothing`, but not
  what error text you get, or exactly when. WoWUIBugs issue titles are the best
  proxy (they quote real error strings) — that is Tier 2 observation, not spec.
- **`[gap]` `AuraData` and several other returned structures are typed `table`**
  in the generated docs, so their field layout is not Tier 1. Wiki + WeakAuras'
  `BuffTrigger2.lua` are the fallbacks; label the claim Tier 2/3.
- **`[gap]` CurseForge is Cloudflare-403 from this machine.** Anything only
  documented on a CurseForge project page is out of reach; use GitHub, wago.io,
  or the packaged copy in the live install.
- **`[gap]` `LibSharedMedia-3.0` / `LibDBIcon-1.0` upstream is CurseForge SVN**,
  not git. No clone; read the vendored copies in the live install.
- **Build skew to keep straight.** `wow-ui-source` = 12.0.7.**68887**;
  `BlizzardInterfaceResources` = 12.0.7.**68256**; `vscode-wow-api` annotations =
  **12.0.1**; the wiki's API index page is stamped **12.1.0 (68301) PTR** while
  this repo's `game-version.md` says live is **12.0.7** with no PTR. When two
  sources disagree, the local `wow-ui-source` checkout wins.
- **Unverified in-game.** Nothing in this registry has been confirmed by running
  code in the client. Any claim that needs it should be marked
  `@verify-ingame` per this repo's convention.

---

## 7. Per-topic routing

Start at the ★ source; the others are corroboration. Numbers in brackets are
section references above.

### anatomy-and-runtime
★ `wow-ui-source` `.toc` corpus [1.1] + `Blizzard_SharedXMLBase/` (`Mixin.lua`,
`Pools.lua`, `EnumUtil.lua`, `Compat.lua`, `EnvironmentUtil.lua`) ·
`Blizzard_AddOnList/`, `Blizzard_AddOnPerformance/`, `Blizzard_ScriptErrorsFrame/`
· `C_AddOns.*` and `C_AddOnProfiler.*` via `wowkb.uiapi system AddOn` [5.1]
· wiki `TOC format` (493 lines, 2026-07-09), `AddOn`, `Addon compartment`,
`Using the AddOn namespace` (⚠ 2025-09-16) [5.2]
· `vscode-wow-api/Annotations/Core/Lua/` for the Lua 5.1 surface incl. `bit` [3.6]
· real third-party `.toc` files in the live install [1.3]
· **gotcha:** shipped tocs contain Blizzard-only directives [1.1].

### api-events-and-discovery
★ `wowkb.uiapi` — 6144 functions / 1741 events with payloads [1.2, 5.1]
· `Blizzard_EventTrace/Blizzard_EventTrace.lua` (`/eventtrace`) and
`Blizzard_APIDocumentation/` (`/api`, syntax at `:120-139`) [1.1]
· `Blizzard_DebugTools/Blizzard_TableInspector.lua` [1.1]
· wiki `Events` (2207 lines), `World of Warcraft API` (⚠ stamped 12.1.0 PTR) [2.1]
· `BlizzardInterfaceResources/Resources/Events.lua` for a flat list [3.7]
· `Patch <ver>/API changes` for what moved [2.1].

### frames-textures-animation
★ `Blizzard_SharedXML/UI.xsd` — the XML schema, Tier 1 [1.1]
· `Blizzard_SharedXML/` (`Backdrop`, `NineSlice`, `AnimationTemplates`,
`LayoutFrame`, `ManagedLayoutFrame`, `HybridScrollFrame`, `Interpolator`,
`EasingUtil`, `ModelScene*`) and `Blizzard_SharedXMLBase/RegionLayoutManager.lua`,
`TextureUtil.lua`, `Rectangle.lua` [1.1]
· `wowkb.uiapi widget <name>` — 77 ScriptObject tables, 1384 widget methods [5.1]
· wiki `Widget API` (630 lines), `Category:Widgets`, `Category:XML elements`,
`XML/Frame`, `UIOBJECT Frame` [2.1]
· Tier 3: WeakAuras `RegionTypes/`+`SubRegionTypes/`, Plater `Plater_Animations.lua`,
`libs/LibCustomGlow` [3.1, 3.3]
· ⚠ note which widget methods carry `SecretReturnsForAspect` / `SecretArgumentsAddAspect`.

### security-taint-and-restricted-data  ← the topic with the best Tier-1 evidence
★ `Blizzard_RestrictedAddOnEnvironment/` (7 Lua + 2 XML) and
`Blizzard_FrameXML/SecureTemplates.lua` [1.1]
★ `wowkb.uiapi predicates` (51), `secure --protected|--restricted|--hookable`,
and the full annotation-count table in [1.2] — this *is* the security surface
· `Blizzard_SharedXMLBase/SecureTypes.lua`, `Blizzard_SharedXML/SecureUtil.lua`,
`PixelUtilSecure.lua`, `SecureUIPanelTemplates.lua`, `SecureScrollTemplates.lua` [1.1]
· wiki `Secret Values` (2026-07-22 — current) **and** `Secure Execution and
Tainting` (⚠ 2026-02-15, describes the 2.0/3.0 model, no secret values) [2.1]
· wiki `Patch 12.0.0/API changes` + `Planned API changes` + 12.0.5/12.0.7 —
the blue-post archive [2.1]
· WoWUIBugs: 13 `secret value` issues, 86 `taint` issues [2.2]
· Tier 3 practice: BigWigs `IsSecret` guards, ElvUI (32 files), Details (30),
Plater (11), oUF (3), `libs/TaintLess` (⚠ pre-Midnight) [3.1, 3.3]
· wiki-only globals: `issecure`, `issecurevariable`, `securecall`,
`securecallfunction`, `secureexecuterange`, `forceinsecure`, `hooksecurefunc` —
Tier 2, cite the revision [1.2, 3.6].
⚠ **Corrected 2026-07-23:** this line previously also listed `issecretvalue`,
`hasanysecretvalues` and `scrub` as wiki-only. They are **Tier 1**, fully
documented in `FrameScriptDocumentation.lua` — see the correction in §1.2.

### module-architecture
★ `Ace3/AceAddon-3.0` [3.2] and BigWigs `Core/BossPrototype.lua` +
`Core/PluginPrototype.lua` + `Loader.lua` [3.1]
· Blizzard's own: `Blizzard_SharedXMLBase/CallbackRegistry.lua`,
`GlobalCallbackRegistry.lua`, `Mixin.lua`, `ObjectUpdater.lua`, and the 317
`Blizzard_*` addons as a partitioning case study [1.1]
· ElvUI (suite), Details (`classes/`+`core/`), WeakAuras (`WeakAuras`/
`WeakAurasOptions`/`WeakAurasTemplates` split) [3.1]
· `.pkgmeta` + `packager/README.md` for the LoD/multi-toc/build story [3.4, 3.5]
· wiki `Using the AddOn namespace` (⚠ 2025-09-16), `LibStub` HOWTO [2.1]
· **7 clones ≠ 7 independent norms** — Details and Plater share an author.

### state-persistence-and-communication
★ `Ace3/AceDB-3.0` + `AceDBOptions-3.0` (profiles/defaults) and
`Ace3/AceComm-3.0` + `AceSerializer-3.0` [3.2]
★ Live SavedVariables on disk — real shapes, real sizes, and the `.lua.bak`
one-backup-per-file behaviour [1.3]
· Tier 1: `## SavedVariables` / `PerCharacter` / `Machine` in shipped tocs;
`Blizzard_ClientSavedVariables/`, `Blizzard_GlueSavedVariables/`;
`C_ChatInfo.RegisterAddonMessagePrefix` and friends via
`wowkb.uiapi system ChatInfo`; `ADDON_LOADED` / `PLAYER_LOGOUT` payloads [1.1, 5.1]
· `libs/LibSerialize`, `libs/LibDeflate`, `libs/Chomp`, `libs/LibSpecialization`;
`vscode-wow-api/.../Libraries/ChatThrottleLib` [3.3, 3.6]
· WeakAuras `Transmission.lua` + `Modernize.lua` (SV schema migration), BigWigs
comms, Plater `Plater_Comms.lua` / `Plater_ImportExport.lua` [3.1]
· ⚠ WoWUIBugs #748 "Certain API calls don't work correctly during PLAYER_LOGOUT"
(open, *Acknowledged by Blizzard*) [2.2]
· ⚠ Midnight restricts comms in instances — `SecretInChatMessagingLockdown`
(36 functions) and the 12.0.x blue posts [1.2, 2.1].

### libraries-and-ecosystem
★ `Ace3` [3.2] + `libs/` [3.3] + the vendored libs across the live install [1.3]
· `.pkgmeta` externals as a dependency census — WeakAuras' is the richest [3.4]
· `packager/README.md` + `action.yml` for the CI/release standard [3.5]
· `vscode-wow-api/Annotations/Core/Libraries/` — 52 annotated libs, incl. ones we
did not clone (HereBeDragons-2.0, LibQTip-1.0, LibSink-2.0, LibDualSpec-1.0) [3.6]
· wiki `Category:Function Libraries`, `LibStub` HOWTO, `Ace3 for Dummies`,
`Using the BigWigs Packager with GitHub Actions` [2.1]
· distribution: wago.io / WoWInterface / WoWAce reachable, **CurseForge 403** [3.5]
· `libdatabroker-1-1` (frozen 2008) + `LibDBIcon-1.0` (install-only) as the
LDB/minimap-button pattern [3.3]
· ⚠ "everyone uses X" needs a count — say "N of the 7 addons surveyed".
