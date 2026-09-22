from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "student@example.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    delete_response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    assert delete_response.status_code == 200
    data = delete_response.json()
    assert data["message"] == f"Removed {email} from {activity_name}"

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_participant_raises_if_email_not_signed_up():
    activity_name = "Programming Class"
    email = "not-signed-up@example.edu"

    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"
