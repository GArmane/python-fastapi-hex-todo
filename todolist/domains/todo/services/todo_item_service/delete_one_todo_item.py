from typing import Callable


DeleteOneFnType = Callable[[int], bool]


def delete_one_todo_item(delete_one: DeleteOneFnType, id_: int) -> bool:
    return delete_one(id_)
