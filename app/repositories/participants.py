from sqlite3 import Connection

from app.schemas import Participant, ParticipantIn


def get(conn: Connection, participant_id: int) -> Participant:
    row = conn.execute(
        "SELECT id, name, email FROM participants WHERE id = ?", (participant_id,)
    ).fetchone()
    return Participant(**row)


def find_or_create(conn: Connection, data: ParticipantIn) -> Participant:
    row = conn.execute(
        "SELECT id, name, email FROM participants WHERE email = ?", (data.email,)
    ).fetchone()
    if row is not None:
        return Participant(**row)
    with conn:
        cursor = conn.execute(
            "INSERT INTO participants (name, email) VALUES (?, ?)", (data.name, data.email)
        )
    return Participant(id=cursor.lastrowid, **data.model_dump())
