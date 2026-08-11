---
title: API surface, events and discovery
patch: 12.1.0
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://github.com/Gethe/wow-ui-source (tag 12.1.0, version.txt 12.1.0.69273, commit eb941aad028d73ddc69e3e8ef4da709f4d3cd744) — raw/addon-research/wow-ui-source-12.1.0. EVERY corpus count in this file was re-parsed here on 2026-08-11; `[T1 docs @12.1.0]` locators resolve here
  - https://warcraft.wiki.gg/wiki/Patch_12.1.0/API_changes (revid 6801760, 2026-08-09)
  - https://github.com/Gethe/wow-ui-source (version.txt 12.0.7.68887, commit 4383ced30106d51b27e3e86d1987f1552f0d259d) — raw/addon-research/wow-ui-source; the build an UNSTAMPED `file:line` was read at
  - https://warcraft.wiki.gg/wiki/API_Frame_RegisterEvent (revid 6654488, 2026-02-19)
  - https://warcraft.wiki.gg/wiki/API_Frame_RegisterUnitEvent (revid 6735133, 2026-06-04)
  - https://warcraft.wiki.gg/wiki/API_Frame_RegisterAllEvents (revid 6654327, 2026-02-19)
  - https://warcraft.wiki.gg/wiki/UIHANDLER_OnUpdate (revid 3167340, 2023-08-18)
  - https://warcraft.wiki.gg/wiki/UIHANDLER_OnEvent (revid 3807472, 2021-07-27)
  - https://warcraft.wiki.gg/wiki/API_C_Timer.After (revid 6592061, 2026-01-04)
  - https://warcraft.wiki.gg/wiki/API_ScriptRegion_HookScript (revid 6779372, 2026-07-23)
  - https://warcraft.wiki.gg/wiki/API_hooksecurefunc (revid 6588971, 2026-01-03)
  - https://warcraft.wiki.gg/wiki/Patch_12.0.0/API_changes (revid 6747189, 2026-06-18)
  - https://warcraft.wiki.gg/wiki/API_types/SpellIdentifier (revid 6776503, 2026-07-20)
  - https://warcraft.wiki.gg/wiki/Secret_Values (revid 6777907, 2026-07-22)
  - https://wago.tools/api/builds (queried 2026-07-23)
  - in-client measurement, ClientLab v0.1.0 (interface 120007), run 2026-07-24 07:49:13, out of combat  # the `[client 2026-07-24]` claims in this file — event-callback registry, RegisterUnitEvent cap, secure-hook flags, the profiler API. ✅ ARCHIVED, and re-checkable: projects/addon-lab/runs/2026-07-24-v0.1.0-legacy.json holds this run verbatim (6 of its anchors point into this file); the live SavedVariables key was purged by the capture-standard migration
  - Live install /mnt/c/Program Files (x86)/World of Warcraft/_retail_/
  - EllesmereUI v8.7.5 @ c4eba58d996a8436f467ac8f297148bff9dd3008 (2026-08-04),
    https://github.com/EllesmereGaming/EllesmereUI — license CUSTOM, ALL RIGHTS
    RESERVED; read for API discovery only, no code copied. Mined 2026-08-05 via the
    `mine-addon` skill; clone deleted after (step 5). file:line citations resolve
    only against that commit. Unverified residue:
    `addon-dev/mined-pending-verification.md`.
confidence: high
verified: 2026-07-23   # adversarial re-check of every locator + independent re-derivation of every corpus count
---

# API surface, events and discovery

**Scope.** The programming model an addon actually codes against — how work gets
scheduled (events, script handlers, callback registries, timers), what the API
surface looks like and how it is named, and — the part that outlives any specific
fact — **how to find things out for yourself**.

Deferred to siblings: taint and secret-value consequences of hooking →
`security-taint-and-restricted-data`. Widget/region methods, XML markup and
animation → `frames-textures-animation`. `.toc` and load order →
`anatomy-and-runtime`. SavedVariables and addon comms →
`state-persistence-and-communication`.

## Citation conventions used in this file

| Prefix | Means |
|---|---|
| `[T1 src]` | Blizzard's shipped UI source. Paths are relative to the `wow-ui-source` checkout root, i.e. prefix `raw/addon-research/wow-ui-source/`. Build **12.0.7.68887**, commit `4383ced30106`. |
| `[T1 docs]` | `Interface/AddOns/Blizzard_APIDocumentationGenerated/<file>` in the same checkout — Blizzard's machine-generated API spec. **592 `.lua` files** (the directory holds 593 entries; the 593rd is the `.toc`). Cited by bare filename since they all live in that one directory. |
| `[T1 obs]` | Directly observed on the live install at `/mnt/c/Program Files (x86)/World of Warcraft/_retail_/`. Observation of a shipped artefact, not of a spec. |
| `[T2 wiki]` | warcraft.wiki.gg, with revid and last-edit date. Pages rot silently, so the stamp is load-bearing. |
| `[T2 res]` | `Ketho/BlizzardInterfaceResources` @ `774b2c550366` — a derived per-build dump at build **12.0.7.68256**, a *different build of the same patch*. |
| `[T3]` | A named community addon or library at a named commit/version. A data point about that addon, never a rule. |

> ⚠ **Build skew.** This repo's `knowledge/_meta/game-version.md` records live as
> `12.0.7.68453`; the source checkout is `12.0.7.68887`; `BlizzardInterfaceResources`
> is `12.0.7.68256`. `wago.tools/api/builds` reports the newest `wow` build as
> **`12.0.7.68887`**, which is the checkout we are citing. Nothing in this file has been
> executed in the client; items that need that are marked `@verify-ingame`.

---

## 1. The programming model in one paragraph

An addon is a pile of Lua that runs once at load and then **does nothing until
something calls it**. There are exactly four mechanisms that can call it:

1. **Widget script handlers** — `OnEvent`, `OnUpdate`, `OnShow`, `OnClick`, …
   installed with `SetScript` / `HookScript` on a frame or region.
2. **Game events** — the client's ~1741-name event bus, delivered to frames that
   registered for them, through the frame's `OnEvent` handler.
3. **In-process callback registries** — `EventRegistry` and any
   `CallbackRegistryMixin` instance, a pure-Lua publish/subscribe layer Blizzard
   uses for UI-to-UI signalling that is not a game event.
4. **Timers** — `C_Timer.After` / `NewTimer` / `NewTicker`, plus the per-frame
   `OnUpdate` tick.

Everything else — polling loops, dirty flags, throttles — is built out of those
four. The rest of this file is about choosing between them and about how to find
the names.

---

## 2. Events

### 2.1 The corpus, and how events are named

At 12.1.0.69273 the generated documentation declares **1782 events** spread over
**210 system tables**, of which **1034 carry at least one typed payload field**
and **748 carry none** *[T1 docs @12.1.0: whole-corpus count, re-parsed
from all 612 `.lua` files in `Blizzard_APIDocumentationGenerated/`;
`grep -rh 'Type = "Event"' | wc -l` = 1782. The same parse reproduces the
12.0.7.68887 figures — 1741 / 204 / 1013 / 728 — exactly, which is what licenses
comparing the two]*.

⚠ **The `[T2 res]` cross-check is stale and was NOT re-run.**
`BlizzardInterfaceResources` has not been re-pulled past 12.0.7.68256, where
`Resources/Events.lua` listed exactly 1741 event strings in 204 system tables and
corroborated the old numbers on both. The 12.1.0 figures rest on the generated-doc
parse alone. `@verify-ingame` is the wrong marker here — what this needs is a
re-pull of that repo.

⚠ Don't confuse the 210 event-declaring systems with the **314** `Type = "System"`
tables in the whole corpus (§4.1): most systems declare no events at all.

**Every event entry has two names and only one of them is the string you
register with.** The docs give a CamelCase `Name` and a `LiteralName`:

```lua
{
    Name = "CombatLogEventUnfiltered",
    Type = "Event",
    LiteralName = "COMBAT_LOG_EVENT_UNFILTERED",
    HasRestrictions = true,
    SynchronousEvent = true,
    CallbackEvent = true,
},
```
*[T1 docs: `CombatLogDocumentation.lua:129-136`]*

`RegisterEvent` takes the `LiteralName`. The CamelCase `Name` is what the in-game
`/api` browser indexes; it appears **nowhere in Blizzard's game code** —
`grep -rn 'CombatLogEventUnfiltered'` over all 2298 shipped `.lua` files returns
exactly one hit, the doc entry itself at `CombatLogDocumentation.lua:130`
*[T1 src/docs: verified this session]*. So a name found in `/api` that greps to
nothing is usually this, not a missing name.

Only **45 of 1782** events carry any `Documentation` prose — the same 45 as at
12.0.7, so 41 new events arrived with no prose at all *[T1 docs @12.1.0: corpus
count]*. The ones that do are worth reading, because they occasionally state
timing guarantees no other source has — e.g.
`ENCOUNTER_TIMELINE_EVENT_REMOVED`: *"This is guaranteed to fire after an event
has transitioned to a 'final' state such as Canceled or Finished, and will be
delayed at least one game tick to allow for API queries to still access event
data in OnUpdate scripts."* *[T1 docs:
`EncounterTimelineDocumentation.lua:503`, the `ENCOUNTER_TIMELINE_EVENT_REMOVED`
entry]*.

### 2.2 Registering: the widget methods

All event registration is a method on the frame. The Tier-1 signatures, all from
`SimpleFrameAPI`:

| Method | Signature | Line |
|---|---|---|
| `RegisterEvent` | `(eventName: cstring) -> registered: bool` | `SimpleFrameAPIDocumentation.lua:943` |
| `RegisterUnitEvent` | `(eventName: cstring, units: UnitTokenType...) -> registered: bool` | `:984` |
| `RegisterAllEvents` | `()` | `:935` |
| `UnregisterEvent` | `(eventName: cstring) -> registered: bool` | `:1466` |
| `UnregisterAllEvents` | `()` | `:1458` |
| `IsEventRegistered` | `(eventName: cstring) -> isRegistered: bool, units: UnitTokenType?...` | `:681` |
| `RegisterEventCallback` | `(eventName: cstring, cb: FrameEventCallbackType) -> registered: bool` | `:958` |
| `RegisterUnitEventCallback` | `(eventName, cb, units...) -> registered: bool` | `:1000` |

*[T1 docs, all of them]*

The `units` parameter carries `StrideIndex = 1` in the docs, i.e. it is
variadic *[T1 docs: `SimpleFrameAPIDocumentation.lua:991`]*. The declared type is
`UnitTokenType`, a 362-value enumeration (`NumValues = 362, MinValue = 0,
MaxValue = 361`) *[T1 docs: `UnitSharedDocumentation.lua:6-10`]* — but Blizzard's
own call sites pass **strings**, e.g.
`self:RegisterUnitEvent("UNIT_FORM_CHANGED", "player")`
*[T1 src: `Blizzard_Collections/Mainline/Blizzard_MountCollection.lua:149`; also
`Blizzard_UIPanels_Game/Mainline/WorldMapActionButton.lua:93`]*.

> **[unverified]** *Why* a string is accepted where an enum is declared — whether
> the C layer maps the token string onto the enum, or the doc generator simply
> labels unit-token parameters with that type name — is **not** established by
> anything on disk. Both readings fit the evidence. Use the string form (that is
> what ships), but do not repeat a mechanism claim we cannot cite. `@verify-ingame`

Return-value semantics are **not** in Tier 1 (the docs give types, not meanings).
The wiki supplies them: *"Returns true if the frame is successfully registered to
the event. Returns false if the frame was already registered to this event.
Throws an error if the event is invalid."* *[T2 wiki: `API Frame RegisterEvent`,
revid 6654488, 2026-02-19; the erroring behaviour is attributed there to patch
8.0.1]*. Blizzard's own code corroborates that invalid event names are a real
failure mode by asserting on them before registering:
`assert(C_EventUtils.IsEventValid(event), ("Unknown event \"%s\""):format(event))`
*[T1 src: `Blizzard_SharedXML/EventUtil.lua:12`]*.

**`RegisterAllEvents` is a different mode, not a bulk registration, and
`UnregisterEvent` cannot punch a hole in it** `[client 2026-08-05]`. On a frame that has
called `RegisterAllEvents()`:

- `IsEventRegistered(x)` reads **false** — the mode leaves no per-event registration to
  inspect, so the usual predicate cannot tell you what the frame is listening to.
- `UnregisterEvent(x)` **succeeds and returns `false`**, and the event **keeps arriving**:
  the unregistered event was delivered 8 times in the same window its never-unregistered
  paired control was delivered 15 (552 events, 68 distinct, 26 s). A live control is what
  makes that 8 a measurement rather than a quiet window.

So the wiki's account is right, and Blizzard's Event Trace
calls `self:RegisterAllEvents()` *[T1 src:
`Blizzard_EventTrace/Blizzard_EventTrace.lua:107`]* and then
`self:UnregisterEvent("ADDON_LOADED")` *[T1 src: same file, `:702`]* — **a no-op in
Blizzard's own code.** If you need all-events *minus* a few, filter in the handler.
*[T2 wiki: `API Frame RegisterAllEvents`, revid 6654327, 2026-02-19, attributing the
change to 8.0.1]*

`RegisterUnitEvent` accepts *"up to four units"* and *"If no unit is given, then
all units will be watched; which is effectively the same as calling
`Frame:RegisterEvent`"*
*[T2 wiki: `API Frame RegisterUnitEvent`, revid 6735133, 2026-06-04]*.
**The four-unit cap is not enforced.** Registering with *five* unit tokens is
accepted — the call does not error `[client 2026-07-24]`, matching the generated
docs' unbounded variadic rather than the wiki's "up to four". Treat "four" as
guidance about how many filters are useful, not a limit the client applies.
⚠ Only the *acceptance* was measured; whether units past the fourth actually
filter anything was not, so do not rely on a fifth unit being watched.

### 2.3 The frame-as-listener idiom

The handler signature is `(self, event, ...)`, where `self` is the registered
frame and `...` is the payload
*[T2 wiki: `UIHANDLER_OnEvent`, revid 3807472, 2021-07-27]*.
Blizzard's own dispatcher demonstrates it directly:

```lua
self.frameEventFrame = CreateFrame("Frame");
self.frameEventFrame:SetScript("OnEvent", function(frameEventFrame, event, ...)
    self:TriggerEvent(event, ...);
end);
```
*[T1 src: `Blizzard_SharedXMLBase/GlobalCallbackRegistry.lua:7-10`]*

Two shapes recur:

- **One frame, one `if event == …` chain.** The wiki's canonical example
  *[T2 wiki: `UIHANDLER_OnEvent`]*.
- **One frame, a method-per-event lookup** — `frame:SetScript("OnEvent",
  function(self, event, ...) self[event](self, ...) end)` and then
  `function frame:PLAYER_LOGIN() … end` *[T2 wiki: same page, second example]*.
  oUF implements the same dispatch with a visibility guard:
  `local function onEvent(self, event, ...) if(self:IsVisible()) then return
  self[event](self, event, ...) end end` *[T3: oUF @ `5672a3cb10e1`,
  `events.lua:70-74`]*.

Blizzard also ships bulk-registration helpers:
`FrameUtil.RegisterFrameForEvents(frame, events)` loops `frame:RegisterEvent`
over an array, and `FrameUtil.RegisterFrameForUnitEvents(frame, events, ...)`
forwards a shared unit list *[T1 src: `Blizzard_SharedXMLBase/FrameUtil.lua:33-49`;
the full helper set, including the `…EventCallbacks` variants, is `:33-68`]*.
It uses them alongside, not instead of, direct calls: **223**
`FrameUtil.RegisterFrameForEvents` + 12 `…ForUnitEvents` call sites against
**2734** direct `:RegisterEvent(` calls *[T1 src: grep counts over
`Interface/AddOns/`]*. Treat the helper as a convenience, not a house style.

**Dispatch order between frames is not stable, and must not be relied on**
`[client 2026-08-05]`. Four frames created `ABCD` and registered `ABDC` — so creation and
registration order disagree on the last pair, and the observed order discriminates between
them — received 68 firings of one event in **two different orders within a single session**:
registration order `ABDC` 41 times and its exact reverse `CDBA` 27 times. Neither creation
order nor any single rule accounts for both.

That is stronger than "unspecified": it is *observably variable on one frame set in one
session*, so no amount of testing can establish an order to depend on. If two of your
frames must act in sequence, give one frame the event and have it call the other.

The wiki carries an explicit disclaimer box around its own description ("the wiki is not
liable if your addon somehow depends on this and it turns out to be wrong") and reports,
citing a `wowless` test harness, first-registration order with holes back-filled *[T2 wiki:
`API Frame RegisterEvent`, revid 6654488, §In-Depth Details]* — which matches the more
common of the two orders here and not the other.

### 2.4 The annotations that change how an event behaves

Event entries carry flags. Corpus counts at 12.1.0.69273 *[T1 docs @12.1.0: counted over
all 1782 event entries]*:

| Flag | Count | What it is evidence of |
|---|---|---|
| `SynchronousEvent` | 1663 | Blizzard distinguishes synchronous from non-synchronous delivery. **119 events lack it** — unchanged, so all 41 new events are synchronous. |
| `UniqueEvent` | 142 | 111 of the 142 are also non-synchronous. |
| `SecretInChatMessagingLockdown` | 62 | payload becomes secret under comms lockdown |
| `SecretWhenUnitSpellCastRestricted` | 16 | |
| `CallbackEvent` | 12 | see §2.5 |
| `SecretPayloads` | 7 | `MINIMAP_PING`, `UNIT_SPELL_DIMINISH_CATEGORY_STATE_UPDATED`, `RUNE_POWER_UPDATE`, `RUNE_TYPE_UPDATE`, `UNIT_DISTANCE_CHECK_UPDATE`, `UNIT_IN_RANGE_UPDATE`, `UNIT_MAX_HEALTH_MODIFIERS_CHANGED` |
| `HasRestrictions` | 7 | the four `COMBAT_LOG_*`, `MINIMAP_PING`, and **new at 12.1.0** `UNIT_PING_PIN_ADDED` / `UNIT_PING_PIN_REMOVED` |
| `SecretWhenUnitIdentityRestricted` | 3 | |
| **`SecretWhenAurasRestricted`** | **1** | **`UNIT_AURA` — new at 12.1.0, and the whole payload** |
| `SecretWhenEncounterEvent` / `RequireNPERestricted` / `SecretWhenLossOfControlInfoRestricted` / `SecretWhenUnitPowerRestricted` | 1 each | |

⚠⚠ **A `Secret` predicate on an event entry is a SECOND route to a secret payload,
and `SecretPayloads` does not cover it.** The `SecretPayloads` list is unchanged at
seven and `UNIT_AURA` is **not** on it — yet `UNIT_AURA` delivers a fully secret
payload while auras are secret, via `SecretWhenAurasRestricted = true` on the event
*[T1 docs @12.1.0: `UnitAuraDocumentation.lua:602-609`, the marker at `:603`]*. An
audit that enumerates "which events can hand me a secret" by grepping
`SecretPayloads` alone misses it. `security-taint-and-restricted-data` §4.7 owns the
mechanism.

The non-synchronous / `UniqueEvent` set *looks* like the family you would expect
to be coalesced — these seven are all both non-synchronous and `UniqueEvent`:
`ACTIONBAR_UPDATE_COOLDOWN`, `ACTIONBAR_UPDATE_STATE`, `ACTIONBAR_UPDATE_USABLE`,
`BAG_UPDATE_COOLDOWN`, `BAG_UPDATE_DELAYED`, `AREA_POIS_UPDATED`,
`CLUB_MEMBERS_UPDATED` *[T1 docs: flag values read off the corpus, each
re-verified this session]*. That is a **hand-picked 7 of 119**, chosen because
they fit; it is illustration, not proof of a pattern across the set.

> **[gap] The *meaning* of `SynchronousEvent` and `UniqueEvent` is not
> documented anywhere I could reach.** The generated docs carry no
> `Documentation` field for either flag; neither string appears in
> `Blizzard_APIDocumentation/` (the `/api` browser does not render them) nor in
> `Blizzard_EventTrace/`; and warcraft.wiki.gg has no page for either. The
> natural reading — *synchronous = dispatched inline at the moment the C code
> raises it; non-synchronous = queued; unique = at most one queued instance,
> i.e. coalesced* — is **inference, not evidence.** Do not build a throttling
> design on it without testing. `@verify-ingame`
> Looked at: `wowkb.uiapi grep`, `Blizzard_APIDocumentation/*.lua`,
> `Blizzard_EventTrace/*.lua`, `wowkb.wiki search`.
>
> `grep -rn 'SecureHooksAllowed\|SynchronousEvent\|UniqueEvent'` over every
> non-generated `.lua`/`.xml` in the checkout returns **zero** hits, so these are
> annotations the doc generator emits and nothing in the shipped Lua consumes or
> explains. For `SynchronousEvent`/`UniqueEvent` their names are suggestive and that
> is all we have.
>
> **`SecureHooksAllowed` and `CallbackEvent` are no longer in that boat** — both are
> measured `[client 2026-07-24]` and both are enforced: hooking a
> `SecureHooksAllowed = false` function is refused outright (§5.4), and
> `C_EventUtils.IsCallbackEvent` tracks the `CallbackEvent` flag exactly (§2.5). That
> two of the four annotations turned out to be real is a reason to *test* the other
> two rather than to keep reasoning about them.

Secret-payload consequences belong to the security topic; the wiki's `Secret
Values` page states that these predicates apply to *"Guarded APIs **and
events**"* *[T2 wiki: `Secret Values`, revid 6777907, 2026-07-22]*.

### 2.5 The Midnight event-callback API

12.0.0 added a **second, frameless** way to receive events. New in that patch,
per the wiki's consolidated added-API lists: globals `RegisterEventCallback`,
`RegisterUnitEventCallback`, `UnregisterEventCallback`,
`UnregisterUnitEventCallback`, `C_EventUtils.IsCallbackEvent`; widget methods
`Frame:RegisterEventCallback`, `Frame:RegisterUnitEventCallback` *[T2 wiki:
`Patch 12.0.0/API changes`, revid 6747189, 2026-06-18]*.

Tier-1 signatures *[T1 docs: `FrameScriptDocumentation.lua:296, :308, :442, :454`]*:

```
RegisterEventCallback(eventName: cstring, callback: EventCallbackType)
RegisterUnitEventCallback(eventName: cstring, callback: EventCallbackType, unit: UnitToken)
UnregisterEventCallback(eventName: cstring, callback: EventCallbackType)
UnregisterUnitEventCallback(eventName: cstring, callback: EventCallbackType, unit: UnitToken)
```

All four are annotated `SecureHooksAllowed = false` *[T1 docs: same lines]*.

The `callback` parameter is typed `EventCallbackType`, declared as
`Type = "CallbackType"` with no fields — i.e. the spec says nothing about its
shape *[T1 docs: `FrameScriptDocumentation.lua:503-505`]*. **In practice a plain
Lua function works**: Blizzard calls the global form with bare functions at five
sites *[T1 src: `Blizzard_ChatFrame/Shared/ClassTalentHelper.lua:15, :20, :25,
:30`; `Blizzard_SharedXMLGame/Tooltip/TooltipComparisonManager.lua:387`]*, e.g.

```lua
RegisterEventCallback("CLASS_TALENTS_SWITCH_TO_LOADOUT_BY_NAME", function(_nilOwner, loadoutName)
    CheckLoadPlayerSpellsFrame();
    PlayerSpellsFrame.TalentsFrame:LoadConfigByName(loadoutName);
end);
```
*[T1 src: `ClassTalentHelper.lua:15-18`]*

**Every callback fed to this API in the shipped tree declares a leading
`_nilOwner` parameter before the payload** — 7 sites, all spelling the name
identically and all discarding it: `ClassTalentHelper.lua:15, :20, :25, :30`,
`TooltipComparisonManager.lua:383`, and both wrappers in `Event.lua` (`:6`, `:20`)
*[T1 src: `grep -rn '_nilOwner'` over `Interface/AddOns/` returns exactly those
7 lines]*. That consistency is the only evidence for the dispatch convention;
the spec itself says nothing (see rule 25).

A `C_FunctionContainers` container is the *other* accepted shape, and Blizzard
wraps in one when it wants a stable value to unregister with:

```lua
function Event.RegisterCallback(event, cb)
    local cbContainer = C_FunctionContainers.CreateCallback(function(_nilOwner, ...) cb(...) end);
    local handle = { Unregister = function() UnregisterEventCallback(event, cbContainer); end };
    RegisterEventCallback(event, cbContainer);
    return handle;
end
```
*[T1 src: `Blizzard_SharedXMLBase/Event.lua:5-17` — the whole file is 31 lines;
`Event.RegisterUnitCallback` is the same shape at `:19-31`]*

`C_FunctionContainers.CreateCallback` — the factory that wrapper depends on — is
**absent from the generated documentation** and appears in the shipped source as
exactly 11 call sites, only two of which (`Event.lua:6`, `:20`) are about events
at all *[T1 docs/src: `wowkb.uiapi missing C_FunctionContainers` → "generated
docs: no, UI source hits: 11"; verified by direct grep]*. The container's only
observable purpose here is to give `handle:Unregister()` a value it can pass back
to `UnregisterEventCallback`.

The `Frame:` variants take a `FrameEventCallbackType`, likewise an empty
`CallbackType` *[T1 docs: `SimpleFrameAPIDocumentation.lua:1489-1491`]*, and
Blizzard passes bare closures to those too:
`self:RegisterEventCallback("MINIMAP_PING", function() PlaySound(SOUNDKIT.MAP_PING); end)`
*[T1 src: `Blizzard_Minimap/Mainline/Minimap.lua:150`]* — that one takes no
parameters at all, so it is not evidence either way about the owner argument.

> **The two forms do not demand different callback shapes.** Both accept a bare function
> and both accept a container; the global form is called with bare functions at five sites
> (above) and with a container at two. Full census of `RegisterEventCallback` /
> `RegisterUnitEventCallback` in the checkout — global form:
> `ClassTalentHelper.lua:15, :20, :25, :30`, `TooltipComparisonManager.lua:387`,
> `Event.lua:14`, `:28`; `Frame:` form: `Minimap.lua:150`, `FrameUtil.lua:53`, `:66`
> *[T1 src]*.

> **[gap] `Frame:UnregisterEventCallback` is undocumented but used.** Blizzard's
> own helper calls `frame:UnregisterEventCallback(event)` — one argument — at
> *[T1 src: `Blizzard_SharedXMLBase/FrameUtil.lua:59`]*, yet no
> `UnregisterEventCallback` exists on `SimpleFrameAPI` in the generated docs
> (only the global, at `FrameScriptDocumentation.lua:442`, and that one requires
> the callback as a second argument) *[T1 docs: `grep 'Name =
> "UnregisterEventCallback"'` over all 592 doc files returns exactly one hit]*.
> It is also **absent from the 12.0.0 added-widget list**, which does carry
> `Frame:RegisterEventCallback` and `Frame:RegisterUnitEventCallback`
> *[T2 wiki: `Patch 12.0.0/API changes` revid 6747189, §Consolidated changes →
> Widgets → Added (28)]*, and the wiki has no `API Frame UnregisterEventCallback`
> page *[T2 wiki: reported `PAGE DOES NOT EXIST`]*. `FrameUtil.lua:59`
> is the **only** call site in the entire checkout.
>
> **Measured: the frame method does not exist.** `UnregisterEventCallback` on a live
> frame reads `nil` `[client 2026-07-24]` — the name resolves only to the global at
> `FrameScriptDocumentation.lua:442`, not to a widget method. So `FrameUtil.lua:59` is
> **a latent error in Blizzard's own shipped code**: that line would raise
> *"attempt to call method 'UnregisterEventCallback' (a nil value)"* if it ever ran.
> Its being the sole call site is consistent with the path being dead.
> ⚠ **Do not call `frame:UnregisterEventCallback(...)`.** To unregister a callback,
> use the global two-argument form, which takes the callback back as its second
> argument — meaning you must keep a reference to it.

**`CallbackEvent = true` marks 12 events** *[T1 docs: grep over the corpus]*:

`COMBAT_LOG_EVENT`, `COMBAT_LOG_EVENT_UNFILTERED`,
`COMBAT_LOG_EVENT_INTERNAL_UNFILTERED`, `COMBAT_LOG_APPLY_FILTER_SETTINGS`,
`COMBAT_LOG_REFILTER_ENTRIES`, `ENCOUNTER_STATE_CHANGED`,
`TOOLTIP_SHOW_ITEM_COMPARISON`, `MINIMAP_PING`,
`CLASS_TALENTS_SWITCH_TO_LOADOUT_BY_INDEX`,
`CLASS_TALENTS_SWITCH_TO_LOADOUT_BY_NAME`,
`CLASS_TALENTS_SWITCH_TO_SPECIALIZATION_BY_INDEX`,
`CLASS_TALENTS_SWITCH_TO_SPECIALIZATION_BY_NAME`.

There is a companion predicate, `C_EventUtils.IsCallbackEvent(eventName) ->
isCallbackEvent` *[T1 docs: `EventUtilsDocumentation.lua:11-24`]*. **The docs
carry no prose for it**, and it is called nowhere in the shipped Lua, so *"the 12
`CallbackEvent` events are exactly the ones this API accepts"* is a reasonable
reading but **not** a Tier-1 statement. What *is* Tier 1: all six of Blizzard's
own `RegisterEventCallback` call sites use events from this list
(`CLASS_TALENTS_SWITCH_TO_*` ×4, `TOOLTIP_SHOW_ITEM_COMPARISON`, `MINIMAP_PING`),
as does `Blizzard_CombatLogProcessor` (`COMBAT_LOG_EVENT`,
`COMBAT_LOG_REFILTER_ENTRIES`, `COMBAT_LOG_APPLY_FILTER_SETTINGS`).
**The predicate tracks the flag.** `C_EventUtils.IsCallbackEvent("MINIMAP_PING")`
(flagged) returns **true** and `IsCallbackEvent("PLAYER_LOGIN")` (unflagged) returns
**false** `[client 2026-07-24]`. So *"the 12 `CallbackEvent` events are exactly what
the callback API accepts"* is no longer just a reasonable reading — the client agrees
on both sides of the boundary, and `IsCallbackEvent` is the cheap runtime check for
whether an event can be used with `RegisterEventCallback` at all.

**Nobody in the surveyed ecosystem uses it.** Across the seven cloned addons —
WeakAuras2, BigWigs, Details, Plater, ElvUI, oUF, Ace3 — there are **0**
occurrences of `RegisterEventCallback` in any `.lua` file, against 1503
occurrences of `:RegisterEvent(` *[T3: counted over the clones at the commits in
`sources.md` §3.1–3.2; note the `.pkgmeta` caveat that library code is not in
these trees, and that Details and Plater share an author]*.

### 2.6 The combat log: the registration that now errors

This is the highest-consequence event change in Midnight and it is worth
spelling out with all its evidence.

**Claim: on Retail 12.0.x, `frame:RegisterEvent("COMBAT_LOG_EVENT_UNFILTERED")`
raises an error.** Three independent sources:

1. *[T2 wiki: `Patch 12.0.0/API changes`, revid 6747189, 2026-06-18, §Summary]* —
   *"COMBAT_LOG_EVENT and COMBAT_LOG_EVENT_UNFILTERED will error when trying to
   register them."*
2. *[T1 obs: live install, `RaiderIO` 12.0.7 (v202607232037), `core.lua:14618`]* —
   a commented-out entry in that addon's tracking-event list reading
   `-- "COMBAT_LOG_EVENT_UNFILTERED", -- TODO: This didn't error on beta, but
   started to upon 12.0 release`. This is a shipping addon's own field note,
   dated by its own build stamp.
3. *[T3: BigWigs @ `3fdc10f6cfd1`, 2026-07-21]* — the addon's entire combat-log
   subscription API is disabled on Retail: `function boss:Log(event, func, ...)
   if self:Retail() then return end` (`Core/BossPrototype.lua:1201-1202`), same
   guard on `boss:Death` (`:1234-1235`), and the plugin-level registration is
   wrapped in `if not BigWigsLoader.isRetail then` (`Plugins/BattleRes.lua:1503-1505`,
   `:1524-1526`).

Blizzard's own combat-log consumer no longer uses a frame at all:

```lua
Event.RegisterCallback("COMBAT_LOG_EVENT", OnCombatLogEvent);
```
*[T1 src: `Blizzard_CombatLogProcessor/Blizzard_CombatLogProcessor.lua:21`]*

**But addons cannot copy that file.** Its manifest declares
`## UseSecureEnvironment: 1` *[T1 src:
`Blizzard_CombatLogProcessor/Blizzard_CombatLogProcessor.toc`]*, which is a
Blizzard-internal directive (see `anatomy-and-runtime`), and the read APIs it
uses live in `C_CombatLogSecure`, whose documentation table is stamped
`Environment = "SecureOnly"` — **one of only two so marked among the 385 doc
tables that declare an `Environment` at all** (308 `System` + 77 `ScriptObject`;
the remaining 207 top-level doc tables are shared `Tables`/`Predicates` files with
no `Environment` field). The other is `PingManagerSecure` / `C_PingSecure`
*[T1 docs: `grep -rh 'Environment ='` returns 383 × `"All"` and 2 ×
`"SecureOnly"`; `CombatLogSecureDocumentation.lua:6`,
`PingManagerSecureDocumentation.lua:6`]*.

The addon-facing `C_CombatLog` namespace that remains is filter/retention
plumbing only: `ApplyFilterSettings`, `AreFilteredEventsEnabled`, `ClearEntries`,
`DoesObjectMatchFilter`, `GetEntryRetentionTime`, `GetMessageLimit`,
`IsCombatLogRestricted`, `RefilterEntries`, `SetEntryRetentionTime`,
`SetFilteredEventsEnabled`, `SetMessageLimit` *[T1 docs:
`CombatLogDocumentation.lua`, 11 functions]*. Notably **`C_CombatLog.GetCurrentEventInfo`
is not among them**, even though the deprecation shim still assigns
`CombatLogGetCurrentEventInfo = C_CombatLog.GetCurrentEventInfo` *[T1 src:
`Blizzard_DeprecatedCombatLog/Deprecated_CombatLog.lua:18`, itself gated on
`GetCVarBool("loadDeprecationFallbacks")` at `:4`]*.

The shim file **explains itself**, and it is worth reading before assuming a
mystery: its header comment says *"Some functions have been relocated to the
secure environment, for which no deprecation is (intentionally) provided."*
*[T1 src: same file, `:10-11`]*. Six of the `C_CombatLog.*` names it assigns —
`AddEventFilter`, `ClearEventFilters`, `GetCurrentEntryInfo`,
**`GetCurrentEventInfo`**, `GetEntryCount`, `ShouldShowCurrentEntry` — are absent
from the documented `C_CombatLog` surface and **present on `C_CombatLogSecure`**
*[T1 docs: `CombatLogSecureDocumentation.lua:11, :16, :36, :45, :54, :102`]*, the
`Environment = "SecureOnly"` table below. **Measured: all six read `nil` on
`C_CombatLog` from addon code** `[client 2026-07-24]`. So `Environment = "SecureOnly"`
is enforced exactly the way the read predicted — by not binding the name in our
environment at all, rather than by a call-time refusal. The deprecation shim's
`CombatLogGetCurrentEventInfo = C_CombatLog.GetCurrentEventInfo` therefore assigns
`nil` for us even with `loadDeprecationFallbacks` on.

Several addons on this install still contain `RegisterEvent("COMBAT_LOG_EVENT_UNFILTERED")`
without a flavour guard — e.g. `TellMeWhen` 12.0.13,
`Components/IconTypes/IconType_cleu/cleu.lua:582-583` *[T1 obs]*. That is
evidence the code is still shipped, **not** evidence that it works.

### 2.7 `EventRegistry` and `CallbackRegistryMixin` — the in-process bus

Separate from game events, Blizzard runs a Lua-level pub/sub layer. `EventRegistry`
is a global instance of `CallbackRegistryMixin` *[T1 src:
`Blizzard_SharedXMLBase/GlobalCallbackRegistry.lua:1`]*, with
`SetUndefinedEventsAllowed(true)` so arbitrary string keys are legal *[T1 src:
same file, `:5`]*.

Properties worth knowing, all Tier 1 from
`Blizzard_SharedXMLBase/CallbackRegistry.lua`:

- **One callback per (event, owner).** `RegisterCallback` unconditionally calls
  `self:UnregisterCallback(event, owner)` before inserting, with the comment
  *"An owner can have a single callback per event"* (`:128-130`). Registering
  twice with the same owner silently replaces.
- **Omitting `owner` allocates an anonymous one** from a counter, and the comment
  says that is *"fine when you never intend to release the callback"* (`:17-19`,
  `:118-119`). A `number` owner is reserved and raises an error (`:120-121`).
- **`RegisterCallbackWithHandle` returns `{Unregister = …}`** — the releasable
  form (`:155-158`).
- **`TriggerEvent` is reentrancy-safe.** Registrations made *during* a dispatch
  go to a deferred table and are merged in afterwards (`:87-94`, `:160-182`,
  `:184-223`). The comment at `:191` reads *"TriggerEvent appears to need to
  support reentrant calls for now."*
- **Bridging to game events is refcounted through frame attributes.**
  `EventRegistry:RegisterFrameEvent` reads a count off `frameEventFrame:GetAttribute(frameEvent)`,
  calls `RegisterEvent` only when it is 0, and increments *[T1 src:
  `GlobalCallbackRegistry.lua:13-21`]*; `UnregisterFrameEvent` mirrors it
  (`:23-31`). ⚠ **Do not read that attribute store as a taint barrier** — nothing in
  `GlobalCallbackRegistry.lua` says it is one, and the code is a plain refcount that
  happens to live in a frame attribute, uncommented. The genuine taint-barrier
  mechanism is elsewhere: `CallbackRegistry.lua`'s `SecureInsertEvent`, comment at
  `:125`, delegate frame at `:21-26`.

`EventUtil` layers the one-shot helpers on top: `ContinueOnAddOnLoaded`,
`ContinueOnPlayerLogin`, `ContinueAfterAllEvents`, and the generic
`RegisterOnceFrameEventAndCallback(frameEvent, callback, ...)` which additionally
filters on required payload prefix arguments before firing and unregistering
*[T1 src: `Blizzard_SharedXML/EventUtil.lua:38-106`]*. Each of the `ContinueOn*`
helpers checks the already-happened case first and calls back synchronously
(`:72-79`, `:81-88`) — the pattern that avoids the classic "my addon loaded after
`PLAYER_LOGIN` and never initialised" bug.

Ace3's equivalent, for comparison: `AceEvent-3.0` funnels **every** consumer
through a **single shared frame** named `AceEvent30Frame`, registering the
underlying game event lazily on `OnUsed` and unregistering on `OnUnused`
*[T3: Ace3 @ `4475787f06f7`, `AceEvent-3.0/AceEvent-3.0.lua:23, :32-37`]*.

### 2.8 A fourth dispatch shape: a choke-point method used as an alert channel

`EventRegistry` (§2.7) is not the only in-process bus Blizzard ships. A subsystem can also
publish through **a plain mixin method that exists to be called at a choke point** — no game
event, no `EventRegistry` callback, no registration anywhere, just the one function every
signal in that subsystem flows through. The worked instance is the Cooldown Manager's
`CooldownViewerItemMixin:TriggerAlertEvent(event)`
*[T1 src: `Blizzard_CooldownViewer/CooldownViewer.lua:483-493`]*, whose body only walks
`self.alertsByEvent[event]` to play a configured sound or visual — so it *does nothing* when
the player has configured no alert, and is still **called**, which is what makes it hookable.

That is the generalisable point: **a choke-point method is a dispatch shape, and
`hooksecurefunc` on it is a supported way to observe a subsystem** (§5.4 treats
`hooksecurefunc` as a discovery instrument; this is the same tool used as a runtime signal).
A post-hook fires regardless of what the original did, so an addon sees every signal even
when Blizzard's own handler early-outs. Two conditions make or break it:

- **Hook the instance, not the mixin table**, when the methods were `Mixin()`-copied onto
  each object — a hook on the shared table is not what the object will call.
- **Readable is not the same as useful.** The same subsystem's `item:IsActive()` stays
  readable in restricted combat and is a **constant `true`** on one of its two families —
  no `nil`, no error, nothing to distinguish it from a real signal.

The Cooldown Manager's own six alert types, what each edge actually means, and what the
channel does and does not survive under Secret Values are
[`cooldown-manager`](./cooldown-manager.md) §5.

---

## 3. `OnUpdate`, timers and dirty flags

### 3.1 The `OnUpdate` contract

`(self, elapsed)`, where `elapsed` is seconds since the previous dispatch
*[T2 wiki: `UIHANDLER_OnUpdate`, revid 3167340, 2023-08-18]* — an **old** page:
its "excluding time when the UI was not being drawn" clause carries the wiki's
own `{{fact}}` tag, i.e. the wiki does not vouch for it]*. Blizzard's helper uses
exactly that signature *[T1 src: `Blizzard_SharedXMLBase/FrameUtil.lua:17`]*.

**`OnUpdate` is blocked by hiding the frame *or* its parent, and resumes on re-show**
`[client 2026-08-05]`. A child frame ticking across four half-second phases counted 39
ticks while shown, **0** while self-hidden, **0** while its (shown) self sat under a hidden
parent, and 61 once re-shown — with `IsVisible()` reading `true/false/false/true` across
the same phases. So visibility, not merely `IsShown()`, is the gate, and a hidden subtree
costs nothing. This confirms the wiki *[T2 wiki: same page]* and explains oUF's independent
`self:IsVisible()` guard *[T3: oUF `events.lua:72`]*.

**A Tier-1 hazard worth internalising:** clearing an `OnUpdate` script does not
guarantee the handler will not run again on the same frame. Blizzard's own helper
carries a boolean specifically for it:

```lua
function FrameUtil.RegisterUpdateFunction(frame, frequencySeconds, func)
    -- Prevents the OnUpdate handler from running the same frame it was
    -- removed.
    frame.canUpdate = true;
    ...
```
*[T1 src: `Blizzard_SharedXMLBase/FrameUtil.lua:11-31`; `UnregisterUpdateFunction`
sets `canUpdate = false` **and** clears the script, `:28-31`]*

That same function is Blizzard's own throttled-`OnUpdate` reference
implementation — decrement a countdown by `dt`, reset and fire when it crosses
zero.

### 3.2 `C_Timer`

Three documented functions *[T1 docs: `UITimerDocumentation.lua:11, :22, :39`]*:

```
C_Timer.After(seconds: number, callback: TimerCallback)
C_Timer.NewTicker(seconds: number, callback: TickerCallback, iterations: number?) -> cbObject
C_Timer.NewTimer(seconds: number, callback: TickerCallback) -> cbObject
```

`NewTicker`/`NewTimer` return an object; Blizzard calls `:Cancel()` on it
*[T1 src: `Blizzard_SharedXMLBase/ObjectUpdater.lua:11, :27`;
`Blizzard_SharedXMLBase/TimedCallback.lua:7-12, :20`]*. `C_Timer.After` returns
nothing and is therefore **not cancellable** *[T1 docs:
`UITimerDocumentation.lua:11-20`, no `Returns` block]*.

`RunNextFrame(callback)` is literally `C_Timer.After(0, callback)` *[T1 src:
`Blizzard_SharedXMLBase/FunctionUtil.lua:126-128`]*, and *"With a duration of
0 ms, the earliest the callback will be called is on the next frame"*
*[T2 wiki: `API C_Timer.After`, revid 6592061, 2026-01-04]*.

**When a ticker is the wrong tool** — the only substantive statement I could find
is a Blizzard blue post the wiki archives verbatim:

> *"In most cases, initiating a second C_Timer is still going to be cheaper than
> using an Animation or OnUpdate. … The one case where you're better off not
> using the new C_Timer system is when you have a ticker with a very short period
> – something that's going to fire every couple frames. For example, you have a
> ticker you want to fire every 0.05 seconds; you're going to be best served by
> using an OnUpdate function."*
>
> — Rygarius, "[Sticky] 6.0 Add-On Changes", 2014-09-09, quoted at
> *[T2 wiki: `API C_Timer.After`, revid 6592061, §Details]*

That is Tier-1 *content* through a Tier-2 channel, but it is **twelve years old
and describes the 6.0 implementation**. Do not present it as current guidance
about Midnight; present it as the only articulated rationale anyone has, and
measure with `C_AddOnProfiler` (§5.1) instead.

Blizzard's own usage census across the 2298 shipped `.lua` and 1028 `.xml` files:
**382** `SetScript("OnUpdate"` calls, **259** XML `<OnUpdate>` *elements*
(there are **0** `OnUpdate=` attributes — it is markup, not an attribute), **125**
`C_Timer.After`, **46** `C_Timer.NewTicker`, **29** `RunNextFrame` (one of which
is the definition itself) *[T1 src: `grep -rho` counts over
`Interface/AddOns/`]*. Blizzard has not abandoned `OnUpdate`.

### 3.3 The dirty-flag idiom, as Blizzard writes it

`BaseLayoutMixin` in `Blizzard_SharedXML/LayoutFrame.lua` is the reference
implementation. The whole pattern is 40 lines:

```lua
function BaseLayoutMixin:OnUpdate()                       -- :78
    if self:IsDirty() then
        self:Layout();
    end
end

function BaseLayoutMixin:MarkDirty()                      -- :84
    self.dirty = true;

    -- To optimize performance, only set OnUpdate while marked dirty.
    self:SetScript("OnUpdate", self.OnUpdate);

    -- Tell any ancestors who may also be LayoutFrames that they should also become dirty
    local parent = self:GetParent();
    while parent do
        if IsLayoutFrame(parent) then
            parent:MarkDirty();
            return;
        end
        parent = parent:GetParent();
    end
end

function BaseLayoutMixin:ShouldClearOnUpdateAfterClean()  -- :102
    return self:IsDirty() and (self.OnUpdate == BaseLayoutMixin.OnUpdate);
end

function BaseLayoutMixin:MarkClean()                      -- :106
    local canClearScript = self:ShouldClearOnUpdateAfterClean();
    self.dirty = false;
    self:OnCleaned();
    -- The OnUpdate script is only cleared if it was assigned the original update function in MarkDirty.
    -- If this script is overridden, its the override's responsibility to call the original OnUpdate function.
    if canClearScript then
        self:SetScript("OnUpdate", nil);
    end
end
```
*[T1 src: `Blizzard_SharedXML/LayoutFrame.lua:78-121`, verbatim except for the
elided `IsDirty`/`OnCleaned` accessors at `:119-125`; `IsLayoutFrame` is the file
local at `:6`]*

Five properties fall out of that, and they are the reusable part:

1. **The `OnUpdate` script exists only while work is pending.** It is installed by
   `MarkDirty` and removed by `MarkClean`. A frame with nothing to do costs
   nothing per frame.
2. **Marking is idempotent.** N marks between two frames produce one `Layout()`.
   That is the coalescing.
3. **Dirtiness propagates up**, and the walk *returns* at the first
   layout-frame ancestor rather than continuing — the ancestor's own `MarkDirty`
   continues the chain.
4. **Removal is conditional on ownership.** `ShouldClearOnUpdateAfterClean`
   compares `self.OnUpdate` — the mixin *method*, not the installed script —
   against `BaseLayoutMixin.OnUpdate` by identity (`:103`). A subclass that
   overrode the `OnUpdate` **method** keeps its script, and inherits the
   documented obligation to call the base one. (A subclass that left the method
   alone but called `SetScript("OnUpdate", …)` itself is *not* detected by this
   check — the code reads the method table, not `GetScript`.)
5. **Cleaning is the layout's job, not the tick's** — *usually*. Three of the
   four concrete `Layout()` implementations end with `self:MarkClean()`
   *[T1 src: same file, `LayoutMixin:Layout` `:253-267` → `:266`;
   `ResizeLayoutMixin:Layout` `:486-531` → `:530`;
   `StaticGridLayoutFrameMixin:Layout` `:630-723` → `:722`]*. The fourth,
   **`GridLayoutFrameMixin:Layout` (`:539-571`), does not**: it delegates to
   `ResizeLayoutMixin.Layout(self)` at `:569` (which cleans), but its early
   `return` at `:542` — taken whenever `ShouldUpdateLayout` is false, e.g. the
   frame is hidden (`:586-588`) — exits with the frame still dirty. So Blizzard's
   own tree contains a counterexample to the "always MarkClean" rule; see
   §"Rules we could audit against" #14.

The file also ships a variant, `OverrideLayoutFrameOnUpdateMixin`, for frames
that need a per-frame tick *in addition to* layout: it registers `OnUpdate` when
`self.dirty or self:NeedsOnUpdate()` and re-evaluates that after every tick
*[T1 src: same file, `:743-767`]*.

`ObjectUpdater` is the other Blizzard scheduling primitive — a small state
machine (`Ready/Begin/Update/End`) driven by `C_Timer.NewTicker(0.01, …)` that
calls a work function until an `isComplete` predicate returns true, then cancels
itself *[T1 src: `Blizzard_SharedXMLBase/ObjectUpdater.lua:1-58`]*. Use it as the
model for chunking a long job across frames.

### 3.4 Debouncing at the event layer

`AceBucket-3.0` is the ecosystem's answer to burst events. Its own header
describes the algorithm exactly:

> *"Initially, no schedule is running, and its waiting for the first event to
> happen. The first event will start the bucket, and get the scheduler running,
> which will collect all events in the given interval. When that interval is
> reached, the bucket is pushed to the callback and a new schedule is started.
> When a bucket is empty after its interval, the scheduler is stopped."*
>
> *[T3: Ace3 @ `4475787f06f7`, `AceBucket-3.0/AceBucket-3.0.lua:4-9`]*

It also aggregates `arg1` into a `{[unit] = count}` table, *"mostly designed for
the `UNIT_*` events"* *[T3: same file, `:11-14`]*. That is leading-edge-start,
trailing-edge-flush debouncing with argument coalescing — worth knowing as a
shape even if you do not take the dependency.

---

## 4. The API surface and its vocabulary

### 4.0 ⚠ Kstrings (`|K…|k`) — opaque server strings, and NOT secret values

Chat, LFG and Club payloads can carry server-resolved opaque strings encoded as a
`|K…|k` escape sequence. The generated docs declare them as first-class types —
`kstringLfgListChat`, `kstringLfgListApplicant`, `kstringLfgListSearch`
(`LFGListInfoDocumentation.lua:692, 845, 871-873, 912`) and `kstringClubMessage`
(`ClubDocumentation.lua:1846`); `ClubDocumentation.lua:1800` states outright that a
name *"may be encoded as a Kstring"*. Blizzard's own chat code branches on the
two-character prefix (`Blizzard_ChatFrameBase/Mainline/FloatingChatFrame.lua:2455`,
`strsub(playerTarget, 1, 2) ~= "|K"`).

**Stripping the sequence with a `gsub` destroys the value rather than sanitising it.**

⚠⚠ **Document them as a SEPARATE mechanism, and resist the obvious conflation.**
Kstrings **predate Midnight** and have nothing to do with Secret Values — but the
failure mode looks identical (a name renders empty or garbled), so a reader who has
just learned §4 of the security file will diagnose it wrong and reach for
`issecretvalue`, which answers `false`. A shipping addon's own source comment calls
them "secret value placeholders"; that is exactly the mistake to avoid.
*[T1: the doc types + Blizzard's own branch, above. Surfaced by an addon-mining run;
the addon adds nothing the Tier-1 sources do not already carry, so cite Blizzard.]*

### 4.1 Shape

At 12.1.0.69273 the generated documentation declares **6335 functions**, split
**4202 namespaced** (`C_Something.Function`) · **695 globals** · **1438 widget
methods**; plus **844 enumerations**, **752 structures + 20 `CallbackType`s**,
**60 constants** and **57 predicate declarations** *[T1 docs @12.1.0: whole-corpus
re-parse of all 612 `.lua` files. The same parse reproduces 12.0.7.68887's
6144 = 4068 + 692 + 1384 exactly]*.

⚠ **`wowkb.uiapi stats` still reports the 12.0.7 numbers.** Its index is built from
`raw/addon-research/wow-ui-source`, which is deliberately still at 12.0.7.68887 so
that this subtree's several hundred unstamped `file:line` citations keep resolving;
the 12.1.0 tree sits beside it as `wow-ui-source-12.1.0`. If the two disagree, the
counts above are the current ones.

Two counting caveats, because `wowkb.uiapi stats` prints rounder numbers than
the corpus actually contains:

- its **`structs 735`** is `Type = "Structure"` (715) **plus** `Type =
  "CallbackType"` (20) in one bucket. The `CallbackType`s are the opaque
  callback handles of §2.5 — not structures, and worth keeping separate.
- its **`predicates`** figure is *all* predicate declarations, not secret ones: of
  the 57, **22** are `Type = "Secret"` and **35** are `Type = "Precondition"`
  (`RequiresValidActionSlot`, `RequiresComparableUnitTokens`, …). Reading the total
  as "secret predicates" overstates the secrecy vocabulary by 2.6×.

*[T1 docs @12.1.0: `grep -rho 'Type = "Structure"' | wc -l` = 752, `…"CallbackType"` = 20;
predicate types counted by re-parse.]*

The 4202 namespaced functions live in
**239 distinct namespaces, every one of which begins with `C_`** *[T1 docs: same
index]*. The largest are `C_Commentator` (144), `C_Item` (117), `C_PvP` (107),
`C_Calendar` (90), `C_QuestLog` (90), `C_TradeSkillUI` (88), `C_AuctionHouse`
(85), `C_Club` (83), `C_TransmogCollection` (83), `C_TooltipInfo` (82).

**Only 839 of the 6335 function entries carry any prose at all** *[T1 docs @12.1.0: same
index]*. The spec is a shape declaration, not a manual.

Widget methods are declared on **79 `ScriptObject` tables** — the two added at
12.1.0 are `SimpleVectorGraphicsAPI` (the SVG object type) and
`SimpleAnimRadialProgressAPI` (a new `Animation` subtype); see
`frames-textures-animation` §1.1 *[T1 docs @12.1.0]* and — critically —
**the docs express no inheritance between them**. Each table is a flat
`{Name = …, Type = "ScriptObject", Environment = …, Functions = {...}}` with no
parent field *[T1 docs: `SimpleFrameAPIDocumentation.lua:1-6` and
`SimpleScriptRegionAPIDocumentation.lua:1-6`, structurally identical headers]*.
So `SetScript` **is not declared on `SimpleFrameAPI` at all**, even though every
frame has it. Where it *is* declared shows the generator's actual habit —
duplication, not inheritance: `SetScript` appears on **three** ScriptObject
tables, `SimpleScriptRegionAPI` (`:628`), `SimpleAnimAPI` (`:343`) and
`SimpleAnimGroupAPI` (`:318`), with `GetScript` / `HasScript` / `HookScript`
repeated across the same three *[T1 docs: `grep -rn 'Name = "SetScript"'` returns
exactly those three hits]*. **You cannot derive "does a Frame have method X" from
the generated docs alone.** The hierarchy has to come
from `[T2 wiki: Widget API]` or `[T2 res: Resources/WidgetHierarchy.png,
Resources/ScriptObjectAPI.lua]`.

### 4.2 The core vocabulary: units, GUIDs, spell identifiers

Three type names carry most of the API's meaning, and **none of them is defined
in the generated docs**:

| Type name | Uses in the corpus | Declared? |
|---|---|---|
| `WOWGUID` | 391 | no |
| `UnitToken` | 264 | no |
| `UnitTokenVariant` | 100 | no |
| `SpellIdentifier` | 74 | no |
| `UnitTokenPvPRestrictedForAddOns` | 28 | no |
| `AuraData` | 10 | no |

*[T1 docs @12.1.0: `grep 'Type = "<name>"'` counts vs `grep 'Name = "<name>",'`
declarations across all 612 doc files — every one of these appears only as a
parameter/return/`InnerType` type, never as a `Tables` entry; the declaration grep
returns empty for all six.]*

⚠ **`AuraData` is the one on this list where "undeclared" is now the *least*
important thing about it.** At 12.1.0 `AuraData` structs are **always fully secret**
*[T2 wiki: Patch 12.1.0/API changes, the 2026-06-30 and 2026-07-07 entries,
revid 6801760, 2026-08-09 — "AuraData structs are now always fully secret"]*, and the 16
`C_UnitAuras` functions that return one all carry `RequiresUnitAuraAccess`, which
**errors** from addon code while auras are secret. So the shape you cannot cite from
Tier 1 is also a shape you cannot read at runtime. See
`security-taint-and-restricted-data` §4.7 and §3.5.

The one that *is* declared is `UnitTokenType`, an `Enumeration` with
`NumValues = 362, MinValue = 0, MaxValue = 361`, members `None=0, Player=1,
Pet=2, Vehicle=3, Mouseover=4, Target=5, TargetTarget=6, SoftEnemy=7,
SoftFriend=8, SoftInteract=9, Focus=10, FocusTarget=11, AnyTarget=12, …
Raid1=19 …` *[T1 docs: `UnitSharedDocumentation.lua:6-45`]*. That is the closest
thing to a canonical unit-token list Tier 1 offers.

The *distinct* unit-token type names in signatures are load-bearing, not
cosmetic: `UnitGUID(unit: UnitTokenPvPRestrictedForAddOns)` carries
`SecretWhenUnitIdentityRestricted = true`, `UnitIsUnit(unit1: UnitToken, unit2:
UnitToken)` carries `RequiresComparableUnitTokens` +
`SecretWhenUnitComparisonRestricted`, and `UnitExists(unit: UnitToken?)` carries
neither *[T1 docs: `UnitDocumentation.lua:1209, :2290, :1160`]*. The parameter
type name tells you which restriction family applies. See
`security-taint-and-restricted-data` for what the predicates mean.

`SpellIdentifier` is the wildcard: *"a Spell ID, name, name(subtext), or link"*,
and *"when passing a localized name it requires the spell to be in your
spellbook"* *[T2 wiki: `API types/SpellIdentifier`, revid 6776503, 2026-07-20]*.
The wiki page enumerates ~70 consumers. Prefer numeric IDs — they are
locale-independent and do not depend on spellbook state.

### 4.3 What the generated docs will not tell you

- **No error semantics.** `HasRestrictions` (**266** functions — **273** annotations
  total, 7 of them on events) and `MayReturnNothing` (**612**) say *that* something
  can fail, never *what* you get *[T1 docs @12.1.0]*.
- **Partial global coverage.** `hooksecurefunc`, `issecure`, `issecurevariable`
  and `securecall` are absent, as is the global `CreateFrame` — note that a
  *different*, same-named `CreateFrame` **is** documented, on the SecureOnly
  `C_PingSecure` namespace (`PingManagerSecureDocumentation.lua:16`), so a bare
  name grep will mislead you. `wowkb.uiapi missing <name>` distinguishes "absent
  from docs" from "absent from the game".
  ⚠ **`scrub` is *not* absent**, despite belonging to the same family — it is
  documented at `FrameScriptDocumentation.lua:348-362`, with prose and a
  `SecureHooksAllowed = false` flag.
- **Named types that are never declared.** Named types like `AuraData` (10 uses, 0
  declarations) resolve to nothing — see the table in §4.2, and note that `AuraData`
  is additionally always-fully-secret at 12.1.0.
  ⚠ The "716 bare `table` parameters/returns" figure was measured at 12.0.7.68887 and
  **was not re-derived** for 12.1.0; treat it as approximate and rising.
- **`Enum.ScriptBindingType` does not exist in Tier 1.** The wiki's `HookScript`
  page names it *[T2 wiki: `API ScriptRegion HookScript`, revid 6779372, 2026-07-23
  — it types `bindingType` as `Enum.ScriptBindingType?` and transcludes
  an `Enum.ScriptBindingType` page]*, but `grep -r ScriptBinding` over all 592
  generated doc files returns nothing, and the docs type the parameter as a bare
  `number` *[T1 docs: `SimpleScriptRegionAPIDocumentation.lua:325-335`]*. What does exist is the
  legacy global set `LE_SCRIPT_BINDING_TYPE_INTRINSIC_PRECALL = 0`,
  `LE_SCRIPT_BINDING_TYPE_EXTRINSIC = 1`,
  `LE_SCRIPT_BINDING_TYPE_INTRINSIC_POSTCALL = 2`, `NUM_LE_SCRIPT_BINDING_TYPES = 2`
  *[T2 res: `Resources/LuaEnum.lua:9251-9254`]* — and note that those four values
  are internally inconsistent (3 named values, `NUM_… = 2`).

---

## 5. Discovery — how to find things

This is the part that stays true after the API numbers change.

### 5.1 In the client

| Command | What it gives you | Evidence |
|---|---|---|
| `/api` | The full generated API spec, searchable. `/api search <name>`, `/api system list`, `/api <system> list`, `/api <system> search <name>`. **"All searches support Lua patterns."** | *[T1 src: `Blizzard_APIDocumentation/Blizzard_APIDocumentation.lua:116-142`; slash string `SLASH_API1 = "/api"` at T2 res `Resources/GlobalStrings/enUS.lua:18044`; wired at T1 src `Blizzard_ChatFrameBase/Shared/SlashCommands.lua:1420-1423`]* |
| `/eventtrace`, `/etrace` | Live event log with payloads, timestamps, filters, search, pause, and a **secret-value toggle**. Carries a *render-frame* counter (not a per-widget-frame counter) used to print "(Δseconds, Δframes)" between events. Also logs `EventRegistry` callback traffic. | *[T1 src: `Blizzard_EventTrace/Blizzard_EventTrace.lua:988-993`; `RegisterAllEvents()` at `:107`; `hooksecurefunc(EventRegistry, "TriggerEvent", …)` at `:113-115`; secret toggle at `:887-891`; frame counter at `:96`, `:674`, `:714-716`; strings at T2 res `enUS.lua:18406-18409`]* |
| `/dump`, `/tinspect` (`/tableinspect`), `/fstack` (`/framestack`), `/run` (`/script`), `/reload`, `/console` | Value dump, interactive table inspector, frame-under-cursor stack, one-liner execution. | *[T2 res: `enUS.lua:18377, 18759-18762, 18419-18422, 18701-18704, 18679, 18353`; wired at T1 src `Blizzard_ChatFrameBase/Shared/SlashCommands.lua:1329, :1359-1367` and `Blizzard_ChatFrameBase/Mainline/SlashCommandsOverrides.lua:171`]* |

Both `/api` and `/eventtrace` back onto `LoadOnDemand: 1` addons
(`Blizzard_APIDocumentation`, `Blizzard_EventTrace`), so they cost nothing until
invoked *[T1 src: the two `.toc` files]*.

⚠ `/dump` and `/tinspect` are **not unconditionally available**: **both** bail out
if Kiosk mode is enabled, if `C_AddOns.GetScriptsDisallowedForBeta()`, or if the
`Enum.GameRule.UserScriptsDisabled` game rule is active, and **both** then gate on
`AreDangerousScriptsAllowed()` behind a `DANGEROUS_SCRIPTS_WARNING` popup
*[T1 src: `Blizzard_ChatFrameBase/Shared/SlashCommands.lua:1329-1337` (tinspect,
kiosk check `:1330-1333`, dangerous-scripts check `:1334-1337`) and `:1359-1367`
(dump)]*. `/fstack` has neither gate *[T1 src:
`Blizzard_ChatFrameBase/Mainline/SlashCommandsOverrides.lua:171-173`]*.
"It didn't print anything" is not the same as "the value is nil".

**Two CVars belong on this list**, because they turn tooltips and the taint log into
discovery instruments, and both are new at 12.1.0 *[T2 wiki: Patch 12.1.0/API changes
§CVars/Added and the 2026-07-21 entry, revid 6801760, 2026-08-09]*:

| CVar | Default | What it gives you |
|---|---|---|
| `tooltipShowAuraSpellIDs` | `0` | *"Show spell IDs in tooltips for unit auras."* ⚠ **Does not persist between sessions** — Blizzard says so explicitly, so `/console` it each login. This is the discovery route that *replaces* reading spell IDs out of aura data, which 12.1.0 closed (`security-taint-and-restricted-data` §4.7); mousing over the aura is now the cheap way to learn an ID. |
| `taintLogObjectSecrets` | `0` | *"include additional taint log entries when script objects gain secret aspects or values."* The "when did this frame become secret" instrument; `security` §2.3. |

`C_CVar.AreCVarsLoaded()` is the matching load-lifecycle probe, also new
*[T1 docs @12.1.0: `CVarDocumentation.lua:11-18`]* — the CVar analogue of gating on
`ADDON_LOADED` before reading SavedVariables.

For measuring rather than exploring, `C_AddOnProfiler` exposes 10 functions and
the `AddOnProfilerMetric` enum: `SessionAverageTime`, `RecentAverageTime`,
`EncounterAverageTime`, `LastTime`, `PeakTime`, and bucket counters
`CountTimeOver1Ms` … `CountTimeOver1000Ms` *[T1 docs:
`AddOnProfilerDocumentation.lua`, `AddOnProfilerConstantsDocumentation.lua:19`]*.
`C_AddOnProfiler.GetTopKAddOnsForMetric(metric, k)` and
`C_AddOnProfiler.MeasureCall(func, args)` are the interesting two.

There is also an *event*-level profiler pair — `GetCurrentEventID()` and
`GetEventTime(eventProfileIndex) -> totalElapsedTime, numExecutedHandlers,
slowestHandlerName, slowestHandlerTime` *[T1 docs:
`FrameScriptDocumentation.lua:163, :181`]*. **Neither is called anywhere in the
2298 shipped `.lua` files** *[T1 src: grep returns zero non-documentation hits]*,
so the shipped source carries no worked example of how to obtain a valid
`eventProfileIndex`.
**Both exist as functions, and both return nothing useful when called from outside
an event handler**: `GetCurrentEventID()` returns `nil`, and `GetEventTime(0)`
likewise `[client 2026-07-24]`. Neither errors — they simply have no answer there.
That leaves the pair usable only from *inside* a handler, and still with no worked
example of obtaining a valid index; assume it needs a profiling CVar we have not
identified. Do not build on this pair.

### 5.2 Off the client

The ordering that works:

1. **`wowkb.uiapi`** over the local `wow-ui-source` checkout — the Tier-1 spec,
   already indexed, output already in `file:line` form. `func`, `event`,
   `system`, `widget`, `enum`, `struct`, `secure`, `predicates`, `grep`,
   and `missing <name>` (the honesty guard: *docs / source / neither*).
2. **Grep the shipped source for a call site.** A signature tells you the shape;
   Blizzard's own use tells you the idiom. Almost every non-obvious thing in this
   file was settled that way.
3. **`wowkb.wiki`** for semantics Tier 1 omits — return-value meanings, error
   conditions, patch history. Always carry the printed `lastedit` into the claim.
4. **`townlong-yak.com/framexml/<build>/<AddOn>/<File.lua>`** when the question is
   *"what changed between builds"* — it has per-file compare links our single
   `--depth 1` checkout cannot give.
5. **`[T2 res] BlizzardInterfaceResources`** for flat enumerations: every global
   frame name, template, atlas, CVar, GlobalString, and the 1741-entry
   `Resources/Events.lua`.

### 5.3 The wiki's one irreplaceable asset

Blizzard's technical addon-developer communication happens on the **WoWUIDev
Discord**, which is not publicly fetchable *[see `sources.md` §6]*. The
`Patch <ver>/API changes` pages archive those posts verbatim, and additionally
carry the consolidated added/removed lists that tell you *when* a name appeared.
That is how §2.5's "these seven names are new in 12.0.0" was established.
`uv run python -m wowkb.wiki changes 12.0.0 12.0.5 12.0.7`.

### 5.4 `hooksecurefunc` as a discovery instrument

It is the sanctioned post-hook: *"The hook will be called with the same arguments
after the original call is performed"*, *"return values from hookfunc are
discarded"*, and *"You cannot 'unhook' a function … except by a UI reload"*
*[T2 wiki: `API hooksecurefunc`, revid 6588971, 2026-01-03]*. Blizzard uses it in
its own code, including on `EventRegistry:TriggerEvent` to make Event Trace see
callback traffic *[T1 src: `Blizzard_EventTrace/Blizzard_EventTrace.lua:113-115`]*
— which is the single best demonstration of hooking-as-instrumentation in the
shipped tree.

Two hard limits, from different tiers:

- *[T2 wiki, attributed to 11.0.0]* — 23 named functions cannot be hooked at all
  (`getfenv`, `getmetatable`, `hooksecurefunc`, `ipairs`, `issecurevalue`,
  `issecurevariable`, `next`, `rawget`, `rawset`, `pairs`, `pcall`,
  `pcallwithenv`, `scrub`, `securecall`, `securecallfunction`,
  `secureexecuterange`, `select`, `setfenv`, `setmetatable`, `type`, `unpack`,
  `wipe`, `xpcall`); the attempt raises *"Cannot hook function"*.
- *[T1 docs]* — **exactly 24 documented functions carry `SecureHooksAllowed =
  false`, and zero carry `= true`**: `CheckAllowProtectedFunctions`,
  `CreateFromMixins`, `CreateSecureDelegate`, `Mixin`, `RegisterEventCallback`,
  `RegisterUnitEventCallback`, `SetTableSecurityOption`,
  `UnregisterEventCallback`, `UnregisterUnitEventCallback`, `canaccessallvalues`,
  `canaccesssecrets`, `canaccesstable`, `canaccessvalue`, `dropsecretaccess`,
  `dumpobject`, `hasanysecretvalues`, `issecrettable`, `issecretvalue`,
  `mapvalues`, `scrub`, `scrubsecretvalues`, `secretunwrap`, `secretwrap`,
  `securecallmethod` *[T1 docs: `grep -rh 'SecureHooksAllowed = false' | wc -l` =
  24, `… = true` = 0, over all 592 doc files; names re-extracted this session]*.
  Note the two lists overlap only on `scrub`.
  ✅ **What the annotation means is now measured: `SecureHooksAllowed = false`
  means `hooksecurefunc` refuses the function.** Hooking `CreateFromMixins` — which
  carries the flag and is *not* on the wiki's list — fails, and the error names both
  the caller and the target:
  `hooksecurefunc(): CreateFromMixins is forbidden for hooking` `[client 2026-07-24]`.
  Two things follow. First, the annotation is enforced, not merely descriptive, so
  **treat all 24 as unhookable**. Second, the refusal message is **distinct from the
  wiki's *"Cannot hook function"*** for the 23-name list, which suggests two separate
  engine checks rather than one — consistent with the lists overlapping on only
  `scrub`. The union, not either list alone, is what an addon must avoid.

For script handlers the analogue is `HookScript`, which *"If the script type
doesn't have an existing handler … will be equivalent to `SetScript`"*, whose
hooks *"remain in place until replaced or cleared with SetScript"*, and which can
be applied repeatedly *"until a stack overflow occurs after too many hooks"*
*[T2 wiki: `API ScriptRegion HookScript`, revid 6779372, 2026-07-23]*.

Taint consequences of all of this: `security-taint-and-restricted-data`.

### 5.5 When the runtime API will not answer: DB2 via wago.tools

Some questions are about *game data*, not the API — "what is the spell ID for X",
"what rows exist in this table", "which build introduced this". The client does
not expose the client database tables to Lua; `wago.tools` mirrors them.

- `https://wago.tools/api/builds` → per-product build list, newest first. Compare it
  against `version.txt` in the source checkout you are citing — a mismatch is the
  cheapest possible staleness check on your own tooling.
- `https://wago.tools/db2/<Table>/csv?build=<version>` → the table as CSV. Wrapped
  as `uv run python -m wowkb.wago <Db2Table> [--build …]` *[repo tool:
  `tools/wowkb/wago.py:25-36` (the `download()` helper)]*.

Pin the `--build` when you want a reproducible citation; the default is "latest",
which moves.

Also useful for template discovery *inside* the client:
`C_XMLUtil.GetTemplateInfo(name)` *[T1 docs: `XMLUtilDocumentation.lua:11-25`]* and
`C_XMLUtil.GetTemplates()` *[T1 docs: same file, `:27-34`]*. Blizzard uses the
former to resolve a template's frame type
*[T1 src: `Blizzard_SharedXMLBase/FrameUtil.lua:155-160`]*.

### 5.6 Free staleness detectors

Down-tier any source on sight if it:

- tells you to look in `Interface/FrameXML/` or `Interface/SharedXML/` as
  top-level directories — those have not existed since the Midnight layout
  *[see `sources.md` §1.1]*;
- describes reading the combat log by registering `COMBAT_LOG_EVENT_UNFILTERED`
  on a frame without mentioning that this errors on 12.0.x (§2.6);
- **describes reading auras via `UNIT_AURA`, `C_UnitAuras.GetUnitAuras`,
  `GetAuraDataByIndex`/`BySlot`/`ByAuraInstanceID`, or by diffing
  `updateInfo.addedAuras` / `removedAuraInstanceIDs`, without saying the payload is
  fully secret and those reads error on 12.1.0+** — this is the single largest
  falsified body of community aura code, and it looks completely idiomatic
  (`security-taint-and-restricted-data` §4.7, §3.5);
- **names `SecureAuraHeaderTemplate`** as a live Retail template — it is Classic-only
  from 12.1.0 (`security` §3.4);
- **shows an addon calling `CreateFrame("AuraButton", …)` or
  `container:AddAuraFrame(button)`** — that was a mid-PTR 12.1.0 API that was removed
  before ship, so this dates a page to roughly 2026-06/07 (`security` §3.5);
- discusses `Frame:RegisterEvent` restrictions without mentioning secret values;
- names `github.com/Amadeus-/WoWAddonDevGuide` as a reference — that repo is
  AI-generated, GitHub-archived, and has been falsified against Tier 1
  *[see `sources.md` §4]*.

### 5.7 Predicting whether a `C_*` return goes secret, before you fly it

A cheap read of the generated docs narrows "will this be readable in restricted combat?"
before anyone runs the client. Three signals, in order of strength:

1. **An absent `Predicate` is positive evidence.** Predicates are how the docs declare *when*
   a return goes secret (`security-taint-and-restricted-data` §4.7); the cooldown and aura
   APIs carry them. A function whose doc entry declares none — e.g. everything in
   `AssistedCombatDocumentation.lua` *[T1 docs]* — is not on the secrecy ladder at all.
2. **`SecretArguments` is about the *argument*, not the return.** It governs whether a secret
   may be *passed in*. `C_SpellBook.IsSpellKnown` carries
   `SecretArguments = "AllowedWhenUntainted"` and is readable. Do not read this annotation as
   a warning about the result.
3. **Blizzard doing plain arithmetic on the return, in a file that registers
   `PLAYER_REGEN_DISABLED`,** is suggestive — a `~=` or `>` on a secret cannot survive. ⚠ It
   is only suggestive: Blizzard's code is untainted, an addon's is not, so this predicts
   nothing on its own.

The signals are necessary, not sufficient — an annotation is a shape claim, and behaviour is
what a measurement closes. The worked case that ran the ladder and then flew it is
`C_AssistedCombat.GetNextCastSpell`, in [`cooldown-manager`](./cooldown-manager.md) §7
Tier 3.

---

## 6. Gaps

- **[gap] `SynchronousEvent` / `UniqueEvent` semantics.** Emitted by the doc
  generator, consumed by nothing in the shipped Lua, explained nowhere. Looked in:
  all 592 generated doc files, every other `.lua`/`.xml` in the checkout (zero
  hits), `Blizzard_APIDocumentation/` (the `/api` renderer), `Blizzard_EventTrace/`,
  and warcraft.wiki.gg via `wowkb.wiki search`.
  **`SecureHooksAllowed` and `CallbackEvent` are CLOSED** `[client 2026-07-24]` —
  both are enforced by the client, §5.4 and §2.5.
- **[gap] `EventCallbackType` / `FrameEventCallbackType` are opaque.** Both are
  declared `Type = "CallbackType"` with zero fields, so the spec asserts nothing
  about the accepted shape. What is *observed*: both a plain Lua function and a
  `C_FunctionContainers.CreateCallback` container are accepted by the global
  form, and a plain function by the `Frame:` form. `C_FunctionContainers` itself
  is undocumented (11 source call sites, no doc entry). Unresolved: whether the
  container buys anything beyond an unregisterable identity, and whether the
  leading `_nilOwner` argument is ever non-nil.
- **[closed] `Frame:UnregisterEventCallback` does not exist** `[client 2026-07-24]`
  — it reads `nil` on a live frame, making `FrameUtil.lua:59` a latent error in
  Blizzard's own code. Use the global two-argument form. See §2.5.
- **[closed] Event dispatch order between frames is observably variable**
  `[client 2026-08-05]` — two different orders for one event within one session on one
  frame set. Not merely unspecified: unusable. See §2.3.
- **[closed] `RegisterAllEvents` + `UnregisterEvent`: the wiki is right**
  `[client 2026-08-05]` — the unregister returns `false` and the event keeps arriving, so
  Blizzard's Event Trace `:702` is a no-op in its own code. See §2.2.
- **[gap] `GetCurrentEventID` / `GetEventTime`** exist as functions and both return
  `nil` when called outside an event handler `[client 2026-07-24]`. Still open: how
  to obtain a valid `eventProfileIndex`, which has no worked example in the 2298
  shipped `.lua` files and probably needs a profiling CVar we have not identified.
- **[mostly closed] `C_CombatLog.GetCurrentEventInfo`** is referenced by the
  deprecation shim but absent from the documented `C_CombatLog` surface — because
  it (and five sibling names) were relocated to the SecureOnly
  `C_CombatLogSecure`, which the shim's own header comment says is deliberately
  left undeprecated (§2.6). Only the runtime `nil` remains unproven from disk.
- **[gap] Nothing here has been run in the client.** Every `@verify-ingame`
  marker above is a real, testable question, not a hedge.

---

## Rules we could audit against

Concrete enough that a linter or a code reviewer can decide pass/fail.

⚠ Each rule states the **tier of its strongest evidence**. A Tier-2 rule is a
convention with a plausible source, not a fact about the client: flag, do not
fail, on those. A rule marked **[inference]** rests on an annotation whose meaning
Blizzard has not documented (§2.4 gap) — advisory only.

1. **The string passed to `RegisterEvent` must be an event's `LiteralName`, not
   its documentation `Name`.** `RegisterEvent("CombatLogEventUnfiltered")` is
   invalid; `"COMBAT_LOG_EVENT_UNFILTERED"` is the literal.
   *[Tier 1: `CombatLogDocumentation.lua:130` — `Name = "CombatLogEventUnfiltered"` —
   and `:132` — `LiteralName = "COMBAT_LOG_EVENT_UNFILTERED"`.]*

2. **An event name that is not in the 1741-entry corpus must be validated before
   registration, because registering an invalid event raises rather than returns.**
   `C_EventUtils.IsEventValid(eventName)` is the guard.
   *[Tier 1 for the guard's existence: `EventUtilsDocumentation.lua:26`, and
   Blizzard asserting on it at `Blizzard_SharedXML/EventUtil.lua:12`. Tier 2 for
   the raising behaviour: wiki `API Frame RegisterEvent`, revid 6654488.]*

3. **On Retail 12.0.x, no code path may call
   `frame:RegisterEvent("COMBAT_LOG_EVENT")` or
   `frame:RegisterEvent("COMBAT_LOG_EVENT_UNFILTERED")` unguarded.**
   *[Tier 2: wiki `Patch 12.0.0/API changes` revid 6747189 §Summary. Tier 1 obs:
   `RaiderIO` 12.0.7 (v202607232037) `core.lua:14618` disables it with the note
   "started to [error] upon 12.0 release". Tier 3: BigWigs @3fdc10f6cfd1 gates it
   behind `if not BigWigsLoader.isRetail` at `Plugins/BattleRes.lua:1503`, and
   makes `boss:Log` a no-op on Retail at `Core/BossPrototype.lua:1201-1202`.]*

4. **`C_CombatLogSecure.*` is unreachable from an addon.** Its documentation table
   declares `Environment = "SecureOnly"` — one of exactly two of the 385 tables
   that declare an `Environment` at all (308 `System` + 77 `ScriptObject`; the
   other 207 top-level doc tables are `Tables`/`Predicates`-only shared files
   with no `Environment` field).
   *[Tier 1: `CombatLogSecureDocumentation.lua:1-6` (`Environment` at `:6`);
   corpus count 383 × `"All"` + 2 × `"SecureOnly"`, the other being
   `PingManagerSecure` / `C_PingSecure`. **Measured**: all six of the relocated
   `C_CombatLog.*` names read `nil` from addon code `[client 2026-07-24]`, so
   `SecureOnly` is enforced by not binding the name in our environment — no longer
   an inference. Corroboration: `Blizzard_CombatLogProcessor.toc` declares
   `## UseSecureEnvironment: 1`.]*

5. **`RegisterAllEvents` and `UnregisterEvent` must not be mixed on the same
   frame.** The unregister returns `false` and the event goes on arriving; filter in
   the handler instead. Blizzard does exactly this at
   `Blizzard_EventTrace/Blizzard_EventTrace.lua:107` and `:702`, where it achieves
   nothing.
   *[`[client 2026-08-05]`; T2 wiki `API Frame RegisterAllEvents`, revid 6654327.]*

6. **A `CallbackRegistryMixin` owner has at most one callback per event; a second
   `RegisterCallback` with the same owner silently replaces the first.**
   *[Tier 1: `Blizzard_SharedXMLBase/CallbackRegistry.lua:128-130` —
   `self:UnregisterCallback(event, owner)` is called unconditionally before
   insertion, with that comment.]*

7. **A `CallbackRegistryMixin` callback that must ever be released has to be
   registered via `RegisterCallbackWithHandle` (or with an explicit non-numeric
   owner).** `RegisterCallback` with `owner == nil` allocates an anonymous
   counter ID that the caller cannot reconstruct.
   *[Tier 1: `CallbackRegistry.lua:118-119` for the anonymous allocation, `:17-19`
   for the comment that this is only acceptable when never releasing, `:155-158`
   for the handle form.]*

8. **Passing a `number` as a `CallbackRegistryMixin` owner is an error.**
   *[Tier 1: `CallbackRegistry.lua:120-121` — `error("… 'owner' as number is
   reserved internally.")`.]*

9. **`hooksecurefunc` cannot target any of the 24 functions annotated
   `SecureHooksAllowed = false`** — which includes all four event-callback
   registration globals. The attempt is refused with
   `hooksecurefunc(): <name> is forbidden for hooking`.
   *[Tier 1 for the annotation: 24 entries carry `SecureHooksAllowed = false` and
   none carries `true`; e.g. `FrameScriptDocumentation.lua:296`
   (`RegisterEventCallback`), `:308`, `:442`, `:454`. **Tier 1 for the behaviour:
   measured in the client** — hooking `CreateFromMixins` fails with that message
   `[client 2026-07-24]`. It is a *fail*, not merely a flag. Note the message
   differs from rule 10's *"Cannot hook function"*, so the two restrictions are
   separate engine checks and an addon must avoid the **union** of both lists,
   which overlap only on `scrub`.]*

10. **`hooksecurefunc` must not target any of the 23 names on the 11.0.0
    unhookable list** (`pairs`, `next`, `type`, `select`, `securecall`, …);
    the attempt raises "Cannot hook function".
    *[Tier 2: wiki `API hooksecurefunc`, revid 6588971, §Restrictions.]*

11. **A frame whose `OnUpdate` handler does nothing on most ticks should not have
    an `OnUpdate` script installed on those ticks.** The auditable form of the
    dirty-flag pattern: `SetScript("OnUpdate", …)` in the mark-dirty path,
    `SetScript("OnUpdate", nil)` in the mark-clean path.
    *[Tier 1: `Blizzard_SharedXML/LayoutFrame.lua:84-88` and `:106-117`, with the
    in-source rationale "To optimize performance, only set OnUpdate while marked
    dirty."]*

12. **Code that clears its own `OnUpdate` from inside a handler must also carry a
    guard flag** — clearing the script does not prevent the handler running again
    on the same frame.
    *[Tier 1: `Blizzard_SharedXMLBase/FrameUtil.lua:11-31`; the `frame.canUpdate`
    flag exists precisely to "prevent the OnUpdate handler from running the same
    frame it was removed".]*

13. **A `MarkClean` implementation that unconditionally clears `OnUpdate` breaks
    subclasses.** The clear must be conditional on the mixin's `OnUpdate` **method**
    still being the base one (`self.OnUpdate == BaseLayoutMixin.OnUpdate`, an
    identity comparison on the method table — *not* on `GetScript("OnUpdate")`).
    *[Tier 1: `LayoutFrame.lua:102-104` (`ShouldClearOnUpdateAfterClean`, the
    comparison at `:103`) and the comment at `:112-113`.]*

14. **Every code path through a concrete `Layout()` must reach `MarkClean()`,**
    or the frame stays dirty and its `OnUpdate` never comes off. **Audit the
    early returns, not just the last line** — an early `return` before
    `MarkClean()` is the failure mode.
    *[Tier 1, and note the shipped tree is not clean here: three of the four
    concrete implementations end in `MarkClean()` — `LayoutFrame.lua:266`, `:530`,
    `:722` — but `GridLayoutFrameMixin:Layout` (`:539-571`) has an early `return`
    at `:542` (when `ShouldUpdateLayout` is false, e.g. the frame is hidden,
    `:586-588`) that leaves `self.dirty` set. So "Blizzard always does this" is
    **false**; the rule stands on the mechanism in `MarkDirty`/`MarkClean`
    (`:84-117`), not on universal Blizzard compliance.]*

15. **`C_Timer.After` returns nothing, so any timer that might need cancelling
    must use `C_Timer.NewTimer` or `C_Timer.NewTicker`.**
    *[Tier 1: `UITimerDocumentation.lua:11-20` has no `Returns` block; `:22` and
    `:39` return `cbObject`. Blizzard calls `:Cancel()` on those at
    `Blizzard_SharedXMLBase/ObjectUpdater.lua:27` and `TimedCallback.lua:7-12`.]*

16. **`RunNextFrame(f)` and `C_Timer.After(0, f)` are the same call and neither
    runs in the current frame.**
    *[Tier 1 for the identity: `Blizzard_SharedXMLBase/FunctionUtil.lua:126-128`.
    Tier 2 for the timing: wiki `API C_Timer.After`, revid 6592061 — "the earliest
    the callback will be called is on the next frame".]*

17. **An addon that needs an event which may already have fired must check the
    already-happened state before registering.** The auditable shape is
    Blizzard's: `if IsLoggedIn() then callback() return end` before registering
    `PLAYER_LOGIN`; `if isLoaded then callback() return end` before registering
    `ADDON_LOADED`.
    *[Tier 1: `Blizzard_SharedXML/EventUtil.lua:71-79` (`ContinueOnAddOnLoaded`)
    and `:81-88` (`ContinueOnPlayerLogin`).]*

18. **`RegisterUnitEvent` filters are per-registration and a later plain
    `RegisterEvent` for the same event replaces them.** Code that does both for
    one event on one frame has an ordering bug.
    *[Tier 2: wiki `API Frame RegisterUnitEvent`, revid 6735133 — "Repeated calls
    with the same event will overwrite old registrations. Calling
    Frame:RegisterEvent will also overwrite the old registration." Tier 3
    corroboration that the filter is readable back:
    `IsEventRegistered(frame, event)` returns `registered, unit1, unit2` and oUF
    branches on it at `events.lua:48-52`.
    ⚠ The wiki's *"up to four units"* is **not** a client-enforced cap: a
    five-unit registration is accepted without error `[client 2026-07-24]`.
    Whether the fifth actually filters was not measured.]*

19. **`IsEventRegistered` returns more than a boolean** — `isRegistered: bool,
    units: UnitTokenType?…` (variadic, `StrideIndex = 1`). So `if
    f:IsEventRegistered(e) then` and `local reg = f:IsEventRegistered(e)` are both
    fine (Lua truncates to one value), but in a **tail position** the call expands
    to all its returns: `foo(f:IsEventRegistered(e))` passes N arguments,
    `{f:IsEventRegistered(e)}` builds an N-element table, and
    `return f:IsEventRegistered(e)` returns N values. Wrap in parentheses to
    truncate.
    *[Tier 1: `SimpleFrameAPIDocumentation.lua:680-696`, returns at `:691-695`.
    Tier 3 that the extra returns are load-bearing: oUF reads them back at
    `events.lua:48-52`.]*

20. **Do not infer that a widget lacks a method because it is absent from that
    widget's documentation table.** The generated docs record no inheritance:
    `SetScript` is declared on **three** tables — `SimpleScriptRegionAPI`,
    `SimpleAnimAPI` and `SimpleAnimGroupAPI` — and **not** on `SimpleFrameAPI`,
    which every frame nonetheless has. The triplication is itself the point: the
    generator duplicates rather than inherits.
    *[Tier 1: `SimpleScriptRegionAPIDocumentation.lua:628`,
    `SimpleAnimAPIDocumentation.lua:343`, `SimpleAnimGroupAPIDocumentation.lua:318`;
    `SimpleFrameAPIDocumentation.lua:1-6` and
    `SimpleScriptRegionAPIDocumentation.lua:1-6` show flat, parentless table
    headers.]*

21. **A claim that a global "does not exist" must be backed by a check of both
    the generated docs and the shipped source**, because Tier-1 doc coverage of
    globals is partial (692 documented globals; the global `CreateFrame` and
    `hooksecurefunc` are not among them). And a bare-name grep is not enough
    either: a *namespaced* function can share a global's name (`C_PingSecure.CreateFrame`).
    *[Tier 1: `wowkb.uiapi missing <name>` reports docs/source/neither;
    e.g. `hooksecurefunc` → "generated docs: no, UI source hits: 14" (verified);
    `PingManagerSecureDocumentation.lua:16` for the name collision.]*

22. **Any citation of `Enum.ScriptBindingType` as Tier 1 is unsupported.** The
    string `ScriptBinding` does not occur in any of the 592 generated
    documentation files; the parameter is typed bare `number`. (This does **not**
    prove the enum is absent from the client — only that the generated spec does
    not declare it. Code using the `LE_SCRIPT_BINDING_TYPE_*` globals is fine.)
    *[Tier 1: `grep -r ScriptBinding` over
    `Blizzard_APIDocumentationGenerated/` returns nothing;
    `SimpleScriptRegionAPIDocumentation.lua:325-335`. Tier 2 res for the legacy
    globals that do exist: `Resources/LuaEnum.lua:9251-9254` — and the wiki's own
    `HookScript` example uses `LE_SCRIPT_BINDING_TYPE_INTRINSIC_POSTCALL`.]*

23. **Spell lookups in shipped code should pass a numeric spell ID, not a
    localized name** — name resolution requires the spell to be in the player's
    spellbook.
    *[Tier 2: wiki `API types/SpellIdentifier`, revid 6776503, 2026-07-20.]*

24. **A doc-generated type name is not a documented type.** `WOWGUID`,
    `UnitToken`, `UnitTokenVariant`, `SpellIdentifier`,
    `UnitTokenPvPRestrictedForAddOns` and `AuraData` appear 391/264/100/74/28/10
    times as parameter/return types and are declared zero times — so their shape
    must be cited from Tier 2, never presented as Tier 1.
    ⚠ **`AuraData` additionally fails at runtime, not just at citation time**: the
    struct is always fully secret at 12.1.0 and every function returning one carries
    `RequiresUnitAuraAccess` (`FailureMode = Error`). Code that reads an `AuraData`
    field in combat throws. Audit for the read, not just for the type name.
    *[Tier 1 @12.1.0: declaration-vs-use grep over all 612 generated doc files; every
    declaration grep returns empty. Tier 2 for the secrecy: `Patch 12.1.0/API changes`,
    revid 6801760, 2026-08-09.]*

25. **A `RegisterEventCallback` callback must accept a leading owner argument
    before the payload.** Every Blizzard callback in the shipped tree declares it
    (and discards it) as `_nilOwner`; a handler written as
    `function(payloadArg) … end` will read the owner as its first payload value.
    *[Tier 1, 7 sites: `Blizzard_ChatFrame/Shared/ClassTalentHelper.lua:15, :20,
    :25, :30`; `Blizzard_SharedXMLGame/Tooltip/TooltipComparisonManager.lua:383`;
    `Blizzard_SharedXMLBase/Event.lua:6`, `:20`. **[inference]** that this is a
    contract rather than six consistent conventions — the generated docs declare
    `EventCallbackType` with no fields at all
    (`FrameScriptDocumentation.lua:503-505`). `@verify-ingame`]*

---

## Changelog

- 2026-08-11 — 12.1.0. Every corpus count **re-parsed**, not hand-edited: §2.1
  1741→1782 events / 204→210 systems, §2.4 the flag table, §4.1 6144→6335 functions
  (4202/695/1438). The same parser reproduces the 12.0.7 figures exactly, which is
  what licenses the comparison. §2.4 gained the finding the patch-day heads-up got
  wrong: **`SecretPayloads` is still 7 and `UNIT_AURA` is still not on it** — the
  secret payload arrives via a `Secret` *predicate* on the event entry, a second
  route the old anchor did not anticipate. §4.2/§4.3/rule 24: `AuraData` is now
  always-fully-secret **and** unreadable. §5.1 gained `tooltipShowAuraSpellIDs`;
  §5.6 gained four aura-shaped staleness detectors. ⚠ The `[T2 res] Events.lua`
  cross-check is stale — that repo was not re-pulled.
- 2026-08-05 — **six ClientLab answers** `[client 2026-07-24]`. `SecureHooksAllowed`
  is enforced, with a message (`… is forbidden for hooking`) distinct from the wiki
  list's *"Cannot hook function"* — two checks, avoid the union (§5.4, rule 9);
  `IsCallbackEvent` tracks the `CallbackEvent` flag on both sides (§2.5); all six
  relocated `C_CombatLog.*` names read `nil` (§3, rule 4); **`Frame:UnregisterEventCallback`
  does not exist**, making `FrameUtil.lua:59` a latent error in Blizzard's own code
  (§2.5); the four-unit `RegisterUnitEvent` cap is not enforced (§2.3, rule 18);
  `GetCurrentEventID`/`GetEventTime` exist but return `nil` outside a handler (§5.1).
- 2026-08-05 — §2.8–2.9 (the Cooldown Manager alert channel; `C_AssistedCombat`) moved to
  `cooldown-manager.md`. Only the generalisable choke-point dispatch shape stays here.
- 2026-07-23 — adversarial re-verification of every locator and corpus count (front matter
  `verified:`). Six claims were corrected in place; all six were re-checked against the
  12.0.7.68887 checkout on 2026-08-05 and stand.
