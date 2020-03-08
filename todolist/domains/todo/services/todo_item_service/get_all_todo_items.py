from typing import Awaitable, Callable, Iterable

from todolist.domains.todo.entities.todo_item import TodoItem


FetchAllFnType = Callable[[], Awaitable[Iterable[TodoItem]]]


async def get_all_todo_items(fetch_all: FetchAllFnType) -> Iterable[TodoItem]:
    return await fetch_all()
