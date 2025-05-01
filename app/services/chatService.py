from typing import List
from app.core.enviroment import OLLAMA_URI
from ollama import AsyncClient
from app.core.log import Logger
from app.domain.chat import Chat
from app.repository.chat import ChatRepository
from app.schemas.chats import ChatDocument


class ChatService:
    def __init__(self, repository: ChatRepository):
        self.client = AsyncClient(host=OLLAMA_URI)
        self.repo = repository

    async def create_chat_auto(self, chat: Chat, query: str) -> str:
        try:
            prompt = f"""
            You are an assistant that generates short, clear chat titles based on the first message in a conversation.
            without unnecessary words and explanations, just the title. 
            Message: "{query}"

            Generate a concise chat title:
            """
            response = await self.client.chat(model="llama2", messages=[
                {"role": "user", "content": prompt}
            ])
            chat.title = response['message']['content'].strip()
            chatDB = ChatDocument(telegram_id=chat.telegram_id,model=chat.model,title=chat.title)
            resultDB = await self.repo.create_chat(chatDB)
        except Exception as e:
            raise Exception(f"chat create auto service: {e}")
        
        return str(resultDB.id)
    
    async def create_chat(self, chat: Chat) -> str:
        try:
            chatDB = ChatDocument(telegram_id=chat.telegram_id,model=chat.model,title=chat.title)
            resultDB = await self.repo.create_chat(chatDB)
        except Exception as e:
            raise Exception(f"chat create service: {e}")
        
        return str(resultDB.id)
    

    async def get_chat(self, chat_id: str) -> Chat:
        try:
            chat = await self.repo.get_chat(chat_id)
        except Exception as e:
            raise Exception(f"chat get service: {e}")
        
        return Chat(id=chat.id,
                    telegram_id=chat.telegram_id, 
                    model=chat.model,
                    title=chat.title,
                    created_at=chat.created_at)


    async def get_chats_by_telegram_id(self, telegram_id: int) -> List[Chat]:
        try: 
            chats = await self.repo.get_chats_by_telegram_id(telegram_id)
        except Exception as e:
            raise Exception(f"chat get chats service: {e}")
        
        chatsResponse = [Chat(id=chat.id,
                              telegram_id=chat.telegram_id, 
                              model=chat.model,
                              title=chat.title,
                              created_at=chat.created_at) for chat in chats]
        return chatsResponse
        
        
    async def delete_chat(self, chat_id:str):
        try:
            await self.repo.delete_chat(chat_id)
        except Exception as e:
            raise Exception(f"chat delete service: {e}")
