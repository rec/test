foo = 1
bar = 2
baz = 3

def __dir__():
    return 'foo', 'bar'

__all__ = 'foo', 'bar'
