import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(dotenv_path=dotenv_path, override=True)

# Теперь можно получить переменные окружения
API_VERSION = os.getenv("API_VERSION")
APP_NAME = os.getenv("APP_NAME")
MONGO_URI = os.getenv("MONGO_URI")
OLLAMA_URI = os.getenv("OLLAMA_URI")

# Печатаем для проверки
print(f"API_VERSION: {API_VERSION}")
print(f"APP_NAME: {APP_NAME}")
print(f"MONGO_URI: {MONGO_URI}")
print(f"OLLAMA_URI: {OLLAMA_URI}")
