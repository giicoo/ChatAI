import configparser
from typing import List

from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from app.schemas.Chats import Chat
from app.schemas.Users import User
from app.schemas.Messages import Message



class Repository:
    def __init__(self,):
        self.uri = ""

        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.db = self.client["db"]
        self.users = self.db["users"]
        self.chats = self.db["chats"]
        self.msgs = self.db["msgs"]
    
    def ping(self) -> str:
        try:
            self.client.admin.command('ping')
            return  "Pinged your deployment. You successfully connected to MongoDB!"
        except Exception as e:
            return e

    def create_user(self, user: dict[str, any]) -> ObjectId:
        u = self.users.insert_one(user)
        return u.inserted_id
    
    def create_chat(self, chat: dict[str, any]) -> ObjectId:
        c = self.chats.insert_one(chat)
        return c.inserted_id
    
    def delete_chat(self, chat_id: ObjectId):
        self.chats.delete_one({"_id":chat_id})
    
    def get_chats(self, telegram_id: int):
        chats: List[Chat] = []
        for chat in self.chats.find({"telegram_id":telegram_id}):
            print(chat)
    
    def create_message(self, msg: dict[str, any]) -> ObjectId:
        m = self.msgs.insert_one(msg)
        return m.inserted_id

    


