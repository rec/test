import functools


def f(*args, **kwds):
    print(args, kwds)


g = functools.partial(f, foo=1)
h = functools.partial(g, foo=2, bar=3)

h(bar=4)
