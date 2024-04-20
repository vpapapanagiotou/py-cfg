from typing import Generator, Iterable, List

from cfg.symbol import Symbol
from cfg.utilities import is_list_of_instance


class SymbolString:
    symbols: List[Symbol]

    def __init__(self, symbols: Iterable[Symbol]):
        assert isinstance(symbols, Iterable)

        self.symbols = list(symbols)

        assert is_list_of_instance(self.symbols, Symbol)

    def __eq__(self, other) -> bool:
        return isinstance(other, SymbolString) and self.symbols == other.symbols

    def __getitem__(self, item) -> Symbol:
        return self.symbols[item]

    def __iter__(self) -> Generator[Symbol, None, None]:
        for symbol in self.symbols:
            yield symbol

    def __len__(self) -> int:
        return len(self.symbols)

    def __str__(self) -> str:
        return " ".join(map(str, self.symbols))

    def is_terminal(self) -> bool:
        return all(map(lambda symbol: symbol.is_terminal, self.symbols))

    def is_non_terminal(self) -> bool:
        return all(map(lambda symbol: not symbol.is_terminal, self.symbols))
