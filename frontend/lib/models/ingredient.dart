class Ingredient {
  final String name;
  final bool found;
  final String? category;
  final String? usedFor;
  final dynamic safety;
  final String? riskLevel;
  final String? description;
  final List<String>? sources;
  final String? error;

  Ingredient({
    required this.name,
    this.found = true,
    this.category,
    this.usedFor,
    this.safety,
    this.riskLevel,
    this.description,
    this.sources,
    this.error,
  });

  factory Ingredient.fromJson(Map<String, dynamic> json) {
    return Ingredient(
      name: json['name'] ?? 'Unknown',
      found: json['found'] ?? true,
      category: json['category'],
      usedFor: json['used_for'],
      safety: json['safety'],
      riskLevel: json['risk_level'],
      description: json['description'],
      sources: json['sources'] != null ? List<String>.from(json['sources']) : null,
      error: json['error'],
    );
  }
}
