class NotIterable:
    pass


no = NotIterable()


def iterate():
    for i in no:
        print(i)


def assert_not_iterable():
    try:
        iterate()
    except TypeError as e:
        assert e.args == ("'NotIterable' object is not iterable",)
    else:
        assert False, 'Should not be iterable'


assert_not_iterable()

no.__iter__ = lambda: iter(range(3))
assert_not_iterable()

NotIterable.__iter__ = lambda self: iter(range(3))
iterate()
