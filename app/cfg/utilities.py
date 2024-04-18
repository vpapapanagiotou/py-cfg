from typing import List


def is_optional_instance(obj, class_or_tuple) -> bool:
    return obj is None or isinstance(obj, class_or_tuple)


def is_list_of_instance(obj, class_or_tuple) -> bool:
    return isinstance(obj, List) and all(map(lambda i: isinstance(i, class_or_tuple), obj))


def append(list: List, item) -> int:
    """
    Append item to list and return the index of the item in the list

    :param list:
    :return:
    """
    list.append(item)

    return len(list) - 1
