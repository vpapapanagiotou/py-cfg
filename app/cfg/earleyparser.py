from typing import Generator, List, NoReturn, Optional

from cfg import example
from cfg.contextfreegrammar import ContextFreeGrammar
from cfg.rule import Rule
from cfg.symbol import Symbol
from cfg.symbolstring import SymbolString
from cfg.utilities import symbol_string_from_str

_DOT = '•'


def _special_fmt_1(string: SymbolString, i: int) -> str:
    labels = list(map(str, string))
    labels.insert(i, _DOT)

    return ' '.join(map(str, labels))


def _special_fmt_2(strings: List[str]) -> List[str]:
    n = max(map(len, strings))

    return list(map(lambda s: s.ljust(n), strings))


class EarleyItem:
    rule: Rule
    start: int
    i: int

    def __init__(self, rule: Rule, start: int = 0, i: int = 0):
        self.rule = rule
        self.start = start
        self.i = i

    def __eq__(self, other) -> bool:
        return isinstance(
            other, EarleyItem
        ) and self.rule == other.rule and self.start == other.start and self.i == other.i

    def __hash__(self) -> int:
        return hash((self.rule, self.start, self.i))

    def __str__(self) -> str:
        return f'{self.rule.frm} -> {_special_fmt_1(self.rule.to, self.i)}  S({self.start})'

    def is_complete(self) -> bool:
        return self.i == len(self.rule.to)

    def next_symbol(self) -> Optional[Symbol]:
        if self.i < len(self.rule.to):
            return self.rule.to[self.i]
        else:
            return None


class EarleyItemSet:
    earley_items: List[EarleyItem]

    def __init__(self):
        self.earley_items = list()

    def __getitem__(self, item) -> EarleyItem:
        return self.earley_items[item]

    def __iter__(self) -> Generator[EarleyItem, None, None]:
        for earley_item in self.earley_items:
            yield earley_item

    def __len__(self) -> int:
        return len(self.earley_items)

    def __str__(self) -> str:
        return ', '.join(map(str, self))

    def add(self, earley_item: EarleyItem) -> NoReturn:
        if earley_item not in self.earley_items:
            self.earley_items.append(earley_item)

    def add_many(self, earley_items: List[EarleyItem]) -> NoReturn:
        for earley_item in earley_items:
            self.add(earley_item)

    def summary(self) -> str:
        if len(self) == 0:
            return ""

        part_1 = list(map(lambda earley_item: earley_item.rule.frm, self.earley_items))
        part_1 = _special_fmt_2(list(map(str, part_1)))

        part_2 = list(map(lambda earley_item: _special_fmt_1(earley_item.rule.to, earley_item.i), self.earley_items))
        part_2 = _special_fmt_2(part_2)

        part_3 = list(map(lambda earley_item: f'S({earley_item.start})', self.earley_items))

        return '\n'.join(map(lambda t: f'{t[0]} -> {t[1]}   {t[2]}', zip(part_1, part_2, part_3)))


def _predict(rules: List[Rule], next_symbol: Symbol, state_idx: int) -> List[EarleyItem]:
    assert not next_symbol.is_terminal  # Optional check

    new_states: List[EarleyItem] = list()

    for rule in rules:
        if rule.frm == next_symbol:
            new_states.append(EarleyItem(rule, state_idx))

    return new_states


def _scan(rules: List[Rule], state: EarleyItem, next_symbol: Symbol) -> List[EarleyItem]:
    assert state.next_symbol().is_terminal  # Optional check

    new_states: List[EarleyItem] = list()

    if state.next_symbol() == next_symbol:
        new_states.append(EarleyItem(state.rule, state.start, state.i + 1))

    return new_states


def _complete(state_set: EarleyItemSet, symbol: Symbol) -> List[EarleyItem]:
    assert not symbol.is_terminal  # Optional check

    new_rules: List[EarleyItem] = list()

    for state in state_set:
        if state.next_symbol() == symbol:
            new_rules.append(EarleyItem(state.rule, state.start, state.i + 1))

    return new_rules


def _earley_parse(cfg: ContextFreeGrammar, string: SymbolString):
    n: int = len(string)

    state_sets: List[EarleyItemSet] = list()
    for i in range(n + 1):
        state_sets.append(EarleyItemSet())

    for rule in cfg.rules:
        if rule.frm == cfg.alphabet.get_start_symbol():
            state_sets[0].add(EarleyItem(rule))

    for state_set_idx, state_set in enumerate(state_sets[:-1]):
        for state in state_set:
            next_symbol = state.next_symbol()
            if next_symbol is None:
                state_set.add_many(_complete(state_sets[state.start], state.rule.frm))
            elif next_symbol.is_terminal:
                state_sets[state_set_idx + 1].add_many(_scan(cfg.rules, state, string[state_set_idx]))
            elif not next_symbol.is_terminal:
                state_set.add_many(_predict(cfg.rules, state.next_symbol(), state_set_idx))
            else:
                raise RuntimeError('This is unexpected')

    state_set_idx = len(state_sets) - 1
    state_set = state_sets[state_set_idx]
    for state in state_set:
        next_symbol = state.next_symbol()
        if next_symbol is None:
            state_set.add_many(_complete(state_sets[state.start], state.rule.frm))
        elif next_symbol.is_terminal:
            pass # state_sets[state_set_idx + 1].add_many(_scan(cfg.rules, state, string[state_set_idx]))
        elif not next_symbol.is_terminal:
            pass  # state_set.add_many(_predict(cfg.rules, state.next_symbol(), state_set_idx))
        else:
            raise RuntimeError('This is unexpected')

    print(print_state_sets(state_sets))


def print_state_sets(state_sets: List[EarleyItemSet]) -> NoReturn:
    for i, state_set in enumerate(state_sets):
         print(f'=== {i} ===\n{state_set.summary()}\n\n')


if __name__ == '__main__':
    cfg: ContextFreeGrammar = example.loup_vaillant()
    string: SymbolString = symbol_string_from_str(cfg.alphabet, '1+(2*3-4)')

    _earley_parse(cfg, string)

    pass
