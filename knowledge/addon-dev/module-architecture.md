---
title: Module architecture and project layout
patch: 12.0.7
fetched: 2026-07-23
reviewed: 2026-07-23
sources:
  - https://github.com/Gethe/wow-ui-source (live, version.txt 12.0.7.68887, commit 4383ced30106d51b27e3e86d1987f1552f0d259d)
  - https://warcraft.wiki.gg/wiki/TOC_format (revid 6767089, 2026-07-09)
  - https://warcraft.wiki.gg/wiki/Using_the_AddOn_namespace (revid 6474636, 2025-09-16)
  - https://warcraft.wiki.gg/wiki/Saving_variables_between_game_sessions (revid 5890180, 2023-12-11)
  - https://github.com/Stanzilla/WoWUIBugs/issues/414
  - https://github.com/Stanzilla/WoWUIBugs/issues/649
  - Live install /mnt/c/Program Files (x86)/World of Warcraft/_retail_/ (81 addon folders, 147 top-level .toc files)
  - Tier 3 clones under raw/addon-research/ — see §0 for commits
confidence: medium
---

# Module architecture and project layout

**Scope.** How to split an addon across files and objects, and which of those
choices the *game* constrains rather than taste. Load order and what it forces on
file-scope code; the `ns` namespace table; module-registration patterns; the
separation of state from presentation; and the three pressures that are specific
to this platform — the taint boundary, pooling, and the SavedVariables format.

What an addon *is* and how the client finds it belongs to `anatomy-and-runtime`.
Taint and secret values belong to `security-taint-and-restricted-data`.
Persistence formats belong to `state-persistence-and-communication`. This file
cites those areas only where they bend the *structure* of the code.

> **The honest headline.** WoW imposes surprisingly little structure. It gives
> you an ordered list of files, one private table per addon, and a global
> namespace. Everything above that — modules, prototypes, registries, mixins — is
> convention, and the conventions in the field disagree with each other. Where
> this file states a rule, the rule is anchored in Tier 1. Where it describes a
> pattern, it says how many of the surveyed codebases actually use it.

## 0. Citation conventions used in this file

| Prefix | Means |
|---|---|
| `[T1 src]` | Blizzard's shipped UI source. Paths relative to the `wow-ui-source` checkout root (prefix `raw/addon-research/wow-ui-source/`). Build **12.0.7.68887**, commit `4383ced30106`. |
| `[T1 docs]` | `Interface/AddOns/Blizzard_APIDocumentationGenerated/…` in that checkout — the machine-generated API spec. |
| `[T1 obs]` | Directly observed on the live install at `/mnt/c/Program Files (x86)/World of Warcraft/_retail_/`. Observation, not spec. |
| `[T2 wiki]` | warcraft.wiki.gg, with revid and last-edit date. Stamp is load-bearing; pages rot silently. |
| `[T2 bug]` | A WoWUIBugs issue. Evidence of *observed behaviour*; the `Acknowledged by Blizzard` label is evidence Blizzard agrees it is a bug. Never evidence of intended design. |
| `[T2 res]` | `Ketho/BlizzardInterfaceResources` @ `774b2c550366`, build **12.0.7.68256** — a *different build of the same patch*. |
| `[T3]` | A named community addon at a named commit. One data point, never a rule. |

**Tier 3 corpus surveyed here** (all `--depth 1`, all under `raw/addon-research/`):
WeakAuras2 `38d4bf1e6099` · BigWigs `3fdc10f6cfd1` · Details `e14de53cc2e1` ·
Plater `2b2ff463cccd` · ElvUI `f60934a174d6` · oUF `5672a3cb10e1` · Ace3
`4475787f06f7`. **Six addons, not seven independent opinions** — Details and
Plater share an author (Tercioo), and ElvUI vendors oUF, so their structural
choices are not independent. Counts below say "of the 6 addons surveyed".

> ⚠ **Nothing here has been run in the client.** Items that need that are marked
> `@verify-ingame` per this repo's convention.

> **Adversarial verification pass, 2026-07-23.** Every locator in this file was
> re-opened against the checkouts and URLs named above. Nine claims were changed:
> the `## Secure` restriction (§5.1, rule 17 — **not** on the wiki's restricted
> list), Plater's use of AceAddon-3.0 (§3.2 — it does not), the "7 abstract-method
> sites / rare, not a house style" finding (§4.2 — the grep was too narrow and the
> conclusion inverted), BigWigs' shipped addon count (§5.4 — 10, not 9), the
> `[Family]`/`[Game]` toc count (§1.3 — 28, not 23), the live-install dependency
> count (§1.4 — 109/147, not 111), the WeakAuras state→region call chain (§4.4 —
> an intermediate was missing), the CooldownViewer dirty-flag producer set (§4.3 —
> two cited producers belong to a different object), and `Mixin.lua`'s line 4→5.
> Each correction is marked inline at the point of use rather than silently
> applied. Everything else in the file reproduced exactly.

---

## 1. What the platform actually constrains

### 1.1 The `.toc` is an ordered list, and order is the whole contract

Files listed in a `.toc` load **in order, top to bottom**
`[T2 wiki: TOC format, revid 6767089, 2026-07-09, §File loading order]`. There is
no dependency resolution between files, no `require`, no forward declaration. A
file's top-level chunk executes the instant it is loaded.

The consequence that shapes every real addon: **anything a file evaluates at file
scope must already exist.** Blizzard's own Cooldown Manager is the cleanest
demonstration. `CooldownViewer.lua` composes a mixin *at file scope*:

```lua
CooldownViewerItemMixin = CreateFromMixins(CooldownViewerItemDataMixin, CooldownViewerVisualAlertTargetMixin);
```
`[T1 src: Interface/AddOns/Blizzard_CooldownViewer/CooldownViewer.lua:87]`

`CooldownViewerItemDataMixin` is created at
`[T1 src: .../CooldownViewerItemData.lua:3]` and
`CooldownViewerVisualAlertTargetMixin` in `CooldownViewerVisualAlertTarget.lua`.
The `.toc` therefore *must* list them earlier, and does — `.toc:11` (visual alert
target), `:20` (item data), `:25` (`CooldownViewer.lua`)
`[T1 src: Blizzard_CooldownViewer/Blizzard_CooldownViewer.toc:11,20,25]`.
Reorder those three lines and `CreateFromMixins` would be handed a `nil` where a
mixin table is expected. `[unverified]` — that the client errors rather than
silently producing an empty mixin is inference from the Lua `SecureMixin`
implementation (`for k, v in pairs(mixin)`, `Mixin.lua:30`); `Mixin` /
`CreateFromMixins` themselves are engine functions (§3.1) whose failure mode has
not been observed. `@verify-ingame`

Function *bodies* are not evaluated at load, so a function that references a
later-loaded global is fine. The constraint bites only on file-scope
expressions — mixin composition, `CreateFrame` calls, table literals that read
another file's value.

### 1.2 XML is a second, nestable ordering mechanism

An XML file may pull in more files: `<Script file="…"/>` and
`<Include file="…"/>` are both children of the root `<Ui>` element.
`Include`'s `file` attribute is **required**; `Script`'s is optional (a `<Script>`
may carry an inline body instead)
`[T1 src: Interface/AddOns/Blizzard_SharedXML/UI.xsd:1157-1166 (<Ui>), :1168-1176 (Include), :1177-1185 (Script)]`.
The wiki states the practical consequence: not every file needs to be in the
`.toc`, because XML can load them `[T2 wiki: TOC format, revid 6767089]`.

Two real strategies exist side by side in the field:

- **ElvUI puts one line in the `.toc`** — `Game\load_mainline.xml` — and that XML
  carries 182 `<Script>`/`<Include>` entries, the first of which is
  `Shared\General\Initialize.lua`
  `[T3: ElvUI@f60934a1 ElvUI/ElvUI_Mainline.toc:27 (its only content line — lines 1-25 are metadata); ElvUI/Game/load_mainline.xml:2; 180 <Script + 2 <Include = 182]`.
- **oUF ships a `.toc` whose only content line is `oUF.xml`**, and that XML lists
  all 41 Lua files in explicit order as 41 `<Script file="…"/>` entries between
  lines 2 and 44 (the file is 88 lines; the tail is a commented-out template)
  `[T3: oUF@5672a3cb oUF.toc:12 (only content line); oUF.xml:2-44]`.
- **BigWigs has zero XML files at all** — everything is `.toc`-ordered
  `[T3: BigWigs@3fdc10f6, 0 files matching *.xml]`.

Neither is more correct. The load-order *semantics* are identical; the difference
is where the list lives.

### 1.3 Per-line conditionals and path variables let one tree serve many clients

`.toc` file-reference lines accept trailing conditions
`[AllowLoad …]`, `[AllowLoadGameType …]`, `[AllowLoadTextLocale …]`, and
path variables `[Family]` (→ `Mainline`/`Classic`) and `[Game]` (→ `Standard`,
`Vanilla`, `TBC`, …)
`[T2 wiki: TOC format, revid 6767089, §Per-line conditional directives, §Per-file variables — file conditions added 11.1.5, metadata conditions added 12.0.7]`.

Blizzard uses this as a **shared-base-plus-override** file layout. `Blizzard_Menu`
loads `MenuTemplates.lua`, then `[Family]\MenuTemplates.lua` immediately after:

```
MenuTemplates.lua
MenuTemplates.xml
[Family]\MenuTemplates.lua
[Family]\MenuTemplates.xml
```
`[T1 src: Blizzard_Menu/Blizzard_Menu.toc:17-20]`

The flavour file then redefines the same global — `MenuStyle1Mixin` is assigned in
both `Mainline/MenuTemplates.lua:51` and `Classic/MenuTemplates.lua:34`, and only
one of the two ever loads `[T1 src]`. 23 of the 346 shipped `.toc` files use
`[Family]`; **28** use `[Family]` or `[Game]`
`[T1 src, counted: grep -rlE '\[Family\]|\[Game\]' --include=*.toc]`. (An earlier
draft of this file reported 23 for the "or" — that is the `[Family]`-only figure.)

### 1.4 Cross-addon order is `Dependencies`, and it is coarse

Within one addon you control order line by line. Across addons you get
`## Dependencies` / `## Dep` / `## RequiredDep` and nothing finer. 225 of the 346
shipped `.toc` files declare one `[T1 src, counted]`; **109** of the 147
top-level third-party `.toc` files on the live install do `[T1 obs, counted
2026-07-23]`. (An earlier draft said 111 — that is the count over all 185 `.toc`
files on the install, including nested embedded-library tocs, and so is not
"of 147".) Blizzard's own root of the dependency graph, `Blizzard_SharedXMLBase`,
is itself declared to depend on `Blizzard_ScriptErrors`
`[T1 src: Blizzard_SharedXMLBase/Blizzard_SharedXMLBase.toc:3]`.

Resolution and failure semantics are the `anatomy-and-runtime` topic's; the
structural consequence here is an **inference**, not a cited rule: if module A's
file-scope code reads a symbol from addon B, addon B must be a declared
dependency, and the reference must not be at file scope unless it is. `[gap]`
I found no Tier-1 or Tier-2 statement of the load-ordering guarantee *between*
addons; the wiki's `TOC format` page documents the directives but not the
resolution order.

### 1.5 SavedVariables load *after* your files — unless you opt out

By default the client loads an addon's SavedVariables **after all of its script
files have run**, then fires `ADDON_LOADED`
`[T2 wiki: Saving variables between game sessions, revid 5890180, 2023-12-11, §The loading process]`.
This is the single biggest reason addon initialisation is split into
"construct at file scope / configure on `ADDON_LOADED`".

Since 11.1.5 there is `## LoadSavedVariablesFirst: 1`, which loads the SV files
*before* the first script file
`[T2 wiki: TOC format, revid 6767089, §LoadSavedVariablesFirst; §Patch changes lists it under 11.1.5]`.
It originated as WoWUIBugs #414, labelled `Acknowledged by Blizzard`, closed
2025-03-07 `[T2 bug: Stanzilla/WoWUIBugs#414]`.

**Adoption is thin.** 2 of the 346 shipped Blizzard `.toc` files use it
(`Blizzard_DamageMeter`, `Blizzard_SettingsDefinitions_Shared`) `[T1 src, counted]`,
and 2 of the 81 addons on the live install (BigWigs, DragonRider) `[T1 obs, counted]`.
So the "defer init to `ADDON_LOADED`" shape is still the overwhelming norm — not
because it is better, but because it is the default.

---

## 2. The `ns` namespace table

### 2.1 What it is

Every Lua file in an addon is called with two varargs: the addon name and a table
private to that addon and shared between its files.

```lua
local addonName, ns = ...
```
`[T2 wiki: Using the AddOn namespace, revid 6474636, 2025-09-16 — "The addon namespace is a private table shared between Lua files in the same addon"]`

⚠ That wiki page is nearly a year old and its only "Patch changes" entry is
3.3.0. It is stable, well-corroborated material, but it is Tier 2 and stale-ish;
the corroboration below is Tier 1.

### 2.2 Blizzard uses it, but sparingly — and mostly for *secure* plumbing

31 of the 2298 Lua files in the shipped UI source bind the vararg
`[T1 src, counted: grep -rl --include=*.lua -E '^local [A-Za-z_, ]+= *\.\.\.']`.
That grep is a **lower bound** — it only catches the `local a, b = ...` form at
column 0, not e.g. `local ns = select(2, ...)`. Blizzard's own comments say what
it is for:

- `-- Used for passing functions between UIParentPanelManager.lua and other files in this addon.`
  `[T1 src: Blizzard_UIParentPanelManager/Shared/UIParentPanelManager.lua:1]`
- `-- Used to store secure functions (and associated data) that need to be called by other addons (to prevent hooking)`
  `[T1 src: Blizzard_CombatAudioAlerts/Blizzard_CombatAudioAlertManager.lua:1]`
- `-- Used for passing RESTRICTED_FUNCTIONS_SCOPE.`
  `[T1 src: Blizzard_RestrictedAddOnEnvironment/RestrictedEnvironment.lua:12]`

The overwhelming majority of Blizzard's cross-file wiring is instead **plain
globals** — 3201 distinct `*Mixin` global tables carrying 25054 methods
`[T1 src, counted: grep -rhoE '^function [A-Za-z_]+Mixin:[A-Za-z_]*\(' --include=*.lua
→ 25054. Quote the pattern with the number — the looser '^function [A-Za-z_]+Mixin:'
gives 25076, so 25054 is only reproducible with the trailing paren group]`. That is
the actual Blizzard convention. `[unverified]` — the clause "and it is the opposite
of what most community style advice says" was uncited and has been cut; no survey
of community style advice was done.

### 2.3 Community usage is heavier, and varies a lot

| Addon | `.lua` files | files binding `...` |
|---|---:|---:|
| oUF | 41 | **41** |
| WeakAuras2 | 198 | 128 |
| BigWigs | 131 | 54 |
| ElvUI | 680 | 55 |
| Plater | 185 | 34 |
| Details | 326 | **111** ⚠ corrected — was 8 |
| Ace3 | 74 | **0** |

`[T3, counted across the clones named in §0]`

> ⚠ **Corrected 2026-07-23 (cross-file reconciliation).** The Details row read
> **8**. That number was a **regex artefact, not a finding**: the grep quoted
> above (`^local [A-Za-z_, ]+= *\.\.\.`) has no digits in its character class, and
> Details' namespace local is spelled **`Details222`** — so 103 of its 111 binding
> files were silently excluded. Re-counted with
> `grep -rlE '^local [A-Za-z_][A-Za-z0-9_]*[[:space:]]*,[[:space:]]*[A-Za-z_][A-Za-z0-9_]*[[:space:]]*=[[:space:]]*\.\.\.'`:
> **111 of 326** (`local addonName, Details222 = ...` ×94, `local _, Details222 = ...`
> ×6, `local tocName, Details222 = ...` ×2, `local addonId, edTable = ...` ×5, …).
>
> **The remaining divergence with `anatomy-and-runtime.md` §5.2 is real and is
> not an error in either file.** That file uses a **two-identifier** regex and so
> reports **WeakAuras2 = 7**, where this table says 128 — because WeakAuras spells
> it `local AddonName = ...` (119 files) plus `local AddonName, TemplatePrivate =
> ...` (7). Both counts reproduce exactly. They measure different *spellings* of
> the same mechanism, so **neither is "the" adoption figure** — always cite the
> regex alongside the count. Verified 2026-07-23:
> two-identifier regex → oUF 41 · Details 111 · BigWigs 54 · ElvUI 55 · Plater 34 ·
> WeakAuras2 **7** · Ace3 0; this section's regex → oUF 41 · Details **8** ·
> BigWigs 54 · ElvUI 55 · Plater 34 · WeakAuras2 **128** · Ace3 0.
> The table above reports the *union* reading (widest correct count per addon).

Ace3 is 0 because its modules are designed to be **embedded into a host addon's
folder**, where `...` would hand them the *host's* namespace, not their own; it
uses LibStub for cross-copy version resolution instead (§3.4). Note the earlier
claim that "a library has no addon folder of its own" is wrong as stated — Ace3
does ship a standalone `Ace3.toc` (`## Title: Lib: Ace3`)
`[T3: Ace3@4475787f Ace3.toc:4]`.

### 2.4 Two real idioms built on it

**Bracketing a private scope by load order.** oUF's first-loaded file creates the
namespace and a `Private` sub-table; its last-loaded file deletes `Private`:

```lua
-- init.lua (first <Script> in oUF.xml)
local _, ns = ...
ns.oUF = {}
ns.oUF.Private = {}

-- finalize.lua (last <Script> in oUF.xml)
local _, ns = ...
-- It's named Private for a reason!
ns.oUF.Private = nil
```
`[T3: oUF@5672a3cb init.lua:1-3, finalize.lua:1-4, ordering at oUF.xml:2 and :44]`

This works *only* because of §1.1 file ordering. It is elegant and it is also
brittle: adding a file after `finalize.lua` silently loses access.

**Exporting the namespace as a global.** ElvUI binds the vararg, fills it, and
publishes it:

```lua
local AddOnName, Engine = ...
local E = AceAddon:NewAddon(AddOnName, 'AceConsole-3.0', 'AceEvent-3.0', 'AceTimer-3.0', 'AceHook-3.0')
...
Engine[1] = E; Engine[2] = {}; Engine[3] = E.privateVars.profile
Engine[4] = E.DF.profile; Engine[5] = E.DF.global
_G.ElvUI = Engine
```
`[T3: ElvUI@f60934a1 ElvUI/Game/Shared/General/Initialize.lua:40 (vararg), :41 (NewAddon), :65-70]`

with the header comment documenting the consumer contract:
*"To load the AddOn engine inside another addon add this to the top of your file:
`local E, L, V, P, G = unpack(ElvUI)`"*
`[T3: ElvUI@f60934a1 ElvUI/Game/Shared/General/Initialize.lua:1-5]`.

### 2.5 The sanctioned cross-addon export: `AllowAddOnTableAccess`

Since 11.1.7 an addon can opt in to letting other addons read its namespace table:

```
## AllowAddOnTableAccess: 1
```

read back with `C_AddOns.GetAddOnLocalTable(name)`. Blizzard's own documentation
string:

> *"Returns the addon table (passed as the second argument of `...` to files) for
> any addon that opts in through setting `AllowAddOnTableAccess: 1` in the toc
> file. Insecure code cannot query addon tables from Blizzard addons."*

`[T1 docs: AddOnsDocumentation.lua:149 (`Name = "GetAddOnLocalTable"`), :152 (the `Documentation` string quoted above)]` ·
`[T2 wiki: TOC format, revid 6767089, §AllowAddOnTableAccess; added 11.1.7]`

Real-world adoption at 12.0.7 is minimal: **1** of 346 shipped Blizzard `.toc`
files (`Blizzard_CombatAudioAlerts.toc:6`) `[T1 src]`, **1** of the 147
third-party `.toc` files on the live install (`DandersFrames.toc:12`) `[T1 obs]`,
and **0** of the 6 addons surveyed `[T3, counted]`. The `_G.ElvUI = Engine`
idiom (§2.4) remains what people actually do.

### 2.6 The gap the namespace does not close

**SavedVariables must be named globals.** `## SavedVariables` takes "a
comma-delimited list of variable names in the global environment"
`[T2 wiki: Saving variables between game sessions, revid 5890180]`. So an addon
that keeps everything in `ns` still has to expose exactly its persisted tables as
globals, and reconnect them at `ADDON_LOADED`. This is a known irritant: WoWUIBugs
#649 *"Private addon storage"* (open, `Feature Request`, filed 2024-09-02) asks
for a third vararg carrying the SV table so that no global is needed
`[T2 bug: Stanzilla/WoWUIBugs#649]`. It has not shipped as of 12.0.7 — the wiki's
TOC-format patch list runs to 12.0.7 with no such field
`[T2 wiki: TOC format, revid 6767089, §Patch changes]`.

---

## 3. Module registration: four patterns, none of them mandated

### 3.1 Blizzard: global mixin tables, wired declaratively in XML

A "module" in Blizzard's UI is a global table of methods named `<Thing>Mixin`,
attached to a frame either in Lua (`Mixin(obj, …)`) or in XML via the `mixin`
attribute.

**`Mixin` and `CreateFromMixins` are engine functions at 12.0.7, not Lua.** Both
appear in the generated docs under the `FrameScript` system, each annotated
`SecureHooksAllowed = false`:

```
CreateFromMixins(mixins: LuaValueVariant) -> object: LuaValueVariant   [SecureHooksAllowed=False]
Mixin(object: LuaValueVariant, mixins: LuaValueVariant) -> outObject   [SecureHooksAllowed=False]
```
`[T1 docs: FrameScriptDocumentation.lua:82 (CreateFromMixins), :279 (Mixin)]`

Neither has a Lua definition anywhere in the shipped source — `Mixin.lua` is 48
lines and *consumes* them (`local PrivateMixin = Mixin;` at **line 5**, not line 4
as an earlier draft said; line 4 is blank), defining only
`CreateAndInitFromMixin`, `CreateSecureMixinCopy`, `SecureMixin`, and
`CreateFromSecureMixins` `[T1 src: Blizzard_SharedXMLBase/Mixin.lua:1-48]`.
Corroborated at a nearby build: both names are listed in `GlobalAPI.lua`, not
`FrameXML.lua` `[T2 res: Resources/GlobalAPI.lua:4842, :5890, build 68256]`.
**[gap]** I could not date the move to C — searched the wiki's
`Patch 12.0.0 / 12.0.5 / 12.0.7 API changes` pages for `Mixin` and
`CreateFromMixins` and found no entry.

`SecureMixin` and `CreateFromSecureMixins` **return early and do nothing** when
`issecure()` is false `[T1 src: Blizzard_SharedXMLBase/Mixin.lua:24-26, :43-45]`.
Addon code should assume those two are unavailable to it.

The XML side of the same mechanism is Tier-1 schema:
`mixin`, `secureMixin`, `parentKey`, `parentArray` and `inherits` are all
attributes of the `LayoutFrameAttributes` group
`[T1 src: Blizzard_SharedXML/UI.xsd:468-476 — inherits :472, mixin :473, secureMixin :474, parentKey :470, parentArray :471]`,
and `mixin` accepts a comma-separated list:

```xml
<GameTooltip name="PrivateAurasTooltip" mixin="GameTooltipDataMixin, PrivateAurasTooltipMixin" …>
```
`[T1 src: Blizzard_PrivateAurasUI/Mainline/PrivateAurasTooltip.xml:4]`

`parentKey="Icon"` on a child region is what makes `self.Icon` exist for the
mixin's methods, with no Lua glue
`[T1 src: Blizzard_CooldownViewer/CooldownViewer.xml:28 (Icon), :48 (Cooldown)]`.

**This declarative style is essentially Blizzard-only.** `parentKey="` appears
17706 times across Blizzard's XML `[T1 src, counted]`; across the 105 XML files in
the 6 surveyed addons it appears 57 times and `mixin="` 4 times
`[T3, counted: WeakAuras 20/3, Details 33/0, Plater 4/1, BigWigs 0/0 (no XML at all), ElvUI 0/0, oUF 0/0]`.
Community addons build frames in Lua.

### 3.2 Ace3 `AceAddon-3.0`: a lifecycle + module tree

The library ships the most explicit module contract in the ecosystem. It
documents three optional callbacks:

> *"**OnInitialize**, which is called directly after the addon is fully loaded. ·
> **OnEnable** which gets called during the `PLAYER_LOGIN` event … · **OnDisable**,
> which is only called when your addon is manually being disabled."*
`[T3: Ace3@4475787f AceAddon-3.0/AceAddon-3.0.lua:5-7]`

The dispatcher is a single frame registered for `ADDON_LOADED` and `PLAYER_LOGIN`
that drains an `initializequeue` then an `enablequeue`
`[T3: Ace3@4475787f AceAddon-3.0/AceAddon-3.0.lua:611-634, frame registration at :632-634]`. Enqueueing happens
inside `NewAddon` `[T3: :136-137]`.

Checkable contracts inside it:

- `NewAddon` **errors** on a duplicate name `[T3: :115]`.
- `NewModule` **errors** on a duplicate module name within a parent `[T3: :235]`.
- A module *is* an addon: `NewModule` calls `AceAddon:NewAddon("<Parent>_<Name>")`
  internally, so modules land in the same init queue and are therefore initialised
  after their parent `[T3: :239, with the reasoning in the comment at :237-238]`.
- Modules inherit their parent's `defaultModuleState`, `defaultModuleLibraries`
  and `defaultModulePrototype` `[T3: :242, :250, :252-258]`.
- Every optional callback is invoked through `safecall`, so a module that errors
  in `OnEnable` does not abort the others `[T3: :494, :523, :558]`.
- It maintains a hard-coded skip-list of Blizzard addons that "load very early …
  and mess with Ace3 addon loading" `[T3: :600-608]` — a load-order workaround
  preserved in a comment dated 2020-08-28 `[T3: :612]`.

Of the 6 addons surveyed, **2 build on `AceAddon-3.0`**: ElvUI
(`AceAddon:NewAddon(AddOnName, …)` at `ElvUI/Game/Shared/General/Initialize.lua:41`)
and Details (`boot.lua:9`, `LibStub("AceAddon-3.0"):NewAddon("_detalhes", …)`) `[T3]`.

⚠ **Correction.** An earlier draft counted Plater as a third, citing
`plater/libs/DF/addon.lua:155`. That line is inside DetailsFramework's
`detailsFramework:CreateAddOn`, which its own comment marks *"deprecated, you
should always prefer using `CreateNewAddOn`"* `[T3: plater@2b2ff463
libs/DF/addon.lua:152-155]`, and **no file outside `plater/libs/` calls
`CreateAddOn` or `NewAddon`** `[T3, counted: grep -rn 'CreateAddOn\|NewAddon'
--include=*.lua over plater/, excluding libs/ → 0 call sites]`. Plater *vendors*
Ace3 libraries; it does not build its addon object on `AceAddon-3.0`.
BigWigs, WeakAuras and oUF have zero `NewAddon` hits at all `[T3, counted]`.

ElvUI's shape is worth naming because it inverts §1.1: it declares **24 modules
eagerly in one file**, `E.ActionBars = E:NewModule('ActionBars', …)` and so on
`[T3: ElvUI/Game/Shared/General/Initialize.lua:72 onward — 24 E:NewModule( calls
in the file]`, and
the implementation files loaded later fetch them back with
`local AB = E:GetModule('ActionBars')`
`[T3: e.g. ElvUI/Game/Shared/Modules/ActionBars/Bind.lua:2]`. The registry is
populated before any consumer exists, so file order among consumers stops
mattering.

### 3.3 Roll-your-own registries: three different shapes

**BigWigs — prototype tables passed through the namespace.** The boss and plugin
base classes are plain tables handed around via `ns`:

```lua
local boss = {}
local core, plugins
do
	local _, tbl =...
	core = tbl.core
	plugins = tbl.plugins
	tbl.bossPrototype = boss
end
```
`[T3: BigWigs@3fdc10f6 Core/BossPrototype.lua:20-27; the mirror image at Core/PluginPrototype.lua:6-14]`

Instances are created by `core:NewBoss(moduleName, zoneId, journalId)`
`[T3: Core/Core.lua:447]` over a metatable
`{ __index = bossPrototype, __metatable = false }` `[T3: Core/Core.lua:441]` —
note `__metatable = false`, which blocks `getmetatable`/`setmetatable` tampering.
`core:RegisterPlugin` errors on an unknown or already-registered name
`[T3: Core/Core.lua:736, :738]`.

⚠ The two registration paths differ, and the difference matters for §3.3's
"duplicates are an error" claim: `core:NewBoss` on a duplicate name **prints**
(`core:Print(bossAlreadyRegistered:format(moduleName))`) and returns, it does not
raise `[T3: Core/Core.lua:447-449]`. Only `RegisterPlugin` errors.

**WeakAuras — typed registries with duplicate rejection.**
`Private.RegisterRegionType(name, createFunction, modifyFunction, default, properties, validate)`
type-checks its **first four** arguments and errors if the region type is already
defined `[T3: WeakAuras2@38d4bf1e WeakAuras/WeakAuras.lua:433-463; duplicate check
at :452, its error at :453]`. Not "every argument": `properties` and `validate` are
never checked, and the branch at `:450` that reads as the `properties` check
re-tests `default` (`type(default) ~= "table" and type(default) ~= "nil"`) while
raising a message about `properties` — an evident copy-paste bug, and dead code
because `:448` already rejected a non-table `default`.
The registry table is `Private.regionTypes`, commented
*"One table per regionType, see RegisterRegionType, notable properties: create,
modify and default"* `[T3: WeakAuras.lua:315-317]`.

**oUF — a four-function element contract.**

```lua
function oUF:AddElement(name, update, enable, disable)
```
with `argcheck` on each and an error on re-registration:
`'Element [%s] is already registered.'`
`[T3: oUF@5672a3cb ouf.lua:1002-1013; duplicate check at :1008]`.
Each of the 31 files in `elements/` self-registers at load
`[T3: oUF/elements/ — 31 files, all listed in oUF.xml:12-42]`.

The common thread across all three, and across Ace3: **registration is by unique
string name, and a duplicate is rejected rather than silently overwriting.** That
is a convention with 4 instances (Ace3, BigWigs, WeakAuras, oUF) — but note the
rejection is not uniformly an `error()`: BigWigs' `NewBoss` prints and returns
(above), while Ace3, WeakAuras, oUF and BigWigs' `RegisterPlugin` raise. Also,
the 4 are not fully independent votes: ElvUI and Details inherit Ace3's behaviour
rather than choosing it. It is not a platform rule.

### 3.4 LibStub: the versioned-singleton contract

Shared libraries do not use the namespace table (they have no folder of their
own when embedded). They use LibStub, 30 lines, public domain:

```lua
function LibStub:NewLibrary(major, minor)
	...
	local oldminor = self.minors[major]
	if oldminor and oldminor >= minor then return nil end
	self.minors[major], self.libs[major] = minor, self.libs[major] or {}
	return self.libs[major], oldminor
end
```
`[T3: Ace3@4475787f LibStub/LibStub.lua:11-19]`

Two structural consequences that are checkable:

1. `NewLibrary` returns **nil** when an equal-or-newer minor is already
   registered `[T3: LibStub.lua:16]`. Library code that does not bail on nil will
   crash indexing nil.
2. On a genuine upgrade the **same table** is returned (`self.libs[major] or {}`)
   `[T3: LibStub.lua:17]`. The newer copy therefore mutates the older one in
   place. Any state or upvalue captured by the old version survives and must be
   re-bound — which is why mature libraries re-read their own state at the top of
   the file rather than re-initialising it.

`GetLibrary` errors if the library is absent unless `silent` is passed
`[T3: LibStub.lua:21-26]`, and `LibStub("Name")` is `GetLibrary` via
`__call` `[T3: LibStub.lua:29]`.

⚠ The `.pkgmeta` externals mechanism means **library source is not in the addon's
git repo** — it is resolved at package time. A clone of WeakAuras contains no
`WeakAuras/Libs/` at all. Grepping a clone and finding no LibStub is not evidence
the addon does not use it. See `libraries-and-ecosystem`.

---

## 4. Separating state from presentation

### 4.1 The CooldownViewer data-mixin / display-mixin split — verified

The claim was that Blizzard's Cooldown Manager item demonstrates a data-mixin vs
display-mixin split. **It does, and it is the strongest Tier-1 example available.**
Here is exactly what is true.

`CooldownViewerItemDataMixin` lives alone in its own 563-line file and owns the
*resolution* of what a cooldown item is: cooldown ID, base/override/linked spell,
aura instance, totem slot, charge and cooldown info, texture and name lookups,
valid alert types
`[T1 src: Blizzard_CooldownViewer/CooldownViewerItemData.lua:3-563]`.

It is consumed by **two independent display layers**:

| Display mixin | Composition site |
|---|---|
| `CooldownViewerItemMixin` (the on-screen HUD item) | `CreateFromMixins(CooldownViewerItemDataMixin, CooldownViewerVisualAlertTargetMixin)` `[T1 src: CooldownViewer.lua:87]` |
| `CooldownViewerSettingsItemMixin` (the settings/edit UI item) | `CreateFromMixins(CooldownViewerItemDataMixin, CooldownViewerBaseReorderTargetMixin, CooldownViewerVisualAlertTargetMixin)` `[T1 src: CooldownViewerSettings.lua:161]` |

That is the payoff — **one data mixin, two presentations** — and it is why the
split exists rather than being ornamental.

The separation is real but not absolute. The data file touches a widget exactly
twice, and both times it is the *shared* `GameTooltip`, never its own regions:
`tooltip:Show()` at `:508` and `GetAppropriateTooltip():Hide()` at `:512`
`[T1 src, counted with the pattern
`:Show\(\)|:Hide\(\)|:SetTexture|:SetAtlas|:SetText|:SetPoint|:SetShown|:SetAlpha|:SetDesaturated|GameTooltip_`
→ **3** hits in `CooldownViewerItemData.lua` (the two above plus the anchor call)
against **34** in `CooldownViewer.lua`. An earlier draft said "2 vs 36" without
recording its grep; that pair is not reproducible]`.
It also calls `GameTooltip_SetDefaultAnchor(tooltip, self)` at `:501`, which
presumes `self` *is* a frame. So the honest description is: **the data mixin
never touches the item's own regions, but it does assume it will be mixed into
a frame.** It is not a headless model object.

There is no `super`. A derived mixin that extends a base method calls the base
explicitly with `self`:

```lua
function CooldownViewerItemMixin:OnCooldownIDSet()
	CooldownViewerItemDataMixin.OnCooldownIDSet(self);
	self:RefreshAlerts();
end
```
`[T1 src: CooldownViewer.lua:461-464; same idiom at CooldownViewerSettings.lua:299 and :305]`

### 4.2 `RefreshData()` is a declared abstract, not a naming habit

The data mixin does not implement its own refresh — it **asserts**:

```lua
function CooldownViewerItemDataMixin:RefreshData()
	assertsafe(false, "RefreshData must be overridden by a derived mixin.");
end
```
`[T1 src: CooldownViewerItemData.lua:496-498]`

Both display layers implement it — `CooldownViewerCooldownItemMixin:RefreshData`
at `[T1 src: CooldownViewer.lua:1136]` and
`CooldownViewerSettingsItemMixin:RefreshData` at
`[T1 src: CooldownViewerSettings.lua:163]`.

⚠ **Corrected.** An earlier draft claimed the abstract-method idiom "appears at
exactly 7 sites … it is rare, not a house style." That was an artefact of grepping
two literal phrases (`must be overridden|must be implemented`), and it is wrong in
both directions:

- Those 7 hits are not all the same idiom. Four are `error(…)`, not `assert`
  `[T1 src: Blizzard_SharedXML/TemplatedList.lua:243,248,253,258]`; one is
  `assert(false, …)` `[T1 src: Blizzard_EncounterTimeline/EncounterTimelineFrameManager.lua:43]`;
  two are `assertsafe(false, …)` `[T1 src: Blizzard_CooldownViewer/CooldownViewerItemData.lua:497;
  Blizzard_EncounterTimeline/EncounterTimelineView.lua:224]`.
- The phrase grep **missed** at least one runtime-enforced abstract:
  `function QuestSessionDialogMixin:Confirm() assert(false); -- implement this in
  derived mixin end` `[T1 src: Blizzard_FrameXML/QuestSession.lua:176]`.
- **Declaring abstracts is common; enforcing them at runtime is rare.** 137 lines
  in the shipped source are a bare comment telling a derived mixin to implement or
  override the method `[T1 src, counted: grep -rniE
  '^\s*--\s*(Override|Implement)[a-z]* (this )?(in|by) (your )?(derived|overriding)? ?mixins?'
  --include=*.lua]` — concentrated in `Blizzard_SharedTalentUI/Blizzard_TalentDisplay.lua`,
  `Blizzard_TalentButtonBase.lua`, `Blizzard_UnitFrame/Mainline/AlternatePowerBarBase.lua`
  and `Blizzard_MapCanvas/MapCanvas_DataProviderBase.lua`.

So the supportable statement is narrower: **Blizzard declares abstract mixin
methods routinely, but almost never makes calling one a runtime error** — roughly
8 enforced sites against 137 comment-only ones. `RefreshData` is one of the
enforced few.

Likewise, `*DataMixin` as a naming convention has exactly **two** instances in the
whole source: `CooldownViewerItemDataMixin` and `GameTooltipDataMixin`
`[T1 src, counted: distinct globals matching ^function <Name>DataMixin:]`.
Two of two expose a `RefreshData()` entry point
`[T1 src: CooldownViewerItemData.lua:496; Blizzard_GameTooltip/Mainline/GameTooltip.lua:955]` —
which is a suggestive corroboration at n=2, and nothing more.

Zoomed out, `Refresh*` is 513 of the 25054 mixin methods in the source, against
2054 `Update*` `[T1 src, counted: grep -rhoE
'^function [A-Za-z_]+Mixin:(Refresh|Update)[A-Za-z]*\(' --include=*.lua]`. **"An idempotent `Refresh` is the norm" is not
supportable.** What *is* supportable: where Blizzard formalises a data/display
seam, the seam is a `RefreshData()` that the display side implements.

### 4.3 The dirty-flag drain, which is what makes refresh idempotent in practice

Both `*DataMixin` consumers pair the refresh entry point with a dirty flag so it
runs at most once per frame regardless of how many events set it. Note where the
flag lives in the CooldownViewer case: on `CooldownViewerItemMixin`, the *display*
mixin (`CooldownViewer.lua:113`), not on the data mixin — the data mixin declares
`RefreshData` and nothing else about scheduling.

```lua
function CooldownViewerItemMixin:MarkDirty()  self.needsFullRefresh = true;  end
function CooldownViewerItemMixin:IsDirty()    return self.needsFullRefresh;  end
function CooldownViewerItemMixin:Clean()
	if self.needsFullRefresh then
		self.needsFullRefresh = false;
		self:RefreshData();
	end
end
```
`[T1 src: CooldownViewer.lua:113-126 — MarkDirty :113, IsDirty :117, Clean :121]`
(the snippet above is reflowed; the source spaces the three onto separate lines).

The drain happens in one `OnUpdate`:

```lua
if self:IsDirty() then self:Clean(); else self:RefreshCooldownInfo(); end
```
`[T1 src: CooldownViewer.lua:1365-1366]`. ⚠ Be precise about scope: that is the
**only** `IsDirty`/`Clean` drain in the whole addon, and it lives in
`CooldownViewerBuffBarItemMixin:OnUpdate` (`:1360`), not in the base item's
`OnUpdate` `[T1 src, counted: `grep -n 'IsDirty\|MarkDirty\|Clean()'` over
`Blizzard_CooldownViewer/*.lua` → 12 hits, one drain]`. The single producer for
that flag is `:1194`.

An earlier draft also listed `CooldownViewerSettingsDataProvider.lua:18, :169` as
"producers on the settings side". They are producers for a **different** dirty
flag on a different object — `CooldownViewerSettingsDataProviderMixin` has its own
`MarkDirty`/`IsDirty` at `:210`/`:214` `[T1 src]`. Same shape, separate mechanism;
they do not feed `CooldownViewerItemMixin:Clean`.

`GameTooltipDataMixin` does the same with `shouldRefreshData` /
`RefreshDataNextUpdate()` — and note its `RefreshData` clears its own flag rather
than a separate `Clean` doing it
`[T1 src: Blizzard_GameTooltip/Mainline/GameTooltip.lua:955-958 (RefreshData, clears at :956),
:960-963 (RefreshDataNextUpdate), :965-972 (the OnEvent producer)]`.

`MarkDirty` is **defined** on 23 distinct mixins in the source `[T1 src, counted:
grep -rhoE '^function [A-Za-z_]+Mixin:MarkDirty\(' --include=*.lua → 23]` (289
total textual occurrences, most of them call sites).
Blizzard also ships a generic incremental driver, `CreateObjectUpdater(data,
updateFunc, isCompleteFunc, finishFunc)`, which runs `updateFunc` on a 0.01s
ticker until `isCompleteFunc` returns true
`[T1 src: Blizzard_SharedXMLBase/ObjectUpdater.lua:5-12, :38-58]`.

### 4.4 WeakAuras: the same seam, at a much larger scale

WeakAuras is the second data point, and it is structured as an explicit pipeline
rather than a mixin composition. Its comment states the contract:

> *"Trigger State, updated by trigger systems, then applied to regions by
> `UpdatedTriggerState` … Notable properties: **changed**: Whether this trigger
> state was recently changed and its properties need to be applied to a region.
> The glue code resets this after syncing the region to the trigger state."*

`[T3: WeakAuras2@38d4bf1e WeakAuras/WeakAuras.lua:336-345]`

The registries are separate tables keyed by type: `Private.regionTypes`,
`Private.subRegionTypes`, `Private.regionOptions`, `Private.subRegionOptions`,
`Private.triggerTypes`, `Private.triggerTypesOptions`
`[T3: WeakAuras.lua:316, :319, :323, :326, :330, :334 — an earlier draft cited
":315-330", which excludes `triggerTypesOptions` at :334]`. Region construction
is `regionTypes[regionType].create(WeakAurasFrame, data)` followed by
`regionTypes[regionType].modify(parent, region, data)`
`[T3: WeakAuras.lua:3421, :3453]`, with a validity check against the type's
declared defaults in between `[T3: :3439]`.

The single seam where state becomes pixels is one small function:

```lua
local function ApplyStateToRegion(id, cloneId, region, parent)
	region.values.customTextUpdated = false
	region:Update()
	region.subRegionEvents:Notify("Update", region.state, region.states)
	UpdateMouseoverTooltip(region)
	region:Expand()
	if parent and parent.ActivateChild then parent:ActivateChild(id, cloneId) end
end
```
`[T3: WeakAuras.lua:4886-4898]`

⚠ The chain has an intermediate the earlier draft omitted. `ApplyStateToRegion`
has exactly **one** call site, `:4986`, inside `ApplyStatesToRegions(id,
activeTrigger, states)` at `:4944`; *that* is what `Private.UpdatedTriggerState`
calls, at `:5101` and `:5122` `[T3: WeakAuras.lua:4886, :4944, :4986, :5025, :5101, :5122]`.
So the seam is `UpdatedTriggerState → ApplyStatesToRegions → ApplyStateToRegion`,
and the `changed`-flag test that gates it is `applyChanges` — set at `:4977-4979`
(`… or (triggerState and triggerState.changed)`), tested at `:4985`.

`Private.UpdatedTriggerState` `[T3: WeakAuras.lua:5025]` is called from **13**
sites: 7 in `WeakAuras.lua` (`:1483, :3232, :4728, :4745, :4773, :4791, :4876`),
5 in `GenericTrigger.lua` (`:956, :1014, :1031, :1093, :1216`) and 1 in
`BuffTrigger2.lua` (`:2004`) `[T3, counted]`. (The earlier draft said "8+" while
listing 7 — the list was WeakAuras.lua-only.) **That many callers is precisely why
the entry point must be safe to call repeatedly** — the `changed` flag is what
makes that true.

So: two independent codebases (Blizzard's CooldownViewer, WeakAuras), two
different mechanisms (mixin composition, registry pipeline), same shape —
*mutable state table → flag → single re-entrant apply function → widgets*.
Two data points. Not a rule.

---

## 5. Pressure that is specific to this platform

These are the three things that make WoW addon structure different from ordinary
application structure. Everything in §5 is Tier 1.

### 5.1 The taint boundary splits code at the file and addon level

Blizzard's own answer to "this code must stay secure" is not a function
attribute — it is a **separate file, or a separate addon.**

- **Separate file, loaded into a different environment.** The `.toc` supports a
  per-file `[LoadIntoEnvironment secure]` condition:
  ```
  Shared\ChatFrameFiltersSecure.lua [LoadIntoEnvironment secure]
  ```
  `[T1 src: Blizzard_ChatFrameBase/Blizzard_ChatFrameBase_Mainline.toc:18; also Blizzard_RestrictedAddOnEnvironment/Blizzard_RestrictedAddOnEnvironment.toc:7]`
  The file that lands there is 9 lines long and exists purely to build one
  secure object, with the reason in a comment:
  > *"This function is required to always execute securely because chat message
  > event filters are stored in lazily-created arrays (one per chat event) and we
  > need to ensure that the first registration of a filter doesn't taint all other
  > filters -or- spread taint back to the chat frame."*
  `[T1 src: Blizzard_ChatFrameBase/Shared/ChatFrameFiltersSecure.lua:1-9]`
  There is a converse condition too, `[AllowLoadEnvironment …]`, in **8 shipped
  `.toc` files across 7 addons** (`Blizzard_SharedXML` has two flavour tocs)
  `[T1 src, counted: Blizzard_CooldownViewer, Blizzard_ObjectiveTracker,
  Blizzard_ScriptErrors, Blizzard_EditMode, Blizzard_CUFProfiles,
  Blizzard_SharedXML (×2), Blizzard_UIParentPanelManager]`. The argument's case is
  not consistent in Blizzard's own files — `Global` at
  `Blizzard_EditMode/Blizzard_EditMode.toc:3-21`, lowercase `global` at
  `Blizzard_CooldownViewer/Blizzard_CooldownViewer.toc:28` `[T1 src]`. `[gap]`
  Whether the parser is case-insensitive is not established.
  **[gap]** Neither `LoadIntoEnvironment` nor `AllowLoadEnvironment` appears on
  the wiki's `TOC format` page (revid 6767089, 2026-07-09), whose per-line
  conditional table lists only `AllowLoad`, `AllowLoadGameType` and
  `AllowLoadTextLocale`. I have no evidence third-party addons may use them, and
  zero uses in the live install's 147 third-party `.toc` files. Treat as
  Blizzard-internal until proven otherwise. `@verify-ingame`

- **Separate addon.** `## UseSecureEnvironment: 1` loads *every* file of an addon
  into a private function environment — 13 shipped `.toc` files set it, and 5 set
  `## Secure: 1` `[T1 src, counted]`. (`[unverified]` — an earlier draft called
  `Secure` "the older" of the two; I found nothing dating either directive.)
  Blizzard has split whole features in
  two along this line: `Blizzard_Communities` / `Blizzard_CommunitiesSecure` and
  `Blizzard_ClassTrial` / `Blizzard_ClassTrialSecure` both exist as sibling
  addons `[T1 src: 4 directories under Interface/AddOns/]`.

  ⚠ **Only one of the two is documented as restricted.** The wiki's §Restricted
  reads *"The following tags are inaccessible to third-party AddOns"* and lists
  exactly five: `AllowLoad`, `EscalateErrorDuringLoad`, `LoadFirst`,
  `SavedVariablesMachine`, `UseSecureEnvironment`
  `[T2 wiki: TOC format, revid 6767089, 2026-07-09, §Restricted]`. **`Secure` is
  not on that list, and the page does not document a `## Secure` tag at all** — an
  earlier draft asserted it was restricted, which the cited source does not
  support. What is observable is only that 5 shipped Blizzard tocs set it and 0 of
  the 147 third-party tocs on this install do `[T1 src / T1 obs, counted]`.
  Treat `Secure` as **undocumented**, not as documented-and-restricted.
  `@verify-ingame`

- **XML has a scoping element too.** `<ScopedModifier>` wraps a run of `<Ui>`
  children and carries `forbidden`, `scriptsUseGivenEnv`, `addToSecureEnv`,
  `hideFromGlobalEnv`, `fullLockdown`
  `[T1 src: Blizzard_SharedXML/UI.xsd:1145-1155, referenced from <Ui> at :1161]`.
  20 Blizzard XML files use it `[T1 src, counted]`; **0** of the 6 surveyed
  addons and **0** third-party XML files on the live install do `[T3/T1 obs, counted]`.
  **[gap]** Whether an addon may use it at all is unestablished — it is in the
  schema, which is Tier 1, but nothing in the field exercises it. `@verify-ingame`

- **Even the callback dispatcher is a taint barrier.** Blizzard's shared
  `CallbackRegistryMixin:TriggerEvent` does not call registrants directly; it
  routes every one through `securecallfunction` inside `secureexecuterange`
  `[T1 src: Blizzard_SharedXMLBase/CallbackRegistry.lua:198-214]`, and the
  registration path routes the table-key insertion through a secure delegate with
  the comment `-- Taint barrier for inserting event key into callback tables.`
  `[T1 src: CallbackRegistry.lua:125-126, delegate at :106-110]`. The architectural
  point: **a module seam in this game is also a taint seam**, and Blizzard's own
  shared bus treats it as one.

### 5.2 Pooling forces ownership discipline

`Pools.lua` is 866 lines and enforces three things you cannot opt out of if you
use the shipped pools.

**Objects must be tables.** `assert(type(object) == "table")` in `Acquire`, with
the comment *"While pools don't necessarily need to only contain tables, support
for other types has not been tested, and therefore isn't allowed until we can
justify a use for them."* `[T1 src: Blizzard_SharedXMLBase/Pools.lua:50-55]`

**An object may only be released to the pool that owns it.**
`Release` asserts the object is active in *this* pool unless the caller passes
`canFailToFindObject` (which only pool *collections* do, because they iterate)
`[T1 src: Pools.lua:78-90; the collection path at :394-397]`.

**A secret value may never enter a secure pool** — and the comment gives the
architectural reason, which is the whole point of this section:

> *"We don't want to allow secret values to be released into secure pools because
> of internal assertions in the SecureStack container that disallow secret values
> - and because **if one secret object enters a pool, all future acquisitions end
> up being secret too.**"*

`[T1 src: Pools.lua:265-280; the guard is issecretvalue(object) at :274]`

**The default is the secure variant.** `CreateFramePool`, `CreateObjectPool`,
`CreateTexturePool`, `CreateFontStringPool`, `CreateActorPool`,
`CreateFramePoolCollection`, `CreateFontStringPoolCollection`,
`CreateMaskTexturePool` are all plain aliases of their `CreateSecure*`
counterparts, under the comment *"Aliases until we determine if we want to change
any code to explicitly create the secure or unsecured variant"*
`[T1 src: Pools.lua:854-863 — comment at :854-855, the eight aliases at :856-863]`. Blizzard's own code calls the alias — 216 call
sites for `CreateFramePool(` versus 2 for `CreateSecureFramePool(`
`[T1 src, counted]`. The unsecured variants exist and are separately named
(`CreateUnsecuredFramePool` etc., `[T1 src: Pools.lua:810-851]`) and are
documented as *"not intended to be used for sharing between tainted and untainted
code"* `[T1 src: Pools.lua:271-272]`.

Secure pools are additionally exposed only through a **proxy** with a fixed method
whitelist — `Acquire`, `ReleaseAll`, `Release`, `EnumerateActive`, `GetNextActive`,
`IsActive`, `GetNumActive`, `DoesObjectBelongToPool`
`[T1 src: Pools.lua:282-297]` — so you cannot reach the pool's internals at all.
Design against those eight methods.

### 5.3 The SavedVariables format forces a data / presentation split

The persisted form is a Lua source file the client rewrites on logout
`[T2 wiki: Saving variables between game sessions, revid 5890180, §Saving to disk]`,
containing only the named globals. The wiki states the type restriction directly:
*"Strings, booleans, numbers and tables are the only variable types that will be
saved (functions, userdata and coroutines will not). Circular references in tables
may not be preserved."* `[T2 wiki: same revid, §Common pitfalls]` — so frames
(userdata-backed) and functions/closures are out. That is a *structural*
constraint, not a style preference: **your persisted model must be a plain-data
tree, disjoint from the
widget tree that renders it.** The Blizzard split in §4.1 and the WeakAuras
pipeline in §4.4 both fall out of this — an addon whose configuration lives on
its frames has nothing serialisable to write.

Two further shape consequences:

- The SV globals do not exist while your files run (§1.5), so the widget tree is
  necessarily constructed against defaults and re-configured later. That is what
  makes an idempotent apply/refresh entry point load-bearing rather than tidy.
- Schema versions must be migrated in code because the format has no versioning
  of its own. WeakAuras carries a dedicated `Modernize.lua` for exactly this
  `[T3: WeakAuras2@38d4bf1e WeakAuras/Modernize.lua]`. Details are the
  `state-persistence-and-communication` topic's.

### 5.4 Load-on-demand and packaging shape the folder tree

Two mechanisms let one source tree ship as several addons.

**`## LoadOnDemand: 1` + `## Dependencies`.** 125 of the 346 shipped Blizzard
`.toc` files are LoD `[T1 src, counted]`; 45 of the 147 third-party `.toc` files
on the live install are `[T1 obs, counted]`. BigWigs is the sharpest example in
the surveyed set: **12 of its 18 `.toc` files are LoD**, and every one of the
12 names `BigWigs` in its `## Dependencies` — only the six per-flavour loader stubs
(`BigWigs.toc`, `_Cata`, `_Mists`, `_TBC`, `_Vanilla`, `_Wrath`) load at login
`[T3: BigWigs@3fdc10f6, all 18 .toc files inspected]`. Note `BigWigs_Options` and
`BigWigs_Plugins` declare *more* than `BigWigs` (`BigWigs, BigWigs_Core,
BigWigs_Plugins` and `BigWigs, BigWigs_Core` respectively). Each raid zone is its
own demand-loaded addon.

**`.pkgmeta` `move-folders`.** The packager relocates subdirectories of the repo
into sibling addon folders at build time:

```
move-folders:
    BigWigs/Core: BigWigs_Core
    BigWigs/Options: BigWigs_Options
    BigWigs/Plugins: BigWigs_Plugins
    BigWigs/TheVoidspire: BigWigs_TheVoidspire
    …
```
`[T3: BigWigs@3fdc10f6 .pkgmeta, move-folders block — 9 entries]`

⚠ 9 entries ships **10** addons, not 9: the repo root itself packages as
`BigWigs` (`package-as: BigWigs`) and the 9 subfolders move out beside it.
Corroborated on disk — the live install carries exactly 10 `BigWigs*` folders
(`BigWigs`, `_Core`, `_Options`, `_Plugins`, `_MarchOnQuelDanas`, `_MidnightWorld`,
`_Sporefall`, `_TheDreamrift`, `_TheVenomousAbyss`, `_TheVoidspire`) `[T1 obs]`.

WeakAuras does the same for `WeakAuras`, `WeakAurasOptions`, `WeakAurasModelPaths`,
`WeakAurasTemplates`, `WeakAurasArchive` — **5 addon folders out of 7
`move-folders` entries**; the remaining two (`LibRangeCheck-3.0`,
`LibAPIAutoComplete-1.0`) relocate libraries within an addon rather than creating
one `[T3: WeakAuras2@38d4bf1e .pkgmeta, move-folders block]`.

So **one git repo ≠ one addon**, and the shipped partition may not match the
directory layout you see in the repo. When reasoning about load order across a
multi-addon suite, read the `.pkgmeta`, not the tree.

### 5.5 Blizzard's own partitioning, as a scale reference

317 `Blizzard_*` addons, 346 `.toc` files, 2298 Lua files `[T1 src, counted]`.
The distribution is extremely skewed: **130 of the 317 contain exactly one Lua
file**, while the largest are `Blizzard_APIDocumentationGenerated` (592),
`Blizzard_SharedXML` (154) and `Blizzard_FrameXML` (65) `[T1 src, counted]`.
This is an existence proof that "one feature, one addon" scales, and that very
small addons are normal — not that you should copy the ratio. Blizzard has
capabilities here that addons do not: `AllowLoad`, `EscalateErrorDuringLoad`,
`LoadFirst`, `SavedVariablesMachine`, `UseSecureEnvironment`
`[T2 wiki: TOC format, revid 6767089, §Restricted — those five and only those
five]`. `Secure` is *not* on the wiki's restricted list (see §5.1); it is
undocumented rather than documented-as-restricted.

---

## 6. Gaps

- **[gap] When `Mixin` / `CreateFromMixins` became engine functions.** They are C
  globals at 12.0.7.68887 (`[T1 docs: FrameScriptDocumentation.lua:82, :279]`,
  no Lua definition anywhere in the source). Searched the wiki's
  `Patch 12.0.0/API changes`, `12.0.5`, `12.0.7` pages for both names — no entry.
  Not established.
- **[gap] `[LoadIntoEnvironment …]` and `[AllowLoadEnvironment …]` are
  undocumented.** Observed in Blizzard `.toc` files `[T1 src]` but absent from
  the wiki's `TOC format` page (revid 6767089, 2026-07-09), and used by 0 of the
  147 third-party `.toc` files on this install. Whether an addon may use them is
  unknown. `@verify-ingame`
- **[gap] `<ScopedModifier>` availability to addons.** In `UI.xsd` (Tier 1), used
  by 20 Blizzard XML files, used by 0 of the 6 surveyed addons and 0 third-party
  XML files on the live install. Cannot say whether it works for addons or is
  silently ignored. `@verify-ingame`
- **[gap] `## Secure` is undocumented, not documented-as-restricted.** 5 shipped
  Blizzard tocs set it `[T1 src, counted]`; the wiki's `TOC format` page (revid
  6767089) does not mention the tag at all, and its §Restricted list does not
  include it. Whether a third-party addon setting it is ignored, honoured or
  rejected is unknown. `@verify-ingame`
- **[gap] No Tier-1 or Tier-2 statement exists on how to structure an addon.**
  There is no Blizzard-authored tutorial. The wiki's `Using the AddOn namespace`
  (revid 6474636, **2025-09-16**) only describes the vararg. No
  Blizzard document recommends a module system, a file layout, or a data/display
  split. Everything in §3 and §4 is inference from shipped code.
- **[gap] Ordering guarantees within a single `.toc` are Tier 2 only.** "Files are
  loaded in order, from top to bottom" comes from the wiki `[T2 wiki: TOC format,
  revid 6767089]`. It is corroborated by Blizzard's own `.toc` files being
  internally consistent with it (§1.1), but I found no Tier-1 statement of the
  rule. `@verify-ingame`
- **[gap] Nothing here was executed in the client.** Every count is a static read
  of source on disk.
- **Not covered, by design:** the `.toc` directive catalogue and the load
  sequence (`anatomy-and-runtime`); what taint and secret values *are*
  (`security-taint-and-restricted-data`); SavedVariables encoding, migration and
  addon comms (`state-persistence-and-communication`); frame/template/animation
  mechanics (`frames-textures-animation`); library selection
  (`libraries-and-ecosystem`).

---

## 7. Rules we could audit against

Concrete and checkable. Each states the tier of the evidence behind it. Where a
statement is a Tier 3 practice rather than a platform rule, it says so and the
audit is "your code is consistent with N surveyed addons", not "your code is
wrong".

1. **A file-scope expression may only reference symbols defined by files loaded
   earlier in the `.toc`, or earlier in the XML that included it.** `.toc` files
   load top to bottom, and a Lua chunk executes on load.
   *[Tier 2 for the ordering rule: wiki `TOC format` revid 6767089, §File loading
   order. Tier 1 for a live instance: `Blizzard_CooldownViewer/CooldownViewer.lua:87`
   composes `CooldownViewerItemDataMixin`, which is created at
   `CooldownViewerItemData.lua:3`; the `.toc` lists the data file at line 20 and
   the composing file at line 25.]*

2. **`## SavedVariables` / `## SavedVariablesPerCharacter` name *globals*.** An
   addon that stores its persisted state only inside its `ns` table will persist
   nothing.
   *[Tier 2: wiki `Saving variables between game sessions` revid 5890180,
   2023-12-11 — "a comma-delimited list of variable names in the global
   environment". Tier 2 corroboration that this is felt as a defect:
   WoWUIBugs#649 "Private addon storage", open, filed 2024-09-02.]*

3. **Without `## LoadSavedVariablesFirst: 1`, no file-scope code in the addon can
   read its SavedVariables.** They are loaded after the last script file, just
   before `ADDON_LOADED`.
   *[Tier 2: wiki `Saving variables between game sessions` revid 5890180, §The
   loading process; wiki `TOC format` revid 6767089, §LoadSavedVariablesFirst,
   added 11.1.5. Origin: WoWUIBugs#414, `Acknowledged by Blizzard`, closed
   2025-03-07. Adoption: 2/346 Blizzard tocs, 2/81 addons on this install.]*

4. **Reading another addon's namespace table requires `## AllowAddOnTableAccess: 1`
   in *that* addon's `.toc` and `C_AddOns.GetAddOnLocalTable(name)` at the reader.
   Insecure code can never read a Blizzard addon's table.**
   *[Tier 1: `AddOnsDocumentation.lua:149`, whose Documentation string states both
   halves. Tier 2 for the directive: wiki `TOC format` revid 6767089, added 11.1.7.]*

5. **`SecureMixin(...)` and `CreateFromSecureMixins(...)` return without effect
   when `issecure()` is false.** Addon code that relies on them silently gets
   nothing.
   *[Tier 1: `Blizzard_SharedXMLBase/Mixin.lua:24-26` (`if ( not issecure() ) then
   return; end`) and `:43-45`.]*

6. **`Mixin` and `CreateFromMixins` are flagged `SecureHooksAllowed = false` in
   the generated API spec.** Audit against the *flag*, not against a behaviour.
   *[Tier 1: `FrameScriptDocumentation.lua:82` (CreateFromMixins, flag on the next
   line), `:279` (Mixin, same). `[gap]` The field's semantics are nowhere defined:
   `SecureHooksAllowed` appears **only** inside
   `Blizzard_APIDocumentationGenerated/` (24 `= false` occurrences) and in no Lua
   logic anywhere in the shipped source `[Tier 1, counted]`. "Cannot be
   secure-hooked" is a reading of the field name, not an observed or documented
   behaviour. `@verify-ingame`]*

7. **A mixin has no `super`; an override that must extend its base calls the base
   table's function explicitly with `self`.**
   *[Tier 1: `Blizzard_CooldownViewer/CooldownViewer.lua:462`
   (`CooldownViewerItemDataMixin.OnCooldownIDSet(self)`), `CooldownViewerSettings.lua:299`
   and `:305`, `Blizzard_SharedXMLBase/GlobalCallbackRegistry.lua:4`.]*

8. **An object released to a pool must be active in *that* pool.** `Release`
   asserts otherwise; only pool *collections* may pass `canFailToFindObject`.
   *[Tier 1: `Blizzard_SharedXMLBase/Pools.lua:78-90`; the collection call site
   passing the flag is `:394-397`.]*

9. **Pooled objects must be tables.** `Acquire` asserts `type(object) == "table"`
   on newly created objects.
   *[Tier 1: `Pools.lua:50-55`.]*

10. **A secret value must never be released into a secure pool.** The guard
    `issecretvalue(object)` fires `assertsafe(false, "attempted to release a
    secret value into a pool: %s")`, and the stated consequence of getting one in
    is that *all future acquisitions from that pool become secret*.
    *[Tier 1: `Pools.lua:265-280`.]*

11. **Code that uses `CreateFramePool` (and its seven sibling aliases) is using
    the *secure* pool and is limited to the eight proxied methods** — `Acquire`,
    `Release`, `ReleaseAll`, `EnumerateActive`, `GetNextActive`, `IsActive`,
    `GetNumActive`, `DoesObjectBelongToPool`.
    *[Tier 1: aliases at `Pools.lua:856-863`; proxy whitelist at `Pools.lua:282-297`.]*

12. **A `CallbackRegistryMixin` owner may hold at most one callback per event.**
    Re-registering the same `(event, owner)` replaces the previous callback —
    `RegisterCallback` unconditionally calls `UnregisterCallback(event, owner)`
    first.
    *[Tier 1: `Blizzard_SharedXMLBase/CallbackRegistry.lua:128-130`, with the
    intent stated in the comment.]*

13. **A numeric `owner` passed to `CallbackRegistryMixin:RegisterCallback` is an
    error** — numbers are reserved for auto-generated owner IDs. Passing `nil`
    yields a generated ID which is returned to the caller.
    *[Tier 1: `CallbackRegistry.lua:118-122`, `:141`.]*

14. **`CallbackRegistryMixin:TriggerEvent` errors on an event not declared via
    `GenerateCallbackEvents`, unless `SetUndefinedEventsAllowed(true)` was
    called.** `EventRegistry` is the one shipped registry that opts in.
    *[Tier 1: `CallbackRegistry.lua:187-189`, `:66-68`;
    `GlobalCallbackRegistry.lua:5`.]*

15. **`GenerateCallbackEvents` errors if any event name in the table is already
    registered on that object.** Two mixins that both declare the same event name
    on one frame cannot coexist.
    *[Tier 1: `CallbackRegistry.lua:279-281`.]*

16. **Every `CallbackRegistryMixin` callback is dispatched through
    `securecallfunction` inside `secureexecuterange`.** A registrant therefore
    cannot rely on inheriting the trigger's secure status, and cannot spread taint
    back to it through the bus.
    *[Tier 1: `CallbackRegistry.lua:198-214`; the registration-side barrier is at
    `:125-126` with `SecureInsertEvent` at `:106-110`.]*

17. **Five `.toc` tags are documented as restricted to Blizzard: `AllowLoad`,
    `EscalateErrorDuringLoad`, `LoadFirst`, `SavedVariablesMachine`,
    `UseSecureEnvironment`.** An addon `.toc` that sets one is copying a
    Blizzard-internal pattern that will not apply to it.
    *[Tier 2: wiki `TOC format` revid 6767089, §Restricted — "The following tags
    are inaccessible to third-party AddOns", listing exactly those five. Tier 1
    for who uses them: 13 shipped tocs set `UseSecureEnvironment`, 19 set
    `LoadFirst`, 177 set `AllowLoad`; 0 of the 147 top-level third-party tocs on
    this install set any of the five.]*
    ⚠ **`## Secure` is NOT on the restricted list** — an earlier version of this
    rule included it, and the cited page does not mention the tag at all. 5
    shipped Blizzard tocs set it `[Tier 1, counted]`, 0 third-party tocs do. Do
    not audit against `Secure` as if it were a documented restriction; audit it,
    if at all, as "undocumented, and nobody in the field uses it". See §6.

18. **`LibStub:NewLibrary` returns `nil` when an equal-or-newer minor is already
    loaded — the call site must bail out on nil.** On a real upgrade the *same*
    table is returned, so upvalues captured by the previous version survive and
    must be re-bound.
    *[Tier 3: `Ace3@4475787f LibStub/LibStub.lua:16` (nil return), `:17`
    (`self.libs[major] or {}`). A convention of the LibStub-embedding libraries,
    not a platform rule. `[unverified]` — the earlier claim that "every
    LibStub-based library in the ecosystem depends on it" was not surveyed and is
    withdrawn; the checkable statement is only about libraries that call
    `LibStub:NewLibrary`.]*

19. **Registration by unique string name rejects duplicates rather than
    overwriting, in every module system surveyed.** Audit as "a second
    registration under the same name is rejected" — *not* as "raises", because one
    of the four rejects by printing.
    *[Tier 3, 4 instances: `Ace3 AceAddon-3.0.lua:115` (addon) and `:235` (module);
    `BigWigs Core/Core.lua:738` (plugin); `WeakAuras WeakAuras.lua:453` (region
    type); `oUF ouf.lua:1008` (element). Counter-case in the same corpus:
    `BigWigs Core/Core.lua:447-449` — `NewBoss` on a duplicate calls `core:Print`
    and returns, it does not raise. The four are not fully independent either:
    ElvUI and Details inherit Ace3's behaviour rather than choosing it.
    A convention, not a rule.]*

20. **Where Blizzard formalises a data/display seam, the display side implements
    `RefreshData()` and the data side declares it abstract.** Both `*DataMixin`
    tables in the shipped source do this.
    *[Tier 1: `CooldownViewerItemData.lua:496-498` declares it with
    `assertsafe(false, "RefreshData must be overridden by a derived mixin.")`;
    implemented at `CooldownViewer.lua:1136` and `CooldownViewerSettings.lua:163`.
    `GameTooltipDataMixin:RefreshData` at `GameTooltip.lua:955`.
    **n = 2** — `*DataMixin` is 2 of 3201 mixin tables, and `Refresh*` is 513 of
    25054 mixin methods. Do not audit this as "every mixin needs a RefreshData".]*

21. **A refresh entry point with more than one producer needs a dirty flag, or it
    runs once per producer per frame.** Blizzard's shape is
    `MarkDirty` → `IsDirty` → `Clean` (which clears the flag *before* calling
    `RefreshData`), drained in an `OnUpdate`.
    *[Tier 1: `CooldownViewer.lua:113` / `:117` / `:121` (the three methods),
    `:1365-1366` (the drain — the addon's only one, inside
    `CooldownViewerBuffBarItemMixin:OnUpdate` at `:1360`), single producer at
    `:1194`. `GameTooltipDataMixin` is the same shape with the flag cleared inside
    `RefreshData` itself rather than by a separate `Clean`:
    `Blizzard_GameTooltip/Mainline/GameTooltip.lua:955-958, :960-963, :965-972`.
    ⚠ `CooldownViewerSettingsDataProvider.lua:18, :169` were previously cited here
    as producers; they mark a **different** object dirty
    (`CooldownViewerSettingsDataProviderMixin`, own `MarkDirty`/`IsDirty` at
    `:210`/`:214`), so do not audit them as part of this chain.
    Tier 3 corroboration at scale: WeakAuras' `changed` flag
    (`WeakAuras.lua:336-345`), with `Private.UpdatedTriggerState` (`:5025`) called
    from 13 sites — `WeakAuras.lua:1483, :3232, :4728, :4745, :4773, :4791, :4876`;
    `GenericTrigger.lua:956, :1014, :1031, :1093, :1216`; `BuffTrigger2.lua:2004`.
    **The rule is a design observation from 2 Tier-1 + 1 Tier-3 instances, not a
    platform requirement** — nothing in the API forces it.]*

22. **A data mixin that calls `GameTooltip_SetDefaultAnchor(tooltip, self)` is not
    frame-independent.** Blizzard's own "data" mixin still assumes it is mixed
    into a frame — do not claim a data/display split is total without checking
    for this.
    *[Tier 1: `CooldownViewerItemData.lua:501`; the file's only other widget calls
    are `tooltip:Show()` at `:508` and `GetAppropriateTooltip():Hide()` at `:512`
    — **3** widget touches versus **34** in the paired display file, counted with
    `grep -cE ':Show\(\)|:Hide\(\)|:SetTexture|:SetAtlas|:SetText|:SetPoint|:SetShown|:SetAlpha|:SetDesaturated|GameTooltip_'`.
    An earlier version said "2 versus 36" without recording the pattern; that pair
    is not reproducible.]*

23. **A `.pkgmeta` `move-folders` block means the shipped addon partition differs
    from the repo tree.** Load-order and dependency reasoning must be done against
    the shipped partition.
    *[Tier 3: `BigWigs@3fdc10f6 .pkgmeta` — 9 `move-folders` entries
    (`BigWigs_Core`, `BigWigs_Options`, `BigWigs_Plugins` + **6** zone addons),
    which with the `package-as: BigWigs` root ships **10** addons, not 9;
    `WeakAuras2@38d4bf1e .pkgmeta` — 7 `move-folders` entries, of which 5 create
    addon folders and 2 relocate libraries. Corroborated on disk `[Tier 1 obs]`:
    the live install carries exactly 10 `BigWigs*` folders.]*

24. **LoD is the standard partitioning tool: 125/346 shipped tocs and 45/147
    top-level third-party tocs on this install set `## LoadOnDemand: 1`, and all
    12 LoD BigWigs tocs name `BigWigs` in `## Dependencies`.**
    *[Tier 1 src / Tier 1 obs for the counts; Tier 3 for the BigWigs pattern
    (`BigWigs@3fdc10f6`, all 18 `.toc` files inspected — 2 of the 12 declare more
    than `BigWigs`). The load-failure semantics themselves are the
    `anatomy-and-runtime` topic's.]*
    `[unverified]` The stronger form this rule used to state — "…or the symbol
    will be missing" — is an inference about cross-addon load order that I could
    not source; see the `[gap]` in §1.4. Audit the counts and the declaration, not
    the failure mode.

25. **XML-declarative composition (`mixin=`, `parentKey=`) is a Blizzard house
    style, not an ecosystem norm.** An audit that flags Lua-built frames as
    "wrong" is auditing against Blizzard's code, not against practice.
    *[Tier 1 for the mechanism: `Blizzard_SharedXML/UI.xsd:468-476`. Counts:
    Blizzard uses `parentKey="` 17706 times; the 6 surveyed addons use it 57 times
    across 105 XML files and `mixin="` 4 times; BigWigs ships no XML at all.]*
