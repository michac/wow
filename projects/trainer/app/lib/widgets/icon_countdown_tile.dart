import 'package:flutter/material.dart';

import 'sweep_painter.dart';

/// A WoW-style square ability/debuff icon: a coloured tile (placeholder for the
/// real spell icon, M5), an optional radial cooldown [sweepFraction], an
/// optional numeric [seconds] countdown, an optional [stacks] corner number,
/// and an optional [badge] (e.g. "GCD" when a button is unusable).
class IconCountdownTile extends StatelessWidget {
  const IconCountdownTile({
    super.key,
    required this.face,
    required this.color,
    this.size = 64,
    this.sweepFraction = 0,
    this.seconds,
    this.stacks,
    this.badge,
    this.dim = false,
    this.glow = false,
  });

  final String face;
  final Color color;
  final double size;

  /// Portion of the tile still covered by the cooldown sweep, in `[0, 1]`.
  final double sweepFraction;

  /// Remaining seconds to show centred; null hides it.
  final double? seconds;

  /// Stack count shown in the corner; null hides it.
  final int? stacks;

  /// Short reason badge shown at the bottom (why a button is dim).
  final String? badge;

  final bool dim;
  final bool glow;

  @override
  Widget build(BuildContext context) {
    final secondsLabel = seconds?.ceil().clamp(0, 999).toString();

    return Opacity(
      opacity: dim ? 0.4 : 1.0,
      child: Container(
        width: size,
        height: size,
        decoration: BoxDecoration(
          color: color,
          borderRadius: BorderRadius.circular(8),
          border: Border.all(
            color: glow ? Colors.amberAccent : Colors.black54,
            width: glow ? 3 : 1.5,
          ),
          boxShadow: glow
              ? [const BoxShadow(color: Colors.amber, blurRadius: 10)]
              : null,
        ),
        clipBehavior: Clip.antiAlias,
        child: Stack(
          alignment: Alignment.center,
          children: [
            // Face label (placeholder for the spell icon).
            Text(
              face,
              style: TextStyle(
                fontSize: size * 0.32,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
            // Radial cooldown sweep over the face.
            if (sweepFraction > 0)
              Positioned.fill(
                child: CustomPaint(
                  painter: SweepPainter(fraction: sweepFraction),
                ),
              ),
            // Centred numeric countdown (WoW-style), drawn above the sweep.
            if (secondsLabel != null)
              Text(
                secondsLabel,
                style: TextStyle(
                  fontSize: size * 0.34,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                  shadows: const [Shadow(color: Colors.black, blurRadius: 3)],
                ),
              ),
            // Stack count, bottom-right.
            if (stacks != null && stacks! > 0)
              Positioned(
                right: 3,
                bottom: 1,
                child: Text(
                  '$stacks',
                  style: TextStyle(
                    fontSize: size * 0.26,
                    fontWeight: FontWeight.bold,
                    color: Colors.amberAccent,
                    shadows: const [Shadow(color: Colors.black, blurRadius: 3)],
                  ),
                ),
              ),
            // Reason badge, bottom-centre.
            if (badge != null)
              Positioned(
                bottom: 2,
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 1),
                  decoration: BoxDecoration(
                    color: Colors.black54,
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: Text(
                    badge!,
                    style: TextStyle(
                      fontSize: size * 0.18,
                      fontWeight: FontWeight.w600,
                      color: Colors.white,
                    ),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
