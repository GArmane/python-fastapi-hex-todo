from contextlib import contextmanager

from todolist.infra.database.sqlalchemy import init_database, metadata


def _truncate_tables():
    metadata.bind.execute(
        "TRUNCATE {} RESTART IDENTITY".format(
            ",".join(table.name for table in reversed(metadata.sorted_tables))
        )
    )


@contextmanager
def clear_database():
    init_database()
    _truncate_tables()
    yield
    _truncate_tables()
