from pymongo import MongoClient
import os

def get_mongo_client():
    mongo_url = os.getenv("MONGO_URL", "mongodb://mongo:27017/")
    client = MongoClient(mongo_url)
    return client["transflow_db"]["corridas"]
