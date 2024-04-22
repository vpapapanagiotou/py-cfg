from itertools import chain
from typing import Iterable, List, NoReturn, Optional

from cfg.alphabet import Alphabet, get_symbol_by_label
from cfg.rule import Rule
from cfg.symbol import _START_SYMBOL_LABEL, Symbol
from cfg.symbolstring import SymbolString
from utils.typingutils import is_list_of_instance


class ContextFreeGrammar:
    alphabet: Alphabet
    start_symbol: Symbol
    rules: List[Rule]

    def __init__(
        self,
        alphabet: Alphabet,
        start_symbol: Symbol,
        rules: Iterable[Rule],
        *,
        fix: Optional[bool] = False,
        ignore_duplicate_rules: Optional[bool] = False
    ):
        assert isinstance(alphabet, Alphabet)
        assert isinstance(start_symbol, Symbol)
        assert isinstance(rules, Iterable)

        self.alphabet = alphabet
        self.start_symbol = start_symbol
        self.rules = list()

        for rule in rules:
            if rule not in self.rules:
                self.rules.append(rule)
            else:
                if not ignore_duplicate_rules:
                    raise ValueError(f'Duplicate rule: {rule}')
        assert is_list_of_instance(rules, Rule)

        if fix:
            self.fix()

    def __str__(self) -> str:
        V_str = f'V={{{self.alphabet}}}'
        Sigma_str = f'Σ={{{SymbolString(filter(lambda symbol: symbol.is_terminal, self.alphabet))}}}'
        S_str = f'S={self.start_symbol}'
        rules_str = ', '.join(map(str, self.rules))
        R_str = f'R={{{rules_str}}}'

        return f'{V_str}, {Sigma_str}, {S_str}, {R_str}'

    def fix(self) -> NoReturn:
        self.rules = list(set(self.rules))
        # self.rules = sorted(self.rules)
        self.rules = list(filter(lambda rule: SymbolString([rule.frm]) != rule.to, self.rules))

    def summary(self) -> str:
        V_str = f'V={{{self.alphabet}}}'
        Sigma_str = f'Σ={{{SymbolString(filter(lambda symbol: symbol.is_terminal, self.alphabet))}}}'
        S_str = f'S={self.start_symbol}'
        rules_str = '\n'.join(map(lambda rule: f'  {rule}', self.rules))
        R_str = f'R={{\n{rules_str}\n}}'

        return f'{V_str}\n{Sigma_str}\n{S_str}\n{R_str}'


def context_free_grammar_from_rules(
    rules: List[Rule], start_symbol_label: str = _START_SYMBOL_LABEL
) -> ContextFreeGrammar:
    symbols = chain.from_iterable(map(lambda rule: [rule.frm] + list(rule.to), rules))
    alphabet = Alphabet(symbols)
    start_symbol = get_symbol_by_label(alphabet, _START_SYMBOL_LABEL)

    return ContextFreeGrammar(alphabet, start_symbol, rules)


if __name__ == "__main__":
    S = Symbol('S')
    A = Symbol('A')
    B = Symbol('B')
    a = Symbol('a')
    b = Symbol('b')
    symbols = [A, B, a, b]

    ss = SymbolString([A, a, b])
    print(ss == ss, ss == SymbolString([A, a]), ss == SymbolString([A, a, b]), ss == [A, a], ss == [A, a, 'b'])

    alphabet = Alphabet(symbols)

    rules = [Rule(A, [B, A]), Rule(A, [a, B]), Rule(B, [b]), Rule(B, [a])]
    rules.sort()

    cfg = ContextFreeGrammar(alphabet, S, rules)
    print(cfg.summary())
