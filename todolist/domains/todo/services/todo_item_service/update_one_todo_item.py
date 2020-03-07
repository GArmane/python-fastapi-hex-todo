from typing import Callable, Optional, TypeVar

from todolist.domains.todo.entities.todo_item import (
    CreateTodoItemDto,
    TodoItem,
    UpdateTodoItemDto,
)

_T = TypeVar("_T", CreateTodoItemDto, UpdateTodoItemDto)
_UpdateFnType = Callable[[_T, int], Optional[TodoItem]]


def update_one_todo_item(
    update_one: _UpdateFnType[_T], dto: _T, id_: int
) -> Optional[TodoItem]:
    return update_one(dto, id_)
