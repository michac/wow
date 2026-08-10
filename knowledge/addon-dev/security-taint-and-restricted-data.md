---
title: Security — protected actions, taint, and restricted data (secret values)
patch: 12.0.7
fetched: 2026-08-05
reviewed: 2026-08-07
sources:
  - https://github.com/Gethe/wow-ui-source (live, 12.0.7.68887, commit 4383ced30106)
  - IN-CLIENT MEASUREMENT 2026-08-07 — ClientLab v0.2.2 `curve-step-and-clamp-semantics`
    and `duration-curve-result-secret`, Demonology Warlock.  §4.8.1 finding 4 — Step is a
    previous-point floor, both curve types clamp outside their range, and every Evaluate*
    result is secret even with a non-secret curve.
  - IN-CLIENT MEASUREMENT 2026-08-06 — ClientLab v0.2.2
    `duration-predicate-secret-in-combat`, Demonology Warlock, 5 in-combat runs.
    §4.8.4 — the four duration predicates are SECRET BOOLEANS, the first boolean-typed
    secrets this workspace has obtained, which is what gives §4.2 row 8 a source.
  - IN-CLIENT MEASUREMENT 2026-08-04 — CDMProbe `/cdmp curve` (CurveLab.lua v0.32.98),
    Havoc Demon Hunter, 12.0.7 live. §4.8.1 is the only RUN evidence in this file.
  - IN-CLIENT MEASUREMENT 2026-08-04 — CDMProbe `/cdmp curve text` (CurveLab.lua
    v0.32.117), Demonology Warlock, 12.0.7 live. §4.8.1 finding 2 — a SECRET cooldown
    remaining rendered as ticking text IN COMBAT via FormatRemainingDuration + SetText.
  - EllesmereUI v8.7.5 @ c4eba58d996a8436f467ac8f297148bff9dd3008 (2026-08-04),
    https://github.com/EllesmereGaming/EllesmereUI — license CUSTOM, ALL RIGHTS
    RESERVED; read for API discovery only, no code copied. Mined via the
    `mine-addon` skill; clone deleted after (step 5). file:line citations resolve
    only against that commit. Unverified residue:
    `addon-dev/mined-pending-verification.md`.
  - EllesmereUICooldownManager (installed addon, read for API discovery only, no code
    copied) — `EllesmereUICdmBuffBars.lua:4499-4517`, the working SetMinMaxValues(0,1)
    -> SetTimerDuration ordering behind §4.8.1 finding 3.
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
(Tier 2: `Secret Values`, revid 6777907, 2026-07-22 — *"When execution is not
tainted secret values are effectively equivalent to regular values, and no
operations on them are blocked."*). A protected function can be blocked with no secrets anywhere
in sight. Diagnose them separately.

Blizzard's own stated goal for the 12.0 layer, verbatim from the addon-dev blue
post archived on the wiki:

> The overall goal of these API changes is to limit addons' ability to perform
> complex logic based off combat information, and thus optimally solve problems
> that would otherwise require player thought and coordination. But a secondary
> goal (almost as important) is to still allow addons to customize the look and
> feel of the UI (including combat-related UIs).
>
> — *Midnight Public Alpha Addon API Changes* (WoWUIDev Discord). Tier-1 content
> read through its Tier-2 archive, which quotes
> the post of 2025-10-01 at `Patch 12.0.0/Planned API changes`, revid 6746061, 2026-06-17. The Discord
> permalink `discord.com/channels/327414731654692866/1422999311410790541` is
> **not independently verifiable, see §6**

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
change input handling. On an ordinary addon frame these methods are **not**
restricted, and the §1.2 propagation does not reach one by the routes an addon
actually uses. Measured `[client 2026-08-06]`: a plain
`CreateFrame("Frame", nil, UIParent)` anchored to UIParent reads
`IsProtected() == false, false` — even though **UIParent itself reads
`true, true`** — and re-anchoring that same frame to `ActionButton1`
(`true, true`) left it `false, false`. In combat, `SetPoint`, `SetScale`, `Show`
and `Hide` all succeeded on it. So the spread runs **outward from the protected
frame** — to *its* parents and to the frames *it* is anchored to — and not
inward to whatever chooses to parent or anchor itself onto one. Parenting an
addon frame to UIParent, which is the ordinary case, costs nothing.

> `[gap]` **The in-combat half of that measurement covered 4 of the 59, not all of
> them.** `SetPoint`, `SetScale`, `Show` and `Hide` were exercised on the addon frame
> in combat; the other 55 were not, and the general claim above is an inference from
> the four plus the `IsProtected() == false` reading. Two of the unmeasured entries are
> ones addons reach for constantly and are worth naming: **`SetFrameStrata`**, which is
> additionally the **only `SecretArguments = NotAllowed`** member of the strata/level
> family (§4.2 of `frames-textures-animation.md`), and **`SetHeight` / `SetWidth`**,
> the resizing siblings of the `SetPoint` that *was* measured. Code that must not
> guess should do its strata and its geometry out of combat and keep the in-combat
> path to the four. `@verify-ingame`

> `[gap]` **A dependent of a frame carrying a SECRET anchor is a different question from a
> dependent of a PROTECTED frame, and only the protected half is measured.** The run above
> anchored to `ActionButton1`, which is never fed a secret. §4.8.1 findings 10 and 12
> record anchor-chain contagion propagating **down to the dependent** from
> `FontString:SetText` and `Texture:SetColorTexture`, and the Cooldown Manager writes
> secret cooldown text onto its own item frames in combat — so an addon frame anchored to
> a CDM item frame can inherit a secret anchor by a route the measurement never touched.
> **Whether such a dependent still accepts `SetPoint` / `Show` / `Hide` is unmeasured.**
> This is a source-read inference from the two findings, not a run: nothing was executed
> in the client for it. An overlay anchored to a CDM item frame should treat a frame that
> silently fails to move as this possibility rather than as its own bug. `@verify-ingame`

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
The second flag distinguishes "protected because a template said so" from
"protected by contagion" (parent / anchor), and **only the explicit half is
measured**: two template-declared protected frames — UIParent and
`ActionButton1` — both read `true, true`, and an ordinary addon frame reads
`false, false` `[client 2026-08-06]`. **[gap]** No `true, false` frame, one
protected *only* by contagion, was produced, so that half of the reading remains
inference: the generated docs carry **no** `Documentation` string for either
return, and neither wiki page defines the pair.
What *is* Tier 1 is that Blizzard's own secure-handler API
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
`Documentation` string. ⚠ **"Forbidden" is not the same as "hidden from the
global environment"** — the wiki's own text for `MouseFocusValidForLimitedInput`
lists *"forbidden, hidden from the global environment, fully locked down, script
inaccessible, or protected frames"* as **five separate** conditions, so any gloss
that equates two of them is wrong. What is Tier 1 is the *behaviour*: Blizzard's secure-handler API refuses
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
either") — **yet it exists: it resolves to a `function` in the client**
`[client 2026-07-24]`. So the name is live, and only its *semantics* are Tier 2.
The wiki is the only source for those: `API issecurevariable`,
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
A *second, differently worded* comment states the reason from the other side:
*"Setting attributes is how the external UI should communicate with this frame.
That way their taint won't be spread to this code."*
(`Blizzard_CatalogShop/Blizzard_CatalogShop.lua:525`,
`Blizzard_WowTokenUI/Blizzard_WowTokenUI.lua:287`). The two comments are distinct
strings, not one comment at eight sites.

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

   Enable with `/console taintLog 1` and restart. `@verify-ingame` — level 5's
   behaviour is unconfirmed; there is no `taint.log` in `_retail_/Logs/` on this
   install, consistent with the default of `0`.

2. **Register `ADDON_ACTION_BLOCKED` / `ADDON_ACTION_FORBIDDEN`** and read the
   `isTainted` / `function` payload (§1.4).

3. **`issecurevariable(tbl, key)`** to name the tainting addon for a specific
   global or table field (Tier 2).

4. **`debugstack` / `debuglocals` are themselves secret-contaminated as of
   12.0.7**: *"debugstack and debuglocals will now return secret values if the
   current function — or any caller up the stack — has accessed a secret
   value."* (Tier-2 archive of the Blizzard blue post of
   2026-04-30: `Patch 12.0.7/API changes`, revid 6778033, 2026-07-22). Blizzard's own error
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

(Labels and states are read with `gh api repos/Stanzilla/WoWUIBugs/issues/<n>`;
re-run it before relying on any of them.)

A `taint` search of the tracker returns ~86 issues and a `secret value` search
13 (counts recorded in `sources.md` §2.2).

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
defines **ten** templates (ten `<Frame>`/`<Button>` elements, at :6, :13, :21,
:29, :37, :45, :56, :67, :78, :90), each binding a widget script to a named
attribute whose value is a **string of restricted Lua**:

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

The environment handed to snippets is an explicit allow-list, and it is
**assembled from two files** — reading only the first gives the wrong answer
about what a snippet can do.

1. `RESTRICTED_FUNCTIONS_SCOPE` at `RestrictedEnvironment.lua:24-77`: `math`,
   `string`, `select`, `tonumber`, `tostring`, `rawtype`, the `str*` family, and
   the `math` scalar functions. Its comment *"table is provided elsewhere, as
   direct tables are not allowed"* (:27) names the second file rather than
   excluding `table`.
2. `RestrictedExecution.lua` then merges that scope into
   `LOCAL_Restricted_Global_Functions` (`:276-294`, merge at `:317-321`) and adds
   a **`table` namespace** (`:323-333`) with `maxn`, `insert`, `remove`, `sort`,
   `concat`, `wipe` and **`new`**, plus at top level `newtable`, `copytable`,
   `pairs`, `ipairs`, `next`, `unpack`, `wipe`, `tinsert`, `tremove`, a
   restricted-table-aware `type`, and `rtgsub` (`:276-294`). Every one of these
   is an `rtable.*` function — the restricted-table implementations exported at
   `RestrictedInfrastructure.lua:563-580`, not stock Lua `table`. Namespaces are
   copied in through `PopulateGlobalFunctions` (`:297-315`, called at `:319` and
   `:335`), which re-exposes each sub-table behind a `newproxy` with
   `__index`/`__metatable = false`, so a snippet may call through `table.*` but
   may not write to it.

**So snippet-local storage is entirely possible.** `BuildRestrictedClosure`
rejects the `{}` constructor at build time (`:63-66`), and
**`newtable()` / `table.new()` is the sanctioned substitute** — that is exactly
what "table is provided elsewhere, as direct tables are not allowed" means. What
you get back is a *restricted* table (`RestrictedTable_create`,
`RestrictedInfrastructure.lua:282`, exported as `rtable.newtable` at `:568`), so
iterate it with the injected `pairs`/`next`/`ipairs`/`unpack` — those are the
only ones in scope, and they are the restricted-table-aware implementations.

Game state is exposed only at macro-conditional granularity via
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

oUF is the smallest complete real user of this machinery (504 K of code; the
784 K figure elsewhere in the corpus is the clone including `.git`). It builds
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
> — Blizzard, *Midnight Public Alpha Addon API Changes*; Tier-2 archive of the
> post of 2025-10-01: `Patch 12.0.0/Planned API changes`, revid 6746061, 2026-06-17

Secrecy is a property of the **value**, and the restriction is a property of the
**path**. Untainted code operates on secrets normally.

### 4.2 The operation table

Originally from Tier 2 (`Secret Values`, revid 6777907, 2026-07-22), the only
consolidated statement of the rules. **Every row below has now been executed in the
client against a genuine Secret Value** — a tracked cooldown read in combat — so this
table is Tier 1 by measurement `[client 2026-08-05]`. **When a disallowed operation
happens the result is an immediate Lua error**, not a nil return.

The **result column is the half the wiki does not state**, and it is where the surprises
are: an allowed operation does not necessarily give back a plain value.

| Operation on a secret, from tainted code | Allowed? | Is the RESULT secret? |
|---|---|---|
| Store in a local / upvalue / table **value** | ✅ | n/a — the stored value stays secret |
| Pass to a **Lua** function | ✅ | **yes** — it comes back out secret |
| Pass to a **C** function | ❌ unless explicitly marked (§4.5) | — |
| Concatenate, if string or number | ✅ | **yes** |
| `string.format` / `string.join` / `string.concat` | ✅ | **yes** |
| Arithmetic | ❌ | — |
| Compare (`==`, `<`, …) | ❌ **except against `nil`** — see below | — |
| Boolean test on a **boolean** secret | ❌ *(unverified — see below)* | — |
| Boolean test on a **non-boolean** secret | ✅ | **no** — a plain boolean |
| Length operator `#` | ❌ | — |
| Use as a table **key** | ❌ | — |
| Index or index-assign (`secret.foo`, `secret["foo"] = 1`) | ❌ both directions | — |
| Call it as a function | ❌ | — |
| `type(secret)` | ✅ — **returns the real type** | **no** — a plain string |

⚠ **`string.format` and `..` return a SECRET string.** That is the row most likely to be
misread as an escape hatch: formatting a secret is permitted, so it looks like a way to
get text out — but the text is itself secret and printing it is the next error. The two
operations that hand back a genuinely plain value are `type()` and a truthiness test on a
non-boolean.

⚠ **The boolean-secret row is the one thing here still NOT measured — but it is no longer
unanswerable.** It was open because no boolean-valued secret was known to exist: every
secret this client had handed an addon was a cooldown *number*, and the test recorded
`measured = false` with that reason rather than a verdict `[client 2026-08-05]`. **A source
now exists** — `LuaDurationObject:HasExpired()` / `IsActive()` / `HasStarted()` / `IsZero()`
all return secret **booleans** in combat (§4.8.4) `[client 2026-08-06]`. The ❌ is still
Tier 2 alone until the operation itself is executed against one.
`` @pending-test: secret-op-bool-test-boolean ``

**`== nil` is permitted, and it is the one comparison that is.** Measured all four ways
`[client 2026-08-05]`: `s == nil` → `false`, `nil == s` → `false`, `s ~= nil` → `true`,
all plain booleans and none erroring — while the control `s == 0` threw
*"attempt to compare upvalue 'v' (a secret number value, while execution tainted by
'ClientLab')"*. So a nil-guard on a maybe-secret value is safe, which is consistent with
the model: comparing against nil leaks nothing that holding the value did not already.
⚠ **This does not license comparing to nil in product code.** The house rule stands —
class-check first (`issecretvalue`), branch on the class. This row exists so the table is
honest, not to change the practice.

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
`canaccessvalue(val)`. Exact lines in `Blizzard_SharedXML/Dump.lua`:
`type(val)` :98 → `canaccessvalue(val)` :106, :113 (in `prepSimple`);
`type(val)` :149 → `canaccessvalue(val)` :151;
`type(val)` :309 → `issecretvalue(val)` :312 → `canaccessvalue`/`canaccesstable`
:315 (in `DevTools_DumpValue`);
`type(value)` :406 → `canaccesstable(value)` :407.
The correct guard is `issecretvalue(v)` or `canaccessvalue(v)`, never `type()`.

**Trap 2 — truthiness is type-dependent.** `if secretNumber then` is legal and returns a
plain boolean `[client 2026-08-05]`; `if secretBoolean then` errors. You cannot tell which
you have without asking. **Only the first half is measured**: the boolean case has never
been executed and rests on Tier 2 alone, as the operation table above records. ⚠ The
*existence* of secret booleans is no longer in doubt — §4.8.4's four duration predicates
are ones `[client 2026-08-06]` — so "in practice every secret is a number" is a reading
that has now been falsified, and code that boolean-tests a secret without a class check is
exposed rather than merely theoretically wrong.

**Trap 2b — a formatted secret is still secret.** `string.format("%s", s)` and `"x" .. s`
are both permitted, which reads like a way to get text out. The result is a **secret
string** `[client 2026-08-05]`, so the print is the next error. The only operations that
hand back a genuinely plain value are `type()` and a truthiness test on a non-boolean.

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
`Blizzard_APIDocumentationGenerated/FrameScriptDocumentation.lua`. The secret
family is Tier 1, unlike
`issecure`/`issecurevariable`/`securecall`/`forceinsecure`, which are wiki-only
for their *semantics* — though all four are now confirmed to **exist** as
functions in the client `[client 2026-07-24]`:

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
carry `SecretArguments = "AllowedWhenUntainted"` in the same file. The ninth,
`canaccesssecrets`, takes **no arguments at all** and therefore carries no
`SecretArguments` field; `dropsecretaccess` is likewise argument-less and
unannotated. Read literally against the wiki's definition of that value (§4.5), a *tainted*
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
`GetCooldownAuraBySpellID`:299, `GetAuraBaseDuration`:133,
`GetRefreshExtendedDuration`:349 — `UnitAuraDocumentation.lua`), `UnitName`:2368, `UnitNameFromGUID`:2385,
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
code cannot pass a secret number to any of the four.** The absence of
`NotAllowed` does **not** mean "they accept secrets" — that reading drops the
untainted/tainted distinction. The sanctioned path for secret cooldown data is
instead §4.8.

⚠ **`AllowedWhenTainted` governs the *arguments*; a `Precondition` can still
refuse the *call*.** Two of the `C_UnitAuras` entries above carry
`RequiresNonSecretAura = true` on top of `AllowedWhenTainted`:
`GetPlayerAuraBySpellID` (`UnitAuraDocumentation.lua:332`, marker at `:335`) and
`GetUnitAuraBySpellID` (`:369`, marker at `:372`). So being on the 120-member
list is necessary and not sufficient — see §4.7 for what that predicate does.
`GetCooldownAuraBySpellID`, `GetAuraBaseDuration` and `GetRefreshExtendedDuration`
do **not** carry it.

### 4.6 Aspects, anchors, and const accessors

Passing a secret into a widget setter *marks the object*. There are three
outcomes, and **they are not mutually exclusive** — read them as three things
that can happen, not as a three-way choice. One setter can do two of them
(`SetText` does (a) and (b) together; see the worked example below).

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

**Worked example — `FontString:SetText`, which does (a) and (b) at once.** It is
the aspect case an addon can actually trigger: it adds `Text`
(`SimpleFontStringAPIDocumentation.lua:653-656`) and is
`SecretArguments = "AllowedWhenTainted"`, so tainted addon code *can* feed it a
secret, after which `FontString:GetText` returns secret for `Text` (`:352`).
⚠ **It also marks anchoring secret** — measured, the FontString *and its
dependent* flip to `IsAnchoringSecret`, which is outcome (b), not (a)
(§4.8.1 finding 10, `[client 2026-08-04]`). Mechanically that follows: a
FontString's extent is derived from its text, so a secret string implies a
secret size.

**The practical rule: a FontString you feed a secret must be a leaf.** Anchor it
*to* things; never anchor anything *to* it, and never read `GetPoint`/`GetWidth`
off its dependents. §4.8.1 records the anchor-safe alternative for secret text.

⚠ `Frame:SetShown` also declares
`SecretArgumentsAddAspect = { Enum.SecretAspect.Shown }`
(`SimpleFrameAPIDocumentation.lua:1354-1358`), and `IsShown` **and** `IsVisible`
derive from `Shown` (`:841, :895`) — but `SetShown` is *both*
`SecretArguments = "AllowedWhenUntainted"` **and** `IsProtectedFunction = true`,
so an addon cannot set that aspect by passing a secret. If your `IsShown` starts
returning a secret, the aspect was applied by *untainted* (Blizzard) code, not by
you — which does happen, so guard the getter anyway (rule 19).

Aspects do not share state — an object with `Shown` set still returns clean
values from the `Alpha` getters.

Query with `FrameScriptObject:HasSecretAspect(aspect)` /
`HasAnySecretAspect()` (`SimpleFrameScriptObjectAPIDocumentation.lua:52, 38`).

An aspect can also **block a call outright**, not just secrete its return. The
`RequiresFontStringTextAccess` precondition — *"Guarded APIs reject access for
tainted callers if the object has the secret Text aspect assigned"*,
`FailureMode = "ReturnNothing"` (`SecretPredicatesDocumentation.lua:21-24`) — is
applied to exactly two APIs, both text-measurement:
`FontString:CalculateScreenAreaFromCharacterSpan`
(`SimpleFontStringAPIDocumentation.lua:10`, marker at `:12`) and
`FontString:FindCharacterIndexAtCoordinate` (`:72`, marker at `:75`). So a
FontString that has ever been fed a secret string stops being measurable by
tainted code — a second, independent reason it has to be a layout leaf.

**(b) Whole-object secrecy.** The object is marked as having secret values —
`HasSecretValues()` (`SimpleFrameScriptObjectAPIDocumentation.lua:69`) — and
that in turn marks all anchoring/positioning data secret, propagating **down**
the anchor chain to dependents but not up.
`ScriptRegion:IsAnchoringSecret()` (`SimpleScriptRegionAPIDocumentation.lua:367`)
tests it; `IsAnchoringRestricted()` (`:353`) is the neighbouring query.
A setter with **no** declared aspect can only do this — but declaring an aspect
does not exempt a setter from it, which is why `SetText` does (a) and (b) both.
Down-only propagation is Tier 2 + blue post in the generated-docs sense, and
confirmed in client at §4.8.1 findings 4 and 6 (`[client 2026-08-04]`).

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

The two kinds behave differently, and the `FailureMode` field proves it:

```
Type = "Secret"        19   FailureMode absent            (all 19)
Type = "Precondition"  32   FailureMode = "ReturnNothing"  20
                            FailureMode = "Error"           5
                            FailureMode = "ReturnWithError" 5
                            FailureMode absent              2
```

A `Secret` predicate never changes *whether* the call succeeds — it changes
what the return **is**. A `Precondition` predicate changes whether you get a
value at all. Conflating the two is the difference between "guard the value"
and "guard the call".

⚠ **The two `Precondition`s with no `FailureMode` are the dangerous ones**,
because Tier 1 does not say what they do on failure:
`RestrictedForMacroChatMessages` (`ChatConstantsDocumentation.lua:233`) and
**`RequiresNonSecretAura`** (`UnitAuraDocumentation.lua:560`). Neither carries a
`Documentation` string either. **[gap]**

**`RequiresNonSecretAura` — the per-aura allowlist.** It is applied to exactly
three `C_UnitAuras` getters, all keyed by spell identity rather than by aura
index or instance ID: `GetAuraDataBySpellName` (`UnitAuraDocumentation.lua:205`,
marker at `:208`), `GetPlayerAuraBySpellID` (`:332`, marker at `:335`) and
`GetUnitAuraBySpellID` (`:369`, marker at `:372`). All three also carry
`SecretWhenUnitAuraRestricted`, and two of the three (`GetPlayerAuraBySpellID`,
`GetUnitAuraBySpellID`) are `AllowedWhenTainted` (§4.5). The consequence is that
*aura secrecy under restriction is not a blanket seal*: a spell the client flags
non-secret still answers through these three. Being a `Precondition`, a spell
that is **not** on the allowlist fails at the *call*, not at the value — so do
not guard these with `issecretvalue` on the return. ⚠ Because the failure mode
is undeclared, whether that failure is silent absence or an error is
**unverified here**: treat a `nil` return as "not on the allowlist" and do not
assume you will get an error. `@verify-ingame`

⚠ The allowlist membership is per-spell client data, not an API contract, so it
moves between builds. Anything built on one specific aura passing the predicate
is standing on a moving floor. [Tier 1 for the annotation.]

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

⚠ **`UnitInRange` being on that list does not mean range checking is lost.**
`C_Spell.IsSpellInRange(spellIdentifier, targetUnit)` carries **no secret
predicate at all** (`SpellDocumentation.lua:841-855`, only
`SecretArguments = "AllowedWhenTainted"`) and returns true / false / **nil**
(nil = the check was invalid — unknown spell, missing target).
`C_Item.IsItemInRange` is likewise unpredicated
(`ItemDocumentation.lua:1498-1511`). So a per-spec ladder of spell IDs is the
working range check under restriction. ⚠ Resolve each id through
`C_SpellBook.FindSpellOverrideByID` first, or a talent-replaced base id silently
answers `nil` and reads as "out of range". [Tier 1 for the predicates; the ladder
pattern seen working in EllesmereUI 8.7.5, read for API discovery only.]

Observed application counts at this build (`grep -rh '<predicate> = true' … | wc -l`):
`SecretInChatMessagingLockdown` 98 · **`SecretWhenUnitStatsRestricted` 50**
(the second-widest) · `SecretWhenUnitAuraRestricted` 20 ·
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

**Per-field markers — secrecy is not all-or-nothing per call.** The function-level
predicates above say *when the call goes secret*; a second, finer layer annotates
**individual return fields and table contents**, and it is what tells you which parts
of a restricted return you can still use. Counts at 12.0.7.68887
(`grep -rhoE '\b(NeverSecret|ConditionalSecret|SecretReturns|ReturnsNeverSecret) = true' … | sort | uniq -c`):

| Marker | Count | Level | Means |
|---|---|---|---|
| `NeverSecret = true` | **921** | return field | this field survives even when the call is restricted — **the most common secret-related annotation in the whole corpus** |
| `SecretReturns = true` | 18 | function | every return always secret |
| `ReturnsNeverSecret = true` | 15 | function | the inverse guarantee, e.g. `LuaDurationObject:HasSecretValues()` |
| `ConditionalSecret = true` | 15 | return field | this field *may* be secret depending on the ambient predicate |
| `NeverSecretContents = true` | 2 | table field | the table's **elements** are never secret |
| `ConditionalSecretContents = true` | 2 | table field | the table's **elements** may be secret |

Worked example — `UnitAuraUpdateInfo`, the `UNIT_AURA` payload
(`UnitConstantsDocumentation.lua:31-40`):

```lua
{ Name = "removedAuraInstanceIDs", Type = "table", InnerType = "number", NeverSecretContents = true },
{ Name = "addedAuras",             Type = "table", InnerType = "AuraData", ConditionalSecretContents = true },
{ Name = "updatedAuraInstanceIDs", Type = "table", InnerType = "number", NeverSecretContents = true },
```

That asymmetry is directly legible in Blizzard's own consumer. `CooldownViewerMixin:OnUnitAura`
(`Blizzard_CooldownViewer/CooldownViewer.lua:1629`) routes the **removed** and **updated**
paths through an `auraInstanceID → itemFrame` map (`:1517`) — a table lookup, which requires a
readable ID — while the **added** path broadcasts to *every* item frame and lets each one test
the aura itself (`:1661`, `NeedsAddedAuraUpdate` at `:424`). The generated docs say why: the
two ID lists are `NeverSecretContents`, the added-aura table is not. The same pair appears on
`C_UnitAuras.GetUnitAuras`' `auras` return (`UnitAuraDocumentation.lua:422`,
`ConditionalSecretContents`) — the call the CDM's per-frame aura scan makes.

**Reading rule:** to answer "is this value secret", check the function's predicate *and* the
field's own marker. A `SecretWhen…`-restricted function can still hand back perfectly usable
identity fields; 921 `NeverSecret` annotations exist precisely so that identity (spellIDs,
instance IDs, class filenames, texture IDs) keeps flowing while magnitudes and timings do not.

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

  ⚠ **`LuaCurveEvaluatedResult` is referenced as a return type NINE times and
  declared NOWHERE** `[T1 obs @ 12.0.7.68887]` — there is no `Structure` entry for
  it anywhere in the generated corpus. Its only definition is prose on
  `UnitHealthPercent` / `UnitPowerPercent`: *"If no curve is specified, a floating
  point percentage value. Else, the result of evaluating the curve with the
  percentage as the input."* So the type is **polymorphic in the curve's output**:
  a `LuaCurveObject` (`AddPoint(x: number, y: number)`) yields a number, a
  `LuaColorCurveObject` (`AddPoint(x: number, y: colorRGBA)`) yields a colour. Both
  derive from `LuaCurveObjectBase`, which is why every consumer types the argument
  to the base and accepts either. **Do not write a type check against this name** —
  there is nothing to check against.
- **Durations.** `C_DurationUtil.CreateDuration()` (`:11`),
  `CreateDurationTextBinding()` (`:21`), `CreateManualClock()` (`:31`) — all in
  `DurationUtilDocumentation.lua`. ⚠ Cite the getter, not `:3-9`, which is the
  system header, not the functions. A `LuaDurationObject`
  (`LuaDurationObjectAPIDocumentation.lua`) carries `SetTimeFromStart`,
  `SetTimeFromEnd`, `SetTimeSpan`, `GetRemainingDuration`, `HasExpired`,
  `IsActive`, `EvaluateRemainingPercent(curve, modifier)`
  (`SecretWhenCurveSecret`), `FormatRemainingDuration(formatter, modifier)`
  (`SecretWhenNumericFormatterSecret`), and — importantly —
  `HasSecretValues()` marked `ReturnsNeverSecret = true`, so you can always ask
  whether a duration is carrying secrets.
  Per-method verdicts: **§4.8.4**, which is the table to read before asking this
  object anything.
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

#### 4.8.1 Which channels actually carry a secret `[client 2026-08-04]`

⚠ **Measured, not read.** Everything in this subsection was run in the client. Unmarked
claims elsewhere in this file are source reads — see §0's evidence classes. Measured with `/cdmp curve` (CDMProbe
`CurveLab.lua`, v0.32.98) on a **Havoc Demon Hunter**, out of combat and in a
dummy pull, at 12.0.7. Sources: `UnitPowerPercent(player, Fury, false, curve)`,
`UnitHealthPercent`, `C_Spell.GetSpellCooldownDuration`,
`C_UnitAuras.GetAuraDuration`, `GetAuraDispelTypeColor`,
`GetAuraApplicationDisplayCount`. The readback is the **aspect**
(`HasSecretAspect`), not the value — the values are unreadable by construction.

**The model in §4.5–4.8 holds.** All four negative controls refused:
`curve:Evaluate(secret)` → *"Secret values are only allowed…"*, `curve:AddPoint(0,
secret)`, `C_CurveUtil.EvaluateGameCurve(id, secret)` and
`Cooldown:SetCooldown(secret, secret)` all raised. The `AllowedWhenUntainted`
reading in §4.5 is confirmed against the client.

**Curve and duration objects are `userdata`, not tables.** `C_CurveUtil.CreateCurve`
/ `CreateColorCurve` / `C_DurationUtil.CreateDuration` /
`CreateDurationTextBinding` / `CreateManualClock` all return userdata. A
capability probe written as `type(o) == "table" and type(o[name]) == "function"`
reports them **method-less**; probe with a pcall'd call instead.

| channel | setter | result |
|---|---|---|
| transparency | `SetAlpha` | ✅ **carries** — aspect `{Alpha}`; `GetEffectiveAlpha` then **throws** |
| colour | `SetVertexColor` | ✅ **carries** — aspect `{VertexColor, Alpha}` |
| brightness | `SetDesaturation` | ✅ **carries** — aspect `{Desaturation}`; `IsDesaturated` then **throws** |
| bar fill | `SetValue` / `SetMinMaxValues` | ✅ **carries** — aspect `{BarValue}` |
| bar colour | `SetStatusBarColor` | ✅ **carries** — but only with a bar texture, and the aspect lands on the **texture** |
| rotation | `Texture:SetRotation` | ✅ **carries** — aspect `{Rotation}` |
| **duration** | `SetCooldownFromDurationObject` · `StatusBar:SetTimerDuration` · `DurationTextBinding` | ✅ **carries, renders, and does NOT poison the anchor chain** `[client 2026-08-04]`. ⚠ Aspect-less — there is **no readback**, so "the call was accepted" is not evidence a pixel moved; the StatusBar route additionally needs `SetMinMaxValues(0,1)` **first** or it draws at 0 % width. Full recipe below. |
| text | `FontString:SetText` / `SetFormattedText` | ⚠ **carries AND poisons the anchor chain** — see below |
| ⚠ | `Texture:SetTexture` | ❌ **REFUSES** — *"Cannot set texture to a secret string value."* |
| ⚠ | `Texture:SetAtlas` | ⚪ accepted, nothing observable changed — **and not attributable to secrecy**, see below |
| ⚠ | `Texture:SetColorTexture` | ⚠ **POISONS the anchor chain** on every secret source |
| ⚠ | `AnimVertexColor:SetStartColor`/`SetEndColor` | ⚪ accepted, nothing observable changed |

**0. `SetAtlas` cannot be probed with the secrets we can obtain, and the attempt is
recorded so it is not repeated.** An atlas NAME is a string; the only secret string
reachable from a cooldown source is a concatenation (§4.2 row 4), which is **never a
valid atlas name**. Shown as three framed cells — a valid plain name, an invalid plain
name, and the secret string — a person reported the secret cell **indistinguishable from
the invalid one** `[client 2026-08-05]`. Both are blank, so "the secret was dropped" and
"a bad name renders nothing" produce identical pixels and the observation attributes
nothing to secrecy.

⚠ **Do not read that as "the channel is dead."** It means this *probe* is inconclusive.
Settling it needs a secret that is *itself* a valid atlas name, and no such source has
been identified — if none exists, `SetAtlas` is permanently unfalsifiable here and should
be documented as such rather than left looking untested. The sibling half of the same
question — `AnimVertexColor:SetStartColor`/`SetEndColor` — has **not been attempted at
all**; those take colours rather than names, so the category problem above does not apply
to them and they remain the live half.

**1. The duration route works, and it is the useful one.**
`C_Spell.GetSpellCooldownDuration(spellID, false)` returns a duration whose
`HasSecretValues()` is **true in combat and false out of it**, and all three sinks
consume it (`anchor 0>0` on subject and dependent — no contagion). **`C_UnitAuras.GetAuraDuration`
behaves identically**, which is a live in-combat *aura* timer. The `AuraData` record
being sealed in combat is a fact about **that record**; a duration object is a way round
it for display. ⚠ `C_Spell.GetSpellChargeDuration` returns
**nothing** for a spell with no charges (`MayReturnNothing`); that is not a refusal.

⚠⚠ **"Accepted" is not "displayed", and on an aspect-less sink nothing tells you which
you have.** The three duration sinks declare **no** `SecretArgumentsAddAspect`
(`SimpleStatusBarAPIDocumentation.lua:308-320`), so there is *no readback of any kind*.
`hsv` and `anchor 0>0` prove the object carried a secret and the chain stayed clean —
neither shows a pixel moving. A correctly installed duration (`GetTimerDuration` →
userdata, `IsZero` false) drawing at **0 % width** is fully consistent with that
evidence, and is what happens when the bar has no range (finding 3). **On any
aspect-less channel, the only oracle is an eyeball.**

**2. ✅✅ CONFIRMED IN COMBAT — the shortest route to a secret number on screen is
two calls, and it is TEXT, not a bar.** `[client 2026-08-04]` Demonology, Summon
Demonic Tyrant 265187 (`/cdmp curve text`):

```lua
local dur = C_Spell.GetSpellCooldownDuration(spellID, true)   -- ignoreGCD = true
local fmt = C_StringUtil.CreateSecondsFormatter()             -- StringUtilDocumentation.lua:29-37
local s   = dur:FormatRemainingDuration(fmt, Enum.DurationTimeModifier.RealTime)
fontString:SetText(s)                                          -- renders. In combat. Ticking.
```

`FormatRemainingDuration` returns a **`string`**
(`LuaDurationObjectAPIDocumentation.lua:144-158`) — not a curve result, not an
object — and it comes back **SECRET in combat**, which `SetText` then renders per
finding 10. **No curve, no StatusBar, no `DurationTextBinding`, no clock.** Both
halves were already in this file and were simply never used together.
⚠ **The constraint is finding 10's other half**: `SetText` with a secret also marks
**anchoring** secret, so the FontString must be a **leaf** — its own holder, and
nothing ever anchored to it. ⚠ `modifier` is `Nilable = false` *with* a `Default`
(`:154`) — pass it explicitly; see §4.6's `Default ≠ Nilable` rule.

**3. ⚠⚠ `StatusBar:SetTimerDuration` NEEDS A RANGE — `SetMinMaxValues(0, 1)` FIRST.**
A timer **drives the value within** a range; it does not bring one. With no range
the bar holds a valid duration object and draws **0 %**. This was misdiagnosed here
first: Blizzard calls `SetMinMaxValues(0, 0)` in
`EncounterTimelineTimerEvent.lua:76-82` under *"Ensure the timer bar doesn't keep a
reference to the timer object"*, which reads as "min/max releases the timer, never
call it". **The releasing part is the degenerate ZERO range, not the call** — `(0,0)`
is teardown, `(0,1)` is setup. Confirmed against a shipping implementation rather
than inferred from a teardown path: **EllesmereUICooldownManager**
(`EllesmereUICdmBuffBars.lua:4499-4517`) does `sb:SetMinMaxValues(0, 1)` and *then*
`sb:SetTimerDuration(durObj, interp, RemainingTime)`, in that order.
⚠ It also reaches for `Enum.StatusBarInterpolation.None`, which is **not** in the
generated enum (only `Immediate = 0` and `ExponentialEaseOut = 1`,
`SimpleStatusBarConstantsDocumentation.lua:25-28`) — prefer the documented member.
⚠ And `SetStatusBarTexture` returns a `success` **bool** (`:295-307`) that almost
everyone discards; a texture that fails to resolve yields a bar nothing can fill.
✅ **The bar renders.** `[client 2026-08-04]` — a live Summon Demonic Tyrant cooldown bar
drawing off a secret duration, in combat, on the recipe above.

**4. ⚠⚠ A DURATION OBJECT IS ITSELF A CURVE EVALUATOR — the curve sink we
concluded did not exist.** `LuaDurationObject:EvaluateRemainingDuration(curve,
modifier)` takes a `LuaCurveObjectBase` and returns a `LuaCurveEvaluatedResult`
(`LuaDurationObjectAPIDocumentation.lua:72-88`). So a **Step** curve
(`LuaCurveType.Step = 1`, *"performs no interpolation between points, instead
snapping to values exactly"*, `LuaCurveObjectConstantsDocumentation.lua:14`)
**thresholds a secret cooldown-remaining entirely in C**:

```lua
local curve = C_CurveUtil.CreateCurve()
curve:SetType(Enum.LuaCurveType.Step)
curve:AddPoint(0, 1); curve:AddPoint(threshold, 0)     -- our points, not secret
local r = dur:EvaluateRemainingDuration(curve, Enum.DurationTimeModifier.RealTime)
texture:SetDesaturation(r)                              -- AllowedWhenTainted sink
```

§4.8.1 concluded secret **counts** have no curve sink. True for counts — but a
duration object carries its own evaluator, so this is a general *"threshold a
secret number engine-side"* primitive, and it reaches `Desaturation` and
`CooldownStyle`, both already graded ✅ carries above.
✅ **The result is SECRET, and `SecretWhenCurveSecret` is not the whole condition**
`[client 2026-08-07]`. All five `Evaluate*` methods returned `<secret number>` in
combat on a duration whose `HasSecretValues()` was true, with the curve's own
`HasSecretValues()` reading **false** and `GetRemainingDuration` secret as the
control. So the annotation names a *sufficient* condition for secrecy, not a
necessary one — a non-secret curve does **not** buy a readable result, and the
binary-search leak the annotation seemed to license does not exist. **Feed the
result straight to a sink; there is nothing to read and nothing to guard.**

✅ **`Step` holds the PREVIOUS point's value, so an edge lands exactly on that point's
x** `[client 2026-08-07]`. Measured on a two-point curve `(0, 10)` and `(20, 20)`:

| x | −5 | 0 | 5 | 9.9 | 10 | 10.1 | 15 | 19.9 | **20** | 25 | 100 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `Step` | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | **20** | 20 | 20 |
| `Linear` | 10 | 10 | 12.5 | 14.95 | 15 | 15.05 | 17.5 | 19.95 | **20** | 20 | 20 |

It is a **floor**, not nearest-point — the value changes at `x = 20`, not at the midpoint
`x = 10`. So a threshold at *t* is two points: `AddPoint(0, below)` and
`AddPoint(t, above)`. ⚠ Nothing in the shipped UI uses `Step`
`[T1 obs: every Blizzard curve is Linear @ 12.0.7.68887]`, so this measurement is the
only description of its behaviour that exists.

✅ **Both curve types CLAMP outside their point range** `[client 2026-08-07]` — `x = −5`
returns the first `y` and `x = 25` / `x = 100` return the last, on `Step` and `Linear`
alike (table above). This had been inferred from `EncounterTimelineTrailAlphaCurve`
defining points only at `x = 0.0` and `0.1` while driving alpha across a full 0→1
progress `[T1 src: EncounterTimelineConstants.lua:193-196]`; the inference was right, and
a curve needs no padding point to be safe at its edges.
⚠ An **empty** curve evaluates to `0`, as documented — measured, so a zero result means
"no points" and not "the evaluation failed".
`` @pending-test: curve-step-and-clamp-semantics ``

⚠ **`C_CurveUtil.CreateColorCurve` is used NOWHERE in the shipped UI** `[T1 obs @
12.0.7.68887]`, so the colour-curve path has no Blizzard precedent — though `UnitPowerPercent`
taking one *is* measured (finding 8). Its `AddPoint` takes `(x: number, y: colorRGBA)`, and
`LuaColorCurveObject` additionally carries `EvaluateUnpacked` returning four plain numbers
(`LuaColorCurveObjectAPIDocumentation.lua:62-80`) — the packed `Evaluate` returns a
ColorMixin, which is finding 9's readable-table-with-secret-members shape.
⚠ **`modifier` is `Nilable = false` WITH a `Default`** (`:82`) — pass it
explicitly (§4.6's `Default ≠ Nilable` rule). A shipping addon passes an *alpha
value* in that slot, evidently believing it is a fallback; there is no fallback
parameter. Do not copy that shape.
*Seen working in:* EllesmereUI 8.7.5 (read for API discovery only, no code copied).
*Confidence:* high on the mechanism, **unmeasured** on result secrecy.

**5. `StatusBar:SetToTargetValue()` after arming a timer, on first show.** A bar
just made visible otherwise interpolates from its stale previous value up to the
timer's position. `SetToTargetValue` *"immediately finishes any interpolation of
the bar and snaps it to the target value"*
(`SimpleStatusBarAPIDocumentation.lua:322-329`). So the full recipe is
`SetMinMaxValues(0, 1)` → `SetTimerDuration(dur, interp, RemainingTime)` →
*`SetToTargetValue()` if newly shown*. *Confidence:* high.

**6. `Cooldown:SetCooldownFromDurationObject` needs NO range-equivalent** — unlike
the StatusBar, the duration object is passed bare and the swipe geometry comes
from it (`FrameAPICooldownDocumentation.lua:305-314`; `clearIfZero` defaults
`true`). Two riders: the swipe is drawn from the widget's **armed duration**, not
from the `SetDrawSwipe` flag, so `SetDrawSwipe(true)` on a cleared widget draws
nothing; and a widget that may be showing aura display time needs
`SetUseAuraDisplayTime(false)` first (`:545-554`) or it keeps drawing the aura
timer. *Confidence:* high on the first, medium on the ordering rider.

**7. A second text route: `GetRemainingDuration()` → `SetFormattedText`.**
`GetRemainingDuration(modifier)` returns a `DurationSeconds`
(`LuaDurationObjectAPIDocumentation.lua:270-283`) that is a **secret number in
combat**, and `FontString:SetFormattedText` (`AllowedWhenTainted`, aspect `{Text}`)
renders it. Unlike finding 2's formatter route the format string lives in Lua, so
precision is per-call. ⚠ It inherits finding 10 — `SetFormattedText` **poisons
anchoring**, so the FontString must be a leaf. `DurationTextBinding` remains the
only anchor-safe text route.
⚠⚠ **AND `type(x) == "number"` IS THE WRONG GUARD.** A secret number fails it, so
a bare `type()` check silently rejects exactly the in-combat case you need. Ask
`issecretvalue` first (rule 15). *Confidence:* high on the API pair.

**8. `UnitPowerPercent` accepts a `LuaColorCurveObject`.** Its curve argument is
typed `LuaCurveObjectBase` (`UnitDocumentation.lua:2729`), the shared base of both
curve types, and the client **does** take a colour curve there: secret Fury drove
`SetVertexColor` directly, with no boolean quantisation. Previously inferred from
the type signature; now measured.

**9. ⚠⚠ A COLOUR RESULT IS A READABLE TABLE WITH SECRET MEMBERS.** Both
`UnitPowerPercent(…colorCurve)` and `GetAuraDispelTypeColor` return an ordinary
ColorMixin whose `.r`/`.g`/`.b` are secret. So `issecretvalue` on the table is
**false** and `issecrettable` is **false** — you must ask about the *members*.
Code that classifies a colour by the table alone concludes "no secret here".

**10. ⚠⚠ TEXT APPLIES AN ASPECT *AND* MARKS ANCHORING SECRET.** `FontString:SetText(secret)`
records **both** `landed=aspect+` (the `{Text}` aspect) **and** `anchor 0>1` on the
FontString *and its dependent* — the two outcomes co-occur, which is why §4.6 states them
as non-exclusive. Mechanically this is unsurprising — a FontString's extent is
derived from its text, so a secret string implies a secret size — but the
consequence is practical: **never anchor anything to a FontString you feed a secret
string.** ⚠ **`DurationTextBinding` does NOT do this**: it writes the text C-side
and the anchor stayed clean (`0>0`), so it is the anchor-safe route to secret text
and `SetText` is not.

**11. `SetTexture` refuses a secret string outright** despite carrying
`SecretArguments = "AllowedWhenTainted"`
(`SimpleTextureBaseAPIDocumentation.lua:441`). The annotation is necessary, not
sufficient — the client's own message is *"Cannot set texture to a secret string
value."* `SetAtlas`, on the identical annotation, accepts it silently.

**12. `SetColorTexture` poisons the anchor chain**, confirming the §4.6(b)
prediction for the aspect-less setters, and the contagion **reached the dependent
child** — down-chain propagation observed, not merely documented. `UIParent` stayed
clean throughout (the canary never fired), so **propagation really is down-only**;
that had been Tier 2.

**13. ✅ `StatusBar:SetStatusBarColor` carries a secret — but only on a bar that HAS a
status-bar texture, and the aspect lands on the TEXTURE, not the bar.** An earlier
run recorded *"Object did not allow secret."* on every attempt; that was the
probe's own bug (a StatusBar with no `SetStatusBarTexture`, and that setter tints
the bar's texture, so there was no object to mark). Re-measured with a texture:
the call succeeds and `GetStatusBarColor` flips to secret. ⚠ **But
`HasSecretAspect(VertexColor)` on the StatusBar stays FALSE** (`landed=aspect-`,
`read=SECRET`) — so **an aspect can land on a delegated child object rather than
the one you called the setter on**, and an aspect check on the wrong object reports
a working channel as inert. Check `GetStatusBarTexture()` for this one.

⚠ **The client's refusal message distinguishes the two failure modes**: *"Object did
not allow secret."* is the **object** refusing, where *"Cannot set texture to a
secret string value."* (finding 11) is the **argument** being rejected. Read the
message — the docs' `SecretArguments` annotation only covers the second.

**[gap] — the two `⚪` rows above are unresolved by construction.** `SetAtlas` and
the two `AnimVertexColor` setters declare no aspect, expose no getter and did not
touch the anchor chain, so "accepted and nothing observable changed" is the strongest
statement the instrument can make. Whether the pixel moved needs an eyeball on
`/cdmp curve card`. `@verify-ingame`

#### 4.8.2 A THRESHOLD CUE ON A SECRET COUNT — shipped and confirmed in play

⚠ **This is not a measurement, it is a working technique.** Built and flown
`[client 2026-08-04]` (Demonology): a visible cue that fires at
*>6 Wild Imps* and at *4 Demonic Core* — two counts that are **secret in combat**
and, per §4.8.1, have **no curve sink**, so they can never reach alpha, colour or a
bar. Text is the only channel that accepts one at all.

**The trick is that the comparison happens in C and we consume only the visual
difference.** `C_UnitAuras.GetAuraApplicationDisplayCount(unit, auraInstanceID,
minDisplayCount, maxDisplayCount)` (`UnitAuraDocumentation.lua:112-128`) is a
three-way quantiser:

| applications | returns |
|---|---|
| below `min` | **empty string** |
| between | the count |
| above `max` | `"*"` |

An empty string renders nothing; a count renders. So a FontString fed
`(unit, id, 7, nil)` is **invisible below 7 stacks and shows the number at 7+**, and
no Lua ever reads, compares or sees the value. **The appearance of the text is the
cue.** Confirmed on screen: the number appears on crossing the threshold.

**Three preconditions, all of them non-obvious:**

1. **A live `auraInstanceID`.** The call is `RequiresValidUnitAuraInstance` and the
   aura enumeration is sealed in combat — but `item.auraInstanceID` on Blizzard's own
   CDM frame reads a plain number in a pull (cooldown-manager.md §7 Tier 2). Without
   that the technique is dead; a secret id would be **refused**, since the API is
   `SecretArguments = "AllowedWhenUntainted"`.
   ⚠ **`unit` should come off the same frame.** `item.auraDataUnit` is a plain
   `"player"` / `"target"` and is non-nil *iff* that row has a live bound aura (same
   section), so one frame supplies both arguments, they describe the same aura instance on
   the same unit, and a nil unit is the same statement as no instance to point at. This
   pairing is a **composition of two measured facts and has not itself been run** — the
   flown cue hardcoded `"player"`, which is correct for a self-buff and says nothing about
   a target aura. `@verify-ingame`
2. **The FontString must be a LEAF.** `SetText` with a secret applies `{Text}` *and*
   marks anchoring secret, propagating down (§4.8.1 finding 10). Anchor it *to*
   something and never anchor anything *to it*.
3. **Draw where you like.** ⚠ The read needs the CDM item frame; **the draw does
   not.** By the time you hold the string the comparison is done and it is ordinary
   text. Anchoring the draw to the item is a design choice, and a poor one here — the
   same aura can be tracked on **two viewers at once** (Demonic Core: bar *and* icon),
   so a first-match-wins anchor flip-flops.

⚠ **Out of combat the same call returns a PLAIN STRING** (`SecretWhenUnitAuraRestricted`,
so the seal is contextual, not permanent). Openers and desk checks can read the count
as ordinary text; only mid-pull is the quantiser needed.

#### 4.8.3 `[client]` Which comparisons a secret survives — partial, measured

Bare `==` against a **number** throws: `item.auraSpellID == spellID` killed a refresh
loop the instant combat started `[client 2026-08-04]`. `x == nil` is **permitted**, and it
is the only comparison that is — measured all four ways `[client 2026-08-05]`, with `s == 0`
as the throwing control in the same sample. §4.2's operation table is the row to cite. So a
nil-guard on a maybe-secret value is safe and a guard on anything else is not, which is what
lets a channel return "nil, or a value you may not look at" as its whole contract.

**The practical rule needs neither:** ask `ns.ClassOf`/`issecretvalue` first and branch
on the **class**, never on the value. Then nothing depends on which comparisons the
client happens to allow.

⚠ **And the meta-lesson from four rounds of debugging this**, worth more than either
fact: *every* guard was on the reads expected to be secret, and *every* actual break
was on a value not thought of as data at all — a frame's `auraSpellID`, a StatusBar
with no texture, a holder frame with no rect. The secret-values model is not the hard
part. Remembering that everything touching a restricted object is in scope is.

#### 4.8.4 `LuaDurationObject` — the per-method verdict table

**Read this before asking this object anything.** It exists because the object's facts
were previously spread through findings 1–7 as prose, and prose cannot show you the
difference between *"measured, and the answer is no"* and *"nobody ever asked"*. A blank
cell below is a question; a filled one is closed. The §4.8.1 channel table has stopped
anyone re-asking about setters for the same reason.

Methods from `LuaDurationObjectAPIDocumentation.lua` @ 12.0.7.68887. "Under restriction"
means **in combat, on an object whose `HasSecretValues()` is true** — out of combat the
whole object is plain and no row here applies.

| Method | Returns | Under restriction | Evidence |
|---|---|---|---|
| `HasSecretValues()` | bool | **PLAIN, always** | `ReturnsNeverSecret = true`; read `true` in combat on a player buff and a target debuff `[client 2026-08-05]` |
| `GetRemainingDuration(mod)` | `DurationSeconds` | **SECRET** | both columns of the aura table `[client 2026-08-05]`; also finding 7. **The seal has no hole here** |
| `FormatRemainingDuration(fmt, mod)` | string | **secret string that RENDERS** | finding 2 `[client 2026-08-04]` — `SetText` puts it on screen, ticking, in combat. ⚠ the FontString must be a leaf (finding 10) |
| `EvaluateRemainingDuration(curve, mod)` | `LuaCurveEvaluatedResult` | **SECRET** | `[client 2026-08-07]` — secret **even with a non-secret curve** (`curve:HasSecretValues()` false), control `GetRemainingDuration` secret in the same sample. `SecretWhenCurveSecret` is a sufficient condition, not a necessary one |
| `EvaluateRemainingPercent` · `EvaluateElapsedDuration` · `EvaluateElapsedPercent` · `EvaluateTotalDuration` | same | **SECRET** | all four measured in the same sample `[client 2026-08-07]`. **The curve route leaks nothing — hand the result to a sink and stop guarding it** |
| `HasExpired(mod)` · `IsActive(mod)` · `HasStarted(mod)` · `IsZero()` | bool | **SECRET booleans** | All four read `<secret boolean>` in combat, on 5 in-combat runs, on a duration whose `HasSecretValues()` is true, with `GetRemainingDuration` secret in the same sample as the control `[client 2026-08-06]`. **There is no readable in-combat cooldown predicate on this object**, and the absent annotation was again not a guarantee. A secret bool may not gate a branch, but it still drives `SetAlphaFromBoolean` / `SetVertexColorFromBoolean` leak-free — so readiness is **drawable and not branchable *on this object***. An addon that must *branch* on readiness gets it off a different surface: `C_Spell.GetSpellCooldown(id).isActive` is a **plain, discriminating boolean in restricted combat** (`cooldown-manager.md` §7 Tier 3), because that struct seals per member rather than whole. Failing that, the `Available` / `OnCooldown` alert edges of `cooldown-manager.md` §5.1, with that section's warning about the rows those edges never fire for. These are also the workspace's **first boolean-typed secrets**, which is what supplies the operation table's row 8 with a source it never had |
| `GetElapsedDuration` · `GetTotalDuration` · `GetStartTime` · `GetEndTime` · `GetRemainingPercent` · `GetElapsedPercent` · `GetClockTime` · `GetModRate` | numbers | **UNMEASURED**, presumed secret | Same shape as `GetRemainingDuration`. Nobody has needed one; **presumed is not measured** and this row says so rather than implying coverage |
| `Copy()` | `LuaDurationObject` | **PLAIN handle** | `ReturnsNeverSecret = true` |
| `SetTimeFromStart` · `SetTimeFromEnd` · `SetTimeSpan` · `SetClock` · `Assign` · `Reset` · `SetToDefaults` · `GetClock` | — | setters/handles, no readback | — |

**Consumption — settled, and not in question.** All three sinks accept the object and
draw it in combat: `Cooldown:SetCooldownFromDurationObject` (finding 6),
`StatusBar:SetTimerDuration` (finding 3 `[client 2026-08-04]`, ⚠ `SetMinMaxValues(0,1)`
**first** or it draws 0 %), and `DurationTextBinding` (finding 10, the anchor-safe text
route). Confirmed end to end by eyeball on both a player buff and a target debuff
`[client 2026-08-05]`, and corroborated by a shipping addon. **Displaying an in-combat
duration is a closed question. Reading its number is a closed question — you cannot.**
What is open is exactly one row above.

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
  chat)."* `[T2 archive: 2025-10-01]`. The `Chat` member of
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

12.0.7's own security-relevant deltas, from the blue post `[T2 blue: 2026-04-30]` archived at
`Patch 12.0.7/API changes` (revid 6778033, 2026-07-22):
`GameTooltip_AddMoneyLine` added and all internal `SetTooltipMoney` calls
removed; unit-identity-restricted APIs now return nil/defaults instead of
erroring on unsupported tokens; `debugstack`/`debuglocals` become secret once
anything up the stack has touched a secret; `SimulateMouse*` no longer carry
taint but are gated on `MouseFocusValidForLimitedInput`;
`GetEventCPUUsage`/`GetFunctionCPUUsage`/`GetScriptCPUUsage` returned to
addons; chat events for currency/honour/loot/money/reputation/XP gains are no
longer secret.

### 4.11 Reading the *verdict* instead of the value — the display channel

§4.8 is one direction: hand a secret to a sink that can render it without you seeing it.
This is the **other** direction, and it is not documented anywhere in Blizzard's API surface
because it is not an API at all.

**The mechanism.** Blizzard's own untainted code reads a secret, decides something from it,
and writes that decision into ordinary widget state — a shown flag, a frame reference, a
plain boolean, a colour. **The decision is readable even when its inputs are not.** So when
a value is sealed, the question to ask is not "is there another accessor" but *"where does
the client render this, and what ordinary Lua does it write on the way there?"*

**The worked example** `[client 2026-07-31]` (`Blizzard_CooldownViewer` @ 12.0.7.68887).
`CooldownViewerItemMixin:IsInPandemicTime(timeNow)` is

```lua
return self.pandemicStartTime and timeNow >= self.pandemicStartTime and timeNow <= self.pandemicEndTime;
```

`[T1 src: CooldownViewer.lua:587]`. Calling it from an addon **throws** — but the method is
not restricted. Its *body* compares `pandemicStartTime`/`pandemicEndTime`, and those read
secret, so the comparison is what fails. That distinction is the whole point: *"the method
is restricted"* and *"the numbers are restricted"* imply different workarounds, and only the
second one has one.

The workaround is that Blizzard evaluates it anyway, every frame:
`CheckPandemicTimeDisplay` runs from the item's `OnUpdate` `[:98, :562]` and calls
`ShowPandemicStateFrame` / `HidePandemicStateFrame`, which **set and nil `self.PandemicIcon`**
`[:570-585]`. So `item.PandemicIcon ~= nil` is a live mirror of a predicate you cannot
evaluate — measured over a full DoT cycle as `nil` → `table` on entering the window → `nil`
again on refresh, never secret, never throwing.

**⚠ THE NAIVE FORM OF THIS RULE IS WRONG, and the same file refutes it.** "Look at the UI
tree for data" would also have you read `item:IsActive()`, which on a tab-1 row is
`return self.cooldownID ~= nil` `[:362-364]` — **a constant `true`** with no error and no nil
to distinguish it from a real signal. Frame state is not evidence merely because it is
readable. Four preconditions, each of which is a **measurement, not an assumption**:

| | Ask | Why it bites |
|---|---|---|
| 1 | **Recomputed, or set once?** | Per-frame (`OnUpdate`) is safe. Event-set state has the staleness problem you were escaping — you would be trading one one-shot for another. |
| 2 | **A derived verdict, or a stored copy?** | A frame holding `self.remaining = <secret>` gets you nothing. Presence/absence and enums declassify; numbers usually do not. |
| 3 | **Does it discriminate?** | Capture it in **both** states before believing it. This is exactly where `IsActive()` fails, and the failure is silent. |
| 4 | **Does it fail loudly?** | Almost never. It is an implementation detail at a pinned build, not an API — no deprecation, no warning. If it disappears it reads `nil` forever, which is indistinguishable from a legitimate negative. |

**The cost, stated plainly.** Anything consuming one of these needs a **bind-time capability
check** and a documented fallback, and it needs re-verifying on patch day like a moving
value — it carries none of the stability an API name does. Precondition 4 is the one that
turns this from a technique into a liability if skipped: a silently-absent field degrades
into a confident wrong answer, which is worse than the sealed value you started with.

**Other instances of the same mechanism** (all `[client]`, all in
`projects/cooldown-hud/docs` / `cooldown-manager.md` §7): `item.wasSetFromCharges` /
`wasSetFromCooldown` / `wasSetFromAura` — plain booleans recording which of four secret
sources won this refresh, i.e. *what the dial currently means*; `item.auraDataUnit` — a
plain `"player"`/`"target"` string naming which side a bound aura is on, where the whole
`AuraData` record is sealed; and `item:IsActive()` on **tab 2 only**, where it genuinely
tracks aura liveness. The last one is the pair that makes precondition 3 concrete: the same
method name, on two mixins, is a real signal on one and a constant on the other.

---

### 4.12 Power secrecy is per power type — PRIMARY resources are always secret

**This is the single most consequential secrecy rule for a rotation addon, and it is easy to
get exactly backwards from experience.** `UnitPower` is `SecretWhenUnitPowerRestricted`
(§4.7), which reads like an ambient combat gate. It is not. The restriction is **per power
type**, and the split is **primary vs. secondary resource**:

> "We have relaxed restrictions around `UnitPower` so the player's **secondary** resources
> are no longer secret (**primary resources remain secret**). Affected resources: Combo
> Points, Runes, Soul Shards, Holy Power, Chi, Arcane Charges, Essence."
>
> — `[T1 blue: Midnight Public Alpha Addon API Changes, 2025-11-24]`
>   (archived at `https://warcraft.wiki.gg/wiki/Patch_12.0.0/Planned_API_changes`)

So the **seven never-secret power types** are exactly that list. Everything else — **Mana,
Rage, Focus, Energy, Runic Power, Fury, Pain, Insanity, Maelstrom** — is secret, which is
**most specs in the game**.

**⚠ "Contextually secret" means the UNIT, not combat. There is no out-of-combat window.**
`[client 2026-08-03]`:

| probe | Fury (17) | Holy Power (9) |
|---|---|---|
| `C_Secrets.GetPowerTypeSecrecy(t)` | **2** (`ContextuallySecret`) | **0** (`NeverSecret`) |
| `C_Secrets.ShouldUnitPowerBeSecret("player", t)` | **true**, in a city *and* mid-pull | false |

The predicate's own documentation says why: *"…unless the subject unit does not have a power
of this type."* A Demon Hunter always has Fury, so Fury is always secret. Anyone waiting for
a quiet moment to seed a value is waiting for something that cannot happen.

**⚠ `UnitPower` and `UnitPowerMax` are DIFFERENT PREDICATES, and the max is readable.**
`UnitPowerMax` carries `SecretWhenUnitPowerMaxRestricted`, which applies only to units that
are **not player-controlled**. So on the player you can read the cap and never the current
value — an asymmetry worth knowing before concluding the whole rail is dark.

#### The sanctioned replacement: `C_Spell.IsSpellUsable`

`C_Spell.IsSpellUsable(spellID) -> isUsable, insufficientPower`
`[T1 src: SpellDocumentation.lua:873-888 @ 12.0.7.68887]`. It carries
`SecretArguments = "AllowedWhenTainted"` and — decisively — **no `SecretReturns` and no
`SecretWhen*` predicate at all**, so both returns are plain booleans from a tainted caller.
`insufficientPower` is documented as *"True if spell is specifically unusable due to
insufficient power (ie MANA, RAGE, etc)"*.

This is §4.11's rule generalised into an actual API: **read the verdict, not the value.** It
is the same shape as §4.8's `GetSpellCooldownDuration` → `LuaDurationObject` — Blizzard
answers the question in C and never hands you the input.

`[client 2026-08-03]`, **one sample, at low Fury** (Havoc Demon Hunter):

| spell | `isUsable` | `insufficientPower` |
|---|---|---|
| Throw Glaive 185123 | true | **false** |
| Eye Beam 198013 | false | **true** |
| Blade Dance 188499 | false | **true** |
| Chaos Strike 162794 | false | **true** |

Three spells reporting insufficient power while a fourth in the **same sample** reports fine
proves the flag is computed **per spell against its own cost**. At high Fury all four read
`true / false`.

**⚠ Three traps, all of which have cost this workspace a build.**

1. **Use `insufficientPower`, NOT `isUsable`.** `isUsable` was measured returning **true for
   a spell visibly on cooldown**. It answers *"can I afford it"*, not *"can I cast it"*.
   Readiness still has to come from a cooldown channel.
2. **DB2 costs are not the client's costs.** Throw Glaive reads `insufficientPower = false`
   at a Fury level where everything else fails — i.e. **free** — while DB2 `SpellPower` says
   25. Any hardcoded cost table is wrong for some build; ask the client.
3. **It is BINARY.** It is false at 40 Fury and at 170 alike, so **overcap avoidance is
   unrecoverable through it**. If you need "how full is the bar", the only route is §4.8's
   curve trick — `UnitPowerPercent(unit, type, unmodified, curve)` evaluated in C and handed
   straight to a draw call — and that result is unreadable to Lua by construction.

**⚠ A macro is a faithful test bed for `IsSpellUsable` specifically** (it has no return
predicate to gate), **but not in general**: the 3473 APIs marked `AllowedWhenUntainted`
genuinely behave differently from addon code. Macros get **no** secrecy exemption —
`issecretvalue(UnitPower("player", 17))` returns **true inside a macro** too.

**⚠ And "my resource bar works fine in ElvUI" is not a counter-example.** §4.8's
`AllowedWhenTainted` list lets a secret be *displayed* (`SetValue`, `SetText`,
`SetVertexColor`, …) while remaining un-branchable, and `print()` renders one. Both
observations are consistent with the secrecy finding; neither contradicts it.

**The failure mode this rule exists to prevent** is not "the gate does not work" — it is
that a refused read gets coerced to `0` somewhere downstream and every resource comparison
silently inverts: every spender unaffordable, every generator maximally urgent. That is
**absent-is-never-zero** (§4.3) applied to a rail rather than a field, and it shipped
undetected through 100 green unit tests in `projects/cooldown-hud` because the fixtures
supplied the number the client refuses. If your test harness can hand the code a resource
value, it cannot reproduce the only state the game ever produces.

---

## 5. What real addons do (Tier 3 — practice, not rules)

Measured across the seven clones in `raw/addon-research/`, at the commits
recorded in `sources.md` §3.1. **Details and Plater share an author
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
plus `CanCompareUnitTokens` on the next line (`init.lua:15-16`) — asking the
*predicate* before the call rather than testing the *result* after.

None of the above is a rule. It is what four of the seven surveyed codebases
ship at the commits recorded in `sources.md` §3.1.

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
  `HasRestrictions` (**236**), and a per-predicate `FailureMode` of
  `ReturnNothing`/`Error`/`ReturnWithError`, or none at all (§4.7). It never gives you
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
- **[mostly closed] The undocumented security primitives all EXIST.** `issecure`,
  `issecurevariable`, `issecretvalue`, `issecrettable`, `canaccessvalue`,
  `secureexecuterange`, `forceinsecure`, `hooksecurefunc` and `scrub` every one
  resolves as a `function`, and `C_Secrets` as a `table` `[client 2026-07-24]`.
  That matters most for **`issecurevariable`**, which is absent from the generated
  docs *and* appears nowhere in the shipped source — it is nonetheless present and
  callable, so the wiki (`API issecurevariable`, revid 6588975, 2026-01-03) is
  describing something real, not something removed.
  ⚠ Still open: **existence was measured, behaviour was not.** No signature,
  argument order or return shape here has been exercised, so the wiki remains the
  only source for *semantics*. Existence is the cheap half.
- **[gap] `taintLog` level 5 unverified.** The wiki says 12.0.1 added it; the
  BlizzardInterfaceResources dump (build 68256) does not mention it. No
  `taint.log` exists on this install to check against. `@verify-ingame`
- **[gap] Only the `[client]`-tagged claims — §4.8.1–§4.8.3, §4.11, §4.12 — have
  been executed in the client.** Everything else here is static-source or
  documentary, §0–§4.7 included. Anything phrased as runtime behaviour —
  especially the operation table in §4.2 and the aspect-marking claims in §4.6 —
  should be confirmed in game before being relied on, and the one place that was
  is exactly where the generated-docs reading turned out to be insufficient
  (`SetTexture` carries `AllowedWhenTainted` and still refuses a secret string).
  This is a **coverage statement, not a claim** — there is nothing here for a single
  marker to resolve, so it carries none. The per-operation questions it implies live
  in `projects/addon-lab/questions.json` (README §1.2), where each is separately
  answerable.
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
7. A snippet may only call names present in the assembled restricted scope:
   `RESTRICTED_FUNCTIONS_SCOPE` (`RestrictedEnvironment.lua:24-77`),
   `DIRECT_MACRO_CONDITIONAL_NAMES` (`:81+`), **and** the injections
   `RestrictedExecution.lua` adds on top — including a `table` namespace
   (`maxn`, `insert`, `remove`, `sort`, `concat`, `wipe`, `new`) and top-level
   `newtable`/`copytable`/`pairs`/`ipairs`/`next`/`unpack`/`tinsert`/`tremove`/
   `type`/`rtgsub`. Snippet-local storage is available: `newtable()` /
   `table.new()` is the substitute for the `{}` constructor rule 6 rejects (§3.2).
   [Tier 1: `RestrictedExecution.lua:276-294, 323-335`;
   `RestrictedInfrastructure.lua:563-580` (the `rtable` export);
   `RestrictedEnvironment.lua:24-77`]
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
    [Tier 2 for the `type()` behaviour: `Secret Values`, revid 6777907, 2026-07-22.
    Tier 1 for Blizzard writing code that way:
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
17b. A read of Blizzard **widget internals** used as a substitute for a sealed
    value (§4.11) is guarded at bind time and has a documented fallback. It is an
    implementation detail at a pinned build, not an API: it carries no
    deprecation and no error, so its disappearance reads as a legitimate
    negative. The read must also be shown to **discriminate** — captured in both
    states — because the failure mode is a constant, not an exception.
    ⚠ `CooldownViewerItemMixin:IsActive()` is the standing counter-example: on
    tab 2 it tracks aura liveness, on tab 1 it is `self.cooldownID ~= nil`, i.e.
    constant `true`. Same method, two mixins, opposite trustworthiness.
    [Tier 1: `Blizzard_CooldownViewer/CooldownViewer.lua:362-364` (the constant),
    `:570-585` + `:98` (the per-frame `PandemicIcon` write).
    [client 2026-07-31] for both the constant-true measurement and the
    `PandemicIcon` cycle]
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
    `Enum.SecretAspect.Shown` cannot be **triggered** by an addon — `SetShown` is
    `AllowedWhenUntainted` *and* `IsProtectedFunction = true`.
    ⚠ **"An addon cannot trigger it" is not "an addon will never see it."**
    `IsVisible` carries `SecretReturnsForAspect = { Enum.SecretAspect.Shown }`
    (`SimpleScriptRegionAPIDocumentation.lua:534-536`), and an addon-created frame
    parented into an **engine-owned** subtree returns a secret from it, because the
    engine drives the parent's shown state. A bare boolean test on that return
    errors. **Guard the getter side always**, whoever set the aspect.
    [Tier 3 for the engine-subtree reachability, reported against 12.1.0 aura
    buttons; Tier 1 for the annotation.] `@verify-ingame`
    [Tier 1: `SimpleFontStringAPIDocumentation.lua:653-656, 352`;
    `SimpleFrameAPIDocumentation.lua:1354-1358, 841, 895`]
20. Code must not assume `GetPoint`/`GetLeft`/`GetWidth` are readable on a
    frame anchored (directly or transitively) to a frame marked
    `HasSecretValues()`. Test with `ScriptRegion:IsAnchoringSecret()`.
    ⚠ **A FontString fed a secret via `SetText` is one of these** — it takes the
    `Text` aspect *and* goes anchoring-secret, so it must be a layout leaf:
    anchor it to things, never things to it (§4.6, measured at §4.8.1 finding 10).
    [Tier 1 for the APIs: `SimpleScriptRegionAPIDocumentation.lua:367`;
    `SimpleFrameScriptObjectAPIDocumentation.lua:69`. Tier 2 for downward
    propagation: the blue post of 2025-10-01 and `Secret Values`, revid 6777907, 2026-07-22]
21. Aspect/secret state on a widget is cleared only by
    `FrameScriptObject:SetToDefaults()`, which is itself
    `IsProtectedFunction = true` — so on a **protected** frame it cannot be
    called from addon code in combat. On an ordinary unprotected addon frame it
    **is** callable, so mid-combat clearing is not categorically impossible.
    Separately, Tier 2 notes that *clearing anchor points* can reset the
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
    `RequiresFontStringTextAccess` with `FailureMode = "ReturnNothing"`, so they
    return nothing (not an error) once the `Text` aspect is set. Layout code
    that divides by the returned width will then fail on nil.
    [Tier 1: `SecretPredicatesDocumentation.lua:21-24`;
    `SimpleFontStringAPIDocumentation.lua:10, 72`]
25c. Code distinguishes the two predicate kinds: a `Type = "Secret"` predicate
    (19 of them, none declaring a `FailureMode`) changes the *value* returned; a
    `Type = "Precondition"` predicate (32, of which 20 `ReturnNothing`,
    5 `Error`, 5 `ReturnWithError`, 2 undeclared) changes whether the *call*
    succeeds. Guarding a Precondition-annotated API with `issecretvalue` on its
    return is the wrong guard — it may have returned nothing at all. The
    Precondition addon code hits most often is `RequiresNonSecretAura` on
    `C_UnitAuras.GetPlayerAuraBySpellID` / `GetUnitAuraBySpellID` /
    `GetAuraDataBySpellName` (§4.7).
    [Tier 1: `uv run python -m wowkb.uiapi predicates` over
    `Blizzard_APIDocumentationGenerated/` at 12.0.7.68887 — 51 predicates,
    counts as given]
26. Error-reporting code that formats a message for display first checks
    `canaccessvalue(message)` — as of 12.0.7 `debugstack` and `debuglocals`
    themselves return secrets once anything up the stack has touched one.
    [Tier 1 for the pattern: `Blizzard_ScriptErrors/Blizzard_ScriptErrors.lua:75-83`.
    Tier 2 (blue-post archive) for the 12.0.7 change:
    `Patch 12.0.7/API changes`, revid 6778033, 2026-07-22]

---

## Changelog

- 2026-08-09 — §4.8.4: the four predicates stay secret, but "branch on readiness from events
  instead" was too narrow — `C_Spell.GetSpellCooldown(id).isActive` is a plain in-combat
  boolean (`cooldown-manager.md` §7 Tier 3). The claim is scoped to the object it measured.
- 2026-08-08 — §4.8.3's `== nil` marker dropped: §4.2's operation table already carried the
  measurement, so the claim read open in one section and closed in another. §4.8.2 gains the
  `unit` half of the quantiser's first precondition, marked unrun as a pairing.
- 2026-08-08 — §1.1: `[gap]` on the untested half of the anchoring claim — a dependent of a
  frame carrying a **secret** anchor (a CDM item frame in combat), as against the protected
  `ActionButton1` the measurement used.
- 2026-08-08 — §1.1: `[gap]` marking which of the 59 protected functions the in-combat
  addon-frame measurement actually covered — four, not all — and naming `SetFrameStrata`
  and `SetHeight`/`SetWidth` as the unmeasured ones addons reach for.
- 2026-08-07 — §4.8.1 finding 4: `Step` is a **previous-point floor** (an edge lands on the
  point's own x, not the midpoint), both curve types **clamp** outside their range, and every
  `Evaluate*` result is **secret even with a non-secret curve** — so the curve route grades a
  sealed duration with nothing to guard and no leak to avoid.
- 2026-08-07 — §4.8.4: the four `LuaDurationObject` predicates are **secret booleans**, so
  there is no readable in-combat cooldown predicate and readiness is drawable but not
  branchable. §4.2 row 8 and §4.3 trap 2: a boolean-typed secret is no longer hypothetical,
  so the row is answerable and the test is queued against that source.
- 2026-08-05 — **the security-primitive surface is measured** `[client 2026-07-24]`:
  all ten probed names exist (`C_Secrets` as a table, the rest as functions), including
  **`issecurevariable`**, which is absent from the generated docs *and* from the shipped
  source yet is live. Existence only — no signature or return shape was exercised, so
  the wiki remains the sole source for semantics (§2.3, §4.1).
- 2026-08-05 — §3.2 / rule 7: `table` **is** available to secure snippets. The
  restricted scope is assembled from two files and we had only read the first;
  `newtable()` / `table.new()` is the sanctioned `{}` substitute, so
  snippet-local storage is possible.
- 2026-08-05 — §4.5, §4.7: `RequiresNonSecretAura` is a per-aura **allowlist**
  Precondition on three `C_UnitAuras` spell-keyed getters. Aura secrecy under
  restriction is not a blanket seal, and `AllowedWhenTainted` alone does not mean
  the call will run.
- 2026-08-05 — §4.6: the three outcomes are not mutually exclusive. `SetText`
  applies the `Text` aspect **and** marks anchoring secret, so a FontString fed a
  secret must be a layout leaf.
