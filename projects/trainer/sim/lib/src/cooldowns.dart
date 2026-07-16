import 'package:meta/meta.dart';

/// Immutable snapshot of an ability's cooldown.
///
/// M1 uses a single-charge timestamp model ([readyAt]); [charges] /
/// [maxCharges] are carried for forward-compatibility with charge-based
/// abilities in later milestones.
@immutable
class CooldownState {
  const CooldownState({
    required this.readyAt,
    this.charges = 1,
    this.maxCharges = 1,
  });

  /// Sim-clock time at which the ability becomes usable again.
  final double readyAt;
  final int charges;
  final int maxCharges;

  /// Whether the cooldown is up at sim time [now].
  bool isReady(double now) => now >= readyAt;

  /// Seconds remaining at sim time [now] (0 once ready).
  double remainingAt(double now) {
    final left = readyAt - now;
    return left > 0 ? left : 0;
  }

  @override
  String toString() => 'CooldownState(readyAt: $readyAt)';
}
