from typing import Iterable, Optional, Protocol

from todolist.core.accounts.entities.user import UserRegistry
from todolist.core.todo.entities.todo_item import (
    CreateTodoItemDto,
    TodoItem,
    UpdateTodoItemDto,
)


class TodoItemRepo(Protocol):
    async def delete(self, user: UserRegistry, id_: int) -> bool:
        ...

    async def fetch(self, user: UserRegistry, id_: int) -> Optional[TodoItem]:
        ...

    async def fetch_all_by_user(self, user: UserRegistry) -> Iterable[TodoItem]:
        ...

    async def persist(self, user: UserRegistry, dto: CreateTodoItemDto) -> TodoItem:
        ...

    async def replace(
        self, user: UserRegistry, dto: CreateTodoItemDto, id_: int,
    ) -> Optional[TodoItem]:
        ...

    async def update(
        self, user: UserRegistry, dto: UpdateTodoItemDto, id_: int,
    ) -> Optional[TodoItem]:
        ...
