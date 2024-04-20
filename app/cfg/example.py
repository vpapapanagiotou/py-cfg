from cfg.contextfreegrammar import ContextFreeGrammar
from cfg.rule import Rule
from cfg.alphabet import Alphabet
from cfg.alphabet import Symbol


def etc_3_6_1() -> ContextFreeGrammar:
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


def loup_vaillant_1() -> ContextFreeGrammar:
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


def loup_vaillant_2() -> ContextFreeGrammar:
    A = Symbol('A')
    alphabet = Alphabet([A])

    S = alphabet.get_start_symbol()
    e = alphabet.get_empty_string_symbol()

    rules = [Rule(S, [e]), Rule(S, [A]), Rule(A, [S])]

    return ContextFreeGrammar(alphabet, rules)


def lebill_1() -> ContextFreeGrammar:
    X = Symbol('X')
    a = Symbol('a')
    b = Symbol('b')
    c = Symbol('c')

    alphabet = Alphabet([X, a, b, c])
    S = alphabet.get_start_symbol()
    e = alphabet.get_empty_string_symbol()

    rules = [
        Rule(S, [a, X, c]),
        Rule(X, [b]),
        Rule(X, [e])
    ]

    return ContextFreeGrammar(alphabet, rules)
