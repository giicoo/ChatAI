from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from sse_starlette import EventSourceResponse
from app.repository.chat import ChatRepository
from app.repository.message import MessageRepository
from app.services.messageService import MessageService

MsgRouter = APIRouter(
    prefix="/v1/msgs", tags=["msgs"]
)
msgRepo = MessageRepository()
chatRepo = ChatRepository()
msgServuice = MessageService(msgRepo, chatRepo)

@MsgRouter.get("/")
async def get():
    with open("app/static/index.html") as f:
        html = f.read()
    return HTMLResponse(html)

@MsgRouter.get("/stream")
async def stream(chat_id: str, query: str):
    return EventSourceResponse(msgServuice.get_chat_stream(chat_id, query))

