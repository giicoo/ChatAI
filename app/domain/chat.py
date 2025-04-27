from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

@dataclass
class Chat:
    telegram_id: int
    model: Literal["llama2"]
    title: str
    created_at: datetime = field(default_factory=datetime.now)