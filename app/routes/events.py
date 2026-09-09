import sqlite3
from typing import Annotated

from fastapi import APIRouter, Depends

from app.auth import require_admin
from app.db import get_connection
from app.repositories import events
from app.schemas import Event, EventIn

router = APIRouter(prefix="/events", tags=["events"])


@router.get("")
def list_events(conn: Annotated[sqlite3.Connection, Depends(get_connection)]) -> list[Event]:
    return events.list_events(conn)


@router.post("", status_code=201, dependencies=[Depends(require_admin)])
def create_event(
    conn: Annotated[sqlite3.Connection, Depends(get_connection)], data: EventIn
) -> Event:
    return events.create_event(conn, data)


@router.get("/{event_id}")
def get_event(conn: Annotated[sqlite3.Connection, Depends(get_connection)], event_id: int) -> Event:
    return events.get_event(conn, event_id)
