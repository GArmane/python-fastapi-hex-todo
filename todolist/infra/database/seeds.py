import logging
from typing import Any, Dict, Iterable

from databases import Database
from sqlalchemy.schema import Table

from todolist.core.accounts.services.hash_service import hash_
from todolist.infra.database.models.todo_item import TodoItem
from todolist.infra.database.models.user import User
from todolist.infra.database.sqlalchemy import (
    database_context,
    init_database,
    truncate_database,
)

logger = logging.getLogger(__name__)


async def _populate_table(
    db: Database, table: Table, values: Iterable[Dict[str, Any]],
):
    name: str = table.name
    query = table.insert()

    logger.info(f"Seeding table {name}")
    await db.execute_many(query, list(values))
    logger.info(f"Seeded table {name} successfully")


async def _populate_user(db: Database) -> None:
    values = [
        {"email": "john.doe@gmail.com", "password_hash": hash_("dev@1234")},
        {"email": "jane.doe@gmail.com", "password_hash": hash_("dev2@1234")},
        {"email": "mark.fisher@yahoo.com", "password_hash": hash_("dev3@1234")},
        {"email": "ann.tobias@outlook.com", "password_hash": hash_("dev4@1234")},
    ]
    await _populate_table(db, User, values)
    for index, _ in enumerate(values):
        await _populate_todo_item(db, index + 1)


async def _populate_todo_item(db: Database, user_id: int) -> None:
    values = [
        {"msg": "Program new awesome web app", "is_done": True, "user_id": user_id},
        {"msg": "Play videogames", "is_done": True, "user_id": user_id},
        {"msg": "Wash dishes", "is_done": False, "user_id": user_id},
        {"msg": "Write blog post", "is_done": False, "user_id": user_id},
    ]
    await _populate_table(db, TodoItem, values)


async def run() -> None:
    logger.info("Initializing databases")
    init_database()
    async with database_context() as database:
        logger.info("Truncating database")
        await truncate_database()
        logger.info("Populating database")
        for fn in [_populate_user]:
            await fn(database)
        logger.info("Finished populating PostgreSQL database")
