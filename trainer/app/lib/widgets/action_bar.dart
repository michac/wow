import 'package:flutter/material.dart';

import '../game_controller.dart';
import 'ability_button.dart';

/// Bottom-anchored thumb grid of ability buttons. Renders one button per
/// ability in the config's priority order; big touch targets, generous spacing.
class ActionBar extends StatelessWidget {
  const ActionBar({super.key, required this.controller});

  final GameController controller;

  @override
  Widget build(BuildContext context) {
    final ids = controller.config.priority;
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 8, 16, 24),
      child: Wrap(
        alignment: WrapAlignment.center,
        spacing: 14,
        runSpacing: 14,
        children: [
          for (final id in ids)
            AbilityButton(controller: controller, id: id),
        ],
      ),
    );
  }
}
