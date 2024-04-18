from cfg.contextfreegrammar import ContextFreeGrammar
from cfg.rule import Rule
from cfg.alphabet import Alphabet
from cfg.alphabet import Symbol


def toy_cfg() -> ContextFreeGrammar:
    A = Symbol(label='A', is_terminal=False)
    a = Symbol(label='a', is_terminal=True)
    b = Symbol(label='b', is_terminal=True)

    alphabet = Alphabet(symbols=[A, a, b])

    rules = [Rule(alphabet.get_start_symbol(), A), Rule(A, a), Rule(A, b)]

    return ContextFreeGrammar(alphabet=alphabet, rules=rules)


def parenthesis() -> ContextFreeGrammar:
    left_bracket = Symbol(label='(', is_terminal=True)
    right_bracket = Symbol(label=')', is_terminal=True)

    alphabet = Alphabet(symbols=[left_bracket, right_bracket])
    S = alphabet.get_start_symbol()

    rules = [
        Rule(S, [left_bracket, S, right_bracket]),
        Rule(S, [S, S]),
        Rule(S, alphabet.get_empty_string_symbol())
    ]

    return ContextFreeGrammar(alphabet=alphabet, rules=rules)


def fully_erasable() -> ContextFreeGrammar:
    A = Symbol(label='A', is_terminal=False)
    B = Symbol(label='B', is_terminal=False)

    alphabet = Alphabet(symbols=[A, B])
    S = alphabet.get_start_symbol()
    e = alphabet.get_empty_string_symbol()

    rules = [
        Rule(S, [A, B]),
        Rule(S, A),
        Rule(A, e),
        Rule(S, B),
        Rule(B, S),
        Rule(B, A)
    ]

    return ContextFreeGrammar(alphabet=alphabet, rules=rules)
