import 'package:rotation_sim/sim.dart';

/// A readable test harness that reads like a button log:
///
/// ```dart
/// ScriptedSession(rng: AlwaysRng())
///   ..press(AbilityId.agony)
///   ..advance(18.0);
/// ```
///
/// [advance] drives the engine one fixed sub-step at a time so it can sample
/// debuff uptime at full resolution, and accumulates every emitted event.
class ScriptedSession {
  ScriptedSession({required SimConfig config, SimRng? rng})
      : engine = Engine(config: config, rng: rng);

  final Engine engine;

  /// All events emitted across the session, in order.
  final List<SimEvent> events = [];

  /// Result of the most recent [press].
  CastResult? lastResult;

  final Map<DebuffId, double> _activeTime = {};
  double _elapsed = 0;

  GameState get state => engine.state;

  /// Press a button (attempt a cast). Records [lastResult].
  ScriptedSession press(AbilityId id) {
    lastResult = engine.cast(id);
    return this;
  }

  /// Advance [seconds] of sim time, sub-step by sub-step, sampling uptime.
  ScriptedSession advance(double seconds) {
    final dt = engine.config.fixedDt;
    final steps = (seconds / dt).round();
    for (var i = 0; i < steps; i++) {
      events.addAll(engine.tick(dt));
      for (final id in DebuffId.values) {
        if (engine.state.debuffActive(id)) {
          _activeTime[id] = (_activeTime[id] ?? 0) + dt;
        }
      }
      _elapsed += dt;
    }
    return this;
  }

  /// Fraction of elapsed time [id] was active (`[0, 1]`).
  double uptime(DebuffId id) =>
      _elapsed == 0 ? 0 : (_activeTime[id] ?? 0) / _elapsed;

  /// All events of a given concrete type, in order.
  List<T> eventsOf<T extends SimEvent>() => events.whereType<T>().toList();

  /// Count of events of a given concrete type.
  int countOf<T extends SimEvent>() => eventsOf<T>().length;
}
