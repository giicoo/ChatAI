from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime, timezone

from pydantic_mongo import AbstractRepository, PydanticObjectId
from typing import Literal, Optional, List


class Message(BaseModel):
    id: Optional[PydanticObjectId] = None
    chat_id: Optional[PydanticObjectId] 
    role: Literal["user", "assistant"]
    content: str
    created_at: datetime = Field(default_factory=datetime.now)

class ChatRequest(BaseModel):
    query: str
