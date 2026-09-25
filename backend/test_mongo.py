from pymongo import MongoClient
from pymongo.server_api import ServerApi
import certifi

from app.config import MONGODB_URI


client = MongoClient(
    MONGODB_URI,
    server_api=ServerApi("1"),
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=10000
)

try:
    result = client.admin.command("ping")
    print("PING:", result)

    server_info = client.server_info()
    print("MongoDB version:", server_info["version"])

except Exception as e:
    print("ERROR:", repr(e))

finally:
    client.close()