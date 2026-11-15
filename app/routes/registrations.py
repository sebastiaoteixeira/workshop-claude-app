import csv
from io import StringIO

from fastapi import APIRouter, Response

from app.db import Conn
from app.repositories import events, participants, registrations
from app.schemas import ParticipantIn, Registration

router = APIRouter(prefix="/events/{event_id}/registrations", tags=["registrations"])

CSV_COLUMNS = ("name", "email", "created_at")


@router.post("", status_code=201)
def register(conn: Conn, event_id: int, data: ParticipantIn) -> Registration:
    event = events.get_event(conn, event_id)
    participant = participants.find_or_create(conn, data)
    return registrations.register(conn, event, participant)


@router.get("")
def list_registrations(conn: Conn, event_id: int) -> list[Registration]:
    events.get_event(conn, event_id)
    return registrations.list_for_event(conn, event_id)


@router.get(".csv", response_class=Response)
def export_registrations(conn: Conn, event_id: int) -> Response:
    events.get_event(conn, event_id)
    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(CSV_COLUMNS)
    writer.writerows(
        (r.participant.name, r.participant.email, r.created_at.isoformat())
        for r in registrations.list_for_event(conn, event_id)
    )
    return Response(buffer.getvalue(), media_type="text/csv")


@router.delete("/{participant_id}", status_code=204)
def cancel(conn: Conn, event_id: int, participant_id: int) -> None:
    events.get_event(conn, event_id)
    registrations.cancel(conn, event_id, participant_id)
