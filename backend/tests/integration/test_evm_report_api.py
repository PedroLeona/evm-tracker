import pytest

from tests.integration.helpers import (
    ACTIVITY_KEYS,
    PROJECT_KEYS,
    assert_metrics_contract,
    create_demo_project,
    create_project,
)

MISSING_ID = 999


def test_report_contract_contains_project_consolidated_and_activities(client):
    project = create_demo_project(client)

    response = client.get(f"/api/projects/{project['id']}/evm")

    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"project", "consolidated", "activities"}
    assert set(body["project"]) == PROJECT_KEYS
    assert_metrics_contract(body["consolidated"])
    assert len(body["activities"]) == 3
    for activity in body["activities"]:
        assert set(activity) == ACTIVITY_KEYS
        assert_metrics_contract(activity["metrics"])


def test_consolidated_numbers_match_the_hand_calculation(client):
    # BAC 80000 | PV 52000 | EV 42500 | AC 50000 (worked out by hand, see db/02_seed.sql).
    project = create_demo_project(client)

    consolidated = client.get(f"/api/projects/{project['id']}/evm").json()["consolidated"]

    assert consolidated["budget_at_completion"] == 80000.0
    assert consolidated["planned_value"] == 52000.0
    assert consolidated["earned_value"] == 42500.0
    assert consolidated["actual_cost"] == 50000.0
    assert consolidated["cost_variance"] == -7500.0
    assert consolidated["schedule_variance"] == -9500.0
    assert consolidated["cost_performance_index"] == 0.85
    assert consolidated["schedule_performance_index"] == pytest.approx(0.8173)
    assert consolidated["estimate_at_completion"] == pytest.approx(94117.65)
    assert consolidated["variance_at_completion"] == pytest.approx(-14117.65)


def test_report_interprets_cpi_and_spi(client):
    project = create_demo_project(client)

    consolidated = client.get(f"/api/projects/{project['id']}/evm").json()["consolidated"]

    assert consolidated["cost_status"] == "OVER_BUDGET"
    assert consolidated["schedule_status"] == "BEHIND"
    assert "Sobre presupuesto" in consolidated["cost_interpretation"]
    assert "Atrasado" in consolidated["schedule_interpretation"]


def test_report_for_project_without_activities_is_zero_with_undefined_indices(client):
    project = create_project(client)

    body = client.get(f"/api/projects/{project['id']}/evm").json()

    assert body["activities"] == []
    assert body["consolidated"]["budget_at_completion"] == 0.0
    assert body["consolidated"]["cost_performance_index"] is None
    assert body["consolidated"]["schedule_performance_index"] is None
    assert body["consolidated"]["cost_status"] == "UNDEFINED"


def test_report_reflects_changes_immediately(client):
    project = create_demo_project(client)
    activity_id = client.get(f"/api/projects/{project['id']}/activities").json()[1]["id"]

    client.delete(f"/api/activities/{activity_id}")
    consolidated = client.get(f"/api/projects/{project['id']}/evm").json()["consolidated"]

    assert consolidated["budget_at_completion"] == 30000.0
    assert consolidated["cost_status"] == "UNDER_BUDGET"


def test_report_for_unknown_project_returns_404(client):
    response = client.get(f"/api/projects/{MISSING_ID}/evm")

    assert response.status_code == 404
    assert response.json() == {"detail": f"Project {MISSING_ID} not found"}
