import inspect
# import xmod
import sys


# @xmod
def maina(f):
    # @functools.wraps(f)
    def wrapped(*a, **ka):
        print(f.__module__ == '__main__')
        if len(inspect.stack()) <= 2:
            return f(*sys.argv[1:])

    return wrapped


@maina
def main(*args):
    print('a', *args)


main()
