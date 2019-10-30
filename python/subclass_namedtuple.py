from collections import namedtuple


class Child(namedtuple('Child', 'a b c')):
    def __init__(self, a, b, c):
        super().__init__(a=b, b=c, c=a)
