import 'package:flutter/scheduler.dart';
import 'package:flutter/widgets.dart';
import 'package:rotation_sim/sim.dart';

/// The ~20-line adapter between the headless [Engine] and Flutter.
///
/// Owns the [Engine] and a vsync [Ticker]; drives `engine.tick(dt)` once per
/// frame and notifies listeners so a [ListenableBuilder] repaints. Holds **no
/// sim logic** — it only converts the Ticker's cumulative elapsed into a
/// per-frame delta and forwards input.
class GameController extends ChangeNotifier {
  GameController({required TickerProvider vsync, SimConfig? config, SimRng? rng})
      : _engine = Engine(config: config ?? afflictionSimplified(), rng: rng) {
    _ticker = vsync.createTicker(_onTick)..start();
  }

  final Engine _engine;
  late final Ticker _ticker;
  Duration _lastElapsed = Duration.zero;

  /// Current immutable snapshot.
  GameState get state => _engine.state;

  /// The config in play (for durations, costs, the priority list).
  SimConfig get config => _engine.config;

  /// Dispatch a button press. Never throws; notifies so instant abilities
  /// (and the start of a cast bar) show within the same frame.
  CastResult cast(AbilityId id) {
    final result = _engine.cast(id);
    notifyListeners();
    return result;
  }

  /// Pure predicate mirroring [cast]'s gate — null means castable.
  CastRejectReason? canCast(AbilityId id) => _engine.canCast(id);

  void _onTick(Duration elapsed) {
    // Ticker gives cumulative elapsed; the engine wants seconds this frame.
    // Use microseconds — millisecond truncation drifts the sim clock at 60fps.
    final dt = (elapsed.inMicroseconds - _lastElapsed.inMicroseconds) / 1e6;
    _lastElapsed = elapsed;
    if (dt <= 0) return;
    // Clamp guards a stalled frame (e.g. a debugger break) from dumping a huge
    // catch-up into the engine's accumulator.
    _engine.tick(dt.clamp(0.0, 0.25));
    notifyListeners();
  }

  @override
  void dispose() {
    _ticker.dispose();
    super.dispose();
  }
}
