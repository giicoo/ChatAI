import asyncio
import time
import json
from fastapi import APIRouter
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse, StreamingResponse
from ollama import AsyncClient, chat
from sse_starlette import EventSourceResponse
from app.schemas.Messages import ChatRequest
from app.services.OllamaService import OllamaService

MsgRouter = APIRouter(
    prefix="/v1/msgs", tags=["msgs"]
)
ai_service = OllamaService()

@MsgRouter.get("/")
async def get():
    return HTMLResponse(html)

@MsgRouter.get("/stream")
async def stream(query: str):
    return EventSourceResponse(ai_service.get_chat_stream(query))


html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Chat Stream Test (EventSource)</title>
</head>
<body>

<h1>Chat Stream Test (EventSource)</h1>
<form id="chat-form">
    <input type="text" id="message" autocomplete="off" placeholder="Type your message..." required />
    <button type="submit">Send</button>
</form>

<ul id="messages"></ul>

<script>
    const form = document.getElementById('chat-form');
    const input = document.getElementById('message');
    const messages = document.getElementById('messages');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const query = input.value.trim();
        if (!query) return;

        // Создаём новый EventSource для каждого запроса
        const eventSource = new EventSource(`/v1/msgs/stream?query=${encodeURIComponent(query)}`);

        // Создаём новый элемент для отображения сообщения
        const currentMessage = document.createElement('li');
        currentMessage.textContent = `You: ${query} - `;
        messages.appendChild(currentMessage);

        eventSource.onmessage = function(event) {
            if (event.data === '[DONE]') {
                eventSource.close();
                return;
            }
            currentMessage.textContent += event.data;
        };

        eventSource.onerror = function(error) {
            console.error('EventSource failed:', error);
            eventSource.close();
        };

        input.value = ''; // Очистить поле ввода
    });
</script>

</body>
</html>


"""