import 'package:meta/meta.dart';

/// Immutable snapshot of a target debuff (Agony / Corruption / Haunt).
///
/// Pandemic refresh math lives in the engine; this is the resulting state.
/// [nextTickAt] is the sim-clock time of this debuff's next damage tick
/// (`double.infinity` for non-ticking debuffs like Haunt).
@immutable
class DebuffState {
  const DebuffState({
    required this.appliedAt,
    required this.expiresAt,
    required this.nextTickAt,
  });

  final double appliedAt;
  final double expiresAt;
  final double nextTickAt;

  /// Whether the debuff is still up at sim time [now].
  bool isActiveAt(double now) => now < expiresAt;

  /// Seconds remaining at sim time [now] (0 once expired).
  double remainingAt(double now) {
    final left = expiresAt - now;
    return left > 0 ? left : 0;
  }

  @override
  String toString() =>
      'DebuffState(expiresAt: $expiresAt, nextTickAt: $nextTickAt)';
}
