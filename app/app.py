from contextfreegrammar.alphabet import Symbol

x = Symbol('S', False)

class A:
    def __init__(self, l):
        self.l = l

a = A([x])
x.description = 'abcde'
pass