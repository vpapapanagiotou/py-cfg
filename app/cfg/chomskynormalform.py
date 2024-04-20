from typing import List, Set

from cfg.alphabet import alphabet_from
from cfg.contextfreegrammar import ContextFreeGrammar
from cfg.example import example_3_6_1
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
    new_rules: List[Rule] = list()

    for rule in cfg.rules:
        # If rule is not long, do nothing with it
        if len(rule.to) <= 2:
            new_rules.append(rule)
            continue

        rules1: List[Rule] = list()
        frm_str = str(rule.frm)
        frm = rule.frm
        for i in range(len(rule.to) - 2):
            to0 = rule.to[i]
            to1 = Symbol(label=f'{frm_str}_{i}', is_terminal=False)

            new_symbols.append(to1)
            rules1.append(Rule(frm, [to0, to1]))

            frm = to1
        rules1.append(Rule(frm, rule.to[-2:]))

        if rule.p is not None:
            rules1[0].p = rule.p
            for new_rule in rules1[1:]:
                new_rule.p = 1

        new_rules.extend(rules1)

    return ContextFreeGrammar(alphabet_from(cfg.alphabet, new_symbols), new_rules, fix=True)


def _erasables(cfg: ContextFreeGrammar) -> Set[Symbol]:
    erasables: Set[Symbol] = set()
    erasables.add(cfg.alphabet.get_empty_string_symbol())

    previous_len: int = -1
    while len(erasables) != previous_len:
        for rule in cfg.rules:
            if all(map(lambda symbol: symbol in erasables, rule.to)):
                erasables.add(rule.frm)
        previous_len = len(erasables)

    return erasables


def _remove_e_rules(cfg: ContextFreeGrammar) -> ContextFreeGrammar:
    e = cfg.alphabet.get_empty_string_symbol()

    erasables = _erasables(cfg)

    new_rules: List[Rule] = list()
    for rule in cfg.rules:
        if rule.to != [e]:
            new_rules.append(rule)
        if len(rule.to) == 2:
            if rule.to[0] in erasables:
                new_rules.append(Rule(frm=rule.frm, to=[rule.to[1]]))  # TODO define p
            if rule.to[1] in erasables:
                new_rules.append(Rule(frm=rule.frm, to=[rule.to[0]]))  # TODO define p

    return ContextFreeGrammar(cfg.alphabet, cfg.rules + new_rules, fix=True)


def _derived(cfg: ContextFreeGrammar, symbol: Symbol) -> Set[Symbol]:
    derived: Set[Symbol] = set()
    derived.add(symbol)

    previous_len = -1
    while len(derived) != previous_len:
        for rule in cfg.rules:
            if len(rule.to) != 1:
                continue
            if rule.frm in derived:
                derived.add(rule.to[0])
        previous_len = len(derived)

    return derived


def _remove_short_rules(cfg: ContextFreeGrammar) -> ContextFreeGrammar:
    derived = list(map(lambda symbol: _derived(cfg, symbol), cfg.alphabet))

    rules1: List[Rule] = list(filter(lambda rule: len(rule.to) == 2, cfg.rules))

    rules2: List[Rule] = list()
    for rule in rules1:
        derived0 = derived[cfg.alphabet.symbols.index(rule.to[0])]
        derived1 = derived[cfg.alphabet.symbols.index(rule.to[1])]
        for symbol0 in derived0:
            for symbol1 in derived1:
                rules2.append(Rule(frm=rule.frm, to=[symbol0, symbol1]))  # TODO define p

    return ContextFreeGrammar(cfg.alphabet, rules1 + rules2, fix=True)


if __name__ == "__main__":
    cfg = example_3_6_1()
    print(cfg)

    cfg1 = _remove_long_rules(cfg)
    print(f'\nStep 1\n{cfg1}')

    cfg2 = _remove_e_rules(cfg1)
    print(f'\nStep 2\n{cfg2}')

    cfg3 = _remove_short_rules(cfg2)
    print(f'\nStep 3\n{cfg3}')

    print(list(map(is_in_chomsky_normal_form, [cfg, cfg1, cfg2, cfg3])))
