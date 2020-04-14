from fastapi.routing import APIRouter
from . import user


def _build_router() -> APIRouter:
    rt = APIRouter()
    rt.include_router(user.router, prefix="/user", tags=["User"])
    return rt


router = _build_router()
