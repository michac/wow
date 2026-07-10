import 'package:flutter/material.dart';
import 'package:rotation_sim/sim.dart';

import 'game_controller.dart';
import 'widgets/action_bar.dart';
import 'widgets/cast_bar.dart';
import 'widgets/control_bar.dart';
import 'widgets/resource_bar.dart';
import 'widgets/summary_panel.dart';
import 'widgets/target_panel.dart';

/// The only [StatefulWidget] in the app: it hosts the vsync + [GameController]
/// lifecycle and rebuilds the whole (tiny) tree once per frame via a single
/// [ListenableBuilder]. Optional [config]/[rng] let tests inject determinism.
class GameScreen extends StatefulWidget {
  const GameScreen({super.key, this.config, this.rng, this.pullSeconds});

  final SimConfig? config;
  final SimRng? rng;

  /// Pull length override (seconds). Null uses the engine's default (60). Lets
  /// tests inject a short pull to reach the end-of-pull summary quickly.
  final double? pullSeconds;

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
      pullSeconds: widget.pullSeconds,
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
            return Stack(
              children: [
                Column(
                  children: [
                    // Status (cast/resource/debuff) up top, away from thumbs.
                    TargetPanel(controller: _controller),
                    CastBar(state: state),
                    ResourceBar(state: state),
                    const Spacer(),
                    _Readout(controller: _controller),
                    const Spacer(),
                    // Pull controls, then the action grid — both thumb-reachable.
                    ControlBar(controller: _controller),
                    ActionBar(controller: _controller),
                  ],
                ),
                // End-of-pull summary overlays the frozen board.
                if (_controller.ended) SummaryPanel(controller: _controller),
              ],
            );
          },
        ),
      ),
    );
  }
}

/// Live top readout: the pull **countdown** (mm:ss) over a rough **DPS-equiv**
/// number, both updating every frame. The end-of-pull grade lives in the
/// summary overlay.
class _Readout extends StatelessWidget {
  const _Readout({required this.controller});

  final GameController controller;

  @override
  Widget build(BuildContext context) {
    // Ceil so a full 60s pull reads "1:00" and only hits "0:00" at the end.
    final total = controller.secondsLeft.ceil();
    final clock = '${total ~/ 60}:${(total % 60).toString().padLeft(2, '0')}';
    final dps = controller.stats.dpsEquivalent;
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Text(
          clock,
          style: const TextStyle(
            fontSize: 28,
            fontWeight: FontWeight.w600,
            fontFeatures: [FontFeature.tabularFigures()],
            color: Colors.white70,
          ),
        ),
        Text(
          '${dps.toStringAsFixed(1)} DPS-equiv',
          style: const TextStyle(
            fontSize: 15,
            fontFeatures: [FontFeature.tabularFigures()],
            color: Colors.white38,
          ),
        ),
      ],
    );
  }
}
