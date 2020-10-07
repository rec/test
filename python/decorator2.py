import functools

def print_before(label='DEBUG:'):

    def decorator(func):

        @functools.wraps(func)
        def wrapped(*args, **kwds):
            print(label, func.__name__, args, kwds)
            return func(*args, **kwds)

        return wrapped

    return decorator


@print_before()
def foo(bar, baz):
    return bar, baz


@print_before
def bing(bar, baz):
    return bar, baz


foo(1, 2)
bing(2, 3)
