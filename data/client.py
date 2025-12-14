import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()
uri = os.environ.get("MONGO_DB_URI")


class MongoClientSingleton:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = MongoClient(uri, server_api=ServerApi('1'))
            try:
                cls._client.admin.command("ping")
                print("Pinged your deployment. You successfully connected to MongoDB!")
            except Exception as e:
                raise RuntimeError(f"MongoDB connection failed: {e}")
        return cls._client
    
client = MongoClientSingleton.get_client()