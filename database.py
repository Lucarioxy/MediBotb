from pymongo import MongoClient
from pymongo.collection import Collection
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_CLIENT = os.getenv('MONGO_CLIENT')

client = MongoClient(MONGO_CLIENT)
db = client["myChatbotDb"] 

def get_user_collection() -> Collection:
    return db["users"]

def get_files_collection() -> Collection:
    return db["files"]

def get_db():
    try:
        yield db
    finally:
        pass
