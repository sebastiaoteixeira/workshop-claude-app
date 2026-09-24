import sqlite3
from math import ceil
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app import settings
from app.auth import require_admin
from app.db import get_connection
from app.repositories import events
from app.schemas import Event, EventIn, Page

router = APIRouter(prefix="/events", tags=["events"])


@router.get("")
def list_events(
    conn: Annotated[sqlite3.Connection, Depends(get_connection)],
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1)] = settings.DEFAULT_PAGE_SIZE,
) -> Page[Event]:
    total = events.count_events(conn)
    return Page(
        items=events.list_events(conn, offset=(page - 1) * page_size, limit=page_size),
        page=page,
        page_size=page_size,
        total=total,
        total_pages=ceil(total / page_size),
    )


@router.post("", status_code=201, dependencies=[Depends(require_admin)])
def create_event(
    conn: Annotated[sqlite3.Connection, Depends(get_connection)], data: EventIn
) -> Event:
    return events.create_event(conn, data)


@router.get("/{event_id}")
def get_event(conn: Annotated[sqlite3.Connection, Depends(get_connection)], event_id: int) -> Event:
    return events.get_event(conn, event_id)
