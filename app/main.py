from fastapi import Depends, FastAPI

from app.configs.Enviroment import get_environment_variables

from app.routers.v1.MsgRouter import MsgRouter
from app.routers.v1.ChatRouter import ChatRouter
from app.routers.v1.UserRouter import UserRouter


env = get_environment_variables()

app = FastAPI(
    title=env.APP_NAME,
    version=env.API_VERSION,
)

app.include_router(ChatRouter)
app.include_router(UserRouter)
app.include_router(MsgRouter)

