import inspect


def foo(a, b, *args, r1, r2, **kwds):
    pass


def signature(function):
    parameters = inspect.signature(function).parameters.values()
