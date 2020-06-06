from functools import partial
from typing import Any, Dict, Iterable, Union

from sqlalchemy.schema import Table

from todolist.infra.database.models.todo_item import TodoItem
from todolist.infra.database.models.user import User
from todolist.infra.database.sqlalchemy import metadata


ValuesType = Dict[str, Any]


def insert_model(model: Table, values: Union[ValuesType, Iterable[ValuesType]]) -> None:
    query = model.insert()
    if isinstance(values, Dict):
        metadata.bind.execute(query, **values)
    else:
        metadata.bind.execute(query, list(values))


register_user = partial(insert_model, User)
insert_todo_item = partial(insert_model, TodoItem)
