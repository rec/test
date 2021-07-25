import traceback

def one(a, b):
    return two(b, a)


def two(x, y):
    traceback.print_stack()
    print(traceback.format_stack())


def three():
    print(one(1, 1))


three()
