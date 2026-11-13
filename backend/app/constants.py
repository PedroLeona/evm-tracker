"""Shared constants. Centralised so no magic numbers or strings leak into the code."""

from decimal import Decimal

API_PREFIX = "/api"
API_DOCS_URL = "/api-docs"
API_REDOC_URL = "/api-redoc"

PERCENT_BASE = Decimal("100")
NEUTRAL_INDEX = Decimal("1")
NO_TOLERANCE = Decimal("0")
MIN_TOLERANCE = NO_TOLERANCE
MAX_TOLERANCE = Decimal("1")

# Default tolerance tiers as (minimum BAC, allowed deviation of an index from 1).
# The same percentage is worth far more money on a large budget, so larger budgets
# get tighter tolerances. Amounts use the same currency as the BAC. These values are
# a starting point: the business can override them with the TOLERANCE_TIERS setting.
DEFAULT_TOLERANCE_TIERS = (
    (Decimal("0"), Decimal("0.05")),
    (Decimal("50000000"), Decimal("0.03")),
    (Decimal("500000000"), Decimal("0.01")),
)
INDEX_PRECISION = Decimal("0.0001")
MONEY_PRECISION = Decimal("0.01")

NAME_MAX_LENGTH = 120
DESCRIPTION_MAX_LENGTH = 500

MONEY_MAX_DIGITS = 14
PERCENT_MAX_DIGITS = 5
DECIMAL_PLACES = 2
MIN_PERCENT = 0
MAX_PERCENT = 100

RESOURCE_PROJECT = "Project"
RESOURCE_ACTIVITY = "Activity"
