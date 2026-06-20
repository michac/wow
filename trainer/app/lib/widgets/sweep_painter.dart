import 'dart:math' as math;

import 'package:flutter/material.dart';

/// WoW-style radial cooldown sweep: a dark wedge covering [fraction] of the
/// tile (1.0 = full overlay, 0.0 = none), starting at 12 o'clock and sweeping
/// clockwise — it shrinks as the timer runs down.
class SweepPainter extends CustomPainter {
  const SweepPainter({required this.fraction, this.color = const Color(0x99000000)});

  /// Portion still covered, in `[0, 1]`.
  final double fraction;
  final Color color;

  @override
  void paint(Canvas canvas, Size size) {
    final f = fraction.clamp(0.0, 1.0);
    if (f <= 0) return;
    final rect = Offset.zero & size;
    final center = rect.center;
    final paint = Paint()..color = color;

    if (f >= 1.0) {
      canvas.drawRect(rect, paint);
      return;
    }

    // A wedge from the center out to the tile edge. Using the diagonal as the
    // radius guarantees the wedge reaches the corners of the square tile.
    final radius = size.longestSide;
    final start = -math.pi / 2; // 12 o'clock
    final sweep = 2 * math.pi * f;
    final path = Path()
      ..moveTo(center.dx, center.dy)
      ..arcTo(
        Rect.fromCircle(center: center, radius: radius),
        start,
        sweep,
        false,
      )
      ..close();
    canvas.save();
    canvas.clipRect(rect);
    canvas.drawPath(path, paint);
    canvas.restore();
  }

  @override
  bool shouldRepaint(SweepPainter old) =>
      old.fraction != fraction || old.color != color;
}
