from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["talent_acquisition_db"]  

logs_collection = db["logs"]

async def connect_mongo():
    global client, db, logs_collection
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["talent_acquisition_db"]
    logs_collection = db["logs"]

async def close_mongo():
    client.close()