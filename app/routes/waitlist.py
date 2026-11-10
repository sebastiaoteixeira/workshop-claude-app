from fastapi import APIRouter

from app.db import Conn
from app.errors import ConflictError
from app.repositories import events, participants, registrations, waitlist
from app.schemas import ParticipantIn, Registration, WaitlistEntry

router = APIRouter(prefix="/events/{event_id}/waitlist", tags=["waitlist"])


@router.post("", status_code=201)
def join(conn: Conn, event_id: int, data: ParticipantIn) -> WaitlistEntry:
    event = events.get_event(conn, event_id)
    if registrations.count_for_event(conn, event_id) < event.capacity:
        raise ConflictError("event has available seats")
    participant = participants.find_or_create(conn, data)
    if registrations.is_registered(conn, event_id, participant.id):
        raise ConflictError("participant already registered")
    return waitlist.join(conn, event_id, participant)


@router.get("")
def list_waitlist(conn: Conn, event_id: int) -> list[WaitlistEntry]:
    events.get_event(conn, event_id)
    return waitlist.list_for_event(conn, event_id)


@router.post("/promote", status_code=201)
def promote(conn: Conn, event_id: int) -> Registration:
    event = events.get_event(conn, event_id)
    participant = waitlist.first(conn, event_id)
    registration = registrations.register(conn, event, participant)
    waitlist.remove(conn, event_id, participant.id)
    return registration
