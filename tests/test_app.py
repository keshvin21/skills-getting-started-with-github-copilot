from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "student@example.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    delete_response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert delete_response.status_code == 200
    data = delete_response.json()
    assert data["message"] == f"Removed {email} from {activity_name}"

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_participant_raises_if_email_not_signed_up():
    # Arrange
    activity_name = "Programming Class"
    email = "not-signed-up@example.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_signup_rejects_duplicate_participant():
    # Arrange
    activity_name = "Soccer Club"
    email = "duplicate@example.edu"
    signup_url = f"/activities/{activity_name}/signup?email={email}"
    first_response = client.post(signup_url)

    # Act
    duplicate_response = client.post(signup_url)

    # Assert
    assert first_response.status_code == 200
    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["detail"] == (
        "Student is already signed up for this activity"
    )
    participants = client.get("/activities").json()[activity_name]["participants"]
    assert participants.count(email) == 1
