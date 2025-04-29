from typing import List
from bson import ObjectId
from app.schemas.messages import MessageDocument


class MessageRepository:
    async def create_msg(self, msg: MessageDocument) -> MessageDocument:
        await msg.insert() 
        return msg
    
    async def get_msgs_by_chat_id(self, chat_id: str) -> List[MessageDocument]:
        msgs = await MessageDocument.find(MessageDocument.chat_id == ObjectId(chat_id)).to_list()
        return msgs

    
