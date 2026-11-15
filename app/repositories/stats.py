from sqlite3 import Connection

TABLES = ("events", "participants", "registrations")


def counts(conn: Connection) -> dict[str, int]:
    return {table: conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0] for table in TABLES}
