import 'package:flutter/material.dart';
import 'screens/scan_screen.dart';

void main() {
  runApp(const NutriLensApp());
}

class NutriLensApp extends StatelessWidget {
  const NutriLensApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'NutriLens',
      theme: ThemeData(
        primarySwatch: Colors.green,
      ),
      home: const ScanScreen(),
    );
  }
}
