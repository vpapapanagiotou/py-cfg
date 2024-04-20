from unittest import TestCase


class Test1(TestCase):

    def test1(self):
        x = [i for i in range(10)]
        for i in x:
            print(i)

