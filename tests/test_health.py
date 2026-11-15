from tests.conftest import ANA


def test_health_reports_counts(client, create_event, register):
    event = create_event()
    register(event, ANA)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "events": 1, "participants": 1, "registrations": 1}
