import contextlib


def test():
    yield 2
    yield from range(4)
    yield from zip(range(3), range(3))


@contextlib.contextmanager
def test2():
    for i in range(4):
        try:
            yield i
        except:
            print('exception', i)
        else:
            print('no exception', i)


def test3():
    with test2() as i:
        if i in (0, 3):
            raise ValueError


# print(list(test()))
test3()
