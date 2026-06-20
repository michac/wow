import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:rotation_sim/sim.dart';
import 'package:rotation_trainer_app/game_screen.dart';
import 'package:rotation_trainer_app/widgets/ability_button.dart';

/// Pump the game screen on a portrait phone-sized surface with injected
/// determinism. Never use `pumpAndSettle` — the game Ticker never settles.
Future<void> pumpGame(
  WidgetTester tester, {
  SimConfig? config,
  SimRng? rng,
}) async {
  tester.view.physicalSize = const Size(1080, 2400);
  tester.view.devicePixelRatio = 3.0;
  addTearDown(tester.view.resetPhysicalSize);
  addTearDown(tester.view.resetDevicePixelRatio);
  await tester.pumpWidget(MaterialApp(home: GameScreen(config: config, rng: rng)));
}

Finder abilityButton(AbilityId id) =>
    find.byWidgetPredicate((w) => w is AbilityButton && w.id == id);

/// Advance the game by stepping fixed 1/60s render frames, the way the real
/// Ticker drives it. (One giant `pump` would be capped by the controller's
/// stalled-frame clamp, so step frames instead.)
Future<void> advance(WidgetTester tester, double seconds) async {
  const step = Duration(microseconds: 16667); // ~1/60s, the engine's fixed dt
  final frames = (seconds * 60).round();
  for (var i = 0; i < frames; i++) {
    await tester.pump(step);
  }
}

void main() {
  testWidgets('renders the action bar and hides the cast bar at rest',
      (tester) async {
    await pumpGame(tester, rng: const NeverRng());
    expect(find.byType(AbilityButton), findsNWidgets(5));
    expect(find.text('Target dummy'), findsOneWidget);
    expect(find.text('Shadow Bolt'), findsNothing); // cast bar hidden
  });

  testWidgets('tapping Agony applies the debuff (countdown appears)',
      (tester) async {
    await pumpGame(tester, rng: const NeverRng());
    await tester.tap(abilityButton(AbilityId.agony));
    await tester.pump(const Duration(milliseconds: 16));
    // Agony's 18s timer now counts down on the target panel.
    expect(find.text('18'), findsOneWidget);
  });

  testWidgets('Shadow Bolt shows the cast bar, which clears on completion',
      (tester) async {
    await pumpGame(tester, rng: const NeverRng());
    await tester.tap(abilityButton(AbilityId.shadowBolt));
    await tester.pump(const Duration(milliseconds: 16));
    expect(find.text('Shadow Bolt'), findsOneWidget); // cast bar label

    await advance(tester, 3.0); // past the 2.0s cast
    expect(find.text('Shadow Bolt'), findsNothing); // bar hidden again
  });

  testWidgets('spending the last shard disables Unstable Affliction',
      (tester) async {
    await pumpGame(
      tester,
      config: afflictionSimplified(shardStart: 1),
      rng: const NeverRng(),
    );
    expect(find.text('◇'), findsNothing); // affordable at first

    await tester.tap(abilityButton(AbilityId.unstableAffliction));
    await tester.pump(const Duration(milliseconds: 16));
    // 1 → 0 shards: UA now reports insufficientResource via the ◇ badge.
    expect(find.text('◇'), findsOneWidget);
  });

  testWidgets('the GCD dims other buttons, then frees them', (tester) async {
    await pumpGame(tester, rng: const NeverRng());
    await tester.tap(abilityButton(AbilityId.agony));
    await tester.pump(const Duration(milliseconds: 16));
    expect(find.text('GCD'), findsWidgets); // on-GCD buttons gated

    await advance(tester, 1.6); // past the 1.5s GCD
    expect(find.text('GCD'), findsNothing);
  });

  testWidgets('a debuff timer visibly counts down', (tester) async {
    await pumpGame(tester, rng: const NeverRng());
    await tester.tap(abilityButton(AbilityId.corruption));
    await tester.pump(const Duration(milliseconds: 16));
    expect(find.text('14'), findsOneWidget); // Corruption's 14s duration

    // Advance to ~11.6s remaining — clear of integer ceil() boundaries.
    await advance(tester, 2.4);
    expect(find.text('14'), findsNothing);
    expect(find.text('12'), findsOneWidget);
  });
}
