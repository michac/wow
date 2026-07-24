---
title: Addon anatomy and the runtime environment
patch: 12.0.7
fetched: 2026-07-23
reviewed: 2026-07-23
sources:
  - https://github.com/Gethe/wow-ui-source (live, version.txt 12.0.7.68887, commit 4383ced30106d51b27e3e86d1987f1552f0d259d)
  - https://warcraft.wiki.gg/wiki/TOC_format (revid 6767089, 2026-07-09)
  - https://warcraft.wiki.gg/wiki/AddOn_loading_process (revid 6302251, 2025-04-23)
  - https://warcraft.wiki.gg/wiki/Using_the_AddOn_namespace (revid 6474636, 2025-09-16)
  - https://warcraft.wiki.gg/wiki/Lua_functions (revid 6779934, 2026-07-23)
  - https://warcraft.wiki.gg/wiki/ADDON_LOADED (revid 6590223, 2026-01-03)
  - https://warcraft.wiki.gg/wiki/PLAYER_LOGIN (revid 6589506, 2026-01-03)
  - https://warcraft.wiki.gg/wiki/PLAYER_ENTERING_WORLD (revid 6590943, 2026-01-03)
  - https://warcraft.wiki.gg/wiki/VARIABLES_LOADED (revid 6589741, 2026-01-03)
  - https://warcraft.wiki.gg/wiki/MACRO_reload (revid 2436052, 2020-12-23 — stale)
  - https://warcraft.wiki.gg/wiki/API_date (revid 3016063, 2022-07-21 — stale)
  - Live install /mnt/c/Program Files (x86)/World of Warcraft/_retail_/ (81 addon folders, 147 top-level .toc files, 38 nested .toc files, 26 client-written AddOns.txt)
  - https://github.com/Ketho/BlizzardInterfaceResources (commit 774b2c550366, build 12.0.7.68256)
confidence: high
---

# Addon anatomy and the runtime environment

**Scope.** What an addon physically *is*, how the client finds and loads it, what
happens between the loading screen and your first frame, and what kind of Lua
machine your code lands in. Cross-file code organisation is the
`module-architecture` topic; taint and secret values are `security-taint-and-restricted-data`.

## Citation conventions used in this file

| Prefix | Means |
|---|---|
| `[T1 src]` | Blizzard's shipped UI source. Paths are relative to the `wow-ui-source` checkout root, i.e. prefix `raw/addon-research/wow-ui-source/`. Build **12.0.7.68887**, commit `4383ced30106`. |
| `[T1 docs]` | `Interface/AddOns/Blizzard_APIDocumentationGenerated/…` in the same checkout — Blizzard's machine-generated API spec. |
| `[T1 obs]` | Directly observed on the live install at `/mnt/c/Program Files (x86)/World of Warcraft/_retail_/`. Observation of shipped artefacts, not of a spec. |
| `[T2 wiki]` | warcraft.wiki.gg, with revision id and last-edit date. Community-written; stamp is load-bearing because pages rot silently. |
| `[T2 res]` | `Ketho/BlizzardInterfaceResources` — a derived per-build dump. **Build 12.0.7.68256**, a *different build of the same patch* than the source checkout. |
| `[T3]` | A named community addon at a named commit. A data point, never a rule. |

> ⚠ **Build skew.** This repo's `knowledge/_meta/game-version.md` records live as
> `12.0.7.68453`; the source checkout is `12.0.7.68887`; `BlizzardInterfaceResources`
> is `12.0.7.68256`. Same patch, three builds. Nothing in this file has been run in
> the client — items that need that are marked `@verify-ingame`.

> ✅ **Adversarial verification pass, 2026-07-23.** Every locator in this file was
> re-opened independently: 346 shipped tocs + 147 installed tocs re-censused, every
> cited `.lua`/`.xml`/`.xsd`/`.toc` line re-read, all ten wiki pages re-fetched at
> the stated revids, all seven Tier-3 checkouts re-counted. The overwhelming
> majority reproduced exactly. Nine claims were corrected; each correction is marked
> inline with **"corrected from the draft"** so the delta is auditable. The two that
> mattered most: the `acos`/`asin`/`atan`/`atan2` direction in §5.3 / rule 11, and
> the `AddOns.txt` argument in §1 / rule 19b.

---

## 1. What an addon is

An addon is **a folder under `Interface/AddOns/` containing a `.toc` manifest of the
same name, plus the Lua/XML files that manifest lists.** There is no binary, no
registration step, and no installer contract — the client enumerates the directory.

On the live install the layout is:

```
_retail_/
  Interface/AddOns/<AddonName>/<AddonName>.toc     ← the only thing under Interface/
  WTF/Config.wtf
  WTF/SavedVariables/
  WTF/Account/<ACCOUNT>/…                          ← per-account & per-character SVs
  Errors/                                          ← Lua error dumps
  Logs/  Cache/  Fonts/  Screenshots/
```
`[T1 obs]` — `_retail_/Interface/` contains exactly one entry, `AddOns`; `_retail_/WTF/`
contains `Account`, `Config.wtf`, `SavedVariables`; `_retail_/Errors/` held one
`2026-05-21_13.01.49_Error_33292.txt`.

**Blizzard's own 317 `Blizzard_*` addons are not on disk here.** The live install's
`Interface/AddOns/` holds 81 directories and **zero** whose name begins with
`Blizzard_` `[T1 obs]`; the 317 are visible only in the extracted `wow-ui-source`
mirror `[T1 src: Interface/AddOns/, 317 dirs]`. (They ship inside the client's
packaged data rather than as loose files — `[gap]` I did not verify the container
format; townlong-yak hosts a CASC browser, which is Tier 2 and not something I
checked against this install.) So **you cannot
enumerate addons by scanning the folder** — use `C_AddOns.GetNumAddOns()` /
`C_AddOns.GetAddOnName(i)` `[T1 docs: AddOnsDocumentation.lua:256, :181]`.

### Manifest placement is exact

On this install **147 of 147** top-level `.toc` files sit at
`Interface/AddOns/<Folder>/<Folder>[_Suffix].toc`, with `_Suffix` drawn from the
recognised flavour list; zero mismatches `[T1 obs]`. The wiki states the rule
outright: *"The filename of the `.toc` file must match the folder it's inside,
otherwise the `.toc` file won't load."* `[T2 wiki: TOC format, revid 6767089,
2026-07-09]`.

A further **38** `.toc` files exist *nested* deeper (e.g.
`Bartender4/libs/LibStub/LibStub.toc`, `EllesmereUI/Libs/LibDeflate/LibDeflate.toc`)
`[T1 obs]`. These are vestigial manifests belonging to embedded libraries.

**The client's own per-character list is suggestive but not decisive.** The client
writes a per-character `WTF/Account/<ACCOUNT>/<Realm>/<Char>/AddOns.txt` of
`<AddonName>: enabled|disabled` — 26 such files on this install, newest written
**2026-07-23 17:26** with 78 entries (49 `enabled`, 29 `disabled`) `[T1 obs]`.

> ⚠ **Corrected from the draft: the 26 files do NOT carry an identical name set.**
> Re-counted: sizes are 78 (×1), 71 (×21), 70 (×2) and **3 (×2)**; the union is 78
> names but the *intersection is only 3* `[T1 obs, set arithmetic over all 26
> files]`. Each file is per-character state, evidently written as of that
> character's last session — the 71-entry files all lack the same 7 recently-added
> addons. Only the single newest file spans the full union.

**No nested library that has its own `.toc` appears in any of the 26** — no
`LibStub`, `LibDeflate`, `LibSharedMedia-3.0` `[T1 obs]`. (The draft also listed
`CallbackHandler-1.0` and `LibDBIcon-1.0`; **corrected** — those ship as nested
*folders* with no `.toc` at all, e.g. `Bartender4/libs/LibDBIcon-1.0/`, so their
absence proves nothing about nested manifests.)

> `[gap]` **This is weaker evidence than the draft claimed.** The draft argued
> "disabled addons are still listed, therefore absence ⇒ never enumerated". That
> inference does not survive the next paragraph: **8 well-formed, top-level addon
> folders are also absent** from the newest file. So absence from `AddOns.txt` is
> demonstrably *not* proof that the client never enumerated a name. What the
> observation supports is only the weaker statement: *no nested-`.toc` library has
> ever been observed in a client-written addon list on this install.* The rule in
> §19b rests on the wiki's folder-name requirement, not on this.
> `@verify-ingame`: `C_AddOns.DoesAddOnExist("LibStub")` is the decisive test.

Two more things fall out of the same file, and both cut against naive assumptions:

- It lists **three `Blizzard_*` names with no folder on disk** —
  `Blizzard_ObjectiveTracker`, `Blizzard_CompactRaidFrames`, `Blizzard_CombatText`
  `[T1 obs]` — independent confirmation that Blizzard addons are enumerable but
  not present as files (§ rule 19).
- It is **not** a mirror of the folder set: the union over all 26 retains 2 names
  whose folders are gone (`BetterCooldownManager`, `OPie_Classic`) and omits 8
  folders that are present with well-formed tocs (`RaiderIO`,
  `RaiderIO_DB_US_{F,M,R}`, `TellMeWhen_Options`, `EllesmereUIDataBars`,
  `Bartender4ModernGlowEffects`, `Bartender4 Animations`) `[T1 obs]`. Note the
  other 12 `RaiderIO_DB_*` region packs (CN/EU/KR/TW) *are* listed — only the US
  three and the `RaiderIO` core are missing.

> `[gap]` **Why those 8 are omitted is unresolved.** Re-checked independently and
> no pattern holds: the set mixes `LoadOnDemand: 1` (TellMeWhen_Options) with
> non-LoD, mixes has-`Dependencies` with none, mixes current `## Interface: 120007`
> (RaiderIO, EllesmereUIDataBars) with out-of-date `120000`
> (Bartender4ModernGlowEffects), and every folder on the install shares the same
> 13:36–13:38 mtime band, so mtime cannot separate them either. The most likely
> mundane explanation — *installed after the character last logged in* — is
> consistent with the per-character size variance above but is **not established**.
> Do **not** treat `AddOns.txt` as the authoritative installed-addon list.
> `@verify-ingame`: `C_AddOns.DoesAddOnExist("LibStub")` and
> `C_AddOns.DoesAddOnExist("RaiderIO")` would settle both halves of this.

Blizzard's own corpus does **not** obey the folder-name rule: 2 of 346 shipped
`.toc` files mismatch their directory (`Blizzard_BarbershopUI/Blizzard_BarberShopUI.toc`,
`Blizzard_EndOfMatchUI/Blizzard_EndMatchUI.toc`) `[T1 src]`. The checkout also
carries an explicit manifest listing all 346 toc paths,
`Interface/ui-toc-list.txt` `[T1 src, 346 lines, backslash-separated paths]` —
consistent with Blizzard's addons being discovered from a list rather than by the
folder-name convention. `[gap]` That the *client* uses that file is inference; I
found no statement of it. Either way: **do not infer addon-facing rules from the
shipped corpus.**

---

## 2. The `.toc` manifest

### 2.1 Syntax

Three line kinds `[T2 wiki: TOC format, 2026-07-09]`:

```wowtoc
## Directive: Value      # metadata
# a comment
Path\To\File.lua         # a file to load, in order
```

- Values are whitespace-trimmed after the colon; leading whitespace before `#`
  makes the line a *filename*, not a comment.
- Backslashes are recommended over forward slashes.
- The client reads only the first **1024 characters** of each line; the rest is
  silently ignored. `[T2 wiki only — I found no Tier 1 statement of this limit.]`

**Only `.lua` and `.xml` appear as file entries.** Across the 346 shipped tocs:
2380 file entries end in `.lua` and 1299 in `.xml`, and nothing else `[T1 src]`.
Across the 147 third-party tocs on this install: 1482 `.lua`, 183 `.xml`, nothing
else `[T1 obs]`. (Entry counts exceed on-disk file counts — 2298 `.lua` files in the
checkout — because flavour-specific tocs list the same files.) Media (`.tga`,
`.blp`, `.ogg`) lives in the folder and is referenced by *path at runtime*, e.g.
`## IconTexture: Interface\AddOns\BigWigs\Media\Icons\minimap_raid.tga`
`[T1 obs: BigWigs/BigWigs.toc]`, never listed as a load entry.

### 2.2 The addon-facing directive set

This is the set the wiki documents as usable by third-party addons, annotated with
**how many directive lines occur across the 147 third-party `.toc` files on this
install** (a line count, not a file count — the non-localised forms are one per toc
in practice) `[T1 obs]`. Definitions are
`[T2 wiki: TOC format, revid 6767089, 2026-07-09]` unless a Tier-1 locator is given.

| Directive | Lines on this install | Meaning |
|---|---|---|
| `Title` | 147 | Name in the AddOns list. Localise with `Title-deDE` etc.; later entries win, so the bare fallback goes first. |
| `Interface` | 147 | Client interface version(s). Comma-delimited list allowed (10.2.7+). |
| `IconTexture` | 141 | Texture path for the list icon. |
| `Version` | 120 | Free-form; readable via `GetAddOnMetadata`. |
| `Dependencies` | 109 | Hard deps — must load first. Aliases: `RequiredDeps`, and **any word starting with `Dep`** (Blizzard's own tocs use `## Dep:` 68× and `## RequiredDep:` 30× `[T1 src]`). |
| `Author` | 109 | Informational. |
| `Notes` | 74 | Tooltip text. Localisable. |
| `SavedVariables` | 55 | Account-wide persisted globals. |
| `LoadOnDemand` | 46 | `1` ⇒ don't load at login; wait for `C_AddOns.LoadAddOn()`. ⚠ 46 is the **line** count; 45 are `: 1` and 1 is `: 0` (§4.3). |
| `DefaultState` | 45 | `disabled` ⇒ user must enable explicitly. |
| `OptionalDeps` | 24 | Load first *if present*; absence is not an error. |
| `Category` | 21 | Collapsible header in the AddOns list. Localisable. |
| `Group` | 18 | Indented sub-list under a parent addon. |
| `SavedVariablesPerCharacter` | 10 | Per-character persisted globals. |
| `LoadSavedVariablesFirst` | 7 | `1` ⇒ SVs load *before* the addon's files instead of after (added 11.1.5). |
| `License` | 8 | Informational. |
| `AddonCompartmentFunc` | 4 | **Global** function name invoked from the minimap addon-compartment dropdown. |
| `AddonCompartmentFuncOnEnter` / `…OnLeave` | 3 / 3 | Hover callbacks, same global-name resolution. |
| `AllowAddOnTableAccess` | 1 | `1` ⇒ other addons may fetch your namespace table via `C_AddOns.GetAddOnLocalTable` `[T1 docs: AddOnsDocumentation.lua:149]`. |
| `LoadWith` | 1 | Load me when *that* addon loads. Implies LoadOnDemand. |
| `X-*` | many | Arbitrary custom metadata, readable via `GetAddOnMetadata`. The install shows `X-Website` 58, `X-Category` 50, `X-Curse-Project-ID` 30, `X-Wago-ID` 30, `X-WoWI-ID` 22, plus addon-private ones like `X-BigWigs-LoadOn-InstanceId` 32. |

Documented but **unused on this install** (0 of 147): `LoadManagers`,
`OnlyBetaAndPTR`, `IconAtlas`, `AllowLoadGameType` as a *metadata* directive
`[T1 obs]`.

`GetAddOnMetadata(name, variable)` is the runtime reader for `Author`, `Version`
and any `X-*` field `[T1 docs: AddOnsDocumentation.lua:165]`. Blizzard's own
minimap code reads `AddonCompartmentFunc`, `IconTexture`, `IconAtlas`,
`AddonCompartmentFuncOnEnter`, `AddonCompartmentFuncOnLeave` through it
`[T1 src: Blizzard_Minimap/Mainline/AddonCompartment.lua:81, 86, 106, 113]`.

**The compartment callback must be a true global.** Blizzard resolves it as
`_G[addonCompartmentFunc](addonName, ...)` `[T1 src: AddonCompartment.lua:99]`.
A file-local or namespace-table function will not be found.

### 2.3 Restricted directives — do not use them

The wiki's `== Restricted ==` section — *"The following tags are inaccessible to
third-party AddOns"* — contains exactly five: `AllowLoad`,
`EscalateErrorDuringLoad`, `LoadFirst`, `SavedVariablesMachine`,
`UseSecureEnvironment` `[T2 wiki: TOC format §Restricted, revid 6767089,
2026-07-09]`.

**`Secure` is not one of them.** It appears on that page only as a patch-change
note (*"Patch 1.11.0 — Added the `Secure` metadata field"*) with no section of its
own and no restricted marking `[T2 wiki: TOC format §Patch changes]`, yet it is
live in the shipped corpus on 5 tocs `[T1 src]` and used by 0 of 147 third-party
tocs `[T1 obs]`. Treat it as Blizzard-internal by inference, not by citation.

Corroboration is clean in both directions:

- Shipped Blizzard tocs use them heavily — `AllowLoad` 177, `LoadFirst` 19,
  `UseSecureEnvironment` 13, `Secure` 5, `SavedVariablesMachine` 3,
  `EscalateErrorDuringLoad` 3 `[T1 src, per-line counts over 346 tocs]`.
- **Zero of the 147 third-party tocs on this install use any of them** `[T1 obs]`.

`UseSecureEnvironment: 1` means *"all files present in an addon should be loaded
into a private function environment"* `[T2 wiki]`. It appears on 13 Blizzard addons
— `Blizzard_PrivateAurasUI`, `Blizzard_CombatLogProcessor`, `Blizzard_StoreUI`,
`Blizzard_CatalogShop`, `Blizzard_SecureTransferUI`, `Blizzard_PingUI` and others
`[T1 src]`. Its existence as an opt-in is the clearest indication that the
**default is the shared global environment** (§5).

Also present in the shipped corpus but **absent from the wiki's directive list
entirely** — treat as Blizzard-internal and unusable:

| Seen | Where `[T1 src]` |
|---|---|
| `## ShowInAddOnList: 0` | `Blizzard_PerksProgram/Blizzard_PerksProgram.toc:3` |
| `## ShowInDebugList: 1` | `Blizzard_EventTrace/Blizzard_EventTrace.toc:4` |
| `## SuppressLocalTableRef: 1` | `Blizzard_RecruitAFriend/Blizzard_RecruitAFriend.toc:5` — the wiki says this was **removed in 11.0.0**, yet it is still in the 12.0.7 corpus. |

### 2.4 Per-line conditionals and variables

Conditions attach to a metadata line or a file line, in square brackets
`[T2 wiki: TOC format, 2026-07-09]`:

| Condition | Since | Note |
|---|---|---|
| `[AllowLoad …]` | (no version given) | Restricts to in-game vs glue screen. The wiki calls it *"functionally inoperable for addons, as only Blizzard code works in the glue screen environment."* Note this is a **condition**, distinct from the restricted `## AllowLoad:` **directive**. |
| `[AllowLoadGameType a, b]` | files 11.1.5 · **metadata 12.0.7** | Patch 11.1.5 also made `AllowLoadGameType` *"usable by insecure addons"*. |
| `[AllowLoadTextLocale enUS, frFR]` | files 11.2.0.61787 · **metadata 12.0.7** | Locale codes as returned by `GetLocale()`. |

The wiki also warns that although *"conditions can appear anywhere in a file
reference line"*, for compatibility they *"should generally only ever be used at
the end of a line"* `[T2 wiki: TOC format, revid 6767089]`.

Variables expand inside file paths: `[Family]` → `Mainline`/`Classic` (11.1.5),
`[Game]` → `Standard`/`Vanilla`/`TBC`/`Wrath`/`Cata`/`Mists`/`WoWLabs`/`WoWHack`
(11.1.5), `[TextLocale]` → `enUS`/`deDE`/… (11.2.0.61787).

Both features are live in the shipped corpus — across 346 tocs the bracketed
conditionals are `[AllowLoadGameType]` 228, `[AllowLoadEnvironment]` 39,
`[AllowLoad]` 36, `[ExcludeLoadGameType]` 3, `[LoadIntoEnvironment]` 2
`[T1 src]`. The 12.0.7 *metadata* conditional is visible at
`Blizzard_CatalogShop/Blizzard_CatalogShop.toc:6-7`:

```
## Dep: Blizzard_UIParent [AllowLoad game]
## Dep: Blizzard_GlueParent [AllowLoad glue]
```
`[T1 src]`

**Three bracketed conditionals in the shipped corpus are undocumented by the wiki**:
`[AllowLoadEnvironment Global]` (39 uses across 8 tocs — 22 of them in
`Blizzard_EditMode/Blizzard_EditMode.toc:3-24`, the rest in
`Blizzard_ScriptErrors/Blizzard_ScriptErrors.toc:6`, `Blizzard_ObjectiveTracker`,
`Blizzard_CUFProfiles`, `Blizzard_CooldownViewer`, `Blizzard_SharedXML` ×2,
`Blizzard_UIParentPanelManager`),
`[LoadIntoEnvironment secure]`
(`Blizzard_ChatFrameBase/Blizzard_ChatFrameBase_Mainline.toc:18`,
`Blizzard_RestrictedAddOnEnvironment/Blizzard_RestrictedAddOnEnvironment.toc:7`),
and `[ExcludeLoadGameType vanilla]`
(`Blizzard_Minimap/Blizzard_Minimap_Classic.toc:17-18`,
`Blizzard_SharedXMLGame/Blizzard_SharedXMLGame.toc:9`) `[T1 src]`.

> `[gap]` I could not establish whether these three are usable by third-party
> addons. Looked in: the wiki `TOC format` page (revid 6767089 — they are not
> mentioned in any section, documented or restricted), and the 147 third-party
> tocs on this install (zero uses). The two `…Environment` ones sit alongside
> `UseSecureEnvironment` semantically, so *assume restricted* until shown otherwise.
> This is a genuine new observation not in the source registry.

A real third-party example of the documented features, `[T1 obs: BigWigs/BigWigs.toc]`
(BigWigs v419.1 as shipped on this install):

```wowtoc
## Interface: 120100, 120005, 120007
## LoadSavedVariablesFirst: 1
Locales\[TextLocale].lua [AllowLoadTextLocale deDE, esES, esMX, frFR, itIT, koKR, ptBR, ruRU, zhCN, zhTW]
```

### 2.5 The `Interface` version

`## Interface: 120007` is 12.0.7 — `major*10000 + minor*100 + patch`
`[T2 wiki: TOC format]`, corroborated by `[T1 obs: TomTom/TomTom.toc:1]`
(`## Interface: 120007`) at live patch 12.0.7. The authoritative runtime read is
the 4th return of `GetBuildInfo()`
`[T1 docs: BuildDocumentation.lua:10 → buildVersion, buildNumber, buildDate,
interfaceVersion, localizedVersion, buildInfo]`.

*"If you don't specify an Interface version, WoW will always treat the addon as out
of date."* `[T2 wiki: TOC format §Interface version, revid 6767089]`. The gate is
real and visible in Tier 1: `AddonList_HasOutOfDate()` scans every addon for
`enabled and not loadable and reason == "INTERFACE_VERSION"`
`[T1 src: Blizzard_AddOnList/AddonList.lua:783]`, `AddonList_DisableOutOfDate()`
disables exactly that set `[:809]`, and the user override is the `ForceLoad`
checkbox — labelled with the global string `ADDON_FORCE_LOAD` = "Load out of date
AddOns" `[T1 src: Blizzard_AddOnList/AddonList.xml:137`; string body at
`T2 res: GlobalStrings/enUS.lua:701]` — whose `OnClick` toggles
`C_AddOns.SetAddonVersionCheck(false/true)` `[T1 src: AddonList.lua:276-285, the
calls at :279 and :282` — the draft cited `:275-278`, which is the `OnShow`
handler, **corrected**`]`.

Comma-delimited multi-flavour lists are normal in the wild — TellMeWhen_Options
ships `## Interface: 120005, 120007, 110205, 50503, 50504, 40402, 20505, 11508`
`[T1 obs: TellMeWhen_Options/TellMeWhen_Options.toc:1]`. Note BigWigs lists
`120100` (12.1.0) first, ahead of live `[T1 obs]`.

Alternatively, ship separate `AddonName_Mainline.toc` / `_Classic` / `_Vanilla` /
`_TBC` / `_Wrath` / `_Cata` / `_Mists` / `_Standard` / `_WoWLabs` / `_WoWHack`
files; the client picks the specific suffix over `_Mainline`/`_Classic`, and falls
back to bare `AddonName.toc` `[T2 wiki: TOC format]`. Legacy `-WOTLKC` and `-BCC`
are still recognised. Both patterns appear on this install (e.g.
`LittleWigs/LittleWigs_Mainline.toc` alongside `LittleWigs_Cata.toc`) `[T1 obs]`.

---

## 3. Loading files inside one addon

Files execute **top to bottom in `.toc` order** `[T2 wiki: AddOn loading process,
revid 6302251, 2025-04-23]`. Not every file need be listed: an XML file may pull in
more work as it is parsed, via `<Script file="…"/>` and `<Include file="…"/>`.
Both elements are Tier-1 schema:

```xml
<xs:element name="Include" substitutionGroup="UiField">   <!-- attribute file, use="required" -->
<xs:element name="Script"  substitutionGroup="UiField">   <!-- attribute file, use="optional" -->
```
`[T1 src: Blizzard_SharedXML/UI.xsd:1168, 1177]`, both children of the root `<Ui>`
element `[T1 src: UI.xsd:1157]`.

Consequence: **a file that is neither listed in the `.toc` nor reached by a
`<Script>`/`<Include>` never executes.** Dead `.lua` files in an addon folder are
inert, not loaded-and-broken.

Paths may reach outside the addon folder. **16 of the 81 installed addons** (26 of
the 147 tocs) load files from a *sibling* addon's directory — the 15 `RaiderIO_DB_*`
data packs and `TellMeWhen_Options`:
`..\TellMeWhen\Options\includes.xml` `[T1 obs: TellMeWhen_Options/TellMeWhen_Options.toc:19]`
and `../RaiderIO/db/db_mythicplus_us_characters.lua`
`[T1 obs: RaiderIO_DB_US_M/RaiderIO_DB_US_M.toc:12]`. Both slash directions occur.
The wiki's TOC page documents neither `..` nor parent-relative paths at revid
6767089, so this is Tier-3 practice by two authors, not a sanctioned feature —
and 16 folders is not 16 independent data points.

By default **SavedVariables load after the last file listed**, unless
`LoadSavedVariablesFirst: 1` flips it `[T2 wiki: AddOn loading process]`. Then
`ADDON_LOADED` fires. (Persistence detail belongs to
`state-persistence-and-communication`.)

---

## 4. Load order, dependencies, and load-on-demand

### 4.1 Order across addons

*"Blizzard's AddOns usually load first (the native UI), followed by custom AddOns
in alphabetical order. However, `.toc` directives can override this behaviour"*
`[T2 wiki: AddOn loading process, revid 6302251, 2025-04-23]`.

> `[gap]` **Alphabetical ordering is Tier 2 only.** I found no Tier-1 statement of
> inter-addon ordering. Looked in: `Blizzard_APIDocumentationGenerated` (the
> `AddOns` system exposes no ordering API — 29 functions, none about order
> `[T1 docs: AddOnsDocumentation.lua:3]`), `Blizzard_AddOnList/AddonList.lua`,
> `Blizzard_SharedXMLBase/AddOnUtil.lua`. The hedge word "usually" is the wiki's
> own. **Do not build on alphabetical order** — use `Dependencies`.

One hard Tier-1 ordering fact: **addons are not loadable while Blizzard's FrameXML
is loading.** Blizzard's own comment:

```lua
-- RegisterAddons cannot be called OnLoad because addons are explicitly not loadable during FrameXML load
```
`[T1 src: Blizzard_Minimap/Mainline/AddonCompartment.lua:71]` — and the code
therefore defers to `PLAYER_ENTERING_WORLD` `[T1 src: AddonCompartment.lua:66, 69-75]`.

### 4.2 Dependencies

`Dependencies` (aliases `RequiredDeps`, `Dep…`) are **hard and transitive**.
Blizzard's own helper resolves them recursively before loading:

```lua
local function GetAddOnDependenciesRecursive(addonName, dependencyArray, dependencyTable)
```
`[T1 src: Blizzard_SharedXMLBase/AddOnUtil.lua:3]`, driven by
`C_AddOns.GetAddOnDependencies(name)` `[T1 docs: AddOnsDocumentation.lua:83]` and
consumed by `AddOnUtil.LoadAddOn` `[T1 src: AddOnUtil.lua:40-52]`.

`OptionalDeps` names *"AddOns that should load first if available"*
`[T2 wiki: TOC format §OptionalDeps, revid 6767089]`. **Corrected from the draft:**
that page does **not** say an absent optional dep is harmless, so "it never blocks
the load" is not a cited claim — it is the natural reading of "if available", and
the shipped corpus offers no counter-example, but treat it as `[unverified]`
until an explicit source or in-game test says otherwise. `@verify-ingame`.

Failure is reported as a **reason token**, not prose.
`C_AddOns.GetAddOnInfo(name)` returns
`name, title, notes, loadable, reason, security`
`[T1 docs: AddOnsDocumentation.lua:114]`; `C_AddOns.IsAddOnLoadable(name, character,
demandLoaded)` returns `loadable, reason` `[T1 docs: :304]`. The token is localised
by looking up `_G["ADDON_"..reason]`:

```lua
entry.Status:SetText(_G["ADDON_"..reason]);
```
`[T1 src: Blizzard_AddOnList/AddonList.lua:395]`, same pattern in
`UIParentLoadAddOn` `[T1 src: Blizzard_UIParent/Shared/UIParent.lua:254]`.

The token vocabulary is enumerable from the global strings `[T2 res:
Resources/GlobalStrings/enUS.lua:679-726]` — `BANNED`, `CORRUPT`, `DEMAND_LOADED`,
`DISABLED`, `EXCLUDED_FROM_BUILD`, `INCOMPATIBLE`, `INSECURE`,
`INTERFACE_VERSION`, `MISSING`, `NOT_AVAILABLE`, `NO_ACTIVE_INTERFACE` (the draft
listed only 7 of these 11 and stopped the range at `:724`; **corrected**), and the
15-member `DEP_*` family at `:684-698`
(`DEP_BANNED`, `DEP_CORRUPT`, `DEP_DEMAND_LOADED`, `DEP_DISABLED`,
`DEP_EXCLUDED_FROM_BUILD`, `DEP_INCOMPATIBLE`, `DEP_INSECURE`,
`DEP_INTERFACE_VERSION`, `DEP_MISSING`, `DEP_NOT_AVAILABLE`,
`DEP_NO_ACTIVE_INTERFACE`, `DEP_USER_ADDONS_DISABLED`, `DEP_WRONG_ACTIVE_INTERFACE`,
`DEP_WRONG_GAME_TYPE`, `DEP_WRONG_LOAD_PHASE`). This is a list of *localised
strings named `ADDON_<token>`*, not a Blizzard-published enum of reasons; the
mapping to actual `reason` returns is by construction of `_G["ADDON_"..reason]`.
Blizzard code branches on
`"DEP_DISABLED"`, `"DEP_DEMAND_LOADED"`, `"DEMAND_LOADED"` and `"INTERFACE_VERSION"`
by literal string `[T1 src: AddonList.lua:190, 366, 402-403; AddonCompartment.lua:83, 89]`.

Enable state is tri-valued, not boolean:
`Enum.AddOnEnableState = { None = 0, Some = 1, All = 2 }`
`[T1 docs: AddOnsDocumentation.lua:424]` — "Some" meaning enabled for some
characters. Blizzard's own per-character test is
`C_AddOns.GetAddOnEnableState(addonName, character) == Enum.AddOnEnableState.All`
`[T1 src: AddOnUtil.lua:64-67]`.

Security state is `Enum.AddOnSecurityStatus = { Secure = 0, Insecure = 1, Banned = 2,
NotAvailable = 3 }` `[T1 docs: AddOnsDocumentation.lua:437]`; `GetAddOnInfo`'s 6th
return is the string form, and Blizzard compares it to `"SECURE"`
`[T1 src: AddonCompartment.lua:94]`.

### 4.3 Load-on-demand

`## LoadOnDemand: 1` defers loading until something calls
`C_AddOns.LoadAddOn(name) -> loaded: bool?, value: string?`
`[T1 docs: AddOnsDocumentation.lua:347]`. Blizzard's own wrapper names that second
return `reason` and surfaces it as a dialog:

```lua
function UIParentLoadAddOn(name)
	local loaded, reason = C_AddOns.LoadAddOn(name);
	if ( not loaded ) then
		… SetBasicMessageDialogText(format(ADDON_LOAD_FAILED, name, _G["ADDON_"..reason])) …
```
`[T1 src: Blizzard_UIParent/Shared/UIParent.lua:250-259]`.

LoD is common on Blizzard's side (**125** of 346 shipped tocs set
`## LoadOnDemand: 1` `[T1 src]`) and third-party (**45** of 147 on this install
`[T1 obs]`, e.g. `BigWigs_Options`,
`TellMeWhen_Options`, the 15 `RaiderIO_DB_*` data packs, per-zone `LittleWigs_*`
modules).

> ⚠ **Corrected 2026-07-23 (cross-file reconciliation).** This paragraph, and
> rule 20 below, previously read "167 of 346" and "46 of 147". Those are counts of
> tocs carrying a `## LoadOnDemand` **line of any value**, and **42 shipped tocs
> declare `## LoadOnDemand: 0`** (plus 1 third-party toc), which is the explicit
> *opposite* of load-on-demand. Re-counted `[T1 src / T1 obs]`:
> `## LoadOnDemand: 1` → **125**/346 shipped and **45**/147 third-party;
> `: 0` → 42 shipped and 1 third-party. `module-architecture.md` §5.4 already
> carried the correct 125/45; the two files now agree. The **line** counts in
> §2.2 and in `sources.md` §1.1 (`LoadOnDemand` 167 / 46) remain right *as line
> frequencies* — do not read either as "is load-on-demand".

`C_AddOns.IsAddOnLoaded(name)` returns **two** booleans —
`loadedOrLoading, loaded` `[T1 docs: AddOnsDocumentation.lua:322]`. Code that
reads only the first return cannot distinguish "loaded" from "currently loading".

Related: `C_AddOns.IsAddOnLoadOnDemand(name)` `[:289]`,
`C_AddOns.DoesAddOnExist(name)` `[:32]`,
`C_AddOns.DoesAddOnHaveLoadError(name)` `[:47]` — the last is Tier-1 evidence that
**a load error is tracked per addon**, i.e. one addon erroring does not take the
rest down. Nothing in the source uses it `[T1 src: only its own doc entry matches]`.

> `[gap]` Whether a Lua error *inside* a `.toc`-listed file aborts only that file
> or the whole addon's remaining files is **not established**. Looked in:
> `Blizzard_APIDocumentationGenerated` (only `DoesAddOnHaveLoadError`, no
> semantics), `Blizzard_ScriptErrors/`, the wiki `AddOn loading process` page
> (silent on it), `TOC format` (silent). `@verify-ingame`.

---

## 5. The shared Lua sandbox

### 5.1 One global environment for everybody

**By default every addon's chunks execute against the same global table.** The
evidence is behavioural and Tier 1:

- Blizzard calls addon-defined globals by name out of `_G`:
  `_G[addonCompartmentFunc](addonName, ...)`
  `[T1 src: Blizzard_Minimap/Mainline/AddonCompartment.lua:99]`.
- Blizzard walks the whole global environment as a plain table:
  `for k,v in pairs(getfenv(0)) do` `[T1 src: Blizzard_SharedXML/Dump.lua:168, 197, 477]`,
  and aliases it: `local _G = getfenv(0);`
  `[T1 src: Blizzard_TimeManager/Mainline/Blizzard_TimeManager.lua:5]`.
- String/dynamic indexing of `_G` is everywhere in the shipped source: **912
  occurrences of `_G[` across 180 of the 2298 `.lua` files**, of which **421** are
  the string-literal form `_G["` `[T1 src, grep -rohE '_G\[' over
  Interface/AddOns/**/*.lua]`.
- The per-addon private environment is an explicit **opt-in** restricted directive
  (`UseSecureEnvironment: 1`, 13 Blizzard addons) `[T1 src; T2 wiki §Restricted]` —
  which only makes sense if the default is shared.

Practical consequence: **an unprefixed global is a collision.** Any addon can read,
overwrite, or wrap any other addon's globals.

> `[gap]` I did **not** establish that this is literally one `lua_State` shared by
> all addons. No Tier-1 or Tier-2 source states the VM topology. Everything above
> is evidence of a *shared global table*, which is what actually matters for code.
> Looked in: generated docs (no VM/state API), the wiki `Lua functions` page
> (revid 6779934), `Blizzard_RestrictedAddOnEnvironment/`.

### 5.2 The per-file vararg: `local ADDON, ns = ...`

Each Lua file is a chunk whose **varargs are `(addonName, addonTable)`**. Tier 1
confirms this in the documentation string for the accessor:

> "Returns the addon table (**passed as the second argument of `...` to files**) for
> any addon that opts in through setting `AllowAddOnTableAccess: 1` in the toc file.
> Insecure code cannot query addon tables from Blizzard addons."
> — `C_AddOns.GetAddOnLocalTable(name)` `[T1 docs: AddOnsDocumentation.lua:149]`

The wiki spells out the shape: *"The addon namespace is a private table shared
between Lua files in the same addon"*, `addonName, addonTable = ...`
`[T2 wiki: Using the AddOn namespace, revid 6474636, 2025-09-16]`. Added in patch
3.3.0 per the same page.

The table is created by the client, per addon, and is the **same object** in every
file of that addon — *"a private table shared between Lua files in the same addon"*
`[T2 wiki: Using the AddOn namespace, revid 6474636]`. It is not global — hence the
`AllowAddOnTableAccess` opt-in for external reads.

> `[gap]` **Whether an inline XML `<OnLoad>` body sees the addon vararg is not
> established.** The wiki page speaks only of "Lua files"; `UI.xsd` types script
> bodies as plain string content `[T1 src: UI.xsd:1177-1185]` and says nothing
> about their varargs. Of the 2123 `<OnLoad` occurrences in the shipped XML, 6 have
> `...` within three lines and **all six forward event/callback varargs, none reads
> an addon table** `[T1 src: Blizzard_UIPanels_Game/Mainline/QuestMapFrame.xml:196
> (a commented-out line), Blizzard_FrameXML/PVPHonorSystem.xml:92-93 and :322-323,
> Blizzard_ChatFrameBase/Mainline/FloatingChatFrame.xml:194]`. Note the six are
> only four distinct sites, and one of them is dead code — so this is an argument
> from silence, not evidence. Do not assume either way. `@verify-ingame`.

Practice, counted rather than asserted. Metric: **`.lua` files containing at least
one chunk-level (column-0, unindented) line matching
`^local <ident>\s*,\s*<ident>\s*=\s*\.\.\.`** — reproducible with that regex over
each checkout, `.git/` excluded:

| Addon `[T3, commits per sources.md]` | Files using the idiom | Total `.lua` |
|---|---|---|
| oUF `5672a3cb10e1` | 41 | 41 |
| details `e14de53cc2e1` | 111 | 326 |
| BigWigs `3fdc10f6cfd1` | 54 | 131 |
| ElvUI `f60934a174d6` | 55 | 680 |
| plater `2b2ff463cccd` | 34 | 185 |
| WeakAuras2 `38d4bf1e6099` | 7 | 198 |
| Ace3 `4475787f06f7` | 0 | 74 |

> ⚠ **Cross-file note (2026-07-23).** `module-architecture.md` §2.3 counts the
> same thing with a **one-or-more-identifier** regex and reports **WeakAuras2 =
> 128** where this table says 7, and (after its own 2026-07-23 correction)
> **Details = 111**, matching this table. Both greps reproduce exactly; they
> measure different *spellings*. Neither number is "the" adoption figure — cite
> the regex with the count.

WeakAuras' low count is a spelling difference, not a different mechanism — it uses
the split form `local AddonName = ...` / `local Private = select(2, ...)`
`[T3: WeakAuras2 `38d4bf1e6099`, WeakAuras/Init.lua:2-4, WeakAuras/WeakAuras.lua:2-4]`.
Ace3's zero is expected: it is a **library** distributed by embedding, so it cannot
rely on being any particular addon `[T3: Ace3 `4475787f06f7`]`. oUF opens with
`local parent, ns = ...` then immediately reads its own toc metadata via that name:
`C_AddOns.GetAddOnMetadata(parent, 'X-oUF')` `[T3: oUF/ouf.lua:1-2]`.

Blizzard uses it too, but sparsely — **30 of 2298** shipped Lua files `[T1 src]`, e.g.
`local _, PrivateAuras = ...;`
`[T1 src: Blizzard_PrivateAurasUI/PrivateAuraInit.lua:1]`,
`local _, namespace = ...;`
`[T1 src: Blizzard_CooldownBroadcaster/TrackedCooldowns.lua:1]`. Blizzard's own code
is overwhelmingly global-based.

### 5.3 What Lua you actually get

*"World of Warcraft uses a modified version of Lua 5.1 which also supports taint.
Notably, operating system and file I/O libraries are not present."*
`[T2 wiki: Lua functions, revid 6779934, **2026-07-23** — edited the day this file
was written]`.

**Present** `[T2 wiki: Lua functions]`: the base library (`assert`, `error`,
`pcall`, `xpcall`, `select`, `type`, `tonumber`, `tostring`, `pairs`, `ipairs`,
`next`, `unpack`, `rawget`/`rawset`/`rawequal`, `setmetatable`/`getmetatable`,
`setfenv`/`getfenv`, `loadstring`, `newproxy`, `collectgarbage`), `string`, `table`,
`math`, `coroutine`, and the Lua 5.2 `bit` library (since patch 1.9).
`date`, `time` and `difftime` exist **as globals** — the `Lua functions` page lists
all three in the base-library section `[T2 wiki: Lua functions, revid 6779934]`, and
`API date` explains why: *"date() is a reference to the os.date function. It is put
in the global table as the os module is not available."* `[T2 wiki: API date, revid
3016063, **2022-07-21** — a stale page; the claim is corroborated by the current
`Lua functions` listing, which is why it is repeated here]`.

**Absent.** Two strengths of evidence here, and they are not the same:

- `os` and `io` are **stated** absent — *"operating system and file I/O libraries
  are not present"* `[T2 wiki: Lua functions, revid 6779934]`.
- `package`/`require`, `dofile`, `loadfile`, `module` are **not stated** absent
  anywhere I found; they are simply **not listed** among the libraries the page
  enumerates (base, math, string, table, coroutine, bit). Absence from a list is
  weaker than a statement. `[gap]` Looked in: the wiki `Lua functions` page
  (revid 6779934, whole page), `wowkb.uiapi missing require` (not in the generated
  docs), and the shipped source.

Tier-1 corroboration by absence: across the 2298 `.lua` files of the shipped UI
there is **not one** call to `require(`, `dofile`, `loadfile`, `module(`, or —
with a word-boundary-anchored regex `(^|[^A-Za-z0-9_."])(os|io)\.[a-z]` — `os.`
or `io.` `[T1 src, grep over Interface/AddOns/**/*.lua]`. That is corroboration,
not proof of absence, but it is a strong signal that no Blizzard code assumes them.
`@verify-ingame`: `/dump type(require), type(os), type(io)` settles it in one line.

**WoW-specific additions**, verified as actually used by the shipped UI `[T1 src,
file counts]`: `strcmputf8i` (36 files), `strlenutf8` (8), `securecall` (60),
`table.count` (2), `table.create` (2), `fastrandom` (1), `string.rtgsub` (1).

- **Corrected from the draft:** it also listed `loadstring` (6 files) and
  `newproxy` (3) as WoW-specific. Both are **stock Lua 5.1** — they are already in
  the "Present" list above, and the wiki tags neither with `{{apitag|wow}}`
  `[T2 wiki: Lua functions, revid 6779934]`. The file counts are right; the label
  was not.
- `string.rtgsub` is wiki-tagged **`framexml`**, i.e. flagged as Blizzard-internal
  rather than addon-facing `[T2 wiki: Lua functions §String library]`. `[gap]` I did
  not establish whether an addon can call it. `@verify-ingame`.

The wiki also lists `table.freeze`, `table.isfrozen`, `table.removemulti`,
`strsplittable`, `string.split`/`join`/`trim`/`concat`, `tostringall` — of which
`table.freeze`, `table.isfrozen`, `table.removemulti` and `strsplittable` have
**zero** uses in the shipped source `[T1 src, re-counted]`, so they rest on Tier 2
alone. (`table.removemulti` was in the draft's wiki list but missing from its
zero-use list; **corrected**.) `@verify-ingame`.

Coroutines exist but are barely used by Blizzard: `coroutine.` appears in 2 files
`[T1 src]`.

**The Lua-4 compatibility globals are on notice.** `Blizzard_SharedXMLBase/Compat.lua`
opens:

```lua
--[[
	These defitinitions are for compatability with lua 4 code.
	THIS FILE WILL BE REMOVED IN A FUTURE UPDATE!
	PLEASE UPDATE ALL EXISTING CODE ASAP TO USE THE LUA 5.1 EQUIVALENTS
]]
```
`[T1 src: Blizzard_SharedXMLBase/Compat.lua:1-5]`

It is what defines the familiar bare globals: `tinsert`, `tremove`, `wipe`, `sort`,
`getn`, `foreach`, `foreachi` `[:10-16]`; `abs`, `ceil`, `floor`, `max`, `min`,
`mod`, `random`, `sqrt`, `PI` and seven **degree-based** trig wrappers `[:20-43]`;
`strbyte`, `strchar`, `strfind`, `format`, `gmatch`, `gsub`, `strlen`, `strlower`,
`strmatch`, `strrep`, `strrev`, `strsub`, `strtrim`, `strupper` `[:47-61]`.

> ⚠ **Corrected from the draft, which said all seven trig wrappers are
> "degree-taking". They are not — the two halves differ, and getting this backwards
> is exactly the silent bug the rule is meant to catch.** Read the actual lines:
>
> ```lua
> acos = function (x) return math.deg(math.acos(x)) end   -- :22   arg = ratio, RESULT in degrees
> asin = function (x) return math.deg(math.asin(x)) end   -- :23
> atan = function (x) return math.deg(math.atan(x)) end   -- :24
> atan2 = function (x,y) return math.deg(math.atan2(x,y)) end -- :25
> cos = function (x) return math.cos(math.rad(x)) end     -- :27   ARG in degrees, result = ratio
> sin = function (x) return math.sin(math.rad(x)) end     -- :41
> tan = function (x) return math.tan(math.rad(x)) end     -- :43
> ```
> `[T1 src: Blizzard_SharedXMLBase/Compat.lua:22-25, 27, 41, 43]`. Corroborated
> Tier 2: *"acos … Returns the arc cosine of the value in degrees"* vs *"cos …
> Returns the cosine of the degree value"* `[T2 wiki: Lua functions §Math library,
> revid 6779934, 2026-07-23]`.

Two consequences worth internalising:
1. `sin(x)` and `math.sin(x)` are **not the same function** — the bare `sin`/`cos`/
   `tan` take **degrees**, `math.sin`/`cos`/`tan` take radians; the bare `acos`/
   `asin`/`atan`/`atan2` take the same plain ratio as their `math.*` counterparts
   but **return degrees instead of radians** `[T1 src: Compat.lua:22-25, 27, 41, 43]`.
2. Compat.lua is loaded *first* in `Blizzard_SharedXMLBase`
   `[T1 src: Blizzard_SharedXMLBase/Blizzard_SharedXMLBase.toc:4]`, i.e. long before
   any user addon — but Blizzard has announced its removal.

### 5.4 Errors

The global error handler is Blizzard's, installed at the bottom of
`Blizzard_ScriptErrors`:

```lua
seterrorhandler(HandleLuaError);
```
`[T1 src: Blizzard_ScriptErrors/Blizzard_ScriptErrors.lua:101]`

Blizzard exposes a registration hook, but gates it:

```lua
function AddLuaErrorHandler(handler)
	assert(issecure());
```
`[T1 src: Blizzard_ScriptErrors/Blizzard_ScriptErrors.lua:66-67]`

> `[gap]` Whether an addon can ever satisfy `issecure()` at that call site is a
> security-topic question, not settled here. The assert is Tier 1; the conclusion
> "addons cannot register a Lua error handler this way" is inference.
> `@verify-ingame`.

`geterrorhandler()` is used pervasively by Blizzard for deferred error reporting
`[T1 src: Blizzard_SharedXMLBase/ErrorUtil.lua:3, 18-19;
Blizzard_RestrictedAddOnEnvironment/SecureHandlers.lua:35]`.

The Blizzard_ScriptErrors addon itself carries `## EscalateErrorDuringLoad: 1`
`[T1 src: Blizzard_ScriptErrors/Blizzard_ScriptErrors.toc:5]` — the restricted
directive the wiki describes as *"appears to have no effect in public clients"*
`[T2 wiki: TOC format]`.

---

## 6. The lifecycle

### 6.1 Login / reload sequence

| # | Event | Payload `[T1 docs]` | Doc flag | Locator |
|---|---|---|---|---|
| 1 | `ADDON_LOADED` | `addOnName: cstring, containsBindings: bool` | `SynchronousEvent` | `AddOnsDocumentation.lua:389` |
| 2 | `PLAYER_LOGIN` | *(none)* | `SynchronousEvent` | `SystemDocumentation.lua:129` |
| 3 | `PLAYER_ENTERING_WORLD` | `isInitialLogin: bool, isReloadingUi: bool` | `SynchronousEvent` | `SystemDocumentation.lua:112` |
| 4 | `PLAYER_REGEN_DISABLED` | *(none)* — only if already in combat | `SynchronousEvent` | `UnitDocumentation.lua:3725` |
| 5 | `SPELLS_CHANGED` | *(none)* | **`UniqueEvent`**, *not* `SynchronousEvent` | `SpellBookDocumentation.lua:900` |

Rows 1–4 carry `SynchronousEvent = true` in the generated docs `[T1 docs]`;
`SPELLS_CHANGED` instead carries `UniqueEvent = true` and no synchronous flag
`[T1 docs: SpellBookDocumentation.lua:900-903]`. `[gap]` The flags are common —
`SynchronousEvent = true` occurs 1622× and `UniqueEvent = true` 142× across the
generated docs `[T1 docs]` — but **their meaning is defined nowhere**: no
`Documentation` field on any of them, and zero occurrences of either identifier in
the 2298 shipped `.lua` files outside `Blizzard_APIDocumentationGenerated/`
`[T1 src, grep]`. Do not read "dispatched inline rather than queued" into
`SynchronousEvent` — that is an inference no source I found supports.

Ordering itself is `[T2 wiki: AddOn loading process, revid 6302251, 2025-04-23]`
plus `[T2 wiki: PLAYER_LOGIN, revid 6589506, 2026-01-03]` — *"Triggered immediately
before `PLAYER_ENTERING_WORLD` on login and UI Reload, but NOT when entering/leaving
instances."*

What each is for:

- **`ADDON_LOADED`** — *"An addon is loaded after all .lua files have been run and
  SavedVariables have loaded. … this is the first time an AddOn can access its saved
  variables"* `[T2 wiki: ADDON_LOADED, revid 6590223, 2026-01-03]`. It fires **once
  per addon**, so a handler must test `arg1` against its own name; and because
  load-on-demand addons can load at any moment, it keeps firing all session. The
  `containsBindings` boolean was added in 10.1.0 `[T2 wiki]`.
- **`PLAYER_LOGIN`** — fires once per login/reload, before the first
  `PLAYER_ENTERING_WORLD`. The right home for one-time init and frame placement
  `[T2 wiki: AddOn loading process]`.
- **`PLAYER_ENTERING_WORLD`** — fires on **every** loading screen: login, reload,
  and each zone/instance transition. `isInitialLogin` is true whenever the character
  logs in (including after a trip to character select); `isReloadingUi` marks a
  `/reload` `[T1 docs: SystemDocumentation.lua:112; T2 wiki: PLAYER_ENTERING_WORLD,
  revid 6590943, 2026-01-03]`. Blizzard uses exactly this event as its
  "addons are loadable now" signal `[T1 src: AddonCompartment.lua:66, 71-73]`.
- **`SPELLS_CHANGED`** — currently fires after the above, but the wiki explicitly
  flags that this "was not always this way" `[T2 wiki: AddOn loading process]`.

**`VARIABLES_LOADED` is not part of the sequence.** *"Previously (prior to 3.0.1)
this event was part of the loading sequence. … it no longer has a guaranteed order
that can be relied on. … Addons should not use this event to check if their addon's
saved variables have loaded."* `[T2 wiki: VARIABLES_LOADED, revid 6589741,
2026-01-03]`. It is still a live event `[T1 docs: SystemDocumentation.lua:220]` —
it just means *Blizzard's* CVars/keybindings, not yours. (The wiki contradicts
itself on the patch: the `VARIABLES_LOADED` page says **3.0.1**, while
`AddOn loading process` §Patch changes says **3.0.2** `[T2 wiki, revid 6302251]`.
Nothing turns on which; the point is "since Wrath, unordered".)

Error path: `SAVED_VARIABLES_TOO_LARGE(addOnName: cstring)`
`[T1 docs: AddOnsDocumentation.lua:410]`, fired **after** `ADDON_LOADED`
`[T2 wiki: ADDON_LOADED; AddOn loading process]`.

### 6.2 Logout / unload sequence

`PLAYER_LEAVING_WORLD` → `PLAYER_LOGOUT` → `ADDONS_UNLOADING`
`[T2 wiki: AddOn loading process]`.

- `PLAYER_LOGOUT()` `[T1 docs: SystemDocumentation.lua:135]` — last chance to touch
  SavedVariables (the wiki marks this claim `{{fact}}`, i.e. self-flagged as
  uncited).
- `ADDONS_UNLOADING(closingClient: bool)` `[T1 docs: AddOnsDocumentation.lua:400]`
  — fires **once**, not per addon; the `closingClient` boolean is Tier-1 proof that
  the client distinguishes "quitting" from "reloading". The wiki adds that it does
  not occur on a crash or Alt-F4 — also `{{fact}}`-tagged, so Tier 2 at best.

> ⚠ WoWUIBugs **#748 "Certain API calls don't work correctly during PLAYER_LOGOUT"**
> is open and labelled *Acknowledged by Blizzard* `[T2 tracker, per sources.md §2.2]`.
> Treat the logout window as degraded.

---

## 7. `/reload` semantics

`/reload` ≡ `/console reloadUI` ≡ `/run ReloadUI()`
`[T2 wiki: MACRO reload, revid 2436052, **2020-12-23** — stale page, but the
mechanism is confirmed Tier 1 below]`.

```lua
function ReloadUI()
	C_UI.Reload();
end
```
`[T1 src: Blizzard_SharedXML/InterfaceUtil.lua:1-3]`, and
`C_UI.Reload()` `[T1 docs: UIManagerDocumentation.lua:65]`.

What a reload does, from the evidence:

1. **Tears the UI down like a logout.** `ADDONS_UNLOADING` fires and SavedVariables
   are committed — *"All AddOns commit SavedVariables prior to reloading, quitting
   or logging off"* `[T2 wiki: AddOn loading process, revid 6302251 — the sentence
   carries a `{{fact}}` self-flag]`. Tier 1 supplies only the payload shape
   `closingClient: bool` `[T1 docs: AddOnsDocumentation.lua:400]`; that a reload
   passes it as `false` is **inference from the field name**, not a sourced fact.
   `@verify-ingame`.
2. **Re-runs the whole §6.1 sequence.** `PLAYER_ENTERING_WORLD` arrives with
   `isReloadingUi = true` and `isInitialLogin = false`
   `[T1 docs: SystemDocumentation.lua:112]`.
3. **Re-reads the filesystem.** *"Newly created/added files and even complete addons
   are detected when doing a `/reload` after the game has started"*
   `[T2 wiki: TOC format, revid 6767089, 2026-07-09]`, attributed there to patch
   9.0.1 for toc metadata + new files and to patch 4.0.1 for changes to file order.
   This is why an addon-development loop is edit → `/reload`, with no client restart.
4. **Does not re-log the character.** `PLAYER_LOGIN` still fires
   `[T2 wiki: PLAYER_LOGIN, revid 6589506 — "on login and UI Reload"]`, and the
   wiki notes *"If this is a reload, talent information is also available"* at
   `PLAYER_ENTERING_WORLD` `[T2 wiki: AddOn loading process, revid 6302251]`.
   `[unverified]` The draft added "the world state is not re-fetched from scratch";
   no source I found says that, so it is cut to the two cited facts.

> `[gap]` I found no Tier-1 or Tier-2 statement of the *exact* set of state a
> reload preserves vs discards (e.g. whether the Lua state is fully destroyed or
> recycled). Looked in: generated docs for `C_UI.Reload` (no `Documentation`
> field), `Blizzard_SharedXML/InterfaceUtil.lua`, the wiki `MACRO reload` and
> `AddOn loading process` pages. Behaviourally, addon chunks are re-executed, since
> `ADDON_LOADED` fires again. `@verify-ingame`.

---

## 8. Introspecting the environment at runtime

`C_AddOns` — 29 functions, 3 events `[T1 docs: AddOnsDocumentation.lua:3]`. Beyond
what §4 covers: `GetAddOnTitle` `[:241]`, `GetAddOnNotes` `[:196]`,
`GetAddOnInterfaceVersion` `[:134]`, `GetAddOnOptionalDependencies` `[:211]`,
`GetAddOnSecurity` `[:226]`, `IsAddOnDefaultEnabled` `[:274]`,
`IsAddonVersionCheckEnabled` `[:338]`, `SetAddonVersionCheck` `[:375]`,
`GetScriptsDisallowedForBeta` `[:265]`, plus the mutating `DisableAddOn` `[:11]`,
`DisableAllAddOns` `[:22]`, `EnableAddOn` `[:62]`, `EnableAllAddOns` `[:73]`,
`ResetAddOns` `[:363]`, `ResetDisabledAddOns` `[:367]`, `SaveAddOns` `[:371]`.
(The draft gave the same seven line numbers but in a different order from the
names, so `EnableAddOn` read as `:11`; **corrected** — names and lines now pair.)

`C_AddOnProfiler` — 10 functions `[T1 docs: AddOnProfilerDocumentation.lua:3]`:
`IsEnabled`, `GetAddOnMetric(name, metric)`, `GetOverallMetric`,
`GetApplicationMetric`, `GetTopKAddOnsForMetric`, `GetTicksPerSecond`,
`MeasureCall`, `AddMeasuredCallEvent`, plus the performance-message pair
(`CheckForPerformanceMessage` is `MayReturnNothing`,
`AddPerformanceMessageShown` `HasRestrictions`). Metrics come from
`Enum.AddOnProfilerMetric` — 12 values: `SessionAverageTime`, `RecentAverageTime`,
`EncounterAverageTime`, `LastTime`, `PeakTime`, and the `CountTimeOver{1,5,10,50,100,500,1000}Ms`
buckets `[T1 docs: AddOnProfilerConstantsDocumentation.lua:19]`.

Memory, separately: `GetAddOnMemoryUsage(name)` and `UpdateAddOnMemoryUsage()`
`[T1 docs: PerformanceDocumentation.lua:25, :94]`, used by the addon list
`[T1 src: Blizzard_AddOnList/AddonList.lua:761, 769, 866]`. `GetAddOnCPUUsage`
still exists in the docs `[T1 docs: PerformanceDocumentation.lua:10]` but has **no
call sites** in the shipped UI `[T1 src]` — the CPU story moved to
`C_AddOnProfiler`.

---

## 9. Consolidated gaps

- `[gap]` **Inter-addon load order is Tier 2 only** and hedged ("usually …
  alphabetical"). No Tier-1 API or source statement found. §4.1.
- `[gap]` **Three bracketed toc conditionals in the shipped corpus are undocumented**
  — `[AllowLoadEnvironment …]`, `[LoadIntoEnvironment …]`, `[ExcludeLoadGameType …]`.
  Not in the wiki's TOC page at revid 6767089, not used by any third-party toc here.
  Not previously in the source registry. §2.4.
- `[gap]` **Three shipped `##` directives are undocumented** — `ShowInAddOnList`,
  `ShowInDebugList`, and `SuppressLocalTableRef` (which the wiki says was *removed*
  in 11.0.0 yet is present at 12.0.7). §2.3.
- `[gap]` **Per-file error containment on load** is unestablished — only
  `C_AddOns.DoesAddOnHaveLoadError` proves errors are tracked per addon. §4.3.
- `[gap]` **"One VM"** is not sourced. The evidence supports "one shared global
  table"; VM topology is unstated anywhere I looked. §5.1.
- `[gap]` **Nested `.toc` files are still not proven un-enumerable.** The draft
  marked this "resolved" on the strength of `AddOns.txt`; that argument is retracted
  (§1) because 8 well-formed *top-level* folders are missing from the same file, so
  absence there proves nothing. The rule rests on Tier 2 (the wiki's placement
  requirement) with `AddOns.txt` as corroboration. §1, §19b.
- `[gap]` **`AddOns.txt` omits 8 present, well-formed addon folders** and retains 2
  removed ones; no pattern (LoD, deps, declared `Interface`, mtime) explains the
  omissions. It is also **not** consistent across characters — 78/71/70/3 entries
  across the 26 files, intersection of 3. §1.
- `[gap]` **Engine-level dependency transitivity is unsourced.** `AddOnUtil.lua`
  proves only that Blizzard's Lua demand-load helper recurses. §4.2, rule 21.
- `[gap]` **`OptionalDeps` never blocking a load** is the natural reading of the
  wiki's "if available", not a cited statement. §4.2.
- `[gap]` **`SynchronousEvent` / `UniqueEvent` are undefined.** They annotate 1622
  and 142 event entries respectively but carry no `Documentation` field and appear
  nowhere in the shipped `.lua` outside the generated docs. §6.1.
- `[gap]` **Whether an inline XML `<OnLoad>` sees the addon vararg** — unestablished
  in schema, wiki, or shipped usage. §5.2.
- `[gap]` **Whether addon code can call `AddLuaErrorHandler`** turns on `issecure()`
  in that frame; not resolved here. §5.4.
- `[gap]` **The 1024-char toc line limit** rests on the wiki alone. §2.1.
- `[gap]` **`table.freeze` / `table.isfrozen` / `table.removemulti` /
  `strsplittable`** are wiki-only — zero uses in the shipped UI source. §5.3.
- `[gap]` **`string.rtgsub` is wiki-tagged `framexml`** — whether addons may call
  it at all is unestablished. §5.3.
- **Nothing here has been run in the client.** Items marked `@verify-ingame` above
  are the ones where that would change the answer.

---

## Rules we could audit against

Each rule is checkable against real addon source or a real `.toc`.

1. **Every addon folder contains a `.toc` whose basename equals the folder name,
   optionally plus a recognised flavour suffix** (`_Mainline`, `_Classic`,
   `_Standard`, `_Vanilla`, `_TBC`, `_Wrath`, `_Cata`, `_Mists`, `_WoWLabs`,
   `_WoWHack`, legacy `-WOTLKC`/`-BCC`). Violation ⇒ the toc is not loaded.
   *[Tier 2: warcraft.wiki.gg `TOC format` revid 6767089, 2026-07-09 — §Rules +
   intro for the name rule ("otherwise the .toc file won't load"), §Client-specific
   TOC files for the suffix table and its `_Mainline`/`_Classic`-rank-lowest
   precedence. Tier 1 corroboration: re-counted, 147/147 third-party tocs on the
   live install conform to exactly that suffix list.]*
   ⚠ **Blizzard's own corpus violates this rule twice** (§1), so do not use the
   shipped tocs as the reference implementation of it.

2. **A `.toc` lists only `.lua` and `.xml` as file entries.** Any other extension
   on a load line is a bug. *[Tier 1: 346 shipped tocs → 2380 `.lua` + 1299 `.xml`
   entries, nothing else, `wow-ui-source@4383ced` `Interface/AddOns/*/*.toc`.
   Tier 1 obs: 147 third-party tocs → 1482 `.lua` + 183 `.xml`, nothing else.]*

3. **A third-party `.toc` must not contain the `##` directives `AllowLoad`,
   `LoadFirst`, `UseSecureEnvironment`, `SavedVariablesMachine` or
   `EscalateErrorDuringLoad`.** (Note this is the *metadata* `## AllowLoad:`; the
   bracketed `[AllowLoad …]` *condition* is a separate, documented, addon-facing
   feature.)
   *[Tier 2 for the restriction: wiki `TOC format` §Restricted, revid 6767089,
   2026-07-09 — exactly these five. Tier 1 corroboration: 0/147 third-party tocs on
   this install use any of them, while Blizzard tocs use `AllowLoad` 177×,
   `LoadFirst` 19×, `UseSecureEnvironment` 13×, `SavedVariablesMachine` 3×,
   `EscalateErrorDuringLoad` 3× — e.g.
   `Blizzard_ScriptErrors/Blizzard_ScriptErrors.toc:4-5`.]*

3b. **Weaker, same shape: `Secure`, `SuppressLocalTableRef`, `ShowInAddOnList` and
   `ShowInDebugList` should also not appear in a third-party `.toc`.** These are
   *undocumented or unmarked*, not documented-as-restricted, so this rule is an
   inference from usage, not a cited prohibition.
   *[Tier 1 usage only: `Secure` on 5 shipped tocs;
   `Blizzard_RecruitAFriend/Blizzard_RecruitAFriend.toc:5`,
   `Blizzard_PerksProgram/Blizzard_PerksProgram.toc:3`,
   `Blizzard_EventTrace/Blizzard_EventTrace.toc:4`; 0/147 third-party tocs.
   Note the wiki says `SuppressLocalTableRef` was removed in 11.0.0, yet it is
   present at 12.0.7.68887.]*

4. **A `.toc` with no `## Interface:` line is permanently "out of date" and will
   not load unless the user ticks "Load out of date AddOns".**
   *[Tier 2: wiki `TOC format` §Interface version, revid 6767089. Tier 1
   corroboration: the gate exists in code — `reason == "INTERFACE_VERSION"` at
   `Interface/AddOns/Blizzard_AddOnList/AddonList.lua:783` and `:809`.]*

5. **A `.toc` that uses a bracketed per-file conditional or a `[Family]`/`[Game]`
   path variable must declare `## Interface:` ≥ 110105; `[TextLocale]` /
   `[AllowLoadTextLocale]` require ≥ 110200; a bracketed conditional on a `##`
   metadata line requires ≥ 120007.** Older declared interfaces plus these features
   is an inconsistency.
   *[Tier 2: wiki `TOC format` §Patch changes, revid 6767089.]*

6. **An `ADDON_LOADED` handler must compare the first payload argument to its own
   addon name.** A handler that acts on every `ADDON_LOADED` will re-run whenever
   any load-on-demand addon loads, at any point in the session.
   *[Tier 1: payload is `ADDON_LOADED(addOnName: cstring, containsBindings: bool)`,
   `Blizzard_APIDocumentationGenerated/AddOnsDocumentation.lua:389`. Tier 2:
   wiki `AddOn loading process` revid 6302251 — "Confirm which AddOn loaded using
   the first argument (in case a LoadOnDemand AddOn loaded in parallel)".]*

7. **Code that reads its own SavedVariables before its `ADDON_LOADED` reads the
   file-scope defaults, not persisted data** — unless the toc sets
   `LoadSavedVariablesFirst: 1`.
   *[Tier 2: wiki `ADDON_LOADED` revid 6590223 ("this is the first time an AddOn
   can access its saved variables") and `AddOn loading process` revid 6302251
   ("Saved variables load after the last file listed in the TOC").]*

8. **Nothing may key initialisation off `VARIABLES_LOADED`.** Its ordering relative
   to `PLAYER_ENTERING_WORLD` has been unguaranteed since 3.0.1.
   *[Tier 2: wiki `VARIABLES_LOADED` revid 6589741, 2026-01-03 — "Addons should not
   use this event to check if their addon's saved variables have loaded".]*

9. **One-time initialisation belongs in `PLAYER_LOGIN`, not
   `PLAYER_ENTERING_WORLD`.** A `PLAYER_ENTERING_WORLD` handler that does not
   branch on `isInitialLogin`/`isReloadingUi` will re-run on every zone and instance
   transition.
   *[Tier 1: payload `PLAYER_ENTERING_WORLD(isInitialLogin: bool,
   isReloadingUi: bool)`, `SystemDocumentation.lua:112`. Tier 2: wiki
   `PLAYER_LOGIN` revid 6589506 — fires "on login and UI Reload, but NOT when
   entering/leaving instances".]*

10. **No addon file may call `os.*` or `io.*`** — those libraries are stated
    absent. **`require`, `dofile`, `loadfile` and `module` should likewise not
    appear**, on the weaker footing that the wiki enumerates no such library and
    the shipped UI never calls them.
    *[Tier 2 for `os`/`io`: wiki `Lua functions` revid 6779934, 2026-07-23 —
    "operating system and file I/O libraries are not present". Tier 2 by omission
    for the other four: same page, whole-page read, they appear nowhere. Tier 1
    corroboration for all six: zero call sites across all 2298 `.lua` files of
    `wow-ui-source@4383ced`, word-boundary-anchored for `os.`/`io.`.]*

11. **The bare trig globals are degree-based, but in two different directions.**
    `sin`/`cos`/`tan` take **degrees** where `math.sin`/`cos`/`tan` take radians;
    `acos`/`asin`/`atan`/`atan2` take the **same** argument as their `math.*`
    counterparts but **return degrees** where `math.*` returns radians. Mixing
    either pair is a silent correctness bug. **Audit for both directions — the
    earlier draft of this rule said all seven "take degrees", which is wrong for
    the four arc functions and would mis-flag correct code.**
    *[Tier 1: `Interface/AddOns/Blizzard_SharedXMLBase/Compat.lua` — `:41`
    `sin = function (x) return math.sin(math.rad(x)) end` (arg wrapped in `rad`)
    vs `:22` `acos = function (x) return math.deg(math.acos(x)) end` (result
    wrapped in `deg`); also `:23, :24, :25, :27, :43`. Tier 2 corroboration:
    warcraft.wiki.gg `Lua functions` revid 6779934, 2026-07-23, §Math library.]*

12. **Code that relies on the Lua-4 compatibility globals (`tinsert`, `tremove`,
    `wipe`, `getn`, `foreach`, `foreachi`, `sort`, `strfind`, `strlen`, `format`,
    `mod`, `PI`, …) is on a deprecation path Blizzard has announced.**
    *[Tier 1: `Blizzard_SharedXMLBase/Compat.lua:1-5` — "THIS FILE WILL BE REMOVED
    IN A FUTURE UPDATE! PLEASE UPDATE ALL EXISTING CODE ASAP TO USE THE LUA 5.1
    EQUIVALENTS".]*

13. **Any global an addon defines is readable and writable by every other addon;
    only names reached through the per-file addon table are private.** Audit: every
    global an addon creates should be prefixed with the addon name or be a
    deliberate public API.
    *[Tier 1: Blizzard resolves third-party callbacks out of the shared `_G` —
    `_G[addonCompartmentFunc](addonName, ...)` at
    `Blizzard_Minimap/Mainline/AddonCompartment.lua:99`; the global environment is
    an ordinary table — `for k,v in pairs(getfenv(0)) do` at
    `Blizzard_SharedXML/Dump.lua:168`.]*

14. **The addon table is the second file-level vararg, and is reachable from
    outside the addon only if that addon sets `## AllowAddOnTableAccess: 1`.**
    Code calling `C_AddOns.GetAddOnLocalTable("Other")` where `Other` has not opted
    in will not get a table; and it can never get one from a Blizzard addon.
    *[Tier 1: `C_AddOns.GetAddOnLocalTable` documentation string at
    `AddOnsDocumentation.lua:149` — "Returns the addon table (passed as the second
    argument of `...` to files) for any addon that opts in through setting
    `AllowAddOnTableAccess: 1` … Insecure code cannot query addon tables from
    Blizzard addons."]*

15. **`## AddonCompartmentFunc` must name a global function.** A file-local or
    `ns.`-scoped function will not be invoked.
    *[Tier 1: `Blizzard_Minimap/Mainline/AddonCompartment.lua:99` resolves it as
    `_G[addonCompartmentFunc](addonName, ...)`; the metadata is read at `:81`.]*

16. **`C_AddOns.LoadAddOn` returns `(loaded, reason)` where `reason` is a bare
    token, not display text.** Code that shows the second return to a user shows a
    raw token; the localised string is `_G["ADDON_"..reason]`.
    *[Tier 1: `Blizzard_UIParent/Shared/UIParent.lua:250-256`; the same idiom at
    `Blizzard_AddOnList/AddonList.lua:395`. Token vocabulary at Tier 2:
    `BlizzardInterfaceResources@774b2c55 Resources/GlobalStrings/enUS.lua:679-724`.]*

17. **`C_AddOns.IsAddOnLoaded` returns two booleans — `loadedOrLoading, loaded`.**
    Single-return call sites cannot tell "loaded" from "still loading".
    *[Tier 1: `AddOnsDocumentation.lua:322`.]*

18. **`C_AddOns.GetAddOnEnableState` returns a tri-state enum, not a boolean.**
    Truthiness tests are wrong: `None = 0`, `Some = 1`, `All = 2`.
    *[Tier 1: `Enum.AddOnEnableState` at `AddOnsDocumentation.lua:424`; Blizzard's
    own per-character test compares against `Enum.AddOnEnableState.All` at
    `Blizzard_SharedXMLBase/AddOnUtil.lua:66`.]*

19. **Addon enumeration must go through `C_AddOns.GetNumAddOns()` /
    `GetAddOnName(i)`, never a filesystem scan and never `AddOns.txt`** —
    Blizzard's 317 `Blizzard_*` addons are not present under `Interface/AddOns/` on
    disk, and the client's own `AddOns.txt` is neither complete nor current.
    *[Tier 1 obs: the live install's `Interface/AddOns/` holds 81 directories, 0
    beginning `Blizzard_`; the newest of 26 `AddOns.txt` files (2026-07-23 17:26)
    lists 78 names, of which 3 are `Blizzard_*` with no folder and 2 are addons no
    longer installed, while omitting 8 installed folders. Tier 1 API:
    `AddOnsDocumentation.lua:256, :181`.]*

19b. **An embedded library shipped as `<Addon>/Libs/<Lib>/<Lib>.toc` is not an
    addon and must not be referenced as one** (no `## Dependencies: LibStub`, no
    `C_AddOns.IsAddOnLoaded("LibStub")`). Only a `.toc` at
    `Interface/AddOns/<Folder>/<Folder>.toc` is enumerated.
    *[Tier 2 is what this rule actually rests on: the wiki's placement requirement,
    `TOC format` revid 6767089, 2026-07-09 (intro + §Rules). Tier 1 obs is
    **corroboration only**: 38 nested `.toc` files exist on this install and no
    nested-`.toc` library name (`LibStub`, `LibDeflate`, `LibSharedMedia-3.0`)
    appears in any of the 26 client-written `AddOns.txt` files.]*
    ⚠ **Weakened from the draft**, which argued absence from `AddOns.txt` proves
    never-enumerated. It does not: 8 well-formed *top-level* addon folders are also
    absent from that file (§1). Absence there is consistent with the rule, not
    proof of it. `@verify-ingame` for certainty:
    `C_AddOns.DoesAddOnExist("LibStub")`.

20. **A `LoadOnDemand: 1` addon does not load of its own accord at login**, so its
    `ADDON_LOADED` can arrive at any point in the session — or not at all. An LoD
    addon whose initialisation is gated on `PLAYER_LOGIN` will, if demand-loaded
    later, never initialise.
    *[Tier 2: wiki `TOC format` §LoadOnDemand revid 6767089 — "`1` to delay loading
    until `LoadAddOn()`"; `AddOn loading process` revid 6302251 — "LoadOnDemand
    AddOns might trigger part-way or after all steps have finished". Tier 1
    corroboration that this is a mainstream configuration: **125**/346 shipped tocs
    and **45**/147 third-party tocs on this install set `## LoadOnDemand: 1`
    (a further 42 shipped + 1 third-party set it to `0`, which is not LoD).
    ⚠ **Corrected 2026-07-23** from 167/46, which were any-value line counts —
    see the note in §4.3.]*
    ⚠ **Softened from the draft's "never fires `ADDON_LOADED` during login".** An
    LoD addon can still be loaded during login by something else — as another
    addon's `Dependencies` target, or via `## LoadWith` (which the wiki says
    *implies* LoadOnDemand, `§LoadWith` revid 6767089). Audit for the gating bug,
    not for the absolute.

21. **`Dependencies` are hard, and a broken dependency chain is reported as a
    `DEP_*` reason rather than the addon's own.**
    *[Tier 2 for "must load first": wiki `TOC format` §Dependencies revid 6767089.
    Tier 1 for the reason surface: Blizzard branches on `"DEP_DISABLED"` at
    `Blizzard_AddOnList/AddonList.lua:190` and `:368`, and the 15-member `DEP_*`
    string family exists at `GlobalStrings/enUS.lua:684-698` (Tier 2 `res` dump).]*
    ⚠ **The draft's transitivity citation is over-claimed and is corrected here.**
    `Blizzard_SharedXMLBase/AddOnUtil.lua:3-18` (`GetAddOnDependenciesRecursive`,
    consumed by `AddOnUtil.LoadAddOn` at `:40-52`) shows Blizzard's **own Lua
    demand-load helper** walking `C_AddOns.GetAddOnDependencies`
    (`AddOnsDocumentation.lua:83`) recursively. That proves the *helper* is
    transitive. It does **not** prove the client's login-time loader is.
    `[gap]` No Tier-1 or Tier-2 statement of engine-level dependency transitivity
    found; looked in the generated docs (no such API or prose), `AddonList.lua`,
    and both wiki pages. `@verify-ingame`.

22. **Files that are neither listed in the `.toc` nor pulled in by an XML
    `<Script file=…/>` or `<Include file=…/>` never execute.**
    *[Tier 1 for the mechanism: `Blizzard_SharedXML/UI.xsd:1168` (`Include`,
    `file` required) and `:1177` (`Script`, `file` optional), both children of
    `<Ui>` at `:1157`. Tier 2 for the consequence: wiki `TOC format` §File loading
    order, revid 6767089.]*

23. **No addon may call `AddLuaErrorHandler` from a tainted execution path** — the
    function asserts on `issecure()`.
    *[Tier 1: `Blizzard_ScriptErrors/Blizzard_ScriptErrors.lua:66-67`. Whether an
    addon call frame is ever secure is out of scope here — `@verify-ingame`.]*
