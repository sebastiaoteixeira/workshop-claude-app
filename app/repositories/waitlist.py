from sqlite3 import Connection, Row

from app.errors import ConflictError, NotFoundError
from app.repositories import participants
from app.schemas import Participant, WaitlistEntry

ENTRIES = """
    SELECT event_id, participant_id, created_at,
           row_number() OVER (PARTITION BY event_id ORDER BY id) AS position
    FROM waitlist
"""


def _entry(conn: Connection, row: Row) -> WaitlistEntry:
    return WaitlistEntry(
        event_id=row["event_id"],
        position=row["position"],
        created_at=row["created_at"],
        participant=participants.get(conn, row["participant_id"]),
    )


def is_waiting(conn: Connection, event_id: int, participant_id: int) -> bool:
    row = conn.execute(
        "SELECT 1 FROM waitlist WHERE event_id = ? AND participant_id = ?",
        (event_id, participant_id),
    ).fetchone()
    return row is not None


def join(conn: Connection, event_id: int, participant: Participant) -> WaitlistEntry:
    if is_waiting(conn, event_id, participant.id):
        raise ConflictError("participant already in the waitlist")
    with conn:
        conn.execute(
            "INSERT INTO waitlist (event_id, participant_id) VALUES (?, ?)",
            (event_id, participant.id),
        )
    row = conn.execute(
        f"SELECT * FROM ({ENTRIES}) WHERE event_id = ? AND participant_id = ?",
        (event_id, participant.id),
    ).fetchone()
    return _entry(conn, row)


def list_for_event(conn: Connection, event_id: int) -> list[WaitlistEntry]:
    rows = conn.execute(
        f"SELECT * FROM ({ENTRIES}) WHERE event_id = ? ORDER BY position", (event_id,)
    )
    return [_entry(conn, row) for row in rows]


def first(conn: Connection, event_id: int) -> Participant:
    row = conn.execute(
        "SELECT participant_id FROM waitlist WHERE event_id = ? ORDER BY id LIMIT 1", (event_id,)
    ).fetchone()
    if row is None:
        raise NotFoundError(f"waitlist for event {event_id} is empty")
    return participants.get(conn, row["participant_id"])


def remove(conn: Connection, event_id: int, participant_id: int) -> None:
    with conn:
        conn.execute(
            "DELETE FROM waitlist WHERE event_id = ? AND participant_id = ?",
            (event_id, participant_id),
        )
