from typing import Generator, Iterable, List, NoReturn

from cfg.symbol import Symbol
from utils.typingutils import is_list_of_instance


class SymbolString:
    _symbols: List[Symbol]

    def __init__(self, symbols: Iterable[Symbol]):
        assert isinstance(symbols, Iterable)

        self._symbols = list(symbols)

        assert is_list_of_instance(self._symbols, Symbol)

    def __eq__(self, other) -> bool:
        return isinstance(other, SymbolString) and self._symbols == other._symbols

    def __getitem__(self, item) -> Symbol:
        return self._symbols[item]

    def __iter__(self) -> Generator[Symbol, None, None]:
        for symbol in self._symbols:
            yield symbol

    def __len__(self) -> int:
        return len(self._symbols)

    def __str__(self) -> str:
        return " ".join(map(str, self._symbols))

    def insert(self, i: int, symbol: Symbol) -> NoReturn:
        self._symbols.insert(i, symbol)

    def is_terminal(self) -> bool:
        return all(map(lambda symbol: symbol.is_terminal, self._symbols))
