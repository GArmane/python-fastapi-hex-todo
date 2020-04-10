from typing import List

from fastapi import Response
from fastapi.routing import APIRouter

from todolist.core.todo.entities.todo_item import (
    CreateTodoItemDto,
    TodoItem,
    UpdateTodoItemDto,
)
from todolist.core.todo.services import todo_item_service
from todolist.infra.database.repositories.todo_item_repository import (
    create_one as repo_create_one,
    delete_one as repo_delete_one,
    get_all as repo_get_all,
    get_one_by_id as repo_get_one_by_id,
    replace_one_by_id as repo_replace_one_by_id,
    update_one_by_id as repo_update_one_by_id,
)
from todolist.infra.database.sqlalchemy import database

# Router
router = APIRouter()


# Handlers
@router.post(
    "",
    response_model=TodoItem,
    status_code=201,
    responses={201: {"description": "Item created"}},
)
@database.transaction()
async def create_one(dto: CreateTodoItemDto):
    return await todo_item_service.create_one(repo_create_one, dto)


@router.delete(
    "/{item_id}",
    status_code=204,
    responses={
        204: {"description": "Item deleted"},
        404: {"description": "Item not found"},
    },
)
@database.transaction()
async def delete_one(item_id: int):
    result = await todo_item_service.delete_one(repo_delete_one, item_id)
    if not result:
        return Response(status_code=404)
    return Response(status_code=204)


@router.get(
    "",
    response_model=List[TodoItem],
    status_code=200,
    responses={200: {"description": "Items found"}},
)
@database.transaction()
async def get_all():
    return list(await todo_item_service.get_all(repo_get_all))


@router.get(
    "/{item_id}",
    response_model=TodoItem,
    status_code=200,
    responses={
        200: {"description": "Item found"},
        404: {"description": "Item not found"},
    },
)
@database.transaction()
async def get_one(item_id: int):
    item = await todo_item_service.get_one(repo_get_one_by_id, item_id)
    if not item:
        return Response(status_code=404)
    return item


@router.put(
    "/{item_id}",
    response_model=TodoItem,
    status_code=200,
    responses={
        200: {"description": "Item replaced"},
        404: {"description": "Item not found"},
    },
)
@database.transaction()
async def replace_one(dto: CreateTodoItemDto, item_id: int):
    item = await todo_item_service.update_one(repo_replace_one_by_id, dto, item_id)
    return item if item else Response(status_code=404)


@router.patch(
    "/{item_id}",
    response_model=TodoItem,
    status_code=200,
    responses={
        200: {"description": "Item updated"},
        404: {"description": "Item not found"},
    },
)
@database.transaction()
async def update_one(dto: UpdateTodoItemDto, item_id: int):
    item = await todo_item_service.update_one(repo_update_one_by_id, dto, item_id)
    return item if item else Response(status_code=404)
