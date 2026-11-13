"""Shared constants. Centralised so no magic numbers or strings leak into the code."""

from decimal import Decimal

API_PREFIX = "/api"
API_DOCS_URL = "/api-docs"
API_REDOC_URL = "/api-redoc"

PERCENT_BASE = Decimal("100")
NEUTRAL_INDEX = Decimal("1")
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
