import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.repository.user import UserRepository
from app.schemas.users import User, UserIn, UserOut
from app.services.userService import UserService


UserRouter = APIRouter(
    prefix="/v1/users", tags=["users"]
)

userRepo = UserRepository()
userService = UserService(userRepo)

@UserRouter.post("/create")
async def create_user(user: UserIn):
    try:
        user_id = await userService.create_user(User(telegram_id=user.telegram_id,
                                                     username=user.username))
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=f"server error: {e}")

    return JSONResponse({"user_id":user_id}, 200)

@UserRouter.get("/get/{telegram_id}", response_model=UserOut)
async def get_chat(telegram_id: int):
    try: 
        user = await userService.get_user(telegram_id)
        response = UserOut(id=user.id,
                           telegram_id=user.telegram_id,
                           username=user.username,
                           created_at=user.created_at)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=f"server error: {e}")
    return response
