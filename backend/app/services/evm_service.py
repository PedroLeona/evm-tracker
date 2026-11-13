"""Bridges persisted entities and the pure EVM domain calculations."""

from collections.abc import Sequence
from dataclasses import dataclass

from app.domain.evm import (
    EvmInputs,
    EvmMetrics,
    calculate_activity_metrics,
    calculate_project_metrics,
)
from app.models import Activity, Project


@dataclass(frozen=True)
class ProjectReport:
    project: Project
    consolidated: EvmMetrics
    activities: Sequence[Activity]


def to_evm_inputs(activity: Activity) -> EvmInputs:
    return EvmInputs(
        budget_at_completion=activity.budget_at_completion,
        planned_percent=activity.planned_percent,
        actual_percent=activity.actual_percent,
        actual_cost=activity.actual_cost,
    )


def calculate_for_activity(activity: Activity) -> EvmMetrics:
    return calculate_activity_metrics(to_evm_inputs(activity))


def build_project_report(project: Project) -> ProjectReport:
    consolidated = calculate_project_metrics(
        to_evm_inputs(activity) for activity in project.activities
    )
    return ProjectReport(
        project=project, consolidated=consolidated, activities=project.activities
    )
