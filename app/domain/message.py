from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

@dataclass
class Message:
    id: str = None
    chat_id: str = None
    role: Literal["user", "assistant"] = "user"
    content: str = None
    created_at: datetime = field(default_factory=datetime.now)
