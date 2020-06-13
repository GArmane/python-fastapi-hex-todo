from dataclasses import dataclass
from typing import Callable, cast

from todolist.core.accounts.protocols import UserRepo
from todolist.core.todo.protocols import TodoItemRepo
from todolist.infra.database.repositories import todo_item_repository, user_repository


@dataclass(frozen=True)
class Dependencies:
    user_repo: UserRepo
    todo_item_repo: TodoItemRepo


def _build_dependencies() -> Callable[[], Dependencies]:
    deps = Dependencies(
        user_repo=cast(UserRepo, user_repository),
        todo_item_repo=cast(TodoItemRepo, todo_item_repository),
    )

    def fn() -> Dependencies:
        return deps

    return fn


get_dependencies = _build_dependencies()
