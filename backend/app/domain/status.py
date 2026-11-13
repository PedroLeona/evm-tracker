"""Cost and schedule status derived from CPI and SPI."""

from decimal import Decimal
from enum import StrEnum

from app.constants import NEUTRAL_INDEX


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


def classify_cost(cost_performance_index: Decimal | None) -> CostStatus:
    if cost_performance_index is None:
        return CostStatus.UNDEFINED
    if cost_performance_index > NEUTRAL_INDEX:
        return CostStatus.UNDER_BUDGET
    if cost_performance_index < NEUTRAL_INDEX:
        return CostStatus.OVER_BUDGET
    return CostStatus.ON_BUDGET


def classify_schedule(schedule_performance_index: Decimal | None) -> ScheduleStatus:
    if schedule_performance_index is None:
        return ScheduleStatus.UNDEFINED
    if schedule_performance_index > NEUTRAL_INDEX:
        return ScheduleStatus.AHEAD
    if schedule_performance_index < NEUTRAL_INDEX:
        return ScheduleStatus.BEHIND
    return ScheduleStatus.ON_SCHEDULE
