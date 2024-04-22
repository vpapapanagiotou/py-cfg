from typing import List, Set


def is_list_of_instance(obj, class_or_tuple) -> bool:
    return isinstance(obj, List) and all(map(lambda i: isinstance(i, class_or_tuple), obj))


def is_set_of_instance(obj, class_or_tuple) -> bool:
    return isinstance(obj, Set) and all(map(lambda i: isinstance(i, class_or_tuple), obj))
