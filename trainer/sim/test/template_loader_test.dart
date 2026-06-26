import 'dart:convert';

import 'package:rotation_sim/sim.dart';
import 'package:test/test.dart';

/// A minimal but fully valid template, kept as a Dart map so each error-class
/// test can mutate one field and re-encode. Deliberately NOT a copy of the
/// shipped asset — avoids a second drift surface (the asset is verified for
/// fidelity by the app's `flutter test`).
Map<String, dynamic> _validTemplate() => {
      'id': 'test',
      'name': 'Test',
      'gcd': 1.5,
      'resources': [
        {'id': 'soulShard', 'min': 0, 'max': 5, 'startAt': 3},
      ],
      'abilities': [
        {
          'id': 'agony',
          'name': 'Agony',
          'castTime': 0,
          'onGcd': true,
          'applies': {'debuff': 'agony'},
        },
        {
          'id': 'shadowbolt',
          'name': 'Shadow Bolt',
          'castTime': 2.0,
          'onGcd': true,
          'instantIfAura': 'nightfall',
          'consumesAura': 'nightfall',
          'effect': {'damage': 100},
        },
        {
          'id': 'ua',
          'name': 'Unstable Affliction',
          'castTime': 0,
          'onGcd': true,
          'cost': {'soulShard': 1},
          'effect': {'damage': 220},
        },
      ],
      'debuffs': [
        {
          'id': 'agony',
          'name': 'Agony',
          'duration': 18,
          'tickInterval': 2,
          'pandemic': 0.3,
          'tickDamage': 10,
          'onTick': {
            'chance': 0.5,
            'generates': {'soulShard': 1},
          },
        },
        {
          'id': 'corruption',
          'name': 'Corruption',
          'duration': 14,
          'tickInterval': 2,
          'tickDamage': 8,
          'onTick': {'chance': 0.15, 'grantsAura': 'nightfall'},
        },
      ],
      'auras': [
        {'id': 'nightfall', 'name': 'Nightfall', 'duration': 12, 'maxStacks': 2},
      ],
      'priority': ['agony', 'ua', 'shadowbolt'],
    };

/// Encode a template, optionally after applying [mutate].
String _json([void Function(Map<String, dynamic>) mutate = _noop]) {
  final t = _validTemplate();
  mutate(t);
  return jsonEncode(t);
}

void _noop(Map<String, dynamic> _) {}

void main() {
  group('happy path', () {
    test('parses to the expected collections, gcd, and priority', () {
      final c = loadTemplate(_json());

      expect(c.gcd, 1.5);
      expect(c.priority, [
        AbilityId.agony,
        AbilityId.unstableAffliction,
        AbilityId.shadowBolt,
      ]);
      expect(c.abilities.keys.toSet(), {
        AbilityId.agony,
        AbilityId.unstableAffliction,
        AbilityId.shadowBolt,
      });
      expect(c.debuffs.keys.toSet(), {DebuffId.agony, DebuffId.corruption});
      expect(c.auras.keys.toSet(), {AuraId.nightfall});
      expect(c.resources.keys.toSet(), {ResourceId.soulShard});
    });

    test('maps fields onto the engine structs', () {
      final c = loadTemplate(_json());

      final ua = c.abilities[AbilityId.unstableAffliction]!;
      expect(ua.cost, 1);
      expect(ua.costResource, ResourceId.soulShard);
      expect(ua.damage, 220);

      final sb = c.abilities[AbilityId.shadowBolt]!;
      expect(sb.castTime, 2.0);
      expect(sb.instantIfAura, AuraId.nightfall);
      expect(sb.consumesAura, AuraId.nightfall);

      final agony = c.debuffs[DebuffId.agony]!;
      expect(agony.tickDamage, 10);
      expect(agony.onTickShardChance, 0.5);
      expect(agony.onTickShardAmount, 1);

      final corr = c.debuffs[DebuffId.corruption]!;
      expect(corr.onTickAuraChance, 0.15);
      expect(corr.grantsAura, AuraId.nightfall);
      expect(corr.pandemic, 0.3, reason: 'defaulted when omitted');
    });

    test('gcd defaults to 1.5 when omitted', () {
      final c = loadTemplate(_json((t) => t.remove('gcd')));
      expect(c.gcd, 1.5);
    });
  });

  group('lenient on extras', () {
    test('icon/display/unknown top-level keys are ignored', () {
      final json = _json((t) {
        t['spec'] = 'affliction';
        t['class'] = 'warlock';
        t['somethingNew'] = 42;
        (t['abilities'] as List).first['icon'] = 'spell_whatever';
        (t['resources'] as List).first['display'] = 'pips';
      });
      expect(() => loadTemplate(json), returnsNormally);
    });
  });

  group('numeric tolerance', () {
    test('tickInterval accepts both int 2 and double 2.0', () {
      final asInt = loadTemplate(_json((t) {
        (t['debuffs'] as List).first['tickInterval'] = 2;
      }));
      final asDouble = loadTemplate(_json((t) {
        (t['debuffs'] as List).first['tickInterval'] = 2.0;
      }));
      expect(asInt.debuffs[DebuffId.agony]!.tickInterval, 2.0);
      expect(asDouble.debuffs[DebuffId.agony]!.tickInterval, 2.0);
    });
  });

  group('error classes', () {
    void expectThrows(void Function(Map<String, dynamic>) mutate) {
      expect(() => loadTemplate(_json(mutate)),
          throwsA(isA<TemplateException>()));
    }

    test('invalid JSON', () {
      expect(() => loadTemplate('{ not json'),
          throwsA(isA<TemplateException>()));
    });

    test('non-object top level', () {
      expect(() => loadTemplate('[]'), throwsA(isA<TemplateException>()));
    });

    test('unknown ability id', () {
      expectThrows((t) => (t['abilities'] as List).first['id'] = 'fireball');
    });

    test('unknown debuff id', () {
      expectThrows((t) => (t['debuffs'] as List).first['id'] = 'immolate');
    });

    test('duplicate id', () {
      expectThrows((t) => (t['abilities'] as List)
          .add((t['abilities'] as List).first));
    });

    test('missing required key', () {
      expectThrows((t) => (t['abilities'] as List).first.remove('name'));
    });

    test('wrong type', () {
      expectThrows((t) => (t['abilities'] as List).first['onGcd'] = 'yes');
    });

    test('dangling reference: consumes an aura that is not defined', () {
      expectThrows((t) => t['auras'] = []);
    });

    test('dangling reference: applies a debuff that is not defined', () {
      // Drop corruption from debuffs but keep an ability applying it.
      expectThrows((t) {
        (t['abilities'] as List).add({
          'id': 'corruption',
          'name': 'Corruption',
          'castTime': 0,
          'onGcd': true,
          'applies': {'debuff': 'corruption'},
        });
        (t['debuffs'] as List)
            .removeWhere((d) => (d as Map)['id'] == 'corruption');
      });
    });

    test('priority references an undefined ability', () {
      expectThrows((t) => (t['priority'] as List).add('haunt'));
    });

    test('out-of-range: startAt above max', () {
      expectThrows((t) => (t['resources'] as List).first['startAt'] = 9);
    });

    test('out-of-range: min greater than max', () {
      expectThrows((t) => (t['resources'] as List).first['min'] = 10);
    });

    test('out-of-range: probability above 1', () {
      expectThrows((t) =>
          ((t['debuffs'] as List).first['onTick'] as Map)['chance'] = 1.5);
    });

    test('negative duration', () {
      expectThrows((t) => (t['debuffs'] as List).first['duration'] = -1);
    });

    test('maxStacks below 1', () {
      expectThrows((t) => (t['auras'] as List).first['maxStacks'] = 0);
    });

    test('onTick with both generates and grantsAura', () {
      expectThrows((t) {
        (t['debuffs'] as List).first['onTick'] = {
          'chance': 0.5,
          'generates': {'soulShard': 1},
          'grantsAura': 'nightfall',
        };
      });
    });
  });
}
