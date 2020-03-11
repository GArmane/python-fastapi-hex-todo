from typing import Awaitable, Callable, Iterable, Optional, Tuple, TypeVar

from todolist.domains.todo.entities.todo_item import (
    CreateTodoItemDto,
    TodoItem,
    UpdateTodoItemDto,
)

PersistOneFnType = Callable[[CreateTodoItemDto], Awaitable[TodoItem]]

DeleteManyFnType = Callable[[Iterable[int]], Awaitable[bool]]
DeleteOneFnType = Callable[[int], Awaitable[bool]]

FetchAllFnType = Callable[[], Awaitable[Iterable[TodoItem]]]
FetchOneFnType = Callable[[int], Awaitable[TodoItem]]

T = TypeVar("T", CreateTodoItemDto, UpdateTodoItemDto)
UpdateFnType = Callable[[T, int], Awaitable[Optional[TodoItem]]]

KV = TypeVar("KV", CreateTodoItemDto, UpdateTodoItemDto)
UpdateManyFnType = Callable[[Iterable[Tuple[int, KV]]], Awaitable[Iterable[TodoItem]]]


async def create_one(
    persist_one: PersistOneFnType, dto: CreateTodoItemDto,
) -> TodoItem:
    return await persist_one(dto)


async def delete_many(delete_many: DeleteManyFnType, ids: Iterable[int]) -> bool:
    return await delete_many(ids)


async def delete_one(delete_one: DeleteOneFnType, id_: int) -> bool:
    return await delete_one(id_)


async def get_all(fetch_all: FetchAllFnType) -> Iterable[TodoItem]:
    return await fetch_all()


async def get_one(fetch_one: FetchOneFnType, id_: int) -> Optional[TodoItem]:
    return await fetch_one(id_)


async def update_many(
    update_many: UpdateManyFnType[KV], dtos: Iterable[KV], ids: Iterable[int]
) -> Iterable[TodoItem]:
    return await update_many(zip(ids, dtos))


async def update_one(
    update_one: UpdateFnType[T], dto: T, id_: int
) -> Optional[TodoItem]:
    return await update_one(dto, id_)
