from fastapi.routing import APIRouter
from pydantic import BaseModel, Field
from todolist.config.environment import get_current_settings


router = APIRouter()


class Status(BaseModel):
    title: str = Field(..., description="API title")
    description: str = Field(..., description="Brief description of the API")
    version: str = Field(..., description="API semver version number")
    status: str = Field(..., description="API current status")


@router.get("/status", status_code=200, response_model=Status)
def health_check():
    settings = get_current_settings()
    return {
        "title": settings.WEB_APP_TITLE,
        "description": settings.WEB_APP_DESCRIPTION,
        "version": settings.WEB_APP_VERSION,
        "status": "OK",
    }
