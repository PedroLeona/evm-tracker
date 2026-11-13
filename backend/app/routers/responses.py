"""Reusable OpenAPI response declarations."""

from typing import Any

from app.schemas import ErrorResponse

NOT_FOUND_RESPONSE: dict[int | str, dict[str, Any]] = {
    404: {"model": ErrorResponse, "description": "The requested resource does not exist."}
}
