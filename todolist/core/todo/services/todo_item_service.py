from typing import Iterable, Optional, Union

from todolist.core.accounts.entities.user import UserRegistry
from todolist.core.todo.entities.todo_item import (
    CreateTodoItemDto,
    TodoItem,
    UpdateTodoItemDto,
)
from todolist.core.todo.protocols import TodoItemRepo


async def create(
    repo: TodoItemRepo, user: UserRegistry, dto: CreateTodoItemDto,
) -> TodoItem:
    return await repo.persist(user, dto)


async def delete(repo: TodoItemRepo, user: UserRegistry, id_: int) -> bool:
    return await repo.delete(user, id_)


async def get(repo: TodoItemRepo, user: UserRegistry, id_: int) -> Optional[TodoItem]:
    return await repo.fetch(user, id_)


async def get_all(repo: TodoItemRepo, user: UserRegistry) -> Iterable[TodoItem]:
    return await repo.fetch_all_by_user(user)


async def update(
    repo: TodoItemRepo,
    user: UserRegistry,
    dto: Union[CreateTodoItemDto, UpdateTodoItemDto],
    id_: int,
) -> Optional[TodoItem]:
    if isinstance(dto, CreateTodoItemDto):
        return await repo.replace(user, dto, id_)
    else:
        return await repo.update(user, dto, id_)
