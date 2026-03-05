def test_get_activities_returns_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert "participants" in payload["Chess Club"]
    assert isinstance(payload["Chess Club"]["participants"], list)


def test_get_activities_disables_caching(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.headers.get("cache-control") == "no-store"
