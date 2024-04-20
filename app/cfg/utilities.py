from typing import Iterable, List, Optional

from cfg.alphabet import Alphabet
from cfg.symbolstring import SymbolString


def symbol_string_from_labels(alphabet: Alphabet, labels: Iterable[str]) -> SymbolString:
    assert isinstance(alphabet, Alphabet)
    assert isinstance(labels, Iterable)

    return SymbolString(map(lambda label: alphabet.get_by_label(label), labels))


def symbol_string_from_str(alphabet: Alphabet, s: str, *, split: Optional[str] = None):
    if split is None:
        labels = [*s]
    else:
        labels = s.split(split)

    return symbol_string_from_labels(alphabet, labels)
