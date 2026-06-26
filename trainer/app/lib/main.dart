import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:rotation_sim/sim.dart';

import 'app.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  // Portrait-only; a no-op on web/desktop, meaningful on the eventual phone.
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);

  // Boot the roster from the bundled JSON template — the spec is data, not code.
  // Debug-loud, release-fallback: a bad template fails the dev loop visibly but
  // keeps a shipped build bootable on the hard-coded oracle.
  SimConfig? config;
  try {
    final json =
        await rootBundle.loadString('assets/templates/affliction_simple.json');
    config = loadTemplate(json);
  } catch (_) {
    if (kDebugMode) rethrow;
    config = afflictionSimplified();
  }

  runApp(RotationTrainerApp(config: config));
}
