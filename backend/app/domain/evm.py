"""Pure Earned Value Management calculations.

No framework or I/O dependencies: everything here is deterministic and unit-testable.

Conventions
-----------
* Percentages are expressed on a 0-100 scale.
* An index whose denominator is zero is *undefined* and reported as ``None``
  (never 0, never infinity), so callers cannot mistake "no data" for "bad".
* Project-level figures are computed from the summed PV, EV, AC and BAC of the
  activities, never by averaging per-activity indices.
* Rounding happens only when building the final result, so consolidation does
  not accumulate rounding error.
"""

from collections.abc import Iterable
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

from app.constants import INDEX_PRECISION, MONEY_PRECISION, PERCENT_BASE
from app.domain.interpretation import COST_MESSAGES, SCHEDULE_MESSAGES
from app.domain.status import (
    CostStatus,
    ScheduleStatus,
    classify_cost,
    classify_schedule,
)
from app.domain.tolerance import DEFAULT_TOLERANCE_POLICY, TolerancePolicy


@dataclass(frozen=True)
class EvmInputs:
    budget_at_completion: Decimal
    planned_percent: Decimal
    actual_percent: Decimal
    actual_cost: Decimal


@dataclass(frozen=True)
class EvmMetrics:
    budget_at_completion: Decimal
    planned_value: Decimal
    earned_value: Decimal
    actual_cost: Decimal
    cost_variance: Decimal
    schedule_variance: Decimal
    cost_performance_index: Decimal | None
    schedule_performance_index: Decimal | None
    estimate_at_completion: Decimal | None
    variance_at_completion: Decimal | None
    cost_status: CostStatus
    schedule_status: ScheduleStatus
    tolerance: Decimal

    @property
    def tolerance_percent(self) -> Decimal:
        return self.tolerance * PERCENT_BASE

    @property
    def cost_interpretation(self) -> str:
        return COST_MESSAGES[self.cost_status]

    @property
    def schedule_interpretation(self) -> str:
        return SCHEDULE_MESSAGES[self.schedule_status]


@dataclass(frozen=True)
class _Totals:
    budget_at_completion: Decimal
    planned_value: Decimal
    earned_value: Decimal
    actual_cost: Decimal

    @classmethod
    def zero(cls) -> "_Totals":
        empty = Decimal(0)
        return cls(empty, empty, empty, empty)

    def __add__(self, other: "_Totals") -> "_Totals":
        return _Totals(
            self.budget_at_completion + other.budget_at_completion,
            self.planned_value + other.planned_value,
            self.earned_value + other.earned_value,
            self.actual_cost + other.actual_cost,
        )


def calculate_activity_metrics(
    inputs: EvmInputs, policy: TolerancePolicy = DEFAULT_TOLERANCE_POLICY
) -> EvmMetrics:
    return _build_metrics(_to_totals(inputs), policy)


def calculate_project_metrics(
    activities: Iterable[EvmInputs], policy: TolerancePolicy = DEFAULT_TOLERANCE_POLICY
) -> EvmMetrics:
    totals = sum((_to_totals(item) for item in activities), start=_Totals.zero())
    return _build_metrics(totals, policy)


def _to_totals(inputs: EvmInputs) -> _Totals:
    return _Totals(
        budget_at_completion=inputs.budget_at_completion,
        planned_value=_percent_of(inputs.planned_percent, inputs.budget_at_completion),
        earned_value=_percent_of(inputs.actual_percent, inputs.budget_at_completion),
        actual_cost=inputs.actual_cost,
    )


def _percent_of(percent: Decimal, amount: Decimal) -> Decimal:
    return percent / PERCENT_BASE * amount


def _build_metrics(totals: _Totals, policy: TolerancePolicy) -> EvmMetrics:
    tolerance = policy.tolerance_for(totals.budget_at_completion)
    cost_index = _safe_divide(totals.earned_value, totals.actual_cost)
    schedule_index = _safe_divide(totals.earned_value, totals.planned_value)
    estimate_at_completion = _safe_divide(totals.budget_at_completion, cost_index)
    variance_at_completion = _subtract_if_defined(
        totals.budget_at_completion, estimate_at_completion
    )

    return EvmMetrics(
        budget_at_completion=_round_money(totals.budget_at_completion),
        planned_value=_round_money(totals.planned_value),
        earned_value=_round_money(totals.earned_value),
        actual_cost=_round_money(totals.actual_cost),
        cost_variance=_round_money(totals.earned_value - totals.actual_cost),
        schedule_variance=_round_money(totals.earned_value - totals.planned_value),
        cost_performance_index=_round_index(cost_index),
        schedule_performance_index=_round_index(schedule_index),
        estimate_at_completion=_round_optional_money(estimate_at_completion),
        variance_at_completion=_round_optional_money(variance_at_completion),
        cost_status=classify_cost(cost_index, tolerance),
        schedule_status=classify_schedule(schedule_index, tolerance),
        tolerance=tolerance,
    )


def _safe_divide(numerator: Decimal, denominator: Decimal | None) -> Decimal | None:
    if not denominator:
        return None
    return numerator / denominator


def _subtract_if_defined(minuend: Decimal, subtrahend: Decimal | None) -> Decimal | None:
    if subtrahend is None:
        return None
    return minuend - subtrahend


def _round_money(value: Decimal) -> Decimal:
    return value.quantize(MONEY_PRECISION, rounding=ROUND_HALF_UP)


def _round_optional_money(value: Decimal | None) -> Decimal | None:
    return None if value is None else _round_money(value)


def _round_index(value: Decimal | None) -> Decimal | None:
    return None if value is None else value.quantize(INDEX_PRECISION, rounding=ROUND_HALF_UP)
