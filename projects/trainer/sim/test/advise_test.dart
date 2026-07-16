import 'package:rotation_sim/sim.dart';
import 'package:test/test.dart';

import 'support/fixtures.dart';

void main() {
  group('advise() priority', () {
    test('opens on Agony when nothing is up', () {
      final engine = Engine(config: afflictionConfig(), rng: const NeverRng());
      expect(engine.advise(), AbilityId.agony);
    });

    test('advises Corruption once Agony is up', () {
      final engine = Engine(config: afflictionConfig(), rng: const NeverRng());
      engine.cast(AbilityId.agony);
      expect(engine.advise(), AbilityId.corruption);
    });

    test('advises Haunt when both DoTs are up and Haunt is ready', () {
      final engine = Engine(config: afflictionConfig(), rng: const NeverRng());
      engine.cast(AbilityId.agony);
      engine.advanceBy(1.5);
      engine.cast(AbilityId.corruption);
      expect(engine.advise(), AbilityId.haunt);
    });

    test('advises UA at high shards once DoTs + Haunt are handled', () {
      final engine =
          Engine(config: afflictionConfig(shardStart: 5), rng: const NeverRng());
      engine.cast(AbilityId.agony);
      engine.advanceBy(1.5);
      engine.cast(AbilityId.corruption);
      engine.advanceBy(1.5);
      engine.cast(AbilityId.haunt);
      engine.advanceBy(1.5); // Haunt resolves: debuff up, on cooldown

      expect(engine.advise(), AbilityId.unstableAffliction);
    });

    test('falls through to Shadow Bolt at low shards', () {
      final engine =
          Engine(config: afflictionConfig(shardStart: 3), rng: const NeverRng());
      engine.cast(AbilityId.agony);
      engine.advanceBy(1.5);
      engine.cast(AbilityId.corruption);
      engine.advanceBy(1.5);
      engine.cast(AbilityId.haunt);
      engine.advanceBy(1.5);

      expect(engine.advise(), AbilityId.shadowBolt);
    });

    test('re-advises Agony when it enters the pandemic window', () {
      final engine = Engine(config: afflictionConfig(), rng: const NeverRng());
      engine.cast(AbilityId.agony);
      engine.advanceBy(13.0); // remaining ~5s, inside the 5.4s window
      expect(engine.advise(), AbilityId.agony);
    });
  });
}
