# Rotation Trainer — mobile spec

Status: **planning** · Owner: Michael · Created: 2026-06-19

A phone game that simulates standing at a **target dummy** practicing a WoW
spec's rotation — except the keybinds are virtual buttons under your thumbs.
Load a class template, see ability buttons + a cast bar + your resource bar +
the target's debuffs, and drill the priority until it's muscle memory. Built
for a **Pixel 6** but cross-platform by construction (one Flutter codebase →
Android now, iOS/desktop/web later).

Scope tracks the repo: **Retail / Midnight (12.0.x)** only. The first slice is
**Affliction Warlock, simplified** — it exercises a resource (Soul Shards), a
hard-cast filler (the cast bar), and target DoTs (debuff tracking) in one spec,
and this repo already carries Affliction KB + spell data to draw on.

## Progress log

- *(none yet — this is the initial spec)*

## Decisions (locked)

| Axis | Choice | Why |
|------|--------|-----|
| Engine/UI | **Flutter (Dart)** | One codebase → native Android (Pixel 6) plus iOS/desktop/web later. 120 Hz-capable, real haptics, custom-painted bars/cooldown sweeps without DOM cost. Honors "cool if not platform-locked." |
| Architecture | **Headless sim core + thin UI** | Pure-Dart rotation engine (no Flutter imports) that ticks game state; widgets only render + dispatch input. Keeps the hard logic unit-testable and lets a future web/desktop shell reuse it verbatim. |
| Class data | **Data-driven templates (JSON)** | A spec = a JSON document (abilities, resources, DoTs, procs, priority). New specs are data, not code. Authored by hand for the prototype; later derivable from this repo's `talents.json` + Stage-A spell enrichment. |
| First spec | **Affliction Warlock (simplified)** | Covers shards + cast bar + DoTs in one. Faithful *shape*, trimmed *content* (see "Simplified Affliction" below). |
| Input model | **Thumb-reachable button grid, portrait** | Phone held upright, both thumbs on a bottom action bar; status (cast bar, resources, debuffs) up top out from under the thumbs. |
| Time base | **Fixed-timestep sim, `Ticker`-driven** | Deterministic 60–120 Hz fixed update decoupled from render; makes GCD/cast/tick math exact and replayable in tests. |

### What "simplified" means (prototype, not shipped balance)
Faithful enough that the muscle memory transfers; trimmed enough to nail the
engine + UI first. Numbers are **placeholders**, not sim-accurate — balance is
explicitly out of scope until the engine is proven.

## Goals / non-goals

**Goals**
- **Feel like the game**: GCD, cast/channel times, resource gen/spend, DoT
  durations + refresh (pandemic) all behave like Retail so the practice carries.
- **Snappy + tactile**: <1 frame button→repaint; haptic tick on cast/GCD/proc.
- **One-handed-friendly portrait** UI sized for a Pixel 6 (≈6.4", 1080×2400).
- **Teach, don't just simulate**: optional "next ability" highlight (Hekili-style)
  + post-pull feedback (uptime %, wasted GCDs, overcapped resource).
- **Data-driven**: adding a spec = authoring a template, no engine changes.

**Non-goals (prototype)**
- Sim-accurate damage / stat scaling / gear / haste breakpoints.
- Multiplayer, accounts, leaderboards, cloud saves.
- Movement, boss mechanics, multiple enemies (single dummy only).
- Talent selection UI (that's the *other* todo — the talent calculator). A
  template here is one fixed build; later it can *import* a calculator loadout.
- Classic / pre-Midnight specs.

## Architecture overview

```
class template JSON  (abilities, resources, dots, procs, priority)
        │  load + validate
        ▼
┌─────────────────────────────────────────────┐
│  sim core  (pure Dart, no Flutter)           │
│   GameState { time, gcdEnds, cast?, ... }    │
│   ├─ resources:  Map<id, Resource>           │   builder/spender, regen, cap
│   ├─ cooldowns:  Map<abilityId, CdState>     │   charges, recovery
│   ├─ playerAuras: Map<id, Aura>              │   procs/buffs (Nightfall…)
│   ├─ targetDebuffs: Map<id, Debuff>          │   DoTs: applied/expires/pandemic
│   ├─ castBar: { ability, startedAt, ends }   │   cast + channel
│   └─ tick(dt): advance time, expire, regen,  │
│                tick DoTs, resolve cast,       │
│                emit DamageEvent / FloatText   │
│   advise(): next-ability per priority list   │   (practice hint)
│   cast(abilityId): validate → start/execute  │
└─────────────────────────────────────────────┘
        │ state stream (ChangeNotifier / Riverpod)
        ▼
Flutter widgets  (render-only)
   ├─ TargetPanel   — health, debuff icons w/ duration sweep + stack count
   ├─ CastBar       — fills L→R, channel ticks, interrupt/clip feedback
   ├─ ResourceBar   — shard pips (0–5) / generic bar; proc glow
   ├─ PlayerAuras   — buff/proc icons (Nightfall stacks…)
   ├─ ActionBar     — thumb grid of AbilityButtons (cd sweep, charges, ready glow)
   └─ Readout       — DPS-ish score, timer, "next" hint, end-of-pull summary
```

The split is the load-bearing decision: **the sim core never imports Flutter**.
It advances on a fixed timestep and exposes immutable snapshots; the UI is a
pure function of the latest snapshot plus an input dispatcher. That keeps the
rotation rules in fast unit tests and lets a later web/desktop build reuse them.

## Simulation engine (the hard part)

Fixed-timestep loop (accumulator over Flutter's `Ticker`), default dt = 1/60 s.
Each tick, in order:
1. **Advance clock**; resolve an in-progress **cast/channel** if it completed
   (apply its effect — damage, apply DoT, gain/spend resource, grant aura).
2. **Channels**: tick on their cadence (e.g. Drain Soul every N ms) while held.
3. **Expire** auras + debuffs whose `expires <= now` (fire "DoT fell off" event).
4. **DoT ticks**: each active debuff ticks on its interval → damage (+ side
   effects, e.g. Agony tick rolls a Soul Shard fragment).
5. **Regen** resources (energy/focus/mana style) toward cap; clamp; flag overcap.
6. **GCD**: track `gcdEnds`; most buttons are gated by it (off-GCD abilities flagged).
7. **Procs**: evaluate proc triggers (e.g. Corruption tick → Nightfall stack).

`cast(abilityId)` validation gates, surfaced to the UI as *why* a button is dim:
- GCD active (unless ability is off-GCD)
- already casting (or a channel in progress)
- on cooldown / no charge available
- insufficient resource (or, for spenders, resource == 0)
- — instant abilities resolve immediately; cast-time abilities start the CastBar
  and resolve on completion; **moving/recast clips** the cast (teachable mistake).

Sub-systems each spec template can use:
- **Resources** — `{ id, min, max, startAt, regenPerSec? }`; discrete (shard pips)
  or continuous (energy bar). Generators add, spenders subtract, both flag waste.
- **DoTs / debuffs** — `{ duration, tickInterval, pandemic: 0.3 }`. Refresh within
  the pandemic window extends instead of clipping (the real refresh rule, a key
  thing to practice). Track per-DoT remaining for the duration sweep ring.
- **Cooldowns + charges** — recovery time, charge count, charge-refill.
- **Player auras / procs** — stacks, duration, "empowers next X" semantics.
- **Channels** — held casts that tick and can be re-started by a proc mid-channel.

### Simplified Affliction (first template)
Trim the live priority (`knowledge/classes/warlock/affliction/rotation.md`) to a
recognizable core. Soul Shards 0–5.

| Button | Type | Effect (placeholder numbers) |
|--------|------|------------------------------|
| **Agony** | instant, DoT | applies/refreshes Agony (18 s, ticks ~2 s); each tick has a chance to generate 1 shard |
| **Corruption** | instant, DoT | applies/refreshes Corruption (14 s); ticks can grant a **Nightfall** proc |
| **Shadow Bolt** | 2.0 s cast (filler) | damage; the cast-bar workhorse. *Nightfall* makes the next one instant |
| **Unstable Affliction** | instant, spender | costs 1 shard; the primary shard dump |
| **Haunt** | 1.5 s cast, cooldown | applies Haunt debuff (damage amp), short CD — second tracked debuff + a cooldown to weave |

Priority hint (`advise()`): keep Agony up → keep Corruption up → Haunt on CD →
spend shards on Unstable Affliction at high shards → Shadow Bolt filler (instant
if Nightfall). Deferred to later milestones: Drain Soul channel, Darkglare/Dark
Harvest burst window, Shard Instability, multi-DoT/AoE. Faithful shape; the deep
mechanics layer in once the engine holds.

## UI / layout (portrait, Pixel 6)

```
┌───────────────────────────────┐
│  Target dummy  ❤▓▓▓▓░  60%     │  TargetPanel: health + tracked debuffs
│   [Agony 12s②][Corr 9s][Haunt] │  icons w/ shrinking duration ring + stacks
├───────────────────────────────┤
│  ▓▓▓▓▓▓▓▓░░░  Shadow Bolt 0.7s │  CastBar (hidden when not casting)
├───────────────────────────────┤
│  Shards ◆◆◆◆◇   [Nightfall ②]  │  ResourceBar (pips) + player procs
│                                │
│         DPS 4.2k · 0:18        │  Readout / score / timer
│                                │
│        (next: Agony ►)         │  practice hint glow on the button
├───────────────────────────────┤
│   ┌────┐ ┌────┐ ┌────┐         │
│   │Agon│ │Corr│ │Haun│         │  ActionBar — thumb grid, bottom third
│   └────┘ └────┘ └────┘         │  big touch targets, cd sweep, charge pips,
│   ┌────┐ ┌────┐                │  ready-glow, dim+reason when unusable
│   │ SB │ │ UA │                │
│   └────┘ └────┘                │
└───────────────────────────────┘
```
- Buttons ≥ 56 dp, spaced for thumbs; bottom-anchored so they sit under a
  natural grip. Status (cast/resource/debuff) lives up top, away from thumbs.
- Haptic + subtle flash on: GCD ready, proc gained, DoT about to expire,
  clipped cast (negative feedback). Optional sound later.
- Cooldown sweep + numeric timer on each button; charges as corner pips.

## Class-template schema (draft)

```jsonc
{
  "id": "warlock-affliction-simple",
  "name": "Affliction Warlock (simplified)",
  "spec": "affliction", "class": "warlock",
  "patch": "12.0.7",
  "gcd": 1.5,
  "resources": [
    { "id": "soulShard", "min": 0, "max": 5, "startAt": 3, "display": "pips" }
  ],
  "abilities": [
    { "id": "agony", "name": "Agony", "icon": "spell_shadow_curseofsargeras",
      "castTime": 0, "onGcd": true,
      "applies": { "debuff": "agony" } },
    { "id": "shadowbolt", "name": "Shadow Bolt", "icon": "spell_shadow_shadowbolt",
      "castTime": 2.0, "onGcd": true,
      "instantIfAura": "nightfall", "consumesAura": "nightfall",
      "effect": { "damage": 100, "generates": { "soulShard": 0 } } },
    { "id": "ua", "name": "Unstable Affliction", "icon": "spell_shadow_unstableaffliction_3",
      "castTime": 0, "onGcd": true,
      "cost": { "soulShard": 1 }, "effect": { "damage": 220 } },
    { "id": "haunt", "name": "Haunt", "icon": "ability_warlock_haunt",
      "castTime": 1.5, "onGcd": true, "cooldown": 15,
      "applies": { "debuff": "haunt" } }
  ],
  "debuffs": [
    { "id": "agony",  "name": "Agony", "duration": 18, "tickInterval": 2,
      "pandemic": 0.3, "onTick": { "chance": 0.5, "generates": { "soulShard": 1 } } },
    { "id": "corruption", "name": "Corruption", "duration": 14, "tickInterval": 2,
      "pandemic": 0.3, "onTick": { "chance": 0.15, "grantsAura": "nightfall" } },
    { "id": "haunt", "name": "Haunt", "duration": 8, "damageAmp": 0.10 }
  ],
  "auras": [
    { "id": "nightfall", "name": "Nightfall", "duration": 12, "maxStacks": 2 }
  ],
  "priority": ["agony", "corruption", "haunt", "ua", "shadowbolt"]
}
```
Numbers are placeholders. Icon slugs reuse this repo's Stage-A enrichment
(`app/static/data/.../<spec>.json` carries icon slugs/URLs) so the trainer and
the talent calculator share one icon source. Bundle templates as Flutter assets
for the prototype.

## Feedback / "am I doing it right?"

- **Live hint (toggleable)**: `advise()` highlights the next priority ability —
  training wheels you can switch off to test recall.
- **End-of-pull summary**: DoT uptime %, GCDs used vs available (wasted GCD time),
  resource overcap count, casts clipped, a rough DPS-equivalent score. This is
  the actual "practice" payoff — quantifies the dummy session.

## Repo layout (proposed)

```
trainer/                         # new Flutter app
  lib/
    sim/                         # pure Dart — NO flutter imports
      game_state.dart
      engine.dart                # tick(), cast(), advise()
      template.dart              # JSON model + validation
      resources.dart  dots.dart  cooldowns.dart  auras.dart
    ui/
      action_bar.dart  ability_button.dart  cast_bar.dart
      resource_bar.dart  target_panel.dart  readout.dart
    app.dart  main.dart
  assets/templates/warlock-affliction-simple.json
  assets/icons/                  # or reuse repo Stage-A icon URLs at runtime
  test/sim/                      # engine unit tests (the priority + DoT math)
  pubspec.yaml
```
Lives in its own top-level `trainer/` (parallel to `app/` and `tools/`), since
it's a separate Flutter toolchain. Shares *data* (icons/spell ids) with `app/`,
not code.

## Milestones (vertical slices)

1. **Engine spike (headless).** Pure-Dart `tick()`/`cast()` with one resource,
   one DoT (pandemic refresh), GCD, a cast-time ability. Unit tests assert DoT
   uptime + shard gen over a scripted button sequence. No UI. *Proves the core.*
2. **Minimum playable.** Flutter shell: ActionBar + CastBar + ResourceBar +
   TargetPanel wired to the engine. Tap buttons, see the cast bar fill, shards
   move, two debuff timers tick. Runs on the Pixel 6. *Proves the feel.*
3. **Template loader.** Drive everything from `warlock-affliction-simple.json`;
   validate on load. Swapping the JSON swaps the rotation with no code change.
4. **Practice feedback.** `advise()` next-ability glow + end-of-pull summary
   (uptime, wasted GCDs, overcap, clips, score).
5. **Polish + faithfulness.** Haptics, cooldown sweeps, proc glow (Nightfall),
   charges; tighten Affliction numbers/priority toward the KB rotation. Channel
   support (Drain Soul) + a cooldown window (Darkglare) as stretch.
6. **Second spec.** Author a combo-point or focus template (Assassination /
   Beast Mastery) to prove the data model generalizes. Spec picker.

## Open questions

- **State plumbing** — raw `ChangeNotifier`/`ValueListenable` vs Riverpod vs
  signals. Lean minimal (`ChangeNotifier` + `ListenableBuilder`) for the spike;
  revisit if widget rebuilds get coarse.
- **Icons** — bundle a small set as assets vs fetch Blizzard-media URLs (the
  `app/` Stage-A source) at runtime. Bundling is simpler offline; reuse is DRY.
  Resolve at milestone 2.
- **Damage model fidelity** — pure placeholder vs pull real coefficients later.
  Prototype stays placeholder; "score" is relative, not sim-accurate. Revisit
  only if/when a sim mode is wanted (currently a non-goal).
- **Template authoring source** — hand-authored now; later auto-derive from
  `knowledge/classes/**/talents.json` + a priority distilled from the rotation
  KB. Big lever for "every spec for free," but out of prototype scope.
- **Haste / GCD scaling** — fixed 1.5 s GCD + fixed cast times for the prototype;
  add a haste stat that scales GCD/cast/tick later (it's the same math the
  engine already does, just parameterized).
- **Distribution** — debug-install via `flutter run` to the Pixel 6 for now;
  decide later between a signed APK sideload, Play Store, or a Flutter-web build
  (the cross-platform payoff) for sharing.
```
