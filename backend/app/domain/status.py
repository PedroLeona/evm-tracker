"""Cost and schedule status derived from CPI and SPI."""

from decimal import Decimal
from enum import StrEnum

from app.constants import NEUTRAL_INDEX, NO_TOLERANCE


class CostStatus(StrEnum):
    UNDER_BUDGET = "UNDER_BUDGET"
    ON_BUDGET = "ON_BUDGET"
    OVER_BUDGET = "OVER_BUDGET"
    UNDEFINED = "UNDEFINED"


class ScheduleStatus(StrEnum):
    AHEAD = "AHEAD"
    ON_SCHEDULE = "ON_SCHEDULE"
    BEHIND = "BEHIND"
    UNDEFINED = "UNDEFINED"


def classify_cost(
    cost_performance_index: Decimal | None, tolerance: Decimal = NO_TOLERANCE
) -> CostStatus:
    """Classify the CPI. Within ``tolerance`` of 1 (bounds included) counts as on budget."""
    if cost_performance_index is None:
        return CostStatus.UNDEFINED
    if cost_performance_index > NEUTRAL_INDEX + tolerance:
        return CostStatus.UNDER_BUDGET
    if cost_performance_index < NEUTRAL_INDEX - tolerance:
        return CostStatus.OVER_BUDGET
    return CostStatus.ON_BUDGET


def classify_schedule(
    schedule_performance_index: Decimal | None, tolerance: Decimal = NO_TOLERANCE
) -> ScheduleStatus:
    """Classify the SPI. Within ``tolerance`` of 1 (bounds included) counts as on schedule."""
    if schedule_performance_index is None:
        return ScheduleStatus.UNDEFINED
    if schedule_performance_index > NEUTRAL_INDEX + tolerance:
        return ScheduleStatus.AHEAD
    if schedule_performance_index < NEUTRAL_INDEX - tolerance:
        return ScheduleStatus.BEHIND
    return ScheduleStatus.ON_SCHEDULE
