from typing import List


def _ljust_max(strings: List[str]) -> List[str]:
    n = max(map(len, strings))

    return list(map(lambda s: s.ljust(n), strings))
