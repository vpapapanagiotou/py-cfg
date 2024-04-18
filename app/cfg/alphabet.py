from typing import List

from cfg.symbol import Symbol
from cfg.utilities import is_list_of_instance


class Alphabet:
    symbols: List[Symbol]

    def __init__(self, symbols: List[Symbol]):
        assert is_list_of_instance(symbols, Symbol)