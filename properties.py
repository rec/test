
class Test:
    @property
    def foo(self):
        return 'foo'

    bar = 'bar'

    def __init__(self):
        self.baz = 'baz'

    def method(self=None):
        if self:
            return self.foo
        return Test.bar
