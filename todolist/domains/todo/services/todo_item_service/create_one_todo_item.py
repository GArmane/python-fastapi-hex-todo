from typing import Callable

from todolist.domains.todo.entities.todo_item import CreateTodoItemDto, TodoItem


PersistOneFnType = Callable[[CreateTodoItemDto], TodoItem]


def create_one_todo_item(
    persist_one: PersistOneFnType, dto: CreateTodoItemDto,
) -> TodoItem:
    return persist_one(dto)
