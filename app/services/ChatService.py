from typing import List, Optional

from fastapi import Depends
from app.repository import Repository


class ChatService:
    repo: Repository

    def __init__(self, repo: Repository = Depends()) -> None:
        self.repo = repo

    