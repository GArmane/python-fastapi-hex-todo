from typing import Awaitable, Callable, Optional

from todolist.core.accounts.entities.user import Credentials, User, UserRegistry
from todolist.core.accounts.services import hash_service
from todolist.core.accounts.services.exceptions import EmailNotUniqueError

PersistUserFn = Callable[[str, str], Awaitable[User]]
FetchUserByEmail = Callable[[str], Awaitable[Optional[User]]]
FetchUserById = Callable[[int], Awaitable[Optional[User]]]


async def get_by_credentials(
    fetch_user: FetchUserByEmail, credentials: Credentials,
) -> Optional[UserRegistry]:
    user = await fetch_user(credentials.email.lower())

    if not user:
        return None

    password = credentials.password
    password_hash = user.password_hash

    if not hash_service.verify(password, password_hash):
        return None

    return UserRegistry(**user.dict())


async def get_by_id(fetch_user: FetchUserById, id_: int) -> Optional[UserRegistry]:
    user = await fetch_user(id_)
    return UserRegistry(**user.dict()) if user else None


async def register(
    fetch_user: FetchUserByEmail, persist_user: PersistUserFn, credentials: Credentials
) -> UserRegistry:
    email = credentials.email.lower()

    user = await fetch_user(email)
    if user:
        raise EmailNotUniqueError(email)

    password_hash = hash_service.hash_(credentials.password)

    user = await persist_user(email, password_hash)
    return UserRegistry(**user.dict())
