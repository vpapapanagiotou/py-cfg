from typing import Iterable, List, Optional

from contextfreegrammar.alphabet import Alphabet, get_symbol_by_label
from contextfreegrammar.symbolstring import SymbolString


def symbol_string_from_labels(alphabet: Alphabet, labels: Iterable[str]) -> SymbolString:
    return SymbolString(map(lambda label: get_symbol_by_label(alphabet, label), labels))


def symbol_string_from_str(alphabet: Alphabet, s: str, *, split: Optional[str] = None):
    if split is None:
        labels = [*s]
    else:
        labels = s.split(split)

    return symbol_string_from_labels(alphabet, labels)
