from decimal import Decimal

import pytest

from app.domain.evm import (
    EvmInputs,
    calculate_activity_metrics,
    calculate_project_metrics,
)
from app.domain.interpretation import COST_MESSAGES, SCHEDULE_MESSAGES
from app.domain.status import (
    CostStatus,
    ScheduleStatus,
    classify_cost,
    classify_schedule,
)


def make_inputs(
    budget: str = "1000", planned: str = "50", actual: str = "40", cost: str = "600"
) -> EvmInputs:
    return EvmInputs(
        budget_at_completion=Decimal(budget),
        planned_percent=Decimal(planned),
        actual_percent=Decimal(actual),
        actual_cost=Decimal(cost),
    )


DESIGN = make_inputs("20000", "100", "100", "18000")
DEVELOPMENT = make_inputs("50000", "60", "40", "30000")
TESTING = make_inputs("10000", "20", "25", "2000")


class TestActivityMetrics:
    def test_spent_60_percent_of_budget_for_40_percent_of_work(self):
        # Hand calculation: PV=500, EV=400, AC=600.
        metrics = calculate_activity_metrics(make_inputs())

        assert metrics.planned_value == Decimal("500.00")
        assert metrics.earned_value == Decimal("400.00")
        assert metrics.cost_variance == Decimal("-200.00")
        assert metrics.schedule_variance == Decimal("-100.00")
        assert metrics.cost_performance_index == Decimal("0.6667")
        assert metrics.schedule_performance_index == Decimal("0.8000")
        assert metrics.estimate_at_completion == Decimal("1500.00")
        assert metrics.variance_at_completion == Decimal("-500.00")
        assert metrics.cost_status is CostStatus.OVER_BUDGET
        assert metrics.schedule_status is ScheduleStatus.BEHIND

    def test_under_budget_and_ahead_of_schedule(self):
        # PV=400, EV=500, AC=400 -> CPI=1.25, SPI=1.25, EAC=800, VAC=+200.
        metrics = calculate_activity_metrics(make_inputs(planned="40", actual="50", cost="400"))

        assert metrics.cost_variance == Decimal("100.00")
        assert metrics.schedule_variance == Decimal("100.00")
        assert metrics.cost_performance_index == Decimal("1.2500")
        assert metrics.schedule_performance_index == Decimal("1.2500")
        assert metrics.estimate_at_completion == Decimal("800.00")
        assert metrics.variance_at_completion == Decimal("200.00")
        assert metrics.cost_status is CostStatus.UNDER_BUDGET
        assert metrics.schedule_status is ScheduleStatus.AHEAD

    def test_exactly_on_budget_and_on_schedule(self):
        metrics = calculate_activity_metrics(make_inputs(planned="50", actual="50", cost="500"))

        assert metrics.cost_performance_index == Decimal("1.0000")
        assert metrics.schedule_performance_index == Decimal("1.0000")
        assert metrics.variance_at_completion == Decimal("0.00")
        assert metrics.cost_status is CostStatus.ON_BUDGET
        assert metrics.schedule_status is ScheduleStatus.ON_SCHEDULE

    def test_completed_activity_has_eac_equal_to_actual_cost(self):
        metrics = calculate_activity_metrics(DESIGN)

        assert metrics.earned_value == Decimal("20000.00")
        assert metrics.cost_performance_index == Decimal("1.1111")
        assert metrics.estimate_at_completion == Decimal("18000.00")
        assert metrics.variance_at_completion == Decimal("2000.00")


class TestEdgeCases:
    def test_zero_actual_cost_leaves_cost_indicators_undefined(self):
        metrics = calculate_activity_metrics(make_inputs(cost="0"))

        assert metrics.cost_performance_index is None
        assert metrics.estimate_at_completion is None
        assert metrics.variance_at_completion is None
        assert metrics.cost_status is CostStatus.UNDEFINED
        assert metrics.cost_variance == Decimal("400.00")
        assert metrics.schedule_performance_index == Decimal("0.8000")

    def test_zero_actual_progress_with_cost_means_nothing_earned(self):
        metrics = calculate_activity_metrics(make_inputs(actual="0", cost="300"))

        assert metrics.earned_value == Decimal("0.00")
        assert metrics.cost_performance_index == Decimal("0.0000")
        assert metrics.schedule_performance_index == Decimal("0.0000")
        assert metrics.cost_status is CostStatus.OVER_BUDGET
        assert metrics.schedule_status is ScheduleStatus.BEHIND

    def test_zero_cpi_makes_estimate_at_completion_undefined_instead_of_failing(self):
        metrics = calculate_activity_metrics(make_inputs(actual="0", cost="300"))

        assert metrics.estimate_at_completion is None
        assert metrics.variance_at_completion is None

    def test_zero_planned_progress_leaves_schedule_index_undefined(self):
        metrics = calculate_activity_metrics(make_inputs(planned="0"))

        assert metrics.planned_value == Decimal("0.00")
        assert metrics.schedule_performance_index is None
        assert metrics.schedule_status is ScheduleStatus.UNDEFINED
        assert metrics.cost_performance_index == Decimal("0.6667")

    def test_nothing_planned_done_or_spent_is_fully_undefined(self):
        metrics = calculate_activity_metrics(make_inputs(planned="0", actual="0", cost="0"))

        assert metrics.cost_performance_index is None
        assert metrics.schedule_performance_index is None
        assert metrics.cost_status is CostStatus.UNDEFINED
        assert metrics.schedule_status is ScheduleStatus.UNDEFINED

    def test_indices_are_rounded_half_up_to_four_decimals(self):
        # EV=2, PV=3 -> 0.66666... rounds to 0.6667; EV=2, AC=16 -> 0.125 stays exact.
        metrics = calculate_activity_metrics(make_inputs("100", "3", "2", "16"))

        assert metrics.schedule_performance_index == Decimal("0.6667")
        assert metrics.cost_performance_index == Decimal("0.1250")


class TestProjectConsolidation:
    def test_project_without_activities_is_all_zero_and_undefined(self):
        metrics = calculate_project_metrics([])

        assert metrics.budget_at_completion == Decimal("0.00")
        assert metrics.planned_value == Decimal("0.00")
        assert metrics.earned_value == Decimal("0.00")
        assert metrics.actual_cost == Decimal("0.00")
        assert metrics.cost_performance_index is None
        assert metrics.schedule_performance_index is None
        assert metrics.estimate_at_completion is None
        assert metrics.cost_status is CostStatus.UNDEFINED
        assert metrics.schedule_status is ScheduleStatus.UNDEFINED

    def test_consolidated_totals_are_sums_of_the_activities(self):
        # Hand calculation: BAC=80000, PV=52000, EV=42500, AC=50000.
        metrics = calculate_project_metrics([DESIGN, DEVELOPMENT, TESTING])

        assert metrics.budget_at_completion == Decimal("80000.00")
        assert metrics.planned_value == Decimal("52000.00")
        assert metrics.earned_value == Decimal("42500.00")
        assert metrics.actual_cost == Decimal("50000.00")
        assert metrics.cost_variance == Decimal("-7500.00")
        assert metrics.schedule_variance == Decimal("-9500.00")

    def test_consolidated_indices_come_from_totals_not_from_averaging_indices(self):
        metrics = calculate_project_metrics([DESIGN, DEVELOPMENT, TESTING])

        assert metrics.cost_performance_index == Decimal("0.8500")
        assert metrics.schedule_performance_index == Decimal("0.8173")
        assert metrics.estimate_at_completion == Decimal("94117.65")
        assert metrics.variance_at_completion == Decimal("-14117.65")

        per_activity = [
            calculate_activity_metrics(item).cost_performance_index
            for item in (DESIGN, DEVELOPMENT, TESTING)
        ]
        naive_average = sum(per_activity) / len(per_activity)
        assert metrics.cost_performance_index != naive_average.quantize(Decimal("0.0001"))

    def test_single_activity_project_matches_the_activity(self):
        activity_metrics = calculate_activity_metrics(DEVELOPMENT)
        project_metrics = calculate_project_metrics([DEVELOPMENT])

        assert project_metrics == activity_metrics

    def test_a_good_activity_cannot_hide_a_bad_one_in_the_consolidated_status(self):
        metrics = calculate_project_metrics([DESIGN, DEVELOPMENT])

        assert metrics.cost_status is CostStatus.OVER_BUDGET
        assert metrics.schedule_status is ScheduleStatus.BEHIND

    def test_consolidation_uses_unrounded_values(self):
        thirds = make_inputs("100", "33.33", "33.33", "33.33")
        metrics = calculate_project_metrics([thirds, thirds, thirds])

        assert metrics.planned_value == Decimal("99.99")
        assert metrics.cost_performance_index == Decimal("1.0000")


class TestClassification:
    @pytest.mark.parametrize(
        ("index", "expected"),
        [
            (Decimal("1.0001"), CostStatus.UNDER_BUDGET),
            (Decimal("1"), CostStatus.ON_BUDGET),
            (Decimal("0.9999"), CostStatus.OVER_BUDGET),
            (Decimal("0"), CostStatus.OVER_BUDGET),
            (None, CostStatus.UNDEFINED),
        ],
    )
    def test_cost_status_from_cpi(self, index, expected):
        assert classify_cost(index) is expected

    @pytest.mark.parametrize(
        ("index", "expected"),
        [
            (Decimal("1.0001"), ScheduleStatus.AHEAD),
            (Decimal("1"), ScheduleStatus.ON_SCHEDULE),
            (Decimal("0.9999"), ScheduleStatus.BEHIND),
            (Decimal("0"), ScheduleStatus.BEHIND),
            (None, ScheduleStatus.UNDEFINED),
        ],
    )
    def test_schedule_status_from_spi(self, index, expected):
        assert classify_schedule(index) is expected

    def test_every_status_has_an_interpretation_message(self):
        assert set(COST_MESSAGES) == set(CostStatus)
        assert set(SCHEDULE_MESSAGES) == set(ScheduleStatus)

    def test_metrics_expose_the_interpretation_of_their_statuses(self):
        metrics = calculate_activity_metrics(make_inputs())

        assert metrics.cost_interpretation == COST_MESSAGES[CostStatus.OVER_BUDGET]
        assert metrics.schedule_interpretation == SCHEDULE_MESSAGES[ScheduleStatus.BEHIND]
