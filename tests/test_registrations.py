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
