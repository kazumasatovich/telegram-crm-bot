from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Status(Enum):
    NEW = "Новая"
    IN_PROGRESS = "В процессе"
    CLOSED = "Закрыта"


@dataclass
class Request:
    id: int
    user_id: int
    username: str
    text: str
    status: Status = Status.NEW
    created_at: datetime = field(default_factory=datetime.now)
