from decimal import Decimal

import pytest

from app.errors import ResourceNotFoundError
from app.repositories import ActivityRepository, ProjectRepository
from app.schemas import ActivityPayload, ProjectPayload
from app.services.activity_service import ActivityService
from app.services.project_service import ProjectService

MISSING_ID = 999


@pytest.fixture
def project_service(session):
    return ProjectService(ProjectRepository(session))


@pytest.fixture
def activity_service(session):
    return ActivityService(ActivityRepository(session), ProjectRepository(session))


def make_activity_payload(**overrides) -> ActivityPayload:
    values = {
        "name": "Development",
        "budget_at_completion": Decimal("1000"),
        "planned_percent": Decimal("50"),
        "actual_percent": Decimal("40"),
        "actual_cost": Decimal("600"),
    }
    return ActivityPayload(**{**values, **overrides})


class TestProjectService:
    def test_get_missing_project_raises_not_found(self, project_service):
        with pytest.raises(ResourceNotFoundError):
            project_service.get_project(MISSING_ID)

    def test_update_missing_project_raises_not_found(self, project_service):
        with pytest.raises(ResourceNotFoundError):
            project_service.update_project(MISSING_ID, ProjectPayload(name="x"))

    def test_report_for_project_without_activities_has_undefined_indices(self, project_service):
        project = project_service.create_project(ProjectPayload(name="Empty"))

        report = project_service.build_report(project.id)

        assert report.activities == []
        assert report.consolidated.cost_performance_index is None

    def test_deleting_a_project_removes_its_activities(
        self, project_service, activity_service
    ):
        project = project_service.create_project(ProjectPayload(name="Doomed"))
        activity = activity_service.create_activity(project.id, make_activity_payload())

        project_service.delete_project(project.id)

        with pytest.raises(ResourceNotFoundError):
            activity_service.get_activity(activity.id)


class TestActivityService:
    def test_create_activity_in_missing_project_raises_not_found(self, activity_service):
        with pytest.raises(ResourceNotFoundError):
            activity_service.create_activity(MISSING_ID, make_activity_payload())

    def test_list_for_missing_project_raises_not_found(self, activity_service):
        with pytest.raises(ResourceNotFoundError):
            activity_service.list_for_project(MISSING_ID)

    def test_update_replaces_every_field(self, project_service, activity_service):
        project = project_service.create_project(ProjectPayload(name="P"))
        activity = activity_service.create_activity(project.id, make_activity_payload())

        updated = activity_service.update_activity(
            activity.id,
            make_activity_payload(name="Renamed", actual_percent=Decimal("75")),
        )

        assert updated.name == "Renamed"
        assert updated.actual_percent == Decimal("75")

    def test_delete_missing_activity_raises_not_found(self, activity_service):
        with pytest.raises(ResourceNotFoundError):
            activity_service.delete_activity(MISSING_ID)
