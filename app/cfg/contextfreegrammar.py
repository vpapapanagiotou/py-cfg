from typing import Iterable, List, NoReturn, Optional

from cfg.alphabet import Alphabet
from cfg.rule import Rule
from cfg.symbol import Symbol
from cfg.symbolstring import SymbolString
from utils.typingutils import is_list_of_instance


class ContextFreeGrammar:
    alphabet: Alphabet
    rules: List[Rule]

    def __init__(self, alphabet: Alphabet, rules: Iterable[Rule], *, fix: Optional[bool] = False):
        assert isinstance(alphabet, Alphabet)
        assert isinstance(rules, Iterable)

        self.alphabet = alphabet
        self.rules = list(rules)

        assert is_list_of_instance(rules, Rule)

        if fix:
            self.fix()

    def __str__(self) -> str:
        V_str = f'V={{{self.alphabet}}}'
        Sigma_str = f'Σ={{{SymbolString(filter(lambda symbol: symbol.is_terminal, self.alphabet))}}}'
        S_str = f'S={self.alphabet.get_start_symbol()}'
        rules_str = ', '.join(map(str, self.rules))
        R_str = f'R={{{rules_str}}}'

        return f'{V_str}, {Sigma_str}, {S_str}, {R_str}'

    def fix(self) -> NoReturn:
        self.alphabet.symbols = self.alphabet.symbols[:2] + sorted(self.alphabet.symbols[2:])
        self.rules = sorted(list(set(self.rules)))
        self.rules = list(filter(lambda rule: SymbolString([rule.frm]) != rule.to, self.rules))


if __name__ == "__main__":
    A = Symbol('A', False)
    B = Symbol('B', False)
    a = Symbol('a', True)
    b = Symbol('b', True)
    symbols = [A, B, a, b]

    ss = SymbolString([A, a, b])
    print(ss == ss, ss == SymbolString([A, a]), ss == SymbolString([A, a, b]), ss == [A, a], ss == [A, a, 'b'])

    alphabet = Alphabet(symbols=symbols)

    rules = [Rule(A, [B, A]), Rule(A, [a, B]), Rule(B, [b]), Rule(B, [a])]
    rules.sort()

    cfg = ContextFreeGrammar(alphabet=alphabet, rules=rules)
    print(cfg)
