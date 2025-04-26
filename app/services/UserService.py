

from typing import Any
from bson import ObjectId
from fastapi import Depends
from app.repository.Repository import Repository
from app.schemas.Users import User, UserCreate


class UserService:
    repo: Repository

    def __init__(self, repo: Repository = Depends()) -> None:
        self.repo = repo

    def create_user(self, user: UserCreate) -> ObjectId:
        userDB = User(telegram_id=user.telegram_id, telegram_username=user.telegram_username).model_dump()
        id = self.repo.create_user(userDB)
        return id