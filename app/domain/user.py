from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class User:
    id: str = None
    telegram_id: int = 0
    username: str = None
    created_at: datetime = field(default_factory=datetime.now)