"""Activity use cases."""

from app.constants import RESOURCE_ACTIVITY, RESOURCE_PROJECT
from app.errors import ResourceNotFoundError
from app.models import Activity
from app.repositories import ActivityRepository, ProjectRepository
from app.schemas import ActivityPayload


class ActivityService:
    def __init__(
        self, activities: ActivityRepository, projects: ProjectRepository
    ) -> None:
        self._activities = activities
        self._projects = projects

    def list_for_project(self, project_id: int) -> list[Activity]:
        self._ensure_project_exists(project_id)
        return self._activities.list_for_project(project_id)

    def get_activity(self, activity_id: int) -> Activity:
        activity = self._activities.find(activity_id)
        if activity is None:
            raise ResourceNotFoundError(RESOURCE_ACTIVITY, activity_id)
        return activity

    def create_activity(self, project_id: int, payload: ActivityPayload) -> Activity:
        self._ensure_project_exists(project_id)
        activity = Activity(project_id=project_id, **payload.model_dump())
        return self._activities.save(activity)

    def update_activity(self, activity_id: int, payload: ActivityPayload) -> Activity:
        activity = self.get_activity(activity_id)
        for field, value in payload.model_dump().items():
            setattr(activity, field, value)
        return self._activities.save(activity)

    def delete_activity(self, activity_id: int) -> None:
        self._activities.delete(self.get_activity(activity_id))

    def _ensure_project_exists(self, project_id: int) -> None:
        if self._projects.find(project_id) is None:
            raise ResourceNotFoundError(RESOURCE_PROJECT, project_id)
