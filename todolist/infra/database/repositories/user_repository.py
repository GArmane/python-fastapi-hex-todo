from typing import Optional

from todolist.core.accounts.entities.user import User, UserRegistry
from todolist.infra.database.models.user import User as Model
from todolist.infra.database.sqlalchemy import database


async def fetch_by_email(email: str) -> Optional[User]:
    query = Model.select().where(Model.c.email == email)
    result = await database.fetch_one(query)

    return User.parse_obj(dict(result)) if result else None


async def register(registry: UserRegistry) -> User:
    values = registry.dict()
    query = Model.insert().values(**values)

    last_record_id = await database.execute(query)
    return User.parse_obj({**values, "id": last_record_id})
