import 'package:flutter/material.dart';
import 'package:rotation_sim/sim.dart';

import '../game_controller.dart';
import '../ui_labels.dart';
import 'icon_countdown_tile.dart';

/// One thumb button. Dispatches [GameController.cast] on tap, and dims itself
/// (with a terse reason badge + cooldown/GCD sweep) whenever
/// [GameController.canCast] reports it unusable. Rebuilt every frame by the
/// parent [ListenableBuilder], so the dim/undim flips live.
class AbilityButton extends StatelessWidget {
  const AbilityButton({super.key, required this.controller, required this.id});

  final GameController controller;
  final AbilityId id;

  @override
  Widget build(BuildContext context) {
    final state = controller.state;
    final now = state.time;
    final def = controller.config.abilities[id];
    final reason = controller.canCast(id);
    final enabled = reason == null;

    // Cooldown sweep (Haunt) takes precedence; otherwise show the GCD sweep so
    // the whole bar visibly winds down between casts, WoW-style.
    final cd = state.cooldowns[id];
    final onCooldown = cd != null && !cd.isReady(now);
    double sweep = 0;
    double? seconds;
    if (onCooldown && def != null && def.cooldown > 0) {
      sweep = (cd.remainingAt(now) / def.cooldown).clamp(0.0, 1.0);
      seconds = cd.remainingAt(now);
    } else if (def != null && def.onGcd && state.isGcdActive) {
      sweep = (state.gcdRemaining / controller.config.gcd).clamp(0.0, 1.0);
    }

    return InkWell(
      borderRadius: BorderRadius.circular(8),
      onTap: enabled ? () => controller.cast(id) : null,
      child: IconCountdownTile(
        face: abilityFace(id),
        color: abilityColor(id),
        size: 72,
        sweepFraction: sweep,
        seconds: seconds,
        dim: !enabled,
        badge: enabled ? null : rejectBadge(reason),
      ),
    );
  }
}
