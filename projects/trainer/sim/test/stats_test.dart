import 'package:rotation_sim/sim.dart';
import 'package:test/test.dart';

import 'support/fixtures.dart';
import 'support/script.dart';

void main() {
  group('SessionStats accumulation (scripted pulls)', () {
    test('Agony up for its full duration → uptimeFraction ≈ 1.0', () {
      final s = ScriptedSession(config: afflictionConfig(), rng: const NeverRng())
        ..press(AbilityId.agony)
        ..advance(18.0);

      // Sub-tick rounding (final step expires it) leaves a hair under 1.
      expect(s.engine.stats.uptimeFraction(DebuffId.agony),
          greaterThan(0.98));
      expect(s.engine.stats.uptimeFraction(DebuffId.agony),
          lessThanOrEqualTo(1.0));
    });

    test('a pure idle gap counts wasted GCDs', () {
      // 9s of doing nothing, gcd 1.5 → 6 wasted globals.
      final s = ScriptedSession(config: afflictionConfig(), rng: const NeverRng())
        ..advance(9.0);

      expect(s.engine.stats.idleSeconds, closeTo(9.0, 0.05));
      expect(s.engine.stats.wastedGcds, 6);
    });

    test('shards generated at cap → overcap matches overcapped events', () {
      // Start at the 5-shard cap; AlwaysRng makes every Agony tick proc a
      // shard, and with no spender pressed they all overcap.
      final s = ScriptedSession(
        config: afflictionConfig(shardStart: 5),
        rng: const AlwaysRng(),
      )
        ..press(AbilityId.agony)
        ..advance(18.0);

      final overcapEvents = s
          .eventsOf<ShardGenerated>()
          .where((e) => e.overcapped)
          .length;
      expect(overcapEvents, greaterThan(0));
      expect(s.engine.stats.overcap, overcapEvents);
    });

    test('clipping a hard cast with an on-GCD ability → clips == 1', () {
      final s = ScriptedSession(config: afflictionConfig(), rng: const NeverRng())
        ..press(AbilityId.shadowBolt) // 2.0s hard cast, sets a 1.5s GCD
        ..advance(1.6) // GCD free (1.5), cast still running (< 2.0)
        ..press(AbilityId.agony); // on-GCD → clips the Shadow Bolt

      expect(s.engine.stats.clips, 1);
    });

    test('dpsEquivalent == totalDamage / elapsed; total sums DamageEvents', () {
      final s = ScriptedSession(config: afflictionConfig(), rng: const NeverRng())
        ..press(AbilityId.agony)
        ..advance(18.0);

      final summed = s
          .eventsOf<DamageEvent>()
          .fold<double>(0, (acc, e) => acc + e.amount);
      final stats = s.engine.stats;

      expect(stats.totalDamage, summed);
      expect(stats.dpsEquivalent, stats.totalDamage / stats.elapsed);
    });

    test('a do-nothing pull grades in the F band', () {
      final s = ScriptedSession(config: afflictionConfig(), rng: const NeverRng())
        ..advance(60.0); // runs the full default pull, empty

      expect(s.engine.isEnded, isTrue);
      expect(s.engine.stats.grade, lessThan(60));
      expect(s.engine.stats.letter, 'F');
    });
  });

  group('pull lifecycle', () {
    test('advanceBy past the pull length lands exactly on pullSeconds', () {
      final engine = Engine(config: afflictionConfig(), rng: const NeverRng())
        ..advanceBy(120); // 60s pull; overshoot by 60s

      expect(engine.isEnded, isTrue);
      expect(engine.stats.elapsed, 60.0); // exact, not 60.0000001
      expect(engine.state.time, 60.0);
    });

    test('the pull freezes once ended — further ticks do not advance', () {
      final engine = Engine(config: afflictionConfig(), rng: const NeverRng())
        ..advanceBy(60);
      final frozen = engine.stats.totalDamage;

      engine.advanceBy(10); // ignored once ended
      expect(engine.state.time, 60.0);
      expect(engine.stats.totalDamage, frozen);
    });

    test('stop() ends the pull early at the current time', () {
      final engine = Engine(config: afflictionConfig(), rng: const NeverRng())
        ..advanceBy(10)
        ..stop();

      expect(engine.isEnded, isTrue);
      expect(engine.stats.elapsed, closeTo(10.0, 1e-6));
    });

    test('reset() zeroes every accumulator and clears isEnded', () {
      final engine = Engine(config: afflictionConfig(), rng: const AlwaysRng())
        ..cast(AbilityId.agony)
        ..advanceBy(120); // end the pull, accumulate stats
      expect(engine.isEnded, isTrue);

      engine.reset();

      expect(engine.isEnded, isFalse);
      expect(engine.state.time, 0.0);
      final stats = engine.stats;
      expect(stats.elapsed, 0.0);
      expect(stats.totalDamage, 0.0);
      expect(stats.idleSeconds, 0.0);
      expect(stats.clips, 0);
      expect(stats.overcap, 0);
      expect(stats.uptimeSeconds.values, everyElement(0.0));
      expect(engine.state.debuffActive(DebuffId.agony), isFalse);
    });
  });

  group('grade formula bands (SessionStats)', () {
    SessionStats stats({
      Map<DebuffId, double>? uptime,
      double idle = 0,
      int overcap = 0,
      int clips = 0,
    }) =>
        SessionStats(
          elapsed: 60,
          totalDamage: 60000,
          uptimeSeconds: uptime ??
              {DebuffId.agony: 60, DebuffId.corruption: 60, DebuffId.haunt: 60},
          idleSeconds: idle,
          overcap: overcap,
          clips: clips,
          gcd: 1.5,
        );

    test('full uptime, no waste → 100 / A', () {
      final s = stats();
      expect(s.grade, 100);
      expect(s.letter, 'A');
    });

    test('every DoT missing + heavy waste → clamps to 0 / F', () {
      final s = stats(
        uptime: {DebuffId.agony: 0, DebuffId.corruption: 0, DebuffId.haunt: 0},
        idle: 60,
        overcap: 10,
        clips: 3,
      );
      expect(s.grade, 0);
      expect(s.letter, 'F');
    });

    test('a clean pull grades strictly above a sloppy one', () {
      final clean = stats();
      final sloppy = stats(
        uptime: {DebuffId.agony: 30, DebuffId.corruption: 20, DebuffId.haunt: 0},
        idle: 12,
        overcap: 3,
        clips: 1,
      );
      expect(clean.grade, greaterThan(sloppy.grade));
    });
  });
}
