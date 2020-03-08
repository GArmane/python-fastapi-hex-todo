from typing import Awaitable, Callable, Optional

from todolist.domains.todo.entities.todo_item import TodoItem


FetchOneFnType = Callable[[int], Awaitable[TodoItem]]


async def get_one_todo_item(fetch_one: FetchOneFnType, id_: int) -> Optional[TodoItem]:
    return await fetch_one(id_)
