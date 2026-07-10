import 'abilities.dart';
import 'auras.dart';
import 'cast.dart';
import 'cast_result.dart';
import 'cooldowns.dart';
import 'debuffs.dart';
import 'events.dart';
import 'game_state.dart';
import 'ids.dart';
import 'priority.dart';
import 'resources.dart';
import 'rng.dart';
import 'stats.dart';

/// Mutable internal representation of an in-progress cast.
class _Cast {
  _Cast({
    required this.ability,
    required this.kind,
    required this.startedAt,
    required this.endsAt,
    required this.clipped,
  });

  final AbilityId ability;
  final CastKind kind;
  final double startedAt;
  final double endsAt;
  final bool clipped;
}

/// Mutable internal representation of a debuff.
class _Debuff {
  _Debuff({
    required this.appliedAt,
    required this.expiresAt,
    required this.nextTickAt,
  });

  double appliedAt;
  double expiresAt;
  double nextTickAt;
}

/// Mutable internal representation of an aura.
class _Aura {
  _Aura({required this.expiresAt, required this.stacks});

  double expiresAt;
  int stacks;
}

/// The headless rotation engine.
///
/// Pure Dart — no Flutter. Holds mutable internals, advances on a fixed
/// timestep, and exposes immutable [GameState] snapshots plus per-tick
/// [SimEvent] lists. `cast()`/`canCast()` share one `_validate`, so they can
/// never disagree.
class Engine {
  Engine({required SimConfig config, SimRng? rng, double pullSeconds = 60})
      : _config = config,
        _rng = rng ?? SeededRng(_defaultSeed),
        _dt = config.fixedDt,
        _pullSeconds = pullSeconds,
        _endsAt = pullSeconds {
    _initState();
    _seedUptime();
    _state = _snapshot();
  }

  static const int _defaultSeed = 42;

  /// Accumulator tolerance: absorbs float noise so calling `tick(dt)` exactly
  /// performs exactly one sub-step (never a skipped or doubled step).
  static const double _accEps = 1e-9;

  /// Boundary tolerance for tick / expiry / cooldown / gcd comparisons. Large
  /// relative to clock drift (~1e-13 over thousands of steps) but far smaller
  /// than one sub-step, so a tick landing exactly on a boundary still fires.
  static const double _eps = 1e-6;

  final SimConfig _config;
  final SimRng _rng;
  final double _dt;

  /// Fixed pull length (practice config, *not* template data). A pull auto-ends
  /// at this many seconds; `reset()` returns `_endsAt` here.
  final double _pullSeconds;

  // ---- mutable internals --------------------------------------------------
  double _now = 0;
  double _acc = 0;
  double _gcdEndsAt = 0;
  int _clipCount = 0;

  // ---- M4 pull lifecycle + stat accumulators ------------------------------
  /// Sim time the pull ends. Starts at [_pullSeconds]; `stop()` shortens it to
  /// `_now` for an early end.
  double _endsAt;
  double _totalDamage = 0;
  final Map<DebuffId, double> _uptimeSeconds = {};
  double _idleSeconds = 0;

  final Map<ResourceId, int> _resourceCurrent = {};
  final Map<ResourceId, int> _resourceOvercap = {};
  final Map<AbilityId, double> _cooldownReadyAt = {};
  final Map<AuraId, _Aura> _auras = {};
  final Map<DebuffId, _Debuff> _debuffs = {};
  _Cast? _cast;

  /// Events produced by instant casts, flushed on the next [tick].
  final List<SimEvent> _pending = [];

  late GameState _state;

  // ---- public API ---------------------------------------------------------

  /// Cached snapshot of the current state.
  GameState get state => _state;

  /// The configuration this engine runs.
  SimConfig get config => _config;

  /// The pull length in seconds (fixed for the pull; `secondsLeft` derives off
  /// this in the UI).
  double get pullSeconds => _pullSeconds;

  /// Whether the pull has ended (reached [_endsAt] or been `stop()`ped).
  bool get isEnded => _now >= _endsAt - _eps;

  /// End-of-pull statistics built from the current accumulators. Cheap enough
  /// to read every frame for the live DPS-equivalent line.
  SessionStats get stats {
    var overcap = 0;
    for (final r in _state.resources.values) {
      overcap += r.overcapWasted;
    }
    return SessionStats(
      elapsed: _now,
      totalDamage: _totalDamage,
      uptimeSeconds: Map<DebuffId, double>.of(_uptimeSeconds),
      idleSeconds: _idleSeconds,
      overcap: overcap,
      clips: _clipCount,
      gcd: _config.gcd,
    );
  }

  /// End the pull early (Stop button): freeze the clock here so `isEnded` holds
  /// and the accumulators stop growing on the next tick.
  void stop() => _endsAt = _now;

  /// Restart from a genuine fresh state — clears the clock, the live
  /// aura/debuff/cooldown maps, the in-progress cast, buffered events, and every
  /// stat accumulator, then reseeds resources and re-snapshots.
  void reset() {
    _now = 0;
    _acc = 0;
    _gcdEndsAt = 0;
    _clipCount = 0;
    _totalDamage = 0;
    _idleSeconds = 0;
    _endsAt = _pullSeconds;
    _uptimeSeconds.clear();
    _debuffs.clear();
    _auras.clear();
    _cooldownReadyAt.clear();
    _cast = null;
    _pending.clear();
    _initState();
    _seedUptime();
    _state = _snapshot();
  }

  /// Advance by a render frame [frameDt]; accumulate into fixed sub-steps.
  /// Returns all events produced (including any buffered from instant casts).
  List<SimEvent> tick(double frameDt) {
    final events = <SimEvent>[];
    if (_pending.isNotEmpty) {
      events.addAll(_pending);
      _pending.clear();
    }
    // Once ended, freeze: flush buffered events but advance nothing.
    if (isEnded) {
      _state = _snapshot();
      return events;
    }
    _acc += frameDt;
    while (_acc >= _dt - _accEps) {
      // Clamp the final sub-step to the pull boundary: take a partial step
      // landing on `_endsAt`, then snap `_now` there to kill float drift so
      // `elapsed == pullSeconds` holds under `==` and the accumulators freeze.
      if (_now + _dt >= _endsAt - _eps) {
        final remaining = _endsAt - _now;
        if (remaining > 0) _step(remaining, events);
        _now = _endsAt;
        _acc = 0;
        break;
      }
      _step(_dt, events);
      _acc -= _dt;
    }
    _state = _snapshot();
    return events;
  }

  /// Headless test entry point — advance by [seconds] with no Ticker.
  List<SimEvent> advanceBy(double seconds) => tick(seconds);

  /// Validate then (if allowed) start/resolve the cast. Never throws.
  CastResult cast(AbilityId id) {
    final reason = _validate(id);
    if (reason != null) return CastRejected(reason);
    final def = _config.abilities[id]!;

    // Clip an in-progress hard cast when starting a new on-GCD ability (the
    // GCD is already free here, else _validate would have returned gcdActive).
    var clipped = false;
    if (_cast != null && _cast!.kind == CastKind.hardCast && def.onGcd) {
      _pending.add(CastClipped(at: _now, ability: _cast!.ability));
      _clipCount++;
      _cast = null;
      clipped = true;
    }

    if (def.cooldown > 0) {
      _cooldownReadyAt[id] = _now + def.cooldown;
    }

    final CastResolution resolution;
    if (def.isChannel) {
      _cast = _Cast(
        ability: id,
        kind: CastKind.channel,
        startedAt: _now,
        endsAt: _now + def.channelDuration,
        clipped: clipped,
      );
      resolution = CastResolution.channelStarted;
    } else if (_isInstant(def)) {
      final consumesAura =
          def.consumesAura != null && _auraActive(def.consumesAura!);
      _applyAbility(def, _pending, consumesAura: consumesAura);
      resolution = CastResolution.instant;
    } else {
      _cast = _Cast(
        ability: id,
        kind: CastKind.hardCast,
        startedAt: _now,
        endsAt: _now + def.castTime,
        clipped: clipped,
      );
      resolution = CastResolution.castStarted;
    }

    if (def.onGcd) _gcdEndsAt = _now + _config.gcd;
    _state = _snapshot();
    return CastAccepted(resolution);
  }

  /// Pure predicate mirroring [cast]'s gate — null means castable.
  CastRejectReason? canCast(AbilityId id) => _validate(id);

  /// Next priority ability per the simplified list. Pure read.
  AbilityId? advise() => advisePriority(_state, _config);

  // ---- validation ---------------------------------------------------------

  CastRejectReason? _validate(AbilityId id) {
    final def = _config.abilities[id];
    if (def == null) return CastRejectReason.unknownAbility;

    final readyAt = _cooldownReadyAt[id];
    if (readyAt != null && _now < readyAt - _eps) {
      return CastRejectReason.onCooldown;
    }

    if (def.costResource != null && def.cost > 0) {
      final have = _resourceCurrent[def.costResource] ?? 0;
      if (have < def.cost) return CastRejectReason.insufficientResource;
    }

    if (def.onGcd && _now < _gcdEndsAt - _eps) {
      return CastRejectReason.gcdActive;
    }

    if (_cast != null) {
      if (def.onGcd) {
        // On-GCD ability with the GCD free: a hard cast can be clipped
        // (allowed), but a channel cannot be — channeling blocks.
        if (_cast!.kind == CastKind.channel) {
          return CastRejectReason.channeling;
        }
      } else {
        // Off-GCD ability cannot start while a cast/channel is in progress.
        return _cast!.kind == CastKind.channel
            ? CastRejectReason.channeling
            : CastRejectReason.alreadyCasting;
      }
    }

    return null;
  }

  bool _isInstant(AbilityDef def) {
    if (def.castTime <= 0) return true;
    return def.instantIfAura != null && _auraActive(def.instantIfAura!);
  }

  // ---- fixed-step simulation ----------------------------------------------

  /// One fixed sub-step. The spec's 7-step order; RNG is consumed only in the
  /// DoT-tick step, exactly once per proc-eligible tick. DoT ticks are
  /// processed before fall-off so a tick landing exactly at expiry still lands
  /// (matching WoW's final tick), then the debuff expires the same step.
  void _step(double dt, List<SimEvent> events) {
    // 1. advance clock; resolve a completed cast/channel.
    _now += dt;
    final cast = _cast;
    if (cast != null && _now >= cast.endsAt - _eps) {
      // A hard cast only began because its aura was down at cast start (else it
      // would have resolved instantly), so a resolving hard cast never
      // consumes an aura — instants handle consumption immediately.
      _applyAbility(_config.abilities[cast.ability]!, events,
          consumesAura: false);
      _cast = null;
    }

    // 2. channels tick on cadence — no channel in the M1 roster; path present.

    // 3. + 4. DoT ticks (with proc side effects), then expiry.
    _tickDots(events);
    _expire(events);

    // 5. regen continuous resources — shards are discrete; overcap is counted
    //    at generation time, so nothing to do here in M1.

    // 6. GCD — pure timestamp compare, surfaced via GameState.isGcdActive.

    // 7. proc hook for non-tick triggers — intentionally empty in M1.

    // ---- M4 stat accumulators ------------------------------------------
    // Whole-`dt` attribution: a debuff active this sub-step earns the full dt,
    // so uptime carries ≤ one-tick (16.7 ms) rounding — fine for practice
    // stats. `_debuffs` is pruned by `_expire` above, so this counts only
    // debuffs still up at end of step.
    for (final id in _debuffs.keys) {
      _uptimeSeconds[id] = (_uptimeSeconds[id] ?? 0) + dt;
    }
    // Idle = a sub-step you could have filled (GCD free, not casting) but
    // didn't — the wasted-GCD signal. Mirrors the cast gate's GCD threshold.
    final gcdActive = _now < _gcdEndsAt - _eps;
    if (!gcdActive && _cast == null) {
      _idleSeconds += dt;
    }
  }

  void _tickDots(List<SimEvent> events) {
    for (final entry in _debuffs.entries) {
      final id = entry.key;
      final d = entry.value;
      final def = _config.debuffs[id]!;
      if (def.tickInterval <= 0) continue;

      while (d.nextTickAt <= _now + _eps &&
          d.nextTickAt <= d.expiresAt + _eps) {
        final tickAt = d.nextTickAt;

        if (def.tickDamage > 0) {
          final amount = def.tickDamage * _damageMultiplier();
          _totalDamage += amount;
          events.add(DamageEvent(at: tickAt, amount: amount, debuff: id));
        }

        // Exactly one rng.chance() per proc-eligible tick, in tick order.
        if (def.onTickShardChance > 0) {
          if (_rng.chance(def.onTickShardChance)) {
            _generateShards(def.onTickShardAmount, events, at: tickAt);
          }
        } else if (def.onTickAuraChance > 0 && def.grantsAura != null) {
          if (_rng.chance(def.onTickAuraChance)) {
            _grantAura(_config.auras[def.grantsAura]!, events, at: tickAt);
          }
        }

        d.nextTickAt += def.tickInterval;
      }
    }
  }

  void _expire(List<SimEvent> events) {
    _debuffs.removeWhere((id, d) {
      if (_now + _eps >= d.expiresAt) {
        events.add(DotExpired(at: _now, debuff: id));
        return true;
      }
      return false;
    });
    _auras.removeWhere((id, a) => _now + _eps >= a.expiresAt || a.stacks <= 0);
  }

  // ---- effect application -------------------------------------------------

  void _applyAbility(
    AbilityDef def,
    List<SimEvent> events, {
    required bool consumesAura,
  }) {
    // Spend resource cost.
    if (def.costResource != null && def.cost > 0) {
      final res = def.costResource!;
      final resDef = _config.resources[res]!;
      final next = (_resourceCurrent[res]! - def.cost);
      _resourceCurrent[res] = next < resDef.min ? resDef.min : next;
    }

    // Consume the aura that made this instant (e.g. Nightfall → Shadow Bolt).
    if (consumesAura && def.consumesAura != null) {
      _consumeAura(def.consumesAura!);
    }

    if (def.damage > 0) {
      final amount = def.damage * _damageMultiplier();
      _totalDamage += amount;
      events.add(DamageEvent(at: _now, amount: amount, ability: def.id));
    }

    if (def.generatesShard > 0) {
      _generateShards(def.generatesShard, events, at: _now);
    }

    if (def.appliesDebuff != null) {
      _applyOrRefreshDebuff(_config.debuffs[def.appliesDebuff]!, events);
    }

    if (def.appliesAura != null) {
      _grantAura(_config.auras[def.appliesAura]!, events, at: _now);
    }
  }

  void _applyOrRefreshDebuff(DebuffDef def, List<SimEvent> events) {
    final existing = _debuffs[def.id];
    final active = existing != null && existing.expiresAt > _now;

    final double newExpiry;
    if (active) {
      final remaining = existing.expiresAt - _now;
      final window = def.pandemic * def.duration;
      if (remaining <= window) {
        // Inside the pandemic window: extend, capped at 1.3 * duration.
        final extended = remaining + def.duration;
        final cap = 1.3 * def.duration;
        newExpiry = _now + (extended > cap ? cap : extended);
      } else {
        // Outside the window: a clip — set the full base duration.
        newExpiry = _now + def.duration;
      }
    } else {
      newExpiry = _now + def.duration;
    }

    final double nextTickAt;
    if (def.tickInterval <= 0) {
      nextTickAt = double.infinity;
    } else if (active) {
      // Refresh keeps the rolling tick cadence (modern DoT behaviour).
      nextTickAt = existing.nextTickAt;
    } else {
      nextTickAt = _now + def.tickInterval;
    }

    _debuffs[def.id] = _Debuff(
      appliedAt: _now,
      expiresAt: newExpiry,
      nextTickAt: nextTickAt,
    );
    events.add(DotApplied(
      at: _now,
      debuff: def.id,
      refreshed: active,
      expiresAt: newExpiry,
    ));
  }

  void _grantAura(AuraDef def, List<SimEvent> events, {required double at}) {
    final existing = _auras[def.id];
    final stacks = existing == null
        ? 1
        : (existing.stacks + 1).clamp(0, def.maxStacks);
    _auras[def.id] = _Aura(expiresAt: at + def.duration, stacks: stacks);
    events.add(AuraGranted(at: at, aura: def.id, stacks: stacks));
  }

  void _consumeAura(AuraId id) {
    final a = _auras[id];
    if (a == null) return;
    final next = a.stacks - 1;
    if (next <= 0) {
      _auras.remove(id);
    } else {
      a.stacks = next;
    }
  }

  void _generateShards(int amount, List<SimEvent> events, {required double at}) {
    if (amount <= 0) return;
    const id = ResourceId.soulShard;
    final def = _config.resources[id];
    if (def == null) return;
    var cur = _resourceCurrent[id] ?? 0;
    for (var i = 0; i < amount; i++) {
      if (cur < def.max) {
        cur++;
        events.add(ShardGenerated(at: at, amount: 1, overcapped: false));
      } else {
        _resourceOvercap[id] = (_resourceOvercap[id] ?? 0) + 1;
        events.add(ShardGenerated(at: at, amount: 1, overcapped: true));
      }
    }
    _resourceCurrent[id] = cur;
  }

  double _damageMultiplier() {
    var mult = 1.0;
    for (final id in _debuffs.keys) {
      mult += _config.debuffs[id]!.damageAmp;
    }
    return mult;
  }

  bool _auraActive(AuraId id) {
    final a = _auras[id];
    return a != null && a.stacks > 0 && a.expiresAt > _now;
  }

  // ---- snapshot -----------------------------------------------------------

  void _initState() {
    for (final def in _config.resources.values) {
      _resourceCurrent[def.id] = def.startAt;
      _resourceOvercap[def.id] = 0;
    }
  }

  /// Seed the uptime map with *every* config debuff at 0, so a never-applied
  /// DoT is still graded (and rendered) rather than silently absent.
  void _seedUptime() {
    _uptimeSeconds.clear();
    for (final id in _config.debuffs.keys) {
      _uptimeSeconds[id] = 0;
    }
  }

  GameState _snapshot() {
    final resources = <ResourceId, ResourceState>{};
    for (final def in _config.resources.values) {
      resources[def.id] = ResourceState(
        current: _resourceCurrent[def.id] ?? def.startAt,
        min: def.min,
        max: def.max,
        overcapWasted: _resourceOvercap[def.id] ?? 0,
      );
    }

    final cooldowns = <AbilityId, CooldownState>{};
    for (final def in _config.abilities.values) {
      if (def.cooldown > 0) {
        cooldowns[def.id] =
            CooldownState(readyAt: _cooldownReadyAt[def.id] ?? 0);
      }
    }

    final auras = <AuraId, AuraState>{
      for (final e in _auras.entries)
        e.key: AuraState(expiresAt: e.value.expiresAt, stacks: e.value.stacks),
    };

    final debuffs = <DebuffId, DebuffState>{
      for (final e in _debuffs.entries)
        e.key: DebuffState(
          appliedAt: e.value.appliedAt,
          expiresAt: e.value.expiresAt,
          nextTickAt: e.value.nextTickAt,
        ),
    };

    final c = _cast;
    final castState = c == null
        ? null
        : CastState(
            ability: c.ability,
            kind: c.kind,
            startedAt: c.startedAt,
            endsAt: c.endsAt,
            clipped: c.clipped,
          );

    return GameState(
      time: _now,
      gcdEndsAt: _gcdEndsAt,
      clipCount: _clipCount,
      resources: resources,
      cooldowns: cooldowns,
      auras: auras,
      debuffs: debuffs,
      cast: castState,
    );
  }
}
