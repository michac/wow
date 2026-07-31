# Cooldown HUD — technical notes (what the game allows)

> The **Secret-Values reality and the CDM capability map**: what an addon can read,
> branch on, and display under Midnight 12.0, plus the positioning/anchoring
> architecture. Spec-agnostic and engine-independent — this is the ground the pipeline
> (`architecture.md`) is shaped around. Demonology-specific data (tracked set, override
> pairs, blind spots) lives in `specs/demonology/notes.md`; vision/design language in
> `design.md`.
>
> ⚠ Some **build findings reference the retired old engine** (`HudCore`/`HudState` and
> the old `/cdmp hud status` output) — those are **provenance** (how the finding was
> measured), not a description of today's code. The HUD is now the W4 pipeline.

## 1. The hard constraint — Midnight "Secret Values"

12.0 introduced **Secret Values**: in restricted content (combat / instanced
maps / PvP), tainted addon code may **display** personal combat state through
Blizzard-sanctioned pipes but may **not read it back to branch** (no arithmetic,
comparison, boolean test, or conditional visibility on a secret). This is why
Team WeakAuras will not ship a Midnight version, and a standalone addon inherits
the exact same wall.

**We confirmed the precise line empirically** (CDMProbe `dump` + `secret`, in a
delve, in combat — SavedVariables captured to disk):

| Data | Read in Lua (can branch) | Display |
| --- | --- | --- |
| **Soul Shards** (`UnitPower(SoulShards)`) | ✅ **yes** — read `2`, `20` frags; the shard bar's color-flip-at-max is a live `if n >= MAX` that worked without tainting | ✅ |
| **GCD** (spell 61304) | ✅ yes (whitelisted) | ✅ |
| **Tracked spell IDs** — **ICON** viewers (`item:GetSpellID()`) | ✅ yes, in combat too (v0.12.0 probe: `Devour Magic id=388215` read fine mid-fight) | ✅ |
| **Tracked spell IDs** — **BUFF** viewers, aura ACTIVE | ❌ **`<secret>` in combat** (v0.12.0 probe, corrected 2026-07-21 — this row previously claimed a blanket ✅) | ✅ |
| **Player's own casts** (`UNIT_SPELLCAST_START` / `SUCCEEDED` / `STOP` / `INTERRUPTED`, `unitTarget == "player"`) | ✅ **yes** — readable spellID in **all four phases**, 0 secret across 178 events (v0.12.0 probe); Blizzard relaxed the restriction for personal casts | ✅ |
| **Cooldown timing** (`GetSpellCooldown().duration`) | ⚠ **combat-gated, not absent** — `<secret fields>` on all 13 tracked spells IN combat, **fully readable on all 13 OUT of combat** (v0.12.0 probe, 2026-07-21). Open-world both runs, so the gate is **combat**, not instancing | ✅ secure swipe via duration object |
| **Aura/DoT/proc timing + stacks** | ❌ query errors / returns nothing in restricted combat | ✅ secure BuffBar / BuffIcon viewer |
| **Buff/proc *presence*** (aura **edges** via `TriggerAlertEvent`) | ✅ **yes** — the alert choke point below delivers applied/removed edges precisely, with no setting dependency | ✅ |
| **Buff/proc *presence*** (`item:IsShown()` **level** on a CDM buff item) | ⚠ **conditional** — readable, but only *means* anything when the viewer hides inactive items (see the `hideWhenInactive` caveat below) | ✅ |

**The surprise win:** Soul Shards are readable *and branchable* in instanced
combat, buff-item `IsShown()` gives us proc *presence* without the secret aura,
and our own casts carry a readable spellID. So the parts of the original vision I
expected to lose — **glitter/sound when shards cap, proc-driven highlights,
self-driven timing cues** — are all buildable in real content. Only *secret*
quantities (exact cooldown remaining, aura stack counts) are off-limits.

### ⚠ `type()` LIES about a Secret Value — the registry-poisoning trap (2026-07-21)

The v0.12.0 probe read `id=<secret>` off an **active** buff item in combat while
the same call out of combat returned `296553`. That matters far beyond the
readout, because of how the value behaves:

**`type(secret) == "number"` is TRUE.** A Secret Value passes an ordinary type
check, so the standard `if ok and type(id) == "number" then return id end` guard
in `ns.ItemSpellID` / `ns.ItemBaseSpellID` **returns the secret** rather than
rejecting it. `ns.IsSecret` is the only reliable test, and it has to be applied at
the *source*, not at every use site.

The consequence is a **poisoned registry**: a rebind that lands in combat stores a
secret as `e.baseSpellID`, and every downstream `e.baseSpellID == spellID`
comparison — `entriesForSpell`, and therefore the whole proc-glow routing — is
then comparing a secret. Corroborating evidence, not yet proven: the same run
logged **`other=47`** in the alert counters, and that bucket doubles as the
`pcall`-failure sink in `HudState.onAlert`. (The counter should be split so
"unhandled alert type" and "handler threw" stop being the same number.)

Rule: **resolve identity out of combat and never overwrite a known-good ID with
an unreadable one.** An unreadable ID means "keep what you had", not "update".

### Spell overrides — the transform channel, confirmed (2026-07-21)

`COOLDOWN_VIEWER_SPELL_OVERRIDE_UPDATED` fired **12 times** in one dummy session,
closing an earlier open question (previously `spell-override events: 0` in every pass). The
pairs also disambiguate three IDs the spec table had been guessing at:

| base | override | note |
| --- | --- | --- |
| `105174` Hand of Gul'dan | **`434635` Ruination** | resolves the 434635/434636 ambiguity |
| `686` Shadow Bolt | **`434506` Infernal Bolt** | resolves the 433891/434506 ambiguity |
| `1276467` Grimoire: Fel Ravager | **`388215` Devour Magic** | the "it becomes a purge on cooldown" case |
| `119898` Command Demon | `119914` Axe Toss | fires normally — see the correction below |

Two findings ride on that table:

1. **Shadow Bolt's half of the Art wheel is observable even though SB is not in
   the tracked set.** The blind-spot list recorded "SB → Infernal Bolt has no icon to light" as
   a permanent blind spot; it is now a blind spot only in *where to draw*, not in
   *what we know*. That reopens it as addressable.
2. **The event is not sufficient on its own** — though *not* for the reason first
   recorded. ⚠ **Corrected 2026-07-21:** the initial run showed Command Demon at
   base≠live with an override count of **zero**, and that was read as "the event
   does not fire for this button". A later run caught it firing **4 times**. The
   real mechanism is duller and more general: the override is set when the pet is
   summoned, which is **before our recorder starts listening** (login, `/reload`,
   or the HUD being enabled mid-session). So the event is fine — our *window* on
   it is what's partial. The conclusion survives intact and matters more broadly
   than a per-button quirk: **a missed event and an absent event are
   indistinguishable to us**, so identity must be **polled at bind time**, with
   the event as the fast path that keeps it current. Any design that trusts only
   the event is correct exactly until something happens before it was watching.

### What we own vs borrow

| Piece | How |
| --- | --- |
| Layout, colour, identity, chrome, keybinds | **ours** (pure rendering — never restricted) |
| Soul Shard rail + cap glitter + cap sound | **ours** (shards readable & branchable) |
| Proc highlight (e.g. a proc lighting the empowered spell) | **ours** (buff-item aura **edges** via `TriggerAlertEvent`; `IsShown()` is only a conditional level backstop) |
| Napkin timing cues (fixed-CD approach, short-CD pings) | **ours** (own casts + `GetSpellBaseCooldown`) |
| Icon art, cooldown swipe, countdown text, charges | **borrowed — and now untouched.** Blizzard's secure Cooldown widget draws it; v1 adds nothing over the icon |
| DoT / proc duration + stacks bars | **borrowed** — restyle the secure BuffBar/Icon viewer |
| "Off cooldown" / "pandemic" **sounds** | **borrowed** — Blizzard's native right-click CDM alerts (secure, survive combat) |
| Which spells tracked, bucket & order | **not ours** — we bind to whatever layout is active, per item by `GetCooldownID()` (§5). We ship no layout string |

**Design consequence:** architect as *dumb honest renderers over the secure CDM*.
Own the logic where the data is ours (shards, proc presence, our own casts,
layout); borrow the display where it isn't (cooldown/DoT timers); route
conditional-in-combat audio through Blizzard's native alerts. Anything needing a
secret quantity is not-in-v1 — and is flagged as such (`architecture.md` → Blind
spots) rather than faked.

### Skinning specifics (source-grounded, 2026-07-15)

Ground truth for item internals is **Blizzard's UI source** (there is no wiki
page for the item templates): [`Blizzard_CooldownViewer/CooldownViewer.lua`](https://github.com/Gethe/wow-ui-source/blob/live/Interface/AddOns/Blizzard_CooldownViewer/CooldownViewer.lua)
· [`.xml`](https://github.com/Gethe/wow-ui-source/blob/live/Interface/AddOns/Blizzard_CooldownViewer/CooldownViewer.xml)
· [`CooldownViewerAlert.lua`](https://github.com/Gethe/wow-ui-source/blob/live/Interface/AddOns/Blizzard_CooldownViewer/CooldownViewerAlert.lua)
· mirror [townlong-yak.com/framexml](https://www.townlong-yak.com/framexml/). Widgets/data:
[UIOBJECT_Cooldown](https://warcraft.wiki.gg/wiki/UIOBJECT_Cooldown),
[C_CooldownViewer](https://warcraft.wiki.gg/wiki/API_C_CooldownViewer.GetCooldownViewerCooldownInfo),
[Secret Values](https://warcraft.wiki.gg/wiki/Secret_Values).

`Blizzard_CooldownViewer` is an **untainted built-in addon** → it reads real
values and drives every icon/bar/text/sound; we restyle pixels, we don't read
values. Blizzard re-applies texture/colour on every per-item repaint, so anything
that *does* write to an item must **re-apply after Blizzard** (§9).

Item anatomy (regions we style): icon items = `Icon` (Texture) + `MaskTexture` +
`Cooldown` (radial swipe) + `ChargeCount.Current` (FontString) + `CooldownFlash`
(off-cd flip anim). Buff-icon adds `Applications` (FontString = aura stack count,
e.g. imp count). Buff-bar = `Bar` (StatusBar) + `.BarBG` + `.Pip` (spark) +
`.Name` + `.Duration`.

| Capability | Verdict | Notes |
| --- | --- | --- |
| Hide/replace/resize/crop **or tint** `Icon` texture | ✅ styleable — **but v1 does not** | `SetTexture(nil)`/`SetAlpha`/`SetTexCoord`; `SetDesaturated(true)` + `SetVertexColor(r,g,b)` keeps the shape and recolours it. **Proven and deliberately unused** — tinting hurt swipe/countdown legibility, so v1 leaves icons native and the hooks sit dormant |
| Restyle cooldown **swipe** (color/edge/texture) | ✅ art | **radial only — no linear mode**; timing secure |
| **Cooldown bar** (linear fill) | ⚠ build-your-own | no native cooldown bar; own StatusBar fed by `C_Spell.GetSpellCooldownDuration` object |
| Restyle/recolor/resize **buff-bar** fill, drop its icon | ✅ styleable | `Bar` StatusBar; `SetBarContent(NameOnly)`; fill secure (`SetValue`), don't read `GetValue` |
| **Cooldown countdown text** | ✅ displayed, ❌ read | Blizzard draws the number; unreadable in Lua (like `Applications` count) |
| Stack count (`Applications`) | ✅ displayed, ❌ read | restyle/enlarge/reposition the FontString; can't read the number. **Wild Imps → enlarge Blizzard's X and append a static "/6"** (the ≥6 Implosion gate); Demonic Core's cap is **4** — different constant, don't cross them |
| Pandemic indicator | ✅ restyle/replace | it's a `PandemicIcon` **state frame** — restyle it, or observe its shown-state and draw our own (e.g. an offset arrow). "In pandemic?" is secret. **Not** available for cooldowns (auras only). |
| Free/proc glow | ✅ art | spell-activation-overlay (`SPELL_ACTIVATION_OVERLAY_GLOW_SHOW/HIDE`, `RefreshOverlayGlow`); restyle via LibCustomGlow; trigger secure. Distinct from **Assisted Highlight** (`C_AssistedCombat`, Blizzard-only). |
| Native sound alerts | ✅ Blizzard-secure | **six** `Enum.CooldownViewerAlertEventType`: `Available` (off-cd), `OnCooldown`, `ChargeGained`, `PandemicTime`, **`OnAuraApplied`**, **`OnAuraRemoved`** → a native sound on *proc-applied* (Demonic Core gained) is possible, not just off-cd/pandemic. User-configured (right-click); programmatic injection = experiment. |
| Layout: orient/rows/direction/spacing | ✅ | `RefreshLayout`: orientation, iconLimit (stride/rows), direction, padding, scale; EditMode / LibEditModeOverride out of combat |
| Draw our own regions past the icon bounds | ✅ unconstrained | no `clipsChildren` in the CDM templates; `MaskTexture` masks only the `Icon`. Anchor per-icon readouts freely (§9) |

**Rolling our own cooldown timer (napkin timing) — CONFIRMED viable.** Cooldown
*timing* is secret, but **the player's own casts are not**: `UNIT_SPELLCAST_START`
and `UNIT_SPELLCAST_SUCCEEDED` filtered to `unitTarget == "player"` deliver a
**readable spellID** in restricted combat, and `GetSpellBaseCooldown(spellID)` is
readable static metadata. So the recipe works: **on player cast → start a
`GetSpellBaseCooldown`-length timer**. Accurate for **fixed-CD** abilities (Summon
Demonic Tyrant = 60 s — the sturdy anchor); **drifts** on haste-scaled charge
recharges and CDR/reset procs, so napkin cues always round down, fire early, and
yield to the native ready-alert as ground truth. `COMBAT_LOG_EVENT_UNFILTERED`
errors now, so `UNIT_SPELLCAST_*` is the surviving cast path. Probed by **`/cdmp
casts`**; v0.5.3 logs START/SUCCEEDED/STOP/INTERRUPTED per-phase.

> **Assumption (2026-07-20):** both events carry a readable spellID **in all
> combat contexts**. Confirmed in a delve (SUCCEEDED) and at an open-world dummy
> (START), and treated as settled — Blizzard relaxed the restriction for personal
> casts, and we are not holding the feature hostage to sampling every content
> type. This also gives us **cast-in-flight** tracking (START →
> SUCCEEDED/STOP/INTERRUPTED) without `UnitCastingInfo`, so the anticipation layer
> rides on one assumed path rather than two. If it ever reads secret somewhere,
> `hud status` says so (`napkin: live | unavailable | not probed`) and we fix it
> then.

**Ready / pandemic / flash are fully re-skinnable — via observation, no secret
read.** `hooksecurefunc` the Blizzard-driven show/hide methods to get the *edge*,
then hide theirs and draw our own arbitrary shape anywhere:

- **Ready edge:** see the alert choke point below — `TriggerAlertEvent` is
  strictly better than either `TriggerAvailableAlert` or the Cooldown widget's
  `OnCooldownDone` script, and gives us the *falling* edge for free. **This means
  we CAN show a ready cue on cooldowns** — from the observed edge, not a secret
  read. This is the M3b mechanism, shipped in v0.7.0.
- **Pandemic:** hook `CooldownViewerItemMixin:ShowPandemicStateFrame` /
  `HidePandemicStateFrame` → hide `item.PandemicIcon`, show our own (e.g. an
  offset arrow). (`IsInPandemicTime` is secret-derived — drive off the hook, not a
  poll.)
- **Off-cd flash:** `item.CooldownFlash:IsShown()` / hook `RefreshSpellCooldownInfo`.

#### `TriggerAlertEvent` — one choke point for every state edge (2026-07-20, M3b)

Re-reading the source for M3b turned up a **better mechanism than the plan
assumed, plus two traps that would have shipped as silent no-ops.** All four
findings are re-verified against `CooldownViewer.lua` @ build 68453.

**(1) `CooldownViewerItemMixin:TriggerAlertEvent(event)` (`:483`) is called as
`self:TriggerAlertEvent(...)` — a dynamic method lookup on the item instance —
from all six alert paths:**

| Enum | Call site | Meaning for us |
| --- | --- | --- |
| `Available` | `:500` | ready **rising** edge |
| `OnCooldown` | `:1068` | ready **falling** edge |
| `OnAuraApplied` | `:612` | proc gained |
| `OnAuraRemoved` | `:622` | proc lost |
| `ChargeGained` | `:608` | charge recharge |
| `PandemicTime` | `:556` | pandemic edge (see below) |

Decisively, **the user's alert configuration is checked *inside* the body**
(`self.alertsByEvent[event]`), *after* the call — so the method is invoked
unconditionally and `hooksecurefunc(item, "TriggerAlertEvent", …)` fires **even
for spells the user has configured no alert on**. One hook per item instance
gives every edge, precisely, with **no polling and no secret read**. This
replaced an `IsShown()`-polling design for #2/#3 and removed the need to pull the
cast-tracking module forward for #5's falling edge.

As with the icon-tint leaf hooks (§9), these methods are `Mixin()`-copied onto
**each** item frame, so the hook must go on the item **instance**, guarded once
per frame.

**(2) TRAP — `OnCooldownDone` cannot be hooked the obvious way.**
`CooldownViewerCooldownItemMixin:OnLoad` does
`self:GetCooldownFrame():SetScript("OnCooldownDone", GenerateClosure(self.OnCooldownDone, self))`
(`:700`, and again at `:1262` for buff icons). The closure captures the
**function reference at OnLoad**, so a later
`hooksecurefunc(item, "OnCooldownDone", …)` is **never reached from the script
path** — it would have shipped as a silent no-op. If it's ever wanted it must be
`item.Cooldown:HookScript("OnCooldownDone", …)`. Given (1), we don't need it.

**(3) The Demonic Art transform is directly observable — and it was already an
M3a bug.** `CooldownViewerItemDataMixin:GetSpellID()` (`CooldownViewerItemData.lua:174`)
returns `overrideSpellID` **in preference to the base spell**, and the viewer
registers **`COOLDOWN_VIEWER_SPELL_OVERRIDE_UPDATED`** carrying
`(baseSpellID, overrideSpellID)` (`:1556`/`:1593`). That event *is* Demonic Art:
HoG → Ruination flips the item's reported spellID. Two consequences:

- **#3 gets a precise trigger** — we learn exactly *which button* transformed,
  rather than inferring "something is armed" from Diabolic Ritual's presence.
  (Which matters more than it sounds: the Ritual buff is present through most of
  the *accumulation*, so presence alone would have been lit nearly always. v0.7.0
  drives the glow off the override event only, and reports the presence edge
  alongside it as corroboration.)
- **It was a live M3a defect** — while transformed, `ns.ItemSpellID` returns
  Ruination, so the M3a keybind lookup missed and **the keybind blanked out**
  mid-rotation. Fixed in v0.7.0: anything keyed on ability *identity* (keybinds,
  the proc registry) resolves off **`GetBaseSpellID()`** (`ns.ItemBaseSpellID`),
  falling back to the override, never the other way round.

**(4) CAVEAT — `IsShown()` presence is conditional on a user setting.**
`CooldownViewerItemMixin:ShouldBeShown()` (`:311`) returns **true immediately**
when `not self.allowHideWhenInactive` **or** `not self.hideWhenInactive`. So if
the buff viewer isn't set to hide-when-inactive, `item:IsShown()` is
**constant-true**, and a proc glow driven off it **latches on permanently** —
worse than no glow at all. The earlier unqualified "proc presence via
`IsShown()`" claim in this section is corrected accordingly: it must be
**capability-checked**, never assumed. v0.7.0 therefore ships a **layered** model
— *edges* (primary, config-independent) · *level* at bind (`IsShown`, only where
the setting makes it meaningful) · a throttled *poll* backstop — and
`/cdmp hud status` reports which layers are actually live rather than pretending.

Also worth a probe: `item.isActive` is the very field `ShouldBeShown` consults
(`:370`/`:378`). If it reads non-secret it's a strictly better level source than
`IsShown`; `hud status` prints it for exactly that reason (M3c upgrade).

**Buff-vs-cooldown = one sequenced widget, but splittable.** Stock CDM overwrites
the item's cooldown with the self-buff's remaining while the buff is up (aura
colour), then shows the recast cooldown — one Cooldown widget, Blizzard-sequenced
(`CacheCooldownValues` → `CheckCacheCooldownValuesFromAura`). To show **two**
elements: render the **cooldown-to-recast** yourself via
`C_Spell.GetSpellCooldownDuration` (duration object, secret-safe), and let
Blizzard drive the **buff** half by tracking that buff in the `BuffBar` viewer.
The buff's remaining time is *not* self-computable as a **number** (aura
`expirationTime` secret); there **is** a secret-safe **object** analogue
(`C_UnitAuras.GetAuraDuration` → `LuaDurationObject`, *not* flagged
`SecretWhenUnitAuraRestricted`, unlike the raw-number `GetAuraBaseDuration`) — but
it needs a valid `auraInstanceID` you can't identify as *yours* without a secret
read, so it's unusable for a DoT in practice (see the paint-vs-feed subsection
below). *(Still open: verify a spell can live in both
Essential + BuffBar categories at once.)*

### Target/unit auras — the *whole record* is secret, not just its timing (2026-07-22, source @ 68453)

Earlier rows in this section said aura *timing/stacks* are secret. The
machine-readable API annotations say more: in restricted content the **entire
`AuraData` record** is secret, by the **same "restricted" gate as cooldowns** —
not a looser one. From `Blizzard_APIDocumentationGenerated/UnitAuraDocumentation.lua`:

- Every `C_UnitAuras.Get*` returning `AuraData` is `SecretWhenUnitAuraRestricted =
  true` — `GetAuraDataByIndex` / `ByAuraInstanceID` / `BySlot` / `BySpellName`,
  `GetBuffDataByIndex`, `GetDebuffDataByIndex`, `GetPlayerAuraBySpellID`,
  `GetUnitAuraBySpellID`. `GetUnitAuras` returns its `auras` table with
  `ConditionalSecretContents = true`. So `spellId`, `applications`, `duration`,
  `expirationTime`, `sourceUnit`, `auraInstanceID`, … are all opaque — reading
  *"is this debuff even up"* is as walled as reading its time-left.
- **Not player-vs-target.** `GetPlayerAuraBySpellID` is *also*
  secret-when-restricted — your own auras via the aura API are as sealed as the
  target's. The reads the HUD actually uses (`UnitPower`, `UNIT_SPELLCAST_*`,
  frame-state) are deliberately **not** the aura API. **So proc presence comes off
  Blizzard's rendered frames (`item:IsShown()`, `TriggerAlertEvent` edges), never
  off `C_UnitAuras`.**
- **Readable escape hatches:** `GetUnitAuraInstanceIDs` / `GetAuraSlots` are *not*
  flagged secret → they return **opaque handles** (you learn auras *exist*, not
  what they are); the `UNIT_AURA` event edge; `AddBlockedAura(unit,
  auraInstanceID)` lets you **hide an aura you can't read**;
  `GetAuraApplicationDisplayCount` returns a display *string* with `NeverSecret`
  min/max clamps; a `RequiresNonSecretAura` carve-out exists for auras the game
  deems non-secret (combat DoTs won't qualify).

### Aura-backed cooldown items — how the CDM tracks a DoT like Agony (2026-07-22, source @ 68453)

A CDM item is **one abstraction over four backing sources**: a totem, a spell
cooldown, a self-aura, or a **target aura** (an offensive DoT). Agony is the last
case — the "cooldown" swipe on its icon is actually the **remaining duration of your
Agony debuff on your target**, not a cooldown.

> ⚠ **Corrected 2026-07-31 (twice).** This section originally said *three* sources and
> offered a `hasAura`/`selfAura` classifier. Both were wrong; see the two amendments
> below. The full resolution model now lives in
> **`knowledge/addon-dev/cooldown-manager.md`** (identity ladder, the per-family value
> cascade, refresh cadence, the readable surface) — read that first; this section keeps
> only the DoT-specific taint ledger.

- ⚠ **The `hasAura`/`selfAura` classifier was WRONG — do not use it.** This bullet used
  to read: *"`hasAura && not selfAura` = target-DoT; `hasAura && selfAura` =
  self-buff-with-duration; `hasAura=false` = a real cooldown."* It is refuted by our own
  measurement: **Demonic Core is `selfAura=true, hasAura=FALSE`** (cooldownID 777) and
  is emphatically not "a real cooldown" — the v0.30.0 fix in `State.lua` exists
  precisely because gating on `hasAura` alone hard-coded every proc aura inactive.
  Two reasons it was never sound:
  1. **Nothing in Blizzard's Lua reads those fields.** A grep across all of
     `Interface/` finds `hasAura`/`selfAura`/`charges` only in the generated
     documentation table — they are DB2 hints the C side consumes. The classifier was
     ours, presented as Blizzard's.
  2. **The real split is the item's mixin family**, which *is* structural: Essential +
     Utility are `CooldownViewerCooldownItemMixin` (four value sources, incl. a real
     spell cooldown); TrackedBuff + TrackedBar are `CooldownViewerBuffItemMixin`
     (three sources, **no cooldown rung at all**). The settings UI enforces the line —
     a row cannot be dragged across it. Classify on **family**; within a family the
     category is user-editable placement and tells you nothing.
- **The struct is still the richest readable config** —
  `C_CooldownViewer.GetCooldownViewerCooldownInfo(cooldownID)` returns
  `{spellID, overrideSpellID, overrideTooltipSpellID, linkedSpellIDs[], selfAura,
  hasAura, charges, isKnown, flags, category}`
  (`CooldownViewerDocumentation.lua:118`), readable even when live aura state is
  secret. The salvageable parts are `linkedSpellIDs` (the static aura-candidate pool —
  this is where the Immolate/Wither pairing already lives, as game data rather than a
  hand-authored spec fact), `isKnown`, `flags` and `category`. Just not
  `hasAura`/`selfAura` as a type oracle.
- **Runtime linkage** (`CooldownViewerItemData.lua`): `scanUnits = {player,
  target}` in order; `FindLinkedSpellForCurrentAuras` matches a `linkedSpellIDs`
  entry and **requires `auraData.sourceUnit == "player"`** (your DoT, not another
  lock's); target auras filtered `"HARMFUL|PLAYER"`. On a hit the aura *becomes*
  the item's identity — `GetSpellID` precedence is *active aura → linked →
  overrideTooltip → override → base* (`:174`) — and its expiration/duration drive
  the swipe.
  ⚠ **This is only ONE of the two ways the `linked` rung gets set.** The other,
  `UpdateLinkedSpell` on `SPELL_UPDATE_COOLDOWN`, needs **no aura and performs no
  sourceUnit check** — it just tests whether the spellID the event happened to carry is
  in `linkedSpellIDs`. It is also *sticky*: an aura removal clears the link only when it
  matches the bound aura. So a row can report a linked identity with nothing live
  anywhere. Full mechanism in `knowledge/addon-dev/cooldown-manager.md` §2.2–2.3.
- **Current target only**, re-homed on target switch (`OnNewTarget`,
  `CooldownViewer.lua:631`). Single-target; a multi-DoT spread across a pack is
  invisible to it.
- `CanUseAuraForCooldown` gates on `Enum.CooldownSetSpellFlags.HideAura` (=1;
  `HideByDefault`=2) — authored in the `CooldownSetSpell` DB2 (wago-readable; same
  table `wowkb.spec_inventory` reads).
- **Taint ledger for a DoT item:** classification **readable**; the swipe (debuff
  time-left) **borrow**; presence **edge** (`OnAuraApplied`/`OnAuraRemoved` via the
  `TriggerAlertEvent` choke point) — *not* a re-scan, because Blizzard's linkage
  scan runs in **untainted** code that reads auras freely and a tainted replica
  hits the wall; pandemic **edge** (below), current target only. So a DoT is
  assistable at **proc-glow fidelity** for the current target; multi-target spread
  stays sealed. This softens the earlier "DoT specs are hopeless" read — see the
  second-spec direction (e.g. an Affliction pass).

### Pandemic — two edge signals, never a number (2026-07-22, source @ 68453)

The red pandemic glow on a DoT is **two separate signals**, both hookable, neither
carrying a value:

1. **One-shot `PandemicTime` alert** (rising edge) — `TriggerPandemicAlert` →
   `TriggerAlertEvent(PandemicTime)` (`CooldownViewer.lua:552`), fires **once per
   aura instance** (guarded by `nextAvailableTimeToPlayPandemicAlert`), through the
   same choke point.
2. **Sustained state frame** — `ShowPandemicStateFrame` (`:570`) /
   `HidePandemicStateFrame` (`:578`), item-instance hookable; shown for the whole
   window (the glow itself).

The window = `[expiration − pandemicCarryover, expiration]`, computed from
`GetRefreshExtendedDuration − GetAuraBaseDuration` (`:511`) — **both secret**, so
you get the edge, never the seconds, and there is no pre-window signal to
*anticipate* off. Only arms for `GetAuraDataUnit() == "target"` (`:515`) → current
target only. ("Refresh on window-open" is the correct DoT play anyway, so the edge
lands where the decision is.) ⚠ **Untested in-game** — the probe has only run on
Demo (no target-DoT tracked). Needs an Affliction pass to confirm the hook fires
in restricted combat (parked in `_meta/kb-inbox.md`).

### Two glow systems + borrowing the swipe: paint vs feed (2026-07-22, source @ 68453)

**Two distinct glow layers** (this doc previously described only the first):

1. **Activation / proc overlay glow** — `RefreshOverlayGlow` (`:1118`) →
   `C_SpellActivationOverlay.IsSpellOverlayed(spellID)` →
   `ActionButtonSpellAlertManager:ShowAlert(item)` / `HideAlert(item)`; the item
   frame is the target. This is a **third proc-presence path** alongside
   `TriggerAlertEvent` and `IsShown` — the `SPELL_ACTIVATION_OVERLAY_GLOW_SHOW/HIDE`
   events carry the spellID edge. *(Open: whether `IsSpellOverlayed` reads
   non-secret when polled in combat; the events are edges regardless.)*
2. **`CooldownViewerVisualAlert` (MarchingAnts + Flash)** — a *separate* pooled,
   self-recycling glow layer, 5 tint variants each (gold `FFD700` / cyan `3FBFD4` /
   red `CA1A1A` / green `4DAF63` / blue `3F6EC7`), acquired via
   `CooldownViewerVisualAlertsManager:AcquireAlert(payload, item)`
   (`CooldownViewerAlert.lua:238`) from the user's right-click **Visual** alert.
   **Candidate for the M4 burst-lane "go" cue in Blizzard's own idiom.**

**Borrowing the swipe = paint vs feed.** The `Cooldown` widget API is partitioned
(`FrameAPICooldownDocumentation.lua`): **feed-the-clock** (`SetCooldown*`,
`GetCooldownTimes` → read = secret) vs **paint-the-dial** (`SetSwipeColor` /
`SetSwipeTexture` / `SetEdgeTexture` / `SetDrawSwipe` / `SetDrawEdge` /
`SetHideCountdownNumbers` / `SetCountdownFont` / `SetReverse` / `SetRotation`).
Styling methods carry **no timing** — the C engine holds the secret duration and
self-animates — **so you restyle without ever knowing the remaining duration.**
Two consequences:

- **Re-apply after Blizzard.** `RefreshSpellCooldownInfo` re-applies `SetSwipeColor`
  + `SetDrawSwipe` + `CooldownFrame_Set` on **every** refresh (`:1037`); a one-shot
  restyle is clobbered → `hooksecurefunc` the item's refresh **per instance** and
  be the last writer (the §9 leaf-hook pattern, applied to `item.Cooldown`).
- **Drawing your OWN timed swipe needs a duration — via a secret-safe object
  only.** `SetCooldown(start,dur)` is `SecretArguments = "AllowedWhenUntainted"` →
  a tainted addon can't pass a secret number, only a non-secret one (napkin) or a
  secret-safe `LuaDurationObject` via `SetCooldownFromDurationObject`.
  `C_Spell.GetSpellCooldownDuration(spellID)` yields one for real cooldowns; for a
  DoT, `GetAuraDuration` yields one too but can't be aimed at your instance (above),
  so **the DoT swipe is borrow-only in practice.**

---

## 5. Architecture

- **Vehicle:** standalone addon `michac/CDMProbe` (MIT), a thin skin over the
  built-in Cooldown Manager. Deployed via ghaddons (GitHub release → install).
- **Bind to the live layout.** Per item by `GetCooldownID()` on the
  `RefreshLayout` hook — reorder-safe, absent spells skipped, no import string.
  Design baseline = the DB2-default filtered set (`CooldownSet`/`CooldownSetSpell`,
  spec 266 = set 60). **Built in M3a** (`HudCore.lua`); the registry is keyed
  `"<viewerName>:cd<cooldownID>"`, with a frame-index fallback for any item that
  doesn't expose one.
  - **Keying on `cooldownID` rather than `spellID` is load-bearing, not
    fastidiousness** — confirmed in-game 2026-07-20: Diabolic Ritual `428514` is
    tracked as **two** cooldownIDs sharing one spellID (§2 correction 2), so a
    spellID-keyed table drops a live item silently.
  - Rebinding is driven by **`RefreshLayout` + `COOLDOWN_VIEWER_DATA_LOADED` +
    `PLAYER_ENTERING_WORLD`**, with **no backstop ticker** (§9). ⏳ *Whether that
    event set is sufficient is **not yet confirmed in-game** — the first pass
    logged `RefreshLayout=0`, i.e. no relayout had happened. This bullet gets
    finished, or corrected with the missing event, after that test.*
- **Leave the icon viewers' icons alone.** v1 draws **chrome around** `item.Icon`
  — keybind corner text, group/mode accents, proc-glow overlays, ready accents —
  and never writes to the icon texture itself, so Blizzard's art, swipe, countdown,
  charges and native glow all survive untouched.
- **Bar viewers:** restyle `item.Bar` on the BuffBar viewer (per-spell colour).
- **Layout:** v1 assumes orientation=Vertical; we **anchor** our overlay to the
  live viewer frames rather than scripting absolute positions. Custom overlays
  (shard rail, burst lane, keybind chrome) are our own frames.
- **Reapply on Blizzard relayout:** post-hook `RefreshLayout` to reflow the
  rail/blocks and re-hook newly-pooled item frames.

Reference (read-only): EnhancedCooldownManager (GPL-3.0) — Soul Shard resource
bar + per-spell coloured bars. No code copied.

### Positioning — anchor, never move

**Positioning: anchor, don't hardcode.** Build overlay frames with
`SetPoint(..., EssentialCooldownViewer, ...)` — anchored to the **live viewer
frame**, not screen coords. When the user drags the CDM in Edit Mode, the
viewer's anchor moves and our overlay **rides along automatically**, no polling.
Frame geometry (`GetRect` / `GetPoint`) is **not** a Secret Value → reading and
following it is legal even in combat (only *changing* the secure frame is
out-of-combat-only). Re-sync on the single choke point:

```lua
hooksecurefunc(EssentialCooldownViewer, "RefreshLayout", function(v) ns:Resync(v) end)
```

`CooldownViewerMixin:RefreshLayout()` runs on tracked-set change (via the
`CooldownViewerSettings.OnDataChanged` callback), orientation/size change, aura
full-update, and show. In `Resync` we re-flow our rail / blocks / keybinds and
read `v:IsHorizontal()` so the overlay degrades gracefully if the user flips
orientation. Anchor the rail to the viewer's *edge* (our rail `TOPRIGHT` → viewer
`TOPLEFT`) so "beside the character" moves as one unit.

**We do NOT reposition the CDM frames (source-grounded 2026-07-18).** The four
viewers inherit **`EditModeCooldownViewerSystemTemplate`** (`CooldownViewer.xml:283`)
→ they are **Edit Mode *system* frames**: protected, position owned by the Edit
Mode manager, not by our `SetPoint`. `EditModeSystemMixin:ApplySystemAnchor()`
(`Blizzard_EditMode/Shared/EditModeSystemTemplates.lua:350`) does
`ClearAllPoints()` + `SetPoint()` **from saved layout data** (`systemInfo.anchorInfo`)
on Edit Mode enter/exit, layout apply, `/reload`, and login. **Consequences:**

- A **runtime-only reposition that auto-reverts when the addon is off is not
  achievable.** Direct `SetPoint` on a viewer is protected (combat-blocked +
  taints Edit Mode), and even OOC the manager re-anchors from saved data and
  clobbers it. There is no transient-position channel for these frames.
- Moving the CDM at all = a **persistent** LibEditModeOverride write into saved
  Edit Mode state; it does not self-revert. "Revert to pre-addon settings" would
  mean **storing the prior `anchorInfo`/orientation and writing it back** through
  the same channel — not a magic undo.
- Forcing a position out-of-band also **desyncs Edit Mode** (editor shows the
  saved spot, frame renders elsewhere, snaps back on Edit Mode open).

**Decision (2026-07-18): the addon never moves the CDM.** The user positions the
CDM once; **our overlay flanks whatever position it has** (anchored to the viewer
frame, §9 F4) — and being *our* frame, the overlay vanishes cleanly when the mod
is off, with zero Edit Mode entanglement and nothing to undo. We also **assume a
vertical layout** rather than staying orientation-agnostic: this is a personal,
opinionated mod, so designing for horizontal isn't worth it. A programmatic
first-run "flank" setter (+ save-for-undo) via LibEditModeOverride is deferred as
**optional polish** (M7) — it is the sole unproven feasibility piece, so keeping
it out of the critical path de-risks the whole config story.

**Combat caveat:** Edit Mode writes (orientation / default position) are
out-of-combat only — apply on `PLAYER_LOGIN` / spec-change, defer if
`InCombatLockdown()`. *Following* the frame by anchor works in combat.

**Edit UI confirmed in-game (2026-07-17).** The per-viewer Edit Mode panel
("Essential Cooldowns") exposes: **Orientation** (Vertical), **# Rows** (the
wrap/`iconLimit` in vertical), **Icon Direction** (Up/Down — the *primary fill
axis* in vertical; wrap columns spill rightward), **Icon Size**, **Icon
Padding**, **Opacity**, **Visibility** (Always/InCombat/Hidden), **Show Timer**,
**Show Tooltips** — plus buttons *Reset To Default Position*, *Advanced Cooldown
Settings* (→ the tracked-set panel), and *Cooldown Manager Options*. The live
vertical Essential + Utility columns flanking the character (ref screenshots
2026-07-17) are the baseline we skin.

*(The Cooldown Layout string / Edit Mode string three-layer model — what each
carries and how a curated layout would be delivered — is parked; it becomes
relevant again only if a curated layout override is re-opened, see `status.md`.)*

---

## 9. M1 build findings (CDMProbe v0.5.x — the prototype skin)

M1 built `/cdmp crt` (`CRT.lua`): keep-and-tint the Essential/Utility icons, draw
dummy chrome (label / keybind / block-char meter), a scanline/vignette overlay, a
viewer-anchored shard rail, and a `DEMONOLOGY.SYS` terminal frame. It validated
five feasibility questions and corrected two earlier assumptions.

> **Read F1/F5 in context:** the icon-tint they validate is **proven but unused** —
> v1 leaves icons native.
> The findings are kept because the hooks stay in the addon, dormant, gating a
> future optional solid-colour mode. F2–F4 are load-bearing for v1 as written.

### F1–F5 verdicts (validated in-game, live 12.0.7)

- **F1 keep + tint — ✅** *(dormant).* `item.Icon:SetDesaturated(true)` +
  `SetVertexColor` keeps the icon shape and recolors it; stable once persisted (F5).
- **F2 chrome over a secure item — ✅.** Our own frames/FontStrings draw over the
  item with no taint. **This is what v1 is built on.**
- **F3 scanline / vignette — ✅.** Overlay frame + line textures over the viewer.
- **F4 anchored rail rides along — ✅.** Rail `SetPoint(TOPRIGHT, viewer, TOPLEFT)`
  follows the CDM when dragged in Edit Mode, no polling.
- **F5 tint persistence — ✅** *(dormant)*, but **not** the way §1/§5 first assumed.

### The persistence fix — hook the LEAF methods, per instance

Blizzard re-colours the icon from many paths, most **outside** `RefreshData`
(`CooldownViewer.lua` @ 68453):

- `RefreshIconColor` → sets `ITEM_USABLE_COLOR` (**white**) from
  `SPELL_UPDATE_USABLE` (line 776), spell-range-check (785), and cooldownID-set
  (715). In a city, usable/range events fire constantly → the observed white flash.
- `RefreshIconDesaturation` → from `OnCooldownDone` (743).
- `RefreshSpellTexture` (`SetTexture`, which resets desaturation + vertex color)
  → from `OnSpellUpdateIconEvent` (191), and inside `RefreshData` (1141).

The fix (v0.5.2): hook the **three leaf methods that actually write the icon** —
`RefreshIconColor`, `RefreshIconDesaturation`, `RefreshSpellTexture` — and
re-force our colour *after* each, so we are the **last writer on every path**.
These methods are **`Mixin()`-copied onto each item frame**, so a hook on the
shared mixin table wouldn't reach already-created frames — hook the **item
INSTANCE** (guarded once per frame). The viewer-level `RefreshLayout` hook is for
**reflowing chrome + re-hooking newly-pooled items** on relayout, never for tint.

**Status: deleted (the finding survives here).** v1 writes nothing to the icon, so
these hooks were never active. When `CRT.lua` was deleted in **M3a (v0.6.0)** this
machinery was rescued into `HudTint.lua` — kept unwired (nothing called
`ns.HudTint.Install()`; every callback gated on `ns.HudTint.enabled = false`) as the
scaffolding an optional solid-colour mode would need. `HudTint.lua` was then **deleted
in W4a (2026-07-24)** alongside the other solid-colour experiments; the last-writer-on-
every-path finding above is recoverable from git history. This is what an optional
solid-colour mode would rebuild (set `enabled`, point `colorFor` at a spellID→rgb
function, install from the bind pass) — recorded here so rediscovering it costs no
build iteration.

**Superseded consequence:** this section used to end with "M3 must decide how
'ready vs on-cooldown' is re-encoded now that we own the icon's colour on every
repaint path." That decision **dissolved** with the aesthetic revision — icons stay
native, so Blizzard's own on-cooldown dimming is preserved for free and we never
owned that pixel. M3b *adds* a ready accent off the observed ready edge (§1) and
owns the empty-board recede; it re-encodes nothing.

### Nothing clips our overlay (drawing is unconstrained; data is the limit)

No `clipsChildren` anywhere in the CDM templates; the item `MaskTexture` masks
only the `Icon` texture, not child regions. So we can draw our own
frames/FontStrings **extending past the icon in any direction**, anchored
per-icon — e.g. a horizontal readout row (`row:SetPoint("LEFT", item, "RIGHT")`).
The real constraint is **data, not drawing**: whatever *fills* such a row (a
cooldown bar / countdown number) is a secret timer, so it must be fed by the
borrowed secure Cooldown widget or the napkin timer, never read by us (§1).

### Chrome on a narrow vertical column

Wide banners (`>> DEMONOLOGY.SYS / v12.0.7 // CDM OVERLAY`) overflow/clip a ~28px
column when anchored with **two** horizontal points (that fixes their width). Use
**compact, single-center-anchor** labels that auto-size over the column
(`DEMO.SYS` / `v12.0.7` header, blinking `C:\>_` footer). Box-drawing glyphs
(`╔══╗`) may not be in WoW's bundled fonts — prefer block chars / ASCII.

### Performance

Cheap and event-driven. Each leaf-hook fire = 3 texture setters; even in combat
across ~12 items that's low-hundreds of trivial calls/sec, well under WeakAuras.
No `OnUpdate` polling (except a single napkin-math countdown); no taint
(`hooksecurefunc` + pure rendering setters).

**Both cleanups are DONE in M3a (v0.6.0)** — with one deliberate substitution:

- **(a) The 2 s backstop ticker is gone.** `HudCore` re-binds the registry *and*
  re-attaches chrome to newly-pooled items inside the `RefreshLayout` callback,
  which is the job the ticker was papering over, plus
  `COOLDOWN_VIEWER_DATA_LOADED` and `PLAYER_ENTERING_WORLD` for tracked-set
  rebuilds without a relayout. `/cdmp hud status` prints per-source fire counts so
  the in-game pass can confirm the event path alone holds. *(If something still
  detaches, the fix is another **event**, not the ticker back — and which event
  was missing gets recorded here.)* **Awaiting the in-game confirmation.**
- **(b) Scanlines no longer grow their pool** — but **not** via the single tiled
  texture originally planned. Tiling needs a bundled power-of-two art file, and a
  binary asset whose load can't be verified from outside the game is a silent
  visual regression waiting to happen. Took the named fallback instead: a **fixed
  pool, hard-capped** (128 lines at 3 px = 384 px of column), allocated lazily and
  only re-anchored on reflow. Allocations stop entirely once the tallest viewer
  has been seen, so it's O(1) amortised — the property the cleanup was for. The
  tiled texture stays available if the cap ever becomes a real limit.

---

## 8. Provenance

- Research: two agent reports (12.0 addon API under Secret Values; glanceable-UI
  design) — synthesized into §1 and the design language (`design.md`).
- Empirical: CDMProbe M0 probe runs (live 12.0.7, Kil'jaeden delve) + the M1
  build (v0.5.x, in-game at The Bazaar — §9) + the v0.5.3 cast-phase probe
  (open-world dummy, 2026-07-19).
- Source (Tier 1): `Gethe/wow-ui-source` @ build **68453** (= live 12.0.7), clone
  at `~/code/github/wow-ui-source` (**present on this machine** — blobless `live`
  checkout). `Blizzard_CooldownViewer/{CooldownViewer, CooldownViewerItemData,
  CooldownViewerAlert, CooldownViewerVisualAlert*,
  CooldownViewerSettingsDataStoreSerialization}.lua`,
  `Blizzard_APIDocumentationGenerated/{CooldownViewer, UnitAura, FrameAPICooldown,
  CooldownViewerConstants, EditModeManagerConstants}Documentation.lua`. Grounds the
  positioning/anchoring approach, the §9 leaf-method finding, the parked config
  model,
  and the **2026-07-22 source-read batch** (target-aura secrecy, aura-backed
  cooldown items, the two glow systems, swipe paint-vs-feed, pandemic two-signal).
- Rotation: `knowledge/classes/warlock/demonology/rotation.md` (Diabolist,
  12.0.7; simc MID1 APL + maxroll/Method/Kalamazi), enriched by
  `diabolist-sequences.md` (top-6 WCL Mythic parses).
