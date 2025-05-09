from typing import Generator, Iterable, Optional, Set

from pycfg.symbol import Symbol
from utils.typingutils import is_set_of_instance


class Alphabet:
    _symbols: Set[Symbol]

    def __init__(self, symbols: Iterable[Symbol]):
        assert isinstance(symbols, Iterable)

        self._symbols = set(symbols)

        assert is_set_of_instance(self._symbols, Symbol)

    def __iter__(self) -> Generator[Symbol, None, None]:
        for symbol in self._symbols:
            yield symbol

    def __len__(self) -> int:
        return len(self._symbols)

    def __str__(self) -> str:
        return " ".join(map(str, sorted(self._symbols)))


def get_symbol_by_label(
        symbols: Iterable[Symbol], label: str, *, raise_on_not_found: Optional[bool] = True
) -> Optional[Symbol]:
    result = list(filter(lambda symbol: symbol.label == label, symbols))
    if len(result) == 0:
        if raise_on_not_found:
            raise ValueError(f'No symbol with label "{label}"')
        else:
            return None
    elif len(result) == 1:
        return result[0]
    else:
        raise RuntimeError('This is unexpected')
