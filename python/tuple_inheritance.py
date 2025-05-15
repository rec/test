class Tuple(tuple):
    def __new__(cls, *args):
        assert len(args) == 3
        return super().__new__(cls, args)

    # This doesn't work.
    # def __init__(self, *args):
    #     assert len(args) == 3
    #     return tuple.__init__(self, args)
    # or
    #     return tuple.__init__(self, *args)


class Tuple2(tuple):
   def __init__(self, target, *matches):
       self.target = target
       super().__init__(compile(m) for m in matches)


import typing

class Tuple3(typing.NamedTuple):
    a: list[int]
    b: list[int]

    def __new__(cls, i: int):
        return super().__new__([0] * i, [1] * i)


t = Tuple3(2)
print(t, t.a, t.b)
