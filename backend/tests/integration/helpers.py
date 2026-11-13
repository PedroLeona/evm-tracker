"""Shared helpers and contract assertions for the integration tests."""

from fastapi.testclient import TestClient

METRIC_KEYS = {
    "budget_at_completion",
    "planned_value",
    "earned_value",
    "actual_cost",
    "cost_variance",
    "schedule_variance",
    "cost_performance_index",
    "schedule_performance_index",
    "estimate_at_completion",
    "variance_at_completion",
    "cost_status",
    "schedule_status",
    "cost_interpretation",
    "schedule_interpretation",
}
ACTIVITY_KEYS = {
    "id",
    "project_id",
    "name",
    "budget_at_completion",
    "planned_percent",
    "actual_percent",
    "actual_cost",
    "metrics",
}
PROJECT_KEYS = {"id", "name", "description"}

DEMO_ACTIVITIES = [
    ("Design", 20000, 100, 100, 18000),
    ("Development", 50000, 60, 40, 30000),
    ("Testing", 10000, 20, 25, 2000),
]


def activity_body(**overrides) -> dict:
    body = {
        "name": "Development",
        "budget_at_completion": 1000,
        "planned_percent": 50,
        "actual_percent": 40,
        "actual_cost": 600,
    }
    return {**body, **overrides}


def create_project(client: TestClient, name: str = "ERP migration") -> dict:
    response = client.post("/api/projects", json={"name": name, "description": "Demo"})
    assert response.status_code == 201
    return response.json()


def create_activity(client: TestClient, project_id: int, **overrides) -> dict:
    response = client.post(
        f"/api/projects/{project_id}/activities", json=activity_body(**overrides)
    )
    assert response.status_code == 201
    return response.json()


def create_demo_project(client: TestClient) -> dict:
    project = create_project(client)
    for name, budget, planned, actual, cost in DEMO_ACTIVITIES:
        create_activity(
            client,
            project["id"],
            name=name,
            budget_at_completion=budget,
            planned_percent=planned,
            actual_percent=actual,
            actual_cost=cost,
        )
    return project


def assert_metrics_contract(metrics: dict) -> None:
    assert set(metrics) == METRIC_KEYS
    assert isinstance(metrics["planned_value"], float)
    assert isinstance(metrics["cost_status"], str)
    assert isinstance(metrics["cost_interpretation"], str)
