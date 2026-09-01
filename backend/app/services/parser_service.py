import re

def extract_ingredients(raw_text: str) -> list[str]:
    """Extract a clean list of ingredients from the OCR text."""

    # remove "Ingredients" from raw test
    cleaned_text = re.sub(
        r"ingredients\s*:",
        "",
        raw_text,
        flags = re.IGNORECASE
    )

    # replace new lines with commas
    cleaned_text = cleaned_text.replace("\n", ",")

    # split by commas
    ingredients = cleaned_text.split(",")

    # remove extra whitespace and empty strings
    ingredients = [ingredient.strip() for ingredient in ingredients if ingredient.strip()]

    return ingredients
