---
title: Security — protected actions, taint, and restricted data (secret values)
patch: 12.0.7
fetched: 2026-07-23
reviewed: 2026-07-23
sources:
  - https://github.com/Gethe/wow-ui-source (live, 12.0.7.68887, commit 4383ced30106)
  - https://warcraft.wiki.gg/wiki/Secret_Values (revid 6777907, 2026-07-22)
  - https://warcraft.wiki.gg/wiki/Secure_Execution_and_Tainting (revid 6651217, 2026-02-15)
  - https://warcraft.wiki.gg/wiki/Patch_12.0.0/Planned_API_changes (revid 6746061, 2026-06-17)
  - https://warcraft.wiki.gg/wiki/Patch_12.0.0/API_changes (revid 6747189, 2026-06-18)
  - https://warcraft.wiki.gg/wiki/Patch_12.0.7/API_changes (revid 6778033, 2026-07-22)
  - https://warcraft.wiki.gg/wiki/API_hooksecurefunc (revid 6588971, 2026-01-03)
  - https://warcraft.wiki.gg/wiki/API_issecurevariable (revid 6588975, 2026-01-03)
  - https://warcraft.wiki.gg/wiki/API_issecure (revid 6588974, 2026-01-03)
  - https://warcraft.wiki.gg/wiki/API_forceinsecure (revid 6588967, 2026-01-03)
  - https://warcraft.wiki.gg/wiki/CVar_taintLog (revid 6739475, 2026-06-08)
  - https://github.com/Stanzilla/WoWUIBugs
confidence: high
---

# Security: protected actions, taint, and restricted data

**All Tier-1 file:line citations in this file are relative to the
`wow-ui-source` checkout at `raw/addon-research/wow-ui-source`, commit
`4383ced30106`, `version.txt` = `12.0.7.68887`** — i.e. `Interface/AddOns/...`.
Counts were produced by grep/scripted extraction over
`Interface/AddOns/Blizzard_APIDocumentationGenerated/` at that build and are
reproducible; re-run them after any `git pull` of the checkout.

**Adversarial verification pass, 2026-07-23.** Every Tier-1 file:line, every
count, every wiki revid and every WoWUIBugs label in this file was re-opened
against the source. Corrections made in that pass are called out inline as
"an earlier draft…". The material refutations were: the "casting/targeting have
no callable API" claim in §1.1 (false — see the ⚠ there), the
`SecureHandlerTemplates.xml` template count (§3.2), the claim that all nine
secret-testing primitives carry `SecretArguments` (§4.4), four of seven
"densest user" attributions (§2.2), the `HasRestrictions` count (§6), and the
`Frame:SetShown` worked example (§4.6, §7 rule 19).

Tier definitions are in [`sources.md`](./sources.md) §0. Short form:
**Tier 1** = Blizzard's shipped UI source and its generated API docs ·
**Tier 2** = warcraft.wiki.gg and WoWUIBugs · **Tier 3** = community addons
(practice, never rules) · **Tier 4** = blogs (corroborate or omit).

---

## 0. Three systems, not one

The single most common error in community writing on this topic is treating
"taint", "protected", and "secret" as one thing. They are three independent
mechanisms that compose:

| System | Since | Governs | Failure mode |
|---|---|---|---|
| **Protection / combat lockdown** | Patch 2.0 | *Can this call happen at all?* | Call is refused; `ADDON_ACTION_BLOCKED` fires |
| **Taint** | Patch 2.0 | *Is this execution path trusted?* | Protected calls on that path are refused |
| **Secret values** | Patch 12.0.0 (Midnight) | *May this path read/compute on this datum?* | **Immediate Lua error** at the operation |

A value can be secret on an untainted path and be perfectly usable
(Tier 2: `Secret Values`, 2026-07-22 — *"When execution is not tainted secret
values are effectively equivalent to regular values, and no operations on them
are blocked."*). A protected function can be blocked with no secrets anywhere
in sight. Diagnose them separately.

Blizzard's own stated goal for the 12.0 layer, verbatim from the addon-dev blue
post archived on the wiki:

> The overall goal of these API changes is to limit addons' ability to perform
> complex logic based off combat information, and thus optimally solve problems
> that would otherwise require player thought and coordination. But a secondary
> goal (almost as important) is to still allow addons to customize the look and
> feel of the UI (including combat-related UIs).
>
> — *Midnight Public Alpha Addon API Changes*, 2025-10-01, WoWUIDev Discord
> (Tier-1 content via Tier-2 archive: `Patch 12.0.0/Planned API changes`,
> revid 6746061, 2026-06-17; Discord permalink
> `discord.com/channels/327414731654692866/1422999311410790541` — **not
> independently verifiable, see §10**)

---

## 1. Protected actions and combat lockdown

### 1.1 What "protected" means

A **protected function** succeeds only from a secure (untainted) execution
path. In the generated docs this is the `IsProtectedFunction = true` marker.
At 12.0.7.68887 exactly **59** documented entries carry it
(`grep -rh 'IsProtectedFunction' Blizzard_APIDocumentationGenerated/ | grep -c '= true'` → 59).

Notably, **58 of the 59 are widget methods, not global game APIs.** The full
set, by owning documentation file:

- `SimpleButtonAPIDocumentation.lua` — `Disable`:53, `Enable`:62,
  `RegisterForClicks`:270, `RegisterForMouse`:281, `SetEnabled`:334
- `SimpleFrameAPIDocumentation.lua` — `ClearAttribute`:40, `ClearAttributes`:57,
  `EnableGamePadButton`:195, `EnableGamePadStick`:206, `EnableKeyboard`:217,
  `Hide`:628, `Lower`:917, `Raise`:926, `SetClampRectInsets`:1088,
  `SetClampedToScreen`:1102, `SetFixedFrameLevel`:1144, `SetFixedFrameStrata`:1155,
  `SetFrameLevel`:1176, `SetFrameStrata`:1188, `SetHitRectInsets`:1209,
  `SetHyperlinksEnabled`:1234, `SetID`:1245, `SetIgnoreParentScale`:1267,
  `SetScale`:1342, `SetShown`:1354, `SetToplevel`:1366, `SetUsingParentLevel`:1388,
  `Show`:1409, `StartMoving`:1418, `StartSizing`:1429, `StopMovingOrSizing`:1441
- `SimpleScriptRegionResizingAPIDocumentation.lua` — `AdjustPointsOffset`:10,
  `ClearAllPoints`:22, `ClearPoint`:32, `ClearPointsOffset`:43, `SetAllPoints`:111,
  `SetHeight`:123, `SetPoint`:134, `SetPointsOffset`:149, `SetSize`:161, `SetWidth`:173
- `SimpleScriptRegionAPIDocumentation.lua` — `EnableMouse`:72, `EnableMouseMotion`:83,
  `EnableMouseWheel`:94, `SetCollapsesLayout`:548, `SetMouseClickEnabled`:559,
  `SetMouseMotionEnabled`:570, `SetParent`:581, `SetPassThroughButtons`:592,
  `SetPropagateMouseClicks`:604, `SetPropagateMouseMotion`:616
- `SimpleRegionAPIDocumentation.lua` — `SetIgnoreParentScale`:168, `SetScale`:179
- `SimpleScrollFrameAPIDocumentation.lua` — `SetHorizontalScroll`:79,
  `SetScrollChild`:91, `SetVerticalScroll`:102
- `SimpleLineAPIDocumentation.lua` — `ClearAllPoints`:10
- `SimpleAnimAPIDocumentation.lua` / `SimpleAnimGroupAPIDocumentation.lua` — (none)
- `SimpleFrameScriptObjectAPIDocumentation.lua` — `SetToDefaults`:136
- `TooltipComparisonDocumentation.lua` — `C_TooltipComparison.CompareItem`:11
  (**the only namespaced C_ function in the set**)

That list is the concrete answer to "what can't my addon do to a **protected**
frame in combat": show/hide, move, resize, re-parent, re-scale, re-layer, and
change input handling. On an ordinary, never-protected addon frame these methods
are not restricted — **with the caveat in §1.2 that protection propagates to a
protected frame's parents and anchor targets**, so an "ordinary" frame can
acquire the restriction by being anchored or parented into a protected chain
(Tier 2 for that propagation; no Tier-1 statement found).

⚠ **`IsProtectedFunction = true` is not the whole protected-function surface.**
It is the marker the *generated widget/API docs* use, and 58 of its 59 entries
are widget methods. Casting and targeting APIs still exist and are still
callable names — `TargetUnit` is documented at
`TargetScriptDocumentation.lua:186` with `HasRestrictions = true` (not
`IsProtectedFunction`), and `CastSpellByName` is not in the generated docs at
all yet is called from Blizzard's own secure dispatcher
(`Blizzard_FrameXML/SecureTemplates.lua:394`). What stops an addon using them to
make a decision is that a *tainted* path cannot execute them, not that the
function is missing. Do not read the 59-entry list as "everything else is
callable from addon code".

The Tier-2 statement of the actual rule: *"Since normal AddOn code is tainted,
it cannot change targets or perform actions directly"*
(`Secure Execution and Tainting`, revid 6651217, 2026-02-15). The only sanctioned
path to a cast is a hardware-triggered click on a secure action button (§3). The
same page archives the original 2006 Blizzard statement
(Tier 2 quoting a 2006 blue post — *"AddOns and macros will still be able to cast
spells (with user interaction of course), they just won't be able to use logic to
intelligently pick spells or targets."*).

**[gap] `HasRestrictions = true` (236 entries at this build) is undefined at
Tier 1.** It is the marker actually carried by the classic
protected/hardware-event C functions (`TargetUnit`, `C_AuctionHouse.PlaceBid`,
`C_BattleNet.SendWhisper`, `COMBAT_LOG_EVENT`, …). Neither the generated docs
nor the wiki state what it means precisely. I looked in
`Blizzard_APIDocumentationGenerated/`, `Blizzard_APIDocumentation/`, and the
wiki `Secret Values` page. Treat it as "restricted for tainted callers, exact
failure mode unspecified".

### 1.2 Protected frames

A frame becomes protected by inheriting a template carrying `protected="true"`.
Tier 2 phrases this as *"protection is **generally** inherited from specially
designed templates"* (`Secure Execution and Tainting`, revid 6651217) — I found
no Tier-1 statement that a template is the *only* route, so do not audit on the
assumption that a frame without such a template cannot be protected; test with
`IsProtected()`. The attribute itself is Tier-1 schema:
`Blizzard_SharedXML/UI.xsd:484` declares
`<xs:attribute name="protected" type="xs:boolean" default="false"/>`.
The root secure template is one line:

```xml
<Frame name="SecureFrameTemplate" protected="true" propagateMouseInputMask="Clicks" virtual="true"/>
```
`Blizzard_FrameXML/SecureTemplatesBase.xml:4`

`ScriptRegion:IsProtected()` returns **two** values —
`isProtected, isProtectedExplicitly`
(`SimpleScriptRegionAPIDocumentation.lua:492`, returns at `:502-503`).
**[unverified]** The natural reading is that the second flag distinguishes
"protected because a template said so" from "protected by contagion"
(parent / anchor) — but the generated docs carry **no** `Documentation` string
for either return, and neither wiki page defines the pair. That is inference, not
a documented contract. What *is* Tier 1 is that Blizzard's own secure-handler API
checks the *explicit* flag:
`if (not select(2, header:IsProtected())) then error("Header frame must be
explicitly protected"); end`
(`Blizzard_RestrictedAddOnEnvironment/SecureHandlers.lua:496-499`).

Protection spreads to parents and anchor targets, and that spread is reversible
by re-anchoring or re-parenting out of combat — Tier 2 only
(`Secure Execution and Tainting`, revid 6651217, 2026-02-15: *"Control
restrictions on protected frames are also applied to their parents and any
frames they are anchored to. … This propagation is temporary, and re-anchoring
or re-parenting the frame out of combat can release the restriction."*). The
same page states the one-way rule: *"Once a frame has been declared protected it
cannot be made unprotected"*. I found no Tier-1 statement of either. **[gap]**

`ScriptRegion:CanChangeProtectedState()`
(`SimpleScriptRegionAPIDocumentation.lua:10`) and
`C_RestrictedActions.CheckAllowProtectedFunctions(object, silent)`
(`RestrictedActionsDocumentation.lua:11-27`) are the runtime queries. The
latter's `silent` argument is documented as *"If true, don't signal blocked
action errors if protected function calls are disallowed"* — i.e. calling it
non-silently can itself raise the blocked-action path.

### 1.3 Lockdown is now one of six restriction types

`InCombatLockdown()` still exists and is now documented as a member of the
`C_RestrictedActions` system with an empty namespace override
(`RestrictedActionsDocumentation.lua:44-53`). It is the *narrow* query. The
general one is:

```
C_RestrictedActions.IsAddOnRestrictionActive(type) -> active
C_RestrictedActions.GetAddOnRestrictionState(type) -> state
```
`RestrictedActionsDocumentation.lua:28-43, 54-69`

```
Enum.AddOnRestrictionType  = Combat 0, Encounter 1, ChallengeMode 2,
                             PvPMatch 3, Map 4, Chat 5
Enum.AddOnRestrictionState = Inactive 0, Activating 1, Active 2
```
`RestrictedActionsConstantsDocumentation.lua:19` (Type, members :26-31) and
`:6` (State, members :13-15). Each member carries a `Documentation` string;
the load-bearing one is `Activating`: *"State used during the dispatch of
ADDON_RESTRICTION_STATE_CHANGED to infer that a restriction is about to become
active, but won't be enforced until event dispatch has completed."*
(`:14`) — i.e. the event handler itself is your last unrestricted window.
`Map` is *"The player is on a map that applies addon restrictions"* (`:30`) and
`Chat` is *"The player is in a state where addon chat communications are
restricted"* (`:31`).

`ADDON_RESTRICTION_STATE_CHANGED(type, state)` is documented as
*"sequenced such that it will always be fired before a restriction becomes
active, or after it is deactivated"*, and
`IsAddOnRestrictionActive` *"will always return false during dispatch of
ADDON_RESTRICTION_STATE_CHANGED"*
(`RestrictedActionsDocumentation.lua:58, 96-107`). That pair of sentences is
the contract for "do my setup before the restriction lands".

### 1.4 The blocked/forbidden events

```
ADDON_ACTION_BLOCKED(isTainted: cstring, function: cstring)     RestrictedActionsDocumentation.lua:75
ADDON_ACTION_FORBIDDEN(isTainted: cstring, function: cstring)   RestrictedActionsDocumentation.lua:86
MACRO_ACTION_BLOCKED(function: cstring)                         RestrictedActionsDocumentation.lua:109
MACRO_ACTION_FORBIDDEN(function: cstring)                       RestrictedActionsDocumentation.lua:119
```

All four are `SynchronousEvent = true`. "Blocked" = a protected action refused
on a tainted path. "Forbidden" = an action addons may never take at all. The
payload names the culprit; that is the primary in-game taint signal.

**[gap] The exact user-visible error text for each is not Tier 1.** The
generated docs give the payload shape and nothing else. Observed strings come
from WoWUIBugs issue bodies (Tier 2, observation not spec).

### 1.5 Forbidden frames

`FrameScriptObject:SetForbidden()` / `IsForbidden()`
(`SimpleFrameScriptObjectAPIDocumentation.lua:128, 83`). **[unverified] — what
"forbidden" *means* is not stated at Tier 1.** Neither entry carries a
`Documentation` string. An earlier draft of this file said a forbidden frame is
"hidden from the global environment for tainted code"; the wiki's own text for
`MouseFocusValidForLimitedInput` lists *"forbidden, hidden from the global
environment, fully locked down, script inaccessible, or protected frames"* as
**five separate** conditions, so that gloss conflated two of them and has been
removed. What is Tier 1 is the *behaviour*: Blizzard's secure-handler API refuses
to operate on a forbidden frame and will *mark the caller's frame forbidden* if
it tries to reference one:

```lua
if (CheckForbidden(header)) then
    MakeForbidden(frame);
    error("Cannot use SecureHandlers API on forbidden frames");
```
`SecureHandlers.lua:483-487` (also :446-449, :475-478, :574-578)

The wiki records the error string *"attempted to index a forbidden table"* for
the analogous table case (Tier 2: `Secret Values`, revid 6777907).

---

## 2. Taint

### 2.1 The model

Tier 2 (`Secure Execution and Tainting`, revid 6651217, 2026-02-15) is the only
prose statement of the rules, and it predates and does not cover secret values.
Its summary:

- Execution starts secure; it becomes tainted the moment it reads a value or
  calls a closure introduced by an addon.
- New values inherit the taint of the path that created them. Reading a secure
  value from a tainted path yields a tainted copy; the original stays clean.
- Executing a tainted closure taints the current path.
- Taint persists until `/reload` or relog.

`issecure()` returns whether the current path is untainted
(Tier 2: `API issecure`, revid 6588974, 2026-01-03). It is **not** in the
generated docs but is used 51 times in the shipped source, e.g.
`Blizzard_SharedXMLBase/Mixin.lua:24,43`,
`Blizzard_ScriptErrors/Blizzard_ScriptErrors.lua:67` (`assert(issecure())`),
`Blizzard_EditMode/Shared/EditModeManager.lua:702`
(`if issecure() or not InCombatLockdown() then`).

`forceinsecure()` deliberately taints the current path
(Tier 2: `API forceinsecure`, revid 6588967). Blizzard uses it as a safety
valve — 24 hits, including
`Blizzard_FrameXML/SecureTemplates.lua:746`, where a secure action button
about to dispatch to a *user-supplied* handler taints itself first:

```lua
-- There exist a few means for this lookup to return user-provided
-- functions that don't carry taint, so consider this to be at-risk.
atRisk = true;
handler = rawget(self, actionType);
...
if atRisk then forceinsecure(); end
```
`Blizzard_FrameXML/SecureTemplates.lua:738-746`

`issecurevariable([tbl,] key) -> isSecure, taintSource` is the introspection
primitive. **It appears nowhere in the shipped source and nowhere in the
generated docs** (`wowkb.uiapi missing issecurevariable` → "NOT FOUND in
either"). The wiki is the only source: Tier 2, `API issecurevariable`,
revid 6588975, 2026-01-03 — second return is the addon name that tainted the
key, `""` for a macro, `nil` if secure; it cannot inspect locals or non-string
keys; and an unset key with an `__index` metatable reports the metatable's
taint instead.

### 2.2 Not spreading taint into Blizzard code

**Post-hooks.** `hooksecurefunc([tbl,] name, func)` installs a hook that runs
*after* the original with the same arguments, without tainting it
(Tier 2: `API hooksecurefunc`, revid 6588971, 2026-01-03). The same page
records that since Patch 11.0.0 a set of function names cannot be hooked at all
("Cannot hook function"): `getfenv`, `getmetatable`, `hooksecurefunc`, `ipairs`,
`issecurevalue`, `issecurevariable`, `next`, `rawget`, `rawset`, `pairs`,
`pcall`, `pcallwithenv`, `scrub`, `securecall`, `securecallfunction`,
`secureexecuterange`, `select`, `setfenv`, `setmetatable`, `type`, `unpack`,
`wipe`, `xpcall`.

Tier 1 has a *different and independent* deny-list. The generated docs carry a
`SecureHooksAllowed` field, and **every one of its 24 occurrences is `false`**
(`grep -rh 'SecureHooksAllowed' … | sed 's/.*= //' | sort | uniq -c` →
`24 false,`; zero `true`). So it is a deny marker, not a permit marker. The 24:

`C_RestrictedActions.CheckAllowProtectedFunctions`
(`RestrictedActionsDocumentation.lua:11`), and in
`FrameScriptDocumentation.lua`: `canaccessallvalues`:20, `canaccesssecrets`:37,
`canaccesstable`:48, `canaccessvalue`:65, `CreateFromMixins`:82,
`CreateSecureDelegate`:98, `dropsecretaccess`:131, `dumpobject`:137,
`hasanysecretvalues`:210, `issecrettable`:227, `issecretvalue`:244,
`mapvalues`:261, `Mixin`:279, `RegisterEventCallback`:296,
`RegisterUnitEventCallback`:308, `scrubsecretvalues`:331, `scrub`:348,
`secretunwrap`:365, `secretwrap`:383, `securecallmethod`:400,
`SetTableSecurityOption`:429, `UnregisterEventCallback`:442,
`UnregisterUnitEventCallback`:454.

Only `scrub` is on both lists. Treat the union as unhookable.

`frame:HookScript(script, func)` is the widget-script equivalent (Tier 2, same
page). Two further properties from that page that constrain design:
**a hook cannot be removed except by a UI reload** (repeated calls *add* hooks),
and **`setfenv` on a hooked function errors afterwards**. It also replaces the
function reference, so a hook installed after an XML `<OnHide function="…"/>`
binding was resolved will never fire — hook something the handler calls instead.

**Secure call barriers.** These are absent from the generated docs but heavily
used in shipped code, so their *existence and idiom* is Tier 1 by observation
even though their semantics are Tier 2:

Counts are `grep -rnw '<name>' --include=*.lua Interface/AddOns/` with the
generated-documentation directory excluded, at 12.0.7.68887. ⚠ **These are raw
line hits, not call sites** — Blizzard localises each primitive at the top of
almost every consuming file (`local forceinsecure = forceinsecure;`), so roughly
half of each count is aliasing. `forceinsecure`'s 24 hits are 12 aliases + 12
real calls, verified by reading them.

| Function | Shipped-source hits | Densest file (hits) |
|---|---|---|
| `securecall` | 135 | `Blizzard_Menu/Menu.lua` (16) |
| `securecallfunction` | 220 | `Blizzard_Settings_Shared/Blizzard_SettingsPanel.lua` (36), then `Blizzard_Menu/Menu.lua` (30) |
| `secureexecuterange` | 45 | `Blizzard_EditMode/Shared/EditModeManager.lua` (13), then `Blizzard_MapCanvas/Blizzard_MapCanvas.lua` (10) |
| `scrub` | 49 | `Blizzard_RestrictedAddOnEnvironment/RestrictedFrames.lua` (30) |
| `forceinsecure` | 24 | no dense user — 12 files, max 3 hits (`Blizzard_Console/Blizzard_Console.lua`, `Blizzard_ChatFrameBase/Shared/SlashCommands.lua`) |
| `issecure` | 51 | `Blizzard_RestrictedAddOnEnvironment/RestrictedInfrastructure.lua` (10) |
| `hooksecurefunc` | 14 | `Blizzard_PTRFeedback/Blizzard_PTRFeedback_Tooltips.lua` (6) |

(An earlier draft named `Blizzard_SharedXMLBase/Mixin.lua`,
`Blizzard_MapCanvas`, `SecureTemplates.lua` and `SecureTypes.lua` as the densest
users of `issecure` / `secureexecuterange` / `forceinsecure` /
`securecallfunction`. Re-counting refuted all four; the table above is the
re-count.)

`securecallmethod(object, "method", ...)` **is** documented, at
`FrameScriptDocumentation.lua:400-417`, with the clearest Tier-1 statement of
what a call barrier does: *"Invokes a named method on an object with a secure
call barrier that prevents errors or taint from function lookup and execution
from propagating to the caller."* Its `Returns` doc adds: *"If an error
occurred, this result list will be empty."* Method lookup *"uses raw access and
ignores any associated metatable."*

`scrub` is documented at `FrameScriptDocumentation.lua:348-363`:
*"Returns a transformed list of values with inputs that are either secret or are
not string, number, or boolean type replaced by nil values."* Its sibling
`scrubsecretvalues` (:331-346) nils **only** secrets, keeping tables/functions.

**Attributes as a taint firewall.** Blizzard's own guidance in-source is to talk
to secure code only through frame attributes:

> All of these functions should be safe to call by tainted code. They should
> only communicate with secure code via SetAttribute and GetAttribute.
>
> `Blizzard_StoreUI/Blizzard_Shared_StoreUIInbound.lua:4`

That exact comment appears at **six** sites, all `*Inbound.lua` files:
`Blizzard_StoreUI/Blizzard_Shared_StoreUIInbound.lua:4`,
`Blizzard_WowTokenUI/Blizzard_WowTokenUIInbound.lua:4`,
`Blizzard_SimpleCheckout/Blizzard_SimpleCheckout_Inbound.lua:4`,
`Blizzard_CatalogShop/Blizzard_CatalogShop_Inbound.lua:4`,
`Blizzard_CatalogShopRefundFlow/Blizzard_CatalogShopRefundFlow_Inbound.lua:4`,
`Blizzard_CatalogShopTopUpFlow/Blizzard_CatalogShopTopUpFlow_Inbound.lua:9`.
A *different but aligned* comment states the reason from the other side:
*"Setting attributes is how the external UI should communicate with this frame.
That way their taint won't be spread to this code."*
(`Blizzard_CatalogShop/Blizzard_CatalogShop.lua:525`,
`Blizzard_WowTokenUI/Blizzard_WowTokenUI.lua:287`). An earlier draft cited those
two as the same comment; they are not.

**`SecureTypes` — Blizzard's own containers.** `Blizzard_SharedXMLBase/SecureTypes.lua`
(393 lines) exists because *"Secure types are expected to be used by Blizzard
code to prevent taint propagation while accessing values, particularly in cases
where container types are used that can have a mixture of secure and insecurely
sourced values"* (:21-23). The factories hang off a global `SecureTypes` table:
`SecureTypes.CreateSecureMap` (:94), `CreateSecureArray` (:217),
`CreateSecureStack` (:224), `CreateSecureValue` (:266), `CreateSecureNumber`
(:307), `CreateSecureBoolean` (:340), `CreateSecureFunction` (:388).
`Blizzard_Menu/Menu.lua:1-4` localises four of them — that module is the
densest consumer. Every read goes through
`securecallfunction(rawget, self.tbl, key)` (:30) or
`securecallfunction(next, …)` (:48); every write asserts the value is not
secret (:34-35, :114-115, :234, :262, :287, :328, :357). It also documents a
subtlety with a comment repeated three times: *"Element move will taint
execution"* (:120, :132, :137) — `tinsert` at an index, `tremove`, and
`tDeleteItem` all shift elements, so they are wrapped in `securecallfunction`
while a plain append is not.

This is a Blizzard-internal facility. **Nothing establishes that addons should
or can use `SecureTypes`** — an addon's execution is tainted anyway, so the
barrier protects Blizzard from the addon, not the reverse.

### 2.3 Diagnosing taint

1. **`taintLog` CVar → `Logs/taint.log`.** The file is *"written periodically
   and once at logout"* — so do not expect it to be current mid-session
   (Tier 2: `CVar taintLog`, revid 6739475, 2026-06-08). Tier 2 in two places
   that disagree slightly:
   - `CVar taintLog` (revid 6739475, 2026-06-08) lists levels
     `0` off · `1` blocked-action errors and the taint events leading to them ·
     `2` global reads/writes · `3` upvalue reads/writes · `4` table-field
     reads/writes · **`5` writes of secret values to globals, upvalues, or table
     fields (added 12.0.1)** · `11` no functional difference.
   - `BlizzardInterfaceResources/Resources/CVars.lua:1429` (build 12.0.7.**68256**,
     i.e. a different build from our source checkout) carries the in-client
     description and stops at level 4.

   Enable with `/console taintLog 1` and restart. **@verify-ingame** — I could
   not confirm level 5's behaviour; there is no `taint.log` in
   `_retail_/Logs/` on this install (checked 2026-07-23), consistent with the
   default of `0`.

2. **Register `ADDON_ACTION_BLOCKED` / `ADDON_ACTION_FORBIDDEN`** and read the
   `isTainted` / `function` payload (§1.4).

3. **`issecurevariable(tbl, key)`** to name the tainting addon for a specific
   global or table field (Tier 2).

4. **`debugstack` / `debuglocals` are themselves secret-contaminated as of
   12.0.7**: *"debugstack and debuglocals will now return secret values if the
   current function — or any caller up the stack — has accessed a secret
   value."* (Blizzard blue post 2026-04-30, archived at Tier 2:
   `Patch 12.0.7/API changes`, revid 6778033, 2026-07-22). Blizzard's own error
   handler already guards for this:
   `if canaccessvalue(formattedMessage) then addframetext(...)`
   `Blizzard_ScriptErrors/Blizzard_ScriptErrors.lua:75-83`.

### 2.4 Taint at a distance — what it actually looks like

Taint's defining nuisance is that the error surfaces in *Blizzard* code, in a
file your addon never touched. Real, currently-filed examples (Tier 2 —
observed behaviour, and where labelled, Blizzard agreement that it is a bug;
never evidence of intended design):

- **WoWUIBugs #801** *"MoneyFrame.lua error: attempt to perform arithmetic on a
  secret value (GameTooltip money)"* — labels `Acknowledged by Blizzard`.
  Stack is entirely Blizzard: `MoneyFrame.lua:303` ← `SetTooltipMoney` ←
  `GameTooltip_OnTooltipAddMoney` ← `TooltipDataRules.lua:146` ←
  `AlertFrameSystems.lua:447` on a loot-alert mouseover. Blizzard's 12.0.7 fix
  was a new API (`GameTooltip_AddMoneyLine`) plus removing every internal
  `SetTooltipMoney` call.
- **WoWUIBugs #804** *"MathUtil.lua:28: attempt to compare local 'max' (a secret
  value) after opening a modified player menu in a dungeon"* — reproduced with
  **all addons disabled** via a **one-line** `/run Menu.ModifyMenu(...)` snippet.
  Stack: `MathUtil.lua:28` ← `LayoutFrame.lua:225` ← `Menu.lua:1467
  PerformLayout`. Labels `Bug` + `Mainline` only — **not** `Acknowledged by
  Blizzard`. ⚠ The report is against **12.0.0.65560 (Midnight prepatch)**, six
  patches behind live; the issue is closed and has not been re-verified at
  12.0.7 here.
- **WoWUIBugs #453** *"Map canvas overlays, click, and mouse action handlers
  taint the UI"* — `Acknowledged by Blizzard` + `High Priority`; **closed**.
- **WoWUIBugs #826** *"Dropdown taint breaking VisitHouse and Communities frame
  during encounter combat"* (open).
- **WoWUIBugs #811** *"Tooltip secret value error inside LayoutFrame.lua"*
  (open; labels `Bug`, `Regression`, `Mainline`, `Default UI`).

(Labels and states re-checked via `gh api repos/Stanzilla/WoWUIBugs/issues/<n>`
on 2026-07-23.)

A `taint` search of the tracker returns ~86 issues and a `secret value` search
13 (counts recorded in `sources.md` §2.2, 2026-07-23).

---

## 3. The sanctioned escape hatch: secure frames, templates, handlers

### 3.1 Secure action buttons

`Blizzard_FrameXML/SecureTemplates.xml` defines three templates
(the whole file is 26 lines):

| Template | Line | Notes |
|---|---|---|
| `SecureActionButtonTemplate` | :4-10 | inherits `SecureFrameTemplate`, mixin `SecureActionButtonMixin`, `OnClick="SecureActionButton_OnClick"` |
| `InsecureActionButtonTemplate` | :13-18 | **not protected**; its OnClick body is literally `if not InCombatLockdown() then SecureActionButton_OnClick(self, button, down); end` |
| `SecureUnitButtonTemplate` | :21-25 | `OnClick="SecureUnitButton_OnClick"` |

Two Tier-1 comments in that file bound what an addon gets: *"Our usage of this
template will always override this and supply the extra arguments, and for now
AddOns won't be able to have `isKeyPress` or `isSecureAction` set"* (:6-7, and
again at :15 for the insecure variant). `SecureFrameTemplate` itself is defined
one line long in `SecureTemplatesBase.xml:4`; that same file also ships four
`Insecure*PropagatorTemplate` frames (:14-17) which are *not* protected — the
naming is deliberate and easy to misread.

Behaviour is entirely attribute-driven. `SecureTemplates.lua` builds a
dispatch table `local SECURE_ACTIONS = {}` at :254 and populates **30** action
types, each keyed by the frame's `type` attribute:

`action` · `actionbar` · `actionrelease` · `assist` · `attribute` ·
`cancelaura` · `click` · `destroytotem` · `equipmentset` · `flyout` · `focus` ·
`item` · `leavevehicle` · `macro` · `mainassist` · `maintank` · `menu` ·
`multispell` · `outfit` · `pet` · `raidtarget` · `returnhome` · `spell` ·
`stop` · `target` · `teleporthome` · `togglemenu` · `toy` · `visithouse` ·
`worldmarker`
(`SecureTemplates.lua:256-660`; extracted with
`grep -oE 'SECURE_ACTIONS\.[a-z]+' | sort -u` → 30)

Attribute names support a modifier/button grammar documented in the file header
(`SecureTemplates.lua:6-30`): `"<modifier>-<name><button>"`, with `*` as a
wildcard for either part, and `ATTRIBUTE_NOOP = ""` (:22) to punch an explicit
hole in a wildcard. So `self:SetAttribute("*type*", "spell")` plus
`self:SetAttribute("shift-type1", ATTRIBUTE_NOOP)` is the shape.

The dispatcher resolves button → unit → action type
(`GetConvertedButtonUnitAndActionType`, :688-725), including the
`harmbutton`/`helpbutton` remap by unit disposition (:698-704), and refuses if
the unit does not exist (:716-718, `if unit and unit ~= "none" and not
UnitExists(unit) then return nil; end`).

### 3.2 Secure handler snippets

`Blizzard_RestrictedAddOnEnvironment/SecureHandlerTemplates.xml` (106 lines)
defines **ten** templates (an earlier draft said nine while listing ten — the
file has ten `<Frame>`/`<Button>` elements, at :6, :13, :21, :29, :37, :45, :56,
:67, :78, :90), each binding a widget script to a named attribute whose value is
a **string of restricted Lua**:

| Template | Line | Snippet attribute(s) |
|---|---|---|
| `SecureHandlerBaseTemplate` | :6 | — (`SecureHandler_OnLoad` only) |
| `SecureHandlerStateTemplate` | :13 | `OnAttributeChanged` → `_onstate-*` |
| `SecureHandlerAttributeTemplate` | :21 | `OnAttributeChanged` → `_onattributechanged` |
| `SecureHandlerClickTemplate` | :29 | `_onclick` |
| `SecureHandlerDoubleClickTemplate` | :37 | `_ondoubleclick` |
| `SecureHandlerDragTemplate` | :45 | `_ondragstart`, `_onreceivedrag` |
| `SecureHandlerShowHideTemplate` | :56 | `_onshow`, `_onhide` |
| `SecureHandlerMouseUpDownTemplate` | :67 | `_onmouseup`, `_onmousedown` |
| `SecureHandlerMouseWheelTemplate` | :78 | `_onmousewheel` |
| `SecureHandlerEnterLeaveTemplate` | :90 | `_onenter`, `_onleave` (guarded on `motion`) |

`SecureHandler_OnLoad` installs four convenience methods on the frame —
`Execute`, `WrapScript`, `UnwrapScript`, `SetFrameRef`
(`SecureHandlers.lua:752-757`) — wrapping the globals
`SecureHandlerExecute(frame, body)` (:680), `SecureHandlerWrapScript(frame,
script, header, preBody, postBody)` (:602), `SecureHandlerUnwrapScript(frame,
script)` (:646) and `SecureHandlerSetFrameRef(frame, label, refFrame)` (:702).

**The snippet sandbox is genuinely restricted, and the restrictions are
syntactic.** `RestrictedExecution.lua:BuildRestrictedClosure` rejects a body
before compiling it:

```lua
if (body:match("function")) then
    return nil, "The function keyword is not permitted";
end
if (body:match("[{}]")) then
    return nil, "Direct table creation is not permitted";
end
```
`Blizzard_RestrictedAddOnEnvironment/RestrictedExecution.lua:58-66`
(the same `function` check is applied to the signature, :68-71)

The environment handed to snippets is an explicit allow-list —
`RESTRICTED_FUNCTIONS_SCOPE` at `RestrictedEnvironment.lua:24-77`: `math`,
`string`, `select`, `tonumber`, `tostring`, the `str*` family, and the `math`
scalar functions. `table` is deliberately excluded — the comment says
*"table is provided elsewhere, as direct tables are not allowed"* (:27). Game
state is exposed only at macro-conditional granularity via
`DIRECT_MACRO_CONDITIONAL_NAMES` (:81+): `SecureCmdOptionParse`,
`GetShapeshiftForm`, `IsStealthed`, `UnitExists`, `UnitIsDead`, `UnitIsGhost`,
`UnitPlayerOrPetInParty`, `UnitPlayerOrPetInRaid`, the modifier-key predicates,
`IsModifiedClick`, `GetMouseButtonClicked`, …

**The whole secure-handler API refuses to run in combat**, by design and with a
literal error:

```lua
if (InCombatLockdown()) then
    -- This shouldn't ever happen because API frame is protected,
    -- but just in case someone does something silly...
    error("Cannot use SecureHandlers API during combat");
```
`SecureHandlers.lua:435-439`

### 3.3 State drivers and unit watches

`SecureStateDriver.lua` (197 lines) is small enough to read whole. It exposes
`RegisterAttributeDriver(frame, attribute, values)` /
`UnregisterAttributeDriver` (:8, :16) and the thin bridges
`RegisterStateDriver(frame, state, values)` →
`RegisterAttributeDriver(frame, "state-"..state, values)` (:26-28), plus
`RegisterUnitWatch(frame, asState)` / `UnregisterUnitWatch` (:38, :47) and
`UnitWatchRegistered(frame)` (:69).

Concrete facts worth knowing:
- Attribute names beginning with `_` are rejected outright
  (`attribute:sub(1, 1) ~= "_"`, :9).
- The whole thing is driven by macro-conditional evaluation:
  `local newValue = SecureCmdOptionParse(values)` (`resolveDriver`, :95-96).
- `"state-visibility"` is special-cased to `Show`/`Hide` plus a
  `statehidden` attribute (:98-104).
- **It is polled, not event-driven, at 0.2 s by default**:
  `STATE_DRIVER_UPDATE_THROTTLE = 0.2` (:63, consumed at :119-122). The 0.2 is a
  *default*, not a constant — `SecureStateDriverManager_OnAttributeChanged`
  accepts an `updatetime` attribute that overwrites it (`:173-174`). The twelve
  registered events
  (`MODIFIER_STATE_CHANGED`, `ACTIONBAR_PAGE_CHANGED`, `UPDATE_BONUS_ACTIONBAR`,
  `PLAYER_ENTERING_WORLD`, `UPDATE_SHAPESHIFT_FORM`, `UPDATE_STEALTH`,
  `PLAYER_TARGET_CHANGED`, `PLAYER_FOCUS_CHANGED`, `PLAYER_REGEN_DISABLED`,
  `PLAYER_REGEN_ENABLED`, `UNIT_PET`, `GROUP_ROSTER_UPDATE`; :185-196) only
  force the next tick by setting `timer = 0` (:143). The file explicitly says
  mouseover and others' target changes are
  *"deliberately ignoring … because they change so much"* (:197).

`SecureGroupHeaders.lua` (1092 lines) is the party/raid frame factory; its
contract is a large attribute set read via `GetAttribute` — `template`,
`templateType`, `point`, `xOffset`, `yOffset`, `sortDir`, `columnSpacing`,
`startingIndex`, `unitsPerColumn`, `maxColumns`, `columnAnchorPoint`,
`minWidth`, `minHeight`, `showRaid`, `showParty`, `showSolo`, `showPlayer`,
`nameList`, `groupFilter`, `roleFilter`, `sortMethod`, `groupBy`,
`groupingOrder`, `strictFiltering`, `initialConfigFunction`,
`_initialAttributeNames`, `_initialAttribute-<name>`, `_ignore`
(`SecureGroupHeaders.lua:67, 111-123, 130-144, 163-165, 180, 250-251, 262-274, 392-396, 412, 463`).
Note :123 — initial attributes are copied through `scrub()`.

### 3.4 A readable worked example (Tier 3)

oUF is the smallest complete real user of this machinery (784 K). It builds
`PetBattleFrameHider` from `SecureHandlerStateTemplate` (`oUF/ouf.lua:22`),
defaults headers to `SecureGroupHeaderTemplate` (:643), sets the child template
to `'SecureUnitButtonTemplate, SecureHandlerStateTemplate,
SecureHandlerEnterLeaveTemplate, PingableUnitFrameTemplate'` (:649), hands the
click-cast header over with `SecureHandlerSetFrameRef(header,
'clickcast_header', _G.Clique.header)` (:705), creates single frames as
`CreateFrame('Button', name, PetBattleFrameHider, 'SecureUnitButtonTemplate,
PingableUnitFrameTemplate')` (:736) and drives visibility with
`RegisterUnitWatch(object)` (:743). That is one addon's arrangement, not a
required one.

Across the seven surveyed clones, the secure-template footprint is uneven:
ElvUI 21 files, Details 2, Plater 2, oUF 2, **BigWigs 0, WeakAuras 0, Ace3 0**
(the exact grep is in §5). Reading that as "secure templates are for unit frames
and action bars, not for boss mods or aura displays" is an inference, not a
documented rule.

---

## 4. Secret values — the 12.0 addition

### 4.1 What a secret is

> The easiest way to think of Secret Values (Secrets) is that they are like
> black boxes, which contain a Lua value of any type (number, string, boolean,
> etc) inside them. Insecure (tainted) Lua code can receive Secrets from our
> APIs and pass those Secrets into certain APIs, but it cannot actually see the
> value that is inside of that box.
>
> — Blizzard, *Midnight Public Alpha Addon API Changes*, 2025-10-01
> (Tier 2 archive: `Patch 12.0.0/Planned API changes`, revid 6746061)

Secrecy is a property of the **value**, and the restriction is a property of the
**path**. Untainted code operates on secrets normally.

### 4.2 The operation table

From Tier 2 (`Secret Values`, revid 6777907, 2026-07-22), which is the only
consolidated statement of the rules. **When a disallowed operation happens the
result is an immediate Lua error**, not a nil return.

| Operation on a secret, from tainted code | Allowed? |
|---|---|
| Store in a local / upvalue / table **value** | ✅ |
| Pass to a **Lua** function | ✅ |
| Pass to a **C** function | ❌ unless that API is explicitly marked (§4.5) |
| Concatenate, if string or number | ✅ |
| `string.format` / `string.join` / `string.concat` | ✅ |
| Arithmetic | ❌ |
| Compare (`==`, `<`, …) | ❌ |
| Boolean test on a **boolean** secret | ❌ |
| Boolean test on a **non-boolean** secret | ✅ (type isn't secret: nil→false, everything else→true) |
| Length operator `#` | ❌ |
| Use as a table **key** | ❌ |
| Index or index-assign (`secret.foo`, `secret["foo"] = 1`) | ❌ |
| Call it as a function | ❌ |
| `type(secret)` | ✅ — **returns the real type** |

### 4.3 The traps

**Trap 1 — `type()` is not a guard.** `type(secret)` returns `"number"`,
`"string"`, etc. So

```lua
if type(v) == "number" and v > 0 then   -- the comparison ERRORS on a secret
```

passes the type check and blows up on the comparison. Tier 2 states this
explicitly (`Secret Values`, revid 6777907: *"Querying the type of a secret
value type(secret) returns its real type"*). Blizzard's own dumper is written to
match — it takes `local valType = type(val)` and then separately asks
`canaccessvalue(val)`. Exact lines in `Blizzard_SharedXML/Dump.lua` (re-checked
by `grep -n`, an earlier draft was off by up to 3 on four of them):
`type(val)` :98 → `canaccessvalue(val)` :106, :113 (in `prepSimple`);
`type(val)` :149 → `canaccessvalue(val)` :151;
`type(val)` :309 → `issecretvalue(val)` :312 → `canaccessvalue`/`canaccesstable`
:315 (in `DevTools_DumpValue`);
`type(value)` :406 → `canaccesstable(value)` :407.
The correct guard is `issecretvalue(v)` or `canaccessvalue(v)`, never `type()`.

**Trap 2 — truthiness is type-dependent.** `if secretNumber then` is legal;
`if secretBoolean then` errors. You cannot tell which you have without asking.

**Trap 3 — the error lands in Blizzard's file.** See §2.4; WoWUIBugs #801 and
#804 are the canonical shapes (`attempt to perform arithmetic on a secret
value`, `attempt to compare local 'max' (a secret value)`).

**Trap 4 — a secret you store propagates.** Putting a secret into a *shared*
table is legal, but the next consumer inherits the problem. Blizzard's own
object pools refuse it outright:

```lua
-- ... if one secret object enters a pool, all future acquisitions end up
-- being secret too.
if issecretvalue(object) then
    assertsafe(false, "attempted to release a secret value into a pool: %s", tostring(object));
```
`Blizzard_SharedXMLBase/Pools.lua:265-277`

**Trap 5 — writing a secret as a table key by *untainted* code poisons the
table permanently.** Tier 2 (`Secret Values`): *"When untainted code stores a
secret value as a table key, the table itself is irrevocably marked with both
of the aforementioned flags"* — i.e. indexed access yields secrets **and**
tainted code cannot touch it at all.

### 4.4 Testing for secrets

Nine primitives, **all in the generated docs** in
`Blizzard_APIDocumentationGenerated/FrameScriptDocumentation.lua`
(this corrects `sources.md` **§1.2** — the "Global coverage is partial" bullet —
and **§7**, whose routing line calls `issecretvalue`, `hasanysecretvalues` and
`scrub` "wiki-only globals". That is true of
`issecure`/`issecurevariable`/`securecall`/`forceinsecure`, but **not** of the
secret family, which is fully documented at Tier 1):

| Function | Line | Documentation string (verbatim from the file) |
|---|---|---|
| `issecretvalue(value)` | :244 | "Returns true if a supplied value is a secret value." |
| `hasanysecretvalues(...)` | :210 | "Returns true if a supplied value is a secret value." (varargs form) |
| `issecrettable(t)` | :227 | "…true if the table value itself is secret, or if flags on the table are set such that accesses of the table would produce secrets." |
| `canaccessvalue(value)` | :65 | "…the immediate calling function has appropriate permissions to access and operate on a specific value." |
| `canaccessallvalues(...)` | :20 | varargs form of the above |
| `canaccesstable(t)` | :48 | "…false if the caller cannot access the table value itself, or if access to the table contents is disallowed by taint." |
| `canaccesssecrets()` | :37 | "…true if the immediate calling function has appropriate permissions to access or operate on secret values." |
| `scrub(...)` | :348 | nils secrets **and** anything not string/number/boolean |
| `scrubsecretvalues(...)` | :331 | nils secrets only |

Plus three that change state rather than report it:
`secretwrap(...)` (:383, "Converts all supplied values to secret values"),
`secretunwrap(...)` (:365, `HasRestrictions = true` — "Unwraps all supplied
secrets"), and `dropsecretaccess()` (:131, "Removes the ability for the
immediate calling function to access secret values"). `mapvalues(func, ...)`
(:261) applies a function across a varargs list in place.

Tables get their own lever: `SetTableSecurityOption(table, option)`
(:429, `HasRestrictions = true`) with
`Enum.TableSecurityOption = DisallowTaintedAccess 0, DisallowSecretKeys 1,
SecretWrapContents 2` (:490-501).

**[gap] — a real inconsistency I could not resolve.** **Eight** of those nine
carry `SecretArguments = "AllowedWhenUntainted"` in the same file. (The ninth,
`canaccesssecrets`, takes **no arguments at all** and therefore carries no
`SecretArguments` field — an earlier draft said "every one of those nine", which
is wrong. `dropsecretaccess` is likewise argument-less and unannotated.) Read
literally against the wiki's definition of that value (§4.5), a *tainted*
caller could not pass a secret to `issecretvalue` — which would make the
function useless to addons, and directly contradicts Blizzard's own blue post
(*"you can also test if a value is Secret by calling the issecretvalue API"*,
addressed to addon authors) and the wiki's *"AddOns can test secrets via the
following functions"*. Three of the seven surveyed addons call it from addon
code and ship (§5). The likely explanation is the argument type: these are the
only two files in the whole generated-doc corpus that use
`Type = "LuaValueReference"` (`FrameScriptDocumentation.lua`, 24 uses;
`LuaTableUtilDocumentation.lua`, 6 uses), which reads as "a reference to a
value, not the value itself". **I could not find any Tier-1 or Tier-2 statement
confirming that `LuaValueReference` arguments are exempt from `SecretArguments`.
Do not build a claim on either reading.**

### 4.5 `SecretArguments` — the three-way, and the table that actually matters

Every documented API may declare whether it accepts secrets. Semantics are
Tier 2 (`Secret Values`, revid 6777907):

| Value | Meaning | Count at 12.0.7.68887 |
|---|---|---|
| `"AllowedWhenUntainted"` | accepts secrets **only if execution isn't tainted** — i.e. **not from addon code** | **3473** |
| `"AllowedWhenTainted"` | always accepts secrets | **120** |
| `"NotAllowed"` | never accepts secrets, even from untainted callers | **84** |

(`grep -rh 'SecretArguments = ' … | sed 's/.*= //' | sort | uniq -c`)

Because all addon code is tainted, **`AllowedWhenTainted` is the real
"you may hand a secret to this" list, and it has 120 members.** The widget half
of it — the part that governs "can I display this secret without computing on
it" — is:

- **FontString**: `SetText`, `SetFormattedText`, `SetTextToFit`, `SetTextColor`
  (`SimpleFontStringAPIDocumentation.lua:653, 528, 698, 664`)
- **Frame / Region**: `SetAlpha`, `SetAlphaFromBoolean`, `SetID`
  (`SimpleFrameAPIDocumentation.lua:1029, 1040, 1245`); `SetAlpha`,
  `SetAlphaFromBoolean`, `SetVertexColor`, `SetVertexColorFromBoolean`
  (`SimpleRegionAPIDocumentation.lua:123, 134, 191, 205`)
- **StatusBar**: `SetValue`, `SetMinMaxValues`, `SetStatusBarColor`,
  `SetStatusBarDesaturated`, `SetStatusBarDesaturation`
  (`SimpleStatusBarAPIDocumentation.lua:331, 216, 259, 273, 284`)
- **Texture**: `SetTexture`, `SetAtlas`, `SetColorTexture`, `SetTexCoord`,
  `SetSpriteSheetCell`, `SetRotation`, `SetDesaturated`, `SetDesaturation`
  (`SimpleTextureBaseAPIDocumentation.lua:441, 278, 313, 417, 402, 380, 326, 337`)
- **VertexColor animation**: `SetEndColor`, `SetStartColor`
  (`SimpleAnimVertexColorAPIDocumentation.lua:36, 46`)
- **Cooldown**: only the *style* setters — `SetDrawBling`, `SetDrawEdge`,
  `SetDrawSwipe`, `SetEdgeColor`, `SetSwipeColor`
  (`FrameAPICooldownDocumentation.lua:384, 395, 406, 417, 506`)
- **Tooltip**: `SetText` (`FrameAPITooltipDocumentation.lua:107`)

and the data half is dominated by `C_Spell` — **42 of the 120** live in
`SpellDocumentation.lua` alone, i.e. essentially the whole spell-info surface
takes secrets (`GetSpellCooldown`:249,
`GetSpellCharges`:231, `GetSpellTexture`:517, `GetSpellName`:440,
`GetSpellInfo`:338, `IsSpellUsable`:873, `IsSpellInRange`:841, …, all in
`SpellDocumentation.lua`), several `C_UnitAuras.*`
(`GetPlayerAuraBySpellID`:332, `GetUnitAuraBySpellID`:369,
`GetCooldownAuraBySpellID`:299, `GetAuraBaseDuration`:133 —
`UnitAuraDocumentation.lua`), `UnitName`:2368, `UnitNameFromGUID`:2385,
`UnitClassFromGUID`:933, `UnitTokenFromGUID`:3150
(`UnitDocumentation.lua`), the `C_StringUtil.*` escape/format helpers
(`StringUtilDocumentation.lua:41-222`), `AbbreviateNumbers` /
`BreakUpLargeNumbers` / `AbbreviateLargeNumbers`
(`LocalizationDocumentation.lua:10, 26, 42`), `C_ColorUtil.WrapTextInColor`
and friends (`ColorUtilDocumentation.lua:91, 107, 124`),
`C_ClassColor.GetClassColor` (`ClassColorDocumentation.lua:11`) and
`Ambiguate` / `C_PlayerInfo.GetPlayerInfoByGUID`
(`PlayerScriptDocumentation.lua:22, 675`).

⚠ **`Cooldown:SetCooldown` is *not* on that list.** `SetCooldown`,
`SetCooldownDuration`, `SetCooldownFromExpirationTime` and `SetCooldownUNIX`
all carry `SecretArguments = "AllowedWhenUntainted"` together with
`SecretArgumentsAddAspect = { Enum.SecretAspect.Cooldown }`
(`FrameAPICooldownDocumentation.lua:280-283, 293-296, 316-319, 329-332`).
Read against the Tier-2 definition of `AllowedWhenUntainted`, **tainted addon
code cannot pass a secret number to any of the four.** `sources.md` §4 asserts
the opposite ("they DO accept secrets") on the strength of the absence of
`NotAllowed`; that reading drops the untainted/tainted distinction and should
be corrected. The sanctioned path for secret cooldown data is instead §4.8.

### 4.6 Aspects, anchors, and const accessors

Passing a secret into a widget setter *marks the object*. Three distinct
outcomes:

**(a) Aspect.** If the setter carries `SecretArgumentsAddAspect`, the object
gains that aspect and every getter carrying the matching
`SecretReturnsForAspect` starts returning secrets. **52 setters** add aspects
and **82 getters** derive secrecy from them (counted by scripted extraction over
the generated docs). `Enum.SecretAspect` is a bitfield with 29 members
(`SecretAspectConstantsDocumentation.lua:5-42`):

`ObjectDebug` · `ObjectName` · `ObjectType` · `ObjectSecrets` · `ObjectSecurity`
· `Attributes` · `Hierarchy` (all reported `EnumValue = 1` — see the caveat
below) · `ID` 2 · `Toplevel` 4 · `Text` 8 · `SecureText` 16 · `Shown` 32 ·
`Scale` 64 · `Alpha` 128 · `FrameLevel` 256 · `ScrollRange` 512 · `Cursor` 1024
· `VertexColor` 2048 · `Desaturation` 4096 · `TexCoords` 8192 · `BarValue` 16384
· `Cooldown` 32768 · `Rotation` 65536 · `MinimumWidth` 131072 · `Padding` 262144
· `CooldownStyle` 524288 · `TooltipTexture` 1048576 · `ButtonState` 2097152 ·
`ScrollOffset` 4194304

⚠ The first seven members all report `EnumValue = 1` **in the shipped file
itself** (`SecretAspectConstantsDocumentation.lua:13-19`) — this is not a
tooling artefact on our side. Header says `NumValues = 29, MinValue = 1,
MaxValue = 4194304`. Do not do bit arithmetic on those seven.

Worked example, all Tier 1, **and the only one of the two an addon can actually
trigger**: `FontString:SetText` adds `Text`
(`SimpleFontStringAPIDocumentation.lua:653-656`) and is
`SecretArguments = "AllowedWhenTainted"`, so tainted addon code *can* feed it a
secret; `FontString:GetText` then returns secret for `Text` (`:352`).

⚠ `Frame:SetShown` also declares
`SecretArgumentsAddAspect = { Enum.SecretAspect.Shown }`
(`SimpleFrameAPIDocumentation.lua:1354-1358`), and `IsShown` **and** `IsVisible`
derive from `Shown` (`:841, :895`) — but `SetShown` is *both*
`SecretArguments = "AllowedWhenUntainted"` **and** `IsProtectedFunction = true`,
so an addon cannot set that aspect by passing a secret. If your `IsShown` starts
returning a secret, the aspect was applied by *untainted* (Blizzard) code, not by
you. An earlier draft used this as the headline worked example without that
caveat.

Aspects do not share state — an object with `Shown` set still returns clean
values from the `Alpha` getters.

Query with `FrameScriptObject:HasSecretAspect(aspect)` /
`HasAnySecretAspect()` (`SimpleFrameScriptObjectAPIDocumentation.lua:52, 38`).

An aspect can also **block a call outright**, not just secrete its return. The
`RequiresFontStringTextAccess` precondition — *"Guarded APIs reject access for
tainted callers if the object has the secret Text aspect assigned"*,
`failureMode = ReturnNothing` (`SecretPredicatesDocumentation.lua:21`) — is
applied to exactly two APIs, both text-measurement:
`FontString:CalculateScreenAreaFromCharacterSpan`
(`SimpleFontStringAPIDocumentation.lua:10`, marker at `:12`) and
`FontString:FindCharacterIndexAtCoordinate` (`:72`, marker at `:75`;
an earlier draft said `:73`). So a FontString that has
ever been fed a secret string stops being measurable by tainted code, which is
a layout problem, not a display problem.

**(b) Whole-object secrecy.** A setter that accepts secrets but has *no*
declared aspect marks the object as having secret values —
`HasSecretValues()` (`SimpleFrameScriptObjectAPIDocumentation.lua:69`) — and
that in turn marks all anchoring/positioning data secret, propagating **down**
the anchor chain to dependents but not up.
`ScriptRegion:IsAnchoringSecret()` (`SimpleScriptRegionAPIDocumentation.lua:367`)
tests it; `IsAnchoringRestricted()` (`:353`) is the neighbouring query.
The propagation rule is Tier 2 + blue post, not the generated docs.

⚠ **The wiki's own example for this case is stale.** `Secret Values`
(revid 6777907, 2026-07-22) says *"calling StatusBar:SetValue(value) with a
secret numeric value does not apply an explicit aspect"*. At 12.0.7.68887
`SetValue` carries `SecretArgumentsAddAspect = { Enum.SecretAspect.BarValue }`
(`SimpleStatusBarAPIDocumentation.lua:331-334`), so it **does**. Prefer the
generated docs for any specific API.

**(c) Const accessor.** `ConstSecretAccessor = true` (**37** occurrences).
Tier 1 gives only the marker — there is no `Documentation` string on it anywhere
in the corpus. The semantics are **Tier 2** (`Secret Values`, revid 6777907):
*"Calling these functions with secret values does not apply any aspects nor does
it mark the object as having secret values, however the return values of the
function will be implicitly secret."* The wiki's own example is
`ScriptRegion:GetHeight(ignoreRect)`. Examples in the docs:
`ScriptRegion:GetHeight` (`SimpleScriptRegionAPIDocumentation.lua:136`),
`GetWidth` (:283), `GetSize` (:236), `IsMouseOver` (:459), `HasScript` (:300);
`Frame:GetAttribute` (`SimpleFrameAPIDocumentation.lua:260`),
`IsEventRegistered` (:681); `FrameScriptObject:HasSecretAspect`
(`SimpleFrameScriptObjectAPIDocumentation.lua:52`), `IsObjectType` (:97);
`ScriptRegionResizing:GetPoint` (`SimpleScriptRegionResizingAPIDocumentation.lua:65`).

**Clearing.** `FrameScriptObject:SetToDefaults()` is the only documented way to
clear aspects and secret state, and it is itself `IsProtectedFunction = true`
(`SimpleFrameScriptObjectAPIDocumentation.lua:136`) — so it is unavailable to
tainted code on a protected frame in combat. Clearing anchor points is
separately said to reset the anchoring-secret state (Tier 2).
`IsPreventingSecretValues()` (`:114`) exists; **[gap]** — no Tier-1 or Tier-2
prose explains what sets it. There is no documented `PreventSecretValues`
setter in the generated docs.

### 4.7 Predicates: *when* a return is secret

51 predicates are declared across the corpus, split `Type = "Precondition"` (32)
and `Type = "Secret"` (19). They are **not** all in one file:
`SecretPredicatesDocumentation.lua` declares 25 of them (7 `Precondition` at
:9-42, 18 `Secret` at :48+); the other 26 are declared in the per-system file
that uses them (e.g. `MouseFocusValidForLimitedInput` at
`InputDocumentation.lua:329`, `RequiresClubsInitialized` at
`ClubDocumentation.lua:1973`, `RestrictedForMacroChatMessages` at
`ChatConstantsDocumentation.lua:233`). Full dump:
`uv run python -m wowkb.uiapi predicates`.

The two kinds behave differently, and the `failureMode` field proves it:

```
Type = "Secret"        19   failureMode = None            (all 19)
Type = "Precondition"  32   failureMode = ReturnNothing   20
                            failureMode = Error            5
                            failureMode = ReturnWithError  5
                            failureMode = None             2
```

A `Secret` predicate never changes *whether* the call succeeds — it changes
what the return **is**. A `Precondition` predicate changes whether you get a
value at all. Conflating the two is the difference between "guard the value"
and "guard the call".

The distinction that most sources get wrong:

- **Unconditional.** `SecretReturns = true` — **18 functions**, always secret.
  `UnitHealth` (`UnitDocumentation.lua:1446`), `UnitHealthMissing` (:1408),
  `UnitHealthPercent` (:1426), `UnitPercentHealthFromGUID` (:2514),
  `UnitGetIncomingHeals` (:1237), `UnitGetTotalAbsorbs` (:1254),
  `UnitGetTotalHealAbsorbs` (:1270), `UnitCastingDuration` (:798),
  `UnitInRange` (:1618), `UnitPowerBarTimerInfo` (:2643),
  `UnitSpellTargetClass` (:3003), `UnitSpellTargetName` (:3020),
  `PlayerIsSpellTarget` (:510), `ClosestUnitPosition` (:53),
  `ClosestGameObjectPosition` (:34),
  `C_CombatText.GetCurrentEventInfo` (`CombatTextDocumentation.lua:21`),
  `C_RaidMarkers.GetRaidTargetIndex` (`RaidMarkersDocumentation.lua:36`),
  `C_SpellDiminishUI.ShouldTrackSpellDiminishCategory`
  (`SpellDiminishUIDocumentation.lua:52`).
- **Conditional.** e.g. `UnitPower` is `SecretWhenUnitPowerRestricted`
  (`UnitDocumentation.lua:2610`); `UnitName` is
  `SecretWhenUnitIdentityRestricted` (`:2368`);
  `C_Spell.GetSpellCooldown` is `SecretWhenCooldownsRestricted`
  (`SpellDocumentation.lua:249`).

Observed application counts at this build (`grep -rh '<predicate> = true' … | wc -l`):
`SecretInChatMessagingLockdown` 98 · **`SecretWhenUnitStatsRestricted` 50**
(omitted from an earlier draft — it is the second-widest) ·
`SecretWhenUnitAuraRestricted` 20 ·
`SecretWhenUnitIdentityRestricted` 15 · `SecretWhenCooldownsRestricted` 14 ·
`SecretWhenInCombat` 4 · `SecretInActivePvPMatch` 2 ·
**`SecretOnRestrictedMaps` 0** — declared as a predicate
(`SecretPredicatesDocumentation.lua:58`) but applied to zero documented entries
at 12.0.7.68887.

Predicates can be evaluated directly. `C_Secrets` (system `SecretUtil`,
`SecretPredicateAPIDocumentation.lua`) exposes **27** functions, including
`HasSecretRestrictions()`, `ShouldCooldownsBeSecret()`, `ShouldAurasBeSecret()`,
`ShouldUnitIdentityBeSecret(unit)`, `ShouldUnitPowerBeSecret(unit, powerType)`,
`ShouldUnitAuraInstanceBeSecret(unit, auraInstanceID)`,
`ShouldSpellCooldownBeSecret(spellIdentifier)`,
`CanCompareUnitTokens(unit1, unit2)`, `GetSpellAuraSecrecy(spellIdentifier)`.
Secrecy levels are `Enum.SecrecyLevel = NeverSecret 0, AlwaysSecret 1,
ContextuallySecret 2` (`SecretWrapperConstantsDocumentation.lua:6`) — several
predicate descriptions note that per-spell / per-power-type flags **take
priority over the ambient restriction**.

Events can carry secret payloads too: `SecretPayloads = true` on 7 events —
`MINIMAP_PING` (`MinimapDocumentation.lua:261`), `RUNE_POWER_UPDATE` (:3873)
and `RUNE_TYPE_UPDATE` (:3885), `UNIT_DISTANCE_CHECK_UPDATE` (:4086),
`UNIT_IN_RANGE_UPDATE` (:4160), `UNIT_MAX_HEALTH_MODIFIERS_CHANGED` (:4214)
in `UnitDocumentation.lua`, and
`UNIT_SPELL_DIMINISH_CATEGORY_STATE_UPDATED` (`SpellDiminishUIDocumentation.lua:77`).
`ConditionalSecret` appears 17 times at return-field level.

### 4.8 Curves and Durations — computing on secrets without seeing them

Blizzard's answer to "I need a health-coloured bar / a cooldown sweep but I
can't do the arithmetic":

- **Curves.** `C_CurveUtil.CreateCurve()` (`CurveUtilDocumentation.lua:21`,
  returns a `LuaCurveObject`) and `C_CurveUtil.CreateColorCurve()` (`:11`,
  returns a `LuaColorCurveObject`). `UnitHealthPercent(unit, usePredicted,
  curve)` takes a curve and returns *"If no curve is specified, a floating point
  percentage value. Else, the result of evaluating the curve with the percentage
  as the input"* (`UnitDocumentation.lua:1426-1443`). The evaluation happens
  in C; your Lua never sees the number.
  `C_CurveUtil.EvaluateColorFromBoolean` / `EvaluateColorValueFromBoolean` are
  both `SecretArguments = "AllowedWhenTainted"`
  (`CurveUtilDocumentation.lua:31, 49`) — a secret boolean can pick a colour.
- **Durations.** `C_DurationUtil.CreateDuration()` (`:11`),
  `CreateDurationTextBinding()` (`:21`), `CreateManualClock()` (`:31`) — all in
  `DurationUtilDocumentation.lua`; an earlier draft cited `:3-9`, which is the
  system header, not the functions. A `LuaDurationObject`
  (`LuaDurationObjectAPIDocumentation.lua`) carries `SetTimeFromStart`,
  `SetTimeFromEnd`, `SetTimeSpan`, `GetRemainingDuration`, `HasExpired`,
  `IsActive`, `EvaluateRemainingPercent(curve, modifier)`
  (`SecretWhenCurveSecret`), `FormatRemainingDuration(formatter, modifier)`
  (`SecretWhenNumericFormatterSecret`), and — importantly —
  `HasSecretValues()` marked `ReturnsNeverSecret = true`, so you can always ask
  whether a duration is carrying secrets.
- **The join.** `C_Spell.GetSpellCooldownDuration(spellIdentifier, ignoreGCD)`
  returns a `LuaDurationObject` and carries **no secret predicate at all**
  (`SpellDocumentation.lua:267`), and
  `Cooldown:SetCooldownFromDurationObject(duration, clearIfZero)`
  (`FrameAPICooldownDocumentation.lua:305-313`) consumes one. Compare
  `C_Spell.GetSpellCooldown`, which returns a `SpellCooldownInfo` table and *is*
  `SecretWhenCooldownsRestricted` (`SpellDocumentation.lua:249`). That is the
  Tier-1 evidence for "route cooldowns through duration objects, not numbers".
  `DurationTextBinding` (`DurationTextBindingObjectAPIDocumentation.lua`) does
  the same job for a FontString, with `SetFormatter`, `SetTextFormat`,
  `SetExpiredText`, `SetUpdateInterval` and its own
  `HasSecretValues() [ReturnsNeverSecret]`. `StatusBar:SetTimerDuration(duration,
  interpolation, direction)` (`SimpleStatusBarAPIDocumentation.lua:310`) is the
  bar-shaped sink, and the wiki names it as the intended consumer
  (`Secret Values`, revid 6777907: *"These can be passed to
  StatusBar:SetTimerDuration()"*).

  ⚠ **Read the mechanism, not a whitelist.** All three duration sinks —
  `SetCooldownFromDurationObject` (`FrameAPICooldownDocumentation.lua:305`),
  `SetTimerDuration` (`:310`) and the binding APIs — are themselves
  `SecretArguments = "AllowedWhenUntainted"`, i.e. they do **not** accept a
  secret argument from addon code. That is not a contradiction: what you hand
  them is a `LuaDurationObject`, which is an ordinary (non-secret) object that
  carries the secret timing internally. The route works because the number never
  enters Lua, not because these functions are on the 120-member
  `AllowedWhenTainted` list. They are not.

### 4.9 Communication and combat log

- `COMBAT_LOG_EVENT` and `COMBAT_LOG_EVENT_UNFILTERED` carry
  `HasRestrictions = true` (`CombatLogDocumentation.lua:122, 130`); the wiki
  records that registering them now errors (`Patch 12.0.0/API changes`, revid
  6747189, 2026-06-18 — verbatim: *"COMBAT_LOG_EVENT and
  COMBAT_LOG_EVENT_UNFILTERED will error when trying to register them."*).
  `CombatLogGetCurrentEventInfo` survives only as an alias to
  `C_CombatLog.GetCurrentEventInfo` in
  `Blizzard_DeprecatedCombatLog/Deprecated_CombatLog.lua:18` — and that whole
  file early-returns unless the `loadDeprecationFallbacks` CVar is set (`:4-6`),
  so the alias is **not guaranteed to exist**. The same file's own comment
  (`:10-11`) says *"Some functions have been relocated to the secure
  environment, for which no deprecation is (intentionally) provided."*
- `SecretInChatMessagingLockdown` is by far the widest predicate — **98**
  documented entries, overwhelmingly the `CHAT_MSG_*` events themselves
  (`ChatInfoDocumentation.lua:835-2529`), the club/communities message readers
  (`ClubDocumentation.lua:400-930`), LFG search results
  (`LFGListInfoDocumentation.lua:119-408`), `GetChatLineText` /
  `GetChatLineSenderName` / `GetChatLineSenderGUID`
  (`ChatInfoDocumentation.lua:178, 162, 146`) and the voice-chat member APIs.
  Its declared condition: *"when encounter, challenge mode, or PvP match addon
  restrictions are in effect, and when the player is on a
  communication-restricted map such as a dungeon or raid"*
  (`SecretPredicatesDocumentation.lua:53`).
- `C_ChatInfo.SendAddonMessage` and `SendAddonMessageLogged` are
  `SecretArguments = "NotAllowed"` (`ChatInfoDocumentation.lua:516, 535`) —
  you can never put a secret on the wire, from any path.
- The blue post states the outbound rule directly: *"While in an instance, chat
  messages will be sent to Lua as Secret Values, and addons are not allowed to
  send communications to other players (either through addon comms or regular
  chat)."* (2025-10-01, Tier 2 archive). The `Chat` member of
  `Enum.AddOnRestrictionType` (value 5) is the corresponding runtime query.
- `RestrictedForMacroChatMessages` (`ChatConstantsDocumentation.lua:233`)
  restricts macro-initiated chat on externally observable channels during
  instance encounters.

### 4.10 What changed after 12.0.0

Predicates carry `apiname.added` stamps on the wiki (`Secret Values`, revid
6777907): `SecretWhenInCombat`, `SecretWhenUnitIdentityRestricted`,
`SecretWhenUnitAuraRestricted`, `SecretWhenAnchoringSecret` and others in
12.0.0; `SecretInActivePvPMatch`, `SecretWhenLossOfControlInfoRestricted`,
`SecretWhenUnitThreatStateRestricted`, `RequiresUnitIdentityAccess` in 12.0.1;
`SecretOnRestrictedMaps`, `SecretWhenCooldownsRestricted`,
`SecretWhenUnitStatsRestricted`, `RequiresDeclassifiedUnitIdentity` in 12.0.5;
`MouseFocusValidForLimitedInput` in 12.0.7. The page also lists
`SecretWhenAurasRestricted` and `RequiresUnitAuraAccess` as **12.1.0**, which is
ahead of live — the wiki's API index is stamped for a build this repo's
`game-version.md` says is not deployed. Neither appears in our 12.0.7.68887
checkout.

12.0.7's own security-relevant deltas, from the 2026-04-30 blue post archived at
`Patch 12.0.7/API changes` (revid 6778033, 2026-07-22):
`GameTooltip_AddMoneyLine` added and all internal `SetTooltipMoney` calls
removed; unit-identity-restricted APIs now return nil/defaults instead of
erroring on unsupported tokens; `debugstack`/`debuglocals` become secret once
anything up the stack has touched a secret; `SimulateMouse*` no longer carry
taint but are gated on `MouseFocusValidForLimitedInput`;
`GetEventCPUUsage`/`GetFunctionCPUUsage`/`GetScriptCPUUsage` returned to
addons; chat events for currency/honour/loot/money/reputation/XP gains are no
longer secret.

---

## 5. What real addons do (Tier 3 — practice, not rules)

Measured 2026-07-23 across the seven clones in `raw/addon-research/`, at the
commits recorded in `sources.md` §3.1. **Details and Plater share an author
(Tercioo) and are not independent data points.** The exact commands, so the
numbers are reproducible:

```bash
# "secret primitive" column
grep -rl -E 'issecretvalue|hasanysecretvalues|issecrettable|canaccessvalue|canaccesstable|canaccesssecrets|scrubsecretvalues|C_Secrets' --include=*.lua <addon>
# "secure template" column
grep -rl -E 'SecureHandler|RegisterStateDriver|RegisterAttributeDriver|SecureGroupHeader|SecureActionButtonTemplate|SecureUnitButtonTemplate' --include=*.lua --include=*.xml <addon>
```

| Addon | Files calling a secret primitive | Files touching secure templates/handlers |
|---|---|---|
| WeakAuras2 | 0 | 0 |
| BigWigs | 5 | 0 |
| Details | 30 | 2 |
| Plater | 11 | 2 |
| ElvUI | 1 (its vendored oUF `init.lua`) | 21 |
| oUF | 4 | 2 |
| Ace3 | 0 | 0 |

⚠ **Do not measure this with a case-insensitive `grep -i secret`.** That returns
8 files for WeakAuras — all false positives: the ability *Secret Technique*
(`WeakAurasTemplates/TriggerTemplatesData.lua:1965`), *Secret Infusion* (:3717)
and model paths like `monestarysecretdoor.m2`
(`WeakAurasModelPaths/ModelPathsClassicEra.lua:32800`). The same trap inflates
every row (ElvUI 67, Details 42).

⚠ WeakAuras' zero is **not** evidence it ignores secrets either. `.pkgmeta`
means libraries resolve at package time, so the clone has no `Libs/` directory
at all (`sources.md` §3.4), and WeakAuras is not installed on this machine to
compare against.

Two patterns are visible in more than one codebase:

**Defensive local aliasing for cross-version compat.** BigWigs:
```lua
local issecretvalue = issecretvalue or function() return false end -- XXX 12.0 compat
```
`BigWigs/Core/BossPrototype.lua:4625`, `Core/PluginPrototype.lua:86`,
`Core/Core.lua:239`, and in the Classic fork of the same file at
`Core/BossPrototype_Classic.lua:4360`; `hasanysecretvalues` the same at
`Core/BossPrototype.lua:49` and `Core/BossPrototype_Classic.lua:49`; and a
variant returning nothing at `Tools/AutoInvite.lua:69`. ElvUI's vendored
oUF does the null-safe form instead:
`return issecretvalue and issecretvalue(value)` and
`return not canaccessvalue or canaccessvalue(value)`
(`ElvUI/ElvUI_Libraries/Game/Shared/oUF/init.lua:68, 84`).

**Guard immediately before a forbidden operation.** BigWigs wraps the string
op, with the reason in the comment:
```lua
if db.emphUppercase and not self:IsSecret(text) then -- Cannot do upper or gsub on secrets :(
```
`BigWigs/Plugins/Messages.lua:933`; equality comparison guarded at
`Plugins/Bars.lua:1873`; a whole feature disabled when the trigger is secret at
`Plugins/Pull.lua:393`. oUF guards a GUID comparison at
`oUF/ouf.lua:241` and `oUF/elements/portrait.lua:62`, and inverts a string test
to `if(str and (issecretvalue(str) or str ~= '')) then` at
`oUF/elements/tags.lua:713, 726` — i.e. "treat a secret as non-empty rather
than comparing it".

ElvUI's vendored oUF also wraps `C_Secrets` prospectively:
`local ShouldUnitIdentityBeSecret = C_Secrets and C_Secrets.ShouldUnitIdentityBeSecret`
plus `CanCompareUnitTokens` on the next line (`init.lua:15-16`; an earlier draft
said `:14-15`, which is `UnitThreatSituation`) — asking the *predicate* before
the call rather than testing the *result* after.

None of the above is a rule. It is what four of seven surveyed codebases were
shipping on 2026-07-23.

---

## 6. Gaps — what I looked for and did not find

- **[gap] Blizzard's primary channel is unreadable.** Every technical statement
  quoted in §0, §4.1, §4.9 traces to a WoWUIDev Discord post
  (`discord.com/channels/327414731654692866/…`). Discord permalinks are not
  publicly fetchable. Everything here goes through the wiki's verbatim
  blockquote archive. Looked at: news.blizzard.com article 24244638 (names zero
  APIs), us.forums.blizzard.com Discourse API (no UI&Macro category exists),
  WebSearch.
- **[gap] No Blizzard-authored prose on any of this.** The generated docs are a
  shape spec — only 858 of 9521 entries carry a `Documentation` field at all.
  There is no official tutorial, no error-semantics reference, no migration
  guide.
- **[gap] Error *text* is not Tier 1, though the failure *shape* now is.**
  Tier 1 gives you the shape: `MayReturnNothing` (596 entries),
  `HasRestrictions` (**236**, re-counted — an earlier draft said 231), and a
  per-predicate `failureMode` of
  `None`/`ReturnNothing`/`Error`/`ReturnWithError` (§4.7). It never gives you
  the error string, and never says at what point in a frame the check runs.
  WoWUIBugs issue bodies are the best available proxy (§2.4) and are
  observations, not spec. Blizzard's own `error(...)` calls in
  `SecureHandlers.lua` and `RestrictedExecution.lua` are the exception — those
  strings are literal Tier 1 (§3.2).
- **[gap] `SecretArguments` on the secret-testing primitives is internally
  inconsistent** with Blizzard's own statement that addons should call
  `issecretvalue`. See §4.4. Unresolved.
- **[gap] `IsPreventingSecretValues()` is undocumented.** It exists at
  `SimpleFrameScriptObjectAPIDocumentation.lua:114`; nothing in the source, the
  docs, or the wiki says what sets the state.
- **[gap] `HasRestrictions = true` has no definition at Tier 1 or Tier 2.**
  236 entries carry it, including the classic protected/hardware-event C
  functions (`TargetUnit` at `TargetScriptDocumentation.lua:186`,
  `C_AuctionHouse.PlaceBid`, `C_BattleNet.SendWhisper`) and the two combat-log
  events. It is a *different* axis from `IsProtectedFunction` (59, widget
  methods) and from `SecretArguments`. Looked in
  `Blizzard_APIDocumentationGenerated/`, `Blizzard_APIDocumentation/`, the wiki
  `Secret Values` and `Secure Execution and Tainting` pages. Not found.
- **[gap] `IsProtected()`'s second return, `SetForbidden`/`IsForbidden`, and
  `ConstSecretAccessor` carry no Tier-1 `Documentation` string.** Only
  `ConstSecretAccessor` has a Tier-2 definition (`Secret Values`); the other two
  are marked `[unverified]` in §1.2 and §1.5.
- **[gap] Taint propagation through parents and anchors is Tier 2 only.** I
  found no Tier-1 statement of the rule, only Blizzard code that relies on it.
- **[gap] `issecure`, `issecurevariable`, `securecall`, `securecallfunction`,
  `secureexecuterange`, `forceinsecure`, `hooksecurefunc`, `CreateFrame` are
  absent from the generated docs.** `issecurevariable` appears **nowhere in the
  shipped source either** — the wiki (2026-01-03) is the only source for its
  signature and semantics.
- **[gap] `taintLog` level 5 unverified.** The wiki says 12.0.1 added it; the
  BlizzardInterfaceResources dump (build 68256) does not mention it. No
  `taint.log` exists on this install to check against. **@verify-ingame**
- **[gap] Nothing here has been executed in the client.** Every claim is
  static-source or documentary. Anything phrased as runtime behaviour —
  especially the operation table in §4.2 and the aspect-marking claims in §4.6 —
  should be confirmed in game before being relied on. **@verify-ingame**
- **Build skew.** `wow-ui-source` 12.0.7.**68887** vs
  `BlizzardInterfaceResources` 12.0.7.**68256** vs the wiki's API index stamped
  **12.1.0 (68301)**. On conflict the local checkout wins; where I used the
  other two I said so.

---

## 7. Rules we could audit against

Each is checkable against real code by grep or by reading a call site. Tier in
brackets is the evidence the rule rests on.

**Protection and lockdown**

1. Calling any of the 59 `IsProtectedFunction = true` widget methods on a frame
   that is protected, from addon code, while `InCombatLockdown()` is true, is a
   blocked action. The 59 are enumerated in §1.1.
   ⚠ This rule is **necessary, not sufficient** — passing it does not mean the
   code is combat-safe. `IsProtectedFunction` is the *generated-widget-doc*
   marker only; restricted global/C APIs (`TargetUnit`, and everything else
   carrying `HasRestrictions = true`, 236 entries) are governed separately and
   are **not** on the 59-entry list. See the `[gap]` in §1.1.
   [Tier 1: `IsProtectedFunction = true` × 59 in
   `Blizzard_APIDocumentationGenerated/`; list at `Simple*APIDocumentation.lua`
   lines given in §1.1]
2. A frame used as a secure-handler *header* must be **explicitly** protected;
   `select(2, frame:IsProtected())` must be true, or `SecureHandlerWrapScript`
   raises `"Header frame must be explicitly protected"`.
   [Tier 1: `SecureHandlers.lua:625` (in `SecureHandlerWrapScript`), `:690`
   (in `SecureHandlerExecute`), `:497` (in the attribute-driven `_wrap` path)]
3. No call into the `SecureHandlers` API (`Execute`, `WrapScript`,
   `UnwrapScript`, `SetFrameRef`) may occur while `InCombatLockdown()` is true;
   it raises `"Cannot use SecureHandlers API during combat"`.
   [Tier 1: `SecureHandlers.lua:435-439`]
4. Code that sets up secure state must complete before
   `ADDON_RESTRICTION_STATE_CHANGED` reports `Active` for the relevant
   `Enum.AddOnRestrictionType`; during dispatch of that event
   `IsAddOnRestrictionActive` returns false and must not be used as the gate.
   [Tier 1: `RestrictedActionsDocumentation.lua:58, 96-107`]
5. An addon that wants a combat-blocked-action diagnostic registers
   `ADDON_ACTION_BLOCKED` / `ADDON_ACTION_FORBIDDEN`, whose payload is
   `(isTainted: string, function: string)` — two arguments, both strings.
   [Tier 1: `RestrictedActionsDocumentation.lua:75-95`]

5b. Setup that must beat a restriction is done no later than the
    `ADDON_RESTRICTION_STATE_CHANGED` handler that reports
    `Enum.AddOnRestrictionState.Activating` for that type. After that dispatch
    completes the restriction is enforced.
    [Tier 1: `RestrictedActionsConstantsDocumentation.lua:14` —
    *"…won't be enforced until event dispatch has completed"*]

**Secure snippets**

6. A secure-handler snippet body containing the substring `function`, or either
   of `{` `}`, is rejected at build time — `BuildRestrictedClosure` returns nil
   plus `"The function keyword is not permitted"` / `"Direct table creation is
   not permitted"`. The check is a plain `string.match`, so it also rejects
   those substrings inside comments and string literals.
   [Tier 1: `RestrictedExecution.lua:58-66`]
7. A snippet may only call names present in `RESTRICTED_FUNCTIONS_SCOPE` or
   `DIRECT_MACRO_CONDITIONAL_NAMES`; `table` is not among them.
   [Tier 1: `RestrictedEnvironment.lua:24-77` (note :27) and :81+]
8. `RegisterAttributeDriver` silently no-ops on any attribute name whose first
   character is `_`.
   [Tier 1: `SecureStateDriver.lua:9`]
9. State drivers resolve on a polling timer (default 0.2 s), not synchronously on
   the registered events — code that assumes a state change is visible in the
   same frame as the event is wrong. Do not hardcode 0.2 as invariant: the
   throttle is overwritable via the manager's `updatetime` attribute.
   [Tier 1: `SecureStateDriver.lua:63, 119-122, 143, 173-174, 185-196`]

**Taint**

10. Any hook onto a Blizzard function that may reach protected code uses
    `hooksecurefunc` or `frame:HookScript`, never `SetScript` over the original
    and never assignment to the global.
    [Tier 2: `API hooksecurefunc`, revid 6588971, 2026-01-03]
11. No call to `hooksecurefunc` targets any of the 24 functions annotated
    `SecureHooksAllowed = false` (§2.2), nor any of the 23 names the wiki lists
    as unhookable since 11.0.0. Violation raises `"Cannot hook function"`.
    [Tier 1 for the 24: `FrameScriptDocumentation.lua` lines in §2.2 and
    `RestrictedActionsDocumentation.lua:11`. Tier 2 for the 23:
    `API hooksecurefunc`, revid 6588971]
12. Addon → Blizzard-secure-code communication goes through
    `SetAttribute`/`GetAttribute`, not through shared tables or direct calls.
    [Tier 1 as Blizzard's own stated practice:
    `Blizzard_StoreUI/Blizzard_Shared_StoreUIInbound.lua:4`;
    `Blizzard_WowTokenUI/Blizzard_WowTokenUIInbound.lua:4`;
    `Blizzard_CatalogShop/Blizzard_CatalogShop.lua:525`]
12b. `hooksecurefunc` is called once per target per session, from load-time
    code — never from a settings-change or enable/disable path. Hooks cannot be
    removed short of `/reload` and repeated calls stack.
    [Tier 2: `API hooksecurefunc`, revid 6588971, 2026-01-03 —
    *"You cannot 'unhook' a function … Calling hooksecurefunc() multiple times
    only adds more hooks to be called."*]
12c. A function that has been `hooksecurefunc`'d is never subsequently passed to
    `setfenv`, and a hook is never installed on a name after an XML
    `function="…"` attribute has already bound it (the binding captured the old
    reference and your hook will not fire).
    [Tier 2: `API hooksecurefunc`, revid 6588971, 2026-01-03]

**Secret values**

13. A guard on a possibly-secret value uses `issecretvalue`, `canaccessvalue`,
    `issecrettable`, `canaccesstable` or `hasanysecretvalues` — **never
    `type(v) == "<t>"`**, which returns the true type of a secret and therefore
    passes.
    [Tier 2 for the `type()` behaviour: `Secret Values`, revid 6777907,
    2026-07-22. Tier 1 for Blizzard writing code that way:
    `Blizzard_SharedXML/Dump.lua:98/106/113`, `:149/151`, `:309/312/315`,
    `:406/407`]
14. No arithmetic, comparison, `#`, indexing, indexed assignment, function call,
    or table-key use is performed on a value that has not been proved
    non-secret on that path.
    [Tier 2: `Secret Values`, revid 6777907. Observed failures:
    WoWUIBugs #801 (arithmetic), #804 (comparison)]
15. A boolean test (`if v then`) on a value that may be a **boolean** secret is
    a violation; the same test on a non-boolean secret is legal. Code relying on
    truthiness must first establish the value is not a boolean.
    [Tier 2: `Secret Values`, revid 6777907]
16. Any secret handed to a C API is handed only to one of the **120** functions
    annotated `SecretArguments = "AllowedWhenTainted"` (§4.5). The 3473
    `"AllowedWhenUntainted"` entries do **not** qualify from addon code, and the
    84 `"NotAllowed"` entries never qualify.
    [Tier 1 for the annotations and counts:
    `grep -rh 'SecretArguments = ' Blizzard_APIDocumentationGenerated/ | sed 's/.*= //' | sort | uniq -c`
    → 120 / 3473 / 84. Tier 2 for what the three values mean:
    `Secret Values`, revid 6777907]
17. Cooldown display driven by possibly-secret timing uses
    `C_Spell.GetSpellCooldownDuration` → `Cooldown:SetCooldownFromDurationObject`,
    not `C_Spell.GetSpellCooldown` → `Cooldown:SetCooldown`. The former returns
    a `LuaDurationObject` and carries no secret predicate; the latter is
    `SecretWhenCooldownsRestricted` and `SetCooldown` is only
    `AllowedWhenUntainted`. Note the sink is *also* `AllowedWhenUntainted` —
    what makes the route legal is that a duration object is not a secret value,
    not that the setter is on the `AllowedWhenTainted` list.
    [Tier 1: `SpellDocumentation.lua:249, 267`;
    `FrameAPICooldownDocumentation.lua:280-283, 305-313`]
18. Percentage/colour derivation from a secret unit stat goes through a curve
    (`C_CurveUtil.CreateCurve` / `CreateColorCurve`, passed to e.g.
    `UnitHealthPercent(unit, usePredicted, curve)`) rather than through Lua
    arithmetic.
    [Tier 1: `CurveUtilDocumentation.lua:3-30`; `UnitDocumentation.lua:1426-1443`]
19. Code must not assume a getter returns a plain value after the matching
    setter was fed a secret. If a setter carries `SecretArgumentsAddAspect`
    (52 setters), every getter carrying the same `SecretReturnsForAspect`
    (82 getters) returns a secret thereafter. The **addon-reachable** example is
    `FontString:SetText` (`AllowedWhenTainted`) → `GetText` via
    `Enum.SecretAspect.Text`. The `SetShown` → `IsShown`/`IsVisible` pairing via
    `Enum.SecretAspect.Shown` is real in the docs but an addon cannot trigger it:
    `SetShown` is `AllowedWhenUntainted` *and* `IsProtectedFunction = true`. Audit
    for the getter side regardless — Blizzard code can set the aspect on a frame
    you then read.
    [Tier 1: `SimpleFontStringAPIDocumentation.lua:653-656, 352`;
    `SimpleFrameAPIDocumentation.lua:1354-1358, 841, 895`]
20. Code must not assume `GetPoint`/`GetLeft`/`GetWidth` are readable on a
    frame anchored (directly or transitively) to a frame marked
    `HasSecretValues()`. Test with `ScriptRegion:IsAnchoringSecret()`.
    [Tier 1 for the APIs: `SimpleScriptRegionAPIDocumentation.lua:367`;
    `SimpleFrameScriptObjectAPIDocumentation.lua:69`. Tier 2 for downward
    propagation: `Secret Values`, revid 6777907, and the 2025-10-01 blue post]
21. Aspect/secret state on a widget is cleared only by
    `FrameScriptObject:SetToDefaults()`, which is itself
    `IsProtectedFunction = true` — so on a **protected** frame it cannot be
    called from addon code in combat. On an ordinary unprotected addon frame it
    is callable; an earlier draft over-generalised this to "any design that needs
    mid-combat clearing is unimplementable", which does not follow. Separately,
    Tier 2 notes that *clearing anchor points* can reset the
    anchoring-secret state (a different lever from `SetToDefaults`).
    [Tier 1: `SimpleFrameScriptObjectAPIDocumentation.lua:136`. Tier 2 for
    "only `SetToDefaults` clears aspects" and for the anchor-clearing reset:
    `Secret Values`, revid 6777907]
22. No secret is ever passed to `C_ChatInfo.SendAddonMessage` or
    `SendAddonMessageLogged`; both are `SecretArguments = "NotAllowed"`.
    [Tier 1: `ChatInfoDocumentation.lua:516, 535`]
23. No addon registers `COMBAT_LOG_EVENT` or `COMBAT_LOG_EVENT_UNFILTERED`.
    [Tier 1 for the restriction marker: `CombatLogDocumentation.lua:122, 130`
    (`HasRestrictions = true`). Tier 2 for "registering errors":
    `Patch 12.0.0/API changes`, revid 6747189, 2026-06-18]
24. A secret is never released into an object pool. Blizzard's own pool asserts
    against it because one secret object makes every later acquisition secret.
    [Tier 1: `Blizzard_SharedXMLBase/Pools.lua:265-277`]
25. Handling of the 18 unconditionally-secret functions (§4.7, `UnitHealth` et
    al.) never compares, does arithmetic on, or indexes their return value; only
    the Curve/Duration/widget sinks consume it. `SecretReturns = true` carries no
    predicate, so there is no restriction state in which `UnitHealth` returns a
    readable number to tainted code. (A bare truthiness test `if UnitHealth(u)
    then` is technically legal per rule 15 because the return is numeric, not
    boolean — but it tells you nothing useful, so treat it as a smell rather than
    a violation.)
    [Tier 1: `SecretReturns = true` × 18, e.g. `UnitDocumentation.lua:1446`.
    Tier 2 for the boolean-test exception: `Secret Values`, revid 6777907]
25b. A FontString that has been given a secret string via `SetText` is never
    afterwards measured with `CalculateScreenAreaFromCharacterSpan` or
    `FindCharacterIndexAtCoordinate` by tainted code — those two carry
    `RequiresFontStringTextAccess` with `failureMode = ReturnNothing`, so they
    return nothing (not an error) once the `Text` aspect is set. Layout code
    that divides by the returned width will then fail on nil.
    [Tier 1: `SecretPredicatesDocumentation.lua:21`;
    `SimpleFontStringAPIDocumentation.lua:10, 73`]
25c. Code distinguishes the two predicate kinds: a `Type = "Secret"` predicate
    (19 of them, all `failureMode = None`) changes the *value* returned; a
    `Type = "Precondition"` predicate (32, of which 20 `ReturnNothing`,
    5 `Error`, 5 `ReturnWithError`, 2 `None`) changes whether the *call*
    succeeds. Guarding a Precondition-annotated API with `issecretvalue` on its
    return is the wrong guard — it may have returned nothing at all.
    [Tier 1: `uv run python -m wowkb.uiapi predicates` over
    `Blizzard_APIDocumentationGenerated/` at 12.0.7.68887 — 51 predicates,
    counts as given]
26. Error-reporting code that formats a message for display first checks
    `canaccessvalue(message)` — as of 12.0.7 `debugstack` and `debuglocals`
    themselves return secrets once anything up the stack has touched one.
    [Tier 1 for the pattern: `Blizzard_ScriptErrors/Blizzard_ScriptErrors.lua:75-83`.
    Tier 2 (blue-post archive) for the 12.0.7 change:
    `Patch 12.0.7/API changes`, revid 6778033, 2026-07-22]
