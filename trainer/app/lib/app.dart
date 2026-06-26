import 'package:flutter/material.dart';
import 'package:rotation_sim/sim.dart';

import 'game_screen.dart';

/// Root app: a dark Material 3 theme (reads like a game, no white flash) over
/// the single [GameScreen]. An optional [config] (loaded from a JSON template
/// by `main`) is threaded down; null falls back to the engine default.
class RotationTrainerApp extends StatelessWidget {
  const RotationTrainerApp({super.key, this.config});

  final SimConfig? config;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Rotation Trainer',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        brightness: Brightness.dark,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF6B3FA0),
          brightness: Brightness.dark,
        ),
        scaffoldBackgroundColor: const Color(0xFF14121A),
      ),
      home: GameScreen(config: config),
    );
  }
}
