from typing import Iterable, Optional

from cfg.symbol import Symbol
from cfg.symbolstring import SymbolString


class Rule:
    frm: Symbol
    to: SymbolString
    p: Optional[float]

    def __init__(self, frm: Symbol, to: Iterable[Symbol], p: Optional[float] = None):
        assert isinstance(frm, Symbol)
        assert isinstance(to, Iterable)
        assert isinstance(p, (type(None), float))

        assert not frm.is_terminal

        self.frm = frm
        self.to = SymbolString(to)
        self.p = p

    def __eq__(self, other) -> bool:
        return isinstance(other, Rule) and self.frm == other.frm and self.to == other.to and self.p == other.p

    def __hash__(self) -> int:
        return hash(self.frm.label + ''.join(map(str, self.to)))

    def __lt__(self, other):
        return str(self) < str(other)

    def __str__(self) -> str:
        if self.p is None:
            p_str = ''
        else:
            p_str = f' (p={self.p})'
        return f'{self.frm} -> {self.to}{p_str}'
