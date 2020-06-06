from typing import Awaitable, Callable, Optional

from todolist.core.accounts.entities.user import Credentials, User, UserRegistry
from todolist.core.accounts.protocols import UserRepo
from todolist.core.accounts.services import hash_service
from todolist.core.accounts.services.exceptions import (
    EmailNotUniqueError,
    UserNotFoundError,
)

PersistUserFn = Callable[[str, str], Awaitable[User]]
FetchUserById = Callable[[int], Awaitable[Optional[User]]]


async def get_by_credentials(
    repo: UserRepo, credentials: Credentials,
) -> Optional[UserRegistry]:
    user = await repo.fetch_by_email(credentials.email.lower())

    if not user:
        return None

    password = credentials.password
    password_hash = user.password_hash

    if not hash_service.verify(password, password_hash):
        return None

    return UserRegistry(**user.dict())


async def get_by_id(repo: UserRepo, id_: int) -> Optional[UserRegistry]:
    user = await repo.fetch(id_)
    return UserRegistry(**user.dict()) if user else None


async def get_by_id_or_raise(repo: UserRepo, id_: int) -> UserRegistry:
    user = await get_by_id(repo, id_)
    if not user:
        raise UserNotFoundError(id_)
    return user


async def register(repo: UserRepo, credentials: Credentials) -> UserRegistry:
    email = credentials.email.lower()

    user = await repo.fetch_by_email(email)
    if user:
        raise EmailNotUniqueError(email)

    password_hash = hash_service.hash_(credentials.password)

    user = await repo.persist(email, password_hash)
    return UserRegistry(**user.dict())
