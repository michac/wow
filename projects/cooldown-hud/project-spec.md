# Cooldown HUD — project spec & design doc

A condensed, glanceable cooldown/resource HUD that **skins Blizzard's built-in
Cooldown Manager** (Midnight 12.0). The idea: **vertical space encodes priority,
horizontal space encodes grouping** (line a burst cooldown up with what it
buffs), **no icons — color + position + short labels**, live resource counters,
timing/decay cues, "juice" (glitter) when a resource caps, and audio cues from a
learnable library. Decluttering is the game: an **empty board = nothing to do**.

**v1 target spec: Demonology Warlock.** Prototype/probe addon: `michac/CDMProbe`
(checked out at `addon/`, gitignored from the workspace). This doc is the source
of truth for the design; the addon is the source of truth for the code.

Status: **M0 (feasibility probe) complete** — the capability map below is
confirmed on the live 12.0.7 client (delve, in combat). Next: M1 layout.

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
| Which spells tracked, as bar vs icon | a **shipped profile** (Edit Mode / import string) |

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
| Hide/replace/resize/crop `Icon` texture | ✅ styleable | `SetTexture(nil)`/`SetAlpha`/`SetTexCoord`; post-hook `RefreshData` |
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
concept is about.

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

**Sound sources (M4).** Two tiers, both MIT-clean: (1) **built-in `PlaySound(SOUNDKIT.*)`**
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
(presence). Pick/mix a direction, then M1 implements it.

---

## 5. Architecture

- **Vehicle:** standalone addon `michac/CDMProbe` (MIT), a thin skin over the
  built-in Cooldown Manager. Deployed via ghaddons (GitHub release → install).
- **Skin the icon viewers:** hide `item.Icon`, paint a solid color block +
  4-letter label, leave the secure `item.Cooldown` swipe running over it.
- **Bar viewers:** restyle `item.Bar` on the BuffBar viewer (per-spell color).
- **Layout:** Edit Mode orientation (vertical/horizontal) per viewer +
  `LibEditModeOverride` for scripted positions (out of combat; `SaveChanges` in
  combat, `ApplyChanges` out). Custom overlays (shard rail) are our own frames.
- **Reapply on Blizzard relayout:** low-freq watchdog / hooks.

Reference (read-only): EnhancedCooldownManager (GPL-3.0) — Soul Shard resource
bar + per-spell colored bars. No code copied.

---

## 6. Milestone log

- **M0 — feasibility probe (done, CDMProbe v0.1–v0.2.2).** `dump` / `skin` /
  `shards` / `secret` / `log` / `casts`. Confirmed the capability map above;
  hardened against Secret-Values taint; reports persist to SavedVariables (read
  off disk). Deep-dive source research on item skinning (§1 Skinning specifics).
- **M1 — Essential color-column + shard rail.** Skin Essential vertically as
  color blocks (keep swipe); custom shard rail with cap glitter + sound. Pick a
  design direction from §4.
- **M2 — horizontal burst lane.** Group Tyrant + Dreadstalkers + Grimoire; shared
  lane tint; common-fate brighten when all ready.
- **M3 — borrowed DoT/proc bars.** Restyle the BuffBar viewer (Demonic Core,
  Dominion of Argus) to match; proc-presence highlight on Demonbolt.
- **M4 — audio.** Wire the earcon set: shard-cap (ours) + native ready/pandemic
  alerts; sound library + toggles.
- **M5 — profile + polish.** Ship/import the standardized tracked set; Edit-Mode
  layout persistence; second spec after Demo proves the pattern.

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
- [ ] Does `LibEditModeOverride` reposition the secure CDM item frames cleanly on
      12.0.7, or do we relayout our own overlay frames? (known CDM taint pitfalls)
- [ ] Confirm whether an addon can **inject** alert entries (sound/visual)
      programmatically vs user-only right-click; and whether custom `.ogg` can
      substitute a built-in alert sound.
- [x] Wild Imp / Demonic Core **count** — RESOLVED: `Applications` count is
      Blizzard-displayed but **secret** to us. For "[X]/4", enlarge Blizzard's X
      and append a static "/4"; we cannot reliably count procs ourselves.
- [ ] Which profile do we standardize on (Kalamazi Demo CDM vs a curated set)?

---

## 8. Provenance

- Research: two agent reports (12.0 addon API under Secret Values; glanceable-UI
  design) — synthesized into §1 and §3.
- Empirical: CDMProbe M0 runs, live 12.0.7, character on Kil'jaeden delve.
- Rotation: `knowledge/classes/warlock/demonology/rotation.md` (Diabolist,
  12.0.7; simc MID1 APL + maxroll/Method/Kalamazi).
