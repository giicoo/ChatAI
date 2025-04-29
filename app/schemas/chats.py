from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from beanie import PydanticObjectId


class ChatSheme(BaseModel):
    id: Optional[PydanticObjectId] = None
    telegram_id: int
    model: str
    title: str
    created_at: datetime = Field(default_factory=datetime.now)


    class Config:
        json_encoders = {PydanticObjectId: str}


class ChatDocument(ChatSheme, Document):
    class Settings:
        collection = "chats"

class ChatIn(BaseModel):
    telegram_id: int
    model: str
    title: str

class ChatOut(BaseModel):
    id: Optional[PydanticObjectId]
    telegram_id: int
    model: str
    title: str
    created_at: datetime 


    class Config:
        json_encoders = {PydanticObjectId: str}