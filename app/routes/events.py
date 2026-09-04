import sqlite3
from typing import Annotated

from fastapi import APIRouter, Depends

from app.db import get_connection
from app.repositories import events
from app.schemas import Event, EventIn

router = APIRouter(prefix="/events", tags=["events"])


@router.get("")
def list_events(conn: Annotated[sqlite3.Connection, Depends(get_connection)]) -> list[Event]:
    return events.list_events(conn)


@router.post("", status_code=201)
def create_event(
    conn: Annotated[sqlite3.Connection, Depends(get_connection)], data: EventIn
) -> Event:
    return events.create_event(conn, data)
