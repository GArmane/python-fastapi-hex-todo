from sqlalchemy.schema import Table, Column
from sqlalchemy.types import Integer, String, Boolean
from todolist.infra.database.sqlalchemy import metadata


TodoItem = Table(
    "todo_item",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("msg", String(100), nullable=False),
    Column("is_done", Boolean(), nullable=False),
)
