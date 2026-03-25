import pytest


def test_get_activities_returns_configuration(client):
    response = client.get("/activities")
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert "Chess Club" in payload
    assert "Programming Class" in payload


def test_signup_happy_path(client):
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": new_email})
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {new_email} for {activity_name}"}

    # Validate participant was added
    activities_response = client.get("/activities").json()
    assert new_email in activities_response[activity_name]["participants"]


def test_signup_invalid_activity_returns_404(client):
    response = client.post("/activities/Bad%20Club/signup", params={"email": "a@b.com"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_email_returns_400(client):
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"
