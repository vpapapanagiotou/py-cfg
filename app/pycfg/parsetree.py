from typing import Iterable, List, NoReturn, Optional, Self

from pycfg.symbol import Symbol
from utils.typingutils import is_list_of_instance


class TreeNode:
    symbol: Symbol
    children: List[Self]
    parent: Self
    index: Optional[int]

    def __init__(self, symbol: Symbol, children: Optional[List[Self]] = None, parent: Optional[Self] = None):
        assert isinstance(symbol, Symbol)
        assert children is None or is_list_of_instance(children, TreeNode)
        assert isinstance(parent, (type(None), TreeNode))

        self.symbol = symbol
        if children is None:
            self.children = list()
        else:
            self.children = children
        self.parent = parent

    def __str__(self) -> str:
        return str(self.symbol)

    def append_child(self, symbol: Symbol) -> NoReturn:
        self.children.append(TreeNode(symbol, parent=self))

    def append_children(self, symbols: Iterable[Symbol]) -> NoReturn:
        for symbol in symbols:
            self.append_child(symbol)


class ParseTree:
    pass


if __name__ == "__main__":
    root = TreeNode(Symbol('a'))
    root.append_children([Symbol('b1'), Symbol('b2')])
    root.children[1].append_child(Symbol('c'))
