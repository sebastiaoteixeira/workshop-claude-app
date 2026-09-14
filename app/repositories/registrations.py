from sqlite3 import Connection, Row

from app.errors import ConflictError
from app.schemas import Event, Participant, Registration

SELECT_REGISTRATIONS = """
    SELECT r.event_id, r.created_at, p.id, p.name, p.email
    FROM registrations r JOIN participants p ON p.id = r.participant_id
"""


def _registration(row: Row) -> Registration:
    return Registration(
        event_id=row["event_id"],
        created_at=row["created_at"],
        participant=Participant(id=row["id"], name=row["name"], email=row["email"]),
    )


def count_for_event(conn: Connection, event_id: int) -> int:
    return conn.execute(
        "SELECT count(*) FROM registrations WHERE event_id = ?", (event_id,)
    ).fetchone()[0]


def is_registered(conn: Connection, event_id: int, participant_id: int) -> bool:
    row = conn.execute(
        "SELECT 1 FROM registrations WHERE event_id = ? AND participant_id = ?",
        (event_id, participant_id),
    ).fetchone()
    return row is not None


def register(conn: Connection, event: Event, participant: Participant) -> Registration:
    if is_registered(conn, event.id, participant.id):
        raise ConflictError("participant already registered")
    if count_for_event(conn, event.id) >= event.capacity:
        raise ConflictError("event is full")
    with conn:
        conn.execute(
            "INSERT INTO registrations (event_id, participant_id) VALUES (?, ?)",
            (event.id, participant.id),
        )
    row = conn.execute(
        f"{SELECT_REGISTRATIONS} WHERE r.event_id = ? AND r.participant_id = ?",
        (event.id, participant.id),
    ).fetchone()
    return _registration(row)
