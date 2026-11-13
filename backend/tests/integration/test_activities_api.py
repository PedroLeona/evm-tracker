import pytest

from tests.integration.helpers import (
    ACTIVITY_KEYS,
    activity_body,
    assert_metrics_contract,
    create_activity,
    create_project,
)

MISSING_ID = 999


def test_create_activity_returns_201_with_calculated_metrics(client):
    project = create_project(client)

    response = client.post(f"/api/projects/{project['id']}/activities", json=activity_body())

    assert response.status_code == 201
    body = response.json()
    assert set(body) == ACTIVITY_KEYS
    assert body["project_id"] == project["id"]
    assert_metrics_contract(body["metrics"])
    assert body["metrics"]["planned_value"] == 500.0
    assert body["metrics"]["earned_value"] == 400.0
    assert body["metrics"]["cost_performance_index"] == pytest.approx(0.6667)
    assert body["metrics"]["cost_status"] == "OVER_BUDGET"
    assert body["metrics"]["schedule_status"] == "BEHIND"


def test_create_activity_in_unknown_project_returns_404(client):
    response = client.post(f"/api/projects/{MISSING_ID}/activities", json=activity_body())

    assert response.status_code == 404
    assert response.json() == {"detail": f"Project {MISSING_ID} not found"}


@pytest.mark.parametrize(
    "invalid_field",
    [
        {"name": ""},
        {"budget_at_completion": 0},
        {"budget_at_completion": -10},
        {"planned_percent": 101},
        {"planned_percent": -1},
        {"actual_percent": 100.01},
        {"actual_cost": -0.01},
        {"actual_cost": "not a number"},
    ],
)
def test_create_activity_with_invalid_data_returns_422(client, invalid_field):
    project = create_project(client)

    response = client.post(
        f"/api/projects/{project['id']}/activities", json=activity_body(**invalid_field)
    )

    assert response.status_code == 422


def test_create_activity_with_missing_fields_returns_422(client):
    project = create_project(client)

    response = client.post(f"/api/projects/{project['id']}/activities", json={"name": "Only name"})

    assert response.status_code == 422


def test_list_activities_returns_each_one_with_metrics(client):
    project = create_project(client)
    create_activity(client, project["id"], name="One")
    create_activity(client, project["id"], name="Two")

    response = client.get(f"/api/projects/{project['id']}/activities")

    assert response.status_code == 200
    body = response.json()
    assert [activity["name"] for activity in body] == ["One", "Two"]
    for activity in body:
        assert set(activity) == ACTIVITY_KEYS
        assert_metrics_contract(activity["metrics"])


def test_list_activities_of_unknown_project_returns_404(client):
    response = client.get(f"/api/projects/{MISSING_ID}/activities")

    assert response.status_code == 404


def test_get_activity_returns_the_activity_with_metrics(client):
    project = create_project(client)
    activity = create_activity(client, project["id"])

    response = client.get(f"/api/activities/{activity['id']}")

    assert response.status_code == 200
    assert response.json() == activity


def test_get_unknown_activity_returns_404_with_error_contract(client):
    response = client.get(f"/api/activities/{MISSING_ID}")

    assert response.status_code == 404
    assert response.json() == {"detail": f"Activity {MISSING_ID} not found"}


def test_update_activity_recalculates_the_metrics(client):
    project = create_project(client)
    activity = create_activity(client, project["id"])

    response = client.put(
        f"/api/activities/{activity['id']}",
        json=activity_body(planned_percent=40, actual_percent=50, actual_cost=400),
    )

    assert response.status_code == 200
    metrics = response.json()["metrics"]
    assert metrics["cost_performance_index"] == 1.25
    assert metrics["schedule_performance_index"] == 1.25
    assert metrics["estimate_at_completion"] == 800.0
    assert metrics["variance_at_completion"] == 200.0
    assert metrics["cost_status"] == "UNDER_BUDGET"
    assert metrics["schedule_status"] == "AHEAD"


def test_update_activity_with_invalid_data_returns_422(client):
    project = create_project(client)
    activity = create_activity(client, project["id"])

    response = client.put(
        f"/api/activities/{activity['id']}", json=activity_body(actual_percent=150)
    )

    assert response.status_code == 422


def test_update_unknown_activity_returns_404(client):
    response = client.put(f"/api/activities/{MISSING_ID}", json=activity_body())

    assert response.status_code == 404


def test_delete_activity_returns_204_and_removes_it(client):
    project = create_project(client)
    activity = create_activity(client, project["id"])

    delete_response = client.delete(f"/api/activities/{activity['id']}")
    get_response = client.get(f"/api/activities/{activity['id']}")

    assert delete_response.status_code == 204
    assert get_response.status_code == 404


def test_delete_unknown_activity_returns_404(client):
    response = client.delete(f"/api/activities/{MISSING_ID}")

    assert response.status_code == 404


def test_activity_with_zero_cost_returns_null_cost_indicators(client):
    project = create_project(client)

    activity = create_activity(client, project["id"], actual_cost=0)

    metrics = activity["metrics"]
    assert metrics["cost_performance_index"] is None
    assert metrics["estimate_at_completion"] is None
    assert metrics["variance_at_completion"] is None
    assert metrics["cost_status"] == "UNDEFINED"
