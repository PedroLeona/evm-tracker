"""Domain-level errors and their translation into HTTP responses."""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class ResourceNotFoundError(Exception):
    def __init__(self, resource: str, identifier: int) -> None:
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} {identifier} not found")


async def _handle_not_found(_: Request, error: ResourceNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(error)},
    )


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ResourceNotFoundError, _handle_not_found)
