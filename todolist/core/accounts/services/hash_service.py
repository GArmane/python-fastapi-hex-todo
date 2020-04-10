from passlib.hash import argon2

_hasher: argon2 = argon2.using()


def hash_(value: str) -> str:
    return str(_hasher.hash(value))


def verify(value: str, hash_: str) -> bool:
    return bool(_hasher.verify(value, hash_))
