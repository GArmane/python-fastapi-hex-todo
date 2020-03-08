from typing import Awaitable, Callable


DeleteOneFnType = Callable[[int], Awaitable[bool]]


async def delete_one_todo_item(delete_one: DeleteOneFnType, id_: int) -> bool:
    return await delete_one(id_)
