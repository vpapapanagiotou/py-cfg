from typing import Generator, Iterable, List, Optional

from cfg.symbol import _EMPTY_STRING_SYMBOL_LABEL, _START_SYMBOL_LABEL, Symbol
from cfg.utilities import is_list_of_instance


class Alphabet:
    symbols: List[Symbol]

    def __init__(self, symbols: Iterable[Symbol]):
        assert isinstance(symbols, Iterable)

        self.symbols = list()
        self.symbols.append(Symbol(label=_START_SYMBOL_LABEL, is_terminal=False, description='The start symbol'))
        self.symbols.append(Symbol(label=_EMPTY_STRING_SYMBOL_LABEL, is_terminal=True, description='The empty string symbol'))

        for symbol in symbols:
            if symbol in self.symbols:
                raise ValueError(f'Cannot have multiple symbols with the same label (duplicate label is "{symbol}"')
            self.symbols.append(symbol)

        assert is_list_of_instance(self.symbols, Symbol)

    def __getitem__(self, item):
        return self.symbols[item]

    def __iter__(self) -> Generator[Symbol, None, None]:
        for symbol in self.symbols:
            yield symbol

    def __str__(self) -> str:
        S = self.get_start_symbol()
        e = self.get_empty_string_symbol()

        return ' '.join(map(str, [S, e] + sorted(self.symbols[2:])))

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


def alphabet_from(alphabet: Alphabet, symbols: List[Symbol]) -> Alphabet:
    return Alphabet(alphabet.symbols[2:] + symbols)
