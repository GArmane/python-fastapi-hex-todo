from typing import Callable, Iterable


DeleteManyFnType = Callable[[Iterable[int]], bool]


def delete_many_todo_items(delete_many: DeleteManyFnType, ids: Iterable[int]) -> bool:
    return delete_many(ids)
