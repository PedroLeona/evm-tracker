from decimal import Decimal

import pytest

from app.config import Settings, ToleranceTierSetting
from app.domain.tolerance import DEFAULT_TOLERANCE_POLICY, InvalidTolerancePolicyError

TIERS_ENV_VAR = "TOLERANCE_TIERS"


def test_defaults_apply_when_no_tiers_are_configured(monkeypatch):
    monkeypatch.delenv(TIERS_ENV_VAR, raising=False)

    assert Settings().tolerance_policy is DEFAULT_TOLERANCE_POLICY


def test_tiers_can_be_overridden_with_the_environment_variable(monkeypatch):
    monkeypatch.setenv(
        TIERS_ENV_VAR,
        '[{"min_budget": 0, "tolerance_percent": 8}, '
        '{"min_budget": 1000, "tolerance_percent": 2.5}]',
    )

    policy = Settings().tolerance_policy

    assert policy.tolerance_for(Decimal("999")) == Decimal("0.08")
    assert policy.tolerance_for(Decimal("1000")) == Decimal("0.025")


def test_percent_values_are_converted_to_fractions():
    settings = Settings(tolerance_tiers=[ToleranceTierSetting(min_budget=0, tolerance_percent=5)])

    assert settings.tolerance_policy.tolerance_for(Decimal("1")) == Decimal("0.05")


def test_invalid_configured_tiers_are_rejected():
    settings = Settings(tolerance_tiers=[ToleranceTierSetting(min_budget=100, tolerance_percent=5)])

    with pytest.raises(InvalidTolerancePolicyError):
        _ = settings.tolerance_policy
