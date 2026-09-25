from app.integrations.mongodb import ingredient_collection

def find_ingredient(name: str):
    ingredient = ingredient_collection.find_one(
        {
            "$or": [
                {
                    "name": {
                        "$regex": f"^{name}$",
                        "$options": "i"
                    }
                },
                {
                    "aliases": {
                        "$regex": f"^{name}$",
                        "$options": "i"
                    }
                }
            ]
        },
        {
            "_id": 0
        }
    )

    return ingredient
