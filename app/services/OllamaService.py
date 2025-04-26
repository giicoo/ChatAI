import asyncio
import json
import time
from ollama import AsyncClient, Client

class OllamaService:
    def __init__(self,
                 address: str = "http://localhost:11434",
                 model: str = "llama2"):
        self._address = address
        self._model = model
        self.client = AsyncClient(host=self._address)

    async def get_chat_stream(self, query: str):
        chat_messages = [{'role': 'user', 'content': query}]
        
        response =  await self.client.chat(model=self._model, messages=chat_messages, stream=True)
        
        async for chunk in response:
            yield chunk['message']['content']
            
            