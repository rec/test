import contextlib

@contextlib.contextmanager
def test_context():
    print('a')
    yield
    print('b')


def run_context(c):
    print('one')
    with c:
        print('two')
        yield
        print('three')
    print('four')


def test_it():
    print('U')
    tc = run_context(test_context())
    print('V')
    next(tc)
    print('W')
    try:
        next(tc)
    except StopIteration:
        print('X')
    else:
        print('Y!!!')

test_it()
