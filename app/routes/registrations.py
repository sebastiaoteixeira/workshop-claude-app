from fastapi import APIRouter

from app.db import Conn
from app.repositories import events, participants, registrations
from app.schemas import ParticipantIn, Registration

router = APIRouter(prefix="/events/{event_id}/registrations", tags=["registrations"])


@router.post("", status_code=201)
def register(conn: Conn, event_id: int, data: ParticipantIn) -> Registration:
    event = events.get_event(conn, event_id)
    participant = participants.find_or_create(conn, data)
    return registrations.register(conn, event, participant)


@router.get("")
def list_registrations(conn: Conn, event_id: int) -> list[Registration]:
    events.get_event(conn, event_id)
    return registrations.list_for_event(conn, event_id)
