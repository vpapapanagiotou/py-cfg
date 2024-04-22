from typing import List, Set

from cfg.alphabet import Alphabet
from cfg.contextfreegrammar import ContextFreeGrammar
from cfg.rule import Rule
from cfg.symbol import Symbol


def is_in_chomsky_normal_form(cfg: ContextFreeGrammar) -> bool:
    assert isinstance(cfg, ContextFreeGrammar)

    return all(map(lambda rule: len(rule.to) == 2, cfg.rules))


def chomsky_normal_form(cfg: ContextFreeGrammar) -> ContextFreeGrammar:
    assert isinstance(cfg, ContextFreeGrammar)

    cfg = _remove_long_rules(cfg)
    cfg = _remove_e_rules(cfg)
    cfg = _remove_short_rules(cfg)

    return cfg


def _remove_long_rules(cfg: ContextFreeGrammar) -> ContextFreeGrammar:
    new_symbols: List[Symbol] = list()
    rules: List[Rule] = list(filter(lambda _rule: not _rule.is_long(), cfg.rules))

    for rule in filter(lambda _rule: _rule.is_long(), cfg.rules):
        new_rules: List[Rule] = list()

        new_frm = rule.frm
        for i in range(len(rule.to) - 2):
            to0 = rule.to[i]
            to1 = Symbol(label=f'{rule.frm}_{i}', is_terminal=False)

            new_symbols.append(to1)
            new_rules.append(Rule(new_frm, [to0, to1]))

            new_frm = to1
        new_rules.append(Rule(new_frm, rule.to[-2:]))

        if rule.p is not None:
            new_rules[0].p = rule.p
            for new_rule in new_rules[1:]:
                new_rule.p = 1

        rules.extend(new_rules)

    return ContextFreeGrammar(Alphabet(list(cfg.alphabet) + new_symbols), cfg.start_symbol, rules, fix=True)


def _erasables(cfg: ContextFreeGrammar) -> Set[Symbol]:
    previous_len: int = 0
    empty_rules = filter(lambda rule: rule.is_empty(), cfg.rules)
    erasables: Set[Symbol] = set(map(lambda rule: rule.frm, empty_rules))

    while len(erasables) != previous_len:
        previous_len = len(erasables)
        for rule in cfg.rules:
            if all(map(lambda symbol: symbol in erasables, rule.to)):
                erasables.add(rule.frm)

    return erasables


def _remove_e_rules(cfg: ContextFreeGrammar) -> ContextFreeGrammar:
    erasables = _erasables(cfg)

    new_rules: List[Rule] = list(filter(lambda _rule: not _rule.is_empty(), cfg.rules))

    for rule in filter(lambda _rule: len(_rule.to) == 2, new_rules):
        if rule.to[0] in erasables:
            new_rules.append(Rule(rule.frm, [rule.to[1]]))  # TODO define p
        if rule.to[1] in erasables:
            new_rules.append(Rule(rule.frm, [rule.to[0]]))  # TODO define p

    return ContextFreeGrammar(cfg.alphabet, cfg.start_symbol, new_rules, fix=True, ignore_duplicate_rules=True)


def _derived(cfg: ContextFreeGrammar, symbol: Symbol) -> Set[Symbol]:
    previous_len = 0
    derived: Set[Symbol] = set()
    derived.add(symbol)

    while len(derived) != previous_len:
        previous_len = len(derived)
        for rule in filter(lambda _rule: _rule.is_short(), cfg.rules):
            if rule.frm in derived:
                derived.add(rule.to[0])

    return derived


def _remove_short_rules(cfg: ContextFreeGrammar) -> ContextFreeGrammar:
    symbols = list(cfg.alphabet)
    derived_from = list(map(lambda symbol: _derived(cfg, symbol), symbols))

    new_rules_1: List[Rule] = list(filter(lambda rule: not rule.is_short(), cfg.rules))

    new_rules_2: List[Rule] = list()
    for rule in new_rules_1:
        derived0 = derived_from[symbols.index(rule.to[0])]
        derived1 = derived_from[symbols.index(rule.to[1])]
        for symbol0 in derived0:
            for symbol1 in derived1:
                new_rules_2.append(Rule(rule.frm, [symbol0, symbol1]))  # TODO define p

    return ContextFreeGrammar(
        cfg.alphabet, cfg.start_symbol, new_rules_1 + new_rules_2, fix=True, ignore_duplicate_rules=True
    )


if __name__ == "__main__":
    from cfg.example import etc_3_6_1

    cfg = etc_3_6_1()
    print(cfg.summary())

    cfg1 = _remove_long_rules(cfg)
    print(f'\nStep 1\n{cfg1.summary()}')

    cfg2 = _remove_e_rules(cfg1)
    print(f'\nStep 2\n{cfg2.summary()}')

    cfg3 = _remove_short_rules(cfg2)
    print(f'\nStep 3\n{cfg3.summary()}')

    print(list(map(is_in_chomsky_normal_form, [cfg, cfg1, cfg2, cfg3])))
