import 'package:rotation_sim/sim.dart';
import 'package:test/test.dart';

import 'support/fixtures.dart';

void main() {
  group('fixed-timestep accumulator', () {
    test('a sub-dt frame does not advance the clock until dt accumulates', () {
      final engine = Engine(config: afflictionConfig(), rng: const NeverRng());
      final dt = engine.config.fixedDt;

      engine.tick(dt * 0.5);
      expect(engine.state.time, 0,
          reason: 'half a sub-step should not step the clock');

      engine.tick(dt * 0.5);
      expect(engine.state.time, closeTo(dt, 1e-9),
          reason: 'the second half completes one fixed sub-step');
    });

    test('one big frame runs many fixed sub-steps', () {
      final engine = Engine(config: afflictionConfig(), rng: const NeverRng());
      engine.tick(1.0);
      expect(engine.state.time, closeTo(1.0, 1e-6));
    });

    test('advanceBy is tick by another name', () {
      final a = Engine(config: afflictionConfig(), rng: const NeverRng());
      final b = Engine(config: afflictionConfig(), rng: const NeverRng());
      a.tick(3.0);
      b.advanceBy(3.0);
      expect(a.state.time, closeTo(b.state.time, 1e-12));
    });

    test('calling tick(dt) exactly N times yields exactly N sub-steps', () {
      final engine = Engine(config: afflictionConfig(), rng: const NeverRng());
      final dt = engine.config.fixedDt;
      for (var i = 0; i < 600; i++) {
        engine.tick(dt);
      }
      expect(engine.state.time, closeTo(600 * dt, 1e-6));
    });
  });

  group('tick ordering / event flushing', () {
    test('instant-cast events flush on the next tick', () {
      final engine = Engine(config: afflictionConfig(), rng: const NeverRng());
      final result = engine.cast(AbilityId.agony);
      expect(result, isA<CastAccepted>());

      // The DotApplied from the press is buffered, surfaced on the next tick.
      final events = engine.tick(engine.config.fixedDt);
      expect(events.whereType<DotApplied>().length, 1);
      expect((events.whereType<DotApplied>().first).debuff, DebuffId.agony);
    });

    test('a completed hard cast resolves and clears the cast', () {
      final engine = Engine(config: afflictionConfig(), rng: const NeverRng());
      engine.cast(AbilityId.shadowBolt); // 2.0s hard cast
      expect(engine.state.isCasting, isTrue);

      final events = engine.advanceBy(2.0);
      expect(engine.state.isCasting, isFalse);
      expect(events.whereType<DamageEvent>().any((e) => e.ability == AbilityId.shadowBolt),
          isTrue);
    });
  });
}
