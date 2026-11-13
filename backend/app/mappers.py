"""Translate domain objects and entities into API response schemas."""

from app.models import Activity
from app.schemas import (
    ActivityResponse,
    EvmMetricsResponse,
    ProjectEvmReportResponse,
    ProjectResponse,
)
from app.services.evm_service import ProjectReport, calculate_for_activity


def to_activity_response(activity: Activity) -> ActivityResponse:
    return ActivityResponse(
        id=activity.id,
        project_id=activity.project_id,
        name=activity.name,
        budget_at_completion=activity.budget_at_completion,
        planned_percent=activity.planned_percent,
        actual_percent=activity.actual_percent,
        actual_cost=activity.actual_cost,
        metrics=EvmMetricsResponse.model_validate(calculate_for_activity(activity)),
    )


def to_report_response(report: ProjectReport) -> ProjectEvmReportResponse:
    return ProjectEvmReportResponse(
        project=ProjectResponse.model_validate(report.project),
        consolidated=EvmMetricsResponse.model_validate(report.consolidated),
        activities=[to_activity_response(activity) for activity in report.activities],
    )
