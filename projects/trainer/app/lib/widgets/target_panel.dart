import 'package:flutter/material.dart';
import 'package:rotation_sim/sim.dart';

import '../game_controller.dart';
import '../ui_labels.dart';
import 'icon_countdown_tile.dart';

/// The target dummy: a placeholder health bar plus the tracked debuffs, each a
/// WoW-style icon tile with a shrinking radial sweep + numeric countdown.
class TargetPanel extends StatelessWidget {
  const TargetPanel({super.key, required this.controller});

  final GameController controller;

  /// Fixed display order for the debuff row.
  static const _order = [DebuffId.agony, DebuffId.corruption, DebuffId.haunt];

  @override
  Widget build(BuildContext context) {
    final state = controller.state;

    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 12, 16, 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Text('Target dummy',
                  style: TextStyle(fontWeight: FontWeight.w600)),
              const SizedBox(width: 12),
              Expanded(
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(4),
                  child: const LinearProgressIndicator(
                    value: 0.6, // placeholder — engine has no health model
                    minHeight: 14,
                    backgroundColor: Colors.black45,
                    valueColor: AlwaysStoppedAnimation(Color(0xFFB23A3A)),
                  ),
                ),
              ),
              const SizedBox(width: 8),
              const Text('60%', style: TextStyle(color: Colors.white70)),
            ],
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              for (final id in _order) ...[
                _DebuffTile(id: id, state: state),
                const SizedBox(width: 10),
              ],
            ],
          ),
        ],
      ),
    );
  }
}

class _DebuffTile extends StatelessWidget {
  const _DebuffTile({required this.id, required this.state});

  final DebuffId id;
  final GameState state;

  @override
  Widget build(BuildContext context) {
    final now = state.time;
    final debuff = state.debuffs[id];

    if (debuff == null) {
      // Inactive slot — greyed, so the tile appearing/vanishing reads as the
      // timer falling off.
      return IconCountdownTile(
        face: debuffFace(id),
        color: debuffColor(id),
        size: 56,
        dim: true,
      );
    }

    final remaining = debuff.remainingAt(now);
    final window = debuff.expiresAt - debuff.appliedAt;
    final fraction = window > 0 ? (remaining / window).clamp(0.0, 1.0) : 0.0;

    return IconCountdownTile(
      face: debuffFace(id),
      color: debuffColor(id),
      size: 56,
      seconds: remaining,
      sweepFraction: fraction,
    );
  }
}
