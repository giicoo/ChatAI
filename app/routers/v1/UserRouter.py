import datetime
import json
from bson import json_util
from typing import List, Optional
from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


from app.schemas.Users import User, UserCreate, UserResponse
from app.services.UserService import UserService

UserRouter = APIRouter(
    prefix="/v1/users", tags=["users"]
)

@UserRouter.post("/create", response_model=UserResponse)
def create(user: UserCreate, userService: UserService = Depends()):
    """
    Создает документы в коллекции users с полями: \n
    **_id** : MongoDB ID \n
    **tg_id**: telegram id \n
    **username**: telegram username \n
    **created_at**: created datetime \n
    """
    id = userService.create_user(user)
    return UserResponse(id=id)