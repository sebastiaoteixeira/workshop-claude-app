"""Rebuilds the workshop database from scratch with a fixed, reproducible data set."""

from datetime import datetime, timedelta
from random import Random

from app import settings
from app.db import connect, migrate

EVENTS = [
    ("Workshop de Git", "2026-10-06T18:00:00", 30),
    ("Noite de Code Review", "2026-10-13T18:30:00", 20),
    ("Talk: Sistemas Distribuidos", "2026-10-20T18:00:00", 60),
    ("Hackathon NEI", "2026-10-24T09:00:00", 25),
    ("Workshop de Docker", "2026-11-03T18:00:00", 30),
    ("Sessao de Esclarecimento de Erasmus", "2026-11-10T17:00:00", 40),
]

FIRST_NAMES = (
    "Ana Bruno Carla Daniel Eva Filipe Gabriela Hugo Ines Joao "
    "Leonor Miguel Nuno Olivia Pedro Rita Rui Sara Tiago"
).split()
LAST_NAMES = "Martins Silva Costa Ferreira Oliveira Santos Pereira Sousa".split()

KNOWN = [("Ana", "Martins"), ("Rui", "Costa")]
IMPORTED_FROM_FORM = [
    ("Ana Martins", "Ana.Martins@ua.pt"),
    ("Rui Costa", "rui.costa@ua.pt "),
]

SEED = 2026
FIRST_REGISTRATION = datetime(2026, 9, 21, 10, 0)


def participants() -> list[tuple[str, str]]:
    rng = Random(SEED)
    pairs = [
        (first, last) for first in FIRST_NAMES for last in LAST_NAMES if (first, last) not in KNOWN
    ]
    chosen = KNOWN + rng.sample(pairs, 36)
    people = [(f"{first} {last}", f"{first}.{last}@ua.pt".lower()) for first, last in chosen]
    return people + IMPORTED_FROM_FORM


def registrations(people_count: int) -> list[tuple[int, int, str]]:
    rng = Random(SEED)
    rows = []
    for event_id, (_, _, capacity) in enumerate(EVENTS, start=1):
        taken = rng.sample(range(1, people_count - len(IMPORTED_FROM_FORM) + 1), min(capacity, 11))
        if event_id == 4:
            taken = list(range(1, capacity + 1)) + [people_count - 1, people_count]
        rows += [
            (event_id, pid, (FIRST_REGISTRATION + timedelta(hours=event_id, minutes=n)).isoformat())
            for n, pid in enumerate(taken)
        ]
    return rows


def main() -> None:
    settings.DATABASE_PATH.unlink(missing_ok=True)
    settings.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = connect(settings.DATABASE_PATH)
    migrate(conn)
    people = participants()
    with conn:
        conn.executemany("INSERT INTO events (title, starts_at, capacity) VALUES (?, ?, ?)", EVENTS)
        conn.executemany("INSERT INTO participants (name, email) VALUES (?, ?)", people)
        conn.executemany(
            "INSERT INTO registrations (event_id, participant_id, created_at) VALUES (?, ?, ?)",
            registrations(len(people)),
        )
    conn.close()
    print(f"seeded {settings.DATABASE_PATH}")


if __name__ == "__main__":
    main()
