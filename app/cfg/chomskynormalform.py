from typing import List, Set

from cfg.example import fully_erasable
from cfg.rule import Alphabet
from cfg.contextfreegrammar import ContextFreeGrammar
from cfg.examples import Rule
from cfg.alphabet import Symbol, SymbolString


def is_in_chomsky_normal_form(cfg: ContextFreeGrammar) -> bool:
    assert isinstance(cfg, ContextFreeGrammar)

    def check1(rule: Rule) -> bool:
        """ A -> B C """
        return len(rule.to) == 2 and all(map(lambda symbol: symbol.is_non_terminal, rule.to))

    def check2(rule: Rule) -> bool:
        """ A -> a """
        return len(rule.to) == 1 and rule.to[0].is_terminal

    # There is no reason for check3, because the empty string symbol ''
    # is not treated specially. So, it falls within the scope of type 2

    def check(rule: Rule) -> bool:
        return check1(rule=rule) and check2(rule=rule)

    return all(map(check, cfg.rules))


def _cnf_long_rules(cfg: ContextFreeGrammar) -> List[Rule]:
    cnf_rules: List[Rule] = list()

    for rule in cfg.rules:
        # If rule is not long, do nothing with it
        if len(rule.to) <= 2:
            cnf_rules.append(rule)
            continue

        new_rules: List[Rule] = list()
        frm_str = str(rule.frm)
        frm = rule.frm
        for i in range(len(rule.to) - 2):
            to0 = rule.to[i]
            to1 = Symbol(symbol=f'{frm_str}_{i}', is_terminal=False)
            new_rules.append(Rule(frm, [to0, to1]))
            frm = to1
        new_rules.append(Rule(frm, rule.to[-2:]))

        if rule.p is not None:
            new_rules[0].p = rule.p
            for new_rule in new_rules[1:]:
                new_rule.p = 1

        cnf_rules.extend(new_rules)

    return cnf_rules


def _erasables(cfg: ContextFreeGrammar):
    erasables: Set[Symbol] = set()
    e = cfg.alphabet.get_empty_string_symbol()

    previous_len: int = -1
    while len(erasables) != previous_len:
        for rule in cfg.rules:
            if all(map(lambda symbol: symbol == e or symbol in erasables, rule.to)):
                erasables.add(rule.frm)
        previous_len = len(erasables)

    return erasables


if __name__ == "__main__":
    A = Symbol('A', False)
    B = Symbol('B', False)
    a = Symbol('a', True)
    b = Symbol('b', True)
    c = Symbol('c', True)
    d = Symbol('d', True)

    alphabet = Alphabet(symbols=[A, B, a, b, c, d])

    rules = [
        Rule(A, [a, b, c, d, d, a], 0.3),
        Rule(B, [a, b, c]),
        Rule(alphabet.get_start_symbol(), [A, B])
    ]

    cfg = ContextFreeGrammar(alphabet=alphabet, rules=rules)
    print(f'ContextFreeGrammar:\n{cfg}\n')

    cfg_rules = _cnf_long_rules(cfg)
    cfg_rules_str = '\n'.join(map(str, cfg_rules))
    print(f'CNF rules:\n{cfg_rules_str}\n')

    erasables = list(_erasables(fully_erasable()))
    print(f'Erasables: {SymbolString(erasables)}\n')
