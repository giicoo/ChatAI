from typing import List
from bson import ObjectId
from app.schemas.chats import ChatDocument


class ChatRepository:
    async def create_chat(self, chat: ChatDocument) -> ChatDocument:
        await chat.insert() 
        return chat

    async def get_chat(self, chat_id: str) -> ChatDocument:
        chat = await ChatDocument.get(ObjectId(chat_id))
        return chat

    async def get_chats_by_telegram_id(self, telegram_id: int) -> List[ChatDocument]:
        chats = await ChatDocument.find(ChatDocument.telegram_id == telegram_id).to_list()
        return chats

    async def delete_chat(self, chat_id: str):
        chat = await ChatDocument.get(ObjectId(chat_id))
        if chat:
            await chat.delete()

