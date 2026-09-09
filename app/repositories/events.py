from sqlite3 import Connection

from app.errors import NotFoundError
from app.schemas import Event, EventIn

COLUMNS = "id, title, starts_at, capacity"


def list_events(conn: Connection) -> list[Event]:
    rows = conn.execute(f"SELECT {COLUMNS} FROM events ORDER BY id")
    return [Event(**row) for row in rows]


def get_event(conn: Connection, event_id: int) -> Event:
    row = conn.execute(f"SELECT {COLUMNS} FROM events WHERE id = ?", (event_id,)).fetchone()
    if row is None:
        raise NotFoundError(f"event {event_id} not found")
    return Event(**row)


def create_event(conn: Connection, data: EventIn) -> Event:
    with conn:
        cursor = conn.execute(
            "INSERT INTO events (title, starts_at, capacity) VALUES (?, ?, ?)",
            (data.title, data.starts_at.isoformat(), data.capacity),
        )
    return Event(id=cursor.lastrowid, **data.model_dump())
