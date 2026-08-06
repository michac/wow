---
title: The Cooldown Manager — how a CDM row resolves
patch: 12.0.7
fetched: 2026-08-05
reviewed: 2026-08-05   # + a client capture 2026-07-31 (CDMProbe /cdmp census, Destruction both hero trees)
sources:
  - raw/addon-research/wow-ui-source @ 12.0.7.68887 — Interface/AddOns/Blizzard_CooldownViewer/*
  - raw/addon-research/wow-ui-source @ 12.0.7.68887 — Blizzard_APIDocumentationGenerated/CooldownViewer{,Constants}Documentation.lua
  - wago.tools DB2 @ 12.0.7 — CooldownSet, CooldownSetSpell, CooldownSetLinkedSpell (raw/wago/)
  - projects/cooldown-hud/docs/ — CDMProbe in-client captures, session detail
  - in-client capture, CDMProbe AlertTape v0.32.27 (/cdmp alerts), Destruction Warlock, 2026-07-30  # §5.1 alert-channel confirmations
  - in-client capture, CDMProbe AlertTape v0.32.29, Destruction/Hellcaller Warlock, 2026-07-30  # §5.4 same-frame refresh tie; simultaneous PandemicTime on both Immolate cooldownIDs
  - in-client capture, CDMProbe v0.32.32 decision log, Destruction Warlock (Hellcaller AND Diabolist), 2026-07-30  # §2.8 cid 66181's base/display spellID split + hero-talent-dependent isKnown; override event firing for an untracked display id
  - in-client capture, CDMProbe v0.32.46 decision log, Destruction Warlock (both hero trees), 2026-07-31  # §5.3 ChargeGained is a prediction-queue drain, not a charge
  - in-client capture, CDMProbe /cdmp census, Destruction Warlock (both hero trees), 2026-07-31  # §2.5, §7 the readable-surface sweep
  - in-client capture, CDMProbe v0.32.53 flight recorder, Destruction + Demonology Warlock, 2026-08-01  # §7 Tier 3 C_AssistedCombat readable through combat
  - in-client capture, CDMProbe /cdmp curve stack, Demonology Warlock, 2026-08-04  # §7 Tier 2 auraInstanceID plain / auraSpellID secret
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
because the workspace has an addon (`CDMProbe`) built entirely on top of it and the
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

> `[client 2026-07-31]` (CDMProbe `/cdmp census`, Destruction, both hero trees,
> 72 cooldownIDs × in/out of combat). Two separate answers:
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

Two facts `[client 2026-07-30]` (CDMProbe decision log, Destruction Warlock, Hellcaller
**and** Diabolist) that between them break the naive "walk the set, key by `spellID`"
reading of the CDM database.

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
(The general shape — a choke-point method as a dispatch surface, and `hooksecurefunc` on
it as a runtime signal — is [`api-events-and-discovery`](./api-events-and-discovery.md)
§2.8's claim; this section owns the instance.)

The event argument is `Enum.CooldownViewerAlertEventType`, six members
`[T1 docs: CooldownViewerConstantsDocumentation.lua:43-55]`:

| Value | Member | Raised at | What the edge actually means |
|---|---|---|---|
| 1 | `Available` | `CooldownViewer.lua:500` | a cooldown finished — for a charged ability, **once per charge restored**, not once per "became usable" (§5.3) |
| 2 | `PandemicTime` | `:556` | a tracked **target** DoT entered its refresh window (§5.2) |
| 3 | `OnCooldown` | `:1068` | went on cooldown — but **never fires for a charged ability** (§5.3) |
| 4 | `ChargeGained` | `:608` | *one entry in a prediction queue came due*, which is not the same as "+1 charge" (§5.3) |
| 5 | `OnAuraApplied` | `:612` | a **fresh** application — not a stack, not a refresh (§5.4) |
| 6 | `OnAuraRemoved` | `:622` | the bound aura instance went away (§5.4) |

**`[client 2026-07-30]` All six fire in restricted combat** (CDMProbe `AlertTape`,
`/cdmp alerts`, Destruction Warlock, 12.0.7). Counts from one ~80 s pull: `ChargeGained`
×10 (Conflagrate), `OnAuraApplied` ×15, `OnAuraRemoved` ×13, `PandemicTime` ×5; `Available`
×7 and `OnCooldown` on four non-charged entries over a longer pull in the same session.

**Why this channel matters disproportionately under Secret Values.** The alerts are raised
by Blizzard's *trusted* code from data it can see, and the argument is a plain enum — so the
channel carries information in restricted combat that the corresponding direct API reads
refuse. `ChargeGained` is the sharpest case: `C_Spell.GetSpellCharges` is secret in combat,
so a gain *edge* may be the only in-combat charge information available at all. This is the
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
`[client 2026-07-31]` + T1 src:

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
(`ChargeGained` + a seeded baseline, since `C_Spell.GetSpellCharges` is secret in combat),
not from the cooldown edges.

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
(with `allowUnlearned`), `GetValidAlertTypes(cooldownID)` and `IsCooldownViewerAvailable`.

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
| `item.auraDataUnit` | both | **readable** `[client 2026-07-31]` | Plain `"player"` / `"target"`; non-nil **iff** the row has a live bound aura, and it discriminates. The only in-combat "is the DoT up" read available — see below. |
| `item.auraInstanceID` | both | **readable — a plain number** `[client 2026-08-04]` | The key that unlocks the instance-scoped aura APIs — see below. |
| **`item.PandemicIcon`** | both | **readable — presence *is* the live pandemic state** `[client 2026-07-31]` | A frame reference, not a number. `~= nil` mirrors `IsInPandemicTime` exactly — see below. |
| `item.wasSetFromCharges` / `wasSetFromCooldown` / `wasSetFromAura` | tab 1 | **readable** `[client 2026-07-31]` | Plain booleans set by bare assignment `[:648-669]` recording **which of the four sources won this refresh** — i.e. what the dial currently *means*. 66–69 readable vs 9 `nil` per capture, unchanged in and out of combat. The one axis separating "the swipe is a cooldown" from "the swipe is an aura remaining". |
| `item:IsActive()` | tab 2 only, meaningfully | **readable** `[client 2026-07-31]` | On tab 1 it is `cooldownID ~= nil` → a **constant `true`** that is actively misleading, not merely useless (§8 rule 10). Gate on family. |
| `item:IsShown()` | both | conditional | `ShouldBeShown` returns true immediately when `not allowHideWhenInactive` **or** `not hideWhenInactive` `[:311-335]`. If the viewer is not set to hide-when-inactive this is **constant true** and anything driven off it latches on permanently. Capability-check, never assume. |
| `item.cooldownID` | both | **can read secret** | The binding key. Resolve out of combat; never overwrite a known-good id with an unreadable one. |
| `item.cooldownStartTime` / `cooldownDuration` | tab 1 | **secret** | Copied straight from `C_Spell.GetSpellCooldown`, so they inherit its secrecy. Values, not verdicts. |
| `item.pandemicStartTime` / `pandemicEndTime` | both | **secret**; `IsInPandemicTime` **throws** `[client 2026-07-30]` | The throw is a *comparison* failure inside the method body `[:587]`, not a block — so the guard is `pcall`, not `issecretvalue` (§5.2). |
| `item.pandemicAlertTriggerTime` / `nextAvailableTimeToPlayPandemicAlert` | both | **secret** `[client 2026-07-31]` | The alert's arm + throttle, transitioning exactly as `[:548-555]` describes. Useful only as a *class* (armed vs fired); the numbers never read. |
| `item.auraSpellID` | both | **secret** `[client 2026-08-04]` | Written from aura data (`auraInfo.spellId`, §2.5) so it inherits the seal — unlike its sibling `auraInstanceID`. ⚠ **Never compare it; class-check first.** `aid == spellID` on this field threw the moment a pull started and killed an entire refresh loop. |
| `item:GetSpellID()` | both | **secret** `[client 2026-07-31]` | Secret on 8 of 51 frame rows in combat — exactly the rows carrying a live bound aura (rung 1) — and readable on all of them out of combat. `item:GetBaseSpellID()` stays readable throughout: the *display* identity is restricted in combat while the *base* is not, the opposite of what a consumer keying on `GetSpellID()` wants. |
| `item:GetAuraSpellID()` | both | **secret** `[client 2026-07-31]` | Rung 1 is present, not absent — it simply cannot be read while restricted. `nil` out of combat when no aura is bound. |
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
which is the "is the DoT up" read nothing else can currently answer. Together with
`PandemicIcon` a tab-1 row exposes two readable in-combat aura facts: *is it up*, and *is it
in pandemic*.

**`auraInstanceID` is the key to the instance-scoped aura APIs.** `RequiresValidUnitAuraInstance`
APIs need an instance id, and the enumeration that hands them out (`GetAuraDataByIndex` and
friends) is sealed in a pull — but Blizzard's own frame carries one and keeps it fresh
(`SetAuraInstanceInfo`, §2.5). `[client 2026-08-04]` (CDMProbe `/cdmp curve stack`,
Demonology, in combat): a plain number on Wild Imps 296553 and Demonic Core 264173, and it
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

### Tier 3 — the live game API

| Read | Status |
|---|---|
| `UnitPower` | **`[client]`** readable *and branchable* in instanced combat |
| `UNIT_SPELLCAST_*` (player) | **`[client]`** readable spellID in all four phases |
| `C_SpellActivationOverlay.IsSpellOverlayed` | **`[client]`** readable in combat |
| `C_AssistedCombat.GetNextCastSpell` | **`[client 2026-08-01]`** readable — a plain number in combat and out. See below: readability is proven, usefulness is not |
| `C_Spell.GetSpellCooldown` / `GetSpellCharges` | **`[client]`** fully readable **out** of combat, secret **in** |
| `C_UnitAuras.Get*` | The `AuraData` record is secret when restricted. Three getters carry a **per-aura** `RequiresNonSecretAura` precondition — but its failure behaviour is undocumented, see below |

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
not go secret.** `[client 2026-08-01]` (CDMProbe v0.32.53 flight recorder, Destruction +
Demonology): it returns a **plain number** — `issecretvalue()` false, safe to compare, format
and use as a table key — both out of combat and inside a dummy pull, on both `false` and
`true`. `IsAvailable()` returned a plain bool and `GetRotationSpells()` a plain (non-secret)
table in the same samples. Every other cooldown channel in this file refuses in restricted
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
- **Not covered here:** the settings/layout serialization format, Edit Mode anchoring of
  the viewer frames, and the `CooldownViewerVisualAlert` pool. The first two are
  recorded in `projects/cooldown-hud/docs/notes.md`; none has a consumer in this KB yet.

---

## Changelog

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
