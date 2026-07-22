# Cooldown HUD — guiding spec (vision & design language)

> The non-technical **what & why**: how it should feel, look, and behave.
> Sibling docs carry the rest — read them for anything technical or scheduled.
>
> **Doc map (§ cross-refs):** §0 Direction + §3 Design language → **this doc** ·
> §0.5 Guidance model → `guidance-model.md` · §1–§2, §4–§5, §9 (Secret-Values
> findings / architecture / provenance) → `notes.md` · §6 Milestones + §7 Open
> questions → `milestones.md` · superseded work → `notes-archive.md`.

## Elevator pitch

A spec-specific **overlay that enhances Blizzard's built-in Cooldown Manager**
(Midnight 12.0) — more precisely, a **rotation helper wearing a skin**: its job is
to make the *next decision* pop, not to make the CDM prettier (§0.5). The idea:
**vertical space encodes priority, horizontal space encodes grouping** (line a
burst cooldown up with what it buffs) — realized as a **vertical CDM column with
our overlay frames beside it**. We **leave Blizzard's icons native and untouched**
and build the value-add in the **terminal chrome around them**: keybinds, an owned
soul-shard rail, mode chrome, timing/decay cues, "juice" (glitter) when a resource
caps, and audio cues from a learnable library. Decluttering is the game: an
**empty board = nothing to do**.

**What ships is not open-ended.** The committed v1 indicator set — 18 rows tagged
Core / Stretch / Defer per milestone — is `guidance-model.md` **§0.5.8**. That
table is the contract; this doc is how it looks and feels.

**v1 target spec: Demonology Warlock.** Prototype/probe addon: `michac/CDMProbe`
(checked out at `addon/`, gitignored from the workspace). These docs are the
source of truth for the design; the addon is the source of truth for the code.

---

## 0. Direction (sharpened 2026-07-17)

The concept narrows from "a glanceable HUD" to a specific, opinionated product:
**a spec-specific overlay that *enhances* Blizzard's Cooldown Manager, authored
against an imported cooldown-settings profile.** Three pillars:

1. **Bind to the live layout; don't ship one.** *(Revised 2026-07-18 — the M2
   decision reverses the original pillar, which made an imported Cooldown Layout
   string a hard dependency.)* The overlay binds **per item to whatever layout is
   currently active**, keyed by `GetCooldownID()` on the `RefreshLayout` hook
   (`notes.md` §5/§9) — reorder-safety and missing-spell-skip come free from
   binding-by-ID. The design baseline is the **real DB2-default filtered set**
   (`CooldownSet`/`CooldownSetSpell`, spec 266 = set 60), not a curated list.
   `SetLayoutData` *is* addon-writable out of combat (§7), so shipping a curated
   layer-① override stays possible — but it is **M7 territory**, re-opened only if
   the defaults prove insufficient (the noisy 13-spell Utility default is the
   likely trigger). Still the anti-WeakAuras — we just get determinism from
   binding-by-ID instead of from enforcement.
2. **Deploy vertically, beside the character** (left or right) — not a bar
   under/over. Priority reads top→bottom. **We never move the CDM frames**: they're
   Edit Mode system frames with manager-owned position, and forcing a move desyncs
   Edit Mode (`notes.md` §5). The user positions the column once; our overlay
   anchors to the viewer, rides along when it moves, and vanishes cleanly when it's
   off. v1 **assumes a vertical orientation** rather than staying
   orientation-agnostic.
3. **The overlay enhances, doesn't replace.** On top of Blizzard's secure widgets:
   an owned **soul-shard rail**, **mode chrome** that reads generate-vs-spend
   preattentively, **keybind labels**, **proc-glows** on the buttons a proc
   transforms, and **napkin-math timing cues** (§1) as a big cooldown approaches.
   The full list with verdicts is §0.5.8. **Stretch:** a cyberpunk skin (M7).

Everything below still holds; where the original "2D board" assumed a single grid
*under* the character, the **horizontal grouping** (burst lane) now lives in *our*
overlay frames beside a **vertical** CDM, not in the CDM's own layout.

**Chosen v1 aesthetic: terminal / TUI, CRT-flavoured.** *(Originally "CRT /
green-phosphor", 2026-07-17 — `notes.md` §4; **revised 2026-07-19** after looking
at the M1 prototype in anger. See the M3 note in `milestones.md` §6.)* Two things
changed:

- **The hard green-monochrome constraint is relaxed.** Colour may carry meaning
  again — group, mode, readiness — which the §3 colour language and the mode spine
  both need. The *feel* is unchanged: monospace, scanline/vignette chrome,
  block-char meters, the compact `DEMONOLOGY.SYS` terminal frame.
- **We no longer tint the Blizzard icons.** Desaturating + green-tinting them
  measurably **hurt** cooldown legibility — the native swipe and countdown both
  read worse — which defeats the entire point of keeping the icons. v1 leaves them
  **native and untouched**; the leaf-method tint hooks (`notes.md` §9) go
  **dormant** (kept, not deleted — they gate a future optional solid-colour mode).
  The **4-letter ability labels are dropped** with them: noise that obscured the
  swipe and countdown, and only paid off in a solid-colour skin. Keybinds stay as
  small corner chrome.

So the treatment is still *of Blizzard's real icon columns*, not an independent
UI — but "no icons" from the original vision is now retired in favour of
"**icons kept, untouched — we own the chrome around them**."

> **The overlay is a rotation helper, not just a skin (§0.5).** *What* to signal,
> *when*, and *how* — the ranked salience moments, the generate/spend/burst mode
> model, and the moment→readable-signal map that the M3–M6 widgets implement — live
> in the **guidance model → `guidance-model.md`** (§0.5). This doc stays the vision
> + design language; that doc is the contract the design language serves.

---

## 3. Design language

### Layout sketch (vertical = priority, horizontal = grouping)

```
  ┌ SPEND ─────────────────────────────────┐   ← mode chrome: PREP · GENERATE · SPEND · BURST
  │   shards ▮▮▮▯▯░                         │     (ambient tint + glyph; no motion)
  │                └ ░ = ghost "incoming" segment during an in-flight builder cast
  └────────────────────────────────────────┘
   (the shard rail now stands VERTICAL to the left of the icons — see the
    feedback pass; this sketch predates that move)

   ┌─ burst window ─────────────────┐
   │  [icon] [icon]  ·  [icon]      │   ← Tyrant · Dreadstalkers  =  the go-gate (brighten together)
   └────────────────────────────────┘     Grimoire = brighten-if-up, NEVER a gate (2-min CD)
        [icon]  [icon]✳  [icon] 6/6   ← core spenders: HoG · Demonbolt(✳ = proc-glow) · Implosion
         ⌐q      ⌐e       ⌐r             keybind = small corner chrome; "6/6" = borrowed imp
                                          stack text + our static "/6"

   Demonic Core ▬▬▬2      Dominion ▬▬    ← BORROWED secure bars, restyled (Stretch, M5)

   [icon] [icon] │ [icon] [icon] [icon] │ [icon]   ← utility: defensive │ CC │ mobility
```

Every `[icon]` is **Blizzard's, unmodified** — its art, cooldown swipe, countdown
text, charges and native glow all survive. Everything else in the sketch is ours.

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
- **Tier 1 — burst lane:** Tyrant + Dreadstalkers + the tracked Grimoire summon,
  aligned horizontally. Shared lane tint (common region) so "the window" reads as
  one object. **The go-gate is Tyrant + Dreadstalkers only** — those two brighten
  together (common-fate) to mean "go." The **Grimoire brightens if it's up but is
  never part of the gate**: it's a ~2-min cooldown, absent from roughly half the
  windows (21 Grimoire casts vs 48 Tyrant across the top parses), so gating on it
  would suppress the cue for half the burst windows. *(Corrected 2026-07-19 —
  §0.5.8.6 blocking error #2.)*
- **Tier 2 — core spenders:** Hand of Gul'dan, Demonbolt, Implosion.
- **Tier 3 — utility:** defensives / CC / mobility, sub-grouped horizontally.

### Colour language (grayscale-legible, redundant)

Hue carries **group**, not per-ability identity (stays inside the ~7-color
categorical ceiling). Reuse WoW school associations.

**Where the hue lives (revised 2026-07-19).** Since we no longer touch the icon
art, the group colour and the generator-vs-consumer batch tint ride on **our
icon-adjacent accents** — borders, corner ticks, the burst-lane backdrop, the rail
and mode chrome — not on the icons themselves. The build→spend axis still reads
preattentively; it just reads off the frame instead of the fill.

**Identity = colour(group) × position × native icon art.** *(Was `× 4-letter
label`; the label leg was dropped with the icon tint.)* This is not a loss of
[X1] redundancy — it's an upgrade: Blizzard's icon art is a far stronger
non-colour signifier than a 4-letter abbreviation, it's the one every player
already knows, and it survives desaturation / CVD / periphery at least as well.
Leaving the icons untouched is therefore an **accessibility gain**, not just a
legibility one — which is a large part of why the tint was dropped.

| Group | Hue | Members |
| --- | --- | --- |
| Summon-demon (burst) | fel green | Tyrant, Dreadstalkers, the tracked Grimoire summon *(Doomguard removed — neither tracked nor cast in the modern build)* |
| Core shadow damage | shadow violet | Hand of Gul'dan, Demonbolt, Shadow/Infernal Bolt |
| Fel explosion | bright lime | Implosion |
| Proc / resource | arcane cyan | Demonic Core, Soul Shard rail accent |
| Defensive | blue | Unending Resolve, Dark Pact |
| CC | muted slate | Shadowfury, Axe Toss, Mortal Coil |
| Mobility | gold | Demonic Circle |

Saturation/luminance encode **state, not identity**: dim = on cooldown / not
ready; bright = ready/actionable. That makes "readiness" a preattentive luminance
pop, independent of the identity hue.

*(Revised 2026-07-19: the M1-era caveat — "we own the icon's colour on every
repaint path, so on-cooldown desaturation is ours to re-encode" (`notes.md` §9) —
**no longer applies**. With the icons left native, Blizzard's own on-cooldown
dimming and swipe are preserved for free, and that open design decision
**dissolves**: we don't own that pixel any more. We *add* a ready accent off the
observed ready edge, and we own the recede.)*

### Encoding rules per state

| State | Encoding | Source |
| --- | --- | --- |
| On cooldown | Blizzard's own dimming + secure radial swipe + countdown, untouched | **borrowed** (we add nothing) |
| Ready | our **accent lights** on the surrounding chrome + a one-shot "settle", fired off the observed ready edge (**`TriggerAlertEvent`** — *not* `OnCooldownDone`, which cannot be hooked; `notes.md` §1) | ours (accent) + native ready sound |
| Shards 0–5 | segmented rail fills; at 5 → luminance flip + one-shot glitter + earcon, read as **"spend or waste"** (see below) | **ours** |
| Shard incoming (cast in flight) | **ghost segment** at the head of the rail (+1 SB / +3 Infernal Bolt / +2 Demonbolt) | **ours** (anticipation) |
| Mode (PREP/GENERATE/SPEND/BURST) | ambient chrome tint + luminance + a redundant glyph; **no motion**, positions locked | **ours** |
| Demonic Core proc up | Demonbolt proc-glow overlay; **softens at ≥4 shards** (its +2 would overcap) | **ours** (aura **edge** via `TriggerAlertEvent`; `IsShown` is only a capability-checked backstop) |
| Demonic Art armed | proc-glow the **transformed** button (HoG→Ruination; **SB→Infernal Bolt is unglowable in v1** — SB isn't tracked, §0.5.5) | **ours** (`COOLDOWN_VIEWER_SPELL_OVERRIDE_UPDATED` — the override event names *which* button transformed) |
| Wild Imps present | borrowed stack-count text, enlarged, + our static **"/6"** | borrowed (count) + ours (denominator) |
| Tyrant approaching | ~15 s **warm-up tint** (awareness only) → ~5 s **HOLD/BANK** treatment → motion onset at ~0 | **ours** (napkin) |
| DoT/proc time + stacks | restyled secure bar, drains toward empty | borrowed |
| Pandemic / refresh window | native visual + sound alert | borrowed (right-click CDM alert) |
| Not actionable | recede (dim) — never continuously animate a steady state | ours |

**Shard cap is a warning, not a trophy** ([B1]). A cap deliberately converts
further generation into wasted value, so the cue must read **"spend or waste"**,
not "full!". The glitter stays — it's the one-shot motion onset that earns the
eye — but the colour and the earcon lean *urgent*, not celebratory. This is a
deliberate correction of the earlier "→ gold + glitter" framing.

### The mode spine and the three cross-cutting dimensions

Three behaviours in §0.5.8.2 aren't single widgets — several indicators inherit
them, so they need a design-language treatment of their own.

**(a) Mode chrome — the spine.** One ambient state that frames every finer cue:
**PREP** (out of combat — calm, its own fourth resting state, *not* GENERATE) ·
**GENERATE** (cool/dim) · **SPEND** (active) · **BURST** (hot/bright). Carried as a
preattentive colour + luminance shift on the chrome ([M1], and Blizzard's own CDM
already encodes phase this way — [M2]), plus a redundant glyph so it isn't
colour-alone ([X1]). Steady-state: **no motion**, and element positions never move
between phases ([V7]).

**(b) The pre-pull affordance — be richest when we're allowed to be.** Out of
combat the Secret-Values wall is down, so PREP is the one place we can legitimately
show a queued "press this next" that [R3] refuses in combat: a short **opener
queue** ghosting the scripted sequence, draining as you pull. It advances by
**matching the ability pressed**, not by slot position, so the opener's branch
orderings don't desync it; it dissolves when the first Tyrant window closes. It
renders as a **left-to-right strip of keybinds above the panel**. (The opener
enters combat shard-poor off a pre-pull demon setup, where the board, not the
shard bar, is what's full — so no "bank to N" fill-to marker applies.)

**(c) The anticipation layer — spend cast-time saying what's coming.** While a
builder is in flight its yield is already deterministic, so we show it early: a
**ghost segment** at the head of the rail, and if that ghost would cross the spend
threshold, the chrome **pre-warms toward SPEND** — so the flip has already happened
by the time the cast lands, instead of a beat late.

**(d) Escalating telegraph — one napkin engine, three consumers.** Tyrant (60 s,
our sturdiest clock), Dreadstalkers (~20 s), Implosion (15 s). Juice escalates with
urgency and never maxes out ([J1]); motion is reserved for the single most urgent
instant ([V4]). Two leads matter and must not be conflated:

- **~15 s — warm-up: awareness only, non-instructional.** A low-salience "Tyrant
  approaching" glow. It does **not** tell you to stop dumping, and it never
  overrides the P0 overcap cue.
- **~5 s (≤2 GCDs) — HOLD/BANK: instructional.** *Now* the rail says "hold for
  Tyrant" and the lane crescendos into the go-gate. This window is short on
  purpose: a 15 s freeze force-overcaps (Cores proc ~every 3.6 s, Demonbolt refunds
  +2), so a long hold actively makes you play worse.

The Dreadstalkers approach ping **suppresses when Tyrant is imminent** — one
Dreadstalkers per cycle is held so the dogs are fresh *inside* the window — and
becomes a "stage for Tyrant" treatment instead. Awareness cues may be imprecise;
**instructional cues must be correct**, because they tell the player to stop doing
the otherwise-right thing.

### Audio spec (~6 earcons, timbre-distinct, short/soft) — **Stretch (M6)**

> Per §0.5.8.5-D the whole audio layer is **Stretch**: only the **shard-cap
> earcon** is near-essential (it pairs with our P0 anchor). Everything else is
> native or nice-to-have, and the layer is cuttable without shame.

| Event | Sound | Ours / native |
| --- | --- | --- |
| Soul Shards cap (5) | urgent rising tick — **"spend or waste"**, not a fanfare ([B1]) | **ours** (shards readable) |
| Summon Demonic Tyrant ready | low resonant "gong" | native ready alert |
| Call Dreadstalkers ready | mid double-tick | native ready alert |
| Demonic Core proc gained | soft cyan "ding" | **native `OnAuraApplied` alert** (secure) — or ours off the `TriggerAlertEvent` aura edge |
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

### The shipped profile — **none (revised 2026-07-18)**

v1 ships **no CDM profile at all.** The original plan standardized on one tracked
set (candidate: Kalamazi "Demonology CDM") so the colour/priority map would be
deterministic; the M2 decision replaced that with **binding per item by
`GetCooldownID()` to the active layout**, which buys the same determinism without
asking the user to import anything.

- **Design baseline** = the real DB2-default filtered set
  (`CooldownSet`/`CooldownSetSpell`, spec 266 = set 60).
- **Absent spells are skipped** and reorders are safe, for free, from
  binding-by-ID.
- **Re-open condition:** if the defaults prove insufficient — the noisy 13-spell
  Utility default is the likely trigger, and the predictive Diabolic Ritual tracker
  (§0.5.8 #18) *needs* the per-stage auras added — this returns as a curated
  **layer-① Cooldown Layout string** in **M7**, where enforcement strength
  (auto-apply → import-and-verify → nag) becomes the UX question.
