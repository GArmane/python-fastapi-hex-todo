from typing import Callable, Optional

from todolist.domains.todo.entities.todo_item import TodoItem


FetchOneFnType = Callable[[int], TodoItem]


def get_one_todo_item(fetch_one: FetchOneFnType, id_: int) -> Optional[TodoItem]:
    return fetch_one(id_)
