from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app import settings
from app.db import connect, get_connection, migrate
from app.main import app

EVENT = {"title": "Hackathon NEI", "starts_at": "2026-11-20T18:00:00", "capacity": 2}
ANA = {"name": "Ana Martins", "email": "ana.martins@ua.pt"}
BRUNO = {"name": "Bruno Silva", "email": "bruno.silva@ua.pt"}


@pytest.fixture
def client() -> Iterator[TestClient]:
    conn = connect(":memory:")
    migrate(conn)
    app.dependency_overrides[get_connection] = lambda: conn
    yield TestClient(app)
    app.dependency_overrides.clear()
    conn.close()


@pytest.fixture
def admin_headers() -> dict[str, str]:
    return {"X-Admin-Token": settings.ADMIN_TOKEN}


@pytest.fixture
def create_event(client, admin_headers):
    def create(**overrides) -> dict:
        response = client.post("/events", json={**EVENT, **overrides}, headers=admin_headers)
        assert response.status_code == 201
        return response.json()

    return create


@pytest.fixture
def register(client):
    def register_in(event: dict, participant: dict):
        return client.post(f"/events/{event['id']}/registrations", json=participant)

    return register_in
