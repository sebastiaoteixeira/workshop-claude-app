from datetime import datetime

from pydantic import BaseModel, Field


class EventIn(BaseModel):
    title: str
    starts_at: datetime
    capacity: int = Field(gt=0)


class Event(EventIn):
    id: int


class EventDetail(Event):
    available_seats: int


class Page[T](BaseModel):
    items: list[T]
    page: int
    page_size: int
    total: int
    total_pages: int


class ParticipantIn(BaseModel):
    name: str
    email: str


class Participant(ParticipantIn):
    id: int


class Registration(BaseModel):
    event_id: int
    participant: Participant
    created_at: datetime


class WaitlistEntry(BaseModel):
    event_id: int
    position: int
    participant: Participant
    created_at: datetime
