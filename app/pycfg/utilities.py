from typing import Iterable, Iterator, List, Optional, Set

from pycfg.alphabet import Alphabet, get_symbol_by_label
from pycfg.contextfreegrammar import ContextFreeGrammar
from pycfg.rule import Rule
from pycfg.symbol import Symbol
from pycfg.symbolstring import SymbolString


def symbol_string_from_labels(alphabet: Alphabet, labels: Iterable[str]) -> SymbolString:
    return SymbolString(map(lambda label: get_symbol_by_label(alphabet, label), labels))


def symbol_string_from_str(alphabet: Alphabet, s: str, *, split: Optional[str] = None):
    if split is None:
        labels = [*s]
    else:
        labels = s.split(split)

    return symbol_string_from_labels(alphabet, labels)


def erasables_set(rules: Iterable[Rule]) -> Set[Symbol]:
    if isinstance(rules, Iterator):
        rules = list(rules)

    previous_len: int = 0
    empty_rules = filter(lambda rule: rule.is_empty(), rules)
    erasables: Set[Symbol] = set(map(lambda rule: rule.frm, empty_rules))

    while len(erasables) != previous_len:
        previous_len = len(erasables)
        for rule in rules:
            if all(map(lambda symbol: symbol in erasables, rule.to)):
                erasables.add(rule.frm)

    return erasables
