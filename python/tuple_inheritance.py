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
