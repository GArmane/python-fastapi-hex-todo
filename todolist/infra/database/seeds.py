import logging
from typing import Any, Dict, Iterable

from databases import Database
from sqlalchemy.schema import Table

from todolist.infra.database.models.todo_item import TodoItem
from todolist.infra.database.sqlalchemy import database_context, init_database

logger = logging.getLogger(__name__)


async def _populate_table(
    db: Database, table: Table, values: Iterable[Dict[str, Any]],
):
    name: str = table.name
    query = table.insert()

    logger.info(f"Seeding table {name}")
    await db.execute_many(query, list(values))
    logger.info(f"Seeded table {name} successfully")


async def _populate_todo_item(db: Database) -> None:
    values = [
        {"id": 1, "msg": "Program new awesome web app", "is_done": True},
        {"id": 2, "msg": "Play videogames", "is_done": True},
        {"id": 3, "msg": "Wash dishes", "is_done": False},
        {"id": 4, "msg": "Write blog post", "is_done": False},
    ]
    await _populate_table(db, TodoItem, values)


async def run() -> None:
    logger.info("Initializing databases")
    init_database()
    async with database_context() as database:
        logger.info("Populating PostgreSQL database")
        await _populate_todo_item(database)
        logger.info("Finished populating PostgreSQL database")
