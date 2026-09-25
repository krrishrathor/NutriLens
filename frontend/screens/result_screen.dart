import 'package:flutter/material.dart';
import '../models/analysis_response.dart';
import '../models/ingredient.dart';

class ResultScreen extends StatelessWidget {
  final AnalysisResponse response;

  const ResultScreen({Key? key, required this.response}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Analysis Results')),
      body: response.ingredients.isEmpty
          ? const Center(child: Text('No ingredients found.'))
          : ListView.builder(
              itemCount: response.ingredients.length,
              itemBuilder: (context, index) {
                return _IngredientCard(ingredient: response.ingredients[index]);
              },
            ),
    );
  }
}

class _IngredientCard extends StatelessWidget {
  final Ingredient ingredient;

  const _IngredientCard({Key? key, required this.ingredient}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      elevation: 3,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Expanded(
                  child: Text(
                    ingredient.name,
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
                if (!ingredient.found)
                  const Chip(
                    label: Text('Not Found', style: TextStyle(color: Colors.white)),
                    backgroundColor: Colors.redAccent,
                  )
              ],
            ),
            if (ingredient.error != null) ...[
              const SizedBox(height: 8),
              Text(
                'Error: \${ingredient.error}',
                style: const TextStyle(color: Colors.red),
              ),
            ],
            if (ingredient.category != null) ...[
              const SizedBox(height: 8),
              _InfoRow(label: 'Category', value: ingredient.category!),
            ],
            if (ingredient.usedFor != null) ...[
              const SizedBox(height: 4),
              _InfoRow(label: 'Used For', value: ingredient.usedFor!),
            ],
            if (ingredient.riskLevel != null) ...[
              const SizedBox(height: 4),
              _InfoRow(label: 'Risk Level', value: ingredient.riskLevel!),
            ],
            if (ingredient.safety != null) ...[
              const SizedBox(height: 4),
              if (ingredient.safety is String)
                _InfoRow(label: 'Safety', value: ingredient.safety)
              else if (ingredient.safety is Map)
                _InfoRow(
                  label: 'Safety',
                  value: '\${ingredient.safety["classification"] ?? ""}'
                      '\${ingredient.safety["basis"] != null ? " (\${ingredient.safety["basis"]})" : ""}',
                ),
            ],
            if (ingredient.description != null) ...[
              const SizedBox(height: 12),
              const Text(
                'Description:',
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 4),
              Text(ingredient.description!),
            ],
            if (ingredient.sources != null && ingredient.sources!.isNotEmpty) ...[
              const SizedBox(height: 12),
              const Text(
                'Sources:',
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 4),
              ...ingredient.sources!.map((s) => Text(
                    '• \$s',
                    style: const TextStyle(color: Colors.blue, fontSize: 12),
                  )),
            ],
          ],
        ),
      ),
    );
  }
}

class _InfoRow extends StatelessWidget {
  final String label;
  final String value;

  const _InfoRow({Key? key, required this.label, required this.value}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            '\$label: ',
            style: const TextStyle(fontWeight: FontWeight.bold),
          ),
          Expanded(
            child: Text(value),
          ),
        ],
      ),
    );
  }
}
