import functools


def f(*args, **kwds):
    print(args, kwds)


g = functools.partial(f, foo=1)

print(g(foo=2, bar=3))
