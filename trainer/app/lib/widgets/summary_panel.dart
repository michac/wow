import 'package:flutter/material.dart';
import 'package:rotation_sim/sim.dart';

import '../game_controller.dart';
import '../ui_labels.dart';

/// End-of-pull summary, shown as a translucent overlay above the frozen board
/// once [GameController.ended]. Headline **grade + letter**, then the
/// **DPS-equivalent**, then the discrete practice stats. A **Practice again**
/// button restarts the pull.
class SummaryPanel extends StatelessWidget {
  const SummaryPanel({super.key, required this.controller});

  final GameController controller;

  @override
  Widget build(BuildContext context) {
    final stats = controller.stats;
    return Positioned.fill(
      child: ColoredBox(
        color: Colors.black54,
        child: Center(
          child: Container(
            margin: const EdgeInsets.all(24),
            padding: const EdgeInsets.symmetric(horizontal: 28, vertical: 24),
            constraints: const BoxConstraints(maxWidth: 360),
            decoration: BoxDecoration(
              color: const Color(0xFF23232B),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: Colors.white24),
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  '${stats.grade.round()}',
                  style: TextStyle(
                    fontSize: 56,
                    fontWeight: FontWeight.w800,
                    color: _gradeColor(stats.letter),
                    height: 1.0,
                  ),
                ),
                Text(
                  'Grade ${stats.letter}',
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                    color: Colors.white70,
                  ),
                ),
                const SizedBox(height: 16),
                Text(
                  '${stats.dpsEquivalent.toStringAsFixed(1)} DPS-equiv',
                  style: const TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.w700,
                    fontFeatures: [FontFeature.tabularFigures()],
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 16),
                const Divider(color: Colors.white24, height: 1),
                const SizedBox(height: 12),
                // Per-DoT uptime rows (stable enum order).
                for (final id in DebuffId.values)
                  if (stats.uptimeSeconds.containsKey(id))
                    _StatRow(
                      label: '${debuffLabel(id)} uptime',
                      value: '${(stats.uptimeFraction(id) * 100).round()}%',
                    ),
                _StatRow(label: 'Wasted GCDs', value: '${stats.wastedGcds}'),
                _StatRow(label: 'Shard overcap', value: '${stats.overcap}'),
                _StatRow(label: 'Casts clipped', value: '${stats.clips}'),
                const SizedBox(height: 20),
                FilledButton.icon(
                  onPressed: controller.reset,
                  icon: const Icon(Icons.refresh),
                  label: const Text('Practice again'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  static Color _gradeColor(String letter) => switch (letter) {
        'A' => const Color(0xFF6BD98A),
        'B' => const Color(0xFFA8D96B),
        'C' => const Color(0xFFE6C84F),
        'D' => const Color(0xFFE39A4F),
        _ => const Color(0xFFE35F5F),
      };
}

/// A single label/value line in the summary.
class _StatRow extends StatelessWidget {
  const _StatRow({required this.label, required this.value});

  final String label;
  final String value;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 3),
      child: Row(
        children: [
          Expanded(
            child: Text(label,
                style: const TextStyle(fontSize: 15, color: Colors.white70)),
          ),
          const SizedBox(width: 12),
          Text(
            value,
            style: const TextStyle(
              fontSize: 15,
              fontWeight: FontWeight.w700,
              fontFeatures: [FontFeature.tabularFigures()],
              color: Colors.white,
            ),
          ),
        ],
      ),
    );
  }
}
