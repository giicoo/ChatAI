from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI

from app.api.v1.chat import ChatRouter
from app.core.enviroment import settings
from app.api.v1.message import MsgRouter
from app.api.v1.user import UserRouter

from app.core.database import close_mongo_connection, connect_to_mongo


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield 
    await close_mongo_connection()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    lifespan=lifespan
)

app.include_router(ChatRouter)
app.include_router(UserRouter)
app.include_router(MsgRouter)






