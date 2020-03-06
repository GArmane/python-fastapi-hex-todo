from typing import Protocol
from todolist.domain.entities.todo_item import CreateTodoItemDto, TodoItem


class _Deps(Protocol):
    def create_one(self, dto: CreateTodoItemDto) -> TodoItem:
        ...


def create_one_todo_item(dto: CreateTodoItemDto, deps: _Deps) -> TodoItem:
    return deps.create_one(dto)
