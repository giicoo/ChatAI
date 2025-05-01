from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal, Optional
from beanie import PydanticObjectId


class Message(BaseModel):
    id: Optional[PydanticObjectId] = None
    chat_id: Optional[PydanticObjectId] 
    role: Literal["user", "assistant"]
    content: str
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {PydanticObjectId: str}


class MessageDocument(Message, Document):
    class Settings:
        collection = "msgs"

class MessageIn(BaseModel):
    chat_id: Optional[PydanticObjectId] 
    content: str

    class Config:
        json_encoders = {PydanticObjectId: str}

class MessageOut(BaseModel):
    id: Optional[PydanticObjectId] 
    chat_id: Optional[PydanticObjectId] 
    role: Literal["user", "assistant"]
    content: str
    created_at: datetime 

    class Config:
        json_encoders = {PydanticObjectId: str}