"""FastAPI dependency providers that wire services to a request-scoped session."""

from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_session
from app.domain.tolerance import TolerancePolicy
from app.repositories import ActivityRepository, ProjectRepository
from app.services.activity_service import ActivityService
from app.services.project_service import ProjectService


@lru_cache
def get_tolerance_policy() -> TolerancePolicy:
    """The tolerance policy configured for this deployment (read once, then cached)."""
    return settings.tolerance_policy


def get_project_service(session: Session = Depends(get_session)) -> ProjectService:
    return ProjectService(ProjectRepository(session))


def get_activity_service(session: Session = Depends(get_session)) -> ActivityService:
    return ActivityService(ActivityRepository(session), ProjectRepository(session))
