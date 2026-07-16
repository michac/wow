import 'package:rotation_sim/sim.dart';
import 'package:test/test.dart';

import 'support/fixtures.dart';

CastRejectReason? rejectReason(CastResult r) =>
    r is CastRejected ? r.reason : null;

void main() {
  group('every CastRejectReason path', () {
    test('unknownAbility — ability not in config', () {
      final engine = Engine(config: configWithoutHaunt(), rng: const NeverRng());
      final r = engine.cast(AbilityId.haunt);
      expect(rejectReason(r), CastRejectReason.unknownAbility);
    });

    test('onCooldown — Haunt cannot recast immediately', () {
      final engine = Engine(config: afflictionConfig(), rng: const NeverRng());
      engine.cast(AbilityId.haunt);
      expect(engine.canCast(AbilityId.haunt), CastRejectReason.onCooldown);
    });

    test('insufficientResource — UA with zero shards', () {
      final engine =
          Engine(config: afflictionConfig(shardStart: 0), rng: const NeverRng());
      final r = engine.cast(AbilityId.unstableAffliction);
      expect(rejectReason(r), CastRejectReason.insufficientResource);
    });

    test('gcdActive — second on-GCD ability inside the GCD', () {
      final engine = Engine(config: afflictionConfig(), rng: const NeverRng());
      engine.cast(AbilityId.agony);
      final r = engine.cast(AbilityId.corruption);
      expect(rejectReason(r), CastRejectReason.gcdActive);
    });

    test('alreadyCasting — off-GCD ability during a hard cast', () {
      final engine = Engine(config: configWithOffGcd(), rng: const NeverRng());
      engine.cast(AbilityId.shadowBolt); // 2.0s hard cast, GCD 1.5
      engine.advanceBy(1.6); // GCD free, cast still in progress
      final r = engine.cast(AbilityId.unstableAffliction); // off-GCD here
      expect(rejectReason(r), CastRejectReason.alreadyCasting);
    });

    test('channeling — on-GCD ability during a channel', () {
      final engine = Engine(config: configWithChannel(), rng: const NeverRng());
      engine.cast(AbilityId.shadowBolt); // 3.0s channel, GCD 1.5
      engine.advanceBy(1.6); // GCD free, channel still in progress
      final r = engine.cast(AbilityId.agony);
      expect(rejectReason(r), CastRejectReason.channeling);
    });
  });

  group('cast() and canCast() never disagree', () {
    test('castable: canCast null and cast accepted', () {
      final engine = Engine(config: afflictionConfig(), rng: const NeverRng());
      expect(engine.canCast(AbilityId.agony), isNull);
      expect(engine.cast(AbilityId.agony), isA<CastAccepted>());
    });

    test('rejected: canCast reason matches cast reason', () {
      final engine = Engine(config: afflictionConfig(), rng: const NeverRng());
      engine.cast(AbilityId.agony); // burns the GCD
      final predicted = engine.canCast(AbilityId.corruption);
      final actual = rejectReason(engine.cast(AbilityId.corruption));
      expect(predicted, isNotNull);
      expect(predicted, actual);
    });
  });
}
