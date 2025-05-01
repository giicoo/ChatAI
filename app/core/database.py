from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.enviroment import MONGO_URI
from app.schemas.chats import ChatDocument
from app.schemas.messages import MessageDocument
from app.schemas.users import UserDocument

client: AsyncIOMotorClient = None
db = None

async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["db"]
    await init_beanie(db, document_models=[ChatDocument, UserDocument, MessageDocument])
    print("MongoDB connected")

async def close_mongo_connection():
    global client
    client.close()
    print("MongoDB connection closed")


