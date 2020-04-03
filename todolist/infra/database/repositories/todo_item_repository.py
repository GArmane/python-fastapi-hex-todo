from typing import Iterable, Optional

from todolist.core.todo.entities.todo_item import (
    CreateTodoItemDto,
    TodoItem,
    UpdateTodoItemDto,
)
from todolist.infra.database.models.todo_item import TodoItem as Model
from todolist.infra.database.sqlalchemy import database


async def count_by_id(id_: int) -> int:
    query = Model.count().where(Model.c.id == id_)
    return int(await database.execute(query))


async def create_one(dto: CreateTodoItemDto) -> TodoItem:
    values = dto.dict()
    query = Model.insert().values(**values)

    last_record_id = await database.execute(query)
    return TodoItem.parse_obj({**values, "id": last_record_id})


async def delete_one(id_: int) -> bool:
    if not await count_by_id(id_):
        return False

    query = Model.delete().where(Model.c.id == id_)
    await database.execute(query)
    return True


async def get_all() -> Iterable[TodoItem]:
    query = Model.select()
    results = await database.fetch_all(query)
    return (TodoItem.parse_obj(dict(r)) for r in results)


async def get_one_by_id(id_: int) -> Optional[TodoItem]:
    query = Model.select().where(Model.c.id == id_)
    result = await database.fetch_one(query)
    return TodoItem.parse_obj(dict(result)) if result else None


async def replace_one_by_id(dto: CreateTodoItemDto, id_: int) -> Optional[TodoItem]:
    if not await count_by_id(id_):
        return None

    values = dto.dict()
    query = Model.update().where(Model.c.id == id_).values(**values)
    await database.execute(query)
    return TodoItem.parse_obj({**values, "id": id_})


async def update_one_by_id(dto: UpdateTodoItemDto, id_: int) -> Optional[TodoItem]:
    if not await count_by_id(id_):
        return None

    values = dto.dict(exclude_unset=True)
    query = Model.update().where(Model.c.id == id_).values(**values)
    await database.execute(query)

    return await get_one_by_id(id_)
