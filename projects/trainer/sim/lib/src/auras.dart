import 'package:meta/meta.dart';

/// Immutable snapshot of a player aura / proc (Nightfall in M1).
@immutable
class AuraState {
  const AuraState({
    required this.expiresAt,
    required this.stacks,
  });

  /// Sim-clock time at which the aura falls off.
  final double expiresAt;
  final int stacks;

  /// Whether the aura is still up at sim time [now].
  bool isActiveAt(double now) => now < expiresAt && stacks > 0;

  /// Seconds remaining at sim time [now] (0 once expired).
  double remainingAt(double now) {
    final left = expiresAt - now;
    return left > 0 ? left : 0;
  }

  @override
  String toString() => 'AuraState(stacks: $stacks, expiresAt: $expiresAt)';
}
