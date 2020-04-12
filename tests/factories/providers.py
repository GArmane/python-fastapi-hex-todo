from faker.providers import BaseProvider
from faker import Faker

from passlib.hash import argon2


fake = Faker()


class PasswordHashProvider(BaseProvider):
    def password_hash(self) -> str:
        return str(argon2.hash(fake.pystr()))
