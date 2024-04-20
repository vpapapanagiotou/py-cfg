from typing import Optional

_START_SYMBOL_LABEL: str = 'S'
_EMPTY_STRING_SYMBOL_LABEL: str = 'e'


class Symbol:
    label: str
    is_terminal: bool
    description: Optional[str]

    def __init__(self, label: str, is_terminal: Optional[bool] = None, description: Optional[str] = None):
        assert isinstance(label, str)
        assert isinstance(is_terminal, (type(None), bool))
        assert isinstance(description, (type(None), str))

        assert ' ' not in label, 'Spaces are not allowed in symbols'

        if is_terminal is None:
            is_terminal = label == label.lower()

        self.label = label
        self.is_terminal = is_terminal
        self.description = description

    def __eq__(self, other) -> bool:
        return isinstance(other, Symbol) and self.label == other.label and self.is_terminal == other.is_terminal

    def __hash__(self) -> int:
        return hash((self.label, self.is_terminal))

    def __lt__(self, other) -> bool:
        return self.label < other.label

    def __str__(self, extended: bool = False) -> str:
        return self.label
