import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:rotation_sim/sim.dart';
import 'package:rotation_trainer_app/app.dart';
import 'package:rotation_trainer_app/widgets/ability_button.dart';

/// Field-by-field config equality. No value-equality on the engine structs, so
/// this is the M3 fidelity oracle: `closeTo` for doubles, `==` for enums/lists.
void expectConfigEquals(SimConfig a, SimConfig b) {
  expect(a.gcd, closeTo(b.gcd, 1e-9));
  expect(a.fixedDt, closeTo(b.fixedDt, 1e-9));
  expect(a.priority, b.priority);

  expect(a.abilities.keys.toSet(), b.abilities.keys.toSet());
  for (final id in b.abilities.keys) {
    final x = a.abilities[id]!;
    final y = b.abilities[id]!;
    expect(x.id, y.id);
    expect(x.name, y.name);
    expect(x.castTime, closeTo(y.castTime, 1e-9));
    expect(x.onGcd, y.onGcd);
    expect(x.cooldown, closeTo(y.cooldown, 1e-9));
    expect(x.cost, y.cost);
    expect(x.costResource, y.costResource);
    expect(x.appliesDebuff, y.appliesDebuff);
    expect(x.appliesAura, y.appliesAura);
    expect(x.instantIfAura, y.instantIfAura);
    expect(x.consumesAura, y.consumesAura);
    expect(x.damage, y.damage);
    expect(x.generatesShard, y.generatesShard);
    expect(x.isChannel, y.isChannel);
    expect(x.channelDuration, closeTo(y.channelDuration, 1e-9));
  }

  expect(a.debuffs.keys.toSet(), b.debuffs.keys.toSet());
  for (final id in b.debuffs.keys) {
    final x = a.debuffs[id]!;
    final y = b.debuffs[id]!;
    expect(x.id, y.id);
    expect(x.name, y.name);
    expect(x.duration, closeTo(y.duration, 1e-9));
    expect(x.tickInterval, closeTo(y.tickInterval, 1e-9));
    expect(x.pandemic, closeTo(y.pandemic, 1e-9));
    expect(x.tickDamage, y.tickDamage);
    expect(x.onTickShardChance, closeTo(y.onTickShardChance, 1e-9));
    expect(x.onTickShardAmount, y.onTickShardAmount);
    expect(x.onTickAuraChance, closeTo(y.onTickAuraChance, 1e-9));
    expect(x.grantsAura, y.grantsAura);
    expect(x.damageAmp, closeTo(y.damageAmp, 1e-9));
  }

  expect(a.auras.keys.toSet(), b.auras.keys.toSet());
  for (final id in b.auras.keys) {
    final x = a.auras[id]!;
    final y = b.auras[id]!;
    expect(x.id, y.id);
    expect(x.name, y.name);
    expect(x.duration, closeTo(y.duration, 1e-9));
    expect(x.maxStacks, y.maxStacks);
  }

  expect(a.resources.keys.toSet(), b.resources.keys.toSet());
  for (final id in b.resources.keys) {
    final x = a.resources[id]!;
    final y = b.resources[id]!;
    expect(x.id, y.id);
    expect(x.min, y.min);
    expect(x.max, y.max);
    expect(x.startAt, y.startAt);
  }
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('the bundled JSON reproduces afflictionSimplified() field-for-field',
      () async {
    final json =
        await rootBundle.loadString('assets/templates/affliction_simple.json');
    final loaded = loadTemplate(json);
    expectConfigEquals(loaded, afflictionSimplified());
  });

  testWidgets('the app boots from the loaded config and renders all 5 abilities',
      (tester) async {
    tester.view.physicalSize = const Size(1080, 2400);
    tester.view.devicePixelRatio = 3.0;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    // rootBundle.loadString does real async I/O, which never resolves inside
    // testWidgets' fake-async zone — load it on the real event loop.
    final config = await tester.runAsync(() async {
      final json = await rootBundle
          .loadString('assets/templates/affliction_simple.json');
      return loadTemplate(json);
    });

    await tester.pumpWidget(RotationTrainerApp(config: config));
    await tester.pump(const Duration(milliseconds: 16));

    expect(find.byType(AbilityButton), findsNWidgets(5));
  });
}
