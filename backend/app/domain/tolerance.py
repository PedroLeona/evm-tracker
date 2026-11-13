"""Tolerance policy: how far an index may stray from 1 and still count as "on plan".

The allowed deviation depends on the budget: the same percentage means very different
money on a small and on a large budget, so larger budgets get tighter tolerances.

Tiers are plain data, so the business can tune them without touching the calculation
logic (see ``Settings.tolerance_tiers``).
"""

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from decimal import Decimal

from app.constants import DEFAULT_TOLERANCE_TIERS, MAX_TOLERANCE, MIN_TOLERANCE


class InvalidTolerancePolicyError(ValueError):
    """Raised when the configured tolerance tiers are inconsistent."""


@dataclass(frozen=True)
class ToleranceTier:
    """From ``min_budget`` upwards, an index may deviate from 1 by ``tolerance`` (a fraction)."""

    min_budget: Decimal
    tolerance: Decimal


@dataclass(frozen=True)
class TolerancePolicy:
    tiers: tuple[ToleranceTier, ...]

    def __post_init__(self) -> None:
        _validate(self.tiers)

    @classmethod
    def from_pairs(cls, pairs: Iterable[tuple[Decimal, Decimal]]) -> "TolerancePolicy":
        ordered = sorted(pairs, key=lambda pair: pair[0])
        return cls(tuple(ToleranceTier(budget, tolerance) for budget, tolerance in ordered))

    def tolerance_for(self, budget: Decimal) -> Decimal:
        applicable = self.tiers[0]
        for tier in self.tiers:
            if budget >= tier.min_budget:
                applicable = tier
        return applicable.tolerance


def _validate(tiers: Sequence[ToleranceTier]) -> None:
    if not tiers:
        raise InvalidTolerancePolicyError("At least one tolerance tier is required")
    if tiers[0].min_budget != 0:
        raise InvalidTolerancePolicyError("The first tolerance tier must start at budget 0")
    _validate_ascending(tiers)
    _validate_tolerances(tiers)


def _validate_ascending(tiers: Sequence[ToleranceTier]) -> None:
    for previous, current in zip(tiers, tiers[1:], strict=False):
        if current.min_budget <= previous.min_budget:
            raise InvalidTolerancePolicyError("Tier budgets must be strictly ascending")


def _validate_tolerances(tiers: Sequence[ToleranceTier]) -> None:
    for tier in tiers:
        if not MIN_TOLERANCE <= tier.tolerance < MAX_TOLERANCE:
            raise InvalidTolerancePolicyError(
                "Each tolerance must be at least 0% and below 100%"
            )


DEFAULT_TOLERANCE_POLICY = TolerancePolicy.from_pairs(DEFAULT_TOLERANCE_TIERS)
