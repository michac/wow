---
title: The Cooldown Manager — how a CDM row resolves
patch: 12.1.0
fetched: 2026-08-16
reviewed: 2026-08-16   # 12.1.0 source reads, plus ONE 12.1.0 client capture (§4.2). Every other [client] tag below is 12.0.7 and was not restamped
sources:
  - raw/addon-research/wow-ui-source-12.1.0 @ 12.1.0.69273 — Interface/AddOns/Blizzard_CooldownViewer/*, Blizzard_SharedXML/LayoutFrame.lua, Blizzard_SharedXMLBase/Pools.lua and Blizzard_APIDocumentationGenerated/CooldownViewer{,Constants}Documentation.lua. `[T1 src @12.1.0]` / `[T1 docs @12.1.0]` locators resolve here
  - https://warcraft.wiki.gg/wiki/Patch_12.1.0/API_changes (revid 6801760, 2026-08-09)
  - raw/addon-research/wow-ui-source @ 12.0.7.68887 — Interface/AddOns/Blizzard_CooldownViewer/*
  - raw/addon-research/wow-ui-source @ 12.0.7.68887 — Blizzard_APIDocumentationGenerated/CooldownViewer{,Constants}Documentation.lua
  - wago.tools DB2 @ 12.0.7 — CooldownSet, CooldownSetSpell, CooldownSetLinkedSpell (raw/wago/)
  - projects/cooldown-hud/docs/ — CDMProbe in-client captures, session detail
  - in-client capture, CDMProbe AlertTape v0.32.27 (/cdmp alerts), Destruction Warlock, 2026-07-30  # §5.1 alert-channel confirmations. ⚠ NOT RE-CHECKABLE — no extract of this session survives on disk; the surviving alert-tape extract holds only v0.32.44 / 2026-07-31 sessions
  - in-client capture, CDMProbe AlertTape v0.32.29, Destruction/Hellcaller Warlock, 2026-07-30  # §5.4 same-frame refresh tie; simultaneous PandemicTime on both Immolate cooldownIDs. ⚠ NOT RE-CHECKABLE — same rolled-off session set as the line above
  - in-client capture, CDMProbe v0.32.32 decision log, Destruction Warlock (Hellcaller AND Diabolist), 2026-07-30  # §2.8 cid 66181's base/display spellID split + hero-talent-dependent isKnown; override event firing for an untracked display id. ⚠ NOT RE-CHECKABLE — the surviving decision-log extract holds only v0.32.95 / 2026-08-03
  - in-client capture, CDMProbe v0.32.46 decision log, Destruction Warlock (both hero trees), 2026-07-31  # §5.3 ChargeGained is a prediction-queue drain, not a charge. ⚠ NOT RE-CHECKABLE — same surviving extract as the line above, which does not reach this session
  - in-client capture, CDMProbe /cdmp census, Destruction Warlock (both hero trees), 2026-07-31  # §2.5, §7 the readable-surface sweep
  - in-client capture, cap v0.2.1/v0.2.2 `edge` stream (`wowkb.capture cap edge`), Demonology/Diabolist Warlock, 2026-08-07  # §7 the alert channel is silent on cid 760: 0 edges of 1054 over 171 casts
  - in-client capture, CDMProbe v0.32.53 flight recorder, Destruction + Demonology Warlock, 2026-08-01  # §7 Tier 3 C_AssistedCombat readable through combat. ⚠ NOT RE-CHECKABLE — no surviving extract carries that version, that date, or any GetNextCastSpell sample
  - in-client capture, CDMProbe /cdmp curve stack, Demonology Warlock, 2026-08-04  # §7 Tier 2 auraInstanceID plain / auraSpellID secret
  - in-client capture, cap v0.2.0 bind log, Destruction + Demonology Warlock (both hero trees) AND Retribution Paladin, 2026-08-06  # §2 overrideSpellID always populated; §4 TRAIT_CONFIG_UPDATED precedes the rebuild; §7 Tier 1 category set is a superset
  - in-client capture, ClientLab v0.2.2 `cdm-identity-readable-in-combat`, Demonology Warlock, 5 in-combat runs, 2026-08-06  # §2 overrideSpellID is the in-combat identity route and MOVES; §4 GetSpellID's secret set is volatile and does not track auraDataUnit. ⚠ The capture itself is GONE — the surviving lab-runs extract reaches only 2026-08-05 and contains no run of this id. The recorded field values survive transcribed verbatim in observations.md, which is the archive of record for this one
  - in-client capture, cap v0.2.1 bind log, Demonology/Diabolist Warlock, 2026-08-07  # §1.2 the three row enumerations (DB2 65 / category set 44 / laid out 21) and which HideByDefault rows a saved layout un-hid
  - in-client capture, ClientLab CDMSweep, Demonology Warlock, 2026-08-09 (raw/clab-cdmsweep.log, raw/clab-cdmevent.log)  # §7 the SpellCooldownInfo per-member seal, Bar.Pip:IsShown(), the totem channel, GetSpellCooldownDuration in restricted combat
  - in-client capture, live 12.1.0.69214, Havoc Demon Hunter, EssentialCooldownViewer with 9 item frames, 2026-08-16  # §4.2 the SetPoint re-anchor: takes effect and holds across a 138 s fight in a session with no re-layout. Two sessions on one login — the first with a third-party CDM re-skin's cooldown override ENABLED (it won every round), the second with it disabled
  - EllesmereUI v8.7.5 @ c4eba58d996a8436f467ac8f297148bff9dd3008 (2026-08-04),
    https://github.com/EllesmereGaming/EllesmereUI — license CUSTOM, ALL RIGHTS
    RESERVED; read for API discovery only, no code copied. Mined 2026-08-05 via the
    `mine-addon` skill; clone deleted after (step 5). file:line citations resolve
    only against that commit. Unverified residue:
    `addon-dev/mined-pending-verification.md`.
confidence: high
---

# The Cooldown Manager — how a CDM row resolves

## 0. What this file is, and what it is not

**This is a system study, not one of the seven topic files.** The
[README](./README.md) §1 topic map partitions *mechanisms* — events, frames, taint,
persistence — so that any addon-dev question lands in exactly one file. This file
is organised the other way: around **one Blizzard system**, `Blizzard_CooldownViewer`,
because this workspace builds addons entirely on top of it and the
model does not survive being cut into seven pieces.

It therefore **defers to the topics for general mechanism** and only claims what is
specific to the CDM:

| Ask about | Owned by |
|---|---|
| Mixin composition, the data/display split, the dirty flag as a pattern | [`module-architecture`](./module-architecture.md) §2.1, §4.1, §4.3 — already covers `CooldownViewerItemMixin` in detail |
| **Reading widget internals as a substitute for a sealed value** — the mechanism, its four preconditions, and why the naive form is wrong | [`security-taint-and-restricted-data`](./security-taint-and-restricted-data.md) **§4.11** + rule 17b. This file supplies the *instances* (`PandemicIcon`, `wasSetFrom*`, `auraDataUnit`, and tab-1 `IsActive()` as the counter-example); that one owns the rule |
| What secret values are, `SecretArguments`, how to display what you cannot read | [`security-taint-and-restricted-data`](./security-taint-and-restricted-data.md) |
| Event registration mechanics, `hooksecurefunc` as an instrument, `OnUpdate` vs ticker | [`api-events-and-discovery`](./api-events-and-discovery.md) |
| Texture channels, pooling, anchoring to Blizzard frames | [`frames-textures-animation`](./frames-textures-animation.md) |

---

## 0b. ⚠ 12.1.0 REWROTE THIS SYSTEM AND THIS FILE HAS NOT BEEN RE-FLOWN

**Read this before using anything below.** The Cooldown Manager was one of 12.1.0's
larger reworks. This file was updated against the 12.1.0 **source** on patch day; it
was **not** re-measured in the client, and it was not re-derived line by line.

**What that means for the three kinds of claim here:**

| Claim kind | Status at 12.1.0 |
|---|---|
| **`[client YYYY-MM-DD]` measurements** | **Taken on 12.0.7, and NOT restamped** — with one exception, §4.2, which was measured on live 12.1.0.69214 and says so. Each still says the date it was measured. Several are about the *readable surface* of item frames, which the rework plausibly moved. Treat every other one as "was true on 12.0.7" and re-fly before building on it. |
| **Unstamped `[T1 src: …:NNN]` line numbers** | **12.0.7.68887, and not re-resolved.** `Blizzard_CooldownViewer/` gained six files and lost five (below), so many of these have shifted; the *mechanism* they cite is usually still there, the *line* frequently is not. A locator stamped `@12.1.0` was read on the new tree. |

**The stamp is the whole convention, and it is per-locator, not per-section.**
`[T1 src @12.1.0: <file>:<line>]` means *this line number was opened on the
12.1.0.69273 tree*; a bare `[T1 src: <file>:<line>]` means it was not. Restamping is
therefore how a locator gets fixed — re-open it, write the new number, add `@12.1.0`.
⚠ **A stamp is a claim about the LINE, never about the evidence class.** `[T1 src
@12.1.0]` is a **source read**, which README §0 ranks below `[client YYYY-MM-DD]`: it
says what Blizzard's Lua does, not what the running client does. Nothing here upgrades
a source read into a measurement, and §4.1 — the densest run of `@12.1.0` locators in
the file — is source, start to finish.
| **Structural claims about categories, families and identity** | **Partly falsified — corrected in place below.** The category enum more than doubled, the two hidden pseudo-categories were renamed, and there is now a third display mode. Those specific corrections are made at their sections; the identity ladder (§2) and value cascade (§3) were **not** re-derived. |

**The file-level diff, as the cheapest map of what moved**
`[T1 src @12.1.0 vs 12.0.7, `Blizzard_CooldownViewer/`]`:

- **Gone (5):** `CooldownViewerVisualAlert.lua`, `CooldownViewerVisualAlertData.lua`,
  `CooldownViewerVisualAlertTemplates.lua/.xml`, `CooldownViewerVisualAlertsManager.lua/.xml`
- **New (6+):** `CooldownViewerSecure.lua`, `GroupBuffFilter.lua/.xml`,
  `CooldownViewerDraggedItemBase.lua/.xml`, `CooldownViewerEditAlertBase.lua/.xml`,
  `CooldownViewerVisualAlertTarget.lua`

The visual-alert subsystem §5.1 and §6 describe was **restructured**, not merely
moved. `@verify-ingame`

**What 12.1.0 added, in one list** (each expanded at its section):

1. **The CDM now tracks trinkets, potions and racial cooldowns/durations** — five new
   categories and three new row fields (§1.3).
2. **Group buffs** — a third display mode, a new settings UI, `GetGroupBuffItems`, and
   four new `C_UnitAuras` functions with two events (§1.4).
3. **`HiddenSpell` / `HiddenAura` were renamed `HiddenActive` / `HiddenPassive`**
   (§1.2) — a silent breakage for anything referencing them by name.
4. **A "Short" sounds category** (26 sounds) and CDM sounds feeding the **Combat Audio
   Assist** accessibility feature (§5.5).
5. **CDM rows can be pinged** (§5.6).
6. `SPELL_UPDATE_COOLDOWN` **gained an `itemID` payload field** (§5).

---

⚠ **This file is where the subtree's in-client measurement is concentrated.** README §0
defines `[client YYYY-MM-DD]` as the strongest evidence class and deliberately keeps no
census of where it appears; `grep -rl '\[client 20'` is the live list, and every other
topic file carries measurements too. A large subset of the claims below are **client-confirmed** and are marked
**`[client]`** with their capture in the front matter. Everything
else is a source read at the pinned build, and unsettled claims carry
`@verify-ingame` as usual.

---

## 1. The two families

A CDM row belongs to one of two families, and **the family is the only stable fact
about it.** Everything else — its identity, what its dial means — is re-derived on
every refresh.

The settings panel presents **three** display modes, and the two row families map to
the first two:

```lua
local displayModeToCategories =
{
	["spells"]     = { Enum.CooldownViewerCategory.Essential,    Enum.CooldownViewerCategory.Utility,
	                   Enum.CooldownViewerCategory.EquipSlotEssential, Enum.CooldownViewerCategory.SpecAgnosticEssential,
	                   Enum.CooldownViewerCategory.HiddenActive },
	["auras"]      = { Enum.CooldownViewerCategory.TrackedBuff,  Enum.CooldownViewerCategory.TrackedBar,
	                   Enum.CooldownViewerCategory.EquipSlotTracked,   Enum.CooldownViewerCategory.SpecAgnosticTracked,
	                   Enum.CooldownViewerCategory.HiddenPassive },
	["groupBuffs"] = {},
};
```
`[T1 src @12.1.0: Blizzard_CooldownViewer/CooldownViewerSettings.lua:1518-1523]`

**Two families, still.** Each of the four real categories per mode is an
Essential-side or a Tracked-side member; the split is unchanged in kind, only widened
(§1.3). `["groupBuffs"] = {}` is deliberately empty — the third mode is not
category-driven at all and is served by its own filter UI (§1.4).

The same spell/aura split appears in the data provider's hidden-category mapping —
Essential and Utility fall back to `HiddenActive`, TrackedBuff and TrackedBar to
`HiddenPassive`
`[T1 src @12.1.0: .../CooldownViewerSettingsDataProvider.lua:67-70]`.

**A row cannot be dragged across the line.** Not because the data layer forbids it —
`GetCooldownCategoryChangeStatus` explicitly declines to check the category, with a
comment saying it *could* be expanded to
`[T1 src: .../CooldownViewerSettingsLayoutManager.lua:946-950]` — but because
`GetValidAssignmentCategories` only ever offers categories drawn from
`self.currentCategories`, i.e. **the tab currently open**
`[T1 src: .../CooldownViewerSettings.lua:1554-1567]`.

### 1.1 The two families behave differently

| | Tab 1 — "spells" | Tab 2 — "auras" |
|---|---|---|
| Mixin | `CooldownViewerCooldownItemMixin` `[:678]` | `CooldownViewerBuffItemMixin` `[:1157]` |
| Categories | Essential, Utility, **EquipSlotEssential, SpecAgnosticEssential** | TrackedBuff, TrackedBar, **EquipSlotTracked, SpecAgnosticTracked** |
| Value sources | **four** — charges, spell cooldown, aura/totem, edit mode | **three** — totem, aura, edit mode |
| Spell-cooldown rung | yes | **none — structurally cannot show a cooldown** |
| `IsActivelyCast()` | `true` `[:680]` | `false` (inherits the base) `[ItemData.lua:534]` |
| `ShouldBeActive()` | `cooldownID ~= nil` `[:362]` — **constant true once bound** | tracks aura liveness `[:1186]` |
| Extra regions | `ChargeCount`, `CooldownFlash`, `OutOfRange` | `Applications`, `DebuffBorder` |
| Extra events | five (§5) | **none** — `OnEvent` is a bare pass-through `[:2054-2056]` |

The useful compression: **tab 1 answers "can I press this", tab 2 answers "is this
running".** A spell tracked in both is not redundancy — it is the two questions asked
separately.

> **Consequence for consumers.** Category *within* a family is user-editable placement
> and tells you nothing (Essential ↔ Utility are interchangeable; so are
> TrackedBuff ↔ TrackedBar). Family tells you a great deal. Classify on family, not
> on category.

### 1.2 `HideByDefault` — a row that exists in the data and never gets a frame

A CDM row can carry `Enum.CooldownSetSpellFlags.HideByDefault`, and such a row is
**filtered out in Blizzard's Lua**, not in C, at data-set construction.
`CooldownViewerSettingsDataProviderMixin` pulls the raw set —
`C_CooldownViewer.GetCooldownViewerCategorySet(cooldownCategory, ALLOW_ALL_COOLDOWNS_IN_SET)`
`[T1 src: CooldownViewerSettingsDataProvider.lua:85]` — then, for each id, tests the flag
and **rewrites the row's own `category`** to a pseudo-category
`[T1 src: :93-96]`:

```lua
local isDisabled = FlagsUtil.IsSet(info.flags, Enum.CooldownSetSpellFlags.HideByDefault);
if isDisabled then
    info.category = cooldownCategoryToHiddenCategoryMapping[info.category];
end
```

The two flag members are `HideAura = 1` and `HideByDefault = 2`
`[T1 docs: CooldownViewerConstantsDocumentation.lua:16-27]`.

⚠ **The two pseudo-categories are `HiddenActive` and `HiddenPassive`, and they are not
enum members.** They are `-1` and `-2`, **assigned into the enum table by Blizzard's own
addon** at `[T1 src @12.1.0: CooldownViewerSettingsConstants.lua:4-5]`; the generated C
enum declares `NumValues = 9`, members 0–8 only
`[T1 docs @12.1.0: CooldownViewerConstantsDocumentation.lua]`. So they are **nil until
`Blizzard_CooldownViewer` has loaded**, and they are **negative** — anything iterating the
enum or assuming a contiguous range is surprised. (The pseudo-category mapping itself is
the snippet quoted in §1: Essential/Utility → `HiddenActive`, TrackedBuff/TrackedBar →
`HiddenPassive`.)

⚠⚠ **They were called `HiddenSpell` and `HiddenAura` through 12.0.7.** The rename is
silent in the worst way: the old names are ordinary table keys that simply stop being
assigned, so `Enum.CooldownViewerCategory.HiddenSpell` reads **`nil`** rather than
erroring, and a comparison against it matches every row whose `category` is also nil —
or none at all. Grep for both names.

**The consequence is that the row gets no frame.** `GetOrderedCooldownIDsForCategory`
matches on the (now rewritten) category
`[T1 src @12.1.0: CooldownViewerSettingsDataProvider.lua:249-260]`,
a viewer asks it for its own category `[T1 src @12.1.0: CooldownViewer.lua:2066-2069]`, and
`RefreshLayout` `[T1 src @12.1.0: :2021]` pools a frame only for what comes back. A hidden
row is in nobody's category, so nothing is pooled for it. The same function applies two
further suppressions on the way out — `isInvisible` (gated on `CDM_HIDE_INVISIBLE_ITEMS`)
at `:253` and `isKnown` at `:254` — so three independent mechanisms can keep a row out of
a viewer.

> ⚠ **THEREFORE NO ALERT EDGE CAN FIRE FOR A HIDDEN ROW.** All six alerts are
> `self:TriggerAlertEvent(…)` called on **item-frame methods**
> `[T1 src @12.1.0: CooldownViewer.lua:518, :579, :632, :636, :640, :1179]`,
> and **every one of them is reached through
> `self.itemFramePool:EnumerateActive()`** — with no exception for the aura pair. The
> timer-driven three go through the `OnUpdate` enumeration
> `[T1 src: CooldownViewer.lua:1622-1627]`; the two aura edges go through
> `CooldownViewerMixin:CheckAuraRemovedAlertTriggers` `[:1672-1680]` and
> `CheckAuraAddedAlertTriggers` `[:1682-1690]`, called from `OnUnitAura` at `[:1636]` and
> `[:1669]`, which enumerate the pool at `[:1675]` and `[:1685]` before calling
> `itemFrame:CheckTriggerAuraRemovedAlert(…)` / `CheckTriggerAuraAppliedAlert(…)`.
> ⚠ **Not** `auraInstanceIDToItemFramesMap` `[:1641, :1652]` — that map drives
> `OnUnitAuraRemovedEvent` / `OnUnitAuraUpdatedEvent`, which are display refreshes, not
> alert triggers. No frame, no method call, no edge.
>
> **This scopes the alert-choke-point technique.** The `hooksecurefunc(item,
> "TriggerAlertEvent")` hook described in §5.1 observes **every** edge, and that
> completeness guarantee is real — but it is scoped to **bound rows**. A consumer latching
> readiness or aura presence off this channel is blind to a `HideByDefault` row and gets
> **no error and no absent value** to tell it so; it simply never hears about that ability.
> Enumerate the candidate set and reconcile, or the gap is invisible.

**But the API still sees hidden rows.** `GetCooldownViewerCategorySet` returns them —
provably, because it is the exact call Blizzard makes *immediately before* doing the
hiding, so a C-side filter would make the Lua rewrite dead code — and
`GetCooldownViewerCooldownInfo(cooldownID)` answers for any id, hidden or not. That is what
makes an offline DB2 enumeration reconcilable with a live one.

> ⚠ **The struct carries the RAW DB2 `category` and `flags`, never the player's effective
> placement.** The rewrite above mutates a Lua-side copy held by the data provider; a fresh
> `GetCooldownViewerCooldownInfo` call returns the unmodified DB2 values. The **effective**
> category exists only in Blizzard Lua, at
> `CooldownViewerSettings:GetDataProvider():GetCooldownInfoForID(id).category`. Reading
> `info.category` from the API and calling it "where this row is" is wrong for every hidden
> row and for every row the player has moved.

**A saved layout can un-hide a `HideByDefault` row.** After the rewrite, the data provider
re-applies the player's saved block — `DeserializeCooldownInfo` sets
`cooldownInfo.category = block.category or cooldownInfo.category`
`[T1 src: CooldownViewerSettingsLayoutManager.lua:732-737]` — and it is gated on
`activeLayoutMatchesCurrentSpec` `[T1 src: CooldownViewerSettingsDataProvider.lua:143-149]`,
which resolves through `CanActivateLayout` comparing the layout's class+spec tag against the
current one `[T1 src: CooldownViewerSettingsLayoutManager.lua:212-221]`. So "hidden" is a
default, not a property, and it is **per class+spec**.

**The Lua path that writes that saved block**, for the record:
`CooldownViewerSettingsDataProviderMixin:SetCooldownToCategory(sourceCooldownID, category)`
`[T1 src @12.1.0: CooldownViewerSettingsDataProvider.lua:315-322]` resolves the row's info
and hands it to `ChangeCooldownInfoInternal` `[@12.1.0: :335-347]`, which asks the layout
manager for a `GetCooldownCategoryChangeStatus` verdict and then calls
`WriteCooldownInfo_Category`. The `HideByDefault` rewrite this un-does is the one at
`[@12.1.0: :115-118]`, keyed through the pseudo-category mapping table at `[@12.1.0: :66-77]`.
⚠ **This writes the player's saved layout** — it is the same persisted state the settings UI
edits, not a display-side override, so a caller is mutating a user setting.
Whether driving that path (or its settings-UI equivalent) actually lands the row in a viewer
end to end is a separate question and an open one — §9 holds it. Reading this paragraph as
"so it works" is exactly the inference §9 says nobody has closed.

> ⚠ **The signal that this happened is a Lua callback, not a game event.**
> `EventRegistry:TriggerEvent("CooldownViewerSettings.OnDataChanged")`
> `[T1 src @12.1.0: CooldownViewerSettingsLayoutManager.lua:832]`, raised from
> `NotifyListeners` `[@12.1.0: :823-836]` —
> which is **suppressed while notifications are locked** for batched changes and fires once
> afterwards. Treat it as a hint and re-poll, the same discipline §4 already asks for on
> `TRAIT_CONFIG_UPDATED`. There is no `COOLDOWN_VIEWER_*` event for a layout edit.

`[client 2026-08-07]` **Both halves observed on one character.** Demonology Warlock,
cap v0.2.1 `bind` capture: DB2 `CooldownSetID 60` carries **65** rows of which **28** are
`HideByDefault`; `GetCooldownViewerCategorySet` summed **44**; cap walked **21**. Two of the
flagged rows — Dominion of Argus (cid `169561`) and Unending Resolve (cid `84183`) — are in
the live bind, i.e. un-hidden by a saved layout; Infernal Bolt's aura row (cid `172289`,
spell `433891`, `flags = 2`) is not, and produces nothing at all.
`[T1 db2: CooldownSetSpell @ 12.0.7]`

### 1.3 Trinkets, potions and racials — the five new categories (12.1.0)

`Enum.CooldownViewerCategory` went from **4 members to 9**
`[T1 docs @12.1.0: CooldownViewerConstantsDocumentation.lua]`:

| Member | Value | Family | Since |
|---|---:|---|---|
| `Essential` | 0 | tab 1 | 12.0 |
| `Utility` | 1 | tab 1 | 12.0 |
| `TrackedBuff` | 2 | tab 2 | 12.0 |
| `TrackedBar` | 3 | tab 2 | 12.0 |
| **`GroupBuff`** | 4 | *neither* — §1.4 | **12.1.0** |
| **`SpecAgnosticEssential`** | 5 | tab 1 | **12.1.0** |
| **`SpecAgnosticTracked`** | 6 | tab 2 | **12.1.0** |
| **`EquipSlotEssential`** | 7 | tab 1 | **12.1.0** |
| **`EquipSlotTracked`** | 8 | tab 2 | **12.1.0** |

The two axes are what the names say. **`SpecAgnostic*`** is a row that is not
spec-scoped — the natural home for **racial abilities** and other class-wide
cooldowns, which previously had no category that made sense. **`EquipSlot*`** is a row
whose source is an **equipped item** rather than a spellbook entry: trinkets, and the
on-use item cooldowns generally.

**§1.1's "classify on family, not on category" rule survives, and it matters more now.** ⚠
Each new category is unambiguously tab-1-side or tab-2-side, so family is still the
stable fact. But a consumer that **enumerated categories by literal** — `{Essential,
Utility}` and `{TrackedBuff, TrackedBar}` — now silently misses more than half the
possible rows, and misses them without any error. Enumerate from
`displayModeToCategories` (§1) or from the enum, never from a hand-written pair.

**Three new fields on `CooldownViewerCooldown`**
`[T1 docs @12.1.0: CooldownViewerDocumentation.lua:126-146]`, plus one that turns out
to matter:

| Field | Type | What it is |
|---|---|---|
| `spellCategoryID` | `number?` | the **shared-cooldown category** a row belongs to — this is how potions work. `CooldownViewerItemDataMixin` resolves it through `C_Spell.GetLastCategoryCooldownSource(spellCategoryID) -> spellID, itemID` and then binds from *that* `[T1 src @12.1.0: CooldownViewerItemData.lua:50-54]`, so a potion row tracks "whatever last consumed this category", not a fixed spell. |
| `equipSlot` | `luaIndex?` | the inventory slot a row's item sits in. Read via `GetInventoryItemCooldown("player", equipSlot)` `[T1 src @12.1.0: CooldownViewer.lua:1018-1031]` — note Blizzard's own `-- TODO: Support potions as well, this won't just be equipslot` at `:1018`, i.e. **the item path is explicitly unfinished**. |
| `buffSlot` | `luaIndex?` | the aura slot for the item's buff half `[T1 src @12.1.0: CooldownViewerItemData.lua:274, defaulting to 1]`. |
| `isInvisible` | `bool` | a row the settings UI filters out, gated on the constant `CDM_HIDE_INVISIBLE_ITEMS` `[T1 src @12.1.0: CooldownViewerSettingsDataProvider.lua:253-254; CooldownViewerSettings.lua:49-50]`. **A third suppression mechanism**, distinct from `HideByDefault` (§1.2) and from `isKnown`. |

⚠ **`isInvisible` is a fourth way for a row to exist and not be there**, on top of
§1.2's `HideByDefault`, `isKnown = false`, and never having been laid out. §1.2's
warning — that a consumer latching off the alert channel is blind to unbound rows and
gets no error saying so — now has one more source. `@verify-ingame` — nothing here
has been observed in a client.

⚠ **An `EquipSlot*` row's value does NOT come from `C_Spell.GetSpellCooldown`.** It
comes from `GetInventoryItemCooldown`, a different API on a different key. §3's value
cascade was derived on spell-backed rows only and **was not re-derived** for the item
path. Treat §3 as describing tab-1 spell rows. `@verify-ingame`

### 1.4 Group buffs — a third display mode that is not a row family (12.1.0)

`GroupBuff` (category 4) is in the enum but in **neither** display mode's category
list (§1). Its mode, `["groupBuffs"]`, maps to the empty set and is served by a
dedicated filter UI — `GroupBuffFilter.lua/.xml`, new files in the addon, refreshed
via `self.GroupBuffFilter:Refresh()` when that mode is selected
`[T1 src @12.1.0: CooldownViewerSettings.lua:1522, :1547-1549]`.

The player-facing feature is a healer tool: assign visual alerts to specific group-buff
spells, and hide chosen buffs from raid frames
`[T1 game: 12.1 content update notes, via `_meta/changelog-12.1.md`]`.

**The addon-facing surface is new and small:**

- **`C_CooldownViewer.GetGroupBuffItems() -> groupBuffItems: GroupBuffItem[]`**
  `[T1 docs @12.1.0: CooldownViewerDocumentation.lua:43-50]`. The struct is
  `{ spellID: number, name: cstring, iconID: fileID, flags: GroupBuffItemFlags,
  isKnown: bool }` `[:148-159]` — note it is **not** a `CooldownViewerCooldown` and
  carries **no `cooldownID`**, so the five-rung identity ladder of §2 does not apply
  to it. It is a flat spell list, keyed by `spellID`.
- **Four new `C_UnitAuras` functions** — `GetGroupBuffVisualAlerts` /
  `SetGroupBuffVisualAlerts`, `GetHiddenGroupBuffs` / `SetHiddenGroupBuffs`
  `[T2 wiki: Patch 12.1.0/API changes §Global API/Added, revid 6801760, 2026-08-09]`.
  Both getters return `NeverSecretContents` tables — `visualAlerts` of
  `GroupBuffVisualAlertInfo` and `spellIDs` of `number`
  `[T1 docs @12.1.0: UnitAuraDocumentation.lua:521, :532]`, which is worth noting
  against §4.7 of `security-taint-and-restricted-data`: **these two survive the 12.1.0
  aura seal**, because they are configuration rather than aura state.
- **Two new events** — `GROUP_BUFF_VISUAL_ALERTS_CHANGED` and
  `HIDDEN_GROUP_BUFFS_CHANGED` `[T2 wiki: same page §Events/Added]`. Config-changed
  notifications, in the same spirit as §4's `TRAIT_CONFIG_UPDATED`: a hint to re-poll.
- Four `CooldownManagerLayout_*` globals wrap the same four setters/getters
  `[T2 wiki: same page §FrameXML/Added]`.

`@verify-ingame` — none of this has been run. In particular, whether a `GroupBuff` row
ever produces an item frame in a viewer (as opposed to living only in the settings
filter) is **unestablished**; the empty category list for its display mode suggests
not, but that is an inference from one snippet.

---

## 2. Identity — five rungs, one pool

`GetSpellID()` returns on the first non-nil rung `[T1 src: .../CooldownViewerItemData.lua:174-196]`:

1. `GetAuraSpellID()` — the bound live aura
2. `cooldownInfo.linkedSpellID` — the elected variant
3. `cooldownInfo.overrideTooltipSpellID`
4. `cooldownInfo.overrideSpellID`
5. `cooldownInfo.spellID` — the base

**Rungs 1–3 all draw from the same pool**: the row's static `linkedSpellIDs` list.
They are not three tiers of one test — they are three different questions with three
different lifetimes. Blizzard's own comment on rung 3 confirms the shared pool:
*"Override tooltip spell even if the linked spell is not active, it will always be one
of the associated linkedSpellIDs"* `[T1 src: ItemData.lua:167-172]`.

| Rung | Question | Stored on | Lifetime |
|---|---|---|---|
| 1 `auraSpellID` | which **live aura instance** is this frame bound to *right now*? | **the item frame** | ephemeral — dies with the aura |
| 2 `linkedSpellID` | which candidate is the **currently relevant variant**? | the shared config record | **sticky** — outlives the aura |
| 3 `overrideTooltipSpellID` | which candidate is the **permanent stand-in**, live or not? | the shared config record | static, DB2-authored |
| 4 `overrideSpellID` | has something **replaced this button wholesale**? | the shared config record | set/cleared by the override event |
| 5 `spellID` | what was this row **configured as**? | the shared config record | static |

> ⚠ **`overrideSpellID` is ALWAYS populated — it mirrors `spellID` when nothing is
> overridden, and is never nil.** `[client 2026-08-06]` (cap v0.2.0 `bind` capture,
> **200/200 rows** carried the field, across Destruction + Demonology Warlock and
> Retribution Paladin, both Warlock hero trees).
>
> Two consequences, and the first is a trap:
>
> 1. **`overrideSpellID ~= nil` does not mean "this row is overridden."** The only
>    honest test is `overrideSpellID ~= spellID`. A consumer writing
>    `local id = info.overrideSpellID or info.spellID` gets the right answer by
>    accident — the two are equal in the un-overridden case — but reads as though the
>    override were the exception, and any code that *branches* on the override being
>    present is wrong on every row.
> 2. **Rung 5 of `GetSpellID()` is therefore unreachable** if the same record backs it,
>    since rung 4 can never be nil. *Inferred from the info table, not measured on
>    `GetSpellID()` directly* — the capture read `GetCooldownViewerCooldownInfo`.
>
> The five genuine overrides in that capture, for contrast: 686 Shadow Bolt → 29722
> Incinerate, 348 Immolate → 445468 Wither (Hellcaller), 85256 Templar's Verdict →
> 383328 Final Verdict, 35395 Crusader Strike → 404542 Crusading Strikes, 31884
> Avenging Wrath → 462048.

> ⚠ **`overrideSpellID` IS the in-combat display-identity route, and it is the only one.**
> `[client 2026-08-06]` — 21 rows, 5 in-combat runs, **plain on 21/21 in every run**, while
> `item:GetSpellID()` refused on a different 1–3 rows each time (§4).
> ⚠ **Evidence gone** — that lab run is off the ring and no surviving extract holds it; the
> recorded per-row values survive only as a transcription in this subtree's queue, which is
> the archive of record for it. The same applies to the Tier-2 `GetSpellID()` row in §7.
>
> It clears both halves of the bar, which matters because a widget read that is merely
> *readable* can still be a constant:
>
> - **It reads.** No refusal on any row, on any run, in restricted combat.
> - **It discriminates.** It was observed **moving mid-pull** where the out-of-combat bind
>   had it equal to `spellID`: cid 135056 Grimoire `1276452 → 132411` in 3 of 5 runs, cid
>   2425 Command Demon `119898 → 119914` in 3 of 5. So the field carries the **live**
>   override, not only the permanent spec/hero one — one field, both lifetimes.
>
> ⚠ **The consequence for a consumer that binds out of combat**: an out-of-combat read
> gives the ability's *resting* identity, so a transform is invisible to it. A transforming
> ability needs the struct re-read in combat, on the cooldownID, and compared against the
> base — `overrideSpellID ~= spellID`, which is the same honest test as above.
>
> ⚠ **`132411` and `119914` do not resolve in the static Game Data namespace.** When it and
> the running client disagree about an id, the client wins.

### 2.1 `linkedSpellIDs` (plural) vs `linkedSpellID` (singular)

- **`linkedSpellIDs`** is the *static candidate pool* from DB2 — always present as a
  table, frequently empty, hard-capped at **4**
  (`COOLDOWN_VIEWER_LINKED_SPELLS_SIZE`)
  `[T1 src: Blizzard_APIDocumentationGenerated/CooldownViewerConstantsDocumentation.lua]`.
  It never itself becomes the identity.
- **`linkedSpellID`** is the *elected* one, and is nil until something elects it.

### 2.2 Rung 2 has two election paths — only one involves an aura

**Path A — aura.** `RefreshLinkedSpell` walks `scanUnits` and calls
`FindLinkedSpellForCurrentAuras(unit)`, which requires a candidate's aura to be live
**and** `auraData.sourceUnit == "player"`
`[T1 src: ItemData.lua:12-23, :25-43]`. When this path fires it calls
`SetAuraInstanceInfo(auraData)` in the same breath — i.e. **it sets rung 1 too**,
which is exactly why rung 2 so rarely wins on its own.

**Path B — cooldown event.** `UpdateLinkedSpell(spellID)` runs from
`NeedsCooldownUpdate` on every `SPELL_UPDATE_COOLDOWN` carrying a spellID
`[T1 src: CooldownViewer.lua:381-390; ItemData.lua:126-150]`. It performs
**no aura query, no cooldown query and no sourceUnit check** — it is a
`tContains(linkedSpellIDs, spellID)` test on the *incoming event payload*:

- incoming spellID is in the pool → elect it
- incoming spellID is the base → clear the election

> **Common misreading:** that rung 2 "checks which linked spell you can cast", e.g. by
> querying cooldowns to see which variant you are talented into. It does not. The
> election is a **side effect of whatever the client happened to send a cooldown update
> for.** If no event ever names a candidate, path B never elects it, talented or not.

### 2.3 The asymmetry that makes rung 2 sticky

```lua
function CooldownViewerItemMixin:OnUnitAuraRemovedEvent()
	if self:GetAuraSpellID() == self:GetLinkedSpell() then
		self:SetLinkedSpell(nil);
	end
	self:ClearAuraInstanceInfo();
	self:RefreshData();
end
```
`[T1 src: CooldownViewer.lua:194-202]`

Rung 1 is **always** cleared. Rung 2 is cleared **only if it was the same spell.** A
link elected through path B therefore survives auras coming and going indefinitely.
That is the point of having both: one tracks the live application, the other remembers
which variant you are playing.

### 2.4 Why rung 1 looks like a superset of rung 2

Because its match set *is* one. Rung 2's election considers only `linkedSpellIDs`, but
rung 1 binds via `SpellIDMatchesAnyAssociatedSpellIDs`, which tests the aura, the
elected link, `overrideTooltipSpellID`, `overrideSpellID`, the base **and every pool
candidate** `[T1 src: ItemData.lua:200-229]`. So rung 1 can bind to the base spell's
own aura, which is never in the pool.

The resolution of the apparent paradox is lifetime, not scope: rung 1 matches the most
and **holds nothing**.

### 2.5 What `self.auraSpellID` actually is

Not a spell setting — a **binding to one specific aura application**. Written by
`SetAuraInstanceInfo(auraData)` together with `auraInstanceID`
`[T1 src: ItemData.lua:243-254]`, after which the frame registers itself in the
viewer's `auraInstanceIDToItemFramesMap` so `UNIT_AURA` deltas route *directly to that
frame* rather than fanning out `[T1 src: CooldownViewer.lua:282-292, :1628-1668]`.

**Why it is the only rung on the frame:** because `cooldownInfo` is not on the frame
either. It comes from `GetCooldownInfoForID`, which returns
`displayData.cooldownInfoByID[cooldownID]` — the settings data provider's **single
cached record per cooldownID**, handed to whichever frame binds that id
`[T1 src: CooldownViewerSettingsDataProvider.lua:242-246; CooldownViewerItemData.lua:46-47]`.
So `SetOverrideSpell` and `SetLinkedSpell` **mutate shared, durable state**. An
aura-instance binding is neither shared nor durable.

> `[client 2026-07-31]` (a census of 72 cooldownIDs on a Destruction Warlock, both hero
> trees, in and out of combat). Two separate answers:
>
> - **Rung 4 (`overrideSpellID`) DOES carry into a fresh read.** cid 164597 Immolate reads
>   `overrideSpellID = 445468` (Wither) on Hellcaller and `348` on Diabolist, from a plain
>   `GetCooldownViewerCooldownInfo` — and `item:GetSpellID()` agrees. So the hero-talent
>   variant is delivered by rung 4, not by the linked-spell election.
> - **Rung 2 (`linkedSpellID`, singular) is NOT in a fresh read — and was never elected at
>   all.** 0 of 72 rows carried it; 19 carried a non-empty `linkedSpellIDs` pool. And
>   `item:GetLinkedSpell()` returned `nil` on every frame too, so this is not a
>   struct-vs-frame divergence: on this character nothing ever ran the election (§2.2
>   path B needs a `SPELL_UPDATE_COOLDOWN` naming a pool candidate).
>
> The practical rule: **read the override from the struct, and do not build on the elected
> link** — it may simply never be set.

### 2.6 The aura scan

`scanUnits = { "player", "target" }`, in that order, first hit wins
`[T1 src: ItemData.lua:1]` — **a self-buff shadows a target debuff on the same row.**
The filter is chosen by *friendliness*, not intent:

```lua
if UnitExists(unit) and UnitIsFriend("player", unit) then
    return "HELPFUL|PLAYER|INCLUDE_NAME_PLATE_ONLY";
end
return "HARMFUL|PLAYER";
```
`[T1 src: ItemData.lua:352-364]`

The `|PLAYER` component is what keeps another player's identically-named DoT off your
row. Note also that `IsAuraActive` treats `expirationTime == 0` as **infinite**, not
expired `[T1 src: ItemData.lua:381-383]`, and that `CanUseAuraForCooldown` (the
`HideAura` flag) gates only whether an aura may drive the *value* — it does not stop
the aura taking the identity rung `[T1 src: ItemData.lua:419-426]`.

### 2.7 Worked example — Destruction's Immolate `[client]`

**`CooldownSetSpell.ID` is the runtime `cooldownID`**, so the DB2 joins directly to
what the client hands you. Immolate is two rows:

| cooldownID | Category | Base (rung 5) | Pool (rungs 1–3) |
|---|---|---|---|
| **164597** | 0 · Essential | `348` Immolate — *the cast* | `157736` Immolate, `445474` Wither |
| **133441** | 2 · TrackedBuff (`HideByDefault`) | `157736` Immolate — *the DoT* | `445474` Wither |

`[T1 db2: CooldownSetSpell + CooldownSetLinkedSpell @ 12.0.7]`

Two things this makes concrete:

1. **The pool is not primarily about hero-talent variants.** Even with Hellcaller out
   of the picture, the cast (`348`) and the DoT it applies (`157736`) are *different
   spellIDs*. A spell→aura mapping has to exist regardless; Wither is one extra entry
   in a list that was already required.
2. **`445474` Wither is the pool/aura id only — the cast is a different id.** The DB2 shape
   is ambiguous here: `445474` appears as a candidate in both a cast-based row and an
   aura-based row, which reads as one spellID doing both jobs. It is not.
   `[client 2026-07-31]` the live `overrideSpellID` on cid 164597 for a Hellcaller build is
   **`445468`** (the cast), while `445474` is the pool/aura id — two ids, mirroring
   Immolate's 348 / 157736.

`[client 2026-07-30]` Those two cooldownIDs are the exact pair in the captured same-frame
pandemic tie — `OnAuraRemoved` + `OnAuraApplied` on cid `133441` **and** `164597`, all at
`131184.611` (§5.4).

**Rung 3 in Warlock terms:** 8 rows carry the `UseAsTooltip` flag
(`Enum.CooldownSetLinkedSpellFlags.UseAsTooltip`), e.g. cid `182891` Grimoire: Imp Lord
→ tooltip `1288945` Imp Lord. A rung-3 candidate displays **even with nothing live**,
which is what separates it from rung 2.

### 2.8 A row's base spellID can be a spell the character does not have

Two facts `[client 2026-07-30]` (one Destruction Warlock, Hellcaller **and** Diabolist)
that between them break the naive "walk the set, key by `spellID`"
reading of the CDM database. ⚠ **Evidence gone** — the decision-log capture behind this
whole subsection is off the ring with no surviving extract; re-checking means re-flying.

**One ability can occupy two cooldownIDs carrying different spellIDs.** Immolate appears as
`cid 133441 → spellID 157736` (the DoT **aura** id, on the Buff-bar viewer) *and*
`cid 164597 → spellID 348` (the **cast** id, on Essential) — see §2.7 — and **both raise
`PandemicTime`** (§5.4). Keying an ability by a single "the" spellID is unsafe: the pressable
row and the aura row disagree, and which one a consumer sees depends on which viewer it
walked.

**And a row's base spellID can be a spell the spec does not even have.** Destruction's set
carries `cid 66181 → spellID 686` (**Shadow Bolt**) with its display overridden to
**Incinerate `29722`** — an id that appears in `CooldownSetSpell` for *no* set at all
`[T1 db2: CooldownSetSpell @ 12.0.7]`. The same character, in one session, read that entry
`isKnown = false` on **Hellcaller** (Blizzard drew nothing) and `isKnown = true` on
**Diabolist** (Blizzard drew an Incinerate icon) `[client 2026-07-30]`. Three consequences
for anyone walking the CDM database:

1. **"Is ability X on screen?" is not answerable from base spellIDs.** It has to union each
   row's `spellID` with its `overrideSpellID` / `overrideTooltipSpellID` / resolved live id.
   Keying only by base reports Incinerate as absent while Blizzard is visibly drawing it.
2. **Use the STATIC override fields, not just the live one, for that test.** While a
   transform is armed the live id becomes the transform's (here Infernal Bolt `433891`), so
   a live-id-only check flickers false exactly when the ability is most active.
3. **`isKnown = false` is not stable across a spec's hero trees**, so a set read once at
   login can be wrong after a talent swap. `SPELLS_CHANGED` is the invalidation signal.

`COOLDOWN_VIEWER_SPELL_OVERRIDE_UPDATED` **fires for such an entry**, including when the
overridden display is a spell with no `CooldownSetSpell` row of its own — observed as the
Diabolist Demonic-Art transform arming on `cid 66181` (114 of 137 logged decision changes
carried an armed Art) `[client 2026-07-30]`. So the override channel is usable for abilities
the Cooldown Manager does not otherwise track.

---

## 3. The value cascade — what the dial means

### 3.1 Tab 1 — all four sources run, later ones overwrite

```lua
function CooldownViewerCooldownItemMixin:CacheCooldownValues()
	local timeNow = GetTime();
	self:CheckCacheCooldownValuesFromCharges(timeNow);
	self:CheckCacheCooldownValuesFromSpellCooldown(timeNow);
	self:CheckCacheCooldownValuesFromAura(timeNow);
	self:CheckCacheCooldownValuesFromEditMode();
	...
```
`[T1 src: CooldownViewer.lua:956-984]`

This is **not** first-match-wins. Each source may write, and each records itself via a
`wasSetFrom*` flag:

| Order | Source | Guard | Colour written |
|---|---|---|---|
| 1 | charges `[:864]` | only if `cooldownStartTime > 0 and currentCharges > 0` | `ITEM_COOLDOWN_COLOR` + draw-edge |
| 2 | spell cooldown `[:908]` | **skipped** if `HasVisualDataSource_Charges()` | `ITEM_COOLDOWN_COLOR` |
| 3 | totem, else aura `[:816]` | totem early-returns before the aura lookup | `ITEM_AURA_COLOR` |
| 4 | edit mode `[:939]` | only if no spell source wrote | — |

The aura branch is the one that surprises: it **overwrites** whatever the cooldown
branch just wrote — *"If the spell results in a self buff, give those values precedence
over the spell's cooldown until the buff is gone"* `[T1 src: :819]` — and it
deliberately does **not** check the charges flag, so a charged aura-applying ability
keeps its charge *count* while losing its charge *swipe* `[T1 src: :840-841]`.

The two colours are the only on-screen tell:
`ITEM_AURA_COLOR = CreateColor(1, 0.95, 0.57, 0.7)` (pale gold) vs
`ITEM_COOLDOWN_COLOR = CreateColor(0, 0, 0, 0.7)` (black)
`[T1 src: CooldownViewer.lua:55-56]`.

### 3.2 Tab 2 — first match wins, and there is no cooldown rung

```lua
function CooldownViewerBuffItemMixin:GetCooldownValues()
	-- totemData -> auraData -> editMode -> zeros
```
`[T1 src: CooldownViewer.lua:1208-1233]`

A tab-2 row **structurally cannot display a spell cooldown.** With no aura and no
totem it has nothing to show, and `ShouldBeActive` turns it off.

### 3.3 Charges use a different identity ladder

```lua
function CooldownViewerItemDataMixin:GetSpellChargeInfo()
	-- To ensure that charges work correctly for cooldown items that are actively cast,
	-- apply auras, and have charges only check the override or base spell ids.
	local chargeSpellID = info.overrideSpellID or info.spellID;
	return C_Spell.GetSpellCharges(chargeSpellID);
```
`[T1 src: ItemData.lua:282-296]`

`overrideSpellID or spellID` — **rungs 4 and 5 only**, skipping the aura and linked
rungs that `GetSpellID()` would have taken. Two ladders on one row, and Blizzard
comments the reason. A consumer reading charges off the display identity is reading a
different spell than the client is.

Separately, the number rendered in `ChargeCount` is not always charges: when
`maxCharges <= 1` it falls back to `C_Spell.GetSpellCastCount` — *"'cast count' (also
called 'use count')"* `[T1 src: CooldownViewer.lua:997-1013]`.

---

## 4. When it runs

Mostly event-driven, with two per-frame exceptions. **Nothing is registered while a
viewer is hidden** — every event in §5 is registered in `OnShow` and dropped in
`OnHide` `[T1 src: CooldownViewer.lua:1554-1580, :1944-1962]`.

| Trigger | Cadence | Effect |
|---|---|---|
| Viewer `OnEvent` `[:1590]` | event | Fans out to **every active item frame**; each runs a `Needs*Update` predicate and calls `RefreshData()` only on a match. One event is N predicate tests, not N re-resolves. |
| `RefreshData()` `[:1136]` | on match | The full re-resolve: `ClearVisualDataSource` → `RefreshAuraInstance` → charges → cooldown → texture → desaturation → colour → border → overlay glow → active. |
| Viewer `OnUpdate` `[:1622]` | **every frame** | Wired via `<OnUpdate method="OnUpdate"/>` `[T1 src: CooldownViewer.xml:289]`. Fans out to each item's `OnUpdate` `[:89]`, which does **no re-resolution** — it only checks four time-based alert triggers: Available, PandemicTime, the pandemic display state, ChargeGained. **The alerts are polled; identity is not.** |
| **BuffBar** item `OnUpdate` `[:1360]` | **every frame** | The exception. A TrackedBar item additionally calls `RefreshActive()` then either `Clean()` (a full `RefreshData`) or `RefreshCooldownInfo()`, which re-reads `GetAuraData()`. **Bar rows re-scan auras every frame; icon rows do not.** |
| `MarkDirty` / `Clean` `[:113-126]` | deferred | A buff item discovering a re-link during `ShouldBeActive` marks itself dirty rather than re-resolving inline `[:1194]`. |
| `UNIT_AURA` full update | bulk | `isFullUpdate` short-circuits per-aura routing and calls `RefreshLayout()` on the whole viewer `[T1 src @12.1.0: CooldownViewer.lua:1803-1806]` — the heaviest path, the one that re-pools frames, and the one that reaches **in combat** (§4.1). |

> ⚠ **`TRAIT_CONFIG_UPDATED` fires BEFORE the CDM rebuilds its set — a hero-tree swap
> settles over two events and ~5 s.** `[client 2026-08-06]` (cap v0.2.0 `bind` capture,
> Destruction Warlock, Diabolist ⇄ Hellcaller). At `TRAIT_CONFIG_UPDATED` the talent API
> already answered **Hellcaller** while the viewers still returned the **Diabolist** row
> set; `SPELLS_CHANGED` **4.7 s later** carried the new rows (26 → 25, and Immolate's row
> picked up its Wither override). Measured in both directions.
>
> An addon that re-reads its identity on `TRAIT_CONFIG_UPDATED` alone therefore binds the
> **old rows under the new tree label** and stays that way until something else fires. The
> mitigation is the one §5 already implies — treat every one of these events as a hint and
> re-poll on all of them, never trust a single event to mean "the set is now correct."

> ⚠ **Turning the Cooldown Manager OFF in Options fires NONE of the CDM/talent events —
> an addon watching only those never learns the player disabled it.**
> `[client 2026-08-06]` (cap v0.2.0 `bind` capture). The player unchecked the enable box,
> the viewers visibly disappeared, the box was re-checked — and across **5.7 minutes** the
> addon logged **zero** samples. Nothing woke it, off or back on.
>
> The negative is bounded, and precisely: none of `PLAYER_ENTERING_WORLD`,
> `SPELLS_CHANGED`, `ACTIVE_PLAYER_SPECIALIZATION_CHANGED`, `PLAYER_SPECIALIZATION_CHANGED`,
> `TRAIT_CONFIG_UPDATED`, `ACTIVE_COMBAT_CONFIG_CHANGED`, `COOLDOWN_VIEWER_DATA_LOADED`,
> `COOLDOWN_VIEWER_TABLE_HOTFIXED` or `COOLDOWN_VIEWER_SPELL_OVERRIDE_UPDATED` fired.
> *Untested:* `CVAR_UPDATE`, which is the obvious candidate and the first thing to try.
>
> ⚠ **This is a sampling failure, not a detection failure**, and the distinction decides
> the fix. The state was fully observable at the time — §4 records that a hidden viewer
> still returns every item frame, so a poll would have read rows unchanged with the
> viewers' own `IsShown()` false. The verdict was computable and simply never asked for.
> Anything reporting CDM availability therefore needs a trigger it does not currently have;
> adding verdicts is useless without one.

### 4.1 Layout and ordering — what re-anchors an item frame, and when

Everything in this section is a **source read on the 12.1.0 tree**; every locator carries
`@12.1.0` and none of it was measured in the client (§0b). A viewer is a
`GridLayoutFrameMixin`, its item frames are pooled children, and the whole ordering story
runs through one field.

**`layoutIndex` is both the grid sort key and the cooldownID data index — the same
number, doing two jobs.** `CooldownViewerMixin:RefreshLayout` acquires one frame per row
and stamps `itemFrame.layoutIndex = i` `[T1 src @12.1.0: CooldownViewer.lua:2021-2029]`.
`RefreshData` then binds each frame's identity by looking its own index up in the ID list —
`local cooldownID = cooldownIDs and cooldownIDs[itemFrame.layoutIndex]`
`[@12.1.0: :2071-2077]` — while `BaseLayoutMixin:GetLayoutChildren` sorts the children with
`LayoutIndexComparator` before returning them `[@12.1.0: Blizzard_SharedXML/LayoutFrame.lua:58-68,
the sort at :64; the comparator at :44-56]`.

> ⚠ **Therefore rewriting `layoutIndex` to reorder a row self-cancels.** Both the position
> *and* the identity follow the index, so two frames given each other's indices swap their
> cooldownIDs on the next `RefreshData` as well as their slots: the icons trade places and
> trade contents, and the row looks unchanged. Duplicate values are worse than useless —
> the comparator raises `GMError` naming both frames
> `[@12.1.0: LayoutFrame.lua:45-53]`. **A positional reorder has to be `ClearAllPoints()` +
> `SetPoint()` on the frame**, leaving `layoutIndex` alone.

**`GetItemFrames()` answers in `layoutIndex` order, not in drawn order.** It is
`GetItemContainerFrame():GetLayoutChildren()` and the container is the viewer itself
`[@12.1.0: CooldownViewer.lua:1632-1639]` — so it returns Blizzard's *intended* order, and a
`SetPoint` re-anchor is invisible to it. A consumer that derives "which row is leftmost"
from the `GetItemFrames()` index is reading intent; drawn position comes from
`GetLeft()` / `GetTop()` on the frame, and nowhere else.

**`alwaysUpdateLayout` is set once and never cleared, so there is no quiet layout.**
`RefreshLayout` sets `itemContainerFrame.alwaysUpdateLayout = true`
`[@12.1.0: CooldownViewer.lua:2036]` — Blizzard's own comment says it is needed for icon-scale
changes, which do not otherwise dirty the layout — and `GridLayoutFrameMixin:ShouldUpdateLayout`
early-returns `true` whenever it is set `[@12.1.0: LayoutFrame.lua:589-596]`. From the first
`RefreshLayout` onward, **every** `Layout()` call re-anchors **every** child unconditionally.
The "nothing changed, skip it" early-out that the rest of `ShouldUpdateLayout` implements is
unreachable on a CDM viewer.

**`RefreshLayout` is the destructive path, and it is reachable in combat.** Its first act is
`self.itemFramePool:ReleaseAll()` `[@12.1.0: CooldownViewer.lua:2022]`; the pool's reset
callback is `Pool_HideAndClearAnchors` plus `itemFrame.layoutIndex = nil`
`[@12.1.0: :1642-1646]`, and `Pool_HideAndClearAnchors` calls `Hide()` **and
`ClearAllPoints()`** `[@12.1.0: Blizzard_SharedXMLBase/Pools.lua:519-522]`. So a
`RefreshLayout` discards every anchor a rider ever set. Its callers:

| Caller | Locator `@12.1.0` | Reaches combat? |
|---|---|---|
| `CooldownViewerMixin:OnShow` | `CooldownViewer.lua:1740` | on show |
| `CooldownViewerMixin:SetIsEditing` | `:1929` | Edit Mode only |
| `OnCooldownDataChanged`, else-branch | `:2017` | on a settings/layout change |
| **`OnUnitAura`, `isFullUpdate` branch** | **`:1803-1806`** | **yes** |

The last one is the one that matters, and it is **broader than "the player's auras changed"**:

```lua
function CooldownViewerMixin:OnUnitAura(_unit, unitAuraUpdateInfo)
	CooldownViewer_MarkAuraCacheDirty();

	if not unitAuraUpdateInfo or unitAuraUpdateInfo.isFullUpdate then
		self:RefreshLayout();
		return;
	end
```
`[T1 src @12.1.0: CooldownViewer.lua:1800-1806]`

- **The unit is discarded.** `OnShow` registers `RegisterUnitEvent("UNIT_AURA", "player",
  "target")` `[@12.1.0: :1733]` and the handler names its first parameter `_unit` — Blizzard's
  own unused-parameter convention. There is no filter, so **a full aura update on your target
  rebuilds the whole layout**, even though no target aura affects the viewer. Contrast
  `AuraFrameEventListenerMixin` in `BuffFrame.lua`, which gates the same event on
  `unit == PlayerFrame.unit` `[@12.1.0: BuffFrame.lua:294]`. The CDM is strictly more
  trigger-happy than the buff frame.
- **A nil payload counts too** — `if not unitAuraUpdateInfo or …`. Any `UNIT_AURA` arriving
  without update info is a teardown.
- **`PLAYER_TARGET_CHANGED` is registered but is *not* one.** It routes to
  `OnPlayerTargetChanged` → `RefreshActiveFramesForTargetChange`
  `[@12.1.0: CooldownViewer.lua:1777, and the method just below OnUnitAura]`, which never touches
  the layout. Swapping targets is not itself destructive; whatever aura full-update accompanies
  acquiring a new unit is.

> ⚠ **What sets `isFullUpdate` is not in the Lua.** It arrives already decided in the payload —
> `UnitAuraUpdateInfo.isFullUpdate` is declared a non-nilable bool defaulting false
> `[T1 src @12.1.0: UnitConstantsDocumentation.lua:59]` — and no consumer in the shipped UI
> documents the condition
> `[searched 2026-08-16: every isFullUpdate reader in wow-ui-source-12.1.0 — Blizzard_AuraContainer,
> Blizzard_NamePlates, Blizzard_PrivateAurasUI, Blizzard_BuffFrame, PartyMemberFrame,
> DemonHunterSoulFragmentsBar, EvokerEbonMightBar, SharedXML]`; the only remark is
> `ManagedAuraContainer.lua:333` on deferring rebuilds. **The rate of this teardown is therefore
> not answerable by source reading and needs measurement.**

**Anything that anchors, parents or decorates an item frame must be able to re-apply itself
after an arbitrary mid-combat teardown**, and must not assume its anchors survived.

**A same-count settings change does not disturb anchors.** `OnCooldownDataChanged` compares
`self.itemFramePool:GetNumActive()` against the new item count and takes an in-place
`RefreshData(cooldownIDs, forceSet)` path when they match, calling `RefreshLayout` only
otherwise `[@12.1.0: :2007-2019]`. Blizzard's comment states the intent: *"If the frame count
hasn't changed, update cooldown data in-place without releasing and re-acquiring frames or
re-running the layout engine."* So a row swapped for another row keeps every frame, every
anchor and every index; only the *count* changing is destructive.

**Cooldown start and end do not re-run the layout at all.** `SPELL_UPDATE_COOLDOWN`,
`SPELL_UPDATE_USES`, `SPELL_UPDATE_USABLE`, `SPELL_RANGE_CHECK_UPDATE` and the two
`SPELL_ACTIVATION_OVERLAY_GLOW_*` events are handled by `CooldownViewerCooldownMixin:OnEvent`,
which does nothing but fan each one out to `itemFramePool:EnumerateActive()`
`[@12.1.0: CooldownViewer.lua:2167-2200]`. Frames do not move because an ability came off
cooldown.

**An inactive row keeps its grid slot; the row gaps rather than closing up.** All four item
templates set `includeAsLayoutChildWhenHidden="true"`
`[@12.1.0: CooldownViewer.xml:24, :93, :162, :213]`, and `BaseLayoutMixin:AddLayoutChildren`
admits a child on `region:IsShown() or region.includeAsLayoutChildWhenHidden`
`[@12.1.0: LayoutFrame.lua:38]`. `CooldownViewerItemMixin:UpdateShownState` only calls
`SetShown` `[@12.1.0: CooldownViewer.lua:310-313]` and does not mark the viewer dirty. A row
that goes inactive is hidden in place: it still occupies its cell, and the icons either side
of it do not move.

**The viewer anchors the pandemic state frame ONTO the item frame.**
`CooldownViewerMixin:AnchorPandemicStateFrame` `SetPoint`s the pooled state frame to the
item's `TOPLEFT`/`BOTTOMRIGHT` `[@12.1.0: CooldownViewer.lua:2129-2133]`, and
`BuffBarCooldownViewerMixin` overrides it `[@12.1.0: :2353]`. Consequence: **re-*parenting* an
item frame breaks that anchor chain; re-*anchoring* it does not.**

**On protection, what the XML says and what it does not.** Across
`Blizzard_CooldownViewer/*.xml` the `protected` attribute is **absent** — the four item
templates inherit `CooldownViewerBaseItemTemplate` `[@12.1.0: CooldownViewer.xml:4-10]`,
a plain virtual `<Frame>` carrying three script bindings and no attributes beyond `name`
and `virtual`.

> ⚠ **That settles the declaration, not the runtime.** Whether the client nonetheless
> treats a laid-out CDM item frame as protected by some other route — a secure ancestor,
> a C-side flag, or `CooldownViewerSecure.lua`, which 12.1.0 added (§0b) — is not
> established at any tier here, and the XML cannot settle it.
> `` `@pending-test: cdm-item-frame-protected` `` — `IsProtected()` on a live item frame and
> on the viewer, in and out of combat.

### 4.2 A re-anchor measured, and the limit on how far it was measured

`[client 2026-08-16]` on live 12.1.0.69214, `EssentialCooldownViewer` with 9 active item
frames and a third-party Cooldown Manager re-skin loaded. Method: out of combat every item
frame got `ClearAllPoints()` and a `SetPoint` onto a plain non-secure frame that was **not**
its parent — the frames stayed parented to the viewer — and drawn position was read back
per frame with `GetLeft()` / `GetTop()` against the intended order, with `Layout` and
`RefreshLayout` both hooked.

- **The re-anchor takes effect.** Immediately after the out-of-combat apply the
  left-to-right read-back matched the intended order exactly; the same read before the apply
  gave the viewer's own order. `[client 2026-08-16]`
- **Positions held through combat — in a session where the layout did not re-run, and that
  is the whole claim.** Order still read as intended at combat entry and again at combat
  exit across a 138 s fight, with no frame moving; over that same session neither layout
  hook fired, so the `RefreshLayout` teardown §4.1 describes was not exercised and the
  `UNIT_AURA` `isFullUpdate` path that reaches combat was not among the events sampled.
  Persistence *across* a re-layout is therefore not established by this, and §8's rule 20 —
  assume your anchors are torn down mid-combat — stands unchanged. `[client 2026-08-16]`
- **The per-frame paint is unaffected by the move.** The viewer kept drawing cooldown swipe,
  charges and glow normally on the repositioned frames. `[client 2026-08-16]`
- **Another addon re-anchoring the same frames wins, and the losing signature misleads.**
  In an earlier session on the same login, with a third-party CDM re-skin's cooldown
  override enabled, the read-back never matched the intended order: re-applying at 2 Hz
  left the sampled positions **identical across 35 consecutive samples**, with neither
  layout hook firing in that window `[client 2026-08-16]`. Disabling that override and
  re-arming produced the clean result above, on the same login — so the cause is the
  competitor, not timing. ⚠ **The constant read-back reads like "the apply never landed"
  and is not**: a competitor that wins deterministically every round is caught in *its*
  layout by every sample, so a failed apply and a lost fight are indistinguishable from
  sampled positions alone. What separates them is that no layout hook fired (so Blizzard
  did not move them) plus the disable/re-arm. `[client 2026-08-16]`

---

## 5. Events — and they differ by family

Six registered by the shared viewer mixin
`[T1 src: CooldownViewer.lua:1556-1561]`; **five more by tab 1 only**
`[T1 src: :1948-1952]`; tab 2 adds nothing.

| Event | Family | Effect on the row |
|---|---|---|
| `COOLDOWN_VIEWER_SPELL_OVERRIDE_UPDATED` | both | Writes rung 4, then full `RefreshData`. Fires **redundantly** — Blizzard's own `SetOverrideSpell` early-returns on an unchanged value `[ItemData.lua:88-105]`. |
| `SPELL_UPDATE_COOLDOWN` | both | May re-elect rung 2 (§2.2 path B), then `RefreshData`. ⚠ **Gained an `itemID` payload field at 12.1.0** `[T2 wiki: Patch 12.1.0/API changes §Events/Changed, revid 6801760, 2026-08-09]` — the item half of §1.3's trinket/potion tracking. A handler that positionally unpacks this payload must be re-checked. |
| `UNIT_AURA` | both | Registered `("player", "target")` only. Routed by `auraInstanceID` to exact frames; added-auras fan out to all. ⚠⚠ **At 12.1.0 this payload is FULLY SECRET while auras are restricted** (`security-taint-and-restricted-data.md` §4.7) and the `auraInstanceID` lists lost their `NeverSecretContents` markers. The routing described here is Blizzard's own untainted code and still works; **an addon reproducing it does not.** Every measurement in §5.4 and §7 that reads an `auraInstanceID` was taken on 12.0.7 and is the most likely thing in this file to have been falsified. `@verify-ingame` |
| `UNIT_TARGET` | both | `OnNewTarget` on every frame: clears the link, clears pandemic timing, forces inactive `[:631-638]`. |
| `SPELL_UPDATE_ICON` | both | Texture only — no re-resolve. |
| `PLAYER_TOTEM_UPDATE` | both | Rebinds totem data, which outranks auras in both families. |
| `SPELL_ACTIVATION_OVERLAY_GLOW_SHOW` / `_HIDE` | **tab 1** | The proc glow — §6. |
| `SPELL_UPDATE_USES` | **tab 1** | Recomputes charges only. |
| `SPELL_UPDATE_USABLE` | **tab 1** | Icon colour only. Fires constantly in a city. |
| `SPELL_RANGE_CHECK_UPDATE` | **tab 1** | Out-of-range tint; only for rows whose base spell has a range `[:709-716]`. |

### 5.1 The alert choke point — available on both families

`CooldownViewerItemMixin:TriggerAlertEvent(event)` `[T1 src @12.1.0: CooldownViewer.lua:500-511]`
is called from all six alert paths and is **invoked unconditionally** — the user's
alert configuration is consulted *inside* the body (`self.alertsByEvent[event]`).
So `hooksecurefunc(item, "TriggerAlertEvent", …)` observes **every edge, even for
spells the user has configured no alert on.** Because the methods are `Mixin()`-copied
onto each frame, the hook must go on the item **instance**, not the shared mixin table.

> ⚠ **That completeness guarantee is scoped to BOUND rows.** The hook is per item frame,
> and a `HideByDefault` row never gets one — so it raises no edge at all, silently (§1.2).
> "Every edge" means every edge on the rows the viewers laid out, not every edge the spec's
> abilities could produce.

> ⚠⚠ **AND IT IS FALSE FOR `Available`, WHICH IS GATED ON THE PLAYER'S ALERT CONFIGURATION.**
> `TriggerAlertEvent` is indeed called unconditionally — but only from paths that *run*, and
> the `Available` path is reached from `CooldownViewerItemMixin:OnUpdate`
> `[T1 src @12.1.0: CooldownViewer.lua:54-57]`, which the viewer drives only for frames in
> `itemFramesNeedingOnUpdateMap` `[@12.1.0: :1795]`. Registration is
> `NeedsOnUpdateRegistration()` = `self.pandemicAlertTriggerTime or (self.alertsByEvent and
> next(self.alertsByEvent))` `[@12.1.0: :472-474]`. **So a row the player has configured no
> alert on never ticks, and therefore can never fire `Available`** — regardless of
> `allowAvailableAlert`, which is armed correctly and then simply never examined.
> `OnCooldown` is unaffected: it fires from the data-refresh path `[@12.1.0: :1178-1180]`,
> which runs for every row.
>
> **The channel is therefore ASYMMETRIC**, and a readiness latch built on it is a one-way
> door: rows go not-ready and never come back. `[client 2026-08-16]` Havoc, one pull,
> 9 bound rows: **322 `OnCooldown` across 8 distinct cids, 35 `Available` on exactly ONE
> cid** — the only row with an alert configured. Every other row latched not-ready on its
> first cast and stayed there for the rest of combat.
>
> **The symmetric ready edge is not in this channel at all — it is a widget script.** Every
> tab-1 item wires `self:GetCooldownFrame():SetScript("OnCooldownDone", …)` at `OnLoad`
> `[T1 src @12.1.0: CooldownViewer.lua:725]`, and the engine fires it when the swipe
> completes: no `alertsByEvent`, no `OnUpdate` registration, no player configuration. An
> addon observes it additively with `HookScript`, leaving Blizzard's handler intact.
> `` `@pending-test: cdm-oncooldowndone-fires-without-alerts` ``
>
> `alertsByEvent` is a plain table on the item frame, so a consumer *can* ask which of its
> rows are able to answer. And the direct read
> `CooldownViewerCooldownItemMixin:IsOnCooldown()` `[@12.1.0: :705-707]` —
> `isOnActualCooldown and not IsExpired()` — may be simpler still, but whether it survives
> restricted combat is **unmeasured**: it derives from `spellCooldownInfo.duration`/`endTime`,
> which are secret in combat, so it may hand tainted code a secret boolean rather than a plain
> one. `` `@pending-test: cdm-item-cooldown-flags-secrecy` ``
(The general shape — a choke-point method as a dispatch surface, and `hooksecurefunc` on
it as a runtime signal — is [`api-events-and-discovery`](./api-events-and-discovery.md)
§2.8's claim; this section owns the instance.)

The event argument is `Enum.CooldownViewerAlertEventType`, six members
`[T1 docs: CooldownViewerConstantsDocumentation.lua:43-55]`:

| Value | Member | Raised at | What the edge actually means |
|---|---|---|---|
| 1 | `Available` | `CooldownViewer.lua:518` `@12.1.0` | a cooldown finished — for a charged ability, **once per charge restored**, not once per "became usable" (§5.3) |
| 2 | `PandemicTime` | `:579` `@12.1.0` | a tracked **target** DoT entered its refresh window (§5.2) |
| 3 | `OnCooldown` | `:1179` `@12.1.0` | went on cooldown — but **never fires for a charged ability** (§5.3) |
| 4 | `ChargeGained` | `:632` `@12.1.0` | *one entry in a prediction queue came due*, which is not the same as "+1 charge" (§5.3) |
| 5 | `OnAuraApplied` | `:636` `@12.1.0` | a **fresh** application — not a stack, not a refresh (§5.4) |
| 6 | `OnAuraRemoved` | `:640` `@12.1.0` | the bound aura instance went away (§5.4) |

⚠ **The alert *subsystem* was restructured at 12.1.0** — five `CooldownViewerVisualAlert*`
files removed, `CooldownViewerVisualAlertTarget.lua` and `CooldownViewerEditAlertBase.lua/.xml`
added (§0b). The six **event types** below are unchanged in the generated enum, and
`TriggerAlertEvent` still exists; whether the choke point is still reached by the same
six paths, and whether the pool-enumeration argument of §1.2 still holds, was **not
re-derived**. `@verify-ingame`

**`[client 2026-07-30]` All six fire in restricted combat** (Destruction Warlock, the
alert channel taped end to end). Counts from one ~80 s pull: `ChargeGained`
×10 (Conflagrate), `OnAuraApplied` ×15, `OnAuraRemoved` ×13, `PandemicTime` ×5; `Available`
×7 and `OnCooldown` on four non-charged entries over a longer pull in the same session.
⚠ **Evidence gone.** That capture is off the SavedVariables ring and no extract of it
survives on disk, so these counts stand on what was written down at the time; confirming
them means re-flying the tape.

> ⚠ **`Available` and `OnCooldown` NEVER fire for an ability with no real cooldown** — a second
> silence on top of the alert-configuration gate above, and a different one — and a
> consumer latching readiness off this channel has to know which of its rows are silent.
> `CheckCacheCooldownValuesFromSpellCooldown` arms `allowAvailableAlert` only when
> `duration > MIN_GLOBAL_RECOVERY_TIME` (0.75 s, a file-local constant)
> `[T1 src: CooldownViewer.lua:893, :922]`, and `CheckAllowOnCooldown` `[:895-906]` requires
> the same duration to exceed both the GCD and the previously cached one. That is the gate
> that keeps the global cooldown from being announced as a cooldown — deliberate, and the
> reason a GCD-only row is quiet rather than chattering every 1.5 s.
>
> So a filler, a resource spender or any other no-cooldown press raises **neither edge,
> ever**, and a latch seeded from these alone stays at its initial value for that row for
> the whole session. That must read as *unknown*, not as *ready* or *not ready* — the two
> wrong defaults light or blank a whole roster and both look like a working addon.

**Why this channel matters disproportionately under Secret Values.** The alerts are raised
by Blizzard's *trusted* code from data it can see, and the argument is a plain enum — so the
channel carries information in restricted combat that the corresponding direct API reads
refuse. `ChargeGained` is the sharpest case: `C_Spell.GetSpellCharges` does not hand back a
readable **charge count** in combat (whether the rest of `SpellChargeInfo` seals with it is
unmeasured — §7 Tier 3), so a gain *edge* may be the only in-combat charge information
available at all. This is the
single best in-combat signal on either side of the split, because it is an observation of a
choke point rather than a secret-guarded API read.

> ⚠ **A RE-APPLICATION OF A LIVE AURA RAISES NOTHING** `[client 2026-07-31]`, and this is
> the sharpest limit on the whole channel. Over one Destruction pull: **41 Immolate casts**
> onto a target whose Immolate was already up produced **exactly one `OnAuraApplied`** (the
> first application) and **zero `OnAuraRemoved`**. `PandemicTime` likewise fired **once**
> and never re-armed, though the DoT re-entered its window repeatedly.
>
> So the aura edges describe an aura's **first application and first pandemic entry, then
> silence** for as long as it is maintained. A refresh is not "Removed + Applied" — it is
> *nothing at all*. The same-frame `OnAuraRemoved` + `OnAuraApplied` pair in §5.4 is a
> different event: a genuine re-application after a lapse, not a refresh of a live aura.
>
> **Why it is one-shot, from the source.** `TriggerPandemicAlert` (`:552-555`) clears
> `pandemicAlertTriggerTime` and sets `nextAvailableTimeToPlayPandemicAlert =
> pandemicEndTime`, commented *"Prevent the alert from playing again for this instance"*;
> `ShouldTriggerPandemicAlert` (`:549`) then gates on `timeNow` passing that. Re-arming runs
> through `CheckSetPandemicAlertTriggerTime` (`:511`), which additionally requires
> `GetAuraDataUnit() == "target"`, a live aura, and a positive `carriedOverToNewCast`.
> Both halves observed `[client 2026-07-31]`: `trigger=SECRET / nextAvailable=nil` while
> armed, then `trigger=nil / nextAvailable=SECRET` the instant it fired.
>
> **Consequence: take the edge as a one-shot notification, never as a state.** But there IS
> a state, and it is readable — **`item.PandemicIcon`** (§7 Tier 2). It is recomputed every
> frame and *clears on a refresh*, which is precisely what the edge cannot do.

### 5.2 `PandemicTime` — Blizzard computes the real refresh window, then seals it

This is the alert worth understanding in detail, because it replaces a community rule of
thumb with an exact value. `CheckSetPandemicAlertTriggerTime`
`[T1 src: CooldownViewer.lua:511-531]` does:

```lua
local extendedDuration = C_UnitAuras.GetRefreshExtendedDuration("target", auraData.auraInstanceID, self:GetSpellID());
local baseDuration     = C_UnitAuras.GetAuraBaseDuration("target", auraData.auraInstanceID, self:GetSpellID());
local carriedOverToNewCast = (extendedDuration and baseDuration) and (extendedDuration - baseDuration) or 0;
```

`pandemicStartTime = auraData.expirationTime - carriedOverToNewCast` `[:523]` — i.e. the
window is derived from **how much duration a recast would actually carry over**, per spell
and per current state, not from the community's "30% of base duration" heuristic. Anything
reasoning about DoT refresh should prefer this to its own arithmetic.

Three conditions gate it, all easy to miss:

1. **Target auras only** — `if self:GetAuraDataUnit() == "target" and isActive` `[:515]`. A
   self-buff never gets pandemic state, however long it lasts.
2. **Eligibility is DATA-driven, not a user setting** — `CanTriggerAlertType` resolves
   through `C_CooldownViewer.GetValidAlertTypes(cooldownID)`
   `[T1 src: CooldownViewerItemData.lua:541, 550-553]`, a public documented API
   `[T1 docs: CooldownViewerDocumentation.lua:52-65]`, so an addon can ask ahead of time
   whether a tracked spell will ever produce a pandemic signal. ⚠ This is the **only** path
   in the addon that consults it — the list gates `PandemicTime` and nothing else (§7 Tier 1).
3. **`carriedOverToNewCast > 0`** `[:520]` — no carry-over, no window.

**The window is also parked on the item as state — and an addon cannot read it.**
`item.pandemicStartTime` / `item.pandemicEndTime` are set at `[:534-542]`
(`pandemicEndTime` is the aura's expiration time), re-evaluated every frame from `OnUpdate`
`[:89-98]`, and re-armed by `CheckSetPandemicAlertTriggerTime` on aura updates
`[:208, :859, :1205]`. In restricted combat **both read `SECRET`** `[client 2026-07-30]`,
as does `pandemicAlertTriggerTime` while armed — it reads `nil` once the alert has fired,
cleared at `[:554]`. The `PandemicTime` **alert fires normally** in the same conditions:
the edge survives, the state does not.

`item:IsInPandemicTime(timeNow)` — `pandemicStartTime and timeNow >= pandemicStartTime and
timeNow <= pandemicEndTime` `[T1 src: CooldownViewer.lua:587-589]` — **throws** rather than
returning a secret boolean `[client 2026-07-30]`. The method is **not blocked**: its body
*compares* those two secret fields, and comparing a secret errors. **The guard is therefore
`pcall`, not `issecretvalue`.** Untainted code does the same arithmetic fine; we cannot.

**The design consequence:** an addon can learn *that* a DoT entered its refresh window (the
edge) but cannot ask *how long is left*. Two patterns survive — an **edge-driven latch**
(set on `PandemicTime`, clear on `OnAuraRemoved`/`OnAuraApplied` for the same cooldownID),
and, better, the per-frame readable mirror **`item.PandemicIcon`** (§7 Tier 2), which unlike
the edge also clears on a refresh.

⚠ **Do not read "not populated" from a `nil` here.** The same capture shows `nil` on
non-eligible items and `SECRET` on eligible ones, which is exactly the discrimination that
makes the result meaningful: the fields *are* populated, we are simply not allowed to read
them. An instrument that collapsed `SECRET` into `nil` would have concluded the opposite.
Out-of-combat behaviour is **unmeasured** — every alert in the capture fired in combat.

The visual side is unambiguous regardless: the pandemic FX are real frames
`[T1 src: PandemicAlertAnimation.xml:3 (icon), :47 (bar)]`, and the icon one of them
shows/hides is `item.PandemicIcon` itself.

### 5.3 `ChargeGained` is about CHARGES, not aura stacks — and it over-fires

A natural assumption is that a stacking proc (Demonic Core, Backdraft) would raise
`ChargeGained` as it accumulates. It cannot, and the reason is in the mixin tree:

- `CooldownViewerCooldownItemMixin` `[T1 src: CooldownViewer.lua:678]` — the parent of
  `CooldownViewerEssentialItemMixin` `[:1150]` and `CooldownViewerUtilityItemMixin`
  `[:1153]` — is the **only** owner of `CacheChargeValues` / `SetCachedChargeValues`
  `[:997, :986]`, which is the sole path to `AddChargeGainedAlertTime`.
- `CooldownViewerBuffItemMixin` `[:1157]`, parent of the BuffIcon `[:1245]` and BuffBar
  `[:1318]` items, derives from `CooldownViewerItemMixin` **directly** and never picks up
  that mixin. A tab-2 entry therefore has no charge-caching code at all.

What the count actually reads, in precedence order `[T1 src: CooldownViewer.lua:997-1016]`:
`GetSpellChargeInfo()` when `maxCharges > 1` (real charges) → else
`C_Spell.GetSpellCastCount(spellID)`, the "cast count" / "use count" (Blizzard's own
comment: *"can have different meanings based on the context of the spell"*) → else unchanged
and hidden. The alert then fires on any **increase** of that cached value
(`previousCooldownChargesCount < cooldownChargesCount` `[:992-994]`).

❗ **But `ChargeGained` is not "one charge was gained".** It is *"one entry in a prediction
queue came due"*, and the difference is load-bearing for anyone counting charges off it
`[client 2026-07-31]` + T1 src: ⚠ **the measured half's capture is gone** — off the ring,
no surviving extract — though the source read below stands on its own and is re-checkable.

- `AddChargeGainedAlertTime(predictedChargeCount, predictedChargeGainTime)` `[:591-594]`
  writes into `chargeGainedAlertTimes`, a table **keyed by predicted charge count**.
- **Two independent producers write it.** A *predictor* —
  `CheckCacheCooldownValuesFromCharges` `[:886]` registers `currentCharges + 1` at a
  **future** timestamp on every refresh while a recharge is running — and an *observer*,
  the `SetCachedChargeValues` path above, which registers the new count at `GetTime()`.
- `ShouldTriggerChargeGainedAlert` `[:596-605]` drains **at most one due entry per call**
  (it `return`s on the first hit) and is polled once per frame from `OnUpdate` `[:100-101]`.

So a backlog of two due entries fires as **two alerts on consecutive frames**, and one real
charge restore can raise the alert twice. Measured on Conflagrate: a `0 → 1 → 2` climb in
**200 ms**, plus credits 1.9 s and 4.0 s apart on an ability whose recharge is several
seconds. **A consumer that credits `+1` per alert overcounts** — it claims a charge the
player does not have and cues a press that fails.

It errs the other way too: `OnCooldownIDCleared` `[:722]` nils
`previousCooldownChargesCount`, so `considerAddingAlert` is false on the next set and the
first rise after **any** re-resolve is swallowed.

**The workable rule:** treat the alert as *"the count may have risen"*, and bound credits by
a **gain floor** — a charge cannot return faster than its recharge. `C_Spell.GetSpellCharges`
exposes `cooldownDuration` **out of combat**, and that is the only source for the number.
Seed the floor OOC, refuse a second credit inside it, and the cases you get wrong (a genuine
cooldown-reset proc) bias toward **under**counting, which is the safe direction.

❗ **A CHARGED ABILITY NEVER RAISES `OnCooldown`** `[client 2026-07-30]`. Conflagrate
(`cid 18860`) advertises `Available, OnCooldown, ChargeGained` in `GetValidAlertTypes`, and
across a ~190 s pull it raised **`Available` ×7 and `OnCooldown` ×0** — while four
non-charged entries in the same capture (`18800`, `18812`, `18814`, `33527`) raised
`OnCooldown` normally. `Available` fires **once per charge restored**, not once per "the
ability became usable".

The consequence for anyone building readiness on these edges: an `Available`/`OnCooldown`
pair is **not a complete state machine for a charged ability** — the "on" edge never
arrives, so a latch built from them reads *ready* forever after the first charge comes back,
including at zero charges. Readiness for a charged spell has to come from the charge count
(`ChargeGained` + a seeded baseline, since `C_Spell.GetSpellCharges` yields no readable
**charge count** in combat), not from the cooldown edges.

⚠ And the obvious fallback does not work either: a charged spell's cooldown often lives on
its **charge category**, not the spell. Conflagrate `17962` has `RecoveryTime = 0` with
`ChargeCategory = 672` `[T1 db2: SpellCooldowns, SpellCategories @ 12.0.7]`, so
`GetSpellBaseCooldown` yields nothing to count down from.

**The live lead this leaves open:** the `GetSpellCastCount` fallback means an ability icon
*can* raise `ChargeGained` without having real charges. Whether any spec's proc is modelled
that way — e.g. Demonic Core surfacing as a cast count on Demonbolt — is unmeasured and
would be a way to count something otherwise secret. `@verify-ingame`

### 5.4 The aura edges mark a fresh application, and a refresh fires both at once

**`OnAuraApplied` does not count stacks.** It fires only from
`unitAuraUpdateInfo.addedAuras`, matched on `aura.auraInstanceID ==
self:GetAuraSpellInstanceID()` `[T1 src: CooldownViewer.lua:615-618, :1682-1690]`. A stack
gained on an existing aura keeps the same `auraInstanceID` and arrives under
`updatedAuraInstanceIDs`, which nothing here listens to. `[client 2026-07-30]` Backdraft
(a 2-stack buff on the BuffBar viewer) raised `OnAuraApplied` ×5 / `OnAuraRemoved` ×5 across
~10 Conflagrate charge gains — applications, not increments. Conflagrate (2 real charges) in
the same capture raised `Available, OnCooldown, ChargeGained` and no aura edges.
⚠ **Evidence gone** — this subsection's alert-tape capture is off the ring with no
surviving extract, here and in the same-frame finding below; re-checking means re-flying.

**A re-application after a lapse fires BOTH clears in one frame, with the same timestamp.**
`[client 2026-07-30]` Re-applying a DoT raises `OnAuraRemoved` **and** `OnAuraApplied` for
the same cooldownID at an identical `GetTime()` — the capture shows both on `cid 133441`
*and* `cid 164597` at `131184.611`. So an edge latch that simply takes the last write lets
**Blizzard's dispatch order** decide whether the addon believes the aura is up or gone, and a
timestamp comparison cannot break the tie because the timestamps are equal. The rule that
resolves it is semantic, not temporal: **a re-application supersedes the removal it
replaces.** Anything latching `OnAura*` needs that precedence explicitly.

⚠ Do not confuse that with the maintained-aura case above: a refresh of a *live* aura raises
**nothing at all** (§5.1). The same-frame pair is a genuine re-application after a lapse.

The same capture also confirms §2.7's two-cooldownID warning in its sharpest form: both
Immolate rows raised `PandemicTime` at the *identical* timestamp (`131182.959`), so a
consumer keying per cooldownID gets two edges for one game event and must fold them to one
answer.

### 5.5 Sounds — a "Short" category, and the Combat Audio Assist tie-in (12.1.0)

`Enum.CooldownViewerSoundCategory` gained a **`Short`** member, carrying **26** sound
entries — Bell Strike, Bell Tree, Big Pot, Blades, Coffee Mug, Cow Bell, Finger Snap,
Guitar, Kalimba, Metal Blade Drop / On Rod, Metal Impact, Mini Wood Xylophone, Paper
Cup, Sheet Metal, Stove Pipe (+ Blade), Sword Shing, Synth Bleep / Blurp / Error /
High, Triangle, Water Drop, Wine Bottle, Wood Xylophone — each a
`{ soundEnum, soundKitID, text }` row with a real `SoundKit` id (353387–353428)
`[T1 src @12.1.0: Blizzard_CooldownViewer/CooldownViewerSoundAlertData.lua:58-84]`.
The menu-building helpers are new globals: `CooldownViewerUtil.BuildSoundMenus`,
`GetSoundTypeSoundKit`, `GetSoundTypeText`, `AddSoundAlertRadio`
`[T2 wiki: Patch 12.1.0/API changes §FrameXML/Added, revid 6801760, 2026-08-09]`.

**CDM sounds now also feed the Combat Audio Assist accessibility feature**
`[T1 game: 12.1 content update notes, via `_meta/changelog-12.1.md`]`. The addon-facing
trace of that is `C_CombatAudioAlert.SpeakText` gaining a `utteranceID` return plus
`MayReturnNothing`, and a new `CombatAudioAlertUtil.*` global family (11 functions)
`[T2 wiki: same page]`. ⚠ **That family is not part of `Blizzard_CooldownViewer`** — it
is a separate system the CDM's sound configuration feeds. Nothing here establishes an
addon-readable link between a CDM alert edge and an utterance. `@verify-ingame`

### 5.6 CDM rows can be pinged (12.1.0)

Spells and items shown on the Cooldown Manager can be **pinged**, alongside action-bar
spells, certain items, and player resources
`[T1 game: 12.1 content update notes, via `_meta/changelog-12.1.md`]`. The addon-facing
surface, all Tier 2 `[wiki: Patch 12.1.0/API changes, revid 6801760, 2026-08-09]`:

- Two new events, **`UNIT_PING_PIN_ADDED` / `UNIT_PING_PIN_REMOVED`**, and both carry
  `HasRestrictions = true` `[T1 docs @12.1.0]` — they are 2 of only 7 events in the
  whole corpus that do, alongside the four `COMBAT_LOG_*` and `MINIMAP_PING`. Treat
  them as guarded, not as a free readout.
- `Enum.PingSubjectType` gained **`ActionReady`, `ActionOnCooldown`,
  `ActionUnavailable`** — i.e. the ping payload encodes *cooldown state*, which is
  precisely the kind of thing §7 is about. ⚠ Whether an addon can read that
  discriminator, and whether it survives restricted combat, is **unestablished** and is
  the single most interesting open question 12.1.0 raises for this file.
  `@verify-ingame`
- `C_Ping.SendMacroPing`'s signature changed (arg1 is now a `PingMacroInfo`; the
  `targetToken` arg2 was removed), and `C_Ping.GetContextualPingTypeForUnit` was
  **removed**. Slash commands `/pingspell:<id>` and `/pingitem:<id>` are new
  `[T1 game: content update notes]`.

---

## 6. The proc glow is not a CDM mechanism

A frequent misreading is that a tracked buff (e.g. Demonic Core) is wired to the icon
of the spell it empowers (Demonbolt). **There is no such link inside the CDM.** The
chain leaves the system entirely:

1. **Game core** marks the *empowered* spell as overlay-activated when the enabling
   aura is applied. Entirely outside `Blizzard_CooldownViewer`.
2. **`SPELL_ACTIVATION_OVERLAY_GLOW_SHOW(spellID)`** fires carrying the **empowered
   spell's** id. The enabling aura's id appears nowhere in the payload. This is the
   same generic event the action bars have used for years.
3. **Only tab-1 viewers hear it** `[T1 src: CooldownViewer.lua:1948-1949]`. A tab-2 row
   can never glow this way.
4. The row tests `NeedSpellActivationUpdate(spellID)`, which is exactly
   `spellID == self:GetSpellID()` `[T1 src: :788-794]` — an **exact match against the
   row's currently-resolved identity**, not the base and not the pool. If a linked aura
   has taken rung 1, an incoming glow no longer matches.
5. `RefreshOverlayGlow` draws through `ActionButtonSpellAlertManager` and, when called
   with no event argument, falls back to polling
   `C_SpellActivationOverlay.IsSpellOverlayed(spellID)` `[T1 src: :1118-1134]`.

Two consequences worth holding onto:

- It is the **only proc channel requiring no aura read**, which is why it survives when
  `C_UnitAuras` goes secret in combat. **`[client]`** `IsSpellOverlayed` measured
  readable in combat (fired 27× in a measured pull).
- It lands on the **empowered spell** — the one actually pressed — which is more
  actionable than knowing the buff exists.

---

## 7. The readable surface

Three tiers. Status reflects what has been established, not what the docs promise.

> ⚠⚠ **THIS SECTION IS THE ONE MOST EXPOSED TO 12.1.0 AND IT HAS NOT BEEN RE-FLOWN.**
> Every `[client]` tag below was measured on **12.0.7** and is unchanged — none was
> restamped, because none was re-measured. Two 12.1.0 changes bear on it directly and
> neither has been tested:
> 1. **Auras went wholesale secret.** Anything below that reads an `auraInstanceID`, an
>    `AuraData` field, or a `UNIT_AURA` payload is describing a channel that 12.1.0
>    sealed for addon code (`security-taint-and-restricted-data` §4.7). Tier-2's
>    `auraDataUnit` / `auraInstanceID` findings are the specific ones at risk.
> 2. **The item-frame internals moved.** Five alert files were removed and six added
>    (§0b); every Tier-2 field below is an implementation detail at a pinned build,
>    which §4.11 of the security file already warns degrades **silently** to `nil`.
>
> Re-fly before building on any row here. `@verify-ingame`

### Tier 1 — structural config (identical on both families)

`C_CooldownViewer.GetCooldownViewerCooldownInfo(cooldownID)` returns
`{cooldownID, spellID, spellCategoryID, overrideSpellID, overrideTooltipSpellID,
equipSlot, buffSlot, linkedSpellIDs[], selfAura, hasAura, charges, isKnown,
isInvisible, flags, category}` — **fifteen fields at 12.1.0, up from eleven** (§1.3
for what the four new ones mean)
`[T1 docs @12.1.0: CooldownViewerDocumentation.lua:126-146]`.
Readable config even when live state is not. Also `GetCooldownViewerCategorySet`
(with `allowUnlearned`), `GetValidAlertTypes(cooldownID)`, `IsCooldownViewerAvailable`,
and **new at 12.1.0** `GetGroupBuffItems()` (§1.4).

> ⚠ **`GetCooldownViewerCategorySet` is a SUPERSET of what is laid out — it is not a
> row count.** Summed across all four categories with `allowUnlearned = false`, it runs
> well above the number of item frames the viewers actually return
> `[client 2026-08-06]` (cap v0.2.0 `bind` capture, 12 samples, 3 specs):
>
> | spec | rows walked | category set |
> |---|---|---|
> | Destruction (Diabolist) | 26 | 45–46 |
> | Destruction (Hellcaller) | 25 | 42 |
> | Demonology | 21 | 44 |
> | Retribution | 25 | 38 |
>
> So `rows ≤ set` is a usable sanity bound and `rows == set` is **not** an invariant —
> don't build an acceptance check on their agreeing. `allowUnlearned = false` already
> excludes unlearned spells, so the residue is something else; *the mechanism is
> unproven* (most likely rows the player has disabled in the Cooldown Manager's own
> config, which `GetItemFrames` would not return).

> ⚠ **`GetValidAlertTypes` gates `PandemicTime` and nothing else — it is not "what this row
> can raise".** `CanTriggerAlertType` is called in exactly **one** place in the whole addon:
> the pandemic arming path `[T1 src: CooldownViewer.lua:520]`. Nothing on the `Available` /
> `OnCooldown` / `ChargeGained` / `OnAuraApplied` / `OnAuraRemoved` paths consults it —
> `CheckTriggerAuraAppliedAlert` `[:615-618]`, for instance, checks only that the
> `auraInstanceID` matches. So the list is **what the settings UI offers the player to
> configure**, plus a hard gate on `PandemicTime` (§5.2); a hook on `TriggerAlertEvent` sees
> strictly more and is the only complete observation.
>
> Measured on both sides of the divergence. `[client 2026-07-30]` Shadowburn's eligibility is
> `(none)`, yet it raised `OnAuraApplied` ×3 and `OnAuraRemoved` ×3 in combat.
> `[client 2026-07-31]` cid `164597` (Immolate, Essential) reported **`PandemicTime` only**
> while the alert tape recorded an `OnAuraApplied` on that same cooldownID in the same
> session — only the BuffBar twin (cid `133441`) was reported eligible for the aura edges.
> So anything built on the list (a coverage report, a "this row can never fire an edge"
> claim) must say **"not reported eligible"**, never "cannot fire".
>
> The list *is* static per cooldownID: `validAlertTypes` is invalidated only when the frame's
> cooldownID is set or cleared `[T1 src: CooldownViewerItemData.lua:48, :65]`, never on cast,
> cooldown, aura or combat entry — a *data* property, unaffected by what the player has
> pressed. Observed values, for calibration: Conflagrate → `Available, OnCooldown,
> ChargeGained`; Summon Infernal / Cataclysm / Malevolence → `Available, OnCooldown`; Chaos
> Bolt, Shadowburn, Command Demon → `(none)`. The `(none)` cases correlate with having
> neither a recovery time nor a charge category in DB2 (Shadowburn `17877` and Chaos Bolt
> `116858` both carry `ChargeCategory = 0` and `RecoveryTime = 0`, against Conflagrate
> `17962`'s `ChargeCategory = 672`) `[T1 db2: SpellCategories, SpellCooldowns @ 12.0.7]` —
> i.e. there is simply no recovery event to configure.

⚠ **`hasAura` / `selfAura` / `charges` have zero consumers in Blizzard's Lua.** A grep
across all of `Interface/` finds them only in the generated documentation table. They
are DB2 hints the C side consumes. **Any classifier built on them is the addon
author's own invention**, and the most obvious such classifier is **false**: the rule
"`hasAura=false` ⇒ a real cooldown" is refuted by Demonic Core, which measures
`selfAura=true, hasAura=false` on cooldownID 777 `[client 2026-07-31]`. Classify on
**family** (§1.1) instead.

### Tier 2 — derived state parked on the item frame

| Field / method | Family | In restricted combat | The rule |
|---|---|---|---|
| `item.auraDataUnit` | both | **readable** `[client 2026-07-31]` | Plain `"player"` / `"target"`; non-nil **iff** the row has a live bound aura, and it discriminates. The in-combat "is the DoT up" read for an **aura-backed** row — see below. A totem-backed row has no aura to bind and answers on the two rows beneath instead. |
| **`item.Bar.Pip:IsShown()`** | tab 2, BuffBar only | **readable — a plain boolean** `[client 2026-08-09]` | Blizzard's own `currentTime > 0` verdict mirrored into widget state `[T1 src: CooldownViewer.lua:1414-1442]`. `true` **iff** the bar is live, on 5 cooldownIDs each observed in both states; never secret, never threw. The sturdy "is this bar live" read, and it works on aura- and totem-backed rows alike — see below. |
| `item.totemData` | both | **secret when populated, plain `nil` otherwise** `[client 2026-08-09]` | Set by `RefreshTotemData` from the player totem cache `[T1 src: CooldownViewer.lua:817, :1308, :1471]`. Secret on 3 of 141 rows, `nil` on the other 138. Class-check only: the record is sealed, so it says *this row is totem-backed and live* and nothing more — see below. |
| `item.auraInstanceID` | both | **readable — a plain number** `[client 2026-08-04]` | The key that unlocks the instance-scoped aura APIs — see below. |
| **`item.PandemicIcon`** | both | **readable — presence *is* the live pandemic state** `[client 2026-07-31]` | A frame reference, not a number. `~= nil` mirrors `IsInPandemicTime` exactly — see below. |
| `item.wasSetFromCharges` / `wasSetFromCooldown` / `wasSetFromAura` | tab 1 | **readable** `[client 2026-07-31]` | Plain booleans set by bare assignment `[:648-669]` recording **which of the four sources won this refresh** — i.e. what the dial currently *means*. 66–69 readable vs 9 `nil` per capture, unchanged in and out of combat. The one axis separating "the swipe is a cooldown" from "the swipe is an aura remaining". |
| `item:IsActive()` | tab 2 only, meaningfully | **readable** `[client 2026-07-31]` | On tab 1 it is `cooldownID ~= nil` → a **constant `true`** that is actively misleading, not merely useless (§8 rule 10). Gate on family. |
| `item:IsShown()` | both | conditional | `ShouldBeShown` returns true immediately when `not allowHideWhenInactive` **or** `not hideWhenInactive` `[:311-335]`. If the viewer is not set to hide-when-inactive this is **constant true** and anything driven off it latches on permanently. Capability-check, never assume. |
| `item.cooldownID` | both | **readable — plain, in combat and out** `[client 2026-08-06]` | The binding key, and the one field here that never sealed: 26 rows across all four viewers, **zero** secret reads on the field or on `item:GetCooldownID()`, over 4 out-of-combat runs and 13 samples spread through a pull. The two expressions never disagreed. It carries no `Secret*` annotation to guarantee it, so class-check as usual — but a binding that retains a stale id against an unreadable one is guarding a case never observed. |
| `item.cooldownStartTime` / `cooldownDuration` | tab 1 | **secret** | Copied straight from `C_Spell.GetSpellCooldown`, so they inherit its secrecy. Values, not verdicts. |
| `item.pandemicStartTime` / `pandemicEndTime` | both | **secret**; `IsInPandemicTime` **throws** `[client 2026-07-30]` | The throw is a *comparison* failure inside the method body `[:587]`, not a block — so the guard is `pcall`, not `issecretvalue` (§5.2). |
| `item.pandemicAlertTriggerTime` / `nextAvailableTimeToPlayPandemicAlert` | both | **secret** `[client 2026-07-31]` | The alert's arm + throttle, transitioning exactly as `[:548-555]` describes. Useful only as a *class* (armed vs fired); the numbers never read. |
| `item.auraSpellID` | both | **secret** `[client 2026-08-04]` | Written from aura data (`auraInfo.spellId`, §2.5) so it inherits the seal — unlike its sibling `auraInstanceID`. ⚠ **Never compare it; class-check first.** `aid == spellID` on this field threw the moment a pull started and killed an entire refresh loop. |
| `item:GetSpellID()` | both | **secret on SOME rows, and which rows MOVES between reads** `[client 2026-08-06]` ⚠ *evidence gone — that lab run is off the ring; the per-row values survive only as a queue transcription* | 1–3 of 21 rows read secret across 5 in-combat runs of the same character, and the secret set was different in three of them. ⚠ **It does not track `auraDataUnit`**: a BuffBar row with no bound aura read secret in 3 of 5 runs while a BuffIcon row *with* one read plain in 3 of 5 — so the earlier "exactly the rows carrying a live bound aura" reading was one sample's coincidence and is **not** a rule you may key on. The volatility is the mechanism: rung 1 resolves the *live* display identity, so its secrecy is per-read live state and not a property of the row. `item:GetBaseSpellID()` stays readable throughout. **Do not build an in-combat identity read on this** — use the struct's `overrideSpellID` (§2), which read plain on 21/21 rows in every one of those runs. |
| `item:GetAuraSpellID()` | both | **secret** `[client 2026-07-31]` | Rung 1 is present, not absent — it simply reads secret while restricted. `nil` out of combat when no aura is bound. |
| `item:GetLinkedSpell()` | both | `nil` on every row measured `[client 2026-07-31]` | See §2.5 — rung 2 was never elected on a Destruction character in either hero tree, on the frame *or* in a fresh struct read. |
| `item.auraDataCached` / `GetAuraDataCached()` | both | **container plain, members SECRET** `[client 2026-08-05]` | The record itself reads as a normal `table` (field *and* accessor), and it can be indexed — but `expirationTime`, `duration`, `timeMod` and `applications` all read **secret**. Only `auraInstanceID` is a plain `number`. See below. |

**`auraDataUnit` is the best in-combat aura-presence signal found so far.** It is the only
thing that says **which side the bound aura is on**, and nothing in the Tier-1 struct carries
it. `[client 2026-07-31]` (Destruction, both hero trees): `nil` on every row out of combat;
in combat exactly the rows with a live bound aura answer — Immolate cid 133441 and 164597 →
`"target"`, Backdraft / Malevolence / Conflagration of Chaos → `"player"`. A **control in the
same pull** read `nil` in combat *before* the DoT was applied and `"target"` once applied, so
it discriminates rather than latching. That matters more than it looks: with the alert
channel silent for a maintained aura (§5.1) and `C_UnitAuras` sealed, a non-nil
`auraDataUnit` is a *readable, in-combat* statement that this row has a live bound aura —
which is the "is the DoT up" read no other **aura** channel answers in a pull. It is not the
only readable liveness signal on a row: a BuffBar row also carries `Bar.Pip:IsShown()`, which
answers the narrower "is this bar live" without saying which unit or whether an aura is
involved at all (below). Together with `PandemicIcon` a tab-1 row exposes two readable
in-combat aura facts: *is it up*, and *is it in pandemic*.

⚠ **The Call Dreadstalkers BuffBar row is TOTEM-BACKED, not aura-backed — the aura
instruments read empty because the row has no aura to bind.** Blizzard's buff-item code
checks totems **before** auras: `GetCooldownValues` returns `totemData.expirationTime,
duration, modRate` and falls through to `GetAuraData()` only when the totem lookup misses
`[T1 src: CooldownViewer.lua:1208-1233]`, and `IsExpired` branches the same way
`[:1167-1184]`. Measured on cid `760` `[client 2026-08-09]`: a Call Dreadstalkers cast
raised `PLAYER_TOTEM_UPDATE` on two slots in the same second, and `item.totemData` read
**secret** — i.e. populated — while `item.auraDataUnit` stayed `nil`.

So the two negative aura measurements on this row were **correct reports of an absent
aura**, and both are now explained rather than open:

1. **`auraDataUnit` read `nil`** on cid `760` (BuffBar, base 104316) on **13 in-combat
   samples across a pull with several casts** `[client 2026-08-06]` — while five genuine
   aura rows on the same two viewers (Demonic Core 264173, Wild Imp 296553, Dominion of
   Argus 1276166 and both Diabolic Ritual rows) bound normally in the same samples.
2. **The alert channel raised nothing on that row.** cap's `edge` capture holds **1054
   alert edges** (`Available` / `OnCooldown` / `OnAuraApplied` / `OnAuraRemoved`) across the
   M3b flight and the pull after it, and **zero of any kind on cid 760** — over **171 Call
   Dreadstalkers casts**, counted off `OnCooldown cid:671` on the press row. A genuine aura
   row in the same captures, Dominion of Argus cid `169561`, raised **71 `OnAuraApplied` and
   70 `OnAuraRemoved`**. `[client 2026-08-07]`

The remaining time this row shows comes off the **totem channel** described under Tier 3,
and the "is it live" verdict is readable off the bar's own pip, below.

**The bar row is real, it is bound, and it draws.** Call Dreadstalkers occupies **two**
rows: cid `671` on the `EssentialCooldownViewer` (the cooldown icon) **and cid `760` on the
`BuffBarCooldownViewer`** — confirmed live on every bind-log read on a Demonology
character, and in `CooldownSetSpell` as `760,60,104316,3` (Category 3 =
TrackedBar). The bar row also carries a **linked spell the icon row does not** —
`CooldownSetLinkedSpell` row `688,193332,0,760`, which the same bind log reads back on
the live frame as `pool=193332`, and `193332` raises its **own `SPELL_UPDATE_COOLDOWN` in the same second as
the cast** `[client 2026-08-09]`. That is a second real handle on the summon; the pip below
makes it unnecessary. `[client 2026-08-07]` `[T1 db2 @ 12.0.7]`

**`Bar.Pip:IsShown()` is the readable in-combat "is this bar live" boolean, and it clears
the discriminate test.** `CooldownViewerBuffBarItemMixin:RefreshCooldownInfo`
`[T1 src: CooldownViewer.lua:1414-1442]` computes `currentTime = expirationTime - GetTime()`
— secret arithmetic Blizzard is allowed to do — and lands the verdict in widget state:
`barFrame:SetValue(currentTime)` and **`pipTexture:SetShown(currentTime > 0)`**. Reading the
pip back is a plain widget read. Measured across **5 distinct BuffBar cooldownIDs, each
observed in BOTH states** (`169561`, `181089`, `760`, `777`, `84224`) `[client 2026-08-09]`:

| bar state | `Bar.Pip:IsShown()` | `Bar:GetValue()` | `item.totemData` |
|---|---|---|---|
| live | **`true`**, a plain boolean | **secret** | secret on the totem-backed rows, `nil` on the aura-backed ones |
| idle | **`false`**, a plain boolean | usually plain `0` | `nil` |

The pip never read secret and never threw, on any sample. This is the `PandemicIcon`
pattern — Blizzard's own comparison, mirrored into widget state — and it is subject to the
same four preconditions that pattern carries, in
[`security-taint-and-restricted-data`](./security-taint-and-restricted-data.md) §4.11 and
its rule 17b.

⚠ **`Bar:GetValue()` is NOT a substitute for the pip — a bar that has once been fed a secret
can go on reading secret while idle.** Counted over the 49 samples in that capture where the
bar widget exists (8 live, 41 idle): it read `secret` on **8 of 8** live samples but plain `0`
on only **38 of 41** idle ones. On the other **3**, with the pip already reading `false`,
`GetValue()` returned `secret` **and** `GetMinMaxValues()` returned `secret|secret` — two
cooldownIDs, `181089` (×2) and `777`, each of which had been live earlier **in the same
session**. Both read plain `0` again at the login sweep after a `/reload`. `[client 2026-08-09]`

**The source rules out the obvious explanation.** `pipTexture:SetShown(false)` occurs at
exactly **one** place `[T1 src: CooldownViewer.lua:1440]`, inside the same `else` branch that
writes `SetMinMaxValues(0, 0)` and `SetValue(0)` from plain constants `[:1433-1441]` — so the
only path that can turn the pip off is the one that writes the plain zeros, and there is no
"another path hid it" to blame. The likely mechanism is instead that a
StatusBar's **readback class is sticky**: once the widget has been handed a secret, its
getters keep answering secret for the life of the frame, whatever is written afterwards. The
value is not stale — it is unreadable. ⚠ **That mechanism is unproven, `n = 3`**, and nothing
here distinguishes it from a per-widget latch Blizzard clears on some event we did not sample.
The practical conclusion does not depend on which: the pip is the sturdy read, the bar value is
not.

⚠⚠ **A negative measurement names an *instrument*, a *row* and a *build*.** The sentence
that generalises it to "nothing can read this" is always the sentence nobody measured — and
it is the sentence that gets quoted downstream while the qualification underneath it is left
behind. **Put the qualification in the headline.** Call Dreadstalkers is the worked example:
generalising "the aura instruments report nothing" into "nothing can read this" is **false** —
the value sits on the totem channel.

**`auraInstanceID` is the key to the instance-scoped aura APIs.** `RequiresValidUnitAuraInstance`
APIs need an instance id, and the enumeration that hands them out (`GetAuraDataByIndex` and
friends) is sealed in a pull — but Blizzard's own frame carries one and keeps it fresh
(`SetAuraInstanceInfo`, §2.5). `[client 2026-08-04]` (Demonology, in combat): a plain
number on Wild Imps 296553 and Demonic Core 264173, and it
passes cleanly into `C_UnitAuras.GetAuraApplicationDisplayCount`, which is
`SecretArguments = "AllowedWhenUntainted"` and would have **refused** a secret. See
[`security-taint-and-restricted-data`](./security-taint-and-restricted-data.md) §4.8.2 for
what that buys.

**`PandemicIcon` replaces both the sealed number and the one-shot alert.**
`CheckPandemicTimeDisplay` `[:562]` runs **every frame** from the item's `OnUpdate` `[:98]`
and calls `Show`/`HidePandemicStateFrame`, which set and nil this field `[:570-585]`. So
`PandemicIcon ~= nil` mirrors `IsInPandemicTime` exactly — and it is a *frame reference*, not
a secret number, so reading it costs nothing. `[client 2026-07-31]` over a full DoT cycle
(cid 164597 Immolate): `nil` before application → `nil` while up but pre-pandemic → `table`
in pandemic → `nil` again immediately after a refresh. Never secret, never threw.

**`auraDataCached` was the most promising open lead on this frame. It is now CLOSED, and
the answer is no.** Every item frame parks the **complete `AuraData` record** of its
currently-bound aura on itself, written in the *same statement block* as `auraDataUnit` —
the field already measured readable in combat — and nil'd together with it
`[T1 src: CooldownViewerItemData.lua:395-408, accessor :411-413]`. Blizzard's own consumers
read `.expirationTime`, `.duration`, `.timeMod`, `.applications` and `.auraInstanceID` off
it. The hope was that if those members were plain in combat, the "how much time is left on
my DoT" read that §5.2 and this section both call unanswerable would already be sitting on
the frame.

**Measured in a real pull** (Demonology, 29 item frames scanned, the bound row on
`BuffIconCooldownViewer`) `[client 2026-08-05]`:

| | class in combat |
|---|---|
| the record itself (`item.auraDataCached`) | **`table`** — plain, and indexable |
| `item:GetAuraDataCached()` | **`table`** — same |
| `.expirationTime` | **secret** |
| `.duration` | **secret** |
| `.timeMod` | **secret** |
| `.applications` | **secret** |
| `.auraInstanceID` | **`number`** — plain |

So the **container** is readable while its **time-bearing members are not**, which is the
same seam every sibling field on this frame sits on. Secrecy is tagged per value at read
time, and Blizzard reading them from untainted code says nothing about us reading them from
tainted code — that was the whole risk in the lead, and it is what the measurement found.

**But the record's plain `auraInstanceID` opens the duration-object route, and that DOES
work — on both sides.** `[client 2026-08-05]`, Destruction, in combat, 30 item frames:

```lua
local unit = item.auraDataUnit                 -- plain: "player" | "target"
local id   = item.auraDataCached.auraInstanceID -- plain number
local dur  = C_UnitAuras.GetAuraDuration(unit, id)   -- LuaDurationObject (userdata)
```

| | player buff (387109) | target debuff (**348 Immolate**) |
|---|---|---|
| viewer | `BuffIconCooldownViewer` | `EssentialCooldownViewer` |
| `auraInstanceID` | plain `number` | plain `number` |
| `GetAuraDuration(unit, id)` | **`userdata`** | **`userdata`** |
| `HasSecretValues()` | **`true`** | **`true`** |
| `GetRemainingDuration()` | **secret** | **secret** |

Four things follow. The **two-argument signature is confirmed** — `(unit, auraInstanceID)`,
no fallback arity needed. It works **friendly-on-player and player-on-target alike**, so a
DoT and a self-buff use one code path. `HasSecretValues()` returning a plain `true` proves
the object really is carrying the sealed timing rather than an empty shell. And
`GetRemainingDuration()` staying **secret** means the seal has no hole here — the object is
a *display* channel, not a readback.

**And it RENDERS.** Fed to `StatusBar:SetTimerDuration`, the aura bars for both the player
buff and the target debuff **animate exactly as a control bar built from plain numbers
does** — confirmed by eyeball `[client 2026-08-05]`, which is the only oracle that exists
here because all three duration sinks declare no `SecretArgumentsAddAspect` and expose no
readback. So this is a complete, working display channel end to end:

```lua
-- in combat, on a CDM row with a live bound aura
local bar = CreateFrame("StatusBar", ...)
bar:SetMinMaxValues(0, 1)                         -- ⚠ BEFORE the timer, or it draws at 0 %
bar:SetTimerDuration(C_UnitAuras.GetAuraDuration(item.auraDataUnit,
                                                 item.auraDataCached.auraInstanceID), 0, 0)
```

⚠ **You still cannot learn the number** — `GetRemainingDuration()` is secret and the
in-combat remaining-time *read* stays unanswerable. What changed is that you can **show**
it. A HUD can draw an honest DoT timer it is not allowed to inspect.

What the record *also* adds is
`auraInstanceID` as a **plain, in-combat, per-aura identity** — enough to tell "the same
aura instance is still on the target" from "a different one is", which is a genuinely new
in-combat fact even though it carries no timing. Pair it with `auraDataUnit` (which side
the aura is on) and `PandemicIcon` (is it refreshable) for the readable set.

**How you OBTAIN these rows: `GetItemFrames()` keeps answering when the viewer is
hidden.** It is `GetItemContainerFrame():GetLayoutChildren()`, and the container is the
viewer itself `[T1 src @12.1.0: CooldownViewer.lua:1632-1639]`. `GetLayoutChildren` admits a
pooled child only if three conditions hold — the child is shown **or** sets
`includeAsLayoutChildWhenHidden`, it is not ignored in layout, and it carries a
`layoutIndex`
`[T1 src @12.1.0: Blizzard_SharedXML/LayoutFrame.lua:33-42 (the filter at :38), :58-68]`. The
shown leg tests the **child's** own `IsShown()`, not the viewer's `IsVisible()` — and all
four item templates set `includeAsLayoutChildWhenHidden = true`
`[T1 src @12.1.0: CooldownViewer.xml:24, :93, :162, :213]`, so that leg never binds on a CDM
row at all (§4.1 takes the same fact the other way: the row keeps its grid slot). The
viewer's `OnHide` unregisters events without releasing `itemFramePool`
`[T1 src @12.1.0: CooldownViewer.lua:1743-1753]`.

**Measured with all four viewers hidden in Edit Mode** `[client 2026-08-06]`
(Destruction, out of combat):

| viewer | `IsShown` / `IsVisible` | children | of those, shown | pool active | `#GetItemFrames()` |
|---|---|---|---|---|---|
| `EssentialCooldownViewer` | false / false | 10 | 9 | 9 | **9** |
| `UtilityCooldownViewer` | false / false | 8 | 7 | 7 | **7** |
| `BuffIconCooldownViewer` | false / false | 9 | 1 | 7 | **7** |
| `BuffBarCooldownViewer` | false / false | 4 | 0 | 3 | **3** |

`#GetItemFrames()` equals the pool's active count on every viewer, hidden or not. The two
aura viewers are the ones that prove the mechanism rather than merely surviving it: their
item frames are individually **not** shown (1 of 9 and 0 of 4) and are returned anyway —
which is `includeAsLayoutChildWhenHidden`, not luck.

⚠ **So a consumer cannot tell "the CDM is hidden" from "the CDM is showing" by counting
rows, and a row count of zero means the pool is empty — nothing else.** A health check
that reports *hidden* off an empty enumeration is reporting a state it cannot observe;
read the viewer's own `IsShown()` for that, and let the row count mean *configured*.

### Tier 3 — the live game API

| Read | Status |
|---|---|
| `UnitPower` | **`[client]`** readable *and branchable* in instanced combat |
| `UNIT_SPELLCAST_*` (player) | **`[client]`** readable spellID in all four phases |
| `C_SpellActivationOverlay.IsSpellOverlayed` | **`[client]`** readable in combat |
| `C_AssistedCombat.GetNextCastSpell` | **`[client 2026-08-01]`** ⚠ *evidence gone — capture off the ring, no surviving extract* — readable — a plain number in combat and out. See below: readability is proven, usefulness is not |
| `C_Spell.GetSpellCooldown` | **`[client 2026-08-09]`** **not sealed whole** — a plain table whose members seal individually. `isEnabled` / `isActive` / `isOnGCD` read plain in restricted combat; `startTime` / `duration` / `modRate` are secret. See below |
| `C_Spell.GetSpellCharges` | **`[client 2026-08-11]`** a plain table whose members seal by state. Conflagrate at 2/2 was wholly readable even in restricted combat; at 1/2 and 0/2 its current count and recharge values were secret, while `maxCharges=2` and `isActive=true` stayed plain. See below |
| `C_Spell.GetSpellCooldownDuration(spellIdentifier, ignoreGCD)` | **`[client 2026-08-09]`** returns a `LuaDurationObject` in restricted combat, `HasSecretValues()` plain `true`, every getter on it secret. See below |
| `C_UnitAuras.Get*` | The `AuraData` record is secret when restricted. Three getters carry a **per-aura** `RequiresNonSecretAura` precondition — but its failure behaviour is undocumented, see below |

**`C_Spell.GetSpellCooldown` is NOT sealed whole, and `isActive` is a readable, branchable
in-combat "is this spell on cooldown" boolean.** The call returns a **plain table whose
members seal individually** — `issecrettable` was false on all 142 samples in the capture,
in combat and out. Over the **90 in-combat samples** in which `startTime` read secret
(Demonology Warlock, one row per tracked spell) `[client 2026-08-09]`:

| Field | Doc annotation | In restricted combat |
|---|---|---|
| `startTime` · `duration` · `modRate` | — | **secret**, 90/90 |
| `isEnabled` | `NeverSecret = true` | **plain `true`**, 90/90 |
| `isActive` | `NeverSecret = true` | **plain boolean** — `false` ×71, `true` ×19 |
| `isOnGCD` | `NeverSecret = true` | **plain** — `nil` ×76, `true` ×14 |
| `activeCategory` | — | `nil` ×76, **secret** ×14 |
| `timeUntilEndOfStartRecovery` | — | `nil` ×71, **secret** ×19 |

`[T1 docs: SpellSharedDocumentation.lua:18-32]` for the annotations. They hold at runtime,
and the two unannotated nilable fields seal exactly when they carry a value. **`isActive`
discriminates** — 71 false against 19 true across the same pulls — so it is a real predicate
and not a constant, which is the test a widget-or-field read has to clear before anyone
builds on it. `isOnGCD` carries Blizzard's own caveat in the docs: *"do not trust this field
unless responding to a `SPELL_UPDATE_COOLDOWN` event"*.

**A different channel from `LuaDurationObject`, and not a contradiction of it.**
[`security-taint-and-restricted-data`](./security-taint-and-restricted-data.md) §4.8.4's
*"the object exposes no readable in-combat readiness of its own"* is a claim about the
duration object, whose `HasExpired` / `IsActive` / `HasStarted` / `IsZero` are **secret
booleans** — and it stays true. `C_Spell.GetSpellCooldown(id).isActive` is a plain boolean
on a different surface. So: an addon that must **branch** on readiness has this call, and an
addon that must **draw** remaining time has the duration object.

**`GetSpellCharges` also seals per member—and per state.** `[client 2026-08-11]` A direct
Conflagrate `17962` characterization started from an exact 2/2 seed and sampled again at
combat entry, 1/2, and 0/2. The returned table itself stayed plain throughout. At 2/2 in
restricted combat every sampled member was readable: `currentCharges=2`, `maxCharges=2`,
`cooldownStartTime=0`, `cooldownDuration=9.326`, `chargeModRate=1`, `isActive=false`. At
both 1/2 and 0/2, `currentCharges`, start, duration, and rate were secret; `maxCharges=2`
and `isActive=true` remained plain. This matches the two `NeverSecret` annotations
`[T1 docs: SpellSharedDocumentation.lua:5-17]` but establishes the runtime shape they did
not state.

**Therefore `isActive` is recharge state, not charged readiness.** It distinguishes full
2/2 from recharging, but deliberately collapses castable 1/2 and uncastable 0/2. An addon
may seed exact count and recharge duration while full/out of combat, but once recharge
begins it needs a bounded estimator to branch on “at least one charge”; the client-owned
Cooldown Manager can still display the sealed exact count and swipe.

That last sentence is deliberately narrower than “custom charge context is impossible.”
The shipped surface separately offers a sealed display string through
`C_Spell.GetSpellDisplayCount`, and a client-owned next-charge duration through
`C_Spell.GetSpellChargeDuration`; `FontString:SetText` and
`Cooldown:SetCooldownFromDurationObject` are their corresponding sinks. Source inspection
supports both compositions and ordinary Cooldown styling remains available around the
duration sink, but their actual restricted-combat pixels are a visual question.
`@pending-test: conflagrate-charge-context-displays`

**`C_Spell.GetSpellCooldownDuration` bypasses the CDM entirely and survives restricted
combat.** It takes a spell identifier and `ignoreGCD` and returns a `LuaDurationObject`
`[T1 docs: SpellDocumentation.lua:266-283]` — no cooldownID, no item frame, no viewer. It
declares no `SecretWhenCooldownsRestricted`, unlike `GetSpellCharges` `[:230-247]` and
`GetSpellCooldown` `[:248-265]`, carrying only `SecretArguments = "AllowedWhenTainted"` as
does its sibling `GetSpellChargeDuration` `[:213-229]`. `[client 2026-08-09]` on **90
in-combat samples**, on both `ignoreGCD = false` and `ignoreGCD = true`: it returns a
`userdata` object every time, `HasSecretValues()` reads a plain `true`, and every numeric
and boolean getter on it reads secret. That is the whole duration-object design working as
designed — the object holds the secret internally and is handed to a sink, so there is
nothing to seal at the boundary (see
[`security-taint-and-restricted-data`](./security-taint-and-restricted-data.md) §4.8).

**The totem channel — a Warlock's summons occupy totem slots, and the seal there differs
call by call.** `GetTotemInfo(slot)` and `GetTotemTimeLeft(slot)` both carry
`SecretWhenTotemSlotSecret = true`; **`GetTotemDuration(slot)` carries no `Secret*When*` seal
at all** — only `SecretArguments = "AllowedWhenUntainted"` `[T1 docs:
TotemDocumentation.lua:43-96]`, which is a rule about what you may pass *in*, not about what
comes back: the `slot` argument has to be a plain number or addon code is refused. Measured in restricted
combat on a **Warlock**, `GetNumTotemSlots()` returns **5** — the totem system is not
shaman-only, and Demonology's summons occupy slots. Sampled on `PLAYER_TOTEM_UPDATE` edges,
five slots per edge, **55 slot reads: 24 occupied, 31 empty** `[client 2026-08-09]`:

| call | occupied slot (24) | empty slot (31) |
|---|---|---|
| `GetTotemInfo(slot)` | returns 7 values — `haveTotem` · `totemName` · `startTime` · `duration` · `icon` · `modRate` · `spellID` — every one **secret** on **23 of the 24**; on the 24th `totemName` read a plain `nil` and the other six stayed secret | returns 7 values; six **secret**, and `icon` — the **fifth** return, not the last — **plain `nil`** on 31/31 |
| `GetTotemTimeLeft(slot)` | **secret** | **plain `0`** |
| `GetTotemDuration(slot)` | a **`LuaDurationObject`** | **`nil`** |

On that duration object `HasSecretValues()` returns a **plain `true`**, and all thirteen
numeric and boolean getters probed read **secret**: `GetRemainingDuration`,
`GetTotalDuration`, `GetStartTime`, `GetEndTime`, `GetElapsedDuration`, `GetElapsedPercent`,
`GetRemainingPercent`, `GetClockTime`, `GetModRate`, `HasExpired`, `HasStarted`, `IsActive`,
`IsZero`. Same contract as the aura and spell duration objects: **drawable, not readable.**

⚠ **`spellID` seals, so totem data alone cannot tell one summon from another.** Identity has
to come from the CDM row binding, or from something outside the totem API.

⚠ **A second, weaker signal, and it is fragile: the *readability class* of `GetTotemTimeLeft`
discriminates occupancy** — plain `0` when the slot is empty, secret when it is occupied,
31 against 24 with no exceptions. `issecretvalue()` returns a plain boolean, so branching on
the class is legal Lua. But it leaks the fact the seal exists to withhold, it may be an
oversight Blizzard closes, and `Bar.Pip:IsShown()` (Tier 2) answers the same question more
sturdily. `GetTotemInfo`'s `icon` return discriminates identically and carries the same
caveat.

⚠⚠ **Call the raw totem API above, never Blizzard's cached wrapper — reading the wrapper
can leave Blizzard's own state torn.** `CooldownViewerItemDataMixin:GetCurrentPlayerTotemCache()`
is a one-line pass-through `[T1 src: CooldownViewerItemData.lua:492-493]` to a module-local
memoiser, `GetPlayerTotemsCached` `[:446-486]`, and the memoiser is not a pure read. On a
cache miss it **wipes the shared upvalue first** — `playerTotemCache = {}` `[:449]` — then
branches on `GetTotemInfo`'s first return, `if hasTotem then` `[:454]`, which is the very
value the table above measured **secret** on an occupied slot; and it restamps
`playerTotemCacheTime = now` only at `[:482]`, after the whole rebuild has completed. A
throw at `:454` therefore lands **between the wipe and the restamp**, leaving Blizzard's
cache empty under a stale timestamp rather than merely failing the caller.
`CooldownViewerItemMixin:RefreshTotemData` reads that same cache on every cooldown-,
BuffIcon- and BuffBar-item refresh `[T1 src: CooldownViewer.lua:231, called from :817,
:1308, :1471]`, and none of those call sites catches an error.

**The general rule, and it is not about totems: a Blizzard "getter" that memoises into a
module-local upvalue is not a pure read.** Calling one from tainted code can damage state
Blizzard's own secure path depends on, so the failure is not confined to your own frame.
Prefer the raw API — `GetTotemInfo(slot)` owns no shared state, so the worst it can do to
you is refuse. ⚠ Whether Blizzard's *own* untainted call is affected the same way is **not
established**, and nothing here claims it either way. ⚠ This is a source read; no in-client
measurement of the effect survives on disk.

**`C_UnitAuras`'s seal is annotated per aura — but what that buys is undocumented.** Three
getters carry a `Precondition` named `RequiresNonSecretAura = true`: `GetAuraDataBySpellName`
(`UnitAuraDocumentation.lua:208`), `GetPlayerAuraBySpellID` (`:335`) and
`GetUnitAuraBySpellID` (`:372`), the predicate itself declared at `:558-561`
`[T1 docs]`. Its existence is the interesting part: the seal is described **per aura**, not
as a blanket property of the API, so "your own auras are as sealed as the target's" is at
least stated too strongly. Two Tier-1 reasons not to build on it yet:

- **`[gap]` The predicate declares no `FailureMode`.** It is one of exactly **two** of the
  corpus's 32 `Precondition` declarations that omit the field (the other is
  `RestrictedForMacroChatMessages`) `[T1 docs: re-counted at 12.0.7.68887]`. So *what
  happens* when the precondition fails — silent absence, an error, a value plus an error —
  is not stated anywhere at Tier 1, and the Precondition-vs-Secret split in
  [`security-taint-and-restricted-data`](./security-taint-and-restricted-data.md) §4.7
  cannot be cited for it. `@verify-ingame`
- **All three also carry `SecretWhenUnitAuraRestricted = true`** (`:207`, `:334`, `:371`) —
  a *Secret* predicate stacked on top of the Precondition. Passing the precondition
  therefore does not on its own mean the record comes back readable, and how the two
  annotations interact is undocumented.

⚠⚠ The practical floor is moving regardless: Ebon Might (395296) was reportedly dropped from
the non-secret set during 12.1.0 PTR, killing a shipping addon's numeric `expirationTime`
path outright. *[Tier 1 for the annotations; Tier 3 for the narrowing.]*

**`C_AssistedCombat.GetNextCastSpell(checkForVisibleButton)` is a rotation answer that does
not go secret.** `[client 2026-08-01]` (Destruction + Demonology, sampled by a flight
recorder): it returns a **plain number** — `issecretvalue()` false, safe to compare, format
and use as a table key — both out of combat and inside a dummy pull, on both `false` and
`true`. `IsAvailable()` returned a plain bool and `GetRotationSpells()` a plain (non-secret)
table in the same samples. ⚠ **Evidence gone** — the flight-recorder capture behind this
paragraph is off the ring and no surviving extract carries its version, its date or any
sample of the call; both the readability finding and the constant below rest on what was
written down at the time. Every other cooldown channel in this file refuses in restricted
combat; this one does not. *(Why it survives is predictable from the generated docs, and the
reasoning generalises beyond the CDM — see
[`api-events-and-discovery`](./api-events-and-discovery.md) §5.7.)*

⚠ **Readability is proven; usefulness is not.** `` @pending-test:
assisted-combat-next-cast-varies `` The capture recorded a **constant `691`
(Summon Felhunter)** at every sample, out of combat and in, on both arguments.

⚠⚠ **That constant is not evidence the oracle is stuck, and must not be quoted as
though it were.** The recorder dedups by readability *class*, so it sampled only at
readable⇄secret transitions — of which there were none — and a value changing every GCD
would have been recorded **exactly once**, indistinguishable from one that never changed.
The measurement cannot separate the two hypotheses, so it supports neither. Before
treating this as an oracle to diff a rotation against, take a **value-sampling** pass —
one keyed to the player's own casts, not to a timer or a readability edge, since a
rotation answer should advance when you cast. Note also what it is by design: a generic
single-target rotation with **no AoE/mode awareness and no burst planning**.

**The three-step, and it is the same on all three channels.** Auras, spell cooldowns and
totems now each expose the identical shape: a **plain boolean** says whether there is
anything to show, a **duration object** carries the sealed timing, and a **sink** draws it.
Nothing in between reads a number, and nothing in between needs to.

```lua
-- 1. DETECT with a plain boolean. Both of these are branchable in restricted combat.
local live  = item.Bar.Pip:IsShown()                     -- BuffBar row: Blizzard's own verdict, mirrored
local cd    = C_Spell.GetSpellCooldown(id)               -- MayReturnNothing: nil on an unknown spell
local onCD  = cd and cd.isActive                         -- NeverSecret; this struct's OTHER members are not

-- 2. OBTAIN the duration object. One call per channel; each holds its secret internally.
local d
if     slot   then d = GetTotemDuration(slot)                     -- nil when the slot is empty
elseif instID then d = C_UnitAuras.GetAuraDuration(unit, instID)  -- both args must be plain, or it refuses
else               d = C_Spell.GetSpellCooldownDuration(id, false) -- MayReturnNothing: nil-guard it
end

-- 3. HAND IT TO A SINK. Never read it back: every getter on the object is secret.
bar:SetMinMaxValues(0, 1)        -- ⚠ BEFORE the timer, or a correct duration draws at 0 %
bar:SetTimerDuration(d, 0, 1)    -- 0 = Interpolation.Immediate, 1 = TimerDirection.RemainingTime
                                 -- StatusBar; or Cooldown:SetCooldownFromDurationObject(d)
```

⚠ **An eyeball is the only oracle for step 3.** The duration sinks declare no
`SecretArgumentsAddAspect` and expose no programmatic readback, so "the call did not error" is not
evidence that a pixel moved.

**Summary: the readable surface changes with the family, but asymmetrically.** Tier 1
is identical. Tier 2 diverges hardest — tab 1 carries a cooldown/charge cache and the
source flags; tab 2 carries little but computes on demand, and is the only side where
`IsActive()` means anything.

---

## 8. Rules we could audit against

1. **Classify on family, never on category.** Essential↔Utility and
   TrackedBuff↔TrackedBar are user-editable placement (§1).
2. **Never assume a row's identity is its base spellID.** Resolve through
   `GetSpellID()`'s ladder, and expect the answer to change mid-combat (§2).
3. **Read charges on `overrideSpellID or spellID`**, not on the display identity —
   mirror `GetSpellChargeInfo` (§3.3).
4. **Do not read `IsActive()` uniformly across families.** Gate it on family, or it is
   a constant on the tab-1 side with no error to distinguish it (§1.1, §7).
5. **Do not treat a value's trust and a value's meaning as one axis.** "How much do I
   trust this number" and "is this number a cooldown, a recharge, or an aura remaining"
   are independent (§3.1).
6. **Hook `TriggerAlertEvent` per item instance, not on the mixin table** — the methods
   are `Mixin()`-copied (§5.1).
7. **Do not drive proc state off `IsShown()` without a capability check** (§7).
8. **Do not build a classifier on `hasAura`/`selfAura` and call it Blizzard's** —
   nothing in Blizzard's Lua reads them (§7).
9. **Expect `COOLDOWN_VIEWER_SPELL_OVERRIDE_UPDATED` to fire redundantly**, and to have
   *already fired* before your addon loaded. A missed event and an absent event are
   indistinguishable — poll identity at bind time, use the event as the fast path (§5).
10. **Never read `item:IsActive()` as a *value* on tab 1 — it is a constant, and it is
    ACTIVELY MISLEADING, not merely useless.** `[client 2026-07-31]`: every tab-1 row with
    a live frame read `IsActive() == true` out of combat, standing still, with no target —
    including pure utilities (Soulstone, Create Soulwell, Demonic Circle). The sharpest
    demonstration is cid `164597` Immolate, where the *same frame* simultaneously reported
    `IsActive = true`, `wasSetFromAura = false` and `auraDataUnit = nil`: the frame calls
    itself active while its own source flags say no aura drove it. This is the concrete
    form of rule 4, and a consumer that folds it into an "is this buff up" signal gets a
    permanent true. Gate on **family** (§1.1).
11. **Wrap `item:IsInPandemicTime()` in `pcall`, not `issecretvalue`.** It compares two
    secret fields internally and therefore *throws* rather than returning a secret (§5.2).
12. **Never credit "+1 charge" per `ChargeGained`.** The alert drains a prediction queue and
    over-fires; bound credits by a recharge-derived gain floor seeded out of combat (§5.3).
13. **Never build readiness for a charged ability out of `Available` + `OnCooldown`.** The
    "on" edge never arrives for a charged spell, so the latch reads *ready* forever after
    the first restore, including at zero charges (§5.3).
14. **Never read `GetValidAlertTypes` as "what this row can raise".** It is the settings-UI
    offer list plus a hard gate on `PandemicTime` alone; say "not reported eligible", never
    "cannot fire" (§7 Tier 1).
15. **Never key an ability by a single spellID when walking the CDM set.** Union each row's
    base `spellID` with `overrideSpellID`, `overrideTooltipSpellID` and the resolved live
    id, and re-read the set on `SPELLS_CHANGED` — `isKnown` is not stable across hero
    trees (§2.8).
16. **Never read the Tier-1 struct's `category` as "where this row is".** It is the raw DB2
    value; the player's effective placement — including the `HideByDefault` rewrite — exists
    only in Blizzard Lua, at `GetDataProvider():GetCooldownInfoForID(id).category` (§1.2).
17. **Never conflate the three row enumerations.** DB2 `CooldownSetSpell` for the spec's
    `CooldownSetID` ⊇ `GetCooldownViewerCategorySet` ⊇ the frames the viewers lay out
    (65 / 44 / 21 on one measured spec, §1.2 and §7 Tier 1). Say which one a coverage claim
    is measured against; a hidden row is present in the first two and absent from the third,
    and it raises no alert edge at all.
18. **Never reorder a CDM row by rewriting `layoutIndex`.** Grid position *and* cooldownID
    binding both key off that one field, so swapping two frames' indices swaps their
    contents too and the row looks untouched; a duplicate raises `GMError`. Reorder with
    `ClearAllPoints()` + `SetPoint()` and leave the index alone (§4.1).
19. **Never read drawn position out of a `GetItemFrames()` index.** That enumeration is in
    `layoutIndex` order — Blizzard's intended order — and is blind to any `SetPoint`
    re-anchor. Drawn position is `GetLeft()` / `GetTop()` (§4.1).
20. **Assume any anchor, parent or decoration you put on an item frame is torn down
    mid-combat.** `UNIT_AURA`'s `isFullUpdate` branch calls `RefreshLayout`, which
    `ReleaseAll()`s the pool, and the reset callback `Hide()`s, `ClearAllPoints()`s and
    nils `layoutIndex`. Re-apply on a signal; never assume persistence (§4.1).
21. **Re-anchor an item frame; do not re-parent it.** The viewer `SetPoint`s the pandemic
    state frame onto the item, so re-parenting breaks that chain and re-anchoring does not
    (§4.1).
22. **Never read "the templates declare no `protected` attribute" as "these frames are safe
    to touch in combat."** That is a fact about `Blizzard_CooldownViewer/*.xml`; the runtime
    question is open and the XML does not answer it (§4.1).
23. **Do not gate a layout rider on "did the row set change".** A same-count settings change
    takes the in-place `RefreshData` path and disturbs nothing, while a `UNIT_AURA` full
    update tears everything down without the set changing at all (§4.1).

---

## 9. Gaps and pending work

- **`[gap]`** Whether the rung-2 election ever fires *at all* in practice, on any spec. It
  did not on Destruction in either hero tree; §2.2 path B needs a `SPELL_UPDATE_COOLDOWN`
  naming a pool candidate, and nothing sent one. If it never fires, rung 2 is dead weight in
  every consumer's ladder.
- **`[gap]`** What `RequiresNonSecretAura` does when it fails (§7 Tier 3). It is one of only
  two Preconditions in the corpus declaring no `FailureMode`, and the three getters carrying
  it also carry the `SecretWhenUnitAuraRestricted` *Secret* predicate — so neither the
  failure behaviour nor the interaction of the two annotations is documented at Tier 1.
- **`[gap]`** Whether any spec's proc is modelled as a **cast count** rather than real
  charges, so that `ChargeGained` fires for it off `C_Spell.GetSpellCastCount` (§5.3) — that
  would be a way to count something otherwise secret.
- **`[gap]`** Whether the **Summon Demonic Tyrant player aura is literally spellID
  `265187`** — i.e. whether the Essential row's own id is what a "Tyrant is active" read
  would key on. Three spells named **Demonic Power** exist in the Midnight id range
  (`265273`, `281870`, `1276788`) `[T1 db2: SpellName @ 12.0.7]`, any of which could be the
  aura the summon actually applies. It is no longer a blocker for reading Tyrant's state:
  the `HideByDefault` bar row (cid `84224`, `flags = 2`, base `265187`) is un-hidden by a
  saved layout on a measured Demonology character, is **totem-backed** rather than
  aura-backed, and answers through the pip and the totem channel (§7 Tier 2/Tier 3)
  `[client 2026-08-09]`. What stays open is the aura's identity itself. `@verify-ingame`
- **`[gap]`** Whether enabling a `HideByDefault` row through the Cooldown Manager's own UI
  actually lands it in a viewer, end to end (§1.2). The Lua path says yes and two rows on
  one measured character are un-hidden by a saved layout — but nobody has performed the
  enable and re-read the bind, so "the player can turn it on" is an inference.
  `@verify-ingame`
- **Not covered here:** the settings/layout serialization format, Edit Mode anchoring of
  the viewer frames, and the `CooldownViewerVisualAlert` pool. None has a consumer in
  this KB yet.

---

## Changelog

- 2026-08-16 — new **§4.2**, the first client measurement on 12.1.0 and the measured
  counterpart to §4.1: a `ClearAllPoints()` + `SetPoint` re-anchor onto a non-parent frame
  takes effect, survives a 138 s fight, and does not disturb the per-frame paint — but only
  in a session where no layout ran, so it says nothing about the `RefreshLayout` teardown.
  An earlier session in which the apply did not take is recorded open, not solved. §0b's
  "every `[client]` tag is 12.0.7" now carries its one exception.
- 2026-08-16 — new **§4.1 layout and ordering**, all source-read at 12.1.0: `layoutIndex` is
  both grid sort key and cooldownID index (so an index-rewrite reorder self-cancels);
  `GetItemFrames()` is intent order, not drawn order; `alwaysUpdateLayout` is never cleared;
  `RefreshLayout` `ReleaseAll()`s and is reachable in combat via `UNIT_AURA` `isFullUpdate`;
  a same-count settings change is in-place; cooldown events never re-layout; an inactive row
  keeps its slot; the pandemic frame anchors onto the item. §8 gains rules 18–23. Six stale
  unstamped locators re-resolved and stamped `@12.1.0` (`RefreshLayout` :1824→:2021,
  `GetItemFrames` :1490→:1636, the `isFullUpdate` branch :1628→:1803, `TriggerAlertEvent`
  :483→:500, `GetOrderedCooldownIDsForCategory` :230→:249, the `OnDataChanged` trigger
  :784→:832), plus the six alert raise sites and the four `.xml` template lines.
- 2026-08-11 — 12.1.0, **source diff only, no re-flight** (§0b is the standing warning).
  `Enum.CooldownViewerCategory` 4 → 9 members: trinkets/potions via `EquipSlot*`,
  racials via `SpecAgnostic*`, plus `GroupBuff` (new §1.3, §1.4). `HiddenSpell` /
  `HiddenAura` **renamed** `HiddenActive` / `HiddenPassive` — reads `nil`, does not
  error (§1.2). Three new row fields + `isInvisible` as a fourth suppression path.
  `GetGroupBuffItems` + `GroupBuffItem` (no `cooldownID`, so §2's ladder does not
  apply). New §5.5 sounds ("Short", 26 entries; Combat Audio Assist) and §5.6 pinging.
  `SPELL_UPDATE_COOLDOWN` gained `itemID`; `UNIT_AURA`'s payload is now fully secret.
  Five `CooldownViewerVisualAlert*` files removed, six added. ⚠ **No `[client]` tag was
  restamped and §2/§3/§7 were not re-derived.**
- 2026-08-09 — **§7: three corrections, all from one in-client sweep.** `C_Spell.GetSpellCooldown`
  is **not** sealed whole — it is a plain table whose members seal individually, and
  `isActive` is a plain, discriminating, in-combat "on cooldown" boolean (`GetSpellCharges`
  stays unmeasured on that point). `Bar.Pip:IsShown()` is **tried and works** — the
  "nobody has tried either" `[gap]` is gone. And the cid-760 summons puzzle is closed the
  other way round: the row is **totem-backed**, so the aura instruments were correctly
  reporting an absent aura. New: the totem channel, and `C_Spell.GetSpellCooldownDuration`
  measured in restricted combat instead of inferred from an annotation. Two traps for anyone
  re-deriving this: `Bar:GetValue()`'s idle secret reads are a **sticky readback class**, not
  a second path that hides the pip — `SetShown(false)` has exactly one call site and it writes
  the plain zeros; and `GetTotemInfo` returns `icon` **fifth**, not last.
- 2026-08-08 — **§7 corrected: "a summon binds no aura" was an overstatement and is gone.**
  The claim now names its two instruments (`auraDataUnit`, the alert channel), its one row
  (cid 760) and its build, and carries a second measurement — **zero alert edges of any kind
  on cid 760 across 1054 edges and 171 Call Dreadstalkers casts**, against 71/70 aura edges on
  Dominion of Argus cid 169561 in the same captures `[client 2026-08-07]`. The hedge that used
  to sit *below* the overstatement is now **in the headline**, because three downstream
  documents had quoted the headline and dropped the correction.
- 2026-08-07 — **§1.2 is new: `HideByDefault`.** A flagged row is filtered out in Blizzard's
  *Lua* at data-set construction (the category is rewritten to a `-1`/`-2` pseudo-category),
  so it **never gets an item frame and therefore raises no alert edge** — which **scopes
  §5.1's `hooksecurefunc(TriggerAlertEvent)` completeness guarantee to bound rows**. The API
  still returns hidden rows, and the Tier-1 struct's `category`/`flags` are the **raw DB2**
  values, never the effective placement. A saved layout can un-hide one, per class+spec, and
  signals it only through a Lua `EventRegistry` callback. §7 Tier 3:
  `C_Spell.GetSpellCooldownDuration` carries **no** `SecretWhenCooldownsRestricted` unlike
  its two siblings — recorded as a **doc-annotation inference, not a measurement**. §8 gains
  rules 16 and 17.
- 2026-08-07 — §2: `overrideSpellID` is the **in-combat display-identity route** — plain on
  every row and observed moving mid-pull. §4: `item:GetSpellID()`'s secret set is **volatile
  between reads and does not track `auraDataUnit`**, so the earlier aura-boundness correlation
  is not a rule. §5.1: `Available` / `OnCooldown` never fire for a row with no real cooldown.
- 2026-08-06 — §2: `overrideSpellID` is **always populated**, so `~= nil` never means
  "overridden" and rung 5 is unreachable. §4: `TRAIT_CONFIG_UPDATED` precedes the CDM
  rebuild by ~5 s, and **disabling the CDM in Options fires none of the nine CDM/talent
  events** — a sampling failure, not a detection one. §7 Tier 1:
  `GetCooldownViewerCategorySet` is a superset of the laid-out rows, not a row count.
  First client evidence from a non-Warlock class.
- 2026-08-05 — absorbed the Cooldown-Manager alert-channel study from
  `api-events-and-discovery.md` §2.8–2.9 (now §2.8, §5.1–5.4, §7 Tier 1 and Tier 3).
- 2026-08-05 — §7 Tier 3: `C_UnitAuras` carries a per-aura `RequiresNonSecretAura`
  precondition this KB had never recorded — but it declares no `FailureMode`, so "a
  non-secret aura still answers" is an open question, not an established escape hatch.
- 2026-07-31 — §5.2: the pandemic fields read SECRET in combat and `IsInPandemicTime`
  *throws* rather than returning a secret, so the guard is `pcall`, not `issecretvalue`.
- 2026-07-31 — §7 Tier 1: `GetValidAlertTypes` gates `PandemicTime` and nothing else; it is
  not "what this row can raise".
- 2026-07-31 — §8 rule 10: tab-1 `item:IsActive()` is a constant `true`, not a signal.
