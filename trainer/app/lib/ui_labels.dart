import 'package:flutter/material.dart';
import 'package:rotation_sim/sim.dart';

/// Presentation-only mappings (sim enums → display strings/colours). Keeping
/// these here means the widgets don't each grow a `switch`. This is pure UI
/// data, not sim logic, so it belongs on the Flutter side.

/// Short tile face (placeholder for the real spell icon, which lands in M5).
String abilityFace(AbilityId id) => switch (id) {
      AbilityId.agony => 'Ag',
      AbilityId.corruption => 'Co',
      AbilityId.shadowBolt => 'SB',
      AbilityId.unstableAffliction => 'UA',
      AbilityId.haunt => 'Ha',
    };

String abilityName(AbilityId id) => switch (id) {
      AbilityId.agony => 'Agony',
      AbilityId.corruption => 'Corruption',
      AbilityId.shadowBolt => 'Shadow Bolt',
      AbilityId.unstableAffliction => 'Unstable Affliction',
      AbilityId.haunt => 'Haunt',
    };

/// Distinct tile tint per ability, so the placeholder grid reads at a glance.
Color abilityColor(AbilityId id) => switch (id) {
      AbilityId.agony => const Color(0xFF6B3FA0),
      AbilityId.corruption => const Color(0xFF3F7A4D),
      AbilityId.shadowBolt => const Color(0xFF394B8A),
      AbilityId.unstableAffliction => const Color(0xFF8A3F6B),
      AbilityId.haunt => const Color(0xFF7A6A3F),
    };

String debuffFace(DebuffId id) => switch (id) {
      DebuffId.agony => 'Ag',
      DebuffId.corruption => 'Co',
      DebuffId.haunt => 'Ha',
    };

Color debuffColor(DebuffId id) => switch (id) {
      DebuffId.agony => const Color(0xFF6B3FA0),
      DebuffId.corruption => const Color(0xFF3F7A4D),
      DebuffId.haunt => const Color(0xFF7A6A3F),
    };

/// Terse badge for why a button is dim (WoW-style shorthand).
String rejectBadge(CastRejectReason reason) => switch (reason) {
      CastRejectReason.gcdActive => 'GCD',
      CastRejectReason.onCooldown => 'CD',
      CastRejectReason.insufficientResource => '◇',
      CastRejectReason.alreadyCasting => '…',
      CastRejectReason.channeling => '…',
      CastRejectReason.unknownAbility => '?',
    };
