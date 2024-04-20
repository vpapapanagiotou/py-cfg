from typing import List
from unittest import TestCase

from cfg import example
from cfg.contextfreegrammar import ContextFreeGrammar
from cfg.earleyparser import EarleyParser
from cfg.utilities import symbol_string_from_labels


class EarleyParserTests(TestCase):
    def _check(self, cfg: ContextFreeGrammar, accepted: List[str], not_accepted: List[str]):
        strings = accepted + not_accepted
        correct_in_language = [True] * len(accepted) + [False] * len(not_accepted)

        symbol_strings = list(map(lambda labels: symbol_string_from_labels(cfg.alphabet, labels), strings))
        parser = EarleyParser(cfg)

        for symbol_string, correct_in_language in zip(symbol_strings, correct_in_language):
            with self.subTest(symbol_string):
                self.assertEqual(parser.parse(symbol_string).in_language, correct_in_language)

    def test1(self):
            cfg = example.loup_vaillant_1()
            accepted = ['1+(2*3-4)']
            not_accepted = ['1+']
            self._check(cfg, accepted, not_accepted)
