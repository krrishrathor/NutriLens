import json

from app.integrations.tavily import search_ingredient
from app.integrations.gemini import generate_response
from app.integrations.mongodb import save_ingredient
from app.schemas.research_schema import ResearchResult


def parse_json_response(response: str) -> dict:
    """
    Convert Gemini's response into a Python dictionary.
    Handles Markdown code fences such as ```json ... ```.
    """

    cleaned_response = response.strip()

    # Remove opening Markdown fence
    if cleaned_response.startswith("```json"):
        cleaned_response = cleaned_response[len("```json"):].strip()

    elif cleaned_response.startswith("```"):
        cleaned_response = cleaned_response[len("```"):].strip()

    # Remove closing Markdown fence
    if cleaned_response.endswith("```"):
        cleaned_response = cleaned_response[:-3].strip()

    # Convert JSON string -> Python dictionary
    return json.loads(cleaned_response)



def research_ingredient(name: str):
    search_results = search_ingredient(name)

    if not search_results:
        return {
            "success": False,
            "message": f"No research results found for '{name}'."
        }

    evidence_parts = []

    for result in search_results:
        evidence_parts.append(f"""
            Title: {result['title']}
            URL: {result['url']}
            Content:
            {result['content']}

            -------------------------
        """
        )

    evidence = "\n-----------------------------\n".join(evidence_parts)

    prompt = f"""
        You are a food ingredient research assistant.

        Research target:
        {name}

        Below is evidence retrieved from web sources.

        {evidence}

        Your task is to identify and summarize the ingredient using ONLY
        information supported by the supplied sources.

        Important rules:

        1. Identify the canonical ingredient name.
        2. Identify aliases and additive codes.
        3. Explain what the ingredient is.
        4. Explain why it is used in food.
        5. Assess safety only when the supplied evidence supports such an assessment.
        6. Never invent a safety conclusion.
        7. If the sources do not provide enough evidence for a safety judgment,
        explicitly say so.
        8. Mention relevant conditions of use or limitations.
        9. Do not provide medical diagnoses.
        10. Return ONLY valid JSON.

        Source reliability rules:
        - Tier 1 sources are authoritative regulatory or scientific sources.
        - Tier 2 sources are secondary sources.
        - Tier 3 sources are low-confidence sources.
        - Do not make a safety or regulatory claim solely from a Tier 3 source.
        - Do not treat a search result's wording as proof of a regulatory classification.
        - If authoritative evidence is insufficient, say that the safety assessment is inconclusive.
        - Never invent regulatory limits.

        Safety and regulatory rules:
        - Do not infer that an ingredient is safe merely because it has an E-number or INS number.
        - Do not infer approval for a specific jurisdiction unless a source explicitly supports it.
        - Distinguish between:
        "approved/authorized for specified uses"
        and
        "safe in all circumstances".
        - Do not invent maximum permitted levels.
        - Do not claim GRAS status unless an authoritative source explicitly supports it.
        - A general FDA/EFSA information page is not sufficient evidence for a specific ingredient's regulatory status.
        - Prefer ingredient-specific regulatory assessments and authoritative scientific sources.
        - If ingredient-specific evidence is insufficient, use:
        "Insufficient evidence from retrieved authoritative sources"
        rather than guessing.
        - Always preserve the original searched identifier as an alias.

        Use EXACTLY this structure:

        {{
            "name": "string",
            "aliases": ["string"],
            "category": "string",
            "used_for": "string",
            "safety": {{
                "classification": "string",
                "basis": "string",
                "caveat": "string"
            }},
            "risk_level": "string",
            "description": "string",
            "sources": ["url1", "url2"]
        }}
    """

    try:

        response = generate_response(prompt)

        # Step 1: Gemini string -> Python dictionary
        data = parse_json_response(response)

        # Step 2: Preserve original searched identifier
        aliases = data.get("aliases", [])
        aliases = [alias for alias in aliases if alias.lower() != name.lower()]
        data["aliases"] = [name] + aliases  # Ensure the searched name is first in the list
        
        if name not in data["aliases"]:
            data["aliases"].insert(0, name)

        # Step 3: Validate dictionary against Pydantic schema
        validated_result = ResearchResult.model_validate(data)
        
        validated_data = validated_result.model_dump()

        save_ingredient(validated_data)

        return {
            "success": True,
            "research": validated_result.model_dump()
        }

    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:

        return {
            "success": False,
            "message": f"Research failed: {str(e)}",
        }