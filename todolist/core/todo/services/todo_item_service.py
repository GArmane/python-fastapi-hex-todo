from typing import Awaitable, Callable, Iterable, Optional, Tuple, TypeVar

from todolist.core.accounts.entities.user import UserRegistry
from todolist.core.todo.entities.todo_item import (
    CreateTodoItemDto,
    TodoItem,
    UpdateTodoItemDto,
)

PersistOneFnType = Callable[[UserRegistry, CreateTodoItemDto], Awaitable[TodoItem]]

DeleteManyFnType = Callable[[UserRegistry, Iterable[int]], Awaitable[bool]]
DeleteOneFnType = Callable[[UserRegistry, int], Awaitable[bool]]

FetchAllFnType = Callable[[UserRegistry], Awaitable[Iterable[TodoItem]]]
FetchOneFnType = Callable[[UserRegistry, int], Awaitable[Optional[TodoItem]]]

T = TypeVar("T", CreateTodoItemDto, UpdateTodoItemDto)
UpdateFnType = Callable[[UserRegistry, T, int], Awaitable[Optional[TodoItem]]]

KV = TypeVar("KV", CreateTodoItemDto, UpdateTodoItemDto)
UpdateManyFnType = Callable[
    [UserRegistry, Iterable[Tuple[int, KV]]], Awaitable[Iterable[TodoItem]]
]


async def create_one(
    persist_one: PersistOneFnType, user: UserRegistry, dto: CreateTodoItemDto,
) -> TodoItem:
    return await persist_one(user, dto)


async def delete_many(
    delete_many: DeleteManyFnType, user: UserRegistry, ids: Iterable[int]
) -> bool:
    return await delete_many(user, ids)


async def delete_one(delete_one: DeleteOneFnType, user: UserRegistry, id_: int) -> bool:
    return await delete_one(user, id_)


async def get_all(fetch_all: FetchAllFnType, user: UserRegistry) -> Iterable[TodoItem]:
    return await fetch_all(user)


async def get_one(
    fetch_one: FetchOneFnType, user: UserRegistry, id_: int
) -> Optional[TodoItem]:
    return await fetch_one(user, id_)


async def update_many(
    update_many: UpdateManyFnType[KV],
    user: UserRegistry,
    dtos: Iterable[KV],
    ids: Iterable[int],
) -> Iterable[TodoItem]:
    return await update_many(user, zip(ids, dtos))


async def update_one(
    update_one: UpdateFnType[T], user: UserRegistry, dto: T, id_: int
) -> Optional[TodoItem]:
    return await update_one(user, dto, id_)
