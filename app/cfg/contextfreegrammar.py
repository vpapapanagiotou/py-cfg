from typing import List

from cfg.alphabet import Alphabet
from cfg.rule import Rule
from cfg.symbol import Symbol, SymbolString
from cfg.utilities import is_list_of_instance


class ContextFreeGrammar:
    symbols: List[Symbol]
    rules: List[Rule]

    def __init__(self, alphabet: Alphabet, rules: List[Rule]):
        assert isinstance(alphabet, Alphabet)
        assert is_list_of_instance(rules, Rule)

        self.alphabet: Alphabet = alphabet
        self.rules: List[Rule] = rules

    def __str__(self):
        rules_str = "\n".join(map(str, self.rules))
        return f'{self.alphabet}\n{rules_str}'


if __name__ == "__main__":
    A = Symbol('A', False)
    B = Symbol('B', False)
    a = Symbol('a', True)
    b = Symbol('b', True)
    symbols = [A, B, a, b]

    ss = SymbolString([A, a, b])
    print(ss == ss, ss == SymbolString([A, a]), ss == SymbolString([A, a, b]), ss == [A, a], ss == [A, a, 'b'])

    alphabet = Alphabet(symbols=symbols)

    rules = [
        Rule(A, [B, A]),
        Rule(A, [a, B]),
        Rule(B, b),
        Rule(B, b)
    ]

    cfg = ContextFreeGrammar(alphabet=alphabet, rules=rules)
    print(cfg)
