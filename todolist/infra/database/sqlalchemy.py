import databases
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData
from toolz.functoolz import pipe

from todolist.config.environment import get_initial_settings

_SETTINGS = get_initial_settings()


database = databases.Database(_SETTINGS.DATABASE_PG_URL)
metadata = MetaData()


async def connect_database():
    await database.connect()


async def disconnect_database():
    await database.disconnect()


def init_database() -> None:
    import todolist.infra.database.models  # noqa: F401

    pipe(_SETTINGS.DATABASE_PG_URL, create_engine)
