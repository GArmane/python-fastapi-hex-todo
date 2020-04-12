from pydantic import BaseModel, EmailStr, Field


class Credentials(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

    class Config:
        allow_mutation = False
        orm_mode = True


class User(BaseModel):
    id: int
    email: EmailStr
    password_hash: str

    class Config:
        allow_mutation = False
        orm_mode = True


class UserRegistry(BaseModel):
    email: EmailStr
    password_hash: str

    class Config:
        allow_mutation = False
        orm_mode = True
