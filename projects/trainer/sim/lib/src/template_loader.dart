// Pure-Dart JSON → [SimConfig] loader. This is the "single seam" [ids.dart]'s
// doc comment anticipates: the wire-format spellings ("ua", "shadowbolt") live
// here in private const maps, never in the engine core.
//
// Imports only dart:convert + the engine's pure data layer — no package:flutter,
// no dart:io — so it parses a String and its tests run under `dart test`.

import 'dart:convert';

import 'abilities.dart';
import 'ids.dart';

/// String → enum tables. The wire format is authored by hand in the template
/// JSON; the engine speaks enums. Keep the two vocabularies bridged only here.
const _abilityIds = {
  'agony': AbilityId.agony,
  'corruption': AbilityId.corruption,
  'shadowbolt': AbilityId.shadowBolt,
  'ua': AbilityId.unstableAffliction,
  'haunt': AbilityId.haunt,
};
const _debuffIds = {
  'agony': DebuffId.agony,
  'corruption': DebuffId.corruption,
  'haunt': DebuffId.haunt,
};
const _auraIds = {'nightfall': AuraId.nightfall};
const _resourceIds = {'soulShard': ResourceId.soulShard};

/// Thrown for any invalid template input. [path] is a best-effort breadcrumb
/// into the JSON (e.g. "abilities[2].applies.debuff").
class TemplateException implements Exception {
  TemplateException(this.message, [this.path]);

  final String message;
  final String? path;

  @override
  String toString() =>
      'TemplateException: $message${path == null ? '' : ' (at $path)'}';
}

/// Parse + validate a template JSON document into the exact [SimConfig] the
/// engine consumes. Throws [TemplateException] on any invalid input.
///
/// Two phases: (1) build the four collections with typed accessors, (2)
/// cross-check every id reference against the parsed collections — this is what
/// catches "Shadow Bolt consumes nightfall but no nightfall aura defined".
SimConfig loadTemplate(String json) {
  final Object? decoded;
  try {
    decoded = jsonDecode(json);
  } on FormatException catch (e) {
    throw TemplateException('invalid JSON: ${e.message}');
  }
  if (decoded is! Map) {
    throw TemplateException('top-level value must be an object', r'$');
  }
  final root = decoded;

  // Deferred reference checks (phase 2): each closure captures its own path and
  // runs once all collections exist.
  final deferred = <void Function()>[];

  // Declared up front so phase-2 closures built while parsing abilities can
  // close over the (still-empty) debuff/aura collections that are filled later.
  final resources = <ResourceId, ResourceDef>{};
  final abilities = <AbilityId, AbilityDef>{};
  final debuffs = <DebuffId, DebuffDef>{};
  final auras = <AuraId, AuraDef>{};

  // --- resources -----------------------------------------------------------
  final resList = _list(root, 'resources', r'$');
  for (var i = 0; i < resList.length; i++) {
    final path = 'resources[$i]';
    final r = _asObject(resList[i], path);
    final idStr = _str(r, 'id', path);
    final id = _resourceId(idStr, '$path.id');
    if (resources.containsKey(id)) {
      throw TemplateException('duplicate resource id "$idStr"', '$path.id');
    }
    final min = _int(r, 'min', path);
    final max = _int(r, 'max', path);
    final startAt = _int(r, 'startAt', path);
    if (min > max) {
      throw TemplateException('min ($min) > max ($max)', path);
    }
    if (startAt < min || startAt > max) {
      throw TemplateException('startAt ($startAt) out of [$min, $max]', path);
    }
    resources[id] = ResourceDef(id: id, min: min, max: max, startAt: startAt);
  }

  // --- abilities -----------------------------------------------------------
  final abList = _list(root, 'abilities', r'$');
  for (var i = 0; i < abList.length; i++) {
    final path = 'abilities[$i]';
    final a = _asObject(abList[i], path);
    final idStr = _str(a, 'id', path);
    final id = _abilityId(idStr, '$path.id');
    if (abilities.containsKey(id)) {
      throw TemplateException('duplicate ability id "$idStr"', '$path.id');
    }
    final name = _str(a, 'name', path);
    final castTime = _nonNeg(_num(a, 'castTime', path), 'castTime', path);
    final onGcd = _bool(a, 'onGcd', path);
    final cooldown =
        _nonNeg(_num(a, 'cooldown', path, dflt: 0), 'cooldown', path);

    // cost: { soulShard: 1 } — a single-key resource map.
    var cost = 0;
    ResourceId? costResource;
    if (a.containsKey('cost')) {
      final costMap = _asObject(a['cost'], '$path.cost');
      final entry = _singleEntry(costMap, '$path.cost');
      final wire = entry.key;
      costResource = _resourceId(wire, '$path.cost');
      cost = _intValue(entry.value, '$path.cost.$wire');
      final cr = costResource;
      deferred.add(() {
        if (!resources.containsKey(cr)) {
          throw TemplateException(
              'cost references undefined resource "$wire"', '$path.cost');
        }
      });
    }

    // applies: { debuff: ... } and/or { aura: ... }
    DebuffId? appliesDebuff;
    AuraId? appliesAura;
    if (a.containsKey('applies')) {
      final applies = _asObject(a['applies'], '$path.applies');
      if (applies.containsKey('debuff')) {
        final wire = _str(applies, 'debuff', '$path.applies');
        appliesDebuff = _debuffId(wire, '$path.applies.debuff');
        final d = appliesDebuff;
        deferred.add(() {
          if (!debuffs.containsKey(d)) {
            throw TemplateException(
                'applies undefined debuff "$wire"', '$path.applies.debuff');
          }
        });
      }
      if (applies.containsKey('aura')) {
        final wire = _str(applies, 'aura', '$path.applies');
        appliesAura = _auraId(wire, '$path.applies.aura');
        final au = appliesAura;
        deferred.add(() {
          if (!auras.containsKey(au)) {
            throw TemplateException(
                'applies undefined aura "$wire"', '$path.applies.aura');
          }
        });
      }
    }

    AuraId? instantIfAura;
    if (a.containsKey('instantIfAura')) {
      final wire = _str(a, 'instantIfAura', path);
      instantIfAura = _auraId(wire, '$path.instantIfAura');
      final au = instantIfAura;
      deferred.add(() {
        if (!auras.containsKey(au)) {
          throw TemplateException(
              'instantIfAura references undefined aura "$wire"',
              '$path.instantIfAura');
        }
      });
    }
    AuraId? consumesAura;
    if (a.containsKey('consumesAura')) {
      final wire = _str(a, 'consumesAura', path);
      consumesAura = _auraId(wire, '$path.consumesAura');
      final au = consumesAura;
      deferred.add(() {
        if (!auras.containsKey(au)) {
          throw TemplateException(
              'consumesAura references undefined aura "$wire"',
              '$path.consumesAura');
        }
      });
    }

    // effect: { damage: N, generates: { soulShard: N } }
    var damage = 0;
    var generatesShard = 0;
    if (a.containsKey('effect')) {
      final effect = _asObject(a['effect'], '$path.effect');
      damage = _int(effect, 'damage', '$path.effect', dflt: 0);
      if (effect.containsKey('generates')) {
        final gen = _asObject(effect['generates'], '$path.effect.generates');
        final entry = _singleEntry(gen, '$path.effect.generates');
        final wire = entry.key;
        final genRes = _resourceId(wire, '$path.effect.generates');
        generatesShard =
            _intValue(entry.value, '$path.effect.generates.$wire');
        deferred.add(() {
          if (!resources.containsKey(genRes)) {
            throw TemplateException(
                'effect generates undefined resource "$wire"',
                '$path.effect.generates');
          }
        });
      }
    }

    abilities[id] = AbilityDef(
      id: id,
      name: name,
      castTime: castTime,
      onGcd: onGcd,
      cooldown: cooldown,
      cost: cost,
      costResource: costResource,
      appliesDebuff: appliesDebuff,
      appliesAura: appliesAura,
      instantIfAura: instantIfAura,
      consumesAura: consumesAura,
      damage: damage,
      generatesShard: generatesShard,
    );
  }

  // --- debuffs -------------------------------------------------------------
  final dbList = _list(root, 'debuffs', r'$');
  for (var i = 0; i < dbList.length; i++) {
    final path = 'debuffs[$i]';
    final d = _asObject(dbList[i], path);
    final idStr = _str(d, 'id', path);
    final id = _debuffId(idStr, '$path.id');
    if (debuffs.containsKey(id)) {
      throw TemplateException('duplicate debuff id "$idStr"', '$path.id');
    }
    final name = _str(d, 'name', path);
    final duration = _nonNeg(_num(d, 'duration', path), 'duration', path);
    final tickInterval = _nonNeg(
        _num(d, 'tickInterval', path, dflt: 0), 'tickInterval', path);
    final pandemic =
        _prob(_num(d, 'pandemic', path, dflt: 0.3), 'pandemic', path);
    final damageAmp = _num(d, 'damageAmp', path, dflt: 0);
    final tickDamage = _int(d, 'tickDamage', path, dflt: 0);

    // onTick is a tagged union: either { chance, generates: { soulShard: N } }
    // or { chance, grantsAura: "nightfall" }.
    var onTickShardChance = 0.0;
    var onTickShardAmount = 0;
    var onTickAuraChance = 0.0;
    AuraId? grantsAura;
    if (d.containsKey('onTick')) {
      final onTick = _asObject(d['onTick'], '$path.onTick');
      final chance =
          _prob(_num(onTick, 'chance', '$path.onTick'), 'chance', '$path.onTick');
      final hasGen = onTick.containsKey('generates');
      final hasGrant = onTick.containsKey('grantsAura');
      if (hasGen && hasGrant) {
        throw TemplateException(
            'onTick cannot have both generates and grantsAura', '$path.onTick');
      }
      if (hasGen) {
        final gen = _asObject(onTick['generates'], '$path.onTick.generates');
        final entry = _singleEntry(gen, '$path.onTick.generates');
        final wire = entry.key;
        final genRes = _resourceId(wire, '$path.onTick.generates');
        onTickShardChance = chance;
        onTickShardAmount =
            _intValue(entry.value, '$path.onTick.generates.$wire');
        deferred.add(() {
          if (!resources.containsKey(genRes)) {
            throw TemplateException(
                'onTick generates undefined resource "$wire"',
                '$path.onTick.generates');
          }
        });
      } else if (hasGrant) {
        final wire = _str(onTick, 'grantsAura', '$path.onTick');
        grantsAura = _auraId(wire, '$path.onTick.grantsAura');
        onTickAuraChance = chance;
        final au = grantsAura;
        deferred.add(() {
          if (!auras.containsKey(au)) {
            throw TemplateException(
                'onTick grants undefined aura "$wire"', '$path.onTick.grantsAura');
          }
        });
      } else {
        throw TemplateException(
            'onTick must have either generates or grantsAura', '$path.onTick');
      }
    }

    debuffs[id] = DebuffDef(
      id: id,
      name: name,
      duration: duration,
      tickInterval: tickInterval,
      pandemic: pandemic,
      tickDamage: tickDamage,
      onTickShardChance: onTickShardChance,
      onTickShardAmount: onTickShardAmount,
      onTickAuraChance: onTickAuraChance,
      grantsAura: grantsAura,
      damageAmp: damageAmp,
    );
  }

  // --- auras ---------------------------------------------------------------
  final auList = _list(root, 'auras', r'$');
  for (var i = 0; i < auList.length; i++) {
    final path = 'auras[$i]';
    final au = _asObject(auList[i], path);
    final idStr = _str(au, 'id', path);
    final id = _auraId(idStr, '$path.id');
    if (auras.containsKey(id)) {
      throw TemplateException('duplicate aura id "$idStr"', '$path.id');
    }
    final name = _str(au, 'name', path);
    final duration = _nonNeg(_num(au, 'duration', path), 'duration', path);
    final maxStacks = _int(au, 'maxStacks', path);
    if (maxStacks < 1) {
      throw TemplateException('maxStacks ($maxStacks) must be >= 1', path);
    }
    auras[id] = AuraDef(
      id: id,
      name: name,
      duration: duration,
      maxStacks: maxStacks,
    );
  }

  // --- priority ------------------------------------------------------------
  final priority = <AbilityId>[];
  final priList = _list(root, 'priority', r'$');
  for (var i = 0; i < priList.length; i++) {
    final p = 'priority[$i]';
    final v = priList[i];
    if (v is! String) {
      throw TemplateException('priority entry must be a string', p);
    }
    final id = _abilityId(v, p);
    deferred.add(() {
      if (!abilities.containsKey(id)) {
        throw TemplateException(
            'priority entry "$v" is not a defined ability', p);
      }
    });
    priority.add(id);
  }

  final gcd = _nonNeg(_num(root, 'gcd', r'$', dflt: 1.5), 'gcd', r'$');

  // --- phase 2: run deferred cross-reference checks ------------------------
  for (final check in deferred) {
    check();
  }

  return SimConfig(
    abilities: abilities,
    debuffs: debuffs,
    auras: auras,
    resources: resources,
    priority: priority,
    gcd: gcd,
  );
}

// ---------------------------------------------------------------------------
// Typed accessors — each throws TemplateException with a path-tagged message.
// ---------------------------------------------------------------------------

Map _asObject(Object? v, String path) {
  if (v is! Map) throw TemplateException('expected an object', path);
  return v;
}

List _list(Map m, String key, String path) {
  final v = m[key];
  if (v == null) throw TemplateException('missing required key "$key"', path);
  if (v is! List) throw TemplateException('"$key" must be an array', '$path.$key');
  return v;
}

String _str(Map m, String key, String path) {
  final v = m[key];
  if (v == null) throw TemplateException('missing required key "$key"', path);
  if (v is! String) {
    throw TemplateException('"$key" must be a string', '$path.$key');
  }
  return v;
}

bool _bool(Map m, String key, String path) {
  final v = m[key];
  if (v == null) throw TemplateException('missing required key "$key"', path);
  if (v is! bool) {
    throw TemplateException('"$key" must be a boolean', '$path.$key');
  }
  return v;
}

/// num-tolerant double reader: JSON `2` and `2.0` are both valid.
double _num(Map m, String key, String path, {double? dflt}) {
  final v = m[key];
  if (v == null) {
    if (dflt != null) return dflt;
    throw TemplateException('missing required key "$key"', path);
  }
  if (v is num) return v.toDouble();
  throw TemplateException('"$key" must be a number', '$path.$key');
}

int _int(Map m, String key, String path, {int? dflt}) {
  final v = m[key];
  if (v == null) {
    if (dflt != null) return dflt;
    throw TemplateException('missing required key "$key"', path);
  }
  if (v is! int) {
    throw TemplateException('"$key" must be an integer', '$path.$key');
  }
  return v;
}

int _intValue(Object? v, String path) {
  if (v is! int) throw TemplateException('value must be an integer', path);
  return v;
}

MapEntry<String, Object?> _singleEntry(Map m, String path) {
  if (m.length != 1) {
    throw TemplateException('expected exactly one key', path);
  }
  final e = m.entries.first;
  return MapEntry(e.key as String, e.value);
}

double _nonNeg(double v, String what, String path) {
  if (v < 0) throw TemplateException('$what ($v) must be >= 0', path);
  return v;
}

double _prob(double v, String what, String path) {
  if (v < 0 || v > 1) {
    throw TemplateException('$what ($v) must be in [0, 1]', path);
  }
  return v;
}

AbilityId _abilityId(String s, String path) =>
    _abilityIds[s] ?? (throw TemplateException('unknown ability id "$s"', path));
DebuffId _debuffId(String s, String path) =>
    _debuffIds[s] ?? (throw TemplateException('unknown debuff id "$s"', path));
AuraId _auraId(String s, String path) =>
    _auraIds[s] ?? (throw TemplateException('unknown aura id "$s"', path));
ResourceId _resourceId(String s, String path) =>
    _resourceIds[s] ??
    (throw TemplateException('unknown resource id "$s"', path));
