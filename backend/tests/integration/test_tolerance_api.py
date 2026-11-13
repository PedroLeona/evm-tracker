import pytest

from app.dependencies import get_tolerance_policy
from app.domain.tolerance import TolerancePolicy
from tests.integration.helpers import create_activity, create_project


@pytest.fixture
def strict_policy():
    return TolerancePolicy.from_pairs([(0, 0)])


def test_activity_inside_the_default_tolerance_is_reported_on_budget(client):
    project = create_project(client)

    # CPI 0.9804: inside the 5% band that applies to small budgets.
    activity = create_activity(
        client, project["id"], actual_cost=510, planned_percent=50, actual_percent=50
    )

    metrics = activity["metrics"]
    assert metrics["cost_performance_index"] == pytest.approx(0.9804)
    assert metrics["tolerance_percent"] == 5.0
    assert metrics["cost_status"] == "ON_BUDGET"
    assert metrics["schedule_status"] == "ON_SCHEDULE"


def test_overriding_the_policy_changes_the_status_without_changing_the_numbers(
    client, strict_policy
):
    project = create_project(client)
    create_activity(client, project["id"], actual_cost=510, planned_percent=50, actual_percent=50)
    default_report = client.get(f"/api/projects/{project['id']}/evm").json()["consolidated"]

    client.app.dependency_overrides[get_tolerance_policy] = lambda: strict_policy
    strict_report = client.get(f"/api/projects/{project['id']}/evm").json()["consolidated"]

    assert default_report["cost_status"] == "ON_BUDGET"
    assert strict_report["cost_status"] == "OVER_BUDGET"
    assert strict_report["tolerance_percent"] == 0.0
    assert strict_report["cost_performance_index"] == default_report["cost_performance_index"]


def test_report_exposes_the_tolerance_of_the_consolidated_budget(client):
    project = create_project(client)
    create_activity(client, project["id"], budget_at_completion=30_000_000)
    create_activity(client, project["id"], budget_at_completion=30_000_000)

    body = client.get(f"/api/projects/{project['id']}/evm").json()

    assert [a["metrics"]["tolerance_percent"] for a in body["activities"]] == [5.0, 5.0]
    assert body["consolidated"]["tolerance_percent"] == 3.0
