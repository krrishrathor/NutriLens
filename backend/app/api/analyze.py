from fastapi import APIRouter

from app.schemas.scan_schema import ScanRequest
from app.services.parser_service import extract_ingredients
from app.services.ingredient_service import find_ingredient
from app.agents.research_agent import research_ingredient

router = APIRouter()


@router.post("/scan")
def scan(request: ScanRequest):

    parsed_ingredients = extract_ingredients(request.raw_text)

    results = []

    for ingredient in parsed_ingredients:

        details = find_ingredient(ingredient)

        if details:
            results.append(details)
        else:
            research_response = research_ingredient(ingredient)
            if research_response.get("success"):
                results.append(research_response["research"])
            else:
                results.append({
                    "name": ingredient,
                    "found": False,
                    "error": research_response.get("message")
                })

    return {
        "success": True,
        "ingredients": results,
        "count": len(results)
    }