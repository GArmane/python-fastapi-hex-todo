from typing import Awaitable, Callable, Iterable


DeleteManyFnType = Callable[[Iterable[int]], Awaitable[bool]]


async def delete_many_todo_items(
    delete_many: DeleteManyFnType, ids: Iterable[int]
) -> bool:
    return await delete_many(ids)
