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

- **2026-06-19 — Milestone 1 complete (headless sim engine).** Installed the
  Flutter toolchain on WSL2 (git-clone + PATH; bundled Dart 3.12.2). Built
  `projects/trainer/sim/`, a pure-Dart package with **no `package:flutter` import**:
  `tick()`/`advanceBy()`/`cast()`/`canCast()`/`advise()` engine for the
  simplified Affliction model. Fixed-timestep accumulator (`kFixedDt = 1/60`),
  7-step tick order, determinism via an injected `SimRng`
  (Seeded/Always/Never/Scripted), immutable `GameState` snapshots +
  `List<SimEvent>` per tick, enum-keyed identity (`ids.dart`), pandemic
  refresh, shard gen + overcap tracking, GCD/cast/Nightfall-instant/clip,
  and a shared `_validate` behind `cast`/`canCast`. **37 tests green
  (`dart test`), `dart analyze` clean.** Commit `9c37fe6`.
  - Decisions locked during M1: keep real proc probabilities in the model and
    push determinism into the RNG (no fake "every Nth tick"); DoT ticks resolve
    *before* fall-off so a tick landing exactly at expiry still lands;
    `alreadyCasting`/`channeling` are off-GCD/channel-only paths (the M1 roster
    is all on-GCD, so a hard cast in the post-GCD window *clips* rather than
    rejecting — keeping `cast`/`canCast` consistent).
- **2026-06-19 — Milestone 2 complete (minimum playable Flutter shell).** Built
  `projects/trainer/app/` (`rotation_trainer_app`), a Flutter app that `path:`-depends on
  the M1 `rotation_sim` engine and renders it — **no sim logic in widgets**. A
  `GameController` (`ChangeNotifier`) owns the `Engine` + a vsync `Ticker`,
  converts the Ticker's cumulative elapsed into a per-frame delta, and drives
  `engine.tick(dt)`; a single `ListenableBuilder` repaints the tree each frame.
  UI: portrait `TargetPanel` (health placeholder + WoW-style **icon tiles with a
  numeric countdown + radial cooldown sweep** for Agony/Corruption/Haunt),
  `CastBar` (L→R fill, hidden at rest), `ResourceBar` (5 shard pips + Nightfall
  chip), and a thumb-grid `ActionBar` of `AbilityButton`s that dispatch `cast`
  and dim + show a reason badge (GCD/CD/◇) via `canCast`. **6 widget tests green
  (`flutter test`), `flutter analyze` clean, `flutter build web` succeeds.**
  - Decisions locked during M2: **run target = Flutter web** — `flutter run -d
    web-server --web-port 8080` + open `localhost` in the Windows browser
    (`winbrowser`), mirroring the repo's Vite workflow (verified serving HTTP
    200). Plain `path:` dep over a pub workspace. Timers render as WoW-style
    icon tiles (placeholder letter faces; real Blizzard icon art is a one-line
    `Image.network` swap in M5). Code kept target-agnostic (no `dart:io`/`html`,
    no plugins) so a later Pixel 6 build is a `-d` flag + Android setup.
  - **Rendering-backend caveat:** web renders with **Skia/CanvasKit**; a modern
    Pixel 6 build uses **Impeller** (no Skia) — verified against the local
    `~/flutter` repo. Visually equivalent for M2's primitives, but reserve final
    judgment on smoothness/feel (and haptics/touch ergonomics) for a device build.
- **2026-06-19 — Milestone 3 complete (JSON template loader).** The roster is
  now **data, not code**. Added `projects/trainer/sim/lib/src/template_loader.dart`, a
  **pure-Dart** `loadTemplate(String) → SimConfig` (imports only `dart:convert` +
  the engine's data layer — no `package:flutter`/`dart:io`, so it tests under
  `dart test`). It is the **single seam** `ids.dart` anticipated: the wire-format
  spellings (`"ua"`, `"shadowbolt"`) live in private string→enum maps here, never
  in the engine core. Two-phase parse — (1) build the four collections with typed
  path-tagging accessors, (2) cross-check every id reference against the parsed
  collections (catches e.g. "consumes nightfall but no nightfall aura defined").
  Fail-fast `TemplateException` (path-tagged), lenient on unknown extra keys
  (`icon`/`display`/`spec`/…), strict on required+typed values, all id refs, and
  ranges (`min<=max`, `startAt∈[min,max]`, probabilities∈[0,1], non-negative
  durations, `maxStacks>=1`, no dup ids, priority⊆abilities). `num`-tolerant
  doubles (JSON `2` and `2.0`). Canonical template bundled at
  `projects/trainer/app/assets/templates/affliction_simple.json`; `main()` is now async —
  `rootBundle.loadString` → `loadTemplate` → `RotationTrainerApp(config:)`, wrapped
  **debug-loud / release-fallback** (rethrow in `kDebugMode`, else fall back to
  `afflictionSimplified()`). The JSON reproduces `afflictionSimplified()`
  **field-for-field** (verified by a no-value-equality field-by-field helper) and
  editing it changes the rotation with no code change. **Loader: 21 tests green
  (`dart test`, total 58 in `projects/trainer/sim`); app: 8 tests green (`flutter test`,
  the 6 M2 widget tests untouched + asset-fidelity + boot smoke); both analyze
  clean.**
  - Decisions locked during M3: string→enum tables live in the loader (the
    "single seam"), not `ids.dart`; one canonical JSON under `app/assets/`
    (Flutter's bundler rejects `../sim/...` — no copies, no drift); no
    value-equality on the engine structs (a field-by-field test helper instead);
    no `TemplateMeta` yet (`icon`/`display`/`spec`/`class`/`patch` ignored — icons
    are M5); `tickDamage` + the `onTick` tagged union added to the draft schema so
    the doc stays honest. **Gotcha:** `rootBundle.loadString` inside `testWidgets`
    hangs (fake-async zone never resolves real I/O) — load it via
    `tester.runAsync(...)`; a plain `test` is fine.
- **2026-07-09 — Milestone 4 complete (practice feedback).** The trainer now
  *coaches*. Two features, both driven off signals the engine already emitted.
  **(1) Next-ability hint glow** — `GameController.advised` surfaces
  `engine.advise()`; `AbilityButton` sets the (already-implemented) amber
  `IconCountdownTile.glow` when `showHints && advised == id && enabled` (never
  highlights a dimmed tile). A lightbulb toggle in the new `ControlBar` flips
  `showHints` for recall testing. **(2) End-of-pull summary** — a new
  `SessionStats` value type (`sim/lib/src/stats.dart`) holds the raw
  accumulators + pure derived getters (`dpsEquivalent`, `uptimeFraction`,
  `wastedGcds`, and a **placeholder** composite `grade` 0–100 + `letter`), and
  `SummaryPanel` overlays the frozen board with grade/DPS-equiv/per-DoT
  uptime/wasted-GCDs/overcap/clips + a **Practice again** button. All stat math
  **and** the pull lifecycle live in the engine (headless-testable): a fixed
  **60s pull** (`Engine(pullSeconds:)`) with a boundary clamp that snaps
  `_now` onto `_endsAt` so `elapsed == pullSeconds` holds under `==`, plus
  `stop()` (early end), `reset()` (genuine fresh start — clears the live
  aura/debuff/cooldown maps + cast + accumulators, reseeds resources), and
  `isEnded`/`stats` reads. `game_screen.dart` gains a live countdown + DPS-equiv
  readout and mounts the `ControlBar` + summary `Stack`. **Sim: 71 tests green
  (`dart test`, +13 in `stats_test.dart`); app: 13 tests green (`flutter test`,
  +5 for glow/toggle/summary/stop/reset); both analyze clean; web build
  compiles.**
  - Decisions locked during M4: **fixed-length pull** (default 60s, countdown,
    auto-summary at 0, Stop to end early, Reset to restart) over an open-ended
    dummy; headline is a **composite 0–100 grade + letter** above the
    DPS-equiv + discrete stats. Grade **weights** (`kWDot/kWOvercap/kWClip/
    kWGcd`) and `pullSeconds` are **intentional placeholder consts** — balance
    is M5. The uptime map is seeded with **all** config debuffs (defaulting 0)
    so a never-applied DoT is still graded/rendered; Haunt is a CD-gated amp
    that can't hit 100% uptime over a long pull, so grading it against full
    uptime is a known imperfection while `W_dot` is a placeholder. Uptime
    accrues at whole-`dt` (≤16.7 ms) granularity. **Gotcha:** the 60s cap froze
    the pre-existing `shard_generation` statistical smoke (it needs ~2000s of
    ticks) — gave that one test `pullSeconds: double.infinity` via a new
    `ScriptedSession` param.
- *Next: Milestone 5 — Affliction fidelity + polish (real icon art, tuned
  numbers/weights, Nightfall proc-glow, Drain Soul channel + Darkglare window).*

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
    { "id": "corruption", "name": "Corruption", "icon": "spell_shadow_abominationexplosion",
      "castTime": 0, "onGcd": true,
      "applies": { "debuff": "corruption" } },
    { "id": "shadowbolt", "name": "Shadow Bolt", "icon": "spell_shadow_shadowbolt",
      "castTime": 2.0, "onGcd": true,
      "instantIfAura": "nightfall", "consumesAura": "nightfall",
      "effect": { "damage": 100 } },
    { "id": "ua", "name": "Unstable Affliction", "icon": "spell_shadow_unstableaffliction_3",
      "castTime": 0, "onGcd": true,
      "cost": { "soulShard": 1 }, "effect": { "damage": 220 } },
    { "id": "haunt", "name": "Haunt", "icon": "ability_warlock_haunt",
      "castTime": 1.5, "onGcd": true, "cooldown": 15,
      "applies": { "debuff": "haunt" }, "effect": { "damage": 80 } }
  ],
  "debuffs": [
    { "id": "agony",  "name": "Agony", "duration": 18, "tickInterval": 2,
      "pandemic": 0.3, "tickDamage": 10,
      "onTick": { "chance": 0.5, "generates": { "soulShard": 1 } } },
    { "id": "corruption", "name": "Corruption", "duration": 14, "tickInterval": 2,
      "pandemic": 0.3, "tickDamage": 8,
      "onTick": { "chance": 0.15, "grantsAura": "nightfall" } },
    { "id": "haunt", "name": "Haunt", "duration": 8, "damageAmp": 0.10 }
  ],
  "auras": [
    { "id": "nightfall", "name": "Nightfall", "duration": 12, "maxStacks": 2 }
  ],
  "priority": ["agony", "corruption", "haunt", "ua", "shadowbolt"]
}
```
`onTick` is a **tagged union**: exactly one of `generates: { <resource>: N }`
(per-tick resource gen) or `grantsAura: "<aura>"` (per-tick proc), gated by
`chance` in `[0,1]`. `tickDamage` is the per-tick damage of a DoT (M3 addition to
the draft). The M3 loader (`projects/trainer/sim/lib/src/template_loader.dart`) parses this
shape into `SimConfig` byte-for-byte against `afflictionSimplified()`; the canonical
file is bundled at `projects/trainer/app/assets/templates/affliction_simple.json`.
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
projects/trainer/                         # new Flutter app
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
Lives in its own folder under `projects/trainer/` (alongside the other companion
apps), since it's a separate Flutter toolchain. Shares *data* (icons/spell ids)
with the talent calculator,
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
