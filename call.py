class Call:
    def __init__(self):
        self.__setattr__ = print


class Call2:
    def __setattr__(self, k, v):
        print(k, v)


c = Call()
c.foo = 'bar'

c2 = Call2()
c2.foo2 = 'bar2'
