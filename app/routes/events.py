from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app import settings
from app.auth import require_admin
from app.db import Conn
from app.repositories import events, registrations
from app.schemas import Event, EventDetail, EventIn, Page

router = APIRouter(prefix="/events", tags=["events"])


@router.get("")
def list_events(
    conn: Conn,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = settings.DEFAULT_PAGE_SIZE,
) -> Page[Event]:
    return events.list_events(conn, page, page_size)


@router.post("", status_code=201, dependencies=[Depends(require_admin)])
def create_event(conn: Conn, data: EventIn) -> Event:
    return events.create_event(conn, data)


@router.get("/{event_id}")
def get_event(conn: Conn, event_id: int) -> EventDetail:
    event = events.get_event(conn, event_id)
    taken = registrations.count_for_event(conn, event_id)
    return EventDetail(**event.model_dump(), available_seats=event.capacity - taken)
