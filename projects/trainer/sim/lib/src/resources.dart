import 'package:meta/meta.dart';

/// Immutable snapshot of a single resource (Soul Shards in M1).
///
/// Discrete in M1 (shard pips 0..5). [overcapWasted] is the running count of
/// resource units generated while already at [max] — tracked now, surfaced by
/// M4's end-of-pull summary.
@immutable
class ResourceState {
  const ResourceState({
    required this.current,
    required this.min,
    required this.max,
    required this.overcapWasted,
  });

  final int current;
  final int min;
  final int max;
  final int overcapWasted;

  bool get isFull => current >= max;
  bool get isEmpty => current <= min;

  @override
  String toString() =>
      'ResourceState($current/$max, wasted: $overcapWasted)';
}
