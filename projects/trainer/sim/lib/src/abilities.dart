import 'package:meta/meta.dart';

import 'ids.dart';

/// Default fixed timestep: 60 Hz. Lives in [SimConfig] so the same constant
/// drives the engine accumulator and any test harness sampling cadence.
const double kFixedDt = 1 / 60;

/// Static definition of an ability. Pure data — M3's JSON loader produces
/// exactly this shape; M1 hard-codes the roster in [afflictionSimplified].
@immutable
class AbilityDef {
  const AbilityDef({
    required this.id,
    required this.name,
    required this.castTime,
    required this.onGcd,
    this.cooldown = 0,
    this.cost = 0,
    this.costResource,
    this.appliesDebuff,
    this.appliesAura,
    this.instantIfAura,
    this.consumesAura,
    this.damage = 0,
    this.generatesShard = 0,
    this.isChannel = false,
    this.channelDuration = 0,
  });

  final AbilityId id;
  final String name;

  /// Hard-cast time in seconds (0 == instant).
  final double castTime;
  final bool onGcd;

  /// Cooldown in seconds (0 == none). Starts when the cast begins.
  final double cooldown;

  /// Resource cost; spent on effect application.
  final int cost;
  final ResourceId? costResource;

  /// Debuff applied/refreshed on resolution.
  final DebuffId? appliesDebuff;

  /// Aura granted on resolution.
  final AuraId? appliesAura;

  /// If this aura is up, the cast is instant instead of hard-cast.
  final AuraId? instantIfAura;

  /// Aura whose stack is consumed when the cast resolves as instant.
  final AuraId? consumesAura;

  final int damage;

  /// Shards generated directly on cast (distinct from DoT-tick generation).
  final int generatesShard;

  final bool isChannel;
  final double channelDuration;

  AbilityDef copyWith({
    double? castTime,
    bool? onGcd,
    double? cooldown,
    int? cost,
    ResourceId? costResource,
    bool? isChannel,
    double? channelDuration,
  }) {
    return AbilityDef(
      id: id,
      name: name,
      castTime: castTime ?? this.castTime,
      onGcd: onGcd ?? this.onGcd,
      cooldown: cooldown ?? this.cooldown,
      cost: cost ?? this.cost,
      costResource: costResource ?? this.costResource,
      appliesDebuff: appliesDebuff,
      appliesAura: appliesAura,
      instantIfAura: instantIfAura,
      consumesAura: consumesAura,
      damage: damage,
      generatesShard: generatesShard,
      isChannel: isChannel ?? this.isChannel,
      channelDuration: channelDuration ?? this.channelDuration,
    );
  }
}

/// Static definition of a target debuff (DoT or pure amp).
@immutable
class DebuffDef {
  const DebuffDef({
    required this.id,
    required this.name,
    required this.duration,
    required this.tickInterval,
    this.pandemic = 0.3,
    this.tickDamage = 0,
    this.onTickShardChance = 0,
    this.onTickShardAmount = 0,
    this.onTickAuraChance = 0,
    this.grantsAura,
    this.damageAmp = 0,
  });

  final DebuffId id;
  final String name;
  final double duration;

  /// Seconds between ticks (0 == non-ticking, e.g. Haunt).
  final double tickInterval;

  /// Pandemic window as a fraction of [duration] (0.3 == refresh within the
  /// last 30% extends rather than clips).
  final double pandemic;

  final int tickDamage;

  /// Per-tick chance to generate [onTickShardAmount] shards.
  final double onTickShardChance;
  final int onTickShardAmount;

  /// Per-tick chance to grant [grantsAura].
  final double onTickAuraChance;
  final AuraId? grantsAura;

  /// Fractional damage amp this debuff grants while active (Haunt).
  final double damageAmp;
}

/// Static definition of a player aura.
@immutable
class AuraDef {
  const AuraDef({
    required this.id,
    required this.name,
    required this.duration,
    required this.maxStacks,
  });

  final AuraId id;
  final String name;
  final double duration;
  final int maxStacks;
}

/// Static definition of a resource.
@immutable
class ResourceDef {
  const ResourceDef({
    required this.id,
    required this.min,
    required this.max,
    required this.startAt,
  });

  final ResourceId id;
  final int min;
  final int max;
  final int startAt;
}

/// Everything the engine needs to run a spec: roster, debuff/aura/resource
/// definitions, priority list, and timing constants. Immutable; the engine
/// holds one for its lifetime.
@immutable
class SimConfig {
  const SimConfig({
    required this.abilities,
    required this.debuffs,
    required this.auras,
    required this.resources,
    required this.priority,
    this.gcd = 1.5,
    this.fixedDt = kFixedDt,
  });

  final Map<AbilityId, AbilityDef> abilities;
  final Map<DebuffId, DebuffDef> debuffs;
  final Map<AuraId, AuraDef> auras;
  final Map<ResourceId, ResourceDef> resources;
  final List<AbilityId> priority;
  final double gcd;
  final double fixedDt;

  SimConfig copyWith({
    Map<AbilityId, AbilityDef>? abilities,
    Map<ResourceId, ResourceDef>? resources,
    List<AbilityId>? priority,
  }) {
    return SimConfig(
      abilities: abilities ?? this.abilities,
      debuffs: debuffs,
      auras: auras,
      resources: resources ?? this.resources,
      priority: priority ?? this.priority,
      gcd: gcd,
      fixedDt: fixedDt,
    );
  }
}

/// The M1 simplified-Affliction roster. Numbers are deliberate placeholders
/// (not sim-accurate balance) per the spec; the *shape* is faithful.
SimConfig afflictionSimplified({int shardStart = 3}) {
  return SimConfig(
    gcd: 1.5,
    priority: const [
      AbilityId.agony,
      AbilityId.corruption,
      AbilityId.haunt,
      AbilityId.unstableAffliction,
      AbilityId.shadowBolt,
    ],
    abilities: const {
      AbilityId.agony: AbilityDef(
        id: AbilityId.agony,
        name: 'Agony',
        castTime: 0,
        onGcd: true,
        appliesDebuff: DebuffId.agony,
      ),
      AbilityId.corruption: AbilityDef(
        id: AbilityId.corruption,
        name: 'Corruption',
        castTime: 0,
        onGcd: true,
        appliesDebuff: DebuffId.corruption,
      ),
      AbilityId.shadowBolt: AbilityDef(
        id: AbilityId.shadowBolt,
        name: 'Shadow Bolt',
        castTime: 2.0,
        onGcd: true,
        instantIfAura: AuraId.nightfall,
        consumesAura: AuraId.nightfall,
        damage: 100,
      ),
      AbilityId.unstableAffliction: AbilityDef(
        id: AbilityId.unstableAffliction,
        name: 'Unstable Affliction',
        castTime: 0,
        onGcd: true,
        cost: 1,
        costResource: ResourceId.soulShard,
        damage: 220,
      ),
      AbilityId.haunt: AbilityDef(
        id: AbilityId.haunt,
        name: 'Haunt',
        castTime: 1.5,
        onGcd: true,
        cooldown: 15,
        appliesDebuff: DebuffId.haunt,
        damage: 80,
      ),
    },
    debuffs: const {
      DebuffId.agony: DebuffDef(
        id: DebuffId.agony,
        name: 'Agony',
        duration: 18,
        tickInterval: 2,
        pandemic: 0.3,
        tickDamage: 10,
        onTickShardChance: 0.5,
        onTickShardAmount: 1,
      ),
      DebuffId.corruption: DebuffDef(
        id: DebuffId.corruption,
        name: 'Corruption',
        duration: 14,
        tickInterval: 2,
        pandemic: 0.3,
        tickDamage: 8,
        onTickAuraChance: 0.15,
        grantsAura: AuraId.nightfall,
      ),
      DebuffId.haunt: DebuffDef(
        id: DebuffId.haunt,
        name: 'Haunt',
        duration: 8,
        tickInterval: 0,
        damageAmp: 0.10,
      ),
    },
    auras: const {
      AuraId.nightfall: AuraDef(
        id: AuraId.nightfall,
        name: 'Nightfall',
        duration: 12,
        maxStacks: 2,
      ),
    },
    resources: {
      ResourceId.soulShard: ResourceDef(
        id: ResourceId.soulShard,
        min: 0,
        max: 5,
        startAt: shardStart,
      ),
    },
  );
}
