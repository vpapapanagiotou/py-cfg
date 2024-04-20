from typing import List


def is_list_of_instance(obj, class_or_tuple) -> bool:
    return isinstance(obj, List) and all(map(lambda i: isinstance(i, class_or_tuple), obj))
