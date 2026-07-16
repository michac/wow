import 'package:meta/meta.dart';

import 'auras.dart';
import 'cast.dart';
import 'cooldowns.dart';
import 'debuffs.dart';
import 'ids.dart';
import 'resources.dart';

/// Immutable snapshot of the whole simulation at sim time [time].
///
/// This is the sole window M2's UI gets onto engine internals: the engine
/// rebuilds a fresh [GameState] after every `tick`/`cast`. All sub-structs are
/// immutable and all maps are keyed by enums. Expired auras/debuffs are pruned
/// before the snapshot, so the `*Active` helpers can rely on map membership.
@immutable
class GameState {
  const GameState({
    required this.time,
    required this.gcdEndsAt,
    required this.clipCount,
    required this.resources,
    required this.cooldowns,
    required this.auras,
    required this.debuffs,
    required this.cast,
  });

  /// Current sim-clock time in seconds.
  final double time;

  /// Sim time the global cooldown ends.
  final double gcdEndsAt;

  /// Running count of hard casts clipped this session (tracked for M4).
  final int clipCount;

  final Map<ResourceId, ResourceState> resources;
  final Map<AbilityId, CooldownState> cooldowns;
  final Map<AuraId, AuraState> auras;
  final Map<DebuffId, DebuffState> debuffs;

  /// In-progress cast/channel, or null.
  final CastState? cast;

  bool get isGcdActive => time < gcdEndsAt;
  double get gcdRemaining {
    final left = gcdEndsAt - time;
    return left > 0 ? left : 0;
  }

  bool get isCasting => cast != null;

  /// Current value of a resource (0 if absent).
  int resource(ResourceId id) => resources[id]?.current ?? 0;

  /// Whether a debuff is currently up.
  bool debuffActive(DebuffId id) => debuffs.containsKey(id);

  /// Whether an aura is currently up.
  bool auraActive(AuraId id) => auras.containsKey(id);

  /// Stack count of an aura (0 if absent).
  int auraStacks(AuraId id) => auras[id]?.stacks ?? 0;

  @override
  String toString() {
    return 'GameState(t: ${time.toStringAsFixed(2)}, '
        'shards: ${resource(ResourceId.soulShard)}, '
        'debuffs: ${debuffs.keys.toList()}, '
        'auras: ${auras.keys.toList()}, '
        'cast: $cast)';
  }
}
