import os

from pymongo import MongoClient

mongo_uri = os.getenv("MONGO_URI", "mongodb://mongodb:27017/asset_db")

mongo_client = MongoClient(mongo_uri)

db = mongo_client.get_database("asset_db")


def get_db():
    """
    Returns the database instance.
    """
    return db
