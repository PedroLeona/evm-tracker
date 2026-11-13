"""HTTP endpoints for projects and their consolidated EVM report."""

from fastapi import APIRouter, Depends, Response, status

from app.dependencies import get_project_service, get_tolerance_policy
from app.domain.tolerance import TolerancePolicy
from app.mappers import to_report_response
from app.routers.responses import NOT_FOUND_RESPONSE
from app.schemas import ProjectEvmReportResponse, ProjectPayload, ProjectResponse
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("", response_model=list[ProjectResponse], summary="List projects")
def list_projects(
    service: ProjectService = Depends(get_project_service),
) -> list[ProjectResponse]:
    return [ProjectResponse.model_validate(project) for project in service.list_projects()]


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a project",
)
def create_project(
    payload: ProjectPayload, service: ProjectService = Depends(get_project_service)
) -> ProjectResponse:
    return ProjectResponse.model_validate(service.create_project(payload))


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    responses=NOT_FOUND_RESPONSE,
    summary="Get a project",
)
def get_project(
    project_id: int, service: ProjectService = Depends(get_project_service)
) -> ProjectResponse:
    return ProjectResponse.model_validate(service.get_project(project_id))


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    responses=NOT_FOUND_RESPONSE,
    summary="Replace a project's data",
)
def update_project(
    project_id: int,
    payload: ProjectPayload,
    service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    return ProjectResponse.model_validate(service.update_project(project_id, payload))


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=NOT_FOUND_RESPONSE,
    summary="Delete a project and all its activities",
)
def delete_project(
    project_id: int, service: ProjectService = Depends(get_project_service)
) -> Response:
    service.delete_project(project_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{project_id}/evm",
    response_model=ProjectEvmReportResponse,
    responses=NOT_FOUND_RESPONSE,
    summary="Earned Value report",
    description=(
        "Returns the project, its per-activity metrics and the consolidated "
        "project metrics (computed from summed PV, EV and AC), including the "
        "CPI and SPI interpretation."
    ),
)
def get_project_evm_report(
    project_id: int,
    service: ProjectService = Depends(get_project_service),
    policy: TolerancePolicy = Depends(get_tolerance_policy),
) -> ProjectEvmReportResponse:
    return to_report_response(service.build_report(project_id, policy), policy)
