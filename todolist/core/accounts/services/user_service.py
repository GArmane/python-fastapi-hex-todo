from typing import Awaitable, Callable, Optional

from todolist.core.accounts.entities.user import Credentials, User, UserRegistry
from todolist.core.accounts.services import hash_service

PersistOneFn = Callable[[UserRegistry], Awaitable[User]]
FetchByCredentialsFn = Callable[[Credentials], Awaitable[Optional[User]]]


async def get_by_credentials(
    fetch_user: FetchByCredentialsFn, credentials: Credentials
) -> Optional[User]:
    user = await fetch_user(credentials)

    if not user:
        return None

    password = credentials.password
    password_hash = user.password_hash

    if not hash_service.verify(password, password_hash):
        return None

    return user


async def register(persist_one: PersistOneFn, credentials: Credentials) -> User:
    password_hash = hash_service.hash_(credentials.password)
    registry = UserRegistry(email=credentials.email, password_hash=password_hash)

    return await persist_one(registry)
