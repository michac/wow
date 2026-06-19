import 'package:meta/meta.dart';

import 'ids.dart';

/// Side effects produced by a tick (or by an instant cast, flushed on the next
/// tick). The UI renders these as floating text / haptics / flashes; tests
/// assert on them. Every event carries the sim-clock time [at] it occurred.
@immutable
sealed class SimEvent {
  const SimEvent({required this.at});

  final double at;
}

/// Damage dealt by an ability hit ([ability]) or a DoT tick ([debuff]).
/// Exactly one of the two is non-null.
final class DamageEvent extends SimEvent {
  const DamageEvent({
    required super.at,
    required this.amount,
    this.ability,
    this.debuff,
  });

  final double amount;
  final AbilityId? ability;
  final DebuffId? debuff;

  @override
  String toString() => 'DamageEvent($amount, ability: $ability, debuff: $debuff)';
}

/// A debuff was applied or refreshed. [refreshed] distinguishes a re-apply
/// from a first application; [expiresAt] is the resulting fall-off time.
final class DotApplied extends SimEvent {
  const DotApplied({
    required super.at,
    required this.debuff,
    required this.refreshed,
    required this.expiresAt,
  });

  final DebuffId debuff;
  final bool refreshed;
  final double expiresAt;

  @override
  String toString() => 'DotApplied($debuff, refreshed: $refreshed)';
}

/// A debuff fell off (expired).
final class DotExpired extends SimEvent {
  const DotExpired({required super.at, required this.debuff});

  final DebuffId debuff;

  @override
  String toString() => 'DotExpired($debuff)';
}

/// A resource unit was generated. [overcapped] is true when it was wasted
/// because the resource was already at cap.
final class ShardGenerated extends SimEvent {
  const ShardGenerated({
    required super.at,
    required this.amount,
    required this.overcapped,
  });

  final int amount;
  final bool overcapped;

  @override
  String toString() => 'ShardGenerated($amount, overcapped: $overcapped)';
}

/// An aura was granted or refreshed (Nightfall). [stacks] is the post-grant
/// stack count.
final class AuraGranted extends SimEvent {
  const AuraGranted({
    required super.at,
    required this.aura,
    required this.stacks,
  });

  final AuraId aura;
  final int stacks;

  @override
  String toString() => 'AuraGranted($aura, stacks: $stacks)';
}

/// A hard cast was clipped (interrupted) by starting a new on-GCD ability.
/// [ability] is the cast that was lost — a teachable mistake.
final class CastClipped extends SimEvent {
  const CastClipped({required super.at, required this.ability});

  final AbilityId ability;

  @override
  String toString() => 'CastClipped($ability)';
}
