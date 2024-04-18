from typing import Generator, List, Optional

from cfg.symbol import EMPTY_STRING_LABEL, START_LABEL, Symbol
from cfg.utilities import is_list_of_instance


class Alphabet:
    symbols: List[Symbol]

    def __init__(self, symbols: List[Symbol]):
        assert is_list_of_instance(symbols, Symbol)

        self.symbols = list()
        self.symbols.append(Symbol(label=START_LABEL, is_terminal=False, description='The start symbol'))
        self.symbols.append(Symbol(label=EMPTY_STRING_LABEL, is_terminal=True, description='The empty string symbol'))

        for symbol in symbols:
            if symbol in self.symbols:
                raise ValueError(f'Cannot have multiple symbols with the same label (duplicate label is "{symbol}"')
            self.symbols.append(symbol)

    def __getitem__(self, item):
        return self.symbols[item]

    def __iter__(self)-> Generator[Symbol, None, None]:
        for symbol in self.symbols:
            yield symbol

    def get_start_symbol(self) -> Symbol:
        return self[0]

    def get_empty_string_symbol(self) -> Symbol:
        return self[1]

    def get_by_label(self, label: str) -> Optional[None]:
        result = list(filter(lambda symbol: symbol == label, self.symbols))
        if len(result) == 0:
            return None
        elif len(result) == 1:
            return result[0]
        else:
            raise RuntimeError('This is unexpected')
