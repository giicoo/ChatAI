import logging
from typing import List
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import JSONResponse
from app.core.log import Logger
from app.domain.chat import Chat
from app.repository.chat import ChatRepository
from app.schemas.chats import ChatIn, ChatOut
from app.services.chatService import ChatService

ChatRouter = APIRouter(
    prefix="/v1/chats", tags=["chats"]
)

chatRepo = ChatRepository()
chatService = ChatService(chatRepo)

@ChatRouter.post("/create")
async def create_chat(chat: ChatIn):
    try:
        chat_id = await chatService.create_chat(Chat(telegram_id=chat.telegram_id, 
                                                    model=chat.model, 
                                                    title=chat.title))
    except Exception as e:
        Logger.error(e)
        raise HTTPException(status_code=500, detail=f"server error: {e}")

    return JSONResponse({"chat_id":chat_id}, 200)

@ChatRouter.post("/create-auto")
async def create_chat_auto(chat: ChatIn, query: str):
    try:
        chat_id = await chatService.create_chat_auto(Chat(telegram_id=chat.telegram_id, 
                                                          model=chat.model), query)
    except Exception as e:
        Logger.error(e)
        raise HTTPException(status_code=500, detail=f"server error: {e}")

    return JSONResponse({"chat_id":chat_id}, 200)

@ChatRouter.get("/get/{chat_id}", response_model=ChatOut)
async def get_chat(chat_id: str):
    try: 
        chat = await chatService.get_chat(chat_id)
        response = ChatOut(id=chat.id, 
                        telegram_id=chat.telegram_id, 
                        model=chat.model, 
                        title=chat.title,
                        created_at=chat.created_at)
    except Exception as e:
        Logger.error(e)
        raise HTTPException(status_code=500, detail=f"server error: {e}")
    return response

@ChatRouter.get("/get-all/{telegram_id}", response_model=List[ChatOut])
async def get_chats(telegram_id: int):
    try: 
        chats = await chatService.get_chats_by_telegram_id(telegram_id)
        response: List[ChatOut] = []
        for chat in chats:
            response.append(ChatOut(id=chat.id, 
                                    telegram_id=chat.telegram_id, 
                                    model=chat.model, 
                                    title=chat.title,
                                    created_at=chat.created_at))
            
    except Exception as e:
        Logger.error(e)
        raise HTTPException(status_code=500, detail=f"server error: {e}")
    return response

@ChatRouter.delete("/delete")
async def delete_chat(chat_id:str=None):
    try: 
        await chatService.delete_chat(chat_id)
    except Exception as e:
        Logger.error(e)
        raise HTTPException(status_code=500, detail=f"server error: {e}")