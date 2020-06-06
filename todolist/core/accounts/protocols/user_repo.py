from typing import Optional, Protocol

from todolist.core.accounts.entities.user import User


class UserRepo(Protocol):
    async def persist(self, email: str, password_hash: str) -> User:
        ...

    async def fetch(self, id_: int) -> Optional[User]:
        ...

    async def fetch_by_email(self, email: str) -> Optional[User]:
        ...
