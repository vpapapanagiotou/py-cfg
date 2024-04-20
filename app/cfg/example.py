from cfg.contextfreegrammar import ContextFreeGrammar
from cfg.rule import Rule
from cfg.alphabet import Alphabet
from cfg.alphabet import Symbol


def toy_cfg() -> ContextFreeGrammar:
    A = Symbol('A')
    a = Symbol('a')
    b = Symbol('b')

    alphabet = Alphabet(symbols=[A, a, b])

    rules = [
        Rule(alphabet.get_start_symbol(), [A]),
        Rule(A, [a]),
        Rule(A, [b])
    ]

    return ContextFreeGrammar(alphabet, rules)


def parenthesis() -> ContextFreeGrammar:
    left_bracket = Symbol('(', True)
    right_bracket = Symbol(')', True)

    alphabet = Alphabet([left_bracket, right_bracket])
    S = alphabet.get_start_symbol()

    rules = [
        Rule(S, [left_bracket, S, right_bracket]),
        Rule(S, [S, S]),
        Rule(S, [alphabet.get_empty_string_symbol()])
    ]

    return ContextFreeGrammar(alphabet=alphabet, rules=rules)


def fully_erasable() -> ContextFreeGrammar:
    A = Symbol('A', False)
    B = Symbol('B', False)

    alphabet = Alphabet([A, B])
    S = alphabet.get_start_symbol()
    e = alphabet.get_empty_string_symbol()

    rules = [
        Rule(S, [A, B]),
        Rule(S, [A]),
        Rule(A, [e]),
        Rule(S, [B]),
        Rule(B, [S]),
        Rule(B, [A])
    ]

    return ContextFreeGrammar(alphabet, rules)


def partially_erasable() -> ContextFreeGrammar:
    A = Symbol('A', False)
    B = Symbol('B', False)
    C = Symbol('B', False)
    c = Symbol('c', True)

    alphabet = Alphabet([A, B])
    S = alphabet.get_start_symbol()
    e = alphabet.get_empty_string_symbol()

    rules = [
        Rule(S, [A, B]),
        Rule(S, [A]),
        Rule(A, [e]),
        Rule(S, [B]),
        Rule(B, [S]),
        Rule(B, [A]),
        Rule(A, [c]),
        Rule(B, [C]),
        Rule(C, [c])
    ]

    return ContextFreeGrammar(alphabet, rules)


def example_3_6_1() -> ContextFreeGrammar:
    left_parenthesis = Symbol('(')
    right_parenthesis = Symbol(')')

    alphabet = Alphabet([left_parenthesis, right_parenthesis])
    S = alphabet.get_start_symbol()
    e = alphabet.get_empty_string_symbol()

    rules = [
        Rule(S, [S, S]),
        Rule(S, [left_parenthesis, S, right_parenthesis]),
        Rule(S, [e])
    ]

    return ContextFreeGrammar(alphabet, rules)


def loup_vaillant() -> ContextFreeGrammar:
    sum_symbol = Symbol('Sum')
    product_symbol = Symbol('Product')
    factor_symbol = Symbol('Factor')
    number_symbol = Symbol('Number')
    leftp_symbol = Symbol('(')
    rightp_symbol = Symbol(')')
    plus_symbol = Symbol('+')
    minus_symbol = Symbol('-')
    asterisk_symbol = Symbol('*')
    slash_symbol = Symbol('/')
    num_symbols = [Symbol(str(i)) for i in range(10)]

    alphabet = Alphabet([
        sum_symbol, product_symbol, factor_symbol, number_symbol, leftp_symbol, rightp_symbol,
        plus_symbol, minus_symbol, asterisk_symbol, slash_symbol
    ] + num_symbols)

    rules = [
        Rule(alphabet.get_start_symbol(), [sum_symbol]),
        Rule(sum_symbol, [sum_symbol, plus_symbol, product_symbol]),
        Rule(sum_symbol, [sum_symbol, minus_symbol, product_symbol]),
        Rule(sum_symbol, [product_symbol]),
        Rule(product_symbol, [product_symbol, asterisk_symbol, factor_symbol]),
        Rule(product_symbol, [product_symbol, slash_symbol, factor_symbol]),
        Rule(product_symbol, [factor_symbol]),
        Rule(factor_symbol, [leftp_symbol, sum_symbol, rightp_symbol]),
        Rule(factor_symbol, [number_symbol]),
    ]
    rules.extend([Rule(number_symbol, [num_symbols[i], number_symbol]) for i in range(10)])
    rules.extend([Rule(number_symbol, [num_symbols[i]]) for i in range(10)])

    return ContextFreeGrammar(alphabet, rules)
