class Foo(object):
    class Bar(object):
        def __init__(self, a):
            self.a = a

bar = Foo.Bar(1)
