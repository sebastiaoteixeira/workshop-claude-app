import sqlite3
from typing import Annotated

from fastapi import APIRouter, Depends

from app.db import get_connection
from app.repositories import events, participants, registrations
from app.schemas import ParticipantIn, Registration

router = APIRouter(prefix="/events/{event_id}/registrations", tags=["registrations"])


@router.post("", status_code=201)
def register(
    conn: Annotated[sqlite3.Connection, Depends(get_connection)],
    event_id: int,
    data: ParticipantIn,
) -> Registration:
    event = events.get_event(conn, event_id)
    participant = participants.find_or_create(conn, data)
    return registrations.register(conn, event, participant)
