import 'package:meta/meta.dart';

import 'ids.dart';

/// Immutable end-of-pull statistics — the raw accumulators the engine gathers
/// over a pull, plus the pure derived numbers M4's summary panel renders.
///
/// The engine builds one of these on demand from its accumulators (see
/// `Engine.stats`); nothing here mutates. All the "how good was that pull?"
/// math lives in getters so it stays deterministically unit-testable headless.
@immutable
class SessionStats {
  const SessionStats({
    required this.elapsed,
    required this.totalDamage,
    required this.uptimeSeconds,
    required this.idleSeconds,
    required this.overcap,
    required this.clips,
    required this.gcd,
  });

  /// Seconds of pull elapsed (== pull length once the pull has ended).
  final double elapsed;

  /// Sum of every [amount] the pull's DamageEvents carried.
  final double totalDamage;

  /// Per-debuff seconds-active accumulator. Seeded with every config debuff
  /// (defaulting to 0), so a never-applied DoT is still graded and rendered.
  final Map<DebuffId, double> uptimeSeconds;

  /// Seconds the player could have acted (no GCD, no cast) but didn't — the
  /// wasted-GCD signal.
  final double idleSeconds;

  /// Resource units generated while already at cap (summed across resources).
  final int overcap;

  /// Hard casts clipped by starting a new on-GCD ability.
  final int clips;

  /// The GCD length (seconds) this pull ran with — used to convert idle time
  /// into a whole-GCD count.
  final double gcd;

  // ---- derived numbers ----------------------------------------------------

  /// Rough DPS-equivalent: total damage over the pull length. Placeholder-
  /// relative (the M1 roster numbers aren't sim-accurate), matching the doc.
  double get dpsEquivalent => elapsed <= 0 ? 0 : totalDamage / elapsed;

  /// Fraction of the pull [id] was active, clamped `[0, 1]`.
  double uptimeFraction(DebuffId id) {
    if (elapsed <= 0) return 0;
    return ((uptimeSeconds[id] ?? 0) / elapsed).clamp(0.0, 1.0);
  }

  /// Whole GCDs' worth of idle time — the count of "wasted" globals.
  int get wastedGcds => gcd <= 0 ? 0 : (idleSeconds / gcd).round();

  // ---- grade --------------------------------------------------------------
  //
  // PLACEHOLDER weights. Balance is explicitly out of scope until the M1
  // roster's numbers are tuned (M5): these consts only need to move the grade
  // in the right *direction*, not model real Affliction value. Note Haunt is a
  // CD-gated amp — it can't sit at 100% uptime over a long pull, so grading it
  // against full uptime is imperfect; acceptable while W_dot is a placeholder.

  /// Penalty per DoT for a full uptime shortfall (scaled by the shortfall).
  static const double kWDot = 15;

  /// Penalty per overcapped resource unit.
  static const double kWOvercap = 2;

  /// Penalty per clipped hard cast.
  static const double kWClip = 5;

  /// Penalty per wasted GCD.
  static const double kWGcd = 2;

  /// Composite pull grade in `[0, 100]`. Starts at 100 and subtracts the
  /// weighted DoT-uptime shortfall over the tracked debuffs plus the overcap /
  /// clip / wasted-GCD penalties.
  double get grade {
    var score = 100.0;
    for (final id in uptimeSeconds.keys) {
      score -= (1 - uptimeFraction(id)) * kWDot;
    }
    score -= kWOvercap * overcap;
    score -= kWClip * clips;
    score -= kWGcd * wastedGcds;
    return score.clamp(0.0, 100.0);
  }

  /// Letter grade for [grade]: A≥90 / B≥80 / C≥70 / D≥60 / F otherwise.
  String get letter {
    final g = grade;
    if (g >= 90) return 'A';
    if (g >= 80) return 'B';
    if (g >= 70) return 'C';
    if (g >= 60) return 'D';
    return 'F';
  }

  @override
  String toString() =>
      'SessionStats(elapsed: ${elapsed.toStringAsFixed(1)}, '
      'grade: ${grade.toStringAsFixed(0)}$letter, '
      'dps~: ${dpsEquivalent.toStringAsFixed(1)})';
}
