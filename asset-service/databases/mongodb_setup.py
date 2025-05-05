from pymongo import MongoClient
import os

mongo_uri = os.getenv("MONGO_URI","mongodb://mongodb:27017/asset_db")

client = MongoClient(mongo_uri)

db = client.get_database("asset_db")

def get_db():
    """
    Returns the database instance.
    """
    return db
