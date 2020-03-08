from typing import Awaitable, Callable, Iterable, Tuple, TypeVar

from todolist.domains.todo.entities.todo_item import (
    CreateTodoItemDto,
    TodoItem,
    UpdateTodoItemDto,
)

KV = TypeVar("KV", CreateTodoItemDto, UpdateTodoItemDto)
UpdateManyFnType = Callable[[Iterable[Tuple[int, KV]]], Awaitable[Iterable[TodoItem]]]


async def update_many_todo_items(
    update_many: UpdateManyFnType[KV], dtos: Iterable[KV], ids: Iterable[int]
) -> Iterable[TodoItem]:
    return await update_many(zip(ids, dtos))
