---
title: Libraries and the addon ecosystem
patch: 12.0.7
fetched: 2026-07-23
reviewed: 2026-07-23
sources:
  - https://github.com/Gethe/wow-ui-source (live, version.txt 12.0.7.68887, commit 4383ced30106d51b27e3e86d1987f1552f0d259d)
  - https://github.com/WoWUIDev/Ace3 (commit 4475787f06f74d2079b2ab2082195432103da424, 2026-07-10)
  - https://github.com/BigWigsMods/packager (commit 36b4c3b7b7bd17c835ad8c83fed4976c067edfbe, 2026-06-17)
  - https://warcraft.wiki.gg/wiki/LibStub (revid 6029070, 2024-05-08)
  - https://warcraft.wiki.gg/wiki/TOC_format (revid 6767089, 2026-07-09)
  - https://warcraft.wiki.gg/wiki/Category:Function_Libraries (revid 5355606, 2019-06-08)
  - Live install /mnt/c/Program Files (x86)/World of Warcraft/_retail_/ (81 installed addons, 23 vendored LibStub copies)
  - GitHub repository metadata via `gh api repos/<owner>/<repo>` (queried 2026-07-23)
  - https://api.mmoui.com/v3/game/WOW/filelist.json (8134 entries, fetched 2026-07-23)
  - Clones at raw/addon-research/ — WeakAuras2 38d4bf1e, BigWigs 3fdc10f6, details e14de53c, plater 2b2ff463, ElvUI f60934a1, oUF 5672a3cb, Bagnon 9f72bd96, TaintLess a4f3eda9 (all verified 2026-07-23)
confidence: medium
verified: 2026-07-23   # adversarial re-check of every locator; 11 claims corrected, see "Adversarial verification pass"
---

# Libraries and the addon ecosystem

**Scope.** The community's shared infrastructure: what a "library" physically is,
how embedding actually works, which problems are solved well enough that rolling
your own is a mistake, which libraries are legacy, and what mature open-source
addons are worth reading *for*. Module boundaries inside one addon are the
`module-architecture` topic; SavedVariables and addon comms mechanics are
`state-persistence-and-communication`; taint and secret values are
`security-taint-and-restricted-data`.

## Citation conventions used in this file

| Prefix | Means |
|---|---|
| `[T1 src]` | Blizzard's shipped UI source. Paths are relative to the `wow-ui-source` checkout root (`raw/addon-research/wow-ui-source/`). Build **12.0.7.68887**, commit `4383ced30106`. |
| `[T1 docs]` | `Interface/AddOns/Blizzard_APIDocumentationGenerated/…` in the same checkout. |
| `[T1 obs]` | Directly observed on the live install at `/mnt/c/Program Files (x86)/World of Warcraft/_retail_/`. Observation of shipped artefacts. |
| `[T2 wiki]` | warcraft.wiki.gg with revid + last-edit date. Stamps are load-bearing; pages rot silently. |
| `[T2 gh]` | GitHub repository metadata read through `gh api` on 2026-07-23. A `pushed_at` date is evidence about the repo, not about whether the code works. |
| `[T3]` | A named community addon or library at a named commit / a named vendored copy on this install. **A data point, never a rule.** |

> ⚠ **The clones and the install are different artefacts.** The `raw/addon-research/`
> clones are *upstream source*. The copies under
> `_retail_/Interface/AddOns/*/Libs/` are *packaged release output* — the
> BigWigs packager has already substituted `@keyword@` build markers and pulled
> externals in. Where a claim depends on which one, this file says which.
>
> ⚠ **Nothing here has been run in the client.** Items needing that are marked
> `@verify-ingame` per repo convention.

### Adversarial verification pass — 2026-07-23

Every locator in this file was re-opened by a second pass whose brief was to
refute it. Roughly 50 claims were checked; **11 were wrong** and are corrected
in place, each with an inline note saying what the earlier draft said. Summary of
what changed, so a reader who saw the previous version knows what to un-learn:

| § | Was | Is |
|---|---|---|
| §1 | ElvUI calls LibStub in 24 non-library files | **3** (21 hits were inside `ElvUI_Libraries/`) |
| §2.2, Rule 27 | 3 byte-variants of LibStub, 1 program | **7 byte-variants, 2 programs** |
| §2.3, §4, Rule 5 | CallbackHandler v6 **and v7** use `loadstring` dispatchers | **v6 only**; v7 is a plain `xpcall` loop |
| §3.1 | "mature libraries ship both `lib.xml` and `.toc`" | unsupported generalisation → `[gap]` + the three observed combinations |
| §3.3 | WeakAuras externals span 3 hosts | **4** (`repos.wowace.com` was missed) |
| §3.3, §11, Rule 7 | Details! has 19 in-tree lib dirs; WeakAuras has 27 externals | **18** dirs; **25** externals |
| §5 | a CurseForge-SVN pointer for Ace3 is a staleness signal | **refuted** — WeakAuras and BigWigs package Ace3 from those SVN trunks today |
| §5.2 | Details, **Plater** and ElvUI call `LibStub("AceAddon-3.0")` | Details and ElvUI only; Plater: zero call sites |
| §8.2, Rule 2 | LibDBIcon consumes LDB *optionally* | it hard-requires LDB; the `silent` flag only swaps the error message |
| §9, Rule 25 | LibDeflate is an external in **ElvUI**'s `.pkgmeta` | ElvUI vendors it in-tree; not an external |
| §9 | "Dongle, Rock, Sea, Ace2" named on the wiki category | category members are `Ace (AddOns)`, `ChatThrottleLib`, `Dongle`, `LibKarma`, `Sea` — **Rock and Ace2 are not** |

Additionally, six locators were off by a line or two and were tightened
(AceSerializer's `error` is `:106` not `:104`; AceTimer's clamp is `:33-35` not
`:34`; Bagnon's `LibStub('C_Everywhere')` is `frame.lua:7` not `:6`; the wiki's
`X-_____` line is wikitext **376**; LSM's duplicate-key early-out is `:265-268`;
oUF's global-collision block is `:1026-1034`), three overreaching statements were
weakened to what their source shows (`EventRegistry` as an addon-facing API;
LibDBIcon's maintenance status; the "same defensive shim" in §10), and
three counts were corrected (Details 108 → unchanged, but ElvUI is a 13-module
suite not 20; oUF is 504 KB not 784 KB; `LIBSTUB_MINOR` is declared on a
two-variable line, so the grep in the old locator would not have matched).

**Everything not listed above verified as written**, including all 12 Tier-1
Blizzard-source locators (`CallbackRegistry.lua:112/155/184/269`,
`GlobalCallbackRegistry.lua:1-11/13-36`, `Blizzard_Settings.lua:133/143/153/161/173/382/398/404`,
`AddonCompartment.lua:81/106/113/136`, `MenuUtil.lua:151/335/354/373`,
`11_0_0_MenuImplementationGuide.lua:4-7` verbatim, `Pools.lua:856-861`,
`Blizzard_SharedXML_Mainline.toc:212-215`, `UIDropDownMenu.lua` 1589 lines / 62
functions / `GetCurrentEnvironment()` at `:1`, `UITimerDocumentation.lua:11/22/39`,
`AddOnsDocumentation.lua:165`), every Ace3 component version and line count, the
23/16/81 LibStub census, the 14-copy 1/3/10 CallbackHandler census, the 5-copy
`12000001` LibSharedMedia census, the 165-file secret-value grep, all 15 GitHub
`pushed_at`/star figures, all four wiki revids, the WoWInterface 8134-entry
filelist and its 2017-09-04 Ace3 date, and the wago 401.

---

## 1. There is no platform library system. There are three community conventions.

Blizzard ships **no** library loader, no version arbitration, and no dependency
resolution beyond `.toc` `## Dependencies`. The string `LibStub` does not appear
anywhere in the 3685-file shipped UI source `[T1 src: grep -ril 'libstub' over
Interface/AddOns/ → zero hits]`. Everything in this file is community convention
built on top of two primitives the game does give you: a shared global table `_G`,
and `.toc` metadata readable via `C_AddOns.GetAddOnMetadata(name, variable)`
`[T1 docs: AddOnsDocumentation.lua:165]`.

Three arbitration conventions coexist in code shipping today:

**(a) LibStub** — a global registry keyed by "major" name, with numeric "minor"
version arbitration. Overwhelmingly dominant. §2.

**(b) A bare global version gate.** ChatThrottleLib, bundled *inside* AceComm-3.0,
does not use LibStub at all: it declares `local CTL_VERSION = 31`, bails if
`_G.ChatThrottleLib.version >= CTL_VERSION`, and otherwise publishes itself on the
global `[T3: Ace3@4475787f AceComm-3.0/ChatThrottleLib.lua:26, :31, :54]`.

**(c) Custom `.toc` metadata plus a caller-chosen global.** oUF reads
`C_AddOns.GetAddOnMetadata(parent, 'X-oUF')` at load and installs itself into
`_G[global]`, erroring if the name is already taken or if a non-oUF parent tries to
claim the name `oUF` `[T3: oUF@5672a3cb ouf.lua:2 and :1026-1033; oUF.toc:7
declares `## X-oUF: oUF`]`. Arbitrary `X-`-prefixed metadata being readable is
Tier 2: *"X-_____: Any custom metadata prefixed by 'X-'"*
`[T2 wiki: TOC format, revid 6767089, 2026-07-09 — wikitext line 376
(`action=raw`), verified 2026-07-23]`.

Do not assume LibStub. Six of the seven reference addons surveyed call
`LibStub(...)` from non-library code; oUF calls it zero times
`[T3: grep over the 7 clones, excluding vendored-library paths
(`/libs?/`, `/Libraries/`, `ElvUI_Libraries/`) — WeakAuras2 69 files,
Details 131, BigWigs 25, ElvUI **3**, Plater 15, Bagnon 5, oUF 0. Re-counted
2026-07-23]`.

> **Corrected on verification.** An earlier draft of this file reported ElvUI at
> 24. That count did not exclude `ElvUI_Libraries/` (the directory name has no
> `/libs/` or `/Libraries/` path segment, so the exclusion regex missed it):
> 21 of the 24 hits are inside ElvUI's own bundled libraries. Outside them ElvUI
> calls LibStub in exactly three files —
> `ElvUI/Game/Shared/General/Initialize.lua`, `…/Modules/Skins/Ace3.lua`,
> `…/Modules/Skins/Skins.lua` `[T3: ElvUI@f60934a1]`.

---

## 2. LibStub

### 2.1 What it is

51 lines of public-domain Lua, unchanged in substance since 2007. The shipped copy
inside BigWigs still carries its Subversion keyword line
`-- $Id: LibStub.lua 76 2007-09-03 01:50:17Z mikk $`
`[T1 obs / T3: _retail_/Interface/AddOns/BigWigs/Libs/LibStub/LibStub.lua:1]`.

The whole API:

| Call | Behaviour |
|---|---|
| `LibStub:NewLibrary(major, minor)` | Returns `nil` if an equal-or-newer minor is already registered; otherwise returns `(libtable, oldminor)`. The table is **reused across upgrades** — `self.libs[major] or {}`. |
| `LibStub:GetLibrary(major[, silent])` | Returns `(libtable, minor)`. **Errors** if absent and `silent` is falsy. |
| `LibStub:IterateLibraries()` | `pairs` over the registry. |
| `LibStub(major[, silent])` | `__call` metamethod aliased to `GetLibrary`. |

`[T1 obs / T3: BigWigs/Libs/LibStub/LibStub.lua:20-28 (NewLibrary, oldminor gate
at :25), :36-41 (GetLibrary, error at :38), :46-48, :50 (`setmetatable(LibStub,
{ __call = LibStub.GetLibrary })`)]`. Same semantics in the upstream Ace3 copy at
`Ace3@4475787f LibStub/LibStub.lua:11-19, :21-26, :28, :29` `[T3]`.

`minor` is coerced with `tonumber(strmatch(minor, "%d+"))`, so `"1.2.3"` becomes
`1` — the assert only requires that the value *contain* a number
`[T3: BigWigs copy LibStub.lua:22]`. The Tier-2 write-up matches
`[T2 wiki: LibStub, revid 6029070, 2024-05-08 — argument/return tables]`.

### 2.2 The self-upgrading load pattern

The whole file is wrapped in `if not LibStub or LibStub.minor < LIBSTUB_MINOR then`
`[T3: BigWigs copy LibStub.lua:9; Ace3 copy :6]`. Every addon embeds its own copy;
whichever loads first wins, later copies see an equal-or-newer `minor` and no-op.
`LIBSTUB_MINOR` is **2** in every copy on this install, so in practice the first
loaded copy always wins.

Measured on the live install: **23 copies of `LibStub.lua`, across 16 of the 81
installed top-level addons**. Those 23 files are **7 distinct byte sequences**,
which collapse to **2 distinct programs** once comments and whitespace are
stripped (21 copies + 2 copies). The only executable difference between the two
is `strmatch` (21 copies, incl. BigWigs) vs `string.match` (2 copies — TomTom and
DandersFrames, matching the upstream Ace3 copy); in WoW `strmatch` is the global
alias of `string.match`, so behaviour is identical. All 23 declare
`LIBSTUB_MINOR = 2` — the declaration is
`local LIBSTUB_MAJOR, LIBSTUB_MINOR = "LibStub", 2`, so grep for that line, not
for `LIBSTUB_MINOR = 2` `[T1 obs: `find … -name LibStub.lua` under
`_retail_/Interface/AddOns/`, md5 over raw bytes and over comment/whitespace-
stripped text, 2026-07-23]`.

> **Corrected on verification.** An earlier draft said "3 byte-variants that
> reduce to the same program". Both numbers were wrong: 7 byte-variants, 2
> programs. The *conclusion* (no version drift, one behaviour) survives.

### 2.3 The failure modes LibStub actually has

**Different minors of the same library ship simultaneously, and the loser's
consumers get the winner's code.** On this install `CallbackHandler-1.0` exists in
14 vendored copies at three different minors — **10 × v8, 3 × v7, 1 × v6**
`[T1 obs: v6 in `Simulationcraft/libs/`, v7 in `ClassCodex/`, `RaiderIO/`,
`TradeSkillMaster/External/EmbeddedLibs/`, v8 in the other ten]`. Those versions
are not cosmetically different — but the three differ from each other in
**two** steps, not one:

| Minor | Dispatch | Evidence |
|---|---|---|
| v6 | Builds a per-arity dispatcher by `loadstring`-ing generated Lua, then calls it; each handler runs under `xpcall(call, eh)` | `[T1 obs / T3: Simulationcraft/libs/CallbackHandler-1.0/CallbackHandler-1.0.lua:25-57 — `CreateDispatcher` at :25, `loadstring` at :51, `Dispatchers` memo table at :54-58]` |
| v7 | **No `loadstring` dispatcher.** A plain `repeat … until` loop calling `xpcall(method, errorhandler, ...)` | `[T1 obs / T3: RaiderIO/libs/CallbackHandler-1.0/CallbackHandler-1.0.lua:25-32]` |
| v8 | Same loop shape, but `securecallfunction(method, ...)` instead of `xpcall` | `[T3: Ace3@4475787f CallbackHandler-1.0/CallbackHandler-1.0.lua:15-22, call at :19]` |

An addon shipping v6 will, at runtime, be talking to whichever minor won.

> **Corrected on verification.** An earlier draft said "v6 *and v7* build
> dispatchers with `loadstring`". Only v6 does. v7 still *upvalues* `loadstring`
> at `:11` — vestigially, it is never called — which is presumably what misled
> the first pass. The taint-relevant difference (`xpcall` vs
> `securecallfunction`) is v7→v8, not v6→v7.

**Upgrade-in-place is the library's job, and libraries disagree about it.** Two
contrasting real implementations:

- `CallbackHandler-1.0` does `if not CallbackHandler then return end -- No upgrade
  needed` and then rebuilds nothing. Registries created by an older minor keep the
  closures they were built with `[T3: Ace3 copy CallbackHandler-1.0.lua:5, with the
  per-registry closures created inside `CallbackHandler.New` at :32-…]`.
- `LibDataBroker-1.1` does the opposite: it captures `oldminor` and patches the live
  table under version gates — `if oldminor < 2 then … end`, `if oldminor < 3 then … end`
  `[T1 obs / T3: BigWigs/Libs/LibDataBroker-1.1/LibDataBroker-1.1.lua:5-7, :14, :21, :35]`.

**Load order is not something you control.** LibStub has no dependency graph. The
convention libraries use instead is a hard assert at the top of the file:
`assert(LibStub, "LibDataBroker-1.1 requires LibStub")` and
`assert(LibStub:GetLibrary("CallbackHandler-1.0", true), "LibDataBroker-1.1 requires
CallbackHandler-1.0")` `[T3: same file, :2-3]`.

`[gap]` I could not establish, from Tier 1 or Tier 2, the exact inter-addon file
load order the client uses, so I cannot state which copy of a library "usually"
wins on a given install. The `.toc`/dependency ordering rules are the
`anatomy-and-runtime` topic's; the observable consequence here is only that
*multiple minors coexist on disk*.

---

## 3. Embedding vs standalone: how it actually works

### 3.1 There is no such thing as "installing a library"

A library is just Lua files that some addon's load list points at. Two entry points
are conventional, and mature libraries ship both:

- **`lib.xml`** (or `<Name>.xml`) — a minimal `<Ui>` wrapper with `<Script file=…/>`,
  meant to be `<Include>`d by the *embedding addon*. Example, verbatim, four lines
  (the `xmlns` block wraps): `<Ui …>` / `<Script file="LibSharedMedia-3.0.lua" />` /
  `</Ui>` `[T1 obs / T3: Bartender4/libs/LibSharedMedia-3.0/lib.xml]`.
- **`<Name>.toc`** — for standalone installation.

Whether a *packaged* copy carries either file is not predictable, because the
packager can strip them. On this install: `Bartender4/libs/LibSharedMedia-3.0/`
holds `lib.xml` and no `.toc`; `TellMeWhen/Lib/LibSharedMedia-3.0/` holds a
`.toc`; and `BigWigs/Libs/LibSharedMedia-3.0/` holds **neither** — just the
`.lua` — because `Libs/LibSharedMedia-3.0/lib.xml` is in BigWigs' `.pkgmeta`
`ignore:` list `[T1 obs, 2026-07-23; T3: BigWigs@3fdc10f6 .pkgmeta ignore block]`.
Counted across the install there are 24 `lib.xml` files and 38 `.toc` files at
depth ≥3 (i.e. inside a parent addon) `[T1 obs]`.
`[gap]` I did **not** establish that "mature libraries ship both" as a norm — an
earlier draft asserted that without a survey. What is shown above is that all
three combinations occur.

Details! shows the embedding side plainly: an `embeds.xml` that `<Script>`s
`Libs\LibStub\LibStub.lua` first and then `<Include>`s each library's own xml
`[T3: details@e14de53c embeds.xml]`. Ace3 shows it from the library side: its own
`.toc` lists `LibStub\LibStub.lua` before every `Ace*-3.0\Ace*-3.0.xml`
`[T3: Ace3@4475787f Ace3.toc]`.

### 3.2 An embedded library's `.toc` is inert, and is routinely stale

Because the client only loads `Interface/AddOns/<Folder>/<Folder>.toc` (plus the
flavour-suffixed forms of that same name, e.g. `<Folder>_Mainline.toc`) — *"The
filename of the `.toc` file must match the folder it's inside, otherwise the
`.toc` file won't load"* `[T2 wiki: TOC format, revid 6767089, 2026-07-09,
wikitext lines 2, 5, 180]` — a `.toc`
sitting inside `SomeAddon/Libs/SomeLib/` is never parsed by the client. The
consequence is visible on this install: `EllesmereUI/Libs/LibDeflate/LibDeflate.toc`
declares `## Interface: 80300` — an 8.3.0 interface number, five expansions stale —
inside an addon running on 12.0.7 `[T1 obs: that file, line 1]`. **Never read an
embedded library's `## Interface:` as a compatibility signal.**

### 3.3 `.pkgmeta` externals: resolved at package time, not in git

The BigWigs packager (`release.sh`, 3351 lines) reads `.pkgmeta` and fetches
`externals` from Git/SVN/Mercurial during packaging
`[T3: packager@36b4c3b7 README.md:80-81]`. Caveat straight from that README: *"An
external's .pkgmeta is only parsed for ignore and externals will not have
localization keywords replaced"* `[T3: README.md:80-81]`. `enable-nolib-creation`
(default `no`) produces a stripped build for users who fetch libraries separately
`[T3: README.md:89-92]`; `no-lib-strip` marks blocks kept out of *nolib* builds and
is **not supported in Lua files** `[T3: README.md:163-164]`.

**The commonly repeated claim "libraries are never in the addon's git repo" is
false as a general rule.** Measured across the seven clones:

| Clone | lib dirs present in git | externals declared in `.pkgmeta` |
|---|---|---|
| WeakAuras2 `38d4bf1e` | 0 | 25 |
| ElvUI `f60934a1` | 10 (`ElvUI_Libraries/Game/Shared/`, incl. a 50-file oUF) | 21 |
| BigWigs `3fdc10f6` | 3 (`Libs/LibStub`, `Libs/CallbackHandler-1.0`, `Libs/LibDataBroker-1.1`) | 16 |
| Details! `e14de53c` | 18 (`Libs/` holds 19 entries, one of which is the file `libs.xml`) | **0 — no `externals:` block at all** |
| Plater `2b2ff463` | 23 (`libs/` holds 25 entries; `indent.lua` and `libs.xml` are files) | 23 (the same set, vendored *and* declared) |
| oUF `5672a3cb` | 0 | 0 — `.pkgmeta` has no externals; oUF has no library dependencies |
| Bagnon `9f72bd96` | 0 | **no `.pkgmeta` file exists**; deps come via `## Dependencies: BagBrother` |

`[T3: `ls`/`find` over each clone plus each `.pkgmeta`, 2026-07-23. Details' pkgmeta
is `package-as` + `move-folders` only; Bagnon.toc:10 carries the Dependencies line.]`

So: **grepping a clone and finding no `LibStub` proves nothing** (true for
WeakAuras2), but **finding library code in a clone is also normal** (true for four
of seven). Read the `.pkgmeta` before concluding either way.

WeakAuras' `.pkgmeta` remains the single richest dependency census of a large 2026
addon — **25** externals across `WeakAuras/Libs/` (20) and `WeakAurasOptions/Libs/` (5),
two of them version-pinned (`Archivist` at tag `v1.0.8`, `LibSerialize` at tag `v1.0.0`)
and drawn from **four** different hosts — `github.com`, `repos.curseforge.com`,
`repos.wowace.com` (`LibUIDropDownMenu`), and
`www.townlong-yak.com/addons.git/taintless` `[T3: WeakAuras2@38d4bf1e .pkgmeta,
re-parsed 2026-07-23]`. (An earlier draft said three hosts and omitted
`repos.wowace.com`.)

### 3.4 Embedding into an *object*: the Ace3 `:Embed` contract

"Embedding" also names a second, unrelated thing: copying a library's methods onto
your addon table. AceAddon implements it and defines the contract:

```
local lib = LibStub:GetLibrary(libname, true)
… elseif lib and type(lib.Embed) == "function" then
      lib:Embed(addon)
  elseif lib then
      error("… Library '%s' is not Embed capable")
```
`[T3: Ace3@4475787f AceAddon-3.0/AceAddon-3.0.lua:182-193]`

So **a library is "embeddable" iff it exposes `lib:Embed(target)`**, and asking
AceAddon to embed one that doesn't is a hard error, not a silent skip. That is a
checkable rule about Ace3, not about the game.

---

## 4. CallbackHandler-1.0 — the pub/sub substrate

`CallbackHandler:New(target[, RegisterName, UnregisterName, UnregisterAllName])`
installs `:RegisterCallback` / `:UnregisterCallback` / `:UnregisterAllCallbacks`
onto `target` and returns a registry with `:Fire(eventname, ...)`
`[T3: Ace3@4475787f CallbackHandler-1.0/CallbackHandler-1.0.lua:32, defaults at :34-38, `registry:Fire` at :49]`.
Passing `false` for `UnregisterAllName` suppresses that method `[T3: :36-38]`.

At v8 (current in Ace3, 10 of 14 copies on this install) dispatch runs each
subscriber through `securecallfunction` `[T3: :15-22, call at :19]`. That is
relevant to the taint topic — but exactly *what* `securecallfunction` guarantees
belongs to `security-taint-and-restricted-data`, not here; this file records only
that v8 uses it and v6/v7 did not. v6/v7 ran subscribers under `xpcall` (v6 via a
`loadstring`-generated dispatcher, v7 via a plain loop) — see the table in §2.3.

Re-entrancy is handled with a `recurse` counter and an `insertQueue`, so
registering from inside a callback is deferred rather than mutating the table
mid-iteration `[T3: Ace3 copy — `registry:Fire` at :49, recurse counter :51-56,
queue drain :58-72]`.

**Blizzard ships something comparable** — `CallbackRegistryMixin`, §7. It is a
mixin you apply to your own object, not a shared cross-addon registry reachable by
name, so it is not a drop-in replacement for the LibStub-published
CallbackHandler that libraries like LibSharedMedia and LibDataBroker hand out.

---

## 5. Ace3

`https://github.com/WoWUIDev/Ace3`, clone at `4475787f06f7` (2026-07-10), 110 stars
`[T2 gh]`. **Actively maintained**: the changelog's newest entry is
*"Ace3 Release - Revision r1390 (February 3rd, 2026)"* and its first bullet is a
12.0-specific migration note — *"AceConfigDialog-3.0: The original category ID is
now preserved in AddToBlizOptions in 12.0, making it mandatory for addons to store
the second return value and forward it to Settings.OpenToCategory"*
`[T3: Ace3@4475787f changelog.txt:1, :3]`. The r1377 entry (2025-10-28) carries
*"AceComm-3.0: Updated ChatThrottleLib for WoW 12.0"* and
*"AceGUI-3.0: EditBox: Fix InsertLink hook for WoW 12.0"* `[T3: changelog.txt:8-15 — the quoted bullets are :10 and :15]`.

**Do not treat a `wowace.com` / CurseForge-SVN pointer for Ace3 as a staleness
signal.** An earlier draft of this file claimed exactly that and it is **refuted**
by current evidence: WeakAuras2 at `38d4bf1e` (2026-07-20) pulls five Ace3
components straight from `https://repos.curseforge.com/wow/ace3/trunk/…`, and
BigWigs at `3fdc10f6` (2026-07-21) pulls six from
`https://repos.wowace.com/wow/ace3/trunk/…` `[T3: their `.pkgmeta` externals
blocks]`. Ace3's own toc still carries `## X-Website: http://www.wowace.com`
`[T3: Ace3@4475787f Ace3.toc:6]`. The SVN trunks are live mirrors that the two
biggest addons in the corpus package from today.
`[gap]` The GitHub repo `WoWUIDev/Ace3` was **created 2022-09-20**
`[T2 gh: `.created_at`]`, but I could not establish from Tier 1 or Tier 2 that
the project *moved* orgs, or which of GitHub / CurseForge SVN / wowace SVN is
canonical versus mirrored. Treat all three as live locations.

`Ace3.toc` declares
`## Interface: 11508, 11509, 20505, 20506, 30405, 38001, 40402, 50503, 50504, 120100, 120005, 120007`
— multi-flavour comma form, and it lists **120100**, an *interface* number for a
12.1.0 client, ahead of live 12.0.7 (`120007`) `[T3: Ace3.toc:1]`. (Interface
numbers are `MMmmpp`, not build numbers; the earlier draft called it a build
number.)

### 5.1 Component register (versions read off the clone)

| Component | MAJOR/MINOR | Lines | What it actually buys you |
|---|---|---|---|
| `AceAddon-3.0` | 13 `[:33]` | 649 | Addon/module object graph, `OnInitialize`/`OnEnable`/`OnDisable` lifecycle keyed to `ADDON_LOADED`/`PLAYER_LOGIN`, library embedding. |
| `AceEvent-3.0` | 4 | 126 | `self:RegisterEvent("X", handler)` on your object; one shared hidden frame. |
| `AceTimer-3.0` | 17 `[:20]` | 278 | Handle-based cancel, `:CancelAllTimers()` per object. **Thin over `C_Timer.After`.** |
| `AceBucket-3.0` | 4 | 260 | Coalescing bursty events into one delayed call. |
| `AceHook-3.0` | 9 `[AceHook-3.0.lua:13]` | 510 | Managed secure/insecure hooks with unhooking; checks `issecurevariable` before deciding `[:151, :153]`, uses `hooksecurefunc` `[:234, :244]`. |
| `AceDB-3.0` | 33 `[AceDB-3.0.lua:44]` | 797 | Profiles, defaults, namespaces over SavedVariables. |
| `AceDBOptions-3.0` | 15 `[:5]` | 456 | The stock profile-management options table. |
| `AceLocale-3.0` | 6 `[:5]` | 133 | Locale tables with fallback. §6. |
| `AceConsole-3.0` | 7 | 246 | Slash-command registration + printf helpers. |
| `AceGUI-3.0` | 41 `[AceGUI-3.0.lua:28]` | 7110 | Widget toolkit (the biggest single component by far). |
| `AceConfig-3.0` | 3; `Registry` 22, `Cmd` 14, `Dialog` 92 | 3263 | Declarative options-table → GUI + slash interface. |
| `AceComm-3.0` | 14 | 1002 | Addon-message chunking (`\001`/`\002`/`\003` prefixes, 255-byte payloads) over a bundled ChatThrottleLib `[:41-43, :95]`. |
| `AceSerializer-3.0` | 5 | 287 | `^S`/`^N`/`^F`/`^T`/`^B`/`^Z` (+ `^f`/`^t`/`^b`) text serialization `[:54-107]`. |
| `AceTab-3.0` | 10 `[AceTab-3.0.lua:7]` | 442 | Tab-completion in edit boxes. |
| `CallbackHandler-1.0` | 8 | 202 | §4. Bundled, not strictly part of Ace. |

`[T3: all from Ace3@4475787f; line counts are `wc -l` over each component dir.]`

### 5.2 When *not* to use Ace3

These are honest observations, not rules.

- **AceTimer over C_Timer.** AceTimer-3.0 upvalues `C_Timer.After` and calls it for
  every schedule; it clamps delays below 0.01 s because *"Restrict to the lowest time
  that the C_Timer API allows us"* `[T3: AceTimer-3.0.lua:30 (upvalue), :33-35 (the
  clamp — `if` on :33, assignment + comment on :34), :66 (the same clamp on the
  looping re-arm), :67 and :75 (the `C_TimerAfter` calls)]`. If you
  need one fire-and-forget delay, `C_Timer.After` is the same thing without a
  dependency `[T1 docs: UITimerDocumentation.lua:11]`. AceTimer earns its keep only
  when you need cancellation handles or per-object bulk cancel.
- **AceAddon is not required to use the rest of Ace3.** Of the seven clones, only
  **two** call `LibStub("AceAddon-3.0")` from their own code — Details
  `[T3: details@e14de53c boot.lua:9 — `LibStub("AceAddon-3.0"):NewAddon("_detalhes",
  "AceTimer-3.0", "AceComm-3.0", "AceSerializer-3.0", "NickTag-1.0")`]` and ElvUI
  `[T3: ElvUI@f60934a1 ElvUI/Game/Shared/General/Initialize.lua:37 —
  `_G.LibStub('AceAddon-3.0')`]`. **Plater does not**: it declares `libs/AceAddon-3.0`
  as an external but the string `AceAddon` appears zero times outside `libs/`
  `[T3: plater@2b2ff463, grep 2026-07-23]` — an earlier draft of this file listed
  Plater here and that was wrong. WeakAuras and BigWigs also do not; the only
  `AceAddon` hits in BigWigs are two backwards-compat comments
  `[T3: BigWigs@3fdc10f6 Core/Core.lua:452, :501]`. WeakAuras uses Ace3 for the
  options UI plus comms and serialization — its non-lib Lua names `AceGUI-3.0` 47×,
  and `AceTimer-3.0` / `AceSerializer-3.0` / `AceComm-3.0` twice each
  `[T3: string census over each clone's non-lib Lua, 2026-07-23]`.
- **AceGUI-3.0 is 7110 lines.** If your options are five checkboxes, Blizzard's own
  `Settings` API (§7) is a smaller surface with no dependency and native placement in
  the game's options panel.
- **AceSerializer-3.0 has no secret-value awareness.** Its dispatcher branches on
  `type(v)` for `string`/`number`/`table`/`boolean`/`nil` and *errors* on anything
  else: `error(MAJOR..": Cannot serialize a value of type '"..t.."'")`
  `[T3: AceSerializer-3.0.lua — `SerializeValue` at :54, `local t=type(v)` at :56,
  the branch chain at :58 / :63 / :83 / :93 / :101, and the `error` at **:106**]`.
  (An earlier draft cited `:104` for the error; it is `:106`.)
  Neither `LibSerialize` nor `LibDeflate`
  mentions secrets either — zero hits for `issecretvalue`/`secret` in
  `libs/LibSerialize/LibSerialize.lua` and `libs/LibDeflate/LibDeflate.lua`
  `[T3: grep over `raw/addon-research/libs/`]`. What actually happens when a secret
  value reaches one of them is `@verify-ingame`.

---

## 6. Localization

**AceLocale-3.0** (v6, 133 lines) normalises `enGB` → `enUS` at load
`[T3: AceLocale-3.0.lua:15-18]` and hands back a table whose `__index` is the
interesting part:

```lua
__index = function(self, key)
    rawset(self, key, key)
    geterrorhandler()(MAJOR..": "..…..": Missing entry for '"..tostring(key).."'")
    return key
end
```
`[T3: AceLocale-3.0.lua:24-30]` — a missing key **returns the key itself and raises a
non-fatal error**, once per key. `:NewLocale(app, locale, isDefault, silent)` with
`silent` swaps in a variant that returns the key without complaining `[T3: :33-38]`.
Registering a non-default locale writes through a proxy that turns `= true` into
`= key`; the default-locale proxy refuses to overwrite an existing value so locale
files can load in any order `[T3: :48-69]`.

**It is far from universal.** Across the seven clones: Details references
`AceLocale-3.0` in 108 files, Bagnon in 3, ElvUI in 2, Plater in 1; **WeakAuras,
BigWigs and oUF reference it in zero** and instead branch on `GetLocale()` in
plain Lua tables (WeakAuras 34 files, BigWigs 14) `[T3: grep census over the clones,
2026-07-23]`. That is four of seven using it at all and only one leaning on it hard.
So **not using AceLocale is normal in this corpus**. What the three non-users
actually do is branch on `GetLocale()` and select a plain Lua table; I did **not**
verify that any of them uses the specific
`setmetatable({}, {__index=function(_,k) return k end})` fallback idiom, so treat
that idiom as a suggestion, not as observed practice `[gap]`.

`[gap]` The wiki's `Localizing an addon` HOWTO was last edited **2023-10-22**
(revid 5585193, 143 lines) `[T2 wiki]` — I did not verify its contents against
12.0.7 behaviour and would not cite it for anything mechanical.

---

## 7. What Blizzard now ships that used to need a library

This is the most important part of the buy-vs-build map, because most guides
predate it. All Tier 1.

| Need | Blizzard's shipped answer | Evidence |
|---|---|---|
| Delayed / repeating calls | `C_Timer.After` / `NewTicker` / `NewTimer` | `[T1 docs: UITimerDocumentation.lua:11, :22, :39]` |
| Intra-addon pub/sub | `CallbackRegistryMixin` — `RegisterCallback`, `TriggerEvent`, `GenerateCallbackEvents`, `RegisterCallbackWithHandle` | `[T1 src: Blizzard_SharedXMLBase/CallbackRegistry.lua:112, :155, :184, :269]` |
| A global event bus (Blizzard's own; addons can reach it because it is a global) | `EventRegistry` (a `CallbackRegistryMixin` instance with `SetUndefinedEventsAllowed(true)`, plus `RegisterFrameEvent`/`UnregisterFrameEvent` refcounting) | `[T1 src: Blizzard_SharedXMLBase/GlobalCallbackRegistry.lua:1-11, :13-36]` — the source shows *what it is*; it contains **no** statement that addons are an intended consumer, and the taint consequences of an addon publishing on it are `security-taint-and-restricted-data`'s. `[gap]` |
| Options panel | The `Settings` API: `RegisterAddOnCategory`, `RegisterVerticalLayoutCategory`, `RegisterCanvasLayoutCategory`, `RegisterAddOnSetting`, `CreateCheckbox`, `CreateSlider`, `CreateDropdown`, `OpenToCategory` | `[T1 src: Blizzard_Settings_Shared/Blizzard_Settings.lua:133, :153, :161, :173, :382, :398, :404, :143]` |
| Minimap button / launcher | The **addon compartment** — declare `## AddonCompartmentFunc` (plus `…FuncOnEnter`/`…FuncOnLeave`) in your `.toc`; Blizzard reads it with `GetAddOnMetadata` and registers you | `[T1 src: Blizzard_Minimap/Mainline/AddonCompartment.lua:81, :106, :113, :136]` |
| Dropdown / context menus | `Blizzard_Menu` — `MenuUtil.CreateContextMenu`, `CreateButtonMenu`, `CreateCheckboxMenu`, `CreateRadioMenu` | `[T1 src: Blizzard_Menu/MenuUtil.lua:151, :335, :354, :373]` |
| Object pooling | `CreateObjectPool` / `CreateFramePool` / `CreateTexturePool` / `CreateFontStringPool` / `CreateActorPool` / `CreateFramePoolCollection` — note these are **aliases to the `CreateSecure*` variants** | `[T1 src: Blizzard_SharedXMLBase/Pools.lua:856-861, alias comment at :854-855]` |
| Mixin-style OO | `Mixin`, `CreateFromMixins` (implemented by the client, not in Lua), plus `CreateAndInitFromMixin`, `SecureMixin` | `[T1 docs: Blizzard_APIDocumentationGenerated/FrameScriptDocumentation.lua:82 (`CreateFromMixins`), :279 (`Mixin`) — i.e. FrameScript, not Lua. T1 src: Blizzard_SharedXMLBase/Mixin.lua:5-6 (upvalued as `PrivateMixin`/`PrivateCreateFromMixins`), :8-12, :23-30. Grep for `function Mixin(`/`function CreateFromMixins(` over the whole checkout → zero definitions]` |

### 7.1 The UIDropDownMenu situation, stated precisely

Blizzard's own in-source guide says it outright:

> *"Blizzard_Menu is a new framework for creating context menus and dropdown menus,
> and is a complete replacement for UIDropDownMenu. All uses of UIDropDownMenu have
> been converted to use Blizzard_Menu, and UIDropDownMenu is now deprecated. Due to
> the large fundamental differences between these two systems, shims have not been
> provided…"*

`[T1 src: Blizzard_Menu/11_0_0_MenuImplementationGuide.lua:4-7]`

But **it is deprecated, not removed at 12.0.7**: `Mainline\UIDropDownMenu.lua` is
still listed in the shipped toc and is still a 1589-line implementation defining 62
`UIDropDownMenu*` functions `[T1 src: Blizzard_SharedXML/Blizzard_SharedXML_Mainline.toc:212-215;
Blizzard_SharedXML/Mainline/UIDropDownMenu.lua, `wc -l` = 1589, 62 `^function UIDropDownMenu` matches]`.
`[gap]` That file opens with `local envTable = GetCurrentEnvironment();` and resolves
frames through `envTable[...]` rather than `_G` `[T1 src: same file:1, :53, :71]`, so
I **cannot** conclude from source alone that `UIDropDownMenu_Initialize` is still
reachable as a global from addon code. Relatedly — though I have no source stating
the causal link — `LibUIDropDownMenu`, a forked copy of the old system, is still an
external in WeakAurasOptions in 2026
`[T3: WeakAuras2@38d4bf1e .pkgmeta — `WeakAurasOptions/Libs/LibUIDropDownMenu:
https://repos.wowace.com/wow/libuidropdownmenu/trunk/LibUIDropDownMenu`]`.
Resolving whether the globals still work is `@verify-ingame`.

---

## 8. The libraries worth not rewriting

Ranked by how much of the problem is *cross-addon coordination* — the part you
genuinely cannot solve alone.

### 8.1 LibSharedMedia-3.0 — the strongest case for "do not roll your own"

It is a **shared registry**: one addon registering a font makes that font selectable
in every other addon that consumes LSM. That coordination is the entire product;
a private copy is worthless. 324 lines.

Version on this install is `12000001`, commented `-- 12.0.0 v1 / increase manually on
changes` — patch-derived versioning, and evidence of Midnight-era maintenance. All
5 copies on the install are that version `[T1 obs: BigWigs, Bartender4, DandersFrames,
EllesmereUI, TellMeWhen copies of `LibSharedMedia-3.0.lua:13`]`.

Contract worth knowing, all from `[T1 obs / T3: BigWigs/Libs/LibSharedMedia-3.0/LibSharedMedia-3.0.lua]`:

- Media types are `background`, `border`, `font`, `statusbar`, `sound` `[:54-58]`.
- `:Register(mediatype, key, data, langmask)` **returns `false` rather than erroring**
  when the key is already taken — first registration wins `[:264-267]`.
- Path-registered background/border/statusbar/sound media must live under
  `interface`: *"files accessed via path only allowed from interface folder"* `[:251-256]`.
- Sounds must be `.ogg` or `.mp3` `[:257-260]`.
- Non-string `mediatype`/`key` **do** error `[:240-245]`.
- Registration fires `LibSharedMedia_Registered` through its CallbackHandler
  registry `[:37, :39, :271]`; `:Fetch` falls back to the default for the type unless
  `noDefault` `[:275-280]`.
- Fonts registered without a `langmask` are silently dropped on non-western clients
  `[:247-250]`.

Upstream is CurseForge SVN — the file carries a `--@curseforge-project-slug:
libsharedmedia-3-0@` marker on line 1 `[T1 obs: LibSharedMedia-3.0.lua:1]`, and
WeakAuras/BigWigs both external it from
`repos.curseforge.com`/`repos.wowace.com` `[T3: their `.pkgmeta`]`.
`[gap]` There is no *canonical* GitHub repo I could find: a
`gh api search/repositories q=LibSharedMedia-3.0` on 2026-07-23 returns only
third-party mirrors (`wowace-clone/`, `WoWAddonMirrors/`, `NoobTaco/`), none
official and all 0★. Read the vendored copies.

### 8.2 LibDataBroker-1.1 + LibDBIcon-1.0 — the launcher/data-feed pattern

LDB is 90 lines and is essentially a **specification**: a metatable-mediated
attribute store that fires four differently-scoped `LibDataBroker_AttributeChanged*`
callbacks on every attribute write `[T1 obs / T3: BigWigs/Libs/LibDataBroker-1.1/LibDataBroker-1.1.lua:22-33, the four `Fire` calls at :28-31]`.
`__metatable = "access denied"` blocks metatable inspection `[:16]`.

LibDBIcon-1.0 (713 lines) **hard-requires** it. It calls
`LibStub("LibDataBroker-1.1", true)` at `:11` — the `true` only suppresses
LibStub's own error message, because `:12` immediately raises its own:
`if not ldb then error(DBICON10 .. " requires LibDataBroker-1.1.") end`
`[T1 obs: LibDBIcon-1.0.lua:10-12]`. (An earlier draft read the silent flag as
"consumes LDB optionally"; it does not.) It provides the minimap button, with
`Register/Lock/Unlock/Hide/Show/
IsRegistered/Refresh/GetMinimapButton/SetButtonRadius/…` `[T1 obs: LibDBIcon-1.0.lua:11,
`lib:Register` at :363, `lib:AddButtonToCompartment` at :637]`. It also bridges into Blizzard's addon compartment
(`AddonCompartmentFrame` upvalued at `:20`, `customCompartmentIcon` parameter on
`:Register` at `:363`, `AddButtonToCompartment` at `:313`).

Given §7, the honest position is: **if all you need is a click target, the addon
compartment is a `.toc` line with no dependency.** LDB+LibDBIcon buy you a *live
text/value feed* that other displays can render, and a draggable minimap icon —
neither of which Blizzard ships.

### 8.3 Serialization and compression

- **LibSerialize** — active (`pushed_at` 2026-07-16) `[T2 gh: rossnichols/LibSerialize]`.
  The modern binary serializer; WeakAuras pins it at tag `v1.0.0` `[T3: WeakAuras2 .pkgmeta]`.
- **LibDeflate** — pure-Lua DEFLATE/zlib. `pushed_at` **2021-05-05**
  `[T2 gh: SafeteeWoW/LibDeflate, 117 stars, not archived]`. **Stable by design, not
  abandoned**: an external in WeakAuras' and Plater's `.pkgmeta` in 2026, vendored
  in-tree by ElvUI (`ElvUI_Libraries/Game/Shared/LibDeflate/` — **not** an ElvUI
  external, contrary to an earlier draft) and by Details!, and present on this
  install `[T3: those `.pkgmeta` files and trees, 2026-07-23; T1 obs:
  EllesmereUI/Libs/LibDeflate/]`. Say "unchanged since 2021", never "unmaintained".
- **LibCompress** — the thing LibDeflate replaced. The copy on this install carries
  `Revision: $Revision: 83 $` / `Date: 2018-07-03` and registers as
  `LibStub:NewLibrary("LibCompress", 90000 + tonumber(("$Revision: 83 $"):match("%d+")))`
  — i.e. 90083 `[T1 obs:
  MythicDungeonTools/libs/LibCompress/LibCompress.lua:7-9, :13]`. LibDeflate's own
  README benchmarks against it and reports *"LibDeflate with compression level 1
  compresses as fast as LibCompress, but already produces significantly smaller
  data"* `[T3: libs/LibDeflate/README.md:127]`. **Legacy. Prefer LibDeflate for new
  work.** It is still shipped only because old import/export strings need decoding.

### 8.4 Addon comms

`AceComm-3.0` (chunking + ChatThrottleLib) and `Chomp` (`wow-rp-addons/Chomp`,
`pushed_at` 2026-04-20 `[T2 gh]`) are the two live transports. WeakAuras externals
Chomp; Plater, ElvUI and Details external AceComm `[T3: their `.pkgmeta`]`. Mechanics
and the Midnight comms restrictions belong to
`state-persistence-and-communication` — this file only records that both libraries
are alive and that AceComm's payload limit is a hardcoded 255 with the comment
*"Yes, the max is 255 even if the dev post said 256. I tested."*
`[T3: Ace3 AceComm-3.0/AceComm-3.0.lua:95]`.

---

## 9. Maintenance status register

**Recommending a dead library is a real harm, so this table is evidence-first.**
`pushed_at` is repo activity, not proof the code works; a stale date on a
specification-shaped library means nothing.

| Library | Live evidence | Status |
|---|---|---|
| **Ace3** | `WoWUIDev/Ace3` pushed 2026-07-10, 110★ `[T2 gh]`; changelog r1390 dated 2026-02-03 with 12.0-specific fixes `[T3: changelog.txt:1-6]` | **Active.** |
| **LibStub** | Frozen at minor 2 since 2007 `[T1 obs: BigWigs copy `$Id … 2007-09-03` at :1]`; 23 copies on this install, all minor 2 | **Frozen by design.** Not a risk. |
| **CallbackHandler-1.0** | v8 in Ace3 `[T3]`; 10 of 14 install copies at v8 | **Active** (ships inside Ace3). |
| **LibSharedMedia-3.0** | Version `12000001` = "12.0.0 v1" `[T1 obs: :13]`; CurseForge SVN upstream | **Active**, but SVN-hosted and un-clonable from here. |
| **LibDataBroker-1.1** | `tekkub/libdatabroker-1-1` pushed **2015-09-02**, 58★, not archived `[T2 gh]`; 90 lines | **Frozen spec.** Fine to depend on. |
| **LibDBIcon-1.0** | No canonical GitHub repo (`Nevcairiel/LibDBIcon-1.0` → 404; repo search returns only 0★ mirrors) `[T2 gh]`; the single install copy is minor **56** `[T1 obs: :9]` and knows about `AddonCompartmentFrame` `[T1 obs: :20]`, a 10.0-era feature | **`[gap]` Status not established.** Still externalled by BigWigs, WeakAuras and Plater in 2026 `[T3: their `.pkgmeta`]`, which shows it is *shipped*. I found **no** direct evidence of Midnight-era commits — an earlier draft asserted "Active on CurseForge SVN" without any. Only readable via vendored copies. |
| **LibDeflate** | pushed 2021-05-05, 117★ `[T2 gh]`; still externalled by 3 major addons in 2026 `[T3]` | **Stable, still standard.** |
| **LibSerialize** | pushed 2026-07-16 `[T2 gh]` | **Active.** |
| **LibCompress** | Revision 83, 2018-07-03 `[T1 obs]`; superseded per LibDeflate README `[T3]` | **Legacy.** New code should not adopt it. |
| **Chomp** | pushed 2026-04-20 `[T2 gh]` | **Active.** |
| **LibSpecialization** | `BigWigsMods/LibSpecialization` pushed 2026-07-17 `[T2 gh]` | **Active.** |
| **LibCustomGlow-1.0** | `Stanzilla/LibCustomGlow` pushed 2026-07-17 `[T2 gh]`; secret-aware on this install `[T1 obs]` | **Active.** |
| **LibRangeCheck-3.0** | `WeakAuras/LibRangeCheck-3.0` pushed 2026-07-04 `[T2 gh]` | **Active.** |
| **LibGetFrame-1.0** | `mrbuds/LibGetFrame` pushed 2026-07-17 `[T2 gh]` | **Active.** |
| **LibDispel** | `tukui-org/LibDispel` pushed 2026-07-21 `[T2 gh]` | **Active.** |
| **Archivist** | `emptyrivers/Archivist` pushed 2026-02-18 `[T2 gh]`; WeakAuras pins `v1.0.8` `[T3]` | **Maintained, slow.** |
| **oUF** | `oUF-wow/oUF` pushed 2026-07-22, 236★ `[T2 gh]`; `oUF.toc` declares `## Interface: 120007, 120100` `[T3]` | **Active.** |
| **Details Framework (DF)** | `Tercioo/Details-Framework` pushed 2026-07-10 `[T2 gh]` | **Active**, but effectively single-author. |
| **LibDogTag-3.0** | The copy **vendored inside TellMeWhen** versions itself `20260619153904` and carries a secret-value shim `[T1 obs: TellMeWhen/Lib/LibDogTag-3.0/LibDogTag-3.0.lua:9; Helpers.lua:138]` | **Maintained *as shipped by TellMeWhen*.** The version number is a timestamp-shaped integer, and reading it as "2026-06-19" is an inference, not a dated commit. `[gap]` I did not reach LibDogTag-3.0 upstream (wowace SVN per its own header at :4) and so cannot say whether the maintenance is upstream's or TellMeWhen's fork. Either way the "dead library" reputation is wrong for this copy. |
| **LibSpellRange-1.0** | `ascott18/LibSpellRange-1.0` pushed **2024-08-19** `[T2 gh]`; still a WeakAuras external `[T3]` | **Quiet.** Pre-Midnight. Check before adopting. |
| **LibTranslit** | `Vardex/LibTranslit` pushed **2022-11-11** `[T2 gh]` | **Quiet.** Small enough that this may be fine. |
| **TaintLess** | `libs/TaintLess@a4f3eda9`, last commit **2025-02-26**, self-versioned `[24-07-27]`; predates Midnight (12.0.0, 2026-01-20) | **Tier down.** Still shipped by WeakAuras and ElvUI, which proves it is *shipped*, not *current*. Its fix set is pre-secret-values. |
| **LibBabble-\*-3.0** | Only surviving copies on this install are inside TellMeWhen, at `LibBabble-3.0` minor **2** `[T1 obs]` | **Legacy.** Localised-name lookup tables; do not adopt. |
| **Dongle, Sea, LibKarma** | The only *framework* entries in the wiki's near-abandoned library category, whose full membership is `Ace (AddOns)`, `ChatThrottleLib`, `Dongle`, `LibKarma`, `Sea (add-on)` `[T2 wiki: Category:Function Libraries, revid 5355606, 2019-06-08, members read via the MediaWiki API 2026-07-23]`; zero copies on this install `[T1 obs]` | **Dead.** (An earlier draft also listed **Rock** and **Ace2** here as "named on the category" — they are **not** members. They may well be dead, but this file has no evidence for them, so they are removed rather than asserted.) |

### 9.1 Where libraries actually live now

- **GitHub** — most modern libraries. `gh api` works; use it for maintenance signals.
- **CurseForge SVN** (`repos.curseforge.com`, `repos.wowace.com`) — still the home of
  LibStub, CallbackHandler, LibSharedMedia-3.0, LibDBIcon-1.0, LibSink-2.0,
  LibCandyBar-3.0, LibDualSpec-1.0, AceGUI-3.0-SharedMediaWidgets, LibUIDropDownMenu
  `[T3: the externals blocks in WeakAuras2, BigWigs, Plater, ElvUI `.pkgmeta`]`.
  `curseforge.com/wow/addons` is Cloudflare-403 from this box; the SVN repos need an
  SVN client. **Read the vendored copies in the live install.**
- **WoWInterface is stale as a library source.** Its public file list
  (`api.mmoui.com/v3/game/WOW/filelist.json`, 8134 entries, fetched 2026-07-23)
  shows `Ace3` last updated **2017-09-04** there, against r1390 / 2026-02-03 upstream
  `[T2: api.mmoui.com filelist.json vs Ace3@4475787f changelog.txt:1]`. Never take a
  library's version from WoWInterface.

`[gap]` I could not obtain download/adoption counts. `addons.wago.io`'s API returns
**401 Unauthorized** without a key, and CurseForge is 403. So every "widely used"
statement in this file is backed by *counted copies on one install* or *counted
`.pkgmeta` references*, never by download numbers. The 2000+-dependents figure the
wiki cites for LibStub is itself sourced to a now-dead wowace page
`[T2 wiki: LibStub, revid 6029070, ref 1]`.

---

## 10. Midnight (12.0) and libraries

The secret-value change reached library code. Two **independently-authored code
bases** reach for the same *shape* of shim — `issecretvalue or <fallback>` — but
they are not the same shim and only one of the two is a library:

```lua
-- a library
DogTag.issecretvalue = _G.issecretvalue or function() return false end
```
`[T1 obs: TellMeWhen/Lib/LibDogTag-3.0/Helpers.lua:138]`

```lua
-- addon code, not a library
local issecretvalue = issecretvalue or function() end -- XXX 12.0 compat
```
`[T3: BigWigs@3fdc10f6 Tools/AutoInvite.lua:69 — verified directly in the clone]`

Note the fallbacks differ: DogTag's returns `false`, BigWigs' returns `nil`. Both
are falsy so both work as guards, but "the same defensive shim" (an earlier
draft's wording) overstated it, as did calling both of them libraries. **Two
samples is not a pattern** — treat this as two data points showing the idiom
exists, not as an ecosystem convention. oUF guards a GUID comparison directly:
`if(unitGUID ~= nil and not issecretvalue(unitGUID) and unitGUID ~= self.unitGUID) then`
`[T1 obs: EllesmereUIUnitFrames/Libs/oUF/ouf.lua:241]`.

Across the whole live install, **165 Lua files mention `issecretvalue` or
`hasanysecretvalues`** `[T1 obs: grep, 2026-07-23]`, of which the library-path hits
include LibDurability, LibLatency, LibCustomGlow-1.0, LibAdvFlight, oUF,
LibDogTag-3.0 (+ `-Unit-3.0`), and LibRangeCheck-3.0.

**Two library classes that have *not* adapted** and that you should treat as hazards
until proven otherwise: the serializers (§5.2 — AceSerializer, LibSerialize and
LibDeflate contain zero secret references) and **TaintLess**, whose fix set predates
secret values entirely (§9).

---

## 11. Reading mature addons as living documentation

What each is actually worth opening. All Tier 3 — practice, not rules.

| Addon | Commit | Open it for | Caveat |
|---|---|---|---|
| **WeakAuras2** | `38d4bf1e`, 2026-07-20 | The richest `.pkgmeta` dependency census in the ecosystem (25 externals). Sandboxing user-authored Lua (`AuraEnvironment.lua`), import/export + comms (`Transmission.lua`), SavedVariables schema migration (`Modernize.lua`). | Clone contains **no** `Libs/` — every library is an external. Uses Ace3 for the options UI (`AceGUI-3.0`, named in 47 files), plus `AceTimer`, `AceComm` and `AceSerializer`; **not** `AceAddon`. |
| **BigWigs** | `3fdc10f6`, 2026-07-21 | The cleanest module architecture in the set; and the best real Midnight secret-value adaptation, including the `issecretvalue or function() end` compat shim. | Vendors only LibStub / CallbackHandler / LibDataBroker in git; the other 16 are externals. Does **not** use AceAddon. |
| **Details!** | `e14de53c`, 2026-07-21 | Combat-log processing at scale; hand-written `API *.txt` docs; heaviest `AceLocale-3.0` user by far (108 files); the only clone that calls `LibStub("AceAddon-3.0")` in a one-liner worth copying (`boot.lua:9`). | **Zero externals** — 18 libraries committed in-tree (`Libs/` also holds `libs.xml`). Ships its own UI framework (`Libs/DF`). |
| **Plater** | `2b2ff463`, 2026-07-23 | Nameplates, import/export, its own scripting API. | **Shares an author (Tercioo) and the `DF` framework with Details** — Plater externals `libs/DF` straight from `Tercioo/Details-Framework`. The two are *one* data point, not two. |
| **ElvUI** | `f60934a1`, 2026-07-23 | The canonical suite: how a **13-module** UI replacement partitions itself (`ElvUI/Game/Shared/Modules/` — ActionBars, Auras, Bags, Blizzard, Chat, DataBars, DataTexts, Maps, Misc, Nameplates, Skins, Tooltip, UnitFrames); densest secure-template user in the set by a wide margin — 16 files matching `SecureActionButtonTemplate`/`SecureHandler`/`RegisterAttributeDriver`/`SecureUnitButtonTemplate` vs 2 for the next clone `[T3: census 2026-07-23]`. | Vendors 10 library dirs in-tree (including a full 50-file oUF) *and* declares 21 externals. Only **3** of its own non-library files call LibStub. |
| **oUF** | `5672a3cb`, 2026-07-20, 504 KB (excl. `.git`) | **The best single readable example of a zero-dependency library.** No LibStub, no Ace3, no `.pkgmeta` externals. Its `## X-oUF` metadata trick (§1c) is the clearest non-LibStub distribution pattern in the corpus. | `## Notes: Unit frame framework. Does nothing by itself.` — it is a framework for *other* addons, so it shows library authorship, not addon authorship. |
| **Bagnon** | `9f72bd96`, 2026-07-17 | The "split addon" pattern: no `.pkgmeta` at all, no `Libs/`, dependencies satisfied by a sibling addon via `## Dependencies: BagBrother` (`Bagnon.toc:10`) — and cross-addon XML includes (`src/main.xml`: `<Include file="..\..\BagBrother\core\core.xml"/>`). | Uses a compat shim library (`LibStub('C_Everywhere')`, `src/frame.lua:7`) rather than Ace3. `## X-License: All Rights Reserved` (`Bagnon.toc:4`) — readable, not reusable. |

**Counting discipline.** Seven clones is seven data points minus one: Details and
Plater share an author and a framework. When this file says "four of seven", it
means four of these seven, on 2026-07-23, and nothing more.

---

## 12. Gaps

- `[gap]` **No Tier-1 or Tier-2 statement exists that LibStub is the sanctioned
  approach.** It is a 2007 community artefact that the platform neither knows nor
  blesses. Looked in: the full `wow-ui-source` checkout at 12.0.7.68887
  (`grep -ril 'libstub'` over all 3685 files → zero hits, re-run 2026-07-23) and the
  generated API docs under `Blizzard_APIDocumentationGenerated/`. An earlier draft
  also cited "Blizzard's news article 24244638" as a place searched; that reference
  is unverifiable as written and is dropped rather than repeated.
- `[gap]` **The wiki is not a usable library index.**
  `Category:Function Libraries` was last edited **2019-06-08** and has **five
  members**, three of which (Dongle, Sea, LibKarma) are dead
  `[T2 wiki: revid 5355606]`. The real index is the `.pkgmeta` files of active
  addons. There is no maintained ecosystem registry I could find.
- `[gap]` **Adoption numbers are unobtainable from this box.** `addons.wago.io` API
  → 401; `curseforge.com/wow/addons` → 403. Every popularity claim here is a count of
  copies on one install or of `.pkgmeta` references.
- `[gap]` **Whether the deprecated `UIDropDownMenu_*` globals still work for addons
  at 12.0.7.** The file is still loaded and still 1589 lines, but it resolves through
  `GetCurrentEnvironment()` rather than `_G` `[T1 src: UIDropDownMenu.lua:1]`.
  `@verify-ingame`.
- `[gap]` **What actually happens when a secret value reaches AceSerializer /
  LibSerialize / LibDeflate.** Source inspection proves only that none of them tests
  for it. `@verify-ingame`.
- `[gap]` **Inter-addon load order**, hence which of several vendored copies of a
  library wins on a given install, is not established here (see §2.3).
- `[gap]` **LibSharedMedia-3.0 and LibDBIcon-1.0 upstream is CurseForge SVN**, so
  every claim about them rests on packaged copies vendored inside BigWigs on this
  install, not on upstream source.
- `[gap]` **I could not verify Ace3's `tests/` suite runs, or that any library in
  this file has CI.** No test execution was attempted.

---

## Rules we could audit against

1. **`LibStub:NewLibrary` returns `nil` — not a table — when an equal-or-newer minor
   is already registered.** Code of the form `local lib = LibStub:NewLibrary(M, N)`
   that then indexes `lib` without an `if not lib then return end` guard will error on
   any install where another addon shipped the same-or-newer copy.
   *[Tier 1 obs / Tier 3: `BigWigs/Libs/LibStub/LibStub.lua:25` (`if oldminor and
   oldminor >= minor then return nil end`); the guard idiom at
   `Ace3@4475787f CallbackHandler-1.0/CallbackHandler-1.0.lua:5`.]*

2. **`LibStub:GetLibrary(major)` throws unless the second argument is truthy.**
   `LibStub("SomeOptionalLib")` on an install lacking it raises
   `Cannot find a library instance of "…"`; `LibStub("SomeOptionalLib", true)`
   returns `nil`. Any optional-dependency lookup missing the `true` is a bug.
   *[Tier 1 obs / Tier 3: `BigWigs/Libs/LibStub/LibStub.lua:36-41`, error at `:38`.
   Example of the silent form in use — note it is **not** an optional dependency,
   the library just wants to raise its own message: `LibDBIcon-1.0.lua:11-12`
   (`LibStub("LibDataBroker-1.1", true)` then
   `if not ldb then error(DBICON10 .. " requires LibDataBroker-1.1.") end`).]*

3. **A library table handed out by LibStub is reused across upgrades, so any state a
   library keeps must be re-initialised with `or`.** `self.libs[major] or {}` means an
   upgraded library sees the previous minor's table.
   *[Tier 1 obs / Tier 3: `LibStub.lua:26`. The compliant idiom, **five** times in
   five consecutive lines — `DefaultMedia`, `MediaList`, `MediaTable`, `MediaType`,
   `OverrideMedia` — at
   `BigWigs/Libs/LibSharedMedia-3.0/LibSharedMedia-3.0.lua:41-45`, plus
   `lib.callbacks = lib.callbacks or CallbackHandler:New(lib)` at `:39`.]*

4. **A library that changes behaviour between minors and does not gate on `oldminor`
   leaves already-created objects on the old behaviour.** CallbackHandler-1.0
   returns early on upgrade and rebuilds nothing; LibDataBroker-1.1 patches its live
   table under `if oldminor < N` gates. Both patterns exist; only the second
   actually upgrades.
   *[Tier 3: `Ace3 CallbackHandler-1.0.lua:5` vs
   `BigWigs/Libs/LibDataBroker-1.1/LibDataBroker-1.1.lua:5-7, :14, :21, :35`.]*

5. **Multiple minors of the same library ship simultaneously in the wild, and they are
   not behaviourally equivalent.** On this install `CallbackHandler-1.0` is present at
   v6 (1 copy), v7 (3) and v8 (10). **v6** builds per-arity dispatchers with
   `loadstring` and runs handlers under `xpcall`; **v7** drops the `loadstring`
   dispatcher but still runs handlers under `xpcall`; **v8** runs them through
   `securecallfunction`. Any claim of the form "CallbackHandler does X" must name a
   minor.
   *[Tier 1 obs: 14 `CallbackHandler-1.0.lua` files under `_retail_/Interface/AddOns/`,
   minors counted from each file's `local MAJOR, MINOR = "CallbackHandler-1.0", N`
   line (2026-07-23). Tier 1 obs / Tier 3 for the dispatch difference:
   `Simulationcraft/libs/…:25-57` (`CreateDispatcher` :25, `loadstring` :51),
   `RaiderIO/libs/…:25-32` (plain `xpcall` loop),
   `Ace3@4475787f …:15-22` (`securecallfunction` at :19).
   **A previous version of this rule claimed v7 used `loadstring`. It does not** —
   it only upvalues `loadstring` at `:11` without ever calling it.]*

6. **A library shipped inside another addon's folder never has its `.toc` parsed, so
   that `.toc`'s `## Interface:` is not a compatibility signal.**
   `EllesmereUI/Libs/LibDeflate/LibDeflate.toc` says `## Interface: 80300` on a 12.0.7
   install and the addon works. There are **38** such never-parsed `.toc` files on
   this install.
   *[Tier 1 obs: that file, line 1; `find … -mindepth 3 -name '*.toc'` → 38.
   Tier 2 for the placement rule: wiki `TOC format`, revid 6767089, 2026-07-09,
   wikitext lines 2 and 5 — *"The filename of the `.toc` file must match the folder
   it's inside, otherwise the `.toc` file won't load"*, with the example
   `..\Interface\AddOns\MyAddon\MyAddon.toc`. Flavour-suffixed variants of that same
   basename (`MyAddon_Mainline.toc`) also load — wikitext line 180.]*

7. **An addon's git repository is not a reliable inventory of its dependencies in
   either direction.** WeakAuras2 has zero library directories in git and **25**
   `.pkgmeta` externals; Details! has **18** library directories in git and zero
   externals. Read `.pkgmeta` *and* the tree.
   *[Tier 3: `WeakAuras2@38d4bf1e .pkgmeta` (25 external targets, no `Libs/` dir);
   `details@e14de53c .pkgmeta` (no `externals:` key) with `details/Libs/` holding 19
   entries, one of which is the file `libs.xml` → 18 library directories.
   An earlier version of this rule said "27" and "nineteen"; both were wrong, and
   "27" also contradicted its own citation.]*

8. **`AceAddon:EmbedLibrary` errors — it does not skip — on a library that lacks a
   `:Embed` method.** So `MyAddon = AceAddon:NewAddon("X", "SomeLib")` only works if
   `SomeLib.Embed` is a function.
   *[Tier 3: `Ace3@4475787f AceAddon-3.0/AceAddon-3.0.lua:182-193`, error string
   `"Library '%s' is not Embed capable"` at `:191`.]*

9. **AceAddon drains its init and enable queues from one handler bound to both
    `ADDON_LOADED` and `PLAYER_LOGIN`, and it deliberately ignores `ADDON_LOADED`
    for six named Blizzard early-load addons.** Precisely: on either event the
    handler drains `initializequeue` (calling `OnInitialize` via
    `AceAddon:InitializeAddon`); then, **only if `IsLoggedIn()` is already true**,
    it drains `enablequeue` (calling `OnEnable` via `AceAddon:EnableAddon`). So
    before login `OnInitialize` fires and `OnEnable` waits for `PLAYER_LOGIN`;
    after login (load-on-demand addons) both fire in the same handler pass. Code
    that assumes a fixed gap between the two is wrong in one direction or the other.
    *[Tier 3: `Ace3@4475787f AceAddon-3.0/AceAddon-3.0.lua:600-608` (the
    `BlizzardEarlyLoadAddons` table — `Blizzard_DebugTools`, `Blizzard_TimeManager`,
    `Blizzard_BattlefieldMap`, `Blizzard_MapCanvas`,
    `Blizzard_SharedMapDataProviders`, `Blizzard_CombatLog`), `:611-630` (the
    `onEvent` handler; the combined event test at `:613`, the `IsLoggedIn()` gate at
    `:623`), `:632-634` (two `RegisterEvent` calls + `SetScript`), `:493`
    (`InitializeAddon`), `:516` (`EnableAddon`).
    An earlier version of this rule added "or that either fires for a demand-loaded
    Blizzard addon" — that clause was confused and is removed: the six named addons
    are Blizzard's, not Ace addons, and the exclusion only stops the queue from
    being drained *at the moment they load*.]*

10. **AceTimer-3.0 clamps every delay to a floor of 0.01 s.** `self:ScheduleTimer(f, 0)`
    fires no sooner than 10 ms. The looping re-arm path clamps too.
    *[Tier 3: `Ace3@4475787f AceTimer-3.0/AceTimer-3.0.lua:33-35` — `if delay < 0.01
    then` / `delay = 0.01 -- Restrict to the lowest time that the C_Timer API allows
    us` / `end` (an earlier draft cited only `:34`, which is the assignment, not the
    test); the same clamp on re-arm at `:66`; the `C_TimerAfter` calls at `:67` and
    `:75`; the upvalue `local GetTime, C_TimerAfter = GetTime, C_Timer.After` at
    `:30`. Tier 1 for the underlying API: `UITimerDocumentation.lua:11`.]*

11. **AceSerializer-3.0 errors on any value that is not string / number / table /
    boolean / nil.** There is no fall-through and no secret-value branch.
    *[Tier 3: `Ace3 AceSerializer-3.0/AceSerializer-3.0.lua:54` (`SerializeValue`),
    `:56` (`local t=type(v)`), the branch chain at `:58`/`:63`/`:83`/`:93`/`:101`,
    and the `else` at **`:106`**
    (`error(MAJOR..": Cannot serialize a value of type '"..t.."'")`). An earlier
    draft cited `:104`.
    Corroboration that the alternatives are equally unaware: zero matches for
    `issecretvalue`/`secret` in `libs/LibSerialize/LibSerialize.lua` and
    `libs/LibDeflate/LibDeflate.lua`.]*

12. **AceComm-3.0 chunks at 255 bytes and prefixes each chunk with `\001`/`\002`/`\003`.**
    A receiver that reads `CHAT_MSG_ADDON` directly, without AceComm on its side, will
    see those control bytes and truncated payloads.
    *[Tier 3: `Ace3 AceComm-3.0/AceComm-3.0.lua:41-43` and `:95` (`local maxtextlen = 255`
    with the comment "Yes, the max is 255 even if the dev post said 256. I tested.").]*

13. **AceLocale-3.0 returns the missing key as its own value and raises a non-fatal
    error through `geterrorhandler()`, unless the locale was registered `silent`.** So
    a missing translation shows the key on screen *and* produces an error report.
    *[Tier 3: `Ace3 AceLocale-3.0/AceLocale-3.0.lua:24-30` (loud) and `:33-38`
    (silent variant).]*

14. **`LibSharedMedia-3.0:Register` returns `false` instead of erroring when the key
    already exists, so first registration wins and a later registration of the same
    key is silently a no-op.** Code that ignores the return value cannot tell whether
    its media was installed.
    *[Tier 1 obs / Tier 3: `BigWigs/Libs/LibSharedMedia-3.0/LibSharedMedia-3.0.lua` —
    `function lib:Register` at `:239`; the duplicate-key early-out at `:265-268`
    (`if mtable[key] then` / `-- key already registered` / `return false` / `end`);
    against the `error()` calls for bad argument types at `:241` and `:244`.]*

15. **`LibSharedMedia-3.0:Register` also returns `false` for a path outside
    `interface`, and for a sound that is not `.ogg` or `.mp3`.** Both checks apply
    only when `data` is a string and the type is background/border/statusbar/sound.
    *[Tier 1 obs / Tier 3: same file, `:252-256` (`if not path:find("^interface")` —
    comment "files accessed via path only allowed from interface folder" at `:254`)
    and `:258-260` (comment "only ogg and mp3 are valid sounds" at `:258`), inside
    the `type(data) == "string"` guard opened at `:252`.]*

16. **A font registered with LibSharedMedia and no `langmask` is dropped on
    non-western clients.** `:Register` returns `false` before storing it.
    *[Tier 1 obs / Tier 3: same file, `:247-250` — `if mediatype ==
    lib.MediaType.FONT and ((langmask and band(langmask, LOCALE_MASK) == 0) or not
    (langmask or locale_is_western)) then … return false` — against the locale-bit
    constants at `:31-35`.]*

17. **`LibDataBroker-1.1` hard-requires both LibStub and CallbackHandler-1.0 at file
    scope, via two bare `assert(...)` calls before anything else runs.** An addon
    that embeds LDB without also embedding CallbackHandler gets a Lua error and no
    LDB. (Scope note: an error at file scope aborts *that file*; the rest of the
    addon's files still load. "The addon fails to load" — an earlier draft's
    wording — is too strong.)
    *[Tier 1 obs / Tier 3: `BigWigs/Libs/LibDataBroker-1.1/LibDataBroker-1.1.lua:2-3`
    — `assert(LibStub, "LibDataBroker-1.1 requires LibStub")` and
    `assert(LibStub:GetLibrary("CallbackHandler-1.0", true), "LibDataBroker-1.1
    requires CallbackHandler-1.0")`.]*

18. **Every write to an LDB data object fires four callbacks, not one** —
    `LibDataBroker_AttributeChanged`, `…_<name>`, `…_<name>_<key>`, `…__<key>` — and
    a write of an unchanged value fires none.
    *[Tier 1 obs / Tier 3: same file, the four `callbacks:Fire` calls at `:28-31`; the
    early-out is `if attributestorage[self][key] == value then return end` at `:24`.]*

19. **`UIDropDownMenu` is deprecated at Blizzard's own word, with no shims provided,
    while still shipping.** Any addon still calling it is on a path Blizzard has
    declared replaced; `Blizzard_Menu` / `MenuUtil` is the replacement.
    *[Tier 1: `Blizzard_Menu/11_0_0_MenuImplementationGuide.lua:4-7` for the statement;
    `Blizzard_SharedXML/Blizzard_SharedXML_Mainline.toc:212-215` for the fact it still
    loads; `Blizzard_Menu/MenuUtil.lua:151, :335, :354, :373` for the replacement API.]*

20. **A minimap-button library is not required to appear in the addon compartment —
    a `.toc` metadata line is enough.** Blizzard reads `AddonCompartmentFunc`
    (and `AddonCompartmentFuncOnEnter` / `…OnLeave`) via `C_AddOns.GetAddOnMetadata`
    and registers the addon itself.
    *[Tier 1: `Blizzard_Minimap/Mainline/AddonCompartment.lua:81, :106, :113, :136`;
    `C_AddOns.GetAddOnMetadata` at `AddOnsDocumentation.lua:165`.]*

21. **Arbitrary `X-`-prefixed `.toc` metadata is readable at runtime and is a working
    alternative to LibStub for library self-identification.** oUF resolves its global
    name from `## X-oUF` at load and refuses to install over an existing global.
    *[Tier 3 for the usage: `oUF@5672a3cb ouf.lua:2`
    (`local global = C_AddOns.GetAddOnMetadata(parent, 'X-oUF')`) and `:1026-1034`
    (the `if(global) then` collision block, `_G[global] = oUF` at `:1032`),
    `oUF.toc:7` (`## X-oUF: oUF`).
    Tier 2 for the mechanism: wiki `TOC format`, revid 6767089, 2026-07-09,
    wikitext line **376** — "X-_____: Any custom metadata prefixed by 'X-', such as
    'X-Date', 'X-Website' or 'X-Feedback'". Tier 1 for the reader:
    `Blizzard_APIDocumentationGenerated/AddOnsDocumentation.lua:165`
    (`Name = "GetAddOnMetadata"`).]*

22. **Not every library uses LibStub, so `LibStub("X")` is not a general availability
    test.** ChatThrottleLib gates on `_G.ChatThrottleLib.version` and publishes itself
    as a plain global.
    *[Tier 3: `Ace3@4475787f AceComm-3.0/ChatThrottleLib.lua:26, :31, :54`.]*

23. **`TaintLess` as shipped predates Midnight, so nothing in it was written for
    secret values.** Its last commit in the clone is 2025-02-26 and it self-versions
    `[24-07-27]`, both before 12.0.0 (2026-01-20). Its continued presence in WeakAuras'
    and ElvUI's `.pkgmeta` is evidence it is *shipped*, not that it is *current*.
    (Stated as "predates", not "cannot address" — pre-existing fixes may still be
    correct; what the dates rule out is that it was written with secret values in
    mind.)
    *[Tier 3: `raw/addon-research/libs/TaintLess@a4f3eda90db1`, whose single file
    `TaintLess.xml` opens `TaintLess [24-07-27]`; `.pkgmeta` entries in
    `WeakAuras2@38d4bf1e` (`url: https://www.townlong-yak.com/addons.git/taintless`,
    `commit: default`) and `ElvUI@f60934a1`. Tier 1 for the patch date:
    this repo's `knowledge/_meta/game-version.md`.]*

24. **`LibCompress` on this install is at SVN revision 83, dated 2018-07-03, and
    LibDeflate's own published benchmark claims it beats LibCompress on size at
    equal speed.** New code adopting LibCompress is adopting a legacy path.
    *[Tier 1 obs: `MythicDungeonTools/libs/LibCompress/LibCompress.lua:7-9`, version
    expression at `:13` —
    `LibStub:NewLibrary("LibCompress", 90000 + tonumber(("$Revision: 83 $"):match("%d+")))`.
    Tier 3, and note it is the *competitor's own* benchmark:
    `libs/LibDeflate/README.md:127` — "LibDeflate with compression level 1 compresses
    as fast as LibCompress, but already produces significantly smaller data than
    LibCompress." No independent measurement was made for this file.]*

25. **`LibDeflate`'s 2021 `pushed_at` is not evidence of abandonment.** It is an
    external in **two** of the seven surveyed addons' `.pkgmeta` in 2026
    (WeakAuras2, Plater), vendored in-tree by **two** more (ElvUI, Details!), and
    present on this install.
    *[Tier 2 gh: `SafeteeWoW/LibDeflate` pushed 2021-05-05, archived=false, 117 stars.
    Tier 3: externals lines in `WeakAuras2@38d4bf1e` and `plater@2b2ff463`; in-tree at
    `ElvUI/ElvUI_Libraries/Game/Shared/LibDeflate/` and `details/Libs/LibDeflate/`.
    Tier 1 obs: vendored at `EllesmereUI/Libs/LibDeflate/`.
    An earlier draft listed ElvUI as an external — ElvUI's `.pkgmeta` does not
    mention LibDeflate.]*

26. **A library version taken from WoWInterface may be years behind upstream.**
    Its file list shows Ace3 last updated 2017-09-04; upstream's newest changelog entry
    is 2026-02-03.
    *[Tier 2: `https://api.mmoui.com/v3/game/WOW/filelist.json`, fetched 2026-07-23,
    8134 entries. Tier 3: `Ace3@4475787f changelog.txt:1`.]*

27. **`LibStub` is not a version-drift risk on this install: every copy is minor 2.**
    All 23 copies declare `local LIBSTUB_MAJOR, LIBSTUB_MINOR = "LibStub", 2`. They
    are 7 distinct byte sequences reducing to 2 distinct programs, differing only in
    `strmatch` (21 copies) vs `string.match` (2 copies) — aliases of the same
    function — so behaviour is identical regardless of which copy wins.
    *[Tier 1 obs: `find … -name LibStub.lua` over `_retail_/Interface/AddOns/`, md5
    over raw bytes and over comment/whitespace-stripped text, 2026-07-23. An earlier
    draft said "three byte-level variants … the same program"; corrected here.
    **Scope:** "every copy in the wild" was never shown — this is one install of 81
    addons.]*

28. **The string `LibStub` appears nowhere in Blizzard's shipped UI source**, so no
    claim that the client "knows about" or "supports" LibStub can be true.
    *[Tier 1: `grep -ril 'libstub'` over the whole `wow-ui-source` checkout at
    12.0.7.68887, commit `4383ced30106` — zero hits.]*
