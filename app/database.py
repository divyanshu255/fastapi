from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)
db = client.file_sharing
