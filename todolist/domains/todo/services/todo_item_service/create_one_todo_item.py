from typing import Awaitable, Callable

from todolist.domains.todo.entities.todo_item import CreateTodoItemDto, TodoItem


PersistOneFnType = Callable[[CreateTodoItemDto], Awaitable[TodoItem]]


async def create_one_todo_item(
    persist_one: PersistOneFnType, dto: CreateTodoItemDto,
) -> TodoItem:
    return await persist_one(dto)
