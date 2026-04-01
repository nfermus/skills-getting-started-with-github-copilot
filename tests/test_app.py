import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    # Arrange
    # (No setup needed)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_remove_participant():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # Act: Signup
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert: Signup
    assert signup_resp.status_code == 200
    assert f"Signed up {email}" in signup_resp.json()["message"]

    # Act: Get activities after signup
    activities_after_signup = client.get("/activities").json()

    # Assert: Participant added
    assert email in activities_after_signup[activity]["participants"]

    # Act: Remove participant
    remove_resp = client.post(f"/activities/{activity}/remove?email={email}")

    # Assert: Remove
    assert remove_resp.status_code == 200
    assert f"Removed {email}" in remove_resp.json()["message"]

    # Act: Get activities after removal
    activities_after_remove = client.get("/activities").json()

    # Assert: Participant removed
    assert email not in activities_after_remove[activity]["participants"]


def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "daniel@mergington.edu"  # ya existe

    # Act
    resp = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert resp.status_code == 400
    assert "already signed up" in resp.json()["detail"]


def test_remove_nonexistent_participant():
    # Arrange
    activity = "Chess Club"
    email = "noexiste@mergington.edu"

    # Act
    resp = client.post(f"/activities/{activity}/remove?email={email}")

    # Assert
    assert resp.status_code == 404
    assert "Participant not found" in resp.json()["detail"]
