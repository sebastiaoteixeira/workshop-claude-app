from tests.conftest import ANA, BRUNO


def test_register_participant(create_event, register):
    event = create_event()
    response = register(event, ANA)
    assert response.status_code == 201
    body = response.json()
    assert body["event_id"] == event["id"]
    assert body["participant"] == {"id": 1, **ANA}


def test_register_in_unknown_event(register):
    assert register({"id": 999}, ANA).status_code == 404


def test_register_twice_conflicts(create_event, register):
    event = create_event()
    register(event, ANA)
    assert register(event, ANA).status_code == 409


def test_register_when_full_conflicts(create_event, register):
    event = create_event(capacity=1)
    register(event, ANA)
    assert register(event, BRUNO).status_code == 409


def test_list_registrations(client, create_event, register):
    event = create_event()
    register(event, ANA)
    register(event, BRUNO)
    body = client.get(f"/events/{event['id']}/registrations").json()
    assert [r["participant"]["email"] for r in body] == [ANA["email"], BRUNO["email"]]


def test_cancel_registration_frees_capacity(client, create_event, register):
    event = create_event(capacity=1)
    ana = register(event, ANA).json()["participant"]
    assert register(event, BRUNO).status_code == 409
    response = client.delete(f"/events/{event['id']}/registrations/{ana['id']}")
    assert response.status_code == 204
    assert register(event, BRUNO).status_code == 201
