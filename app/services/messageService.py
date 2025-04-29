from ollama import AsyncClient

from app.repository.chat import ChatRepository
from app.repository.message import MessageRepository
from app.schemas.messages import MessageDocument

class MessageService:
    def __init__(self, repoMsg: MessageRepository, repoChat: ChatRepository):
        self.client = AsyncClient(host="")
        self.repoMsg = repoMsg
        self.repoChat = repoChat

    async def get_chat_stream(self, chat_id: str, query: str):
        await self.repoMsg.create_msg(MessageDocument(chat_id=chat_id, role="user",content=query))
        msgs = await self.repoMsg.get_msgs_by_chat_id(chat_id=chat_id)
        chat_messages = [{"role":msg.role, "content":msg.content} for msg in msgs]
        
        chat = await self.repoChat.get_chat(chat_id=chat_id)
        
        response =  await self.client.chat(model=chat.model, messages=chat_messages, stream=True)
        full_response = ""
        async for chunk in response:
            full_response += chunk['message']['content']
            yield chunk['message']['content']
        
        await self.repoMsg.create_msg(MessageDocument(chat_id=chat_id, role="assistant", content=full_response))

        

            
            