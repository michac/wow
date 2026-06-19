import 'package:rotation_sim/sim.dart';
import 'package:test/test.dart';

import 'support/fixtures.dart';
import 'support/script.dart';

void main() {
  group('GCD gating', () {
    test('a second on-GCD cast within the GCD is rejected', () {
      final engine = Engine(config: afflictionConfig(), rng: const NeverRng());
      expect(engine.cast(AbilityId.agony), isA<CastAccepted>());

      final r = engine.cast(AbilityId.corruption);
      expect(r, isA<CastRejected>());
      expect((r as CastRejected).reason, CastRejectReason.gcdActive);
    });

    test('the GCD frees after 1.5s', () {
      final engine = Engine(config: afflictionConfig(), rng: const NeverRng());
      engine.cast(AbilityId.agony);
      engine.advanceBy(1.5);
      expect(engine.canCast(AbilityId.corruption), isNull);
      expect(engine.cast(AbilityId.corruption), isA<CastAccepted>());
    });
  });

  group('hard cast completion', () {
    test('Shadow Bolt resolves at +2.0s, not before', () {
      final engine = Engine(config: afflictionConfig(), rng: const NeverRng());
      final start = engine.cast(AbilityId.shadowBolt);
      expect((start as CastAccepted).kind, CastResolution.castStarted);

      final before = engine.advanceBy(1.9);
      expect(before.whereType<DamageEvent>().where((e) => e.ability == AbilityId.shadowBolt),
          isEmpty);

      final after = engine.advanceBy(0.2); // crosses 2.0s
      expect(after.whereType<DamageEvent>().any((e) => e.ability == AbilityId.shadowBolt),
          isTrue);
      expect(engine.state.isCasting, isFalse);
    });
  });

  group('Nightfall makes Shadow Bolt instant', () {
    test('with Nightfall up, Shadow Bolt is instant and decrements the stack', () {
      final s = ScriptedSession(config: afflictionConfig(), rng: const AlwaysRng())
        ..press(AbilityId.corruption)
        ..advance(2.0); // one Corruption tick grants Nightfall

      final before = s.state.auraStacks(AuraId.nightfall);
      expect(before, greaterThanOrEqualTo(1));

      s.press(AbilityId.shadowBolt);
      expect((s.lastResult! as CastAccepted).kind, CastResolution.instant);
      expect(s.state.isCasting, isFalse);
      expect(s.state.auraStacks(AuraId.nightfall), before - 1);
    });

    test('without Nightfall, Shadow Bolt is a hard cast', () {
      final engine = Engine(config: afflictionConfig(), rng: const NeverRng());
      final r = engine.cast(AbilityId.shadowBolt);
      expect((r as CastAccepted).kind, CastResolution.castStarted);
      expect(engine.state.isCasting, isTrue);
    });
  });

  group('clipping', () {
    test('a new on-GCD ability mid hard-cast clips the old cast', () {
      final s = ScriptedSession(config: afflictionConfig(), rng: const NeverRng())
        ..press(AbilityId.shadowBolt) // 2.0s hard cast
        ..advance(1.6); // GCD freed at 1.5s; cast still in progress

      expect(s.state.isCasting, isTrue);

      s.press(AbilityId.agony); // on-GCD instant → clips Shadow Bolt
      expect(s.lastResult, isA<CastAccepted>());
      expect(s.state.clipCount, 1);
      expect(s.state.isCasting, isFalse,
          reason: 'Agony is instant, so no new cast bar after the clip');

      s.advance(0.1); // flush the buffered CastClipped event
      expect(s.countOf<CastClipped>(), 1);
      expect(s.eventsOf<CastClipped>().single.ability, AbilityId.shadowBolt);
    });
  });
}
