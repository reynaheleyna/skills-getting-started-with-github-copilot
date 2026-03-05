def test_signup_success_adds_participant(client):
    email = "new.student@mergington.edu"

    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert email in participants


def test_signup_unknown_activity_returns_404(client):
    response = client.post("/activities/Unknown Club/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_email_case_and_whitespace_insensitive(client):
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "  MICHAEL@MERGINGTON.EDU  "},
    )

    assert response.status_code == 409
    assert "already signed up" in response.json()["detail"]


def test_signup_rejects_full_activity(client):
    activity_name = "Art Studio"

    # Fill to capacity (15) from its initial 2 participants.
    for i in range(13):
        fill_email = f"fill{i}@mergington.edu"
        fill_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": fill_email},
        )
        assert fill_response.status_code == 200

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": "overflow@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == f"{activity_name} is full"
