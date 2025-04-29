from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from beanie import PydanticObjectId

class UserSheme(BaseModel):
    id: Optional[PydanticObjectId] = None
    telegram_id: int
    username: str
    created_at: datetime = Field(default_factory=datetime.now)


    class Config:
        json_encoders = {PydanticObjectId: str}


class UserDocument(UserSheme, Document):
    class Settings:
        collection = "users"


class UserIn(BaseModel):
   telegram_id: int
   username: str
   
class UserOut(BaseModel):
    id: Optional[PydanticObjectId] 
    telegram_id: int
    username: str
    created_at: datetime 


    class Config:
        json_encoders = {PydanticObjectId: str}

   