import 'dart:math';

/// The *only* source of randomness the engine consumes.
///
/// The model keeps the real proc probabilities (Agony → 0.5 shard, Corruption
/// → 0.15 Nightfall); determinism comes from injecting which draws succeed.
/// The engine contract is: **exactly one [chance] call per proc-eligible tick,
/// in tick order.** Swap implementations to get stochastic feel runs (M2/M5)
/// or exact, assertable test behaviour — with zero changes to engine logic.
abstract interface class SimRng {
  /// Returns whether an event with probability [p] (in `[0, 1]`) occurs.
  bool chance(double p);
}

/// Real pseudo-random draws from a fixed seed. The production / "feel" RNG.
class SeededRng implements SimRng {
  SeededRng(int seed) : _random = Random(seed);

  final Random _random;

  @override
  bool chance(double p) => _random.nextDouble() < p;
}

/// Every eligible proc fires (`chance(p) == p > 0`). Upper-bound test RNG.
class AlwaysRng implements SimRng {
  const AlwaysRng();

  @override
  bool chance(double p) => p > 0;
}

/// No proc ever fires. Baseline / lower-bound test RNG.
class NeverRng implements SimRng {
  const NeverRng();

  @override
  bool chance(double p) => false;
}

/// Replays an exact queued sequence of uniform draws in `[0, 1)`.
///
/// `chance(p)` consumes the next draw and returns `draw < p`. Throws once the
/// queue is exhausted, so a test that over-draws fails loudly rather than
/// silently reusing values.
class ScriptedRng implements SimRng {
  ScriptedRng(List<double> draws) : _draws = List<double>.of(draws);

  final List<double> _draws;
  int _cursor = 0;

  /// Number of draws consumed so far.
  int get consumed => _cursor;

  @override
  bool chance(double p) {
    if (_cursor >= _draws.length) {
      throw StateError(
        'ScriptedRng exhausted after $_cursor draws; engine asked for more.',
      );
    }
    return _draws[_cursor++] < p;
  }
}
