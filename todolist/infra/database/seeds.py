import logging

from databases import Database
from todolist.infra.database.sqlalchemy import database_context, init_database

logger = logging.getLogger(__name__)


async def _populate_todo_item(db: Database) -> None:
    logger.info("Seeding entity TodoItem")
    pass


async def run() -> None:
    logger.info("Initializing databases")
    init_database()
    async with database_context() as database:
        logger.info("Populating PostgreSQL database")
        await _populate_todo_item(database)
        logger.info("Finished populating PostgreSQL database")
