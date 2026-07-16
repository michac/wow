import 'package:rotation_sim/sim.dart';

/// The canonical M1 simplified-Affliction config, optionally with a custom
/// starting shard count for spender tests.
SimConfig afflictionConfig({int shardStart = 3}) =>
    afflictionSimplified(shardStart: shardStart);

/// Config missing Haunt — used to drive the `unknownAbility` reject path.
SimConfig configWithoutHaunt() {
  final base = afflictionSimplified();
  final abilities = Map<AbilityId, AbilityDef>.of(base.abilities)
    ..remove(AbilityId.haunt);
  return base.copyWith(
    abilities: abilities,
    priority: base.priority.where((a) => a != AbilityId.haunt).toList(),
  );
}

/// Config where Unstable Affliction is off-GCD and free — used to drive the
/// `alreadyCasting` reject path (an off-GCD ability started mid hard-cast).
SimConfig configWithOffGcd() {
  final base = afflictionSimplified();
  final abilities = Map<AbilityId, AbilityDef>.of(base.abilities);
  abilities[AbilityId.unstableAffliction] =
      abilities[AbilityId.unstableAffliction]!
          .copyWith(onGcd: false, cost: 0, costResource: null);
  return base.copyWith(abilities: abilities);
}

/// Config where Shadow Bolt is a 3s channel — used to drive the `channeling`
/// reject path (an on-GCD ability pressed during a channel).
SimConfig configWithChannel() {
  final base = afflictionSimplified();
  final abilities = Map<AbilityId, AbilityDef>.of(base.abilities);
  abilities[AbilityId.shadowBolt] = abilities[AbilityId.shadowBolt]!
      .copyWith(castTime: 0, isChannel: true, channelDuration: 3.0);
  return base.copyWith(abilities: abilities);
}
