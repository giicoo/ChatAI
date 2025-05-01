from contextlib import asynccontextmanager
import logging
import time
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request

from app.api.v1.chat import ChatRouter
from app.core.enviroment import API_VERSION, APP_NAME
from app.api.v1.message import MsgRouter
from app.api.v1.user import UserRouter

from app.core.database import close_mongo_connection, connect_to_mongo
from app.core.log import Logger




@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield 
    await close_mongo_connection()

logger = logging.getLogger(__name__)
app = FastAPI(
    title=APP_NAME,
    version=API_VERSION,
    lifespan=lifespan
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    try:
        body = await request.json()
    except:
        body = ""
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    Logger.info({"request-path":request.path_params, "request-query": request.query_params.multi_items(), "body": body, "process_time":process_time})
    return response

app.include_router(ChatRouter)
app.include_router(UserRouter)
app.include_router(MsgRouter)






