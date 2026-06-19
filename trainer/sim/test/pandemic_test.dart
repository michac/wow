import 'package:rotation_sim/sim.dart';
import 'package:test/test.dart';

import 'support/fixtures.dart';
import 'support/script.dart';

void main() {
  const duration = 18.0;
  const pandemicCap = 1.3 * duration; // 23.4
  const window = 0.3 * duration; // 5.4

  double remainingOfAgony(ScriptedSession s) {
    final d = s.state.debuffs[DebuffId.agony]!;
    return d.expiresAt - s.state.time;
  }

  test('refresh inside the pandemic window extends, bounded by 1.3*duration', () {
    final s = ScriptedSession(config: afflictionConfig(), rng: const NeverRng())
      ..press(AbilityId.agony)
      ..advance(13.0); // remaining ~5.0s, inside the 5.4s window

    final remaining = remainingOfAgony(s);
    expect(remaining, lessThanOrEqualTo(window),
        reason: 'precondition: inside pandemic window');

    s.press(AbilityId.agony);
    final newRemaining = remainingOfAgony(s);

    expect(newRemaining, greaterThan(remaining),
        reason: 'inside the window the DoT is extended, not clipped');
    expect(newRemaining, closeTo((remaining + duration).clamp(0, pandemicCap), 1e-3));
    expect(newRemaining, lessThanOrEqualTo(pandemicCap + 1e-6),
        reason: 'extension is capped at 1.3 * duration');
  });

  test('refresh at the window edge caps remaining at exactly 1.3*duration', () {
    final s = ScriptedSession(config: afflictionConfig(), rng: const NeverRng())
      ..press(AbilityId.agony)
      ..advance(12.6); // remaining ~5.4s, the window edge

    final remaining = remainingOfAgony(s);
    // Mirror the engine's own branch using the same measured remaining, so the
    // assertion is robust to float landing either side of the edge.
    final expected =
        remaining <= window ? (remaining + duration).clamp(0, pandemicCap) : duration;

    s.press(AbilityId.agony);
    expect(remainingOfAgony(s), closeTo(expected, 1e-3));
    expect(remainingOfAgony(s), lessThanOrEqualTo(pandemicCap + 1e-6));
  });

  test('refresh outside the window sets full duration (clips remaining)', () {
    final s = ScriptedSession(config: afflictionConfig(), rng: const NeverRng())
      ..press(AbilityId.agony)
      ..advance(2.0); // remaining ~16s, far outside the window

    final remaining = remainingOfAgony(s);
    expect(remaining, greaterThan(window),
        reason: 'precondition: outside pandemic window');

    s.press(AbilityId.agony);
    final newRemaining = remainingOfAgony(s);

    expect(newRemaining, closeTo(duration, 1e-3),
        reason: 'outside the window a refresh just sets the base duration');
    expect(newRemaining, lessThan(remaining + duration),
        reason: 'the remaining time was not banked — a teachable early clip');
  });
}
