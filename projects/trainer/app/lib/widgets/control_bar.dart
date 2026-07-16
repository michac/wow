import 'package:flutter/material.dart';

import '../game_controller.dart';

/// Small bottom-anchored row of pull controls sitting just above the
/// [ActionBar], within thumb reach: **Stop** (end the pull early — hidden once
/// ended), **Reset** (start fresh), and a **hint toggle** for the glow.
class ControlBar extends StatelessWidget {
  const ControlBar({super.key, required this.controller});

  final GameController controller;

  @override
  Widget build(BuildContext context) {
    final ended = controller.ended;
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          // Stop only makes sense while the pull is live.
          if (!ended)
            TextButton.icon(
              onPressed: controller.stop,
              icon: const Icon(Icons.stop),
              label: const Text('Stop'),
            ),
          TextButton.icon(
            onPressed: controller.reset,
            icon: const Icon(Icons.refresh),
            label: const Text('Reset'),
          ),
          IconButton(
            onPressed: controller.toggleHints,
            tooltip: controller.showHints ? 'Hide hints' : 'Show hints',
            isSelected: controller.showHints,
            icon: const Icon(Icons.lightbulb_outline),
            selectedIcon: const Icon(Icons.lightbulb),
          ),
        ],
      ),
    );
  }
}
