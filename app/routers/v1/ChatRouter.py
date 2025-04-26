from typing import List, Optional

from fastapi import APIRouter, Depends, status

ChatRouter = APIRouter(
    prefix="/v1/chats", tags=["chats"]
)

@ChatRouter.get("/")
def test():
    return 