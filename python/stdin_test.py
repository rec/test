import sys


def one():
    i = 0
    for line in sys.stdin:
        i += 1

    print('end', i)


one()
