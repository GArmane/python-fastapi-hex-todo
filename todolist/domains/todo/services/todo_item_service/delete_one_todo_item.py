from typing import Callable


_DeleteOneFnType = Callable[[int], bool]


def delete_one_todo_item(delete_one: _DeleteOneFnType, id_: int) -> bool:
    return delete_one(id_)
