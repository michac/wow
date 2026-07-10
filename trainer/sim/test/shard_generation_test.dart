import 'package:rotation_sim/sim.dart';
import 'package:test/test.dart';

import 'support/fixtures.dart';
import 'support/script.dart';

void main() {
  group('Agony-tick shard generation', () {
    test('AlwaysRng: 9 ticks → 9 shards, capped at 5 with exact overcap', () {
      final s = ScriptedSession(config: afflictionConfig(), rng: const AlwaysRng())
        ..press(AbilityId.agony)
        ..advance(18.0);

      // 9 ticks, every one procs a shard under AlwaysRng.
      expect(s.countOf<ShardGenerated>(), 9);

      final shards = s.state.resources[ResourceId.soulShard]!;
      // Start 3 → +1 +1 reaches cap 5, then 7 wasted.
      expect(shards.current, 5);
      expect(shards.overcapWasted, 7);

      // 2 generations banked, 7 flagged overcapped.
      final wasted =
          s.eventsOf<ShardGenerated>().where((e) => e.overcapped).length;
      expect(wasted, 7);
    });

    test('NeverRng: no ticks proc a shard', () {
      final s = ScriptedSession(config: afflictionConfig(), rng: const NeverRng())
        ..press(AbilityId.agony)
        ..advance(18.0);

      expect(s.countOf<ShardGenerated>(), 0);
      expect(s.state.resources[ResourceId.soulShard]!.current, 3);
      expect(s.state.resources[ResourceId.soulShard]!.overcapWasted, 0);
    });

    test('ScriptedRng: exactly the queued draws decide each tick', () {
      // 4 ticks, draws < 0.5 proc; queue: proc, no, proc, no.
      final s = ScriptedSession(
        config: afflictionConfig(),
        rng: ScriptedRng([0.1, 0.9, 0.2, 0.8]),
      )
        ..press(AbilityId.agony)
        ..advance(8.0); // ticks at 2,4,6,8

      expect(s.countOf<ShardGenerated>(), 2);
    });
  });

  group('statistical smoke', () {
    test('SeededRng(42): ~1000 Agony ticks proc near the 0.5 rate', () {
      // The statistical smoke needs ~2000s of ticks — far past the default
      // 60s pull cap, so run it with an effectively unbounded pull length.
      final s = ScriptedSession(
        config: afflictionConfig(),
        rng: SeededRng(42),
        pullSeconds: double.infinity,
      )..press(AbilityId.agony);

      var guard = 0;
      while (s.eventsOf<DamageEvent>().where((e) => e.debuff == DebuffId.agony).length <
              1000 &&
          guard < 5000) {
        if (!s.state.debuffActive(DebuffId.agony)) {
          s.press(AbilityId.agony);
        }
        s.advance(2.0);
        guard++;
      }

      final ticks = s
          .eventsOf<DamageEvent>()
          .where((e) => e.debuff == DebuffId.agony)
          .length;
      final procs = s.countOf<ShardGenerated>();
      expect(ticks, greaterThanOrEqualTo(1000));

      final rate = procs / ticks;
      expect(rate, closeTo(0.5, 0.05),
          reason: 'observed shard proc rate $rate over $ticks ticks');
    });
  });
}
