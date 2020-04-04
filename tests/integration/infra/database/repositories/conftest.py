import pytest

from tests.utils.database import clear_database
from todolist.infra.database.sqlalchemy import (
    connect_database,
    database,
    disconnect_database,
)


@pytest.fixture(name="database")
async def database_fixture():
    with clear_database():
        await connect_database()
        yield database
        await disconnect_database()
