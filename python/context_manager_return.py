from contextlib import contextmanager


@contextmanager
def c():
    try:
        yield
    except ValueError:
        pass


def fail():
    raise ValueError()


with c():
    a = fail()

print('here')
