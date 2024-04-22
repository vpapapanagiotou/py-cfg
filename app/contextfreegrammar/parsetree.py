from typing import List, Optional, Self

from contextfreegrammar.symbol import Symbol
from utils.typingutils import is_list_of_instance


class TreeNode:
    symbol: Symbol
    children: List[Self]
    parent: Self

    def __init__(self, symbol: Symbol, children: Optional[List[Self]] = None, parent: Optional[Self] = None):
        assert isinstance(symbol, Symbol)
        assert isinstance(children, (type(None), List)) and is_list_of_instance(children, TreeNode)
        assert isinstance(parent, (type(None), TreeNode))

        self.symbol = symbol
        if children is None:
            self.children = list()
        else:
            self.children = children
        self.parent = parent


class ParseTree:
    pass