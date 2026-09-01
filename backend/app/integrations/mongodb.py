import certifi
from pymongo import MongoClient
# from pymongo.server_api import ServerApi

from app.config import MONGODB_URI, DATABASE_NAME

# server_api = ServerApi("1") 

client = MongoClient(
    MONGODB_URI,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=10000
)

database = client[DATABASE_NAME]

ingredient_collection = database["ingredient_knowledge"]


def test_connection():
    try:
        client.admin.command("ping")
        print("MongoDB connection successful!")
    except Exception as e:
        print("MongoDB connection failed:", e)


def create_indexes():
    try:
        ingredient_collection.create_index("name")
        print("MongoDB indexes created successfully!")
    except Exception as e:
        print("Failed to create MongoDB indexes:", e)

def save_ingredient(ingredient: dict):
    result = ingredient_collection.update_one(
        {
            "name": ingredient["name"]
        },
        {
            "$set": ingredient
        },
        upsert=True
    )

    return result