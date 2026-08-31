---
title: Cooldown-Manager rider patterns — 12.1 secret-safe API cookbook
patch: 12.1.0
fetched: 2026-08-12
reviewed: 2026-08-31   # 2026-08-31: §4.6.1 gained the TWO-RIDERS hazard — one item frame carrying two SetPoint reasserts recurses without bound, which is a client crash, plus the two-stage detection and the published conflict-table shape, from an EllesmereUI 9.0.8 live-install read. 2026-08-27: §4.6 rewritten from an EllesmereUI 9.0.5 mining pass — the in-combat reposition question is CLOSED (Tier-1 absence check on CooldownViewer.xml + a shipping addon doing it ungated) and §4.6.1 records the per-frame SetPoint reassert seam. 2026-08-21: §2's EvaluateRemainingDuration second argument corrected to the DurationTimeModifier and §9.2 rewritten on the UNIT_SPELLCAST secrecy annotation, both from the 12.1.0 generated docs. 2026-08-21: the aura-edges frame-enumeration form retired as validated-in-cap (confirmed-by-use, not a controlled measurement). §11 re-grounded 2026-08-19 on shipped 12.1 source; the rest not re-checked — read each [client] tag, not this line
sources:
  - "Cooldown Companion 2.0 (live install)"
  - "Cooldown Manager Centered 4.2.1 (live install)"
  - "EllesmereUI Cooldown Manager 8.8.4 (live install)"
  - "EllesmereUI 9.0.5 (live install, EllesmereUICooldownManager) — mined 2026-08-27 for the
    CDM item-frame reposition question. License CUSTOM, ALL RIGHTS RESERVED; read for API
    discovery only, no code copied"
  - "EllesmereUI 9.0.8 (live install, EllesmereUI + EllesmereUICooldownManager) — read
    2026-08-31 for the two-riders-on-one-frame hazard and the conflict-table surface.
    License CUSTOM, ALL RIGHTS RESERVED; read for API discovery only, no code copied"
  - "Blizzard UI source 12.1.0 — Blizzard_ActionBar, Blizzard_SharedXML/BindingUtil.lua, Blizzard_APIDocumentationGenerated/ActionBarFrameDocumentation.lua"
  - raw/addon-research/wow-ui-source-12.1.0 @ 12.1.0.69273 — Blizzard_APIDocumentationGenerated/LuaDurationObjectAPIDocumentation.lua, UnitDocumentation.lua. `[T1 docs @12.1.0]` locators resolve here
confidence: medium
---

# Cooldown-Manager rider patterns — a 12.1 secret-safe API cookbook

**What this file is.** A distilled cookbook of the API-usage patterns that shipping,
actively-maintained addons use to ride Blizzard's Cooldown Manager (the CDM) on patch
12.1 and to survive the Secret-Value restrictions. It is organised by problem, not by
addon: the same handful of idioms recur across every CDM rider, and the value is the
idiom.

**How these are known, and their confidence.** Every snippet was distilled from live
addons that run on the current patch, then rewritten as a minimal self-contained
illustration — the shapes are faithful to the working code but carry no line-level
provenance by design. The readable-vs-secret boundary claims below describe **what these
addons treat as safe in practice**, which is strong evidence (their authors get bug
reports when it is wrong) but is not the same as our own in-client measurement. Treat a
claim here as `medium` confidence and, where it is load-bearing, confirm it against the
measured facts in `security-taint-and-restricted-data.md` and `cooldown-manager.md`
before building on it. This file is a curated read, not a queue.

---

## 1. The secret-value model — the ground everything stands on

On 12.1, a growing set of the numbers an addon once read straight off the API now arrive
as **secret values** in restricted contexts (instanced combat above all). A secret is a
tagged number/boolean you may **pass to certain engine setters** but may **not** compare,
do arithmetic on, use as a table key, or test for truthiness. Doing any of those raises a
Lua error that aborts the running handler — and if that handler is a `pairs()` event loop,
it takes every later frame in the loop down with it.

The single global that arbitrates it:

```lua
-- issecretvalue(x) -> boolean. Present on 12.x; may be absent on older clients, so
-- guard its own existence when the addon supports back-versions.
if issecretvalue and issecretvalue(x) then
    -- x is secret: do not compare / index / add. Only hand it to an allowed setter.
end
```

### 1.1 The reading rules the addons converge on

Four idioms appear, verbatim in spirit, across all three addons:

**a) Secret-first ordering.** The `issecretvalue` guard must come **before** any other
test, because the "other test" is itself illegal on a secret:

```lua
local function IsUsableSpellID(id)
    if type(id) ~= "number" then return false end          -- see (b): type() not == nil
    if issecretvalue and issecretvalue(id) then return false end  -- BEFORE the > 0 / floor test
    return id > 0 and id == math.floor(id)
end
```

**b) `type(x) ~= "number"`, never `x == nil`.** A secret compares as an error, so even
`x == nil` throws. `type()` is safe and reports `"number"` for a secret — which is exactly
why the `issecretvalue` guard has to run first to separate a real number from a secret one.

**c) Let the value BE the alpha — write it, do not branch on it.** The cleanest secret
trick: if you want to hide a widget when a secret count is zero, write the count straight
into `SetAlpha` (an `AllowedWhenTainted` setter that clamps to `[0,1]`), so `0 -> hidden`,
`1+ -> shown`, with no comparison ever performed:

```lua
local cc = chargeInfo.currentCharges
if issecretvalue and issecretvalue(cc) then
    fontString:SetAlpha(cc)              -- secret written straight through; engine clamps
elseif type(cc) ~= "number" then
    fontString:SetAlpha(1)               -- missing -> visible
else
    fontString:SetAlpha(cc > 1 and 1 or cc)  -- readable -> branch normally
end
```

**d) Fail closed, then prove it structurally.** When a numeric read is unreadable, do not
guess — keep the prior/safe state, and if you still need a decision, derive it from
**never-secret structural fields** (see §1.3) using only `nil`-compares and boolean reads:

```lua
local ok, curDur = pcall(function() return someCooldown:GetCooldownDuration() end)
if not ok or (issecretvalue and issecretvalue(curDur)) then
    -- fall back to a structural proof, e.g. info.linkedSpellID == nil, never the number
end
```

### 1.2 The `AllowedWhenTainted` setter set

These setters accept a secret value and write it without error, which is what makes the
whole "decide engine-side" strategy (§2) possible. The recurring safe set:

```lua
Cooldown:SetCooldownFromDurationObject(durObj)   -- render a cooldown from an opaque object
Cooldown:SetSwipeColor(r, g, b, a)               -- a may be secret
Texture:SetDesaturation(value)                   -- value may be secret (0..1)
Region:SetAlpha(value)                           -- value may be secret; clamps to [0,1]
```

### 1.3 What stays readable (as these addons rely on it)

Not everything is sealed. The addons read these **bare**, with no guard, and treat them as
always-available — the useful readable surface a rider still has in combat:

- `C_Spell.GetSpellCooldown(spellID).isOnGCD` — commented in one addon as *"NeverSecret
  (always readable even during restricted combat)"*. The GCD-vs-cooldown discriminator.
- `C_Spell.GetSpellCooldown(spellID).isActive` and `.isEnabled` — booleans, read bare.
- `C_Spell.GetSpellCharges(spellID).maxCharges` — read bare (the *current* charges are the
  secret half; see §3).
- Structural CDM fields: `info.cooldownID`, `info.linkedSpellID` / `info.linkedSpellIDs`.
- `C_Spell.IsSpellUsable(spellID) -> isUsable, notEnoughPower` — both booleans, read bare.

The dividing line, in one sentence: **identities and booleans tend to stay readable; live
magnitudes (remaining time, current charges, current power in tainted combat, aura
application counts, sometimes even frame sizes) go secret.**

---

## 2. Deciding from a secret without reading it — the engine-curve read

The most important pattern in the whole file. When you need a **decision** that depends on
a secret magnitude ("is the recharge shorter than the running GCD?", "is any cooldown
remaining, so I should desaturate?"), you never read the magnitude. You build a curve that
encodes the decision, hand it plus the opaque duration object to the engine, and the
engine evaluates the secret internally and returns the mapped result (which may itself be
secret — and you pipe it straight into an `AllowedWhenTainted` setter).

⚠ **The second argument is the `DurationTimeModifier`, not a fallback value.**
`EvaluateRemainingDuration(curve, modifier)` declares `modifier` as
`{ Name = "modifier", Type = "DurationTimeModifier", Nilable = false, Default = "RealTime" }`
`[T1 docs @12.1.0: LuaDurationObjectAPIDocumentation.lua — EvaluateRemainingDuration]`, and its
sibling `FormatRemainingDuration` takes the same enum. Passing a number there is passing a
`DurationTimeModifier` whose value happens to be `0` — it does not supply a value for the
"duration carries nothing" case, and there is no argument on this method that does. Feature-gate
`Enum.DurationTimeModifier` alongside the curve enums and pass the member by name.

The opaque duration object comes from one of two spell APIs:

```lua
local durObj = C_Spell.GetSpellCooldownDuration(spellID)   -- cooldown remaining
local durObj = C_Spell.GetSpellChargeDuration(spellID)     -- recharge remaining
```

Build a step curve and evaluate it:

```lua
-- Feature-gate everything first; on a client missing any piece, return the fallback.
if not (durObj and durObj.EvaluateRemainingDuration
        and C_CurveUtil and C_CurveUtil.CreateCurve
        and Enum and Enum.LuaCurveType and Enum.DurationTimeModifier) then
    return fallback
end

local curve = C_CurveUtil.CreateCurve()
curve:SetType(Enum.LuaCurveType.Step)
curve:AddPoint(0, 0)         -- x = remaining seconds, y = mapped result
curve:AddPoint(0.001, 1)     -- any remaining > 0 maps to 1

-- The engine reads the secret remaining-time, applies the curve, returns the result.
-- Second arg is the DurationTimeModifier, NOT a fallback -- it selects which clock the
-- remaining time is measured against, and its documented default is RealTime.
local value = durObj:EvaluateRemainingDuration(curve, Enum.DurationTimeModifier.RealTime)
```

### 2.1 Desaturate an icon while it is on cooldown

```lua
-- Build the curve once at module scope; apply per frame every refresh.
local desatCurve = C_CurveUtil.CreateCurve()
desatCurve:SetType(Enum.LuaCurveType.Step)
desatCurve:AddPoint(0, 0)
desatCurve:AddPoint(0.001, 1)

local function ApplyCooldownDesaturation(frame, durObj)
    local val = durObj:EvaluateRemainingDuration(desatCurve, Enum.DurationTimeModifier.RealTime)
    frame.texture:SetDesaturation(val or 0)   -- AllowedWhenTainted; val may be secret
end
```

### 2.2 Suppress a charge swipe that would end within the current GCD

A subtler curve: the threshold (GCD length) is computed from a value (`UnitSpellHaste`)
that is *also* secret in instanced combat, so it is guarded and floored first, then the
"recharge shorter than the GCD?" comparison is pushed into the curve's break point:

```lua
local function GCDTailAlpha(durObj, normalAlpha)
    local haste = (UnitSpellHaste and UnitSpellHaste("player")) or 0
    if (issecretvalue and issecretvalue(haste)) or type(haste) ~= "number" then
        haste = 0                                   -- secret haste -> assume unhasted
    end
    local len = 1.5 / (1 + haste / 100)
    if len < 0.75 then len = 0.75 end               -- engine GCD floor

    local curve = C_CurveUtil.CreateCurve()
    curve:SetType(Enum.LuaCurveType.Step)
    curve:AddPoint(0, 0)                             -- recharge ends before GCD -> hide
    curve:AddPoint(len, normalAlpha)                 -- recharge outlasts GCD -> show
    return durObj:EvaluateRemainingDuration(curve, Enum.DurationTimeModifier.RealTime)
end

-- consumed straight into an allowed setter:
cd:SetSwipeColor(0, 0, 0, GCDTailAlpha(chargeDurObj, 0.7))
```

### 2.3 The scratch-frame variant — "is it on cooldown?" as a plain boolean

A second, lighter technique for the yes/no case: feed the duration object into a **hidden
throwaway Cooldown widget** and read `IsShown()`, which is a plain boolean even when the
underlying time is secret.

```lua
-- One hidden scratch frame at module scope.
local scratchParent = CreateFrame("Frame"); scratchParent:Hide()
local scratchCooldown = CreateFrame("Cooldown", nil, scratchParent, "CooldownFrameTemplate")

local function DurationObjectShowsCooldown(durObj)
    if not durObj then return false end
    scratchCooldown:SetCooldownFromDurationObject(durObj)
    local shown = scratchCooldown:IsShown()   -- plain bool, secret-safe
    scratchCooldown:SetCooldown(0, 0)          -- reset for the next probe
    return shown
end
```

Note the standing hazard one addon documents: after `SetCooldownFromDurationObject`, the
widget's `GetCooldownTimes()` returns **secret** values — so cache the duration object you
rendered and re-read *it*, never scrape the times back off the widget.

**Measured here, and it holds.** `[client 2026-08-16]` Havoc, 9 Essential rows, in a pull:
feeding each row's `C_Spell.GetSpellCooldownDuration(spellID, true)` into the scratch widget
and reading `IsShown()` gave a **plain boolean on 9 of 9** — never secret, never threw — and
the 8-false / 1-true split matched, row for row, an independent read of the CDM's own
`GetCooldownFrame():IsShown()` in the same run (`cooldown-manager.md` §7). Two different
routes, same answer. This was a mined claim until then; it is ours now, and it is a
general-purpose "is any duration running" primitive rather than a CDM-only one — it needs
only a spellID.

---

## 3. Reading cooldowns and charges secret-safely

### 3.1 The info table, then duration objects

```lua
local info = C_Spell.GetSpellCooldown(spellID)
-- info = { isActive, isEnabled, isOnGCD, timeUntilEndOfStartRecovery, ... }
local isOnGCD = info.isOnGCD or false                          -- NeverSecret

if info.isActive then
    local durObj     = C_Spell.GetSpellCooldownDuration(spellID)        -- GCD-inclusive
    local realDurObj = C_Spell.GetSpellCooldownDuration(spellID, true)  -- true = IGNORE the GCD
    -- classify: a GCD-only "cooldown" must never read as real unavailability
    local realShown   = DurationObjectShowsCooldown(realDurObj)
    local normalShown = DurationObjectShowsCooldown(durObj)
    local gcdOnly = normalShown and not realShown and info.isActive and info.isOnGCD
end
```

### 3.2 Deferred-cooldown detection off the info table

Distinguishes a genuine post-cast lockout from a plain ready state without touching a
secret number:

```lua
local function IsSpellCooldownDeferred(info)
    if info.isEnabled ~= false or info.isActive == true then return false end
    if info.isOnGCD == true then return false end
    local t = info.timeUntilEndOfStartRecovery
    if t == nil then return true end
    if issecretvalue and issecretvalue(t) then return true end   -- unreadable -> stay deferred
    return t <= 0
end
```

### 3.3 The action-slot fallback when the spell cooldown is fully sealed

When `C_Spell.GetSpellCooldown(spellID)` returns `nil` because the cooldown is restricted,
the **action-bar** APIs still hand back duration objects for the same spell. Gate the
fallback on an explicit secrecy query so you only pay for it when needed:

```lua
-- 1. Ask whether this spell's cooldown is secret (0 == not secret).
local secrecy = C_Secrets and C_Secrets.GetSpellCooldownSecrecy
             and C_Secrets.GetSpellCooldownSecrecy(spellID) or 0

-- 2. If the direct read is gone and the cooldown is secret, probe the action slots.
local function ProbeActionSlots(spellID)
    local slots = C_ActionBar.FindSpellActionButtons(spellID)   -- array of slots, or nil
    if not slots then return nil end
    for _, slot in ipairs(slots) do
        local durObj     = C_ActionBar.GetActionCooldownDuration(slot)        -- GCD-inclusive
        local realDurObj = C_ActionBar.GetActionCooldownDuration(slot, true)  -- ignore GCD
        if DurationObjectShowsCooldown(durObj) or DurationObjectShowsCooldown(realDurObj) then
            return { durObj = durObj, realDurObj = realDurObj, slot = slot }
        end
    end
end

local info = C_Spell.GetSpellCooldown(spellID)
if not info and secrecy ~= 0 then
    local probe = ProbeActionSlots(baseSpellID or spellID) or ProbeActionSlots(displaySpellID)
    -- render probe.realDurObj (preferred) or probe.durObj via SetCooldownFromDurationObject
end
```

Probe the **base** spell ID first, then the **display/override** ID — a transformed spell
can sit in the bar under either. Keep the dedupe/scratch tables at module scope and
`wipe()` them each pass so no Blizzard frame reference leaks across ticks.

### 3.4 Charges — the current count is the secret half

```lua
local charges = C_Spell.GetSpellCharges(spellID)
-- { currentCharges, maxCharges, cooldownStartTime, cooldownDuration, chargeModRate }

local cur
if charges and charges.currentCharges ~= nil
   and not (issecretvalue and issecretvalue(charges.currentCharges)) then
    cur = charges.currentCharges                 -- trust only when readable
end

-- maxCharges is read bare; <= 1 means "not really a charge spell"
local hasCharges = charges and charges.maxCharges and charges.maxCharges > 1

-- recharge as a duration object (nil when maxCharges == 1)
local chargeDurObj = hasCharges and C_Spell.GetSpellChargeDuration(spellID) or nil
```

**Text-only fallback when the count is secret.** `C_Spell.GetSpellDisplayCount` returns a
display value that is safe to hand straight to a FontString even when you cannot read the
number in Lua:

```lua
if cur then
    button.count:SetText(cur)                               -- readable number
else
    button.count:SetText(C_Spell.GetSpellDisplayCount(spellID))  -- secret-safe display text
end
```

**Refuse to infer charge state from usability when the count is secret.** A spell can be
unusable for reasons unrelated to charges (cost, reactive windows), so a secret count
leaves the zero-state genuinely *unknown* — do not guess it false:

```lua
if secretDisplayCount then
    button._chargeRecharging = false   -- leave unknown; never derive "0 charges" from IsSpellUsable
end
```

**Override-aware max charges** — a transformed variant can carry the real count the base
lacks:

```lua
local overrideID = C_Spell.GetOverrideSpell(spellID)
if overrideID and overrideID ~= 0 and overrideID ~= spellID then
    local overrideInfo = C_Spell.GetSpellCharges(overrideID)
    -- adopt the override's maxCharges when it reports more
end
-- NB: 0 is truthy in Lua, so an override of 0 ("none") must be checked explicitly.
```

---

## 4. Hooking and skinning the Cooldown Manager

### 4.1 The viewer globals and the Layout / RefreshLayout split

The CDM exposes four viewer frames as named globals:

```lua
EssentialCooldownViewer
UtilityCooldownViewer
BuffIconCooldownViewer
BuffBarCooldownViewer
```

The mined rule is *"hook `Layout` on the Essential/Utility viewers, but `RefreshLayout`
on the buff viewers"*, on the reasoning that Blizzard drives the buff viewers' dynamic
set through the second. **Read it as a floor, not a partition: hook both methods on all
four viewers.** `cooldown-manager.md` §4.1 has the source reads. Two of them bite here:
`RefreshLayout` is the *destructive* path on **every** viewer family — it releases the
whole item-frame pool, and the reset callback hides each frame and clears its anchors —
and it is reachable **in combat** on Essential and Utility too, because a `UNIT_AURA`
full update short-circuits straight into it. A rider that watches only `Layout` on those
two misses the one refresh that actually threw its work away.

```lua
for _, viewer in ipairs({ EssentialCooldownViewer, UtilityCooldownViewer,
                          BuffIconCooldownViewer,  BuffBarCooldownViewer }) do
    hooksecurefunc(viewer, "Layout",        OnViewerRelaidOut)
    hooksecurefunc(viewer, "RefreshLayout", OnViewerRelaidOut)  -- the destructive one
end
```

⚠ **On the destructive path, re-apply is the wrong repair — rebuild.** The pool releases
through a map and re-acquires off a stack, so after a `RefreshLayout` the frame that drew
one row routinely draws another (`cooldown-manager.md` §4.1). A rider holding a
cooldownID → frame table and re-decorating those frames therefore puts correct work on the
wrong icons, and its own bookkeeping cannot detect it, because the cached id is the thing
that is wrong. Re-enumerate `GetItemFrames()` and re-read each `GetCooldownID()`; treat a
live id that disagrees with the cached one as the signal to discard the whole table.

`Layout` still fires often enough to be the wrong place for expensive work: the viewer
sets `alwaysUpdateLayout` and never clears it, so every `Layout()` call re-anchors every
child unconditionally — there is no "nothing changed" early-out to ride on.

**On the combat gate. Repositioning a CDM item frame in combat is a SHIPPING technique,
not a theoretical one** `[T3 obs 2026-08-27]`. The earlier mined text said *any*
repositioning of a Blizzard viewer must be gated so it never runs in combat. That is
wrong, and the correction is now evidenced on both sides:

- **Tier 1, the absence check.** The item templates declare no `protected` attribute and
  no secure template
  `[searched 2026-08-27: Blizzard_CooldownViewer/CooldownViewer.xml for `protected`,
  `SecureFrameTemplate`, `SecureActionButtonTemplate` — no match]`, and the one
  secure-named file in the folder is about secret aura-instance
  map KEYS, not frame protection `[T1 src @12.1.0: CooldownViewerSecure.lua —
  CreateSecureAuraInstanceMap, 36 lines, entire file]`. Nothing marks these frames
  protected at load or at runtime.
- **Tier 3, the existence proof.** EllesmereUI's whole CDM bar system re-anchors
  individual item frames onto its own containers and **carries no `InCombatLockdown`
  gate anywhere on that path** — not in `LayoutCDMBar`, not in `CollectAndReanchor`, and
  not in the reassert hook `[T3 obs: EllesmereUICooldownManager 9.0.5 (live install) —
  EllesmereUICooldownManager.lua:4106-4620 scanned exhaustively for InCombatLockdown, no
  hits; EllesmereUICdmHooks.lua:6107 CollectAndReanchor head. Read for API discovery
  only, no code copied]`.

So `InCombatLockdown()` is **not** what decides whether a `SetPoint` is legal here, and a
rider that gates its re-apply on it will simply lose its layout for the length of every
fight in which the CDM rebuilds.

### 4.6.1 The reassert seam is the ITEM FRAME's own `SetPoint`, not the viewer's `Layout`

⚠ **This is the finding that matters, and it is an architecture difference rather than a
tuning one.** Hooking the viewer's `Layout` / `RefreshLayout` and re-applying afterwards
is a *deferred* repair: Blizzard moves your frames, your hook fires, and you put them
back on a later frame or a later tick. Every path that can refuse in between — a combat
gate, a re-bind that needs to run out of combat, a debounce timer — is a window in which
the player sees Blizzard's layout.

The shipping alternative hooks **`SetPoint` on each item frame** and re-applies
*synchronously, inside Blizzard's own call*:

```lua
-- OUR illustration of the fact, written from scratch. `anchor` is the position this
-- rider decided the frame should hold; `container` is the rider's own frame.
hooksecurefunc(itemFrame, "SetPoint", function(_, _point, relativeTo)
    if relativeTo == container then return end   -- our own write; do not recurse
    itemFrame:ClearAllPoints()
    itemFrame:SetPoint(anchor.point, container, anchor.relPoint, anchor.x, anchor.y)
end)
```

There is no window: whatever moved the frame — `Layout`, `RefreshLayout`, or an internal
path with no hook of its own — the correction lands in the same call stack.
`[T3 obs: EllesmereUICooldownManager 9.0.5 — EllesmereUICdmHooks.lua:2624-2657, the
per-frame SetPoint hook; EllesmereUICooldownManager.lua:4473 and :4598, where the desired
anchor is stamped. Read for API discovery only, no code copied]`

Two mechanics the seam requires, both derivable from the code rather than from its
comments:

1. **Recognise your own writes or recurse forever.** The discriminator used in the wild is
   the `relativeTo` argument — if the frame is being pointed at the rider's own container,
   the rider did it. `[T3 obs: EllesmereUICdmHooks.lua:2651-2652]`
2. **Stamp the desired anchor BEFORE calling `SetPoint`**, because the hook fires
   synchronously during that call and will otherwise read the previous anchor and undo the
   move you are making. `[T3 obs: EllesmereUICooldownManager.lua:4595-4599 — the store
   precedes the SetPoint]`

⚠ **`SetPoint` with the same anchor keyword REPLACES that point; a different keyword
ACCUMULATES a second, conflicting one.** A reassert path and a claim path that disagree
about the keyword will fight rather than overwrite.
`[T3 obs: EllesmereUICdmHooks.lua:2639-2641]` `@verify-ingame`

`[gap]` Whether EllesmereUI applies a **user-authored** order to the icons it collects, or
merely packs them into its bars in the viewer's own order, was not established — it does
not change the reassert mechanism, but it is the open half of "is anyone else ordering
rows by intent". Not searched.

⚠ **One claim here is comment-sourced only and is graded accordingly:** that the client
re-raises an item frame's alpha through paths a `SetAlpha` hook cannot observe
(`SetAlphaFromBoolean`, alpha animations), which is why an unclaimed frame is parked
off-screen by POSITION rather than hidden by alpha. The code shows only the choice, not
the reason. `[T3 comment: EllesmereUICdmHooks.lua:2634-2638]` `confidence: low`
`@verify-ingame`

⚠ **TWO riders on one item frame is unbounded mutual recursion, and it is a CLIENT CRASH
rather than a flicker.** The seam above is not exclusive — more than one shipping addon
applies it to the same Essential item frames. Each one's `relativeTo` discriminator
recognises only its **own** container, so a foreign write is a move to answer: rider A
`SetPoint`s to A's container, which fires B's hook, which `SetPoint`s to B's container,
which fires A's hook, and the whole exchange happens inside one call stack with nothing
bounding it. A rider adopting this seam therefore owes a stand-down: detect another
manager and place nothing, rather than winning the argument.

This is not a prediction. One shipping rider carries a hardcoded early-bail for exactly
this class of addon, checked before any frame is touched, which no-ops its entire Cooldown
Manager module and raises a modal so the player can log in at all; its own comment says
that running both *"crashes the client on the loading screen"*.
`[T3 obs: EllesmereUICooldownManager 9.0.8 (live install) — EllesmereUICooldownManager.lua:34-40,
the guard and its comment; :41-42 sets a global so the generic conflict checker defers to it.
Read for API discovery only, no code copied]`

**Detecting the other manager takes two stages, because "installed" and "managing" are
different questions.** The loaded-addon list (`C_AddOns.IsAddOnLoaded` on the folder name)
says *who* to name, but a module can be present and switched off. The positional test says
whether it is actually holding the row: enumerate an Essential item frame's points and
resolve each `relativeTo` — a point naming neither the viewer's own subtree nor your frame
is somebody else's placement. A rider using the seam above is visible to it both ways, since
it anchors a claimed frame to its own bar container and parks an unclaimed one at
`UIParent` `TOPLEFT`, far off-screen.
`[T3 obs: EllesmereUICdmHooks.lua:2626-2657 — the claim branch and the park branch]`

**The published conflict surface is a table, and a boolean global is how another addon
opts out of it.** Entries carry the other addon's folder name, a display label, the list of
its own modules the conflict targets (or `"all"`), an optional `message`, and an optional
`moduleCheck` predicate. One entry's `moduleCheck` calls a **global function another addon
publishes** — `_G._ERF_IsHoverCastEnabled` — so the popup fires only while that addon's
conflicting feature is actually on. A rider that can stand itself down should publish the
same shape.
`[T3 obs: EllesmereUI 9.0.8 — EllesmereUI.lua:11395-11463, the conflict table;
:11405-11408, the predicate-gated entry; :11435-11440, five entries targeting the Cooldown
Manager module — BetterCooldownManager, CooldownManagerCentered, SkironCooldownManager,
ArcUI, Ayije_CDM]`

### 4.6.2 The deferred shape, for riders that only move whole viewers

Still correct, and cheaper, when the rider repositions a viewer as a unit rather than
re-ordering its children:

```lua
local function OnViewerRelaidOut(viewer)
    -- Cheap and idempotent: this runs a lot, including mid-combat via RefreshLayout.
    viewer:ClearAllPoints()
    viewer:SetPoint("TOPLEFT",     myContainer, "TOPLEFT",     0, 0)
    viewer:SetPoint("BOTTOMRIGHT", myContainer, "BOTTOMRIGHT", 0, 0)
end
```

⚠ **Do not reorder rows by rewriting `layoutIndex`.** On an item frame that field is both
the grid sort key and the index the viewer uses to look up the row's cooldownID, so
swapping two indices swaps the icons' identities along with their slots and nothing
appears to move; duplicates raise `GMError`. Reorder with `ClearAllPoints()` +
`SetPoint()`, and read drawn position from `GetLeft()`/`GetTop()` rather than from a
`GetItemFrames()` index, which is `layoutIndex` order and blind to your re-anchor
(`cooldown-manager.md` §4.1, §8 rules 18–19).

### 4.2 Knowing when an icon is (re)bound — the mixin hook

Each viewer's item frames come from the shared item mixins. Hooking `OnCooldownIDSet`
tells you the exact moment a frame is bound to a new cooldownID, which is where you reset
any per-frame cache:

```lua
hooksecurefunc(CooldownViewerEssentialItemMixin, "OnCooldownIDSet", ResetFrameCache)
hooksecurefunc(CooldownViewerUtilityItemMixin,   "OnCooldownIDSet", ResetFrameCache)
hooksecurefunc(CooldownViewerBuffIconItemMixin,  "OnCooldownIDSet", function(f) ResetFrameCache(f); QueueReanchor() end)
hooksecurefunc(CooldownViewerBuffBarItemMixin,   "OnCooldownIDSet", function(f) ResetFrameCache(f); QueueReanchor() end)
```

Mixin methods are copied per instance, so a mixin hook only affects frames created **after**
it is installed — install at load, and also walk the already-active pool once (below).

### 4.3 Enumerating icons

Two enumerators exist. Riders use one or the other:

```lua
-- The frame pool (catches every active item frame):
for frame in viewer.itemFramePool:EnumerateActive() do
    -- ...
end

-- Or Blizzard's own accessor:
local frames = viewer:GetItemFrames()

-- Catch newly-pooled frames as they are acquired:
hooksecurefunc(viewer.itemFramePool, "Acquire", OnFrameAcquired)
hooksecurefunc(viewer, "OnAcquireItemFrame", function(_, itemFrame)
    itemFrame:SetAlpha(0)   -- keep it blank until your own pass claims it
end)
```

### 4.4 Resolving an icon to its cooldown info

```lua
local cooldownID = frame.cooldownID or (frame.cooldownInfo and frame.cooldownInfo.cooldownID)
local info = C_CooldownViewer.GetCooldownViewerCooldownInfo(cooldownID)
-- info = {
--   spellID,          -- base/static id; CAN be unrelated to what is displayed
--   overrideSpellID,  -- live talent override
--   linkedSpellIDs,   -- array, iterated for identity matching
--   linkedSpellID,    -- singular, nil-compared for stale-link repair
--   cooldownID,
-- }
```

### 4.5 Per-icon skinning via post-hooks, once-guarded and coalesced

The rider re-applies its styling every time Blizzard repaints, by post-hooking the widget
methods on each icon's regions — never calling them itself. Two disciplines make this safe:
a **once-guard** so hooks do not stack across refreshes, and a **coalescing queue** so a
hook that re-triggers the same method does not recurse infinitely.

```lua
-- weak-keyed side table keeps our flags OFF the Blizzard frame (taint hygiene)
local affected = setmetatable({}, { __mode = "k" })

local function HookIconOnce(icon)
    if affected[icon] then return end
    affected[icon] = true

    hooksecurefunc(icon.Cooldown, "SetCooldown", function(self)
        QueueRestyle(self:GetParent())        -- do NOT restyle inline; queue it
    end)
    hooksecurefunc(icon.Cooldown, "Clear", function(self)
        QueueRestyle(self:GetParent())
    end)
    hooksecurefunc(icon.Icon, "SetDesaturated", function(self)
        -- the arg here is a secret; never branch on it, just re-run your pass
        QueueRestyle(self:GetParent())
    end)
    hooksecurefunc(icon.Icon, "SetSize", function(self)
        QueueRestyle(self:GetParent())
    end)
    if icon.RefreshData then
        hooksecurefunc(icon, "RefreshData", function(self) QueueRestyle(self) end)
    end
end

-- QueueRestyle just marks the frame and schedules one flush:
local pending = {}
local function QueueRestyle(f)
    pending[f] = true
    ScheduleFlush()        -- e.g. C_Timer.After(0, FlushRestyle) if not already pending
end
```

Defer your own work **past** Blizzard's layout pass with a zero-delay timer so you never
fight it mid-pass:

```lua
EventRegistry:RegisterCallback("CooldownViewerSettings.OnDataChanged", function()
    C_Timer.After(0, RefreshAll)
end)
```

---

## 5. Resolving an icon's spell ID — the clean-cache pattern

`frame:GetSpellID()` (and `GetAuraSpellID()` for buff frames) returns a **clean** number
while the frame is inactive, but goes **secret** once the frame is active (its aura is up /
it is mid-cooldown in instanced combat). The durable fix is to cache the clean read keyed
by the never-secret `cooldownID`, and reuse it when the getter later goes secret:

```lua
local cleanSidByCDID = {}   -- cooldownID -> clean spellID

local function ResolveSpellID(frame)
    local sid = frame:GetSpellID()
    if IsUsableSpellID(sid) then                 -- clean read (frame inactive)
        local cdid = frame.cooldownID
        if type(cdid) == "number" then cleanSidByCDID[cdid] = sid end
        return sid
    end

    -- frame active -> getter is secret; reuse the cached clean value
    local cdid = frame.cooldownID
    if type(cdid) == "number" and cleanSidByCDID[cdid] then
        return cleanSidByCDID[cdid]
    end

    -- last resorts, in order: info.overrideSpellID, info.spellID,
    -- info.linkedSpellIDs[*], then C_Spell.GetBaseSpell(raw)
end
```

`IsUsableSpellID` is the §1.1 guard (secret-first, then `> 0` and integral). Base/override
resolution wraps `C_Spell.GetBaseSpell` / `C_Spell.GetOverrideSpell`, each re-guarded and
required to differ from the input. The cache self-heals: any later clean read overwrites
its entry.

---

## 6. Proc glow without polling

Blizzard's overlay/proc state is delivered by **events**; the polling APIs
(`C_Spell.IsSpellOverlayed` / `C_SpellActivationOverlay.IsSpellOverlayed`) are
`AllowedWhenUntainted`, so calling them from addon code taints. Track state from events
into a plain set instead.

### 6.1 The event set (for your own tracking panels)

```lua
local procOverlaySpells = {}    -- spellID -> true

frame:RegisterEvent("SPELL_ACTIVATION_OVERLAY_GLOW_SHOW")
frame:RegisterEvent("SPELL_ACTIVATION_OVERLAY_GLOW_HIDE")

-- payload is the spellID:
function OnGlowShow(_, spellID) procOverlaySpells[spellID] = true;  QueueRefresh() end
function OnGlowHide(_, spellID) procOverlaySpells[spellID] = nil;   QueueRefresh() end
```

Consume it checking **both** the base entry ID and the currently-displayed override ID —
the glow can fire for either form:

```lua
local active = procOverlaySpells[baseID] ~= nil
if not active and displayID and displayID ~= baseID then
    active = procOverlaySpells[displayID] ~= nil
end
```

### 6.2 Riding Blizzard's own CDM alert (when you skin the CDM icons directly)

If you are decorating the real CDM icons, hook Blizzard's alert manager instead of
registering the events, so you fire on exactly the frames Blizzard is already glowing —
then hide Blizzard's own overlay and draw your own:

```lua
if ActionButtonSpellAlertManager then
    hooksecurefunc(ActionButtonSpellAlertManager, "ShowAlert", function(_, frame)
        local child = MapAlertFrameToCDMChild(frame)     -- walk parents to a known viewer
        if not child then return end
        if child.SpellActivationAlert then               -- hide Blizzard's overlay
            child.SpellActivationAlert:SetAlpha(0)
            child.SpellActivationAlert:Hide()
        end
        StartMyGlow(child)
    end)
    hooksecurefunc(ActionButtonSpellAlertManager, "HideAlert", function(_, frame)
        local child = MapAlertFrameToCDMChild(frame)
        if child then StopMyGlow(child) end
    end)
end
```

Install these at **file load**, not on a later event: Blizzard re-fires `ShowAlert` during
`PLAYER_LOGIN` for procs that are already up, and a late hook misses them. Map the alerted
frame back to a spell via a `cooldownID -> spellID` memo over
`GetCooldownViewerCooldownInfo`, comparing `info.spellID`/`overrideSpellID` (resolve
overrides with `C_SpellBook.FindSpellOverrideByID`).

---

## 7. Sealed player-aura display via the managed aura container

On 12.1 aura data is wholesale secret, and `GetPlayerAuraBySpellID(...).expirationTime`
never opens its numeric window for a secret-flagged aura mid-combat. The sanctioned way to
still show "this buff is up, with its stacks and its real duration swipe" is to let the
**engine** own the whole display: create a managed aura container filtered to the one aura
you care about, style it inside its creation callback, and never read it back.

The load-bearing parts are the **filter table** and the **creation-window discipline** —
the container factory below is an addon-level helper over Blizzard's managed-aura-container
system; the shape is illustrative but the two disciplines are the real content.

```lua
-- A proxy frame is the anchor target. It is a plain UIParent child, NEVER the aura button.
local proxy = CreateFrame("Frame", nil, UIParent); proxy:Hide()

local container = CreateManagedAuraContainer(proxy, { point = { "CENTER" } })
AddSlotToContainer(container, {
    key    = "fa",
    filter = { "HELPFUL" },                                     -- HELPFUL vs HARMFUL
    -- The identity gate: a helpful include-by-spellID on the player passes REGARDLESS of
    -- the aura's secrecy flag. This is the one readable signal about the aura in combat.
    candidateFilters = { includeSpellIDs = { [auraSpellID] = true } },

    -- extraInit runs in the ONLY window where this subtree may be touched. After it
    -- returns, the button and every child are forbidden to addon code -- reads AND
    -- writes, in and out of combat. So do ALL styling here.
    extraInit = function(button)
        button:SetAllPoints(proxy)                 -- two-point sizing, set once, forever
        button:SetMouseMotionEnabled(false)

        local tex = button:CreateTexture(nil, "ARTWORK")
        tex:SetAllPoints(button)
        tex:SetTexCoord(0.08, 0.92, 0.08, 0.92)

        local cd = CreateFrame("Cooldown", nil, button, "CooldownFrameTemplate")
        cd:SetAllPoints(button)
        cd:SetDrawEdge(false); cd:SetDrawBling(false)
        cd:SetFrameLevel(button:GetFrameLevel() + 1)

        -- Duration TEXT needs a Frame ABOVE the cooldown: regions parented to a
        -- Cooldown render UNDER its swipe. Font it BEFORE registering or the engine errors.
        local tc = CreateFrame("Frame", nil, button); tc:SetAllPoints(button)
        tc:SetFrameLevel(cd:GetFrameLevel() + 5)
        local fs = tc:CreateFontString(nil, "OVERLAY"); fs:SetFont(fontPath, 14, "OUTLINE")
        button:SetDurationText(fs, { textFormatter = fmt })

        -- Bind LAST. The engine now drives icon + real (extension-aware) duration swipe.
        -- SetDurationCooldown TAKES OWNERSHIP of cd; touching it afterwards is illegal.
        button:SetIcon(tex)
        button:SetDurationCooldown(cd)
    end,
})
FinishContainer(container, "player")   -- unit is bound here
```

Two rules this encodes, both of which bite hard if ignored:

- **Anchor a proxy, never the button.** Engine aura buttons are *forbidden objects*: any
  anchor path from your bar to one restriction-locks your bar's own geometry. Reposition by
  moving the proxy (`proxy:SetParent(iconFrame); proxy:SetAllPoints(iconFrame)`); the button
  only ever does `SetAllPoints(proxy)` once, inside `extraInit`.
- **There is no Lua presence signal.** Because you cannot read the aura back, the display
  can only *be shown by the engine while the aura is up*. Do not build logic that asks "is it
  up?" — the container answering that question visually is the whole mechanism.

Wrap the optional parts of `extraInit` in `pcall`: an uncaught error there aborts the
engine's whole create-batch and kills every later slot declaration.

---

## 8. Assisted Combat — Blizzard's own next-cast API

Blizzard ships a one-button rotation engine, and its result is readable. This is how a
rider surfaces a "press this next" glow **legally**: the decision is Blizzard's, made in
the protected client; the addon only animates a texture on the suggested icon. (Whether a
product *wants* to surface a single suggestion is a design question, not an API one — but
the API is here and worth knowing.)

```lua
-- The pure next-cast suggestion. false = do NOT factor in visible action buttons or the
-- assistedCombatHighlight CVar; gives the raw rotation answer decoupled from the bars.
local spellID = C_AssistedCombat.GetNextCastSpell(false)

-- The whole in-rotation set (one array call -> membership table):
local rotation = {}
for _, id in ipairs(C_AssistedCombat.GetRotationSpells() or {}) do rotation[id] = true end

-- Stay in sync with Blizzard's own highlight repaints:
hooksecurefunc(AssistedCombatManager, "UpdateAllAssistedHighlightFramesForSpell", function(_, spellID)
    RepaintMyHighlights()
end)

-- Poll at Blizzard's own configured rate, and only act on a change:
local rate, acc, last = 0.1, 0, nil
pollFrame:SetScript("OnUpdate", function(_, elapsed)
    acc = acc + elapsed
    if acc < rate then return end
    acc = 0
    rate = math.max(0.05, math.min(tonumber(C_CVar.GetCVar("assistedCombatIconUpdateRate")) or 0.1, 1))
    local next = C_AssistedCombat.GetNextCastSpell(false)
    if next ~= last then last = next; RepaintMyHighlights() end
end)
```

Match the suggestion to an icon tolerant of base/override forms:

```lua
local a = C_Spell.GetBaseSpell(iconSpellID) or iconSpellID
local b = C_Spell.GetBaseSpell(suggestedID) or suggestedID
local isSuggested = (a == b)
```

Rebuild the rotation set on: `PLAYER_ENTERING_WORLD`, `PLAYER_TALENT_UPDATE`,
`SPELLS_CHANGED`, `PLAYER_SPECIALIZATION_CHANGED`, `TRAIT_CONFIG_UPDATED`,
`UPDATE_SHAPESHIFT_FORM`.

---

## 9. Press / cast detection

Two different questions with two different answers.

### 9.1 "The player just pressed the button" (predictive, pre-cast)

Hook the global action-button input functions and the per-button `PreClick`. This fires the
instant the key/click goes down, before any server round-trip:

```lua
hooksecurefunc("ActionButtonDown", function(id)
    local btn = _G["ActionButton" .. id]
    OnPressed(btn)
end)
hooksecurefunc("ActionButtonUp",   function(id) OnReleased(_G["ActionButton" .. id]) end)
hooksecurefunc("MultiActionButtonDown", function(bar, id) OnPressed(_G[bar .. "Button" .. id]) end)
hooksecurefunc("MultiActionButtonUp",   function(bar, id) OnReleased(_G[bar .. "Button" .. id]) end)

button:HookScript("PreClick", function(self, mouseButton, down)
    if self.myReentryGuard then return end     -- re-entrancy guard
    self.myReentryGuard = true
    if down then OnPressed(self) end
    self.myReentryGuard = nil
end)
```

Resolve the pressed slot to a spell, tolerant of spell/item/macro actions:

```lua
local function SpellIDFromButton(btn)
    local actionType, id, subType = GetActionInfo(btn.action)
    if actionType == "macro" and subType == "spell" then
        return id
    elseif actionType == "spell" then
        return id
    elseif actionType == "item" then
        return select(2, C_Item.GetItemSpell(id))          -- the item's on-use spell
    elseif actionType == "macro" then
        local name = GetActionText(btn.action)
        local sid = GetMacroSpell(name)
        if not sid then
            local item = GetMacroItem(name)
            sid = item and select(2, C_Item.GetItemSpell(item))
        end
        return sid
    end
end
```

Index and match every icon under its whole `{self, override, base}` spell-ID set so a press
lights the right icon regardless of which form is current:

```lua
AddToMap(cdSpellID, icon)
AddToMap(C_Spell.GetOverrideSpell(cdSpellID), icon)
AddToMap(C_Spell.GetBaseSpell(cdSpellID), icon)
-- lookup mirrors the same three forms of the pressed spell.
```

### 9.2 "The player actually cast this spell" — authoritative, and SEALED on identity

The obvious answer to "did that cast land" is the confirmed-cast event, filtered to the player:

```lua
frame:RegisterUnitEvent("UNIT_SPELLCAST_SUCCEEDED", "player")
frame:SetScript("OnEvent", function(_, _, unit, castGUID, spellID)
    if unit == "player" then RecordCast(spellID) end   -- ⚠ spellID may be SECRET here
end)
```

⚠⚠ **`spellID` on this event is not readable in restricted combat, so it cannot key a ledger.**
`UNIT_SPELLCAST_SUCCEEDED` carries `SecretWhenUnitSpellCastRestricted = true`, and of its four
payload fields only `castBarID` is marked `NeverSecret` — `unitTarget`, `castGUID` and **`spellID`
are not**
`[T1 docs @12.1.0: UnitDocumentation.lua — Event UnitSpellcastSucceeded, LiteralName
UNIT_SPELLCAST_SUCCEEDED]`. The same annotation sits on every sibling `UNIT_SPELLCAST_*` event and
on `UnitCastingInfo` / `UnitChannelInfo`, whose result structures mark only `castBarID`,
`delayTimeMs` and `isTradeskill` `NeverSecret`
`[T1 docs @12.1.0: UnitDocumentation.lua — UnitCastingInfo, UnitCastingInfoResult,
UnitChannelInfoResult]`. So *which* spell is being cast is a **sealed-display** fact under
restriction: forward it to a client-owned sink, never compare, index or truth-test it.

The one thing this channel still gives you is the **fact and timing** of a cast, which is plain:
the event fired, and `castBarID` is readable. Anything more specific than "a cast completed" has
to come from somewhere else.

⚠ **The restricted case is Tier-1 annotation, not measurement.** The one in-client reading on
record was taken **unrestricted** and found a plain `spellID` (`cooldown-manager.md` Tier 3), which
does not bear on the sealed-in-instance case either way. `@verify-ingame` — read
`issecretvalue` on `UNIT_SPELLCAST_SUCCEEDED`'s `spellID` inside an instance, in combat.

**So the readable route is the press, and the two are NOT interchangeable.**

| | §9.1 press hook | `UNIT_SPELLCAST_SUCCEEDED` |
|---|---|---|
| when | key-down, before any server round-trip | after the server confirms |
| what it means | *what I tried* — a press can be cancelled, out of range, or fail | *what landed* |
| the spell id | **readable** — it comes off the action bar (`GetActionInfo`), not from combat state | **sealed under restriction** |
| may key a ledger | yes | no |

**A rolling history of recent casts follows the same split, and the lane follows the source.** A
ring buffer fed from the **press** route is the addon's own plain data and is fully branchable —
it is a history of intents. A ring fed from `UNIT_SPELLCAST_SUCCEEDED` is a history of confirmed
casts whose entries are sealed, so it is forward-to-display only; it can be *shown*, and it can be
*counted* (the count is yours), but no entry in it may be compared to a spell id.

**The consequence for §3's charge estimator:** the readable trigger for "the tracked spell was
just cast" is the **press**, or a CDM charge-alert edge — not the confirmed-cast event, because
its id cannot be matched against the tracked spell under restriction. Debit on the readable
trigger and treat `UNIT_SPELLCAST_SUCCEEDED` as timing only. Match the pressed id under the whole
`{self, override, base}` set (§9.1) so a transform does not silently stop debiting.

---

## 10. Range — event-driven, and suppressing Blizzard's dimming

### 10.1 Push-based range instead of polling

`C_Spell.EnableSpellRangeCheck` registers a spell for `SPELL_RANGE_CHECK_UPDATE` events —
the modern replacement for polling `IsSpellInRange` in an `OnUpdate`:

```lua
C_Spell.EnableSpellRangeCheck(spellID, true)    -- start receiving updates
C_Spell.EnableSpellRangeCheck(spellID, false)   -- stop

frame:RegisterEvent("SPELL_RANGE_CHECK_UPDATE")
frame:SetScript("OnEvent", function(_, _, spellID, inRange, checksRange)
    -- checksRange distinguishes "spell has no range" from "in range".
    local outOfRange = (checksRange and inRange == false) or false
    SetIconRangeState(spellID, outOfRange)
end)
```

Diff the enable/disable calls against your last-registered set so you only flip the spells
that actually changed.

### 10.2 Overriding Blizzard's out-of-range tint on CDM icons

To recolor an icon yourself (e.g. by usability rather than range), post-hook the icon's
`RefreshIconColor` and force-hide its out-of-range texture, using the shared color
constants so you match Blizzard's own palette:

```lua
local function RecolorIcon(child)
    local spellID = child:GetSpellID()
    if not spellID or (issecretvalue and issecretvalue(spellID)) then return end
    local icon = child:GetIconTexture()
    local usable, noPower = C_Spell.IsSpellUsable(spellID)
    if usable then
        icon:SetVertexColor(CooldownViewerConstants.ITEM_USABLE_COLOR:GetRGBA())
    elseif noPower then
        icon:SetVertexColor(CooldownViewerConstants.ITEM_NOT_ENOUGH_MANA_COLOR:GetRGBA())
    else
        icon:SetVertexColor(CooldownViewerConstants.ITEM_NOT_USABLE_COLOR:GetRGBA())
    end
    child:GetOutOfRangeTexture():SetShown(false)   -- kill the red range dim
end

hooksecurefunc(child, "RefreshIconColor", function() RecolorIcon(child) end)
RecolorIcon(child)   -- and once now
```

The `ITEM_*_COLOR` fields on `CooldownViewerConstants` are `ColorMixin`s — call `:GetRGBA()`.

---

## 11. Keybind resolution — spell to on-screen key

A two-stage lookup: spell to action slot, then slot to binding key.

**Stage 1 takes a BASE spell, and that is the API's stated contract, not a fallback.**
`C_ActionBar.FindSpellActionButtons(spellID)` is documented *"Expects a base spell, so if a
spell is overridden the base ID should be provided"*
`[T1 docs: ActionBarFrameDocumentation.lua:66]`. This matters more on the CDM than on a
plain bar: a row's resolved identity is routinely an override while the player's bar holds
the base, so `C_Spell.GetBaseSpell` is the lookup that hits, not the one that rescues.
It returns a **list of absolute slots**, and `MayReturnNothing` — so an unslotted spell
yields **nil, not an empty table** `[T1 docs: ActionBarFrameDocumentation.lua:66]`.
`HasSpellActionButtons(spellID)` is the cheap existence test
`[T1 docs: ActionBarFrameDocumentation.lua:566]`.

**It does not see macros, the stance bar, the pet bar or the possess bar.** Blizzard says so
in its own comment — *"FindSpellActionButtons does not cover special bars like Stance and Pet
bars, so now check those"* `[T1 src: ActionButtonUtil.lua:112]` — and supplements it via
`GetShapeshiftFormInfo` / `GetPetActionInfo` / `GetPossessInfo` inside
`ActionButtonUtil.GetActionBarsForSpell(spellID, …)` `[T1 src: ActionButtonUtil.lua:104]`,
which is the higher-level wrapper to reach for when those bars matter. **Macros are the gap
that shows up first in practice:** the lookup is spell-keyed, so a slot holding a macro that
casts the ability has `actionType == "macro"` and is invisible to it. A player who macros
their cooldowns gets no key on exactly those buttons — which is a product decision (blank, or
fall back to a slot scan), not a bug to fix in this recipe.

```lua
-- Stage 1: spell -> action slots. The BASE form is the documented input; probe both because
-- the CDM hands you the override.
local function SpellActionSlots(spellID)
    local slots = {}
    for _, s in ipairs(C_ActionBar.FindSpellActionButtons(spellID) or {}) do slots[#slots+1] = s end
    local base = C_Spell.GetBaseSpell(spellID)
    if base and base ~= spellID then
        for _, s in ipairs(C_ActionBar.FindSpellActionButtons(base) or {}) do slots[#slots+1] = s end
    end
    return slots
end

-- Stage 2: build a slot -> binding-action reverse map by scanning the real button frames.
-- Reading frame.action off each button handles paged slot numbering with no hardcoded ranges.
local ACTION_BARS = {
    { "ActionButton",              "ACTIONBUTTON",          12 },
    { "MultiBarBottomLeftButton",  "MULTIACTIONBAR1BUTTON", 12 },
    { "MultiBarBottomRightButton", "MULTIACTIONBAR2BUTTON", 12 },
    { "MultiBarRightButton",       "MULTIACTIONBAR3BUTTON", 12 },
    { "MultiBarLeftButton",        "MULTIACTIONBAR4BUTTON", 12 },
    -- MultiBar5Button / 6 / 7 likewise
}
local slotToBinding = {}
local function RebuildSlotMap()
    wipe(slotToBinding)
    for _, bar in ipairs(ACTION_BARS) do
        local framePrefix, bindPrefix, n = bar[1], bar[2], bar[3]
        for i = 1, n do
            local f = _G[framePrefix .. i]
            if f and f.action then
                slotToBinding[f.action] = { bindingAction = bindPrefix .. i, frameName = framePrefix .. i }
            end
        end
    end
end

-- Key lookup, with the click-cast fallback that addon/click bars use.
local function KeyText(bindingAction, frameName)
    local key = GetBindingKey(bindingAction)
             or GetBindingKey("CLICK " .. frameName .. ":LeftButton")
    if key then return AbbreviateKeybind(GetBindingText(key, 1)) end
end
```

Bonus/stance bars need the active-page resolution — a slot on a bonus bar maps to the
current `ActionButton{i}` only while that bonus bar is active:

```lua
local idx = C_ActionBar.GetBonusBarIndexForSlot(slot)
if idx and C_ActionBar.HasBonusActionBar() and idx == C_ActionBar.GetBonusBarIndex() then
    local i = ((slot - 1) % 12) + 1
    -- use binding "ACTIONBUTTON" .. i / frame "ActionButton" .. i
end
```

Rebuild the whole map on: `UPDATE_BINDINGS`, `ACTIONBAR_SLOT_CHANGED`,
`ACTIONBAR_PAGE_CHANGED`, `UPDATE_BONUS_ACTIONBAR`, `UPDATE_OVERRIDE_ACTIONBAR`,
`UPDATE_VEHICLE_ACTIONBAR`, `UPDATE_SHAPESHIFT_FORM`, `PET_BAR_UPDATE`. Blizzard registers
the first two on `ActionBarButtonEventsFrameMixin:OnLoad`
`[T1 src: ActionButton.lua:206-207]` and the bar-level ones on the controller
`[T1 src: ActionBarController.lua:12-24]`. A spec swap surfaces to the bars as a burst of
`ACTIONBAR_SLOT_CHANGED` rather than as its own bar event — no action-bar file registers
`PLAYER_SPECIALIZATION_CHANGED` `[searched 2026-08-19: Blizzard_ActionBar/**,
Blizzard_ActionBarController/**]` — but a cache keyed by spell still wants it, because
talent overrides change which base ID is slotted.

**The whole read chain is callable in combat, and writing your own FontString from it is
safe.** Blizzard handles `UPDATE_BINDINGS` mid-combat and runs
`GetBindingKey` → `GetBindingText` → `HotKey:SetText` with no lockdown check
`[T1 src: ActionButton.lua:950-951, :470-505]`; no file under `Blizzard_ActionBar` guards
this path at all `[searched 2026-08-19: Blizzard_ActionBar/** for InCombatLockdown]`. A
FontString region is not protected even when its parent button is — Blizzard re-`SetPoint`s
`HotKey` inside a protected action button `[T1 src: ActionButton.lua:496-503]`. So any
"rescan only out of combat" fence in a rider is a **cost** rule about scan churn, never a
safety rule, and a fence that defers a dirtied cache to `PLAYER_REGEN_ENABLED` will blank or
stale the hint for the rest of a pull. Debounce instead of deferring.

⚠ **The write side is the opposite.** `SetBinding`, `SaveBindings`, `PlaceAction`,
`PickupAction` and the macro editors are lockdown-gated; reading a binding and displaying it
shares none of that. Blizzard's own guard idiom where it does matter is
`if issecure() or not InCombatLockdown() then` `[T1 src: EditModeManager.lua:712]`.

⚠ **Inside the restricted addon environment `GetActionInfo` is scrubbed** — `scrubActionInfo`
whitelists `spell/companion/item/macro/flyout/outfit` and returns **only** `actionType` for
anything else, dropping `id` and `subType`
`[T1 src: RestrictedEnvironment.lua:162-174]`. Ordinary addon code sees the full return; a
secure snippet does not.

**Formatting the key for display.** `GetBindingText(key, 1)` — the abbreviate flag is a
positional truthy argument (`1`, `true` and `0` all appear in shipped calls), **not** the
string `"KEY_ABBR"` `[T1 src: ActionButton.lua:491]`.

⚠ **The flag abbreviates the MODIFIERS and nothing else, so its output does not fit an icon
corner.** The abbreviations are single lowercase letters — `SHIFT_KEY_TEXT_ABBR = "s"`,
`CTRL_KEY_TEXT_ABBR = "c"`, `ALT_KEY_TEXT_ABBR = "a"`, `META_KEY_TEXT_ABBR` / `CMD_KEY_TEXT_ABBR
= "m"` `[T1 src: GlobalStrings enUS :17900, :5336, :832, :13434, :4186]`. **There is no
abbreviated form of any key NAME.** The `KEY_ABBR_*` family is **gamepad-only** and expands to a
texture escape (`|A:Gamepad_%s_32:14:14|a`) rather than to text `[T1 src:
SharedConstants.lua:56-58, :61-143]`, so a mouse or numpad binding comes back at full length
however the flag is set: `KEY_BUTTON4 = "Mouse Button 4"`, `KEY_BUTTON3 = "Middle Mouse"`,
`KEY_MOUSEWHEELUP = "Mouse Wheel Up"`, `KEY_NUMPAD5 = "Num Pad 5"` `[T1 src: GlobalStrings enUS
:12460, :12457, :12480, :12488]`. Function keys, letters and digits have no `KEY_*` entry at all
and pass through as the raw token. **A rider that wants a short label has to shorten it itself.**

⚠ `[gap]` **The JOINER between an abbreviated modifier and the key is unmeasured.**
`GetBindingText` is implemented C-side and is only ever *called* from Lua — `s-F`, `sF` and `s F`
are all consistent with the string table `[searched 2026-08-19: wow-ui-source 12.0.7 (68453) and
BlizzardInterfaceResources enUS GlobalStrings, for any Lua definition of GetBindingText]`. Write
a shortener that tolerates all three rather than matching one.

**Blizzard does not truncate a long key either — it clips.** `ActionButton.lua:487-508`
(`UpdateHotkeys`) reads `GetBindingText(key, 1)`, treats **`""`** (not nil) as "nothing bound" and
hides the FontString `[:492-494]`, and otherwise fixes the region's size — `SetSize(frameWidth-8,
10)` for keyboard, `SetSize(frameWidth, 16)` for gamepad — and calls `SetText` `[:497-506]`. No
`strsub`, no max length, anywhere in the tree `[searched 2026-08-19: Blizzard_ActionBar/** for
hotkey truncation]`.

**The font Blizzard puts on a hotkey is `Fonts\ARIALN.TTF`, height 12, `outline="NORMAL"`,**
tinted 0.6 grey. Chain: the FontString inherits `NumberFontNormalSmallGray` `[T1 src:
ActionButtonTemplate.xml:85]` → `NumberFontNormalSmall` + a grey colour `[T1 src:
GameFontStyles.xml:21-23]` → `NumberFont_OutlineThick_Mono_Small` `[:18-20]` → the roman member,
ARIALN at 12 `[T1 src: GameFonts.xml:59-61]`. ⚠ The family is named *OutlineThick* and resolves
to a **NORMAL** outline; the THICK variant with that name is the **glue/login** one `[T1 src:
GlueFontStyles.xml:80-85]` and is not the in-game action bar's. Arial Narrow is a deliberate
choice for this problem: narrow buys characters in a fixed-width corner.
`GetBindingKeyForAction(action, useNotBound, useParentheses)` is Blizzard's own wrapper over
the pair, with a `NOT_BOUND` fallback `[T1 src: BindingUtil.lua:151]`. Note that none of
`GetBindingKey` / `GetBindingText` / `SetBinding` appear in the generated API docs — they are
legacy globals, and only `C_KeyBindings.*` is documented
`[searched 2026-08-19: Blizzard_APIDocumentationGenerated/**]`.

---

## 12. Glow library API shape (LibCustomGlow family)

The community glow library (and its forks) exposes four styles behind start/stop pairs.
`color` accepts either `{r,g,b,a}` or a `ColorMixin`; `key` (default `""`) namespaces
multiple glows on one frame so they can coexist and be stopped independently.

```lua
-- Marching-pixels perimeter (optional polygon path via `vertices`):
Lib.PixelGlow_Start(frame, color, numLines, frequency, length, thickness,
                    xOffset, yOffset, border, key, frameLevel, vertices)
Lib.PixelGlow_Stop(frame, key)

-- Rotating shine sparks:
Lib.AutoCastGlow_Start(frame, color, numSparks, frequency, scale,
                       xOffset, yOffset, key, frameLevel, vertices)
Lib.AutoCastGlow_Stop(frame, key)

-- Blizzard action-bar proc flipbook (Start + looping Loop atlases, 6x5 / 30 frames):
Lib.ProcGlow_Start(frame, { frameLevel = 8, color = nil, startAnim = true,
                            xOffset = 0, yOffset = 0, duration = 1, key = "" })
Lib.ProcGlow_Stop(frame, key)

-- "Ants" flipbook (custom sheet via texture/texCoords/frameWidth/frameHeight):
Lib.AntsGlow_Start(frame, { atlas = "RotationHelper_Ants_Flipbook_2x",
                            rows = 6, columns = 5, frames = 30,
                            duration = 1, scale = 1.4, count = 1, key = "" })
Lib.AntsGlow_Stop(frame, key)
```

If you build a flipbook glow by hand rather than via the library, the shape is: an
`AnimationGroup` on an `ADD`-blend texture with a zero-duration `Alpha` animation pinning
it visible plus a `FlipBook` animation walking the sheet:

```lua
local flip = animGroup:CreateAnimation("FlipBook")
flip:SetChildKey("Texture")
flip:SetDuration(1.0)
flip:SetFlipBookRows(6)
flip:SetFlipBookColumns(5)
flip:SetFlipBookFrames(30)
-- FrameWidth/Height = 0 -> derive cell size from rows/cols; nonzero forces exact cells
flip:SetFlipBookFrameWidth(0)
flip:SetFlipBookFrameHeight(0)
```

Guard the host size you read for glow geometry (see §13) — a reparented frame can hand back
a secret size, and the library returns `0, 0` rather than doing arithmetic on it.

---

## 13. Restriction and safe-size guards

### 13.1 Safe size — nil on secret or not-yet-laid-out

```lua
local function GetSafeSize(frame)
    if not frame then return nil end
    local w, h = frame:GetSize()
    if issecretvalue and (issecretvalue(w) or issecretvalue(h)) then return nil end
    if not w or not h or w <= 0 or h <= 0 then return nil end   -- not laid out yet
    return w, h
end
```

Reparented frames in 12.x can return secret sizes; arithmetic on one errors, so callers
keep their last good size when this returns nil.

### 13.2 The addon-restriction (lockdown) probe

`C_RestrictedActions.IsAddOnRestrictionActive` reports whether an addon-restriction
category is active — a superset of the classic combat-lockdown question. There are five
categories; any active one means protected work must be skipped:

```lua
local function IsSomeRestrictionActive()
    if C_RestrictedActions and C_RestrictedActions.IsAddOnRestrictionActive then
        for i = 0, 4 do
            if C_RestrictedActions.IsAddOnRestrictionActive(i) then return true end
        end
    end
    return false
end
```

---

## 14. Refresh wiring — one ticker, dirty flags, deferred flushes

The recurring shape for keeping a rider cheap and taint-safe:

- **One `C_Timer.NewTicker(0.1, ...)`** drives a single refresh pass; nothing polls per
  frame.
- Cooldown/charge **events mark dirty** rather than doing work inline:
  `SPELL_UPDATE_COOLDOWN`, `BAG_UPDATE_COOLDOWN`, `ACTIONBAR_UPDATE_COOLDOWN`,
  `SPELL_UPDATE_CHARGES`, `SPELL_UPDATE_USES`.
- **Coalesce** hook-triggered work into a pending set flushed once (see §4.5).
- **Defer past Blizzard's layout** with `C_Timer.After(0, ...)` so your pass runs after the
  frame Blizzard is currently laying out, never during it.
- Keep your own per-frame state in a **weak-keyed side table**
  (`setmetatable({}, { __mode = "k" })`) so it never lands on a Blizzard frame (taint
  hygiene) and pooled frames garbage-collect cleanly.

---

## 15. The one-paragraph summary

A CDM rider on 12.1 lives inside three constraints and a matching set of moves. Secret
values seal live magnitudes: read them **secret-first**, and when you need a decision from
one, push it **engine-side** through a `C_CurveUtil` step curve and
`DurationObject:EvaluateRemainingDuration`, or through a hidden scratch Cooldown's
`IsShown()`. Taint seals protected frames in combat: hook `Layout` **and** `RefreshLayout` on
all four viewers and the item mixins with `hooksecurefunc`, keep your state in weak-keyed
side tables, do your positioning on a setup path with idempotent re-application (§4.1 — the
CDM item templates declare no protection, so `InCombatLockdown` is a work-shedding gate here
rather than a legality one), and coalesce your work off Blizzard's own repaint edges.
Forbidden objects (engine aura buttons) seal themselves entirely: style them inside their
creation window and anchor a proxy to follow them, never the reverse. Everything readable —
identities, booleans, `isOnGCD`, Assisted-Combat suggestions, overlay-glow events, range
events, keybinds — is fair game, and using it well is the whole craft.

## 6. Auras at 12.1 — the route map

Everything in §1–§5 is cooldowns and charges. Auras are a **separate system** with its own
seal, and the three pieces that make them workable were established on different days, in
different files, filed by how they were found rather than by what they are for. This section
is the entry point; each claim lives in exactly one place and is cited, not restated.

**The starting fact: `C_UnitAuras` is closed to a tainted caller while auras are secret.** The
spell-keyed getters return a silent `nil` — indistinguishable from "no such aura" — and the
enumerators raise. Measured both ways, on the player's own auras as well as the target's:
[`security-taint-and-restricted-data.md`](./security-taint-and-restricted-data.md) §4.7.1.
**Reaching this and stopping is the mistake to avoid**; the capability moved, it did not go
away. Three routes replace it, and they answer *different questions*.

| You want to… | Route | Gives you |
|---|---|---|
| **show** an aura — icon, stacks, a draining timer | `AuraContainer` / `AuraButton` (`security-taint-and-restricted-data.md` §3.5, §3.5.1) | pixels only |
| **know** whether one is up, and branch on it | CDM alert edges (`cooldown-manager.md` §5.1) | a readable boolean |
| **identify** which spell id an aura actually carries | a container narrowed to a candidate set (`security-taint-and-restricted-data.md` §3.5.1) | the id, by eye |

### 6.1 To DISPLAY — the container

Declare intent (which auras, sorted how, at most how many), register output sinks, and the
engine fills them; your code never sees an `AuraData`. Flown from tainted addon code, in
combat, with `includeSpellIDs` honoured on a **hostile** target — so a display scoped to one
spec's own DoTs is buildable
([`security-taint-and-restricted-data.md`](./security-taint-and-restricted-data.md) §3.5.1).

⚠ **It ends at the pixel.** The buttons answer `IsShown` with a secret, so nothing downstream
may branch on whether one appeared. If you need a *decision*, you are in §6.2, not here.

⚠ **Size the button in `initializeFrame` or you will see nothing**, while every call returns
`ok` — the template carries no `<Size>` and the layout never sets one (`security-taint-and-restricted-data.md` §3.5).

### 6.2 To KNOW — the alert edges

A CDM row bound to an aura calls `TriggerAlertEvent` with `OnAuraApplied` / `OnAuraRemoved`,
and **observing a call is not reading a value**, so a latch built on these edges is readable
and branchable. Works for a debuff on an **enemy**, which is what makes it the only surviving
target-aura *predicate*. Hook per item **instance**; the recipe, the enum values and the
measurement are in [`cooldown-manager.md`](./cooldown-manager.md) §5.1.

⚠ **A refresh of a live aura raises nothing** (`cooldown-manager.md` §5.4) — harmless for an up/down latch, since a
refresh does not change up/down, and fatal for anything wanting duration.

⚠ **`Available` is asymmetric and gated on the player's alert config; the aura edges are not**
— they run from the `UNIT_AURA` path rather than `OnUpdate` registration (`cooldown-manager.md` §5.1).

### 6.3 The gate on both — is the row even bound?

Both routes above assume the row you care about reached an item frame. Many aura rows carry
`HideByDefault` and only bind once the player adds them to Tracked Buffs, and a consumer that
cannot tell gets **no error and no absent value** — it simply never hears about that ability
(`cooldown-manager.md` §1.2). A hint resting on an unheard row sits dark forever and reads as *"the condition is
false"*, which is the one thing an unknown must never become.

**Ask the question the hook cares about: did it get a frame?** Enumerate the four viewer
globals' active item frames and read `GetCooldownID()` on each; a frame carrying the id is
what an alert hook attaches to, and a cleared frame answers `nil`. Reconciling against the
settings provider's `GetOrderedCooldownIDsForCategory` instead returns the row **whether or
not the player enabled it** `[client 2026-08-19]`, so it answers a different question than the
one being asked. The frame-enumeration form is in use in cap and was retired as validated-in-cap
`[client 2026-08-21]` — ⚠ **confirmed-by-use, not a controlled enable/disable measurement**; if
you need proof it flips across an enable/disable pair, re-fly it (recover the test from git).

⚠ **Whatever you build, it has to be able to say "I cannot hear this one."** The remedy is one
tracked-buff toggle, and the player has no way to know it is needed unless something tells them.
