import 'package:flutter/material.dart';

import 'game_screen.dart';

/// Root app: a dark Material 3 theme (reads like a game, no white flash) over
/// the single [GameScreen].
class RotationTrainerApp extends StatelessWidget {
  const RotationTrainerApp({super.key});

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
      home: const GameScreen(),
    );
  }
}
