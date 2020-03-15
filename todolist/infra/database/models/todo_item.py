from sqlalchemy.schema import CheckConstraint, Column, Table
from sqlalchemy.types import Boolean, Integer, String

from todolist.infra.database.sqlalchemy import metadata

TodoItem = Table(
    "todo_item",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("msg", String(100), nullable=False),
    Column("is_done", Boolean(), nullable=False),
    CheckConstraint("length(msg) >= 1 AND length(msg) <= 50", name="msg_length",),
)
