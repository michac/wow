import 'package:meta/meta.dart';

import 'ids.dart';

/// Kind of in-progress cast. M1's roster has no channels, but the path is
/// present so M2/M5 can add Drain Soul without touching the engine seam.
enum CastKind { hardCast, channel }

/// Immutable snapshot of an in-progress cast or channel.
///
/// [clipped] marks a cast that *began* by interrupting an earlier hard cast —
/// a teachable mistake M4 surfaces. (The interruption itself is also emitted
/// as a `CastClipped` event.)
@immutable
class CastState {
  const CastState({
    required this.ability,
    required this.kind,
    required this.startedAt,
    required this.endsAt,
    required this.clipped,
  });

  final AbilityId ability;
  final CastKind kind;
  final double startedAt;
  final double endsAt;
  final bool clipped;

  double get duration => endsAt - startedAt;

  /// Fill fraction in `[0, 1]` at sim time [now].
  double progressAt(double now) {
    final span = duration;
    if (span <= 0) return 1;
    final p = (now - startedAt) / span;
    if (p < 0) return 0;
    if (p > 1) return 1;
    return p;
  }

  /// Seconds left at sim time [now] (0 once complete).
  double remainingAt(double now) {
    final left = endsAt - now;
    return left > 0 ? left : 0;
  }

  @override
  String toString() =>
      'CastState($ability, $kind, $startedAt->$endsAt, clipped: $clipped)';
}
