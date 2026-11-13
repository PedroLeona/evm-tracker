"""FastAPI application factory."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.constants import API_DOCS_URL, API_PREFIX, API_REDOC_URL
from app.errors import register_error_handlers
from app.routers import activities, projects

API_TITLE = "EVM Tracker API"
API_VERSION = "1.0.0"
API_DESCRIPTION = (
    "Manage projects and activities and get Earned Value Management indicators "
    "(PV, EV, CV, SV, CPI, SPI, EAC, VAC) per activity and consolidated per project."
)


def create_app() -> FastAPI:
    app = FastAPI(
        title=API_TITLE,
        version=API_VERSION,
        description=API_DESCRIPTION,
        docs_url=API_DOCS_URL,
        redoc_url=API_REDOC_URL,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(projects.router, prefix=API_PREFIX)
    app.include_router(activities.router, prefix=API_PREFIX)
    register_error_handlers(app)

    @app.get("/health", tags=["Health"], summary="Liveness probe")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
