import 'abilities.dart';
import 'game_state.dart';
import 'ids.dart';

/// Advise Unstable Affliction once shards reach this "high" threshold (and the
/// dots/haunt are handled). Placeholder tuning for M1.
const int kUaShardThreshold = 4;

/// Pure next-ability advice for the simplified-Affliction priority:
///
///   agony → corruption → haunt → unstable affliction (high shards) → shadow bolt
///
/// A dot is advised when absent *or* refreshable within its pandemic window
/// (the optimal refresh moment). Returns null only if the priority list is
/// empty / nothing is configured.
AbilityId? advisePriority(GameState s, SimConfig config) {
  if (_dotNeedsRefresh(s, config, DebuffId.agony, AbilityId.agony)) {
    return AbilityId.agony;
  }
  if (_dotNeedsRefresh(s, config, DebuffId.corruption, AbilityId.corruption)) {
    return AbilityId.corruption;
  }

  if (config.abilities.containsKey(AbilityId.haunt) &&
      _abilityReady(s, AbilityId.haunt) &&
      !s.debuffActive(DebuffId.haunt)) {
    return AbilityId.haunt;
  }

  final ua = config.abilities[AbilityId.unstableAffliction];
  if (ua != null) {
    final shards = s.resource(ResourceId.soulShard);
    if (shards >= kUaShardThreshold && shards >= ua.cost) {
      return AbilityId.unstableAffliction;
    }
  }

  if (config.abilities.containsKey(AbilityId.shadowBolt)) {
    return AbilityId.shadowBolt;
  }

  return config.priority.isEmpty ? null : config.priority.first;
}

bool _dotNeedsRefresh(
  GameState s,
  SimConfig config,
  DebuffId debuff,
  AbilityId ability,
) {
  if (!config.abilities.containsKey(ability)) return false;
  final state = s.debuffs[debuff];
  if (state == null) return true;
  final def = config.debuffs[debuff];
  if (def == null) return false;
  final remaining = state.expiresAt - s.time;
  return remaining <= def.pandemic * def.duration;
}

bool _abilityReady(GameState s, AbilityId id) {
  final cd = s.cooldowns[id];
  if (cd == null) return true;
  return cd.isReady(s.time);
}
