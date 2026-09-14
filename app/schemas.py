from datetime import datetime

from pydantic import BaseModel


class EventIn(BaseModel):
    title: str
    starts_at: datetime
    capacity: int


class Event(EventIn):
    id: int


class ParticipantIn(BaseModel):
    name: str
    email: str


class Participant(ParticipantIn):
    id: int


class Registration(BaseModel):
    event_id: int
    participant: Participant
    created_at: datetime
