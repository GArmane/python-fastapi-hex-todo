from typing import Callable, Iterable


_DeleteManyFnType = Callable[[Iterable[int]], bool]


def delete_many_todo_items(delete_many: _DeleteManyFnType, ids: Iterable[int]) -> bool:
    return delete_many(ids)
