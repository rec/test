import functools

if False:
    @functools.lru_cache()
    def foo():
        print('here!')
        return 1


    print(foo())
    print(foo())


    @functools.lru_cache()
    def bar(test=None):
        print('bar!', test)
        return (2, test)


    print(bar())
    print(bar(1))
    print(bar())
    print(bar(1))


@functools.lru_cache()
class Baz:
    def __init__(self, a=None):
        print('baz', a)

    @property
    @functools.lru_cache()
    def foo(self):
        print('foo!')
        return 1

# print(Baz())
# print(Baz(1))
# print(Baz())
# print(Baz(1))

baz = Baz()
print(baz.foo)
print(baz.foo)
print(Baz(1).foo)
print(Baz(1).foo)
