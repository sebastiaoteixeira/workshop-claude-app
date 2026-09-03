from datetime import datetime

from pydantic import BaseModel


class EventIn(BaseModel):
    title: str
    starts_at: datetime
    capacity: int


class Event(EventIn):
    id: int
