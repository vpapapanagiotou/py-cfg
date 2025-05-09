from typing import List, Optional
from unittest import TestCase

from pycfg import example
from pycfg.contextfreegrammar import ContextFreeGrammar
from pycfg.earleyparser import EarleyParser
from pycfg.utilities import symbol_string_from_labels


class EarleyParserTests(TestCase):
    def _check(
        self,
        cfg: ContextFreeGrammar,
        accepted: List[str],
        not_accepted: List[str],
        *,
        print_summary: Optional[bool] = False
    ):
        strings = accepted + not_accepted
        correct_in_language = [True] * len(accepted) + [False] * len(not_accepted)

        symbol_strings = list(map(lambda labels: symbol_string_from_labels(cfg.alphabet, labels), strings))
        parser = EarleyParser(cfg)

        for symbol_string, correct_in_language in zip(symbol_strings, correct_in_language):
            with self.subTest(symbol_string):
                result = parser.parse(symbol_string)
                if print_summary:
                    print(result.summary())
                self.assertEqual(result.in_language, correct_in_language)

    def test0(self):
        cfg = example.etc_3_6_1()
        accepted = ['()()']
        not_accepted = []
        self._check(cfg, accepted, not_accepted, print_summary=True)

    def test_etc361(self):
        cfg = example.etc_3_6_1()
        accepted = ['()', '(())', '((()))', '()()', '()(())', '(())(())', '(()())']
        not_accepted = ['(', ')', '(()', '())', '(())(']
        self._check(cfg, accepted, not_accepted)

    def test_lebill1(self):
        cfg = example.lebill_1()
        accepted = ['abc', 'ac']
        not_accepted = ['a', 'b', 'c', 'ab']
        self._check(cfg, accepted, not_accepted)

    def test_loup_vaillant_1(self):
        cfg = example.loup_vaillant_1()
        accepted = ['1+(2*3-4)']
        not_accepted = ['1+']
        self._check(cfg, accepted, not_accepted)

    def test_loup_vaillant_2(self):
        cfg = example.loup_vaillant_2()
        self._check(cfg, [''], [], print_summary=True)

    def test_loup_vaillant_3a(self):
        cfg = example.loup_vaillant_3a()
        self._check(cfg, ['aaaaa'], [], print_summary=True)

    def test_loup_vaillant_3b(self):
        cfg = example.loup_vaillant_3b()
        self._check(cfg, ['aaaaa'], [], print_summary=True)
