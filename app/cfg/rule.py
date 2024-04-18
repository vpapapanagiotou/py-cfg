from typing import List, Optional, Union

from cfg.symbol import Symbol, SymbolString
from cfg.utilities import is_list_of_instance


class Rule:
    frm: Symbol
    to: SymbolString
    p: Optional[float] = None

    def __init__(self, frm: Symbol, to: Union[Symbol, List[Symbol], SymbolString], p: Optional[float] = None):
        assert isinstance(frm, Symbol)
        assert isinstance(to, (Symbol, SymbolString)) or is_list_of_instance(to, Symbol)

        assert frm.is_non_terminal

        to_: SymbolString
        if isinstance(to, Symbol):
            to_ = SymbolString(symbols=[to])
        elif isinstance(to, list):
            to_ = SymbolString(symbols=to)
        else:
            to_ = to

        self.frm: Symbol = frm
        self.to: SymbolString = to_
        self.p: Optional[float] = p

    def __eq__(self, other) -> bool:
        return isinstance(other, Rule) and self.frm == other.frm and self.to == other.to and self.p == other.p

    def __str__(self) -> str:
        if self.p is None:
            p_str = ''
        else:
            p_str = f' (p={self.p})'
        return f'{self.frm} -> {self.to}{p_str}'
