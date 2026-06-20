import 'package:flutter/material.dart';
import 'package:rotation_sim/sim.dart';

/// Soul Shard pips (0..max) plus a Nightfall proc indicator. Discrete pips are
/// the faithful rendering for shards; a filled pip = an available shard.
class ResourceBar extends StatelessWidget {
  const ResourceBar({super.key, required this.state});

  final GameState state;

  @override
  Widget build(BuildContext context) {
    final res = state.resources[ResourceId.soulShard];
    final current = res?.current ?? 0;
    final max = res?.max ?? 5;
    final nightfall = state.auraActive(AuraId.nightfall);

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Row(
        children: [
          for (var i = 0; i < max; i++)
            Padding(
              padding: const EdgeInsets.only(right: 8),
              child: _Pip(filled: i < current),
            ),
          const Spacer(),
          if (nightfall)
            _NightfallChip(stacks: state.auraStacks(AuraId.nightfall)),
        ],
      ),
    );
  }
}

class _Pip extends StatelessWidget {
  const _Pip({required this.filled});

  final bool filled;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 22,
      height: 22,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        color: filled ? const Color(0xFF9B6BD6) : Colors.transparent,
        border: Border.all(
          color: filled ? const Color(0xFFC9A8F0) : Colors.white24,
          width: 2,
        ),
        boxShadow: filled
            ? [const BoxShadow(color: Color(0x886B3FA0), blurRadius: 6)]
            : null,
      ),
    );
  }
}

class _NightfallChip extends StatelessWidget {
  const _NightfallChip({required this.stacks});

  final int stacks;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: const Color(0xFF2A2140),
        borderRadius: BorderRadius.circular(6),
        border: Border.all(color: Colors.amberAccent, width: 1.5),
      ),
      child: Text(
        stacks > 1 ? 'Nightfall ×$stacks' : 'Nightfall',
        style: const TextStyle(
          fontSize: 12,
          fontWeight: FontWeight.w600,
          color: Colors.amberAccent,
        ),
      ),
    );
  }
}
