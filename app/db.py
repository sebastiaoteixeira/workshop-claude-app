import sqlite3
from collections.abc import Iterator
from pathlib import Path

from app import settings

MIGRATIONS_DIR = Path(__file__).resolve().parent.parent / "migrations"


def connect(path: Path | str) -> sqlite3.Connection:
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def migrate(conn: sqlite3.Connection) -> None:
    conn.execute("CREATE TABLE IF NOT EXISTS schema_migrations (name TEXT PRIMARY KEY)")
    applied = {row["name"] for row in conn.execute("SELECT name FROM schema_migrations")}
    for migration in sorted(MIGRATIONS_DIR.glob("*.sql")):
        if migration.name not in applied:
            conn.executescript(migration.read_text())
            conn.execute("INSERT INTO schema_migrations (name) VALUES (?)", (migration.name,))
    conn.commit()


def get_connection() -> Iterator[sqlite3.Connection]:
    conn = connect(settings.DATABASE_PATH)
    try:
        yield conn
    finally:
        conn.close()
