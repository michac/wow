# Cooldown HUD — design (vision & design language)

> The non-technical **what & why**: what the product is, how it should look and
> feel, and the design principles the pipeline serves. Spec-agnostic — the
> Demonology instantiation (abilities, burst window, colour members) lives in
> `specs/demonology/`. For *how it's built* read `architecture.md`; for what the
> game allows, `notes.md`; for what's next, `status.md`.

## Elevator pitch

A spec-specific **overlay that enhances Blizzard's built-in Cooldown Manager**
(Midnight 12.0) — more precisely, a **rotation helper wearing a skin**: its job is
to make the *next decision* pop, not to make the CDM prettier. The idea:
**vertical space encodes priority, horizontal space encodes grouping** (line a
burst cooldown up with what it buffs) — realized as a **vertical CDM column with
our overlay frames beside it**. We **leave Blizzard's icons native and untouched**
and build the value-add in the **terminal chrome around them**: keybinds, an owned
resource rail, timing/decay cues, and "juice" when a resource caps. Decluttering is
the game: an **empty board = nothing to do**.

**v1 target spec: Demonology Warlock.** These docs are the source of truth for the
design; the addon (`michac/CDMProbe`, checked out at `addon/`) is the source of
truth for the code.

## Direction — three pillars

1. **Bind to the live layout; don't ship one.** The overlay binds **per item to
   whatever layout is currently active**, keyed by `GetCooldownID()` on the
   `RefreshLayout` hook (`notes.md`) — reorder-safety and missing-spell-skip come
   free from binding-by-ID. The design baseline is the **real DB2-default filtered
   set** (`CooldownSet`/`CooldownSetSpell`), not a curated list. This is the
   anti-WeakAuras: we get determinism from binding-by-ID, not from enforcement.
   *(v1 ships **no CDM profile at all.** A curated layer-① override — a shipped
   Cooldown Layout string — stays possible but is deferred; see `status.md`.)*
2. **Deploy vertically, beside the character** (left or right) — not a bar
   under/over. Priority reads top→bottom. **We never move the CDM frames**: they're
   Edit Mode system frames with manager-owned position, and forcing a move desyncs
   Edit Mode (`notes.md`). The user positions the column once; our overlay anchors
   to the viewer, rides along when it moves, and vanishes cleanly when it's off. v1
   **assumes a vertical orientation**.
3. **The overlay enhances, doesn't replace.** On top of Blizzard's secure widgets:
   an owned **resource rail**, **keybind labels**, **proc-glows** on the buttons a
   proc transforms, and **napkin-math timing cues** as a big cooldown approaches.

## Aesthetic — terminal / TUI, CRT-flavoured

Monospace, scanline/vignette chrome, block-char meters, a compact terminal frame.
Two commitments make it an accessibility gain, not just a look:

- **We don't tint the Blizzard icons.** Desaturating/tinting them measurably **hurt**
  cooldown legibility — the native swipe and countdown both read worse — which
  defeats the point of keeping the icons. v1 leaves them **native and untouched**;
  Blizzard's icon art is a far stronger non-colour signifier than any label we could
  add, and it survives desaturation / CVD / periphery. The tint hooks are kept but
  **dormant** (they'd gate a future optional solid-colour mode).
- **Keybinds stay as small corner chrome.** The 4-letter ability labels an earlier
  direction added are dropped — noise that obscured the swipe.

So the treatment is *of Blizzard's real icon columns*, not an independent UI:
**icons kept, untouched — we own the chrome around them.**

## Design language

### Layout: vertical = priority, horizontal = grouping

The CDM itself is a **vertical column** (Essential, then Utility); the horizontal
affordances — a burst/grouping lane and the resource rail — are **our overlay
frames anchored beside it**, not extra rows inside the CDM. Position reads
top→bottom down the column; grouping reads across our overlay. Every icon is
**Blizzard's, unmodified** — its art, cooldown swipe, countdown text, charges and
native glow all survive. Everything else is ours.

### Priority tiers are role-static, NOT dynamically re-sorted

Because cooldown readiness is secret, tiers are **fixed by role** — which is also
what the glanceability research recommends (stable positions build muscle memory;
never continuously re-sort). Liveness comes from **salience within the fixed
layout**, not from reordering. The concrete tiering for v1 (rail → burst lane →
core spenders → utility) is Demonology-specific: `specs/demonology/notes.md`.

### Encoding: state on luminance, meaning on our accents

- **Readiness = luminance.** *On cooldown* borrows Blizzard's own dimming + secure
  radial swipe + countdown, untouched (we add nothing). *Ready* adds **our accent
  lights** on the surrounding chrome + a one-shot "settle", fired off the observed
  ready edge (`notes.md`). Dim = not actionable — never continuously animate a
  steady state; declutter is the point.
- **Hue rides on our chrome, not the icons.** Since we don't touch the icon art, any
  colour meaning lives on **our** icon-adjacent accents — borders, corner ticks, the
  lane backdrop, the rail. **What v1 actually commits to is `emphasis` (urgency),
  not ability-group hue** — the Guidance contract colours a cue by how urgent the
  press is, and the Renderer owns `emphasis → pixels` (`guidance-contract.json` is
  authoritative). A per-group colour language is a documented non-goal for v1.
- **Resource rail.** A segmented rail for the spec's primary resource, fully ours
  (readable and branchable, unlike most combat state). At cap it reads **"spend or
  waste"** — the cap cue is a *warning, not a trophy*: a cap deliberately converts
  further generation into wasted value, so the one-shot juice leans urgent, not
  celebratory. An in-flight builder cast shows a **ghost "incoming" segment** at the
  head of the rail (the yield is already deterministic mid-cast).
- **Proc-glow on the transformed button.** When a proc transforms a button, glow the
  **transformed** button — driven off the override event that names *which* button
  transformed (`notes.md`), not an inference.
- **Napkin timing cues.** As a fixed-CD burst cooldown approaches, escalate a low-
  salience awareness cue; reserve motion for the single most urgent instant. Timing
  math is deliberately back-of-envelope — see the Napkin honesty rule in
  `architecture.md`. The per-ability tuning is spec-specific.

### The pre-pull affordance

Out of combat the Secret-Values wall is down, so it's the one place we can
legitimately show a queued "press this next" that combat refuses: a short **opener
queue** ghosting the scripted sequence, draining as you pull. It advances by
**matching the ability pressed**, not by slot position, so branch orderings don't
desync it; it dissolves once combat's first burst window closes. Renders as a
left-to-right strip of keybinds above the panel.
