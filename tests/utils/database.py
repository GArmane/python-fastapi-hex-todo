from todolist.infra.database.sqlalchemy import init_database, metadata


def clear_database():
    init_database()
    metadata.bind.execute(
        "TRUNCATE {} RESTART IDENTITY".format(
            ",".join(table.name for table in reversed(metadata.sorted_tables))
        )
    )
