from enum import Enum

from fastapi import status
from fastapi.routing import APIRouter
from pydantic import BaseModel, Field

from todolist.config.environment import get_current_settings

router = APIRouter()


class StatusEnum(str, Enum):
    OK = "OK"
    FAILURE = "FAILURE"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"


class HealthCheck(BaseModel):
    title: str = Field(..., description="API title")
    description: str = Field(..., description="Brief description of the API")
    version: str = Field(..., description="API semver version number")
    status: StatusEnum = Field(..., description="API current status")


@router.get(
    "/status",
    response_model=HealthCheck,
    status_code=status.HTTP_200_OK,
    tags=["Health Check"],
    summary="Performs health check",
    description="Performs health check and returns information about running service.",
)
def health_check():
    settings = get_current_settings()
    return {
        "title": settings.WEB_APP_TITLE,
        "description": settings.WEB_APP_DESCRIPTION,
        "version": settings.WEB_APP_VERSION,
        "status": StatusEnum.OK,
    }
