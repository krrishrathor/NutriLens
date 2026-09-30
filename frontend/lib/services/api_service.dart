import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/analysis_response.dart';

class ApiService {
  // Use a configuration mechanism for backend URL in production.
  // For local development, 10.0.2.2 is the Android emulator alias to localhost, 
  // or use the machine's IP.
  final String baseUrl = const String.fromEnvironment('BACKEND_BASE_URL', defaultValue: '10.254.205.26'); // mac ip address: 10.254.205.26

  Future<AnalysisResponse> analyzeIngredients(String rawText) async {
    final url = Uri.parse('$baseUrl/scan');
    
    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'raw_text': rawText}),
      );

      if (response.statusCode == 200) {
        return AnalysisResponse.fromJson(jsonDecode(response.body));
      } else {
        throw Exception('Failed to analyze ingredients. Status code: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Network or backend error: $e');
    }
  }
}
