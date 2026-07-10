/// Public API surface for the headless rotation sim engine.
///
/// Milestone 1 (headless): this barrel is the only import M2's Flutter UI
/// needs. Nothing here imports `package:flutter` — the engine is a pure
/// function of injected config + RNG that exposes immutable [GameState]
/// snapshots and a list of [SimEvent]s per tick.
library;

export 'src/abilities.dart';
export 'src/auras.dart';
export 'src/cast.dart';
export 'src/cast_result.dart';
export 'src/cooldowns.dart';
export 'src/debuffs.dart';
export 'src/engine.dart';
export 'src/events.dart';
export 'src/game_state.dart';
export 'src/ids.dart';
export 'src/resources.dart';
export 'src/rng.dart';
export 'src/stats.dart';
export 'src/template_loader.dart';
