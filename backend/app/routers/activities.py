"""HTTP endpoints for activities."""

from fastapi import APIRouter, Depends, Response, status

from app.dependencies import get_activity_service
from app.mappers import to_activity_response
from app.routers.responses import NOT_FOUND_RESPONSE
from app.schemas import ActivityPayload, ActivityResponse
from app.services.activity_service import ActivityService

router = APIRouter(tags=["Activities"])


@router.get(
    "/projects/{project_id}/activities",
    response_model=list[ActivityResponse],
    responses=NOT_FOUND_RESPONSE,
    summary="List a project's activities with their EVM metrics",
)
def list_activities(
    project_id: int, service: ActivityService = Depends(get_activity_service)
) -> list[ActivityResponse]:
    return [
        to_activity_response(activity) for activity in service.list_for_project(project_id)
    ]


@router.post(
    "/projects/{project_id}/activities",
    response_model=ActivityResponse,
    status_code=status.HTTP_201_CREATED,
    responses=NOT_FOUND_RESPONSE,
    summary="Create an activity in a project",
)
def create_activity(
    project_id: int,
    payload: ActivityPayload,
    service: ActivityService = Depends(get_activity_service),
) -> ActivityResponse:
    return to_activity_response(service.create_activity(project_id, payload))


@router.get(
    "/activities/{activity_id}",
    response_model=ActivityResponse,
    responses=NOT_FOUND_RESPONSE,
    summary="Get an activity with its EVM metrics",
)
def get_activity(
    activity_id: int, service: ActivityService = Depends(get_activity_service)
) -> ActivityResponse:
    return to_activity_response(service.get_activity(activity_id))


@router.put(
    "/activities/{activity_id}",
    response_model=ActivityResponse,
    responses=NOT_FOUND_RESPONSE,
    summary="Replace an activity's data",
)
def update_activity(
    activity_id: int,
    payload: ActivityPayload,
    service: ActivityService = Depends(get_activity_service),
) -> ActivityResponse:
    return to_activity_response(service.update_activity(activity_id, payload))


@router.delete(
    "/activities/{activity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=NOT_FOUND_RESPONSE,
    summary="Delete an activity",
)
def delete_activity(
    activity_id: int, service: ActivityService = Depends(get_activity_service)
) -> Response:
    service.delete_activity(activity_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
