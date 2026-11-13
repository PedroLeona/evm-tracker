from decimal import Decimal

import pytest

from app.domain.evm import (
    EvmInputs,
    calculate_activity_metrics,
    calculate_project_metrics,
)
from app.domain.status import CostStatus, ScheduleStatus, classify_cost, classify_schedule
from app.domain.tolerance import (
    DEFAULT_TOLERANCE_POLICY,
    InvalidTolerancePolicyError,
    TolerancePolicy,
    ToleranceTier,
)

SMALL_TOLERANCE = Decimal("0.05")
MEDIUM_TOLERANCE = Decimal("0.03")
LARGE_TOLERANCE = Decimal("0.01")
MEDIUM_START = Decimal("50000000")
LARGE_START = Decimal("500000000")


def make_inputs(budget: str, planned: str, actual: str, cost: str) -> EvmInputs:
    return EvmInputs(
        budget_at_completion=Decimal(budget),
        planned_percent=Decimal(planned),
        actual_percent=Decimal(actual),
        actual_cost=Decimal(cost),
    )


def pairs(*items: tuple[str, str]) -> list[tuple[Decimal, Decimal]]:
    return [(Decimal(budget), Decimal(tolerance)) for budget, tolerance in items]


class TestTierSelection:
    @pytest.mark.parametrize(
        ("budget", "expected"),
        [
            ("0", SMALL_TOLERANCE),
            ("1000", SMALL_TOLERANCE),
            ("49999999.99", SMALL_TOLERANCE),
            ("50000000", MEDIUM_TOLERANCE),
            ("499999999.99", MEDIUM_TOLERANCE),
            ("500000000", LARGE_TOLERANCE),
            ("99999999999", LARGE_TOLERANCE),
        ],
    )
    def test_default_policy_picks_the_tier_by_budget(self, budget, expected):
        assert DEFAULT_TOLERANCE_POLICY.tolerance_for(Decimal(budget)) == expected

    def test_from_pairs_sorts_unordered_tiers(self):
        policy = TolerancePolicy.from_pairs(pairs(("100", "0.02"), ("0", "0.10")))

        assert policy.tolerance_for(Decimal("99")) == Decimal("0.10")
        assert policy.tolerance_for(Decimal("100")) == Decimal("0.02")

    def test_single_tier_applies_to_every_budget(self):
        policy = TolerancePolicy.from_pairs(pairs(("0", "0.04")))

        assert policy.tolerance_for(Decimal("1")) == Decimal("0.04")
        assert policy.tolerance_for(Decimal("10000000000")) == Decimal("0.04")


class TestPolicyValidation:
    def test_requires_at_least_one_tier(self):
        with pytest.raises(InvalidTolerancePolicyError, match="At least one"):
            TolerancePolicy(())

    def test_first_tier_must_start_at_zero(self):
        with pytest.raises(InvalidTolerancePolicyError, match="start at budget 0"):
            TolerancePolicy.from_pairs(pairs(("10", "0.05")))

    def test_budgets_must_be_strictly_ascending(self):
        with pytest.raises(InvalidTolerancePolicyError, match="strictly ascending"):
            TolerancePolicy.from_pairs(pairs(("0", "0.05"), ("100", "0.03"), ("100", "0.01")))

    def test_tiers_given_unsorted_directly_are_rejected(self):
        tiers = (
            ToleranceTier(Decimal("0"), Decimal("0.05")),
            ToleranceTier(Decimal("200"), Decimal("0.03")),
            ToleranceTier(Decimal("100"), Decimal("0.01")),
        )

        with pytest.raises(InvalidTolerancePolicyError, match="strictly ascending"):
            TolerancePolicy(tiers)

    @pytest.mark.parametrize("tolerance", ["-0.01", "1", "1.5"])
    def test_tolerance_must_be_between_zero_and_one(self, tolerance):
        with pytest.raises(InvalidTolerancePolicyError, match="at least 0%"):
            TolerancePolicy.from_pairs(pairs(("0", tolerance)))

    def test_zero_tolerance_is_allowed(self):
        policy = TolerancePolicy.from_pairs(pairs(("0", "0")))

        assert policy.tolerance_for(Decimal("1")) == Decimal("0")


class TestStatusWithTolerance:
    @pytest.mark.parametrize(
        ("index", "expected"),
        [
            ("1.0501", CostStatus.UNDER_BUDGET),
            ("1.05", CostStatus.ON_BUDGET),
            ("1", CostStatus.ON_BUDGET),
            ("0.95", CostStatus.ON_BUDGET),
            ("0.9499", CostStatus.OVER_BUDGET),
        ],
    )
    def test_cost_bounds_are_inclusive(self, index, expected):
        assert classify_cost(Decimal(index), SMALL_TOLERANCE) is expected

    @pytest.mark.parametrize(
        ("index", "expected"),
        [
            ("1.0301", ScheduleStatus.AHEAD),
            ("1.03", ScheduleStatus.ON_SCHEDULE),
            ("0.97", ScheduleStatus.ON_SCHEDULE),
            ("0.9699", ScheduleStatus.BEHIND),
        ],
    )
    def test_schedule_bounds_are_inclusive(self, index, expected):
        assert classify_schedule(Decimal(index), MEDIUM_TOLERANCE) is expected

    def test_undefined_index_stays_undefined_whatever_the_tolerance(self):
        assert classify_cost(None, SMALL_TOLERANCE) is CostStatus.UNDEFINED
        assert classify_schedule(None, SMALL_TOLERANCE) is ScheduleStatus.UNDEFINED

    def test_a_cpi_that_displays_as_one_is_on_budget_with_the_default_policy(self):
        # CPI 0.99996 used to be flagged OVER_BUDGET while the screen showed 1.00.
        metrics = calculate_activity_metrics(make_inputs("100000", "50", "50", "50002"))

        assert metrics.cost_performance_index == Decimal("1.0000")
        assert metrics.cost_status is CostStatus.ON_BUDGET


class TestMetricsWithTolerance:
    def test_same_cpi_is_judged_differently_depending_on_the_budget(self):
        # CPI = 0.9804 in both. Small budget (5% band) vs large budget (1% band).
        small = calculate_activity_metrics(make_inputs("1000", "50", "50", "510"))
        large = calculate_activity_metrics(make_inputs("600000000", "50", "50", "306000000"))

        assert small.cost_performance_index == large.cost_performance_index == Decimal("0.9804")
        assert small.tolerance == SMALL_TOLERANCE
        assert small.cost_status is CostStatus.ON_BUDGET
        assert large.tolerance == LARGE_TOLERANCE
        assert large.cost_status is CostStatus.OVER_BUDGET

    def test_tolerance_percent_is_the_tolerance_expressed_in_percent(self):
        metrics = calculate_activity_metrics(make_inputs("1000", "50", "50", "500"))

        assert metrics.tolerance_percent == Decimal("5")

    def test_exact_lower_bound_is_on_budget_and_one_cent_more_is_over(self):
        on_bound = calculate_activity_metrics(make_inputs("1000", "95", "95", "1000"))
        past_bound = calculate_activity_metrics(make_inputs("1000", "95", "95", "1000.01"))

        assert on_bound.cost_performance_index == Decimal("0.9500")
        assert on_bound.cost_status is CostStatus.ON_BUDGET
        assert past_bound.cost_status is CostStatus.OVER_BUDGET

    def test_tolerance_also_applies_to_the_schedule(self):
        # SPI = 0.96: inside the 5% band of a small budget, outside the 3% band of a medium one.
        small = calculate_activity_metrics(make_inputs("1000", "50", "48", "480"))
        medium = calculate_activity_metrics(make_inputs("60000000", "50", "48", "28800000"))

        assert small.schedule_performance_index == medium.schedule_performance_index
        assert small.schedule_status is ScheduleStatus.ON_SCHEDULE
        assert medium.schedule_status is ScheduleStatus.BEHIND

    def test_custom_policy_without_tolerance_restores_the_strict_comparison(self):
        strict = TolerancePolicy.from_pairs(pairs(("0", "0")))

        metrics = calculate_activity_metrics(make_inputs("1000", "50", "50", "510"), strict)

        assert metrics.tolerance == Decimal("0")
        assert metrics.cost_status is CostStatus.OVER_BUDGET

    def test_project_uses_the_total_budget_to_choose_the_tier(self):
        # Each activity (30M) sits in the 5% tier, but together (60M) they reach the 3% tier.
        activity = make_inputs("30000000", "50", "50", "15625000")

        single = calculate_activity_metrics(activity)
        consolidated = calculate_project_metrics([activity, activity])

        assert single.cost_performance_index == consolidated.cost_performance_index
        assert single.tolerance == SMALL_TOLERANCE
        assert single.cost_status is CostStatus.ON_BUDGET
        assert consolidated.tolerance == MEDIUM_TOLERANCE
        assert consolidated.cost_status is CostStatus.OVER_BUDGET
