from typing import List

from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse  # type: ignore
from fastapi.routing import APIRouter

from todolist.api.container import get_dependencies
from todolist.api.routers.account.auth import get_current_user
from todolist.core.accounts.entities.user import UserRegistry
from todolist.core.todo.entities.todo_item import (
    CreateTodoItemDto,
    TodoItem,
    UpdateTodoItemDto,
)
from todolist.core.todo.services import todo_item_service
from todolist.infra.database.sqlalchemy import database


repo = get_dependencies().todo_item_repo
router = APIRouter()


# Handlers
@router.post(
    "",
    response_class=JSONResponse,
    response_model=TodoItem,
    status_code=201,
    responses={201: {"description": "Item created"}},
)
@database.transaction()
async def create(
    dto: CreateTodoItemDto, user: UserRegistry = Depends(get_current_user)
):
    return await todo_item_service.create(repo, user, dto)


@router.delete(
    "/{item_id}",
    response_class=JSONResponse,
    status_code=204,
    responses={
        204: {"description": "Item deleted"},
        401: {"description": "User unauthorized"},
        404: {"description": "Item not found"},
    },
)
@database.transaction()
async def delete(item_id: int, user: UserRegistry = Depends(get_current_user)):
    result = await todo_item_service.delete(repo, user, item_id)
    status_code = 204 if result else 404
    return JSONResponse(status_code=status_code)


@router.get(
    "",
    response_class=JSONResponse,
    response_model=List[TodoItem],
    status_code=200,
    responses={
        200: {"description": "Items found"},
        401: {"description": "User unauthorized"},
    },
)
@database.transaction()
async def get_all(user: UserRegistry = Depends(get_current_user)):
    return list(await todo_item_service.get_all(repo, user))


@router.get(
    "/{item_id}",
    response_class=JSONResponse,
    response_model=TodoItem,
    status_code=200,
    responses={
        200: {"description": "Item found"},
        401: {"description": "User unauthorized"},
        404: {"description": "Item not found"},
    },
)
@database.transaction()
async def get(item_id: int, user: UserRegistry = Depends(get_current_user)):
    item = await todo_item_service.get(repo, user, item_id)
    if not item:
        return JSONResponse(status_code=404)
    return item


@router.put(
    "/{item_id}",
    response_class=JSONResponse,
    response_model=TodoItem,
    status_code=200,
    responses={
        200: {"description": "Item replaced"},
        401: {"description": "User unauthorized"},
        404: {"description": "Item not found"},
    },
)
@database.transaction()
async def replace(
    dto: CreateTodoItemDto, item_id: int, user: UserRegistry = Depends(get_current_user)
):
    item = await todo_item_service.update(repo, user, dto, item_id)
    return item if item else JSONResponse(status_code=404)


@router.patch(
    "/{item_id}",
    response_class=JSONResponse,
    response_model=TodoItem,
    status_code=200,
    responses={
        200: {"description": "Item updated"},
        401: {"description": "User unauthorized"},
        404: {"description": "Item not found"},
    },
)
@database.transaction()
async def update(
    dto: UpdateTodoItemDto, item_id: int, user: UserRegistry = Depends(get_current_user)
):
    item = await todo_item_service.update(repo, user, dto, item_id)
    return item if item else JSONResponse(status_code=404)
