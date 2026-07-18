# Cooldown HUD — guiding spec (vision & design language)

> The non-technical **what & why**: how it should feel, look, and behave.
> Sibling docs carry the rest — read them for anything technical or scheduled.
>
> **Doc map (§ cross-refs):** §0 Direction + §3 Design language → **this doc** ·
> §1–§2, §4–§5, §9 (Secret-Values findings / architecture / provenance) →
> `notes.md` · §6 Milestones + §7 Open questions → `milestones.md`.

## Elevator pitch

A spec-specific **overlay that enhances Blizzard's built-in Cooldown Manager**
(Midnight 12.0), authored against an imported cooldown-settings profile. The
idea: **vertical space encodes priority, horizontal space encodes grouping**
(line a burst cooldown up with what it buffs) — realized as a **vertical CDM
column with our overlay frames beside it**. We **keep Blizzard's icons and
recolor them in place** (desaturate + tint), add short labels + keybinds, live
resource counters, timing/decay cues, "juice" (glitter) when a resource caps,
and audio cues from a learnable library. Decluttering is the game: an **empty
board = nothing to do**.

**v1 target spec: Demonology Warlock.** Prototype/probe addon: `michac/CDMProbe`
(checked out at `addon/`, gitignored from the workspace). These docs are the
source of truth for the design; the addon is the source of truth for the code.

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

## 3. Design language

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
luminance pop, independent of the identity hue. *(Implementation caveat from the
M1 build: because we now own the icon's color on every repaint path, "on
cooldown" desaturation is ours to re-encode — see notes.md §9.)*

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
