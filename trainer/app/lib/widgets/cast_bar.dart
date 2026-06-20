import 'package:flutter/material.dart';
import 'package:rotation_sim/sim.dart';

import '../ui_labels.dart';

/// Left-to-right cast/channel fill. Hidden entirely when nothing is casting,
/// per the spec. Progress is read against the sim clock (`state.time`).
class CastBar extends StatelessWidget {
  const CastBar({super.key, required this.state});

  final GameState state;

  @override
  Widget build(BuildContext context) {
    final cast = state.cast;
    if (cast == null) return const SizedBox(height: 28);

    final now = state.time;
    final progress = cast.progressAt(now);
    final remaining = cast.remainingAt(now);

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
      child: SizedBox(
        height: 20,
        child: Stack(
          children: [
            ClipRRect(
              borderRadius: BorderRadius.circular(4),
              child: LinearProgressIndicator(
                value: progress,
                minHeight: 20,
                backgroundColor: Colors.black45,
                valueColor:
                    const AlwaysStoppedAnimation(Color(0xFF9B6BD6)),
              ),
            ),
            Positioned.fill(
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 8),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      abilityName(cast.ability),
                      style: const TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.w600,
                        color: Colors.white,
                      ),
                    ),
                    Text(
                      '${remaining.toStringAsFixed(1)}s',
                      style: const TextStyle(
                        fontSize: 12,
                        color: Colors.white,
                        fontFeatures: [FontFeature.tabularFigures()],
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
