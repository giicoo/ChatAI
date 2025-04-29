from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

@dataclass
class Chat:
    id: str = None
    telegram_id: int = 0
    model: Literal["llama2"] = "llama2"
    title: str = None
    created_at: datetime = field(default_factory=datetime.now)