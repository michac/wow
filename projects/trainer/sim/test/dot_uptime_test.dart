import 'package:rotation_sim/sim.dart';
import 'package:test/test.dart';

import 'support/fixtures.dart';
import 'support/script.dart';

void main() {
  group('DoT apply / tick / uptime', () {
    test('Agony stays up for its full duration (>= 0.99 uptime)', () {
      final s = ScriptedSession(config: afflictionConfig(), rng: const NeverRng())
        ..press(AbilityId.agony)
        ..advance(18.0);

      expect(s.uptime(DebuffId.agony), greaterThanOrEqualTo(0.99));
    });

    test('Agony ticks 9 times over 18s (one DamageEvent per tick)', () {
      final s = ScriptedSession(config: afflictionConfig(), rng: const NeverRng())
        ..press(AbilityId.agony)
        ..advance(18.0);

      final agonyTicks =
          s.eventsOf<DamageEvent>().where((e) => e.debuff == DebuffId.agony);
      expect(agonyTicks.length, 9);
    });

    test('Agony falls off after 18s and emits DotExpired', () {
      final s = ScriptedSession(config: afflictionConfig(), rng: const NeverRng())
        ..press(AbilityId.agony)
        ..advance(18.5);

      expect(s.state.debuffActive(DebuffId.agony), isFalse);
      expect(s.countOf<DotExpired>(), 1);
      expect(s.eventsOf<DotExpired>().single.debuff, DebuffId.agony);
    });

    test('Corruption ticks 7 times over its 14s duration', () {
      final s = ScriptedSession(config: afflictionConfig(), rng: const NeverRng())
        ..press(AbilityId.corruption)
        ..advance(14.0);

      final ticks = s
          .eventsOf<DamageEvent>()
          .where((e) => e.debuff == DebuffId.corruption);
      expect(ticks.length, 7);
    });
  });
}
