def foo(bar):
    return bar + 2


class Foo:
    baz = staticmethod(foo)


f = Foo()
print(f.baz(10))
