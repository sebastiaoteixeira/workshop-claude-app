from tests.conftest import ANA, EVENT


def test_create_event_requires_admin_token(client):
    assert client.post("/events", json=EVENT).status_code == 401


def test_create_event(create_event):
    assert create_event() == {"id": 1, **EVENT}


def test_create_event_rejects_zero_capacity(client, admin_headers):
    response = client.post("/events", json={**EVENT, "capacity": 0}, headers=admin_headers)
    assert response.status_code == 422


def test_get_event(client, create_event):
    event = create_event()
    body = client.get(f"/events/{event['id']}").json()
    assert body.items() >= event.items()


def test_get_event_not_found(client):
    assert client.get("/events/999").status_code == 404


def test_list_events_empty(client):
    body = client.get("/events").json()
    assert body == {"items": [], "page": 1, "page_size": 20, "total": 0, "total_pages": 0}


def test_list_events_second_page(client, create_event):
    ids = [create_event(title=f"Talk {n}")["id"] for n in range(5)]
    body = client.get("/events", params={"page": 2, "page_size": 2}).json()
    assert [event["id"] for event in body["items"]] == ids[2:4]
    assert body["page"] == 2
    assert body["total_pages"] == 3


def test_get_event_includes_available_seats(client, create_event, register):
    event = create_event(capacity=3)
    register(event, ANA)
    body = client.get(f"/events/{event['id']}").json()
    assert body["available_seats"] == 2
