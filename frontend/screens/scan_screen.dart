import 'dart:io';
import 'package:flutter/material.dart';
import '../services/camera_service.dart';
import '../services/mlkit_service.dart';
import '../services/api_service.dart';
import 'result_screen.dart';

class ScanScreen extends StatefulWidget {
  const ScanScreen({Key? key}) : super(key: key);

  @override
  _ScanScreenState createState() => _ScanScreenState();
}

class _ScanScreenState extends State<ScanScreen> {
  final CameraService _cameraService = CameraService();
  final MLKitService _mlkitService = MLKitService();
  final ApiService _apiService = ApiService();

  String? _imagePath;
  String _extractedText = '';
  bool _isProcessing = false;
  String? _errorMessage;

  Future<void> _captureAndProcess() async {
    setState(() {
      _isProcessing = true;
      _extractedText = '';
      _errorMessage = null;
    });

    try {
      final path = await _cameraService.captureImage();
      if (path != null) {
        setState(() {
          _imagePath = path;
        });
        
        final text = await _mlkitService.extractText(path);
        
        setState(() {
          _extractedText = text;
        });

        if (text.trim().isEmpty) {
          setState(() {
            _errorMessage = 'Could not extract text from the image. Please try again.';
          });
          return;
        }

        final analysisResult = await _apiService.analyzeIngredients(text);

        if (!mounted) return;

        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => ResultScreen(response: analysisResult),
          ),
        );
      }
    } catch (e) {
      setState(() {
        _errorMessage = 'Error: \$e';
      });
    } finally {
      if (mounted) {
        setState(() {
          _isProcessing = false;
        });
      }
    }
  }

  @override
  void dispose() {
    _mlkitService.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Scan Ingredients')),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              if (_imagePath != null)
                Image.file(File(_imagePath!), height: 300, fit: BoxFit.cover)
              else
                Container(
                  height: 300,
                  color: Colors.grey[200],
                  child: const Center(child: Text('No image captured')),
                ),
              const SizedBox(height: 20),
              ElevatedButton.icon(
                onPressed: _isProcessing ? null : _captureAndProcess,
                icon: const Icon(Icons.camera_alt),
                label: const Text('Capture Label'),
              ),
              const SizedBox(height: 20),
              if (_isProcessing)
                const Center(child: CircularProgressIndicator())
              else if (_errorMessage != null)
                Container(
                  padding: const EdgeInsets.all(12),
                  color: Colors.red[50],
                  child: Text(
                    _errorMessage!,
                    style: const TextStyle(color: Colors.red),
                  ),
                )
              else if (_extractedText.isNotEmpty)
                Container(
                  padding: const EdgeInsets.all(12),
                  color: Colors.blue[50],
                  child: Text('Extracted: \$_extractedText'),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
