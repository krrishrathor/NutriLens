import json
from pathlib import Path
from app.integrations.mongodb import ingredient_collection

DATABASE_PATH = Path(__file__).resolve().parent / "ingredients.json"

def seed_database():
    with open(DATABASE_PATH, "r", encoding="utf-8") as file:
        ingredients = json.load(file)

    if not ingredients:
        print("No ingredients found in JSON file")
        return

    ingredient_collection.delete_many({})  # Clear existing data -- Why delete_many({})? We're still in development. Every time we run the seed script, it clears the test collection and inserts the current JSON data. That prevents duplicates while we're experimenting.

    result = ingredient_collection.insert_many(ingredients)

    print(f"Inserted {len(result.inserted_ids)} ingredients into MongoDB")

if __name__ == "__main__":
    seed_database()