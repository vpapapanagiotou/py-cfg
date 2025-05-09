import numpy as np

from pycfg.alphabet import get_symbol_by_label
from pycfg.chomskynormalform import chomsky_normal_form, is_in_chomsky_normal_form
from pycfg.contextfreegrammar import ContextFreeGrammar
from pycfg.symbol import Symbol
from pycfg.symbolstring import SymbolString


def _state_matrix(cfg: ContextFreeGrammar, string: SymbolString) -> np.ndarray:
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


class DynamicProgrammingParserResult:
    _state_matrix: np.ndarray
    in_language: bool

    def __init__(self, _state_matrix: np.ndarray, start_symbol: Symbol):
        self._state_matrix = _state_matrix

        self.in_language = start_symbol in _state_matrix[0, -1]


class DynamicProgrammingParser:
    cfg: ContextFreeGrammar

    def __init__(self, cfg: ContextFreeGrammar):
        assert isinstance(cfg, ContextFreeGrammar)

        if is_in_chomsky_normal_form(cfg):
            self.cfg = cfg
        else:
            self.cfg = chomsky_normal_form(cfg)

    def parse(self, string: SymbolString) -> DynamicProgrammingParserResult:
        assert isinstance(string, SymbolString)

        state_matrix = _state_matrix(self.cfg, string)
        return DynamicProgrammingParserResult(state_matrix, self.cfg.start_symbol)


if __name__ == "__main__":
    from pycfg.example import etc_3_6_1

    cfg = etc_3_6_1()
    cfg1 = chomsky_normal_form(cfg)

    lp = get_symbol_by_label(cfg1.alphabet, '(')
    rp = get_symbol_by_label(cfg1.alphabet, ')')
    string = SymbolString([lp, lp, rp, lp, lp, rp, rp, rp])
    print(string)

    print(DynamicProgrammingParser(cfg1).parse(string).in_language)
