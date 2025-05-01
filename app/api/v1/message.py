from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from sse_starlette import EventSourceResponse
from app.core.log import Logger
from app.repository.chat import ChatRepository
from app.repository.message import MessageRepository
from app.schemas.messages import MessageOut
from app.services.messageService import MessageService

MsgRouter = APIRouter(
    prefix="/v1/msgs", tags=["msgs"]
)
msgRepo = MessageRepository()
chatRepo = ChatRepository()
msgServuice = MessageService(msgRepo, chatRepo)

@MsgRouter.get("/")
async def get():
    try:
        with open("app/static/index.html") as f:
            html = f.read()
        return HTMLResponse(html)
    except Exception as e:
        Logger.error(e)
        raise HTTPException(status_code=500, detail=f"server error: {e}")


@MsgRouter.post("/stream")
async def stream(chat_id: str, query: str):
    try:
        return EventSourceResponse(msgServuice.stream(chat_id=chat_id,
                                                      query=query))
    except Exception as e:
        Logger.error(e)
        raise HTTPException(status_code=500, detail=f"server error: {e}")

@MsgRouter.get("/restream")
async def restream(chat_id: str, msg_user_id:str, msg_assistent_id:str, query: str):
    try:
        return EventSourceResponse(msgServuice.restream(chat_id=chat_id,
                                                        msg_user_id=msg_user_id,
                                                        msg_assistent_id=msg_assistent_id,
                                                        query=query))
    except Exception as e:
        Logger.error(e)
        raise HTTPException(status_code=500, detail=f"server error: {e}")

@MsgRouter.get("/msgs/{chat_id}", response_model=List[MessageOut])
async def get_msgs(chat_id:str):
    try:
        msgs = await msgServuice.get_msgs(chat_id=chat_id)
        response = [MessageOut(id=msg.id,
                            chat_id=msg.chat_id,
                            role=msg.role,
                            content=msg.content,
                            created_at=msg.created_at) for msg in msgs]
        return response
    except Exception as e:
        Logger.error(e)
        raise HTTPException(status_code=500, detail=f"server error: {e}")