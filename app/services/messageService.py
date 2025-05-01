import asyncio
from typing import List
from ollama import AsyncClient
from app.core.log import Logger
from app.core.enviroment import OLLAMA_URI
from app.domain.message import Message
from app.repository.chat import ChatRepository
from app.repository.message import MessageRepository
from app.schemas.messages import MessageDocument

class MessageService:
    def __init__(self, repoMsg: MessageRepository, repoChat: ChatRepository):
        self.client = AsyncClient(host=OLLAMA_URI)
        self.repoMsg = repoMsg
        self.repoChat = repoChat

    async def stream(self, chat_id: str, query: str):
        """
        Что происходит:
        1. Создается документ сообщения от user и сохраняется в repoMsg;
        2. Выбирают и обрабатываются все сообщения из нужного чата;
        3. Получают сам чат (для получения нужной модели);
        4. Генерируется ответ от нужной модели, стримится с помощью yield и сохраняется весь ответ в full_response
        5. Создается документ сообщения от модели и сохраняется в repoMsg;
        """
        try:
            await self.repoMsg.create_msg(MessageDocument(chat_id=chat_id, role="user",content=query))
            msgs = await self.repoMsg.get_msgs_by_chat_id(chat_id=chat_id)
            chat_messages = [{"role":msg.role, "content":msg.content} for msg in msgs] # быстро выполняется, так как чаще всего в чатах в среднем 100-1000 сообщений

            chat = await self.repoChat.get_chat(chat_id=chat_id)
            
            response =  await self.client.chat(model=chat.model, messages=chat_messages, stream=True)
            full_response = ""
            async for chunk in response:
                full_response += chunk['message']['content']
                yield chunk['message']['content']

            await self.repoMsg.create_msg(MessageDocument(chat_id=chat_id, role="assistant", content=full_response))
        except Exception as e:
            Logger.error(f"stream message: {e}")
            yield "Произошла ошибка попробуйте еще раз."
    
    async def restream(self, chat_id: str, msg_user_id:str, msg_assistent_id: str, query: str):
        """
        Что происходит:
        1. Обновляется текст сообщения user;
        2. Получают все сообщения из нужного чата;
        3. Фильтруют их до сообщения которое необходимо перегенерировать невключительно;
        4. Передают историю этих отфильтрованных сообщений модели, для перегенерации;
        5. Генерируется ответ от нужной модели, стримится с помощью yield и сохраняется весь ответ в full_response
        6. Обновляется текст сообщения модели;
        
        Что позволяет:
        Перегенерировать ответ на определенное сообщение, используя всю историю до этого сообщения и не затрагивая изменениями другие сообщения.
        Порядок сообщений сохраняется.
        """
        try:
            await self.repoMsg.update_msg(msg_id=msg_user_id, new_msg=query)
            msgs = await self.repoMsg.get_msgs_by_chat_id(chat_id=chat_id)
            chat_messages = []
            for msg in msgs: # быстро выполняется, так как чаще всего в чатах в среднем 100-1000 сообщений
                if str(msg.id) == msg_assistent_id:
                    break
                chat_messages.append({"role":msg.role, "content":msg.content})
            chat = await self.repoChat.get_chat(chat_id=chat_id)
            
            response =  await self.client.chat(model=chat.model, messages=chat_messages, stream=True)
            full_response = ""
            async for chunk in response:
                full_response += chunk['message']['content']
                yield chunk['message']['content']
            
            await self.repoMsg.update_msg(msg_id=msg_assistent_id, new_msg=full_response)
        except Exception as e:
            Logger.error(f"stream message: {e}")
            yield "Произошла ошибка попробуйте еще раз."
        
    async def get_msgs(self, chat_id: str) -> List[Message]:
        try:
            msgs = await self.repoMsg.get_msgs_by_chat_id(chat_id=chat_id)
            response = [Message(id=msg.id,
                                chat_id=msg.chat_id,
                                role=msg.role,
                                content=msg.content,
                                created_at=msg.created_at)  for msg in msgs]
            return response
        except Exception as e:
            raise Exception(f"service message get: {e}")
        

            
            