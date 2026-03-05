def test_unregister_success_removes_participant(client):
    signup_email = "temp.student@mergington.edu"
    client.post("/activities/Programming Class/signup", params={"email": signup_email})

    response = client.delete(
        "/activities/Programming Class/participants",
        params={"email": signup_email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {signup_email} from Programming Class"

    activities_response = client.get("/activities")
    participants = activities_response.json()["Programming Class"]["participants"]
    assert signup_email not in participants


def test_unregister_unknown_activity_returns_404(client):
    response = client.delete(
        "/activities/Unknown Club/participants",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_participant_returns_404(client):
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "missing@mergington.edu"},
    )

    assert response.status_code == 404
    assert "is not signed up" in response.json()["detail"]


def test_unregister_is_case_and_whitespace_insensitive(client):
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "  MICHAEL@MERGINGTON.EDU  "},
    )

    assert response.status_code == 200

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert "michael@mergington.edu" not in participants
