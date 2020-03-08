from typing import Callable, Optional, TypeVar

from todolist.domains.todo.entities.todo_item import (
    CreateTodoItemDto,
    TodoItem,
    UpdateTodoItemDto,
)

T = TypeVar("_T", CreateTodoItemDto, UpdateTodoItemDto)
UpdateFnType = Callable[[T, int], Optional[TodoItem]]


def update_one_todo_item(
    update_one: UpdateFnType[T], dto: T, id_: int
) -> Optional[TodoItem]:
    return update_one(dto, id_)
