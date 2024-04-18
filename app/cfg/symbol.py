from typing import Generator, List, Optional

from cfg.utilities import is_list_of_instance, is_optional_instance


class Symbol:
    symbol: str
    is_terminal: bool
    is_non_terminal: bool
    description: Optional[str] = None

    def __init__(self, symbol: str, is_terminal: bool, description: Optional[str] = None):
        assert isinstance(symbol, str)
        assert isinstance(is_terminal, bool)
        assert is_optional_instance(description, str)

        if ' ' in symbol:
            raise ValueError('Spaces are not allowed in symbols')

        self.symbol = symbol
        self.is_terminal = is_terminal
        self.is_non_terminal = not is_terminal
        self.description = description

    def __eq__(self, other) -> bool:
        if isinstance(other, Symbol):
            return self.symbol == other.symbol
        elif isinstance(other, str):
            return self.symbol == other
        else:
            return False

    def __hash__(self) -> int:
        return hash((self.symbol, self.is_terminal))

    def __str__(self, extended: bool = False) -> str:
        return self.symbol


class SymbolString:
    def __init__(self, symbols: List[Symbol]):
        assert is_list_of_instance(symbols, Symbol)

        self.symbols: List[Symbol] = symbols

    def __eq__(self, other) -> bool:
        if isinstance(other, SymbolString):
            return self.symbols == other.symbols
        elif isinstance(other, list):
            return self.symbols == other
        else:
            return False

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
