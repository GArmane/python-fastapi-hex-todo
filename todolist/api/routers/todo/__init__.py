from fastapi.routing import APIRouter

from . import todo_item


def _build_router() -> APIRouter:
    rt = APIRouter()
    rt.include_router(todo_item.router, prefix="/item", tags=["Todo Item"])
    return rt


router = _build_router()
