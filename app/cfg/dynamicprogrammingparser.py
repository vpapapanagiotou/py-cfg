import numpy as np

from cfg import example
from cfg.chomskynormalform import chomsky_normal_form, is_in_chomsky_normal_form
from cfg.contextfreegrammar import ContextFreeGrammar
from cfg.symbolstring import SymbolString


def _state_matrix(cfg: ContextFreeGrammar, string: SymbolString):
    assert is_in_chomsky_normal_form(cfg)

    n: int = len(string)

    state_matrix = np.empty([n, n], dtype=set)
    for row in range(n):
        for col in range(n):
            state_matrix[row, col] = set()

    for i in range(n):
        state_matrix[i, i].add(string[i])

    for s in range(n):
        for i in range(n - s):
            for k in range(i, i + s):
                for rule in cfg.rules:
                    if rule.to[0] in state_matrix[i, k] and rule.to[1] in state_matrix[k + 1, i + s]:
                        state_matrix[i, i + s].add(rule.frm)

    return state_matrix


class DynamicProgrammingParser:
    cfg: ContextFreeGrammar
    string: SymbolString
    _state_matrix: np.ndarray

    def __init__(self, cfg: ContextFreeGrammar, string: SymbolString):
        assert isinstance(cfg, ContextFreeGrammar)
        assert isinstance(string, SymbolString)

        self.cfg = cfg
        self.string = string
        self._state_matrix = _state_matrix(cfg, string)

    def string_in_language(self) -> bool:
        return cfg.alphabet.get_start_symbol() in self._state_matrix[0, -1]


def string_in_language(cfg: ContextFreeGrammar, string: SymbolString) -> bool:
    return DynamicProgrammingParser(cfg, string).string_in_language()


if __name__ == "__main__":
    cfg = example.example_3_6_1()
    cfg1 = chomsky_normal_form(cfg)

    lp = cfg1.alphabet.get_by_label('(')
    rp = cfg1.alphabet.get_by_label(')')
    string = SymbolString([lp, lp, rp, lp, lp, rp, rp, rp])
    print(string)

    print(string_in_language(cfg1, string))
