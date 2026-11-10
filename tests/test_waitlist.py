from tests.conftest import ANA, BRUNO, CARLA


def waitlist_of(client, event: dict) -> list[tuple[int, str]]:
    body = client.get(f"/events/{event['id']}/waitlist").json()
    return [(entry["position"], entry["participant"]["email"]) for entry in body]


def promote(client, event: dict):
    return client.post(f"/events/{event['id']}/waitlist/promote")


def test_join_waitlist_when_full(full_event, join_waitlist):
    response = join_waitlist(full_event, BRUNO)
    assert response.status_code == 201
    body = response.json()
    assert body["event_id"] == full_event["id"]
    assert body["position"] == 1
    assert body["participant"] == {"id": 2, **BRUNO}


def test_join_waitlist_with_seats_available_conflicts(create_event, join_waitlist):
    assert join_waitlist(create_event(), BRUNO).status_code == 409


def test_join_waitlist_twice_conflicts(full_event, join_waitlist):
    join_waitlist(full_event, BRUNO)
    assert join_waitlist(full_event, BRUNO).status_code == 409


def test_join_waitlist_when_registered_conflicts(full_event, join_waitlist):
    assert join_waitlist(full_event, ANA).status_code == 409


def test_join_waitlist_in_unknown_event(join_waitlist):
    assert join_waitlist({"id": 999}, BRUNO).status_code == 404


def test_list_waitlist_in_arrival_order(client, full_event, join_waitlist):
    join_waitlist(full_event, BRUNO)
    join_waitlist(full_event, CARLA)
    assert waitlist_of(client, full_event) == [(1, BRUNO["email"]), (2, CARLA["email"])]


def test_list_waitlist_in_unknown_event(client):
    assert client.get("/events/999/waitlist").status_code == 404


def test_promote_first_after_cancel(client, full_event, join_waitlist):
    join_waitlist(full_event, BRUNO)
    join_waitlist(full_event, CARLA)
    client.delete(f"/events/{full_event['id']}/registrations/1")
    response = promote(client, full_event)
    assert response.status_code == 201
    assert response.json()["participant"]["email"] == BRUNO["email"]
    assert waitlist_of(client, full_event) == [(1, CARLA["email"])]


def test_promote_when_full_conflicts(client, full_event, join_waitlist):
    join_waitlist(full_event, BRUNO)
    assert promote(client, full_event).status_code == 409
    assert waitlist_of(client, full_event) == [(1, BRUNO["email"])]


def test_promote_empty_waitlist_not_found(client, create_event):
    assert promote(client, create_event()).status_code == 404
