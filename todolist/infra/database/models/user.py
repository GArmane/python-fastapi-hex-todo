from sqlalchemy.schema import Column, Table
from sqlalchemy.types import Integer, Text

from todolist.infra.database.sqlalchemy import metadata

User = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", Text(), unique=True, nullable=False),
    Column("password_hash", Text(), nullable=False),
)
