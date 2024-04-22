from typing import List
from unittest import TestCase

from contextfreegrammar import example
from contextfreegrammar.contextfreegrammar import ContextFreeGrammar
from contextfreegrammar.dynamicprogrammingparser import DynamicProgrammingParser
from contextfreegrammar.utilities import symbol_string_from_labels


class DynamicProgrammingParserTests(TestCase):
    def _check(self, cfg: ContextFreeGrammar, accepted: List[str], not_accepted: List[str]):
        strings = accepted + not_accepted
        correct_in_language = [True] * len(accepted) + [False] * len(not_accepted)

        symbol_strings = list(map(lambda labels: symbol_string_from_labels(cfg.alphabet, labels), strings))
        parser = DynamicProgrammingParser(cfg)

        for symbol_string, correct_in_language in zip(symbol_strings, correct_in_language):
            with self.subTest(symbol_string):
                self.assertEqual(parser.parse(symbol_string).in_language, correct_in_language)

    def test1(self):
        cfg = example.etc_3_6_1()
        accepted = ['()', '(())', '((()))', '()()', '()(())', '(())(())', '(()())']
        not_accepted = ['(', ')', '(()', '())', '(())(']
        self._check(cfg, accepted, not_accepted)

    def test2(self):
        cfg = example.lebill_1()
        accepted = ['abc', 'ac']
        not_accepted = ['a', 'b', 'c', 'ab']
        self._check(cfg, accepted, not_accepted)
