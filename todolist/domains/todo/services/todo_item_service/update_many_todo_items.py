from typing import Callable, Iterable, Tuple, TypeVar

from todolist.domains.todo.entities.todo_item import (
    CreateTodoItemDto,
    TodoItem,
    UpdateTodoItemDto,
)

_KV = TypeVar("_KV", CreateTodoItemDto, UpdateTodoItemDto)
_UpdateManyFnType = Callable[[Iterable[Tuple[int, _KV]]], Iterable[TodoItem]]


def update_many_todo_items(
    update_many: _UpdateManyFnType[_KV], dtos: Iterable[_KV], ids: Iterable[int]
) -> Iterable[TodoItem]:
    return update_many(zip(ids, dtos))
