from contextfreegrammar.contextfreegrammar import context_free_grammar_from_rules, ContextFreeGrammar
from contextfreegrammar.rule import Rule
from contextfreegrammar.symbol import start_symbol, Symbol


def etc_3_6_1() -> ContextFreeGrammar:
    S = start_symbol()
    left_parenthesis = Symbol('(')
    right_parenthesis = Symbol(')')

    rules = [Rule(S, [S, S]), Rule(S, [left_parenthesis, S, right_parenthesis]), Rule(S, [])]

    return context_free_grammar_from_rules(rules)


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

    rules = [Rule(sum_symbol, [sum_symbol, plus_symbol, product_symbol]),
             Rule(sum_symbol, [sum_symbol, minus_symbol, product_symbol]), Rule(sum_symbol, [product_symbol]),
             Rule(product_symbol, [product_symbol, asterisk_symbol, factor_symbol]),
             Rule(product_symbol, [product_symbol, slash_symbol, factor_symbol]), Rule(product_symbol, [factor_symbol]),
             Rule(factor_symbol, [leftp_symbol, sum_symbol, rightp_symbol]), Rule(factor_symbol, [number_symbol]), ]
    rules.extend([Rule(number_symbol, [num_symbols[i], number_symbol]) for i in range(10)])
    rules.extend([Rule(number_symbol, [num_symbols[i]]) for i in range(10)])

    return context_free_grammar_from_rules(rules, sum_symbol.label)


def loup_vaillant_2() -> ContextFreeGrammar:
    S = start_symbol()
    A = Symbol('A')

    rules = [Rule(S, []), Rule(S, [A]), Rule(A, [S])]

    return context_free_grammar_from_rules(rules)


def lebill_1() -> ContextFreeGrammar:
    S = start_symbol()
    X = Symbol('X')
    a = Symbol('a')
    b = Symbol('b')
    c = Symbol('c')

    rules = [Rule(S, [a, X, c]), Rule(X, [b]), Rule(X, [])]

    return context_free_grammar_from_rules(rules)
