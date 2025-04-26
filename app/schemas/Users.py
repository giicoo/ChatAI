from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime, timezone

from typing import Optional

from pydantic_mongo import PydanticObjectId

class User(BaseModel):
   oid: ObjectId
   telegram_id: int
   telegram_username: str
   created_at: datetime = Field(default_factory=datetime.now)

   class Config:
        arbitrary_types_allowed = True


# RESPONSES AND REQUESTS MODELS
class UserCreate(BaseModel):
   telegram_id: int
   telegram_username: str
   
class UserResponse(BaseModel):
   id: Optional[PydanticObjectId] = None

   