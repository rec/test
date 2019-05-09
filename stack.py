import traceback

def foo():
    bar(1)


def bar(x):
    baz(x, 12)


def baz(x, y):
    frame = traceback.extract_stack()[-2]
    print(frame.filename)
    print(dir(frame))


if __name__ == '__main__':
    foo()
