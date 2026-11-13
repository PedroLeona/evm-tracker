"""Persistence access. No business rules live here."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Activity, Project


class ProjectRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_all(self) -> list[Project]:
        return list(self._session.scalars(select(Project).order_by(Project.id)))

    def find(self, project_id: int) -> Project | None:
        return self._session.get(Project, project_id)

    def save(self, project: Project) -> Project:
        self._session.add(project)
        self._session.commit()
        return project

    def delete(self, project: Project) -> None:
        self._session.delete(project)
        self._session.commit()


class ActivityRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_for_project(self, project_id: int) -> list[Activity]:
        statement = (
            select(Activity).where(Activity.project_id == project_id).order_by(Activity.id)
        )
        return list(self._session.scalars(statement))

    def find(self, activity_id: int) -> Activity | None:
        return self._session.get(Activity, activity_id)

    def save(self, activity: Activity) -> Activity:
        self._session.add(activity)
        self._session.commit()
        return activity

    def delete(self, activity: Activity) -> None:
        self._session.delete(activity)
        self._session.commit()
