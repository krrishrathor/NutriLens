from fastapi import APIRouter

from app.schemas.scan_schema import ScanRequest
from app.services.parser_service import extract_ingredients
from app.services.ingredient_service import find_ingredient

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
            results.append({
                "name": ingredient,
                "found": False
            })

    return {
        "success": True,
        "ingredients": results,
        "count": len(results)
    }