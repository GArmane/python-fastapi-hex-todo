from typing import Awaitable, Callable, Optional, TypeVar

from todolist.domains.todo.entities.todo_item import (
    CreateTodoItemDto,
    TodoItem,
    UpdateTodoItemDto,
)

T = TypeVar("T", CreateTodoItemDto, UpdateTodoItemDto)
UpdateFnType = Callable[[T, int], Awaitable[Optional[TodoItem]]]


async def update_one_todo_item(
    update_one: UpdateFnType[T], dto: T, id_: int
) -> Optional[TodoItem]:
    return await update_one(dto, id_)
