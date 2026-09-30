import 'ingredient.dart';

class AnalysisResponse {
  final bool success;
  final List<Ingredient> ingredients;
  final int count;

  AnalysisResponse({
    required this.success,
    required this.ingredients,
    required this.count,
  });

  factory AnalysisResponse.fromJson(Map<String, dynamic> json) {
    var list = json['ingredients'] as List? ?? [];
    List<Ingredient> ingredientsList = list.map((i) => Ingredient.fromJson(i)).toList();
    
    return AnalysisResponse(
      success: json['success'] ?? false,
      ingredients: ingredientsList,
      count: json['count'] ?? 0,
    );
  }
}
