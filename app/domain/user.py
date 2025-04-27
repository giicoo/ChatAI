from dataclasses import dataclass, field
import datetime

@dataclass
class User:
    id: str
    telegram_id: int
    username: str
    created_at: datetime = field(default_factory=datetime.now)