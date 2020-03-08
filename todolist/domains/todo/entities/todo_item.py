from typing import Optional

from pydantic import BaseModel, Field

MsgType = Field(..., min_length=3, max_length=100)
OptionalMsgType = Field(None, min_length=3, max_length=100)


class TodoItem(BaseModel):
    id: int
    msg: str = MsgType
    is_done: bool

    class Config:
        allow_mutation = False
        orm_mode = True


class CreateTodoItemDto(BaseModel):
    msg: str = MsgType
    is_done: bool = False

    class Config:
        allow_mutation = False


class UpdateTodoItemDto(BaseModel):
    msg: Optional[str] = OptionalMsgType
    is_done: Optional[bool]

    class Config:
        allow_mutation = False
