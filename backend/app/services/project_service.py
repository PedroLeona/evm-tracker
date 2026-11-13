"""Project use cases."""

from app.constants import RESOURCE_PROJECT
from app.errors import ResourceNotFoundError
from app.models import Project
from app.repositories import ProjectRepository
from app.schemas import ProjectPayload
from app.services.evm_service import ProjectReport, build_project_report


class ProjectService:
    def __init__(self, projects: ProjectRepository) -> None:
        self._projects = projects

    def list_projects(self) -> list[Project]:
        return self._projects.list_all()

    def get_project(self, project_id: int) -> Project:
        project = self._projects.find(project_id)
        if project is None:
            raise ResourceNotFoundError(RESOURCE_PROJECT, project_id)
        return project

    def create_project(self, payload: ProjectPayload) -> Project:
        return self._projects.save(Project(**payload.model_dump()))

    def update_project(self, project_id: int, payload: ProjectPayload) -> Project:
        project = self.get_project(project_id)
        project.name = payload.name
        project.description = payload.description
        return self._projects.save(project)

    def delete_project(self, project_id: int) -> None:
        self._projects.delete(self.get_project(project_id))

    def build_report(self, project_id: int) -> ProjectReport:
        return build_project_report(self.get_project(project_id))
