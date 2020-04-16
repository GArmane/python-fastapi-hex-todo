from passlib.context import CryptContext


_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_(value: str) -> str:
    return str(_context.hash(value))


def verify(value: str, hash_: str) -> bool:
    return bool(_context.verify(value, hash_))
