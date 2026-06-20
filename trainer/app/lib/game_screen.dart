import 'package:flutter/material.dart';
import 'package:rotation_sim/sim.dart';

import 'game_controller.dart';
import 'widgets/action_bar.dart';
import 'widgets/cast_bar.dart';
import 'widgets/resource_bar.dart';
import 'widgets/target_panel.dart';

/// The only [StatefulWidget] in the app: it hosts the vsync + [GameController]
/// lifecycle and rebuilds the whole (tiny) tree once per frame via a single
/// [ListenableBuilder]. Optional [config]/[rng] let tests inject determinism.
class GameScreen extends StatefulWidget {
  const GameScreen({super.key, this.config, this.rng});

  final SimConfig? config;
  final SimRng? rng;

  @override
  State<GameScreen> createState() => _GameScreenState();
}

class _GameScreenState extends State<GameScreen>
    with SingleTickerProviderStateMixin {
  late final GameController _controller;

  @override
  void initState() {
    super.initState();
    _controller = GameController(
      vsync: this,
      config: widget.config,
      rng: widget.rng,
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: ListenableBuilder(
          listenable: _controller,
          builder: (context, _) {
            final state = _controller.state;
            return Column(
              children: [
                // Status (cast/resource/debuff) up top, away from thumbs.
                TargetPanel(controller: _controller),
                CastBar(state: state),
                ResourceBar(state: state),
                const Spacer(),
                _Readout(state: state),
                const Spacer(),
                // Action grid bottom-anchored, under a natural grip.
                ActionBar(controller: _controller),
              ],
            );
          },
        ),
      ),
    );
  }
}

/// Minimal timer/score line. The real DPS-ish score + end-of-pull summary is M4.
class _Readout extends StatelessWidget {
  const _Readout({required this.state});

  final GameState state;

  @override
  Widget build(BuildContext context) {
    final mins = state.time ~/ 60;
    final secs = (state.time % 60).floor();
    final clock = '$mins:${secs.toString().padLeft(2, '0')}';
    return Text(
      clock,
      style: const TextStyle(
        fontSize: 28,
        fontWeight: FontWeight.w600,
        fontFeatures: [FontFeature.tabularFigures()],
        color: Colors.white70,
      ),
    );
  }
}
