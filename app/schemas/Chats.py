from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field
from datetime import datetime, timezone
from pydantic_mongo import AbstractRepository, PydanticObjectId
from typing import Annotated, Literal, Optional, List

PyObjectId = Annotated[str, BeforeValidator(str)]

class Chat(BaseModel):
   id: Optional[PyObjectId] = Field(alias="_id", default=None)
   telegram_id: int
   model: Literal["llama2"]
   name: str
   created_at: datetime = Field(default_factory=datetime.now)

   model_config = ConfigDict(

        populate_by_name=True,

        arbitrary_types_allowed=True,

        json_schema_extra={

            "example": {

                "name": "Jane Doe",

                "email": "jdoe@example.com",

                "course": "Experiments, Science, and Fashion in Nanophotonics",

                "gpa": 3.0,

            }

        },
   )
 

