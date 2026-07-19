# Cooldown HUD — technical notes & history

> The **how & why-it-works**: the Secret-Values constraint, the capability map,
> the config/positioning architecture, empirical build findings, and provenance.
>
> **Doc map (§ cross-refs):** §0 Direction + §3 Design language → `spec.md` ·
> §0.5 Guidance model → `guidance-model.md` · §1–§2, §4–§5, §9 → **this doc** ·
> §6 Milestones + §7 Open questions → `milestones.md`.

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
| **Tracked spell IDs** (`item:GetSpellID()`) | ✅ yes | ✅ |
| **Cooldown timing** (`GetSpellCooldown().duration`) | ❌ `<secret>` | ✅ secure swipe via duration object |
| **Aura/DoT/proc timing + stacks** | ❌ query errors / returns nothing in restricted combat | ✅ secure BuffBar / BuffIcon viewer |
| **Buff/proc *presence*** (`item:IsShown()` on a CDM buff item) | ✅ **yes** — shown-state is Blizzard-secure but readable, and tracks the (secret) aura being active | ✅ |

**The surprise win:** Soul Shards are readable *and branchable* in instanced
combat, and buff-item `IsShown()` gives us proc *presence* without the secret
aura. So the parts of the original vision I expected to lose — **glitter/sound
when shards cap, proc-driven highlights** — are actually buildable in real
content. Only self-computed **timers** (cooldown/DoT countdowns) are off-limits.

### What we own vs borrow

| Piece | How |
| --- | --- |
| Layout, color, identity, labels | **ours** (pure rendering — never restricted) |
| Soul Shard counter + cap glitter + cap sound | **ours** (shards readable & branchable) |
| Proc highlight (e.g. Demonbolt lit when Demonic Core up) | **ours** (buff item `IsShown()`) |
| Cooldown swipe / "time left" on a cooldown | **borrowed** — Blizzard's secure Cooldown widget draws it |
| DoT / proc duration + stacks bars | **borrowed** — restyle the secure BuffBar/Icon viewer |
| "Off cooldown" / "pandemic" **sounds** | **borrowed** — Blizzard's native right-click CDM alerts (secure, survive combat) |
| Which spells tracked, bucket & order, bar vs icon, alerts | a **shipped per-spec Cooldown Layout string** (paste → Import); orientation via Edit Mode. Two separate systems — see the three-layer model in §5 |

**Design consequence:** architect as *dumb honest renderers over the secure
CDM*. Own the logic where the data is ours (shards, proc presence, layout);
borrow the display where it isn't (cooldown/DoT timers); route conditional-in-
combat audio through Blizzard's native alerts. Anything needing a self-computed
timer or a secret threshold other than shards is open-world-only or not-in-v1.

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
values. Blizzard re-applies texture/color on every per-item repaint, so a skin
must **re-apply after Blizzard**. M1 found the precise choke points: hook the
**leaf** methods `RefreshIconColor` / `RefreshIconDesaturation` /
`RefreshSpellTexture` **per item instance** (§9), *not* `RefreshData` — which
misses the `SPELL_UPDATE_USABLE` / range-check recolor paths and still flashes.

Item anatomy (regions we style): icon items = `Icon` (Texture) + `MaskTexture` +
`Cooldown` (radial swipe) + `ChargeCount.Current` (FontString) + `CooldownFlash`
(off-cd flip anim). Buff-icon adds `Applications` (FontString = aura stack count,
e.g. imp count). Buff-bar = `Bar` (StatusBar) + `.BarBG` + `.Pip` (spark) +
`.Name` + `.Duration`.

| Capability | Verdict | Notes |
| --- | --- | --- |
| Hide/replace/resize/crop **or tint** `Icon` texture | ✅ styleable | `SetTexture(nil)`/`SetAlpha`/`SetTexCoord`; **`SetDesaturated(true)` + `SetVertexColor(r,g,b)` = keep the icon shape but recolor it** (grayscale→group hue, or uniform green for CRT — the v1 default); re-apply per §9 |
| Restyle cooldown **swipe** (color/edge/texture) | ✅ art | **radial only — no linear mode**; timing secure |
| **Cooldown bar** (linear fill) | ⚠ build-your-own | no native cooldown bar; own StatusBar fed by `C_Spell.GetSpellCooldownDuration` object |
| Restyle/recolor/resize **buff-bar** fill, drop its icon | ✅ styleable | `Bar` StatusBar; `SetBarContent(NameOnly)`; fill secure (`SetValue`), don't read `GetValue` |
| **Cooldown countdown text** | ✅ displayed, ❌ read | Blizzard draws the number; unreadable in Lua (like `Applications` count) |
| Imp/stack count (`Applications`) | ✅ displayed, ❌ read | restyle/enlarge/reposition the FontString; can't read the number → for "[X]/4", enlarge Blizzard's X and append a **static** "/4" |
| Pandemic indicator | ✅ restyle/replace | it's a `PandemicIcon` **state frame** — restyle it, or observe its shown-state and draw our own (e.g. an offset arrow). "In pandemic?" is secret. **Not** available for cooldowns (auras only). |
| Free/proc glow | ✅ art | spell-activation-overlay (`SPELL_ACTIVATION_OVERLAY_GLOW_SHOW/HIDE`, `RefreshOverlayGlow`); restyle via LibCustomGlow; trigger secure. Distinct from **Assisted Highlight** (`C_AssistedCombat`, Blizzard-only). |
| Native sound alerts | ✅ Blizzard-secure | **six** `Enum.CooldownViewerAlertEventType`: `Available` (off-cd), `OnCooldown`, `ChargeGained`, `PandemicTime`, **`OnAuraApplied`**, **`OnAuraRemoved`** → so a native sound on *proc-applied* (Demonic Core gained) is possible, not just off-cd/pandemic. User-configured (right-click); programmatic injection = experiment. |
| Layout: orient/rows/direction/spacing | ✅ | `RefreshLayout`: orientation, iconLimit (stride/rows), direction, padding, scale; EditMode / LibEditModeOverride out of combat |
| Draw our own regions past the icon bounds | ✅ unconstrained | no `clipsChildren` in the CDM templates; `MaskTexture` masks only the `Icon`. Anchor per-icon readouts freely (§9) |

**Rolling our own cooldown timer (best-guess) — CONFIRMED viable.** Cooldown
*timing* is secret, but **the player's own casts are not**: `UNIT_SPELLCAST_SUCCEEDED`
filtered to `unitTarget == "player"` delivers a **readable spellID** in restricted
combat (Blizzard relaxed the spellcast restriction for personal casts), and
`GetSpellBaseCooldown(spellID)` is readable static metadata. So the recipe works:
**on player cast → start a `GetSpellBaseCooldown`-length timer**, and we can drive
our own "Tyrant ~5s from ready" salience. Accurate for **fixed-CD** abilities
(Summon Demonic Tyrant = 60s, Doomguard ≈ 2min); **drifts** on haste-scaled
charge recharges and CDR/reset procs (the real modified cooldown is secret).
`COMBAT_LOG_EVENT_UNFILTERED` errors now, so `UNIT_SPELLCAST_*` is the surviving
cast path. Sanity-checked by **`/cdmp casts`** (v0.2.2). *(documented; verify the
player-filtered spellID passes a live `==` in a raid.)*

**Ready / pandemic / flash are fully re-skinnable — via observation, no secret
read.** `hooksecurefunc` the Blizzard-driven show/hide methods to get the *edge*,
then hide theirs and draw our own arbitrary shape anywhere:
- **Pandemic:** hook `CooldownViewerItemMixin:ShowPandemicStateFrame` /
  `HidePandemicStateFrame` → hide `item.PandemicIcon`, show our own (e.g. an
  offset arrow). (`IsInPandemicTime` is secret-derived — drive off the hook, not a poll.)
- **Ready edge:** hook `TriggerAvailableAlert` or the Cooldown widget's
  `OnCooldownDone` script → drive our own "ready" glow. **This means we CAN show a
  ready-glow on cooldowns after all** — from the observed edge, not a secret read.
- **Off-cd flash:** `item.CooldownFlash:IsShown()` / hook `RefreshSpellCooldownInfo`.

**Buff-vs-cooldown = one sequenced widget, but splittable.** Stock CDM overwrites
the item's cooldown with the self-buff's remaining while the buff is up (aura
color), then shows the recast cooldown — one Cooldown widget, Blizzard-sequenced
(`CacheCooldownValues` → `CheckCacheCooldownValuesFromAura`). To show **two**
elements: render the **cooldown-to-recast** yourself via
`C_Spell.GetSpellCooldownDuration` (duration object, secret-safe), and let
Blizzard drive the **buff** half by tracking that buff in the `BuffBar` viewer.
The buff's remaining time is *not* self-computable (aura `expirationTime` secret;
no aura-duration-object analogue). *(verify a spell can live in both Essential +
BuffBar categories at once.)*

---

## 2. The Demonology target

Confirmed tracked set (from the live `dump`, Diabolist profile):

- **Essential (cooldowns):** Hand of Gul'dan `105174`, Call Dreadstalkers
  `104316`, Summon Demonic Tyrant `265187`, Grimoire: Fel Ravager `1276467`,
  Implosion `196277`, Demonbolt `264178`
- **Utility:** Unending Resolve `104773`, Dark Pact `108416` (defensives);
  Shadowfury `30283`, Axe Toss `119914`, Mortal Coil `6789` (CC); Demonic
  Circle: Teleport `48020` (mobility); Blight of Tongues `1271802`
- **Buff bars:** Demonic Core `264173`, Dominion of Argus `1276166`, Unending
  Resolve, Call Dreadstalkers
- **Buff icons:** Wild Imp `296553`, Diabolic Ritual `428514`

**Rotation shape** (distilled from `knowledge/classes/warlock/demonology/
rotation.md`, Diabolist, 12.0.7). Demo is a builder/spender pet-army spec: build
Soul Shards → spend on **Hand of Gul'dan** (summons Wild Imps) → funnel
everything into the **Summon Demonic Tyrant** window (1-min CD, empowers/extends
every demon). The single biggest lever is **how many Hand of Gul'dan casts fit
inside the Tyrant window** — enter it with demons freshly summoned and 2+
Demonic Core charges banked.

**The burst window = the horizontal grouping.** Tyrant should line up with the
demon-summon cooldowns you fire just before it: **Call Dreadstalkers · Grimoire:
Fel Ravager · Summon Doomguard**. When those are up together, the window is
ready. This is the canonical "line Tyrant up with what it buffs" the whole HUD
concept is about — realized (§0) as **our overlay frames beside the vertical CDM
column**, not as a horizontal row inside the CDM's own layout.

**What drives salience (only what we can read):**
- Soul Shards 0–5 (readable) — the rotation gate; cap = act (spend a Hand of
  Gul'dan / commit Tyrant).
- Demonic Core proc *presence* (buff `IsShown`) — highlight Demonbolt.
- Wild Imp presence (buff `IsShown`) — Implosion becomes relevant (imp *count*
  ≥6 is secret; presence + the secure icon's own stack text is the fallback).
- Cooldown ready — cannot self-detect; shown via the borrowed swipe + native
  "ready" sound.

---

## 4. Design exploration

Five interactive prototypes (solid-color, JS-animated within the capability map)
live in the published **"Demonology CDM — 5 design directions"** artifact. They
explore: (1) Priority Column, (2) Burst Lane, (3) Resource-Centric, (4) Compact
Dashboard, (5) Clear-the-Board. Each animates only what's actually achievable —
shard fills + cap glitter (ours), cooldown swipe drain (borrowed), proc glow
(presence). *(This first artifact explored **layout**; the second, below, explored
**visual style** and drove the v1 decision.)*

**Visual-style exploration (2026-07-17) — CRT chosen.** A second artifact restyles
the **real Blizzard icon columns** (icons kept + tinted, addon-feasible ops only,
each direction captioned with its "WoW mapping") across five aesthetics: (A)
Gnomeregan powered-goggles, (B) **CRT / green-phosphor ← CHOSEN**, (C) LCARS, (D)
Bound Grimoire, (E) Neon District (cyberpunk). Saved in-repo at
[`../prototype/overlay-styles.html`](../prototype/overlay-styles.html); published
artifact: <https://claude.ai/code/artifact/939bac84-6701-4eab-ae7c-33f70d40a327>.
**v1 = CRT:** icons desaturated + green-tinted in place (`SetDesaturated` +
`SetVertexColor`), block-char meters, monospace 4-letter labels + keybinds, a
scanline/vignette overlay texture (fake, not a shader). The direction-B terminal
chrome (a `DEMONOLOGY.SYS` header/footer frame, blinking `C:\>_` prompt) was
brought into the addon in the M1 build (§9). **Open tweak:** icon-tint brightness
— bright & clearly readable (current) vs dimmed "text-first / ghostly icons."
Everything else (LCARS elbow curves, grimoire ink-wobble) was flagged as needing
bespoke texture art or being unbuildable; CRT was the most natively feasible.

---

## 5. Architecture

- **Vehicle:** standalone addon `michac/CDMProbe` (MIT), a thin skin over the
  built-in Cooldown Manager. Deployed via ghaddons (GitHub release → install).
- **Skin the icon viewers (treat in place, don't hide):** the v1 default **keeps**
  `item.Icon` and recolors it — `SetDesaturated(true)` + `SetVertexColor` (uniform
  green for the chosen CRT look; group-hue for other directions) — plus our
  4-letter label + keybind around it, leaving the secure `item.Cooldown` swipe
  running over it. This preserves Blizzard's info (icon recognizability, charges,
  proc glow). Full abstraction (hide `Icon` → solid color block) stays an option
  for directions that want it (e.g. LCARS).
- **Bar viewers:** restyle `item.Bar` on the BuffBar viewer (per-spell color).
- **Layout:** we set orientation=Vertical as a default; we **anchor** our overlay
  to the live viewer frames rather than scripting absolute positions (see the
  three-layer model below). Custom overlays (shard rail) are our own frames.
- **Reapply on Blizzard relayout:** post-hook `RefreshLayout` for **relayout**
  (reflow the rail/blocks, re-hook newly-pooled item frames). **Tint persistence
  is a *separate* mechanism** — per-item leaf-method hooks (§9). The earlier
  "RefreshLayout is the single persist watchdog" assumption was **wrong**: it does
  not fire on the per-item recolor paths.

Reference (read-only): EnhancedCooldownManager (GPL-3.0) — Soul Shard resource
bar + per-spell colored bars. No code copied.

### Config delivery & positioning — the three-layer model (source-grounded 2026-07-17)

Verified against the live Blizzard source (`Gethe/wow-ui-source` @ build 68453 =
12.0.7; clone at `~/code/github/wow-ui-source`):
`Blizzard_CooldownViewer/CooldownViewer.lua`,
`CooldownViewerSettingsDataStoreSerialization.lua`,
`Blizzard_APIDocumentationGenerated/EditModeManagerConstantsDocumentation.lua`.
**"Layout" names two independent systems**, each with its own import/export
string — plus our overlay on top:

| Layer | Carries | Delivery |
| --- | --- | --- |
| **① Cooldown Layout** — the "Cooldown Settings" panel → *Copy to Clipboard / Import*; backed by `C_CooldownViewer.GetLayoutData()` / `SetLayoutData()` | **tracked set + per-cooldown category** (Essential / Utility / Hidden, and buff **Icon** = `TrackedBuff` vs **Bar** = `TrackedBar`) + **order** + **per-cooldown alert overrides**. Spec-aware (keyed by class+spec tag). **No** orientation/size/position. | **Auto-apply (confirmed viable, OOC — §7):** addon merges our per-spec layout via `CooldownViewerSettings:GetLayoutManager():ImportLayout(str)` (the Import button's own path) and sets it active — no paste. `SetLayoutData(str)` is also writable but replaces the **whole** store (all specs) → prefer the merge. Fallback: user pastes into the panel's Import. |
| **② Edit Mode** — `EditModeCooldownViewerSetting` | **Orientation** (Horizontal/**Vertical**), IconLimit (wrap), IconDirection, IconSize, IconPadding, Opacity, VisibleSetting, BarContent (IconAndName/IconOnly/**NameOnly**), HideWhenInactive, ShowTimer, ShowTooltips, BarWidthScale — plus frame **position**. Has its own *whole-HUD* export string. | Addon sets **only** Orientation=Vertical (+ optional first-run position) in the user's *current* layout via **LibEditModeOverride**, out of combat. Never ship the whole-HUD string — it clobbers the user's other frames. Position stays the user's. |
| **③ Our overlay** | color, 4-letter labels, keybind text, soul-shard rail, generator/consumer batching, cyberpunk skin | Addon frames, anchored to the viewers (below). |

**Exact serialized fields** (`CooldownViewerSettingsDataStoreSerialization.lua`):
`COOLDOWN_ORDER`, `CATEGORY_OVERRIDES`, `ALERT_OVERRIDES` — CBOR → Deflate →
Base64, prefixed `<encodingVersion>|`. **Two consequences:** (a) **alerts ride in
the string** → a chunk of the §3 / M6 audio+visual-alert set (`Available` /
`OnCooldown` / `PandemicTime` / **`OnAuraApplied`** …) ships *inside* the import
string, secure and combat-safe; (b) icon-vs-bar for buffs is just a category
(`TrackedBuff` vs `TrackedBar`), so it travels in the string too — no separate
setting to configure.

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
read `v:IsHorizontal()` so the overlay stays **orientation-agnostic** (the user
can flip back to horizontal without breaking us). Anchor the rail to the viewer's
*edge* (our rail `TOPRIGHT` → viewer `TOPLEFT`) so "beside the character" moves as
one unit. *(Correction, M1: `RefreshLayout` handles relayout + re-hooking new
items — it does **not** catch per-item recolors, so it is **not** the tint
watchdog. Tint persistence uses per-item leaf hooks; see §9.)*

**Combat caveat:** Edit Mode writes (orientation / default position) are
out-of-combat only — apply on `PLAYER_LOGIN` / spec-change, defer if
`InCombatLockdown()`. *Following* the frame by anchor works in combat.

**Edit UI confirmed in-game (2026-07-17).** The per-viewer Edit Mode panel
("Essential Cooldowns") exposes: **Orientation** (Vertical), **# Rows** (the
wrap/`iconLimit` in vertical), **Icon Direction** (Up/Down — the *primary fill
axis* in vertical; wrap columns spill rightward), **Icon Size**, **Icon
Padding**, **Opacity**, **Visibility** (Always/InCombat/Hidden), **Show Timer**,
**Show Tooltips** — plus buttons *Reset To Default Position*, *Advanced Cooldown
Settings* (→ the tracked-set panel = system ①), and *Cooldown Manager Options*.
The live vertical Essential + Utility columns flanking the character (ref
screenshots 2026-07-17) are the baseline we skin.

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
frame, §5/§9 F4) — and being *our* frame, the overlay vanishes cleanly when the
mod is off, with zero Edit Mode entanglement and nothing to undo. We also **assume
a vertical layout** rather than staying orientation-agnostic: this is a personal,
opinionated mod (text reads left→right, etc.), so designing for horizontal isn't
worth it. A programmatic first-run "flank" setter (+ save-for-undo) via
LibEditModeOverride is deferred as **optional polish** (M7), worth building only
if the one-time manual Edit Mode setup proves annoying — it is the sole unproven
feasibility piece, so keeping it out of the critical path de-risks the whole
config story.

---

## 9. M1 build findings (CDMProbe v0.5.x — the prototype skin)

M1 built `/cdmp crt` (`CRT.lua`): keep-and-tint the Essential/Utility icons, draw
dummy chrome (label / keybind / block-char meter), a scanline/vignette overlay, a
viewer-anchored shard rail, and a `DEMONOLOGY.SYS` terminal frame. It validated
the five feasibility questions **and corrected two earlier assumptions.**

### F1–F5 verdicts (validated in-game, live 12.0.7)

- **F1 keep + tint — ✅.** `item.Icon:SetDesaturated(true)` + `SetVertexColor`
  keeps the icon shape and recolors it green; stable once persisted (F5).
- **F2 chrome over a secure item — ✅.** Our own frames/FontStrings draw over the
  item with no taint.
- **F3 scanline / vignette — ✅.** Overlay frame + line textures over the viewer.
- **F4 anchored rail rides along — ✅.** Rail `SetPoint(TOPRIGHT, viewer, TOPLEFT)`
  follows the CDM when dragged in Edit Mode, no polling.
- **F5 tint persistence — ✅, but NOT the way §1/§5 first assumed** (below).

### The persistence fix — hook the LEAF methods, per instance (corrects §1/§5)

The earlier claim ("post-hook `RefreshData` to persist") was **wrong**. Blizzard
re-colors the icon from many paths, most **outside** `RefreshData`
(`CooldownViewer.lua` @ 68453):

- `RefreshIconColor` → sets `ITEM_USABLE_COLOR` (**white**) from
  `SPELL_UPDATE_USABLE` (line 776), spell-range-check (785), and cooldownID-set
  (715). In a city, usable/range events fire constantly → the observed white flash.
- `RefreshIconDesaturation` → from `OnCooldownDone` (743).
- `RefreshSpellTexture` (`SetTexture`, which resets desaturation + vertex color)
  → from `OnSpellUpdateIconEvent` (191), and inside `RefreshData` (1141).

Hooking only `RefreshData` (addon v0.5.1) still flashed on the usable/range paths
(status showed 65 fires yet it flickered). The fix (v0.5.2): hook the **three leaf
methods that actually write the icon** — `RefreshIconColor`,
`RefreshIconDesaturation`, `RefreshSpellTexture` — and re-force our green *after*
each, so we are the **last writer on every path**.

These methods are **`Mixin()`-copied onto each item frame**, so a hook on the
shared mixin table wouldn't reach already-created frames — we hook the **item
INSTANCE** (guarded once per frame). The viewer-level `RefreshLayout` hook is kept
only to **reflow chrome + re-hook newly-pooled items** on relayout — not for tint.

**Design consequence** (feeds spec.md §3): forcing uniform green in the hook also
overrides Blizzard's on-cooldown desaturation dimming. Fine for the M1 uniform-CRT
look; **M3 must decide how "ready vs on-cooldown" is re-encoded** (luminance per
§3) now that we own the icon's color on every repaint path.

### Nothing clips our overlay (drawing is unconstrained; data is the limit)

No `clipsChildren` anywhere in the CDM templates; the item `MaskTexture` masks
only the `Icon` texture, not child regions. So we can draw our own
frames/FontStrings **extending past the icon in any direction**, anchored
per-icon — e.g. a horizontal readout row (`row:SetPoint("LEFT", item, "RIGHT")`)
like the prototype's `TYRA [Z] ██████████ READY`. The real constraint is **data,
not drawing**: whatever *fills* such a row (a cooldown bar / countdown number) is
a secret timer, so it must be fed by the borrowed secure Cooldown widget or the
napkin-math timer, never read by us (§1).

### Chrome on a narrow vertical column

Wide banners (`>> DEMONOLOGY.SYS / v12.0.7 // CDM OVERLAY`) overflow/clip a ~28px
column when anchored with **two** horizontal points (that fixes their width). Use
**compact, single-center-anchor** labels that auto-size over the column
(`DEMO.SYS` / `v12.0.7` header, blinking `C:\>_` footer). Box-drawing glyphs
(`╔══╗`) may not be in WoW's bundled fonts — prefer block chars / ASCII.

### Performance

Cheap and event-driven. Each leaf-hook fire = 3 texture setters; even in combat
across ~12 items that's low-hundreds of trivial calls/sec, well under WeakAuras.
No `OnUpdate` polling (except a single napkin-math countdown, later); no taint
(`hooksecurefunc` + pure rendering setters). **Pending cleanups (M3 polish):**
(a) re-hook new items off the `RefreshLayout` event and **drop the 2s backstop
ticker**; (b) replace the N scanline textures with one **tiled** texture.

---

## 8. Provenance

- Research: two agent reports (12.0 addon API under Secret Values; glanceable-UI
  design) — synthesized into §1 and spec.md §3.
- Empirical: CDMProbe M0 probe runs (live 12.0.7, Kil'jaeden delve) + the M1
  build (v0.5.x, in-game at The Bazaar — §9).
- Source (Tier 1): `Gethe/wow-ui-source` @ build **68453** (= live 12.0.7), clone
  at `~/code/github/wow-ui-source` — `Blizzard_CooldownViewer/{CooldownViewer,
  CooldownViewerSettingsDataStoreSerialization}.lua`,
  `Blizzard_APIDocumentationGenerated/EditModeManagerConstantsDocumentation.lua`.
  Grounds the §5 three-layer config model, the serialized-field list, the
  `RefreshLayout`/anchoring positioning approach, and the §9 leaf-method finding.
- Rotation: `knowledge/classes/warlock/demonology/rotation.md` (Diabolist,
  12.0.7; simc MID1 APL + maxroll/Method/Kalamazi).
