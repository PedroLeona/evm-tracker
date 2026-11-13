"""Request and response schemas. They define the public API contract (OpenAPI)."""

from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, PlainSerializer

from app.constants import (
    DECIMAL_PLACES,
    DESCRIPTION_MAX_LENGTH,
    MAX_PERCENT,
    MIN_PERCENT,
    MONEY_MAX_DIGITS,
    NAME_MAX_LENGTH,
    PERCENT_MAX_DIGITS,
)
from app.domain.status import CostStatus, ScheduleStatus

JsonNumber = Annotated[
    Decimal, PlainSerializer(float, return_type=float, when_used="json")
]
OptionalJsonNumber = Annotated[
    Decimal | None,
    PlainSerializer(
        lambda value: None if value is None else float(value),
        return_type=float | None,
        when_used="json",
    ),
]


class ErrorResponse(BaseModel):
    detail: str = Field(examples=["Project 42 not found"])


class ProjectPayload(BaseModel):
    name: str = Field(min_length=1, max_length=NAME_MAX_LENGTH, examples=["ERP migration"])
    description: str | None = Field(
        default=None, max_length=DESCRIPTION_MAX_LENGTH, examples=["Move finance to the new ERP"]
    )


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None


class ActivityPayload(BaseModel):
    name: str = Field(min_length=1, max_length=NAME_MAX_LENGTH, examples=["Development"])
    budget_at_completion: Decimal = Field(
        gt=0,
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        description="BAC: total planned budget for the activity.",
        examples=[50000],
    )
    planned_percent: Decimal = Field(
        ge=MIN_PERCENT,
        le=MAX_PERCENT,
        max_digits=PERCENT_MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        description="Percentage of progress planned at the cut-off date (0-100).",
        examples=[60],
    )
    actual_percent: Decimal = Field(
        ge=MIN_PERCENT,
        le=MAX_PERCENT,
        max_digits=PERCENT_MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        description="Percentage of progress actually completed (0-100).",
        examples=[40],
    )
    actual_cost: Decimal = Field(
        ge=0,
        max_digits=MONEY_MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        description="AC: actual cost incurred to date.",
        examples=[30000],
    )


class EvmMetricsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    budget_at_completion: JsonNumber = Field(description="BAC")
    planned_value: JsonNumber = Field(description="PV = planned % x BAC")
    earned_value: JsonNumber = Field(description="EV = completed % x BAC")
    actual_cost: JsonNumber = Field(description="AC")
    cost_variance: JsonNumber = Field(description="CV = EV - AC")
    schedule_variance: JsonNumber = Field(description="SV = EV - PV")
    cost_performance_index: OptionalJsonNumber = Field(
        description="CPI = EV / AC. Null when AC is zero."
    )
    schedule_performance_index: OptionalJsonNumber = Field(
        description="SPI = EV / PV. Null when PV is zero."
    )
    estimate_at_completion: OptionalJsonNumber = Field(
        description="EAC = BAC / CPI. Null when CPI is undefined or zero."
    )
    variance_at_completion: OptionalJsonNumber = Field(
        description="VAC = BAC - EAC. Null when EAC is null."
    )
    cost_status: CostStatus
    schedule_status: ScheduleStatus
    cost_interpretation: str
    schedule_interpretation: str


class ActivityResponse(BaseModel):
    id: int
    project_id: int
    name: str
    budget_at_completion: JsonNumber
    planned_percent: JsonNumber
    actual_percent: JsonNumber
    actual_cost: JsonNumber
    metrics: EvmMetricsResponse


class ProjectEvmReportResponse(BaseModel):
    project: ProjectResponse
    consolidated: EvmMetricsResponse
    activities: list[ActivityResponse]
