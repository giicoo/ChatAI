from dataclasses import dataclass, field
import datetime
from typing import Literal

@dataclass
class Message:
    id: str
    chat_id: str
    role: Literal["user", "assistant"]
    content: str
    created_at: datetime = field(default_factory=datetime.now)
