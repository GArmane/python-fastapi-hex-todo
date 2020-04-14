from typing import List

from fastapi.responses import JSONResponse  # type: ignore
from fastapi.routing import APIRouter

from todolist.core.todo.entities.todo_item import (
    CreateTodoItemDto,
    TodoItem,
    UpdateTodoItemDto,
)
from todolist.core.todo.services import todo_item_service
from todolist.infra.database.repositories import todo_item_repository
from todolist.infra.database.sqlalchemy import database

# Router
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
async def create_one(dto: CreateTodoItemDto):
    return await todo_item_service.create_one(todo_item_repository.create_one, dto)


@router.delete(
    "/{item_id}",
    response_class=JSONResponse,
    status_code=204,
    responses={
        204: {"description": "Item deleted"},
        404: {"description": "Item not found"},
    },
)
@database.transaction()
async def delete_one(item_id: int):
    result = await todo_item_service.delete_one(
        todo_item_repository.delete_one, item_id
    )
    status_code = 204 if result else 404
    return JSONResponse(status_code=status_code)


@router.get(
    "",
    response_class=JSONResponse,
    response_model=List[TodoItem],
    status_code=200,
    responses={200: {"description": "Items found"}},
)
@database.transaction()
async def get_all():
    return list(await todo_item_service.get_all(todo_item_repository.get_all))


@router.get(
    "/{item_id}",
    response_class=JSONResponse,
    response_model=TodoItem,
    status_code=200,
    responses={
        200: {"description": "Item found"},
        404: {"description": "Item not found"},
    },
)
@database.transaction()
async def get_one(item_id: int):
    item = await todo_item_service.get_one(todo_item_repository.get_one_by_id, item_id)
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
        404: {"description": "Item not found"},
    },
)
@database.transaction()
async def replace_one(dto: CreateTodoItemDto, item_id: int):
    item = await todo_item_service.update_one(
        todo_item_repository.replace_one_by_id, dto, item_id
    )
    return item if item else JSONResponse(status_code=404)


@router.patch(
    "/{item_id}",
    response_class=JSONResponse,
    response_model=TodoItem,
    status_code=200,
    responses={
        200: {"description": "Item updated"},
        404: {"description": "Item not found"},
    },
)
@database.transaction()
async def update_one(dto: UpdateTodoItemDto, item_id: int):
    item = await todo_item_service.update_one(
        todo_item_repository.update_one_by_id, dto, item_id
    )
    return item if item else JSONResponse(status_code=404)
