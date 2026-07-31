---
title: The Cooldown Manager — how a CDM row resolves
patch: 12.0.7
fetched: 2026-07-31
reviewed: 2026-07-31
sources:
  - raw/addon-research/wow-ui-source @ 12.0.7.68887 — Interface/AddOns/Blizzard_CooldownViewer/*
  - raw/addon-research/wow-ui-source @ 12.0.7.68887 — Blizzard_APIDocumentationGenerated/CooldownViewer{,Constants}Documentation.lua
  - wago.tools DB2 @ 12.0.7 — CooldownSet, CooldownSetSpell, CooldownSetLinkedSpell (raw/wago/)
  - projects/cooldown-hud/docs/notes.md — CDMProbe in-client captures
confidence: high
---

# The Cooldown Manager — how a CDM row resolves

## 0. What this file is, and what it is not

**This is a system study, not one of the seven topic files.** The
[README](./README.md) §1 topic map partitions *mechanisms* — events, frames, taint,
persistence — so that any addon-dev question lands in exactly one file. This file
is organised the other way: around **one Blizzard system**, `Blizzard_CooldownViewer`,
because the workspace has an addon (`CDMProbe`) built entirely on top of it and the
model does not survive being cut into seven pieces.

It therefore **defers to the topics for general mechanism** and only claims what is
specific to the CDM:

| Ask about | Owned by |
|---|---|
| Mixin composition, the data/display split, the dirty flag as a pattern | [`module-architecture`](./module-architecture.md) §2.1, §4.1, §4.3 — already covers `CooldownViewerItemMixin` in detail |
| What secret values are, `SecretArguments`, how to display what you cannot read | [`security-taint-and-restricted-data`](./security-taint-and-restricted-data.md) |
| Event registration mechanics, `hooksecurefunc` as an instrument, `OnUpdate` vs ticker | [`api-events-and-discovery`](./api-events-and-discovery.md) |
| Texture channels, pooling, anchoring to Blizzard frames | [`frames-textures-animation`](./frames-textures-animation.md) |

⚠ **This file breaks a global property of the subtree.** README §0 states that nothing
under `addon-dev/` has been executed in the client. That remains true of the seven
topics; it is **not** true here. A subset of the claims below are **client-confirmed**
from CDMProbe sessions and are marked **`[client]`** with their capture. Everything
else is a source read at the pinned build, and unsettled claims carry
`@verify-ingame` as usual.

---

## 1. The two families

A CDM row belongs to one of two families, and **the family is the only stable fact
about it.** Everything else — its identity, what its dial means — is re-derived on
every refresh.

The settings panel presents exactly two tabs, and they map to disjoint category sets:

```lua
local displayModeToCategories =
{
	["spells"] = { Enum.CooldownViewerCategory.Essential, Enum.CooldownViewerCategory.Utility, Enum.CooldownViewerCategory.HiddenSpell },
	["auras"] = { Enum.CooldownViewerCategory.TrackedBuff, Enum.CooldownViewerCategory.TrackedBar, Enum.CooldownViewerCategory.HiddenAura },
};
```
`[T1 src: Blizzard_CooldownViewer/CooldownViewerSettings.lua:1463-1467]`

The same spell/aura split appears in the data provider's hidden-category mapping —
Essential and Utility fall back to `HiddenSpell`, TrackedBuff and TrackedBar to
`HiddenAura`
`[T1 src: .../CooldownViewerSettingsDataProvider.lua:47-52]`.

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
| Categories | Essential, Utility | TrackedBuff, TrackedBar |
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

> **@verify-ingame** — because Blizzard mutates the provider's cached struct in place,
> a frame's `cooldownInfo.overrideSpellID` and a *fresh*
> `C_CooldownViewer.GetCooldownViewerCooldownInfo(id)` are different objects and may
> disagree. Whether the C side also carries the override into a fresh read is untested.
> Until settled, track overrides from `COOLDOWN_VIEWER_SPELL_OVERRIDE_UPDATED` rather
> than assuming a fresh struct read reflects them.

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
2. `445474` Wither appears as a candidate in both a cast-based row and an aura-based
   row, consistent with Wither using **one spellID for both the cast and its aura** —
   unlike Immolate, which splits them. @verify-ingame (DB2 shape is consistent with it;
   not independently confirmed).

**`[client]`** Those two cooldownIDs are the exact pair in CDMProbe's captured
same-frame pandemic tie — `OnAuraRemoved` + `OnAuraApplied` on cid `133441` and
`164597`, all at `131184.611` (2026-07-30 capture,
`projects/cooldown-hud/docs/field-fixes-plan.md`).

**Rung 3 in Warlock terms:** 8 rows carry the `UseAsTooltip` flag
(`Enum.CooldownSetLinkedSpellFlags.UseAsTooltip`), e.g. cid `182891` Grimoire: Imp Lord
→ tooltip `1288945` Imp Lord. A rung-3 candidate displays **even with nothing live**,
which is what separates it from rung 2.

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
| `UNIT_AURA` full update | bulk | `isFullUpdate` short-circuits per-aura routing and calls `RefreshLayout()` on the whole viewer `[:1628-1633]` — the heaviest path, and the one that re-pools frames. |

---

## 5. Events — and they differ by family

Six registered by the shared viewer mixin
`[T1 src: CooldownViewer.lua:1556-1561]`; **five more by tab 1 only**
`[T1 src: :1948-1952]`; tab 2 adds nothing.

| Event | Family | Effect on the row |
|---|---|---|
| `COOLDOWN_VIEWER_SPELL_OVERRIDE_UPDATED` | both | Writes rung 4, then full `RefreshData`. Fires **redundantly** — Blizzard's own `SetOverrideSpell` early-returns on an unchanged value `[ItemData.lua:88-105]`. |
| `SPELL_UPDATE_COOLDOWN` | both | May re-elect rung 2 (§2.2 path B), then `RefreshData`. |
| `UNIT_AURA` | both | Registered `("player", "target")` only. Routed by `auraInstanceID` to exact frames; added-auras fan out to all. |
| `UNIT_TARGET` | both | `OnNewTarget` on every frame: clears the link, clears pandemic timing, forces inactive `[:631-638]`. |
| `SPELL_UPDATE_ICON` | both | Texture only — no re-resolve. |
| `PLAYER_TOTEM_UPDATE` | both | Rebinds totem data, which outranks auras in both families. |
| `SPELL_ACTIVATION_OVERLAY_GLOW_SHOW` / `_HIDE` | **tab 1** | The proc glow — §6. |
| `SPELL_UPDATE_USES` | **tab 1** | Recomputes charges only. |
| `SPELL_UPDATE_USABLE` | **tab 1** | Icon colour only. Fires constantly in a city. |
| `SPELL_RANGE_CHECK_UPDATE` | **tab 1** | Out-of-range tint; only for rows whose base spell has a range `[:709-716]`. |

### 5.1 The alert choke point — available on both families

`CooldownViewerItemMixin:TriggerAlertEvent(event)` `[T1 src: CooldownViewer.lua:483-494]`
is called from all six alert paths and is **invoked unconditionally** — the user's
alert configuration is consulted *inside* the body (`self.alertsByEvent[event]`).
So `hooksecurefunc(item, "TriggerAlertEvent", …)` observes **every edge, even for
spells the user has configured no alert on.** Because the methods are `Mixin()`-copied
onto each frame, the hook must go on the item **instance**, not the shared mixin table.

The six types
`[T1 src: Blizzard_APIDocumentationGenerated/CooldownViewerConstantsDocumentation.lua]`:
`Available=1 · PandemicTime=2 · OnCooldown=3 · ChargeGained=4 · OnAuraApplied=5 ·
OnAuraRemoved=6`.

**`[client]`** All six confirmed firing in restricted combat, with per-type meanings
pinned, in the 2026-07-30 CDMProbe capture (see
`api-events-and-discovery.md` §2.8). This is the single best in-combat signal on either
side of the split, because it is an observation of a choke point rather than a
secret-guarded API read.

Pandemic arms **only** when `GetAuraDataUnit() == "target"`, and its window derives from
two secret numbers — you get the edge, never the seconds
`[T1 src: CooldownViewer.lua:511-532]`.

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

### Tier 1 — structural config (identical on both families)

`C_CooldownViewer.GetCooldownViewerCooldownInfo(cooldownID)` returns
`{cooldownID, spellID, overrideSpellID, overrideTooltipSpellID, linkedSpellIDs[],
selfAura, hasAura, charges, isKnown, flags, category}`
`[T1 src: Blizzard_APIDocumentationGenerated/CooldownViewerDocumentation.lua]`.
Readable config even when live state is not. Also `GetCooldownViewerCategorySet`
(with `allowUnlearned`), `GetValidAlertTypes(cooldownID)` — a readable *capability*
probe, currently under-used — and `IsCooldownViewerAvailable`.

⚠ **`hasAura` / `selfAura` / `charges` have zero consumers in Blizzard's Lua.** A grep
across all of `Interface/` finds them only in the generated documentation table. They
are DB2 hints the C side consumes. **Any classifier built on them is the addon
author's own invention**, and one such classifier has already been falsified:
**`[client]`** Demonic Core measures `selfAura=true, hasAura=false` (cooldownID 777),
refuting the rule "`hasAura=false` ⇒ a real cooldown" that
`projects/cooldown-hud/docs/notes.md` asserted until 2026-07-31. *(Corrected in that
file; the refuted claim is retained there with its reasoning.)* Classify on **family**
(§1.1) instead.

### Tier 2 — derived state parked on the item frame

| Field / method | Family | Status | Notes |
|---|---|---|---|
| `item.cooldownID` | both | readable; **can read secret in restricted combat** | The binding key. Resolve out of combat; never overwrite a known-good id with an unreadable one. |
| `item:IsActive()` | **tab 2 only, meaningfully** | **`[client]`** readable | On tab 1 it is `cooldownID ~= nil` → **constant true**. Same method, two meanings (§1.1). |
| `item.auraDataUnit` | both | **@verify-ingame** | A plain `"player"`/`"target"` string — the only thing that says **which side the bound aura is on**. Nothing in the struct carries this. High value if it reads clean. |
| `item.wasSetFromCharges` / `wasSetFromCooldown` / `wasSetFromAura` | tab 1 | **@verify-ingame** | Plain booleans set by bare assignment `[:648-669]`, recording **which source won this refresh** — i.e. what the dial currently *means*. Set by untainted code, same shape as `isActive`, so plausibly clean. **Measure before consuming.** |
| `item.cooldownStartTime` / `cooldownDuration` | tab 1 | secret in combat | Copied straight from `C_Spell.GetSpellCooldown`, so they inherit its secrecy. Values, not verdicts. |
| `item.pandemicStartTime` / `pandemicEndTime` | both | **`[client]`** secret in combat; `IsInPandemicTime` **throws** | 2026-07-30 capture. The `PandemicTime` alert fires normally — take the edge, never the number. |
| `item:IsShown()` | both | conditional | `ShouldBeShown` returns true immediately when `not allowHideWhenInactive` **or** `not hideWhenInactive` `[:311-335]`. If the viewer is not set to hide-when-inactive, this is **constant true** and anything driven off it latches on permanently. Capability-check, never assume. |

### Tier 3 — the live game API

| Read | Status |
|---|---|
| `UnitPower` | **`[client]`** readable *and branchable* in instanced combat |
| `UNIT_SPELLCAST_*` (player) | **`[client]`** readable spellID in all four phases |
| `C_SpellActivationOverlay.IsSpellOverlayed` | **`[client]`** readable in combat |
| `C_Spell.GetSpellCooldown` / `GetSpellCharges` | **`[client]`** fully readable **out** of combat, secret **in** |
| `C_UnitAuras.Get*` | The **entire `AuraData` record** is secret when restricted — including `GetPlayerAuraBySpellID`. Your own auras are as sealed as the target's. See `security-taint-and-restricted-data.md`. |

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

---

## 9. Gaps and pending work

- **`[gap]`** Whether `wasSetFrom*` and `auraDataUnit` survive restricted combat is the
  highest-value open measurement here (§7). Both are cheap to test with a
  `/reload`-flushed capture.
- **`[gap]`** Whether a fresh `GetCooldownViewerCooldownInfo` reflects overrides that
  Blizzard wrote into the provider's cached struct (§2.5).
- **`[gap]`** Whether Wither uses one spellID for cast and aura (§2.7). DB2 shape is
  consistent with it; not confirmed.
- **Applied 2026-07-31 —** `projects/cooldown-hud/docs/notes.md` ("Aura-backed cooldown
  items") asserted `hasAura=false ⇒ a real cooldown` and described a CDM item as an
  abstraction over *three* backing sources. Both corrected in place (four sources; the
  `hasAura`/`selfAura` oracle retained as a refuted claim with its reasoning, replaced
  by the family split). That file now defers here for the resolution model and keeps
  only its DoT-specific taint ledger.
- **Not covered here:** the settings/layout serialization format, Edit Mode anchoring of
  the viewer frames, and the `CooldownViewerVisualAlert` pool. The first two are
  recorded in `projects/cooldown-hud/docs/notes.md`; none has a consumer in this KB yet.
