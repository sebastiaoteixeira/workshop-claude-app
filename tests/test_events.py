from tests.conftest import EVENT


def test_create_event_requires_admin_token(client):
    assert client.post("/events", json=EVENT).status_code == 401


def test_create_event(create_event):
    assert create_event() == {"id": 1, **EVENT}


def test_get_event(client, create_event):
    event = create_event()
    assert client.get(f"/events/{event['id']}").json() == event


def test_get_event_not_found(client):
    assert client.get("/events/999").status_code == 404
