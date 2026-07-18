# Cooldown HUD — project spec & design doc

A spec-specific **overlay that enhances Blizzard's built-in Cooldown Manager**
(Midnight 12.0), authored against an imported cooldown-settings profile. The
idea: **vertical space encodes priority, horizontal space encodes grouping**
(line a burst cooldown up with what it buffs) — realized as a **vertical CDM
column with our overlay frames beside it**. We **keep Blizzard's icons and
recolor them in place** (desaturate + tint), add short labels + keybinds, live
resource counters, timing/decay cues, "juice" (glitter) when a resource caps,
and audio cues from a learnable library. Decluttering is the game: an **empty
board = nothing to do**. See §0 for the sharpened direction.

**v1 target spec: Demonology Warlock.** Prototype/probe addon: `michac/CDMProbe`
(checked out at `addon/`, gitignored from the workspace). This doc is the source
of truth for the design; the addon is the source of truth for the code.

Status: **M0 (feasibility probe) complete** — the §1 capability map is confirmed
on the live 12.0.7 client (delve, in combat), and the §5 config-delivery /
positioning model is **source-grounded** against the live Blizzard UI code
(`Gethe/wow-ui-source` @ build 68453 = 12.0.7). **Next: M1 — a feasibility
prototype skin** (dummy content) to prove the rendering/anchoring stack is
buildable before wiring real config.

---

## 0. Direction (sharpened 2026-07-17)

The concept narrows from "a glanceable HUD" to a specific, opinionated product:
**a spec-specific overlay that *enhances* Blizzard's Cooldown Manager, authored
against an imported cooldown-settings profile.** Three pillars:

1. **Opinionated, imported config is a hard dependency.** The overlay is authored
   against an *exact* tracked set — every cooldown in every bucket (Essential /
   Utility / Buff), in a **known order**. You import our per-spec **Cooldown
   Layout string** (§5); the overlay's color / priority / keybind map is keyed to
   it. **Auto-apply is confirmed viable** (§7 probe: `SetLayoutData` is
   addon-writable out of combat), so enforcement strength (auto-apply →
   import-and-verify → nag) is now a **UX choice, not a capability question**; the
   *authoring* assumption — a fixed, known layout — is not negotiable either way.
   This is the anti-WeakAuras: one blessed layout per spec, deterministic
   downstream, instead of "configure everything."
2. **Deploy vertically, beside the character** (left or right) — not a bar
   under/over. Priority reads top→bottom. The overlay follows the CDM frame's
   **runtime** position by anchoring (§5), so the user keeps control of placement;
   we only ship orientation as a default.
3. **The overlay enhances, doesn't replace.** On top of Blizzard's secure
   widgets: **resource bars that recolor by condition** (soul-shard spend vs
   generate), **keybind labels** on cooldown abilities, an **attention-grabber**
   when a big cooldown is up (napkin-math timer, §1), and **generator-vs-consumer
   color batching** so builders and spenders read at a glance. **Stretch:** a
   cyberpunk skin.

Everything below still holds; where the original "2D board" assumed a single grid
*under* the character, the **horizontal grouping** (burst lane) now lives in *our*
overlay frames beside a **vertical** CDM, not in the CDM's own layout.

**Chosen v1 aesthetic (2026-07-17): CRT / green-phosphor** (§4). Crucially it's a
*treatment of Blizzard's real icon columns*, not an independent UI: we **keep**
the icons and desaturate + green-tint them in place (`SetDesaturated(true)` +
`SetVertexColor`), add monospace 4-letter labels + keybinds, block-char meters,
and a scanline/vignette overlay — so Blizzard's info (icon shape, cooldown swipe,
charges, proc glow) survives. "No icons" from the original vision is retired in
favour of "**icons kept, recolored**."

---

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
values. Blizzard re-applies texture/color each update, so a skin must
**post-hook `RefreshData`** (or the specific `Refresh*`) to persist.

Item anatomy (regions we style): icon items = `Icon` (Texture) + `MaskTexture` +
`Cooldown` (radial swipe) + `ChargeCount.Current` (FontString) + `CooldownFlash`
(off-cd flip anim). Buff-icon adds `Applications` (FontString = aura stack count,
e.g. imp count). Buff-bar = `Bar` (StatusBar) + `.BarBG` + `.Pip` (spark) +
`.Name` + `.Duration`.

| Capability | Verdict | Notes |
| --- | --- | --- |
| Hide/replace/resize/crop **or tint** `Icon` texture | ✅ styleable | `SetTexture(nil)`/`SetAlpha`/`SetTexCoord`; **`SetDesaturated(true)` + `SetVertexColor(r,g,b)` = keep the icon shape but recolor it** (grayscale→group hue, or uniform green for CRT — the v1 default); post-hook `RefreshData` |
| Restyle cooldown **swipe** (color/edge/texture) | ✅ art | **radial only — no linear mode**; timing secure |
| **Cooldown bar** (linear fill) | ⚠ build-your-own | no native cooldown bar; own StatusBar fed by `C_Spell.GetSpellCooldownDuration` object |
| Restyle/recolor/resize **buff-bar** fill, drop its icon | ✅ styleable | `Bar` StatusBar; `SetBarContent(NameOnly)`; fill secure (`SetValue`), don't read `GetValue` |
| **Cooldown countdown text** | ✅ displayed, ❌ read | Blizzard draws the number; unreadable in Lua (like `Applications` count) |
| Imp/stack count (`Applications`) | ✅ displayed, ❌ read | restyle/enlarge/reposition the FontString; can't read the number → for "[X]/4", enlarge Blizzard's X and append a **static** "/4" |
| Pandemic indicator | ✅ restyle/replace | it's a `PandemicIcon` **state frame** — restyle it, or observe its shown-state and draw our own (e.g. an offset arrow). "In pandemic?" is secret. **Not** available for cooldowns (auras only). |
| Free/proc glow | ✅ art | spell-activation-overlay (`SPELL_ACTIVATION_OVERLAY_GLOW_SHOW/HIDE`, `RefreshOverlayGlow`); restyle via LibCustomGlow; trigger secure. Distinct from **Assisted Highlight** (`C_AssistedCombat`, Blizzard-only). |
| Native sound alerts | ✅ Blizzard-secure | **six** `Enum.CooldownViewerAlertEventType`: `Available` (off-cd), `OnCooldown`, `ChargeGained`, `PandemicTime`, **`OnAuraApplied`**, **`OnAuraRemoved`** → so a native sound on *proc-applied* (Demonic Core gained) is possible, not just off-cd/pandemic. User-configured (right-click); programmatic injection = experiment. |
| Layout: orient/rows/direction/spacing | ✅ | `RefreshLayout`: orientation, iconLimit (stride/rows), direction, padding, scale; EditMode / LibEditModeOverride out of combat |

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

## 3. v1 layout spec

### Layout sketch (vertical = priority, horizontal = grouping)

```
        shards  ▮▮▮▮▯                              ← resource rail (OURS: glitter + sound at 5)

   ┌─ burst window ───────────────────────┐
   │  TYRA    DREA    FELR                 │        ← horizontal group: line up before Tyrant
   └───────────────────────────────────────┘          (all lit = go)
        HAND    CORE*   IMPL                        ← core spenders (CORE=Demonbolt, glows on proc)

   Demonic Core ▬▬▬2      Dominion ▬▬               ← BORROWED secure bars (secret timers, styled)

   UNEND  DARK  │  SHAD  AXE  MORT  │  CIRC         ← utility: defensive │ CC │ mobility
```

> **Reconciling with the overlay model (§0):** this sketch is the *logical*
> layout. In the shipped product the CDM itself is a **vertical column**
> (Essential, then Utility) and the horizontal affordances above — the burst
> lane and the shard rail — are **our overlay frames anchored beside it** (§5),
> not extra rows inside the CDM. Position reads top→bottom down the column;
> grouping reads across our overlay.

### Priority tiers (role-static, NOT dynamically re-sorted)

Because cooldown readiness is secret, tiers are **fixed by role** — which is also
what the glanceability research recommends (stable positions build muscle
memory; never continuously re-sort). Liveness comes from salience *within* the
fixed layout, not from reordering.

- **Rail (top):** Soul Shards. The one thing that's fully ours and drives the
  whole rotation.
- **Tier 1 — burst lane:** Tyrant + Dreadstalkers + Grimoire: Fel Ravager,
  aligned horizontally. Shared lane tint (common region) so "the window" reads
  as one object; when all three are available they brighten together
  (common-fate).
- **Tier 2 — core spenders:** Hand of Gul'dan, Demonbolt, Implosion.
- **Tier 3 — utility:** defensives / CC / mobility, sub-grouped horizontally.

### Colour language (grayscale-legible, redundant)

Hue carries **group**, not per-ability identity (stays inside the ~7-color
categorical ceiling). Reuse WoW school associations. Identity =
color(group) × position × 4-letter label, so it survives desaturation / CVD /
periphery.

| Group | Hue | Members |
| --- | --- | --- |
| Summon-demon (burst) | fel green | Tyrant, Dreadstalkers, Grimoire: Fel Ravager, Doomguard |
| Core shadow damage | shadow violet | Hand of Gul'dan, Demonbolt, Shadow/Infernal Bolt |
| Fel explosion | bright lime | Implosion |
| Proc / resource | arcane cyan | Demonic Core, Soul Shard rail accent |
| Defensive | blue | Unending Resolve, Dark Pact |
| CC | muted slate | Shadowfury, Axe Toss, Mortal Coil |
| Mobility | gold | Demonic Circle |

Saturation/luminance encode **state, not identity**: dim = on cooldown / not
ready; bright = ready/actionable. That makes "readiness" a preattentive
luminance pop, independent of the identity hue.

### Encoding rules per state

| State | Encoding | Source |
| --- | --- | --- |
| On cooldown | dim block + secure radial swipe draining | borrowed |
| Ready | bright, saturated block; one-shot "settle" on arrival | ours (style) + native ready sound |
| Shards 0–5 | segmented rail fills; at 5 → gold + one-shot glitter + earcon | **ours** |
| Demonic Core proc up | Demonbolt block glows / outlined | **ours** (`IsShown`) |
| DoT/proc time + stacks | restyled secure bar, drains toward empty | borrowed |
| Pandemic / refresh window | native visual + sound alert | borrowed (right-click CDM alert) |
| Not actionable | recede (dim) — never continuously animate a steady state | ours |

### Audio spec (~6 earcons, timbre-distinct, short/soft)

| Event | Sound | Ours / native |
| --- | --- | --- |
| Soul Shards cap (5) | bright rising "charge" tick | **ours** (shards readable) |
| Summon Demonic Tyrant ready | low resonant "gong" | native ready alert |
| Call Dreadstalkers ready | mid double-tick | native ready alert |
| Demonic Core proc gained | soft cyan "ding" | **native `OnAuraApplied` alert** (secure) — or ours via `IsShown` edge |
| DoT pandemic (if tracked) | dissonant "thunk" | native pandemic alert |
| Board cleared / all-quiet | (optional) soft settle | ours |

Frequency-inversely-proportional-to-loudness; global mute + per-event toggles.

**Sound sources (M6 audio).** Two tiers, both MIT-clean: (1) **built-in `PlaySound(SOUNDKIT.*)`**
— zero bytes, no license, survives combat; audition via [wowhead.com/sounds](https://www.wowhead.com/sounds)
+ [wago.tools/db2/SoundKitName](https://wago.tools/db2/SoundKitName). Candidates:
`READY_CHECK`, `UI_BNET_TOAST`, checkbox tick, coin. (2) **Bundled `.ogg`** under
`CDMProbe\Sound\`, registered in **LibSharedMedia-3.0** (so users can reassign/mute):
**[Kenney UI Audio](https://kenney.nl/assets/ui-audio) (CC0)** is the top pick;
Freesound CC0 + Material Design (CC-BY, needs credit) backfill. **Avoid** (non-
redistributable): Google Assistant library, Sonniss raw files, GTFO/DBM/BigWigs
assets (ARR). Convert wav→ogg: `ffmpeg -i in.wav -c:a libvorbis -q:a 4 out.ogg`,
≤300ms, −3…−6 dB. Reserve bundled files for **shard-cap** + **proc-gained** (ours);
route **ready/pandemic** through the native CDM alert.

### The shipped profile

v1 standardizes on one CDM tracked-set profile so the color/priority map is
deterministic. Candidate: **Kalamazi "Demonology CDM"** (referenced in
`rotation.md`). Decision pending — the ability→tier/color map must match whatever
profile we ship (either an import string bundled in the addon or a short
"set these in Edit Mode" list).

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
[`prototype/overlay-styles.html`](prototype/overlay-styles.html); published
artifact: <https://claude.ai/code/artifact/939bac84-6701-4eab-ae7c-33f70d40a327>.
**v1 = CRT:** icons desaturated + green-tinted in place (`SetDesaturated` +
`SetVertexColor`), block-char meters, monospace 4-letter labels + keybinds, a
scanline/vignette overlay texture (fake, not a shader). **Open tweak:** icon-tint
brightness — bright & clearly readable (current) vs dimmed "text-first / ghostly
icons." Everything else (LCARS elbow curves, grimoire ink-wobble) was flagged as
needing bespoke texture art or being unbuildable; CRT was the most natively
feasible of the five.

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
- **Reapply on Blizzard relayout:** post-hook `RefreshLayout` (the single choke
  point — see below), not a poll.

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
can flip back to horizontal without breaking us). The same hook doubles as the
"persist our skin after Blizzard repaints" watchdog. Anchor the rail to the
viewer's *edge* (our rail `TOPRIGHT` → viewer `TOPLEFT`) so "beside the
character" moves as one unit.

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

---

## 6. Milestone log

Ordering rationale (2026-07-17): **prove the rendering stack works before wiring
real config.** The overlay is authored *against* an imported layout (§0 pillar
1), so it's tempting to build config first — but the open risk is whether we can
skin + anchor at all. So M1 is a throwaway-content prototype that answers that;
only then do we author the real config (M2) and re-point the skin at it (M3).

- **M0 — feasibility probe (done, CDMProbe v0.1–v0.2.2).** `dump` / `skin` /
  `shards` / `secret` / `log` / `casts`. Confirmed the §1 capability map;
  hardened against Secret-Values taint; reports persist to SavedVariables (read
  off disk). Deep-dive source research on item skinning (§1 Skinning specifics)
  and the §5 three-layer config model.

- **M1 — Prototype skin (feasibility, dummy content).** Prove the whole rendering
  stack is buildable on the live client using **placeholder labels / keybinds /
  values that need not line up with the real layout**. The questions M1 answers:
  - Can we `SetDesaturated(true)` + `SetVertexColor` the real `item.Icon` in
    place and make it **persist** across Blizzard's repaints (post-hook
    `RefreshData` / `RefreshLayout`)?
  - Can we draw our own regions over a secure item — monospace 4-letter label,
    keybind text, block-char meter, scanline/vignette overlay — without taint?
  - Can we build a **custom overlay frame** (shard rail) **anchored** to the
    viewer (`SetPoint(..., EssentialCooldownViewer, ...)`) that **rides along**
    when the CDM moves / relayouts?
  Deliverable: a CRT-looking column + rail that *looks* right, wired to fake
  content. If any of these can't be done, the design changes here — that's the
  whole point of doing it first.

- **M2 — Config foundation.** Make it real underneath. Author the per-spec
  **Cooldown Layout string** (system ①, §5) for Demo; **auto-apply** it via
  `CooldownViewerSettings:GetLayoutManager():ImportLayout(str)` (OOC — confirmed
  viable, §7); set **Orientation=Vertical** default (system ②, LibEditModeOverride,
  OOC); confirm anchor-follow against the real tracked set + order. After M2 the
  layout is **fixed and known**, so labels / colours / keybinds / positions have
  a deterministic thing to key to.

- **M3 — First real skin.** Re-point the M1 prototype at the M2 layout: real
  4-letter labels + **real keybinds** (read the binding per tracked spell), the
  §3 group **colour map**, **generator-vs-consumer** batch tint (build→spend axis
  reads preattentively), and the **Demonic Core proc-glow on Demonbolt**
  (`IsShown`). Real shard rail (readable + branchable) with cap glitter + sound.

- **M4 — Burst-window overlay.** Our overlay frames **beside** the vertical CDM
  group **Tyrant · Dreadstalkers · Grimoire: Fel Ravager**; shared lane tint
  (common region) + common-fate brighten when all are up. The **napkin-math
  timer** (§1: player-cast → `GetSpellBaseCooldown` countdown, fixed-CD only)
  drives a salience pop as Tyrant nears ready. This is the horizontal "line
  Tyrant up with what it buffs" grouping — realized in *our* overlay, not the
  CDM's layout.

- **M5 — Borrowed DoT/proc bars.** Restyle the secure BuffBar viewer (Demonic
  Core, Dominion of Argus) to match the skin.

- **M6 — Audio.** Wire the §3 earcon set: our shard-cap + proc-gained, native
  ready / pandemic alerts; LibSharedMedia registration + per-event toggles +
  global mute.

- **M7 — Profile enforcement + second spec + polish.** Choose enforcement-strength
  UX (auto-apply → import-and-verify → nag); prove the pattern on a second spec;
  **cyberpunk-skin stretch** art pass over the block / rail / bar styling.

---

## 7. Open questions / verify-in-game

- [ ] **`/cdmp casts`**: is `UNIT_SPELLCAST_SUCCEEDED`'s spellID readable in
      restricted combat? (decides roll-your-own cooldown timers — Tyrant highlight)
- [ ] Buff-vs-cooldown: can we access the self-buff remaining AND the
      cooldown-to-recast as **two** durations, or only Blizzard's one sequenced
      display? (agent source-checking; e.g. Summon Demonic Tyrant)
- [ ] Pandemic/ready **replacement**: confirm the `PandemicIcon` (and `Available`
      alert / `CooldownFlash`) shown-state is observable so we can hide Blizzard's
      and drive our own arbitrary indicator (offset arrow) — agent + verify-in-game.
- [x] **`SetLayoutData` writability** — RESOLVED (2026-07-17, `/cdmp layout write`,
      out of combat): the call is **permitted from addon code, no blocked-action
      error** → **auto-apply is viable** (program the layout, don't just ask for a
      paste). Two caveats for *how*: (a) `SetLayoutData(str)` replaces the **whole**
      data store (every spec's layouts) — don't clobber; (b) the clean single-layout
      **merge** is `CooldownViewerSettings:GetLayoutManager():ImportLayout(str, info)`
      (what the Import button calls). Follow-up sub-probe: is `ImportLayout`
      addon-callable too? In-combat writability still expected-blocked (untested).
- [x] **Does the export string carry position/orientation?** RESOLVED
      (2026-07-17, source): **NO** — the Cooldown Layout string is only
      `COOLDOWN_ORDER` + `CATEGORY_OVERRIDES` + `ALERT_OVERRIDES`. Orientation /
      size / position are Edit Mode (a *separate* string). Hence the three-layer
      model + anchoring in §5; we do **not** reposition secure CDM frames — we
      anchor our overlay to them and use `LibEditModeOverride` only to set the
      Orientation default out of combat.
- [x] **Alerts in the layout string?** RESOLVED (2026-07-17, source): **YES** —
      `ALERT_OVERRIDES` serializes per-cooldown sound/visual alert config, so
      native alerts ship *inside* the import string (secure, combat-safe). Still
      open: whether an addon can **inject/override** alerts *outside* the string
      programmatically, and whether a custom `.ogg` can substitute a built-in.
- [x] Wild Imp / Demonic Core **count** — RESOLVED: `Applications` count is
      Blizzard-displayed but **secret** to us. For "[X]/4", enlarge Blizzard's X
      and append a static "/4"; we cannot reliably count procs ourselves.
- [ ] Which profile do we standardize on (Kalamazi Demo CDM vs a curated set)?
      Whichever it is, it's authored as the per-spec **Cooldown Layout string**
      (system ①) — export a real one in-game as the baseline.

---

## 8. Provenance

- Research: two agent reports (12.0 addon API under Secret Values; glanceable-UI
  design) — synthesized into §1 and §3.
- Empirical: CDMProbe M0 runs, live 12.0.7, character on Kil'jaeden delve.
- Source (Tier 1): `Gethe/wow-ui-source` @ build **68453** (= live 12.0.7), clone
  at `~/code/github/wow-ui-source` — `Blizzard_CooldownViewer/{CooldownViewer,
  CooldownViewerSettingsDataStoreSerialization}.lua`,
  `Blizzard_APIDocumentationGenerated/EditModeManagerConstantsDocumentation.lua`.
  Grounds the §5 three-layer config model, the serialized-field list, and the
  `RefreshLayout`/anchoring positioning approach.
- Rotation: `knowledge/classes/warlock/demonology/rotation.md` (Diabolist,
  12.0.7; simc MID1 APL + maxroll/Method/Kalamazi).
